from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_v0_1.md"
SCHEMA = ROOT / "schemas" / "controlled_pilot_synthetic_dry_run_corpus_v0_1.schema.json"
CHECKER = ROOT / "tools" / "check_controlled_pilot_synthetic_corpus.py"
MANIFEST = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "manifest_v0_1.json"
VALID_JSONL = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "exports" / "synthetic_prior_auth_denial_internal_appeals_batch_v0_1.jsonl"
INVALID_PII_JSONL = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "invalid" / "invalid_contains_pii_v0_1.jsonl"
INVALID_CLASS_C_JSONL = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "invalid" / "invalid_class_c_missing_expansion_v0_1.jsonl"
PACKAGE_INDEX = ROOT / "pilot_package" / "controlled_pilot_package_index_v0_1.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run_checker(manifest_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(manifest_path.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_synthetic_corpus_doc_exists_and_preserves_non_claims() -> None:
    text = DOC.read_text(encoding="utf-8")

    assert "synthetic JSONL batch exports" in text
    assert "does not use live institutional data, PHI, PII" in text
    assert "does not claim" in text
    assert "live-ingestion authorization" in text


def test_synthetic_corpus_schema_exists_and_names_manifest_type() -> None:
    schema = load_json(SCHEMA)

    assert schema["title"] == "Controlled Pilot Synthetic Dry-Run Corpus Manifest v0.1"
    assert schema["properties"]["record_type"]["const"] == "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_MANIFEST"


def test_manifest_declares_synthetic_only_policy() -> None:
    manifest = load_json(MANIFEST)
    policy = manifest["synthetic_data_policy"]

    assert manifest["record_type"] == "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_MANIFEST"
    assert policy["synthetic_only"] is True
    assert policy["contains_no_phi"] is True
    assert policy["contains_no_pii"] is True
    assert policy["contains_no_live_source_system_data"] is True
    assert policy["contains_no_real_authorization_workflows"] is True


def test_valid_synthetic_corpus_checker_passes() -> None:
    result = run_checker(MANIFEST)

    assert result.returncode == 0, result.stdout + result.stderr
    receipt = json.loads(result.stdout)
    assert receipt["validation_result"] == "PASS"
    assert receipt["record_count"] == 3


def test_valid_synthetic_corpus_contains_class_a_b_c_records() -> None:
    records = load_jsonl(VALID_JSONL)
    classes = {record["synthetic_class"] for record in records}

    assert classes == {
        "CLASS_A_BOUNDED_PRESERVATION",
        "CLASS_B_INDETERMINATE_UNRESOLVED_POINTER",
        "CLASS_C_INVALID_BOUNDARY_EXPANSION",
    }


def test_class_a_record_is_bounded_preservation_pass() -> None:
    records = load_jsonl(VALID_JSONL)
    class_a = next(
        record for record in records
        if record["synthetic_class"] == "CLASS_A_BOUNDED_PRESERVATION"
    )

    assert class_a["expected_rgv_result"] == "PASS"
    assert class_a["downstream_consumption"]["boundary_effect"] == "PRESERVED"
    assert class_a["downstream_consumption"]["attempted_expansion_claims"] == []
    assert class_a["unresolved_pointers"] == []


def test_class_c_record_models_invalid_boundary_expansion() -> None:
    records = load_jsonl(VALID_JSONL)
    class_c = next(
        record for record in records
        if record["synthetic_class"] == "CLASS_C_INVALID_BOUNDARY_EXPANSION"
    )

    assert class_c["expected_rgv_result"] == "FAIL"
    assert class_c["downstream_consumption"]["boundary_effect"] == "EXPANDED"
    assert "LIVE_INGESTION_AUTHORIZATION_GRANTED" in class_c["downstream_consumption"]["attempted_expansion_claims"]


def test_invalid_pii_fixture_fails_checker(tmp_path: Path) -> None:
    manifest = load_json(MANIFEST)
    manifest["jsonl_exports"][0]["path"] = str(
        INVALID_PII_JSONL.relative_to(ROOT)
    ).replace("\\", "/")
    manifest["jsonl_exports"][0]["expected_record_count"] = 1

    temp_manifest = tmp_path / "manifest_invalid_pii.json"
    temp_manifest.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(CHECKER), str(temp_manifest.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    receipt = json.loads(result.stdout)
    assert receipt["validation_result"] == "FAIL"
    assert any(
        "PII-like text" in error or "contains_pii must be false" in error
        for error in receipt["errors"]
    )


def test_invalid_class_c_missing_expansion_fails_checker(tmp_path: Path) -> None:
    manifest = load_json(MANIFEST)
    manifest["jsonl_exports"][0]["path"] = str(
        INVALID_CLASS_C_JSONL.relative_to(ROOT)
    ).replace("\\", "/")
    manifest["jsonl_exports"][0]["expected_record_count"] = 1

    temp_manifest = tmp_path / "manifest_invalid_class_c.json"
    temp_manifest.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(CHECKER), str(temp_manifest.relative_to(ROOT))],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    receipt = json.loads(result.stdout)
    assert receipt["validation_result"] == "FAIL"
    assert any(
        "requires at least one attempted expansion claim" in error
        for error in receipt["errors"]
    )


def test_package_index_includes_synthetic_corpus_components() -> None:
    package_index = load_json(PACKAGE_INDEX)
    component_ids = {
        component["component_id"]
        for component in package_index["package_components"]
    }

    assert "controlled_pilot_synthetic_dry_run_corpus_doc" in component_ids
    assert "controlled_pilot_synthetic_dry_run_corpus_schema" in component_ids
    assert "controlled_pilot_synthetic_dry_run_corpus_checker" in component_ids
    assert "controlled_pilot_synthetic_dry_run_corpus_fixtures" in component_ids
    assert "controlled_pilot_synthetic_dry_run_corpus_tests" in component_ids
