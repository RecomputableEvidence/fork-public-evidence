#!/usr/bin/env python3
"""
RGV Required Source Non-Claim Result Binding v0.1 checker.

This checker binds required source non-claims to RGV PASS result semantics
without modifying the RGV v0.4 evidentiary-weight profile contract.

It does not verify source truth, factual basis, wholeness, completeness,
admissibility, lawfulness, legal sufficiency, compliance, safety, correctness,
institutional authority, runtime authorization, or source completeness.
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

FORBIDDEN_VERIFICATION_SCOPES = {
    "SOURCE_TRUTH",
    "SOURCE_TRUTH_VERIFICATION",
    "FACTUAL_BASIS_CONFIRMATION",
    "WHOLENESS_ASSERTION",
    "COMPLETENESS_ASSERTION",
    "ADMISSIBILITY_INFERENCE",
    "LAWFULNESS_DETERMINATION",
}

NON_CLAIM_FIELDS = (
    "required_source_non_claims",
    "result_non_claims",
)


def err(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}


def is_non_empty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def result_status(record: dict[str, Any]) -> str | None:
    for key in ("result", "verification_result", "status"):
        value = record.get(key)
        if isinstance(value, str):
            return value
    return None


def normalize_scope_values(value: Any) -> set[str]:
    if isinstance(value, str):
        return {value}
    if isinstance(value, list):
        return {item for item in value if isinstance(item, str)}
    return set()


def extract_non_claim_items(record: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    for field in NON_CLAIM_FIELDS:
        value = record.get(field)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    item_copy = dict(item)
                    item_copy["_source_field"] = field
                    items.append(item_copy)

    bundle = record.get("required_source_non_claim_bundle")
    if isinstance(bundle, dict):
        bundle_items = bundle.get("required_non_claims")
        if isinstance(bundle_items, list):
            for item in bundle_items:
                if isinstance(item, dict):
                    item_copy = dict(item)
                    item_copy["_source_field"] = "required_source_non_claim_bundle.required_non_claims"
                    items.append(item_copy)

    return items


def check_forbidden_assertions(record: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    for field, code in FORBIDDEN_ASSERTION_FIELDS.items():
        if record.get(field):
            errors.append(
                err(
                    code,
                    f"{field} is prohibited in RGV result semantics because structural verification does not assert that category",
                )
            )

    scopes = normalize_scope_values(record.get("verification_scope"))
    for scope in sorted(scopes & FORBIDDEN_VERIFICATION_SCOPES):
        errors.append(
            err(
                "PROHIBITED_VERIFICATION_SCOPE",
                f"verification_scope may not include {scope}",
            )
        )

    for field in ("supported_claims", "result_claims", "claims"):
        value = record.get(field)
        if not isinstance(value, list):
            continue

        for index, item in enumerate(value):
            if isinstance(item, str) and item in FORBIDDEN_VERIFICATION_SCOPES:
                errors.append(
                    err(
                        "PROHIBITED_RESULT_CLAIM",
                        f"{field}[{index}] may not assert {item}",
                    )
                )
            elif isinstance(item, dict):
                claim_id = item.get("claim_id") or item.get("id")
                if isinstance(claim_id, str) and claim_id in FORBIDDEN_VERIFICATION_SCOPES:
                    errors.append(
                        err(
                            "PROHIBITED_RESULT_CLAIM",
                            f"{field}[{index}] may not assert {claim_id}",
                        )
                    )

    return errors


def check_required_source_non_claims_for_pass(record: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if result_status(record) != "PASS":
        return errors

    items = extract_non_claim_items(record)
    ids: list[str] = []

    if not items:
        errors.append(
            err(
                "MISSING_RESULT_NON_CLAIMS",
                "RGV PASS result must carry required source non-claims in result_non_claims or required_source_non_claims",
            )
        )
        return errors

    for index, item in enumerate(items):
        non_claim_id = item.get("non_claim_id")
        statement = item.get("statement")

        if not is_non_empty(non_claim_id):
            errors.append(
                err(
                    "MISSING_NON_CLAIM_ID",
                    f"non-claim item {index} must contain a non-empty non_claim_id",
                )
            )
            continue

        ids.append(non_claim_id)

        if non_claim_id in REQUIRED_NON_CLAIM_IDS and not is_non_empty(statement):
            errors.append(
                err(
                    "EMPTY_REQUIRED_NON_CLAIM_STATEMENT",
                    f"{non_claim_id} must carry a non-empty statement",
                )
            )

    counts = Counter(ids)
    for non_claim_id, count in sorted(counts.items()):
        if non_claim_id in REQUIRED_NON_CLAIM_IDS and count > 1:
            errors.append(
                err(
                    "DUPLICATE_REQUIRED_NON_CLAIM_ID",
                    f"{non_claim_id} appears {count} times in RGV PASS result non-claims",
                )
            )

    present = set(ids)
    missing = sorted(REQUIRED_NON_CLAIM_IDS - present)
    for non_claim_id in missing:
        errors.append(
            err(
                "MISSING_REQUIRED_SOURCE_NON_CLAIM_ON_PASS",
                f"RGV PASS result is missing required source non-claim {non_claim_id}",
            )
        )

    return errors


def check_rgv_result(record: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    status = result_status(record)
    if status is None:
        errors.append(
            err(
                "MISSING_RESULT_STATUS",
                "RGV result record must include result, verification_result, or status",
            )
        )
    elif status not in {"PASS", "FAIL", "INDETERMINATE", "ERROR"}:
        errors.append(
            err(
                "INVALID_RESULT_STATUS",
                f"Unsupported result status {status}",
            )
        )

    errors.extend(check_forbidden_assertions(record))
    errors.extend(check_required_source_non_claims_for_pass(record))

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
                            "Usage: check_rgv_result_required_source_non_claim_binding_v0_1.py <rgv_result.json>",
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
                            "RGV result must be a JSON object",
                        )
                    ],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    errors = check_rgv_result(record)
    result = "PASS" if not errors else "FAIL"

    output = {
        "checker": "check_rgv_result_required_source_non_claim_binding_v0_1",
        "checked_record": str(path),
        "result": result,
        "errors": errors,
        "required_non_claim_ids": sorted(REQUIRED_NON_CLAIM_IDS),
        "checker_non_claims": [
            "This checker does not verify SOURCE_TRUTH.",
            "This checker does not confirm factual basis, wholeness, completeness, admissibility, or lawfulness.",
            "This checker binds required source non-claims to RGV PASS semantics without modifying the v0.4 evidentiary-weight profile contract."
        ],
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))