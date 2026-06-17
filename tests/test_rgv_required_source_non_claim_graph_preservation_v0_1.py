import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_required_source_non_claim_graph_preservation_v0_1.py"
BINDING_CHECKER = ROOT / "tools" / "check_rgv_result_required_source_non_claim_binding_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_graph_preservation_v0_1"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_required_non_claim_id_set_matches_rgv_pass_binding_checker():
    graph_checker = load_module(CHECKER, "rgv_graph_preservation_checker")
    binding_checker = load_module(BINDING_CHECKER, "rgv_pass_binding_checker")
    assert graph_checker.REQUIRED_NON_CLAIM_IDS == binding_checker.REQUIRED_NON_CLAIM_IDS


def test_valid_preserved_non_claims_graph_passes():
    proc = run_checker("valid_preserved_non_claims_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_dropped_required_source_non_claim_fails():
    proc = run_checker("invalid_dropped_source_truth_non_claim_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "DROPPED_REQUIRED_SOURCE_NON_CLAIM"
        and "SOURCE_TRUTH_NOT_CLAIMED" in e["message"]
        for e in out["errors"]
    )


def test_source_truth_assertion_on_consumption_node_fails():
    proc = run_checker("invalid_source_truth_assertion_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "SOURCE_TRUTH_ASSERTED" for e in out["errors"])


def test_verified_truth_reliance_fails_as_prohibited_inheritance():
    proc = run_checker("invalid_verified_truth_reliance_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "PROHIBITED_INHERITANCE"
        and "VERIFIED_TRUTH" in e["message"]
        for e in out["errors"]
    )


def test_indeterminate_treated_as_pass_fails():
    proc = run_checker("invalid_indeterminate_treated_as_pass_graph.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "INDETERMINATE_TREATED_AS_PASS" for e in out["errors"])


def test_unauthorized_expansion_without_new_claim_node_fails():
    proc = run_checker("invalid_unauthorized_expansion_without_new_claim_node.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "UNAUTHORIZED_INFERENCE_EXPANSION"
        and "ADMISSIBILITY_INFERENCE" in e["message"]
        for e in out["errors"]
    )


def test_expansion_with_new_claim_node_and_preserved_non_claims_passes():
    proc = run_checker("valid_expansion_with_new_claim_node_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_checker_emits_boundary_non_claims():
    proc = run_checker("valid_preserved_non_claims_graph.json")
    assert proc.returncode == 0
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "does not verify SOURCE_TRUTH" in joined
    assert "downstream preservation" in joined
    assert "does not mutate or reinterpret the v0.4" in joined