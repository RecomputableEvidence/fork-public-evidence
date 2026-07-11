from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_authority_state_invariance_v0_1.py"
FIXTURES = ROOT / "tests/fixtures/authority-state-invariance"
SCHEMAS = [
    ROOT / "schemas/validity_state_transition_event_v0_1.schema.json",
    ROOT / "schemas/authority_transition_event_v0_1.schema.json",
    ROOT / "schemas/reliance_event_v0_1.schema.json",
    ROOT / "schemas/reliance_authority_misalignment_event_v0_1.schema.json",
]


def load_checker():
    spec = importlib.util.spec_from_file_location("asi_checker", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_schemas_are_valid_draft_2020_12():
    for path in SCHEMAS:
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_schema_samples_validate():
    mapping = {
        "validity_state_transition_event_v0_1.schema.json": "validity_state_transition_event.json",
        "authority_transition_event_v0_1.schema.json": "authority_transition_event.json",
        "reliance_event_v0_1.schema.json": "reliance_event.json",
        "reliance_authority_misalignment_event_v0_1.schema.json": "reliance_authority_misalignment_event.json",
    }
    for schema_path in SCHEMAS:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        artifact = json.loads((FIXTURES / "schema-samples" / mapping[schema_path.name]).read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(artifact))
        assert not errors, [error.message for error in errors]


def test_repository_harness_matches_all_declared_expectations():
    result = load_checker().evaluate_repository(ROOT)
    assert result["harness_passed"], result["harness"]
    assert result["valid_case_count"] >= 8
    assert result["invalid_case_count"] >= 12


def test_valid_fixtures_are_structurally_conformant():
    checker = load_checker()
    for path in sorted((FIXTURES / "valid").glob("case_*.json")):
        result = checker.evaluate_case(ROOT, path)
        assert result["structurally_conformant"], (path, result["errors"])
        assert result["error_codes"] == []


def test_invalid_fixtures_are_rejected_with_exact_codes():
    checker = load_checker()
    for path in sorted((FIXTURES / "invalid").glob("case_*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        result = checker.evaluate_case(ROOT, path)
        assert not result["structurally_conformant"], path
        assert result["error_codes"] == sorted(case["expected"]["error_codes"]), (path, result["error_codes"])


def test_not_evaluable_does_not_create_governance_failure():
    checker = load_checker()
    path = next((FIXTURES / "valid").glob("*governance_not_evaluable*.json"))
    result = checker.evaluate_case(ROOT, path)
    emitted = result["emitted_misalignment_events"][0]
    assert emitted["governance_profile_evaluation"] == "NOT_EVALUABLE"
    assert "GOVERNANCE_PROFILE" not in emitted["misalignment_dimensions"]
    assert emitted["structural_misalignment_detected"] is False


def test_lineage_metrics_do_not_count_repeated_references_as_independent_roots():
    checker = load_checker()
    path = next((FIXTURES / "valid").glob("*shared_root*.json"))
    result = checker.evaluate_case(ROOT, path)
    metrics = result["emitted_misalignment_events"][0]["lineage_metrics"]
    assert metrics["apparent_supporting_reference_count"] == 5
    assert metrics["independently_validated_root_count"] == 1
    assert metrics["pci_count"] == 4
    assert metrics["pci_ratio"] == 5.0


def test_non_claim_loss_is_a_component_misalignment():
    checker = load_checker()
    path = next((FIXTURES / "invalid").glob("*non_claim_loss*.json"))
    result = checker.evaluate_case(ROOT, path)
    emitted = result["emitted_misalignment_events"][0]
    assert "NON_CLAIM_LOSS" in result["error_codes"]
    assert "NON_CLAIM_SURVIVAL" in emitted["misalignment_dimensions"]


def test_cli_harness_exits_zero_and_emits_json():
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["harness_passed"] is True


def test_single_invalid_fixture_exits_nonzero():
    path = next((FIXTURES / "invalid").glob("case_*.json"))
    completed = subprocess.run(
        [sys.executable, str(CHECKER), str(path.relative_to(ROOT)), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1


def test_spec_and_experiment_preserve_boundary_language():
    spec = (ROOT / "docs/specifications/AUTHORITY_STATE_INVARIANCE_AND_TRANSITION_MODEL_v0_1.md").read_text(encoding="utf-8")
    experiment = (ROOT / "docs/experiments/HISTORICAL_AUTHORITY_ACCRETION_EXPERIMENT_DRAFT_v0_1.md").read_text(encoding="utf-8")
    for invariant in range(1, 13):
        assert f"ASI-{invariant:03d}" in spec
    assert "does not assert truth" in spec
    assert "fork_enforcement_action: NONE" in spec
    assert "Cross-System Claim Handoff v0.1" in experiment
    assert "MUST NOT modify or delay" in experiment
    assert "not admitted" in experiment.lower()
