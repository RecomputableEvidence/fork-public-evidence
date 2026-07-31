from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_proof_portfolio_sequence_v0_1.py"
REGISTRY = (
    ROOT
    / "docs/proof-atlas/development/PROOF_PORTFOLIO_REGISTRY_v0_1.json"
)
CONTRACT = (
    ROOT
    / "docs/proof-atlas/development/PROOF_PORTFOLIO_PROMOTION_CONTRACT_v0_1.json"
)


def load_checker():
    spec = importlib.util.spec_from_file_location("proof_portfolio_sequence", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def write_registry(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def finding_codes(result: dict) -> set[str]:
    return {finding["code"] for finding in result["findings"]}


def test_canonical_proof_portfolio_sequence_conforms() -> None:
    result = load_checker().evaluate(check_git=False)
    assert result["findings"] == []
    assert result["status"] == (
        "PROOF_PORTFOLIO_SEQUENCE_CANDIDATE_CONFORMS_NOT_ADMITTED"
    )
    assert result["proof_count"] == 6
    assert result["registered_pr_count"] == 6
    assert result["provider_calls"] == 0


def test_finished_proof_requires_every_promotion_gate(tmp_path: Path) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["promotion_state"] = (
        "FINISHED_PROOF_SURFACE_ADMITTED"
    )
    result = load_checker().evaluate(
        write_registry(tmp_path, payload), CONTRACT, check_git=False
    )
    assert "FINISHED_PROOF_GATE_INCOMPLETE" in finding_codes(result)


def test_duplicate_sequence_and_proof_identifier_rejected(tmp_path: Path) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["sequence"] = 1
    payload["proof_sequence"][1]["proof_id"] = "PROOF-001"
    result = load_checker().evaluate(
        write_registry(tmp_path, payload), CONTRACT, check_git=False
    )
    codes = finding_codes(result)
    assert "PROOF_ID_DUPLICATE" in codes
    assert "PROOF_SEQUENCE_ID_ORDER_MISMATCH" in codes
    assert "PROOF_SEQUENCE_NUMBER_ORDER_MISMATCH" in codes


def test_unfinished_proof_cannot_claim_active_production_capability(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][3]["commercial_track"]["offer_state"] = (
        "ACTIVE_PRODUCTION_CAPABILITY"
    )
    result = load_checker().evaluate(
        write_registry(tmp_path, payload), CONTRACT, check_git=False
    )
    codes = finding_codes(result)
    assert "COMMERCIAL_READINESS_OVERCLAIM" in codes
    assert "ACTIVE_OFFER_WITHOUT_INSTITUTIONAL_VALIDATION" in codes


def test_source_pr_must_be_registered_for_the_proof(tmp_path: Path) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["source_prs"] = [999]
    result = load_checker().evaluate(
        write_registry(tmp_path, payload), CONTRACT, check_git=False
    )
    assert "PROOF_SOURCE_PR_UNREGISTERED" in finding_codes(result)


def test_market_relevance_cannot_promote_evidentiary_standing(
    tmp_path: Path,
) -> None:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    payload["disallowed_promotions"] = [
        item
        for item in payload["disallowed_promotions"]
        if not (
            item["from"] == "MARKET_RELEVANCE"
            and item["to"] == "TECHNICAL_OR_EVIDENTIARY_STANDING"
        )
    ]
    contract_path = tmp_path / "contract.json"
    contract_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    result = load_checker().evaluate(REGISTRY, contract_path, check_git=False)
    assert "REQUIRED_DISALLOWED_PROMOTION_MISSING" in finding_codes(result)


def test_execution_and_provider_calls_remain_closed(tmp_path: Path) -> None:
    payload = copy.deepcopy(load_registry())
    payload["proof_sequence"][5]["execution_authorized"] = True
    payload["proof_sequence"][5]["provider_calls"] = 1
    result = load_checker().evaluate(
        write_registry(tmp_path, payload), CONTRACT, check_git=False
    )
    codes = finding_codes(result)
    assert "EXECUTION_AUTHORITY_OVERCLAIM" in codes
    assert "PROVIDER_CALL_EFFECT_NONZERO" in codes
