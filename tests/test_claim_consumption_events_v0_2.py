import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "claim_consumption_events_v0_2.schema.json"
EXAMPLE_DIR = ROOT / "examples" / "claim_consumption_events_v0_2"

REQUIRED_CCE_NON_CLAIMS = {
    "CCE_NON_CLAIM_SOURCE_TRUTH",
    "CCE_NON_CLAIM_LEGAL_OR_REGULATORY_SUFFICIENCY",
    "CCE_NON_CLAIM_RUNTIME_ENFORCEMENT",
    "CCE_NON_CLAIM_SOURCE_COMPLETENESS",
}


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

    consumed_claims = instance.get("consumed_claims", [])
    consumed_ids = [
        claim.get("claim_id")
        for claim in consumed_claims
        if isinstance(claim, dict)
    ]

    if len(consumed_ids) != len(set(consumed_ids)):
        errors.append("duplicate consumed claim_id")

    consumed_id_set = set(consumed_ids)
    relied = set(instance.get("relied_claim_ids", []))
    rejected = set(instance.get("rejected_claim_ids", []))

    if not relied and not rejected:
        errors.append("CCE must record at least one relied or rejected consumed claim")

    unknown_relied = relied - consumed_id_set
    if unknown_relied:
        errors.append(f"relied_claim_ids not consumed: {sorted(unknown_relied)}")

    unknown_rejected = rejected - consumed_id_set
    if unknown_rejected:
        errors.append(f"rejected_claim_ids not consumed: {sorted(unknown_rejected)}")

    overlap = relied & rejected
    if overlap:
        errors.append(f"claim_ids cannot be both relied and rejected: {sorted(overlap)}")

    by_id = {
        claim.get("claim_id"): claim
        for claim in consumed_claims
        if isinstance(claim, dict) and claim.get("claim_id")
    }

    preserved_non_claim_ids = set(instance.get("preserved_non_claim_ids", []))
    required_preserved = set()
    for claim_id in relied:
        claim = by_id.get(claim_id)
        if claim:
            required_preserved.update(claim.get("source_non_claim_ids", []))

    missing_non_claims = required_preserved - preserved_non_claim_ids
    if missing_non_claims:
        errors.append(f"non_claims from relied claims not preserved: {sorted(missing_non_claims)}")

    unresolved_unknowns = instance.get("unresolved_unknowns", [])
    unknowns_by_claim = {
        unknown.get("related_claim_id")
        for unknown in unresolved_unknowns
        if isinstance(unknown, dict) and unknown.get("related_claim_id")
    }

    for claim_id in relied:
        claim = by_id.get(claim_id)
        if not claim:
            continue
        if claim.get("verification_state") != "PASS" and claim_id not in unknowns_by_claim:
            errors.append(
                f"non-PASS relied claim requires unresolved_unknown: {claim_id}"
            )

    effect = instance.get("boundary_effect")
    detail = instance.get("boundary_effect_detail", {})

    if effect == "EXPANDED":
        for field in [
            "expansion_reason",
            "new_claim_reference",
            "authorizing_party",
            "additional_evidence_refs",
        ]:
            if not detail.get(field):
                errors.append(f"EXPANDED boundary_effect requires {field}")
        if not instance.get("downstream_output", {}).get("new_claim_ids"):
            errors.append("EXPANDED boundary_effect requires downstream_output.new_claim_ids")
    elif effect == "NARROWED":
        if not detail.get("narrowing_reason"):
            errors.append("NARROWED boundary_effect requires narrowing_reason")
        if detail.get("expansion_reason") or detail.get("new_claim_reference"):
            errors.append("NARROWED boundary_effect cannot contain expansion fields")
    elif effect == "PRESERVED":
        forbidden = [
            "narrowing_reason",
            "expansion_reason",
            "new_claim_reference",
            "authorizing_party",
            "additional_evidence_refs",
        ]
        present = [field for field in forbidden if detail.get(field)]
        if present:
            errors.append(f"PRESERVED boundary_effect cannot contain {present}")
        if instance.get("downstream_output", {}).get("new_claim_ids"):
            errors.append("PRESERVED boundary_effect cannot create downstream new_claim_ids")

    cce_non_claim_ids = {
        item.get("non_claim_id")
        for item in instance.get("cce_non_claims", [])
        if isinstance(item, dict)
    }
    missing_required_cce_non_claims = REQUIRED_CCE_NON_CLAIMS - cce_non_claim_ids
    if missing_required_cce_non_claims:
        errors.append(
            f"required CCE non_claims missing: {sorted(missing_required_cce_non_claims)}"
        )

    return errors


def validate_cce(instance: dict):
    validator = schema_validator()
    schema_errors = sorted(validator.iter_errors(instance), key=lambda err: err.path)
    relation_errors = relational_errors(instance)
    return schema_errors, relation_errors


@pytest.mark.parametrize(
    "filename",
    [
        "preserved_runtime_blocked_tool_call.json",
        "expanded_eval_benchmark_pass.json",
    ],
)
def test_examples_validate(filename):
    instance = example(filename)
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_schema_rejects_unknown_top_level_field():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["vendor_truth_guarantee"] = True
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors
    assert relation_errors == []


def test_relie_on_unknown_claim_fails_relational_validation():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["relied_claim_ids"] = ["missing_claim_id"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("relied_claim_ids not consumed" in error for error in relation_errors)


def test_rejected_unknown_claim_fails_relational_validation():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["rejected_claim_ids"] = ["missing_claim_id"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("rejected_claim_ids not consumed" in error for error in relation_errors)


def test_claim_cannot_be_both_relied_and_rejected():
    instance = example("preserved_runtime_blocked_tool_call.json")
    claim_id = instance["relied_claim_ids"][0]
    instance["rejected_claim_ids"] = [claim_id]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("both relied and rejected" in error for error in relation_errors)


def test_duplicate_consumed_claim_ids_fail():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["consumed_claims"].append(copy.deepcopy(instance["consumed_claims"][0]))
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("duplicate consumed claim_id" in error for error in relation_errors)


def test_dropped_non_claim_from_relied_claim_fails():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["preserved_non_claim_ids"] = instance["preserved_non_claim_ids"][:-1]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non_claims from relied claims not preserved" in error for error in relation_errors)


def test_preserved_boundary_cannot_smuggle_new_claim_reference():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["boundary_effect_detail"]["new_claim_reference"] = "smuggled_claim"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot contain" in error for error in relation_errors)


def test_preserved_boundary_cannot_create_downstream_new_claim():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["downstream_output"]["new_claim_ids"] = ["smuggled_claim"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot create" in error for error in relation_errors)


def test_expansion_requires_reason():
    instance = example("expanded_eval_benchmark_pass.json")
    del instance["boundary_effect_detail"]["expansion_reason"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires expansion_reason" in error for error in relation_errors)


def test_expansion_requires_new_claim_reference():
    instance = example("expanded_eval_benchmark_pass.json")
    del instance["boundary_effect_detail"]["new_claim_reference"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires new_claim_reference" in error for error in relation_errors)


def test_expansion_requires_authorizing_party():
    instance = example("expanded_eval_benchmark_pass.json")
    del instance["boundary_effect_detail"]["authorizing_party"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires authorizing_party" in error for error in relation_errors)


def test_expansion_requires_additional_evidence_refs():
    instance = example("expanded_eval_benchmark_pass.json")
    instance["boundary_effect_detail"]["additional_evidence_refs"] = []
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires additional_evidence_refs" in error for error in relation_errors)


def test_expansion_requires_downstream_new_claim_id():
    instance = example("expanded_eval_benchmark_pass.json")
    instance["downstream_output"]["new_claim_ids"] = []
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires downstream_output.new_claim_ids" in error for error in relation_errors)


def test_narrowed_boundary_requires_narrowing_reason():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["boundary_effect"] = "NARROWED"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires narrowing_reason" in error for error in relation_errors)


def test_not_checked_reliance_requires_unresolved_unknown():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["consumed_claims"][0]["verification_state"] = "NOT_CHECKED"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non-PASS relied claim requires unresolved_unknown" in error for error in relation_errors)


def test_not_checked_reliance_with_unresolved_unknown_is_explicit():
    instance = example("preserved_runtime_blocked_tool_call.json")
    claim_id = instance["relied_claim_ids"][0]
    instance["consumed_claims"][0]["verification_state"] = "NOT_CHECKED"
    instance["unresolved_unknowns"] = [
        {
            "unknown_id": "unknown_unchecked_reliance",
            "related_claim_id": claim_id,
            "description": "The relied claim was consumed even though verification was not checked.",
            "effect": "Downstream reviewer must not treat this as a verified claim.",
        }
    ]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_required_cce_non_claims_must_be_present():
    instance = example("preserved_runtime_blocked_tool_call.json")

    # Keep schema shape valid while removing a required CCE non-claim ID.
    # This lets relational validation, not minItems, detect the doctrinal failure.
    instance["cce_non_claims"] = [
        item
        for item in instance["cce_non_claims"]
        if item["non_claim_id"] != "CCE_NON_CLAIM_SOURCE_COMPLETENESS"
    ]
    instance["cce_non_claims"].append(
        {
            "non_claim_id": "CCE_NON_CLAIM_PLACEHOLDER_NOT_REQUIRED",
            "statement": "Placeholder non-claim used to preserve schema minItems while testing required ID enforcement.",
        }
    )

    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("required CCE non_claims missing" in error for error in relation_errors)


def test_schema_rejects_absolute_source_assurance_profile():
    instance = example("preserved_runtime_blocked_tool_call.json")
    instance["consumed_claims"][0]["source_assurance"]["assurance_profile"] = "UNFALSIFIABLE_PHYSICAL_TRUTH"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors
    assert relation_errors == []

