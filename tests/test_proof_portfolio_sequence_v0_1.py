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
    spec = importlib.util.spec_from_file_location(
        "proof_portfolio_sequence",
        CHECKER,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def write_json(tmp_path: Path, name: str, payload: dict) -> Path:
    path = tmp_path / name
    path.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
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


def test_schema_is_executed_against_registry(tmp_path: Path) -> None:
    payload = load_registry()
    payload["undeclared_field"] = "must fail"
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    assert "REGISTRY_SCHEMA_INVALID" in finding_codes(result)


def test_finished_proof_requires_every_promotion_gate(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["promotion_state"] = (
        "FINISHED_PROOF_SURFACE_ADMITTED"
    )
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    codes = finding_codes(result)
    assert "FINISHED_PROOF_GATE_INCOMPLETE" in codes
    assert "FINISHED_PROOF_SELF_ADMISSION_PROHIBITED" in codes


def test_all_true_gate_booleans_cannot_self_admit(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    proof = payload["proof_sequence"][0]
    proof["gates"] = {name: True for name in proof["gates"]}
    proof["promotion_state"] = "FINISHED_PROOF_SURFACE_ADMITTED"
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    codes = finding_codes(result)
    assert "FINISHED_PROOF_SELF_ADMISSION_PROHIBITED" in codes
    assert "ALL_GATES_TRUE_WITHOUT_SEPARATE_ADMISSION_ARTIFACT" in codes


def test_duplicate_sequence_and_proof_identifier_rejected(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["sequence"] = 1
    payload["proof_sequence"][1]["proof_id"] = "PROOF-001"
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    codes = finding_codes(result)
    assert "PROOF_ID_DUPLICATE" in codes
    assert "PROOF_SEQUENCE_ID_ORDER_MISMATCH" in codes
    assert "PROOF_SEQUENCE_NUMBER_ORDER_MISMATCH" in codes


def test_active_production_offer_is_out_of_scope(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    proof = payload["proof_sequence"][3]
    proof["commercial_track"]["offer_state"] = (
        "ACTIVE_PRODUCTION_CAPABILITY"
    )
    proof["gates"] = {name: True for name in proof["gates"]}
    proof["promotion_state"] = "FINISHED_PROOF_SURFACE_ADMITTED"
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    codes = finding_codes(result)
    assert "ACTIVE_PRODUCTION_OFFER_OUT_OF_SCOPE" in codes
    assert "FINISHED_PROOF_SELF_ADMISSION_PROHIBITED" in codes


def test_source_pr_must_be_registered_for_the_proof(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][1]["source_prs"] = [999]
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    assert "PROOF_SOURCE_PR_UNREGISTERED" in finding_codes(result)


def test_routing_pr_cannot_be_used_as_evidence_source(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][0]["source_prs"] = [104]
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    assert "ROUTING_PR_USED_AS_EVIDENCE_SOURCE" in finding_codes(result)


def test_recomputation_route_is_exactly_bound(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["proof_sequence"][3]["scientific_grade"][
        "recomputation_path"
    ] = "tools/check_governed_handoff_cadence_v0_1.py"
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    assert "PROOF_RECOMPUTATION_PATH_MISMATCH" in finding_codes(result)


def test_primary_pr_purpose_is_exactly_bound(
    tmp_path: Path,
) -> None:
    payload = load_registry()
    payload["source_pr_purpose_registry"][1]["primary_role"] = (
        "PUBLIC_ROUTING"
    )
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    assert "PR_PRIMARY_ROLE_MISMATCH" in finding_codes(result)


def test_market_relevance_cannot_promote_evidentiary_standing(
    tmp_path: Path,
) -> None:
    payload = load_contract()
    payload["disallowed_promotions"] = [
        item
        for item in payload["disallowed_promotions"]
        if not (
            item["from"] == "MARKET_RELEVANCE"
            and item["to"] == "TECHNICAL_OR_EVIDENTIARY_STANDING"
        )
    ]
    result = load_checker().evaluate(
        REGISTRY,
        write_json(tmp_path, "contract.json", payload),
        check_git=False,
    )
    assert "REQUIRED_DISALLOWED_PROMOTION_MISSING" in finding_codes(
        result
    )


def test_self_admission_rule_cannot_be_removed(
    tmp_path: Path,
) -> None:
    payload = load_contract()
    payload["self_admission_rule"] = "all gates may self-admit"
    result = load_checker().evaluate(
        REGISTRY,
        write_json(tmp_path, "contract.json", payload),
        check_git=False,
    )
    assert "SELF_ADMISSION_RULE_MISSING" in finding_codes(result)


def test_execution_and_provider_calls_remain_closed(
    tmp_path: Path,
) -> None:
    payload = copy.deepcopy(load_registry())
    payload["proof_sequence"][5]["execution_authorized"] = True
    payload["proof_sequence"][5]["provider_calls"] = 1
    result = load_checker().evaluate(
        write_json(tmp_path, "registry.json", payload),
        CONTRACT,
        check_git=False,
    )
    codes = finding_codes(result)
    assert "EXECUTION_AUTHORITY_OVERCLAIM" in codes
    assert "PROVIDER_CALL_EFFECT_NONZERO" in codes
