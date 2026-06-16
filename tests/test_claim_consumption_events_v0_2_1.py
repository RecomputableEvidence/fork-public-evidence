import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CCE_SCHEMA_PATH = ROOT / "schemas" / "claim_consumption_events_v0_2_1.schema.json"
CBC_SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_2_1.schema.json"
CCE_EXAMPLE_DIR = ROOT / "examples" / "claim_consumption_events_v0_2_1"
CBC_EXAMPLE_DIR = ROOT / "examples" / "claim_boundary_contract_v0_2_1"

CCE_EXAMPLE_NAMES = [
    "preserved_runtime_blocked_tool_call_record.json",
    "edge_eval_benchmark_expansion.json",
]

REQUIRED_CCE_NON_CLAIMS = {
    "CCE_NON_CLAIM_SOURCE_TRUTH",
    "CCE_NON_CLAIM_LEGAL_OR_REGULATORY_SUFFICIENCY",
    "CCE_NON_CLAIM_RUNTIME_ENFORCEMENT",
    "CCE_NON_CLAIM_SOURCE_COMPLETENESS",
    "CCE_NON_CLAIM_EXPANDED_CLAIM_NODE",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def cce_validator():
    schema = load_json(CCE_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def cbc_validator():
    schema = load_json(CBC_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def example(name: str):
    return load_json(CCE_EXAMPLE_DIR / name)


def local_cbc_records():
    records = {}
    for path in CBC_EXAMPLE_DIR.glob("*.json"):
        obj = load_json(path)
        records[obj["claim_id"]] = (path, obj)
    return records


def local_cbc_by_artifact_id():
    records = {}
    for path in CBC_EXAMPLE_DIR.glob("*.json"):
        obj = load_json(path)
        rel = path.relative_to(ROOT).as_posix()
        records[rel] = obj
    return records


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

    if relied - consumed_id_set:
        errors.append(f"relied_claim_ids not consumed: {sorted(relied - consumed_id_set)}")

    if rejected - consumed_id_set:
        errors.append(f"rejected_claim_ids not consumed: {sorted(rejected - consumed_id_set)}")

    if relied & rejected:
        errors.append(f"claim_ids cannot be both relied and rejected: {sorted(relied & rejected)}")

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

    local_sources = local_cbc_by_artifact_id()
    for claim in consumed_claims:
        if not isinstance(claim, dict):
            continue
        source_id = claim.get("source_artifact_id")
        source = local_sources.get(source_id)
        if source:
            source_non_claim_ids = {
                item["non_claim_id"]
                for item in source.get("non_claims", [])
            }
            claim_non_claim_ids = set(claim.get("source_non_claim_ids", []))
            if claim_non_claim_ids != source_non_claim_ids:
                errors.append(
                    f"source_non_claim_ids do not match local CBC for {claim.get('claim_id')}"
                )

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
            errors.append(f"non-PASS relied claim requires unresolved_unknown: {claim_id}")

    effect = instance.get("boundary_effect")
    detail = instance.get("boundary_effect_detail", {})
    resolution = detail.get("new_claim_reference_resolution")

    if effect == "EXPANDED":
        for field in [
            "expansion_reason",
            "new_claim_reference",
            "new_claim_boundary_contract_id",
            "authorizing_party",
            "additional_evidence_refs",
        ]:
            if not detail.get(field):
                errors.append(f"EXPANDED boundary_effect requires {field}")

        if not instance.get("downstream_output", {}).get("new_claim_ids"):
            errors.append("EXPANDED boundary_effect requires downstream_output.new_claim_ids")

        if resolution not in {"LOCAL_RESOLVED", "EXTERNAL_POINTER", "NOT_RESOLVED"}:
            errors.append("EXPANDED boundary_effect requires resolved, external, or unresolved pointer status")

        new_claim_id = detail.get("new_claim_boundary_contract_id")
        local_records = local_cbc_records()

        if resolution == "LOCAL_RESOLVED":
            if new_claim_id not in local_records:
                errors.append(f"LOCAL_RESOLVED new_claim_boundary_contract_id not found: {new_claim_id}")
            else:
                _, cbc = local_records[new_claim_id]
                cbc_schema_errors = list(cbc_validator().iter_errors(cbc))
                if cbc_schema_errors:
                    errors.append(f"LOCAL_RESOLVED CBC did not validate: {new_claim_id}")

        if resolution == "EXTERNAL_POINTER":
            ref = detail.get("new_claim_reference", "")
            if not (ref.startswith("uri:") or ref.startswith("https://") or ref.startswith("http://")):
                errors.append("EXTERNAL_POINTER new_claim_reference must be URI-like")

        if resolution == "NOT_RESOLVED":
            unknown_ids = {item.get("unknown_id") for item in unresolved_unknowns if isinstance(item, dict)}
            if "unknown_new_claim_boundary_unresolved" not in unknown_ids:
                errors.append("NOT_RESOLVED expansion pointer requires unresolved unknown marker")

    elif effect == "NARROWED":
        if not detail.get("narrowing_reason"):
            errors.append("NARROWED boundary_effect requires narrowing_reason")
        if detail.get("expansion_reason") or detail.get("new_claim_reference") or detail.get("new_claim_boundary_contract_id"):
            errors.append("NARROWED boundary_effect cannot contain expansion fields")
        if resolution != "NOT_APPLICABLE":
            errors.append("NARROWED boundary_effect requires NOT_APPLICABLE pointer resolution")
    elif effect == "PRESERVED":
        forbidden = [
            "narrowing_reason",
            "expansion_reason",
            "new_claim_reference",
            "new_claim_boundary_contract_id",
            "authorizing_party",
            "additional_evidence_refs",
        ]
        present = [field for field in forbidden if detail.get(field)]
        if present:
            errors.append(f"PRESERVED boundary_effect cannot contain {present}")
        if instance.get("downstream_output", {}).get("new_claim_ids"):
            errors.append("PRESERVED boundary_effect cannot create downstream new_claim_ids")
        if resolution != "NOT_APPLICABLE":
            errors.append("PRESERVED boundary_effect requires NOT_APPLICABLE pointer resolution")

    cce_non_claim_ids = {
        item.get("non_claim_id")
        for item in instance.get("cce_non_claims", [])
        if isinstance(item, dict)
    }
    missing = REQUIRED_CCE_NON_CLAIMS - cce_non_claim_ids
    if missing:
        errors.append(f"required CCE non_claims missing: {sorted(missing)}")

    return errors


def validate_cce(instance: dict):
    validator = cce_validator()
    schema_errors = sorted(validator.iter_errors(instance), key=lambda err: err.path)
    relation_errors = relational_errors(instance)
    return schema_errors, relation_errors


@pytest.mark.parametrize("filename", CCE_EXAMPLE_NAMES)
def test_cce_v0_2_1_examples_validate(filename):
    instance = example(filename)
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_renamed_expansion_edge_example_exists():
    assert (CCE_EXAMPLE_DIR / "edge_eval_benchmark_expansion.json").exists()
    assert not (CCE_EXAMPLE_DIR / "expanded_eval_benchmark_pass.json").exists()


def test_relie_on_unknown_claim_fails_relational_validation():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["relied_claim_ids"] = ["missing_claim_id"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("relied_claim_ids not consumed" in error for error in relation_errors)


def test_rejected_unknown_claim_fails_relational_validation():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["rejected_claim_ids"] = ["missing_claim_id"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("rejected_claim_ids not consumed" in error for error in relation_errors)


def test_claim_cannot_be_both_relied_and_rejected():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    claim_id = instance["relied_claim_ids"][0]
    instance["rejected_claim_ids"] = [claim_id]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("both relied and rejected" in error for error in relation_errors)


def test_duplicate_consumed_claim_ids_fail():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"].append(copy.deepcopy(instance["consumed_claims"][0]))
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("duplicate consumed claim_id" in error for error in relation_errors)


def test_dropped_non_claim_from_relied_claim_fails():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["preserved_non_claim_ids"] = instance["preserved_non_claim_ids"][:-1]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non_claims from relied claims not preserved" in error for error in relation_errors)


def test_source_non_claim_ids_must_match_local_cbc():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"][0]["source_non_claim_ids"].append("NC_NOT_IN_LOCAL_CBC")
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("source_non_claim_ids do not match local CBC" in error for error in relation_errors)


def test_preserved_boundary_cannot_smuggle_new_claim_reference():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect_detail"]["new_claim_reference"] = "smuggled_claim"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot contain" in error for error in relation_errors)


def test_preserved_boundary_cannot_create_downstream_new_claim():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["downstream_output"]["new_claim_ids"] = ["smuggled_claim"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot create" in error for error in relation_errors)


def test_expansion_requires_new_claim_boundary_contract_id():
    instance = example("edge_eval_benchmark_expansion.json")
    del instance["boundary_effect_detail"]["new_claim_boundary_contract_id"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires new_claim_boundary_contract_id" in error for error in relation_errors)


def test_expansion_local_resolved_must_point_to_local_cbc():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "missing_local_cbc"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("LOCAL_RESOLVED new_claim_boundary_contract_id not found" in error for error in relation_errors)


def test_external_pointer_expansion_can_be_valid_when_uri_like():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "EXTERNAL_POINTER"
    instance["boundary_effect_detail"]["new_claim_reference"] = "uri:registry/fork/cbc/external-limited-review"
    instance["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "external_limited_review_boundary"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_external_pointer_requires_uri_like_reference():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "EXTERNAL_POINTER"
    instance["boundary_effect_detail"]["new_claim_reference"] = "not a uri"
    instance["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "external_limited_review_boundary"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("EXTERNAL_POINTER new_claim_reference must be URI-like" in error for error in relation_errors)


def test_not_resolved_pointer_requires_unresolved_unknown():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_RESOLVED"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("NOT_RESOLVED expansion pointer requires unresolved unknown marker" in error for error in relation_errors)


def test_not_resolved_pointer_with_unknown_marker_is_valid():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_RESOLVED"
    instance["unresolved_unknowns"].append(
        {
            "unknown_id": "unknown_new_claim_boundary_unresolved",
            "description": "The downstream CBC pointer was recorded but not resolved in this validation bundle.",
            "effect": "The verifier does not claim the referenced CBC was inspected.",
        }
    )
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert relation_errors == []


def test_expanded_edge_does_not_hold_expanded_claim_body():
    instance = example("edge_eval_benchmark_expansion.json")
    assert "expanded_claim" not in instance
    assert instance["boundary_effect_detail"]["new_claim_boundary_contract_id"]
    assert "This CCE records the edge" in instance["boundary_effect_detail"]["summary"]


def test_expansion_requires_authorizing_party():
    instance = example("edge_eval_benchmark_expansion.json")
    del instance["boundary_effect_detail"]["authorizing_party"]
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires authorizing_party" in error for error in relation_errors)


def test_expansion_requires_additional_evidence_refs():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["additional_evidence_refs"] = []
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires additional_evidence_refs" in error for error in relation_errors)


def test_expansion_requires_downstream_new_claim_id():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["downstream_output"]["new_claim_ids"] = []
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires downstream_output.new_claim_ids" in error for error in relation_errors)


def test_narrowed_boundary_requires_narrowing_reason():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect"] = "NARROWED"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("requires narrowing_reason" in error for error in relation_errors)


def test_failed_reliance_requires_unresolved_unknown():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"][0]["verification_state"] = "FAIL"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non-PASS relied claim requires unresolved_unknown" in error for error in relation_errors)


def test_not_checked_reliance_requires_unresolved_unknown():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"][0]["verification_state"] = "NOT_CHECKED"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non-PASS relied claim requires unresolved_unknown" in error for error in relation_errors)


def test_not_checked_reliance_with_unresolved_unknown_is_explicit():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
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
    instance = example("preserved_runtime_blocked_tool_call_record.json")
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
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"][0]["source_assurance"]["assurance_profile"] = "UNFALSIFIABLE_PHYSICAL_TRUTH"
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors
    assert relation_errors == []


def test_schema_rejects_unknown_top_level_field():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["vendor_truth_guarantee"] = True
    schema_errors, relation_errors = validate_cce(instance)
    assert schema_errors
    assert relation_errors == []
