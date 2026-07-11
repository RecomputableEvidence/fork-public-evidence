from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

COMMON_PATH = Path("tools/csh_receiver_github_models_v0_1.py")
TOOLS_DIR = Path("tools").resolve()


def load_common():
    spec = importlib.util.spec_from_file_location("csh_receiver_hosted", COMMON_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def receiver_spec(module, receiver: str = "a"):
    if receiver == "a":
        return module.ReceiverSpec(
            receiver_class_id="llm_receiver_a",
            provider="Meta",
            serving_platform="GitHub Models",
            displayed_model_name="Llama 4 Scout 17B 16E Instruct",
            requested_model_id="meta/Llama-4-Scout-17B-16E-Instruct",
            expected_returned_model="Llama-4-Scout-17B-16E-Instruct",
        )
    return module.ReceiverSpec(
        receiver_class_id="llm_receiver_b",
        provider="DeepSeek",
        serving_platform="GitHub Models",
        displayed_model_name="DeepSeek-V3-0324",
        requested_model_id="deepseek/DeepSeek-V3-0324",
        expected_returned_model="DeepSeek-V3-0324",
    )


def write_inputs(tmp_path: Path, *, frozen: bool = True):
    system = tmp_path / "system.txt"
    prompt = tmp_path / "prompt.txt"
    freeze = tmp_path / "freeze.json"
    system.write_text("Follow the frozen receiver instruction.\n", encoding="utf-8")
    prompt.write_text("TEST_ONLY_PROMPT\n", encoding="utf-8")
    freeze.write_text(
        json.dumps(
            {
                "freeze_status": "frozen" if frozen else "draft_unfrozen",
                "baseline_execution_permitted": frozen,
                "subject_commit": "a" * 40,
            }
        ),
        encoding="utf-8",
    )
    return system, prompt, freeze


def output_paths(tmp_path: Path):
    return (
        tmp_path / "request.json",
        tmp_path / "response.json",
        tmp_path / "metadata.json",
    )


def provider_response(model: str, content: str = "TEST_RESPONSE") -> bytes:
    return json.dumps(
        {
            "choices": [{"message": {"content": content, "role": "assistant"}}],
            "model": model,
            "usage": {
                "completion_tokens": 2,
                "prompt_tokens": 4,
                "total_tokens": 6,
            },
        },
        separators=(",", ":"),
    ).encode("utf-8")


def test_request_payload_is_fixed_and_contains_no_optional_capability_fields():
    module = load_common()
    payload = module.build_request_payload(
        receiver_spec(module),
        system_prompt="SYSTEM",
        prompt="PROMPT",
    )
    assert payload == {
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "messages": [
            {"content": "SYSTEM", "role": "system"},
            {"content": "PROMPT", "role": "user"},
        ],
        "model": "meta/Llama-4-Scout-17B-16E-Instruct",
        "presence_penalty": 0,
        "stream": False,
        "temperature": 0,
        "top_p": 1,
    }
    for prohibited in ("tools", "seed", "response_format"):
        assert prohibited not in payload


def test_unfrozen_gate_blocks_before_transport_and_writes_nothing(tmp_path: Path):
    module = load_common()
    system, prompt, freeze = write_inputs(tmp_path, frozen=False)
    request_out, response_out, metadata_out = output_paths(tmp_path)
    calls = []

    def transport(*args):
        calls.append(args)
        raise AssertionError("transport must not be called")

    with pytest.raises(module.AdapterInputError, match="freeze_status"):
        module.execute_receiver(
            receiver_spec(module),
            system_prompt_path=system,
            prompt_path=prompt,
            request_output_path=request_out,
            response_output_path=response_out,
            metadata_output_path=metadata_out,
            freeze_file_path=freeze,
            token="TEST_SECRET",
            transport=transport,
        )
    assert calls == []
    assert not request_out.exists()
    assert not response_out.exists()
    assert not metadata_out.exists()


@pytest.mark.parametrize(
    ("which", "returned_model"),
    [
        ("a", "Llama-4-Scout-17B-16E-Instruct"),
        ("b", "DeepSeek-V3-0324"),
    ],
)
def test_success_preserves_exact_bytes_and_never_persists_secret(
    tmp_path: Path, which: str, returned_model: str
):
    module = load_common()
    system, prompt, freeze = write_inputs(tmp_path)
    request_out, response_out, metadata_out = output_paths(tmp_path)
    raw_response = provider_response(returned_model)
    calls = []

    def transport(endpoint, body, token, timeout):
        calls.append((endpoint, body, token, timeout))
        return module.TransportResponse(
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Request-Id": "TEST_REQUEST_ID",
            },
            body=raw_response,
        )

    secret = "TEST_SECRET_MUST_NOT_BE_PERSISTED"
    code = module.execute_receiver(
        receiver_spec(module, which),
        system_prompt_path=system,
        prompt_path=prompt,
        request_output_path=request_out,
        response_output_path=response_out,
        metadata_output_path=metadata_out,
        freeze_file_path=freeze,
        token=secret,
        transport=transport,
    )
    assert code == 0
    assert len(calls) == 1
    assert response_out.read_bytes() == raw_response

    request_payload = json.loads(request_out.read_text(encoding="utf-8"))
    assert request_payload["model"] == receiver_spec(
        module, which
    ).requested_model_id

    metadata = json.loads(metadata_out.read_text(encoding="utf-8"))
    assert metadata["execution_status"] == "success"
    assert metadata["retry_count"] == 0
    assert metadata["normalization_performed"] is False
    assert metadata["classification_performed"] is False
    assert metadata["returned_model"] == returned_model
    assert secret.encode("utf-8") not in request_out.read_bytes()
    assert secret.encode("utf-8") not in response_out.read_bytes()
    assert secret.encode("utf-8") not in metadata_out.read_bytes()


def test_http_failure_is_preserved_once_without_retry(tmp_path: Path):
    module = load_common()
    system, prompt, freeze = write_inputs(tmp_path)
    request_out, response_out, metadata_out = output_paths(tmp_path)
    calls = []
    raw_error = b'{"message":"rate limited"}'

    def transport(endpoint, body, token, timeout):
        calls.append((endpoint, body, token, timeout))
        return module.TransportResponse(
            status_code=429,
            headers={"Content-Type": "application/json"},
            body=raw_error,
        )

    code = module.execute_receiver(
        receiver_spec(module),
        system_prompt_path=system,
        prompt_path=prompt,
        request_output_path=request_out,
        response_output_path=response_out,
        metadata_output_path=metadata_out,
        freeze_file_path=freeze,
        token="TEST_SECRET",
        transport=transport,
    )
    assert code == 3
    assert len(calls) == 1
    assert response_out.read_bytes() == raw_error
    metadata = json.loads(metadata_out.read_text(encoding="utf-8"))
    assert metadata["execution_status"] == "http_error"
    assert metadata["http_status"] == 429
    assert metadata["retry_count"] == 0


def test_returned_model_mismatch_is_terminal_and_preserved(tmp_path: Path):
    module = load_common()
    system, prompt, freeze = write_inputs(tmp_path)
    request_out, response_out, metadata_out = output_paths(tmp_path)
    raw_response = provider_response("DIFFERENT_MODEL")

    def transport(endpoint, body, token, timeout):
        return module.TransportResponse(200, {}, raw_response)

    code = module.execute_receiver(
        receiver_spec(module),
        system_prompt_path=system,
        prompt_path=prompt,
        request_output_path=request_out,
        response_output_path=response_out,
        metadata_output_path=metadata_out,
        freeze_file_path=freeze,
        token="TEST_SECRET",
        transport=transport,
    )
    assert code == 4
    assert response_out.read_bytes() == raw_response
    metadata = json.loads(metadata_out.read_text(encoding="utf-8"))
    assert metadata["execution_status"] == "returned_model_mismatch"
    assert metadata["returned_model"] == "DIFFERENT_MODEL"


def test_existing_artifact_blocks_before_transport(tmp_path: Path):
    module = load_common()
    system, prompt, freeze = write_inputs(tmp_path)
    request_out, response_out, metadata_out = output_paths(tmp_path)
    response_out.write_text("existing", encoding="utf-8")
    calls = []

    def transport(*args):
        calls.append(args)
        raise AssertionError("transport must not be called")

    with pytest.raises(module.AdapterInputError, match="overwrite"):
        module.execute_receiver(
            receiver_spec(module),
            system_prompt_path=system,
            prompt_path=prompt,
            request_output_path=request_out,
            response_output_path=response_out,
            metadata_output_path=metadata_out,
            freeze_file_path=freeze,
            token="TEST_SECRET",
            transport=transport,
        )
    assert calls == []
    assert response_out.read_text(encoding="utf-8") == "existing"


def test_wrapper_model_bindings_are_explicit():
    source_a = Path("tools/csh_receiver_a_llama_v0_1.py").read_text(
        encoding="utf-8"
    )
    source_b = Path("tools/csh_receiver_b_deepseek_v0_1.py").read_text(
        encoding="utf-8"
    )
    assert 'requested_model_id="meta/Llama-4-Scout-17B-16E-Instruct"' in source_a
    assert 'expected_returned_model="Llama-4-Scout-17B-16E-Instruct"' in source_a
    assert 'requested_model_id="deepseek/DeepSeek-V3-0324"' in source_b
    assert 'expected_returned_model="DeepSeek-V3-0324"' in source_b
    assert "Auto" not in source_a
    assert "Auto" not in source_b


def test_adapter_has_no_retry_library_or_response_classification():
    source = COMMON_PATH.read_text(encoding="utf-8")
    for prohibited in (
        "tenacity",
        "Retry(",
        "classify_unsupported_inheritance",
        "time.sleep",
    ):
        assert prohibited not in source
