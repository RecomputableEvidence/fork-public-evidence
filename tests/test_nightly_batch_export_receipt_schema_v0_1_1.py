from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "examples" / "nightly_batch_export" / "valid"
TOOL_PATH = ROOT / "tools" / "check_nightly_batch_export.py"
SCHEMA_PATH = ROOT / "schemas" / "nightly_batch_export_v0_1_1.schema.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_nightly_batch_export", TOOL_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_checker_emitted_receipt_conforms_to_schema() -> None:
    checker = load_checker()
    receipt = checker.validate_batch(
        VALID_DIR / "valid_hash_reference_only_manifest.json",
        VALID_DIR / "valid_hash_reference_only_records.jsonl",
    )

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(receipt))

    assert errors == []
