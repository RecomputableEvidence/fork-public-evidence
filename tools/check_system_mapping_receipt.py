#!/usr/bin/env python3
"""Deterministic structural checker for SYSTEM_MAPPING_RECEIPT v0.1.

This checker records structural mapping conditions only. It does not approve,
authorize, certify, or evaluate the truth of any claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "system_mapping_receipt_v0_1.schema.json"

RECORDED_KIND = "STRUCTURAL_MAPPING_RECORDED"
INCOMPLETE_KIND = "MAPPING_INCOMPLETE_RECORDED"
EXPANSION_GAP_KIND = "EXPANSION_AUTHORITY_GAP_RECORDED"
NON_CLAIM_DROP_KIND = "NON_CLAIM_DROP_RECORDED"
UNRESOLVED_POINTER_GAP_KIND = "UNRESOLVED_POINTER_MAPPING_GAP_RECORDED"

DO_NOT_MAP_TO = [
    "APPROVAL",
    "AUTHORIZATION",
    "COMPLIANCE",
    "CONTROL_EFFECTIVENESS",
    "DEPLOYMENT_READINESS",
    "LEGAL_SUFFICIENCY",
    "RISK_ACCEPTANCE",
    "SAFETY",
    "TRUTH",
    "WAIVER_APPROVAL",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def pointer_path(parts: list[Any]) -> str:
    rendered: list[str] = []
    for part in parts:
        if isinstance(part, int):
            rendered.append(f"[{part}]")
        else:
            if rendered:
                rendered.append(".")
            rendered.append(str(part))
    return "".join(rendered) if rendered else "$"


def add_error(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def schema_errors(receipt: Any) -> list[dict[str, str]]:
    schema = load_json(SCHEMA_PATH)
    validator = Draft7Validator(schema)
    errors: list[dict[str, str]] = []

    for error in sorted(validator.iter_errors(receipt), key=lambda item: list(item.path)):
        add_error(
            errors,
            "SCHEMA_CONFORMANCE_GAP",
            pointer_path(list(error.path)),
            error.message,
        )

    return errors


def custom_errors(receipt: Any) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if not isinstance(receipt, dict):
        add_error(errors, "MAPPING_RECORD_NOT_OBJECT", "$", "Receipt must be a JSON object.")
        return errors

    records = receipt.get("boundary_behavior_records")
    if not isinstance(records, list):
        return errors

    declared_behavior = receipt.get("consumer_declared_boundary_behavior")
    record_behaviors = [
        record.get("behavior")
        for record in records
        if isinstance(record, dict) and isinstance(record.get("behavior"), str)
    ]

    if declared_behavior == "MIXED":
        if len(set(record_behaviors)) < 2:
            add_error(
                errors,
                "MIXED_DECLARATION_WITHOUT_MIXED_RECORDS",
                "consumer_declared_boundary_behavior",
                "MIXED declaration requires at least two distinct per-claim behavior values.",
            )
    elif declared_behavior in {"PRESERVED", "NARROWED", "EXPANDED", "UNRESOLVED"}:
        for index, behavior in enumerate(record_behaviors):
            if behavior != declared_behavior:
                add_error(
                    errors,
                    "CONSUMER_DECLARATION_RECORD_MISMATCH",
                    f"boundary_behavior_records[{index}].behavior",
                    "Non-MIXED declaration must match each per-claim behavior record.",
                )

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            continue

        base = f"boundary_behavior_records[{index}]"
        behavior = record.get("behavior")
        dropped_non_claims = record.get("dropped_non_claims", [])
        disclosed = record.get("dropped_non_claims_disclosed")
        added_claims = record.get("consumer_added_claims", [])
        unresolved_pointers = record.get("unresolved_pointers", [])
        disposition = record.get("unresolved_pointer_disposition")
        resolution_evidence_refs = record.get("resolution_evidence_refs", [])

        if behavior == "PRESERVED" and dropped_non_claims:
            add_error(
                errors,
                "PRESERVED_RECORD_DROPS_NON_CLAIMS",
                f"{base}.dropped_non_claims",
                "PRESERVED records must not drop upstream non-claims.",
            )

        if dropped_non_claims and disclosed is not True:
            add_error(
                errors,
                "NON_CLAIM_DROPPED_WITHOUT_DISCLOSURE",
                f"{base}.dropped_non_claims_disclosed",
                "Dropped non-claims must be explicitly disclosed.",
            )

        if behavior == "EXPANDED":
            if not added_claims:
                add_error(
                    errors,
                    "EXPANSION_WITHOUT_ADDED_CLAIM",
                    f"{base}.consumer_added_claims",
                    "EXPANDED records require at least one downstream added claim.",
                )

            if isinstance(added_claims, list):
                for claim_index, claim in enumerate(added_claims):
                    claim_base = f"{base}.consumer_added_claims[{claim_index}]"
                    if not isinstance(claim, dict):
                        continue

                    if not is_non_empty_string(claim.get("authority_ref")):
                        add_error(
                            errors,
                            "EXPANSION_AUTHORITY_REF_MISSING",
                            f"{claim_base}.authority_ref",
                            "Downstream added claims require a non-empty authority_ref.",
                        )

                    evidence_refs = claim.get("evidence_refs")
                    if not isinstance(evidence_refs, list) or len(evidence_refs) == 0:
                        add_error(
                            errors,
                            "EXPANDED_CLAIM_EVIDENCE_REF_MISSING",
                            f"{claim_base}.evidence_refs",
                            "Downstream added claims require at least one evidence reference.",
                        )
        elif added_claims:
            add_error(
                errors,
                "ADDED_CLAIM_ON_NON_EXPANDED_RECORD",
                f"{base}.consumer_added_claims",
                "Only EXPANDED records may include downstream added claims.",
            )

        if behavior == "UNRESOLVED" and not unresolved_pointers:
            add_error(
                errors,
                "UNRESOLVED_RECORD_WITHOUT_POINTERS",
                f"{base}.unresolved_pointers",
                "UNRESOLVED records require at least one unresolved pointer.",
            )

        if unresolved_pointers:
            if behavior != "UNRESOLVED":
                add_error(
                    errors,
                    "UNRESOLVED_POINTER_ON_NON_UNRESOLVED_RECORD",
                    f"{base}.behavior",
                    "Records carrying unresolved pointers must use behavior UNRESOLVED.",
                )

            if disposition == "SILENTLY_RESOLVED":
                add_error(
                    errors,
                    "UNRESOLVED_POINTER_SILENTLY_RESOLVED",
                    f"{base}.unresolved_pointer_disposition",
                    "Unresolved pointers must not be silently resolved.",
                )

            if disposition == "NONE":
                add_error(
                    errors,
                    "UNRESOLVED_POINTER_DISPOSITION_MISSING",
                    f"{base}.unresolved_pointer_disposition",
                    "Unresolved pointers require a carried-forward or evidence-backed disposition.",
                )

            if disposition == "RESOLVED_WITH_EVIDENCE" and not resolution_evidence_refs:
                add_error(
                    errors,
                    "UNRESOLVED_POINTER_RESOLUTION_EVIDENCE_MISSING",
                    f"{base}.resolution_evidence_refs",
                    "Evidence-backed pointer resolution requires resolution evidence references.",
                )
        elif disposition and disposition != "NONE":
            add_error(
                errors,
                "POINTER_DISPOSITION_WITHOUT_POINTERS",
                f"{base}.unresolved_pointer_disposition",
                "Pointer disposition must be NONE when no unresolved pointers are present.",
            )

    return errors


def choose_result_kind(errors: list[dict[str, str]]) -> str:
    if not errors:
        return RECORDED_KIND

    codes = {error["code"] for error in errors}

    if {
        "EXPANSION_WITHOUT_ADDED_CLAIM",
        "EXPANSION_AUTHORITY_REF_MISSING",
        "EXPANDED_CLAIM_EVIDENCE_REF_MISSING",
    } & codes:
        return EXPANSION_GAP_KIND

    if {
        "NON_CLAIM_DROPPED_WITHOUT_DISCLOSURE",
        "PRESERVED_RECORD_DROPS_NON_CLAIMS",
    } & codes:
        return NON_CLAIM_DROP_KIND

    if {
        "UNRESOLVED_POINTER_SILENTLY_RESOLVED",
        "UNRESOLVED_POINTER_DISPOSITION_MISSING",
        "UNRESOLVED_POINTER_RESOLUTION_EVIDENCE_MISSING",
        "UNRESOLVED_POINTER_ON_NON_UNRESOLVED_RECORD",
    } & codes:
        return UNRESOLVED_POINTER_GAP_KIND

    return INCOMPLETE_KIND


def build_output(input_path: Path, result_kind: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "checker": {
            "checker_id": "SYSTEM_MAPPING_RECEIPT_CHECKER",
            "checker_version": "0.1",
            "schema_ref": "schemas/system_mapping_receipt_v0_1.schema.json",
            "subject_ref": str(input_path).replace("\\", "/"),
        },
        "result": {
            "result_kind": result_kind,
            "decision_boundary": "NON_DECISIONAL_STRUCTURAL_MAPPING_RECORD_ONLY",
            "safe_to_automate_decisions": False,
            "requires_human_interpretation_before_any_automation": True,
        },
        "limitations": {
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_compliance": True,
            "does_not_validate_approval": True,
            "does_not_validate_authorization": True,
            "does_not_validate_legal_sufficiency": True,
            "does_not_validate_control_effectiveness": True,
            "does_not_determine_policy_permission": True,
            "do_not_map_to": DO_NOT_MAP_TO,
        },
        "errors": sorted(errors, key=lambda item: (item["code"], item["path"], item["message"])),
    }


def check_file(input_path: Path) -> dict[str, Any]:
    errors: list[dict[str, str]] = []

    try:
        receipt = load_json(input_path)
    except json.JSONDecodeError as exc:
        add_error(errors, "JSON_PARSE_GAP", "$", str(exc))
        return build_output(input_path, choose_result_kind(errors), errors)

    errors.extend(schema_errors(receipt))
    errors.extend(custom_errors(receipt))

    result_kind = choose_result_kind(errors)
    return build_output(input_path, result_kind, errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check SYSTEM_MAPPING_RECEIPT v0.1 structure.")
    parser.add_argument("receipt_path", type=Path)
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON.")
    args = parser.parse_args(argv)

    output = check_file(args.receipt_path)

    if args.compact:
        print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(output, indent=2, sort_keys=True))

    return 0 if output["result"]["result_kind"] == RECORDED_KIND else 1


if __name__ == "__main__":
    sys.exit(main())