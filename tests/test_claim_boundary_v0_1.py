from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_claim_boundary.py"
VALID = ROOT / "examples" / "claim_boundary" / "valid_integrity_only.json"
INVALID = ROOT / "examples" / "claim_boundary" / "invalid_overclaim_compliance.json"


def run_checker(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_valid_integrity_only_payload_passes() -> None:
    result = run_checker(VALID)

    assert result.returncode == 0, result.stderr
    assert "CLAIM_BOUNDARY_PASS" in result.stdout


def test_invalid_overclaim_compliance_payload_fails() -> None:
    result = run_checker(INVALID)

    assert result.returncode != 0
    assert "CLAIM_EXPANSION_DEFECT" in result.stderr
    assert (
        "compliant" in result.stderr.lower()
        or "lawful" in result.stderr.lower()
        or "correct" in result.stderr.lower()
        or "admissible" in result.stderr.lower()
    )