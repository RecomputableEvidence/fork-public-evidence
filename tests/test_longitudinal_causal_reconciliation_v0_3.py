from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_longitudinal_causal_reconciliation_v0_3.py"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "fork_longitudinal_causal_reconciliation_v0_3",
        CHECKER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs(checker):
    base = checker.predecessor(ROOT)
    contract = base.strict_load(ROOT / checker.CONTRACT)
    registry = base.strict_load(ROOT / checker.REGISTRY)
    return base, contract, registry


def codes(result) -> set[str]:
    return set(result["finding_codes"])


def evaluate_mutation(checker, contract, registry):
    return checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
        verify_predecessor=False,
    )


def event(registry, event_id):
    return next(item for item in registry["events"] if item["event_id"] == event_id)


def test_exact_causal_reconciliation_surface_conforms() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["findings"] == []
    assert result["status"] == "CAUSAL_RECONCILIATION_REPRODUCED"
    assert result["coverage_receipt"]["result"] == (
        "FRONTIER_BOUNDED_CAUSAL_COVERAGE_REPRODUCED"
    )
    assert result["reconciliation_receipt"]["result"] == (
        "EXPLICIT_CAUSAL_RECONCILIATION_REPRODUCED"
    )


def test_projection_replays_real_two_root_git_frontier() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT, verify_committed=False)
    projection = result["projection"]
    assert result["findings"] == []
    assert projection["active_event_heads"] == [
        "0bac4f60986e0be4da53d6b69c49aab1f7e73e7d"
    ]
    assert projection["state_vector"]["verification_state"] == {
        "root_checksum_surface": "ENFORCED_WITH_DISCREPANCY_PRESERVED",
        "sequence_surface": "AUTHORIZATION_AND_RETRY_OUTCOMES_BOUND",
        "standing": "SEQUENCE_AND_CHECKSUM_LINEAGES_JOINED",
    }
    assert projection["state_vector"]["admission_state"]["standing"] == "NONE"
    assert projection["effects"]["provider_calls"] == 0
    assert projection["effects"]["pair_001_calls"] == 0


def test_registry_order_does_not_control_causal_order() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    expected = checker.evaluate(
        ROOT,
        contract_override=contract,
        registry_override=registry,
        verify_committed=False,
        verify_predecessor=False,
    )
    registry["events"] = list(reversed(registry["events"]))
    shuffled = evaluate_mutation(checker, contract, registry)
    assert shuffled["findings"] == []
    assert shuffled["projection"] == expected["projection"]
    assert shuffled["reconciliation_receipt"] == expected["reconciliation_receipt"]


def test_concurrent_coordinate_diff_preserves_equal_boundaries() -> None:
    checker = load_checker()
    delta = checker.causal_diff(
        ROOT,
        "c879242c4dafad68bdd8e7bcf2466e4169351969",
        "5150ece4c29cea38cfe5e25daeb781423c680834",
    )
    assert delta["status"] == "CAUSAL_DIFF_REPRODUCED"
    assert delta["divergent_dimensions"] == [
        "artifact_state",
        "temporal_closure",
        "unresolved_state",
        "verification_state",
    ]
    assert delta["equal_dimensions"] == [
        "admission_state",
        "authority_state",
        "execution_state",
        "review_state",
    ]


def test_merge_inventory_binds_each_parent_delta() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT, verify_committed=False)
    inventory = {
        item["commit_sha"]: item
        for item in result["coverage_receipt"]["git_inventory"]
    }
    merge = inventory["0bac4f60986e0be4da53d6b69c49aab1f7e73e7d"]
    assert merge["changed_paths"] == []
    assert merge["parent_deltas"][
        "97abe21daed2daec8a608851467875df42a99f0a"
    ]
    assert merge["parent_deltas"][
        "5150ece4c29cea38cfe5e25daeb781423c680834"
    ]


def test_missing_frontier_event_is_unresolved_not_absent() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    registry["events"] = registry["events"][1:]
    result = evaluate_mutation(checker, contract, registry)
    assert "CAUSAL_COVERAGE_UNRESOLVED" in codes(result)


def test_changed_parent_delta_breaks_git_binding() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    join["parent_deltas"][
        "97abe21daed2daec8a608851467875df42a99f0a"
    ] = []
    result = evaluate_mutation(checker, contract, registry)
    assert "CAUSAL_EVENT_GIT_BINDING_MISMATCH" in codes(result)


def test_merge_requires_every_dimension_decision() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    del join["reconciliation_decisions"]["unresolved_state"]
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_DECISION_MISSING" in codes(result)


def test_require_equal_rejects_divergent_inputs() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    join["reconciliation_decisions"]["verification_state"]["policy"] = "REQUIRE_EQUAL"
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_EQUALITY_VIOLATION" in codes(result)


def test_selected_parent_output_must_match_selected_bytes() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E003-SEQUENCE-LINEAGE-JOIN")
    decision = join["reconciliation_decisions"]["verification_state"]
    decision["policy"] = "SELECT_PARENT"
    decision["selected_parent"] = (
        "c879242c4dafad68bdd8e7bcf2466e4169351969"
    )
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_RESULT_MISMATCH" in codes(result)


def test_parent_dimension_digest_is_recomputed() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    decision = join["reconciliation_decisions"]["verification_state"]
    parent = next(iter(decision["parent_state_sha256"]))
    decision["parent_state_sha256"][parent] = "0" * 64
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_INPUT_DIGEST_MISMATCH" in codes(result)


def test_merge_result_digest_is_recomputed() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    join["reconciliation_decisions"]["verification_state"][
        "result_sha256"
    ] = "0" * 64
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_RESULT_DIGEST_MISMATCH" in codes(result)


def test_silent_admission_change_is_rejected() -> None:
    checker = load_checker()
    base, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    decision = join["reconciliation_decisions"]["admission_state"]
    decision["policy"] = "EXPLICIT_JOIN"
    decision["result"] = {"standing": "ADMITTED", "basis": "SYNTHETIC"}
    decision["result_sha256"] = base.state_sha256(decision["result"])
    result = evaluate_mutation(checker, contract, registry)
    assert "ADMISSION_EFFECT_MISMATCH" in codes(result)


def test_frontier_state_digest_is_not_trusted() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    registry["frontier"]["anchors"][0]["state_sha256"] = "0" * 64
    result = evaluate_mutation(checker, contract, registry)
    assert "FRONTIER_STATE_DIGEST_MISMATCH" in codes(result)


def test_explicit_join_is_not_allowed_to_hide_equal_inputs() -> None:
    checker = load_checker()
    _, contract, registry = inputs(checker)
    join = event(registry, "FCR-E004-SEQUENCE-CHECKSUM-JOIN")
    join["reconciliation_decisions"]["review_state"]["policy"] = "EXPLICIT_JOIN"
    result = evaluate_mutation(checker, contract, registry)
    assert "MERGE_POLICY_OVERBROAD" in codes(result)


def test_changed_projection_cache_is_rejected(tmp_path: Path) -> None:
    checker = load_checker()
    base = checker.predecessor(ROOT)
    relative = Path("projection.json")
    (tmp_path / relative).write_text('{"changed":true}\n', encoding="utf-8")
    findings: list[dict[str, str]] = []
    checker.compare_cache(
        tmp_path,
        relative,
        {"changed": False},
        "PROJECTION_CACHE_DIVERGENCE",
        base,
        findings,
    )
    assert {item["code"] for item in findings} == {
        "PROJECTION_CACHE_DIVERGENCE"
    }


def test_predecessor_manifest_bytes_are_preserved_and_scope_is_versioned() -> None:
    checker = load_checker()
    base = checker.predecessor(ROOT)
    historical = (
        ROOT
        / "docs/state/longitudinal-recomputation-v0.2/PACKAGE_MANIFEST_v0_2.json"
    )
    assert base.sha256_file(historical) == (
        "d2bbfc8fa6ec31872071706a85a036164baeb93de4a57287d2d790164463f4fa"
    )
    successor = base.strict_load(ROOT / checker.PREDECESSOR_MANIFEST)
    paths = {item["path"] for item in successor["entries"]}
    assert "docs/state/README.md" not in paths
    assert (
        "receipts/claim-admission/"
        "FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json"
    ) not in paths


def test_adversarial_register_matches_executable_cases() -> None:
    checker = load_checker()
    fixture = json.loads((ROOT / checker.ADVERSARIAL_CASES).read_text(encoding="utf-8"))
    assert {item["expected_code"] for item in fixture["cases"] if "expected_code" in item} == {
        "ADMISSION_EFFECT_MISMATCH",
        "CAUSAL_COVERAGE_UNRESOLVED",
        "CAUSAL_EVENT_GIT_BINDING_MISMATCH",
        "FRONTIER_STATE_DIGEST_MISMATCH",
        "MERGE_DECISION_MISSING",
        "MERGE_EQUALITY_VIOLATION",
        "MERGE_INPUT_DIGEST_MISMATCH",
        "MERGE_POLICY_OVERBROAD",
        "MERGE_RESULT_DIGEST_MISMATCH",
        "MERGE_RESULT_MISMATCH",
        "PROJECTION_CACHE_DIVERGENCE",
    }
