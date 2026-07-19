from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_csh_pre_execution_readiness_v0_1_2.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("csh_pre_execution_readiness", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_structural_readiness_passes_while_execution_is_blocked() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["failed"] == 0
    assert result["result"] == {
        "executable": False,
        "provider_calls_performed": 0,
        "status": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
        "structural_ok": True,
    }
    assert result["prerequisites"] == {
        "CLAIM_ADMISSION_PR_62_ADMITTED": True,
        "CSH_AMENDMENT_PR_ADMITTED": True,
        "INSTRUMENTATION_RELEASE_ANCHOR_PUBLISHED": True,
        "PRESERVATION_PR_61_ADMITTED": True,
        "PROVIDER_IDENTITY_CREDENTIAL_SCOPE_QUOTA_AND_RECEIPT_PATH_VALIDATED": False,
    }


def test_require_executable_fails_closed() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(ROOT), "--json", "--require-executable"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 2
    payload = json.loads(completed.stdout)
    assert payload["result"]["status"] == "STRUCTURALLY_READY_EXECUTION_BLOCKED"


def test_declared_status_contradiction_is_reported(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    binding_path = root / load_checker().BINDING
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    binding["status"] = "READY_FOR_EXECUTION"
    binding_path.write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8", newline="\n")

    checker = load_checker()
    result = checker.evaluate(root)
    check = next(item for item in result["checks"] if item["name"] == "declared_status_consistency")
    assert check["passed"] is False
    assert "declared status contradiction" in check["detail"]
    assert result["result"]["status"] == "PRE_EXECUTION_BINDING_FAILED"
    assert result["result"]["executable"] is False


def test_predetermined_hypothesis_is_exact() -> None:
    checker = load_checker()
    manifest = checker.load(ROOT / checker.MANIFEST)
    binding = checker.load(ROOT / checker.BINDING)
    assert manifest["hypothesis"] == checker.EXPECTED_HYPOTHESIS
    assert binding["bound_hypothesis"] == checker.EXPECTED_HYPOTHESIS


def test_pair_001_requests_are_byte_bound_and_originals_retained() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    checks = {item["name"]: item for item in result["checks"]}
    assert checks["pair_001_exact_request_lineage"]["passed"] is True
    assert checks["publication_state_reconciled"]["passed"] is True
    assert checks["append_only_publication_transition"]["passed"] is True
    assert checks["original_attempt_and_repeat_boundary"]["passed"] is True


def test_publication_state_is_exactly_bound_without_readiness_promotion() -> None:
    checker = load_checker()
    state = checker.load(ROOT / checker.STATE)
    publication = state["publication"]
    assert state["current_phase"] == checker.PUBLISHED_PHASE
    assert publication["status"] == "anchor_ci_green"
    assert publication["patch_commit"] == checker.PATCH_COMMIT
    assert publication["anchor_commit"] == checker.ANCHOR_COMMIT
    assert state["repeat_runs"] == []

    result = checker.evaluate(ROOT)
    assert result["result"]["status"] == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
    assert result["result"]["executable"] is False
    assert result["result"]["provider_calls_performed"] == 0


def test_publication_state_mismatch_fails_closed(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load_checker()
    state_path = root / checker.STATE
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["publication"]["anchor_commit"] = "0" * 40
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    result = checker.evaluate(root)
    check = next(item for item in result["checks"] if item["name"] == "publication_state_reconciled")
    assert check["passed"] is False
    assert result["result"]["status"] == "PRE_EXECUTION_BINDING_FAILED"
    assert result["result"]["executable"] is False


def test_workflow_predecessors_and_successors_are_both_verifiable() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    checks = {item["name"]: item for item in result["checks"]}
    assert checks["workflow_successor_provenance"]["passed"] is True
