import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_required_source_non_claim_graph_preservation_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_graph_preservation_v0_1"


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_new_claim_cannot_use_rgv_pass_as_sole_evidence_for_source_truth():
    proc = run_checker("invalid_new_claim_rgv_pass_sole_evidence_source_truth.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "FORK_PASS_SOLE_EVIDENCE_FOR_PROHIBITED_EXPANSION" for e in out["errors"])


def test_new_claim_cannot_use_rgv_pass_as_authority_basis():
    proc = run_checker("invalid_new_claim_rgv_pass_as_authority.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "FORK_PASS_USED_AS_EXPANSION_AUTHORITY" for e in out["errors"])


def test_structured_metadata_alias_factual_status_fails():
    proc = run_checker("invalid_metadata_alias_factual_status_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "STRUCTURAL_METADATA_CONTRADICTION" for e in out["errors"])


def test_structured_metadata_alias_legal_clearance_fails():
    proc = run_checker("invalid_metadata_alias_legal_clearance_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "STRUCTURAL_METADATA_CONTRADICTION" for e in out["errors"])


def test_indeterminate_cannot_be_used_as_verified_truth_support():
    proc = run_checker("invalid_indeterminate_used_as_verified_truth_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "INDETERMINATE_USED_AS_PROHIBITED_SUPPORT" for e in out["errors"])


def test_fail_cannot_be_treated_as_source_false():
    proc = run_checker("invalid_fail_treated_as_source_false_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "FAIL_TREATED_AS_LEGAL_OR_FACTUAL_DETERMINATION" for e in out["errors"])


def test_fail_cannot_be_treated_as_unlawful():
    proc = run_checker("invalid_fail_treated_as_unlawful_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "FAIL_TREATED_AS_LEGAL_OR_FACTUAL_DETERMINATION" for e in out["errors"])


def test_expansion_with_external_authority_and_external_evidence_passes():
    proc = run_checker("valid_expansion_with_external_authority_and_fork_reference_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_checker_reports_structural_alias_scope_not_nlp():
    proc = run_checker("valid_expansion_with_external_authority_and_fork_reference_graph.json")
    assert proc.returncode == 0
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "structural alias checks" in joined
    assert "does not perform NLP" in joined