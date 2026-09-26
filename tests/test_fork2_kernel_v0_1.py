import json
from pathlib import Path

from fork2.kernel import (
    check_attempt_routing,
    check_r3_selection_no_standing_expansion,
    check_r5_no_retroactive_reinterpretation,
    validate_kernel,
)
from fork2.model import (
    AttemptRecord,
    AttemptResult,
    RoutingState,
    SelectionRecord,
    StandingEffect,
    TransitionProjection,
    TransitionRecord,
)


def _transition() -> TransitionRecord:
    return TransitionRecord(
        "T1",
        "S0",
        "S1",
        "RV1",
        AttemptResult.FAILED,
        AttemptResult.FAILED,
    )


def test_r3_clean_selection_has_no_violation():
    selection = SelectionRecord("SEL-1", "S1", StandingEffect.NONE)
    assert check_r3_selection_no_standing_expansion(selection) == []


def test_r3_rejects_selection_standing_expansion():
    selection = SelectionRecord("SEL-1", "S1", StandingEffect.EXPAND)
    violations = check_r3_selection_no_standing_expansion(selection)
    assert [v.code for v in violations] == ["SELECTION_STANDING_EXPANSION"]
    assert violations[0].relation_id == "R3"


def test_r5_clean_later_rule_projection_preserves_result_and_disposition():
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.FAILED, AttemptResult.FAILED
    )
    assert check_r5_no_retroactive_reinterpretation(_transition(), projection) == []


def test_r5_rejects_transition_id_mismatch():
    projection = TransitionProjection(
        "OTHER", "RV2", AttemptResult.FAILED, AttemptResult.FAILED
    )
    violations = check_r5_no_retroactive_reinterpretation(_transition(), projection)
    assert [v.code for v in violations] == ["TRANSITION_ID_MISMATCH"]


def test_r5_rejects_same_rule_context_claimed_as_later():
    projection = TransitionProjection(
        "T1", "RV1", AttemptResult.FAILED, AttemptResult.FAILED
    )
    violations = check_r5_no_retroactive_reinterpretation(_transition(), projection)
    assert [v.code for v in violations] == ["LATER_RULE_CONTEXT_NOT_DISTINCT"]


def test_r5_rejects_result_only_rewrite():
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.QUALIFIED, AttemptResult.FAILED
    )
    violations = check_r5_no_retroactive_reinterpretation(_transition(), projection)
    assert [v.code for v in violations] == ["HISTORICAL_RESULT_REWRITE"]


def test_r5_rejects_disposition_only_rewrite():
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.FAILED, AttemptResult.QUALIFIED
    )
    violations = check_r5_no_retroactive_reinterpretation(_transition(), projection)
    assert [v.code for v in violations] == ["HISTORICAL_DISPOSITION_REWRITE"]


def test_r5_rejects_result_and_disposition_rewrite():
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.QUALIFIED, AttemptResult.QUALIFIED
    )
    violations = check_r5_no_retroactive_reinterpretation(_transition(), projection)
    assert {v.code for v in violations} == {
        "HISTORICAL_RESULT_REWRITE",
        "HISTORICAL_DISPOSITION_REWRITE",
    }


def test_r7a_failed_attempt_must_remain_addressable():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=False)
    routing = RoutingState(("S0", "S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == ["FAILED_ATTEMPT_NOT_ADDRESSABLE"]
    assert violations[0].relation_id == "R7a"


def test_r7a_failed_attempt_can_remain_addressable_outside_default_route():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=True)
    routing = RoutingState(("S0", "S1"))
    assert check_attempt_routing(attempt, routing) == []


def test_r7a_rejects_failed_attempt_in_default_qualified_route():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=True)
    routing = RoutingState(("S0", "FAILED-S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == ["FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE"]


def test_r7b_unresolved_attempt_must_remain_addressable():
    attempt = AttemptRecord(
        "A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED, addressable=False
    )
    routing = RoutingState(("S0", "S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == ["UNRESOLVED_ATTEMPT_NOT_ADDRESSABLE"]
    assert violations[0].relation_id == "R7b"


def test_r7b_unresolved_attempt_can_remain_addressable_outside_default_route():
    attempt = AttemptRecord(
        "A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED, addressable=True
    )
    routing = RoutingState(("S0", "S1"))
    assert check_attempt_routing(attempt, routing) == []


def test_r7b_rejects_unresolved_attempt_in_default_qualified_route():
    attempt = AttemptRecord(
        "A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED, addressable=True
    )
    routing = RoutingState(("S0", "UNRESOLVED-S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == [
        "UNRESOLVED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE"
    ]


def test_attempt_can_violate_addressability_and_routing_conjuncts_together():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=False)
    routing = RoutingState(("FAILED-S1",))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == [
        "FAILED_ATTEMPT_NOT_ADDRESSABLE",
        "FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
    ]


def test_combined_clean_kernel_state_passes():
    selection = SelectionRecord("SEL-1", "S1")
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.FAILED, AttemptResult.FAILED
    )
    attempts = (
        AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED),
        AttemptRecord("A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED),
    )
    routing = RoutingState(("S0", "S1"))

    assert validate_kernel(
        selections=(selection,),
        historical_projections=((_transition(), projection),),
        attempts=attempts,
        routing=routing,
    ) == []


def test_validate_kernel_aggregates_mixed_violations():
    selection = SelectionRecord("SEL-1", "S1", StandingEffect.EXPAND)
    projection = TransitionProjection(
        "T1", "RV2", AttemptResult.QUALIFIED, AttemptResult.FAILED
    )
    attempts = (
        AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=False),
        AttemptRecord("A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED),
    )
    routing = RoutingState(("FAILED-S1", "UNRESOLVED-S1"))

    violations = validate_kernel(
        selections=(selection,),
        historical_projections=((_transition(), projection),),
        attempts=attempts,
        routing=routing,
    )

    assert [v.code for v in violations] == [
        "SELECTION_STANDING_EXPANSION",
        "HISTORICAL_RESULT_REWRITE",
        "FAILED_ATTEMPT_NOT_ADDRESSABLE",
        "FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
        "UNRESOLVED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
    ]


def test_status_exact_relation_population_and_enforcement_mapping():
    status = json.loads(
        (Path(__file__).parents[1] / "fork2" / "status.json").read_text()
    )
    by_id = {entry["relation_id"]: entry for entry in status["relations"]}

    expected = {
        "R1": ("WITHHELD_PENDING_MORE_EVIDENCE", "NONE"),
        "R2": ("WITHHELD_PENDING_MORE_EVIDENCE", "NONE"),
        "R3": ("FROZEN", "check_r3_selection_no_standing_expansion"),
        "R4": ("WITHHELD_PENDING_MORE_EVIDENCE", "NONE"),
        "R5": ("FROZEN", "check_r5_no_retroactive_reinterpretation"),
        "R6": ("WITHHELD_PENDING_MORE_EVIDENCE", "NONE"),
        "R7a": ("FROZEN", "check_attempt_routing"),
        "R7b": ("FROZEN", "check_attempt_routing"),
        "R8": ("WITHHELD_PENDING_MORE_EVIDENCE", "NONE"),
    }

    assert set(by_id) == set(expected)
    for relation_id, (standing, enforcement) in expected.items():
        assert by_id[relation_id]["standing"] == standing
        assert by_id[relation_id]["kernel_enforcement"] == enforcement
        assert by_id[relation_id]["standing_source"] == (
            f"fork2/provenance.json#relations.{relation_id}"
        )


def test_provenance_relation_standing_matches_status_and_bound_records():
    import hashlib

    repo = Path(__file__).parents[1]
    base = repo / "fork2"
    status = json.loads((base / "status.json").read_text())
    provenance = json.loads((base / "provenance.json").read_text())

    p_relations = provenance["relations"]
    for entry in status["relations"]:
        relation_id = entry["relation_id"]
        assert p_relations[relation_id]["operative_standing"] == entry["standing"]

    assert provenance["authorization"]["authority_external_verification"] == (
        "NOT_ESTABLISHED"
    )
    presence = provenance["repository_presence"]
    assert presence["source_package_bytes_embedded"] is False
    assert presence["bound_record_bytes_embedded"] is True

    for key, rel_path in presence["bound_record_paths"].items():
        digest = hashlib.sha256((repo / rel_path).read_bytes()).hexdigest()
        assert digest == provenance["bound_records"][f"{key}_sha256"]
