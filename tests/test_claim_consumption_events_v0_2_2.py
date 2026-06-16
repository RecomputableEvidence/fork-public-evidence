import copy
import json
from collections import Counter
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CCE_SCHEMA_PATH = ROOT / "schemas" / "claim_consumption_events_v0_2_2.schema.json"
CBC_SCHEMA_PATH = ROOT / "schemas" / "claim_boundary_contract_v0_2_2.schema.json"
CCE_EXAMPLE_DIR = ROOT / "examples" / "claim_consumption_events_v0_2_2"
CBC_EXAMPLE_DIR = ROOT / "examples" / "claim_boundary_contract_v0_2_2"

CCE_EXAMPLES = [
    "preserved_runtime_blocked_tool_call_record.json",
    "edge_eval_benchmark_expansion.json",
]

CBC_EXAMPLES = [
    "runtime_blocked_tool_call_record.json",
    "benchmark_execution_record.json",
    "limited_internal_review_eligibility_boundary.json",
]

REQUIRED_CCE_NON_CLAIMS = {
    "CCE_NON_CLAIM_SOURCE_TRUTH",
    "CCE_NON_CLAIM_LEGAL_OR_REGULATORY_SUFFICIENCY",
    "CCE_NON_CLAIM_RUNTIME_ENFORCEMENT",
    "CCE_NON_CLAIM_SOURCE_COMPLETENESS",
    "CCE_NON_CLAIM_EXPANDED_CLAIM_NODE",
}

ABSOLUTE_ASSURANCE_TERMS = [
    "unfalsifiable",
    "guaranteed",
    "guarantee",
    "fully compliant",
    "complete coverage",
    "safe for production",
    "ready for deployment",
    "no risk",
    "source truth fully confirmed",
    "absolute truth",
    "deployment approved",
    "compliance certification",
]


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


def example(filename: str):
    return load_json(CCE_EXAMPLE_DIR / filename)


def cbc_example(filename: str):
    return load_json(CBC_EXAMPLE_DIR / filename)


def cbc_by_id():
    return {
        cbc_example(filename)["claim_id"]: cbc_example(filename)
        for filename in CBC_EXAMPLES
    }


def duplicate_values(values):
    counts = Counter(v for v in values if v)
    return sorted(value for value, count in counts.items() if count > 1)


def has_unresolved_unknown(instance: dict, claim_id: str = None, unknown_id: str = None):
    for unknown in instance.get("unresolved_unknowns", []):
        if not isinstance(unknown, dict):
            continue
        if unknown_id and unknown.get("unknown_id") == unknown_id:
            return True
        if claim_id and unknown.get("related_claim_id") == claim_id:
            return True
    return False


def source_cbc_from_claim(claim: dict):
    source_artifact_id = claim.get("source_artifact_id")
    if not source_artifact_id:
        return None

    path = ROOT / source_artifact_id
    if path.exists():
        return load_json(path)

    for cbc in cbc_by_id().values():
        if cbc.get("claim_id") == claim.get("claim_id"):
            return cbc
    return None


def relation_errors(instance: dict):
    errors = []

    if instance.get("cce_version") != "CCE_v0_2_2":
        errors.append("wrong CCE version")

    consumed_claims = instance.get("consumed_claims", [])
    consumed_ids = [
        claim.get("claim_id")
        for claim in consumed_claims
        if isinstance(claim, dict)
    ]
    duplicate_consumed = duplicate_values(consumed_ids)
    if duplicate_consumed:
        errors.append(f"duplicate consumed claim_id values: {duplicate_consumed}")

    consumed_id_set = set(consumed_ids)
    relied = set(instance.get("relied_claim_ids", []))
    rejected = set(instance.get("rejected_claim_ids", []))

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

    for claim in consumed_claims:
        if not isinstance(claim, dict):
            continue

        source_cbc = source_cbc_from_claim(claim)
        if source_cbc is not None:
            cce_ids = set(claim.get("source_non_claim_ids", []))
            cbc_ids = {
                item.get("non_claim_id")
                for item in source_cbc.get("non_claims", [])
                if isinstance(item, dict) and item.get("non_claim_id")
            }
            if cce_ids != cbc_ids:
                errors.append(
                    f"source_non_claim_ids do not match local CBC for {claim.get('claim_id')}"
                )

        assurance = claim.get("source_assurance", {})
        for limitation in assurance.get("assurance_limitations", []):
            text = str(limitation).lower()
            for term in ABSOLUTE_ASSURANCE_TERMS:
                if term in text:
                    errors.append(
                        f"assurance_limitations contains absolute assurance language: {term}"
                    )

    for claim_id in relied:
        claim = by_id.get(claim_id)
        if not claim:
            continue
        if claim.get("verification_state") != "PASS" and not has_unresolved_unknown(instance, claim_id=claim_id):
            errors.append(f"non-PASS relied claim requires unresolved_unknown: {claim_id}")

    cce_non_claim_ids = [
        item.get("non_claim_id")
        for item in instance.get("cce_non_claims", [])
        if isinstance(item, dict)
    ]
    duplicate_cce_non_claims = duplicate_values(cce_non_claim_ids)
    if duplicate_cce_non_claims:
        errors.append(f"duplicate cce_non_claim_id values: {duplicate_cce_non_claims}")

    missing_required = REQUIRED_CCE_NON_CLAIMS - set(cce_non_claim_ids)
    if missing_required:
        errors.append(f"required CCE non_claims missing: {sorted(missing_required)}")

    effect = instance.get("boundary_effect")
    detail = instance.get("boundary_effect_detail", {})
    downstream = instance.get("downstream_output", {})
    resolution = detail.get("new_claim_reference_resolution")
    new_claim_boundary_contract_id = detail.get("new_claim_boundary_contract_id")
    new_claim_reference = detail.get("new_claim_reference")
    new_claim_ids = set(downstream.get("new_claim_ids", []))

    expansion_fields = [
        "expansion_reason",
        "new_claim_reference",
        "new_claim_boundary_contract_id",
        "authorizing_party",
        "additional_evidence_refs",
    ]

    if effect == "EXPANDED":
        if resolution == "NOT_APPLICABLE":
            errors.append("EXPANDED boundary_effect cannot use NOT_APPLICABLE resolution")

        required_expansion_fields = [
            "expansion_reason",
            "new_claim_reference",
            "new_claim_boundary_contract_id",
            "authorizing_party",
            "additional_evidence_refs",
        ]
        for field in required_expansion_fields:
            value = detail.get(field)
            if value is None or value == "" or value == []:
                errors.append(f"EXPANDED boundary_effect requires {field}")

        if not new_claim_boundary_contract_id:
            errors.append("EXPANDED boundary_effect requires new_claim_boundary_contract_id")
        elif new_claim_boundary_contract_id not in new_claim_ids:
            errors.append(
                "downstream_output.new_claim_ids must include boundary_effect_detail.new_claim_boundary_contract_id"
            )

        if resolution == "LOCAL_RESOLVED":
            local = cbc_by_id().get(new_claim_boundary_contract_id)
            if local is None:
                errors.append(f"LOCAL_RESOLVED target CBC not found locally: {new_claim_boundary_contract_id}")
            else:
                local_schema_errors = sorted(cbc_validator().iter_errors(local), key=lambda err: err.path)
                if local_schema_errors:
                    errors.append(f"LOCAL_RESOLVED target CBC failed schema validation: {new_claim_boundary_contract_id}")

        elif resolution == "EXTERNAL_POINTER":
            if not (
                isinstance(new_claim_reference, str)
                and (new_claim_reference.startswith("https://") or new_claim_reference.startswith("uri:"))
            ):
                errors.append("EXTERNAL_POINTER requires https:// or uri: reference")

        elif resolution == "NOT_RESOLVED":
            if not has_unresolved_unknown(
                instance,
                claim_id=new_claim_boundary_contract_id,
                unknown_id="unknown_new_claim_boundary_unresolved",
            ):
                errors.append("NOT_RESOLVED pointer requires unresolved_unknown marker")
        elif resolution not in {"LOCAL_RESOLVED", "EXTERNAL_POINTER", "NOT_RESOLVED"}:
            errors.append(f"invalid expansion pointer resolution: {resolution}")

        if "expanded_claim" in instance or "expanded_claim_body" in instance:
            errors.append("CCE must not contain expanded claim body")
        if "expanded_claim" in detail or "expanded_claim_body" in detail:
            errors.append("CCE boundary_effect_detail must not contain expanded claim body")

    elif effect == "PRESERVED":
        if resolution != "NOT_APPLICABLE":
            errors.append("PRESERVED boundary_effect requires NOT_APPLICABLE resolution")
        if new_claim_ids:
            errors.append("PRESERVED boundary_effect cannot create downstream new_claim_ids")

        forbidden_fields = ["narrowing_reason"] + expansion_fields
        present = [field for field in forbidden_fields if detail.get(field)]
        if present:
            errors.append(f"PRESERVED boundary_effect cannot contain boundary-change fields: {present}")

    elif effect == "NARROWED":
        if resolution != "NOT_APPLICABLE":
            errors.append("NARROWED boundary_effect requires NOT_APPLICABLE resolution")
        if new_claim_ids:
            errors.append("NARROWED boundary_effect cannot create downstream new_claim_ids")
        if not detail.get("narrowing_reason"):
            errors.append("NARROWED boundary_effect requires narrowing_reason")

        present = [field for field in expansion_fields if detail.get(field)]
        if present:
            errors.append(f"NARROWED boundary_effect cannot contain expansion fields: {present}")

    else:
        errors.append(f"unknown boundary_effect: {effect}")

    return errors


def validate_cce(instance: dict):
    schema_errors = sorted(cce_validator().iter_errors(instance), key=lambda err: err.path)
    rel_errors = relation_errors(instance)
    return schema_errors, rel_errors


@pytest.mark.parametrize("filename", CCE_EXAMPLES)
def test_examples_validate(filename):
    instance = example(filename)
    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert rel_errors == []


def test_cce_schema_requires_five_non_claim_items():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["cce_non_claims"] = instance["cce_non_claims"][:4]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors
    assert any("required CCE non_claims missing" in error for error in rel_errors)


def test_duplicate_cce_non_claim_ids_fail():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["cce_non_claims"].append(copy.deepcopy(instance["cce_non_claims"][0]))

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("duplicate cce_non_claim_id" in error for error in rel_errors)


def test_downstream_output_artifact_type_rejects_overclaiming_label():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["downstream_output"]["artifact_type"] = "DEPLOYMENT_APPROVED_CLAIM"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors
    assert rel_errors == []


def test_expanded_new_claim_ids_must_include_new_claim_boundary_contract_id():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["downstream_output"]["new_claim_ids"] = ["wrong_downstream_claim_id"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("new_claim_ids must include" in error for error in rel_errors)


def test_indeterminate_reliance_requires_unresolved_unknown():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    claim_id = instance["relied_claim_ids"][0]
    instance["consumed_claims"][0]["verification_state"] = "INDETERMINATE"
    instance["unresolved_unknowns"] = []

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("non-PASS relied claim requires unresolved_unknown" in error for error in rel_errors)


def test_assurance_limitations_cannot_smuggle_absolute_truth_language():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["consumed_claims"][0]["source_assurance"]["assurance_limitations"] = [
        "Source truth fully confirmed and guaranteed."
    ]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("absolute assurance language" in error for error in rel_errors)


def test_expanded_edge_cannot_use_not_applicable_resolution():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_APPLICABLE"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("cannot use NOT_APPLICABLE" in error for error in rel_errors)


def test_not_resolved_pointer_requires_unresolved_unknown_marker():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_RESOLVED"
    instance["unresolved_unknowns"] = []

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("NOT_RESOLVED pointer requires unresolved_unknown" in error for error in rel_errors)


def test_external_pointer_rejects_http_reference():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "EXTERNAL_POINTER"
    instance["boundary_effect_detail"]["new_claim_reference"] = "http://example.test/cbc.json"
    instance["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "cbc_external"
    instance["downstream_output"]["new_claim_ids"] = ["cbc_external"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("EXTERNAL_POINTER requires https:// or uri:" in error for error in rel_errors)


def test_external_pointer_accepts_https_reference():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "EXTERNAL_POINTER"
    instance["boundary_effect_detail"]["new_claim_reference"] = "https://example.test/cbc.json"
    instance["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "cbc_external"
    instance["downstream_output"]["new_claim_ids"] = ["cbc_external"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert rel_errors == []


def test_expanded_edge_does_not_hold_expanded_claim_body():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["expanded_claim_body"] = {"claim": "smuggled claim body"}

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors


def test_source_non_claim_ids_must_match_local_cbc():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["consumed_claims"][0]["source_non_claim_ids"] = ["NC_DEPLOYMENT_READINESS"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("source_non_claim_ids do not match local CBC" in error for error in rel_errors)


def test_preserved_edge_requires_not_applicable_resolution():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_RESOLVED"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect requires NOT_APPLICABLE" in error for error in rel_errors)

def test_preserved_boundary_cannot_smuggle_expansion_fields():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect_detail"]["new_claim_reference"] = "smuggled_reference"
    instance["boundary_effect_detail"]["expansion_reason"] = "hidden expansion"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot contain boundary-change fields" in error for error in rel_errors)


def test_preserved_boundary_cannot_smuggle_narrowing_reason():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect_detail"]["narrowing_reason"] = "hidden narrowing"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("PRESERVED boundary_effect cannot contain boundary-change fields" in error for error in rel_errors)


def test_narrowed_boundary_requires_narrowing_reason():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect"] = "NARROWED"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("NARROWED boundary_effect requires narrowing_reason" in error for error in rel_errors)


def test_narrowed_boundary_cannot_contain_expansion_fields():
    instance = example("preserved_runtime_blocked_tool_call_record.json")
    instance["boundary_effect"] = "NARROWED"
    instance["boundary_effect_detail"]["narrowing_reason"] = "Downstream consumer narrows reliance to record-preservation only."
    instance["boundary_effect_detail"]["new_claim_reference"] = "smuggled_expansion"
    instance["boundary_effect_detail"]["expansion_reason"] = "hidden expansion"

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("NARROWED boundary_effect cannot contain expansion fields" in error for error in rel_errors)


def test_expanded_boundary_requires_expansion_reason():
    instance = example("edge_eval_benchmark_expansion.json")
    del instance["boundary_effect_detail"]["expansion_reason"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("EXPANDED boundary_effect requires expansion_reason" in error for error in rel_errors)


def test_expanded_boundary_requires_authorizing_party():
    instance = example("edge_eval_benchmark_expansion.json")
    del instance["boundary_effect_detail"]["authorizing_party"]

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("EXPANDED boundary_effect requires authorizing_party" in error for error in rel_errors)


def test_expanded_boundary_requires_additional_evidence_refs():
    instance = example("edge_eval_benchmark_expansion.json")
    instance["boundary_effect_detail"]["additional_evidence_refs"] = []

    schema_errors, rel_errors = validate_cce(instance)
    assert schema_errors == []
    assert any("EXPANDED boundary_effect requires additional_evidence_refs" in error for error in rel_errors)
