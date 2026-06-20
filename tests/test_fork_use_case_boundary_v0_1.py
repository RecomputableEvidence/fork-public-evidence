from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_fork_use_case_boundary.py"
EXAMPLES = ROOT / "examples" / "fork_use_cases"

spec = importlib.util.spec_from_file_location("check_fork_use_case_boundary", CHECKER)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


def validate_payload(payload: dict) -> tuple[bool, str, list[str]]:
    return checker.validate_record(payload)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_valid_template() -> dict:
    return load_json(EXAMPLES / "valid_audit_evidence_assembly_v0_1.json")


def test_cli_compact_valid_example_passes():
    proc = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / "valid_audit_evidence_assembly_v0_1.json"), "--compact"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    payload = json.loads(proc.stdout)
    assert proc.returncode == 0
    assert payload["result"]["ok"] is True
    assert payload["limitations"]["scope"] == "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"
    assert payload["limitations"]["automation_interpretation_required"] is True


def test_valid_examples_pass():
    for path in sorted(EXAMPLES.glob("valid_*.json")):
        ok, computed, findings = validate_payload(load_json(path))
        assert ok is True, (path.name, computed, findings)
        assert findings == []


def test_invalid_examples_fail():
    for path in sorted(EXAMPLES.glob("invalid_*.json")):
        ok, computed, findings = validate_payload(load_json(path))
        assert ok is False, path.name
        assert computed in {
            "EXPANSION_AUTHORITY_REF_MISSING",
            "NON_CLAIM_DROPPED",
            "MAPPING_INCOMPLETE",
            "BOUNDARY_EXPANSION_DETECTED",
            "POINTER_UNRESOLVED",
        }
        assert findings


def test_missing_required_root_field_fails():
    payload = load_valid_template()
    del payload["fork_role"]
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert "fork_role:INVALID" in findings


def test_declared_outcome_mismatch_fails():
    payload = load_valid_template()
    payload["downstream_consumption"]["unresolved_pointers"] = ["synthetic_registry.json#MISSING"]
    payload["boundary_result"]["outcome"] = "BOUNDARY_PRESERVED"
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert computed == "POINTER_UNRESOLVED"
    assert any("MISMATCH_DECLARED_BOUNDARY_PRESERVED_COMPUTED_POINTER_UNRESOLVED" in f for f in findings)


def test_non_claim_drop_computes_non_claim_dropped():
    payload = load_valid_template()
    dropped = payload["non_claims"][0]
    payload["downstream_consumption"]["preserved_non_claims"].remove(dropped)
    payload["downstream_consumption"]["dropped_non_claims"] = [dropped]
    payload["boundary_result"]["outcome"] = "NON_CLAIM_DROPPED"
    ok, computed, findings = validate_payload(payload)
    assert ok is True
    assert computed == "NON_CLAIM_DROPPED"
    assert findings == []


def test_mapping_incomplete_fails_when_non_claim_not_preserved_or_dropped():
    payload = load_valid_template()
    missing = payload["non_claims"][0]
    payload["downstream_consumption"]["preserved_non_claims"].remove(missing)
    payload["boundary_result"]["outcome"] = "BOUNDARY_PRESERVED"
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert computed == "MAPPING_INCOMPLETE"
    assert any("INCOMPLETE" in f for f in findings)


def test_expansion_claim_requires_authority_and_evidence():
    payload = load_valid_template()
    payload["downstream_consumption"]["consumer_added_claims"] = [
        {"claim": "The control is effective.", "authority_ref": "", "evidence_refs": []}
    ]
    payload["boundary_result"]["outcome"] = "BOUNDARY_EXPANSION_DETECTED"
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert computed == "EXPANSION_AUTHORITY_REF_MISSING"
    assert any("authority_ref:REQUIRED_FOR_EXPANSION" in f for f in findings)


def test_required_do_not_map_tokens_are_enforced():
    payload = load_valid_template()
    payload["limitations"]["do_not_map_to"] = ["APPROVAL"]
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert any("limitations.do_not_map_to:MISSING" in f for f in findings)


def test_healthcare_synthetic_field_requires_synthetic_true():
    payload = load_json(EXAMPLES / "valid_healthcare_prior_auth_synthetic_v0_1.json")
    payload["synthetic"] = False
    ok, computed, findings = validate_payload(payload)
    assert ok is False
    assert "synthetic:REQUIRED_TRUE_FOR_HEALTHCARE_PRIOR_AUTH_SYNTHETIC" in findings
