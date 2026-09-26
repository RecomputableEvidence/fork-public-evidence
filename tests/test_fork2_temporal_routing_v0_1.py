from fork2.routing import (
    RouteDisposition,
    RoutePhase,
    RoutingSnapshot,
    RoutingTransition,
    allowed_next_phases,
    validate_routing_transition,
)


def _transition(current, successor, *, basis="bounded test basis", operations=()):
    return RoutingTransition(
        transition_id=f"TR-{current.state_id}-{successor.state_id}",
        subject_id=current.subject_id,
        from_state_id=current.state_id,
        to_state_id=successor.state_id,
        from_phase=current.phase,
        to_phase=successor.phase,
        basis=basis,
        operations=operations,
    )


def test_happy_path_clear_subject_routes_inbound_to_outbound():
    inbound = RoutingSnapshot("OBJ-1", "R0", RoutePhase.INBOUND)
    examine = RoutingSnapshot(
        "OBJ-1", "R1", RoutePhase.EXAMINE, predecessor_state_id="R0"
    )
    determine = RoutingSnapshot(
        "OBJ-1",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        findings=("FORMAT_OK", "SOURCE_PRESENT"),
        predecessor_state_id="R1",
    )
    outbound = RoutingSnapshot(
        "OBJ-1",
        "R3",
        RoutePhase.OUTBOUND,
        RouteDisposition.CLEAR,
        findings=determine.findings,
        predecessor_state_id="R2",
    )

    assert validate_routing_transition(inbound, examine, _transition(inbound, examine)) == ()
    assert validate_routing_transition(examine, determine, _transition(examine, determine)) == ()
    assert validate_routing_transition(determine, outbound, _transition(determine, outbound)) == ()


def test_remediation_loop_returns_to_determine_before_outbound():
    determine_1 = RoutingSnapshot(
        "OBJ-2",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("SOURCE_INCOMPLETE",),
    )
    resolve = RoutingSnapshot(
        "OBJ-2",
        "R3",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("SOURCE_INCOMPLETE",),
        predecessor_state_id="R2",
    )
    determine_2 = RoutingSnapshot(
        "OBJ-2",
        "R4",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        findings=("SOURCE_REESTABLISHED",),
        predecessor_state_id="R3",
    )
    outbound = RoutingSnapshot(
        "OBJ-2",
        "R5",
        RoutePhase.OUTBOUND,
        RouteDisposition.CLEAR,
        findings=("SOURCE_REESTABLISHED",),
        predecessor_state_id="R4",
    )

    assert validate_routing_transition(determine_1, resolve, _transition(determine_1, resolve, operations=("REPAIR",))) == ()
    assert validate_routing_transition(resolve, determine_2, _transition(resolve, determine_2, operations=("REEXAMINE", "REDETERMINE"))) == ()
    assert validate_routing_transition(determine_2, outbound, _transition(determine_2, outbound)) == ()


def test_unresolved_subject_must_enter_resolution_not_outbound():
    current = RoutingSnapshot(
        "OBJ-3", "R2", RoutePhase.DETERMINE, RouteDisposition.UNRESOLVED
    )
    outbound = RoutingSnapshot(
        "OBJ-3",
        "R3",
        RoutePhase.OUTBOUND,
        RouteDisposition.CLEAR,
        predecessor_state_id="R2",
    )
    violations = validate_routing_transition(current, outbound, _transition(current, outbound))
    assert "ROUTE_NOT_PERMITTED" in {v.code for v in violations}


def test_archive_only_and_discard_only_are_terminal_routes_not_findings():
    archive = RoutingSnapshot(
        "OBJ-4", "R2", RoutePhase.DETERMINE, RouteDisposition.ARCHIVE_ONLY
    )
    discard = RoutingSnapshot(
        "OBJ-5", "R2", RoutePhase.DETERMINE, RouteDisposition.DISCARD_ONLY
    )
    assert allowed_next_phases(archive) == (RoutePhase.OUTBOUND,)
    assert allowed_next_phases(discard) == (RoutePhase.OUTBOUND,)


def test_open_finding_vocabulary_does_not_create_new_route_types():
    current = RoutingSnapshot(
        "OBJ-6",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("FILE_TRUNCATED", "OBSERVATION_TRUNCATED", "SOMETHING_NEVER_SEEN_BEFORE"),
    )
    assert allowed_next_phases(current) == (RoutePhase.RESOLVE,)


def test_resolution_operation_vocabulary_is_open():
    current = RoutingSnapshot(
        "OBJ-7", "R2", RoutePhase.DETERMINE, RouteDisposition.REMEDIATION_REQUIRED
    )
    successor = RoutingSnapshot(
        "OBJ-7",
        "R3",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        predecessor_state_id="R2",
    )
    transition = _transition(
        current,
        successor,
        operations=("RECOMPUTE", "RECOVER", "CUSTOM_OPERATION_X"),
    )
    assert validate_routing_transition(current, successor, transition) == ()


def test_direct_inbound_to_outbound_is_rejected():
    current = RoutingSnapshot("OBJ-8", "R0", RoutePhase.INBOUND)
    successor = RoutingSnapshot(
        "OBJ-8",
        "R1",
        RoutePhase.OUTBOUND,
        RouteDisposition.CLEAR,
        predecessor_state_id="R0",
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor))
    assert "ROUTE_NOT_PERMITTED" in {v.code for v in violations}


def test_examination_cannot_predeclare_final_disposition():
    current = RoutingSnapshot("OBJ-9", "R0", RoutePhase.INBOUND)
    successor = RoutingSnapshot(
        "OBJ-9",
        "R1",
        RoutePhase.EXAMINE,
        RouteDisposition.CLEAR,
        predecessor_state_id="R0",
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor))
    assert "EXAMINE_DISPOSITION_NOT_UNDETERMINED" in {v.code for v in violations}


def test_determination_requires_a_disposition():
    current = RoutingSnapshot("OBJ-10", "R1", RoutePhase.EXAMINE)
    successor = RoutingSnapshot(
        "OBJ-10", "R2", RoutePhase.DETERMINE, predecessor_state_id="R1"
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor))
    assert "DETERMINATION_MISSING_DISPOSITION" in {v.code for v in violations}


def test_outbound_is_terminal():
    outbound = RoutingSnapshot(
        "OBJ-11", "R3", RoutePhase.OUTBOUND, RouteDisposition.CLEAR
    )
    assert allowed_next_phases(outbound) == ()


def test_subject_substitution_is_rejected():
    current = RoutingSnapshot("OBJ-12", "R1", RoutePhase.EXAMINE)
    successor = RoutingSnapshot(
        "OTHER",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        predecessor_state_id="R1",
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor))
    assert "SUBJECT_ID_CHANGED" in {v.code for v in violations}


def test_successor_must_bind_predecessor_state():
    current = RoutingSnapshot("OBJ-13", "R1", RoutePhase.EXAMINE)
    successor = RoutingSnapshot(
        "OBJ-13",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        predecessor_state_id="WRONG",
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor))
    assert "PREDECESSOR_BINDING_MISMATCH" in {v.code for v in violations}


def test_routing_transition_requires_explicit_basis():
    current = RoutingSnapshot("OBJ-14", "R1", RoutePhase.EXAMINE)
    successor = RoutingSnapshot(
        "OBJ-14",
        "R2",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        predecessor_state_id="R1",
    )
    violations = validate_routing_transition(current, successor, _transition(current, successor, basis=""))
    assert "TRANSITION_BASIS_MISSING" in {v.code for v in violations}


def test_state_id_may_not_be_reused_across_temporal_transition():
    current = RoutingSnapshot("OBJ-15", "R1", RoutePhase.EXAMINE)
    successor = RoutingSnapshot(
        "OBJ-15",
        "R1",
        RoutePhase.DETERMINE,
        RouteDisposition.CLEAR,
        predecessor_state_id="R1",
    )
    transition = RoutingTransition(
        "TR-1",
        "OBJ-15",
        "R1",
        "R1",
        RoutePhase.EXAMINE,
        RoutePhase.DETERMINE,
        "bounded test basis",
    )
    violations = validate_routing_transition(current, successor, transition)
    assert "STATE_ID_REUSED" in {v.code for v in violations}
