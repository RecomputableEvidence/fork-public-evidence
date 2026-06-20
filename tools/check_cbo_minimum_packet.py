#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_PROFILE_ID = "CBO_MINIMUM_PACKET_REQUIREMENTS_v0_1"
EXPECTED_VERSION = "0.1"

REQUIRED_TOP_LEVEL = [
    "profile_id",
    "cbo_version",
    "cbo_id",
    "packet_id",
    "issuer_system",
    "authority_domain",
    "stable_workload_id",
    "emitted_at",
    "continuity_chain",
    "integrity_metadata",
    "preservation_refs",
    "recomputation_refs",
    "boundary_semantics",
    "issuer_claims",
    "issuer_non_claims",
    "fork_permissions",
    "fork_restrictions",
    "downstream_constraints",
    "unresolved_or_excluded_refs",
    "expected_fork_evaluation",
]

REQUIRED_CONTINUITY_CHAIN_FIELDS = [
    "admission_decision_ref",
    "invariant_binding_refs",
    "state_transition_refs",
    "execution_event_refs",
    "emitted_artifact_refs",
]

REQUIRED_FALSE_BOUNDARY_FLAGS = [
    "authority_transfer",
    "fork_validates_issuer_governance",
    "fork_validates_causality",
    "fork_participates_in_runtime_control",
    "fork_accepts_runtime_credentials",
    "fork_claims_control_path_authority",
]

REQUIRED_TRUE_BOUNDARY_FLAGS = [
    "issuer_invariant_refs_are_opaque_to_fork",
]

REQUIRED_TRUE_EXPECTED_FLAGS = [
    "structural_continuity_test_only",
    "can_preserve",
    "can_compare",
    "can_report_continuity_loss",
    "can_recompute_when_metadata_present",
    "does_not_validate_issuer_governance",
    "does_not_validate_causality",
    "does_not_join_runtime_control_path",
]

VALID_STATUS_VALUES = {"ABSENT", "PENDING", "PRESENT", "UNRESOLVED"}
VALID_DIGEST_STATUS_VALUES = {"NOT_PROVIDED", "PENDING", "PRESENT", "UNRESOLVED"}
DISALLOWED_AMBIGUOUS_STATUS_VALUES = {"pending-or-present", "pending_or_present", "PENDING_OR_PRESENT", "PENDING-OR-PRESENT"}

REQUIRED_DO_NOT_INFER = [
    "GOVERNANCE_AUTHORITY",
    "ADMISSIBILITY_AUTHORITY",
    "AUTHORIZATION_AUTHORITY",
    "RUNTIME_CONTROL_AUTHORITY",
    "COMPLIANCE_APPROVAL",
    "SAFETY_APPROVAL",
    "CAUSAL_AUTHORITY",
    "ISSUER_GOVERNANCE_VALIDITY",
    "FORK_RUNTIME_PARTICIPATION",
]

REQUIRED_NON_CLAIM_TERMS = [
    "validate SC governance authority",
    "admission authority",
    "authorization authority",
    "safety authority",
    "compliance authority",
    "causal authority",
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
        raise ValueError("CBO minimum packet JSON must be UTF-8 without BOM.")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    if not isinstance(data, dict):
        raise ValueError("CBO minimum packet root must be a JSON object.")
    return data


def add_finding(findings: list[dict[str, str]], code: str, path: str, message: str) -> None:
    findings.append({"code": code, "path": path, "message": message})


def get_object(data: dict[str, Any], key: str, findings: list[dict[str, str]]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        add_finding(findings, "FIELD_TYPE_INVALID", key, f"{key} must be an object.")
        return {}
    return value


def get_array(data: dict[str, Any], key: str, findings: list[dict[str, str]], path: str | None = None) -> list[Any]:
    value = data.get(key)
    actual_path = path or key
    if not isinstance(value, list):
        add_finding(findings, "FIELD_TYPE_INVALID", actual_path, f"{actual_path} must be an array.")
        return []
    return value


def array_has_nonempty_strings(values: list[Any]) -> bool:
    return all(isinstance(item, str) and item.strip() for item in values) and len(values) > 0


def validate_packet(data: dict[str, Any], artifact_path: str) -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            add_finding(findings, "REQUIRED_FIELD_MISSING", key, f"Missing required field: {key}")

    if data.get("profile_id") != EXPECTED_PROFILE_ID:
        add_finding(findings, "PROFILE_ID_INVALID", "profile_id", f"profile_id must be {EXPECTED_PROFILE_ID}.")

    if data.get("cbo_version") != EXPECTED_VERSION:
        add_finding(findings, "CBO_VERSION_INVALID", "cbo_version", f"cbo_version must be {EXPECTED_VERSION}.")

    for key in ["cbo_id", "packet_id", "issuer_system", "authority_domain", "stable_workload_id", "emitted_at"]:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            add_finding(findings, "FIELD_TYPE_INVALID", key, f"{key} must be a non-empty string.")

    chain = get_object(data, "continuity_chain", findings)
    for key in REQUIRED_CONTINUITY_CHAIN_FIELDS:
        if key not in chain:
            add_finding(findings, "REQUIRED_FIELD_MISSING", f"continuity_chain.{key}", f"Missing continuity chain field: {key}")

    if not isinstance(chain.get("admission_decision_ref"), str) or not chain.get("admission_decision_ref", "").strip():
        add_finding(findings, "FIELD_TYPE_INVALID", "continuity_chain.admission_decision_ref", "admission_decision_ref must be a non-empty string.")

    for key in ["invariant_binding_refs", "state_transition_refs", "execution_event_refs", "emitted_artifact_refs"]:
        values = chain.get(key)
        if not isinstance(values, list) or not array_has_nonempty_strings(values):
            add_finding(findings, "FIELD_TYPE_INVALID", f"continuity_chain.{key}", f"{key} must be a non-empty array of strings.")

    integrity = get_object(data, "integrity_metadata", findings)
    digest_algorithm = integrity.get("digest_algorithm")
    if digest_algorithm not in {"sha256", "SHA-256"}:
        add_finding(findings, "DIGEST_ALGORITHM_INVALID", "integrity_metadata.digest_algorithm", "digest_algorithm must be sha256 or SHA-256.")

    digest_status = integrity.get("digest_status")
    if digest_status in DISALLOWED_AMBIGUOUS_STATUS_VALUES:
        add_finding(findings, "AMBIGUOUS_STATUS_VALUE", "integrity_metadata.digest_status", "digest_status cannot be pending-or-present.")
    elif digest_status not in VALID_DIGEST_STATUS_VALUES:
        add_finding(findings, "STATUS_VALUE_INVALID", "integrity_metadata.digest_status", "digest_status must be one of NOT_PROVIDED, PENDING, PRESENT, UNRESOLVED.")

    for key in ["seal_status", "anchor_status"]:
        value = integrity.get(key)
        if value in DISALLOWED_AMBIGUOUS_STATUS_VALUES:
            add_finding(findings, "AMBIGUOUS_STATUS_VALUE", f"integrity_metadata.{key}", f"{key} cannot be pending-or-present.")
        elif value not in VALID_STATUS_VALUES:
            add_finding(findings, "STATUS_VALUE_INVALID", f"integrity_metadata.{key}", f"{key} must be one of ABSENT, PENDING, PRESENT, UNRESOLVED.")

    if not isinstance(integrity.get("anchor_refs"), list):
        add_finding(findings, "FIELD_TYPE_INVALID", "integrity_metadata.anchor_refs", "anchor_refs must be an array.")

    boundary = get_object(data, "boundary_semantics", findings)
    for key in REQUIRED_FALSE_BOUNDARY_FLAGS:
        if boundary.get(key) is not False:
            add_finding(findings, "AUTHORITY_BOUNDARY_VIOLATION", f"boundary_semantics.{key}", f"{key} must be false.")

    for key in REQUIRED_TRUE_BOUNDARY_FLAGS:
        if boundary.get(key) is not True:
            add_finding(findings, "OPAQUE_REFERENCE_RULE_VIOLATION", f"boundary_semantics.{key}", f"{key} must be true.")

    issuer_claims = get_array(data, "issuer_claims", findings)
    if not array_has_nonempty_strings(issuer_claims):
        add_finding(findings, "ISSUER_CLAIM_MISSING", "issuer_claims", "issuer_claims must contain at least one non-empty string.")

    issuer_non_claims = get_array(data, "issuer_non_claims", findings)
    joined_non_claims = " ".join(str(item) for item in issuer_non_claims)
    for term in REQUIRED_NON_CLAIM_TERMS:
        if term not in joined_non_claims:
            add_finding(findings, "ISSUER_NON_CLAIM_MISSING", "issuer_non_claims", f"Missing issuer non-claim term: {term}")

    get_array(data, "fork_permissions", findings)
    get_array(data, "fork_restrictions", findings)
    get_array(data, "preservation_refs", findings)
    get_array(data, "recomputation_refs", findings)
    get_array(data, "unresolved_or_excluded_refs", findings)

    downstream = get_object(data, "downstream_constraints", findings)
    do_not_infer = downstream.get("do_not_infer")
    if not isinstance(do_not_infer, list):
        add_finding(findings, "FIELD_TYPE_INVALID", "downstream_constraints.do_not_infer", "do_not_infer must be an array.")
        do_not_infer = []

    for token in REQUIRED_DO_NOT_INFER:
        if token not in do_not_infer:
            add_finding(findings, "DO_NOT_INFER_TOKEN_MISSING", "downstream_constraints.do_not_infer", f"Missing do_not_infer token: {token}")

    if downstream.get("requires_human_or_institutional_interpretation") is not True:
        add_finding(
            findings,
            "INTERPRETATION_CONSTRAINT_MISSING",
            "downstream_constraints.requires_human_or_institutional_interpretation",
            "requires_human_or_institutional_interpretation must be true.",
        )

    expected = get_object(data, "expected_fork_evaluation", findings)
    for key in REQUIRED_TRUE_EXPECTED_FLAGS:
        if expected.get(key) is not True:
            add_finding(findings, "EXPECTED_FORK_EVALUATION_INVALID", f"expected_fork_evaluation.{key}", f"{key} must be true.")

    ok = len(findings) == 0

    return {
        "limitations": {
            "checker_semantics_version": "v0.1",
            "limitations_code": "CBO_MINIMUM_PACKET_CHECKER_LIMITATIONS_v0_1",
            "scope": "STRUCTURAL_CONTINUITY_PACKET_BOUNDARY_VALIDATION_ONLY",
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_compliance": True,
            "does_not_validate_legal_sufficiency": True,
            "does_not_validate_admissibility": True,
            "does_not_validate_authorization": True,
            "does_not_validate_approval": True,
            "does_not_validate_causality": True,
            "does_not_validate_issuer_governance": True,
            "does_not_validate_runtime_execution": True,
            "does_not_validate_invariant_meaning": True,
            "issuer_invariant_refs_are_opaque": True,
            "automation_interpretation_required": True,
            "do_not_map_to": REQUIRED_DO_NOT_INFER,
        },
        "result": {
            "artifact_path": artifact_path,
            "ok": ok,
            "computed_outcome": "CBO_MINIMUM_PACKET_STRUCTURALLY_VALID" if ok else "CBO_MINIMUM_PACKET_BOUNDARY_VIOLATION",
            "result_semantics": (
                "ok means the packet is structurally valid for bounded continuity evaluation only; "
                "it does not validate issuer governance, causality, runtime execution, safety, compliance, "
                "authorization, approval, admissibility, or truth."
            ),
            "findings": findings,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a CBO minimum packet v0.1 artifact.")
    parser.add_argument("artifact", help="Path to CBO minimum packet JSON artifact.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args()

    try:
        data = load_json(Path(args.artifact))
        output = validate_packet(data, args.artifact)
        exit_code = 0 if output["result"]["ok"] else 1
    except Exception as exc:
        output = {
            "limitations": {
                "checker_semantics_version": "v0.1",
                "scope": "STRUCTURAL_CONTINUITY_PACKET_BOUNDARY_VALIDATION_ONLY",
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
        exit_code = 2

    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
