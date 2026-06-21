#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CHECKER_VERSION = "BDR_v0_1"

ROOT_REQUIRED = {
    "record_type",
    "record_version",
    "boundary_delta_record_id",
    "source_boundary_ref",
    "downstream_statement_ref",
    "transitions",
    "derived_boundary_delta",
    "structural_outcome",
}

ROOT_ALLOWED = set(ROOT_REQUIRED)

SOURCE_REQUIRED = {
    "source_record_id",
    "claim_boundary_contract_id",
    "source_claim_refs",
    "source_non_claim_refs",
    "source_evidence_refs",
    "source_recomputation_status",
}

DOWNSTREAM_REQUIRED = {
    "downstream_record_id",
    "downstream_statement_refs",
    "downstream_evidence_refs",
}

TRANSITION_REQUIRED = {
    "transition_id",
    "from_ref",
    "to_ref",
    "transition_kind",
    "transformation_rule",
    "supporting_refs",
}

TRANSITION_ALLOWED = set(TRANSITION_REQUIRED) | {"suppression_disclosure_ref"}

DERIVED_REQUIRED = {
    "licensed_claim_surface",
    "claim_scope_generalized",
    "silence_converted_to_claim",
    "authority_expansion_required",
    "evidence_reference_expansion_required",
    "recomputation_status_converted_to_truth",
    "evidence_reference_lost",
    "evidence_reference_suppressed",
    "non_claim_dropped",
}

LICENSED_SURFACES = {
    "SOURCE_SURFACE_PRESERVED",
    "SOURCE_SURFACE_NARROWED",
    "REFERENCE_SUPPRESSED_AT_BOUNDARY",
    "UNLICENSED_EXPANSION_DETECTED",
}

STRUCTURAL_OUTCOMES = {"INSPECTABLE", "NOT_INSPECTABLE"}

SAFE_TRANSITION_KINDS = {
    "CLAIM_SCOPE_PRESERVED",
    "CLAIM_SCOPE_NARROWED",
    "NON_CLAIM_PRESERVED",
    "EVIDENCE_REFERENCE_PRESERVED",
    "EVIDENCE_REFERENCE_LOST",
    "RECOMPUTATION_STATUS_PRESERVED",
    "AUTHORITY_PRESERVED",
}

FAIL_CLOSED_TRANSITION_KINDS = {
    "CLAIM_SCOPE_GENERALIZED",
    "CLAIM_ADDED_FROM_SILENCE",
    "AUTHORITY_EXPANDED",
    "EVIDENCE_REFERENCE_EXPANDED",
    "EVIDENCE_REFERENCE_SUPPRESSED",
    "RECOMPUTATION_STATUS_CONVERTED_TO_TRUTH",
    "NON_CLAIM_DROPPED",
}

KNOWN_TRANSITION_KINDS = SAFE_TRANSITION_KINDS | FAIL_CLOSED_TRANSITION_KINDS

SAFE_TRANSFORMATION_RULES = {
    "PRESERVE_AS_IS",
    "NARROW_SCOPE",
    "RETAIN_NON_CLAIM",
    "PRESERVE_EVIDENCE_REFERENCE",
    "RECORD_REFERENCE_LOSS",
    "PRESERVE_RECOMPUTATION_STATUS",
    "PRESERVE_AUTHORITY",
}

FAIL_CLOSED_TRANSFORMATION_RULES = {
    "GENERALIZE_SCOPE",
    "CONVERT_SILENCE_TO_CLAIM",
    "EXPAND_AUTHORITY",
    "ADD_UNTRANSFERRED_EVIDENCE_REFERENCE",
    "SUPPRESS_REFERENCE",
    "MAP_RECOMPUTATION_TO_TRUTH",
    "DROP_NON_CLAIM",
}

KNOWN_TRANSFORMATION_RULES = SAFE_TRANSFORMATION_RULES | FAIL_CLOSED_TRANSFORMATION_RULES

TRANSITION_KIND_TO_ALLOWED_RULES = {
    "CLAIM_SCOPE_PRESERVED": {"PRESERVE_AS_IS"},
    "CLAIM_SCOPE_NARROWED": {"NARROW_SCOPE"},
    "NON_CLAIM_PRESERVED": {"RETAIN_NON_CLAIM"},
    "EVIDENCE_REFERENCE_PRESERVED": {"PRESERVE_EVIDENCE_REFERENCE"},
    "EVIDENCE_REFERENCE_LOST": {"RECORD_REFERENCE_LOSS"},
    "RECOMPUTATION_STATUS_PRESERVED": {"PRESERVE_RECOMPUTATION_STATUS"},
    "AUTHORITY_PRESERVED": {"PRESERVE_AUTHORITY"},
    "CLAIM_SCOPE_GENERALIZED": {"GENERALIZE_SCOPE"},
    "CLAIM_ADDED_FROM_SILENCE": {"CONVERT_SILENCE_TO_CLAIM"},
    "AUTHORITY_EXPANDED": {"EXPAND_AUTHORITY"},
    "EVIDENCE_REFERENCE_EXPANDED": {"ADD_UNTRANSFERRED_EVIDENCE_REFERENCE"},
    "EVIDENCE_REFERENCE_SUPPRESSED": {"SUPPRESS_REFERENCE"},
    "RECOMPUTATION_STATUS_CONVERTED_TO_TRUTH": {"MAP_RECOMPUTATION_TO_TRUTH"},
    "NON_CLAIM_DROPPED": {"DROP_NON_CLAIM"},
}

PROHIBITED_KEYS = {
    "score",
    "severity",
    "risk_score",
    "confidence",
    "llm_interpretation",
    "cross_record_inference",
    "ranking",
    "recommendation",
    "approval_status",
}

FLAG_RULES = {
    "claim_scope_generalized": {
        "transition_kinds": {"CLAIM_SCOPE_GENERALIZED"},
        "transformation_rules": {"GENERALIZE_SCOPE"},
    },
    "silence_converted_to_claim": {
        "transition_kinds": {"CLAIM_ADDED_FROM_SILENCE"},
        "transformation_rules": {"CONVERT_SILENCE_TO_CLAIM"},
    },
    "authority_expansion_required": {
        "transition_kinds": {"AUTHORITY_EXPANDED"},
        "transformation_rules": {"EXPAND_AUTHORITY"},
    },
    "evidence_reference_expansion_required": {
        "transition_kinds": {"EVIDENCE_REFERENCE_EXPANDED"},
        "transformation_rules": {"ADD_UNTRANSFERRED_EVIDENCE_REFERENCE"},
    },
    "recomputation_status_converted_to_truth": {
        "transition_kinds": {"RECOMPUTATION_STATUS_CONVERTED_TO_TRUTH"},
        "transformation_rules": {"MAP_RECOMPUTATION_TO_TRUTH"},
    },
    "evidence_reference_lost": {
        "transition_kinds": {"EVIDENCE_REFERENCE_LOST"},
        "transformation_rules": {"RECORD_REFERENCE_LOSS"},
    },
    "evidence_reference_suppressed": {
        "transition_kinds": {"EVIDENCE_REFERENCE_SUPPRESSED"},
        "transformation_rules": {"SUPPRESS_REFERENCE"},
    },
    "non_claim_dropped": {
        "transition_kinds": {"NON_CLAIM_DROPPED"},
        "transformation_rules": {"DROP_NON_CLAIM"},
    },
}

UNLICENSED_EXPANSION_FLAGS = {
    "claim_scope_generalized",
    "silence_converted_to_claim",
    "authority_expansion_required",
    "evidence_reference_expansion_required",
    "recomputation_status_converted_to_truth",
    "non_claim_dropped",
}


def finding(code: str, message: str, **extra: Any) -> dict[str, Any]:
    item: dict[str, Any] = {"code": code, "message": message}
    item.update(extra)
    return item


def load_json(path: Path) -> tuple[Any | None, list[dict[str, Any]]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [
            finding(
                "JSON_PARSE_ERROR",
                "Input is not valid JSON.",
                line=exc.lineno,
                column=exc.colno,
            )
        ]


def find_prohibited_keys(value: Any, path: str = "$") -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in PROHIBITED_KEYS:
                findings.append(
                    finding(
                        "PROHIBITED_KEY",
                        "Boundary Delta Record v0.1 forbids scoring, severity, confidence, interpretation, recommendation, approval, and cross-record inference fields.",
                        key=key,
                        path=child_path,
                    )
                )
            findings.extend(find_prohibited_keys(child, child_path))

    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_prohibited_keys(child, f"{path}[{index}]"))

    return findings


def require_string(value: Any, path: str, findings: list[dict[str, Any]]) -> None:
    if not isinstance(value, str) or value == "":
        findings.append(finding("TYPE_ERROR", "Expected non-empty string.", path=path))


def require_string_list(value: Any, path: str, findings: list[dict[str, Any]]) -> None:
    if not isinstance(value, list):
        findings.append(finding("TYPE_ERROR", "Expected array of non-empty strings.", path=path))
        return

    for index, item in enumerate(value):
        if not isinstance(item, str) or item == "":
            findings.append(
                finding(
                    "TYPE_ERROR",
                    "Expected array item to be a non-empty string.",
                    path=f"{path}[{index}]",
                )
            )


def validate_shape(record: Any) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    if not isinstance(record, dict):
        return [finding("ROOT_TYPE_ERROR", "Boundary Delta Record must be a JSON object.")]

    missing_root = sorted(ROOT_REQUIRED - set(record))
    for key in missing_root:
        findings.append(finding("MISSING_REQUIRED_FIELD", "Missing required root field.", field=key))

    unexpected_root = sorted(set(record) - ROOT_ALLOWED)
    for key in unexpected_root:
        findings.append(finding("UNEXPECTED_ROOT_KEY", "Unexpected root field.", field=key))

    if record.get("record_type") != "BOUNDARY_DELTA_RECORD":
        findings.append(
            finding(
                "INVALID_RECORD_TYPE",
                "record_type must be BOUNDARY_DELTA_RECORD.",
                observed=record.get("record_type"),
            )
        )

    if record.get("record_version") != "0.1":
        findings.append(
            finding(
                "INVALID_RECORD_VERSION",
                "record_version must be 0.1.",
                observed=record.get("record_version"),
            )
        )

    if "boundary_delta_record_id" in record:
        require_string(record.get("boundary_delta_record_id"), "$.boundary_delta_record_id", findings)

    source = record.get("source_boundary_ref")
    if not isinstance(source, dict):
        findings.append(finding("TYPE_ERROR", "source_boundary_ref must be an object.", path="$.source_boundary_ref"))
    else:
        for key in sorted(SOURCE_REQUIRED - set(source)):
            findings.append(finding("MISSING_REQUIRED_FIELD", "Missing source_boundary_ref field.", field=key))
        for key in sorted(set(source) - SOURCE_REQUIRED):
            findings.append(finding("UNEXPECTED_SOURCE_KEY", "Unexpected source_boundary_ref field.", field=key))

        for key in ("source_record_id", "claim_boundary_contract_id"):
            if key in source:
                require_string(source.get(key), f"$.source_boundary_ref.{key}", findings)

        for key in ("source_claim_refs", "source_non_claim_refs", "source_evidence_refs"):
            if key in source:
                require_string_list(source.get(key), f"$.source_boundary_ref.{key}", findings)

        if source.get("source_recomputation_status") not in {"RECOMPUTABLE_RECORD_INTEGRITY_ONLY", "NOT_ASSERTED"}:
            findings.append(
                finding(
                    "INVALID_RECOMPUTATION_STATUS",
                    "source_recomputation_status must be RECOMPUTABLE_RECORD_INTEGRITY_ONLY or NOT_ASSERTED.",
                    observed=source.get("source_recomputation_status"),
                )
            )

    downstream = record.get("downstream_statement_ref")
    if not isinstance(downstream, dict):
        findings.append(
            finding(
                "TYPE_ERROR",
                "downstream_statement_ref must be an object.",
                path="$.downstream_statement_ref",
            )
        )
    else:
        for key in sorted(DOWNSTREAM_REQUIRED - set(downstream)):
            findings.append(finding("MISSING_REQUIRED_FIELD", "Missing downstream_statement_ref field.", field=key))
        for key in sorted(set(downstream) - DOWNSTREAM_REQUIRED):
            findings.append(finding("UNEXPECTED_DOWNSTREAM_KEY", "Unexpected downstream_statement_ref field.", field=key))

        if "downstream_record_id" in downstream:
            require_string(downstream.get("downstream_record_id"), "$.downstream_statement_ref.downstream_record_id", findings)

        for key in ("downstream_statement_refs", "downstream_evidence_refs"):
            if key in downstream:
                require_string_list(downstream.get(key), f"$.downstream_statement_ref.{key}", findings)

    transitions = record.get("transitions")
    if not isinstance(transitions, list) or not transitions:
        findings.append(finding("TRANSITIONS_REQUIRED", "transitions must be a non-empty array."))
    elif isinstance(transitions, list):
        for index, transition in enumerate(transitions):
            path = f"$.transitions[{index}]"
            if not isinstance(transition, dict):
                findings.append(finding("TYPE_ERROR", "Transition must be an object.", path=path))
                continue

            for key in sorted(TRANSITION_REQUIRED - set(transition)):
                findings.append(finding("MISSING_REQUIRED_FIELD", "Missing transition field.", field=key, path=path))

            for key in sorted(set(transition) - TRANSITION_ALLOWED):
                findings.append(finding("UNEXPECTED_TRANSITION_KEY", "Unexpected transition field.", field=key, path=path))

            for key in ("transition_id", "from_ref", "to_ref", "transition_kind", "transformation_rule"):
                if key in transition:
                    require_string(transition.get(key), f"{path}.{key}", findings)

            if "supporting_refs" in transition:
                supporting_refs = transition.get("supporting_refs")
                require_string_list(supporting_refs, f"{path}.supporting_refs", findings)
                if isinstance(supporting_refs, list) and len(supporting_refs) == 0:
                    findings.append(
                        finding(
                            "SUPPORTING_REFS_REQUIRED",
                            "Each transition must carry at least one supporting_ref.",
                            transition_id=transition.get("transition_id"),
                        )
                    )

            kind = transition.get("transition_kind")
            rule = transition.get("transformation_rule")

            if isinstance(kind, str) and kind not in KNOWN_TRANSITION_KINDS:
                findings.append(
                    finding(
                        "UNKNOWN_TRANSITION_KIND",
                        "Unknown transition kind fails closed.",
                        transition_id=transition.get("transition_id"),
                        observed=kind,
                    )
                )

            if isinstance(rule, str) and rule not in KNOWN_TRANSFORMATION_RULES:
                findings.append(
                    finding(
                        "UNKNOWN_TRANSFORMATION_RULE",
                        "Unknown transformation rule fails closed.",
                        transition_id=transition.get("transition_id"),
                        observed=rule,
                    )
                )

            if (
                isinstance(kind, str)
                and isinstance(rule, str)
                and kind in KNOWN_TRANSITION_KINDS
                and rule in KNOWN_TRANSFORMATION_RULES
            ):
                allowed_rules = TRANSITION_KIND_TO_ALLOWED_RULES.get(kind, set())
                if rule not in allowed_rules:
                    findings.append(
                        finding(
                            "TRANSITION_KIND_RULE_MISMATCH",
                            "transition_kind and transformation_rule are incompatible under Boundary Delta Record v0.1.",
                            transition_id=transition.get("transition_id"),
                            transition_kind=kind,
                            transformation_rule=rule,
                            allowed_transformation_rules=sorted(allowed_rules),
                        )
                    )

            if kind == "EVIDENCE_REFERENCE_SUPPRESSED":
                if not isinstance(transition.get("suppression_disclosure_ref"), str) or transition.get("suppression_disclosure_ref") == "":
                    findings.append(
                        finding(
                            "SUPPRESSION_DISCLOSURE_REQUIRED",
                            "Suppression must carry a suppression_disclosure_ref.",
                            transition_id=transition.get("transition_id"),
                        )
                    )
            elif "suppression_disclosure_ref" in transition:
                findings.append(
                    finding(
                        "SUPPRESSION_DISCLOSURE_MISPLACED",
                        "suppression_disclosure_ref is only valid for EVIDENCE_REFERENCE_SUPPRESSED transitions.",
                        transition_id=transition.get("transition_id"),
                    )
                )

    derived = record.get("derived_boundary_delta")
    if not isinstance(derived, dict):
        findings.append(
            finding(
                "TYPE_ERROR",
                "derived_boundary_delta must be an object.",
                path="$.derived_boundary_delta",
            )
        )
    else:
        for key in sorted(DERIVED_REQUIRED - set(derived)):
            findings.append(finding("MISSING_REQUIRED_FIELD", "Missing derived_boundary_delta field.", field=key))

        for key in sorted(set(derived) - DERIVED_REQUIRED):
            findings.append(finding("UNEXPECTED_DERIVED_KEY", "Unexpected derived_boundary_delta field.", field=key))

        if derived.get("licensed_claim_surface") not in LICENSED_SURFACES:
            findings.append(
                finding(
                    "INVALID_LICENSED_CLAIM_SURFACE",
                    "licensed_claim_surface is not recognized.",
                    observed=derived.get("licensed_claim_surface"),
                )
            )

        for key in sorted(DERIVED_REQUIRED - {"licensed_claim_surface"}):
            if key in derived and not isinstance(derived.get(key), bool):
                findings.append(
                    finding(
                        "DERIVED_FLAG_TYPE_ERROR",
                        "Derived flags must be boolean.",
                        field=key,
                        observed=derived.get(key),
                    )
                )

    if record.get("structural_outcome") not in STRUCTURAL_OUTCOMES:
        findings.append(
            finding(
                "INVALID_STRUCTURAL_OUTCOME",
                "structural_outcome must be INSPECTABLE or NOT_INSPECTABLE.",
                observed=record.get("structural_outcome"),
            )
        )

    return findings


def derive_flags(record: dict[str, Any]) -> dict[str, bool]:
    flags = {key: False for key in DERIVED_REQUIRED if key != "licensed_claim_surface"}

    transitions = record.get("transitions")
    if not isinstance(transitions, list):
        return flags

    for transition in transitions:
        if not isinstance(transition, dict):
            continue

        kind = transition.get("transition_kind")
        rule = transition.get("transformation_rule")

        for flag, rule_set in FLAG_RULES.items():
            if kind in rule_set["transition_kinds"] or rule in rule_set["transformation_rules"]:
                flags[flag] = True

    return flags


def derive_licensed_surface(record: dict[str, Any], flags: dict[str, bool]) -> str:
    if any(flags[flag] for flag in sorted(UNLICENSED_EXPANSION_FLAGS)):
        return "UNLICENSED_EXPANSION_DETECTED"

    if flags["evidence_reference_suppressed"]:
        return "REFERENCE_SUPPRESSED_AT_BOUNDARY"

    transitions = record.get("transitions")
    if isinstance(transitions, list):
        for transition in transitions:
            if isinstance(transition, dict) and transition.get("transition_kind") == "CLAIM_SCOPE_NARROWED":
                return "SOURCE_SURFACE_NARROWED"

    return "SOURCE_SURFACE_PRESERVED"


def compare_authored_to_derived(
    record: dict[str, Any],
    computed_flags: dict[str, bool],
    computed_surface: str,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    authored = record.get("derived_boundary_delta")

    if not isinstance(authored, dict):
        return findings

    authored_surface = authored.get("licensed_claim_surface")
    if authored_surface != computed_surface:
        findings.append(
            finding(
                "LICENSED_CLAIM_SURFACE_MISMATCH",
                "Authored licensed_claim_surface does not match checker-derived licensed_claim_surface.",
                authored=authored_surface,
                derived=computed_surface,
            )
        )

    for flag, computed_value in sorted(computed_flags.items()):
        if flag not in authored:
            continue

        authored_value = authored.get(flag)
        if not isinstance(authored_value, bool):
            continue

        if authored_value and not computed_value:
            findings.append(
                finding(
                    "DERIVED_FLAG_WITHOUT_SUPPORTING_TRANSITION",
                    "Authored true flag has no supporting transition.",
                    flag=flag,
                )
            )

        if computed_value and not authored_value:
            findings.append(
                finding(
                    "DERIVED_FLAG_NOT_DISCLOSED",
                    "Transition requires true derived flag, but authored flag is false.",
                    flag=flag,
                )
            )

    return findings


def semantic_not_inspectable_findings(flags: dict[str, bool]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for flag in sorted(UNLICENSED_EXPANSION_FLAGS):
        if flags[flag]:
            findings.append(
                finding(
                    "UNLICENSED_SEMANTIC_EXPANSION_DETECTED",
                    "A downstream statement requires material not transferred across the boundary.",
                    flag=flag,
                )
            )

    if flags["evidence_reference_suppressed"]:
        findings.append(
            finding(
                "REFERENCE_SUPPRESSED_AT_BOUNDARY",
                "Reference suppression is mechanically visible and fails closed in v0.1.",
                flag="evidence_reference_suppressed",
            )
        )

    return findings


def limitations() -> dict[str, Any]:
    return {
        "does_not_validate_truth": True,
        "does_not_validate_safety": True,
        "does_not_validate_compliance": True,
        "does_not_validate_legal_sufficiency": True,
        "does_not_score_risk": True,
        "does_not_rank_severity": True,
        "does_not_approve_reliance": True,
        "does_not_perform_llm_interpretation": True,
        "does_not_perform_cross_record_inference": True,
        "does_not_infer_scope_from_text": True,
        "does_not_infer_authority_from_text": True,
        "does_not_infer_evidence_requirements_from_text": True,
        "treats_references_as_opaque_tokens": True,
        "requires_declared_transitions": True,
        "binary_outcomes_only": ["INSPECTABLE", "NOT_INSPECTABLE"],
    }


def check_record(record: Any) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []

    if isinstance(record, dict):
        record_id = record.get("boundary_delta_record_id", "UNKNOWN_RECORD_ID")
    else:
        record_id = "UNKNOWN_RECORD_ID"

    findings.extend(find_prohibited_keys(record))
    findings.extend(validate_shape(record))

    if isinstance(record, dict):
        computed_flags = derive_flags(record)
        computed_surface = derive_licensed_surface(record, computed_flags)
        derived = {"licensed_claim_surface": computed_surface}
        derived.update(computed_flags)

        findings.extend(compare_authored_to_derived(record, computed_flags, computed_surface))
        findings.extend(semantic_not_inspectable_findings(computed_flags))

        provisional_outcome = "NOT_INSPECTABLE" if findings else "INSPECTABLE"
        authored_outcome = record.get("structural_outcome")
        if authored_outcome in STRUCTURAL_OUTCOMES and authored_outcome != provisional_outcome:
            findings.append(
                finding(
                    "STRUCTURAL_OUTCOME_MISMATCH",
                    "Authored structural_outcome does not match checker-derived structural_outcome.",
                    authored=authored_outcome,
                    derived=provisional_outcome,
                )
            )
    else:
        derived = {
            "licensed_claim_surface": "UNLICENSED_EXPANSION_DETECTED",
            "claim_scope_generalized": False,
            "silence_converted_to_claim": False,
            "authority_expansion_required": False,
            "evidence_reference_expansion_required": False,
            "recomputation_status_converted_to_truth": False,
            "evidence_reference_lost": False,
            "evidence_reference_suppressed": False,
            "non_claim_dropped": False,
        }

    outcome = "NOT_INSPECTABLE" if findings else "INSPECTABLE"

    return {
        "checker": "check_boundary_delta_record.py",
        "checker_version": CHECKER_VERSION,
        "record_id": record_id,
        "structural_outcome": outcome,
        "derived": derived,
        "findings": findings,
        "limitations": limitations(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Boundary Delta Record v0.1.")
    parser.add_argument("path", help="Path to Boundary Delta Record JSON.")
    args = parser.parse_args(argv)

    path = Path(args.path)
    record, load_findings = load_json(path)

    if load_findings:
        result = {
            "checker": "check_boundary_delta_record.py",
            "checker_version": CHECKER_VERSION,
            "record_id": "UNKNOWN_RECORD_ID",
            "structural_outcome": "NOT_INSPECTABLE",
            "derived": {
                "licensed_claim_surface": "UNLICENSED_EXPANSION_DETECTED",
                "claim_scope_generalized": False,
                "silence_converted_to_claim": False,
                "authority_expansion_required": False,
                "evidence_reference_expansion_required": False,
                "recomputation_status_converted_to_truth": False,
                "evidence_reference_lost": False,
                "evidence_reference_suppressed": False,
                "non_claim_dropped": False,
            },
            "findings": load_findings,
            "limitations": limitations(),
        }
    else:
        result = check_record(record)

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["structural_outcome"] == "INSPECTABLE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
