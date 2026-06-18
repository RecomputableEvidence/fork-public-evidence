#!/usr/bin/env python3
"""
Fork claim inheritance simulation model checker v0.1.

This checker is intentionally structural. It does not decide truth, safety,
legal sufficiency, admissibility, compliance, authority validity, retention
compliance, legal chain of custody, legal reliance, legal representation,
medical correctness, production readiness, or actual undisclosed downstream
behavior.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


VALID_BUNDLE = Path(
    "examples/claim_inheritance_simulation_model/"
    "synthetic_claim_inheritance_simulation_bundle_v0_1.json"
)

INVALID_MANIFEST = Path(
    "examples/claim_inheritance_simulation_model/invalid/"
    "manifest_invalid_fixtures_v0_1.json"
)

EXPECTED_COVERAGE = [
    "SIM_A_BOUNDARY_PRESERVED",
    "SIM_B_BOUNDARY_NARROWED",
    "SIM_C_NON_CLAIM_DROPPED",
    "SIM_D_EXPANSION_WITHOUT_AUTHORITY",
    "SIM_E_EXPANSION_WITH_RECORDED_UNRESOLVED_AUTHORITY",
    "SIM_F_POINTER_UNRESOLVED",
    "SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED",
    "SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED",
    "SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED",
    "SIM_H_CASCADING_INHERITANCE",
    "SIM_I_BOUNDARY_REJECTION",
    "SIM_J_SCHEMA_BEHAVIOR_COLLAPSE",
    "SIM_K_MULTI_BEHAVIOR_HANDOFF",
    "SIM_L_STRUCTURALLY_VALID_MISLEADING_SELF_REPORT",
    "SIM_M_AGGREGATE_COLLAPSE",
]

EXPECTED_PRECEDENCE = [
    "NO_MAPPING_PRESENT_PRECEDENCE",
    "AGGREGATE_COLLAPSE_PRECEDENCE",
    "INCOMPLETE_MAPPING_PRECEDENCE",
    "UNRESOLVED_REFERENCES_PRECEDENCE",
    "EXPANSION_MAPPING_PRESENT_PRECEDENCE",
    "BOUNDARY_MAPPING_COMPLETE_PRECEDENCE",
    "STRUCTURAL_CONFORMANCE_CONFIRMED_PRECEDENCE",
]

BANNED_DOMAIN_TOKENS = [
    "approved",
    "authorized",
    "compliant",
    "production_ready",
    "hipaa",
    "legal_sufficient",
    "clinical_necessity",
    "medically_appropriate",
    "legal_approval_granted",
]

INCOMPLETE_OUTCOMES = {
    "MAPPING_INCOMPLETE",
    "AUTHORITY_REF_MISSING",
    "EVIDENCE_REF_MISSING",
    "NON_CLAIM_DROPPED",
    "DECLARED_BEHAVIOR_MISMATCH_DETECTED",
    "SCHEMA_BEHAVIOR_COLLAPSE_DETECTED",
}

UNRESOLVED_OUTCOMES = {
    "POINTER_UNRESOLVED",
    "MAPPED_WITH_UNRESOLVED_REFERENCES",
    "AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
    "EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
    "AUTHORITY_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
    "EVIDENCE_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
}

EXPANSION_OUTCOMES = {
    "BOUNDARY_EXPANSION_DETECTED",
    "BOUNDARY_EXPANSION_RECORDED",
}

POSITIVE_AGGREGATES = {
    "BOUNDARY_MAPPING_COMPLETE",
    "STRUCTURAL_CONFORMANCE_CONFIRMED",
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def add_error(errors: List[Dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append(
        {
            "code": code,
            "path": path,
            "message": message,
        }
    )


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def string_values(obj: Any, path: str = "$") -> Iterable[Tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from string_values(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from string_values(value, f"{path}[{index}]")
    elif isinstance(obj, str):
        yield path, obj


def collect_case_outcomes(case: Dict[str, Any]) -> Set[str]:
    outcomes: Set[str] = set(as_list(case.get("expected_structural_outcomes")))
    for record in as_list(case.get("boundary_behavior_records")):
        if isinstance(record, dict):
            outcomes.update(as_list(record.get("structural_outcomes")))

    aggregate_report = case.get("aggregate_report")
    if isinstance(aggregate_report, dict):
        outcomes.update(as_list(aggregate_report.get("included_structural_outcomes")))
        outcomes.update(as_list(aggregate_report.get("omitted_structural_outcomes")))
        if aggregate_report.get("aggregate_collapse_detected") is True:
            outcomes.add("AGGREGATE_COLLAPSE_DETECTED")

    return {str(outcome) for outcome in outcomes if isinstance(outcome, str)}


def computed_aggregate_posture(case: Dict[str, Any]) -> str:
    outcomes = collect_case_outcomes(case)
    aggregate_report = case.get("aggregate_report")

    if "AGGREGATE_COLLAPSE_DETECTED" in outcomes:
        return "AGGREGATE_COLLAPSE_DETECTED"

    if isinstance(aggregate_report, dict):
        omitted = as_list(aggregate_report.get("omitted_structural_outcomes"))
        if omitted:
            return "AGGREGATE_COLLAPSE_DETECTED"

    if outcomes.intersection(INCOMPLETE_OUTCOMES):
        return "INCOMPLETE_MAPPING"

    if outcomes.intersection(UNRESOLVED_OUTCOMES):
        return "MAPPED_WITH_UNRESOLVED_REFERENCES"

    if outcomes.intersection(EXPANSION_OUTCOMES):
        return "EXPANSION_MAPPING_PRESENT"

    if "STRUCTURAL_CONFORMANCE_CONFIRMED" in outcomes:
        return "STRUCTURAL_CONFORMANCE_CONFIRMED"

    if "BOUNDARY_MAPPING_COMPLETE" in outcomes:
        return "BOUNDARY_MAPPING_COMPLETE"

    if not as_list(case.get("boundary_behavior_records")):
        return "NO_MAPPING_PRESENT"

    return "BOUNDARY_MAPPING_COMPLETE"


def check_top_level(bundle: Dict[str, Any], errors: List[Dict[str, str]]) -> None:
    required = [
        "simulation_model_id",
        "schema_version",
        "status",
        "controlled_vocabulary_schema_ref",
        "controlled_vocabulary_baseline",
        "synthetic_only",
        "domain_process",
        "mandatory_non_claims",
        "simulation_class_coverage",
        "aggregate_posture_precedence",
        "simulation_cases",
    ]

    for field in required:
        if field not in bundle:
            add_error(errors, "MISSING_REQUIRED_FIELD", f"$.{field}", "Missing top-level field.")

    if bundle.get("simulation_model_id") != "claim_inheritance_simulation_model_v0_1":
        add_error(
            errors,
            "UNEXPECTED_SIMULATION_MODEL_ID",
            "$.simulation_model_id",
            "Unexpected simulation_model_id.",
        )

    if bundle.get("controlled_vocabulary_baseline") != "fork-controlled-vocabulary-hardening-v0.1.1":
        add_error(
            errors,
            "UNEXPECTED_CONTROLLED_VOCABULARY_BASELINE",
            "$.controlled_vocabulary_baseline",
            "Unexpected controlled vocabulary baseline.",
        )

    if bundle.get("synthetic_only") is not True:
        add_error(errors, "SYNTHETIC_ONLY_REQUIRED", "$.synthetic_only", "synthetic_only must be true.")

    if bundle.get("domain_process") != "DOMAIN_NEUTRAL_SYNTHETIC":
        add_error(
            errors,
            "DOMAIN_NEUTRAL_SYNTHETIC_REQUIRED",
            "$.domain_process",
            "domain_process must be DOMAIN_NEUTRAL_SYNTHETIC.",
        )

    mandatory_non_claims = as_list(bundle.get("mandatory_non_claims"))
    if not mandatory_non_claims:
        add_error(errors, "MANDATORY_NON_CLAIMS_MISSING", "$.mandatory_non_claims", "mandatory_non_claims must be non-empty.")

    coverage = as_list(bundle.get("simulation_class_coverage"))
    for cls in EXPECTED_COVERAGE:
        if cls not in coverage:
            add_error(errors, "SIMULATION_CLASS_COVERAGE_MISSING", "$.simulation_class_coverage", f"Missing coverage class {cls}.")

    precedence = as_list(bundle.get("aggregate_posture_precedence"))
    if precedence != EXPECTED_PRECEDENCE:
        add_error(
            errors,
            "AGGREGATE_PRECEDENCE_ORDER_MISMATCH",
            "$.aggregate_posture_precedence",
            "Aggregate posture precedence does not match canonical order.",
        )


def check_banned_tokens(bundle: Dict[str, Any], errors: List[Dict[str, str]]) -> None:
    for path, value in string_values(bundle):
        lower = value.lower()
        for token in BANNED_DOMAIN_TOKENS:
            pattern = r"(?<![a-z0-9_])" + re.escape(token) + r"(?![a-z0-9_])"
            if re.search(pattern, lower):
                add_error(
                    errors,
                    "BANNED_DOMAIN_OUTCOME_TOKEN",
                    path,
                    f"Banned synthetic-domain token detected: {token}",
                )
                add_error(
                    errors,
                    "SYNTHETIC_DOMAIN_NEUTRALITY_VIOLATION",
                    path,
                    "Synthetic fixture contains domain outcome or compliance-adjacent language.",
                )


def check_record(
    case: Dict[str, Any],
    simulation_class: str,
    record: Dict[str, Any],
    errors: List[Dict[str, str]],
    path: str,
) -> None:
    required = [
        "claim_ref",
        "claim_relationship_state",
        "consumer_declared_boundary_behavior",
        "validator_observed_boundary_behavior",
        "preserved_non_claims",
        "dropped_non_claims",
        "structural_outcomes",
    ]

    for field in required:
        if field not in record:
            add_error(errors, "MISSING_REQUIRED_FIELD", f"{path}.{field}", "Missing boundary record field.")

    relationship = record.get("claim_relationship_state")
    declared = record.get("consumer_declared_boundary_behavior")
    observed = record.get("validator_observed_boundary_behavior")
    outcomes = set(as_list(record.get("structural_outcomes")))
    dropped_non_claims = as_list(record.get("dropped_non_claims"))
    authority_refs = as_list(record.get("authority_refs"))
    evidence_refs = as_list(record.get("evidence_refs"))

    mismatch_required = simulation_class in {
        "SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED",
        "SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED",
        "SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED",
    }

    if mismatch_required and declared != observed:
        if "DECLARED_BEHAVIOR_MISMATCH_DETECTED" not in outcomes:
            add_error(
                errors,
                "DECLARED_BEHAVIOR_MISMATCH_DETECTED",
                path,
                "Self-characterization case differs from validator-observed behavior without mismatch outcome.",
            )
        if "MAPPING_INCOMPLETE" not in outcomes:
            add_error(
                errors,
                "MAPPING_INCOMPLETE",
                path,
                "Self-characterization mismatch must force incomplete mapping visibility.",
            )

    if observed == "NON_CLAIM_DROPPED" or dropped_non_claims:
        if not dropped_non_claims:
            add_error(
                errors,
                "NON_CLAIM_SILENTLY_OMITTED",
                f"{path}.dropped_non_claims",
                "Non-claim loss must be explicitly represented in dropped_non_claims.",
            )
        if "NON_CLAIM_DROPPED" not in outcomes:
            add_error(errors, "NON_CLAIM_DROPPED", path, "Dropped non-claim must emit NON_CLAIM_DROPPED.")
        if "MAPPING_INCOMPLETE" not in outcomes:
            add_error(errors, "MAPPING_INCOMPLETE", path, "Dropped non-claim must emit MAPPING_INCOMPLETE.")

    if observed == "BOUNDARY_EXPANSION_DETECTED":
        if "BOUNDARY_EXPANSION_DETECTED" not in outcomes:
            add_error(errors, "BOUNDARY_EXPANSION_DETECTED", path, "Expansion must remain visible.")

        if relationship == "CLAIM_REFERENCED":
            add_error(
                errors,
                "CLAIM_REFERENCE_SUPPORT_COLLAPSE",
                path,
                "A referenced claim is being treated as support-like expansion.",
            )
            add_error(
                errors,
                "BOUNDARY_EXPANSION_DETECTED",
                path,
                "Reference-only relationship cannot silently carry support-like expansion.",
            )
            add_error(errors, "MAPPING_INCOMPLETE", path, "Reference/support collapse must be incomplete.")

        if not authority_refs:
            if "AUTHORITY_REF_MISSING" not in outcomes:
                add_error(errors, "AUTHORITY_REF_MISSING", path, "Expansion without authority refs must emit AUTHORITY_REF_MISSING.")
            if "MAPPING_INCOMPLETE" not in outcomes:
                add_error(errors, "MAPPING_INCOMPLETE", path, "Expansion without authority refs must be incomplete.")

        if not evidence_refs:
            if "EVIDENCE_REF_MISSING" not in outcomes:
                add_error(errors, "EVIDENCE_REF_MISSING", path, "Expansion without evidence refs must emit EVIDENCE_REF_MISSING.")
            if "MAPPING_INCOMPLETE" not in outcomes:
                add_error(errors, "MAPPING_INCOMPLETE", path, "Expansion without evidence refs must be incomplete.")

    if relationship == "CLAIM_NON_USAGE_DECLARED" and observed not in {"BOUNDARY_PRESERVED", "CLAIM_REJECTED"}:
        add_error(
            errors,
            "CLAIM_NON_USAGE_DECLARED_TREATED_AS_PROVEN_NON_USE",
            path,
            "Declared non-usage must not be treated as verified actual non-use.",
        )
        if "DECLARED_BEHAVIOR_MISMATCH_DETECTED" not in outcomes:
            add_error(
                errors,
                "DECLARED_BEHAVIOR_MISMATCH_DETECTED",
                path,
                "Declared non-usage conflicts with observed behavior.",
            )
        if "MAPPING_INCOMPLETE" not in outcomes:
            add_error(errors, "MAPPING_INCOMPLETE", path, "Declared non-usage conflict must be incomplete.")

    if observed == "POINTER_UNRESOLVED" or "POINTER_UNRESOLVED" in outcomes:
        if "MAPPED_WITH_UNRESOLVED_REFERENCES" not in outcomes:
            add_error(
                errors,
                "MAPPED_WITH_UNRESOLVED_REFERENCES",
                path,
                "Unresolved pointer must propagate into unresolved aggregate visibility.",
            )

    expansion_present = observed in {"BOUNDARY_EXPANSION_DETECTED", "BOUNDARY_EXPANSION_RECORDED"} or bool(
        outcomes.intersection(EXPANSION_OUTCOMES)
    )

    authority_reachable = any(
        isinstance(ref, dict)
        and ref.get("authority_ref_resolution_state") == "AUTHORITY_REF_STRUCTURALLY_REACHABLE"
        for ref in authority_refs
    )
    evidence_reachable = any(
        isinstance(ref, dict)
        and ref.get("evidence_ref_resolution_state") == "EVIDENCE_REF_STRUCTURALLY_REACHABLE"
        for ref in evidence_refs
    )

    if expansion_present and "STRUCTURAL_CONFORMANCE_CONFIRMED" in outcomes and authority_reachable:
        add_error(
            errors,
            "STRUCTURALLY_REACHABLE_TREATED_AS_AUTHORITY_VALID",
            path,
            "Structurally reachable authority ref is being promoted to structural conformance for an expanded claim.",
        )

    if expansion_present and "STRUCTURAL_CONFORMANCE_CONFIRMED" in outcomes and evidence_reachable:
        add_error(
            errors,
            "STRUCTURALLY_REACHABLE_TREATED_AS_EVIDENCE_SUFFICIENT",
            path,
            "Structurally reachable evidence ref is being promoted to structural conformance for an expanded claim.",
        )


def check_case(case: Dict[str, Any], index: int, errors: List[Dict[str, str]]) -> None:
    path = f"$.simulation_cases[{index}]"
    simulation_class = case.get("simulation_class")

    required = [
        "simulation_case_id",
        "simulation_class",
        "synthetic_only",
        "domain_process",
        "objective",
        "input_claims",
        "handoff_events",
        "boundary_behavior_records",
        "expected_structural_outcomes",
        "expected_aggregate_posture",
        "expected_precedence_trigger",
        "non_claims",
    ]

    for field in required:
        if field not in case:
            add_error(errors, "MISSING_REQUIRED_FIELD", f"{path}.{field}", "Missing simulation case field.")

    if case.get("synthetic_only") is not True:
        add_error(errors, "SYNTHETIC_ONLY_REQUIRED", f"{path}.synthetic_only", "simulation case must be synthetic-only.")

    if case.get("domain_process") != "DOMAIN_NEUTRAL_SYNTHETIC":
        add_error(
            errors,
            "DOMAIN_NEUTRAL_SYNTHETIC_REQUIRED",
            f"{path}.domain_process",
            "simulation case must be domain-neutral synthetic.",
        )

    if not as_list(case.get("non_claims")):
        add_error(errors, "MANDATORY_NON_CLAIMS_MISSING", f"{path}.non_claims", "simulation case non_claims must be non-empty.")

    claims = as_list(case.get("input_claims"))
    records = as_list(case.get("boundary_behavior_records"))

    if not records:
        add_error(
            errors,
            "MISSING_BOUNDARY_BEHAVIOR_RECORD",
            f"{path}.boundary_behavior_records",
            "Each simulation case must include at least one boundary behavior record.",
        )
        add_error(errors, "MAPPING_INCOMPLETE", path, "Missing boundary behavior records force incomplete mapping.")

    claim_ids = {
        claim.get("claim_id")
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    record_claim_refs = {
        record.get("claim_ref")
        for record in records
        if isinstance(record, dict) and isinstance(record.get("claim_ref"), str)
    }

    for claim_id in sorted(claim_ids):
        if claim_id not in record_claim_refs:
            add_error(
                errors,
                "MISSING_BOUNDARY_BEHAVIOR_RECORD",
                f"{path}.boundary_behavior_records",
                f"Missing boundary_behavior_record for claim {claim_id}.",
            )
            add_error(errors, "MAPPING_INCOMPLETE", path, "Unmapped claim forces incomplete mapping.")

    for record_index, record in enumerate(records):
        if not isinstance(record, dict):
            add_error(errors, "INVALID_BOUNDARY_BEHAVIOR_RECORD", f"{path}.boundary_behavior_records[{record_index}]", "Record must be object.")
            continue
        check_record(case, str(simulation_class), record, errors, f"{path}.boundary_behavior_records[{record_index}]")

    outcomes = collect_case_outcomes(case)
    expected_posture = case.get("expected_aggregate_posture")
    computed_posture = computed_aggregate_posture(case)

    if expected_posture != computed_posture:
        add_error(
            errors,
            "AGGREGATE_POSTURE_PRECEDENCE_VIOLATION",
            f"{path}.expected_aggregate_posture",
            f"Expected aggregate posture {expected_posture!r} does not match computed posture {computed_posture!r}.",
        )

        if "POINTER_UNRESOLVED" in outcomes:
            add_error(
                errors,
                "POINTER_UNRESOLVED",
                path,
                "Unresolved pointer cannot be collapsed into a positive aggregate posture.",
            )

        if outcomes.intersection(UNRESOLVED_OUTCOMES):
            add_error(
                errors,
                "MAPPED_WITH_UNRESOLVED_REFERENCES",
                path,
                "Unresolved references must remain visible in aggregate posture.",
            )

        if "BOUNDARY_EXPANSION_DETECTED" in outcomes:
            add_error(
                errors,
                "BOUNDARY_EXPANSION_DETECTED",
                path,
                "Detected expansion cannot be collapsed into a positive aggregate posture.",
            )

        if computed_posture == "INCOMPLETE_MAPPING":
            add_error(
                errors,
                "MAPPING_INCOMPLETE",
                path,
                "Incomplete mapping cannot be collapsed into a positive aggregate posture.",
            )

    if simulation_class == "SIM_C_NON_CLAIM_DROPPED":
        if not any(as_list(record.get("dropped_non_claims")) for record in records if isinstance(record, dict)):
            add_error(
                errors,
                "NON_CLAIM_SILENTLY_OMITTED",
                path,
                "SIM_C requires explicit dropped_non_claims.",
            )
            add_error(errors, "NON_CLAIM_DROPPED", path, "SIM_C requires NON_CLAIM_DROPPED.")
            add_error(errors, "MAPPING_INCOMPLETE", path, "SIM_C non-claim drop must be incomplete.")

    if simulation_class == "SIM_D_EXPANSION_WITHOUT_AUTHORITY":
        required = {"AUTHORITY_REF_MISSING", "EVIDENCE_REF_MISSING", "MAPPING_INCOMPLETE"}
        missing = required.difference(outcomes)
        for code in sorted(missing):
            add_error(errors, code, path, f"SIM_D requires {code}.")

    if simulation_class == "SIM_M_AGGREGATE_COLLAPSE":
        aggregate_report = case.get("aggregate_report")
        if not isinstance(aggregate_report, dict):
            add_error(errors, "AGGREGATE_COLLAPSE_DETECTED", path, "SIM_M requires aggregate_report.")
            add_error(errors, "MAPPING_INCOMPLETE", path, "SIM_M without aggregate_report is incomplete.")
        else:
            if aggregate_report.get("aggregate_collapse_detected") is not True:
                add_error(
                    errors,
                    "AGGREGATE_COLLAPSE_DETECTED",
                    f"{path}.aggregate_report.aggregate_collapse_detected",
                    "SIM_M must preserve aggregate collapse detection.",
                )
                add_error(errors, "MAPPING_INCOMPLETE", path, "Aggregate collapse not surfaced forces incomplete mapping.")
            if case.get("expected_aggregate_posture") != "AGGREGATE_COLLAPSE_DETECTED":
                add_error(
                    errors,
                    "AGGREGATE_POSTURE_PRECEDENCE_VIOLATION",
                    f"{path}.expected_aggregate_posture",
                    "SIM_M must aggregate to AGGREGATE_COLLAPSE_DETECTED.",
                )


def check_bundle(bundle: Dict[str, Any], source: str = "<memory>") -> Dict[str, Any]:
    errors: List[Dict[str, str]] = []

    if not isinstance(bundle, dict):
        add_error(errors, "BUNDLE_NOT_OBJECT", "$", "Bundle must be a JSON object.")
        return {
            "ok": False,
            "source": source,
            "error_count": len(errors),
            "errors": errors,
        }

    check_top_level(bundle, errors)
    check_banned_tokens(bundle, errors)

    cases = as_list(bundle.get("simulation_cases"))
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            add_error(errors, "INVALID_SIMULATION_CASE", f"$.simulation_cases[{index}]", "Simulation case must be object.")
            continue
        check_case(case, index, errors)

    return {
        "ok": len(errors) == 0,
        "source": source,
        "error_count": len(errors),
        "errors": errors,
    }


def check_bundle_path(path: Path | str) -> Dict[str, Any]:
    path = Path(path)
    try:
        bundle = load_json(path)
    except ValueError as exc:
        return {
            "ok": False,
            "source": str(path),
            "error_count": 1,
            "errors": [
                {
                    "code": "INVALID_JSON",
                    "path": "$",
                    "message": str(exc),
                }
            ],
        }

    return check_bundle(bundle, source=str(path))


def check_invalid_manifest(manifest_path: Path | str = INVALID_MANIFEST) -> Dict[str, Any]:
    manifest_path = Path(manifest_path)
    manifest = load_json(manifest_path)
    base_dir = manifest_path.parent

    fixture_results = []
    all_ok = True

    for fixture in as_list(manifest.get("fixtures")):
        fixture_file = fixture.get("fixture_file")
        expected_failures = set(as_list(fixture.get("expected_failures")))
        result = check_bundle_path(base_dir / fixture_file)
        actual = {error["code"] for error in result["errors"]}
        missing = sorted(expected_failures.difference(actual))
        fixture_ok = (not result["ok"]) and not missing

        if not fixture_ok:
            all_ok = False

        fixture_results.append(
            {
                "fixture_file": fixture_file,
                "ok": fixture_ok,
                "checker_ok": result["ok"],
                "missing_expected_failures": missing,
                "actual_error_codes": sorted(actual),
            }
        )

    return {
        "ok": all_ok,
        "manifest": str(manifest_path),
        "fixture_results": fixture_results,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check Fork claim inheritance simulation bundles."
    )
    parser.add_argument(
        "bundle",
        nargs="?",
        default=str(VALID_BUNDLE),
        help="Path to a claim inheritance simulation bundle.",
    )
    parser.add_argument(
        "--invalid-manifest",
        action="store_true",
        help="Check the invalid fixture manifest instead of a single bundle.",
    )
    parser.add_argument(
        "--manifest-path",
        default=str(INVALID_MANIFEST),
        help="Path to invalid fixture manifest.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )

    args = parser.parse_args(argv)

    if args.invalid_manifest:
        result = check_invalid_manifest(Path(args.manifest_path))
    else:
        result = check_bundle_path(Path(args.bundle))

    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
