#!/usr/bin/env python3
"""
Fork Definition Boundary Checker v0.1

Purpose:
  Enforce Definition Boundary v0.1 for IDENTITY_UNDEFINED.

Rules:
  - Validate payloads against definition_boundary_v0_1.schema.json.
  - Under IDENTITY_UNDEFINED, reject identity-expanding phrases in:
      * definition_statement
      * allowed_definitions
  - Do not scan forbidden_definitions.
  - Emit DEFINITION_EXPANSION_DEFECT when definition expansion occurs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFINITION_EXPANSION_FAILURE = "DEFINITION_EXPANSION_DEFECT"
SUPPORTED_BOUNDARY_TYPE = "IDENTITY_UNDEFINED"

IDENTITY_EXPANSION_PHRASES = [
    "natural person",
    "human approved",
    "person approved",
    "identity verified",
    "verified identity",
    "authorized reviewer",
    "reviewer was authorized",
    "meaningful review",
    "meaningful human review",
    "employee approved",
    "legal identity",
    "actual human",
    "ryan approved",
]


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:  # noqa: BLE001
        raise ValueError(f"JSON_LOAD_ERROR {path} {exc}") from exc


def validate_against_schema(payload: Any, schema_path: Path) -> list[str]:
    try:
        import jsonschema  # type: ignore[import]
    except Exception:
        return validate_minimal_schema(payload)

    try:
        schema = load_json(schema_path)
    except ValueError as exc:
        return [str(exc)]

    try:
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)
        validator = validator_cls(schema)
        errors: list[str] = []

        for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
            location = ".".join(str(part) for part in error.path)
            if location:
                errors.append(f"SCHEMA_ERROR {location} {error.message}")
            else:
                errors.append(f"SCHEMA_ERROR {error.message}")

        return errors
    except Exception as exc:  # noqa: BLE001
        return [f"SCHEMA_ERROR {exc}"]


def validate_minimal_schema(payload: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(payload, dict):
        return ["SCHEMA_ERROR payload must be a JSON object"]

    required = {
        "boundary_type",
        "definition_statement",
        "allowed_definitions",
        "forbidden_definitions",
    }

    missing = sorted(required - set(payload.keys()))
    if missing:
        errors.append(f"SCHEMA_ERROR missing required fields: {', '.join(missing)}")

    allowed_keys = required
    unexpected = sorted(set(payload.keys()) - allowed_keys)
    if unexpected:
        errors.append(f"SCHEMA_ERROR additional properties: {', '.join(unexpected)}")

    if payload.get("boundary_type") != SUPPORTED_BOUNDARY_TYPE:
        errors.append(
            f"SCHEMA_ERROR boundary_type must be {SUPPORTED_BOUNDARY_TYPE}"
        )

    if not isinstance(payload.get("definition_statement"), str):
        errors.append("SCHEMA_ERROR definition_statement must be a string")

    for field in ("allowed_definitions", "forbidden_definitions"):
        value = payload.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"SCHEMA_ERROR {field} must be a non-empty array")
        elif not all(isinstance(item, str) and item for item in value):
            errors.append(f"SCHEMA_ERROR {field} items must be non-empty strings")

    return errors


def scan_for_identity_overdefinition(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    boundary_type = payload.get("boundary_type")
    if boundary_type != SUPPORTED_BOUNDARY_TYPE:
        errors.append(
            f"BOUNDARY_TYPE_UNSUPPORTED expected {SUPPORTED_BOUNDARY_TYPE!r}, "
            f"got {boundary_type!r}"
        )
        return errors

    definition_statement = payload.get("definition_statement", "")
    if isinstance(definition_statement, str):
        lower_text = definition_statement.lower()
        for phrase in IDENTITY_EXPANSION_PHRASES:
            if phrase in lower_text:
                errors.append(
                    f"{DEFINITION_EXPANSION_FAILURE} definition_statement {phrase!r}"
                )

    allowed_definitions = payload.get("allowed_definitions", [])
    if isinstance(allowed_definitions, list):
        for idx, item in enumerate(allowed_definitions):
            if not isinstance(item, str):
                continue

            lower_item = item.lower()
            for phrase in IDENTITY_EXPANSION_PHRASES:
                if phrase in lower_item:
                    errors.append(
                        f"{DEFINITION_EXPANSION_FAILURE} "
                        f"allowed_definitions[{idx}] {phrase!r}"
                    )

    # forbidden_definitions is intentionally NOT scanned in v0.1.

    return errors


def validate_definition_boundary(path: Path, schema_path: Path) -> list[str]:
    try:
        payload = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    errors = validate_against_schema(payload, schema_path)
    if errors:
        return errors

    if not isinstance(payload, dict):
        return ["SCHEMA_ERROR payload must be a JSON object"]

    errors.extend(scan_for_identity_overdefinition(payload))
    return errors


def run(paths: list[Path], schema_path: Path) -> int:
    any_failed = False

    for path in paths:
        errors = validate_definition_boundary(path, schema_path)
        if errors:
            any_failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"DEFINITION_BOUNDARY_PASS {path}")

    return 1 if any_failed else 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Check Fork Definition Boundaries v0.1."
    )
    parser.add_argument(
        "boundaries",
        nargs="+",
        help="Paths to Definition Boundary JSON payloads.",
    )
    parser.add_argument(
        "--schema",
        default=str(repo_root / "schemas" / "definition_boundary_v0_1.schema.json"),
        help="Path to definition boundary schema JSON.",
    )

    args = parser.parse_args()

    boundary_paths = [Path(p).resolve() for p in args.boundaries]
    schema_path = Path(args.schema).resolve()

    return run(boundary_paths, schema_path)


if __name__ == "__main__":
    raise SystemExit(main())
