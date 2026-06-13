#!/usr/bin/env python3
"""
Fork Artifact Claim Boundary Checker v0.1

Purpose:
    Require machine-readable receipts, release metadata artifacts, and
    reviewer-facing machine summaries to carry a top-level claim_boundary
    block that passes the Fork Claim Boundary checker.

Exit codes:
    0 = all artifacts passed
    1 = one or more artifacts failed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from check_claim_boundary import scan_for_overclaims, validate_against_schema
except ImportError:
    sys.path.append(str(Path(__file__).resolve().parent))
    from check_claim_boundary import scan_for_overclaims, validate_against_schema  # type: ignore


SUPPORTED_ARTIFACT_TYPES = {
    "VERIFICATION_RECEIPT",
    "COHERENCE_RECEIPT",
    "CONFORMANCE_RECEIPT",
    "RELEASE_METADATA",
    "REVIEWER_SUMMARY",
    "MACHINE_READABLE_EVIDENCE_SUMMARY",
}


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError(f"JSON_LOAD_ERROR: {path}: {exc}") from exc


def validate_artifact_envelope(artifact: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(artifact, dict):
        return ["ARTIFACT_SCHEMA_ERROR: artifact must be a JSON object"]

    artifact_type = artifact.get("artifact_type")
    if artifact_type is not None:
        if not isinstance(artifact_type, str):
            errors.append("ARTIFACT_SCHEMA_ERROR: artifact_type must be a string when present")
        elif artifact_type not in SUPPORTED_ARTIFACT_TYPES:
            errors.append(f"ARTIFACT_SCHEMA_ERROR: unsupported artifact_type: {artifact_type!r}")

    if "claim_boundary" not in artifact:
        errors.append("CLAIM_BOUNDARY_BLOCK_MISSING: artifact must include top-level 'claim_boundary' object")
        return errors

    claim_boundary = artifact.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("CLAIM_BOUNDARY_BLOCK_INVALID: claim_boundary must be a JSON object")

    return errors


def validate_artifact(path: Path, claim_boundary_schema_path: Path) -> list[str]:
    try:
        artifact = load_json(path)
    except ValueError as exc:
        return [str(exc)]

    errors = validate_artifact_envelope(artifact)

    if errors:
        return errors

    claim_boundary = artifact["claim_boundary"]

    schema_errors = validate_against_schema(claim_boundary, claim_boundary_schema_path)
    errors.extend(schema_errors)

    if not schema_errors:
        errors.extend(scan_for_overclaims(claim_boundary))

    return errors


def run(paths: list[Path], claim_boundary_schema_path: Path) -> int:
    any_failed = False

    for path in paths:
        errors = validate_artifact(path, claim_boundary_schema_path)

        if errors:
            any_failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"ARTIFACT_CLAIM_BOUNDARY_PASS: {path}")

    return 1 if any_failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Require artifacts to carry a passing Fork claim_boundary block"
    )
    parser.add_argument(
        "artifacts",
        nargs="+",
        help="Path(s) to machine-readable artifact JSON files"
    )
    parser.add_argument(
        "--claim-boundary-schema",
        default=str(
            Path(__file__).resolve().parents[1]
            / "schemas"
            / "claim_boundary_v0_1.schema.json"
        ),
        help="Path to the claim boundary payload schema"
    )

    args = parser.parse_args()

    artifact_paths = [Path(p).resolve() for p in args.artifacts]
    claim_boundary_schema_path = Path(args.claim_boundary_schema).resolve()

    return run(artifact_paths, claim_boundary_schema_path)


if __name__ == "__main__":
    raise SystemExit(main())