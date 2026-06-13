from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_definition_boundary.py"

VALID = ROOT / "examples" / "definition_boundary" / "valid_identity_undefined.json"
INVALID = ROOT / "examples" / "definition_boundary" / "invalid_identity_overdefinition.json"


def run_checker(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_identity_undefined_valid_passes() -> None:
    result = run_checker(VALID)
    assert result.returncode == 0, result.stderr
    assert "DEFINITION_BOUNDARY_PASS" in result.stdout


def test_forbidden_definitions_are_not_scanned() -> None:
    text = VALID.read_text(encoding="utf-8")
    assert "verified identity" in text
    assert "authorized reviewer" in text
    assert "meaningful human review" in text

    result = run_checker(VALID)
    assert result.returncode == 0, result.stderr


def test_identity_overdefinition_fails() -> None:
    result = run_checker(INVALID)
    assert result.returncode != 0
    assert "DEFINITION_EXPANSION_DEFECT" in result.stderr
