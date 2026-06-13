#!/usr/bin/env python3
"""
Fork Provenance Tier Checker v0.1

Purpose:
  Enforce Provenance Tier v0.1.

Implemented rules:
  - GENERATED cannot satisfy DOCUMENTED.
  - DOCUMENTED must not depend on GENERATED content.

Implemented failure codes:
  - PROVENANCE_ESCALATION_DEFECT
  - PROVENANCE_DEPENDENCY_CONTAMINATION

Reserved failure codes:
  - PROVENANCE_UNRESOLVED_REASON_MISSING
  - PROVENANCE_ATTRIBUTION_INCOMPLETE
  - PROVENANCE_SILENT_UPGRADE_DEFECT
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROVENANCE_ESCALATION_DEFECT = "PROVENANCE_ESCALATION_DEFECT"
PROVENANCE_DEPENDENCY_CONTAMINATION = "PROVENANCE_DEPENDENCY_CONTAMINATION"

SUPPORTED_TIERS = {
    "DOCUMENTED",
    "ATTRIBUTED",
    "INTERPRETIVE",
    "GENERATED",
    "UNRESOLVED",
}

SUPPORTED_TRANSFORMATIONS = {
    "NONE",
    "FORMAT_NORMALIZATION",
    "CANONICALIZATION",
    "CRYPTOGRAPHIC_VERIFICATION",
    "SUMMARIZATION",
    "CLASSIFICATION",
    "MODEL_EXTRACTION",
    "SEMANTIC_INFERENCE",
    "HUMAN_INTERPRETATION",
}


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
        "artifact_id",
        "declared_provenance_tier",
        "required_provenance_tier",
        "dependency_provenance_tiers",
        "transformation_type",
        "re_elevation_claimed",
        "unresolved_reason_code",
        "attribution",
    }

    missing = sorted(required - set(payload.keys()))
    if missing:
        errors.append(f"SCHEMA_ERROR missing required fields: {', '.join(missing)}")

    unexpected = sorted(set(payload.keys()) - required)
    if unexpected:
        errors.append(f"SCHEMA_ERROR additional properties: {', '.join(unexpected)}")

    if not isinstance(payload.get("artifact_id"), str) or not payload.get("artifact_id"):
        errors.append("SCHEMA_ERROR artifact_id must be a non-empty string")

    declared = payload.get("declared_provenance_tier")
    required_tier = payload.get("required_provenance_tier")
    transformation = payload.get("transformation_type")

    if declared not in SUPPORTED_TIERS:
        errors.append("SCHEMA_ERROR declared_provenance_tier is unsupported")

    if required_tier not in SUPPORTED_TIERS:
        errors.append("SCHEMA_ERROR required_provenance_tier is unsupported")

    deps = payload.get("dependency_provenance_tiers")
    if not isinstance(deps, list):
        errors.append("SCHEMA_ERROR dependency_provenance_tiers must be an array")
    elif not all(item in SUPPORTED_TIERS for item in deps):
        errors.append("SCHEMA_ERROR dependency_provenance_tiers contains unsupported tier")

    if transformation not in SUPPORTED_TRANSFORMATIONS:
        errors.append("SCHEMA_ERROR transformation_type is unsupported")

    if not isinstance(payload.get("re_elevation_claimed"), bool):
        errors.append("SCHEMA_ERROR re_elevation_claimed must be boolean")

    unresolved = payload.get("unresolved_reason_code")
    allowed_unresolved = {
        None,
        "UNRESOLVED_MISSING_SOURCE",
        "UNRESOLVED_AMBIGUOUS_IDENTITY",
        "UNRESOLVED_NON_RECOMPUTABLE",
        "UNRESOLVED_CONFLICTING_EVIDENCE",
        "UNRESOLVED_UNSUPPORTED_TIER",
    }
    if unresolved not in allowed_unresolved:
        errors.append("SCHEMA_ERROR unresolved_reason_code is unsupported")

    attribution = payload.get("attribution")
    if attribution is not None:
        if not isinstance(attribution, dict):
            errors.append("SCHEMA_ERROR attribution must be null or object")
        else:
            attribution_required = {
                "source_identity",
                "source_reference",
                "source_timestamp_or_version",
            }
            missing_attr = sorted(attribution_required - set(attribution.keys()))
            if missing_attr:
                errors.append(
                    "SCHEMA_ERROR attribution missing required fields: "
                    + ", ".join(missing_attr)
                )

    return errors


def scan_for_provenance_defects(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    declared = payload.get("declared_provenance_tier")
    required = payload.get("required_provenance_tier")
    dependencies = payload.get("dependency_provenance_tiers", [])

    if required == "DOCUMENTED" and declared == "GENERATED":
        errors.append(
            f"{PROVENANCE_ESCALATION_DEFECT} "
            "declared_provenance_tier GENERATED cannot satisfy required_provenance_tier DOCUMENTED"
        )

    if declared == "DOCUMENTED" and isinstance(dependencies, list):
        if "GENERATED" in dependencies:
            errors.append(
                f"{PROVENANCE_DEPENDENCY_CONTAMINATION} "
                "declared_provenance_tier DOCUMENTED must not depend on GENERATED content"
            )

    return errors


def validate_provenance_tier(path: Path, schema_path: Path) -> list[str]:
    try:
        payload = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    errors = validate_against_schema(payload, schema_path)
    if errors:
        return errors

    if not isinstance(payload, dict):
        return ["SCHEMA_ERROR payload must be a JSON object"]

    errors.extend(scan_for_provenance_defects(payload))
    return errors


def run(paths: list[Path], schema_path: Path) -> int:
    any_failed = False

    for path in paths:
        errors = validate_provenance_tier(path, schema_path)
        if errors:
            any_failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"PROVENANCE_TIER_PASS {path}")

    return 1 if any_failed else 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Check Fork Provenance Tiers v0.1."
    )
    parser.add_argument(
        "artifacts",
        nargs="+",
        help="Paths to Provenance Tier JSON payloads.",
    )
    parser.add_argument(
        "--schema",
        default=str(repo_root / "schemas" / "provenance_tier_v0_1.schema.json"),
        help="Path to provenance tier schema JSON.",
    )

    args = parser.parse_args()

    artifact_paths = [Path(p).resolve() for p in args.artifacts]
    schema_path = Path(args.schema).resolve()

    return run(artifact_paths, schema_path)


if __name__ == "__main__":
    raise SystemExit(main())
