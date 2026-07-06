#!/usr/bin/env python3
"""
Fork Surface Interaction Contract Checker v0.1

Structural checker stub for surface-interaction records.

Scope:
- Validates required fields and enumerated values.
- Applies bounded non-absorption checks.
- Returns structural outcomes only.

Non-scope:
- Does not establish truth, approval, compliance, admissibility, legal sufficiency, safety, or authority.
- Does not validate the underlying correctness of external artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


SURFACES = {
    "EVIDENCE_BOUNDARY_SURFACE",
    "TRANSITION_SURFACE",
    "RELIANCE_SURFACE",
    "INTEROPERABILITY_SURFACE",
    "SIMULATION_SURFACE",
    "COMMERCIAL_SURFACE",
}

REFERENCE_TYPES = {
    "BOUNDARY_REFERENCE",
    "TRANSITION_REFERENCE",
    "RELIANCE_REFERENCE",
    "EXTERNAL_ARTIFACT_REFERENCE",
    "SIMULATION_REFERENCE",
    "COMMERCIAL_COMPOSITION_REFERENCE",
}

OPERATIONS = {
    "REFERENCE",
    "PRESERVE_CONTEXT",
    "COMPARE_BOUNDARY_STATE",
    "RECONSTRUCT",
    "COMPOSE_FOR_REVIEW",
    "BIND_EXTERNAL_REFERENCE",
    "MUTATE_BOUNDARY",
    "REINTERPRET_SEMANTICS",
    "EXPAND_VERIFICATION_SCOPE",
    "ASSIGN_TRUTH_VALUE",
    "ASSERT_APPROVAL",
    "ASSERT_COMPLIANCE",
    "ASSERT_ADMISSIBILITY",
    "ASSERT_LEGAL_SUFFICIENCY",
    "ASSERT_SAFETY",
    "IMPORT_EXTERNAL_AUTHORITY",
    "ADOPT_EXTERNAL_ASSERTION",
    "DROP_NON_CLAIMS",
    "DROP_LIMITATIONS",
    "RETROACTIVE_AUTHORIZATION",
}

AUTHORITY_EFFECTS = {
    "NO_AUTHORITY_TRANSFER",
    "AUTHORITY_REFERENCE_ONLY",
    "AUTHORITY_EXPANSION_ATTEMPTED",
    "AUTHORITY_BORROWING_ATTEMPTED",
    "AUTHORITY_EFFECT_UNRESOLVED",
}

SEMANTIC_EFFECTS = {
    "REFERENCE_ONLY",
    "PRESERVATION_ONLY",
    "DELTA_INSPECTION_ONLY",
    "RECONSTRUCTION_ONLY",
    "WORKFLOW_COMPOSITION_ONLY",
    "SEMANTIC_ADOPTION_ATTEMPTED",
    "SEMANTIC_EXPANSION_ATTEMPTED",
    "SEMANTIC_COMPRESSION_DETECTED",
}

VERIFICATION_EFFECTS = {
    "NO_NEW_VERIFICATION",
    "STRUCTURAL_VERIFICATION_ONLY",
    "VERIFICATION_SCOPE_REFERENCED",
    "VERIFICATION_SCOPE_EXPANSION_ATTEMPTED",
    "TRUTH_VERIFICATION_ATTEMPTED",
    "COMPLIANCE_VERIFICATION_ATTEMPTED",
    "APPROVAL_VERIFICATION_ATTEMPTED",
}

CHECKER_OUTCOMES = {
    "SURFACE_INTERACTION_RECORDED",
    "SURFACE_INTERACTION_CONFORMS",
    "SURFACE_INTERACTION_NOT_INSPECTABLE",
    "AUTHORITY_ABSORPTION_ATTEMPTED",
    "SEMANTIC_ADOPTION_ATTEMPTED",
    "VERIFICATION_SCOPE_EXPANSION_ATTEMPTED",
    "COMMERCIAL_SURFACE_EXPANSION_ATTEMPTED",
    "NON_CLAIM_COMPRESSION_DETECTED",
}

REQUIRED_FIELDS = {
    "surface_interaction_contract_version",
    "interaction_id",
    "source_surface",
    "target_surface",
    "reference_type",
    "permitted_operations",
    "prohibited_operations",
    "authority_effect",
    "semantic_effect",
    "verification_effect",
    "declared_outcome",
    "evidence_refs",
    "limitations",
}

FORBIDDEN_APPROVAL_OUTCOMES = {
    "APPROVED",
    "COMPLIANT",
    "SAFE",
    "VALIDATED_AS_TRUE",
    "AUTHORIZED",
    "LEGALLY_SUFFICIENT",
}

ABSORPTION_OPERATIONS = {
    "ASSIGN_TRUTH_VALUE",
    "ASSERT_APPROVAL",
    "ASSERT_COMPLIANCE",
    "ASSERT_ADMISSIBILITY",
    "ASSERT_LEGAL_SUFFICIENCY",
    "ASSERT_SAFETY",
    "IMPORT_EXTERNAL_AUTHORITY",
    "ADOPT_EXTERNAL_ASSERTION",
    "RETROACTIVE_AUTHORIZATION",
}

EVIDENCE_BOUNDARY_MUTATION_OPERATIONS = {
    "MUTATE_BOUNDARY",
    "REINTERPRET_SEMANTICS",
    "EXPAND_VERIFICATION_SCOPE",
}

VERIFICATION_EXPANSION_EFFECTS = {
    "VERIFICATION_SCOPE_EXPANSION_ATTEMPTED",
    "TRUTH_VERIFICATION_ATTEMPTED",
    "COMPLIANCE_VERIFICATION_ATTEMPTED",
    "APPROVAL_VERIFICATION_ATTEMPTED",
}


def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            value = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc

    if not isinstance(value, dict):
        raise ValueError(f"{path}: top-level JSON value must be an object")

    return value


def ensure_list_of_strings(record: Dict[str, Any], field: str) -> List[str]:
    value = record.get(field)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field} must be a non-empty list")

    if not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} must contain only non-empty strings")

    if len(value) != len(set(value)):
        raise ValueError(f"{field} must not contain duplicates")

    return value


def check_enum(value: Any, allowed: Iterable[str], field: str) -> None:
    if value not in allowed:
        raise ValueError(f"{field} has unsupported value: {value!r}")


def is_valid_target_surface(value: Any) -> bool:
    if value in SURFACES:
        return True
    return isinstance(value, str) and value.startswith("EXTERNAL_ARTIFACT:") and len(value) > len("EXTERNAL_ARTIFACT:")


def structural_validate(record: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    missing = sorted(REQUIRED_FIELDS - set(record))
    if missing:
        failures.append(f"Missing required fields: {', '.join(missing)}")
        return failures

    if record.get("surface_interaction_contract_version") != "v0.1":
        failures.append("surface_interaction_contract_version must be v0.1")

    interaction_id = record.get("interaction_id")
    if not isinstance(interaction_id, str) or not interaction_id.startswith("surface-interaction-"):
        failures.append("interaction_id must start with surface-interaction-")

    try:
        check_enum(record.get("source_surface"), SURFACES, "source_surface")
    except ValueError as exc:
        failures.append(str(exc))

    if not is_valid_target_surface(record.get("target_surface")):
        failures.append("target_surface must be a known Fork surface or EXTERNAL_ARTIFACT:<id>")

    try:
        check_enum(record.get("reference_type"), REFERENCE_TYPES, "reference_type")
        check_enum(record.get("authority_effect"), AUTHORITY_EFFECTS, "authority_effect")
        check_enum(record.get("semantic_effect"), SEMANTIC_EFFECTS, "semantic_effect")
        check_enum(record.get("verification_effect"), VERIFICATION_EFFECTS, "verification_effect")
        check_enum(record.get("declared_outcome"), CHECKER_OUTCOMES, "declared_outcome")
    except ValueError as exc:
        failures.append(str(exc))

    try:
        permitted = ensure_list_of_strings(record, "permitted_operations")
        prohibited = ensure_list_of_strings(record, "prohibited_operations")
        ensure_list_of_strings(record, "evidence_refs")
        ensure_list_of_strings(record, "limitations")
    except ValueError as exc:
        failures.append(str(exc))
        return failures

    unsupported_permitted = sorted(set(permitted) - OPERATIONS)
    unsupported_prohibited = sorted(set(prohibited) - OPERATIONS)
    if unsupported_permitted:
        failures.append(f"Unsupported permitted_operations: {', '.join(unsupported_permitted)}")
    if unsupported_prohibited:
        failures.append(f"Unsupported prohibited_operations: {', '.join(unsupported_prohibited)}")

    overlap = sorted(set(permitted) & set(prohibited))
    if overlap:
        failures.append(f"Operations cannot be both permitted and prohibited: {', '.join(overlap)}")

    if record.get("declared_outcome") in FORBIDDEN_APPROVAL_OUTCOMES:
        failures.append("declared_outcome must not use approval/compliance/truth language")

    return failures


def non_absorption_validate(record: Dict[str, Any]) -> Tuple[str, List[str]]:
    failures: List[str] = []

    permitted = set(record.get("permitted_operations", []))
    source = record.get("source_surface")
    target = record.get("target_surface")
    authority_effect = record.get("authority_effect")
    semantic_effect = record.get("semantic_effect")
    verification_effect = record.get("verification_effect")

    if permitted & ABSORPTION_OPERATIONS:
        failures.append(
            "Permitted operations include authority/truth/compliance/adoption operations: "
            + ", ".join(sorted(permitted & ABSORPTION_OPERATIONS))
        )

    if target == "EVIDENCE_BOUNDARY_SURFACE" and permitted & EVIDENCE_BOUNDARY_MUTATION_OPERATIONS:
        failures.append(
            "Interaction with Evidence Boundary Surface permits mutation, reinterpretation, or verification expansion: "
            + ", ".join(sorted(permitted & EVIDENCE_BOUNDARY_MUTATION_OPERATIONS))
        )

    if authority_effect in {"AUTHORITY_EXPANSION_ATTEMPTED", "AUTHORITY_BORROWING_ATTEMPTED"}:
        failures.append(f"Authority absorption attempted: {authority_effect}")

    if semantic_effect in {"SEMANTIC_ADOPTION_ATTEMPTED", "SEMANTIC_EXPANSION_ATTEMPTED"}:
        failures.append(f"Semantic adoption or expansion attempted: {semantic_effect}")

    if verification_effect in VERIFICATION_EXPANSION_EFFECTS:
        failures.append(f"Verification scope expansion attempted: {verification_effect}")

    if source == "COMMERCIAL_SURFACE" and permitted - {"REFERENCE", "PRESERVE_CONTEXT", "COMPOSE_FOR_REVIEW"}:
        failures.append(
            "Commercial Surface may only reference, preserve context, or compose for review in this checker stub"
        )

    if failures:
        if authority_effect in {"AUTHORITY_EXPANSION_ATTEMPTED", "AUTHORITY_BORROWING_ATTEMPTED"}:
            return "AUTHORITY_ABSORPTION_ATTEMPTED", failures
        if semantic_effect in {"SEMANTIC_ADOPTION_ATTEMPTED", "SEMANTIC_EXPANSION_ATTEMPTED"}:
            return "SEMANTIC_ADOPTION_ATTEMPTED", failures
        if verification_effect in VERIFICATION_EXPANSION_EFFECTS:
            return "VERIFICATION_SCOPE_EXPANSION_ATTEMPTED", failures
        return "SURFACE_INTERACTION_NOT_INSPECTABLE", failures

    return "SURFACE_INTERACTION_CONFORMS", []


def check_file(path: Path) -> Tuple[str, List[str], str]:
    record = load_json(path)
    structural_failures = structural_validate(record)
    if structural_failures:
        return "STRUCTURAL_FAILURE", structural_failures, record.get("declared_outcome", "")

    outcome, failures = non_absorption_validate(record)
    declared = record.get("declared_outcome", "")

    if declared != outcome:
        failures = list(failures)
        failures.append(f"declared_outcome {declared!r} does not match computed outcome {outcome!r}")
        return "DECLARED_OUTCOME_MISMATCH", failures, declared

    return outcome, failures, declared


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Check Fork surface-interaction contract records.")
    parser.add_argument("paths", nargs="+", help="JSON fixture paths to check")
    parser.add_argument(
        "--expect-invalid",
        action="store_true",
        help="Return success when files are structurally checkable but produce non-conforming outcomes.",
    )
    args = parser.parse_args(argv)

    exit_code = 0

    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            outcome, failures, declared = check_file(path)
        except Exception as exc:
            print(f"{path}: ERROR: {exc}")
            exit_code = 1
            continue

        if failures:
            print(f"{path}: {outcome}")
            for failure in failures:
                print(f"  - {failure}")
        else:
            print(f"{path}: {outcome}")

        if args.expect_invalid:
            if outcome == "SURFACE_INTERACTION_CONFORMS":
                print(f"  - Expected invalid/non-conforming fixture, but checker returned conforming outcome.")
                exit_code = 1
        else:
            if outcome != "SURFACE_INTERACTION_CONFORMS":
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
