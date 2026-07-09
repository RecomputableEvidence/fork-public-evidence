#!/usr/bin/env python3
"""
Boundary Pressure Review Case Checker v0.1

This checker validates the retrieval-distortion fixtures included in Fork.

A checker pass means only that the included fixtures behaved as expected
under the structural rules below. It does not establish truth, approval,
legal sufficiency, compliance, production readiness, endorsement, audit
sufficiency, or external certification.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "docs" / "review" / "boundary-pressure" / "fixtures"

REQUIRED_PASS_NON_CLAIMS = {
    "does_not_establish_truth",
    "does_not_establish_approval",
    "does_not_establish_compliance",
    "does_not_establish_legal_sufficiency",
    "does_not_establish_production_readiness",
    "does_not_convert_observation_into_endorsement",
    "does_not_convert_failed_retrieval_into_review",
}

RECOGNIZED_COLLAPSES = {
    "failed_retrieval_to_review",
    "partial_access_to_complete_access",
    "observation_to_endorsement",
    "commentary_to_execution",
    "structural_pass_to_truth",
    "recomputation_to_validation",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def add_error(errors: List[str], code: str) -> None:
    errors.append(code)


def evaluate_case(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    required = [
        "case_id",
        "case_version",
        "expected_result",
        "source_access",
        "claims",
        "non_claims",
        "boundary_pressure",
        "interpretation",
    ]

    for key in required:
        if key not in case:
            add_error(errors, f"MISSING_REQUIRED_FIELD:{key}")

    if errors:
        return errors

    if case.get("case_version") != "v0.1":
        add_error(errors, "UNSUPPORTED_CASE_VERSION")

    if case.get("expected_result") not in {"STRUCTURAL_PASS", "STRUCTURAL_FAIL"}:
        add_error(errors, "INVALID_EXPECTED_RESULT")

    source_access = case.get("source_access", {})
    claims = case.get("claims", {})
    non_claims = set(case.get("non_claims", []))
    boundary_pressure = case.get("boundary_pressure", {})
    interpretation = case.get("interpretation", {})

    access_status = source_access.get("status")
    raw_access = bool(source_access.get("raw_artifacts_accessed"))
    executed = bool(source_access.get("execution_performed"))
    limitation_recorded = bool(source_access.get("access_limitation_recorded"))

    content_review = bool(claims.get("content_review_completed"))
    structural_reproduction = bool(claims.get("structural_reproduction_completed"))

    if boundary_pressure.get("pressure_type") != "RETRIEVAL_DISTORTION":
        add_error(errors, "INVALID_PRESSURE_TYPE")

    collapses = set(boundary_pressure.get("prohibited_collapses", []))
    if not bool(collapses & RECOGNIZED_COLLAPSES):
        add_error(errors, "NO_RECOGNIZED_BOUNDARY_PRESSURE_COLLAPSE_DECLARED")

    if access_status in {"NO_ACCESS", "PARTIAL_ACCESS"}:
        if not limitation_recorded:
            add_error(errors, "ACCESS_LIMITATION_NOT_RECORDED")

        if interpretation.get("observation_status") != "ACCESS_LIMITATION_RECORDED":
            add_error(errors, "FAILED_OR_PARTIAL_ACCESS_NOT_PRESERVED_AS_LIMITATION")

        if content_review:
            add_error(errors, "RETRIEVAL_DISTORTION_CONTENT_REVIEW_CLAIMED_WITHOUT_RAW_ACCESS")

        if structural_reproduction:
            add_error(errors, "RETRIEVAL_DISTORTION_REPRODUCTION_CLAIMED_WITHOUT_EXECUTION")

    if access_status == "RAW_ACCESS" and not raw_access:
        add_error(errors, "RAW_ACCESS_STATUS_WITHOUT_RAW_ACCESS_FLAG")

    if access_status == "EXECUTED" and not (raw_access and executed):
        add_error(errors, "EXECUTED_STATUS_WITHOUT_RAW_ACCESS_AND_EXECUTION_FLAGS")

    for claim_name in [
        "approval_claimed",
        "compliance_claimed",
        "legal_sufficiency_claimed",
        "truth_claimed",
    ]:
        if bool(claims.get(claim_name)):
            add_error(errors, f"AUTHORITY_OR_SUFFICIENCY_CLAIM_FORBIDDEN:{claim_name}")

    asserted_meaning = str(claims.get("asserted_meaning", "")).lower()
    high_risk_terms = [
        "approved",
        "certified",
        "validated",
        "compliant",
        "legally sufficient",
        "production ready",
    ]

    for term in high_risk_terms:
        if term in asserted_meaning:
            add_error(errors, f"HIGH_RISK_ASSERTED_MEANING_TERM:{term}")

    if case.get("expected_result") == "STRUCTURAL_PASS":
        missing_non_claims = sorted(REQUIRED_PASS_NON_CLAIMS - non_claims)
        for missing in missing_non_claims:
            add_error(errors, f"MISSING_REQUIRED_NON_CLAIM:{missing}")

    return errors


def main() -> int:
    if not FIXTURE_ROOT.exists():
        print(f"Missing fixture directory: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    paths = sorted(FIXTURE_ROOT.rglob("*.json"))

    if not paths:
        print(f"No fixtures found under: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    expected_values = set()
    unexpected = []

    print("Boundary Pressure Review Case Checker v0.1")
    print(f"Fixture root: {FIXTURE_ROOT}")
    print("")

    for path in paths:
        case = load_json(path)
        expected = case.get("expected_result")
        expected_values.add(expected)

        errors = evaluate_case(case)
        actual = "STRUCTURAL_FAIL" if errors else "STRUCTURAL_PASS"
        rel = path.relative_to(ROOT)

        print(f"{rel}")
        print(f"  case_id: {case.get('case_id')}")
        print(f"  expected: {expected}")
        print(f"  actual:   {actual}")

        for error in errors:
            print(f"  error:    {error}")

        if expected == actual:
            print("  result:   EXPECTATION_MATCHED")
        else:
            print("  result:   EXPECTATION_MISMATCH")
            unexpected.append(str(rel))

        print("")

    if "STRUCTURAL_PASS" not in expected_values:
        print("Missing required positive fixture coverage: STRUCTURAL_PASS", file=sys.stderr)
        return 1

    if "STRUCTURAL_FAIL" not in expected_values:
        print("Missing required negative fixture coverage: STRUCTURAL_FAIL", file=sys.stderr)
        return 1

    if unexpected:
        print("Unexpected fixture results:", file=sys.stderr)
        for rel in unexpected:
            print(f"  - {rel}", file=sys.stderr)
        return 1

    print("All boundary pressure fixture expectations matched.")
    print("")
    print("Interpretation: this is a structural fixture result only. It does not establish truth, approval, legal sufficiency, compliance, production readiness, endorsement, audit sufficiency, or external certification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())