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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["command_completed"] is True
    assert payload["runner"]["mode"] == "single_bundle_check"
    assert payload["structural_result"]["structural_protocol_passed"] is True
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["command_completed"] is True
    assert payload["structural_result"]["structural_protocol_passed"] is False
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["command_completed"] is True
    assert payload["runner"]["mode"] == "invalid_fixture_harness"
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    assert payload["harness_result"]["fixture_count"] == 20
    assert payload["limitations"]["scope"] == "NEGATIVE_TEST_HARNESS_ONLY"
    assert payload["limitations"]["does_not_indicate_structural_conformance"] is True

    fixture_results = payload["harness_result"]["fixture_results"]
    assert fixture_results
    assert all(item["checker_structural_protocol_passed"] is False for item in fixture_results)
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["command_completed"] is True
    assert payload["structural_result"]["structural_protocol_passed"] is True
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
    assert payload["runner"]["command_completed"] is True
    assert payload["structural_result"]["structural_protocol_passed"] is False
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["command_completed"] is True
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    assert payload["harness_result"]["fixture_count"] == 20
    assert payload["limitations"]["scope"] == "NEGATIVE_TEST_HARNESS_ONLY"
    assert payload["limitations"]["does_not_indicate_structural_conformance"] is True

    fixture_results = payload["harness_result"]["fixture_results"]
    assert fixture_results
    assert all("ok" not in item for item in fixture_results)
    assert all("checker_ok" not in item for item in fixture_results)
    assert all("expected_failures_observed" in item for item in fixture_results)
    assert all("checker_structural_protocol_passed" in item for item in fixture_results)

def test_cli_valid_bundle_carries_v014_output_boundary_lock():
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["safe_to_automate"] is False
    assert payload["automation_interpretation_required"] is True
    assert payload["runner"]["command_completed"] is True
    assert payload["runner"]["runner_outcome"] == "completed"
    assert payload["structural_result"]["structural_protocol_passed"] is True
    assert payload["structural_result"]["limitations"]["safe_to_automate"] is False
    assert payload["structural_result"]["limitations"]["does_not_validate_approval"] is True
    assert payload["structural_result"]["limitations"]["does_not_validate_actual_non_use"] is True
    assert "APPROVAL" in payload["structural_result"]["limitations"]["do_not_map_to"]
    assert "EVIDENCE_SUFFICIENCY" in payload["limitations"]["do_not_map_to"]


def test_cli_invalid_manifest_carries_v014_harness_boundary_lock():
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
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["result_kind"] == "INVALID_FIXTURE_HARNESS"
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    assert payload["harness_result"]["limitations"]["scope"] == "HARNESS_RESULT_ONLY"
    assert payload["harness_result"]["limitations"]["safe_to_automate"] is False
    assert "COMPLIANCE" in payload["harness_result"]["limitations"]["do_not_map_to"]
    assert payload["limitations"]["scope"] == "NEGATIVE_TEST_HARNESS_ONLY"

    first_fixture = payload["harness_result"]["fixture_results"][0]
    assert first_fixture["limitations"]["scope"] == "INVALID_FIXTURE_RESULT_ONLY"
    assert first_fixture["findings"]
    assert first_fixture["findings"][0]["check_version"] == "0.1.5"
    assert first_fixture["findings"][0]["severity"] == "EXPECTED_STRUCTURAL_FAILURE"


def test_cli_legacy_output_is_disabled_in_v014():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE), "--legacy-output", "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 2, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)

    assert "ok" not in payload
    assert payload["result_kind"] == "LEGACY_OUTPUT_DISABLED"
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["runner"]["runner_outcome"] == "blocked"
    assert payload["structural_result"] is None
    assert payload["limitations"]["legacy_output_disabled"] is True
    assert payload["limitations"]["safe_to_automate"] is False
    assert payload["limitations"]["automation_interpretation_required"] is True

def test_cli_v014_removes_ambiguous_compatibility_aliases():
    valid = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE), "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert valid.returncode == 0, valid.stdout + valid.stderr
    valid_payload = json.loads(valid.stdout)

    assert "ok" not in valid_payload
    assert valid_payload["runner"]["command_completed"] is True
    assert valid_payload["runner"]["command_completed"] is True
    assert valid_payload["structural_result"]["limitations"]["safe_to_automate"] is False

    harness = subprocess.run(
        [sys.executable, str(TOOL_PATH), "--invalid-manifest", "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert harness.returncode == 0, harness.stdout + harness.stderr
    harness_payload = json.loads(harness.stdout)

    assert "ok" not in harness_payload
    assert harness_payload["runner"]["command_completed"] is True
    assert harness_payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert harness_payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert harness_payload["harness_result"]["limitations"]["safe_to_automate"] is False

    legacy = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE), "--legacy-output", "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert legacy.returncode == 2, legacy.stdout + legacy.stderr
    legacy_payload = json.loads(legacy.stdout)

    assert "ok" not in legacy_payload
    assert legacy_payload["runner"]["command_completed"] is True
    assert legacy_payload["result_kind"] == "LEGACY_OUTPUT_DISABLED"


def test_cli_v015_output_contract_wrapper_preserves_main():
    tool_text = TOOL_PATH.read_text(encoding="utf-8")
    assert "def _v014_main(" in tool_text
    assert "def main(" in tool_text
    assert "V015_OUTPUT_CONTRACT_WRAPPER_START" in tool_text


def test_cli_v015_output_contract_removes_legacy_public_keys_recursively():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(VALID_BUNDLE), "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)

    banned = {
        "ok",
        "runner_succeeded",
        "all_invalid_fixtures_rejected",
        "structurally_conformant",
        "checker_structurally_conformant",
    }

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                assert key not in banned
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["structural_result"]["structural_protocol_passed"] is True
    assert payload["limitations"]["safe_to_automate"] is False
    assert payload["limitations"]["automation_interpretation_required"] is True
    assert payload["limitations"]["limitations_code"] == "LIMIT_STRUCTURAL_SYNTHETIC_PROTOCOL_ONLY_V0_1_5"
    assert "APPROVAL" in payload["limitations"]["do_not_map_to"]
    assert "COMPLIANCE" in payload["limitations"]["do_not_map_to"]
    assert "LEGAL_CHAIN_OF_CUSTODY" in payload["limitations"]["do_not_map_to"]


def test_cli_v015_invalid_manifest_contract_shape():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), "--invalid-manifest", "--pretty"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["output_semantics_version"] == "0.1.5"
    assert payload["result_kind"] == "INVALID_FIXTURE_HARNESS"
    assert payload["structural_result"] is None
    assert payload["harness_result"]["all_invalid_fixtures_produced_expected_structural_failures"] is True
    assert payload["harness_result"]["does_not_indicate_structural_conformance"] is True
    first_fixture = payload["harness_result"]["fixture_results"][0]
    assert first_fixture["checker_structural_protocol_passed"] is False
    assert first_fixture["limitations"]["limitations_code"] == "LIMIT_STRUCTURAL_SYNTHETIC_PROTOCOL_ONLY_V0_1_5"
