#!/usr/bin/env python3
"""Run or verify a bounded, non-experiment GitHub Models provider preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


ENDPOINT = "https://models.github.ai/inference/chat/completions"
API_VERSION = "2022-11-28"
RECEIPT_ID = "CSH_PROVIDER_VALIDATION_RECEIPT_v0_1_2"
CLASSIFICATION = "PROVIDER_VALIDATION_ONLY_EXCLUDED_FROM_CSH_BASELINE"
MODEL_SPECS = (
    {
        "receiver_class_id": "llm_receiver_b",
        "provider": "DeepSeek",
        "requested_model": "deepseek/DeepSeek-V3-0324",
        "expected_returned_model": "DeepSeek-V3-0324",
    },
    {
        "receiver_class_id": "llm_receiver_a",
        "provider": "Meta",
        "requested_model": "meta/Llama-4-Scout-17B-16E-Instruct",
        "expected_returned_model": "Llama-4-Scout-17B-16E-Instruct",
    },
)
SYSTEM_PROMPT = (
    "This is a provider-connectivity validation probe, not an experiment run. "
    "Do not use tools. Return only the requested literal."
)
USER_PROMPT = "Return exactly: CSH_PROVIDER_VALIDATION_OK"


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def pretty_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def strict_json_bytes(raw: bytes) -> Any:
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite value prohibited: {value}")
        ),
    )


def build_probe_request(requested_model: str) -> dict[str, Any]:
    return {
        "frequency_penalty": 0,
        "max_tokens": 32,
        "messages": [
            {"content": SYSTEM_PROMPT, "role": "system"},
            {"content": USER_PROMPT, "role": "user"},
        ],
        "model": requested_model,
        "presence_penalty": 0,
        "stream": False,
        "temperature": 0,
        "top_p": 1,
    }


def selected_quota_headers(headers: Mapping[str, str]) -> dict[str, str]:
    selected: dict[str, str] = {}
    for key, value in headers.items():
        lowered = key.lower()
        if lowered.startswith("x-ratelimit-") or lowered == "retry-after":
            selected[lowered] = str(value)
    return dict(sorted(selected.items()))


def quota_is_observed(headers: Mapping[str, str]) -> bool:
    remaining = [
        value
        for key, value in headers.items()
        if "remaining" in key.lower()
    ]
    if not remaining:
        return False
    try:
        return all(float(value) >= 0 for value in remaining)
    except ValueError:
        return False


def quota_evidence(status_code: int | None, headers: Mapping[str, str]) -> dict[str, Any]:
    if quota_is_observed(headers):
        return {
            "available": True,
            "basis": "RATE_LIMIT_REMAINING_HEADER",
            "remaining_not_quantified": False,
        }
    if status_code is not None and 200 <= status_code < 300:
        return {
            "available": True,
            "basis": "SUCCESSFUL_BOUNDED_PROVIDER_REQUEST",
            "remaining_not_quantified": True,
        }
    return {
        "available": False,
        "basis": "NO_SUCCESSFUL_PROVIDER_REQUEST",
        "remaining_not_quantified": True,
    }


def response_text(payload: Mapping[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise ValueError("provider response does not contain choices[0]")
    first = choices[0]
    if not isinstance(first, dict):
        raise ValueError("provider response choices[0] is not an object")
    message = first.get("message")
    if not isinstance(message, dict) or not isinstance(message.get("content"), str):
        raise ValueError("provider response does not contain string message content")
    return message["content"]


def invoke_probe(spec: Mapping[str, str], token: str, timeout_seconds: int) -> dict[str, Any]:
    request_body = canonical_json_bytes(build_probe_request(spec["requested_model"]))
    request = urllib.request.Request(
        ENDPOINT,
        data=request_body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": API_VERSION,
        },
    )
    status_code: int | None = None
    response_headers: dict[str, str] = {}
    response_body = b""
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            status_code = int(response.status)
            response_headers = {str(k): str(v) for k, v in response.headers.items()}
            response_body = response.read()
    except urllib.error.HTTPError as exc:
        status_code = int(exc.code)
        response_headers = {str(k): str(v) for k, v in exc.headers.items()}
        response_body = exc.read()
    except Exception as exc:
        return {
            **spec,
            "passed": False,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
            "request_sha256": sha256_bytes(request_body),
            "response_body_written": False,
        }

    quota_headers = selected_quota_headers(response_headers)
    result: dict[str, Any] = {
        **spec,
        "http_status": status_code,
        "quota_headers": quota_headers,
        "request_sha256": sha256_bytes(request_body),
        "response_body_sha256": sha256_bytes(response_body),
        "response_body_written": False,
    }
    try:
        if status_code is None or not 200 <= status_code < 300:
            raise ValueError(f"provider returned HTTP {status_code}")
        payload = strict_json_bytes(response_body)
        if not isinstance(payload, dict):
            raise ValueError("provider response is not an object")
        returned_model = payload.get("model")
        if returned_model != spec["expected_returned_model"]:
            raise ValueError(
                "returned model mismatch: "
                f"expected={spec['expected_returned_model']!r}; observed={returned_model!r}"
            )
        content = response_text(payload)
        if "CSH_PROVIDER_VALIDATION_OK" not in content:
            raise ValueError("provider response omitted validation literal")
        result.update(
            {
                "passed": True,
                "quota_evidence": quota_evidence(status_code, quota_headers),
                "returned_model": returned_model,
                "response_text_sha256": sha256_bytes(content.encode("utf-8")),
                "usage": payload.get("usage"),
            }
        )
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        result.update(
            {
                "passed": False,
                "failure": {"type": type(exc).__name__, "message": str(exc)},
            }
        )
    return result


def build_receipt(
    calls: list[dict[str, Any]],
    *,
    output: Path,
    workflow_run_id: str,
    subject_commit: str,
    repository: str,
) -> dict[str, Any]:
    all_passed = len(calls) == len(MODEL_SPECS) and all(call.get("passed") for call in calls)
    quota_passed = all(
        isinstance(call.get("quota_evidence"), dict)
        and call["quota_evidence"].get("available") is True
        for call in calls
    )
    status = "PASS" if all_passed and quota_passed else "FAIL"
    return {
        "receipt_id": RECEIPT_ID,
        "schema_version": "v0.1.2",
        "classification": CLASSIFICATION,
        "status": status,
        "repository": repository,
        "subject_commit": subject_commit,
        "workflow_run_id": int(workflow_run_id),
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": ENDPOINT,
        "validations": {
            "provider_identity": "PASS" if all_passed else "FAIL",
            "credential_scope_models_read": "PASS" if all_passed else "FAIL",
            "quota_available_at_validation_time": "PASS" if quota_passed else "FAIL",
            "receipt_destination": "PASS",
        },
        "authentication": {
            "credential_source": "EPHEMERAL_GITHUB_ACTIONS_GITHUB_TOKEN",
            "required_permission": "models: read",
            "secret_persisted": False,
            "authorization_header_persisted": False,
        },
        "calls": calls,
        "provider_validation_calls_performed": len(calls),
        "pair_001_calls_performed": 0,
        "experiment_run_ids_created": [],
        "receipt_destination": {
            "path": output.as_posix(),
            "write_mode": "CREATE_NEW",
            "round_trip_verified": True,
        },
        "non_claims": [
            "Not a Pair-001 request or repetition",
            "Not included in the CSH baseline or hypothesis test",
            "No provider credential or authorization header persisted",
            "No experiment execution authority",
            "No security, compliance, safety, truth, or production-readiness certification",
        ],
    }


def write_new_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    rendered = pretty_json_bytes(receipt)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(rendered)
    if path.read_bytes() != rendered or strict_json_bytes(rendered) != receipt:
        raise RuntimeError("receipt destination round-trip verification failed")


def verify_receipt(path: Path) -> dict[str, Any]:
    receipt = strict_json_bytes(path.read_bytes())
    if not isinstance(receipt, dict):
        raise ValueError("receipt must be a JSON object")
    if receipt.get("receipt_id") != RECEIPT_ID:
        raise ValueError("receipt identity mismatch")
    if receipt.get("classification") != CLASSIFICATION:
        raise ValueError("receipt classification mismatch")
    if receipt.get("status") != "PASS":
        raise ValueError("provider validation did not pass")
    validations = receipt.get("validations")
    if not isinstance(validations, dict) or set(validations.values()) != {"PASS"}:
        raise ValueError("one or more provider validations did not pass")
    authentication = receipt.get("authentication")
    if not isinstance(authentication, dict):
        raise ValueError("authentication boundary missing")
    if authentication.get("required_permission") != "models: read":
        raise ValueError("credential permission binding mismatch")
    if authentication.get("secret_persisted") is not False:
        raise ValueError("secret persistence boundary violated")
    if authentication.get("authorization_header_persisted") is not False:
        raise ValueError("authorization-header persistence boundary violated")
    if receipt.get("provider_validation_calls_performed") != len(MODEL_SPECS):
        raise ValueError("provider validation call count mismatch")
    if receipt.get("pair_001_calls_performed") != 0:
        raise ValueError("Pair-001 call boundary violated")
    if receipt.get("experiment_run_ids_created") != []:
        raise ValueError("provider validation created experiment run identifiers")
    calls = receipt.get("calls")
    if not isinstance(calls, list) or len(calls) != len(MODEL_SPECS):
        raise ValueError("provider call evidence count mismatch")
    by_requested = {call.get("requested_model"): call for call in calls if isinstance(call, dict)}
    for spec in MODEL_SPECS:
        call = by_requested.get(spec["requested_model"])
        if not isinstance(call, dict) or call.get("passed") is not True:
            raise ValueError(f"provider evidence missing for {spec['requested_model']}")
        if call.get("returned_model") != spec["expected_returned_model"]:
            raise ValueError(f"returned model mismatch for {spec['requested_model']}")
        evidence = call.get("quota_evidence")
        if not isinstance(evidence, dict) or evidence.get("available") is not True:
            raise ValueError(f"quota evidence missing for {spec['requested_model']}")
    destination = receipt.get("receipt_destination")
    if not isinstance(destination, dict) or destination.get("round_trip_verified") is not True:
        raise ValueError("receipt destination was not round-trip verified")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--verify-receipt", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    if args.verify_receipt is not None:
        receipt = verify_receipt(args.verify_receipt)
        print(
            json.dumps(
                {
                    "receipt_id": receipt["receipt_id"],
                    "status": receipt["status"],
                    "pair_001_calls_performed": receipt["pair_001_calls_performed"],
                    "verified": True,
                },
                sort_keys=True,
            )
        )
        return 0

    assert args.output is not None
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token.strip():
        raise SystemExit("GITHUB_TOKEN is required for live provider validation")
    if args.timeout_seconds < 1 or args.timeout_seconds > 300:
        raise SystemExit("timeout must be between 1 and 300 seconds")
    calls = [invoke_probe(spec, token, args.timeout_seconds) for spec in MODEL_SPECS]
    receipt = build_receipt(
        calls,
        output=args.output,
        workflow_run_id=os.environ.get("GITHUB_RUN_ID", "0"),
        subject_commit=os.environ.get("GITHUB_HEAD_SHA", ""),
        repository=os.environ.get("GITHUB_REPOSITORY", ""),
    )
    write_new_receipt(args.output, receipt)
    print(
        json.dumps(
            {
                "receipt": args.output.as_posix(),
                "status": receipt["status"],
                "provider_validation_calls_performed": len(calls),
                "pair_001_calls_performed": 0,
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
