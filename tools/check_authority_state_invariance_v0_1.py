#!/usr/bin/env python3
"""Check Fork Authority State Invariance and Transition Model v0.1 fixtures."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install jsonschema: python -m pip install jsonschema") from exc

CHECKER_VERSION = "AUTHORITY_STATE_INVARIANCE_CHECKER_v0_1"
VALIDITY_TRANSITIONS = {
    "REVALIDATED_CURRENT": "CURRENT",
    "MARKED_EXPIRED": "EXPIRED",
    "MARKED_SUPERSEDED": "SUPERSEDED",
    "MARKED_UNRESOLVED": "UNRESOLVED",
}
AUTHORITY_TRANSITIONS = {
    "GRANTED": "ACTIVE",
    "NARROWED": "ACTIVE",
    "EXPIRED": "EXPIRED",
    "REVOKED": "REVOKED",
    "SUPERSEDED": "SUPERSEDED",
}
SCHEMA_PATHS = {
    "validity_state_transition_event": Path("schemas/validity_state_transition_event_v0_1.schema.json"),
    "authority_transition_event": Path("schemas/authority_transition_event_v0_1.schema.json"),
    "reliance_event": Path("schemas/reliance_event_v0_1.schema.json"),
    "reliance_authority_misalignment_event": Path("schemas/reliance_authority_misalignment_event_v0_1.schema.json"),
}


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def schema_errors(schema: dict[str, Any], value: Any) -> list[str]:
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    ]


def governance_evaluation(event: dict[str, Any], validity: str, authority: dict[str, Any]) -> str:
    profile = event["governance_profile"]
    if profile is None:
        return "NOT_EVALUABLE"
    satisfied = (
        event["observed_reliance_class"] in profile["required_reliance_classes"]
        and authority["status"] in profile["required_authority_statuses"]
        and validity in profile["required_validity_states"]
        and event["observed_context_ref"] in profile["required_context_refs"]
    )
    return "SATISFIED" if satisfied else "NOT_SATISFIED"


def lineage_metrics(lineage: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    root_ids = set(lineage["root_claim_ids"])
    refs = lineage["apparent_supporting_references"]
    validations = lineage["independent_validation_records"]
    bad_ref_roots = sorted({item["root_claim_id"] for item in refs} - root_ids)
    bad_validation_roots = sorted({item["root_claim_id"] for item in validations} - root_ids)
    if bad_ref_roots or bad_validation_roots:
        errors.append("LINEAGE_ROOT_REFERENCE_UNRESOLVED")
    validation_ids = {item["validation_id"] for item in validations}
    independently_validated_roots = {item["root_claim_id"] for item in validations}
    actual_validation_count = len(validation_ids)
    actual_root_count = len(independently_validated_roots)
    if lineage["independent_validation_count"] != actual_validation_count:
        errors.append("INDEPENDENT_VALIDATION_COUNT_MISMATCH")
    if lineage["declared_independent_root_count"] != actual_root_count:
        errors.append("INDEPENDENT_ROOT_COUNT_MISMATCH")
    d = lineage["derivation_depth"]
    vc = actual_validation_count
    r = len(refs)
    ri = actual_root_count
    metrics = {
        "derivation_depth": d,
        "independent_validation_count": vc,
        "validation_chain_depth": lineage["validation_chain_depth"],
        "independently_validated_root_count": ri,
        "apparent_supporting_reference_count": r,
        "dvg": d - vc,
        "dvr": d / max(1, vc),
        "pci_count": r - ri,
        "pci_ratio": r / max(1, ri),
    }
    return metrics, sorted(set(errors))


def evaluate_case(root: Path, case_path: Path) -> dict[str, Any]:
    case = load_json(case_path)
    errors: list[dict[str, str]] = []
    emitted: list[dict[str, Any]] = []

    def add(code: str, detail: str) -> None:
        errors.append({"code": code, "detail": detail})

    required_case = {"case_version", "case_id", "description", "source_claim", "events", "expected"}
    missing = sorted(required_case - set(case))
    if missing:
        add("CASE_STRUCTURE_INVALID", f"missing fields: {', '.join(missing)}")
        return _finish(case_path, case, errors, emitted)

    source = case["source_claim"]
    for field in ("claim_id", "validity_state", "authority_state", "permitted_reliance_classes", "permitted_context_refs", "non_claims"):
        if field not in source:
            add("CASE_STRUCTURE_INVALID", f"source_claim missing {field}")
    if errors:
        return _finish(case_path, case, errors, emitted)

    schemas = {name: load_json(root / path) for name, path in SCHEMA_PATHS.items()}
    validity = source["validity_state"]
    authority = deepcopy(source["authority_state"])

    for index, event in enumerate(case["events"]):
        family = event.get("event_family")
        if family not in ("validity_state_transition_event", "authority_transition_event", "reliance_event"):
            add("EVENT_FAMILY_UNKNOWN", f"event {index}: {family!r}")
            continue
        for message in schema_errors(schemas[family], event):
            add("SCHEMA_VALIDATION_FAILED", f"event {index}: {message}")
        if any(item["code"] == "SCHEMA_VALIDATION_FAILED" and item["detail"].startswith(f"event {index}:") for item in errors):
            continue
        if event["claim_id"] != source["claim_id"]:
            add("CLAIM_ID_MISMATCH", f"event {event['event_id']} references {event['claim_id']}")

        if family == "validity_state_transition_event":
            if event["prior_validity_state"] != validity:
                add("VALIDITY_PRIOR_STATE_MISMATCH", event["event_id"])
            expected_result = VALIDITY_TRANSITIONS[event["event_type"]]
            if event["resulting_validity_state"] != expected_result:
                add("VALIDITY_TRANSITION_INVALID", event["event_id"])
            if canonical(event["authority_state_before"]) != canonical(authority):
                add("VALIDITY_EVENT_AUTHORITY_BEFORE_MISMATCH", event["event_id"])
            if canonical(event["authority_state_before"]) != canonical(event["authority_state_after"]):
                add("REVALIDATION_GRANTS_AUTHORITY", event["event_id"])
            validity = event["resulting_validity_state"]

        elif family == "authority_transition_event":
            if canonical(event["prior_authority_state"]) != canonical(authority):
                add("AUTHORITY_PRIOR_STATE_MISMATCH", event["event_id"])
            expected_status = AUTHORITY_TRANSITIONS[event["event_type"]]
            if event["resulting_authority_state"]["status"] != expected_status:
                add("AUTHORITY_TRANSITION_INVALID", event["event_id"])
            if event["validity_state_before"] != validity or event["validity_state_after"] != validity:
                add("AUTHORITY_EVENT_ALTERS_VALIDITY", event["event_id"])
            if event["event_type"] == "GRANTED" and not event["resulting_authority_state"]["permitted_reliance_classes"]:
                add("AUTHORITY_GRANT_SCOPE_EMPTY", event["event_id"])
            if event["event_type"] == "NARROWED":
                prior = set(event["prior_authority_state"]["permitted_reliance_classes"])
                result = set(event["resulting_authority_state"]["permitted_reliance_classes"])
                if not result < prior:
                    add("AUTHORITY_NARROWING_INVALID", event["event_id"])
            authority = deepcopy(event["resulting_authority_state"])

        else:
            if event["validity_state_before"] != validity:
                add("RELIANCE_VALIDITY_BEFORE_MISMATCH", event["event_id"])
            if event["validity_state_after"] != event["validity_state_before"]:
                add("RELIANCE_ALTERS_VALIDITY", event["event_id"])
            if canonical(event["authority_state_before"]) != canonical(authority):
                add("RELIANCE_AUTHORITY_BEFORE_MISMATCH", event["event_id"])
            if canonical(event["authority_state_after"]) != canonical(event["authority_state_before"]):
                add("RELIANCE_ALTERS_AUTHORITY", event["event_id"])

            validity_ok = validity in event["accepted_validity_states"]
            permitted_class_ok = event["observed_reliance_class"] in event["claim_permitted_reliance_classes"]
            permitted_context_ok = event["observed_context_ref"] in event["claim_permitted_context_refs"]
            permitted_ok = permitted_class_ok and permitted_context_ok
            authority_class_ok = (
                authority["status"] == "ACTIVE"
                and event["observed_reliance_class"] in authority["permitted_reliance_classes"]
            )
            authority_context_ok = event["observed_context_ref"] in authority["context_refs"]
            authority_ok = authority_class_ok and authority_context_ok
            gov = governance_evaluation(event, validity, authority)
            if gov != event["declared_governance_profile_evaluation"]:
                add("GOVERNANCE_PROFILE_EVALUATION_MISMATCH", event["event_id"])
            source_non_claims = set(event["source_non_claims"])
            observed_non_claims = set(event["observed_non_claims"])
            non_claim_ok = source_non_claims.issubset(observed_non_claims)
            metrics, lineage_errors = lineage_metrics(event["lineage"])
            lineage_ok = not lineage_errors

            dimensions: list[str] = []
            if not validity_ok:
                dimensions.append("VALIDITY_STATE")
                add("VALIDITY_STATE_MISALIGNMENT", event["event_id"])
            if not permitted_ok:
                dimensions.append("PERMITTED_RELIANCE")
                if not permitted_class_ok:
                    add("PERMITTED_RELIANCE_MISALIGNMENT", event["event_id"])
                if not permitted_context_ok:
                    add("CLAIM_CONTEXT_MISALIGNMENT", event["event_id"])
            if not authority_ok:
                dimensions.append("AUTHORITY_SCOPE")
                if not authority_class_ok:
                    add("AUTHORITY_SCOPE_MISALIGNMENT", event["event_id"])
                if not authority_context_ok:
                    add("AUTHORITY_CONTEXT_MISALIGNMENT", event["event_id"])
            if gov == "NOT_SATISFIED":
                dimensions.append("GOVERNANCE_PROFILE")
                add("GOVERNANCE_PROFILE_NOT_SATISFIED", event["event_id"])
            if not non_claim_ok:
                dimensions.append("NON_CLAIM_SURVIVAL")
                add("NON_CLAIM_LOSS", event["event_id"])
            if not lineage_ok:
                dimensions.append("LINEAGE_INDEPENDENCE")
                for code in lineage_errors:
                    add(code, event["event_id"])
            if event["fork_enforcement_action"] != "NONE":
                add("FORK_ENFORCEMENT_ACTION_PRESENT", event["event_id"])

            misalignment = {
                "schema_version": "v0.1",
                "event_family": "reliance_authority_misalignment_event",
                "event_id": f"misalignment::{event['event_id']}",
                "source_reliance_event_id": event["event_id"],
                "claim_id": event["claim_id"],
                "computed_at": "2026-07-11T00:00:00Z",
                "checker_version": CHECKER_VERSION,
                "validity_state_compatible": validity_ok,
                "permitted_reliance_compatible": permitted_ok,
                "authority_scope_compatible": authority_ok,
                "governance_profile_evaluation": gov,
                "non_claim_survival_compatible": non_claim_ok,
                "lineage_independence_compatible": lineage_ok,
                "structural_misalignment_detected": bool(dimensions),
                "misalignment_dimensions": dimensions,
                "lineage_metrics": metrics,
                "fork_enforcement_action": "NONE",
            }
            for message in schema_errors(schemas["reliance_authority_misalignment_event"], misalignment):
                add("EMITTED_MISALIGNMENT_SCHEMA_INVALID", message)
            emitted.append(misalignment)

    return _finish(case_path, case, errors, emitted)


def _finish(case_path: Path, case: dict[str, Any], errors: list[dict[str, str]], emitted: list[dict[str, Any]]) -> dict[str, Any]:
    unique = []
    seen = set()
    for item in errors:
        key = (item["code"], item["detail"])
        if key not in seen:
            unique.append(item)
            seen.add(key)
    codes = sorted({item["code"] for item in unique})
    return {
        "case_file": case_path.as_posix(),
        "case_id": case.get("case_id", "<unknown>"),
        "structurally_conformant": not unique,
        "error_codes": codes,
        "errors": unique,
        "emitted_misalignment_events": emitted,
        "expected": case.get("expected"),
    }


def evaluate_repository(root: Path) -> dict[str, Any]:
    base = root / "tests/fixtures/authority-state-invariance"
    valid_paths = sorted((base / "valid").glob("case_*.json"))
    invalid_paths = sorted((base / "invalid").glob("case_*.json"))
    valid_results = [evaluate_case(root, path) for path in valid_paths]
    invalid_results = [evaluate_case(root, path) for path in invalid_paths]
    harness: list[dict[str, Any]] = []
    for result in valid_results + invalid_results:
        expected = result.get("expected") or {}
        expected_conformant = expected.get("structurally_conformant")
        expected_codes = sorted(expected.get("error_codes", []))
        actual_codes = result["error_codes"]
        ok = result["structurally_conformant"] == expected_conformant and actual_codes == expected_codes
        harness.append({
            "case_id": result["case_id"],
            "ok": ok,
            "expected_structurally_conformant": expected_conformant,
            "actual_structurally_conformant": result["structurally_conformant"],
            "expected_error_codes": expected_codes,
            "actual_error_codes": actual_codes,
        })
    failed = [item for item in harness if not item["ok"]]
    return {
        "checker": Path(__file__).name,
        "checker_version": CHECKER_VERSION,
        "valid_case_count": len(valid_results),
        "invalid_case_count": len(invalid_results),
        "harness_passed": not failed and bool(valid_results) and bool(invalid_results),
        "harness": harness,
        "results": valid_results + invalid_results,
        "interpretation": {
            "proves": [
                "governed fixtures satisfy or fail the declared structural invariants as expected",
                "event records are validated against the module schemas",
                "component misalignment results and lineage indicators are recomputable",
            ],
            "does_not_prove": [
                "truth", "compliance", "legal sufficiency", "authority-basis sufficiency",
                "permission to execute", "answerability", "liability", "production readiness",
                "certification", "endorsement",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", nargs="?", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()
    root = repo_root(args.root)
    if args.fixture:
        path = args.fixture if args.fixture.is_absolute() else root / args.fixture
        result = evaluate_case(root, path)
        exit_code = 0 if result["structurally_conformant"] else 1
    else:
        result = evaluate_repository(root)
        exit_code = 0 if result["harness_passed"] else 1
    if args.write_receipt:
        receipt_path = args.write_receipt if args.write_receipt.is_absolute() else root / args.write_receipt
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        if args.fixture:
            print("AUTHORITY_STATE_INVARIANCE_CASE_PASS" if exit_code == 0 else "AUTHORITY_STATE_INVARIANCE_CASE_FAIL")
            print(", ".join(result["error_codes"]) or "no errors")
        else:
            for item in result["harness"]:
                print(f"[{'PASS' if item['ok'] else 'FAIL'}] {item['case_id']}")
            print("AUTHORITY_STATE_INVARIANCE_HARNESS_PASS" if exit_code == 0 else "AUTHORITY_STATE_INVARIANCE_HARNESS_FAIL")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
