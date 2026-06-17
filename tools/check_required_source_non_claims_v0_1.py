#!/usr/bin/env python3
"""
Required Source Non-Claims v0.1 checker.

This checker validates the mandatory source non-claim bundle used by Fork/RGV
evidence-boundary records.

It does not verify source truth, factual basis, wholeness, completeness,
admissibility, lawfulness, legal sufficiency, compliance, safety, correctness,
institutional authority, or runtime authorization.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_NON_CLAIM_IDS = {
    "SOURCE_TRUTH_NOT_CLAIMED",
    "FACTUAL_BASIS_NOT_CONFIRMED",
    "WHOLENESS_NOT_ASSERTED",
    "COMPLETENESS_NOT_STATED",
    "ADMISSIBILITY_NOT_INFERRED",
    "LAWFULNESS_NOT_IMPLIED",
}

FORBIDDEN_ASSERTION_FIELDS = {
    "source_truth_assertions": "SOURCE_TRUTH_ASSERTED",
    "factual_basis_confirmations": "FACTUAL_BASIS_CONFIRMED",
    "wholeness_assertions": "WHOLENESS_ASSERTED",
    "completeness_statements": "COMPLETENESS_STATED",
    "admissibility_inferences": "ADMISSIBILITY_INFERRED",
    "lawfulness_implications": "LAWFULNESS_IMPLIED",
}


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_required_source_non_claims(record: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if record.get("record_type") != "REQUIRED_SOURCE_NON_CLAIM_BUNDLE":
        errors.append(
            err(
                "INVALID_RECORD_TYPE",
                "record_type must be REQUIRED_SOURCE_NON_CLAIM_BUNDLE",
            )
        )

    if record.get("bundle_version") != "0.1":
        errors.append(err("INVALID_BUNDLE_VERSION", "bundle_version must be 0.1"))

    for field, code in FORBIDDEN_ASSERTION_FIELDS.items():
        value = record.get(field)
        if value:
            errors.append(
                err(
                    code,
                    f"{field} is prohibited because required source non-claims cannot coexist with positive source assertion fields",
                )
            )

    non_claims = record.get("required_non_claims")
    if not isinstance(non_claims, list):
        errors.append(
            err(
                "MISSING_REQUIRED_NON_CLAIMS",
                "required_non_claims must be a list",
            )
        )
        return errors

    ids: list[str] = []

    for index, item in enumerate(non_claims):
        if not isinstance(item, dict):
            errors.append(
                err(
                    "INVALID_NON_CLAIM_OBJECT",
                    f"required_non_claims[{index}] must be an object",
                )
            )
            continue

        non_claim_id = item.get("non_claim_id")
        statement = item.get("statement")

        if not is_non_empty(non_claim_id):
            errors.append(
                err(
                    "MISSING_NON_CLAIM_ID",
                    f"required_non_claims[{index}].non_claim_id must be a non-empty string",
                )
            )
            continue

        ids.append(non_claim_id)

        if not is_non_empty(statement):
            errors.append(
                err(
                    "EMPTY_NON_CLAIM_STATEMENT",
                    f"required_non_claims[{index}].statement must be a non-empty string",
                )
            )

    counts = Counter(ids)
    for non_claim_id, count in sorted(counts.items()):
        if count > 1:
            errors.append(
                err(
                    "DUPLICATE_NON_CLAIM_ID",
                    f"{non_claim_id} appears {count} times",
                )
            )

    present = set(ids)
    missing = sorted(REQUIRED_NON_CLAIM_IDS - present)
    for non_claim_id in missing:
        errors.append(
            err(
                "MISSING_REQUIRED_SOURCE_NON_CLAIM",
                f"Missing required source non-claim {non_claim_id}",
            )
        )

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "result": "ERROR",
                    "errors": [
                        err(
                            "USAGE",
                            "Usage: check_required_source_non_claims_v0_1.py <record.json>",
                        )
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    path = Path(argv[1])
    try:
        record = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "checked_record": str(path),
                    "errors": [err("JSON_PARSE_ERROR", str(exc))],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    if not isinstance(record, dict):
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "checked_record": str(path),
                    "errors": [
                        err(
                            "RECORD_NOT_OBJECT",
                            "Required source non-claim bundle must be a JSON object",
                        )
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    errors = check_required_source_non_claims(record)
    result = "PASS" if not errors else "FAIL"

    output = {
        "checker": "check_required_source_non_claims_v0_1",
        "checked_record": str(path),
        "result": result,
        "errors": errors,
        "required_non_claim_ids": sorted(REQUIRED_NON_CLAIM_IDS),
        "checker_non_claims": [
            "This checker does not verify SOURCE_TRUTH.",
            "This checker does not confirm factual basis, wholeness, completeness, admissibility, or lawfulness.",
            "This checker treats required source non-claims as inference constraints, not disclaimers."
        ],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))