#!/usr/bin/env python3
"""Verify the fail-closed DeepSeek receiver-drift classification contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")
CONTRACT = BASE / "pre-execution" / "DEEPSEEK_RECEIVER_DRIFT_CLASSIFICATION_CONTRACT_v0_1_3.json"
REQUEST = BASE / "pre-execution" / "PROVIDER_VALIDATION_REQUEST_v0_1_2.json"
STATE = BASE / "execution-state" / "PAIR-001_EXECUTION_STATE_v0_1_1.json"
ORIGINAL_METADATA = BASE / "receipts" / "baseline" / "pair-001" / "CSH-RUN-001" / "execution-metadata.json"
UPPERCASE_ID = "deepseek/DeepSeek-V3-0324"
LOWERCASE_ID = "deepseek/deepseek-v3-0324"
IDENTICAL_FAILURE_BODY = "aaa6769a31dd521019993212fa93add5efbcdaadc2e777041173091a03fafc23"
RETRY_REQUEST_SHA = "d2c8aabbdda4f17509395aa8a55f607b2b0d52138a251e8da92bb8384a05bcef"
EXPECTED_ATTEMPTS = (
    {
        "attempt_number": 1,
        "observed_at_utc": "2026-07-19T07:38:22.039565+00:00",
        "workflow_run_id": 29678434082,
        "subject_commit": "a10fa59875c10a3b44ea27e8a13976c5b10fea45",
        "request_sha256": "70a1c1d0b05da416d2c419bac137505216dbc2ae497e0114b4e815d2c079584c",
        "receipt_sha256": "739d0729823482bb3bdb9b0507ba0235ecd6319764fb31f4d94cac3bd89e5e5d",
    },
    {
        "attempt_number": 2,
        "observed_at_utc": "2026-07-19T07:42:34.083313+00:00",
        "workflow_run_id": 29678549437,
        "subject_commit": "1ea494b86c097323c27591195c3aea01e778bbf6",
        "request_sha256": "70a1c1d0b05da416d2c419bac137505216dbc2ae497e0114b4e815d2c079584c",
        "receipt_sha256": "4b907397cee94446780eb8fc1efc742722347a74b3e93115648810b2ef78646c",
    },
    {
        "attempt_number": 3,
        "observed_at_utc": "2026-07-19T07:55:24.374494+00:00",
        "workflow_run_id": 29678913206,
        "subject_commit": "a4eec818d19530e500e4e651012d2cd9fb4fded0",
        "request_sha256": RETRY_REQUEST_SHA,
        "receipt_sha256": "774d13a7106c1d40b7ea7b6ac86d1d27dcbc235e7904b1fe2dd548da95d2488f",
    },
)


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite value prohibited: {value}")
            ),
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    required = [CONTRACT, REQUEST, STATE, ORIGINAL_METADATA]
    missing = [path.as_posix() for path in required if not (root / path).is_file()]
    record("required_surface", not missing, "present" if not missing else "; ".join(missing))
    if missing:
        return finish(checks)

    try:
        contract = load(root / CONTRACT)
        request = load(root / REQUEST)
        state = load(root / STATE)
        original = load(root / ORIGINAL_METADATA)
    except (OSError, json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        record("strict_json", False, str(exc))
        return finish(checks)
    record("strict_json", True, "control records parse without duplicate keys")

    objects_ok = all(isinstance(item, dict) for item in (contract, request, state, original))
    record("root_object_shape", objects_ok, "objects" if objects_ok else "one or more root records are not objects")
    if not objects_ok:
        return finish(checks)

    identity_ok = (
        contract.get("contract_id") == "CSH_DEEPSEEK_RECEIVER_DRIFT_CLASSIFICATION_v0_1_3"
        and contract.get("schema_version") == "v0.1.3"
        and contract.get("classification") == "RECEIVER_IDENTIFIER_DRIFT_CAUSE_UNRESOLVED"
        and contract.get("cause") == "UNRESOLVED"
        and contract.get("status") == "CLASSIFIED_RETRY_NOT_AUTHORIZED"
    )
    record("classification_identity", identity_ok, "cause remains UNRESOLVED" if identity_ok else "classification mismatch")

    observations = contract.get("observations", {})
    if not isinstance(observations, dict):
        observations = {}
    july_12 = observations.get("july_12_uppercase_success", {})
    if not isinstance(july_12, dict):
        july_12 = {}
    artifact_bindings_ok = True
    for path_key, digest_key in (
        ("exact_request_path", "exact_request_sha256"),
        ("execution_metadata_path", "execution_metadata_sha256"),
        ("raw_response_path", "raw_response_sha256"),
    ):
        relative = july_12.get(path_key)
        expected_digest = july_12.get(digest_key)
        artifact = root / str(relative)
        if not isinstance(relative, str) or not artifact.is_file() or sha256(artifact) != expected_digest:
            artifact_bindings_ok = False
    original_ok = (
        july_12.get("run_id") == "CSH-RUN-001"
        and july_12.get("classification") == "ORIGINAL_PAIR_001_ATTEMPT"
        and july_12.get("requested_model") == original.get("requested_model") == UPPERCASE_ID
        and july_12.get("returned_model") == original.get("returned_model") == "DeepSeek-V3-0324"
        and july_12.get("http_status") == original.get("http_status") == 200
        and july_12.get("started_at_utc") == original.get("started_at_utc")
        and july_12.get("completed_at_utc") == original.get("completed_at_utc")
        and artifact_bindings_ok
    )
    record("july_12_uppercase_success", original_ok, "HTTP 200 evidence byte-bound" if original_ok else "July 12 evidence mismatch")

    attempts = observations.get("july_19_uppercase_failures", [])
    attempt_errors: list[str] = []
    if not isinstance(attempts, list) or len(attempts) != 3:
        attempt_errors.append("exactly three attempts required")
    else:
        for declared, expected in zip(attempts, EXPECTED_ATTEMPTS, strict=True):
            if not isinstance(declared, dict):
                attempt_errors.append(f"attempt {expected['attempt_number']} is not an object")
                continue
            receipt_path = root / str(declared.get("receipt_path", ""))
            if any(declared.get(key) != value for key, value in expected.items()):
                attempt_errors.append(f"attempt {expected['attempt_number']} declared binding mismatch")
                continue
            if not receipt_path.is_file() or sha256(receipt_path) != expected["receipt_sha256"]:
                attempt_errors.append(f"attempt {expected['attempt_number']} receipt digest mismatch")
                continue
            receipt = load(receipt_path)
            deepseek = next(
                (call for call in receipt.get("calls", []) if isinstance(call, dict) and call.get("provider") == "DeepSeek"),
                {},
            )
            if not (
                receipt.get("classification") == "PROVIDER_VALIDATION_ONLY_EXCLUDED_FROM_CSH_BASELINE"
                and receipt.get("workflow_run_id") == expected["workflow_run_id"]
                and receipt.get("subject_commit") == expected["subject_commit"]
                and receipt.get("observed_at_utc") == expected["observed_at_utc"]
                and receipt.get("pair_001_calls_performed") == 0
                and deepseek.get("requested_model") == declared.get("requested_model") == UPPERCASE_ID
                and deepseek.get("request_sha256") == expected["request_sha256"]
                and deepseek.get("http_status") == declared.get("http_status") == 500
                and deepseek.get("response_body_sha256")
                == declared.get("response_body_sha256")
                == IDENTICAL_FAILURE_BODY
            ):
                attempt_errors.append(f"attempt {expected['attempt_number']} evidence mismatch")
    record(
        "three_july_19_deterministic_500s",
        not attempt_errors,
        "three identical HTTP-status/body-digest failures" if not attempt_errors else "; ".join(attempt_errors),
    )

    catalog = observations.get("current_catalog_snapshot", {})
    if not isinstance(catalog, dict):
        catalog = {}
    catalog_ok = (
        catalog.get("source") == "https://models.github.ai/catalog/models"
        and catalog.get("catalog_id") == LOWERCASE_ID
        and catalog.get("name") == "DeepSeek-V3-0324"
        and catalog.get("registry") == "azureml-deepseek"
        and catalog.get("id_case_relation_to_recorded_requests")
        == "LOWERCASE_WHERE_RECORDED_REQUESTS_USED_UPPERCASE_MODEL_COMPONENT"
    )
    record("lowercase_catalog_snapshot", catalog_ok, LOWERCASE_ID if catalog_ok else "catalog snapshot mismatch")

    stopping = contract.get("precommitted_stopping_rule", {})
    if not isinstance(stopping, dict):
        stopping = {}
    authorization = stopping.get("authorization", {})
    budget = stopping.get("retry_budget", {})
    exact_retry = stopping.get("exact_uppercase_retry", {})
    if not isinstance(authorization, dict):
        authorization = {}
    if not isinstance(budget, dict):
        budget = {}
    if not isinstance(exact_retry, dict):
        exact_retry = {}
    try:
        last_attempt = datetime.fromisoformat(stopping.get("last_uppercase_attempt_observed_at_utc", ""))
        earliest = datetime.fromisoformat(stopping.get("earliest_permitted_retry_at_utc", ""))
        gap_seconds = (earliest - last_attempt).total_seconds()
    except (TypeError, ValueError):
        gap_seconds = -1
    stopping_ok = (
        stopping.get("scope") == "DEEPSEEK_PROVIDER_VALIDATION_DIAGNOSTIC_ONLY"
        and authorization == {
            "explicit_retry_authorization_required": True,
            "present": False,
            "authorization_record": None,
            "connector_publishing_authorization_is_retry_authorization": False,
        }
        and stopping.get("minimum_gap_hours") == 24
        and gap_seconds == 24 * 60 * 60
        and budget == {
            "additional_byte_identical_uppercase_attempts_permitted": 1,
            "additional_byte_identical_uppercase_attempts_consumed": 0,
            "automatic_retries_permitted": 0,
        }
        and exact_retry.get("byte_identity_reference_attempt") == 3
        and exact_retry.get("requested_model") == UPPERCASE_ID
        and exact_retry.get("request_sha256") == RETRY_REQUEST_SHA
        and exact_retry.get("max_tokens") == 2048
        and exact_retry.get("pair_001_run_id_created") is False
    )
    record("one_retry_after_authorization_and_24h", stopping_ok, "one dormant byte-identical retry" if stopping_ok else "retry gate mismatch")

    success = stopping.get("success_path", {})
    identical = stopping.get("identical_failure_path", {})
    different = stopping.get("different_outcome_path", {})
    lowercase = stopping.get("lowercase_diagnostic_path", {})
    if not isinstance(success, dict):
        success = {}
    if not isinstance(identical, dict):
        identical = {}
    if not isinstance(different, dict):
        different = {}
    if not isinstance(lowercase, dict):
        lowercase = {}
    branches_ok = (
        success.get("required_next_step") == "VALIDATE_FRESHNESS_THEN_PUBLISH_SEPARATE_READINESS_ANCHOR"
        and success.get("automatic_pair_001_execution") is False
        and success.get("automatic_readiness_promotion") is False
        and identical.get("identity_condition")
        == {"http_status": 500, "response_body_sha256": IDENTICAL_FAILURE_BODY}
        and identical.get("required_next_step") == "STOP_UPPERCASE_RETRIES"
        and identical.get("additional_uppercase_retries_permitted") == 0
        and different.get("required_next_step") == "STOP_AND_CLASSIFY_NEW_EVIDENCE"
        and different.get("retry_budget_automatically_replenished") is False
        and lowercase.get("available_only_after_identical_uppercase_failure") is True
        and lowercase.get("separate_explicit_authorization_required") is True
        and lowercase.get("requested_model_if_authorized") == LOWERCASE_ID
        and lowercase.get("if_successful_required_amendment") == "CSH-AMEND-004"
        and lowercase.get("if_successful_required_stratum") == "NEW_RECEIVER_VERSION_STRATUM"
        and lowercase.get("completes_original_byte_identical_pair_001_repetitions") is False
    )
    record("precommitted_outcome_branches", branches_ok, "success, stop, and diagnostic branches sealed" if branches_ok else "outcome branch mismatch")

    capture = contract.get("sanitized_error_capture", {})
    if not isinstance(capture, dict):
        capture = {}
    capture_ok = (
        capture.get("required_for_next_authorized_probe") is True
        and capture.get("capture_schema") == "SANITIZED_PROVIDER_ERROR_CODE_v0_1"
        and capture.get("allowed_source_paths") == ["error.code", "error.type"]
        and capture.get("allowed_token_pattern") == "^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$"
        and capture.get("message_persisted") is False
        and capture.get("raw_body_persisted") is False
    )
    record("sanitized_error_capture", capture_ok, "codes allowlisted; message and body prohibited" if capture_ok else "sanitized capture mismatch")

    boundary = contract.get("execution_boundary", {})
    if not isinstance(boundary, dict):
        boundary = {}
    boundary_ok = (
        request.get("status") == boundary.get("provider_validation_request_status") == "BLOCKED_PROVIDER_VALIDATION_FAILED"
        and boundary.get("provider_calls_performed_by_contract_publication") == 0
        and boundary.get("retry_authorized") is False
        and boundary.get("pair_001_calls_performed_by_contract_publication") == 0
        and boundary.get("pair_001_execution_effect") == "NONE"
        and boundary.get("readiness_effect") == "NONE"
        and state.get("repeat_runs") == []
    )
    record("no_calls_no_promotion", boundary_ok, "provider lane blocked; Pair-001 unchanged" if boundary_ok else "execution boundary mismatch")
    return finish(checks)


def finish(checks: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [item for item in checks if not item["passed"]]
    return {
        "checker": Path(__file__).name,
        "result": {
            "valid": not failed,
            "status": "DRIFT_CONTRACT_VALID_RETRY_NOT_AUTHORIZED" if not failed else "DRIFT_CONTRACT_INVALID",
            "cause": "UNRESOLVED",
            "provider_calls_performed": 0,
            "pair_001_execution_effect": "NONE",
            "readiness_effect": "NONE",
        },
        "checks": checks,
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = evaluate(repo_root(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print(result["result"]["status"])
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
