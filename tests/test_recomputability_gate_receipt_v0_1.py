import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.check_recomputability_gate_receipt import validate_receipt

EXAMPLES = ROOT / "examples" / "recomputability_gate_receipt"
TOOL = ROOT / "tools" / "check_recomputability_gate_receipt.py"

def load(name):
    with (EXAMPLES / name).open("r", encoding="utf-8") as f:
        return json.load(f)

def test_strong_recomputation_satisfies_strong_gate_receipt():
    receipt = load("valid_strong_satisfies_strong_gate_receipt.json")
    assert validate_receipt(receipt) == []
    assert receipt["gate_result"] == "PASS"

def test_non_recomputable_satisfies_occurrence_gate_receipt():
    receipt = load("valid_non_recomputable_occurrence_gate_receipt.json")
    assert validate_receipt(receipt) == []
    assert receipt["gate_result"] == "PASS"

def test_non_recomputable_strong_gate_refusal_receipt():
    receipt = load("valid_non_recomputable_strong_gate_refusal_receipt.json")
    assert validate_receipt(receipt) == []
    assert receipt["gate_result"] == "FAIL"
    assert receipt["reason_code"] == "RECOMPUTABILITY_ESCALATION_DEFECT"
    assert receipt["artifact_recomputability_class"] == "NON_RECOMPUTABLE"
    assert receipt["gate_required_class"] == "STRONG_RECOMPUTATION"

def test_missing_artifact_class_is_rejected():
    errors = validate_receipt(load("invalid_missing_artifact_recomputability_class.json"))
    assert "MISSING_REQUIRED_FIELD: artifact_recomputability_class" in errors

def test_missing_gate_required_class_is_rejected():
    errors = validate_receipt(load("invalid_missing_gate_required_class.json"))
    assert "MISSING_REQUIRED_FIELD: gate_required_class" in errors

def test_fail_missing_reason_code_is_rejected():
    errors = validate_receipt(load("invalid_fail_missing_reason_code.json"))
    assert "MISSING_REQUIRED_FIELD: reason_code" in errors

def test_unsupported_gate_result_is_rejected():
    errors = validate_receipt(load("invalid_unsupported_gate_result.json"))
    assert "UNSUPPORTED_GATE_RESULT: NOT_CHECKED" in errors

def test_bare_pass_without_class_comparison_is_rejected():
    errors = validate_receipt(load("invalid_bare_pass_without_class_comparison.json"))
    assert "MISSING_REQUIRED_FIELD: artifact_recomputability_class" in errors
    assert "MISSING_REQUIRED_FIELD: gate_required_class" in errors

def test_non_recomputable_cannot_false_pass_strong_gate():
    errors = validate_receipt(load("invalid_non_recomputable_strong_gate_false_pass.json"))
    assert any("RECOMPUTABILITY_ESCALATION_DEFECT" in error for error in errors)

def test_cli_accepts_refusal_receipt_as_valid_bound_fail():
    result = subprocess.run(
        [sys.executable, str(TOOL), str(EXAMPLES / "valid_non_recomputable_strong_gate_refusal_receipt.json")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "RECOMPUTABILITY_GATE_RECEIPT_OK" in result.stdout
    assert "RECOMPUTABILITY_ESCALATION_DEFECT" in result.stdout

def test_cli_rejects_false_pass():
    result = subprocess.run(
        [sys.executable, str(TOOL), str(EXAMPLES / "invalid_non_recomputable_strong_gate_false_pass.json")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "RECOMPUTABILITY_ESCALATION_DEFECT" in result.stdout
