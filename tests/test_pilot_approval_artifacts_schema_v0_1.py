from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "pilot_approval_artifacts_v0_1.schema.json"
TEMPLATE_DIR = ROOT / "templates" / "pilot_approval_artifacts"
INVALID_DIR = ROOT / "examples" / "pilot_approval_artifacts" / "invalid"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(obj: dict) -> list[str]:
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(obj)]


def assert_valid(obj: dict) -> None:
    assert schema_errors(obj) == []


def assert_invalid(obj: dict) -> None:
    assert schema_errors(obj) != []


def test_all_templates_conform_to_schema() -> None:
    template_paths = sorted(TEMPLATE_DIR.glob("*.json"))
    assert len(template_paths) == 4
    for template_path in template_paths:
        assert_valid(load_json(template_path))


def test_rejects_redaction_missing_approval_authority() -> None:
    assert_invalid(load_json(INVALID_DIR / "invalid_redaction_missing_approval_authority.json"))


def test_rejects_canonicalization_wrong_hash_algorithm() -> None:
    assert_invalid(load_json(INVALID_DIR / "invalid_canonicalization_wrong_hash_algorithm.json"))


def test_rejects_dry_run_unapproved_content_captured() -> None:
    assert_invalid(load_json(INVALID_DIR / "invalid_dry_run_unapproved_content_captured.json"))


def test_rejects_orientation_missing_non_claim() -> None:
    assert_invalid(load_json(INVALID_DIR / "invalid_orientation_missing_non_claim.json"))
