import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_evidentiary_weight_profile_v0_4.py"
EXAMPLES = ROOT / "examples" / "rgv_evidentiary_weight_profile_v0_4"


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_valid_profile_passes():
    proc = run_checker("valid_profile.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_missing_canonicalization_profile_fails():
    proc = run_checker("invalid_missing_canonicalization_profile.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "MISSING_REQUIRED_FIELD" for e in out["errors"])


def test_verifier_version_not_in_sealed_scope_fails():
    proc = run_checker("invalid_verifier_version_not_in_sealed_scope.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "VERIFIER_VERSION_NOT_IN_SEALED_SCOPE" for e in out["errors"])


def test_missing_seal_algorithm_fails():
    proc = run_checker("invalid_missing_seal_algorithm.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "INVALID_OR_MISSING_SEAL_ALGORITHM" for e in out["errors"])


def test_provenance_rollup_laundering_fails():
    proc = run_checker("invalid_provenance_rollup_laundering.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "PROVENANCE_ROLLUP_LAUNDERING" for e in out["errors"])


def test_checker_emits_non_claims():
    proc = run_checker("valid_profile.json")
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "legal sufficiency" in joined
    assert "business-records status" in joined
    assert "RFC8785/JCS implementation conformance" in joined
