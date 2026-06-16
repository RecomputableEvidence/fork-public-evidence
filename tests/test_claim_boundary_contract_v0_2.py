import copy
import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_2.schema.json"
EXAMPLE_PATHS = [
    ROOT / "examples" / "claim_boundary_contract_v0_2" / "runtime_blocked_tool_call.json",
    ROOT / "examples" / "claim_boundary_contract_v0_2" / "eval_benchmark_pass.json",
]

FULL_SCOPE = "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schema():
    return load_json(SCHEMA_PATH)


def validate(schema, instance):
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    assert not errors, "\n".join(
        f"{'/'.join(map(str, error.path))}: {error.message}" for error in errors
    )


def assert_upstream_relied_on_subset_of_received(instance):
    received = instance.get("upstream_claims_received", [])
    relied_on = instance.get("upstream_claims_relied_on", [])

    assert isinstance(received, list)
    assert isinstance(relied_on, list)

    received_ids = set()
    for item in received:
        assert isinstance(item, dict)
        assert "claim_id" in item
        received_ids.add(item["claim_id"])

    relied_on_ids = set()
    for item in relied_on:
        assert isinstance(item, dict)
        assert "claim_id" in item
        relied_on_ids.add(item["claim_id"])

    assert relied_on_ids.issubset(received_ids)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_examples_validate_against_cbc_v0_2_schema(schema, example_path):
    instance = load_json(example_path)
    validate(schema, instance)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_examples_identify_cbc_version(example_path):
    instance = load_json(example_path)
    assert instance["claim_boundary_contract_version"] == "0.2"


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_pass_status_requires_full_boundary_scope(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    broken["verification_status"] = "PASS"
    broken["verification_scope"] = "RECORD_INTEGRITY_ONLY"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_missing_cbc_version_rejected(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    del broken["claim_boundary_contract_version"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_wrong_cbc_version_rejected(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    broken["claim_boundary_contract_version"] = "0.1"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_downstream_may_narrow_must_be_true(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    broken["inheritance_policy"]["downstream_may_narrow"] = False
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_sealed_by_required(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    del broken["sealed_at"]["sealed_by"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_non_claims_must_still_travel_downstream(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    assert broken["non_claims"]
    broken["non_claims"][0]["must_travel_downstream"] = False
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_additional_properties_rejected(schema, example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    broken["fork_should_reject_silent_field_creep"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_upstream_claims_relied_on_subset_of_received(example_path):
    instance = load_json(example_path)
    assert_upstream_relied_on_subset_of_received(instance)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_upstream_claims_relied_on_subset_checker_rejects_unknown_claim(example_path):
    instance = load_json(example_path)
    broken = copy.deepcopy(instance)
    broken.setdefault("upstream_claims_relied_on", []).append(
        {
            "claim_id": "not_received_by_this_cbc",
            "reason": "adversarial fixture",
        }
    )
    with pytest.raises(AssertionError):
        assert_upstream_relied_on_subset_of_received(broken)
