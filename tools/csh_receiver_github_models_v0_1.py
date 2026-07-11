#!/usr/bin/env python3
"""Bounded GitHub Models receiver adapter for CSH v0.1.

The adapter performs exactly one non-streaming request after the canonical
corpus-freeze gate permits baseline execution. It preserves exact request and
response bytes, emits execution metadata, never retries, and performs no
classification or response repair.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ENDPOINT = "https://models.github.ai/inference/chat/completions"
API_VERSION = "2022-11-28"
TOKEN_ENVIRONMENT_VARIABLE = "GITHUB_TOKEN"
DEFAULT_FREEZE_FILE = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/"
    "CORPUS_FREEZE_v0_1.json"
)
ADAPTER_VERSION = "0.1.0"
METADATA_SCHEMA_VERSION = "v0.1"


class AdapterInputError(ValueError):
    """Raised when a receiver execution request violates the frozen protocol."""


@dataclass(frozen=True)
class ReceiverSpec:
    receiver_class_id: str
    provider: str
    serving_platform: str
    displayed_model_name: str
    requested_model_id: str
    expected_returned_model: str


@dataclass(frozen=True)
class TransportResponse:
    status_code: int
    headers: Mapping[str, str]
    body: bytes


Transport = Callable[[str, bytes, str, int], TransportResponse]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def read_utf8_text(path: Path, label: str) -> tuple[bytes, str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise AdapterInputError(f"unable to read {label}: {exc}") from exc
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AdapterInputError(f"{label} must be UTF-8 without BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AdapterInputError(f"{label} must be valid UTF-8: {exc}") from exc
    if "\x00" in text:
        raise AdapterInputError(f"{label} must not contain NUL characters")
    if not text.strip():
        raise AdapterInputError(f"{label} must not be empty")
    return raw, text


def read_freeze_gate(path: Path) -> Mapping[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterInputError(f"unable to read freeze gate: {exc}") from exc
    if not isinstance(value, dict):
        raise AdapterInputError("freeze gate must be a JSON object")
    if value.get("freeze_status") != "frozen":
        raise AdapterInputError("baseline execution blocked: freeze_status is not 'frozen'")
    if value.get("baseline_execution_permitted") is not True:
        raise AdapterInputError(
            "baseline execution blocked: baseline_execution_permitted is not true"
        )
    return value


def build_request_payload(
    spec: ReceiverSpec,
    *,
    system_prompt: str,
    prompt: str,
) -> dict[str, Any]:
    return {
        "frequency_penalty": 0,
        "max_tokens": 2048,
        "messages": [
            {"content": system_prompt, "role": "system"},
            {"content": prompt, "role": "user"},
        ],
        "model": spec.requested_model_id,
        "presence_penalty": 0,
        "stream": False,
        "temperature": 0,
        "top_p": 1,
    }


def _write_new_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(data)
    except FileExistsError as exc:
        raise AdapterInputError(f"refusing to overwrite existing artifact: {path}") from exc


def _assert_new_distinct_paths(paths: Sequence[Path], protected: Sequence[Path]) -> None:
    resolved = [path.resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        raise AdapterInputError("request, response, and metadata paths must be distinct")
    protected_resolved = {path.resolve() for path in protected}
    for path, resolved_path in zip(paths, resolved):
        if resolved_path in protected_resolved:
            raise AdapterInputError(f"output path must not overwrite an input: {path}")
        if path.exists():
            raise AdapterInputError(f"refusing to overwrite existing artifact: {path}")


def _default_transport(
    endpoint: str,
    request_body: bytes,
    token: str,
    timeout_seconds: int,
) -> TransportResponse:
    request = urllib.request.Request(
        endpoint,
        data=request_body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return TransportResponse(
                status_code=int(response.status),
                headers={str(k): str(v) for k, v in response.headers.items()},
                body=response.read(),
            )
    except urllib.error.HTTPError as exc:
        return TransportResponse(
            status_code=int(exc.code),
            headers={str(k): str(v) for k, v in exc.headers.items()},
            body=exc.read(),
        )


def _selected_response_headers(headers: Mapping[str, str]) -> dict[str, str]:
    allowed = {
        "content-type",
        "date",
        "x-github-request-id",
        "x-ms-request-id",
        "x-ratelimit-limit",
        "x-ratelimit-remaining",
        "x-ratelimit-reset",
    }
    result: dict[str, str] = {}
    for key, value in headers.items():
        lowered = key.lower()
        if lowered in allowed:
            result[lowered] = value
    return dict(sorted(result.items()))


def _parse_provider_response(raw: bytes) -> Mapping[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdapterInputError(f"provider response is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AdapterInputError("provider response must be a JSON object")
    return value


def _extract_response_text(value: Mapping[str, Any]) -> str:
    choices = value.get("choices")
    if not isinstance(choices, list) or not choices:
        raise AdapterInputError("provider response does not contain choices[0]")
    first = choices[0]
    if not isinstance(first, dict):
        raise AdapterInputError("provider response choices[0] must be an object")
    message = first.get("message")
    if not isinstance(message, dict):
        raise AdapterInputError("provider response choices[0].message must be an object")
    content = message.get("content")
    if not isinstance(content, str):
        raise AdapterInputError(
            "provider response choices[0].message.content must be a string"
        )
    return content


def execute_receiver(
    spec: ReceiverSpec,
    *,
    system_prompt_path: Path,
    prompt_path: Path,
    request_output_path: Path,
    response_output_path: Path,
    metadata_output_path: Path,
    freeze_file_path: Path = DEFAULT_FREEZE_FILE,
    timeout_seconds: int = 120,
    token: str | None = None,
    transport: Transport = _default_transport,
    entrypoint_path: Path | None = None,
) -> int:
    if timeout_seconds < 1 or timeout_seconds > 600:
        raise AdapterInputError("timeout_seconds must be between 1 and 600")

    freeze = read_freeze_gate(freeze_file_path)
    system_raw, system_text = read_utf8_text(system_prompt_path, "system prompt")
    prompt_raw, prompt_text = read_utf8_text(prompt_path, "receiver prompt")

    protected = [system_prompt_path, prompt_path, freeze_file_path, Path(__file__)]
    if entrypoint_path is not None:
        protected.append(entrypoint_path)
    _assert_new_distinct_paths(
        [request_output_path, response_output_path, metadata_output_path],
        protected,
    )

    effective_token = token if token is not None else os.environ.get(
        TOKEN_ENVIRONMENT_VARIABLE
    )
    if not effective_token or not effective_token.strip():
        raise AdapterInputError(
            f"{TOKEN_ENVIRONMENT_VARIABLE} is not set for hosted receiver execution"
        )

    request_payload = build_request_payload(
        spec,
        system_prompt=system_text,
        prompt=prompt_text,
    )
    request_body = canonical_json_bytes(request_payload)
    _write_new_bytes(request_output_path, request_body)

    started_at = utc_now()
    response: TransportResponse | None = None
    transport_error: Exception | None = None
    try:
        response = transport(
            ENDPOINT,
            request_body,
            effective_token,
            timeout_seconds,
        )
    except Exception as exc:  # preserved as one terminal attempt; never retried
        transport_error = exc
    completed_at = utc_now()

    common_metadata: dict[str, Any] = {
        "adapter_source_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "adapter_version": ADAPTER_VERSION,
        "authentication": {
            "environment_variable": TOKEN_ENVIRONMENT_VARIABLE,
            "secret_persisted": False,
        },
        "classification_performed": False,
        "completed_at_utc": completed_at,
        "endpoint": ENDPOINT,
        "entrypoint_source_sha256": (
            sha256_bytes(entrypoint_path.read_bytes())
            if entrypoint_path is not None else None
        ),
        "freeze_gate": {
            "baseline_execution_permitted": freeze.get(
                "baseline_execution_permitted"
            ),
            "freeze_file": str(freeze_file_path),
            "freeze_status": freeze.get("freeze_status"),
            "subject_commit": freeze.get("subject_commit"),
        },
        "metadata_schema_version": METADATA_SCHEMA_VERSION,
        "normalization_performed": False,
        "parameters": {
            "frequency_penalty": 0,
            "max_tokens": 2048,
            "presence_penalty": 0,
            "stream": False,
            "temperature": 0,
            "top_p": 1,
        },
        "prompt": {
            "byte_length": len(prompt_raw),
            "path": str(prompt_path),
            "sha256": sha256_bytes(prompt_raw),
        },
        "provider": spec.provider,
        "request": {
            "body_byte_length": len(request_body),
            "body_path": str(request_output_path),
            "body_sha256": sha256_bytes(request_body),
            "headers_preserved_without_secret": {
                "accept": "application/vnd.github+json",
                "content-type": "application/json",
                "x-github-api-version": API_VERSION,
            },
        },
        "requested_model": spec.requested_model_id,
        "receiver_class_id": spec.receiver_class_id,
        "response": {
            "body_path": str(response_output_path),
        },
        "retry_count": 0,
        "serving_platform": spec.serving_platform,
        "silent_retries_permitted": False,
        "started_at_utc": started_at,
        "system_prompt": {
            "byte_length": len(system_raw),
            "path": str(system_prompt_path),
            "sha256": sha256_bytes(system_raw),
        },
        "tools_enabled": False,
        "retrieval_enabled": False,
        "conversation_history": "NONE",
    }

    if transport_error is not None:
        common_metadata["execution_status"] = "transport_error"
        common_metadata["transport_error"] = {
            "message": str(transport_error),
            "type": type(transport_error).__name__,
        }
        common_metadata["response"]["body_written"] = False
        _write_new_bytes(metadata_output_path, pretty_json_bytes(common_metadata))
        return 5

    assert response is not None
    _write_new_bytes(response_output_path, response.body)
    common_metadata["http_status"] = response.status_code
    common_metadata["response"].update(
        {
            "body_byte_length": len(response.body),
            "body_sha256": sha256_bytes(response.body),
            "body_written": True,
            "selected_headers": _selected_response_headers(response.headers),
        }
    )

    if response.status_code < 200 or response.status_code >= 300:
        common_metadata["execution_status"] = "http_error"
        _write_new_bytes(metadata_output_path, pretty_json_bytes(common_metadata))
        return 3

    try:
        parsed = _parse_provider_response(response.body)
        returned_model = parsed.get("model")
        if not isinstance(returned_model, str) or not returned_model:
            raise AdapterInputError("provider response model must be a non-empty string")
        response_text = _extract_response_text(parsed)
    except AdapterInputError as exc:
        common_metadata["execution_status"] = "invalid_provider_response"
        common_metadata["validation_error"] = str(exc)
        _write_new_bytes(metadata_output_path, pretty_json_bytes(common_metadata))
        return 4

    common_metadata["returned_model"] = returned_model
    common_metadata["response"]["text_byte_length"] = len(
        response_text.encode("utf-8")
    )
    common_metadata["response"]["text_sha256"] = sha256_bytes(
        response_text.encode("utf-8")
    )
    common_metadata["usage"] = parsed.get("usage")

    if returned_model != spec.expected_returned_model:
        common_metadata["execution_status"] = "returned_model_mismatch"
        common_metadata["expected_returned_model"] = spec.expected_returned_model
        _write_new_bytes(metadata_output_path, pretty_json_bytes(common_metadata))
        return 4

    common_metadata["execution_status"] = "success"
    _write_new_bytes(metadata_output_path, pretty_json_bytes(common_metadata))
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-prompt", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--request-output", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    parser.add_argument("--freeze-file", type=Path, default=DEFAULT_FREEZE_FILE)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    return parser.parse_args(argv)


def run_cli(
    spec: ReceiverSpec,
    argv: Sequence[str] | None = None,
    *,
    entrypoint_path: Path | None = None,
) -> int:
    args = parse_args(argv)
    request_output = args.request_output
    if request_output is None:
        request_output = args.metadata_output.with_name(
            args.metadata_output.name + ".request.json"
        )
    try:
        code = execute_receiver(
            spec,
            system_prompt_path=args.system_prompt,
            prompt_path=args.prompt,
            request_output_path=request_output,
            response_output_path=args.output,
            metadata_output_path=args.metadata_output,
            freeze_file_path=args.freeze_file,
            timeout_seconds=args.timeout_seconds,
            entrypoint_path=entrypoint_path,
        )
    except (AdapterInputError, OSError) as exc:
        print(f"CSH_HOSTED_RECEIVER_ERROR: {exc}", file=sys.stderr)
        return 2

    if code == 0:
        print("CSH_HOSTED_RECEIVER_PASS")
    else:
        print(f"CSH_HOSTED_RECEIVER_TERMINAL_FAILURE: {code}", file=sys.stderr)
    print(f"REQUEST_OUTPUT: {request_output}")
    print(f"RESPONSE_OUTPUT: {args.output}")
    print(f"METADATA_OUTPUT: {args.metadata_output}")
    return code
