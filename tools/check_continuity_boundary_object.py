#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "profile_id",
    "object_id",
    "profile_version",
    "synthetic_trace",
    "issuer_system",
    "receiver_system",
    "continuity_object_semantics",
    "upstream_asserted_events",
    "emitted_evidence",
    "downstream_preservation",
    "non_claims",
    "consumer_constraints",
    "integrity_metadata",
    "unresolveds",
    "expected_boundary_result",
]

REQUIRED_NON_CLAIMS = [
    "does_not_claim_truth",
    "does_not_claim_safety",
    "does_not_claim_compliance",
    "does_not_claim_legal_sufficiency",
    "does_not_claim_admissibility",
    "does_not_claim_authorization",
    "does_not_claim_approval",
    "does_not_claim_causal_correctness",
    "does_not_claim_upstream_governance_validity",
]

REQUIRED_DO_NOT_MAP_TO = [
    "APPROVAL",
    "AUTHORIZATION",
    "COMPLIANCE",
    "LEGAL_SUFFICIENCY",
    "SAFETY",
    "TRUTH",
    "ADMISSIBILITY",
    "RISK_ACCEPTANCE",
    "CAUSAL_PROOF",
    "UPSTREAM_GOVERNANCE_VALIDITY",
]


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Duplicate JSON key detected: {key}")
        seen.add(key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("CBO JSON must be UTF-8 without BOM.")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    if not isinstance(data, dict):
        raise ValueError("CBO root must be a JSON object.")
    return data


def add_finding(findings: list[dict[str, str]], code: str, path: str, message: str) -> None:
    findings.append({"code": code, "path": path, "message": message})


def require_object(data: dict[str, Any], key: str, findings: list[dict[str, str]]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        add_finding(findings, "FIELD_TYPE_INVALID", key, f"{key} must be an object.")
        return {}
    return value


def require_array(data: dict[str, Any], key: str, findings: list[dict[str, str]], path: str) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        add_finding(findings, "FIELD_TYPE_INVALID", path, f"{path} must be an array.")
        return []
    return value


def validate_cbo(data: dict[str, Any], artifact_path: str) -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            add_finding(findings, "REQUIRED_FIELD_MISSING", key, f"Missing required field: {key}")

    if data.get("profile_id") != "CONTINUITY_BOUNDARY_OBJECT_PROFILE_v0_1":
        add_finding(findings, "PROFILE_ID_INVALID", "profile_id", "profile_id must be CONTINUITY_BOUNDARY_OBJECT_PROFILE_v0_1")

    if data.get("profile_version") != "0.1":
        add_finding(findings, "PROFILE_VERSION_INVALID", "profile_version", "profile_version must be 0.1")

    semantics = require_object(data, "continuity_object_semantics", findings)

    expected_false = [
        "authority_transfer",
        "upstream_authority_inherited_by_receiver",
        "receiver_verifies_upstream_governance",
        "causality_crosses_boundary",
    ]
    for key in expected_false:
        if semantics.get(key) is not False:
            add_finding(findings, "AUTHORITY_BOUNDARY_VIOLATION", f"continuity_object_semantics.{key}", f"{key} must be false.")

    if semantics.get("object_role") != "structured_evidence_of_asserted_continuity_path":
        add_finding(
            findings,
            "OBJECT_ROLE_INVALID",
            "continuity_object_semantics.object_role",
            "object_role must be structured_evidence_of_asserted_continuity_path.",
        )

    non_claims = require_array(data, "non_claims", findings, "non_claims")
    for required in REQUIRED_NON_CLAIMS:
        if required not in non_claims:
            add_finding(findings, "NON_CLAIM_MISSING", "non_claims", f"Missing required non-claim: {required}")

    constraints = require_object(data, "consumer_constraints", findings)
    if constraints.get("requires_human_or_institutional_interpretation") is not True:
        add_finding(
            findings,
            "INTERPRETATION_CONSTRAINT_MISSING",
            "consumer_constraints.requires_human_or_institutional_interpretation",
            "requires_human_or_institutional_interpretation must be true.",
        )

    do_not_map_to = constraints.get("do_not_map_to")
    if not isinstance(do_not_map_to, list):
        add_finding(findings, "FIELD_TYPE_INVALID", "consumer_constraints.do_not_map_to", "do_not_map_to must be an array.")
        do_not_map_to = []

    for required in REQUIRED_DO_NOT_MAP_TO:
        if required not in do_not_map_to:
            add_finding(findings, "DO_NOT_MAP_TOKEN_MISSING", "consumer_constraints.do_not_map_to", f"Missing do_not_map_to token: {required}")

    expected = require_object(data, "expected_boundary_result", findings)
    expected_true = [
        "structurally_preservable",
        "upstream_authority_preserved",
        "downstream_authority_not_inherited",
        "requires_review_before_substantive_use",
    ]
    for key in expected_true:
        if expected.get(key) is not True:
            add_finding(findings, "EXPECTED_BOUNDARY_RESULT_INVALID", f"expected_boundary_result.{key}", f"{key} must be true.")

    ok = len(findings) == 0

    return {
        "limitations": {
            "checker_semantics_version": "v0.1",
            "limitations_code": "CONTINUITY_BOUNDARY_OBJECT_CHECKER_LIMITATIONS_v0_1",
            "scope": "STRUCTURAL_BOUNDARY_OBJECT_VALIDATION_ONLY",
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_compliance": True,
            "does_not_validate_legal_sufficiency": True,
            "does_not_validate_admissibility": True,
            "does_not_validate_authorization": True,
            "does_not_validate_approval": True,
            "does_not_validate_causality": True,
            "does_not_validate_upstream_governance": True,
            "automation_interpretation_required": True,
            "do_not_map_to": REQUIRED_DO_NOT_MAP_TO,
        },
        "result": {
            "artifact_path": artifact_path,
            "ok": ok,
            "computed_outcome": "CBO_STRUCTURALLY_VALID" if ok else "CBO_BOUNDARY_VIOLATION",
            "result_semantics": (
                "ok means the CBO is structurally valid and preserves authority-separation semantics only; "
                "it is not a truth, safety, compliance, admissibility, authorization, approval, causality, or upstream-governance verdict."
            ),
            "findings": findings,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Continuity Boundary Object v0.1 artifact.")
    parser.add_argument("artifact", help="Path to CBO JSON artifact.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.artifact))
        output = validate_cbo(data, args.artifact)
    except Exception as exc:
        output = {
            "limitations": {
                "checker_semantics_version": "v0.1",
                "scope": "STRUCTURAL_BOUNDARY_OBJECT_VALIDATION_ONLY",
                "automation_interpretation_required": True,
            },
            "result": {
                "artifact_path": args.artifact,
                "ok": False,
                "computed_outcome": "INPUT_ERROR",
                "findings": [
                    {"code": type(exc).__name__, "path": args.artifact, "message": str(exc)}
                ],
            },
        }
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
        return 2

    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))

    return 0 if output["result"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
