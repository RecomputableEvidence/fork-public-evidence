from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "check_controlled_pilot_readiness_gate.py"
INDEX_PATH = ROOT / "pilot_package" / "controlled_pilot_package_index_v0_1.json"
SCHEMA_PATH = ROOT / "schemas" / "controlled_pilot_readiness_gate_v0_1.schema.json"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_controlled_pilot_readiness_gate", TOOL_PATH
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(obj: dict) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(obj)]


def test_package_index_conforms_to_schema() -> None:
    assert schema_errors(load_json(INDEX_PATH)) == []


def test_readiness_gate_accepts_complete_package() -> None:
    checker = load_checker()
    receipt = checker.validate_readiness(INDEX_PATH)

    assert receipt["gate_result"] == "CONTROLLED_PILOT_PACKAGE_READY"
    assert receipt["component_count_missing"] == 0
    assert all(check["status"] == "PRESENT" for check in receipt["component_checks"])
    assert all(check["status"] == "PASS" for check in receipt["integration_checks"])


def test_readiness_receipt_conforms_to_schema() -> None:
    checker = load_checker()
    receipt = checker.validate_readiness(INDEX_PATH)

    assert schema_errors(receipt) == []


def test_readiness_gate_fails_missing_component(tmp_path: Path) -> None:
    index = load_json(INDEX_PATH)
    index["package_components"][0]["path"] = "docs/DOES_NOT_EXIST.md"

    bad_index_path = tmp_path / "bad_index.json"
    bad_index_path.write_text(
        json.dumps(index, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    checker = load_checker()
    receipt = checker.validate_readiness(bad_index_path)

    assert receipt["gate_result"] == "CONTROLLED_PILOT_PACKAGE_FAILED"
    assert receipt["component_count_missing"] == 1
    assert receipt["missing_components"][0]["code"] == "REQUIRED_COMPONENT_MISSING"


def test_readiness_receipt_preserves_non_claims() -> None:
    checker = load_checker()
    receipt = checker.validate_readiness(INDEX_PATH)

    assert "READINESS_GATE_DOES_NOT_AUTHORIZE_LIVE_INGESTION" in receipt["readiness_non_claims"]
    assert "READINESS_GATE_DOES_NOT_CERTIFY_PRODUCTION_READINESS" in receipt["readiness_non_claims"]
    assert "READINESS_GATE_DOES_NOT_CERTIFY_SOURCE_TRUTH" in receipt["readiness_non_claims"]
    assert "READINESS_GATE_DOES_NOT_REPLACE_INSTITUTIONAL_APPROVAL" in receipt["readiness_non_claims"]


def test_readiness_gate_runs_expected_integration_checks() -> None:
    checker = load_checker()
    receipt = checker.validate_readiness(INDEX_PATH)

    check_ids = {check["check_id"] for check in receipt["integration_checks"]}

    assert "nightly_batch_checker_valid_fixture" in check_ids
    assert "pilot_approval_artifacts_complete_set" in check_ids
    assert "pilot_dry_run_harness_aligned_synthetic_batch" in check_ids
