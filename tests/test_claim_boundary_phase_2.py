from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_artifact_claim_boundary.py"

VALID = ROOT / "examples" / "claim_boundary_artifacts" / "valid_receipt_with_claim_boundary.json"
MISSING = ROOT / "examples" / "claim_boundary_artifacts" / "invalid_receipt_missing_claim_boundary.json"
OVERCLAIM = ROOT / "examples" / "claim_boundary_artifacts" / "invalid_release_metadata_overclaim.json"


def run_checker(*paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), *[str(path) for path in paths]],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_artifact_with_valid_claim_boundary_passes() -> None:
    result = run_checker(VALID)

    assert result.returncode == 0, result.stderr
    assert "ARTIFACT_CLAIM_BOUNDARY_PASS" in result.stdout


def test_artifact_missing_claim_boundary_fails() -> None:
    result = run_checker(MISSING)

    assert result.returncode != 0
    assert "CLAIM_BOUNDARY_BLOCK_MISSING" in result.stderr


def test_artifact_with_overclaiming_claim_boundary_fails() -> None:
    result = run_checker(OVERCLAIM)

    assert result.returncode != 0
    assert "CLAIM_EXPANSION_DEFECT" in result.stderr
    assert (
        "compliant" in result.stderr.lower()
        or "lawful" in result.stderr.lower()
        or "admissible" in result.stderr.lower()
        or "complete" in result.stderr.lower()
    )


def test_mixed_artifact_set_fails_if_any_artifact_fails() -> None:
    result = run_checker(VALID, MISSING)

    assert result.returncode != 0
    assert "ARTIFACT_CLAIM_BOUNDARY_PASS" in result.stdout
    assert "CLAIM_BOUNDARY_BLOCK_MISSING" in result.stderr