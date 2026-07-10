#!/usr/bin/env python3
"""
Fork Public Review Round 004 Interaction Checker v0.1.

Validates filed Round 004 interaction JSON records for required structure and
basic boundary-safety fields.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, production readiness, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List, Tuple


ROUND_ID = "public_review_round_004_accessibility_exterior_governance_longitudinal_readiness"

REQUIRED_TOP_LEVEL = [
    "review_round",
    "reviewer_role",
    "reviewer_environment",
    "access_path",
    "verifier_run",
    "comprehension",
    "governance_articulation",
    "longitudinal_readiness",
    "review_classification",
]

REQUIRED_ENVIRONMENT = [
    "os",
    "shell",
    "python_version",
    "git_available",
]

REQUIRED_ACCESS_PATH = [
    "started_from_repo_root",
    "found_current_proof_surface",
    "found_verifier",
    "found_boundary_pressure_cases",
    "found_longitudinal_protocol",
]

REQUIRED_VERIFIER_RUN = [
    "attempted",
    "passed",
    "failure_reason",
]

REQUIRED_COMPREHENSION = [
    "understood_current_claims",
    "understood_non_claims",
    "identified_overclaim_risk",
]

REQUIRED_GOVERNANCE = [
    "external_model_name",
    "what_it_would_consume",
    "what_it_would_not_inherit",
    "required_boundary_state",
]

REQUIRED_LONGITUDINAL = [
    "missing_artifacts",
    "required_receipts",
    "checker_drift_concerns",
    "packet_failure_concerns",
]

BOOLEAN_FIELDS = {
    ("reviewer_environment", "git_available"),
    ("access_path", "started_from_repo_root"),
    ("access_path", "found_current_proof_surface"),
    ("access_path", "found_verifier"),
    ("access_path", "found_boundary_pressure_cases"),
    ("access_path", "found_longitudinal_protocol"),
    ("verifier_run", "attempted"),
    ("verifier_run", "passed"),
    ("comprehension", "understood_current_claims"),
    ("comprehension", "understood_non_claims"),
}

ARRAY_FIELDS = {
    ("longitudinal_readiness", "missing_artifacts"),
    ("longitudinal_readiness", "required_receipts"),
    ("longitudinal_readiness", "checker_drift_concerns"),
    ("longitudinal_readiness", "packet_failure_concerns"),
}


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        raise ValueError(f"{path}: JSON parse failure: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def require_object(data: Dict[str, Any], key: str, errors: List[str]) -> Dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{key} must be object")
        return {}
    return value


def validate_record(path: pathlib.Path, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing top-level field: {key}")

    if data.get("review_round") != ROUND_ID:
        errors.append("review_round does not match Round 004 identifier")

    environment = require_object(data, "reviewer_environment", errors)
    access_path = require_object(data, "access_path", errors)
    verifier_run = require_object(data, "verifier_run", errors)
    comprehension = require_object(data, "comprehension", errors)
    governance = require_object(data, "governance_articulation", errors)
    longitudinal = require_object(data, "longitudinal_readiness", errors)

    for key in REQUIRED_ENVIRONMENT:
        if key not in environment:
            errors.append(f"reviewer_environment missing field: {key}")

    for key in REQUIRED_ACCESS_PATH:
        if key not in access_path:
            errors.append(f"access_path missing field: {key}")

    for key in REQUIRED_VERIFIER_RUN:
        if key not in verifier_run:
            errors.append(f"verifier_run missing field: {key}")

    for key in REQUIRED_COMPREHENSION:
        if key not in comprehension:
            errors.append(f"comprehension missing field: {key}")

    for key in REQUIRED_GOVERNANCE:
        if key not in governance:
            errors.append(f"governance_articulation missing field: {key}")

    for key in REQUIRED_LONGITUDINAL:
        if key not in longitudinal:
            errors.append(f"longitudinal_readiness missing field: {key}")

    sections = {
        "reviewer_environment": environment,
        "access_path": access_path,
        "verifier_run": verifier_run,
        "comprehension": comprehension,
        "governance_articulation": governance,
        "longitudinal_readiness": longitudinal,
    }

    for section, key in BOOLEAN_FIELDS:
        if key in sections[section] and not isinstance(sections[section][key], bool):
            errors.append(f"{section}.{key} must be boolean")

    for section, key in ARRAY_FIELDS:
        value = sections[section].get(key)
        if value is not None:
            if not isinstance(value, list):
                errors.append(f"{section}.{key} must be array")
            elif not all(isinstance(item, str) for item in value):
                errors.append(f"{section}.{key} must contain only strings")

    classification = data.get("review_classification")
    if not isinstance(classification, str) or not classification.strip():
        errors.append("review_classification must be non-empty string")

    non_authority = str(data.get("non_authority_statement", "")).lower()
    required_boundary_terms = [
        "not",
        "endorsement",
        "validation",
        "certification",
        "legal",
        "compliance",
        "production",
        "authority",
    ]
    for term in required_boundary_terms:
        if term not in non_authority:
            errors.append(f"non_authority_statement missing boundary term: {term}")

    if verifier_run.get("attempted") is False and verifier_run.get("passed") is True:
        errors.append("verifier_run.passed cannot be true when attempted is false")

    return not errors, errors


def find_records(root: pathlib.Path) -> List[pathlib.Path]:
    if not root.exists():
        return []
    return sorted(root.glob("*.json"))


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--observations-root",
        default="docs/review/public-rounds/round-004/observations",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.observations_root)
    paths = find_records(root)

    results = []
    failed = 0

    for path in paths:
        data = load_json(path)
        passed, errors = validate_record(path, data)
        if not passed:
            failed += 1

        results.append({
            "path": str(path).replace("\\", "/"),
            "reviewer_id": data.get("reviewer_id", path.stem),
            "review_classification": data.get("review_classification", ""),
            "evidence_weight": data.get("evidence_weight", ""),
            "passed": passed,
            "errors": errors,
        })

    summary = {
        "checker": "check_public_review_round_004_interactions_v0_1.py",
        "round": ROUND_ID,
        "observations_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker validates interaction filing structure only; it does not "
            "validate truth, compliance, legal sufficiency, safety, authorization, "
            "approval, production readiness, endorsement, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Round 004 interaction filings: {summary['passed']}/{summary['total']} passed")
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            print(f"{status} {result['reviewer_id']} ({result['path']})")
            for error in result["errors"]:
                print(f"  - {error}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))