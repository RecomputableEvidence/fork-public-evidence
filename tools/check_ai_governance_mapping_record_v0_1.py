#!/usr/bin/env python3
"""
AI Governance System Mapping Record checker v0.1.

This checker validates machine-readable mapping records for claim-boundary placement.
It is intentionally bounded: it checks structure, non-claims, prohibited inheritance,
unknowns, authority boundaries, and safe handoff constraints.

It does not prove legal sufficiency, compliance satisfaction, AI output correctness,
decision correctness, audit sufficiency, or market validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "ai_governance_system_mapping_record.v0.1"

REQUIRED_FIELDS: dict[str, type] = {
    "record_version": str,
    "record_status": str,
    "system_id": str,
    "system_name": str,
    "system_owner": str,
    "record_author": str,
    "created_at_utc": str,
    "system_function": str,
    "pipeline_position": str,
    "input_assumptions": list,
    "supported_claims": list,
    "explicit_non_claims": list,
    "emitted_artifacts": list,
    "consumable_artifacts": list,
    "verification_model": dict,
    "evaluation_boundary": dict,
    "authority_boundary": dict,
    "dependency_boundary": list,
    "unknowns": list,
    "failure_states": list,
    "safe_handoffs": list,
    "prohibited_claim_inheritance": list,
    "re_verification_requirements": list,
    "institutional_dependencies": list,
    "mapping_summary": str,
    "declaration": dict,
}

FORK_REQUIRED_NON_CLAIMS = [
    "AI output correctness",
    "decision correctness",
    "source completeness",
    "legal admissibility",
    "compliance satisfaction",
    "audit sufficiency",
    "institutional authority",
    "runtime control",
    "execution permissioning",
    "policy authority",
]

RESTRICTED_AUTHORITY_CLAIM_TERMS = [
    "ai output correctness",
    "decision correctness",
    "source completeness",
    "legal admissibility",
    "compliance satisfaction",
    "audit sufficiency",
    "institutional authority",
    "runtime control",
    "execution permissioning",
    "policy authority",
    "risk acceptance",
    "remediation sufficiency",
    "reporting sufficiency",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(value: Any) -> str:
    return " ".join(str(value).lower().split())


def item_statement(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("statement", ""))
    return str(item)


def statements(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [item_statement(item) for item in items]


def contains_term(texts: list[str], term: str) -> bool:
    t = normalize_text(term)
    return any(t in normalize_text(text) for text in texts)


def add_check(
    result: dict[str, Any],
    check_id: str,
    status: str,
    detail: Any = None,
) -> None:
    result["checks"].append(
        {
            "check_id": check_id,
            "status": status,
            "detail": detail,
        }
    )
    if status == "FAIL":
        result["errors"].append({"check_id": check_id, "detail": detail})
    elif status == "WARN":
        result["warnings"].append({"check_id": check_id, "detail": detail})
    elif status == "INDETERMINATE":
        result["indeterminate_signals"].append({"check_id": check_id, "detail": detail})


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def check_required_fields(record: dict[str, Any], result: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        add_check(result, "REQUIRED_FIELDS_PRESENT", "FAIL", {"missing": missing})
    else:
        add_check(result, "REQUIRED_FIELDS_PRESENT", "PASS", sorted(REQUIRED_FIELDS.keys()))

    type_errors: list[dict[str, str]] = []
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in record:
            continue
        if not isinstance(record[field], expected_type):
            type_errors.append(
                {
                    "field": field,
                    "expected": expected_type.__name__,
                    "actual": type(record[field]).__name__,
                }
            )
    if type_errors:
        add_check(result, "FIELD_TYPES", "FAIL", type_errors)
    else:
        add_check(result, "FIELD_TYPES", "PASS", "All present required fields have expected top-level types.")


def check_schema_version(record: dict[str, Any], result: dict[str, Any]) -> None:
    actual = record.get("record_version")
    if actual == SCHEMA_VERSION:
        add_check(result, "SCHEMA_VERSION_PIN", "PASS", actual)
    else:
        add_check(result, "SCHEMA_VERSION_PIN", "FAIL", {"expected": SCHEMA_VERSION, "actual": actual})


def check_non_claims(record: dict[str, Any], result: dict[str, Any]) -> None:
    explicit_non_claims = record.get("explicit_non_claims")
    if nonempty_list(explicit_non_claims):
        add_check(result, "EXPLICIT_NON_CLAIMS_PRESENT", "PASS", len(explicit_non_claims))
    else:
        add_check(result, "EXPLICIT_NON_CLAIMS_PRESENT", "FAIL", "explicit_non_claims must be a non-empty array.")

    prohibited = record.get("prohibited_claim_inheritance")
    if nonempty_list(prohibited):
        add_check(result, "PROHIBITED_CLAIM_INHERITANCE_PRESENT", "PASS", len(prohibited))
    else:
        add_check(result, "PROHIBITED_CLAIM_INHERITANCE_PRESENT", "FAIL", "prohibited_claim_inheritance must be a non-empty array.")


def check_claim_nonclaim_disjoint(record: dict[str, Any], result: dict[str, Any]) -> None:
    supported = statements(record.get("supported_claims", []))
    non_claims = statements(record.get("explicit_non_claims", []))
    supported_norm = {normalize_text(s): s for s in supported if normalize_text(s)}
    non_claim_norm = {normalize_text(s): s for s in non_claims if normalize_text(s)}
    overlap_keys = sorted(set(supported_norm).intersection(set(non_claim_norm)))
    if overlap_keys:
        add_check(
            result,
            "CLAIM_NONCLAIM_DISJOINT",
            "FAIL",
            [{"supported_claim": supported_norm[k], "explicit_non_claim": non_claim_norm[k]} for k in overlap_keys],
        )
    else:
        add_check(result, "CLAIM_NONCLAIM_DISJOINT", "PASS", "No exact statement overlap detected.")


def check_safe_handoffs(record: dict[str, Any], result: dict[str, Any]) -> None:
    handoffs = record.get("safe_handoffs", [])
    if not nonempty_list(handoffs):
        add_check(result, "SAFE_HANDOFFS_PRESENT", "FAIL", "safe_handoffs must be a non-empty array.")
        return

    add_check(result, "SAFE_HANDOFFS_PRESENT", "PASS", len(handoffs))

    failures: list[dict[str, Any]] = []
    required_arrays = [
        "claims_that_must_not_transfer",
        "non_claims_that_must_travel",
        "unknowns_that_must_travel",
        "re_verification_required",
    ]

    for idx, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            failures.append({"index": idx, "error": "handoff entry must be an object"})
            continue

        handoff_id = handoff.get("id", f"index_{idx}")
        for field in required_arrays:
            if not nonempty_list(handoff.get(field)):
                failures.append(
                    {
                        "handoff": handoff_id,
                        "field": field,
                        "error": "must be a non-empty array",
                    }
                )

    if failures:
        add_check(result, "SAFE_HANDOFF_CONSTRAINTS", "FAIL", failures)
    else:
        add_check(result, "SAFE_HANDOFF_CONSTRAINTS", "PASS", "All safe handoffs carry non-transfer, non-claim, unknown, and re-verification constraints.")


def check_unknowns_dependencies(record: dict[str, Any], result: dict[str, Any]) -> None:
    unknowns = record.get("unknowns")
    if nonempty_list(unknowns):
        add_check(result, "UNKNOWNS_PRESENT", "PASS", len(unknowns))
    else:
        add_check(result, "UNKNOWNS_PRESENT", "FAIL", "unknowns must be a non-empty array.")

    indeterminate_items: list[dict[str, Any]] = []

    for field in ["dependency_boundary", "unknowns", "institutional_dependencies"]:
        items = record.get(field, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            status = str(item.get("status", "")).upper()
            if status in {"UNRESOLVED", "UNKNOWN", "NOT_CHECKED", "UNAVAILABLE", "REVIEW_REQUIRED"}:
                indeterminate_items.append(
                    {
                        "field": field,
                        "id": item.get("id"),
                        "status": status,
                        "statement": item.get("statement"),
                    }
                )

    record_status = str(record.get("record_status", "")).upper()
    if record_status in {"REVIEW_REQUIRED", "INDETERMINATE"}:
        indeterminate_items.append(
            {
                "field": "record_status",
                "status": record_status,
                "statement": "Record status itself requires indeterminate/review handling.",
            }
        )

    if indeterminate_items:
        add_check(result, "INDETERMINATE_SIGNALS", "INDETERMINATE", indeterminate_items)
    else:
        add_check(result, "INDETERMINATE_SIGNALS", "PASS", "No unresolved dependency, unknown, or review-required signals detected.")


def check_authority_boundary(record: dict[str, Any], result: dict[str, Any]) -> None:
    boundary = record.get("authority_boundary")
    if not isinstance(boundary, dict):
        add_check(result, "AUTHORITY_BOUNDARY_PRESENT", "FAIL", "authority_boundary must be an object.")
        return

    required = [
        "authority_status",
        "authority_basis",
        "authority_claims",
        "non_authorities",
        "human_or_institutional_authority_required",
    ]
    missing = [field for field in required if field not in boundary]
    if missing:
        add_check(result, "AUTHORITY_BOUNDARY_PRESENT", "FAIL", {"missing": missing})
        return

    if not nonempty_list(boundary.get("non_authorities")):
        add_check(result, "AUTHORITY_NON_AUTHORITIES_PRESENT", "FAIL", "authority_boundary.non_authorities must be non-empty.")
    else:
        add_check(result, "AUTHORITY_NON_AUTHORITIES_PRESENT", "PASS", len(boundary.get("non_authorities", [])))

    supported = statements(record.get("supported_claims", []))
    authority_claims = [str(x) for x in boundary.get("authority_claims", [])]
    authority_basis = str(boundary.get("authority_basis", ""))

    restricted_hits: list[dict[str, str]] = []
    authority_text = normalize_text(" ".join(authority_claims) + " " + authority_basis)

    for claim in supported:
        normalized_claim = normalize_text(claim)
        for term in RESTRICTED_AUTHORITY_CLAIM_TERMS:
            if term in normalized_claim and term not in authority_text:
                restricted_hits.append({"claim": claim, "restricted_term": term})

    if restricted_hits:
        add_check(
            result,
            "RESTRICTED_AUTHORITY_CLAIM_GUARD",
            "FAIL",
            {
                "message": "Supported claims include authority/correctness/compliance terms without declared authority basis.",
                "hits": restricted_hits,
            },
        )
    else:
        add_check(result, "RESTRICTED_AUTHORITY_CLAIM_GUARD", "PASS", "No unsupported restricted authority claims detected.")


def check_fork_required_non_claims(record: dict[str, Any], result: dict[str, Any]) -> None:
    system_id = normalize_text(record.get("system_id", ""))
    system_name = normalize_text(record.get("system_name", ""))
    is_fork_record = "fork" in system_id or "fork" in system_name

    if not is_fork_record:
        add_check(result, "FORK_REQUIRED_NON_CLAIMS", "PASS", "Not a Fork-specific mapping record.")
        return

    non_claims = statements(record.get("explicit_non_claims", []))
    missing = [term for term in FORK_REQUIRED_NON_CLAIMS if not contains_term(non_claims, term)]

    if missing:
        add_check(
            result,
            "FORK_REQUIRED_NON_CLAIMS",
            "FAIL",
            {
                "message": "Fork records must preserve the canonical Fork non-claims.",
                "missing": missing,
            },
        )
    else:
        add_check(result, "FORK_REQUIRED_NON_CLAIMS", "PASS", FORK_REQUIRED_NON_CLAIMS)


def finalize_status(result: dict[str, Any]) -> None:
    has_fail = any(c["status"] == "FAIL" for c in result["checks"])
    has_indeterminate = any(c["status"] == "INDETERMINATE" for c in result["checks"])

    if has_fail:
        result["overall_status"] = "FAIL"
    elif has_indeterminate:
        result["overall_status"] = "INDETERMINATE"
    else:
        result["overall_status"] = "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check AI Governance System Mapping Record v0.1.")
    parser.add_argument("--record", required=True, help="Path to mapping record JSON.")
    parser.add_argument("--schema", default="schemas/ai_governance_system_mapping_record_v0_1.schema.json")
    parser.add_argument("--output", default=None, help="Optional JSON result output path.")
    args = parser.parse_args()

    record_path = Path(args.record).resolve()
    schema_path = Path(args.schema).resolve()

    result: dict[str, Any] = {
        "checker_name": "check_ai_governance_mapping_record_v0_1",
        "checker_version": "v0.1",
        "checked_at_utc": now_utc(),
        "record_path": str(record_path),
        "schema_path": str(schema_path),
        "overall_status": "UNKNOWN",
        "checks": [],
        "warnings": [],
        "errors": [],
        "indeterminate_signals": [],
        "environment": {
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
    }

    if not record_path.is_file():
        add_check(result, "RECORD_FILE_PRESENT", "FAIL", f"Record file not found: {record_path}")
        finalize_status(result)
    else:
        result["record_sha256"] = sha256_file(record_path)
        result["record_size_bytes"] = record_path.stat().st_size
        add_check(result, "RECORD_FILE_PRESENT", "PASS", {"sha256": result["record_sha256"], "size_bytes": result["record_size_bytes"]})

    if schema_path.is_file():
        result["schema_sha256"] = sha256_file(schema_path)
        result["schema_size_bytes"] = schema_path.stat().st_size
        add_check(result, "SCHEMA_FILE_PRESENT", "PASS", {"sha256": result["schema_sha256"], "size_bytes": result["schema_size_bytes"]})
    else:
        add_check(result, "SCHEMA_FILE_PRESENT", "WARN", f"Schema file not found: {schema_path}. Continuing with built-in v0.1 checks.")

    record: dict[str, Any] | None = None
    if record_path.is_file():
        try:
            loaded = json.loads(record_path.read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                add_check(result, "JSON_PARSE", "FAIL", "Top-level JSON value must be an object.")
            else:
                record = loaded
                add_check(result, "JSON_PARSE", "PASS", "Record parsed as JSON object.")
        except Exception as exc:
            add_check(result, "JSON_PARSE", "FAIL", str(exc))

    if record is not None:
        check_schema_version(record, result)
        check_required_fields(record, result)
        check_non_claims(record, result)
        check_claim_nonclaim_disjoint(record, result)
        check_unknowns_dependencies(record, result)
        check_authority_boundary(record, result)
        check_safe_handoffs(record, result)
        check_fork_required_non_claims(record, result)

    finalize_status(result)

    output_text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
        print(f"result_path={output_path}")

    print(f"AI_GOVERNANCE_MAPPING_RECORD_CHECK_{result['overall_status']}")

    if result["overall_status"] == "PASS":
        return 0
    if result["overall_status"] == "INDETERMINATE":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())