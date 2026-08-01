from __future__ import annotations

import copy
import importlib.util
import io
import json
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/run_csh_provider_validation_v0_1_2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("csh_provider_validation", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = load_module()


def valid_call(spec: dict) -> dict:
    return {
        **spec,
        "passed": True,
        "http_status": 200,
        "quota_headers": {"x-ratelimit-remaining": "99"},
        "quota_evidence": {
            "available": True,
            "basis": "RATE_LIMIT_REMAINING_HEADER",
            "remaining_not_quantified": False,
        },
        "request_sha256": MODULE.sha256_bytes(
            MODULE.canonical_json_bytes(
                MODULE.build_probe_request(spec["requested_model"], spec["max_tokens"])
            )
        ),
        "response_body_sha256": "b" * 64,
        "response_body_written": False,
        "returned_model": spec["expected_returned_model"],
        "response_text_sha256": "c" * 64,
        "usage": {"total_tokens": 4},
    }


def valid_receipt(path: Path) -> dict:
    calls = [valid_call(spec) for spec in MODULE.MODEL_SPECS]
    return MODULE.build_receipt(
        calls,
        output=path,
        workflow_run_id="123",
        subject_commit="d" * 40,
        repository="RecomputableEvidence/fork-public-evidence",
    )


def valid_retry_receipt(path: Path) -> dict:
    spec = MODULE.MODEL_SPECS[0]
    return MODULE.build_receipt(
        [valid_call(spec)],
        output=path,
        workflow_run_id="124",
        subject_commit="e" * 40,
        repository="RecomputableEvidence/fork-public-evidence",
        expected_specs=(spec,),
        validation_mode=MODULE.UPPERCASE_RETRY_MODE,
        request_sha256=MODULE.UPPERCASE_REQUEST_SHA256,
    )


def test_probe_is_synthetic_and_not_pair_001() -> None:
    deepseek = MODULE.MODEL_SPECS[0]
    meta = MODULE.MODEL_SPECS[1]
    payload = MODULE.build_probe_request(deepseek["requested_model"], deepseek["max_tokens"])
    rendered = MODULE.canonical_json_bytes(payload)
    assert b"CSH_PROVIDER_VALIDATION_OK" in rendered
    assert b"Pair-001" not in rendered
    assert b"cross_system_claim_handoff" not in rendered
    assert payload["model"] == "deepseek/DeepSeek-V3-0324"
    assert payload["max_tokens"] == 2048
    assert payload["stream"] is False
    assert MODULE.sha256_bytes(rendered) == MODULE.UPPERCASE_REQUEST_SHA256
    meta_payload = MODULE.build_probe_request(meta["requested_model"], meta["max_tokens"])
    assert meta_payload["max_tokens"] == 32


def test_valid_receipt_verifies(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    assert MODULE.verify_receipt(path)["status"] == "PASS"


def test_valid_one_call_retry_receipt_verifies(tmp_path: Path) -> None:
    path = tmp_path / "retry-receipt.json"
    receipt = valid_retry_receipt(path)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    verified = MODULE.verify_receipt(path)
    assert verified["status"] == "PASS"
    assert verified["validation_mode"] == MODULE.UPPERCASE_RETRY_MODE
    assert verified["provider_validation_calls_performed"] == 1
    assert len(verified["calls"]) == 1
    assert verified["calls"][0]["requested_model"] == "deepseek/DeepSeek-V3-0324"
    assert verified["pair_001_calls_performed"] == 0


def test_current_request_selects_one_uppercase_call() -> None:
    request = MODULE.strict_json_file(ROOT / MODULE.REQUEST_PATH)
    mode, specs = MODULE.select_request_mode(
        ROOT,
        request,
        now=datetime(2026, 8, 1, tzinfo=timezone.utc),
    )
    assert mode == MODULE.UPPERCASE_RETRY_MODE
    assert specs == (MODULE.MODEL_SPECS[0],)
    assert specs[0]["requested_model"] == "deepseek/DeepSeek-V3-0324"
    assert MODULE.sha256_bytes(
        MODULE.canonical_json_bytes(
            MODULE.build_probe_request(specs[0]["requested_model"], specs[0]["max_tokens"])
        )
    ) == MODULE.UPPERCASE_REQUEST_SHA256


def test_retry_request_fails_closed_when_call_budget_expands() -> None:
    request = MODULE.strict_json_file(ROOT / MODULE.REQUEST_PATH)
    changed = copy.deepcopy(request)
    changed["retry_authorization"]["maximum_provider_calls"] = 2
    with pytest.raises(ValueError, match="semantics mismatch"):
        MODULE.select_request_mode(
            ROOT,
            changed,
            now=datetime(2026, 8, 1, tzinfo=timezone.utc),
        )


def test_retry_request_fails_closed_when_successor_digest_is_forged() -> None:
    request = MODULE.strict_json_file(ROOT / MODULE.REQUEST_PATH)
    changed = copy.deepcopy(request)
    changed["retry_authorization"]["current_line_successor"]["sha256"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        MODULE.select_request_mode(
            ROOT,
            changed,
            now=datetime(2026, 8, 1, tzinfo=timezone.utc),
        )


def test_pair_001_call_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["pair_001_calls_performed"] = 1
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Pair-001"):
        MODULE.verify_receipt(path)


def test_secret_persistence_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["authentication"]["secret_persisted"] = True
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="secret persistence"):
        MODULE.verify_receipt(path)


def test_missing_quota_evidence_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["calls"][0]["quota_headers"] = {}
    receipt["calls"][0].pop("quota_evidence")
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="quota evidence"):
        MODULE.verify_receipt(path)


def test_sanitized_error_capture_retains_only_allowlisted_codes() -> None:
    raw = (
        b'{"error":{"code":"InternalServerError","type":"server_error",'
        b'"message":"credential-like secret must not persist"},"request_id":"sensitive"}'
    )
    evidence = MODULE.sanitized_error_code_evidence(raw)
    assert evidence == {
        "capture_schema": "SANITIZED_PROVIDER_ERROR_CODE_v0_1",
        "body_parsed_as_strict_json": True,
        "error_code": "InternalServerError",
        "error_type": "server_error",
        "message_persisted": False,
        "raw_body_persisted": False,
    }
    rendered = json.dumps(evidence)
    assert "credential-like" not in rendered
    assert "request_id" not in rendered


def test_invalid_or_duplicate_key_error_body_captures_no_values() -> None:
    evidence = MODULE.sanitized_error_code_evidence(
        b'{"error":{"code":"first","code":"second","message":"do not persist"}}'
    )
    assert evidence["body_parsed_as_strict_json"] is False
    assert evidence["error_code"] is None
    assert evidence["error_type"] is None
    assert evidence["message_persisted"] is False
    assert evidence["raw_body_persisted"] is False


def test_http_error_receipt_path_includes_sanitized_capture(monkeypatch: pytest.MonkeyPatch) -> None:
    raw = b'{"error":{"code":"InternalServerError","type":"server_error","message":"omit me"}}'

    def fail_request(*_args, **_kwargs):
        raise urllib.error.HTTPError(
            MODULE.ENDPOINT,
            500,
            "Internal Server Error",
            {},
            io.BytesIO(raw),
        )

    monkeypatch.setattr(MODULE.urllib.request, "urlopen", fail_request)
    call = MODULE.invoke_probe(MODULE.MODEL_SPECS[0], "not-persisted", 1)
    assert call["passed"] is False
    assert call["http_status"] == 500
    assert call["sanitized_error"]["error_code"] == "InternalServerError"
    assert call["sanitized_error"]["error_type"] == "server_error"
    assert "omit me" not in json.dumps(call)
