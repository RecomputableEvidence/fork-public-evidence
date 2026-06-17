from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install project test dependencies before running this checker."
    ) from exc


RECEIPT_NON_CLAIMS = [
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_SOURCE_TRUTH",
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_COMPLETENESS",
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_ADMISSIBILITY",
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_LAWFULNESS",
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_COMPLIANCE",
    "BATCH_ACCEPTANCE_DOES_NOT_CERTIFY_MEDICAL_CORRECTNESS",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except json.JSONDecodeError as exc:
            rows.append(
                {
                    "__json_parse_error__": True,
                    "__line_number__": line_number,
                    "__error__": str(exc),
                }
            )
            continue
        rows.append(value)
    return rows


def schema_errors(validator: Draft202012Validator, obj: dict[str, Any]) -> list[str]:
    errors = sorted(validator.iter_errors(obj), key=lambda err: list(err.path))
    messages: list[str] = []
    for err in errors:
        path = ".".join(str(part) for part in err.path)
        if path:
            messages.append(f"{path}: {err.message}")
        else:
            messages.append(err.message)
    return messages


def build_receipt(
    *,
    batch_id: str,
    processed_timestamp: str,
    batch_result: str,
    record_count_received: int,
    record_count_accepted: int,
    record_count_excluded: int,
    record_count_failed_schema: int,
    record_count_missing_hash: int,
    record_count_unknown_source: int,
    errors: list[dict[str, Any]],
    limitations: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "record_type": "FORK_BATCH_VALIDATION_RECEIPT",
        "schema_version": "0.1.1",
        "batch_id": batch_id,
        "processed_timestamp": processed_timestamp,
        "batch_result": batch_result,
        "record_count_received": record_count_received,
        "record_count_accepted": record_count_accepted,
        "record_count_excluded": record_count_excluded,
        "record_count_failed_schema": record_count_failed_schema,
        "record_count_missing_hash": record_count_missing_hash,
        "record_count_unknown_source": record_count_unknown_source,
        "receipt_non_claims": RECEIPT_NON_CLAIMS,
        "errors": errors,
        "limitations": limitations,
    }


def validate_batch(
    manifest_path: Path,
    records_path: Path,
    schema_path: Path | None = None,
) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    schema_path = schema_path or root / "schemas" / "nightly_batch_export_v0_1_1.schema.json"

    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors: list[dict[str, Any]] = []
    limitations: list[dict[str, Any]] = []

    try:
        manifest = load_json(manifest_path)
    except json.JSONDecodeError as exc:
        return build_receipt(
            batch_id="UNKNOWN",
            processed_timestamp="1970-01-01T00:00:00Z",
            batch_result="REJECTED_SCHEMA_INVALID",
            record_count_received=0,
            record_count_accepted=0,
            record_count_excluded=0,
            record_count_failed_schema=0,
            record_count_missing_hash=0,
            record_count_unknown_source=0,
            errors=[{"scope": "manifest", "code": "MANIFEST_JSON_INVALID", "message": str(exc)}],
            limitations=[],
        )

    manifest_errors = schema_errors(validator, manifest)
    batch_id = str(manifest.get("batch_id", "UNKNOWN"))
    processed_timestamp = str(manifest.get("export_timestamp", "1970-01-01T00:00:00Z"))

    if manifest_errors:
        return build_receipt(
            batch_id=batch_id,
            processed_timestamp=processed_timestamp,
            batch_result="REJECTED_SCHEMA_INVALID",
            record_count_received=0,
            record_count_accepted=0,
            record_count_excluded=0,
            record_count_failed_schema=0,
            record_count_missing_hash=0,
            record_count_unknown_source=0,
            errors=[
                {
                    "scope": "manifest",
                    "code": "MANIFEST_SCHEMA_INVALID",
                    "messages": manifest_errors,
                }
            ],
            limitations=[],
        )

    approved_sources = {
        source["source_system_id"]
        for source in manifest.get("source_systems", [])
        if source.get("approved_source") is True
    }

    rows = load_jsonl(records_path)

    received = len(rows)
    accepted = 0
    excluded = 0
    failed_schema = 0
    missing_hash = 0
    unknown_source = 0

    for index, record in enumerate(rows, start=1):
        record_id = str(record.get("record_id", f"line_{index}"))

        if record.get("__json_parse_error__"):
            failed_schema += 1
            errors.append(
                {
                    "scope": "record",
                    "record_id": record_id,
                    "line_number": record.get("__line_number__"),
                    "code": "RECORD_JSON_INVALID",
                    "message": record.get("__error__"),
                }
            )
            continue

        record_errors = schema_errors(validator, record)

        if record.get("batch_id") != batch_id:
            record_errors.append(
                f"batch_id: record batch_id {record.get('batch_id')!r} does not match manifest batch_id {batch_id!r}"
            )

        if record_errors:
            failed_schema += 1
            errors.append(
                {
                    "scope": "record",
                    "record_id": record_id,
                    "code": "RECORD_SCHEMA_INVALID",
                    "messages": record_errors,
                }
            )
            continue

        source_system_id = record["source"]["source_system_id"]
        if source_system_id not in approved_sources:
            excluded += 1
            unknown_source += 1
            limitations.append(
                {
                    "scope": "record",
                    "record_id": record_id,
                    "code": "UNKNOWN_SOURCE_EXCLUDED",
                    "source_system_id": source_system_id,
                }
            )
            continue

        if record["hash"]["hash_value"] is None:
            missing_hash += 1
            limitations.append(
                {
                    "scope": "record",
                    "record_id": record_id,
                    "code": "HASH_NOT_AVAILABLE",
                    "reason": record["hash"]["hash_not_available_reason"],
                }
            )

        accepted += 1

    if failed_schema > 0:
        batch_result = "REJECTED_SCHEMA_INVALID"
    elif excluded > 0 or missing_hash > 0:
        batch_result = "ACCEPTED_WITH_LIMITATIONS"
    else:
        batch_result = "ACCEPTED"

    return build_receipt(
        batch_id=batch_id,
        processed_timestamp=processed_timestamp,
        batch_result=batch_result,
        record_count_received=received,
        record_count_accepted=accepted,
        record_count_excluded=excluded,
        record_count_failed_schema=failed_schema,
        record_count_missing_hash=missing_hash,
        record_count_unknown_source=unknown_source,
        errors=errors,
        limitations=limitations,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Fork Nightly Batch Export / Append-Only Drop v0.1.1 manifest and JSONL records."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--records", required=True, type=Path)
    parser.add_argument("--schema", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    receipt = validate_batch(args.manifest, args.records, args.schema)
    output = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)

    return 0 if receipt["batch_result"] in {"ACCEPTED", "ACCEPTED_WITH_LIMITATIONS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
