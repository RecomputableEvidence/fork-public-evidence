#!/usr/bin/env python3
"""
Fork Claim Boundary Binder v0.1

Purpose:
    Bind a machine-readable Fork artifact to an approved claim profile by
    attaching a derived top-level claim_boundary block.

Exit codes:
    0 = binding succeeded and resulting artifact passed Claim Boundary checks
    1 = binding failed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


try:
    from check_claim_boundary import scan_for_overclaims, validate_against_schema
    from check_artifact_claim_boundary import validate_artifact_envelope
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from check_claim_boundary import scan_for_overclaims, validate_against_schema  # type: ignore
    from check_artifact_claim_boundary import validate_artifact_envelope  # type: ignore


REQUIRED_PROFILE_FIELDS = [
    "profile_id",
    "profile_version",
    "claim_type",
    "claim_scope",
    "claim_statement",
    "allowed_inferences",
    "forbidden_inferences",
    "not_checked",
    "non_claims",
    "binding_rules",
]

CLAIM_BOUNDARY_FIELDS = [
    "claim_type",
    "claim_statement",
    "allowed_inferences",
    "forbidden_inferences",
    "not_checked",
    "non_claims",
]


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError(f"JSON_LOAD_ERROR: {path}: {exc}") from exc


def write_json_no_bom(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    path.write_text(rendered, encoding="utf-8")


def fallback_profile_validation(profile: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(profile, dict):
        return ["PROFILE_SCHEMA_ERROR: profile must be a JSON object"]

    keys = set(profile.keys())
    required = set(REQUIRED_PROFILE_FIELDS)

    missing = sorted(required - keys)
    if missing:
        errors.append(f"PROFILE_SCHEMA_ERROR: missing required fields: {', '.join(missing)}")

    extra = sorted(keys - required)
    if extra:
        errors.append(f"PROFILE_SCHEMA_ERROR: additional properties are not allowed: {', '.join(extra)}")

    if profile.get("profile_version") != "0.1":
        errors.append("PROFILE_SCHEMA_ERROR: profile_version must be '0.1'")

    if profile.get("claim_type") != "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY":
        errors.append("PROFILE_SCHEMA_ERROR: unsupported claim_type")

    for field in ["profile_id", "claim_scope", "claim_statement"]:
        value = profile.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"PROFILE_SCHEMA_ERROR: {field} must be a non-empty string")

    for field in ["allowed_inferences", "forbidden_inferences", "not_checked", "non_claims"]:
        value = profile.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"PROFILE_SCHEMA_ERROR: {field} must be a non-empty array")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"PROFILE_SCHEMA_ERROR: {field}[{index}] must be a non-empty string")

    rules = profile.get("binding_rules")
    if not isinstance(rules, dict):
        errors.append("PROFILE_SCHEMA_ERROR: binding_rules must be an object")
    else:
        if rules.get("existing_claim_boundary_policy") != "FAIL_UNLESS_REPLACE_FLAG":
            errors.append("PROFILE_SCHEMA_ERROR: binding_rules.existing_claim_boundary_policy must be FAIL_UNLESS_REPLACE_FLAG")
        if rules.get("emitted_artifact_must_pass_artifact_checker") is not True:
            errors.append("PROFILE_SCHEMA_ERROR: binding_rules.emitted_artifact_must_pass_artifact_checker must be true")

    return errors


def validate_profile(profile: Any, profile_schema_path: Path) -> list[str]:
    try:
        schema = load_json(profile_schema_path)
    except ValueError as exc:
        return [str(exc)]

    try:
        import jsonschema  # type: ignore
    except Exception:
        return fallback_profile_validation(profile)

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    errors: list[str] = []
    for error in sorted(validator.iter_errors(profile), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path)
        if location:
            errors.append(f"PROFILE_SCHEMA_ERROR: {location}: {error.message}")
        else:
            errors.append(f"PROFILE_SCHEMA_ERROR: {error.message}")

    return errors


def profile_to_claim_boundary(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "claim_type": profile["claim_type"],
        "claim_statement": profile["claim_statement"],
        "allowed_inferences": profile["allowed_inferences"],
        "forbidden_inferences": profile["forbidden_inferences"],
        "not_checked": profile["not_checked"],
        "non_claims": profile["non_claims"],
    }


def validate_bound_artifact_object(bound_artifact: dict[str, Any], claim_boundary_schema_path: Path) -> list[str]:
    errors = validate_artifact_envelope(bound_artifact)
    if errors:
        return errors

    claim_boundary = bound_artifact["claim_boundary"]

    schema_errors = validate_against_schema(claim_boundary, claim_boundary_schema_path)
    errors.extend(schema_errors)

    if not schema_errors:
        errors.extend(scan_for_overclaims(claim_boundary))

    return errors


def bind_claim_boundary(
    source_artifact_path: Path,
    profile_path: Path,
    output_path: Path,
    profile_schema_path: Path,
    claim_boundary_schema_path: Path,
    replace_existing_claim_boundary: bool,
    overwrite_output: bool,
) -> int:
    errors: list[str] = []

    try:
        artifact = load_json(source_artifact_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    try:
        profile = load_json(profile_path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not isinstance(artifact, dict):
        print("BINDING_ERROR: source artifact must be a JSON object", file=sys.stderr)
        return 1

    if not isinstance(profile, dict):
        print("BINDING_ERROR: claim profile must be a JSON object", file=sys.stderr)
        return 1

    profile_errors = validate_profile(profile, profile_schema_path)
    errors.extend(profile_errors)

    if "claim_boundary" in artifact and not replace_existing_claim_boundary:
        errors.append(
            "BINDING_REFUSAL_EXISTING_CLAIM_BOUNDARY: source artifact already contains claim_boundary; use --replace-existing-claim-boundary to replace it"
        )

    if output_path.exists() and not overwrite_output:
        errors.append(
            f"OUTPUT_EXISTS: {output_path}; use --overwrite-output to overwrite it"
        )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    claim_boundary = profile_to_claim_boundary(profile)

    boundary_schema_errors = validate_against_schema(claim_boundary, claim_boundary_schema_path)
    boundary_overclaim_errors: list[str] = []
    if not boundary_schema_errors:
        boundary_overclaim_errors = scan_for_overclaims(claim_boundary)

    errors.extend(boundary_schema_errors)
    errors.extend(boundary_overclaim_errors)

    bound_artifact = dict(artifact)
    bound_artifact["claim_boundary"] = claim_boundary

    errors.extend(validate_bound_artifact_object(bound_artifact, claim_boundary_schema_path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    write_json_no_bom(output_path, bound_artifact)
    print(f"CLAIM_BOUNDARY_BOUND: {output_path}")
    return 0


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser(
        description="Bind a Fork artifact to an approved claim profile"
    )
    parser.add_argument(
        "source_artifact",
        help="Path to source machine-readable artifact JSON"
    )
    parser.add_argument(
        "--profile",
        default=str(repo_root / "claim_profiles" / "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY_v0_1.json"),
        help="Path to approved claim profile JSON"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to write the bound artifact JSON"
    )
    parser.add_argument(
        "--profile-schema",
        default=str(repo_root / "schemas" / "claim_profile_v0_1.schema.json"),
        help="Path to claim profile schema"
    )
    parser.add_argument(
        "--claim-boundary-schema",
        default=str(repo_root / "schemas" / "claim_boundary_v0_1.schema.json"),
        help="Path to claim boundary payload schema"
    )
    parser.add_argument(
        "--replace-existing-claim-boundary",
        action="store_true",
        help="Replace an existing top-level claim_boundary block"
    )
    parser.add_argument(
        "--overwrite-output",
        action="store_true",
        help="Overwrite output path if it already exists"
    )

    args = parser.parse_args()

    return bind_claim_boundary(
        source_artifact_path=Path(args.source_artifact).resolve(),
        profile_path=Path(args.profile).resolve(),
        output_path=Path(args.output).resolve(),
        profile_schema_path=Path(args.profile_schema).resolve(),
        claim_boundary_schema_path=Path(args.claim_boundary_schema).resolve(),
        replace_existing_claim_boundary=args.replace_existing_claim_boundary,
        overwrite_output=args.overwrite_output,
    )


if __name__ == "__main__":
    raise SystemExit(main())