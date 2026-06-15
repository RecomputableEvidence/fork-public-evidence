import copy
import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_1.schema.json"
EXAMPLE_PATHS = [
    ROOT / "examples" / "claim_boundary_contract" / "runtime_blocked_tool_call.json",
    ROOT / "examples" / "claim_boundary_contract" / "eval_benchmark_pass.json",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def schema():
    return load_json(SCHEMA_PATH)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_claim_boundary_contract_examples_validate(schema, example_path):
    instance = load_json(example_path)
    jsonschema.Draft202012Validator(schema).validate(instance)


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_pass_status_is_scoped_to_record_integrity_and_boundary_structure(example_path):
    instance = load_json(example_path)
    assert instance["verification_status"] == "PASS"
    assert instance["verification_scope"] == "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"


@pytest.mark.parametrize("example_path", EXAMPLE_PATHS)
def test_non_claims_must_travel_downstream(example_path):
    instance = load_json(example_path)
    assert instance["inheritance_policy"]["non_claims_must_travel"] is True
    assert (
        instance["inheritance_policy"][
            "downstream_may_drop_non_claims_without_new_explicit_claim"
        ]
        is False
    )
    assert instance["non_claims"], "CBC examples must include explicit non-claims"
    for non_claim in instance["non_claims"]:
        assert non_claim["must_travel_downstream"] is True


def test_missing_non_claims_is_rejected(schema):
    instance = load_json(EXAMPLE_PATHS[0])
    broken = copy.deepcopy(instance)
    del broken["non_claims"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


def test_invalid_verification_status_is_rejected(schema):
    instance = load_json(EXAMPLE_PATHS[0])
    broken = copy.deepcopy(instance)
    broken["verification_status"] = "COMPLIANT"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


def test_invalid_evidence_hash_is_rejected(schema):
    instance = load_json(EXAMPLE_PATHS[0])
    broken = copy.deepcopy(instance)
    broken["evidence_refs"][0]["sha256"] = "not-a-sha256"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)


def test_cannot_drop_non_claims_without_new_explicit_claim(schema):
    instance = load_json(EXAMPLE_PATHS[0])
    broken = copy.deepcopy(instance)
    broken["inheritance_policy"][
        "downstream_may_drop_non_claims_without_new_explicit_claim"
    ] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(broken)