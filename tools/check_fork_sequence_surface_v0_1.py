#!/usr/bin/env python3
"""Verify and deterministically project the Fork Sequence Surface v0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA = Path("schemas/fork_sequence_ledger_v0_1.schema.json")
BASE = Path("docs/sequence-surface")
CONTRACT = BASE / "PAIR_001_SEQUENCE_TRANSITION_CONTRACT_v0_1.json"
LEDGER = BASE / "PAIR_001_SEQUENCE_LEDGER_v0_1.json"
PROJECTION = BASE / "PAIR_001_SEQUENCE_PROJECTION_v0_1.json"
CSH = Path("docs/experiments/cross-system-claim-handoff-v0.1")
DRIFT = CSH / "pre-execution" / "DEEPSEEK_RECEIVER_DRIFT_CLASSIFICATION_CONTRACT_v0_1_3.json"
REQUEST = CSH / "pre-execution" / "PROVIDER_VALIDATION_REQUEST_v0_1_2.json"
STATE = CSH / "execution-state" / "PAIR-001_EXECUTION_STATE_v0_1_1.json"
BINDING = CSH / "pre-execution" / "PRE_EXECUTION_BINDING_v0_1_2.json"
RELEASE_ANCHOR = CSH / "pre-execution" / "INSTRUMENTATION_RELEASE_ANCHOR_v0_1_2.json"
BASE_SEQUENCE_HEAD = "0e58a151cb5801f554619eb44a40948ad03e3e55"
GENESIS_HASH = "0" * 64
UPPERCASE_REQUEST_SHA = "d2c8aabbdda4f17509395aa8a55f607b2b0d52138a251e8da92bb8384a05bcef"
IDENTICAL_FAILURE_BODY_SHA = "aaa6769a31dd521019993212fa93add5efbcdaadc2e777041173091a03fafc23"


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_load(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite value prohibited: {value}")
            ),
        )


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


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def event_sha256(event: dict[str, Any]) -> str:
    payload = dict(event)
    payload.pop("event_sha256", None)
    return sha256_bytes(canonical_json_bytes(payload))


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("Repository root not found")


def add_error(errors: list[dict[str, str]], code: str, detail: str, path: str = "") -> None:
    errors.append({"code": code, "detail": detail, "path": path})


def transition_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    transitions = contract.get("transitions", [])
    if not isinstance(transitions, list):
        return {}
    return {
        item["transition_id"]: item
        for item in transitions
        if isinstance(item, dict) and isinstance(item.get("transition_id"), str)
    }


def safe_evidence_path(root: Path, relative: Any) -> Path | None:
    if not isinstance(relative, str) or not relative:
        return None
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        return None
    candidate = root.joinpath(*pure.parts)
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def derive_projection(
    *,
    root: Path,
    ledger: dict[str, Any],
    contract: dict[str, Any],
    drift: dict[str, Any],
    request: dict[str, Any],
    state: dict[str, Any],
    binding: dict[str, Any],
    release_anchor: dict[str, Any],
) -> dict[str, Any]:
    events = ledger.get("events", [])
    typed_events = [item for item in events if isinstance(item, dict)] if isinstance(events, list) else []
    last = typed_events[-1] if typed_events else {}
    used = {item.get("transition_id") for item in typed_events}
    transitions = transition_map(contract)
    current_state = last.get("to_state")
    successors = sorted(
        transition_id
        for transition_id, transition in transitions.items()
        if transition.get("from_state") == current_state and transition_id not in used
    )
    currently_eligible = [
        transition_id
        for transition_id in successors
        if transitions[transition_id].get("authority_requirement") == "NONE"
    ]
    effects = [item.get("effects", {}) for item in typed_events]
    provider_calls = sum(
        item.get("provider_calls_observed_delta", 0)
        for item in effects
        if isinstance(item, dict) and isinstance(item.get("provider_calls_observed_delta", 0), int)
    )
    originals = sum(
        item.get("pair_001_original_attempts_observed_delta", 0)
        for item in effects
        if isinstance(item, dict) and isinstance(item.get("pair_001_original_attempts_observed_delta", 0), int)
    )
    repetitions = sum(
        item.get("pair_001_repetitions_observed_delta", 0)
        for item in effects
        if isinstance(item, dict) and isinstance(item.get("pair_001_repetitions_observed_delta", 0), int)
    )
    validation_events = [
        item for item in typed_events if item.get("event_type") == "PROVIDER_VALIDATION_ATTEMPT_OBSERVED"
    ]
    validation_calls = sum(item.get("effects", {}).get("provider_calls_observed_delta", 0) for item in validation_events)
    deepseek_http_500_attempts = 0
    meta_successful_validation_calls = 0
    for event in validation_events:
        for reference in event.get("evidence_refs", []):
            if not isinstance(reference, dict):
                continue
            receipt_path = safe_evidence_path(root, reference.get("path"))
            if receipt_path is None or not receipt_path.is_file():
                continue
            receipt = strict_load(receipt_path)
            if not isinstance(receipt, dict):
                continue
            for call in receipt.get("calls", []):
                if not isinstance(call, dict):
                    continue
                if call.get("provider") == "DeepSeek" and call.get("http_status") == 500:
                    deepseek_http_500_attempts += 1
                if call.get("provider") == "Meta" and call.get("passed") is True:
                    meta_successful_validation_calls += 1
    stopping = contract.get("stopping_rules", {})
    uppercase = stopping.get("uppercase_retry", {}) if isinstance(stopping, dict) else {}
    identical = stopping.get("identical_failure", {}) if isinstance(stopping, dict) else {}
    drift_stopping = drift.get("precommitted_stopping_rule", {})
    drift_authorization = drift_stopping.get("authorization", {}) if isinstance(drift_stopping, dict) else {}
    drift_budget = drift_stopping.get("retry_budget", {}) if isinstance(drift_stopping, dict) else {}
    request_disposition = request.get("disposition", {})
    anchor_boundary = contract.get("anchor_boundary", {})
    return {
        "projection_id": "FORK_SEQUENCE_PROJECTION_PAIR_001_v0_1",
        "schema_version": "v0.1",
        "record_kind": "deterministic_sequence_projection",
        "surface_kind": "CROSS_SURFACE_SEQUENCE_PROJECTION",
        "status": "CANDIDATE_NOT_ADMITTED",
        "projection_as_of_utc": contract.get("projection_rules", {}).get("projection_as_of_utc"),
        "source": {
            "ledger_path": LEDGER.as_posix(),
            "ledger_sha256": sha256(root / LEDGER),
            "transition_contract_path": CONTRACT.as_posix(),
            "transition_contract_sha256": sha256(root / CONTRACT),
            "base_sequence_head": ledger.get("base_sequence_head"),
        },
        "sequence": {
            "append_only": ledger.get("append_only") is True,
            "event_count": len(typed_events),
            "current_state": current_state,
            "last_event_id": last.get("event_id"),
            "last_event_sha256": last.get("event_sha256"),
            "declared_successor_transition_ids": successors,
            "currently_eligible_successor_transition_ids": currently_eligible,
        },
        "observed_history": {
            "provider_calls": provider_calls,
            "pair_001_original_attempts": originals,
            "pair_001_repetitions": repetitions,
            "provider_validation_attempts": len(validation_events),
            "provider_validation_calls": validation_calls,
            "deepseek_http_500_attempts": deepseek_http_500_attempts,
            "meta_successful_validation_calls": meta_successful_validation_calls,
        },
        "publication_and_control": {
            "instrumentation_release": str(release_anchor.get("status", "")).upper(),
            "mutable_publication_state": state.get("publication", {}).get("status"),
            "pre_execution_status": binding.get("status"),
            "provider_validation_request_status": request.get("status"),
        },
        "drift": {
            "cause": drift.get("cause"),
            "classification": drift.get("classification"),
            "status": drift.get("status"),
            "uppercase_request_sha256": uppercase.get("request_sha256"),
            "identical_failure_http_status": identical.get("http_status"),
            "identical_failure_body_sha256": identical.get("response_body_sha256"),
        },
        "retry": {
            "explicit_authorization_required": uppercase.get("explicit_authorization_required"),
            "authorization_present": drift_authorization.get("present"),
            "minimum_gap_hours": uppercase.get("minimum_gap_hours"),
            "earliest_permitted_at_utc": uppercase.get("earliest_permitted_at_utc"),
            "remaining_byte_identical_uppercase_attempts": drift_budget.get(
                "additional_byte_identical_uppercase_attempts_permitted"
            ),
            "automatic_attempts": drift_budget.get("automatic_retries_permitted"),
        },
        "execution_boundary": {
            "provider_validation_prerequisite_satisfied": request_disposition.get(
                "provider_validation_prerequisite_satisfied"
            ),
            "provider_execution_permitted": binding.get("provider_execution_permitted"),
            "pair_001_execution_permitted": request_disposition.get("pair_001_execution_permitted"),
            "pair_001_repeat_runs_recorded": len(state.get("repeat_runs", [])),
            "provider_calls_performed_by_sequence_surface_publication": 0,
            "pair_001_calls_performed_by_sequence_surface_publication": 0,
            "readiness_effect": "NONE",
            "execution_effect": "NONE",
        },
        "successor_anchor": {
            "status": anchor_boundary.get("status"),
            "must_bind_exact_merge_commit": anchor_boundary.get("must_bind_exact_merge_commit"),
            "must_bind_successful_workflow_runs": anchor_boundary.get("must_bind_successful_workflow_runs"),
            "provider_call_effect": anchor_boundary.get("provider_call_effect"),
            "pair_001_execution_effect": anchor_boundary.get("pair_001_execution_effect"),
            "readiness_effect": anchor_boundary.get("readiness_effect"),
        },
        "non_claims": [
            "The projection is recomputed evidence, not an authority source.",
            "A declared successor is not authorization to take it.",
            "No diagnostic is classified as a Pair-001 repetition.",
            "No provider call, readiness promotion, or Pair-001 execution is performed by this surface.",
            "Sequence conformance does not establish truth, approval, compliance, safety, legal sufficiency, production readiness, or institutional authority."
        ],
    }


def evaluate(
    root: Path,
    *,
    ledger_override: dict[str, Any] | None = None,
    compare_projection: bool = True,
) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    required = [SCHEMA, CONTRACT, LEDGER, DRIFT, REQUEST, STATE, BINDING, RELEASE_ANCHOR]
    if compare_projection:
        required.append(PROJECTION)
    missing = [path.as_posix() for path in required if not (root / path).is_file()]
    if missing:
        add_error(errors, "SURFACE_REQUIRED_FILE_MISSING", "; ".join(missing))
        return finish(errors, projection=None)

    try:
        schema = strict_load(root / SCHEMA)
        contract = strict_load(root / CONTRACT)
        ledger = ledger_override if ledger_override is not None else strict_load(root / LEDGER)
        drift = strict_load(root / DRIFT)
        request = strict_load(root / REQUEST)
        state = strict_load(root / STATE)
        binding = strict_load(root / BINDING)
        release_anchor = strict_load(root / RELEASE_ANCHOR)
        committed_projection = strict_load(root / PROJECTION) if compare_projection else None
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        add_error(errors, "STRICT_JSON_INVALID", str(exc))
        return finish(errors, projection=None)

    roots = (schema, contract, ledger, drift, request, state, binding, release_anchor)
    if not all(isinstance(item, dict) for item in roots):
        add_error(errors, "ROOT_OBJECT_INVALID", "all sequence control records must be JSON objects")
        return finish(errors, projection=None)

    try:
        Draft202012Validator.check_schema(schema)
        validation_errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(ledger),
            key=lambda item: list(item.absolute_path),
        )
    except Exception as exc:
        add_error(errors, "LEDGER_SCHEMA_INVALID", str(exc), SCHEMA.as_posix())
        return finish(errors, projection=None)
    for item in validation_errors:
        location = "/".join(str(part) for part in item.absolute_path)
        add_error(errors, "LEDGER_SCHEMA_CONFORMANCE_FAILED", item.message, location)

    identity_ok = (
        contract.get("contract_id") == "FORK_SEQUENCE_TRANSITION_CONTRACT_PAIR_001_v0_1"
        and contract.get("schema_version") == "v0.1"
        and contract.get("surface_kind") == "CROSS_SURFACE_SEQUENCE_PROJECTION"
        and contract.get("status") == "CANDIDATE_NOT_ADMITTED"
        and contract.get("initial_state") == "SEQUENCE_INIT"
        and ledger.get("base_sequence_head") == BASE_SEQUENCE_HEAD
        and ledger.get("execution_effect") == "NONE"
    )
    if not identity_ok:
        add_error(errors, "SURFACE_IDENTITY_INVALID", "sequence or contract identity mismatch")

    contract_ref = ledger.get("transition_contract", {})
    if not (
        isinstance(contract_ref, dict)
        and contract_ref.get("path") == CONTRACT.as_posix()
        and contract_ref.get("sha256") == sha256(root / CONTRACT)
    ):
        add_error(errors, "TRANSITION_CONTRACT_BINDING_INVALID", "ledger does not byte-bind the transition contract")

    transitions = transition_map(contract)
    declared_ids = [
        item.get("transition_id")
        for item in contract.get("transitions", [])
        if isinstance(item, dict)
    ]
    if len(declared_ids) != len(set(declared_ids)):
        add_error(errors, "TRANSITION_ID_DUPLICATE", "transition identifiers must be unique")

    events = ledger.get("events", [])
    if not isinstance(events, list):
        events = []
    ordinals = [item.get("ordinal") for item in events if isinstance(item, dict)]
    if ordinals != list(range(1, len(events) + 1)):
        add_error(errors, "EVENT_ORDINALS_NONCONTIGUOUS", f"observed={ordinals}")
    event_ids = [item.get("event_id") for item in events if isinstance(item, dict)]
    if len(event_ids) != len(events) or len(event_ids) != len(set(event_ids)):
        add_error(errors, "EVENT_ID_DUPLICATE", "event identifiers must be present and unique")

    expected_previous = GENESIS_HASH
    expected_state = contract.get("initial_state")
    previous_time: datetime | None = None
    used_transitions: set[str] = set()
    for index, event in enumerate(events):
        path = f"events/{index}"
        if not isinstance(event, dict):
            add_error(errors, "EVENT_OBJECT_INVALID", "event must be an object", path)
            continue
        event_id = str(event.get("event_id"))
        occurred = parse_time(event.get("occurred_at_utc"))
        if occurred is None or (previous_time is not None and occurred < previous_time):
            add_error(errors, "EVENT_TIME_ORDER_INVALID", event_id, path)
        if occurred is not None:
            previous_time = occurred

        if event.get("previous_event_sha256") != expected_previous:
            add_error(errors, "EVENT_HASH_CHAIN_INVALID", f"{event_id} previous hash mismatch", path)
        computed_event_hash = event_sha256(event)
        if event.get("event_sha256") != computed_event_hash:
            add_error(errors, "EVENT_HASH_CHAIN_INVALID", f"{event_id} event hash mismatch", path)
        expected_previous = computed_event_hash

        if event.get("from_state") != expected_state:
            add_error(
                errors,
                "EVENT_STATE_CHAIN_INVALID",
                f"{event_id}: expected from_state={expected_state!r}",
                path,
            )
        expected_state = event.get("to_state")

        if event.get("to_state") == "PAIR_001_EXECUTION_ELIGIBLE":
            add_error(errors, "FORBIDDEN_PROMOTION", f"{event_id} claims execution eligibility", path)

        transition_id = event.get("transition_id")
        transition = transitions.get(transition_id)
        if transition is None:
            add_error(errors, "TRANSITION_UNDECLARED", f"{event_id}: {transition_id!r}", path)
            continue
        if transition_id in used_transitions:
            add_error(errors, "TRANSITION_REUSED", f"{transition_id} appears more than once", path)
        used_transitions.add(str(transition_id))
        if not (
            event.get("from_state") == transition.get("from_state")
            and event.get("to_state") == transition.get("to_state")
            and event.get("event_type") == transition.get("event_type")
        ):
            add_error(errors, "TRANSITION_STATE_MISMATCH", f"{event_id}: {transition_id}", path)

        authority = event.get("authority", {})
        requirement = transition.get("authority_requirement")
        if requirement == "NONE":
            authority_ok = authority == {
                "requirement": "NONE",
                "present": False,
                "reference": None,
                "effect": "NONE",
            }
        else:
            authority_ok = (
                isinstance(authority, dict)
                and authority.get("requirement") == "EXPLICIT_EXTERNAL_AUTHORIZATION"
                and authority.get("present") is True
                and isinstance(authority.get("reference"), str)
                and bool(authority.get("reference"))
                and authority.get("effect") == "NONE"
            )
        if not authority_ok:
            add_error(errors, "AUTHORITY_FORGERY", f"{event_id} authority does not meet contract", path)

        if event.get("effects") != transition.get("expected_effects"):
            add_error(errors, "EVENT_EFFECT_CONTRACT_VIOLATION", event_id, path)

        for ref_index, reference in enumerate(event.get("evidence_refs", [])):
            ref_path = f"{path}/evidence_refs/{ref_index}"
            if not isinstance(reference, dict):
                add_error(errors, "EVIDENCE_REFERENCE_INVALID", event_id, ref_path)
                continue
            artifact = safe_evidence_path(root, reference.get("path"))
            if artifact is None:
                add_error(errors, "EVIDENCE_PATH_INVALID", str(reference.get("path")), ref_path)
            elif artifact.is_symlink():
                add_error(errors, "EVIDENCE_SYMLINK_PROHIBITED", str(reference.get("path")), ref_path)
            elif not artifact.is_file():
                add_error(errors, "EVIDENCE_REFERENCE_INVALID", str(reference.get("path")), ref_path)
            elif sha256(artifact) != reference.get("sha256"):
                add_error(errors, "SOURCE_ARTIFACT_DIGEST_MISMATCH", str(reference.get("path")), ref_path)

    stopping = contract.get("stopping_rules", {})
    uppercase = stopping.get("uppercase_retry", {}) if isinstance(stopping, dict) else {}
    identical = stopping.get("identical_failure", {}) if isinstance(stopping, dict) else {}
    lowercase = stopping.get("lowercase_diagnostic", {}) if isinstance(stopping, dict) else {}
    drift_stopping = drift.get("precommitted_stopping_rule", {})
    drift_budget = drift_stopping.get("retry_budget", {}) if isinstance(drift_stopping, dict) else {}
    stopping_ok = (
        drift.get("cause") == "UNRESOLVED"
        and drift.get("status") == "CLASSIFIED_RETRY_NOT_AUTHORIZED"
        and uppercase.get("explicit_authorization_required") is True
        and uppercase.get("minimum_gap_hours") == 24
        and uppercase.get("earliest_permitted_at_utc") == "2026-07-20T07:55:24.374494+00:00"
        and uppercase.get("request_sha256") == UPPERCASE_REQUEST_SHA
        and uppercase.get("remaining_attempts")
        == drift_budget.get("additional_byte_identical_uppercase_attempts_permitted")
        == 1
        and uppercase.get("automatic_attempts") == drift_budget.get("automatic_retries_permitted") == 0
        and identical.get("http_status") == 500
        and identical.get("response_body_sha256") == IDENTICAL_FAILURE_BODY_SHA
        and identical.get("additional_uppercase_retries") == 0
        and lowercase.get("successful_amendment") == "CSH-AMEND-004"
        and lowercase.get("successful_stratum") == "NEW_RECEIVER_VERSION_STRATUM"
        and lowercase.get("completes_original_pair_001_repetitions") is False
    )
    if not stopping_ok:
        add_error(errors, "STOPPING_RULE_MISMATCH", "sequence and drift stopping rules diverge")

    control_boundary_ok = (
        request.get("status") == "BLOCKED_PROVIDER_VALIDATION_FAILED"
        and request.get("disposition", {}).get("provider_validation_prerequisite_satisfied") is False
        and request.get("disposition", {}).get("pair_001_execution_permitted") is False
        and state.get("publication", {}).get("status") == "anchor_ci_green"
        and state.get("repeat_runs") == []
        and binding.get("status") == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
        and binding.get("provider_execution_permitted") is False
        and binding.get("provider_calls_performed_by_this_stage") == 0
        and release_anchor.get("status") == "published"
        and release_anchor.get("pair_001_execution_effect") == "NONE"
    )
    if not control_boundary_ok:
        add_error(errors, "CONTROL_BOUNDARY_MISMATCH", "Pair-001 control boundary is not fail closed")

    projection = derive_projection(
        root=root,
        ledger=ledger,
        contract=contract,
        drift=drift,
        request=request,
        state=state,
        binding=binding,
        release_anchor=release_anchor,
    )
    if compare_projection and committed_projection != projection:
        add_error(errors, "PROJECTION_MISMATCH", "committed projection differs from deterministic recomputation")
    return finish(errors, projection=projection)


def finish(errors: list[dict[str, str]], *, projection: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "checker": Path(__file__).name,
        "result": {
            "valid": not errors,
            "status": (
                "SEQUENCE_SURFACE_CONFORMS_CANDIDATE_NOT_ADMITTED"
                if not errors
                else "SEQUENCE_SURFACE_INVALID"
            ),
            "provider_calls_performed_by_checker": 0,
            "pair_001_execution_effect": "NONE",
            "readiness_effect": "NONE",
            "anchor_status": "SEPARATE_SUCCESSOR_REQUIRED",
        },
        "errors": errors,
        "error_codes": sorted({item["code"] for item in errors}),
        "projection": projection,
        "non_claims": {
            "does_not_establish_truth": True,
            "does_not_authorize_successor_transition": True,
            "does_not_authorize_provider_calls": True,
            "does_not_promote_readiness": True,
            "does_not_execute_pair_001": True,
            "does_not_resist_coordinated_resealing_without_successor_anchor": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--derive-projection", action="store_true")
    args = parser.parse_args()
    root = repo_root(args.root)
    result = evaluate(root, compare_projection=not args.derive_projection)
    if args.derive_projection:
        if result["projection"] is None or result["errors"]:
            print(json.dumps(result, indent=2, sort_keys=True))
            return 1
        print(pretty_json(result["projection"]), end="")
        return 0
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for error in result["errors"]:
            print(f"[{error['code']}] {error['path']}: {error['detail']}")
        print(result["result"]["status"])
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
