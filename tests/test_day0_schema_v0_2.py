import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/day0_schema_v0_2"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

SCHEMA = load(ROOT / "schemas/longitudinal_reconstruction_day0_packet_manifest_v0_2.schema.json")
VALID = load(FIXTURES / "valid_manifest.json")
CASES = load(FIXTURES / "invalid_cases.json")

def validator():
    checker = FormatChecker()
    assert "date-time" in checker.checkers, "Date-time validation dependency is missing"
    Draft202012Validator.check_schema(SCHEMA)
    return Draft202012Validator(SCHEMA, format_checker=checker)

def test_valid_successor_fixture():
    assert list(validator().iter_errors(VALID)) == []

@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_invalid_fixture_rejected_for_expected_reason(case):
    errors = list(validator().iter_errors(case["instance"]))
    assert any(
        error.validator == case["expected_keyword"]
        and list(error.absolute_path) == case["expected_path"]
        for error in errors
    ), [error.message for error in errors]

def test_predecessor_still_satisfies_original_schema():
    schema = load(ROOT / "schemas/longitudinal_reconstruction_day0_packet_manifest_v0_1.schema.json")
    manifest = load(ROOT / "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/packet_manifest.json")
    Draft202012Validator.check_schema(schema)
    assert list(Draft202012Validator(schema).iter_errors(manifest)) == []

def test_timezone_offset_is_valid():
    instance = copy.deepcopy(VALID)
    instance["created_at_fixed_fixture_time"] = "2026-07-08T17:00:00-07:00"
    assert list(validator().iter_errors(instance)) == []

def test_schema_does_not_claim_file_existence():
    instance = copy.deepcopy(VALID)
    instance["artifact_hashes"][0]["path"] = "synthetic/nonexistent-file.json"
    assert list(validator().iter_errors(instance)) == []
