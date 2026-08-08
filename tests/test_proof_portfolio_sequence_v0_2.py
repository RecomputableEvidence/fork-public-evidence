from __future__ import annotations

import copy
import json
from pathlib import Path

from tools import check_proof_portfolio_sequence_v0_2 as checker


def _registry() -> dict:
    return checker.load(checker.REGISTRY)


def _evaluate_tmp(tmp_path: Path, value: dict) -> dict:
    target = tmp_path / "registry.json"
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    return checker.evaluate(target)


def _codes(result: dict) -> set[str]:
    return {item["code"] for item in result["findings"]}


def test_canonical_registry_conforms() -> None:
    result = checker.evaluate()
    assert result["status"] == checker.PASS
    assert result["findings"] == []
    assert result["proof_count"] == 6


def test_source_evidence_cannot_self_admit_proof(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["proof_sequence"][2]["proof_packaging_state"] = "ADMITTED"
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "SOURCE_TO_PROOF_PROMOTION" in _codes(result) or "PROOF_SELF_ADMISSION" in _codes(result)


def test_proof_order_cannot_change(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["proof_sequence"][1], value["proof_sequence"][2] = value["proof_sequence"][2], value["proof_sequence"][1]
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "PROOF_ORDER_MISMATCH" in _codes(result)


def test_proof003_must_bind_admitted_pr118_successor(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["proof_sequence"][2]["source_admission"]["pull_request"] = 105
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "PROOF003_ADMISSION_BINDING_INVALID" in _codes(result)


def test_pending_proof_source_cannot_be_promoted(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["proof_sequence"][3]["source_evidence_state"] = "ADMITTED_EXTERIOR_EVIDENCE"
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "SOURCE_STATE_PROMOTION_OR_DRIFT" in _codes(result)


def test_execution_cannot_be_authorized(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["proof_sequence"][5]["execution_state"] = "AUTHORIZED"
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "EXECUTION_STATE_INVALID_OR_PROMOTED" in _codes(result)


def test_provider_calls_remain_zero(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["effects"]["provider_calls_authorized"] = 1
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "REGISTRY_SCHEMA_INVALID" in _codes(result) or "EXECUTION_EFFECT_NONZERO" in _codes(result)


def test_model_standing_remains_provisional(tmp_path: Path) -> None:
    value = copy.deepcopy(_registry())
    value["model_state"]["standing"] = "INDEPENDENTLY_VALIDATED_BASELINE"
    result = _evaluate_tmp(tmp_path, value)
    assert result["status"] == checker.FAIL
    assert "REGISTRY_SCHEMA_INVALID" in _codes(result) or "MODEL_STANDING_PROMOTION" in _codes(result)
