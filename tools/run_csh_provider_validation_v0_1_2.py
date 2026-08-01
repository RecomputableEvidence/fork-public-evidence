#!/usr/bin/env python3
"""Run or verify a bounded GitHub Models provider preflight.

The merged request controls the mode:

- REQUESTED: the original two-provider preflight.
- RETRY_REQUESTED: one byte-identical uppercase DeepSeek diagnostic only,
  bound to the admitted authorization anchor and its current-line successor.

Neither mode performs a Pair-001 experiment call.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence


ENDPOINT = "https://models.github.ai/inference/chat/completions"
API_VERSION = "2022-11-28"
RECEIPT_ID = "CSH_PROVIDER_VALIDATION_RECEIPT_v0_1_2"
CLASSIFICATION = "PROVIDER_VALIDATION_ONLY_EXCLUDED_FROM_CSH_BASELINE"
REQUEST_PATH = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/"
    "PROVIDER_VALIDATION_REQUEST_v0_1_2.json"
)
UPPERCASE_AUTHORIZATION_PATH = Path(
    "docs/sequence-surface/authorizations/"
    "PAIR_001_UPPERCASE_PROVIDER_VALIDATION_RETRY_AUTHORIZATION_v0_1.json"
)
UPPERCASE_SUCCESSOR_PATH = Path(
    "docs/sequence-surface/authorizations/"
    "PAIR_001_UPPERCASE_PROVIDER_VALIDATION_RETRY_CURRENT_LINE_SUCCESSOR_v0_1.json"
)
UPPERCASE_AUTHORIZATION_SHA256 = (
    "c57247c10d9366ba6f99859cc56f6676f2f111942f91dbb510bf818f5586bd94"
)
UPPERCASE_SUCCESSOR_SHA256 = (
    "220e3e6a318f90463589e9422873833db58d997a0ab7d1f464cdf126c12acf67"
)
UPPERCASE_AUTHORIZATION_MERGE_COMMIT = (
    "8996a65d02952945062fdf1f29b75aa128d2f9f2"
)
UPPERCASE_AUTHORIZATION_ID = (
    "PAIR_001_UPPERCASE_PROVIDER_VALIDATION_RETRY_AUTHORIZATION_2026_07_22"
)
UPPERCASE_REQUEST_SHA256 = (
    "d2c8aabbdda4f17509395aa8a55f607b2b0d52138a251e8da92bb8384a05bcef"
)
UPPERCASE_NOT_BEFORE = "2026-07-20T07:55:24.374494+00:00"
FULL_MODE = "FULL_PROVIDER_VALIDATION"
UPPERCASE_RETRY_MODE = "UPPERCASE_DEEPSEEK_ONLY"
MODEL_SPECS = (
    {
        "receiver_class_id": "llm_receiver_b",
        "provider": "DeepSeek",
        "requested_model": "deepseek/DeepSeek-V3-0324",
        "expected_returned_model": "DeepSeek-V3-0324",
        "max_tokens": 2048,
    },
    {
        "receiver_class_id": "llm_receiver_a",
        "provider": "Meta",
        "requested_model": "meta/Llama-4-Scout-17B-16E-Instruct",
        "expected_returned_model": "Llama-4-Scout-17B-16E-Instruct",
        "max_tokens": 32,
    },
)
SYSTEM_PROMPT = (
    "This is a provider-connectivity validation probe, not an experiment run. "
    "Do not use tools. Return only the requested literal."
)
USER_PROMPT = "Return exactly: CSH_PROVIDER_VALIDATION_OK"
SANITIZED_ERROR_CAPTURE_SCHEMA = "SANITIZED_PROVIDER_ERROR_CODE_v0_1"
SANITIZED_ERROR_TOKEN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def strict_json_file(path: Path) -> dict[str, Any]:
    value = strict_json_bytes(path.read_bytes())
    if not isinstance(value, dict):
        raise ValueError(f"{path.as_posix()} must contain a JSON object")
    return value


def parse_time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be a string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include an offset")
    return parsed


def safe_bound_path(root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError("bound path must be a non-empty string")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise ValueError("unsafe bound path")
    candidate = root.joinpath(*pure.parts)
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("bound path escapes repository") from exc
    if candidate.is_symlink() or not candidate.is_file():
        raise ValueError(f"bound file missing or not regular: {value}")
    return candidate


def load_bound_json(
    root: Path,
    reference: Any,
    *,
    expected_path: Path | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    if not isinstance(reference, dict) or set(reference) != {"path", "sha256"}:
        raise ValueError("bound reference must contain exactly path and sha256")
    relative = reference.get("path")
    digest = reference.get("sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise ValueError("bound reference digest must be lowercase SHA-256")
    if expected_path is not None and relative != expected_path.as_posix():
        raise ValueError("bound reference path mismatch")
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError("bound reference declared digest mismatch")
    path = safe_bound_path(root, relative)
    if sha256_file(path) != digest:
        raise ValueError("bound reference byte digest mismatch")
    return strict_json_file(path)


def sanitized_error_code_evidence(raw: bytes) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "capture_schema": SANITIZED_ERROR_CAPTURE_SCHEMA,
        "body_parsed_as_strict_json": False,
        "error_code": None,
        "error_type": None,
        "message_persisted": False,
        "raw_body_persisted": False,
    }
    try:
        payload = strict_json_bytes(raw)
    except (UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, ValueError):
        return evidence
    evidence["body_parsed_as_strict_json"] = True
    if not isinstance(payload, dict):
        return evidence
    error = payload.get("error")
    if not isinstance(error, dict):
        return evidence
    for source, destination in (("code", "error_code"), ("type", "error_type")):
        value = error.get(source)
        if isinstance(value, str) and SANITIZED_ERROR_TOKEN.fullmatch(value):
            evidence[destination] = value
    return evidence


def build_probe_request(requested_model: str, max_tokens: int) -> dict[str, Any]:
    return {
        "frequency_penalty": 0,
        "max_tokens": max_tokens,
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
    remaining = [value for key, value in headers.items() if "remaining" in key.lower()]
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


def invoke_probe(spec: Mapping[str, Any], token: str, timeout_seconds: int) -> dict[str, Any]:
    request_body = canonical_json_bytes(
        build_probe_request(spec["requested_model"], spec["max_tokens"])
    )
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
    if status_code is not None and not 200 <= status_code < 300:
        result["sanitized_error"] = sanitized_error_code_evidence(response_body)
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


def validate_uppercase_anchor(anchor: Mapping[str, Any]) -> None:
    expected_boundary = {
        "automatic_execution": False,
        "pair_001_execution_authorized": False,
        "readiness_promotion_authorized": False,
    }
    expected_transitions = [
        "FSS-PAIR001-T012",
        "FSS-PAIR001-T013",
        "FSS-PAIR001-T014",
        "FSS-PAIR001-T015",
        "FSS-PAIR001-T016",
    ]
    if not (
        anchor.get("schema_version") == "v0.1"
        and anchor.get("record_kind") == "explicit_external_authorization_anchor"
        and anchor.get("status") == "ACTIVE"
        and anchor.get("authorization_id") == UPPERCASE_AUTHORIZATION_ID
        and anchor.get("authorization_kind") == "ONE_TIME_UPPERCASE_PROVIDER_VALIDATION_RETRY"
        and anchor.get("subject")
        == {"experiment_id": "cross_system_claim_handoff_v0_1", "pair_id": "PAIR-001"}
        and anchor.get("authorized_transition_ids") == expected_transitions
        and anchor.get("request_sha256") == UPPERCASE_REQUEST_SHA256
        and anchor.get("maximum_provider_calls") == 1
        and anchor.get("not_before_utc") == UPPERCASE_NOT_BEFORE
        and anchor.get("execution_boundary") == expected_boundary
    ):
        raise ValueError("uppercase authorization anchor semantics mismatch")


def validate_current_line_successor(successor: Mapping[str, Any]) -> None:
    anchor_binding = successor.get("authorization_anchor")
    revalidation = successor.get("current_line_revalidation")
    request_transition = successor.get("request_transition")
    boundary = successor.get("execution_boundary")
    governed = successor.get("governed_line")
    if not all(isinstance(item, dict) for item in (anchor_binding, revalidation, request_transition, boundary, governed)):
        raise ValueError("current-line successor shape invalid")
    if not (
        successor.get("schema_version") == "v0.1"
        and successor.get("record_kind") == "current_line_authorization_successor"
        and successor.get("status")
        == "CURRENT_LINE_REVALIDATED_ONE_TIME_RETRY_ELIGIBLE_REQUEST_TRANSITION_PENDING"
        and successor.get("subject")
        == {"experiment_id": "cross_system_claim_handoff_v0_1", "pair_id": "PAIR-001"}
        and governed.get("branch") == "preservation/clean-continuance-v0.1"
        and governed.get("authorization_merge_commit") == UPPERCASE_AUTHORIZATION_MERGE_COMMIT
        and anchor_binding
        == {
            "path": UPPERCASE_AUTHORIZATION_PATH.as_posix(),
            "sha256": UPPERCASE_AUTHORIZATION_SHA256,
            "authorization_id": UPPERCASE_AUTHORIZATION_ID,
            "authorization_kind": "ONE_TIME_UPPERCASE_PROVIDER_VALIDATION_RETRY",
            "maximum_provider_calls": 1,
            "request_sha256": UPPERCASE_REQUEST_SHA256,
            "not_before_utc": UPPERCASE_NOT_BEFORE,
        }
        and revalidation.get("authorization_anchor_bytes_present") is True
        and revalidation.get("authorization_anchor_digest_matches") is True
        and revalidation.get("preregistered_request_bytes_unchanged") is True
        and revalidation.get("requested_model") == MODEL_SPECS[0]["requested_model"]
        and revalidation.get("max_tokens") == MODEL_SPECS[0]["max_tokens"]
        and revalidation.get("request_sha256") == UPPERCASE_REQUEST_SHA256
        and revalidation.get("time_gate_elapsed") is True
        and revalidation.get("automatic_attempts_permitted") == 0
        and revalidation.get("remaining_authorized_attempts") == 1
        and revalidation.get("outcome_mapping_unchanged") is True
        and revalidation.get("cause") == "UNRESOLVED"
        and request_transition.get("path") == REQUEST_PATH.as_posix()
        and request_transition.get("required_pre_execution_status") == "RETRY_REQUESTED"
        and request_transition.get("execution_occurs_only_after_reviewed_merge_to_governed_branch") is True
        and request_transition.get("trusted_workflow_path")
        == ".github/workflows/csh-provider-validation-v0-1-2.yml"
        and request_transition.get("one_call_mode") == UPPERCASE_RETRY_MODE
        and boundary.get("provider_validation_calls_authorized") == 1
        and boundary.get("provider_validation_calls_performed_by_this_record") == 0
        and boundary.get("pair_001_calls_performed") == 0
        and boundary.get("pair_001_execution_authorized") is False
        and boundary.get("readiness_promotion_authorized") is False
        and boundary.get("lowercase_diagnostic_authorized") is False
        and boundary.get("model_substitution_authorized") is False
        and boundary.get("request_byte_modification_authorized") is False
    ):
        raise ValueError("current-line successor semantics mismatch")


def validate_retry_request(root: Path, request: Mapping[str, Any], *, now: datetime | None = None) -> None:
    authorization = request.get("retry_authorization")
    execution = request.get("execution_boundary")
    disposition = request.get("disposition")
    outcome = request.get("outcome_contract")
    if not all(isinstance(item, dict) for item in (authorization, execution, disposition, outcome)):
        raise ValueError("retry request control objects missing")
    anchor = load_bound_json(
        root,
        authorization.get("authorization_anchor"),
        expected_path=UPPERCASE_AUTHORIZATION_PATH,
        expected_sha256=UPPERCASE_AUTHORIZATION_SHA256,
    )
    successor = load_bound_json(
        root,
        authorization.get("current_line_successor"),
        expected_path=UPPERCASE_SUCCESSOR_PATH,
        expected_sha256=UPPERCASE_SUCCESSOR_SHA256,
    )
    validate_uppercase_anchor(anchor)
    validate_current_line_successor(successor)
    probe_digest = sha256_bytes(
        canonical_json_bytes(build_probe_request(MODEL_SPECS[0]["requested_model"], MODEL_SPECS[0]["max_tokens"]))
    )
    observed_now = now or datetime.now(timezone.utc)
    not_before = parse_time(authorization.get("not_before_utc"))
    if observed_now < not_before:
        raise ValueError("uppercase retry time gate has not elapsed")
    if not (
        request.get("request_id") == "CSH_PROVIDER_VALIDATION_REQUEST_v0_1_2"
        and request.get("schema_version") == "v0.1.2"
        and request.get("classification") == CLASSIFICATION
        and request.get("status") == "RETRY_REQUESTED"
        and request.get("repository") == "RecomputableEvidence/fork-public-evidence"
        and request.get("trusted_lineage", {}).get("uppercase_retry_authorization_merge_commit")
        == UPPERCASE_AUTHORIZATION_MERGE_COMMIT
        and authorization.get("present") is True
        and authorization.get("authorization_merge_commit") == UPPERCASE_AUTHORIZATION_MERGE_COMMIT
        and authorization.get("authorization_id") == UPPERCASE_AUTHORIZATION_ID
        and authorization.get("requested_model") == MODEL_SPECS[0]["requested_model"]
        and authorization.get("expected_returned_model") == MODEL_SPECS[0]["expected_returned_model"]
        and authorization.get("max_tokens") == MODEL_SPECS[0]["max_tokens"]
        and authorization.get("request_sha256") == probe_digest == UPPERCASE_REQUEST_SHA256
        and authorization.get("maximum_provider_calls") == 1
        and authorization.get("not_before_utc") == UPPERCASE_NOT_BEFORE
        and authorization.get("automatic_execution") is False
        and authorization.get("one_call_mode") == UPPERCASE_RETRY_MODE
        and execution.get("additional_provider_validation_calls_requested") == 1
        and execution.get("maximum_additional_provider_validation_calls") == 1
        and execution.get("pair_001_calls_performed") == 0
        and execution.get("pair_001_execution_effect") == "NONE"
        and execution.get("readiness_effect") == "NONE"
        and execution.get("experiment_run_ids_created") == []
        and disposition.get("provider_validation_prerequisite_satisfied") is False
        and disposition.get("provider_execution_permitted") is False
        and disposition.get("pair_001_execution_permitted") is False
        and disposition.get("preregistered_request_bytes_changed") is False
        and outcome.get("success_transition") == "FSS-PAIR001-T014"
        and outcome.get("identical_failure_transition") == "FSS-PAIR001-T015"
        and outcome.get("different_outcome_transition") == "FSS-PAIR001-T016"
        and outcome.get("automatic_pair_001_execution") is False
        and outcome.get("automatic_readiness_promotion") is False
        and outcome.get("additional_uppercase_retries_after_identical_failure") == 0
    ):
        raise ValueError("retry request semantics mismatch")


def select_request_mode(
    root: Path,
    request: Mapping[str, Any],
    *,
    now: datetime | None = None,
) -> tuple[str, tuple[dict[str, Any], ...]]:
    status = request.get("status")
    if status == "REQUESTED":
        return FULL_MODE, MODEL_SPECS
    if status == "RETRY_REQUESTED":
        validate_retry_request(root, request, now=now)
        return UPPERCASE_RETRY_MODE, (MODEL_SPECS[0],)
    raise ValueError(f"request status does not authorize provider validation: {status!r}")


def build_receipt(
    calls: list[dict[str, Any]],
    *,
    output: Path,
    workflow_run_id: str,
    subject_commit: str,
    repository: str,
    expected_specs: Sequence[Mapping[str, Any]] = MODEL_SPECS,
    validation_mode: str = FULL_MODE,
    request_sha256: str | None = None,
) -> dict[str, Any]:
    expected = tuple(dict(item) for item in expected_specs)
    all_passed = len(calls) == len(expected) and all(call.get("passed") for call in calls)
    quota_passed = all(
        isinstance(call.get("quota_evidence"), dict)
        and call["quota_evidence"].get("available") is True
        for call in calls
    )
    status = "PASS" if all_passed and quota_passed else "FAIL"
    receipt: dict[str, Any] = {
        "receipt_id": RECEIPT_ID,
        "schema_version": "v0.1.2",
        "classification": CLASSIFICATION,
        "validation_mode": validation_mode,
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
    if validation_mode == UPPERCASE_RETRY_MODE:
        receipt["authorization"] = {
            "authorization_id": UPPERCASE_AUTHORIZATION_ID,
            "authorization_merge_commit": UPPERCASE_AUTHORIZATION_MERGE_COMMIT,
            "authorization_anchor": {
                "path": UPPERCASE_AUTHORIZATION_PATH.as_posix(),
                "sha256": UPPERCASE_AUTHORIZATION_SHA256,
            },
            "current_line_successor": {
                "path": UPPERCASE_SUCCESSOR_PATH.as_posix(),
                "sha256": UPPERCASE_SUCCESSOR_SHA256,
            },
            "maximum_provider_calls": 1,
            "request_sha256": request_sha256 or UPPERCASE_REQUEST_SHA256,
            "pair_001_execution_authorized": False,
            "readiness_promotion_authorized": False,
        }
        receipt["non_claims"].extend(
            [
                "This receipt consumes the one authorized uppercase diagnostic call.",
                "Success leaves freshness validation and readiness anchoring pending.",
                "Failure grants no additional uppercase retry.",
            ]
        )
    return receipt


def write_new_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    rendered = pretty_json_bytes(receipt)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(rendered)
    if path.read_bytes() != rendered or strict_json_bytes(rendered) != receipt:
        raise RuntimeError("receipt destination round-trip verification failed")


def expected_specs_for_receipt(receipt: Mapping[str, Any]) -> tuple[dict[str, Any], ...]:
    mode = receipt.get("validation_mode", FULL_MODE)
    if mode == FULL_MODE:
        return MODEL_SPECS
    if mode == UPPERCASE_RETRY_MODE:
        authorization = receipt.get("authorization")
        if not isinstance(authorization, dict):
            raise ValueError("uppercase retry authorization binding missing")
        if not (
            authorization.get("authorization_id") == UPPERCASE_AUTHORIZATION_ID
            and authorization.get("authorization_merge_commit") == UPPERCASE_AUTHORIZATION_MERGE_COMMIT
            and authorization.get("authorization_anchor")
            == {"path": UPPERCASE_AUTHORIZATION_PATH.as_posix(), "sha256": UPPERCASE_AUTHORIZATION_SHA256}
            and authorization.get("current_line_successor")
            == {"path": UPPERCASE_SUCCESSOR_PATH.as_posix(), "sha256": UPPERCASE_SUCCESSOR_SHA256}
            and authorization.get("maximum_provider_calls") == 1
            and authorization.get("request_sha256") == UPPERCASE_REQUEST_SHA256
            and authorization.get("pair_001_execution_authorized") is False
            and authorization.get("readiness_promotion_authorized") is False
        ):
            raise ValueError("uppercase retry authorization binding mismatch")
        return (MODEL_SPECS[0],)
    raise ValueError("unknown provider validation mode")


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
    expected_specs = expected_specs_for_receipt(receipt)
    if receipt.get("provider_validation_calls_performed") != len(expected_specs):
        raise ValueError("provider validation call count mismatch")
    if receipt.get("pair_001_calls_performed") != 0:
        raise ValueError("Pair-001 call boundary violated")
    if receipt.get("experiment_run_ids_created") != []:
        raise ValueError("provider validation created experiment run identifiers")
    calls = receipt.get("calls")
    if not isinstance(calls, list) or len(calls) != len(expected_specs):
        raise ValueError("provider call evidence count mismatch")
    by_requested = {call.get("requested_model"): call for call in calls if isinstance(call, dict)}
    for spec in expected_specs:
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
    mode.add_argument("--check-request", action="store_true")
    parser.add_argument("--request", type=Path, default=REQUEST_PATH)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()

    if args.verify_receipt is not None:
        receipt = verify_receipt(args.verify_receipt)
        print(
            json.dumps(
                {
                    "receipt_id": receipt["receipt_id"],
                    "status": receipt["status"],
                    "validation_mode": receipt.get("validation_mode", FULL_MODE),
                    "pair_001_calls_performed": receipt["pair_001_calls_performed"],
                    "verified": True,
                },
                sort_keys=True,
            )
        )
        return 0

    root = args.repo_root.resolve()
    request_path = args.request
    if not request_path.is_absolute():
        request_path = root / request_path
    request = strict_json_file(request_path)
    selected_mode, selected_specs = select_request_mode(root, request)
    if args.check_request:
        print(
            json.dumps(
                {
                    "request_status": request["status"],
                    "validation_mode": selected_mode,
                    "provider_calls_authorized": len(selected_specs),
                    "pair_001_calls_performed": 0,
                    "valid": True,
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
    workflow_run_id = os.environ.get("GITHUB_RUN_ID", "")
    subject_commit = os.environ.get("GITHUB_HEAD_SHA", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "")
    if not workflow_run_id.isdigit():
        raise SystemExit("GITHUB_RUN_ID must be numeric")
    if not SHA1_RE.fullmatch(subject_commit):
        raise SystemExit("GITHUB_HEAD_SHA must be a full lowercase commit SHA")
    if repository != request.get("repository"):
        raise SystemExit("GITHUB_REPOSITORY does not match merged request")

    calls = [invoke_probe(spec, token, args.timeout_seconds) for spec in selected_specs]
    receipt = build_receipt(
        calls,
        output=args.output,
        workflow_run_id=workflow_run_id,
        subject_commit=subject_commit,
        repository=repository,
        expected_specs=selected_specs,
        validation_mode=selected_mode,
        request_sha256=(UPPERCASE_REQUEST_SHA256 if selected_mode == UPPERCASE_RETRY_MODE else None),
    )
    write_new_receipt(args.output, receipt)
    print(
        json.dumps(
            {
                "classification": receipt["classification"],
                "status": receipt["status"],
                "validation_mode": selected_mode,
                "provider_validation_calls_performed": receipt["provider_validation_calls_performed"],
                "pair_001_calls_performed": 0,
                "receipt_path": args.output.as_posix(),
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
