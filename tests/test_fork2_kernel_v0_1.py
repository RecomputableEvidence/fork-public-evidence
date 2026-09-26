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


def test_r3_clean_selection_has_no_violation():
    selection = SelectionRecord("SEL-1", "S1", StandingEffect.NONE)
    assert check_r3_selection_no_standing_expansion(selection) == []


def test_r3_rejects_selection_standing_expansion():
    selection = SelectionRecord("SEL-1", "S1", StandingEffect.EXPAND)
    violations = check_r3_selection_no_standing_expansion(selection)
    assert [v.code for v in violations] == ["SELECTION_STANDING_EXPANSION"]
    assert violations[0].relation_id == "R3"


def test_r5_clean_historical_projection_preserves_result_and_disposition():
    transition = TransitionRecord(
        "T1",
        "S0",
        "S1",
        "RV1",
        AttemptResult.FAILED,
        AttemptResult.FAILED,
    )
    projection = TransitionProjection("T1", AttemptResult.FAILED, AttemptResult.FAILED)
    assert check_r5_no_retroactive_reinterpretation(transition, projection) == []


def test_r5_rejects_retroactive_result_and_disposition_rewrite():
    transition = TransitionRecord(
        "T1",
        "S0",
        "S1",
        "RV1",
        AttemptResult.FAILED,
        AttemptResult.FAILED,
    )
    projection = TransitionProjection("T1", AttemptResult.QUALIFIED, AttemptResult.QUALIFIED)
    violations = check_r5_no_retroactive_reinterpretation(transition, projection)
    assert {v.code for v in violations} == {
        "HISTORICAL_RESULT_REWRITE",
        "HISTORICAL_DISPOSITION_REWRITE",
    }
    assert {v.relation_id for v in violations} == {"R5"}


def test_r7a_failed_attempt_can_remain_addressable_outside_default_route():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=True)
    routing = RoutingState(("S0", "S1"))
    assert check_attempt_routing(attempt, routing) == []


def test_r7a_rejects_failed_attempt_in_default_qualified_route():
    attempt = AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED, addressable=True)
    routing = RoutingState(("S0", "FAILED-S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == ["FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE"]
    assert violations[0].relation_id == "R7a"


def test_r7b_unresolved_attempt_can_remain_addressable_outside_default_route():
    attempt = AttemptRecord("A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED, addressable=True)
    routing = RoutingState(("S0", "S1"))
    assert check_attempt_routing(attempt, routing) == []


def test_r7b_rejects_unresolved_attempt_in_default_qualified_route():
    attempt = AttemptRecord("A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED, addressable=True)
    routing = RoutingState(("S0", "UNRESOLVED-S1"))
    violations = check_attempt_routing(attempt, routing)
    assert [v.code for v in violations] == ["UNRESOLVED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE"]
    assert violations[0].relation_id == "R7b"


def test_combined_clean_kernel_state_passes():
    selection = SelectionRecord("SEL-1", "S1")
    transition = TransitionRecord(
        "T1",
        "S0",
        "S1",
        "RV1",
        AttemptResult.FAILED,
        AttemptResult.FAILED,
    )
    projection = TransitionProjection("T1", AttemptResult.FAILED, AttemptResult.FAILED)
    attempts = (
        AttemptRecord("A1", "FAILED-S1", AttemptResult.FAILED),
        AttemptRecord("A2", "UNRESOLVED-S1", AttemptResult.UNRESOLVED),
    )
    routing = RoutingState(("S0", "S1"))

    assert validate_kernel(
        selections=(selection,),
        historical_projections=((transition, projection),),
        attempts=attempts,
        routing=routing,
    ) == []


def test_status_does_not_promote_withheld_relations():
    status = json.loads((Path(__file__).parents[1] / "fork2" / "status.json").read_text())
    by_id = {entry["relation_id"]: entry for entry in status["relations"]}

    for relation_id in ("R1", "R2", "R4", "R6", "R8"):
        assert by_id[relation_id]["standing"] == "WITHHELD_PENDING_MORE_EVIDENCE"
        assert by_id[relation_id]["kernel_enforcement"] == "NONE"

    for relation_id in ("R3", "R5", "R7a", "R7b"):
        assert by_id[relation_id]["standing"] == "FROZEN"
