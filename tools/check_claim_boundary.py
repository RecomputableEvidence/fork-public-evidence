#!/usr/bin/env python3
"""
Fork Claim Boundary Checker v0.1

Purpose:
    Validate a claim boundary payload and reject overclaiming under the
    OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY claim type.

Design:
    - Uses jsonschema if available.
    - Falls back to built-in schema-shape checks if jsonschema is not installed.
    - Enforces v0.1 claim-expansion term rules without external dependencies.

Exit codes:
    0 = claim boundary passed
    1 = claim boundary failed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SUPPORTED_CLAIM_TYPES = {
    "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY"
}

REQUIRED_FIELDS = [
    "claim_type",
    "claim_statement",
    "allowed_inferences",
    "forbidden_inferences",
    "not_checked",
    "non_claims",
]

ARRAY_FIELDS = [
    "allowed_inferences",
    "forbidden_inferences",
    "not_checked",
    "non_claims",
]

FORBIDDEN_TERM_PATTERNS = [
    ("compliant", r"\bcompliant\b"),
    ("compliance", r"\bcompliance\b"),
    ("lawful", r"\blawful\b"),
    ("admissible", r"\badmissible\b"),
    ("correct", r"\bcorrect\b"),
    ("complete", r"\bcomplete\b"),
    ("authorized", r"\bauthorized\b"),
    ("unbiased", r"\bunbiased\b"),
    ("fair", r"\bfair\b"),
    ("validated", r"\bvalidated\b"),
    ("enterprise-proven", r"\benterprise[-\s]proven\b"),
    ("source of truth", r"\bsource\s+of\s+truth\b"),
]


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError(f"JSON_LOAD_ERROR: {path}: {exc}") from exc


def fallback_schema_shape_validation(payload: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(payload, dict):
        return ["SCHEMA_ERROR: payload must be a JSON object"]

    payload_keys = set(payload.keys())
    required_keys = set(REQUIRED_FIELDS)

    missing = sorted(required_keys - payload_keys)
    if missing:
        errors.append(f"SCHEMA_ERROR: missing required fields: {', '.join(missing)}")

    extra = sorted(payload_keys - required_keys)
    if extra:
        errors.append(f"SCHEMA_ERROR: additional properties are not allowed: {', '.join(extra)}")

    claim_type = payload.get("claim_type")
    if claim_type not in SUPPORTED_CLAIM_TYPES:
        errors.append(f"SCHEMA_ERROR: unsupported claim_type: {claim_type!r}")

    claim_statement = payload.get("claim_statement")
    if not isinstance(claim_statement, str) or not claim_statement.strip():
        errors.append("SCHEMA_ERROR: claim_statement must be a non-empty string")

    for field in ARRAY_FIELDS:
        value = payload.get(field)
        if not isinstance(value, list):
            errors.append(f"SCHEMA_ERROR: {field} must be an array")
            continue

        if len(value) == 0:
            errors.append(f"SCHEMA_ERROR: {field} must be non-empty in v0.1")

        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"SCHEMA_ERROR: {field}[{index}] must be a non-empty string")

    return errors


def validate_against_schema(payload: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)

    try:
        import jsonschema  # type: ignore
    except Exception:
        return fallback_schema_shape_validation(payload)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    errors = []
    for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path)
        if location:
            errors.append(f"SCHEMA_ERROR: {location}: {error.message}")
        else:
            errors.append(f"SCHEMA_ERROR: {error.message}")

    return errors


def scan_for_overclaims(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    claim_type = payload.get("claim_type")
    if claim_type != "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY":
        return [f"CLAIM_TYPE_ERROR: unsupported claim_type for v0.1 enforcement: {claim_type!r}"]

    scan_targets: list[tuple[str, str]] = []

    statement = payload.get("claim_statement")
    if isinstance(statement, str):
        scan_targets.append(("claim_statement", statement))

    allowed_inferences = payload.get("allowed_inferences")
    if isinstance(allowed_inferences, list):
        for index, item in enumerate(allowed_inferences):
            if isinstance(item, str):
                scan_targets.append((f"allowed_inferences[{index}]", item))

    for location, text in scan_targets:
        for term, pattern in FORBIDDEN_TERM_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(
                    f"CLAIM_EXPANSION_DEFECT: {location} contains claim-expanding term {term!r}"
                )

    return errors


def run(payload_path: Path, schema_path: Path) -> int:
    errors: list[str] = []

    try:
        payload = load_json(payload_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        errors.extend(validate_against_schema(payload, schema_path))
    except Exception as exc:
        errors.append(f"SCHEMA_VALIDATION_ERROR: {exc}")

    if not errors and isinstance(payload, dict):
        errors.extend(scan_for_overclaims(payload))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"CLAIM_BOUNDARY_PASS: {payload_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Fork Claim Boundary payload v0.1")
    parser.add_argument("payload", help="Path to claim boundary JSON payload")
    parser.add_argument(
        "--schema",
        default=str(Path(__file__).resolve().parents[1] / "schemas" / "claim_boundary_v0_1.schema.json"),
        help="Path to claim boundary JSON Schema",
    )

    args = parser.parse_args()

    payload_path = Path(args.payload).resolve()
    schema_path = Path(args.schema).resolve()

    return run(payload_path, schema_path)


if __name__ == "__main__":
    raise SystemExit(main())