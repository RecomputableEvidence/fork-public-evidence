from pathlib import Path
import importlib.util
import json

from jsonschema import Draft202012Validator


def load_module(path_text, name):
    path = Path(path_text)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_csh_scaffold_is_structurally_valid_and_blocks_unfrozen_execution():
    checker = load_module("tools/check_cross_system_claim_handoff_v0_1.py", "csh_checker")
    result = checker.evaluate(Path.cwd(), require_complete_baseline=False)
    assert result["failed"] == 0


def test_clean_classifier_fixture_has_no_unsupported_inheritance_events():
    classifier = load_module("tools/classify_unsupported_inheritance_v0_1.py", "csh_classifier_clean")
    item = json.loads(Path("tests/fixtures/csh/classifier_input_clean.json").read_text(encoding="utf-8"))
    result = classifier.classify(item)
    assert result["event_count"] == 0


def test_unsupported_classifier_fixture_emits_event_level_findings():
    classifier = load_module("tools/classify_unsupported_inheritance_v0_1.py", "csh_classifier_bad")
    item = json.loads(Path("tests/fixtures/csh/classifier_input_unsupported.json").read_text(encoding="utf-8"))
    result = classifier.classify(item)
    event_types = {event["event_type"] for event in result["events"]}
    assert "claim_expansion_without_boundary" in event_types
    assert "material_non_claim_loss" in event_types
    assert "authority_inheritance" in event_types
    assert "unresolved_reference_collapse" in event_types
    assert "evidence_reference_promotion" in event_types
    assert "verification_upgrade" in event_types
    assert "aggregate_collapse" in event_types


def test_classifier_outputs_validate_against_schema():
    classifier = load_module("tools/classify_unsupported_inheritance_v0_1.py", "csh_classifier_schema")
    item = json.loads(Path("tests/fixtures/csh/classifier_input_unsupported.json").read_text(encoding="utf-8"))
    result = classifier.classify(item)
    schema = json.loads(Path("schemas/unsupported_inheritance_classification_v0_1.schema.json").read_text(encoding="utf-8"))
    assert not list(Draft202012Validator(schema).iter_errors(result))
