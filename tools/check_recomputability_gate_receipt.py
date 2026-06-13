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
