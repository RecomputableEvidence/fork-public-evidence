#!/usr/bin/env python3
"""
AI Governance System Mapping Record checker v0.2.2.

v0.2.2 is a final stabilization patch on top of v0.2.1. It adds:
- static machine-readable error codes for FAIL checks,
- local multi-hop safe-handoff cycle detection inside a single record,
- stronger parser-boundary handling while relying on Python's JSON parser,
- Unicode-aware lexical normalization preservation,
- output-comparison guidance support through deterministic normalized output,
- preservation of v0.2.1 precision hardening and all prior non-claim boundaries.

This checker remains bounded. It does not prove legal admissibility, compliance
satisfaction, audit sufficiency, AI output correctness, decision correctness,
source completeness, institutional authority, runtime control, policy authority,
cross-record graph validity, external artifact existence, or semantic intent.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "ai_governance_system_mapping_record.v0.2.2"

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
    "declared_unknown_classes": list,
    "active_unresolved_unknowns": list,
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

RESTRICTED_CLAIM_PATTERNS: dict[str, list[str]] = {
    "AI output correctness": [
        "ai output correctness",
        "model output correctness",
        "output is correct",
        "ai result is correct",
        "validated ai output",
        "verified ai answer",
        "accurate ai output",
    ],
    "decision correctness": [
        "decision correctness",
        "validated the decision",
        "approved the outcome",
        "decision is correct",
        "outcome is approved",
        "correct decision",
        "decision validated",
        "approved decision",
    ],
    "source completeness": [
        "source completeness",
        "complete source record",
        "complete record",
        "all source events",
        "all relevant source events",
        "complete evidence source",
    ],
    "legal admissibility": [
        "legal admissibility",
        "ready for legal reliance",
        "legally sufficient",
        "legally ready",
        "legal ready",
        "legal approved",
        "legal approval",
        "admissible",
        "admissibility",
        "legal sufficiency",
        "court ready",
    ],
    "compliance satisfaction": [
        "compliance satisfaction",
        "sufficient for compliance",
        "compliance sufficient",
        "compliance satisfied",
        "compliant",
        "compliance complete",
        "compliance ready",
        "regulator ready",
        "regulatory ready",
        "certifies compliance",
        "certified compliant",
        "compliance certified",
    ],
    "audit sufficiency": [
        "audit sufficiency",
        "audit ready",
        "sufficient for audit",
        "audit complete",
        "audit sufficient",
        "audit approved",
    ],
    "institutional authority": [
        "institutional authority",
        "institutionally accepted",
        "institutional acceptance",
        "approved by institution",
        "institution approved",
        "system authorized",
    ],
    "runtime control": [
        "runtime control",
        "controls execution",
        "runtime enforcement",
        "enforces execution",
        "halts execution",
        "blocks execution",
    ],
    "execution permissioning": [
        "execution permissioning",
        "authorizes execution",
        "execution approved",
        "permissioned execution",
        "permits execution",
    ],
    "policy authority": [
        "policy authority",
        "sets policy",
        "approves policy",
        "policy decision",
        "policy approved",
        "policy compliant",
    ],
    "risk acceptance": [
        "risk acceptance",
        "accepts risk",
        "risk accepted",
        "risk approved",
    ],
}

ID_BEARING_ARRAY_FIELDS = [
    "input_assumptions",
    "supported_claims",
    "explicit_non_claims",
    "emitted_artifacts",
    "consumable_artifacts",
    "dependency_boundary",
    "declared_unknown_classes",
    "active_unresolved_unknowns",
    "failure_states",
    "safe_handoffs",
    "prohibited_claim_inheritance",
    "re_verification_requirements",
    "institutional_dependencies",
]

SAFE_HANDOFF_REFERENCE_FIELDS = [
    "allowed_claim_ids",
    "claims_that_must_not_transfer_ids",
    "non_claim_ids_that_must_travel",
    "unknown_ids_that_must_travel",
    "re_verification_requirement_ids",
]

HANDOFF_DEPENDENCY_FIELD = "handoff_dependency_ids"

ERROR_CODE_BY_CHECK_ID: dict[str, str] = {
    "RECORD_FILE_PRESENT": "ERR_RECORD_FILE_MISSING",
    "SCHEMA_FILE_PRESENT": "ERR_SCHEMA_FILE_MISSING",
    "JSON_PARSE": "ERR_JSON_PARSE",
    "SCHEMA_VERSION_PIN": "ERR_SCHEMA_VERSION_MISMATCH",
    "SCHEMA_EQUIVALENT_VALIDATION": "ERR_SCHEMA_EQUIVALENT_VALIDATION",
    "REQUIRED_FIELDS_PRESENT": "ERR_REQUIRED_FIELDS",
    "FIELD_TYPES": "ERR_FIELD_TYPES",
    "UNIQUE_BOUNDARY_ITEM_IDS": "ERR_DUPLICATE_OR_MISSING_ID",
    "EXPLICIT_NON_CLAIMS_PRESENT": "ERR_EXPLICIT_NON_CLAIMS_MISSING",
    "PROHIBITED_CLAIM_INHERITANCE_PRESENT": "ERR_PROHIBITED_CLAIM_INHERITANCE_MISSING",
    "CLAIM_NONCLAIM_DISJOINT": "ERR_CLAIM_NONCLAIM_OVERLAP",
    "DECLARED_UNKNOWN_CLASSES_PRESENT": "ERR_DECLARED_UNKNOWN_CLASSES_MISSING",
    "DECLARED_UNKNOWN_CLASSES_ONLY_DECLARED": "ERR_DECLARED_UNKNOWN_CLASS_STATUS",
    "AUTHORITY_BOUNDARY_PRESENT": "ERR_AUTHORITY_BOUNDARY_MISSING",
    "AUTHORITY_NON_AUTHORITIES_PRESENT": "ERR_AUTHORITY_NON_AUTHORITIES_MISSING",
    "RESTRICTED_AUTHORITY_CLAIM_GUARD": "ERR_RESTRICTED_AUTHORITY_CLAIM",
    "SAFE_HANDOFF_SELF_REFERENCE_GUARD": "ERR_SAFE_HANDOFF_SELF_REFERENCE",
    "LOCAL_HANDOFF_CYCLE_GUARD": "ERR_LOCAL_HANDOFF_CYCLE",
    "SAFE_HANDOFFS_PRESENT": "ERR_SAFE_HANDOFFS_MISSING",
    "SAFE_HANDOFF_ID_REFERENCE_INTEGRITY": "ERR_SAFE_HANDOFF_ID_REFERENCE",
    "FORK_REQUIRED_NON_CLAIMS": "ERR_FORK_REQUIRED_NON_CLAIMS_MISSING",
}



def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(value: Any) -> str:
    text = str(value)
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) not in {"Cf"})
    text = "".join(ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch))
    text = text.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"[_/\\-]+", " ", text)
    text = re.sub(r"[^0-9A-Za-z]+", " ", text)
    return " ".join(text.lower().split())


def item_statement(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("statement", ""))
    return str(item)


def item_id(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("id", ""))
    return ""


def statements(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    return [item_statement(item) for item in items]


def ids(items: Any) -> set[str]:
    if not isinstance(items, list):
        return set()
    return {item_id(item) for item in items if item_id(item)}


def contains_term(texts: list[str], term: str) -> bool:
    t = normalize_text(term)
    return any(t in normalize_text(text) for text in texts)


def error_code_for(check_id: str) -> str:
    return ERROR_CODE_BY_CHECK_ID.get(check_id, f"ERR_{check_id}")


def add_check(
    result: dict[str, Any],
    check_id: str,
    status: str,
    detail: Any = None,
) -> None:
    entry = {
        "check_id": check_id,
        "status": status,
        "detail": detail,
    }
    if status == "FAIL":
        entry["error_code"] = error_code_for(check_id)
    result["checks"].append(entry)
    if status == "FAIL":
        result["errors"].append({"check_id": check_id, "error_code": error_code_for(check_id), "detail": detail})
    elif status == "WARN":
        result["warnings"].append({"check_id": check_id, "detail": detail})
    elif status == "INDETERMINATE":
        result["indeterminate_signals"].append({"check_id": check_id, "detail": detail})


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def schema_type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    return type(value).__name__


def resolve_ref(ref: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"Only local JSON Schema refs are supported: {ref}")
    node: Any = root_schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"Unresolvable JSON Schema ref: {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"JSON Schema ref did not resolve to an object: {ref}")
    return node


def validate_schema_subset(
    instance: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    path: str = "$",
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []

    if "$ref" in schema:
        try:
            return validate_schema_subset(instance, resolve_ref(str(schema["$ref"]), root_schema), root_schema, path)
        except Exception as exc:
            return [{"path": path, "error": str(exc)}]

    expected_type = schema.get("type")
    if expected_type is not None:
        actual_type = schema_type_name(instance)
        if actual_type != expected_type:
            errors.append(
                {
                    "path": path,
                    "error": "type_mismatch",
                    "expected": expected_type,
                    "actual": actual_type,
                }
            )
            return errors

    if "const" in schema and instance != schema["const"]:
        errors.append({"path": path, "error": "const_mismatch", "expected": schema["const"], "actual": instance})

    if "enum" in schema and instance not in schema["enum"]:
        errors.append({"path": path, "error": "enum_mismatch", "allowed": schema["enum"], "actual": instance})

    if isinstance(instance, str):
        min_length = schema.get("minLength")
        if isinstance(min_length, int) and len(instance) < min_length:
            errors.append({"path": path, "error": "minLength", "minLength": min_length, "actual": len(instance)})

    if isinstance(instance, list):
        min_items = schema.get("minItems")
        if isinstance(min_items, int) and len(instance) < min_items:
            errors.append({"path": path, "error": "minItems", "minItems": min_items, "actual": len(instance)})
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(instance):
                errors.extend(validate_schema_subset(item, item_schema, root_schema, f"{path}[{idx}]"))

    if isinstance(instance, dict):
        required = schema.get("required", [])
        if isinstance(required, list):
            for field in required:
                if field not in instance:
                    errors.append({"path": path, "error": "required", "missing": field})

        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for field, subschema in properties.items():
                if field in instance and isinstance(subschema, dict):
                    errors.extend(validate_schema_subset(instance[field], subschema, root_schema, f"{path}.{field}"))

        if schema.get("additionalProperties") is False and isinstance(properties, dict):
            allowed = set(properties.keys())
            for field in instance:
                if field not in allowed:
                    errors.append({"path": f"{path}.{field}", "error": "additionalProperties", "field": field})

    return errors


def check_schema_equivalent_validation(
    record: dict[str, Any],
    schema_path: Path,
    result: dict[str, Any],
) -> None:
    if not schema_path.is_file():
        add_check(result, "SCHEMA_EQUIVALENT_VALIDATION", "FAIL", "Schema file is required for v0.2.2 schema-equivalent validation.")
        return

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict):
            add_check(result, "SCHEMA_EQUIVALENT_VALIDATION", "FAIL", "Schema root must be an object.")
            return
        errors = validate_schema_subset(record, schema, schema)
    except Exception as exc:
        add_check(result, "SCHEMA_EQUIVALENT_VALIDATION", "FAIL", str(exc))
        return

    if errors:
        add_check(result, "SCHEMA_EQUIVALENT_VALIDATION", "FAIL", errors)
    else:
        add_check(result, "SCHEMA_EQUIVALENT_VALIDATION", "PASS", "Record satisfies the supported strict JSON Schema subset.")


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


def check_unique_boundary_item_ids(record: dict[str, Any], result: dict[str, Any]) -> None:
    occurrences: dict[str, list[dict[str, Any]]] = {}
    missing_or_empty: list[dict[str, Any]] = []

    for field in ID_BEARING_ARRAY_FIELDS:
        items = record.get(field, [])
        if not isinstance(items, list):
            continue
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            value = str(item.get("id", ""))
            if not value:
                missing_or_empty.append({"field": field, "index": index})
                continue
            occurrences.setdefault(value, []).append({"field": field, "index": index})

    duplicates = [
        {"id": value, "occurrences": locations}
        for value, locations in sorted(occurrences.items())
        if len(locations) > 1
    ]

    if missing_or_empty:
        add_check(result, "UNIQUE_BOUNDARY_ITEM_IDS", "FAIL", {"missing_or_empty_ids": missing_or_empty})
    elif duplicates:
        add_check(result, "UNIQUE_BOUNDARY_ITEM_IDS", "FAIL", {"duplicate_ids": duplicates})
    else:
        add_check(result, "UNIQUE_BOUNDARY_ITEM_IDS", "PASS", "All declared boundary item IDs are globally unique within the record.")


def check_safe_handoff_self_references(record: dict[str, Any], result: dict[str, Any]) -> None:
    handoffs = record.get("safe_handoffs", [])
    failures: list[dict[str, Any]] = []

    if not isinstance(handoffs, list):
        add_check(result, "SAFE_HANDOFF_SELF_REFERENCE_GUARD", "FAIL", "safe_handoffs must be an array.")
        return

    for index, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            continue
        handoff_id = str(handoff.get("id", ""))
        if not handoff_id:
            continue
        for field in SAFE_HANDOFF_REFERENCE_FIELDS:
            values = handoff.get(field, [])
            if isinstance(values, list) and handoff_id in [str(value) for value in values]:
                failures.append({"handoff": handoff_id, "field": field, "self_reference": handoff_id})

    if failures:
        add_check(result, "SAFE_HANDOFF_SELF_REFERENCE_GUARD", "FAIL", failures)
    else:
        add_check(result, "SAFE_HANDOFF_SELF_REFERENCE_GUARD", "PASS", "No safe handoff references itself through its boundary-reference fields.")



def check_local_handoff_cycles(record: dict[str, Any], result: dict[str, Any]) -> None:
    handoffs = record.get("safe_handoffs", [])
    if not isinstance(handoffs, list):
        add_check(result, "LOCAL_HANDOFF_CYCLE_GUARD", "FAIL", "safe_handoffs must be an array.")
        return

    handoff_ids = {str(h.get("id", "")) for h in handoffs if isinstance(h, dict) and str(h.get("id", ""))}
    graph: dict[str, list[str]] = {handoff_id: [] for handoff_id in handoff_ids}
    failures: list[dict[str, Any]] = []

    for index, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            continue
        handoff_id = str(handoff.get("id", ""))
        if not handoff_id:
            continue
        deps = handoff.get(HANDOFF_DEPENDENCY_FIELD, [])
        if deps is None:
            deps = []
        if not isinstance(deps, list):
            failures.append({"handoff": handoff_id, "field": HANDOFF_DEPENDENCY_FIELD, "error": "must be an array"})
            continue
        for dep in [str(value) for value in deps]:
            if dep not in handoff_ids:
                failures.append({"handoff": handoff_id, "field": HANDOFF_DEPENDENCY_FIELD, "unknown_dependency": dep, "known_handoffs": sorted(handoff_ids)})
            else:
                graph.setdefault(handoff_id, []).append(dep)

    visited: set[str] = set()
    stack: list[str] = []
    stack_set: set[str] = set()
    cycles: list[list[str]] = []

    def dfs(node: str) -> None:
        visited.add(node)
        stack.append(node)
        stack_set.add(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                dfs(nxt)
            elif nxt in stack_set:
                start = stack.index(nxt)
                cycle = stack[start:] + [nxt]
                if cycle not in cycles:
                    cycles.append(cycle)
        stack.pop()
        stack_set.remove(node)

    for node in sorted(graph):
        if node not in visited:
            dfs(node)

    if cycles:
        failures.append({"error": "local safe-handoff dependency cycle detected", "cycles": cycles})

    if failures:
        add_check(result, "LOCAL_HANDOFF_CYCLE_GUARD", "FAIL", failures)
    else:
        add_check(result, "LOCAL_HANDOFF_CYCLE_GUARD", "PASS", "No local multi-hop safe-handoff dependency cycles detected within this record.")


def check_unknowns_dependencies(record: dict[str, Any], result: dict[str, Any]) -> None:
    declared_unknowns = record.get("declared_unknown_classes")
    if nonempty_list(declared_unknowns):
        add_check(result, "DECLARED_UNKNOWN_CLASSES_PRESENT", "PASS", len(declared_unknowns))
    else:
        add_check(result, "DECLARED_UNKNOWN_CLASSES_PRESENT", "FAIL", "declared_unknown_classes must be a non-empty array.")

    bad_declared_statuses: list[dict[str, Any]] = []
    for item in declared_unknowns if isinstance(declared_unknowns, list) else []:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status", "")).upper()
        if status != "DECLARED":
            bad_declared_statuses.append({"id": item.get("id"), "status": status})

    if bad_declared_statuses:
        add_check(result, "DECLARED_UNKNOWN_CLASSES_ONLY_DECLARED", "FAIL", bad_declared_statuses)
    else:
        add_check(result, "DECLARED_UNKNOWN_CLASSES_ONLY_DECLARED", "PASS", "Declared unknown classes use DECLARED status only.")

    indeterminate_items: list[dict[str, Any]] = []

    for field in ["dependency_boundary", "active_unresolved_unknowns", "institutional_dependencies"]:
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
        add_check(result, "INDETERMINATE_SIGNALS", "PASS", "No active unresolved dependency, unknown, or review-required signals detected.")


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
    authority_text = normalize_text(" ".join(authority_claims) + " " + authority_basis)

    restricted_hits: list[dict[str, str]] = []

    for claim in supported:
        normalized_claim = normalize_text(claim)
        for category, patterns in RESTRICTED_CLAIM_PATTERNS.items():
            for pattern in patterns:
                normalized_pattern = normalize_text(pattern)
                if normalized_pattern in normalized_claim and normalized_pattern not in authority_text:
                    restricted_hits.append(
                        {
                            "claim": claim,
                            "restricted_category": category,
                            "matched_pattern": pattern,
                        }
                    )

    if restricted_hits:
        add_check(
            result,
            "RESTRICTED_AUTHORITY_CLAIM_GUARD",
            "FAIL",
            {
                "message": "Supported claims include restricted authority/correctness/compliance language without declared authority basis.",
                "hits": restricted_hits,
            },
        )
    else:
        add_check(result, "RESTRICTED_AUTHORITY_CLAIM_GUARD", "PASS", "No unsupported restricted authority claims detected.")


def check_safe_handoff_id_references(record: dict[str, Any], result: dict[str, Any]) -> None:
    handoffs = record.get("safe_handoffs", [])
    if not nonempty_list(handoffs):
        add_check(result, "SAFE_HANDOFFS_PRESENT", "FAIL", "safe_handoffs must be a non-empty array.")
        return

    add_check(result, "SAFE_HANDOFFS_PRESENT", "PASS", len(handoffs))

    pools = {
        "allowed_claim_ids": ids(record.get("supported_claims", [])),
        "claims_that_must_not_transfer_ids": ids(record.get("prohibited_claim_inheritance", [])),
        "non_claim_ids_that_must_travel": ids(record.get("explicit_non_claims", [])),
        "unknown_ids_that_must_travel": ids(record.get("declared_unknown_classes", [])) | ids(record.get("active_unresolved_unknowns", [])),
        "re_verification_requirement_ids": ids(record.get("re_verification_requirements", [])),
    }

    failures: list[dict[str, Any]] = []
    required_arrays = SAFE_HANDOFF_REFERENCE_FIELDS

    for idx, handoff in enumerate(handoffs):
        if not isinstance(handoff, dict):
            failures.append({"index": idx, "error": "handoff entry must be an object"})
            continue

        handoff_id = handoff.get("id", f"index_{idx}")
        for field in required_arrays:
            values = handoff.get(field)
            if field != "allowed_claim_ids" and not nonempty_list(values):
                failures.append(
                    {
                        "handoff": handoff_id,
                        "field": field,
                        "error": "must be a non-empty array",
                    }
                )
                continue
            if not isinstance(values, list):
                failures.append(
                    {
                        "handoff": handoff_id,
                        "field": field,
                        "error": "must be an array",
                    }
                )
                continue
            unknown_refs = [value for value in values if value not in pools[field]]
            if unknown_refs:
                failures.append(
                    {
                        "handoff": handoff_id,
                        "field": field,
                        "unknown_refs": unknown_refs,
                        "allowed_refs": sorted(pools[field]),
                    }
                )

    if failures:
        add_check(result, "SAFE_HANDOFF_ID_REFERENCE_INTEGRITY", "FAIL", failures)
    else:
        add_check(
            result,
            "SAFE_HANDOFF_ID_REFERENCE_INTEGRITY",
            "PASS",
            "All safe handoff ID references resolve to upstream boundary items.",
        )


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


def make_normalized_result(result: dict[str, Any]) -> dict[str, Any]:
    normalized = {
        "checker_name": result["checker_name"],
        "checker_version": result["checker_version"],
        "overall_status": result["overall_status"],
        "record_sha256": result.get("record_sha256"),
        "schema_sha256": result.get("schema_sha256"),
        "checks": result["checks"],
        "warnings": result["warnings"],
        "errors": result["errors"],
        "indeterminate_signals": result["indeterminate_signals"],
    }
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Check AI Governance System Mapping Record v0.2.2.")
    parser.add_argument("--record", required=True, help="Path to mapping record JSON.")
    parser.add_argument("--schema", default="schemas/ai_governance_system_mapping_record_v0_2_2.schema.json")
    parser.add_argument("--output", default=None, help="Optional JSON result output path.")
    parser.add_argument("--normalized-output", default=None, help="Optional normalized JSON output path without env/path/timestamp fields.")
    args = parser.parse_args()

    record_path = Path(args.record).resolve()
    schema_path = Path(args.schema).resolve()

    result: dict[str, Any] = {
        "checker_name": "check_ai_governance_mapping_record_v0_2_2",
        "checker_version": "v0.2.2",
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
        add_check(result, "SCHEMA_FILE_PRESENT", "FAIL", f"Schema file not found: {schema_path}. v0.2.2 requires schema-equivalent validation.")

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
        check_schema_equivalent_validation(record, schema_path, result)
        check_required_fields(record, result)
        check_unique_boundary_item_ids(record, result)
        check_non_claims(record, result)
        check_claim_nonclaim_disjoint(record, result)
        check_unknowns_dependencies(record, result)
        check_authority_boundary(record, result)
        check_safe_handoff_self_references(record, result)
        check_local_handoff_cycles(record, result)
        check_safe_handoff_id_references(record, result)
        check_fork_required_non_claims(record, result)

    finalize_status(result)

    output_text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
        print(f"result_path={output_path}")

    if args.normalized_output:
        normalized_path = Path(args.normalized_output).resolve()
        normalized_path.parent.mkdir(parents=True, exist_ok=True)
        normalized_path.write_text(json.dumps(make_normalized_result(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"normalized_result_path={normalized_path}")

    print(f"AI_GOVERNANCE_MAPPING_RECORD_V0_2_2_CHECK_{result['overall_status']}")

    if result["overall_status"] == "PASS":
        return 0
    if result["overall_status"] == "INDETERMINATE":
        return 2
    return 1


if __name__ == "__main__":
    sys.exit(main())