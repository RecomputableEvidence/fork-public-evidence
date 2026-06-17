from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "check_pilot_approval_artifacts.py"
TEMPLATE_DIR = ROOT / "templates" / "pilot_approval_artifacts"
INVALID_DIR = ROOT / "examples" / "pilot_approval_artifacts" / "invalid"
SCHEMA_PATH = ROOT / "schemas" / "pilot_approval_artifacts_v0_1.schema.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_pilot_approval_artifacts", TOOL_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_checker_accepts_complete_template_set() -> None:
    checker = load_checker()
    receipt = checker.validate_path(TEMPLATE_DIR, require_complete_set=True)

    assert receipt["validation_result"] == "ACCEPTED"
    assert receipt["artifact_count_received"] == 4
    assert receipt["artifact_count_valid"] == 4
    assert receipt["artifact_count_invalid"] == 0
    assert receipt["required_artifact_types_present"] is True


def test_checker_rejects_missing_required_artifact_when_complete_set_required(tmp_path: Path) -> None:
    for template_path in TEMPLATE_DIR.glob("*.json"):
        if "written_orientation" not in template_path.name:
            shutil.copy(template_path, tmp_path / template_path.name)

    checker = load_checker()
    receipt = checker.validate_path(tmp_path, require_complete_set=True)

    assert receipt["validation_result"] == "REJECTED_REQUIRED_ARTIFACTS_MISSING"
    assert "WRITTEN_ORIENTATION_ARTIFACT" in receipt["missing_required_artifact_types"]


def test_checker_rejects_invalid_artifact() -> None:
    checker = load_checker()
    receipt = checker.validate_path(INVALID_DIR / "invalid_canonicalization_wrong_hash_algorithm.json")

    assert receipt["validation_result"] == "REJECTED_SCHEMA_INVALID"
    assert receipt["artifact_count_invalid"] == 1
    assert receipt["errors"][0]["code"] == "SCHEMA_INVALID"


def test_checker_receipt_preserves_non_claims() -> None:
    checker = load_checker()
    receipt = checker.validate_path(TEMPLATE_DIR, require_complete_set=True)

    assert "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CERTIFY_SOURCE_TRUTH" in receipt["receipt_non_claims"]
    assert "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CERTIFY_HIPAA_COMPLIANCE" in receipt["receipt_non_claims"]
    assert "APPROVAL_ARTIFACT_VALIDATION_DOES_NOT_CREATE_RUNTIME_AUTHORIZATION" in receipt["receipt_non_claims"]


def test_checker_emitted_receipt_conforms_to_schema() -> None:
    checker = load_checker()
    receipt = checker.validate_path(TEMPLATE_DIR, require_complete_set=True)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(receipt))

    assert errors == []
