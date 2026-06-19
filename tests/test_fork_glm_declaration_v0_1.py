import json
import subprocess
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".well-known" / "governance-layer-manifest.json"
MIRROR = ROOT / "glm" / "fork_governance_layer_manifest_v0_1.json"
SCHEMA = ROOT / "schemas" / "fork_glm_declaration_v0_1.schema.json"
CHECKER = ROOT / "tools" / "check_fork_glm_declaration.py"

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def run_checker() -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), str(MANIFEST)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.stdout.strip(), completed.stderr
    return completed.returncode, json.loads(completed.stdout)

def test_schema_is_valid_draft7() -> None:
    jsonschema.Draft7Validator.check_schema(load_json(SCHEMA))

def test_manifest_validates_against_schema() -> None:
    schema = load_json(SCHEMA)
    manifest = load_json(MANIFEST)
    jsonschema.Draft7Validator(schema).validate(manifest)

def test_manifest_and_mirror_match() -> None:
    assert load_json(MANIFEST) == load_json(MIRROR)

def test_checker_records_structural_conformance() -> None:
    code, payload = run_checker()
    assert code == 0
    assert payload["actionability"] == "NON_ACTIONABLE_STRUCTURAL_DECLARATION_ONLY"
    assert payload["result"] == {
        "result_kind": "STRUCTURAL_CONFORMANCE_RECORDED",
        "safe_to_automate": False,
        "requires_human_interpretation_before_any_automation": True,
    }
    assert payload["errors"] == []

def test_manifest_declares_required_non_claims_and_forbidden_interpretations() -> None:
    manifest = load_json(MANIFEST)
    non_claims = set(manifest["claims_boundary"]["explicit_non_claims"])
    forbidden = set(manifest["claims_boundary"]["forbidden_interpretations"])

    for item in [
        "does_not_claim_approval",
        "does_not_claim_truth",
        "does_not_claim_safety",
        "does_not_claim_compliance",
        "does_not_claim_legal_sufficiency",
        "does_not_claim_risk_acceptance",
        "does_not_claim_deployment_readiness",
        "does_not_claim_institutional_authority",
    ]:
        assert item in non_claims

    for item in [
        "approval_status",
        "truth_validation",
        "safety_validation",
        "compliance_certification",
        "authority_transfer",
        "claim_expansion_without_new_authority",
        "ci_cd_blocking_gate",
        "host_native_scoring_input",
        "dashboard_assurance_signal",
        "human_prose_green_signal",
    ]:
        assert item in forbidden

def test_no_pass_fail_or_ok_oracle_in_checker_output() -> None:
    _code, payload = run_checker()
    rendered = json.dumps(payload, sort_keys=True)
    assert "STRUCTURAL_PASS" not in rendered
    assert '"ok"' not in rendered
    assert "APPROVED" not in rendered
    assert "COMPLIANT" not in rendered
