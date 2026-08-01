from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_csh_deepseek_drift_contract_v0_1_3.py"
RUNNER = ROOT / "tools/run_csh_provider_validation_v0_1_2.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_contract_preserves_history_and_validates_current_line_retry() -> None:
    checker = load(CHECKER, "csh_drift_contract")
    result = checker.evaluate(ROOT)
    assert result["failed"] == 0
    assert result["result"] == {
        "cause": "UNRESOLVED",
        "pair_001_execution_effect": "NONE",
        "provider_calls_performed": 0,
        "readiness_effect": "NONE",
        "status": "DRIFT_CONTRACT_VALID_ONE_TIME_UPPERCASE_RETRY_REQUESTED",
        "valid": True,
    }


def test_cause_cannot_be_promoted_from_unresolved(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load(CHECKER, "csh_drift_contract_cause")
    path = root / checker.CONTRACT
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["cause"] = "IDENTIFIER_CASE"
    path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert result["failed"] > 0
    assert result["result"]["status"] == "DRIFT_CONTRACT_INVALID"


def test_historical_contract_cannot_be_rewritten_as_authorization(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load(CHECKER, "csh_drift_contract_authority")
    path = root / checker.CONTRACT
    contract = json.loads(path.read_text(encoding="utf-8"))
    contract["precommitted_stopping_rule"]["authorization"]["present"] = True
    contract["execution_boundary"]["retry_authorized"] = True
    path.write_text(json.dumps(contract, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert result["failed"] > 0
    assert result["result"]["provider_calls_performed"] == 0


def test_current_line_successor_digest_tamper_fails_closed(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load(CHECKER, "csh_drift_contract_successor")
    path = root / checker.CURRENT_LINE_SUCCESSOR
    successor = json.loads(path.read_text(encoding="utf-8"))
    successor["current_line_revalidation"]["remaining_authorized_attempts"] = 2
    path.write_text(json.dumps(successor, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert result["failed"] > 0
    assert result["result"]["status"] == "DRIFT_CONTRACT_INVALID"
    assert result["result"]["pair_001_execution_effect"] == "NONE"


def test_retry_request_cannot_expand_to_pair_001(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load(CHECKER, "csh_drift_contract_request_boundary")
    path = root / checker.REQUEST
    request = json.loads(path.read_text(encoding="utf-8"))
    request["disposition"]["pair_001_execution_permitted"] = True
    path.write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert result["failed"] > 0
    assert result["result"]["pair_001_execution_effect"] == "NONE"


def test_retry_is_byte_identical_to_attempt_003_probe() -> None:
    checker = load(CHECKER, "csh_drift_contract_request")
    runner = load(RUNNER, "csh_provider_validation_request")
    request = runner.build_probe_request("deepseek/DeepSeek-V3-0324", 2048)
    assert runner.sha256_bytes(runner.canonical_json_bytes(request)) == checker.RETRY_REQUEST_SHA


def test_lowercase_success_is_new_stratum_not_original_repetition() -> None:
    checker = load(CHECKER, "csh_drift_contract_lowercase")
    contract = checker.load(ROOT / checker.CONTRACT)
    path = contract["precommitted_stopping_rule"]["lowercase_diagnostic_path"]
    assert path["if_successful_required_amendment"] == "CSH-AMEND-004"
    assert path["if_successful_required_stratum"] == "NEW_RECEIVER_VERSION_STRATUM"
    assert path["completes_original_byte_identical_pair_001_repetitions"] is False
