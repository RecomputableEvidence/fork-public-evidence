import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_required_source_non_claims_v0_1.py"
EXAMPLES = ROOT / "examples" / "required_source_non_claims_v0_1"


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_valid_required_source_non_claims_pass():
    proc = run_checker("valid_required_source_non_claims.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_missing_source_truth_non_claim_fails():
    proc = run_checker("invalid_missing_source_truth_not_claimed.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "MISSING_REQUIRED_SOURCE_NON_CLAIM"
        and "SOURCE_TRUTH_NOT_CLAIMED" in e["message"]
        for e in out["errors"]
    )


def test_duplicate_non_claim_id_fails():
    proc = run_checker("invalid_duplicate_non_claim_id.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "DUPLICATE_NON_CLAIM_ID" for e in out["errors"])


def test_empty_non_claim_statement_fails():
    proc = run_checker("invalid_empty_statement.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "EMPTY_NON_CLAIM_STATEMENT" for e in out["errors"])


def test_source_truth_assertion_fails_even_with_required_bundle():
    proc = run_checker("invalid_source_truth_assertion.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "SOURCE_TRUTH_ASSERTED" for e in out["errors"])


def test_checker_emits_non_claims():
    proc = run_checker("valid_required_source_non_claims.json")
    assert proc.returncode == 0
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "does not verify SOURCE_TRUTH" in joined
    assert "does not confirm factual basis" in joined
    assert "inference constraints" in joined