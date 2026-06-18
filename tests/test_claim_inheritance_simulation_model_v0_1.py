from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = REPO_ROOT / "tools" / "check_claim_inheritance_simulation_model.py"
VALID_BUNDLE = (
    REPO_ROOT
    / "examples"
    / "claim_inheritance_simulation_model"
    / "synthetic_claim_inheritance_simulation_bundle_v0_1.json"
)
INVALID_DIR = REPO_ROOT / "examples" / "claim_inheritance_simulation_model" / "invalid"
INVALID_MANIFEST = INVALID_DIR / "manifest_invalid_fixtures_v0_1.json"


spec = importlib.util.spec_from_file_location(
    "check_claim_inheritance_simulation_model",
    TOOL_PATH,
)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


def test_valid_bundle_passes():
    result = checker.check_bundle_path(VALID_BUNDLE)
    assert result["ok"], json.dumps(result, indent=2)


def test_invalid_manifest_exists_and_lists_fixtures():
    manifest = json.loads(INVALID_MANIFEST.read_text(encoding="utf-8"))
    fixtures = manifest["fixtures"]

    assert manifest["manifest_id"] == "claim_inheritance_invalid_fixture_manifest_v0_1"
    assert manifest["fixture_count"] == 10
    assert len(fixtures) == 10

    for fixture in fixtures:
        path = INVALID_DIR / fixture["fixture_file"]
        assert path.exists(), f"Missing invalid fixture: {path}"
        assert fixture["expected_checker_result"] == "FAIL"
        assert fixture["expected_failures"]


def test_invalid_fixtures_fail_with_expected_error_codes():
    manifest = json.loads(INVALID_MANIFEST.read_text(encoding="utf-8"))

    for fixture in manifest["fixtures"]:
        path = INVALID_DIR / fixture["fixture_file"]
        result = checker.check_bundle_path(path)

        assert not result["ok"], f"{fixture['fixture_file']} unexpectedly passed"

        actual_codes = {error["code"] for error in result["errors"]}
        expected_codes = set(fixture["expected_failures"])
        missing = expected_codes - actual_codes

        assert not missing, (
            f"{fixture['fixture_file']} missing expected failures: "
            f"{sorted(missing)}; actual={sorted(actual_codes)}"
        )


def test_invalid_manifest_check_passes_as_expected_failure_harness():
    result = checker.check_invalid_manifest(INVALID_MANIFEST)
    assert result["ok"], json.dumps(result, indent=2)


def test_cli_valid_bundle_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True


def test_cli_invalid_fixture_exits_nonzero():
    invalid_fixture = INVALID_DIR / "invalid_expansion_missing_authority_evidence_v0_1.json"
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(invalid_fixture)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 1
    payload = json.loads(completed.stdout)
    assert payload["ok"] is False
    assert "AUTHORITY_REF_MISSING" in {error["code"] for error in payload["errors"]}


def test_cli_invalid_manifest_exits_zero_when_expected_failures_match():
    completed = subprocess.run(
        [
            sys.executable,
            str(TOOL_PATH),
            "--invalid-manifest",
            "--manifest-path",
            str(INVALID_MANIFEST),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["ok"] is True
