from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_longitudinal_recomputation_v0_2.py"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "fork_longitudinal_recomputation_v0_2",
        CHECKER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs(checker):
    contract = checker.strict_load(ROOT / checker.CONTRACT)
    registry = checker.strict_load(ROOT / checker.REGISTRY)
    return contract, registry


def codes(result) -> set[str]:
    return set(result["finding_codes"])


def test_exact_longitudinal_recomputation_surface_conforms() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["findings"] == []
    assert result["status"] == "LONGITUDINAL_STATE_REPRODUCED"
    assert result["coverage_receipt"]["result"] == "BOUNDED_EVENT_COVERAGE_REPRODUCED"
    assert result["transition_receipt"]["result"] == "STANDING_TRANSITION_RECOMPUTED"


def test_projection_is_rebuilt_from_reducers_and_events() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT, verify_committed=False)
    projection = result["projection"]
    state = projection["state_vector"]
    assert result["findings"] == []
    assert state["artifact_state"]["basis_commit"] == (
        "f955834681d2f2ee257276acbf68afde0ae0e69d"
    )
    assert state["verification_state"] == {
        "current_head": "f955834681d2f2ee257276acbf68afde0ae0e69d",
        "disposition": "REPRODUCED_WITHIN_DECLARED_SCOPE",
        "freshness": "EXACT_HEAD_BOUND_NO_REVIEW_INHERITANCE",
        "reviewed_head": "bac40d9bdbd7f6b4927a676fef8def70756ad9d5",
        "standing": (
            "PREDECESSOR_HEAD_INDEPENDENTLY_RECOMPUTED_"
            "CURRENT_HEAD_NOT_SEPARATELY_RECOMPUTED"
        ),
    }
    assert state["execution_state"]["reducer_id"] == "FORK_SEQUENCE_SURFACE_REDUCER_v0_1"
    assert state["execution_state"]["sequence"]["current_state"] == (
        "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED"
    )
    assert projection["effects"]["provider_calls"] == 0
    assert projection["effects"]["pair_001_calls"] == 0
    assert projection["effects"]["admission"] == "NONE"


def test_as_of_and_diff_keep_review_standing_head_bound() -> None:
    checker = load_checker()
    base = "bac40d9bdbd7f6b4927a676fef8def70756ad9d5"
    closure = "f955834681d2f2ee257276acbf68afde0ae0e69d"
    at_base = checker.evaluate(ROOT, verify_committed=False, as_of=base)
    assert at_base["findings"] == []
    assert at_base["projection"]["state_vector"]["review_state"]["standing"] == (
        "NO_EXTERIOR_REVIEW_RECEIPT_PRESENT_AT_REPLAY_START"
    )
    delta = checker.state_diff(ROOT, base, closure)
    assert delta["status"] == "LONGITUDINAL_DIFF_REPRODUCED"
    assert delta["changed_dimensions"] == [
        "artifact_state",
        "review_state",
        "temporal_closure",
        "unresolved_state",
        "verification_state",
    ]
    assert delta["preserved_dimensions"] == [
        "admission_state",
        "authority_state",
        "execution_state",
    ]


def test_sequence_surface_is_consumed_not_restated() -> None:
    checker = load_checker()
    contract, _ = inputs(checker)
    synthetic = {
        "standing": "SYNTHETIC_TEST_ONLY",
        "reducer_id": "SYNTHETIC_REDUCER",
        "sequence": {"current_state": "SYNTHETIC"},
    }
    state = checker.materialize_initial_state(contract, synthetic)
    assert state["execution_state"] == synthetic
    source = CHECKER_PATH.read_text(encoding="utf-8")
    assert "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED" not in source
    assert "expected_csh" not in source


def test_state_route_separates_historical_governed_and_candidate_standing() -> None:
    checker = load_checker()
    route = checker.strict_load(ROOT / checker.STATE_ROUTE)
    assert route["historical_projection"]["standing"].endswith(
        "NOT_CURRENT_RELIANCE_STANDING"
    )
    assert route["governed_projection"] == {
        "path": "docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json",
        "source_commit": "1241c0084900f2c60f362205525464582e57b4a7",
        "standing": (
            "CURRENT_WITH_RESPECT_TO_EXACT_GOVERNED_PRESERVATION_"
            "COORDINATE_NOT_DEFAULT_BRANCH"
        ),
    }
    assert route["longitudinal_replay_candidate"]["standing"] == (
        "RESEARCH_CANDIDATE_NOT_ADMITTED"
    )


def test_missing_interval_event_is_unresolved_not_absent() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    registry["events"] = []
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "EVENT_COVERAGE_UNRESOLVED" in codes(result)


def test_undeclared_dimension_change_is_rejected() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    event = registry["events"][0]
    event["affected_dimensions"].append("truth_state")
    event["dimension_effects"]["truth_state"] = {
        "operation": "REPLACE",
        "after": {"standing": "TRUE"},
    }
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "UNDECLARED_DIMENSION_CHANGE" in codes(result)


def test_review_cannot_be_promoted_to_a_different_current_head() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    registry["events"][0]["dimension_effects"]["verification_state"]["after"][
        "standing"
    ] = "CURRENT_HEAD_INDEPENDENTLY_RECOMPUTED"
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "CURRENT_HEAD_REVIEW_STALE" in codes(result)


def test_evidence_preservation_cannot_confer_admission() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    registry["events"][0]["admission_effect"] = "CONFER"
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "ADMISSION_EFFECT_MISMATCH" in codes(result)


def test_execution_change_requires_explicit_effect() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    event = registry["events"][0]
    event["affected_dimensions"].append("execution_state")
    event["dimension_effects"]["execution_state"] = {
        "operation": "REPLACE",
        "after": {
            "standing": "EXECUTION_PERMITTED",
            "provider_calls": 1,
        },
    }
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "EXECUTION_EFFECT_MISMATCH" in codes(result)


def test_concurrent_successor_requires_reconciliation() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    concurrent = copy.deepcopy(registry["events"][0])
    concurrent["ordinal"] = 2
    concurrent["event_id"] = "FLR-TEST-CONCURRENT"
    concurrent["predecessor_event_ids"] = []
    registry["events"].append(concurrent)
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "CONCURRENT_SUCCESSOR_UNRECONCILED" in codes(result)


def test_expired_authority_cannot_remain_active() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    event = registry["events"][0]
    event["affected_dimensions"].append("authority_state")
    event["dimension_effects"]["authority_state"] = {
        "operation": "REPLACE",
        "after": {
            "standing": "ACTIVE",
            "valid_from_utc": "2026-07-22T21:05:49Z",
            "valid_until_utc": "2026-07-23T00:00:00Z",
            "revoked_by_event_id": None,
            "freshness": "EXPIRED_AT_REPLAY_CLOSURE",
        },
    }
    event["authority_effect"] = "CONFER"
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "AUTHORITY_EXPIRED_OR_REVOKED" in codes(result)


def test_event_cannot_precede_its_parent_closure() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    registry["events"][0]["occurred_at_utc"] = "2026-07-22T20:00:00Z"
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "EVENT_TIME_PRECEDES_PARENT" in codes(result)


def test_mutated_bound_review_receipt_is_rejected() -> None:
    checker = load_checker()
    contract, registry = inputs(checker)
    registry["events"][0]["evidence_refs"][0]["sha256"] = "0" * 64
    result = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
    )
    assert "EVIDENCE_DIGEST_MISMATCH" in codes(result)


def test_changed_projection_cache_is_rejected(tmp_path: Path) -> None:
    checker = load_checker()
    relative = Path("projection.json")
    (tmp_path / relative).write_text('{"changed":true}\n', encoding="utf-8")
    findings: list[dict[str, str]] = []
    checker.compare_cache(
        tmp_path,
        relative,
        {"changed": False},
        "PROJECTION_REDUCER_DIVERGENCE",
        findings,
    )
    assert {item["code"] for item in findings} == {
        "PROJECTION_REDUCER_DIVERGENCE"
    }


def test_adversarial_fixture_register_matches_executable_tests() -> None:
    checker = load_checker()
    fixture = json.loads((ROOT / checker.ADVERSARIAL_CASES).read_text(encoding="utf-8"))
    assert {item["expected_code"] for item in fixture["cases"]} == {
        "ADMISSION_EFFECT_MISMATCH",
        "AUTHORITY_EXPIRED_OR_REVOKED",
        "CONCURRENT_SUCCESSOR_UNRECONCILED",
        "CURRENT_HEAD_REVIEW_STALE",
        "EVENT_COVERAGE_UNRESOLVED",
        "EVENT_TIME_PRECEDES_PARENT",
        "EVIDENCE_DIGEST_MISMATCH",
        "EXECUTION_EFFECT_MISMATCH",
        "PROJECTION_REDUCER_DIVERGENCE",
        "UNDECLARED_DIMENSION_CHANGE",
    }
