import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_rgv_required_source_non_claim_graph_preservation_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_graph_preservation_v0_1"


def run_checker(name: str):
    return subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def assert_error(proc, code: str):
    assert proc.returncode == 1, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == code for e in out["errors"]), out


def test_deep_structured_metadata_depth_exceeded_fails_closed():
    proc = run_checker("invalid_deep_metadata_depth_exceeded_graph.json")
    assert_error(proc, "STRUCTURED_METADATA_DEPTH_EXCEEDED")


def test_unmodeled_structured_alias_field_fails():
    proc = run_checker("invalid_unmodeled_structured_alias_field_graph.json")
    assert_error(proc, "UNMODELED_STRUCTURED_ALIAS_FIELD")


def test_dummy_external_evidence_basis_fails_for_prohibited_expansion():
    proc = run_checker("invalid_new_claim_dummy_external_evidence_basis.json")
    assert_error(proc, "WEAK_EXTERNAL_EVIDENCE_BASIS")


def test_authority_chain_rooting_to_rgv_pass_fails():
    proc = run_checker("invalid_authority_chain_roots_to_rgv_pass_graph.json")
    assert_error(proc, "FORK_PASS_ROOT_AUTHORITY_CHAIN")


def test_indeterminate_cannot_be_used_as_negative_content_signal():
    proc = run_checker("invalid_indeterminate_negative_content_signal_graph.json")
    assert_error(proc, "INDETERMINATE_USED_AS_NEGATIVE_CONTENT_SIGNAL")


def test_valid_structured_expansion_with_external_authority_and_evidence_still_passes():
    proc = run_checker("valid_expansion_with_external_authority_and_fork_reference_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_legacy_valid_expansion_fixture_now_uses_structured_external_basis():
    proc = run_checker("valid_expansion_with_new_claim_node_graph.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_checker_reports_structured_external_basis_scope():
    proc = run_checker("valid_expansion_with_external_authority_and_fork_reference_graph.json")
    assert proc.returncode == 0
    out = parse_stdout(proc)
    joined = " ".join(out["checker_non_claims"])
    assert "structured non-Fork authority and evidence references" in joined
    assert "does not perform NLP" in joined