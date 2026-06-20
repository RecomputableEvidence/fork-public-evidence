from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_fork_use_case_boundary.py"
EXAMPLES = ROOT / "examples" / "fork_use_cases"
SCHEMA = ROOT / "schemas" / "fork_use_case_boundary_v0_1.schema.json"

_spec = importlib.util.spec_from_file_location("check_fork_use_case_boundary", CHECKER)
assert _spec is not None and _spec.loader is not None
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)

PRESERVED_VALID_EXAMPLES = {
    "valid_audit_evidence_assembly_v0_1.json",
    "valid_cyber_triage_boundary_v0_1.json",
    "valid_healthcare_prior_auth_synthetic_v0_1.json",
}

ADVERSE_VALID_EXAMPLES = {
    "valid_ai_benchmark_pointer_unresolved_v0_1.json",
    "valid_vendor_risk_boundary_expansion_v0_1.json",
    "valid_non_claim_dropped_v0_1.json",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checker(path: Path) -> tuple[int, dict[str, Any]]:
    record = read_json(path)
    ok, computed, findings = checker.validate_record(record)
    declared = record.get("boundary_result", {}).get("outcome") if isinstance(record.get("boundary_result"), dict) else None
    output = checker.build_output(path, ok, declared, computed, findings)
    return (0 if ok else 1), output


def load_valid_template() -> dict[str, Any]:
    return read_json(EXAMPLES / "valid_audit_evidence_assembly_v0_1.json")


def write_tmp(tmp_path: Path, payload: dict[str, Any], name: str = "case.json") -> Path:
    path = tmp_path / name
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def test_cli_smoke_emits_compact_json():
    path = EXAMPLES / "valid_audit_evidence_assembly_v0_1.json"
    proc = subprocess.run(
        [sys.executable, str(CHECKER), str(path), "--compact"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["result"]["ok"] is True
    assert payload["result"]["boundary_preserved"] is True


def test_valid_examples_pass_with_explicit_interpretation_fields():
    for path in sorted(EXAMPLES.glob("valid_*.json")):
        code, payload = run_checker(path)
        assert code == 0, path.name
        assert payload["result"]["ok"] is True
        assert "boundary_preserved" in payload["result"]
        assert "outcome_requires_review" in payload["result"]
        assert "review_reason" in payload["result"]
        assert "result_semantics" in payload["result"]
        assert payload["limitations"]["scope"] == "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"
        assert payload["limitations"]["automation_interpretation_required"] is True
        assert payload["limitations"]["checker_semantics_version"] == "v0.1.1"


def test_preserved_valid_examples_are_machine_readable_preserved():
    for name in sorted(PRESERVED_VALID_EXAMPLES):
        code, payload = run_checker(EXAMPLES / name)
        assert code == 0, name
        assert payload["result"]["ok"] is True
        assert payload["result"]["computed_outcome"] == "BOUNDARY_PRESERVED"
        assert payload["result"]["boundary_preserved"] is True
        assert payload["result"]["outcome_requires_review"] is False
        assert payload["result"]["review_reason"] == "BOUNDARY_STRUCTURALLY_PRESERVED"


def test_valid_adverse_examples_are_interpretable_but_not_boundary_preserved():
    for name in sorted(ADVERSE_VALID_EXAMPLES):
        code, payload = run_checker(EXAMPLES / name)
        assert code == 0, name
        assert payload["result"]["ok"] is True
        assert payload["result"]["computed_outcome"] != "BOUNDARY_PRESERVED"
        assert payload["result"]["boundary_preserved"] is False
        assert payload["result"]["outcome_requires_review"] is True
        assert payload["result"]["review_reason"].endswith("REQUIRES_REVIEW")


def test_invalid_examples_fail():
    for path in sorted(EXAMPLES.glob("invalid_*.json")):
        code, payload = run_checker(path)
        assert code == 1, path.name
        assert payload["result"]["ok"] is False
        assert payload["result"]["boundary_preserved"] is False
        assert payload["result"]["findings"]


def test_missing_required_root_field_fails(tmp_path: Path):
    payload = load_valid_template()
    del payload["fork_role"]
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert "fork_role:INVALID" in out["result"]["findings"]
    assert out["result"]["boundary_preserved"] is False


def test_declared_outcome_mismatch_fails(tmp_path: Path):
    payload = load_valid_template()
    payload["downstream_consumption"]["unresolved_pointers"] = ["synthetic_registry.json#MISSING"]
    payload["boundary_result"]["outcome"] = "BOUNDARY_PRESERVED"
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert out["result"]["computed_outcome"] == "POINTER_UNRESOLVED"
    assert out["result"]["outcome_requires_review"] is True
    assert any("MISMATCH_DECLARED_BOUNDARY_PRESERVED_COMPUTED_POINTER_UNRESOLVED" in f for f in out["result"]["findings"])


def test_non_claim_drop_computes_non_claim_dropped(tmp_path: Path):
    payload = load_valid_template()
    dropped = payload["non_claims"][0]
    payload["downstream_consumption"]["preserved_non_claims"].remove(dropped)
    payload["downstream_consumption"]["dropped_non_claims"] = [dropped]
    payload["boundary_result"]["outcome"] = "NON_CLAIM_DROPPED"
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 0
    assert out["result"]["ok"] is True
    assert out["result"]["computed_outcome"] == "NON_CLAIM_DROPPED"
    assert out["result"]["boundary_preserved"] is False
    assert out["result"]["outcome_requires_review"] is True


def test_mapping_incomplete_fails_when_non_claim_not_preserved_or_dropped(tmp_path: Path):
    payload = load_valid_template()
    missing = payload["non_claims"][0]
    payload["downstream_consumption"]["preserved_non_claims"].remove(missing)
    payload["boundary_result"]["outcome"] = "BOUNDARY_PRESERVED"
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert out["result"]["computed_outcome"] == "MAPPING_INCOMPLETE"
    assert out["result"]["outcome_requires_review"] is True
    assert any("INCOMPLETE" in f for f in out["result"]["findings"])


def test_expansion_claim_requires_authority_and_evidence(tmp_path: Path):
    payload = load_valid_template()
    payload["downstream_consumption"]["consumer_added_claims"] = [
        {"claim": "The control is effective.", "authority_ref": "", "evidence_refs": []}
    ]
    payload["boundary_result"]["outcome"] = "BOUNDARY_EXPANSION_DETECTED"
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert out["result"]["computed_outcome"] == "EXPANSION_AUTHORITY_REF_MISSING"
    assert out["result"]["review_reason"] == "EXPANSION_POINTER_DEFECT_REQUIRES_REVIEW"
    assert any("authority_ref:REQUIRED_FOR_EXPANSION" in f for f in out["result"]["findings"])


def test_required_do_not_map_tokens_are_enforced(tmp_path: Path):
    payload = load_valid_template()
    payload["limitations"]["do_not_map_to"] = ["APPROVAL"]
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert any("limitations.do_not_map_to:MISSING" in f for f in out["result"]["findings"])


def test_healthcare_synthetic_field_requires_synthetic_true(tmp_path: Path):
    payload = read_json(EXAMPLES / "valid_healthcare_prior_auth_synthetic_v0_1.json")
    payload["synthetic"] = False
    path = write_tmp(tmp_path, payload)
    code, out = run_checker(path)
    assert code == 1
    assert "synthetic:REQUIRED_TRUE_FOR_HEALTHCARE_PRIOR_AUTH_SYNTHETIC" in out["result"]["findings"]


def test_invalid_authority_ref_empty_string_fixture_is_rejected():
    code, out = run_checker(EXAMPLES / "invalid_authority_ref_empty_string_v0_1.json")
    assert code == 1
    assert out["result"]["computed_outcome"] == "EXPANSION_AUTHORITY_REF_MISSING"
    assert any("authority_ref:REQUIRED_FOR_EXPANSION" in f for f in out["result"]["findings"])
    assert any("evidence_refs:REQUIRED_FOR_EXPANSION" in f for f in out["result"]["findings"])


def test_compound_drop_and_unresolved_uses_priority_ordering():
    code, out = run_checker(EXAMPLES / "invalid_compound_drop_and_unresolved_v0_1.json")
    assert code == 1
    assert out["result"]["computed_outcome"] == "NON_CLAIM_DROPPED"
    assert out["result"]["review_reason"] == "NON_CLAIM_DROP_REQUIRES_REVIEW"
    assert any("MISMATCH_DECLARED_BOUNDARY_PRESERVED_COMPUTED_NON_CLAIM_DROPPED" in f for f in out["result"]["findings"])


def test_wrong_structural_scope_is_rejected():
    code, out = run_checker(EXAMPLES / "invalid_scope_wrong_v0_1.json")
    assert code == 1
    assert "boundary_result.structural_verification_scope:INVALID" in out["result"]["findings"]


def test_schema_hardens_consumer_added_claim_authority_and_evidence_refs():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    consumer_added = schema["properties"]["downstream_consumption"]["properties"]["consumer_added_claims"]
    props = consumer_added["items"]["properties"]
    assert props["authority_ref"]["minLength"] == 1
    assert props["evidence_refs"]["minItems"] == 1


def test_result_semantics_do_not_contain_positive_acceptance_language():
    code, out = run_checker(EXAMPLES / "valid_vendor_risk_boundary_expansion_v0_1.json")
    assert code == 0
    text = out["result"]["result_semantics"].lower()
    for prohibited in ["means approved", "means compliant", "means safe", "means sufficient", "means accepted"]:
        assert prohibited not in text