import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_2_1.schema.json"
EXAMPLE_DIR = ROOT / "examples" / "claim_boundary_contract_v0_2_1"
EXAMPLE_NAMES = [
    "runtime_blocked_tool_call_record.json",
    "benchmark_execution_record.json",
    "limited_internal_review_eligibility_boundary.json",
]
FULL_SCOPE = "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_validator():
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def example(name: str):
    return load_json(EXAMPLE_DIR / name)


def relational_errors(instance: dict):
    errors = []

    received = {
        claim.get("claim_id")
        for claim in instance.get("upstream_claims_received", [])
        if isinstance(claim, dict) and claim.get("claim_id")
    }
    relied = {
        claim.get("claim_id")
        for claim in instance.get("upstream_claims_relied_on", [])
        if isinstance(claim, dict) and claim.get("claim_id")
    }
    rejected = {
        claim.get("claim_id")
        for claim in instance.get("upstream_claims_rejected", [])
        if isinstance(claim, dict) and claim.get("claim_id")
    }

    if relied - received:
        errors.append(f"upstream_claims_relied_on not received: {sorted(relied - received)}")
    if rejected - received:
        errors.append(f"upstream_claims_rejected not received: {sorted(rejected - received)}")
    if relied & rejected:
        errors.append(f"upstream claim cannot be both relied on and rejected: {sorted(relied & rejected)}")

    non_claim_ids = [
        item.get("non_claim_id")
        for item in instance.get("non_claims", [])
        if isinstance(item, dict)
    ]
    if len(non_claim_ids) != len(set(non_claim_ids)):
        errors.append("duplicate non_claim_id")

    positive_statement_ids = [
        item.get("statement_id")
        for item in instance.get("positive_claims", [])
        if isinstance(item, dict)
    ]
    if len(positive_statement_ids) != len(set(positive_statement_ids)):
        errors.append("duplicate positive_claim statement_id")

    return errors


def validate_cbc(instance: dict):
    validator = schema_validator()
    schema_errors = sorted(validator.iter_errors(instance), key=lambda err: err.path)
    relation_errors = relational_errors(instance)
    return schema_errors, relation_errors


@pytest.mark.parametrize("filename", EXAMPLE_NAMES)
def test_cbc_v0_2_1_examples_validate(filename):
    instance = example(filename)
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_pass_requires_full_verification_scope():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["verification_status"] = "PASS"
    instance["verification_scope"] = "RECORD_INTEGRITY_ONLY"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_pass_with_not_checked_scope_rejected():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["verification_status"] = "PASS"
    instance["verification_scope"] = "NOT_CHECKED"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_not_checked_requires_not_checked_scope():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["verification_status"] = "NOT_CHECKED"
    instance["verification_scope"] = FULL_SCOPE
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_non_claims_must_travel_downstream():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["non_claims"][0]["must_travel_downstream"] = False
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_upstream_claim_requires_claim_id():
    instance = example("limited_internal_review_eligibility_boundary.json")
    del instance["upstream_claims_relied_on"][0]["claim_id"]
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_upstream_relied_on_must_be_received():
    instance = example("limited_internal_review_eligibility_boundary.json")
    instance["upstream_claims_relied_on"][0]["claim_id"] = "missing_upstream_claim"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("upstream_claims_relied_on not received" in error for error in relation_errors)


def test_upstream_rejected_must_be_received():
    instance = example("limited_internal_review_eligibility_boundary.json")
    instance["upstream_claims_rejected"] = [copy.deepcopy(instance["upstream_claims_received"][0])]
    instance["upstream_claims_rejected"][0]["claim_id"] = "missing_rejected_claim"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("upstream_claims_rejected not received" in error for error in relation_errors)


def test_upstream_claim_cannot_be_both_relied_and_rejected():
    instance = example("limited_internal_review_eligibility_boundary.json")
    instance["upstream_claims_rejected"] = [copy.deepcopy(instance["upstream_claims_relied_on"][0])]
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("both relied on and rejected" in error for error in relation_errors)


def test_claim_ids_unique_across_examples():
    seen = set()
    for filename in EXAMPLE_NAMES:
        claim_id = example(filename)["claim_id"]
        assert claim_id not in seen, f"Duplicate claim_id: {claim_id}"
        seen.add(claim_id)


def test_sealed_by_name_must_be_non_empty():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["sealed_at"]["sealed_by"]["name"] = ""
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_sealed_by_type_must_be_valid_enum():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["sealed_at"]["sealed_by"]["type"] = "UNVERIFIED_PERSONA"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_issuer_semantics_authority_mode_is_enum():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["issuer_semantics_authority"]["mode"] = "legal_dept_freeform"
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_runtime_policy_association_non_claim_present():
    instance = example("runtime_blocked_tool_call_record.json")
    non_claim_ids = {item["non_claim_id"] for item in instance["non_claims"]}
    assert "NC_POLICY_ASSOCIATION_NOT_CERTIFICATION" in non_claim_ids


def test_benchmark_execution_record_avoids_filename_pass_language():
    assert (EXAMPLE_DIR / "benchmark_execution_record.json").exists()
    assert not (EXAMPLE_DIR / "eval_benchmark_pass.json").exists()


def test_benchmark_execution_record_contains_ood_non_claim():
    instance = example("benchmark_execution_record.json")
    non_claim_ids = {item["non_claim_id"] for item in instance["non_claims"]}
    assert "NC_OOD_SAFETY" in non_claim_ids
    assert "NC_DEPLOYMENT_READINESS" in non_claim_ids


def test_schema_rejects_unknown_top_level_field():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["truth_guarantee"] = True
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors
    assert relation_errors == []


def test_duplicate_non_claim_ids_fail_relational_validation():
    instance = example("runtime_blocked_tool_call_record.json")
    instance["non_claims"].append(copy.deepcopy(instance["non_claims"][0]))
    schema_errors, relation_errors = validate_cbc(instance)
    assert schema_errors == []
    assert any("duplicate non_claim_id" in error for error in relation_errors)
