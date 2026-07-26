#!/usr/bin/env python3
"""Validate declared temporal succession without rewriting historical records."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat
from typing import Any


LEDGER_PATH = Path("docs/state/FORK_TEMPORAL_SUCCESSION_LEDGER_v0_1.json")
HISTORICAL_PATH = Path("docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json")
CURRENT_PATH = Path("docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json")
AUDIT_PATH = Path(
    "docs/exterior-observations/observations/"
    "EXTERIOR_OBSERVATION_CLAUDE_MAIN_FD93D05_REPOSITORY_AUDIT_v0_1.md"
)

HISTORICAL_SHA256 = "8e62fdf1adc5cacb087b8f1b2a1a1d8674521990d42b4d3897d17c49f433b098"
GOVERNED_COMMIT = "1241c0084900f2c60f362205525464582e57b4a7"
MAIN_AUDIT_COMMIT = "fd93d051235ec43bee925878bc916d09179b3c90"
CURRENT_PROJECTION_ID = "FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2"
HISTORICAL_PROJECTION_ID = "FORK_PROOF_SURFACE_STATE_v0_1"
FAILURE_CODE = "TEMPORAL_SUCCESSION_RECONCILIATION_REQUIRED"

EXPECTED_EFFECTS = {
    "main_ref": "NONE",
    "preservation_ref": "NONE",
    "existing_pull_requests": "NONE",
    "provider_calls": 0,
    "pair_001_calls": 0,
    "pair_001_repetitions": 0,
    "readiness": "NONE",
    "retry_authorization": "NONE",
    "execution_authority": "NONE",
    "admission": "NONE",
}


class DuplicateKeyError(ValueError):
    pass


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for item in value.values():
            _assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            _assert_finite(item)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=_object_no_duplicates,
            parse_constant=_reject_constant,
        )
    _assert_finite(value)
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_regular_file(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if not relative or pure.is_absolute() or ".." in pure.parts or "\\" in relative:
        raise ValueError(f"unsafe repository-relative path: {relative!r}")
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {relative}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"not a regular file: {relative}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: timestamp must be a non-empty string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"{label}: timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def expect(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def expect_equal(errors: list[str], actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, found {actual!r}")


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    def read_json(relative: str) -> Any:
        try:
            return load_json(safe_regular_file(root, relative))
        except Exception as exc:
            errors.append(f"{relative}: {exc}")
            return {}

    ledger = read_json(LEDGER_PATH.as_posix())
    current = read_json(CURRENT_PATH.as_posix())

    try:
        historical_path = safe_regular_file(root, HISTORICAL_PATH.as_posix())
        expect_equal(
            errors,
            sha256_file(historical_path),
            HISTORICAL_SHA256,
            "July 11 historical projection sha256",
        )
    except Exception as exc:
        errors.append(f"{HISTORICAL_PATH.as_posix()}: {exc}")

    expect_equal(errors, ledger.get("ledger_id"), "FORK_TEMPORAL_SUCCESSION_LEDGER_v0_1", "ledger id")
    completeness = ledger.get("declared_event_registry_complete_through", {})
    expect_equal(errors, completeness.get("commit_sha"), GOVERNED_COMMIT, "ledger completeness commit")
    try:
        completeness_time = parse_time(completeness.get("as_of_utc"), "ledger completeness")
    except Exception as exc:
        errors.append(str(exc))
        completeness_time = datetime.min.replace(tzinfo=timezone.utc)

    records = ledger.get("records", [])
    if not isinstance(records, list):
        errors.append("ledger records must be a list")
        records = []
    records_by_id: dict[str, dict[str, Any]] = {}
    record_times: dict[str, datetime] = {}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {index} is not an object")
            continue
        projection_id = record.get("projection_id")
        if not isinstance(projection_id, str) or not projection_id:
            errors.append(f"record {index} has invalid projection_id")
            continue
        if projection_id in records_by_id:
            errors.append(f"duplicate projection_id: {projection_id}")
            continue
        records_by_id[projection_id] = record
        try:
            record_times[projection_id] = parse_time(
                record.get("projection_as_of_utc"), f"record {projection_id}"
            )
        except Exception as exc:
            errors.append(str(exc))
        path = record.get("path")
        expected_digest = record.get("sha256")
        if not isinstance(path, str) or not isinstance(expected_digest, str):
            errors.append(f"record {projection_id}: path and sha256 are required")
            continue
        try:
            expect_equal(
                errors,
                sha256_file(safe_regular_file(root, path)),
                expected_digest,
                f"record {projection_id} sha256",
            )
        except Exception as exc:
            errors.append(f"record {projection_id}: {exc}")
        scope = record.get("scope")
        expect(
            errors,
            isinstance(scope, list)
            and bool(scope)
            and all(isinstance(item, str) and item for item in scope)
            and len(scope) == len(set(scope)),
            f"record {projection_id}: scope must be a unique non-empty string list",
        )
        expect(
            errors,
            isinstance(record.get("represented_as_current"), bool),
            f"record {projection_id}: represented_as_current must be boolean",
        )

    expect_equal(
        errors,
        records_by_id.get(HISTORICAL_PROJECTION_ID, {}).get("sha256"),
        HISTORICAL_SHA256,
        "historical ledger binding",
    )
    expect_equal(
        errors,
        records_by_id.get(HISTORICAL_PROJECTION_ID, {}).get("represented_as_current"),
        False,
        "historical projection current representation",
    )
    expect_equal(
        errors,
        records_by_id.get(HISTORICAL_PROJECTION_ID, {}).get("successor_projection_id"),
        CURRENT_PROJECTION_ID,
        "historical successor",
    )

    events = ledger.get("admitted_state_changing_events", [])
    if not isinstance(events, list):
        errors.append("admitted_state_changing_events must be a list")
        events = []
    events_by_id: dict[str, dict[str, Any]] = {}
    event_times: dict[str, datetime] = {}
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"event {index} is not an object")
            continue
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"event {index} has invalid event_id")
            continue
        if event_id in events_by_id:
            errors.append(f"duplicate event_id: {event_id}")
            continue
        events_by_id[event_id] = event
        expect_equal(errors, event.get("state_change_admitted"), True, f"event {event_id} admission flag")
        try:
            event_time = parse_time(event.get("admitted_at_utc"), f"event {event_id}")
            event_times[event_id] = event_time
            expect(
                errors,
                event_time <= completeness_time,
                f"event {event_id}: later than declared ledger completeness coordinate",
            )
        except Exception as exc:
            errors.append(str(exc))
        affected = event.get("affected_scope")
        expect(
            errors,
            isinstance(affected, list)
            and bool(affected)
            and all(isinstance(item, str) and item for item in affected)
            and len(affected) == len(set(affected)),
            f"event {event_id}: affected_scope must be a unique non-empty string list",
        )
        path = event.get("source_path")
        expected_digest = event.get("source_sha256")
        if isinstance(path, str) and isinstance(expected_digest, str):
            try:
                expect_equal(
                    errors,
                    sha256_file(safe_regular_file(root, path)),
                    expected_digest,
                    f"event {event_id} source sha256",
                )
            except Exception as exc:
                errors.append(f"event {event_id}: {exc}")
        else:
            errors.append(f"event {event_id}: source_path and source_sha256 are required")

    # Successor links must be reciprocal, acyclic, and temporally forward.
    for projection_id, record in records_by_id.items():
        successor_id = record.get("successor_projection_id")
        if successor_id is None:
            continue
        successor = records_by_id.get(successor_id)
        if successor is None:
            errors.append(f"{projection_id}: unknown successor {successor_id!r}")
            continue
        expect_equal(
            errors,
            successor.get("predecessor_projection_id"),
            projection_id,
            f"{successor_id} predecessor",
        )
        if projection_id in record_times and successor_id in record_times:
            expect(
                errors,
                record_times[successor_id] > record_times[projection_id],
                f"{successor_id}: successor temporal closure must be later than {projection_id}",
            )

    for start_id in records_by_id:
        visited: set[str] = set()
        cursor: str | None = start_id
        while cursor is not None:
            if cursor in visited:
                errors.append(f"successor cycle detected from {start_id}: {cursor}")
                break
            visited.add(cursor)
            next_value = records_by_id.get(cursor, {}).get("successor_projection_id")
            cursor = next_value if isinstance(next_value, str) else None

    # Core temporal-succession rule. A record represented as current may be
    # followed by later admitted state change only if a later successor
    # reconciles each applicable event.
    for projection_id, record in records_by_id.items():
        if not record.get("represented_as_current"):
            continue
        projection_time = record_times.get(projection_id)
        record_scope = set(record.get("scope", []))
        if projection_time is None:
            continue
        for event_id, event in events_by_id.items():
            event_time = event_times.get(event_id)
            if event_time is None or event_time <= projection_time:
                continue
            if not record_scope.intersection(event.get("affected_scope", [])):
                continue
            cursor_id = record.get("successor_projection_id")
            reconciled = False
            while isinstance(cursor_id, str) and cursor_id in records_by_id:
                successor = records_by_id[cursor_id]
                successor_time = record_times.get(cursor_id)
                if (
                    successor_time is not None
                    and successor_time >= event_time
                    and event_id in successor.get("reconciles_event_ids", [])
                ):
                    reconciled = True
                    break
                cursor_id = successor.get("successor_projection_id")
            if not reconciled:
                errors.append(
                    f"{FAILURE_CODE}: {projection_id} is represented as current "
                    f"but later admitted event {event_id} lacks successor reconciliation"
                )

    current_ids = [
        projection_id
        for projection_id, record in records_by_id.items()
        if record.get("represented_as_current")
    ]
    expect_equal(errors, current_ids, [CURRENT_PROJECTION_ID], "represented current projection ids")

    current_record = records_by_id.get(CURRENT_PROJECTION_ID, {})
    expect_equal(errors, current.get("projection_id"), CURRENT_PROJECTION_ID, "current projection id")
    expect_equal(errors, current.get("represented_as_current"), True, "current projection representation")
    expect_equal(
        errors,
        current.get("source_coordinate", {}).get("commit_sha"),
        GOVERNED_COMMIT,
        "current source coordinate",
    )
    expect_equal(
        errors,
        current.get("source_coordinate", {}).get("branch"),
        "preservation/clean-continuance-v0.1",
        "current source branch",
    )
    expect_equal(
        errors,
        current.get("predecessor_projection", {}).get("sha256"),
        HISTORICAL_SHA256,
        "current predecessor digest",
    )
    expect_equal(
        errors,
        current.get("reconciled_event_ids"),
        current_record.get("reconciles_event_ids"),
        "current reconciled event ids",
    )
    expect_equal(errors, current.get("effects"), EXPECTED_EFFECTS, "current zero effects")

    branch_standing = current.get("branch_standing", {})
    expect_equal(
        errors,
        branch_standing.get("main", {}).get("coordinate"),
        MAIN_AUDIT_COMMIT,
        "main historical coordinate",
    )
    expect_equal(
        errors,
        branch_standing.get("preservation/clean-continuance-v0.1", {}).get("coordinate"),
        GOVERNED_COMMIT,
        "governed preservation coordinate",
    )

    csh = current.get("proof_surface", {}).get("cross_system_claim_handoff_v0_1", {})
    expected_csh = {
        "corpus_freeze_status": "frozen",
        "original_attempt_receipts_present": 2,
        "original_attempt_execution_outcomes": ["success", "http_error"],
        "instrumentation_amendment_status": "final",
        "pre_execution_status": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
        "sequence_state": "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED",
        "provider_validation_request_status": "BLOCKED_PROVIDER_VALIDATION_FAILED",
        "receiver_drift_cause": "UNRESOLVED",
        "provider_validation_prerequisite_satisfied": False,
        "uppercase_retry_authorization_present": False,
        "pair_001_execution_permitted": False,
        "pair_001_repetitions": 0,
        "provider_calls_in_observed_sequence": 8,
        "pair_001_original_attempts": 2,
        "provider_validation_calls": 6,
    }
    expect_equal(errors, csh, expected_csh, "current CSH projection")

    bindings = current.get("source_bindings", [])
    if not isinstance(bindings, list):
        errors.append("current source_bindings must be a list")
        bindings = []
    seen_binding_paths: set[str] = set()
    for index, binding in enumerate(bindings):
        if not isinstance(binding, dict):
            errors.append(f"current source binding {index} is not an object")
            continue
        path = binding.get("path")
        expected_digest = binding.get("sha256")
        if not isinstance(path, str) or path in seen_binding_paths:
            errors.append(f"current source binding {index}: invalid or duplicate path {path!r}")
            continue
        seen_binding_paths.add(path)
        if not isinstance(expected_digest, str):
            errors.append(f"current source binding {path}: sha256 is required")
            continue
        try:
            expect_equal(
                errors,
                sha256_file(safe_regular_file(root, path)),
                expected_digest,
                f"current source binding {path}",
            )
        except Exception as exc:
            errors.append(f"current source binding {path}: {exc}")

    observations = ledger.get("bounded_exterior_observations", [])
    expect(errors, isinstance(observations, list) and len(observations) == 1, "one bounded exterior observation required")
    if isinstance(observations, list) and observations:
        observation = observations[0]
        expect_equal(errors, observation.get("path"), AUDIT_PATH.as_posix(), "Claude observation path")
        expect_equal(errors, observation.get("observed_coordinate"), MAIN_AUDIT_COMMIT, "Claude observation coordinate")
        expect_equal(errors, observation.get("state_change_admitted"), False, "Claude observation state-change effect")
        expect_equal(errors, observation.get("triggers_successor_projection"), False, "Claude observation successor effect")
        try:
            expect_equal(
                errors,
                sha256_file(safe_regular_file(root, observation.get("path"))),
                observation.get("sha256"),
                "Claude observation sha256",
            )
        except Exception as exc:
            errors.append(f"Claude observation: {exc}")

    try:
        readme = safe_regular_file(root, "README.md").read_text(encoding="utf-8")
        required_front_door_text = (
            "FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING:START",
            MAIN_AUDIT_COMMIT,
            GOVERNED_COMMIT,
            CURRENT_PATH.as_posix(),
            HISTORICAL_PATH.as_posix(),
        )
        for value in required_front_door_text:
            expect(errors, value in readme, f"README temporal route missing: {value}")
    except Exception as exc:
        errors.append(f"README temporal route: {exc}")

    try:
        summary = safe_regular_file(
            root, "docs/state/FORK_PROOF_SURFACE_STATE_SUMMARY_v0_1.md"
        ).read_text(encoding="utf-8")
        expect(
            errors,
            "HISTORICAL_PROJECTION" in summary and CURRENT_PATH.as_posix() in summary,
            "July 11 summary must route to its successor current projection",
        )
    except Exception as exc:
        errors.append(f"July 11 summary: {exc}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    errors = check(args.repo_root)
    payload = {
        "checker": "temporal_succession_v0_1",
        "governed_coordinate": GOVERNED_COMMIT,
        "historical_projection_sha256": HISTORICAL_SHA256,
        "status": "TEMPORAL_SUCCESSION_CONFORMS" if not errors else "TEMPORAL_SUCCESSION_INVALID",
        "finding_count": len(errors),
        "findings": errors,
        "interpretation": {
            "proves": [
                "declared projection and event bytes match their ledger bindings",
                "the July 11 projection remains byte-identical",
                "declared later admitted state-changing events have successor reconciliation",
                "the public front door routes historical and governed branch standing explicitly",
            ],
            "does_not_prove": [
                "that the event registry is complete",
                "truth",
                "correctness",
                "causality",
                "authority",
                "approval",
                "compliance",
                "legal sufficiency",
                "safety",
                "production readiness",
                "execution permission",
            ],
        },
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif errors:
        print(payload["status"])
        for error in errors:
            print(f"- {error}")
    else:
        print(payload["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
