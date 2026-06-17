from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install project test dependencies before running this checker."
    ) from exc


REQUIRED_ARTIFACT_TYPES = {
    "REDACTION_SCOPE_ARTIFACT",
    "PILOT_CANONICALIZATION_RECORD",
    "DRY_RUN_APPROVAL_ARTIFACT",
    "WRITTEN_ORIENTATION_ARTIFACT",
    "LIVE_INGESTION_AUTHORIZATION_EXTERNAL_REFERENCE",
}

RECEIPT_NON_CLAIMS = [
    "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CERTIFY_SOURCE_TRUTH",
    "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CERTIFY_LEGAL_SUFFICIENCY",
    "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CERTIFY_HIPAA_COMPLIANCE",
    "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_AUTHORIZE_UNSCOPED_CONTENT_CAPTURE",
    "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CREATE_RUNTIME_AUTHORIZATION",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_paths(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(candidate for candidate in path.glob("*.json") if candidate.is_file())



def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dry_run_binding_errors(root: Path, artifact: dict[str, Any]) -> list[str]:
    if artifact.get("record_type") != "DRY_RUN_APPROVAL_ARTIFACT":
        return []

    binding = artifact.get("dry_run_output_binding", {})
    findings: list[str] = []

    pairs = [
        ("validation_receipt_ref", "validation_receipt_sha256"),
        ("dry_run_summary_ref", "dry_run_summary_sha256"),
    ]

    for ref_key, hash_key in pairs:
        ref_value = binding.get(ref_key)
        expected_hash = binding.get(hash_key)

        if not isinstance(ref_value, str) or not isinstance(expected_hash, str):
            findings.append(f"{ref_key}/{hash_key}: dry-run binding is incomplete")
            continue

        referenced_path = root / ref_value
        if not referenced_path.exists():
            findings.append(f"{ref_key}: referenced dry-run output does not exist: {ref_value}")
            continue

        actual_hash = sha256_file(referenced_path)
        if actual_hash.lower() != expected_hash.lower():
            findings.append(
                f"{hash_key}: expected {expected_hash}, computed {actual_hash} for {ref_value}"
            )

    return findings


def schema_errors(validator: Draft202012Validator, obj: dict[str, Any]) -> list[str]:
    errors = sorted(validator.iter_errors(obj), key=lambda err: list(err.path))
    messages: list[str] = []
    for err in errors:
        path = ".".join(str(part) for part in err.path)
        if path:
            messages.append(f"{path}: {err.message}")
        else:
            messages.append(err.message)
    return messages


def build_receipt(
    *,
    checked_path: Path,
    validation_result: str,
    artifact_count_received: int,
    artifact_count_valid: int,
    artifact_count_invalid: int,
    artifact_types_present: list[str],
    missing_required_artifact_types: list[str],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "record_type": "FORK_PILOT_APPROVAL_ARTIFACT_VALIDATION_RECEIPT",
        "schema_version": "0.1",
        "checked_path": str(checked_path),
        "validation_result": validation_result,
        "artifact_count_received": artifact_count_received,
        "artifact_count_valid": artifact_count_valid,
        "artifact_count_invalid": artifact_count_invalid,
        "artifact_types_present": artifact_types_present,
        "required_artifact_types_present": len(missing_required_artifact_types) == 0,
        "missing_required_artifact_types": missing_required_artifact_types,
        "errors": errors,
        "receipt_non_claims": RECEIPT_NON_CLAIMS,
    }


def validate_path(path: Path, require_complete_set: bool = False, schema_path: Path | None = None) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    schema_path = schema_path or root / "schemas" / "pilot_approval_artifacts_v0_1.schema.json"
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    paths = artifact_paths(path)
    errors: list[dict[str, Any]] = []
    valid_count = 0
    invalid_count = 0
    types_present: set[str] = set()

    for artifact_path in paths:
        try:
            artifact = load_json(artifact_path)
        except json.JSONDecodeError as exc:
            invalid_count += 1
            errors.append(
                {
                    "artifact_path": str(artifact_path),
                    "code": "JSON_INVALID",
                    "message": str(exc),
                }
            )
            continue

        artifact_type = artifact.get("record_type")
        if isinstance(artifact_type, str):
            types_present.add(artifact_type)

        artifact_errors = schema_errors(validator, artifact)
        if artifact_errors:
            invalid_count += 1
            errors.append(
                {
                    "artifact_path": str(artifact_path),
                    "artifact_id": artifact.get("artifact_id"),
                    "record_type": artifact.get("record_type"),
                    "code": "SCHEMA_INVALID",
                    "messages": artifact_errors,
                }
            )
            continue

        binding_errors = dry_run_binding_errors(root, artifact)
        if binding_errors:
            invalid_count += 1
            errors.append(
                {
                    "artifact_path": str(artifact_path),
                    "artifact_id": artifact.get("artifact_id"),
                    "record_type": artifact.get("record_type"),
                    "code": "DRY_RUN_OUTPUT_BINDING_INVALID",
                    "messages": binding_errors,
                }
            )
            continue

        valid_count += 1

    missing = sorted(REQUIRED_ARTIFACT_TYPES - types_present) if require_complete_set else []

    if invalid_count > 0:
        result = "REJECTED_SCHEMA_INVALID"
    elif missing:
        result = "REJECTED_REQUIRED_ARTIFACTS_MISSING"
    elif require_complete_set:
        result = "ACCEPTED"
    elif valid_count > 0:
        result = "ACCEPTED"
    else:
        result = "ACCEPTED_WITH_LIMITATIONS"

    return build_receipt(
        checked_path=path,
        validation_result=result,
        artifact_count_received=len(paths),
        artifact_count_valid=valid_count,
        artifact_count_invalid=invalid_count,
        artifact_types_present=sorted(types_present),
        missing_required_artifact_types=missing,
        errors=errors,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Fork Pilot Approval Artifact Templates v0.1.")
    parser.add_argument("--path", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=None)
    parser.add_argument("--require-complete-set", action="store_true")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    receipt = validate_path(args.path, args.require_complete_set, args.schema)
    output = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)

    return 0 if receipt["validation_result"] == "ACCEPTED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
