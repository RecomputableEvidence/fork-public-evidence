#!/usr/bin/env python3
"""
AI Governance System Placement Profile Checker v0.2

Adds Structural Execution Receipts over deterministic normalized checker outputs.

Scope:
- Emits SHA-256 receipts over NORMALIZED_CHECKER_OUTPUT_ONLY.
- Compares existing normalized outputs to receipts.
- Supports full source recompute by re-running the v0.1.1 checker, regenerating
  normalized output, and comparing its SHA-256 hash to the receipt.
- Does not modify the Placement Profile schema.
- Does not validate semantic truth, legal sufficiency, compliance sufficiency,
  audit sufficiency, model safety, runtime behavior, external artifacts,
  cross-record graph validity, or institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


CHECKER_ID = "ai_governance_system_placement_profile_checker_v0_2"
CHECKER_VERSION = "0.2"
RECEIPT_TYPE = "STRUCTURAL_EXECUTION_RECEIPT"
RECEIPT_ARTIFACT_NAME = "Structural Execution Receipt"
RECEIPT_VERSION = "0.2"
HASH_ALGORITHM = "sha256"
HASH_SCOPE = "NORMALIZED_CHECKER_OUTPUT_ONLY"

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_NON_CLAIMS = [
    "Does not validate semantic truth.",
    "Does not validate legal sufficiency.",
    "Does not validate compliance sufficiency.",
    "Does not validate audit sufficiency.",
    "Does not validate model safety.",
    "Does not provide runtime enforcement.",
    "Does not verify external artifact existence.",
    "Does not perform cross-record graph validation.",
    "Does not grant institutional authority.",
    "Does not certify governance systems.",
    "Does not determine whether evidence is legally admissible.",
    "Does not determine whether a workflow decision was correct.",
    "Does not determine whether an organization satisfied regulatory obligations.",
    "Does not infer claim inheritance across handoffs.",
    "Does not treat receipt hashing as proof of governance sufficiency.",
]

EXCLUDED_FROM_HASH = [
    "checked_at_utc",
    "receipt_created_at_utc",
    "record_path",
    "schema_path",
    "environment",
    "runtime_duration",
    "working_directory",
    "hostname",
    "username",
    "stdout",
    "stderr",
]

REQUIRED_RECEIPT_FIELDS = [
    "receipt_type",
    "receipt_artifact_name",
    "receipt_version",
    "receipt_status",
    "checker_id",
    "checker_version",
    "schema_id",
    "schema_version",
    "record_id",
    "system_id",
    "overall_status",
    "checker_exit_code",
    "hash_algorithm",
    "normalized_output_sha256",
    "normalized_output_hash_scope",
    "normalized_output_hash_input_description",
    "receipt_created_at_utc",
    "receipt_environment_fields_excluded_from_hash",
    "non_claims",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(obj, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")


def deterministic_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_normalized_output(normalized_output: Any) -> str:
    return hashlib.sha256(deterministic_json_bytes(normalized_output)).hexdigest()


def legacy_checker_path() -> Path:
    preferred = REPO_ROOT / "tools" / "check_ai_governance_system_placement_profile_v0_1_1.py"
    fallback = REPO_ROOT / "tools" / "check_ai_governance_system_placement_profile_v0_1.py"
    if preferred.exists():
        return preferred
    if fallback.exists():
        return fallback
    raise FileNotFoundError("Missing v0.1.1 or v0.1 placement profile checker.")


def run_legacy_checker(
    record_path: Path,
    schema_path: Path,
    output_path: Optional[Path],
    normalized_output_path: Path,
) -> int:
    checker = legacy_checker_path()
    args = [
        sys.executable,
        str(checker),
        "--record",
        str(record_path),
        "--schema",
        str(schema_path),
        "--normalized-output",
        str(normalized_output_path),
    ]
    if output_path is not None:
        args.extend(["--output", str(output_path)])
    proc = subprocess.run(args, cwd=str(REPO_ROOT))
    return int(proc.returncode)


def make_receipt(normalized_output: Dict[str, Any], checker_exit_code: int) -> Dict[str, Any]:
    return {
        "receipt_type": RECEIPT_TYPE,
        "receipt_artifact_name": RECEIPT_ARTIFACT_NAME,
        "receipt_version": RECEIPT_VERSION,
        "receipt_status": "EMITTED",
        "checker_id": CHECKER_ID,
        "checker_version": CHECKER_VERSION,
        "source_checker_id": normalized_output.get("checker_id", "UNKNOWN_SOURCE_CHECKER"),
        "source_checker_version": normalized_output.get("checker_version", "UNKNOWN_SOURCE_CHECKER_VERSION"),
        "schema_id": "ai_governance_system_placement_profile_v0_1",
        "schema_version": "0.1",
        "record_id": normalized_output.get("record_id", "UNKNOWN_RECORD_ID"),
        "system_id": normalized_output.get("system_id", "UNKNOWN_SYSTEM_ID"),
        "overall_status": normalized_output.get("overall_status", "UNKNOWN"),
        "checker_exit_code": checker_exit_code,
        "hash_algorithm": HASH_ALGORITHM,
        "normalized_output_sha256": sha256_normalized_output(normalized_output),
        "normalized_output_hash_scope": HASH_SCOPE,
        "normalized_output_hash_input_description": (
            "Deterministic JSON serialization of normalized checker output using "
            "UTF-8, sorted keys, compact separators, and no environment-specific fields."
        ),
        "receipt_created_at_utc": utc_now(),
        "receipt_environment_fields_excluded_from_hash": EXCLUDED_FROM_HASH,
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_receipt(receipt: Any) -> List[str]:
    errors: List[str] = []
    if not isinstance(receipt, dict):
        return ["ERR_RECEIPT_TOP_LEVEL_NOT_OBJECT"]

    for field in REQUIRED_RECEIPT_FIELDS:
        if field not in receipt:
            errors.append(f"ERR_RECEIPT_REQUIRED_FIELD_MISSING:{field}")

    if receipt.get("receipt_type") != RECEIPT_TYPE:
        errors.append("ERR_RECEIPT_TYPE_UNSUPPORTED")
    if receipt.get("hash_algorithm") != HASH_ALGORITHM:
        errors.append("ERR_UNSUPPORTED_HASH_ALGORITHM")
    if receipt.get("normalized_output_hash_scope") != HASH_SCOPE:
        errors.append("ERR_RECEIPT_SCOPE_UNSUPPORTED")

    digest = receipt.get("normalized_output_sha256")
    if isinstance(digest, str):
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest.lower()):
            errors.append("ERR_NORMALIZED_OUTPUT_SHA256_INVALID")
    elif "normalized_output_sha256" in receipt:
        errors.append("ERR_NORMALIZED_OUTPUT_SHA256_INVALID")

    return errors


def invalid_verification_result(mode: str, errors: List[str]) -> Dict[str, Any]:
    return {
        "verification_type": "STRUCTURAL_EXECUTION_RECEIPT_VERIFICATION_RESULT",
        "verification_version": RECEIPT_VERSION,
        "verification_mode": mode,
        "verification_status": "RECEIPT_INVALID",
        "errors": errors,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_scope": HASH_SCOPE,
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def make_verification_result(
    mode: str,
    status: str,
    receipt: Dict[str, Any],
    computed_hash: str,
    recomputed_output: Optional[Dict[str, Any]] = None,
    checker_exit_code: Optional[int] = None,
) -> Dict[str, Any]:
    return {
        "verification_type": "STRUCTURAL_EXECUTION_RECEIPT_VERIFICATION_RESULT",
        "verification_version": RECEIPT_VERSION,
        "verification_mode": mode,
        "verification_status": status,
        "receipt_type": receipt.get("receipt_type"),
        "receipt_version": receipt.get("receipt_version"),
        "checker_id": receipt.get("checker_id"),
        "checker_version": receipt.get("checker_version"),
        "schema_id": receipt.get("schema_id"),
        "schema_version": receipt.get("schema_version"),
        "record_id": receipt.get("record_id"),
        "system_id": receipt.get("system_id"),
        "hash_algorithm": receipt.get("hash_algorithm"),
        "expected_normalized_output_sha256": receipt.get("normalized_output_sha256"),
        "computed_normalized_output_sha256": computed_hash,
        "hash_scope": receipt.get("normalized_output_hash_scope"),
        "overall_status_from_receipt": receipt.get("overall_status"),
        "overall_status_from_recomputed_output": (
            recomputed_output.get("overall_status") if isinstance(recomputed_output, dict) else None
        ),
        "checker_exit_code_from_full_recompute": checker_exit_code,
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def emit_receipt(args: argparse.Namespace) -> int:
    if not args.record or not args.schema or not args.normalized_output:
        print("--emit-receipt requires --record, --schema, and --normalized-output", file=sys.stderr)
        return 1

    record_path = Path(args.record)
    schema_path = Path(args.schema)
    normalized_path = Path(args.normalized_output)
    output_path = Path(args.output) if args.output else None

    checker_exit = run_legacy_checker(record_path, schema_path, output_path, normalized_path)

    if not normalized_path.exists():
        print("Legacy checker did not emit normalized output; receipt not emitted.", file=sys.stderr)
        return 1

    try:
        normalized_output = load_json(normalized_path)
    except Exception as exc:
        print(f"Could not parse normalized output: {exc}", file=sys.stderr)
        return 1

    receipt = make_receipt(normalized_output, checker_exit)
    write_json(Path(args.emit_receipt), receipt)

    if checker_exit in (0, 1, 2):
        return checker_exit
    return 1


def load_receipt_for_verification(path: Path, mode: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    try:
        receipt = load_json(path)
    except Exception as exc:
        return None, invalid_verification_result(mode, [f"ERR_RECEIPT_JSON_PARSE:{exc}"])
    errors = validate_receipt(receipt)
    if errors:
        return None, invalid_verification_result(mode, errors)
    return receipt, None


def compare_normalized_output_to_receipt(args: argparse.Namespace) -> int:
    mode = "NORMALIZED_OUTPUT_HASH_COMPARISON"

    if not args.normalized_output:
        result = invalid_verification_result(mode, ["ERR_NORMALIZED_OUTPUT_REQUIRED"])
        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), result)
        print("--verify-receipt without --full-recompute requires --normalized-output", file=sys.stderr)
        return 1

    receipt, invalid_result = load_receipt_for_verification(Path(args.verify_receipt), mode)
    if invalid_result is not None:
        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), invalid_result)
        return 1

    try:
        normalized_output = load_json(Path(args.normalized_output))
    except Exception as exc:
        result = invalid_verification_result(mode, [f"ERR_NORMALIZED_OUTPUT_JSON_PARSE:{exc}"])
        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), result)
        return 1

    computed = sha256_normalized_output(normalized_output)
    expected = receipt["normalized_output_sha256"]
    status = "NORMALIZED_OUTPUT_HASH_MATCH" if computed == expected else "NORMALIZED_OUTPUT_HASH_MISMATCH"
    result = make_verification_result(mode, status, receipt, computed, normalized_output, None)

    if args.receipt_verification_output:
        write_json(Path(args.receipt_verification_output), result)

    return 0 if status == "NORMALIZED_OUTPUT_HASH_MATCH" else 1


def full_source_recompute(args: argparse.Namespace) -> int:
    mode = "FULL_SOURCE_RECOMPUTE"

    if not args.record or not args.schema:
        result = invalid_verification_result(mode, ["ERR_RECORD_AND_SCHEMA_REQUIRED_FOR_FULL_RECOMPUTE"])
        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), result)
        print("--full-recompute requires --record and --schema", file=sys.stderr)
        return 1

    receipt, invalid_result = load_receipt_for_verification(Path(args.verify_receipt), mode)
    if invalid_result is not None:
        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), invalid_result)
        return 1

    normalized_output_arg = Path(args.normalized_output) if args.normalized_output else None
    output_path = Path(args.output) if args.output else None

    with tempfile.TemporaryDirectory() as tmp:
        normalized_path = normalized_output_arg or (Path(tmp) / "recomputed_normalized_output.json")
        checker_exit = run_legacy_checker(Path(args.record), Path(args.schema), output_path, normalized_path)

        if not normalized_path.exists():
            result = invalid_verification_result(mode, ["ERR_RECOMPUTED_NORMALIZED_OUTPUT_NOT_EMITTED"])
            result["checker_exit_code_from_full_recompute"] = checker_exit
            if args.receipt_verification_output:
                write_json(Path(args.receipt_verification_output), result)
            return 1

        try:
            recomputed_output = load_json(normalized_path)
        except Exception as exc:
            result = invalid_verification_result(mode, [f"ERR_RECOMPUTED_NORMALIZED_OUTPUT_JSON_PARSE:{exc}"])
            result["checker_exit_code_from_full_recompute"] = checker_exit
            if args.receipt_verification_output:
                write_json(Path(args.receipt_verification_output), result)
            return 1

        computed = sha256_normalized_output(recomputed_output)
        expected = receipt["normalized_output_sha256"]
        status = "FULL_RECOMPUTE_MATCH" if computed == expected else "FULL_RECOMPUTE_MISMATCH"
        result = make_verification_result(mode, status, receipt, computed, recomputed_output, checker_exit)

        if args.receipt_verification_output:
            write_json(Path(args.receipt_verification_output), result)

        return 0 if status == "FULL_RECOMPUTE_MATCH" else 1


def pass_through_checker(args: argparse.Namespace) -> int:
    if not args.record or not args.schema or not args.normalized_output:
        print("checker pass-through requires --record, --schema, and --normalized-output", file=sys.stderr)
        return 1
    return run_legacy_checker(
        Path(args.record),
        Path(args.schema),
        Path(args.output) if args.output else None,
        Path(args.normalized_output),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Governance System Placement Profile Checker v0.2 Structural Execution Receipts"
    )
    parser.add_argument("--record", help="Placement profile source record JSON.")
    parser.add_argument("--schema", help="Placement profile schema JSON.")
    parser.add_argument("--output", help="Full checker output path.")
    parser.add_argument("--normalized-output", help="Normalized checker output path.")
    parser.add_argument("--emit-receipt", help="Emit Structural Execution Receipt JSON to this path.")
    parser.add_argument("--verify-receipt", help="Verify against this Structural Execution Receipt JSON.")
    parser.add_argument("--receipt-verification-output", help="Write receipt verification result JSON to this path.")
    parser.add_argument("--full-recompute", action="store_true", help="Re-run checker from source record and schema before comparing receipt hash.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.emit_receipt and args.verify_receipt:
        print("Use either --emit-receipt or --verify-receipt, not both.", file=sys.stderr)
        return 1

    if args.emit_receipt:
        return emit_receipt(args)

    if args.verify_receipt:
        if args.full_recompute:
            return full_source_recompute(args)
        return compare_normalized_output_to_receipt(args)

    if args.record and args.schema:
        return pass_through_checker(args)

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

