import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "check_relational_graph_v0_3.py"
SCHEMA_PATH = ROOT / "schemas" / "relational_graph_bundle_v0_3.schema.json"
EXAMPLE_DIR = ROOT / "examples" / "relational_graph_bundle_v0_3"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_tool():
    spec = importlib.util.spec_from_file_location("check_relational_graph_v0_3", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def example(filename: str):
    return load_json(EXAMPLE_DIR / filename)


def validate_bundle_schema(instance: dict):
    schema = load_json(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    return sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda err: err.path)


def graph_result(bundle: dict):
    return load_tool().validate_bundle(bundle, repo_root=ROOT)


def result_for(filename: str):
    return graph_result(example(filename))


@pytest.mark.parametrize(
    "filename",
    [
        "local_expansion_graph_bundle.json",
        "external_pointer_graph_bundle.json",
        "unresolved_pointer_graph_bundle.json",
    ],
)
def test_bundle_examples_schema_validate(filename):
    assert validate_bundle_schema(example(filename)) == []


def test_local_expansion_bundle_passes_closed_local():
    result = result_for("local_expansion_graph_bundle.json")
    assert result["overall_state"] == "PASS"
    assert result["graph_closure_state"] == "CLOSED_LOCAL"
    assert result["errors"] == []
    assert result["checked_counts"]["graph_edges"] >= 1


def test_external_pointer_bundle_passes_with_open_external_state():
    result = result_for("external_pointer_graph_bundle.json")
    assert result["overall_state"] == "PASS"
    assert result["graph_closure_state"] == "OPEN_EXTERNAL_POINTERS"
    assert result["external_pointers"]
    assert result["errors"] == []


def test_unresolved_pointer_bundle_is_indeterminate():
    result = result_for("unresolved_pointer_graph_bundle.json")
    assert result["overall_state"] == "INDETERMINATE"
    assert result["graph_closure_state"] == "OPEN_UNRESOLVED_POINTERS"
    assert result["unresolved_pointers"]
    assert result["errors"] == []


def test_duplicate_cbc_claim_ids_fail():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["cbc_records"].append(copy.deepcopy(bundle["cbc_records"][0]))
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("duplicate CBC" in error for error in result["errors"])


def test_duplicate_cce_event_ids_fail():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["cce_records"].append(copy.deepcopy(bundle["cce_records"][0]))
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("duplicate CCE event_id" in error for error in result["errors"])


def test_missing_local_consumed_source_fails():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["cce_records"][0]["record"]["consumed_claims"][0]["source_artifact_id"] = "examples/missing/source.json"
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("consumed source CBC not found locally" in error for error in result["errors"])


def test_source_non_claim_mismatch_fails():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["cce_records"][1]["record"]["consumed_claims"][0]["source_non_claim_ids"] = ["NC_DEPLOYMENT_READINESS"]
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("source_non_claim_ids do not match local CBC" in error for error in result["errors"])


def test_cycle_detection_fails():
    bundle = example("local_expansion_graph_bundle.json")
    expansion = copy.deepcopy(bundle["cce_records"][1])
    expansion["artifact_id"] = "examples/relational_graph_bundle_v0_3/generated_cycle_edge.json"
    expansion["record"]["event_id"] = "cce_v0_3_cycle_edge"
    source_cbc = bundle["cbc_records"][2]
    target_cbc = bundle["cbc_records"][1]
    expansion["record"]["consumed_claims"][0]["claim_id"] = source_cbc["record"]["claim_id"]
    expansion["record"]["consumed_claims"][0]["source_artifact_id"] = source_cbc["artifact_id"]
    expansion["record"]["consumed_claims"][0]["source_non_claim_ids"] = [item["non_claim_id"] for item in source_cbc["record"]["non_claims"]]
    expansion["record"]["relied_claim_ids"] = [source_cbc["record"]["claim_id"]]
    expansion["record"]["preserved_non_claim_ids"] = expansion["record"]["consumed_claims"][0]["source_non_claim_ids"]
    expansion["record"]["boundary_effect_detail"]["new_claim_boundary_contract_id"] = target_cbc["record"]["claim_id"]
    expansion["record"]["boundary_effect_detail"]["new_claim_reference"] = target_cbc["artifact_id"]
    expansion["record"]["downstream_output"]["new_claim_ids"] = [target_cbc["record"]["claim_id"]]
    bundle["cce_records"].append(expansion)
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("cycle detected" in error for error in result["errors"])


def test_local_resolved_missing_target_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][1]["record"]
    cce["boundary_effect_detail"]["new_claim_boundary_contract_id"] = "cbc_missing_target"
    cce["downstream_output"]["new_claim_ids"] = ["cbc_missing_target"]
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("LOCAL_RESOLVED target CBC not found locally" in error for error in result["errors"])


def test_preserved_smuggled_expansion_field_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][0]["record"]
    cce["boundary_effect_detail"]["new_claim_reference"] = "smuggled"
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("PRESERVED boundary_effect cannot contain" in error for error in result["errors"])


def test_expanded_missing_additional_evidence_refs_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][1]["record"]
    cce["boundary_effect_detail"]["additional_evidence_refs"] = []
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("EXPANDED boundary_effect requires additional_evidence_refs" in error for error in result["errors"])


def test_nonpass_relied_claim_without_unknown_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][0]["record"]
    cce["consumed_claims"][0]["verification_state"] = "INDETERMINATE"
    cce["unresolved_unknowns"] = []
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("non-PASS relied claim requires unresolved_unknown" in error for error in result["errors"])


def test_bundle_schema_rejects_unknown_top_level_field():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["truth_oracle"] = True
    assert validate_bundle_schema(bundle)


def test_graph_non_claims_required():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["bundle_non_claims"] = bundle["bundle_non_claims"][:-1]
    result = graph_result(bundle)
    assert result["overall_state"] == "FAIL"
    assert any("required graph bundle non_claims missing" in error for error in result["errors"])


def test_cli_returns_zero_for_pass_bundle():
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(EXAMPLE_DIR / "local_expansion_graph_bundle.json"), "--repo-root", str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    result = json.loads(completed.stdout)
    assert result["overall_state"] == "PASS"


def test_cli_returns_nonzero_for_fail_bundle(tmp_path):
    bundle = example("local_expansion_graph_bundle.json")
    bundle["cbc_records"].append(copy.deepcopy(bundle["cbc_records"][0]))
    path = tmp_path / "broken_bundle.json"
    path.write_text(json.dumps(bundle), encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(TOOL_PATH), str(path), "--repo-root", str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 1
    result = json.loads(completed.stdout)
    assert result["overall_state"] == "FAIL"

def _rgv_publication_hardening_result(bundle):
    if "graph_result" in globals():
        return graph_result(bundle)
    return load_tool().validate_bundle(bundle, repo_root=ROOT)

def test_duplicate_bundle_non_claim_ids_fail():
    bundle = example("local_expansion_graph_bundle.json")
    bundle["bundle_non_claims"].append(copy.deepcopy(bundle["bundle_non_claims"][0]))

    result = _rgv_publication_hardening_result(bundle)

    assert result["overall_state"] == "FAIL"
    assert any("duplicate bundle non_claim_id" in error for error in result["errors"])


def test_duplicate_cce_non_claim_ids_fail():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][0]["record"]
    cce["cce_non_claims"].append(copy.deepcopy(cce["cce_non_claims"][0]))

    result = _rgv_publication_hardening_result(bundle)

    assert result["overall_state"] == "FAIL"
    assert any("duplicate cce_non_claim_id" in error for error in result["errors"])


def test_expanded_boundary_cannot_use_not_applicable_resolution():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][1]["record"]
    cce["boundary_effect_detail"]["new_claim_reference_resolution"] = "NOT_APPLICABLE"

    result = _rgv_publication_hardening_result(bundle)

    assert result["overall_state"] == "FAIL"
    assert any("EXPANDED boundary_effect cannot use NOT_APPLICABLE" in error for error in result["errors"])


def test_local_source_artifact_claim_id_mismatch_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][0]["record"]

    original_claim_id = cce["consumed_claims"][0]["claim_id"]
    alternate_cbc = next(
        wrapped
        for wrapped in bundle["cbc_records"]
        if wrapped["record"]["claim_id"] != original_claim_id
    )

    cce["consumed_claims"][0]["source_artifact_id"] = alternate_cbc["artifact_id"]

    result = _rgv_publication_hardening_result(bundle)

    assert result["overall_state"] == "FAIL"
    assert any("consumed source artifact claim_id mismatch" in error for error in result["errors"])


def test_self_referential_expansion_cycle_fails():
    bundle = example("local_expansion_graph_bundle.json")
    cce = bundle["cce_records"][1]["record"]

    source_claim = cce["consumed_claims"][0]
    claim_id = source_claim["claim_id"]
    source_artifact_id = source_claim["source_artifact_id"]

    cce["boundary_effect_detail"]["new_claim_reference_resolution"] = "LOCAL_RESOLVED"
    cce["boundary_effect_detail"]["new_claim_reference"] = source_artifact_id
    cce["boundary_effect_detail"]["new_claim_boundary_contract_id"] = claim_id
    cce["downstream_output"]["new_claim_ids"] = [claim_id]

    result = _rgv_publication_hardening_result(bundle)

    assert result["overall_state"] == "FAIL"
    assert any("cycle detected" in error for error in result["errors"])

def _rgv_publication_repair_result(bundle):
    if "graph_result" in globals():
        return graph_result(bundle)
    if "_rgv_publication_hardening_result" in globals():
        return _rgv_publication_hardening_result(bundle)
    return load_tool().validate_bundle(bundle, repo_root=ROOT)

def test_result_non_claims_include_exit_code_non_approval_warning():
    bundle = example("local_expansion_graph_bundle.json")

    result = _rgv_publication_repair_result(bundle)

    result_non_claims = result.get("result_non_claims", [])
    by_id = {
        item.get("non_claim_id"): item.get("statement", "")
        for item in result_non_claims
        if isinstance(item, dict)
    }

    assert "RGV_RESULT_NON_CLAIM_EXIT_CODE_APPROVAL" in by_id

    statement = by_id["RGV_RESULT_NON_CLAIM_EXIT_CODE_APPROVAL"].lower()
    assert "exit code 0" in statement
    assert "not deployment approval" in statement
    assert "compliance certification" in statement
    assert "runtime authorization" in statement
    assert "source-truth validation" in statement
