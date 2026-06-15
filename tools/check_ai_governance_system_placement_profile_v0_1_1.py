#!/usr/bin/env python3
"""Fork AI Governance System Placement Profile Checker v0.1.

Bounded structural and boundary checker for AI Governance Mapping Record:
System Placement Profile v0.1.

This checker validates placement-profile record structure, local references,
claim/non-claim boundaries, restricted authority leakage, and unresolved unknown
status. It does not validate legal sufficiency, compliance sufficiency, audit
sufficiency, model safety, semantic truth, runtime behavior, external artifact
existence, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

CHECKER_ID = "ai_governance_system_placement_profile_checker_v0_1"
CHECKER_VERSION = "0.1"
EXPECTED_PROFILE_VERSION = "ai_governance_system_placement_profile.v0.1"

REQUIRED_TOP_LEVEL = [
    "profile_version",
    "system_identity",
    "role_classification",
    "authority_boundary",
    "supported_claims",
    "explicit_non_claims",
    "evidence_inputs",
    "evidence_outputs",
    "handoff_requirements",
    "unresolved_unknowns",
    "verification_state",
]

ROLE_CLASSIFICATIONS = {
    "evaluator",
    "runtime_monitor",
    "policy_mapper",
    "compliance_mapper",
    "legal_review_support",
    "audit_support",
    "human_review_workflow",
    "risk_scoring_system",
    "incident_response_system",
    "evidence_preservation_system",
    "provenance_system",
    "escalation_router",
    "workflow_orchestrator",
}

DOWNSTREAM_ROLES = {
    "legal_reviewer",
    "compliance_officer",
    "audit_reviewer",
    "risk_owner",
    "model_governance_owner",
    "human_decision_authority",
    "incident_response_lead",
    "deployment_approver",
    "policy_owner",
    "runtime_monitor_owner",
}

VERIFICATION_STATES = {
    "SELF_DECLARED",
    "STRUCTURALLY_CHECKED",
    "EXTERNALLY_REVIEWED",
    "VERIFIED_AGAINST_SCHEMA",
    "VERIFIED_AGAINST_CHECKER",
    "INDETERMINATE",
    "NOT_CHECKED",
}

RESTRICTED_AUTHORITY_PATTERNS = [
    ("ERR_RESTRICTED_COMPLIANCE_SATISFACTION", re.compile(r"\bcompliance[-_\s]*satisf(?:ied|action)\b")),
    ("ERR_RESTRICTED_COMPLIANT", re.compile(r"\bcompliant\b|\bcompliance[-_\s]*(?:approved|ready|certified|guaranteed|sufficient)\b")),
    ("ERR_RESTRICTED_LEGAL_APPROVAL", re.compile(r"\blegally[-_\s]*(?:approved|ready|sufficient)\b|\blegal[-_\s]*(?:approval|approved|ready|sufficiency|admissibility|admissible)\b")),
    ("ERR_RESTRICTED_AUDIT_SUFFICIENCY", re.compile(r"\baudit[-_\s]*(?:sufficient|ready|approved|complete)\b")),
    ("ERR_RESTRICTED_CERTIFICATION", re.compile(r"\bcertif(?:y|ied|ication)\b|\bapproved\b|\bapproval\b")),
    ("ERR_RESTRICTED_DEPLOYMENT_AUTHORITY", re.compile(r"\bdeployment[-_\s]*(?:approved|authorized|ready)\b|\bproduction[-_\s]*(?:approved|authorized|ready)\b")),
    ("ERR_RESTRICTED_SAFETY_ASSURANCE", re.compile(r"\bsafe[-_\s]*(?:for[-_\s]*)?(?:deployment|production)\b|\bsafety[-_\s]*(?:assured|guaranteed|certified)\b")),
]

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")
PARSE_FAILED = object()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    # v0.1.1 hardening: normalize compatibility forms, remove zero-width
    # formatting characters, fold common obfuscating separators, strip combining
    # marks, and lower-case before lexical restricted-authority scans.
    text = unicodedata.normalize("NFKC", text)
    zero_width = {"\\u200b", "\\u200c", "\\u200d", "\\ufeff"}
    text = "".join(ch for ch in text if ch not in zero_width and unicodedata.category(ch) != "Cf")
    for dash in ["\\u2010", "\\u2011", "\\u2012", "\\u2013", "\\u2014", "\\u2212"]:
        text = text.replace(dash, "-")
    text = text.replace("_", " ")
    decomposed = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"\\s+", " ", text).strip()
    return text

def check(check_id: str, status: str, message: str, *, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    item: Dict[str, Any] = {
        "check_id": check_id,
        "status": status,
        "message": message,
    }
    if error_code is not None:
        item["error_code"] = error_code
    if details is not None:
        item["details"] = details
    return item


def load_json_record(path: Path) -> Tuple[Optional[Any], Optional[str]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except Exception as exc:  # json.JSONDecodeError plus read errors
        return PARSE_FAILED, f"{type(exc).__name__}: {exc}"

def collect_ids(record: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    ids: List[Tuple[str, str, str]] = []

    def add(section: str, key: str, items: Iterable[Dict[str, Any]]) -> None:
        for item in items:
            if isinstance(item, dict) and isinstance(item.get(key), str):
                ids.append((item[key], section, key))

    add("supported_claims", "claim_id", record.get("supported_claims", []) if isinstance(record.get("supported_claims"), list) else [])
    add("explicit_non_claims", "non_claim_id", record.get("explicit_non_claims", []) if isinstance(record.get("explicit_non_claims"), list) else [])
    add("evidence_inputs", "evidence_input_id", record.get("evidence_inputs", []) if isinstance(record.get("evidence_inputs"), list) else [])
    add("evidence_outputs", "evidence_output_id", record.get("evidence_outputs", []) if isinstance(record.get("evidence_outputs"), list) else [])
    add("handoff_requirements", "handoff_id", record.get("handoff_requirements", []) if isinstance(record.get("handoff_requirements"), list) else [])
    unknowns = record.get("unresolved_unknowns", {})
    if isinstance(unknowns, dict):
        add("unresolved_unknowns.declared_unknown_classes", "unknown_id", unknowns.get("declared_unknown_classes", []) if isinstance(unknowns.get("declared_unknown_classes"), list) else [])
        add("unresolved_unknowns.active_unresolved_unknowns", "unknown_id", unknowns.get("active_unresolved_unknowns", []) if isinstance(unknowns.get("active_unresolved_unknowns"), list) else [])
    add("non_transitive_clauses", "clause_id", record.get("non_transitive_clauses", []) if isinstance(record.get("non_transitive_clauses"), list) else [])
    return ids


def values_by_key(items: Any, key: str) -> Set[str]:
    if not isinstance(items, list):
        return set()
    return {item[key] for item in items if isinstance(item, dict) and isinstance(item.get(key), str)}


def statements(items: Any, id_key: str) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    if not isinstance(items, list):
        return out
    for item in items:
        if isinstance(item, dict):
            identifier = str(item.get(id_key, "<missing-id>"))
            out.append((identifier, normalize_text(item.get("statement", ""))))
    return out


def gather_restricted_scan_fields(record: Dict[str, Any]) -> List[Tuple[str, str]]:
    fields: List[Tuple[str, str]] = []
    for claim in record.get("supported_claims", []) if isinstance(record.get("supported_claims"), list) else []:
        if isinstance(claim, dict):
            cid = claim.get("claim_id", "<missing-claim-id>")
            for field in ["statement", "scope"]:
                if isinstance(claim.get(field), str):
                    fields.append((f"supported_claims.{cid}.{field}", claim[field]))
            for list_field in ["conditions", "limitations"]:
                if isinstance(claim.get(list_field), list):
                    for idx, value in enumerate(claim[list_field]):
                        if isinstance(value, str):
                            fields.append((f"supported_claims.{cid}.{list_field}[{idx}]", value))
    authority = record.get("authority_boundary", {})
    if isinstance(authority, dict):
        for field in ["functional_claim_perimeter"]:
            if isinstance(authority.get(field), str):
                fields.append((f"authority_boundary.{field}", authority[field]))
        for list_field in ["permitted_assertions"]:
            if isinstance(authority.get(list_field), list):
                for idx, value in enumerate(authority[list_field]):
                    if isinstance(value, str):
                        fields.append((f"authority_boundary.{list_field}[{idx}]", value))
    return fields


def schema_equivalent_type_checks(record: Any) -> List[Dict[str, Any]]:
    failures: List[str] = []
    if not isinstance(record, dict):
        return [check("JSON_PARSE", "FAIL", "Top-level JSON value must be an object.", error_code="ERR_JSON_TOP_LEVEL_NOT_OBJECT")]

    required_missing = [field for field in REQUIRED_TOP_LEVEL if field not in record]
    if required_missing:
        return [check("REQUIRED_FIELDS_PRESENT", "FAIL", "Required top-level fields are missing.", error_code="ERR_REQUIRED_FIELDS_MISSING", details={"missing": required_missing})]
    return [check("REQUIRED_FIELDS_PRESENT", "PASS", "All required top-level fields are present.")]


def run_checks(record: Optional[Any], record_path: Path, schema_path: Path) -> List[Dict[str, Any]]:
    checks: List[Dict[str, Any]] = []

    if schema_path.is_file():
        checks.append(check("SCHEMA_FILE_PRESENT", "PASS", "Schema file is present and readable as a file."))
    else:
        checks.append(check("SCHEMA_FILE_PRESENT", "FAIL", "Schema file is missing or is not a file.", error_code="ERR_SCHEMA_FILE_MISSING", details={"schema_path": str(schema_path)}))

    if record is PARSE_FAILED:
        checks.append(check("JSON_PARSE", "FAIL", "Record could not be parsed as JSON.", error_code="ERR_JSON_PARSE"))
        return checks

    if not isinstance(record, dict):
        checks.append(check("JSON_PARSE", "FAIL", "Top-level JSON value must be an object.", error_code="ERR_JSON_TOP_LEVEL_NOT_OBJECT"))
        return checks
    checks.append(check("JSON_PARSE", "PASS", "Record parsed as a top-level JSON object."))

    missing = [field for field in REQUIRED_TOP_LEVEL if field not in record]
    if missing:
        checks.append(check("REQUIRED_FIELDS_PRESENT", "FAIL", "Required top-level fields are missing.", error_code="ERR_REQUIRED_FIELDS_MISSING", details={"missing": missing}))
    else:
        checks.append(check("REQUIRED_FIELDS_PRESENT", "PASS", "All required top-level fields are present."))

    # Version pin.
    if record.get("profile_version") == EXPECTED_PROFILE_VERSION:
        checks.append(check("PROFILE_VERSION_VALID", "PASS", "Profile version matches v0.1 contract."))
    else:
        checks.append(check("PROFILE_VERSION_VALID", "FAIL", "Profile version does not match v0.1 contract.", error_code="ERR_PROFILE_VERSION_INVALID", details={"expected": EXPECTED_PROFILE_VERSION, "actual": record.get("profile_version")}))

    # Role classification.
    roles = record.get("role_classification")
    invalid_roles: List[Any] = []
    if isinstance(roles, list) and roles:
        invalid_roles = [role for role in roles if role not in ROLE_CLASSIFICATIONS]
    else:
        invalid_roles = [roles]
    if invalid_roles:
        checks.append(check("ROLE_CLASSIFICATION_VALID", "FAIL", "Role classification contains unknown or invalid role values.", error_code="ERR_ROLE_CLASSIFICATION_INVALID", details={"invalid_roles": invalid_roles}))
    else:
        checks.append(check("ROLE_CLASSIFICATION_VALID", "PASS", "Role classification values are within the allowed v0.1 enum."))

    # Verification state enum.
    verification_state = record.get("verification_state", {})
    state = verification_state.get("state") if isinstance(verification_state, dict) else None
    if state in VERIFICATION_STATES:
        checks.append(check("VERIFICATION_STATE_DECLARED", "PASS", "Verification state is declared using an allowed v0.1 value."))
    else:
        checks.append(check("VERIFICATION_STATE_DECLARED", "FAIL", "Verification state is missing or invalid.", error_code="ERR_VERIFICATION_STATE_INVALID", details={"actual": state}))

    # Claim/non-claim arrays.
    supported_claims = record.get("supported_claims")
    explicit_non_claims = record.get("explicit_non_claims")
    if isinstance(supported_claims, list) and supported_claims and isinstance(explicit_non_claims, list) and explicit_non_claims:
        checks.append(check("CLAIM_NONCLAIM_ARRAYS_PRESENT", "PASS", "Supported claims and explicit non-claims arrays are present and non-empty."))
    else:
        checks.append(check("CLAIM_NONCLAIM_ARRAYS_PRESENT", "FAIL", "Supported claims and explicit non-claims arrays must be present and non-empty.", error_code="ERR_CLAIM_NONCLAIM_ARRAYS_MISSING"))

    claim_statements = statements(supported_claims, "claim_id")
    nonclaim_statements = statements(explicit_non_claims, "non_claim_id")
    unknown_obj = record.get("unresolved_unknowns", {}) if isinstance(record.get("unresolved_unknowns"), dict) else {}
    unknown_items: List[Dict[str, Any]] = []
    if isinstance(unknown_obj, dict):
        unknown_items += unknown_obj.get("declared_unknown_classes", []) if isinstance(unknown_obj.get("declared_unknown_classes"), list) else []
        unknown_items += unknown_obj.get("active_unresolved_unknowns", []) if isinstance(unknown_obj.get("active_unresolved_unknowns"), list) else []
    unknown_statements = statements(unknown_items, "unknown_id")

    def overlap(a: List[Tuple[str, str]], b: List[Tuple[str, str]]) -> List[Dict[str, str]]:
        b_by_statement: Dict[str, List[str]] = {}
        for bid, stmt in b:
            if stmt:
                b_by_statement.setdefault(stmt, []).append(bid)
        overlaps: List[Dict[str, str]] = []
        for aid, stmt in a:
            if stmt and stmt in b_by_statement:
                for bid in b_by_statement[stmt]:
                    overlaps.append({"left_id": aid, "right_id": bid, "statement": stmt})
        return overlaps

    cn_overlap = overlap(claim_statements, nonclaim_statements)
    if cn_overlap:
        checks.append(check("CLAIM_NONCLAIM_DISJOINT", "FAIL", "Supported claims and explicit non-claims overlap after normalization.", error_code="ERR_CLAIM_NONCLAIM_OVERLAP", details={"overlaps": cn_overlap}))
    else:
        checks.append(check("CLAIM_NONCLAIM_DISJOINT", "PASS", "Supported claims and explicit non-claims are disjoint by normalized statement."))

    cu_overlap = overlap(claim_statements, unknown_statements)
    if cu_overlap:
        checks.append(check("CLAIM_UNKNOWN_DISJOINT", "FAIL", "Supported claims and unresolved unknowns overlap after normalization.", error_code="ERR_CLAIM_UNKNOWN_OVERLAP", details={"overlaps": cu_overlap}))
    else:
        checks.append(check("CLAIM_UNKNOWN_DISJOINT", "PASS", "Supported claims and unresolved unknowns are disjoint by normalized statement."))

    nu_overlap = overlap(nonclaim_statements, unknown_statements)
    if nu_overlap:
        checks.append(check("NONCLAIM_UNKNOWN_DISJOINT", "FAIL", "Explicit non-claims and unresolved unknowns overlap after normalization.", error_code="ERR_NONCLAIM_UNKNOWN_OVERLAP", details={"overlaps": nu_overlap}))
    else:
        checks.append(check("NONCLAIM_UNKNOWN_DISJOINT", "PASS", "Explicit non-claims and unresolved unknowns are disjoint by normalized statement."))

    # Restricted authority guard scans claim/permitted-assertion surfaces, not explicit non-claims.
    restricted_hits: List[Dict[str, str]] = []
    for field_path, raw_text in gather_restricted_scan_fields(record):
        normalized = normalize_text(raw_text)
        for error_code, pattern in RESTRICTED_AUTHORITY_PATTERNS:
            if pattern.search(normalized):
                restricted_hits.append({"field": field_path, "error_code": error_code, "matched_text": normalized})
    if restricted_hits:
        checks.append(check("RESTRICTED_AUTHORITY_CLAIM_GUARD", "FAIL", "Restricted legal, compliance, audit, approval, safety, or deployment-authority language appeared in claim-bearing fields.", error_code="ERR_RESTRICTED_AUTHORITY_CLAIM", details={"hits": restricted_hits}))
    else:
        checks.append(check("RESTRICTED_AUTHORITY_CLAIM_GUARD", "PASS", "No restricted authority leakage detected in claim-bearing fields."))

    # ID uniqueness and format.
    ids = collect_ids(record)
    seen: Dict[str, List[Tuple[str, str]]] = {}
    invalid_id_format: List[Dict[str, str]] = []
    for identifier, section, key in ids:
        seen.setdefault(identifier, []).append((section, key))
        if not ID_PATTERN.match(identifier):
            invalid_id_format.append({"id": identifier, "section": section, "key": key})
    duplicates = {identifier: locations for identifier, locations in seen.items() if len(locations) > 1}
    if duplicates:
        checks.append(check("UNIQUE_IDS", "FAIL", "Duplicate IDs detected across placement profile boundary items.", error_code="ERR_DUPLICATE_ID", details={"duplicates": duplicates}))
    else:
        checks.append(check("UNIQUE_IDS", "PASS", "All collected placement-profile IDs are unique."))
    if invalid_id_format:
        checks.append(check("ID_FORMAT_VALID", "FAIL", "One or more IDs violate the v0.1 ID pattern.", error_code="ERR_ID_FORMAT_INVALID", details={"invalid_ids": invalid_id_format}))
    else:
        checks.append(check("ID_FORMAT_VALID", "PASS", "All collected IDs match the v0.1 ID pattern."))

    # Local reference integrity.
    input_ids = values_by_key(record.get("evidence_inputs"), "evidence_input_id")
    claim_ids = values_by_key(record.get("supported_claims"), "claim_id")
    nonclaim_ids = values_by_key(record.get("explicit_non_claims"), "non_claim_id")
    output_ids = values_by_key(record.get("evidence_outputs"), "evidence_output_id")
    unknown_ids = {identifier for identifier, section, key in ids if key == "unknown_id"}

    claim_evidence_gaps: List[Dict[str, Any]] = []
    for claim_item in record.get("supported_claims", []) if isinstance(record.get("supported_claims"), list) else []:
        if not isinstance(claim_item, dict):
            continue
        refs = claim_item.get("evidence_basis", [])
        missing_refs = sorted([ref for ref in refs if ref not in input_ids]) if isinstance(refs, list) else ["<evidence_basis_not_array>"]
        if not refs or missing_refs:
            claim_evidence_gaps.append({"claim_id": claim_item.get("claim_id"), "missing_evidence_input_ids": missing_refs})
    if claim_evidence_gaps:
        checks.append(check("CLAIM_EVIDENCE_BASIS_PRESENT", "FAIL", "One or more supported claims lack a resolvable declared evidence basis.", error_code="ERR_CLAIM_EVIDENCE_BASIS_MISSING", details={"gaps": claim_evidence_gaps}))
    else:
        checks.append(check("CLAIM_EVIDENCE_BASIS_PRESENT", "PASS", "Every supported claim references declared evidence inputs."))

    local_gaps: List[Dict[str, Any]] = []
    for output in record.get("evidence_outputs", []) if isinstance(record.get("evidence_outputs"), list) else []:
        if not isinstance(output, dict):
            continue
        missing_claims = sorted([ref for ref in output.get("supports_claim_ids", []) if ref not in claim_ids]) if isinstance(output.get("supports_claim_ids", []), list) else ["<supports_claim_ids_not_array>"]
        missing_nonclaims = sorted([ref for ref in output.get("carries_non_claim_ids", []) if ref not in nonclaim_ids]) if isinstance(output.get("carries_non_claim_ids", []), list) else ["<carries_non_claim_ids_not_array>"]
        if missing_claims or missing_nonclaims:
            local_gaps.append({"evidence_output_id": output.get("evidence_output_id"), "missing_claim_ids": missing_claims, "missing_non_claim_ids": missing_nonclaims})
    for handoff in record.get("handoff_requirements", []) if isinstance(record.get("handoff_requirements"), list) else []:
        if not isinstance(handoff, dict):
            continue
        missing_outputs = sorted([ref for ref in handoff.get("evidence_output_ids", []) if ref not in output_ids]) if isinstance(handoff.get("evidence_output_ids", []), list) else ["<evidence_output_ids_not_array>"]
        missing_nonclaims = sorted([ref for ref in handoff.get("non_claim_ids_to_preserve", []) if ref not in nonclaim_ids]) if isinstance(handoff.get("non_claim_ids_to_preserve", []), list) else ["<non_claim_ids_to_preserve_not_array>"]
        missing_unknowns = sorted([ref for ref in handoff.get("unknown_ids_to_preserve", []) if ref not in unknown_ids]) if isinstance(handoff.get("unknown_ids_to_preserve", []), list) else ["<unknown_ids_to_preserve_not_array>"]
        if missing_outputs or missing_nonclaims or missing_unknowns:
            local_gaps.append({"handoff_id": handoff.get("handoff_id"), "missing_evidence_output_ids": missing_outputs, "missing_non_claim_ids": missing_nonclaims, "missing_unknown_ids": missing_unknowns})
    if local_gaps:
        checks.append(check("LOCAL_REFERENCE_INTEGRITY", "FAIL", "One or more local ID references do not resolve within the record.", error_code="ERR_LOCAL_REFERENCE_GAP", details={"gaps": local_gaps}))
    else:
        checks.append(check("LOCAL_REFERENCE_INTEGRITY", "PASS", "All local placement-profile references resolve within the record."))

    # Handoff role validation.
    invalid_handoff_roles: List[Dict[str, Any]] = []
    for handoff in record.get("handoff_requirements", []) if isinstance(record.get("handoff_requirements"), list) else []:
        if not isinstance(handoff, dict):
            continue
        role = handoff.get("required_downstream_role")
        if role not in DOWNSTREAM_ROLES:
            invalid_handoff_roles.append({"handoff_id": handoff.get("handoff_id"), "role": role})
    if invalid_handoff_roles:
        checks.append(check("HANDOFF_ROLE_REFERENCES_VALID", "FAIL", "One or more handoff roles are outside the allowed downstream-role enum.", error_code="ERR_HANDOFF_ROLE_INVALID", details={"invalid_roles": invalid_handoff_roles}))
    else:
        checks.append(check("HANDOFF_ROLE_REFERENCES_VALID", "PASS", "All declared handoff roles are within the allowed downstream-role enum."))

    active_unknowns = []
    if isinstance(unknown_obj, dict) and isinstance(unknown_obj.get("active_unresolved_unknowns"), list):
        active_unknowns = unknown_obj.get("active_unresolved_unknowns", [])
    if active_unknowns or state == "INDETERMINATE":
        checks.append(check("UNRESOLVED_UNKNOWNS_STATUS", "INDETERMINATE", "Active unresolved unknowns or INDETERMINATE verification state prevent clean closure.", error_code="ERR_ACTIVE_UNRESOLVED_UNKNOWN", details={"active_unresolved_unknown_count": len(active_unknowns), "verification_state": state}))
    else:
        checks.append(check("UNRESOLVED_UNKNOWNS_STATUS", "PASS", "No active unresolved unknowns declare indeterminate status."))

    if isinstance(record.get("non_transitive_clauses"), list) and record.get("non_transitive_clauses"):
        checks.append(check("NON_TRANSITIVE_CLAUSES_PRESENT", "PASS", "Non-transitive clauses are present."))
    else:
        checks.append(check("NON_TRANSITIVE_CLAUSES_PRESENT", "PASS", "Non-transitive clauses are optional in v0.1 and were not required for closure."))

    return checks


def overall_status(checks: List[Dict[str, Any]]) -> str:
    if any(c["status"] == "FAIL" for c in checks):
        return "FAIL"
    if any(c["status"] == "INDETERMINATE" for c in checks):
        return "INDETERMINATE"
    return "PASS"


def make_result(record: Optional[Any], record_path: Path, schema_path: Path, checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    status = overall_status(checks)
    record_id = None
    system_id = None
    if isinstance(record, dict):
        identity = record.get("system_identity", {})
        if isinstance(identity, dict):
            record_id = identity.get("record_id")
            system_id = identity.get("system_id")
    return {
        "checker_id": CHECKER_ID,
        "checker_version": CHECKER_VERSION,
        "checked_at_utc": utc_now(),
        "record_path": str(record_path.resolve()),
        "schema_path": str(schema_path.resolve()),
        "record_id": record_id,
        "system_id": system_id,
        "overall_status": status,
        "status_meaning": {
            "PASS": "Placement profile is structurally valid and boundary-consistent under v0.1 checker scope.",
            "FAIL": "Placement profile violates required structure or boundary rules under v0.1 checker scope.",
            "INDETERMINATE": "Placement profile is structurally interpretable but declares active unresolved unknowns that prevent closure under v0.1 checker scope.",
        }[status],
        "claim_boundary": "STRUCTURAL_AND_BOUNDARY_VALIDATION_ONLY",
        "non_claims": [
            "Does not validate semantic truth of claims.",
            "Does not validate legal sufficiency.",
            "Does not validate compliance sufficiency.",
            "Does not validate audit sufficiency.",
            "Does not validate model safety.",
            "Does not provide runtime enforcement.",
            "Does not grant institutional authority.",
            "Does not verify external artifact existence.",
            "Does not perform cross-record graph validation.",
        ],
        "checks": checks,
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
    }


def make_normalized_result(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "checker_id": result["checker_id"],
        "checker_version": result["checker_version"],
        "record_id": result.get("record_id"),
        "system_id": result.get("system_id"),
        "overall_status": result["overall_status"],
        "claim_boundary": result["claim_boundary"],
        "non_claims": result["non_claims"],
        "checks": [
            {
                key: value
                for key, value in c.items()
                if key in {"check_id", "status", "error_code", "message", "details"}
            }
            for c in sorted(result["checks"], key=lambda item: item["check_id"])
        ],
    }


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check an AI Governance System Placement Profile v0.1 record.")
    parser.add_argument("--record", required=True, help="Path to placement profile JSON record")
    parser.add_argument("--schema", required=True, help="Path to placement profile JSON schema")
    parser.add_argument("--output", required=False, help="Path to full result JSON")
    parser.add_argument("--normalized-output", required=False, help="Path to normalized deterministic result JSON")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    record_path = Path(args.record)
    schema_path = Path(args.schema)

    record, parse_error = load_json_record(record_path)
    checks = run_checks(record, record_path, schema_path)
    if parse_error is not None:
        # Replace generic JSON parse message detail with concrete parse error.
        for item in checks:
            if item["check_id"] == "JSON_PARSE" and item["status"] == "FAIL":
                item["details"] = {"parse_error": parse_error}

    result = make_result(record if isinstance(record, dict) else None, record_path, schema_path, checks)
    normalized = make_normalized_result(result)

    if args.output:
        write_json(Path(args.output), result)
    if args.normalized_output:
        write_json(Path(args.normalized_output), normalized)

    status = result["overall_status"]
    if args.output:
        print(f"result_path={Path(args.output).resolve()}")
    if args.normalized_output:
        print(f"normalized_result_path={Path(args.normalized_output).resolve()}")
    print(f"AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_V0_1_CHECK_{status}")

    if status == "PASS":
        return 0
    if status == "INDETERMINATE":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())