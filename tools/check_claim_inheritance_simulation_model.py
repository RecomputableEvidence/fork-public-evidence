#!/usr/bin/env python3
"""
Fork claim inheritance simulation model checker v0.1.1.

This checker is intentionally structural. It does not decide truth, safety,
legal sufficiency, admissibility, compliance, authority validity, retention
compliance, legal chain of custody, legal reliance, legal representation,
medical correctness, production readiness, or actual undisclosed downstream
behavior.

The checker performs dependency-free schema-conformance checks before semantic
boundary checks. JSON Schema library integration can be added later; this file
keeps the v0.1.1 checker runnable in a minimal Python environment.
"""

from __future__ import annotations

import argparse
import json
import re
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

TOP_REQUIRED = {
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
}

TOP_ALLOWED = set(TOP_REQUIRED)

CASE_REQUIRED = {
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
}

CASE_ALLOWED = CASE_REQUIRED.union(
    {
        "system_assertions",
        "aggregate_report",
        "notes",
    }
)

CLAIM_REQUIRED = {
    "claim_id",
    "claim_text",
    "claim_subject",
    "non_claims",
}

CLAIM_ALLOWED = set(CLAIM_REQUIRED)

ASSERTION_REQUIRED = {
    "assertion_id",
    "assertion_source",
    "assertion_text",
    "non_claims",
}

ASSERTION_ALLOWED = set(ASSERTION_REQUIRED)

HANDOFF_REQUIRED = {
    "handoff_event_id",
    "sender",
    "receiver",
    "timestamp",
    "artifact_ref",
    "record_structural_state",
    "recomputation_state",
    "non_claims",
}

HANDOFF_ALLOWED = set(HANDOFF_REQUIRED)

RECORD_REQUIRED = {
    "claim_ref",
    "claim_relationship_state",
    "consumer_declared_boundary_behavior",
    "validator_observed_boundary_behavior",
    "preserved_non_claims",
    "dropped_non_claims",
    "authority_refs",
    "evidence_refs",
    "structural_outcomes",
}

RECORD_ALLOWED = set(RECORD_REQUIRED)

AUTHORITY_REF_REQUIRED = {
    "authority_ref",
    "authority_ref_kind",
    "authority_ref_resolution_attempted",
    "authority_ref_resolution_state",
}

AUTHORITY_REF_ALLOWED = set(AUTHORITY_REF_REQUIRED)

EVIDENCE_REF_REQUIRED = {
    "evidence_ref",
    "evidence_ref_kind",
    "evidence_ref_resolution_attempted",
    "evidence_ref_resolution_state",
}

EVIDENCE_REF_ALLOWED = set(EVIDENCE_REF_REQUIRED)

AGGREGATE_REPORT_REQUIRED = {
    "aggregate_report_id",
    "receipt_refs",
    "reported_aggregate_posture",
    "expected_aggregate_posture",
    "included_structural_outcomes",
    "omitted_structural_outcomes",
    "aggregate_collapse_detected",
}

AGGREGATE_REPORT_ALLOWED = set(AGGREGATE_REPORT_REQUIRED)

BANNED_DOMAIN_TOKENS = [
    "approved",
    "authorized",
    "compliant",
    "production_ready",
    "production-ready",
    "hipaa",
    "legal_sufficient",
    "clinical_necessity",
    "clinically appropriate",
    "medically appropriate",
    "legal_approval_granted",
]

INCOMPLETE_OUTCOMES = {
    "MAPPING_INCOMPLETE",
    "AUTHORITY_REF_MISSING",
    "EVIDENCE_REF_MISSING",
    "NON_CLAIM_DROPPED",
    "NON_CLAIM_SILENTLY_OMITTED",
    "NON_CLAIM_TAMPERING_DETECTED",
    "DECLARED_BEHAVIOR_MISMATCH_DETECTED",
    "SCHEMA_BEHAVIOR_COLLAPSE_DETECTED",
    "PLACEHOLDER_REF_DETECTED",
    "RESOLUTION_ATTEMPT_STATE_CONTRADICTION",
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

ALLOWED_CLAIM_RELATIONSHIP_STATES = {
    "CLAIM_REFERENCED",
    "CLAIM_USED_AS_SUPPORT",
    "CLAIM_NON_USAGE_DECLARED",
    "CLAIM_RELATIONSHIP_NOT_DECLARED",
}

ALLOWED_BOUNDARY_BEHAVIORS = {
    "BOUNDARY_PRESERVED",
    "BOUNDARY_NARROWED",
    "BOUNDARY_EXPANSION_DETECTED",
    "BOUNDARY_EXPANSION_RECORDED",
    "NON_CLAIM_DROPPED",
    "POINTER_UNRESOLVED",
    "CLAIM_REJECTED",
    "SCHEMA_BEHAVIOR_COLLAPSE_DETECTED",
    "AGGREGATE_COLLAPSE_DETECTED",
    "BOUNDARY_MAPPING_PRESENT",
    "BOUNDARY_MAPPING_COMPLETE",
    "STRUCTURAL_CONFORMANCE_CONFIRMED",
}

ALLOWED_STRUCTURAL_OUTCOMES = {
    "AGGREGATE_COLLAPSE_DETECTED",
    "AUTHORITY_REF_MISSING",
    "AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
    "AUTHORITY_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
    "AUTHORITY_REF_STRUCTURALLY_REACHABLE",
    "BOUNDARY_EXPANSION_DETECTED",
    "BOUNDARY_EXPANSION_RECORDED",
    "BOUNDARY_MAPPING_COMPLETE",
    "BOUNDARY_MAPPING_PRESENT",
    "BOUNDARY_NARROWED",
    "BOUNDARY_PRESERVED",
    "CLAIM_REJECTED",
    "DECLARED_BEHAVIOR_MISMATCH_DETECTED",
    "EVIDENCE_REF_MISSING",
    "EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
    "EVIDENCE_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
    "EVIDENCE_REF_STRUCTURALLY_REACHABLE",
    "MAPPED_WITH_UNRESOLVED_REFERENCES",
    "MAPPING_INCOMPLETE",
    "NON_CLAIM_DROPPED",
    "POINTER_UNRESOLVED",
    "SCHEMA_BEHAVIOR_COLLAPSE_DETECTED",
    "STRUCTURAL_CONFORMANCE_CONFIRMED",
}

ALLOWED_AGGREGATE_POSTURES = {
    "NO_MAPPING_PRESENT",
    "AGGREGATE_COLLAPSE_DETECTED",
    "INCOMPLETE_MAPPING",
    "MAPPED_WITH_UNRESOLVED_REFERENCES",
    "EXPANSION_MAPPING_PRESENT",
    "BOUNDARY_MAPPING_COMPLETE",
    "STRUCTURAL_CONFORMANCE_CONFIRMED",
}

ALLOWED_PRECEDENCE_TRIGGERS = set(EXPECTED_PRECEDENCE)

PLACEHOLDER_REF_VALUES = {
    "tbd",
    "todo",
    "placeholder",
    "placeholder_ref",
    "pending",
    "unknown",
    "n/a",
    "na",
    "null",
    "none",
    "synthetic_placeholder",
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


def add_schema_error(errors: List[Dict[str, str]], code: str, path: str, message: str) -> None:
    add_error(errors, "SCHEMA_VALIDATION_FAILED", path, "Schema conformance failed.")
    add_error(errors, code, path, message)


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def is_non_blank_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_placeholder_ref_value(value: Any) -> bool:
    if not is_non_blank_string(value):
        return True

    normalized = str(value).strip().lower()
    normalized = re.sub(r"[^a-z0-9:/._-]+", "_", normalized)

    if normalized in PLACEHOLDER_REF_VALUES:
        return True

    if re.fullmatch(r"(tbd|todo|placeholder|pending|unknown|none|null|na)[-_:.0-9a-z]*", normalized):
        return True

    return False


def is_usable_ref_value(value: Any) -> bool:
    return is_non_blank_string(value) and not is_placeholder_ref_value(value)


def check_controlled_value(
    value: Any,
    allowed: Set[str],
    errors: List[Dict[str, str]],
    path: str,
    label: str,
    malformed_code: str = "CONTROLLED_VOCABULARY_VALUE_UNKNOWN",
) -> None:
    if not isinstance(value, str) or not value.strip():
        add_error(errors, malformed_code, path, f"{label} must be a non-empty controlled vocabulary string.")
        return

    if value not in allowed:
        if label == "structural_outcome":
            add_error(
                errors,
                "MALFORMED_STRUCTURAL_OUTCOME_TOKEN",
                path,
                f"Unrecognized structural outcome token: {value}",
            )
        add_error(
            errors,
            "CONTROLLED_VOCABULARY_VALUE_UNKNOWN",
            path,
            f"{label} is not in the controlled vocabulary: {value}",
        )


def string_values(obj: Any, path: str = "$") -> Iterable[Tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from string_values(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from string_values(value, f"{path}[{index}]")
    elif isinstance(obj, str):
        yield path, obj


def check_object_shape(
    obj: Any,
    path: str,
    required: Set[str],
    allowed: Set[str],
    errors: List[Dict[str, str]],
) -> None:
    if not isinstance(obj, dict):
        add_schema_error(errors, "INVALID_FIELD_TYPE", path, "Expected object.")
        return

    keys = set(obj.keys())

    for field in sorted(required.difference(keys)):
        add_schema_error(errors, "MISSING_REQUIRED_FIELD", f"{path}.{field}", "Missing required field.")

    for field in sorted(keys.difference(allowed)):
        add_schema_error(errors, "UNEXPECTED_FIELD", f"{path}.{field}", "Unexpected field is not allowed.")


def expect_list(obj: Dict[str, Any], field: str, path: str, errors: List[Dict[str, str]]) -> None:
    if field in obj and not isinstance(obj.get(field), list):
        add_schema_error(errors, "INVALID_FIELD_TYPE", f"{path}.{field}", "Expected array.")


def expect_bool(obj: Dict[str, Any], field: str, path: str, errors: List[Dict[str, str]]) -> None:
    if field in obj and not isinstance(obj.get(field), bool):
        add_schema_error(errors, "INVALID_FIELD_TYPE", f"{path}.{field}", "Expected boolean.")


def schema_conformance_check(bundle: Dict[str, Any], errors: List[Dict[str, str]]) -> None:
    check_object_shape(bundle, "$", TOP_REQUIRED, TOP_ALLOWED, errors)
    if not isinstance(bundle, dict):
        return

    for field in [
        "mandatory_non_claims",
        "simulation_class_coverage",
        "aggregate_posture_precedence",
        "simulation_cases",
    ]:
        expect_list(bundle, field, "$", errors)

    expect_bool(bundle, "synthetic_only", "$", errors)

    cases = bundle.get("simulation_cases")
    if not isinstance(cases, list):
        return

    for case_index, case in enumerate(cases):
        case_path = f"$.simulation_cases[{case_index}]"
        check_object_shape(case, case_path, CASE_REQUIRED, CASE_ALLOWED, errors)
        if not isinstance(case, dict):
            continue

        for field in [
            "input_claims",
            "handoff_events",
            "boundary_behavior_records",
            "expected_structural_outcomes",
            "non_claims",
        ]:
            expect_list(case, field, case_path, errors)

        for optional_list_field in ["system_assertions", "notes"]:
            expect_list(case, optional_list_field, case_path, errors)

        expect_bool(case, "synthetic_only", case_path, errors)

        claims = case.get("input_claims")
        if isinstance(claims, list):
            for claim_index, claim in enumerate(claims):
                claim_path = f"{case_path}.input_claims[{claim_index}]"
                check_object_shape(claim, claim_path, CLAIM_REQUIRED, CLAIM_ALLOWED, errors)
                if isinstance(claim, dict):
                    expect_list(claim, "non_claims", claim_path, errors)

        assertions = case.get("system_assertions")
        if isinstance(assertions, list):
            for assertion_index, assertion in enumerate(assertions):
                assertion_path = f"{case_path}.system_assertions[{assertion_index}]"
                check_object_shape(assertion, assertion_path, ASSERTION_REQUIRED, ASSERTION_ALLOWED, errors)
                if isinstance(assertion, dict):
                    expect_list(assertion, "non_claims", assertion_path, errors)

        handoffs = case.get("handoff_events")
        if isinstance(handoffs, list):
            for handoff_index, handoff in enumerate(handoffs):
                handoff_path = f"{case_path}.handoff_events[{handoff_index}]"
                check_object_shape(handoff, handoff_path, HANDOFF_REQUIRED, HANDOFF_ALLOWED, errors)
                if isinstance(handoff, dict):
                    expect_list(handoff, "non_claims", handoff_path, errors)

        records = case.get("boundary_behavior_records")
        if isinstance(records, list):
            if not records:
                add_schema_error(
                    errors,
                    "MISSING_BOUNDARY_BEHAVIOR_RECORD",
                    f"{case_path}.boundary_behavior_records",
                    "boundary_behavior_records must not be empty.",
                )

            for record_index, record in enumerate(records):
                record_path = f"{case_path}.boundary_behavior_records[{record_index}]"
                check_object_shape(record, record_path, RECORD_REQUIRED, RECORD_ALLOWED, errors)
                if not isinstance(record, dict):
                    continue

                for field in [
                    "preserved_non_claims",
                    "dropped_non_claims",
                    "authority_refs",
                    "evidence_refs",
                    "structural_outcomes",
                ]:
                    expect_list(record, field, record_path, errors)

                authority_refs = record.get("authority_refs")
                if isinstance(authority_refs, list):
                    for ref_index, ref in enumerate(authority_refs):
                        ref_path = f"{record_path}.authority_refs[{ref_index}]"
                        check_object_shape(ref, ref_path, AUTHORITY_REF_REQUIRED, AUTHORITY_REF_ALLOWED, errors)
                        if isinstance(ref, dict):
                            expect_bool(ref, "authority_ref_resolution_attempted", ref_path, errors)

                evidence_refs = record.get("evidence_refs")
                if isinstance(evidence_refs, list):
                    for ref_index, ref in enumerate(evidence_refs):
                        ref_path = f"{record_path}.evidence_refs[{ref_index}]"
                        check_object_shape(ref, ref_path, EVIDENCE_REF_REQUIRED, EVIDENCE_REF_ALLOWED, errors)
                        if isinstance(ref, dict):
                            expect_bool(ref, "evidence_ref_resolution_attempted", ref_path, errors)

        aggregate_report = case.get("aggregate_report")
        if aggregate_report is not None:
            aggregate_path = f"{case_path}.aggregate_report"
            check_object_shape(
                aggregate_report,
                aggregate_path,
                AGGREGATE_REPORT_REQUIRED,
                AGGREGATE_REPORT_ALLOWED,
                errors,
            )
            if isinstance(aggregate_report, dict):
                for field in [
                    "receipt_refs",
                    "included_structural_outcomes",
                    "omitted_structural_outcomes",
                ]:
                    expect_list(aggregate_report, field, aggregate_path, errors)
                expect_bool(aggregate_report, "aggregate_collapse_detected", aggregate_path, errors)


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
            normalized = lower.replace("-", "_").replace(" ", "_")
            normalized_token = token.lower().replace("-", "_").replace(" ", "_")
            pattern = r"(?<![a-z0-9])" + re.escape(normalized_token) + r"(?![a-z0-9])"
            if re.search(pattern, normalized):
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


def check_refs(
    refs: List[Any],
    ref_key: str,
    attempted_key: str,
    state_key: str,
    structurally_reachable_state: str,
    recorded_not_performed_state: str,
    attempted_unreachable_state: str,
    missing_code: str,
    errors: List[Dict[str, str]],
    path: str,
    require_usable_ref: bool = False,
) -> bool:
    usable_ref_found = False

    for index, ref in enumerate(refs):
        ref_path = f"{path}[{index}]"
        if not isinstance(ref, dict):
            add_error(errors, "SCHEMA_VALIDATION_FAILED", ref_path, "Reference entry must be object.")
            continue

        ref_value = ref.get(ref_key)
        if not is_usable_ref_value(ref_value):
            add_error(
                errors,
                "PLACEHOLDER_REF_DETECTED",
                f"{ref_path}.{ref_key}",
                "Reference value is blank, missing, or placeholder-like.",
            )
            continue

        usable_ref_found = True

        attempted = ref.get(attempted_key)
        state = ref.get(state_key)

        if state == structurally_reachable_state and attempted is not True:
            add_error(
                errors,
                "RESOLUTION_ATTEMPT_STATE_CONTRADICTION",
                f"{ref_path}.{state_key}",
                "Structurally reachable reference requires resolution_attempted=true.",
            )
            add_error(errors, "MAPPING_INCOMPLETE", ref_path, "Resolution-attempt contradiction forces incomplete mapping.")

        if state == recorded_not_performed_state and attempted is not False:
            add_error(
                errors,
                "RESOLUTION_ATTEMPT_STATE_CONTRADICTION",
                f"{ref_path}.{state_key}",
                "Recorded-resolution-not-performed requires resolution_attempted=false.",
            )
            add_error(errors, "MAPPING_INCOMPLETE", ref_path, "Resolution-attempt contradiction forces incomplete mapping.")

        if state == attempted_unreachable_state and attempted is not True:
            add_error(
                errors,
                "RESOLUTION_ATTEMPT_STATE_CONTRADICTION",
                f"{ref_path}.{state_key}",
                "Attempted-unreachable state requires resolution_attempted=true.",
            )
            add_error(errors, "MAPPING_INCOMPLETE", ref_path, "Resolution-attempt contradiction forces incomplete mapping.")

    if require_usable_ref and not usable_ref_found:
        add_error(errors, missing_code, path, "Reference list has no usable non-placeholder reference.")
        return False

    return usable_ref_found


def check_non_claim_accounting(
    claim: Dict[str, Any] | None,
    record: Dict[str, Any],
    errors: List[Dict[str, str]],
    path: str,
) -> None:
    if claim is None:
        return

    upstream_non_claims = {
        item
        for item in as_list(claim.get("non_claims"))
        if isinstance(item, str)
    }

    preserved = {
        item
        for item in as_list(record.get("preserved_non_claims"))
        if isinstance(item, str)
    }

    dropped = {
        item
        for item in as_list(record.get("dropped_non_claims"))
        if isinstance(item, str)
    }

    accounted = preserved.union(dropped)
    missing = sorted(upstream_non_claims.difference(accounted))
    extra = sorted(accounted.difference(upstream_non_claims))
    overlap = sorted(preserved.intersection(dropped))

    if overlap:
        add_error(
            errors,
            "NON_CLAIM_PRESERVED_AND_DROPPED_CONTRADICTION",
            path,
            "Non-claims cannot be both preserved and dropped: " + ", ".join(overlap),
        )
        add_error(errors, "MAPPING_INCOMPLETE", path, "Contradictory non-claim mapping forces incomplete mapping.")

    if missing:
        add_error(
            errors,
            "NON_CLAIM_SILENTLY_OMITTED",
            path,
            "Upstream non-claims are not fully accounted for in preserved_non_claims or dropped_non_claims: "
            + ", ".join(missing),
        )
        add_error(errors, "MAPPING_INCOMPLETE", path, "Unaccounted upstream non-claims force incomplete mapping.")

    if extra:
        add_error(
            errors,
            "NON_CLAIM_TAMPERING_DETECTED",
            path,
            "Boundary record contains non-claims not present on the upstream claim: " + ", ".join(extra),
        )
        add_error(errors, "MAPPING_INCOMPLETE", path, "Non-claim mismatch forces incomplete mapping.")


def check_record(
    case: Dict[str, Any],
    simulation_class: str,
    claim_map: Dict[str, Dict[str, Any]],
    record: Dict[str, Any],
    errors: List[Dict[str, str]],
    path: str,
) -> None:
    relationship = record.get("claim_relationship_state")
    declared = record.get("consumer_declared_boundary_behavior")
    observed = record.get("validator_observed_boundary_behavior")
    outcomes = set(as_list(record.get("structural_outcomes")))
    dropped_non_claims = as_list(record.get("dropped_non_claims"))
    authority_refs = as_list(record.get("authority_refs"))
    evidence_refs = as_list(record.get("evidence_refs"))

    claim_ref = record.get("claim_ref")
    claim = claim_map.get(claim_ref) if isinstance(claim_ref, str) else None

    check_controlled_value(
        relationship,
        ALLOWED_CLAIM_RELATIONSHIP_STATES,
        errors,
        f"{path}.claim_relationship_state",
        "claim_relationship_state",
    )
    check_controlled_value(
        declared,
        ALLOWED_BOUNDARY_BEHAVIORS,
        errors,
        f"{path}.consumer_declared_boundary_behavior",
        "consumer_declared_boundary_behavior",
    )
    check_controlled_value(
        observed,
        ALLOWED_BOUNDARY_BEHAVIORS,
        errors,
        f"{path}.validator_observed_boundary_behavior",
        "validator_observed_boundary_behavior",
    )

    for outcome_index, outcome in enumerate(as_list(record.get("structural_outcomes"))):
        check_controlled_value(
            outcome,
            ALLOWED_STRUCTURAL_OUTCOMES,
            errors,
            f"{path}.structural_outcomes[{outcome_index}]",
            "structural_outcome",
        )

    check_non_claim_accounting(claim, record, errors, path)

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

    expansion_detected = observed == "BOUNDARY_EXPANSION_DETECTED"
    expansion_present = observed in {"BOUNDARY_EXPANSION_DETECTED", "BOUNDARY_EXPANSION_RECORDED"} or bool(
        outcomes.intersection(EXPANSION_OUTCOMES)
    )

    check_refs(
        authority_refs,
        "authority_ref",
        "authority_ref_resolution_attempted",
        "authority_ref_resolution_state",
        "AUTHORITY_REF_STRUCTURALLY_REACHABLE",
        "AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
        "AUTHORITY_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
        "AUTHORITY_REF_MISSING",
        errors,
        f"{path}.authority_refs",
        require_usable_ref=False,
    )

    check_refs(
        evidence_refs,
        "evidence_ref",
        "evidence_ref_resolution_attempted",
        "evidence_ref_resolution_state",
        "EVIDENCE_REF_STRUCTURALLY_REACHABLE",
        "EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED",
        "EVIDENCE_REF_RESOLUTION_ATTEMPTED_UNREACHABLE",
        "EVIDENCE_REF_MISSING",
        errors,
        f"{path}.evidence_refs",
        require_usable_ref=False,
    )

    if expansion_detected:
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

        usable_authority = any(
            isinstance(ref, dict) and is_usable_ref_value(ref.get("authority_ref"))
            for ref in authority_refs
        )
        usable_evidence = any(
            isinstance(ref, dict) and is_usable_ref_value(ref.get("evidence_ref"))
            for ref in evidence_refs
        )

        if not usable_authority:
            if "AUTHORITY_REF_MISSING" not in outcomes:
                add_error(errors, "AUTHORITY_REF_MISSING", path, "Expansion without usable authority refs must emit AUTHORITY_REF_MISSING.")
            if "MAPPING_INCOMPLETE" not in outcomes:
                add_error(errors, "MAPPING_INCOMPLETE", path, "Expansion without usable authority refs must be incomplete.")

        if not usable_evidence:
            if "EVIDENCE_REF_MISSING" not in outcomes:
                add_error(errors, "EVIDENCE_REF_MISSING", path, "Expansion without usable evidence refs must emit EVIDENCE_REF_MISSING.")
            if "MAPPING_INCOMPLETE" not in outcomes:
                add_error(errors, "MAPPING_INCOMPLETE", path, "Expansion without usable evidence refs must be incomplete.")

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


def check_declared_non_usage_structural_use(
    records: List[Any],
    errors: List[Dict[str, str]],
    path: str,
) -> None:
    records_by_claim: Dict[str, List[Tuple[int, Dict[str, Any]]]] = {}

    for record_index, record in enumerate(records):
        if not isinstance(record, dict):
            continue
        claim_ref = record.get("claim_ref")
        if not isinstance(claim_ref, str):
            continue
        records_by_claim.setdefault(claim_ref, []).append((record_index, record))

    structural_use_observed = {
        "BOUNDARY_NARROWED",
        "BOUNDARY_EXPANSION_DETECTED",
        "BOUNDARY_EXPANSION_RECORDED",
    }

    for claim_ref, entries in sorted(records_by_claim.items()):
        has_declared_non_usage = any(
            record.get("claim_relationship_state") == "CLAIM_NON_USAGE_DECLARED"
            for _, record in entries
        )

        if not has_declared_non_usage:
            continue

        structurally_used_entries = [
            index
            for index, record in entries
            if record.get("claim_relationship_state") == "CLAIM_USED_AS_SUPPORT"
            or record.get("validator_observed_boundary_behavior") in structural_use_observed
            or record.get("consumer_declared_boundary_behavior") in structural_use_observed
        ]

        if structurally_used_entries:
            add_error(
                errors,
                "CLAIM_NON_USAGE_DECLARED_WITH_STRUCTURAL_USE",
                path,
                "Claim declares non-usage but also appears in structurally used records: "
                + claim_ref,
            )
            add_error(
                errors,
                "MAPPING_INCOMPLETE",
                path,
                "Declared non-usage with structural use forces incomplete mapping.",
            )


def check_case(case: Dict[str, Any], index: int, errors: List[Dict[str, str]]) -> None:
    path = f"$.simulation_cases[{index}]"
    simulation_class = str(case.get("simulation_class"))

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

    claim_map = {
        claim.get("claim_id"): claim
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }

    record_claim_refs = {
        record.get("claim_ref")
        for record in records
        if isinstance(record, dict) and isinstance(record.get("claim_ref"), str)
    }

    for claim_id in sorted(claim_map):
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
        check_record(
            case,
            simulation_class,
            claim_map,
            record,
            errors,
            f"{path}.boundary_behavior_records[{record_index}]",
        )

    check_declared_non_usage_structural_use(records, errors, path)

    outcomes = collect_case_outcomes(case)
    expected_posture = case.get("expected_aggregate_posture")
    expected_precedence = case.get("expected_precedence_trigger")
    computed_posture = computed_aggregate_posture(case)

    check_controlled_value(
        expected_posture,
        ALLOWED_AGGREGATE_POSTURES,
        errors,
        f"{path}.expected_aggregate_posture",
        "expected_aggregate_posture",
    )
    check_controlled_value(
        expected_precedence,
        ALLOWED_PRECEDENCE_TRIGGERS,
        errors,
        f"{path}.expected_precedence_trigger",
        "expected_precedence_trigger",
    )

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

    schema_conformance_check(bundle, errors)
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


from typing import Any, Dict, List, Optional

OUTPUT_SEMANTICS_VERSION = "0.1.3"

MACHINE_READABLE_LIMITATIONS_V013: Dict[str, Any] = {
    "limitations_code": "STRUCTURAL_SYNTHETIC_PROTOCOL_CHECK_ONLY",
    "scope": "STRUCTURAL_SYNTHETIC_PROTOCOL_CHECK_ONLY",
    "synthetic_corpus_only": True,
    "does_not_validate_truth": True,
    "does_not_validate_safety": True,
    "does_not_validate_compliance": True,
    "does_not_validate_legal_sufficiency": True,
    "does_not_validate_admissibility": True,
    "does_not_validate_authority": True,
    "does_not_validate_evidence_sufficiency": True,
    "does_not_validate_medical_correctness": True,
    "does_not_validate_operational_authorization": True,
    "does_not_authorize_production_use": True,
    "does_not_observe_undisclosed_downstream_behavior": True,
    "canonical_warning": "STRUCTURAL_CONFORMANCE_IS_NOT_APPROVAL_TRUTH_COMPLIANCE_AUTHORITY_OR_EVIDENCE_SUFFICIENCY",
}


def _v013_structural_output_from_legacy(result: Dict[str, Any]) -> Dict[str, Any]:
    errors = result.get("errors", [])
    error_count = result.get("error_count", len(errors) if isinstance(errors, list) else 0)

    return {
        "result_kind": "STRUCTURAL_BUNDLE_CHECK",
        "output_semantics_version": OUTPUT_SEMANTICS_VERSION,
        "runner": {
            "runner_succeeded": True,
            "mode": "single_bundle_check",
        },
        "structural_result": {
            "structurally_conformant": bool(result.get("ok", False)),
            "source": result.get("source"),
            "error_count": error_count,
            "errors": errors,
        },
        "harness_result": None,
        "limitations": MACHINE_READABLE_LIMITATIONS_V013,
    }


def _v013_fixture_result_from_legacy(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "fixture_file": item.get("fixture_file"),
        "checker_structurally_conformant": bool(item.get("checker_ok", False)),
        "expected_failures_observed": bool(item.get("ok", False)),
        "actual_error_codes": item.get("actual_error_codes", []),
        "missing_expected_failures": item.get("missing_expected_failures", []),
    }


def _v013_invalid_manifest_output_from_legacy(result: Dict[str, Any]) -> Dict[str, Any]:
    fixture_results = [
        _v013_fixture_result_from_legacy(item)
        for item in result.get("fixture_results", [])
        if isinstance(item, dict)
    ]

    return {
        "result_kind": "INVALID_FIXTURE_HARNESS",
        "output_semantics_version": OUTPUT_SEMANTICS_VERSION,
        "runner": {
            "runner_succeeded": True,
            "mode": "invalid_fixture_harness",
        },
        "structural_result": None,
        "harness_result": {
            "all_invalid_fixtures_rejected": bool(result.get("ok", False)),
            "does_not_indicate_structural_conformance": True,
            "manifest": result.get("manifest"),
            "fixture_count": len(fixture_results),
            "fixture_results": fixture_results,
        },
        "limitations": {
            **MACHINE_READABLE_LIMITATIONS_V013,
            "scope": "NEGATIVE_TEST_HARNESS_ONLY",
            "does_not_indicate_structural_conformance": True,
        },
    }


def _v013_print_json(payload: Dict[str, Any], pretty: bool) -> None:
    import json as _json

    if pretty:
        print(_json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(_json.dumps(payload, sort_keys=True))


def _v013_call_invalid_manifest(manifest_path: Optional[str] = None) -> Dict[str, Any]:
    candidates = (
        "check_invalid_manifest",
        "check_invalid_manifest_path",
        "run_invalid_manifest",
        "check_invalid_fixtures_manifest",
    )

    resolved_manifest_path = manifest_path or globals().get("INVALID_MANIFEST_PATH") or globals().get("INVALID_MANIFEST")

    for name in candidates:
        fn = globals().get(name)
        if not callable(fn):
            continue

        if resolved_manifest_path is not None:
            try:
                return fn(resolved_manifest_path)
            except TypeError:
                pass

        try:
            return fn()
        except TypeError:
            if resolved_manifest_path is None:
                raise
            return fn(resolved_manifest_path)

    raise RuntimeError("No invalid-manifest checker function found")


def main(argv: Optional[List[str]] = None) -> int:
    import argparse as _argparse
    from pathlib import Path as _Path

    parser = _argparse.ArgumentParser(
        description=(
            "Fork claim-inheritance simulation structural checker. "
            "Output semantics v0.1.3 separates runner success from structural conformance."
        )
    )
    parser.add_argument(
        "bundle",
        nargs="?",
        help="Path to a synthetic claim-inheritance simulation bundle.",
    )
    parser.add_argument(
        "--invalid-manifest",
        action="store_true",
        help="Run the negative-test harness. Harness success does not mean structural conformance.",
    )
    parser.add_argument(
        "--manifest-path",
        help="Optional invalid fixture manifest path for compatibility with existing test harnesses.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    parser.add_argument(
        "--legacy-output",
        action="store_true",
        help="Emit pre-v0.1.3 legacy JSON shape for local compatibility only.",
    )

    args = parser.parse_args(argv)

    try:
        if args.invalid_manifest:
            legacy_result = _v013_call_invalid_manifest(args.manifest_path)

            if args.legacy_output:
                _v013_print_json(legacy_result, args.pretty)
                return 0 if bool(legacy_result.get("ok", False)) else 1

            payload = _v013_invalid_manifest_output_from_legacy(legacy_result)
            _v013_print_json(payload, args.pretty)
            return 0 if payload["harness_result"]["all_invalid_fixtures_rejected"] else 1

        if not args.bundle:
            parser.error("bundle path is required unless --invalid-manifest is used")

        legacy_result = check_bundle_path(_Path(args.bundle))

        if args.legacy_output:
            _v013_print_json(legacy_result, args.pretty)
            return 0 if bool(legacy_result.get("ok", False)) else 1

        payload = _v013_structural_output_from_legacy(legacy_result)
        _v013_print_json(payload, args.pretty)
        return 0 if payload["structural_result"]["structurally_conformant"] else 1

    except Exception as exc:
        payload = {
            "result_kind": "RUNNER_ERROR",
            "output_semantics_version": OUTPUT_SEMANTICS_VERSION,
            "runner": {
                "runner_succeeded": False,
                "mode": "runner_error",
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
            "structural_result": None,
            "harness_result": None,
            "limitations": MACHINE_READABLE_LIMITATIONS_V013,
        }
        _v013_print_json(payload, args.pretty)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
