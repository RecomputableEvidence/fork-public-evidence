import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_CHECKER = ROOT / "tools" / "check_required_source_non_claims_v0_1.py"
BINDING_CHECKER = ROOT / "tools" / "check_rgv_result_required_source_non_claim_binding_v0_1.py"
EXAMPLES = ROOT / "examples" / "rgv_required_source_non_claim_result_binding_v0_1"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_binding_checker(name: str):
    return subprocess.run(
        [sys.executable, str(BINDING_CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def parse_stdout(proc):
    return json.loads(proc.stdout)


def test_required_non_claim_id_sets_do_not_drift_between_checkers():
    bundle = load_module(BUNDLE_CHECKER, "required_source_non_claims_checker")
    binding = load_module(BINDING_CHECKER, "rgv_result_binding_checker")
    assert bundle.REQUIRED_NON_CLAIM_IDS == binding.REQUIRED_NON_CLAIM_IDS


def test_nested_required_source_non_claim_bundle_path_passes():
    proc = run_binding_checker("valid_pass_result_with_nested_required_source_non_claim_bundle.json")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = parse_stdout(proc)
    assert out["result"] == "PASS"
    assert out["errors"] == []


def test_fail_result_with_forbidden_source_truth_assertion_fails_binding_checker():
    proc = run_binding_checker("invalid_fail_result_source_truth_asserted.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(e["code"] == "SOURCE_TRUTH_ASSERTED" for e in out["errors"])


def test_pass_with_wrong_non_claim_ids_does_not_satisfy_required_v0_1_bundle():
    proc = run_binding_checker("invalid_pass_with_wrong_non_claim_ids.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    missing = [
        e for e in out["errors"]
        if e["code"] == "MISSING_REQUIRED_SOURCE_NON_CLAIM_ON_PASS"
    ]
    assert len(missing) == 6
    assert any("SOURCE_TRUTH_NOT_CLAIMED" in e["message"] for e in missing)
    assert any("FACTUAL_BASIS_NOT_CONFIRMED" in e["message"] for e in missing)
    assert any("WHOLENESS_NOT_ASSERTED" in e["message"] for e in missing)
    assert any("COMPLETENESS_NOT_STATED" in e["message"] for e in missing)
    assert any("ADMISSIBILITY_NOT_INFERRED" in e["message"] for e in missing)
    assert any("LAWFULNESS_NOT_IMPLIED" in e["message"] for e in missing)

def test_nested_required_source_non_claim_bundle_rejects_additional_unknown_id():
    proc = run_binding_checker("invalid_pass_nested_bundle_with_additional_unknown_id.json")
    assert proc.returncode == 1
    out = parse_stdout(proc)
    assert out["result"] == "FAIL"
    assert any(
        e["code"] == "UNKNOWN_REQUIRED_SOURCE_NON_CLAIM_IN_V0_1_BUNDLE"
        and "RISK_ACCEPTANCE_NOT_INFERRED" in e["message"]
        for e in out["errors"]
    )
