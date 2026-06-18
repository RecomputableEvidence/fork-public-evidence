from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_claim_consumption_event.py"
EXAMPLES = ROOT / "examples" / "claim_consumption_event"
OUTPUT_SCHEMA = ROOT / "schemas" / "claim_consumption_event_checker_output_v0_1.schema.json"
EVENT_SCHEMA = ROOT / "schemas" / "claim_consumption_event_v0_1.schema.json"

def run_checker(example_name: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / example_name)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.stdout.strip(), completed.stderr
    payload = json.loads(completed.stdout)
    return completed.returncode, payload

def assert_output_contract(payload: dict) -> None:
    schema = json.loads(OUTPUT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator(schema).validate(payload)

def test_event_schema_is_valid_draft7() -> None:
    schema = json.loads(EVENT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)

def test_output_schema_is_valid_draft7() -> None:
    schema = json.loads(OUTPUT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)

def test_valid_preserved_boundary_passes() -> None:
    code, payload = run_checker("valid_preserved_boundary.json")
    assert code == 0
    assert payload["result"] == {"ok": True, "result_kind": "STRUCTURAL_PASS"}
    assert payload["limitations"]["does_not_validate_approval"] is True
    assert payload["limitations"]["does_not_validate_truth"] is True
    assert payload["limitations"]["does_not_validate_compliance"] is True
    assert "APPROVAL" in payload["do_not_map_to"]
    assert "LEGAL_SUFFICIENCY" in payload["do_not_map_to"]
    assert_output_contract(payload)

def test_valid_narrowed_boundary_passes() -> None:
    code, payload = run_checker("valid_narrowed_boundary.json")
    assert code == 0
    assert payload["result"]["result_kind"] == "STRUCTURAL_PASS"
    assert payload["non_claims"]["does_not_approve_reliance"] is True
    assert payload["non_claims"]["does_not_validate_policy_fit"] is True
    assert_output_contract(payload)

def test_valid_expanded_boundary_passes_when_expansion_is_explicit() -> None:
    code, payload = run_checker("valid_expanded_boundary_explicit.json")
    assert code == 0
    assert payload["result"]["result_kind"] == "STRUCTURAL_PASS"
    assert_output_contract(payload)

def test_invalid_silent_expansion_fails_closed() -> None:
    code, payload = run_checker("invalid_silent_expansion.json")
    assert code != 0
    assert payload["result"]["ok"] is False
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCE_EXPANSION_REQUIRES_EXPLICIT_NEW_CLAIM" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_missing_decision_owner_fails_schema_validation() -> None:
    code, payload = run_checker("invalid_missing_decision_owner.json")
    assert code != 0
    assert payload["result"]["ok"] is False
    assert payload["result"]["result_kind"] == "SCHEMA_VALIDATION_FAILED"
    assert any("decision_owner" in error["message"] for error in payload["errors"])
    assert_output_contract(payload)

def test_checker_rejects_oracle_like_status_fields(tmp_path: Path) -> None:
    source = json.loads((EXAMPLES / "valid_preserved_boundary.json").read_text(encoding="utf-8"))
    source["approval_status"] = "APPROVED"

    candidate = tmp_path / "oracle_field.json"
    candidate.write_text(json.dumps(source, indent=2), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, str(CHECKER), str(candidate)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )

    payload = json.loads(completed.stdout)
    assert completed.returncode != 0
    assert payload["result"]["result_kind"] in {"SCHEMA_VALIDATION_FAILED", "CONTRACT_VALIDATION_FAILED"}
    assert_output_contract(payload)
