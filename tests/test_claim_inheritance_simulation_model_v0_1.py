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


def error_codes(result):
    return {error["code"] for error in result["errors"]}


def test_valid_bundle_passes():
    result = checker.check_bundle_path(VALID_BUNDLE)
    assert result["ok"], json.dumps(result, indent=2)


def test_invalid_manifest_exists_and_lists_fixtures():
    manifest = json.loads(INVALID_MANIFEST.read_text(encoding="utf-8"))
    fixtures = manifest["fixtures"]

    assert manifest["manifest_id"] == "claim_inheritance_invalid_fixture_manifest_v0_1"
    assert manifest["fixture_count"] == 20
    assert len(fixtures) == 20

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

        actual_codes = error_codes(result)
        expected_codes = set(fixture["expected_failures"])
        missing = expected_codes - actual_codes

        assert not missing, (
            f"{fixture['fixture_file']} missing expected failures: "
            f"{sorted(missing)}; actual={sorted(actual_codes)}"
        )


def test_invalid_manifest_check_passes_as_expected_failure_harness():
    result = checker.check_invalid_manifest(INVALID_MANIFEST)
    assert result["ok"], json.dumps(result, indent=2)


def test_schema_extra_property_fixture_emits_schema_failure():
    path = INVALID_DIR / "invalid_schema_extra_property_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "SCHEMA_VALIDATION_FAILED" in codes
    assert "UNEXPECTED_FIELD" in codes


def test_schema_missing_required_fixture_emits_schema_failure():
    path = INVALID_DIR / "invalid_schema_missing_required_field_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "SCHEMA_VALIDATION_FAILED" in codes
    assert "MISSING_REQUIRED_FIELD" in codes


def test_non_claim_tampering_fixture_fails():
    path = INVALID_DIR / "invalid_non_claim_tampered_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "NON_CLAIM_TAMPERING_DETECTED" in codes
    assert "NON_CLAIM_SILENTLY_OMITTED" in codes
    assert "MAPPING_INCOMPLETE" in codes


def test_partial_non_claim_mapping_fixture_fails():
    path = INVALID_DIR / "invalid_partial_non_claim_mapping_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "NON_CLAIM_SILENTLY_OMITTED" in codes
    assert "MAPPING_INCOMPLETE" in codes


def test_placeholder_ref_fixture_fails():
    path = INVALID_DIR / "invalid_empty_authority_ref_placeholder_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "PLACEHOLDER_REF_DETECTED" in codes
    assert "AUTHORITY_REF_MISSING" in codes
    assert "EVIDENCE_REF_MISSING" in codes
    assert "MAPPING_INCOMPLETE" in codes


def test_structurally_reachable_without_resolution_attempt_fails():
    path = INVALID_DIR / "invalid_structurally_reachable_with_resolution_not_attempted_v0_1.json"
    result = checker.check_bundle_path(path)
    codes = error_codes(result)

    assert not result["ok"]
    assert "RESOLUTION_ATTEMPT_STATE_CONTRADICTION" in codes
    assert "MAPPING_INCOMPLETE" in codes


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

    assert "ok" not in payload
    assert payload["result_kind"] == "STRUCTURAL_BUNDLE_CHECK"
    assert payload["output_semantics_version"] == "0.1.3"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["runner"]["mode"] == "single_bundle_check"
    assert payload["structural_result"]["structurally_conformant"] is True
    assert payload["structural_result"]["error_count"] == 0
    assert payload["harness_result"] is None
    assert payload["limitations"]["does_not_validate_truth"] is True
    assert payload["limitations"]["does_not_validate_compliance"] is True
    assert payload["limitations"]["does_not_validate_authority"] is True
    assert payload["limitations"]["does_not_validate_evidence_sufficiency"] is True
    assert payload["limitations"]["does_not_authorize_production_use"] is True

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

    assert "ok" not in payload
    assert payload["result_kind"] == "STRUCTURAL_BUNDLE_CHECK"
    assert payload["output_semantics_version"] == "0.1.3"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["structural_result"]["structurally_conformant"] is False
    assert payload["structural_result"]["error_count"] > 0
    assert payload["harness_result"] is None
    assert payload["limitations"]["does_not_validate_truth"] is True

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

    assert "ok" not in payload
    assert payload["result_kind"] == "INVALID_FIXTURE_HARNESS"
    assert payload["output_semantics_version"] == "0.1.3"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["runner"]["mode"] == "invalid_fixture_harness"
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_rejected"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    assert payload["harness_result"]["fixture_count"] == 20
    assert payload["limitations"]["scope"] == "NEGATIVE_TEST_HARNESS_ONLY"
    assert payload["limitations"]["does_not_indicate_structural_conformance"] is True

    fixture_results = payload["harness_result"]["fixture_results"]
    assert fixture_results
    assert all(item["checker_structurally_conformant"] is False for item in fixture_results)
    assert all(item["expected_failures_observed"] is True for item in fixture_results)
    assert all("ok" not in item for item in fixture_results)
    assert all("checker_ok" not in item for item in fixture_results)

def assert_fixture_codes(name, expected, forbidden=()):
    result = checker.check_bundle_path(INVALID_DIR / name)
    codes = error_codes(result)

    assert not result["ok"], f"{name} unexpectedly passed"
    assert set(expected).issubset(codes), (
        f"{name} missing expected codes {sorted(set(expected) - codes)}; "
        f"actual={sorted(codes)}"
    )
    assert not set(forbidden).intersection(codes), (
        f"{name} produced forbidden collateral errors "
        f"{sorted(set(forbidden).intersection(codes))}; actual={sorted(codes)}"
    )

def test_declared_non_usage_with_structural_use_fails_cleanly():
    assert_fixture_codes(
        "invalid_declared_non_usage_with_structural_use_v0_1.json",
        {
            "CLAIM_NON_USAGE_DECLARED_WITH_STRUCTURAL_USE",
            "MAPPING_INCOMPLETE",
        },
        forbidden={
            "SCHEMA_VALIDATION_FAILED",
            "NON_CLAIM_SILENTLY_OMITTED",
        },
    )


def test_non_claim_preserved_and_dropped_contradiction_fails_cleanly():
    assert_fixture_codes(
        "invalid_non_claim_preserved_and_dropped_v0_1.json",
        {
            "NON_CLAIM_PRESERVED_AND_DROPPED_CONTRADICTION",
            "NON_CLAIM_DROPPED",
            "MAPPING_INCOMPLETE",
        },
        forbidden={
            "SCHEMA_VALIDATION_FAILED",
            "NON_CLAIM_SILENTLY_OMITTED",
        },
    )


def test_malformed_structural_outcome_token_fails_cleanly():
    assert_fixture_codes(
        "invalid_malformed_structural_outcome_token_v0_1.json",
        {
            "MALFORMED_STRUCTURAL_OUTCOME_TOKEN",
            "CONTROLLED_VOCABULARY_VALUE_UNKNOWN",
        },
        forbidden={
            "SCHEMA_VALIDATION_FAILED",
            "MAPPING_INCOMPLETE",
            "NON_CLAIM_SILENTLY_OMITTED",
        },
    )


def test_tbd_placeholder_ref_fixture_fails_cleanly():
    assert_fixture_codes(
        "invalid_placeholder_ref_tbd_v0_1.json",
        {
            "PLACEHOLDER_REF_DETECTED",
            "AUTHORITY_REF_MISSING",
            "EVIDENCE_REF_MISSING",
            "MAPPING_INCOMPLETE",
        },
        forbidden={
            "SCHEMA_VALIDATION_FAILED",
            "NON_CLAIM_SILENTLY_OMITTED",
        },
    )

def test_cli_valid_bundle_uses_v013_output_semantics():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE), "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)

    assert "ok" not in payload
    assert payload["result_kind"] == "STRUCTURAL_BUNDLE_CHECK"
    assert payload["output_semantics_version"] == "0.1.3"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["structural_result"]["structurally_conformant"] is True
    assert payload["harness_result"] is None
    assert payload["limitations"]["scope"] == "STRUCTURAL_SYNTHETIC_PROTOCOL_CHECK_ONLY"
    assert payload["limitations"]["does_not_validate_truth"] is True
    assert payload["limitations"]["does_not_validate_compliance"] is True
    assert payload["limitations"]["does_not_validate_authority"] is True
    assert payload["limitations"]["does_not_validate_evidence_sufficiency"] is True
    assert payload["limitations"]["does_not_authorize_production_use"] is True


def test_cli_invalid_fixture_uses_v013_structural_failure_semantics():
    invalid_fixture = INVALID_DIR / "invalid_malformed_structural_outcome_token_v0_1.json"
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(invalid_fixture), "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode != 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)

    assert "ok" not in payload
    assert payload["result_kind"] == "STRUCTURAL_BUNDLE_CHECK"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["structural_result"]["structurally_conformant"] is False
    assert payload["structural_result"]["error_count"] > 0
    assert payload["limitations"]["does_not_validate_truth"] is True


def test_cli_invalid_manifest_separates_harness_success_from_structural_conformance():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), "--invalid-manifest", "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)

    assert "ok" not in payload
    assert payload["result_kind"] == "INVALID_FIXTURE_HARNESS"
    assert payload["output_semantics_version"] == "0.1.3"
    assert payload["runner"]["runner_succeeded"] is True
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_rejected"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    assert payload["harness_result"]["fixture_count"] == 20
    assert payload["limitations"]["scope"] == "NEGATIVE_TEST_HARNESS_ONLY"
    assert payload["limitations"]["does_not_indicate_structural_conformance"] is True

    fixture_results = payload["harness_result"]["fixture_results"]
    assert fixture_results
    assert all("ok" not in item for item in fixture_results)
    assert all("checker_ok" not in item for item in fixture_results)
    assert all("expected_failures_observed" in item for item in fixture_results)
    assert all("checker_structurally_conformant" in item for item in fixture_results)
