import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_recomputability_class.py"

VALID_STRONG = REPO_ROOT / "examples" / "recomputability_class" / "valid_strong_satisfies_strong_gate.json"
VALID_NON_RECOMPUTABLE = REPO_ROOT / "examples" / "recomputability_class" / "valid_non_recomputable_occurrence_gate.json"
INVALID_NON_RECOMPUTABLE_STRONG = REPO_ROOT / "examples" / "recomputability_class" / "invalid_non_recomputable_satisfies_strong_gate.json"


def run_checker(path: Path):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )


def test_valid_strong_satisfies_strong_gate_passes():
    result = run_checker(VALID_STRONG)

    assert result.returncode == 0
    assert "RECOMPUTABILITY_CLASS_PASS" in result.stdout


def test_valid_non_recomputable_occurrence_gate_passes():
    result = run_checker(VALID_NON_RECOMPUTABLE)

    assert result.returncode == 0
    assert "RECOMPUTABILITY_CLASS_PASS" in result.stdout


def test_non_recomputable_must_not_satisfy_strong_gate():
    result = run_checker(INVALID_NON_RECOMPUTABLE_STRONG)

    assert result.returncode != 0
    assert "RECOMPUTABILITY_ESCALATION_DEFECT" in result.stdout
    assert "NON_RECOMPUTABLE artifacts must not satisfy gates that require STRONG_RECOMPUTATION" in result.stdout
