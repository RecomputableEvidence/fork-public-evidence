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

REQUIRED_NON_CLAIMS = {
    "does_not_establish_truth",
    "does_not_establish_approval",
    "does_not_establish_compliance",
    "does_not_establish_legal_sufficiency",
    "does_not_establish_production_readiness",
    "does_not_convert_observation_into_endorsement",
    "does_not_convert_failed_retrieval_into_review",
}

PROHIBITED_COLLAPSES = {
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


def require(condition: bool, code: str, errors: List[str]) -> None:
    if not condition:
        errors.append(code)


def evaluate_case(case: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    for key in [
        "case_id",
        "case_version",
        "expected_result",
        "source_access",
        "claims",
        "non_claims",
        "boundary_pressure",
        "interpretation",
    ]:
        require(key in case, f"MISSING_REQUIRED_FIELD:{key}", errors)

    if errors:
        return errors

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

    authority_claims = [
        "approval_claimed",
        "compliance_claimed",
        "legal_sufficiency_claimed",
        "truth_claimed",
    ]

    no_or_partial_access = access_status in {"NO_ACCESS", "PARTIAL_ACCESS"}

    require(
        case.get("case_version") == "v0.1",
        "UNSUPPORTED_CASE_VERSION",
        errors,
    )

    require(
        case.get("expected_result") in {"STRUCTURAL_PASS", "STRUCTURAL_FAIL"},
        "INVALID_EXPECTED_RESULT",
        errors,
    )

    require(
        boundary_pressure.get("pressure_type") == "RETRIEVAL_DISTORTION",
        "INVALID_PRESSURE_TYPE",
        errors,
    )

    if no_or_partial_access:
        require(
            limitation_recorded,
            "ACCESS_LIMITATION_NOT_RECORDED",
            errors,
        )

        require(
            interpretation.get("observation_status") == "ACCESS_LIMITATION_RECORDED",
            "FAILED_OR_PARTIAL_ACCESS_NOT_PRESERVED_AS_LIMITATION",
            errors,
        )

        require(
            not content_review,
            "RETRIEVAL_DISTORTION_CONTENT_REVIEW_CLAIMED_WITHOUT_RAW_ACCESS",
            errors,
        )

        require(
            not structural_reproduction,
            "RETRIEVAL_DISTORTION_REPRODUCTION_CLAIMED_WITHOUT_EXECUTION",
            errors,
        )

    if access_status == "RAW_ACCESS":
        require(raw_access, "RAW_ACCESS_STATUS_WITHOUT_RAW_ACCESS_FLAG", errors)

    if access_status == "EXECUTED":
        require(
            raw_access and executed,
            "EXECUTED_STATUS_WITHOUT_RAW_ACCESS_AND_EXECUTION_FLAGS",
            errors,
        )

    for authority_claim in authority_claims:
        require(
            not bool(claims.get(authority_claim)),
            f"AUTHORITY_OR_SUFFICIENCY_CLAIM_FORBIDDEN:{authority_claim}",
            errors,
        )

    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    for missing in missing_non_claims:
        errors.append(f"MISSING_REQUIRED_NON_CLAIM:{missing}")

    observed_collapses = set(boundary_pressure.get("prohibited_collapses", []))
    require(
        bool(observed_collapses & PROHIBITED_COLLAPSES),
        "NO_RECOGNIZED_BOUNDARY_PRESSURE_COLLAPSE_DECLARED",
        errors,
    )

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
            errors.append(f"HIGH_RISK_ASSERTED_MEANING_TERM:{term}")

    return errors


def main() -> int:
    if not FIXTURE_ROOT.exists():
        print(f"Missing fixture directory: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    paths = sorted(FIXTURE_ROOT.rglob("*.json"))

    if not paths:
        print(f"No fixtures found under: {FIXTURE_ROOT}", file=sys.stderr)
        return 2

    unexpected: List[str] = []

    print("Boundary Pressure Review Case Checker v0.1")
    print(f"Fixture root: {FIXTURE_ROOT}")
    print("")

    for path in paths:
        case = load_json(path)
        expected = case.get("expected_result")
        errors = evaluate_case(case)
        actual = "STRUCTURAL_FAIL" if errors else "STRUCTURAL_PASS"

        expectation_matched = expected == actual

        rel = path.relative_to(ROOT)
        print(f"{rel}")
        print(f"  case_id: {case.get('case_id')}")
        print(f"  expected: {expected}")
        print(f"  actual:   {actual}")

        if errors:
            for error in errors:
                print(f"  error:    {error}")

        if expectation_matched:
            print("  result:   EXPECTATION_MATCHED")
        else:
            print("  result:   EXPECTATION_MISMATCH")
            unexpected.append(str(rel))

        print("")

    if unexpected:
        print("Unexpected fixture results:", file=sys.stderr)
        for rel in unexpected:
            print(f"  - {rel}", file=sys.stderr)
        return 1

    print("All boundary pressure fixture expectations matched.")
    print("")
    print(
        "Interpretation: this is a structural fixture result only. "
        "It does not establish truth, approval, legal sufficiency, "
        "compliance, production readiness, endorsement, audit sufficiency, "
        "or external certification."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())