import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path.cwd()
CHECKER = ROOT / "tools" / "check_ccec_governance_interoperability.py"
EXAMPLES = ROOT / "examples" / "ccec_governance_interoperability"
OUTPUT_SCHEMA = ROOT / "schemas" / "ccec_governance_interoperability_checker_output_v0_1.schema.json"
PROFILE_SCHEMA = ROOT / "schemas" / "ccec_governance_interoperability_profile_v0_1.schema.json"

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

def test_profile_schema_is_valid_draft7() -> None:
    schema = json.loads(PROFILE_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)

def test_output_schema_is_valid_draft7() -> None:
    schema = json.loads(OUTPUT_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)

def test_valid_grc_register_reference_passes() -> None:
    code, payload = run_checker("valid_grc_register_reference.json")
    assert code == 0
    assert payload["checker"]["version"] == "0.1.1"
    assert payload["result"] == {"ok": True, "result_kind": "STRUCTURAL_PASS"}
    assert payload["limitations"]["does_not_transfer_authority"] is True
    assert payload["limitations"]["safe_to_automate"] is False
    assert payload["limitations"]["automation_interpretation_required"] is True
    assert payload["limitations"]["does_not_validate_control_satisfaction"] is True
    assert "AUTHORITY_TRANSFER" in payload["do_not_map_to"]
    assert "CONTROL_SATISFIED" in payload["do_not_map_to"]
    assert "EVIDENCE_SUFFICIENCY" in payload["do_not_map_to"]
    assert_output_contract(payload)

def test_valid_audit_evidence_reference_passes() -> None:
    code, payload = run_checker("valid_audit_evidence_reference.json")
    assert code == 0
    assert payload["result"]["result_kind"] == "STRUCTURAL_PASS"
    assert payload["non_claims"]["does_not_close_unresolved_gaps"] is True
    assert_output_contract(payload)

def test_invalid_compliance_oracle_mapping_fails_closed() -> None:
    code, payload = run_checker("invalid_compliance_oracle_mapping.json")
    assert code != 0
    assert payload["result"]["ok"] is False
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_ORACLE_TARGET_FIELD" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_authority_inheritance_fails_closed() -> None:
    code, payload = run_checker("invalid_authority_inheritance.json")
    assert code != 0
    assert payload["result"]["ok"] is False
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_AUTHORITY_INHERITANCE_PROHIBITED" for error in payload["errors"])
    assert_output_contract(payload)

def test_mapping_kind_must_be_listed_in_permitted_mappings(tmp_path: Path) -> None:
    source = json.loads((EXAMPLES / "valid_grc_register_reference.json").read_text(encoding="utf-8"))
    source["permitted_mappings"].remove("DECISION_OWNER_REFERENCE")

    candidate = tmp_path / "missing_permitted_mapping.json"
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
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_MAPPING_KIND_NOT_PERMITTED" for error in payload["errors"])
    assert_output_contract(payload)

def test_prohibited_mappings_must_be_complete(tmp_path: Path) -> None:
    source = json.loads((EXAMPLES / "valid_grc_register_reference.json").read_text(encoding="utf-8"))
    source["prohibited_mappings"].remove("CONTROL_SATISFIED")

    candidate = tmp_path / "missing_prohibited_mapping.json"
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
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_PROHIBITED_MAPPINGS_INCOMPLETE" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_composite_control_satisfied_rule_fails_closed() -> None:
    code, payload = run_checker("invalid_composite_control_satisfied_rule.json")
    assert code != 0
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_ORACLE_TARGET_FIELD" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_dashboard_badge_collapse_fails_closed() -> None:
    code, payload = run_checker("invalid_dashboard_badge_collapse.json")
    assert code != 0
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_RENDERING_CONSTRAINT_VIOLATION" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_decision_owner_as_approver_fails_closed() -> None:
    code, payload = run_checker("invalid_decision_owner_as_approver.json")
    assert code != 0
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_ORACLE_TARGET_FIELD" for error in payload["errors"])
    assert_output_contract(payload)

def test_invalid_aggregation_control_effectiveness_fails_closed() -> None:
    code, payload = run_checker("invalid_aggregation_control_effectiveness.json")
    assert code != 0
    assert payload["result"]["result_kind"] == "CONTRACT_VALIDATION_FAILED"
    assert any(error["code"] == "CCEC_INTEROP_AGGREGATION_CONSTRAINT_VIOLATION" for error in payload["errors"])
    assert_output_contract(payload)
