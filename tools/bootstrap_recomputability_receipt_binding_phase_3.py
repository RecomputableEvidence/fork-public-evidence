from pathlib import Path
import json
import textwrap

ROOT = Path.cwd()

def write_text(path, content):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8", newline="\n")

def write_json(path, obj):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://fork.example/schemas/recomputability_gate_receipt_v0_1.schema.json",
  "title": "Fork Recomputability Gate Receipt v0.1",
  "type": "object",
  "additionalProperties": False,
  "required": [
    "receipt_type",
    "receipt_version",
    "artifact_recomputability_class",
    "gate_required_class",
    "gate_result",
    "reason_code",
    "claim_boundary"
  ],
  "properties": {
    "receipt_type": {
      "const": "RECOMPUTABILITY_GATE_RECEIPT"
    },
    "receipt_version": {
      "const": "0.1"
    },
    "artifact_recomputability_class": {
      "enum": [
        "NON_RECOMPUTABLE",
        "STRONG_RECOMPUTATION"
      ]
    },
    "gate_required_class": {
      "enum": [
        "OCCURRENCE_EVIDENCE",
        "STRONG_RECOMPUTATION"
      ]
    },
    "gate_result": {
      "enum": [
        "PASS",
        "FAIL"
      ]
    },
    "reason_code": {
      "type": "string",
      "minLength": 1
    },
    "claim_boundary": {
      "type": "string",
      "minLength": 1
    }
  }
}

write_json("schemas/recomputability_gate_receipt_v0_1.schema.json", schema)

base_boundary = "No recomputability gate result may be emitted without exposing the class comparison that produced it."
escalation_boundary = "NON_RECOMPUTABLE artifacts must not satisfy gates requiring STRONG_RECOMPUTATION."

write_json("examples/recomputability_gate_receipt/valid_strong_satisfies_strong_gate_receipt.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "STRONG_RECOMPUTATION",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "PASS",
  "reason_code": "STRONG_RECOMPUTATION_SATISFIES_STRONG_GATE",
  "claim_boundary": base_boundary
})

write_json("examples/recomputability_gate_receipt/valid_non_recomputable_occurrence_gate_receipt.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_required_class": "OCCURRENCE_EVIDENCE",
  "gate_result": "PASS",
  "reason_code": "NON_RECOMPUTABLE_SATISFIES_OCCURRENCE_GATE_ONLY",
  "claim_boundary": "NON_RECOMPUTABLE evidence may support occurrence-level gates but not gates requiring STRONG_RECOMPUTATION."
})

write_json("examples/recomputability_gate_receipt/valid_non_recomputable_strong_gate_refusal_receipt.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "FAIL",
  "reason_code": "RECOMPUTABILITY_ESCALATION_DEFECT",
  "claim_boundary": escalation_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_missing_artifact_recomputability_class.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "FAIL",
  "reason_code": "RECOMPUTABILITY_ESCALATION_DEFECT",
  "claim_boundary": escalation_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_missing_gate_required_class.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_result": "FAIL",
  "reason_code": "RECOMPUTABILITY_ESCALATION_DEFECT",
  "claim_boundary": escalation_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_fail_missing_reason_code.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "FAIL",
  "claim_boundary": escalation_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_unsupported_gate_result.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "NOT_CHECKED",
  "reason_code": "RECOMPUTABILITY_ESCALATION_DEFECT",
  "claim_boundary": escalation_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_bare_pass_without_class_comparison.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "gate_result": "PASS",
  "reason_code": "BARE_PASS_NOT_ALLOWED",
  "claim_boundary": base_boundary
})

write_json("examples/recomputability_gate_receipt/invalid_non_recomputable_strong_gate_false_pass.json", {
  "receipt_type": "RECOMPUTABILITY_GATE_RECEIPT",
  "receipt_version": "0.1",
  "artifact_recomputability_class": "NON_RECOMPUTABLE",
  "gate_required_class": "STRONG_RECOMPUTATION",
  "gate_result": "PASS",
  "reason_code": "BARE_PASS_NOT_ALLOWED",
  "claim_boundary": base_boundary
})

write_text("tools/check_recomputability_gate_receipt.py", r'''
import json
import sys
from pathlib import Path

RECEIPT_TYPE = "RECOMPUTABILITY_GATE_RECEIPT"
RECEIPT_VERSION = "0.1"

ARTIFACT_CLASSES = {
    "NON_RECOMPUTABLE",
    "STRONG_RECOMPUTATION",
}

GATE_REQUIRED_CLASSES = {
    "OCCURRENCE_EVIDENCE",
    "STRONG_RECOMPUTATION",
}

GATE_RESULTS = {
    "PASS",
    "FAIL",
}

REQUIRED_FIELDS = [
    "receipt_type",
    "receipt_version",
    "artifact_recomputability_class",
    "gate_required_class",
    "gate_result",
    "reason_code",
    "claim_boundary",
]

ESCALATION_REASON = "RECOMPUTABILITY_ESCALATION_DEFECT"
ESCALATION_BOUNDARY = "NON_RECOMPUTABLE artifacts must not satisfy gates requiring STRONG_RECOMPUTATION."

def load_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)

def validate_receipt(receipt):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in receipt:
            errors.append(f"MISSING_REQUIRED_FIELD: {field}")

    if errors:
        return errors

    if receipt["receipt_type"] != RECEIPT_TYPE:
        errors.append("INVALID_RECEIPT_TYPE")

    if receipt["receipt_version"] != RECEIPT_VERSION:
        errors.append("INVALID_RECEIPT_VERSION")

    artifact_class = receipt["artifact_recomputability_class"]
    gate_required = receipt["gate_required_class"]
    gate_result = receipt["gate_result"]
    reason_code = receipt["reason_code"]
    claim_boundary = receipt["claim_boundary"]

    if artifact_class not in ARTIFACT_CLASSES:
        errors.append(f"UNSUPPORTED_ARTIFACT_RECOMPUTABILITY_CLASS: {artifact_class}")

    if gate_required not in GATE_REQUIRED_CLASSES:
        errors.append(f"UNSUPPORTED_GATE_REQUIRED_CLASS: {gate_required}")

    if gate_result not in GATE_RESULTS:
        errors.append(f"UNSUPPORTED_GATE_RESULT: {gate_result}")

    if not isinstance(reason_code, str) or not reason_code:
        errors.append("MISSING_REASON_CODE")

    if not isinstance(claim_boundary, str) or not claim_boundary:
        errors.append("MISSING_CLAIM_BOUNDARY")

    if errors:
        return errors

    if artifact_class == "NON_RECOMPUTABLE" and gate_required == "STRONG_RECOMPUTATION":
        if gate_result != "FAIL":
            errors.append("RECOMPUTABILITY_ESCALATION_DEFECT: NON_RECOMPUTABLE artifacts must fail gates requiring STRONG_RECOMPUTATION.")
        if reason_code != ESCALATION_REASON:
            errors.append("MISSING_ESCALATION_REASON_CODE")
        if claim_boundary != ESCALATION_BOUNDARY:
            errors.append("MISSING_ESCALATION_CLAIM_BOUNDARY")

    elif artifact_class == "NON_RECOMPUTABLE" and gate_required == "OCCURRENCE_EVIDENCE":
        if gate_result != "PASS":
            errors.append("INVALID_OCCURRENCE_GATE_RESULT")
        if reason_code != "NON_RECOMPUTABLE_SATISFIES_OCCURRENCE_GATE_ONLY":
            errors.append("INVALID_OCCURRENCE_GATE_REASON_CODE")

    elif artifact_class == "STRONG_RECOMPUTATION" and gate_required == "STRONG_RECOMPUTATION":
        if gate_result != "PASS":
            errors.append("INVALID_STRONG_GATE_RESULT")
        if reason_code != "STRONG_RECOMPUTATION_SATISFIES_STRONG_GATE":
            errors.append("INVALID_STRONG_GATE_REASON_CODE")

    elif artifact_class == "STRONG_RECOMPUTATION" and gate_required == "OCCURRENCE_EVIDENCE":
        if gate_result != "PASS":
            errors.append("INVALID_STRONG_ARTIFACT_OCCURRENCE_GATE_RESULT")

    return errors

def main(argv):
    if len(argv) != 2:
        print("Usage: python tools/check_recomputability_gate_receipt.py <receipt.json>", file=sys.stderr)
        return 2

    path = argv[1]
    try:
        receipt = load_json(path)
    except Exception as exc:
        print(f"RECOMPUTABILITY_GATE_RECEIPT_PARSE_ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_receipt(receipt)
    if errors:
        for error in errors:
            print(error)
        return 1

    print(
        "RECOMPUTABILITY_GATE_RECEIPT_OK: "
        f"{receipt['artifact_recomputability_class']} -> "
        f"{receipt['gate_required_class']} = "
        f"{receipt['gate_result']} "
        f"({receipt['reason_code']})"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
''')

write_text("tests/test_recomputability_gate_receipt_v0_1.py", r'''
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
''')

write_text("docs/RECOMPUTABILITY_RECEIPT_BINDING_v0_1.md", '''
# Recomputability Receipt Binding v0.1

## Purpose

This document defines the v0.7 Phase 3 receipt-binding layer for recomputability gate decisions.

Phase 1 defined recomputability classes.

Phase 2 enforced the strong-gate refusal:

> NON_RECOMPUTABLE evidence cannot satisfy gates requiring STRONG_RECOMPUTATION.

Phase 3 binds that enforcement into explicit receipts.

## Core Invariant

No recomputability gate result may be emitted without exposing the class comparison that produced it.

## Receipt Fields

A recomputability gate receipt records:

- `receipt_type`
- `receipt_version`
- `artifact_recomputability_class`
- `gate_required_class`
- `gate_result`
- `reason_code`
- `claim_boundary`

## Valid Decisions

### STRONG_RECOMPUTATION artifact satisfying STRONG_RECOMPUTATION gate

Result:

- `gate_result`: `PASS`
- `reason_code`: `STRONG_RECOMPUTATION_SATISFIES_STRONG_GATE`

### NON_RECOMPUTABLE artifact satisfying occurrence-level gate

Result:

- `gate_result`: `PASS`
- `reason_code`: `NON_RECOMPUTABLE_SATISFIES_OCCURRENCE_GATE_ONLY`

Claim boundary:

> NON_RECOMPUTABLE evidence may support occurrence-level gates but not gates requiring STRONG_RECOMPUTATION.

### NON_RECOMPUTABLE artifact attempting STRONG_RECOMPUTATION gate

Result:

- `gate_result`: `FAIL`
- `reason_code`: `RECOMPUTABILITY_ESCALATION_DEFECT`

Claim boundary:

> NON_RECOMPUTABLE artifacts must not satisfy gates requiring STRONG_RECOMPUTATION.

## Non-Claims

This receipt-binding layer does not add new recomputability classes.

It does not broaden enforcement.

It does not claim empirical reconstruction improvement.

It does not alter the v0.7 Phase 2 release or tag.

It only serializes the recomputability class comparison that produced a gate result.

## Earned Claim After Phase 3

Fork v0.7 Phase 3 emits receipt-level evidence for recomputability gate decisions, recording the artifact class, gate requirement, result, reason code, and claim boundary for accepted or refused recomputability claims.
''')

print("FORK_V0_7_PHASE_3_RECOMPUTABILITY_RECEIPT_BINDING_FILES_WRITTEN")
