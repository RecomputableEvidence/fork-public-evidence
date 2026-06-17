import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_required_source_non_claim_graph_preservation_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_graph_preservation_v0_1"

REQUIRED_IDS = [
    "SOURCE_TRUTH_NOT_CLAIMED",
    "FACTUAL_BASIS_NOT_CONFIRMED",
    "WHOLENESS_NOT_ASSERTED",
    "COMPLETENESS_NOT_STATED",
    "ADMISSIBILITY_NOT_INFERRED",
    "LAWFULNESS_NOT_IMPLIED",
]


def run_checker_path(path: Path):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def run_checker(name: str):
    return run_checker_path(EXAMPLES / name)


def parse_stdout(proc):
    return json.loads(proc.stdout)


def assert_error(proc, code: str):
    assert proc.returncode == 1, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == code for e in out["errors"]), out
    return out


def test_traversal_safety_failure_class_is_distinct():
    proc = run_checker("invalid_deep_metadata_depth_exceeded_graph.json")
    out = assert_error(proc, "STRUCTURED_METADATA_DEPTH_EXCEEDED")
    assert "TRAVERSAL_SAFETY_LIMIT" in out["failure_classes"]
    assert "SEMANTIC_BOUNDARY_CONTRADICTION" not in out["failure_classes"]


def test_semantic_boundary_failure_class_is_distinct():
    proc = run_checker("invalid_unmodeled_structured_alias_field_graph.json")
    out = assert_error(proc, "UNMODELED_STRUCTURED_ALIAS_FIELD")
    assert "SEMANTIC_BOUNDARY_CONTRADICTION" in out["failure_classes"]
    assert "TRAVERSAL_SAFETY_LIMIT" not in out["failure_classes"]


def test_checker_emits_machine_readable_nlp_scope_not_evaluated():
    proc = run_checker("valid_preserved_non_claims_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["nlp_scope"] == "NOT_EVALUATED"
    assert out["free_text_scope"] == "NOT_EVALUATED_FOR_INFERENCE"


def test_diamond_authority_path_contamination_fails_even_with_external_sibling():
    proc = run_checker("invalid_diamond_authority_contamination_graph.json")
    out = assert_error(proc, "FORK_PASS_ROOT_AUTHORITY_CHAIN")
    assert "AUTHORITY_EVIDENCE_BOUNDARY_DEFECT" in out["failure_classes"]


def test_new_claim_node_empty_non_claim_boundary_fails():
    proc = run_checker("invalid_new_claim_empty_non_claim_boundary_graph.json")
    out = assert_error(proc, "EMPTY_NEW_CLAIM_NON_CLAIM_BOUNDARY")
    assert "AUTHORITY_EVIDENCE_BOUNDARY_DEFECT" in out["failure_classes"]


def test_structured_external_evidence_with_empty_ref_fails():
    proc = run_checker("invalid_structured_external_evidence_empty_ref_graph.json")
    assert_error(proc, "WEAK_EXTERNAL_EVIDENCE_BASIS")


def test_structured_external_evidence_with_placeholder_ref_fails():
    proc = run_checker("invalid_structured_external_evidence_placeholder_ref_graph.json")
    assert_error(proc, "WEAK_EXTERNAL_EVIDENCE_BASIS")


@pytest.mark.parametrize("removed_id", REQUIRED_IDS)
def test_required_source_non_claims_are_enforced_per_id(tmp_path, removed_id):
    source = json.loads((EXAMPLES / "valid_preserved_non_claims_graph.json").read_text(encoding="utf-8"))
    target = source["nodes"][1]
    target["preserved_non_claims"] = [
        item for item in target["preserved_non_claims"] if item != removed_id
    ]

    fixture = tmp_path / f"missing_{removed_id}.json"
    fixture.write_text(json.dumps(source, indent=2, sort_keys=True), encoding="utf-8")

    proc = run_checker_path(fixture)
    out = assert_error(proc, "DROPPED_REQUIRED_SOURCE_NON_CLAIM")
    assert any(removed_id in e["message"] for e in out["errors"])
    assert "STRUCTURAL_PRESERVATION_DEFECT" in out["failure_classes"]