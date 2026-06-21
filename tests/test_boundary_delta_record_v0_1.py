from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_boundary_delta_record.py"
EXAMPLES = ROOT / "examples" / "boundary_delta_record"


def run_checker(filename: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / filename)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert completed.stdout, completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def test_valid_preserved_is_inspectable() -> None:
    code, result = run_checker("valid_preserved_v0_1.json")

    assert code == 0
    assert result["structural_outcome"] == "INSPECTABLE"
    assert result["derived"]["licensed_claim_surface"] == "SOURCE_SURFACE_PRESERVED"
    assert result["findings"] == []


def test_valid_loss_is_inspectable_and_distinct_from_suppression() -> None:
    code, result = run_checker("valid_loss_v0_1.json")

    assert code == 0
    assert result["structural_outcome"] == "INSPECTABLE"
    assert result["derived"]["evidence_reference_lost"] is True
    assert result["derived"]["evidence_reference_suppressed"] is False
    assert result["findings"] == []


def test_scoped_to_generalized_fails_closed() -> None:
    code, result = run_checker("invalid_scoped_to_generalized_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert result["derived"]["claim_scope_generalized"] is True
    assert result["derived"]["licensed_claim_surface"] == "UNLICENSED_EXPANSION_DETECTED"


def test_silence_to_claim_fails_closed() -> None:
    code, result = run_checker("invalid_silence_to_claim_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert result["derived"]["silence_converted_to_claim"] is True


def test_recomputation_to_truth_fails_closed() -> None:
    code, result = run_checker("invalid_recomputation_to_truth_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert result["derived"]["recomputation_status_converted_to_truth"] is True


def test_reference_suppression_fails_closed_and_is_not_loss() -> None:
    code, result = run_checker("invalid_reference_suppression_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert result["derived"]["evidence_reference_suppressed"] is True
    assert result["derived"]["evidence_reference_lost"] is False
    assert result["derived"]["licensed_claim_surface"] == "REFERENCE_SUPPRESSED_AT_BOUNDARY"


def test_unknown_transition_kind_fails_closed() -> None:
    code, result = run_checker("invalid_unknown_transition_kind_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "UNKNOWN_TRANSITION_KIND" for item in result["findings"])


def test_unknown_transformation_rule_fails_closed() -> None:
    code, result = run_checker("invalid_unknown_transformation_rule_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "UNKNOWN_TRANSFORMATION_RULE" for item in result["findings"])


def test_true_flag_without_supporting_transition_fails_closed() -> None:
    code, result = run_checker("invalid_naked_boolean_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "DERIVED_FLAG_WITHOUT_SUPPORTING_TRANSITION" for item in result["findings"])


def test_licensed_surface_mismatch_fails_closed() -> None:
    code, result = run_checker("invalid_licensed_surface_mismatch_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "LICENSED_CLAIM_SURFACE_MISMATCH" for item in result["findings"])


def test_prohibited_scoring_fails_closed() -> None:
    code, result = run_checker("invalid_prohibited_scoring_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "PROHIBITED_KEY" for item in result["findings"])


def test_checker_output_is_deterministic() -> None:
    first = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / "valid_preserved_v0_1.json")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    second = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / "valid_preserved_v0_1.json")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert first.stdout == second.stdout

def test_transition_kind_rule_mismatch_fails_closed() -> None:
    code, result = run_checker("invalid_transition_kind_rule_mismatch_v0_1.json")

    assert code == 1
    assert result["structural_outcome"] == "NOT_INSPECTABLE"
    assert any(item["code"] == "TRANSITION_KIND_RULE_MISMATCH" for item in result["findings"])
