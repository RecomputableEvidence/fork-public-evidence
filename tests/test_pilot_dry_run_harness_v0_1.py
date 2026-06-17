from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "examples" / "nightly_batch_export" / "valid"
TOOL_PATH = ROOT / "tools" / "run_pilot_dry_run.py"
RECEIPT_SCHEMA_PATH = ROOT / "schemas" / "nightly_batch_export_v0_1_1.schema.json"


def load_harness():
    spec = importlib.util.spec_from_file_location("run_pilot_dry_run", TOOL_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_dry_run_rejects_misaligned_synthetic_batch(tmp_path: Path) -> None:
    harness = load_harness()
    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=VALID_DIR / "valid_hash_reference_only_records.jsonl",
        output_dir=tmp_path,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_FAILED"
    assert any(finding["code"] == "BATCH_VALIDATION_REJECTED" for finding in summary["gate_findings"])
    assert summary["batch_result"].startswith("REJECTED_")


def test_dry_run_passes_with_aligned_synthetic_batch(tmp_path: Path) -> None:
    harness = load_harness()

    manifest = json.loads((VALID_DIR / "valid_synthetic_dry_run_manifest.json").read_text(encoding="utf-8"))
    record = json.loads((VALID_DIR / "valid_hash_reference_only_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["batch_id"] = manifest["batch_id"]

    records_path = tmp_path / "aligned_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")

    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=records_path,
        output_dir=tmp_path,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_PASSED"
    assert summary["batch_result"] == "ACCEPTED"
    assert summary["counts"]["record_count_accepted"] == 1
    assert summary["manual_review_candidates"] == []

    receipt_path = tmp_path / f"fork_batch_validation_receipt_{summary['batch_id']}.json"
    summary_path = tmp_path / f"fork_pilot_dry_run_summary_{summary['batch_id']}.json"

    assert receipt_path.exists()
    assert summary_path.exists()


def test_dry_run_passes_with_limitations_for_missing_hash(tmp_path: Path) -> None:
    harness = load_harness()

    manifest = json.loads((VALID_DIR / "valid_synthetic_dry_run_manifest.json").read_text(encoding="utf-8"))
    record = json.loads((VALID_DIR / "valid_missing_hash_with_reason_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["batch_id"] = manifest["batch_id"]

    records_path = tmp_path / "missing_hash_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")

    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=records_path,
        output_dir=tmp_path,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_PASSED_WITH_LIMITATIONS"
    assert summary["batch_result"] == "ACCEPTED_WITH_LIMITATIONS"
    assert summary["counts"]["record_count_missing_hash"] == 1
    assert any(c["condition"] == "HASH_NOT_AVAILABLE" for c in summary["manual_review_candidates"])


def test_dry_run_fails_for_live_phase_without_override(tmp_path: Path) -> None:
    harness = load_harness()
    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_hash_reference_only_manifest.json",
        records_path=VALID_DIR / "valid_hash_reference_only_records.jsonl",
        output_dir=tmp_path,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_FAILED"
    assert any(finding["code"] == "MANIFEST_NOT_DRY_RUN_PHASE" for finding in summary["gate_findings"])


def test_dry_run_allows_live_phase_when_explicitly_overridden(tmp_path: Path) -> None:
    harness = load_harness()
    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_hash_reference_only_manifest.json",
        records_path=VALID_DIR / "valid_hash_reference_only_records.jsonl",
        output_dir=tmp_path,
        allow_live_phase=True,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_PASSED"
    assert summary["batch_result"] == "ACCEPTED"


def test_dry_run_fails_for_full_source_content(tmp_path: Path) -> None:
    harness = load_harness()

    manifest = json.loads((VALID_DIR / "valid_synthetic_dry_run_manifest.json").read_text(encoding="utf-8"))
    record = json.loads((VALID_DIR / "valid_hash_reference_only_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["batch_id"] = manifest["batch_id"]
    record["content_exception"]["full_source_content_included"] = True
    record["content_exception"]["full_content_exception_id"] = "full_content_exception_001"

    records_path = tmp_path / "full_content_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")

    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=records_path,
        output_dir=tmp_path,
    )

    assert summary["gate_result"] == "DRY_RUN_GATE_FAILED"
    assert any(finding["code"] == "FULL_SOURCE_CONTENT_INCLUDED_IN_DRY_RUN" for finding in summary["gate_findings"])


def test_dry_run_receipt_output_conforms_to_nightly_batch_schema(tmp_path: Path) -> None:
    harness = load_harness()

    manifest = json.loads((VALID_DIR / "valid_synthetic_dry_run_manifest.json").read_text(encoding="utf-8"))
    record = json.loads((VALID_DIR / "valid_hash_reference_only_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["batch_id"] = manifest["batch_id"]

    records_path = tmp_path / "aligned_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")

    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=records_path,
        output_dir=tmp_path,
    )

    receipt_path = tmp_path / f"fork_batch_validation_receipt_{summary['batch_id']}.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    schema = json.loads(RECEIPT_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = list(validator.iter_errors(receipt))

    assert errors == []


def test_dry_run_summary_preserves_non_claims(tmp_path: Path) -> None:
    harness = load_harness()

    manifest = json.loads((VALID_DIR / "valid_synthetic_dry_run_manifest.json").read_text(encoding="utf-8"))
    record = json.loads((VALID_DIR / "valid_hash_reference_only_records.jsonl").read_text(encoding="utf-8").splitlines()[0])
    record["batch_id"] = manifest["batch_id"]

    records_path = tmp_path / "aligned_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")

    summary = harness.run_dry_run(
        manifest_path=VALID_DIR / "valid_synthetic_dry_run_manifest.json",
        records_path=records_path,
        output_dir=tmp_path,
    )

    assert "DRY_RUN_DOES_NOT_AUTHORIZE_LIVE_INGESTION" in summary["dry_run_non_claims"]
    assert "DRY_RUN_DOES_NOT_CERTIFY_SOURCE_TRUTH" in summary["dry_run_non_claims"]
    assert "DRY_RUN_DOES_NOT_CERTIFY_COMPLIANCE" in summary["dry_run_non_claims"]
    assert "DRY_RUN_DOES_NOT_CREATE_RUNTIME_AUTHORIZATION" in summary["dry_run_non_claims"]
