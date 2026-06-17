from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "examples" / "nightly_batch_export" / "valid"
INVALID_DIR = ROOT / "examples" / "nightly_batch_export" / "invalid"
TOOL_PATH = ROOT / "tools" / "check_nightly_batch_export.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_nightly_batch_export", TOOL_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_checker_accepts_valid_hash_reference_only_batch() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        VALID_DIR / "valid_hash_reference_only_records.jsonl",
    )

    assert receipt["batch_result"] == "ACCEPTED"
    assert receipt["record_count_received"] == 1
    assert receipt["record_count_accepted"] == 1
    assert receipt["record_count_excluded"] == 0
    assert receipt["record_count_failed_schema"] == 0


def test_checker_accepts_missing_hash_with_limitation() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        VALID_DIR / "valid_missing_hash_with_reason_records.jsonl",
    )

    assert receipt["batch_result"] == "ACCEPTED_WITH_LIMITATIONS"
    assert receipt["record_count_received"] == 1
    assert receipt["record_count_accepted"] == 1
    assert receipt["record_count_missing_hash"] == 1
    assert receipt["limitations"][0]["code"] == "HASH_NOT_AVAILABLE"


def test_checker_excludes_unapproved_source_without_overriding_workflow() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        INVALID_DIR / "invalid_unapproved_source_records.jsonl",
    )

    assert receipt["batch_result"] == "ACCEPTED_WITH_LIMITATIONS"
    assert receipt["record_count_received"] == 1
    assert receipt["record_count_accepted"] == 0
    assert receipt["record_count_excluded"] == 1
    assert receipt["record_count_unknown_source"] == 1
    assert receipt["limitations"][0]["code"] == "UNKNOWN_SOURCE_EXCLUDED"


def test_checker_rejects_schema_invalid_record() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        INVALID_DIR / "invalid_sha256_hash_too_short_records.jsonl",
    )

    assert receipt["batch_result"] == "REJECTED_SCHEMA_INVALID"
    assert receipt["record_count_failed_schema"] == 1
    assert receipt["errors"][0]["code"] == "RECORD_SCHEMA_INVALID"


def test_checker_rejects_batch_id_mismatch() -> None:
    checker = load_checker()

    mismatch_path = INVALID_DIR / "_tmp_invalid_batch_id_mismatch_records.jsonl"
    source_text = (VALID_DIR / "valid_hash_reference_only_records.jsonl").read_text(encoding="utf-8")
    mismatch_path.write_text(source_text.replace("batch_2026_06_17_001", "batch_wrong"), encoding="utf-8", newline="\n")

    try:
        receipt = checker.validate_batch(
            VALID_DIR / "valid_hash_reference_only_manifest.json",
            mismatch_path,
        )
    finally:
        mismatch_path.unlink(missing_ok=True)

    assert receipt["batch_result"] == "REJECTED_SCHEMA_INVALID"
    assert receipt["record_count_failed_schema"] == 1
    assert "does not match manifest batch_id" in receipt["errors"][0]["messages"][-1]


def test_checker_receipt_preserves_non_claims() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        VALID_DIR / "valid_hash_reference_only_records.jsonl",
    )

    assert "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_SOURCE_TRUTH" in receipt["receipt_non_claims"]
    assert "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_COMPLIANCE" in receipt["receipt_non_claims"]
    assert "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_MEDICAL_CORRECTNESS" in receipt["receipt_non_claims"]
