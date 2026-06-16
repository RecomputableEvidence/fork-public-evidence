import copy
import json
from collections import Counter
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_2_2.schema.json"
EXAMPLE_DIR = ROOT / "examples" / "claim_boundary_contract_v0_2_2"

EXAMPLES = [
    "runtime_blocked_tool_call_record.json",
    "benchmark_execution_record.json",
    "limited_internal_review_eligibility_boundary.json",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator():
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def example(filename: str):
    return load_json(EXAMPLE_DIR / filename)


def duplicate_values(values):
    counts = Counter(v for v in values if v)
    return sorted(value for value, count in counts.items() if count > 1)


def relational_errors(instance: dict):
    errors = []

    if instance.get("cbc_version") != "CBC_v0_2_2":
        errors.append("wrong CBC version")

    non_claim_ids = [
        item.get("non_claim_id")
        for item in instance.get("non_claims", [])
        if isinstance(item, dict)
    ]
    duplicate_non_claims = duplicate_values(non_claim_ids)
    if duplicate_non_claims:
        errors.append(f"duplicate non_claim_id values: {duplicate_non_claims}")

    received = instance.get("upstream_claims_received", [])
    relied = instance.get("upstream_claims_relied_on", [])
    rejected = instance.get("upstream_claims_rejected", [])

    received_ids = [
        claim.get("claim_id")
        for claim in received
        if isinstance(claim, dict)
    ]
    duplicate_received = duplicate_values(received_ids)
    if duplicate_received:
        errors.append(f"duplicate upstream_claims_received claim_id values: {duplicate_received}")

    received_id_set = set(received_ids)
    relied_ids = {
        claim.get("claim_id")
        for claim in relied
        if isinstance(claim, dict) and claim.get("claim_id")
    }
    rejected_ids = {
        claim.get("claim_id")
        for claim in rejected
        if isinstance(claim, dict) and claim.get("claim_id")
    }

    unknown_relied = relied_ids - received_id_set
    if unknown_relied:
        errors.append(f"upstream_claims_relied_on not received: {sorted(unknown_relied)}")

    unknown_rejected = rejected_ids - received_id_set
    if unknown_rejected:
        errors.append(f"upstream_claims_rejected not received: {sorted(unknown_rejected)}")

    overlap = relied_ids & rejected_ids
    if overlap:
        errors.append(f"upstream claims cannot be both relied on and rejected: {sorted(overlap)}")

    current_non_claim_id_set = set(non_claim_ids)
    missing_preserved = set()
    for claim in relied:
        if isinstance(claim, dict):
            missing_preserved.update(
                set(claim.get("preserved_non_claim_ids", [])) - current_non_claim_id_set
            )
    if missing_preserved:
        errors.append(
            "upstream preserved_non_claim_ids not represented in current CBC non_claims: "
            f"{sorted(missing_preserved)}"
        )

    return errors


def validate_cbc(instance: dict):
    schema_errors = sorted(validator().iter_errors(instance), key=lambda err: err.path)
    relation_errors = relational_errors(instance)
    return schema_errors, relation_errors


@pytest.mark.parametrize("filename", EXAMPLES)
def test_examples_validate(filename):
    instance = example(filename)
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_all_examples_are_v0_2_2():
    for filename in EXAMPLES:
        assert example(filename)["cbc_version"] == "CBC_v0_2_2"


def test_claim_ids_unique_across_examples():
    claim_ids = [example(filename)["claim_id"] for filename in EXAMPLES]
    assert duplicate_values(claim_ids) == []


def test_duplicate_upstream_claims_received_claim_ids_fail():
    instance = example("limited_internal_review_eligibility_boundary.json")
    received = instance.setdefault("upstream_claims_received", [])

    if received:
        duplicate = copy.deepcopy(received[0])
    else:
        duplicate = copy.deepcopy(instance["upstream_claims_relied_on"][0])

    received.append(copy.deepcopy(duplicate))
    received.append(copy.deepcopy(duplicate))

    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("duplicate upstream_claims_received claim_id" in error for error in relation_errors)


def test_inherited_upstream_nonclaims_must_remain_represented_in_downstream_cbc():
    instance = example("limited_internal_review_eligibility_boundary.json")
    preserved = instance["upstream_claims_relied_on"][0]["preserved_non_claim_ids"]
    assert preserved, "fixture should contain preserved upstream non-claim IDs"

    removed_id = preserved[0]
    instance["non_claims"] = [
        item
        for item in instance["non_claims"]
        if item["non_claim_id"] != removed_id
    ]

    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("upstream preserved_non_claim_ids not represented" in error for error in relation_errors)


def test_duplicate_non_claim_ids_fail_relational_validation():
    instance = example("benchmark_execution_record.json")
    instance["non_claims"].append(copy.deepcopy(instance["non_claims"][0]))

    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("duplicate non_claim_id" in error for error in relation_errors)


def test_benchmark_execution_record_does_not_use_pass_filename():
    assert "pass" not in "benchmark_execution_record.json".lower()


def test_benchmark_execution_record_keeps_deployment_non_claims():
    instance = example("benchmark_execution_record.json")
    ids = {
        item["non_claim_id"]
        for item in instance["non_claims"]
    }
    assert "NC_DEPLOYMENT_READINESS" in ids
    assert "NC_GENERAL_SAFETY" in ids
    assert "NC_OOD_SAFETY" in ids
    assert "NC_PRODUCTION_PERFORMANCE" in ids
