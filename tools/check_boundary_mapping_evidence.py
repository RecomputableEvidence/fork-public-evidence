#!/usr/bin/env python3
"""
Fork Boundary Mapping Evidence Checker v0.1

Validates Fork boundary mapping evidence records.

Scope:
- structural validation for v0.1 boundary mapping evidence examples
- bounded result-token validation
- required non-claim preservation
- required non-inheritance result validation
- no legal/compliance/safety/truth/approval/runtime determinations

Non-scope:
- does not establish legal sufficiency
- does not establish compliance
- does not establish safety
- does not establish truth
- does not establish external endorsement
- does not validate real-world domain facts
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ARTIFACT_TYPE = "FORK_BOUNDARY_MAPPING_EVIDENCE"
ARTIFACT_VERSION = "v0.1"

ALLOWED_RESULT_TOKENS = {
    "BOUNDARY_MAPPING_RECORDED",
    "EVIDENCE_PRESERVED",
    "AUTHORITY_INHERITANCE_NOT_ESTABLISHED",
    "SCOPE_EXPANSION_RECORDED",
    "NON_CLAIM_PRESERVED",
    "UNRESOLVED_AUTHORITY_ASSUMPTION_RECORDED",
}

REQUIRED_RESULT_TOKENS = {
    "BOUNDARY_MAPPING_RECORDED",
    "EVIDENCE_PRESERVED",
    "AUTHORITY_INHERITANCE_NOT_ESTABLISHED",
    "NON_CLAIM_PRESERVED",
    "UNRESOLVED_AUTHORITY_ASSUMPTION_RECORDED",
}

REQUIRED_PRESERVATION_RESULTS = {
    "SOURCE_CLAIM_RECORDED",
    "EVIDENCE_REFERENCES_PRESERVED",
    "BOUNDARY_CROSSING_RECORDED",
    "DOWNSTREAM_ASSUMPTION_RECORDED",
    "NON_CLAIMS_PRESERVED",
    "UNRESOLVED_QUESTIONS_RECORDED",
}

AUTHORITY_TO_REQUIRED_NON_INHERITANCE = {
    "DEPLOYMENT_SAFETY": "SAFETY_INHERITANCE_NOT_ESTABLISHED",
    "COMPLIANCE_STATUS": "COMPLIANCE_INHERITANCE_NOT_ESTABLISHED",
    "ACTION_AUTHORITY": "ACTION_AUTHORITY_INHERITANCE_NOT_ESTABLISHED",
    "RUNTIME_AUTHORIZATION": "ACTION_AUTHORITY_INHERITANCE_NOT_ESTABLISHED",
    "LEGAL_SUFFICIENCY": "LEGAL_SUFFICIENCY_INHERITANCE_NOT_ESTABLISHED",
    "APPROVAL": "APPROVAL_INHERITANCE_NOT_ESTABLISHED",
    "TRUTH_CERTIFICATION": "TRUTH_INHERITANCE_NOT_ESTABLISHED",
}

AUTHORITY_TO_REQUIRED_NON_CLAIM_TEXT = {
    "DEPLOYMENT_SAFETY": "deployment safety",
    "COMPLIANCE_STATUS": "compliance",
    "ACTION_AUTHORITY": "action authority",
    "RUNTIME_AUTHORIZATION": "runtime authorization",
    "LEGAL_SUFFICIENCY": "legal sufficiency",
    "AUDIT_ACCEPTANCE": "audit acceptance",
    "APPROVAL": "approval",
    "TRUTH_CERTIFICATION": "truth",
    "EXTERNAL_ENDORSEMENT": "external endorsement",
    "BUSINESS_FITNESS": "business fitness",
}

REQUIRED_TOP_LEVEL_FIELDS = {
    "artifact_id",
    "artifact_type",
    "artifact_version",
    "mapping_id",
    "mapping_title",
    "domain",
    "native_domain_object",
    "source_claim",
    "evidence_preserved",
    "boundary_crossing",
    "downstream_assumption",
    "attempted_inherited_authority",
    "fork_preservation_result",
    "fork_non_inheritance_result",
    "unresolved_questions",
    "non_claims",
    "result_tokens",
    "determination",
    "created_at",
}


def fail(errors: list[dict[str, str]], code: str, message: str) -> None:
    errors.append({"code": code, "message": message})


def require_object(value: Any, errors: list[dict[str, str]], field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(errors, "INVALID_OBJECT", f"{field} must be an object")
        return {}
    return value


def require_array(value: Any, errors: list[dict[str, str]], field: str, min_items: int = 1) -> list[Any]:
    if not isinstance(value, list):
        fail(errors, "INVALID_ARRAY", f"{field} must be an array")
        return []
    if len(value) < min_items:
        fail(errors, "ARRAY_TOO_SHORT", f"{field} must contain at least {min_items} item(s)")
    return value


def require_string(value: Any, errors: list[dict[str, str]], field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(errors, "INVALID_STRING", f"{field} must be a non-empty string")
        return ""
    return value


def text_contains_any(items: list[Any], needle: str) -> bool:
    lowered = needle.lower()
    return any(isinstance(item, str) and lowered in item.lower() for item in items)


def validate_record(record: dict[str, Any], path: Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []

    missing = sorted(REQUIRED_TOP_LEVEL_FIELDS - set(record.keys()))
    for field in missing:
        fail(errors, "MISSING_REQUIRED_FIELD", f"missing required field: {field}")

    if record.get("artifact_type") != ARTIFACT_TYPE:
        fail(errors, "INVALID_ARTIFACT_TYPE", f"artifact_type must be {ARTIFACT_TYPE}")

    if record.get("artifact_version") != ARTIFACT_VERSION:
        fail(errors, "INVALID_ARTIFACT_VERSION", f"artifact_version must be {ARTIFACT_VERSION}")

    if record.get("determination") != "BOUNDARY_MAPPING_RECORDED":
        fail(errors, "INVALID_DETERMINATION", "determination must remain BOUNDARY_MAPPING_RECORDED")

    mapping_id = require_string(record.get("mapping_id"), errors, "mapping_id")
    if mapping_id and not mapping_id.endswith("_v0_1"):
        fail(errors, "INVALID_MAPPING_ID", "mapping_id must end with _v0_1")

    native_object = require_object(record.get("native_domain_object"), errors, "native_domain_object")
    for field in ("object_type", "object_id", "description"):
        require_string(native_object.get(field), errors, f"native_domain_object.{field}")

    source_claim = require_object(record.get("source_claim"), errors, "source_claim")
    for field in ("claim_id", "statement", "scope"):
        require_string(source_claim.get(field), errors, f"source_claim.{field}")

    evidence_refs = require_array(source_claim.get("evidence_refs"), errors, "source_claim.evidence_refs")
    for idx, ref in enumerate(evidence_refs):
        require_string(ref, errors, f"source_claim.evidence_refs[{idx}]")

    evidence_preserved = require_array(record.get("evidence_preserved"), errors, "evidence_preserved")
    for idx, evidence in enumerate(evidence_preserved):
        evidence_obj = require_object(evidence, errors, f"evidence_preserved[{idx}]")
        for field in ("evidence_id", "evidence_type", "description"):
            require_string(evidence_obj.get(field), errors, f"evidence_preserved[{idx}].{field}")

    boundary_crossing = require_object(record.get("boundary_crossing"), errors, "boundary_crossing")
    for field in ("from_context", "to_context", "boundary_type", "transition_description"):
        require_string(boundary_crossing.get(field), errors, f"boundary_crossing.{field}")

    downstream_assumption = require_object(record.get("downstream_assumption"), errors, "downstream_assumption")
    for field in ("assumption_id", "statement", "assumption_type"):
        require_string(downstream_assumption.get(field), errors, f"downstream_assumption.{field}")

    attempted_authority = require_array(
        record.get("attempted_inherited_authority"),
        errors,
        "attempted_inherited_authority",
    )

    preservation_results = set(
        require_array(record.get("fork_preservation_result"), errors, "fork_preservation_result")
    )
    missing_preservation = sorted(REQUIRED_PRESERVATION_RESULTS - preservation_results)
    for token in missing_preservation:
        fail(errors, "MISSING_PRESERVATION_RESULT", f"missing preservation result: {token}")

    non_inheritance_results = set(
        require_array(record.get("fork_non_inheritance_result"), errors, "fork_non_inheritance_result")
    )

    if "AUTHORITY_INHERITANCE_NOT_ESTABLISHED" not in non_inheritance_results:
        fail(
            errors,
            "MISSING_AUTHORITY_NON_INHERITANCE_RESULT",
            "fork_non_inheritance_result must include AUTHORITY_INHERITANCE_NOT_ESTABLISHED",
        )

    non_claims = require_array(record.get("non_claims"), errors, "non_claims")
    if not text_contains_any(non_claims, "legal sufficiency"):
        fail(errors, "MISSING_LEGAL_SUFFICIENCY_NON_CLAIM", "non_claims must preserve legal sufficiency as a non-claim")

    for authority in attempted_authority:
        require_string(authority, errors, "attempted_inherited_authority[]")

        required_result = AUTHORITY_TO_REQUIRED_NON_INHERITANCE.get(authority)
        if required_result and required_result not in non_inheritance_results:
            fail(
                errors,
                "MISSING_AUTHORITY_SPECIFIC_NON_INHERITANCE_RESULT",
                f"{authority} requires {required_result}",
            )

        required_text = AUTHORITY_TO_REQUIRED_NON_CLAIM_TEXT.get(authority)
        if required_text and not text_contains_any(non_claims, required_text):
            fail(
                errors,
                "MISSING_AUTHORITY_SPECIFIC_NON_CLAIM",
                f"{authority} requires a non-claim mentioning {required_text}",
            )

    unresolved = require_array(record.get("unresolved_questions"), errors, "unresolved_questions", min_items=1)
    for idx, question in enumerate(unresolved):
        require_string(question, errors, f"unresolved_questions[{idx}]")

    result_tokens = set(require_array(record.get("result_tokens"), errors, "result_tokens"))
    unknown_tokens = sorted(result_tokens - ALLOWED_RESULT_TOKENS)
    for token in unknown_tokens:
        fail(errors, "UNKNOWN_RESULT_TOKEN", f"unknown result token: {token}")

    missing_tokens = sorted(REQUIRED_RESULT_TOKENS - result_tokens)
    for token in missing_tokens:
        fail(errors, "MISSING_REQUIRED_RESULT_TOKEN", f"missing required result token: {token}")

    return {
        "path": str(path),
        "mapping_id": record.get("mapping_id"),
        "determination": "STRUCTURAL_PASS" if not errors else "STRUCTURAL_FAIL",
        "errors": errors,
    }


def load_json(path: Path) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as exc:
        return None, {"code": "JSON_LOAD_ERROR", "message": f"{path}: {exc}"}

    if not isinstance(data, dict):
        return None, {"code": "INVALID_JSON_ROOT", "message": f"{path}: root must be an object"}

    return data, None


def default_paths(repo_root: Path) -> list[Path]:
    return sorted((repo_root / "examples" / "fork_boundary_mapping_evidence").glob("*.json"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Fork boundary mapping evidence records.")
    parser.add_argument("paths", nargs="*", help="Specific boundary mapping evidence JSON files to check.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to current directory.")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    paths = [Path(p).resolve() for p in args.paths] if args.paths else default_paths(repo_root)

    if not paths:
        output = {
            "checker": "check_boundary_mapping_evidence.py",
            "checker_version": "v0.1",
            "status": "STRUCTURAL_FAIL",
            "errors": [{"code": "NO_INPUT_FILES", "message": "no boundary mapping evidence files found"}],
            "records": [],
        }
        print(json.dumps(output, indent=2, sort_keys=True))
        return 1

    records: list[dict[str, Any]] = []
    load_errors: list[dict[str, str]] = []

    for path in paths:
        data, error = load_json(path)
        if error:
            load_errors.append(error)
            continue
        assert data is not None
        records.append(validate_record(data, path))

    failed = bool(load_errors) or any(record["determination"] != "STRUCTURAL_PASS" for record in records)

    output = {
        "checker": "check_boundary_mapping_evidence.py",
        "checker_version": "v0.1",
        "status": "STRUCTURAL_FAIL" if failed else "STRUCTURAL_PASS",
        "record_count": len(records),
        "errors": load_errors,
        "records": records,
        "non_claims": [
            "Checker does not establish legal sufficiency.",
            "Checker does not establish regulatory compliance.",
            "Checker does not establish audit acceptance.",
            "Checker does not establish deployment safety.",
            "Checker does not establish model truth.",
            "Checker does not establish agent authorization.",
            "Checker does not establish runtime enforcement.",
            "Checker does not establish external endorsement.",
            "Checker does not establish business fitness.",
            "Checker does not establish claim inheritance."
        ],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
