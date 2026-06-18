from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SYNTHETIC_CORPUS_STRUCTURAL_BANNER = "SYNTHETIC ONLY — STRUCTURAL EVIDENCE-BOUNDARY CHECK; NOT AUTHORIZATION, NOT CLINICAL REVIEW, NOT LEGAL SUFFICIENCY, NOT HIPAA COMPLIANCE, NOT PRODUCTION READINESS, AND NOT A STATUTORY REVIEW PROCESS."



CANONICAL_NON_CLAIMS = [
    "DOES_NOT_CLAIM_MEDICAL_CORRECTNESS",
    "DOES_NOT_CLAIM_LEGAL_SUFFICIENCY",
    "DOES_NOT_CLAIM_REGULATORY_COMPLIANCE",
    "DOES_NOT_CLAIM_HIPAA_COMPLIANCE",
    "DOES_NOT_CLAIM_SOURCE_TRUTH",
    "DOES_NOT_AUTHORIZE_LIVE_INGESTION",
    "DOES_NOT_USE_REAL_PATIENT_DATA",
]

CLASS_EXPECTATIONS = {
    "CLASS_A_BOUNDED_PRESERVATION": {
        "expected_rgv_result": "BOUNDARY_PRESERVED",
        "boundary_effect": "PRESERVED",
        "requires_unresolved": False,
        "requires_expansion": False,
    },
    "CLASS_B_INDETERMINATE_UNRESOLVED_POINTER": {
        "expected_rgv_result": "POINTER_UNRESOLVED",
        "boundary_effect": "UNRESOLVED_POINTER",
        "requires_unresolved": True,
        "requires_expansion": False,
    },
    "CLASS_C_INVALID_BOUNDARY_EXPANSION": {
        "expected_rgv_result": "EXPANSION_DETECTED",
        "boundary_effect": "EXPANDED",
        "requires_unresolved": False,
        "requires_expansion": True,
    },
}

PROHIBITED_TEXT_PATTERNS = [
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b\d{3}[-.]\d{3}[-.]\d{4}\b"),
]


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(walk_strings(item))
        return result
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(walk_strings(item))
        return result
    return []


def has_prohibited_text(value: Any) -> bool:
    for text in walk_strings(value):
        for pattern in PROHIBITED_TEXT_PATTERNS:
            if pattern.search(text):
                return True
    return False


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if manifest.get("record_type") != "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_MANIFEST":
        errors.append("manifest.record_type must be CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_MANIFEST")

    if manifest.get("schema_version") != "0.1":
        errors.append("manifest.schema_version must be 0.1")

    policy = manifest.get("synthetic_data_policy")
    if not isinstance(policy, dict):
        errors.append("manifest.synthetic_data_policy must be an object")
    else:
        required_true = [
            "synthetic_only",
            "contains_no_phi",
            "contains_no_pii",
            "contains_no_real_patients",
            "contains_no_real_members",
            "contains_no_real_providers",
            "contains_no_live_source_system_data",
            "contains_no_real_authorization_workflows",
        ]
        for key in required_true:
            if policy.get(key) is not True:
                errors.append(f"manifest.synthetic_data_policy.{key} must be true")

    if manifest.get("corpus_non_claims") != CANONICAL_NON_CLAIMS:
        errors.append("manifest.corpus_non_claims must match canonical synthetic corpus non-claims exactly")

    exports = manifest.get("jsonl_exports")
    if not isinstance(exports, list) or not exports:
        errors.append("manifest.jsonl_exports must be a non-empty list")

    return errors


def validate_record(record: dict[str, Any], line_no: int) -> list[str]:
    errors: list[str] = []
    prefix = f"line {line_no}"

    required = [
        "record_type",
        "schema_version",
        "event_id",
        "synthetic_class",
        "synthetic_only",
        "contains_phi",
        "contains_pii",
        "source_system",
        "workflow",
        "synthetic_subject_ref",
        "supported_claims",
        "non_claims_required",
        "downstream_consumption",
        "unresolved_pointers",
        "expected_rgv_result",
    ]
    for field in required:
        if field not in record:
            errors.append(f"{prefix}: missing required field {field}")

    if record.get("record_type") != "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_EVENT":
        errors.append(f"{prefix}: record_type must be CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_EVENT")

    if record.get("schema_version") != "0.1":
        errors.append(f"{prefix}: schema_version must be 0.1")

    if record.get("synthetic_only") is not True:
        errors.append(f"{prefix}: synthetic_only must be true")

    if record.get("contains_phi") is not False:
        errors.append(f"{prefix}: contains_phi must be false")

    if record.get("contains_pii") is not False:
        errors.append(f"{prefix}: contains_pii must be false")

    if has_prohibited_text(record):
        errors.append(f"{prefix}: prohibited PII-like text pattern detected")

    if record.get("source_system") != "SYNTHETIC_PRIOR_AUTH_SIMULATOR":
        errors.append(f"{prefix}: source_system must be SYNTHETIC_PRIOR_AUTH_SIMULATOR")

    if record.get("workflow") != "SYNTHETIC_PRIOR_AUTH_DENIAL_INTERNAL_APPEALS_REVIEW":
        errors.append(f"{prefix}: workflow must be SYNTHETIC_PRIOR_AUTH_DENIAL_INTERNAL_APPEALS_REVIEW")

    if record.get("non_claims_required") != CANONICAL_NON_CLAIMS:
        errors.append(f"{prefix}: non_claims_required must match canonical synthetic non-claims exactly")

    cls = record.get("synthetic_class")
    expectation = CLASS_EXPECTATIONS.get(cls)
    if expectation is None:
        errors.append(f"{prefix}: unknown synthetic_class {cls!r}")
        return errors

    if record.get("expected_rgv_result") != expectation["expected_rgv_result"]:
        errors.append(f"{prefix}: expected_rgv_result must be {expectation['expected_rgv_result']}")

    downstream = record.get("downstream_consumption")
    if not isinstance(downstream, dict):
        errors.append(f"{prefix}: downstream_consumption must be an object")
        return errors

    if downstream.get("boundary_effect") != expectation["boundary_effect"]:
        errors.append(f"{prefix}: boundary_effect must be {expectation['boundary_effect']} for {cls}")

    if downstream.get("preserved_non_claims") != CANONICAL_NON_CLAIMS:
        errors.append(f"{prefix}: preserved_non_claims must match canonical synthetic non-claims exactly")

    unresolved = record.get("unresolved_pointers")
    if not isinstance(unresolved, list):
        errors.append(f"{prefix}: unresolved_pointers must be a list")
    elif expectation["requires_unresolved"] and not unresolved:
        errors.append(f"{prefix}: {cls} requires at least one unresolved pointer")
    elif not expectation["requires_unresolved"] and unresolved:
        errors.append(f"{prefix}: {cls} must not include unresolved pointers")

    expansions = downstream.get("attempted_expansion_claims")
    if not isinstance(expansions, list):
        errors.append(f"{prefix}: attempted_expansion_claims must be a list")
    elif expectation["requires_expansion"] and not expansions:
        errors.append(f"{prefix}: {cls} requires at least one attempted expansion claim")
    elif not expectation["requires_expansion"] and expansions:
        errors.append(f"{prefix}: {cls} must not include attempted expansion claims")

    return errors


def validate_jsonl(path: Path) -> tuple[list[str], dict[str, int], int]:
    errors: list[str] = []
    class_counts = {key: 0 for key in CLASS_EXPECTATIONS}
    count = 0

    if not path.exists():
        return [f"missing jsonl export: {path.as_posix()}"], class_counts, count

    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                errors.append(f"line {line_no}: blank JSONL line is not allowed")
                continue
            count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            if not isinstance(record, dict):
                errors.append(f"line {line_no}: record must be a JSON object")
                continue

            cls = record.get("synthetic_class")
            if cls in class_counts:
                class_counts[cls] += 1

            errors.extend(validate_record(record, line_no))

    return errors, class_counts, count


def build_receipt(manifest_ref: Path, errors: list[str], class_counts: dict[str, int], record_count: int) -> dict[str, Any]:
    return {
        "record_type": "CONTROLLED_PILOT_SYNTHETIC_CORPUS_VALIDATION_RECEIPT",
        "schema_version": "0.1",
        "manifest_ref": manifest_ref.as_posix(),
        "validation_result": "BOUNDARY_PRESERVED" if not errors else "EXPANSION_DETECTED",
        "record_count": record_count,
        "class_counts": class_counts,
        "errors": errors,
        "receipt_non_claims": [
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_AUTHORIZE_LIVE_INGESTION",
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_CERTIFY_MEDICAL_CORRECTNESS",
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_CERTIFY_LEGAL_SUFFICIENCY",
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_CERTIFY_REGULATORY_COMPLIANCE",
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_CERTIFY_HIPAA_COMPLIANCE",
            "SYNTHETIC_CORPUS_RECEIPT_DOES_NOT_USE_REAL_PATIENT_DATA",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Fork controlled-pilot synthetic dry-run corpus v0.1."
    )
    parser.add_argument("manifest", help="Path to synthetic dry-run corpus manifest JSON.")
    parser.add_argument("--write-receipt", help="Optional path to write validation receipt JSON.")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = Path(args.manifest)

    errors: list[str] = []
    class_counts = {key: 0 for key in CLASS_EXPECTATIONS}
    record_count = 0

    try:
        manifest = load_json(manifest_path)
    except Exception as exc:
        errors.append(f"could not load manifest: {exc}")
        receipt = build_receipt(manifest_path, errors, class_counts, record_count)
        print(json.dumps(receipt, indent=2, ensure_ascii=False))
        return 1

    if not isinstance(manifest, dict):
        errors.append("manifest must be a JSON object")
    else:
        errors.extend(validate_manifest(manifest))

        for export in manifest.get("jsonl_exports", []):
            if not isinstance(export, dict):
                errors.append("manifest.jsonl_exports entries must be objects")
                continue

            export_path = repo_root / export.get("path", "")
            export_errors, export_class_counts, export_count = validate_jsonl(export_path)
            errors.extend(export_errors)

            record_count += export_count
            for key, value in export_class_counts.items():
                class_counts[key] += value

            expected_count = export.get("expected_record_count")
            if isinstance(expected_count, int) and export_count != expected_count:
                errors.append(f"{export.get('path')}: expected {expected_count} records, observed {export_count}")

            expected_classes = set(export.get("classes", []))
            observed_classes = {key for key, value in export_class_counts.items() if value > 0}
            missing_classes = sorted(expected_classes - observed_classes)
            if missing_classes:
                errors.append(f"{export.get('path')}: missing expected classes {missing_classes}")

    for cls in CLASS_EXPECTATIONS:
        if class_counts[cls] == 0:
            errors.append(f"corpus must include at least one {cls} record")

    receipt = build_receipt(manifest_path, errors, class_counts, record_count)

    if args.write_receipt:
        receipt_path = Path(args.write_receipt)
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    print(json.dumps(receipt, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())


# v0.1.1 hardening invariant:
# Required non-claim for healthcare-adjacent synthetic corpus:
# does_not_claim_statutory_review_process
# This corpus does not represent, simulate, validate, or recommend any statutory prior-authorization, adverse-benefit-determination, utilization-management, or internal-appeals process.
