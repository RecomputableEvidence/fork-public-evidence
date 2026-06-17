from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "nightly_batch_export_v0_1_1.schema.json"
VALID_DIR = ROOT / "examples" / "nightly_batch_export" / "valid"
INVALID_DIR = ROOT / "examples" / "nightly_batch_export" / "invalid"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_first_jsonl(path: Path) -> dict:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    return json.loads(first_line)


def schema_errors(obj: dict) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(obj)]


def assert_valid(obj: dict) -> None:
    errors = schema_errors(obj)
    assert errors == []


def assert_invalid(obj: dict) -> None:
    errors = schema_errors(obj)
    assert errors != []


def test_valid_manifest_and_record_conform_to_schema() -> None:
    assert_valid(load_json(VALID_DIR / "valid_hash_reference_only_manifest.json"))
    assert_valid(load_first_jsonl(VALID_DIR / "valid_hash_reference_only_records.jsonl"))


def test_valid_missing_hash_with_reason_conforms_to_schema() -> None:
    assert_valid(load_first_jsonl(VALID_DIR / "valid_missing_hash_with_reason_records.jsonl"))


def test_valid_claim_consumption_preserved_conforms_to_schema() -> None:
    assert_valid(load_first_jsonl(VALID_DIR / "valid_claim_consumption_preserved_records.jsonl"))


def test_valid_synthetic_dry_run_manifest_conforms_to_schema() -> None:
    assert_valid(load_json(VALID_DIR / "valid_synthetic_dry_run_manifest.json"))


def test_rejects_sha256_hash_too_short() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_sha256_hash_too_short_records.jsonl"))


def test_rejects_hash_and_reason_both_null() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_hash_and_reason_both_null_records.jsonl"))


def test_rejects_hash_and_reason_both_present() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_hash_and_reason_both_present_records.jsonl"))


def test_rejects_redacted_without_redaction_scope() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_redacted_without_redaction_scope_records.jsonl"))


def test_rejects_full_content_without_exception() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_full_content_without_exception_records.jsonl"))


def test_rejects_missing_required_non_claim() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_missing_required_non_claim_records.jsonl"))


def test_rejects_expanded_claim_consumption_without_authority() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_claim_consumption_expanded_without_authority_records.jsonl"))


def test_rejects_free_text_scope_evaluated() -> None:
    assert_invalid(load_first_jsonl(INVALID_DIR / "invalid_free_text_scope_evaluated_records.jsonl"))
