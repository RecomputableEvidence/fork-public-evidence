from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


DRY_RUN_NON_CLAIMS = [
    "DRY_RUN_DOES_NOT_AUTHORIZE_LIVE_INGESTION",
    "DRY_RUN_DOES_NOT_CERTIFY_SOURCE_TRUTH",
    "DRY_RUN_DOES_NOT_CERTIFY_COMPLETENESS",
    "DRY_RUN_DOES_NOT_CERTIFY_ADMISSIBILITY",
    "DRY_RUN_DOES_NOT_CERTIFY_LAWFULNESS",
    "DRY_RUN_DOES_NOT_CERTIFY_COMPLIANCE",
    "DRY_RUN_DOES_NOT_CERTIFY_MEDICAL_CORRECTNESS",
    "DRY_RUN_DOES_NOT_CERTIFY_CLINICAL_APPROPRIATENESS",
    "DRY_RUN_DOES_NOT_CERTIFY_UTILIZATION_MANAGEMENT_SUFFICIENCY",
    "DRY_RUN_DOES_NOT_CREATE_RUNTIME_AUTHORIZATION",
]

DRY_RUN_PHASES = {"SYNTHETIC_DRY_RUN", "REDACTED_DRY_RUN"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            rows.append(json.loads(stripped))
    return rows


def load_batch_checker():
    root = Path(__file__).resolve().parents[1]
    checker_path = root / "tools" / "check_nightly_batch_export.py"
    spec = importlib.util.spec_from_file_location("check_nightly_batch_export", checker_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load checker from {checker_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def detect_full_source_content(manifest: dict[str, Any], records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    content_policy = manifest.get("content_policy", {})
    if content_policy.get("full_source_content_included") is True:
        findings.append(
            {
                "scope": "manifest",
                "code": "FULL_SOURCE_CONTENT_INCLUDED_IN_DRY_RUN",
                "message": "Manifest content_policy indicates full source content is included.",
            }
        )

    for index, record in enumerate(records, start=1):
        record_id = str(record.get("record_id", f"line_{index}"))
        content_exception = record.get("content_exception", {})
        if content_exception.get("full_source_content_included") is True:
            findings.append(
                {
                    "scope": "record",
                    "record_id": record_id,
                    "code": "FULL_SOURCE_CONTENT_INCLUDED_IN_DRY_RUN",
                    "message": "Record content_exception indicates full source content is included.",
                }
            )

    return findings


def manual_review_candidates_from_receipt(receipt: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []

    for limitation in receipt.get("limitations", []):
        candidates.append(
            {
                "source": "validation_receipt.limitations",
                "record_id": limitation.get("record_id"),
                "condition": limitation.get("code"),
                "routing_posture": "INSTITUTION_DEFINED_REVIEW",
            }
        )

    for error in receipt.get("errors", []):
        candidates.append(
            {
                "source": "validation_receipt.errors",
                "record_id": error.get("record_id"),
                "condition": error.get("code"),
                "routing_posture": "INSTITUTION_DEFINED_REVIEW",
            }
        )

    return candidates


def determine_gate_result(
    *,
    receipt: dict[str, Any],
    manifest: dict[str, Any],
    unapproved_content_findings: list[dict[str, Any]],
    allow_live_phase: bool,
) -> tuple[str, list[dict[str, Any]]]:
    gate_findings: list[dict[str, Any]] = []

    batch_result = receipt.get("batch_result")
    if isinstance(batch_result, str) and batch_result.startswith("REJECTED_"):
        gate_findings.append(
            {
                "code": "BATCH_VALIDATION_REJECTED",
                "message": f"Batch validation receipt result was {batch_result}.",
            }
        )

    pilot_phase = manifest.get("pilot_phase")
    if pilot_phase not in DRY_RUN_PHASES and not allow_live_phase:
        gate_findings.append(
            {
                "code": "MANIFEST_NOT_DRY_RUN_PHASE",
                "message": "Dry-run harness requires SYNTHETIC_DRY_RUN or REDACTED_DRY_RUN unless --allow-live-phase is set.",
                "pilot_phase": pilot_phase,
            }
        )

    for finding in unapproved_content_findings:
        gate_findings.append(finding)

    if gate_findings:
        return "DRY_RUN_GATE_FAILED", gate_findings

    if receipt.get("batch_result") == "ACCEPTED_WITH_LIMITATIONS":
        return "DRY_RUN_GATE_PASSED_WITH_LIMITATIONS", gate_findings

    return "DRY_RUN_GATE_PASSED", gate_findings


def run_dry_run(
    *,
    manifest_path: Path,
    records_path: Path,
    output_dir: Path,
    allow_live_phase: bool = False,
) -> dict[str, Any]:
    checker = load_batch_checker()
    manifest = load_json(manifest_path)
    records = load_jsonl(records_path)

    receipt = checker.validate_batch(manifest_path, records_path)
    batch_id = str(receipt.get("batch_id", manifest.get("batch_id", "UNKNOWN")))

    unapproved_content_findings = detect_full_source_content(manifest, records)
    gate_result, gate_findings = determine_gate_result(
        receipt=receipt,
        manifest=manifest,
        unapproved_content_findings=unapproved_content_findings,
        allow_live_phase=allow_live_phase,
    )

    summary = {
        "record_type": "FORK_PILOT_DRY_RUN_SUMMARY",
        "schema_version": "0.1",
        "batch_id": batch_id,
        "pilot_id": manifest.get("pilot_id"),
        "pilot_phase": manifest.get("pilot_phase"),
        "export_mode": manifest.get("export_mode"),
        "capture_mode": manifest.get("capture_mode"),
        "deployment_location": manifest.get("deployment_location"),
        "gate_result": gate_result,
        "batch_result": receipt.get("batch_result"),
        "counts": {
            "record_count_received": receipt.get("record_count_received", 0),
            "record_count_accepted": receipt.get("record_count_accepted", 0),
            "record_count_excluded": receipt.get("record_count_excluded", 0),
            "record_count_failed_schema": receipt.get("record_count_failed_schema", 0),
            "record_count_missing_hash": receipt.get("record_count_missing_hash", 0),
            "record_count_unknown_source": receipt.get("record_count_unknown_source", 0),
        },
        "gate_findings": gate_findings,
        "manual_review_candidates": manual_review_candidates_from_receipt(receipt),
        "unapproved_content_findings": unapproved_content_findings,
        "receipt_path": f"fork_batch_validation_receipt_{batch_id}.json",
        "dry_run_non_claims": DRY_RUN_NON_CLAIMS,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = output_dir / f"fork_batch_validation_receipt_{batch_id}.json"
    summary_path = output_dir / f"fork_pilot_dry_run_summary_{batch_id}.json"

    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run Fork Pilot Dry-Run Harness v0.1 over a synthetic or redacted nightly batch export."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--records", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--allow-live-phase",
        action="store_true",
        help="Allow LIVE_PILOT manifest phase for harness testing only. Default requires dry-run phase.",
    )
    args = parser.parse_args(argv)

    summary = run_dry_run(
        manifest_path=args.manifest,
        records_path=args.records,
        output_dir=args.output_dir,
        allow_live_phase=args.allow_live_phase,
    )

    sys.stdout.write(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return 0 if summary["gate_result"] in {"DRY_RUN_GATE_PASSED", "DRY_RUN_GATE_PASSED_WITH_LIMITATIONS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
