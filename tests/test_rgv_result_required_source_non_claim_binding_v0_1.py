import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_result_required_source_non_claim_binding_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_result_binding_v0_1"


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_valid_pass_result_with_required_source_non_claims_passes():
    proc = run_checker("valid_pass_result_with_required_source_non_claims.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_pass_missing_required_source_non_claim_fails():
    proc = run_checker("invalid_pass_missing_source_truth_not_claimed.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "MISSING_REQUIRED_SOURCE_NON_CLAIM_ON_PASS"
        and "SOURCE_TRUTH_NOT_CLAIMED" in e["message"]
        for e in out["errors"]
    )


def test_pass_duplicate_required_non_claim_fails():
    proc = run_checker("invalid_pass_duplicate_required_non_claim.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "DUPLICATE_REQUIRED_NON_CLAIM_ID" for e in out["errors"])


def test_pass_empty_required_non_claim_statement_fails():
    proc = run_checker("invalid_pass_empty_required_non_claim_statement.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "EMPTY_REQUIRED_NON_CLAIM_STATEMENT" for e in out["errors"])


def test_pass_source_truth_assertion_fails():
    proc = run_checker("invalid_pass_source_truth_asserted.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "SOURCE_TRUTH_ASSERTED" for e in out["errors"])


def test_pass_source_truth_scope_fails():
    proc = run_checker("invalid_pass_source_truth_scope.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "PROHIBITED_VERIFICATION_SCOPE" for e in out["errors"])


def test_fail_result_without_required_source_non_claims_passes_binding_checker():
    proc = run_checker("valid_fail_result_without_required_source_non_claims.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_checker_emits_binding_non_claims():
    proc = run_checker("valid_pass_result_with_required_source_non_claims.json")
    assert proc.returncode == 0
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "does not verify SOURCE_TRUTH" in joined
    assert "does not confirm factual basis" in joined
    assert "without modifying the v0.4 evidentiary-weight profile contract" in joined