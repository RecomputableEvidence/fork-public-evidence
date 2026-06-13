from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_provenance_tier.py"

VALID = ROOT / "examples" / "provenance_tier" / "valid_documented_source.json"
INVALID_GENERATED = (
    ROOT
    / "examples"
    / "provenance_tier"
    / "invalid_generated_satisfies_documented.json"
)
INVALID_DEPENDENCY = (
    ROOT
    / "examples"
    / "provenance_tier"
    / "invalid_documented_depends_on_generated.json"
)


def run_checker(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_valid_documented_source_passes() -> None:
    result = run_checker(VALID)
    assert result.returncode == 0, result.stderr
    assert "PROVENANCE_TIER_PASS" in result.stdout


def test_generated_cannot_satisfy_documented() -> None:
    result = run_checker(INVALID_GENERATED)
    assert result.returncode != 0
    assert "PROVENANCE_ESCALATION_DEFECT" in result.stderr


def test_documented_must_not_depend_on_generated() -> None:
    result = run_checker(INVALID_DEPENDENCY)
    assert result.returncode != 0
    assert "PROVENANCE_DEPENDENCY_CONTAMINATION" in result.stderr
