from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_preservation_integrity_v0_1.py"
ARCHIVE = Path("docs/preservation/failure-mode-archive-v0.1")
INCIDENT = ARCHIVE / "incidents/FORK-INC-2026-07-13-001"
SPECIMEN = INCIDENT / "specimens/fork-evidence-ci.7080e198.malformed.yml.txt"
INCIDENT_RECORD = INCIDENT / "INCIDENT_RECORD_v0_1.json"
CLASSIFICATION = INCIDENT / "CLAIM_CONSUMPTION_FAILURE_CLASSIFICATION_v0_1.json"
RESIDUAL = INCIDENT / "RESIDUAL_CONDITIONS_v0_1.json"
MANIFEST = INCIDENT / "PRESERVATION_MANIFEST_v0_1.json"
SCHEMAS = [
    "preservation_incident_record_v0_1.schema.json",
    "claim_consumption_failure_classification_v0_1.schema.json",
    "preservation_manifest_v0_1.schema.json",
]
RECEIPT = ROOT / "receipts/preservation-integrity/FORK_INC_2026_07_13_001_BASELINE_RECEIPT_v0_1.json"


def materialize(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "docs" / "preservation", root / "docs" / "preservation")
    (root / "schemas").mkdir(parents=True)
    for name in SCHEMAS:
        shutil.copy2(ROOT / "schemas" / name, root / "schemas" / name)
    shutil.copytree(ROOT / ".github" / "workflows", root / ".github" / "workflows")
    return root


def run_checker(root: Path) -> tuple[int, dict]:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--repo-root", str(root)],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.stdout.strip(), completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def error_codes(payload: dict) -> set[str]:
    return {item["code"] for item in payload["errors"]}


def test_preservation_package_passes_structural_checks(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    code, payload = run_checker(root)
    assert code == 0
    assert payload["result"] == {"ok": True, "result_kind": "STRUCTURAL_PASS"}
    assert payload["verification"]["record_count"] == 7
    assert payload["verification"]["schema_count"] == 3
    assert payload["verification"]["specimens"][0]["sha256"] == "842e79b28e79a86aaf437f80380fc7beaad17a14fd534894393dc2e135d3e0ea"
    assert payload["verification"]["specimens"][0]["git_blob_sha1"] == "f6a6c510bc6eff17b00595f0c10b0ecf962b4bf3"
    assert payload["non_claims"]["does_not_certify_security"] is True
    assert payload["non_claims"]["does_not_authorize_execution"] is True


def test_preservation_schemas_are_valid_draft7() -> None:
    for name in SCHEMAS:
        schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
        jsonschema.Draft7Validator.check_schema(schema)


def test_committed_receipt_matches_current_checker_output() -> None:
    code, payload = run_checker(ROOT)
    expected = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert code == 0
    assert payload == expected


def test_mutated_specimen_fails_both_content_address_checks(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    specimen = root / SPECIMEN
    specimen.write_bytes(specimen.read_bytes() + b"# mutation\n")
    code, payload = run_checker(root)
    assert code != 0
    assert {"SPECIMEN_SHA256_MISMATCH", "SPECIMEN_GIT_BLOB_MISMATCH"} <= error_codes(payload)


def test_quarantined_digest_cannot_return_to_live_workflows(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    (root / ".github/workflows/reintroduced.yml").write_bytes((root / SPECIMEN).read_bytes())
    code, payload = run_checker(root)
    assert code != 0
    assert "QUARANTINED_DIGEST_IN_LIVE_WORKFLOW" in error_codes(payload)


def test_intent_cannot_be_inferred_from_preserved_evidence(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / CLASSIFICATION
    value = json.loads(path.read_text(encoding="utf-8"))
    value["intent"] = "MALICIOUS"
    write_json(path, value)
    code, payload = run_checker(root)
    assert code != 0
    assert "INTENT_MUST_REMAIN_NOT_EVALUATED" in error_codes(payload)


def test_preservation_cannot_change_experiment_state(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / INCIDENT_RECORD
    value = json.loads(path.read_text(encoding="utf-8"))
    value["experiment_effect"]["baseline_execution_started"] = True
    write_json(path, value)
    code, payload = run_checker(root)
    assert code != 0
    assert "EXPERIMENT_BOUNDARY_EFFECT" in error_codes(payload)


def test_residual_conditions_cannot_be_erased(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / RESIDUAL
    value = json.loads(path.read_text(encoding="utf-8"))
    value["conditions"] = []
    write_json(path, value)
    code, payload = run_checker(root)
    assert code != 0
    assert "RESIDUAL_CONDITIONS_EMPTY" in error_codes(payload)


def test_duplicate_json_keys_fail_closed(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / CLASSIFICATION
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '  "intent": "NOT_EVALUATED",',
        '  "intent": "NOT_EVALUATED",\n  "intent": "NOT_EVALUATED",',
        1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    code, payload = run_checker(root)
    assert code != 0
    assert "DUPLICATE_JSON_KEY" in error_codes(payload)


def test_main_ref_effect_cannot_be_expanded(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / INCIDENT / "CONTINUANCE_BASIS_v0_1.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    value["main_ref_effect"] = "MOVE"
    write_json(path, value)
    code, payload = run_checker(root)
    assert code != 0
    assert "MAIN_REF_EFFECT_PROHIBITED" in error_codes(payload)


def test_archive_path_traversal_fails_closed(tmp_path: Path) -> None:
    root = materialize(tmp_path)
    path = root / MANIFEST
    value = json.loads(path.read_text(encoding="utf-8"))
    value["specimens"][0]["archive_path"] = "../../.github/workflows/quarantined.yml.txt"
    write_json(path, value)
    code, payload = run_checker(root)
    assert code != 0
    assert "ARCHIVE_PATH_NOT_INERT" in error_codes(payload)
