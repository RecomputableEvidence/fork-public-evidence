from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
OBSERVATION = (
    ROOT / "docs/exterior-observations/reviews/pr91-chatgpt-20260724"
)
ORIGINAL_RECEIPT = (
    OBSERVATION
    / "ORIGINAL_EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_v0_1.json"
)
ORIGINAL_ZIP = (
    OBSERVATION
    / "ORIGINAL_FORK_PR91_EXTERIOR_RECOMPUTATION_CHATGPT_20260724_v0_1.zip"
)
NORMALIZED_RECEIPT = (
    OBSERVATION
    / "EXTERIOR_RECOMPUTATION_RECEIPT_PR91_CHATGPT_20260724_NORMALIZED_v0_1_1.json"
)
PRESERVATION_MANIFEST = OBSERVATION / "PRESERVATION_MANIFEST_v0_1.json"
SCHEMA = (
    ROOT / "schemas/fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json"
)
RETURN_CHECKER = (
    ROOT / "tools/check_longitudinal_exterior_recomputation_return_v0_1.py"
)
NORMALIZER = (
    ROOT / "tools/normalize_longitudinal_exterior_recomputation_return_v0_1.py"
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_original_artifacts_remain_registered_bytes() -> None:
    normalizer = load_module(NORMALIZER, "fork_return_normalizer_v0_1")
    assert normalizer.sha256_file(ORIGINAL_RECEIPT) == (
        normalizer.EXPECTED_SOURCE_RECEIPT_SHA256
    )
    assert normalizer.sha256_file(ORIGINAL_ZIP) == (
        normalizer.EXPECTED_SOURCE_ZIP_SHA256
    )


def test_preservation_manifest_binds_every_non_manifest_file() -> None:
    normalizer = load_module(NORMALIZER, "fork_return_normalizer_v0_1")
    manifest = json.loads(PRESERVATION_MANIFEST.read_text(encoding="utf-8"))
    entries = {item["path"]: item for item in manifest["entries"]}
    actual = {
        path.name
        for path in OBSERVATION.iterdir()
        if path.is_file() and path != PRESERVATION_MANIFEST
    }
    assert set(entries) == actual
    for relative, entry in entries.items():
        path = OBSERVATION / relative
        assert entry["sha256"] == normalizer.sha256_file(path)
        assert entry["size_bytes"] == path.stat().st_size
    assert manifest["self_exclusion"] == {
        "path": "PRESERVATION_MANIFEST_v0_1.json",
        "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
    }


def test_original_rich_return_preserves_schema_negative_evidence() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    original = json.loads(ORIGINAL_RECEIPT.read_text(encoding="utf-8"))
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(original))
    assert errors
    assert any(list(error.path)[:1] == ["executions"] for error in errors)
    assert any(list(error.path)[:1] == ["findings"] for error in errors)
    assert any(list(error.path)[:1] == ["measurements"] for error in errors)


def test_normalized_successor_is_mechanical_and_schema_valid() -> None:
    normalizer = load_module(NORMALIZER, "fork_return_normalizer_v0_1")
    expected = normalizer.normalize(ORIGINAL_RECEIPT, ORIGINAL_ZIP)
    committed = json.loads(NORMALIZED_RECEIPT.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator(schema).validate(committed)
    assert committed == expected
    assert committed["disposition"] == "REPRODUCED_WITH_CORRECTION_REQUIRED"
    assert committed["reviewer_disclosure"] == json.loads(
        ORIGINAL_RECEIPT.read_text(encoding="utf-8")
    )["reviewer_disclosure"]
    assert len(committed["executions"]) == 35
    assert len(committed["measurements"]["adversarial_results"]) == 10
    assert all(
        item["conforms"]
        for item in committed["measurements"]["adversarial_results"]
    )


def test_return_checker_validates_successor_and_source_bindings() -> None:
    checker = load_module(RETURN_CHECKER, "fork_return_checker_v0_1")
    schema = checker.strict_load(SCHEMA)
    receipt = checker.strict_load(NORMALIZED_RECEIPT)
    result = checker.validate_return(
        receipt,
        schema,
        artifact_root=OBSERVATION,
        allow_pending=False,
    )
    assert result["ok"] is True
    assert result["artifact_bindings_verified"] is True
    assert result["status"] == "EXTERIOR_RECOMPUTATION_RETURN_CONFORMS"
    assert result["recorded_disposition"] == (
        "REPRODUCED_WITH_CORRECTION_REQUIRED"
    )
    assert result["substantive_recomputation_inferred"] is False


def test_return_checker_rejects_payload_mutation() -> None:
    checker = load_module(RETURN_CHECKER, "fork_return_checker_v0_1")
    schema = checker.strict_load(SCHEMA)
    receipt = checker.strict_load(NORMALIZED_RECEIPT)
    mutated = copy.deepcopy(receipt)
    mutated["measurements"]["focused_tests"]["passed"] = 15
    result = checker.validate_return(
        mutated,
        schema,
        artifact_root=OBSERVATION,
        allow_pending=False,
    )
    assert result["ok"] is False
    assert "RECEIPT_PAYLOAD_DIGEST_MISMATCH" in result["finding_codes"]


def test_return_checker_rejects_source_artifact_mutation(tmp_path: Path) -> None:
    checker = load_module(RETURN_CHECKER, "fork_return_checker_v0_1")
    schema = checker.strict_load(SCHEMA)
    receipt = checker.strict_load(NORMALIZED_RECEIPT)
    for artifact in receipt["raw_output_artifacts"]:
        source = OBSERVATION / artifact["path"]
        target = tmp_path / artifact["path"]
        target.write_bytes(source.read_bytes())
    with ORIGINAL_RECEIPT.open("rb") as source:
        (tmp_path / ORIGINAL_RECEIPT.name).write_bytes(source.read() + b"\n")
    result = checker.validate_return(
        receipt,
        schema,
        artifact_root=tmp_path,
        allow_pending=False,
    )
    assert result["ok"] is False
    assert "RAW_ARTIFACT_SIZE_MISMATCH" in result["finding_codes"]
    assert "RAW_ARTIFACT_DIGEST_MISMATCH" in result["finding_codes"]
