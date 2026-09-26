from fork2.routing import (
    RouteDisposition,
    RoutePhase,
    RoutingSnapshot,
    RoutingTransition,
    allowed_next_phases,
    validate_routing_transition,
)


def _transition(current, successor, *, basis, operations=()):
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


def test_pr189_clean_candidate_can_exit_with_authority_and_recomputation_limits_preserved():
    determine = RoutingSnapshot(
        "PR189-CANDIDATE",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=(
            "TECHNICAL_CANDIDATE_CLEAN",
            "AUTHORITY_ORIGIN_DECLARED_BOUNDED_NOT_EXTERNALLY_AUTHENTICATED",
            "FULL_PREDECESSOR_RECOMPUTATION_NOT_AVAILABLE_FROM_PR_ALONE",
        ),
    )
    outbound = RoutingSnapshot(
        "PR189-CANDIDATE",
        "O1",
        RoutePhase.OUTBOUND,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=determine.findings,
        predecessor_state_id="D1",
    )
    assert validate_routing_transition(
        determine,
        outbound,
        _transition(determine, outbound, basis="first-class PR189 boundary preserved"),
    ) == ()


def test_truncated_artifact_can_remediate_then_return_for_redetermination():
    determine_1 = RoutingSnapshot(
        "ARTIFACT-TRUNCATED",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("FILE_TRUNCATED", "SOURCE_INCOMPLETE"),
    )
    resolve = RoutingSnapshot(
        "ARTIFACT-TRUNCATED",
        "R1",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=determine_1.findings,
        predecessor_state_id="D1",
    )
    determine_2 = RoutingSnapshot(
        "ARTIFACT-TRUNCATED",
        "D2",
        RoutePhase.DETERMINE,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=("FILE_TRUNCATED_PRESERVED", "SOURCE_REESTABLISHED"),
        predecessor_state_id="R1",
    )
    assert validate_routing_transition(
        determine_1,
        resolve,
        _transition(determine_1, resolve, basis="truncation requires repair", operations=("RECOVER", "REPAIR")),
    ) == ()
    assert validate_routing_transition(
        resolve,
        determine_2,
        _transition(resolve, determine_2, basis="repair completed; redetermination required", operations=("REEXAMINE", "REDETERMINE")),
    ) == ()


def test_failed_recomputation_can_remain_unresolved_after_resolution_attempt():
    determine_1 = RoutingSnapshot(
        "FAILED-RECOMPUTATION",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.UNRESOLVED,
        findings=("RECOMPUTATION_FAILED",),
    )
    resolve = RoutingSnapshot(
        "FAILED-RECOMPUTATION",
        "R1",
        RoutePhase.RESOLVE,
        RouteDisposition.UNRESOLVED,
        findings=determine_1.findings,
        predecessor_state_id="D1",
    )
    determine_2 = RoutingSnapshot(
        "FAILED-RECOMPUTATION",
        "D2",
        RoutePhase.DETERMINE,
        RouteDisposition.UNRESOLVED,
        findings=("RECOMPUTATION_FAILED", "CAUSE_NOT_ESTABLISHED"),
        predecessor_state_id="R1",
    )
    assert validate_routing_transition(
        determine_1,
        resolve,
        _transition(determine_1, resolve, basis="attempt recomputation recovery", operations=("RECOMPUTE",)),
    ) == ()
    assert validate_routing_transition(
        resolve,
        determine_2,
        _transition(resolve, determine_2, basis="recomputation remains unresolved", operations=("REEXAMINE", "REDETERMINE")),
    ) == ()
    assert allowed_next_phases(determine_2) == (RoutePhase.RESOLVE,)


def test_pressure_unresolved_external_return_cannot_currently_exit_as_unresolved():
    current = RoutingSnapshot(
        "EXTERIOR-RETURN-UNBOUND",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.UNRESOLVED,
        findings=("EXTERIOR_RETURN_PRESERVED", "SOURCE_ORIGIN_NOT_BOUND"),
    )
    outbound = RoutingSnapshot(
        "EXTERIOR-RETURN-UNBOUND",
        "O1",
        RoutePhase.OUTBOUND,
        RouteDisposition.UNRESOLVED,
        findings=current.findings,
        predecessor_state_id="D1",
    )
    violations = validate_routing_transition(
        current,
        outbound,
        _transition(current, outbound, basis="emit bounded unresolved return"),
    )
    codes = {v.code for v in violations}
    assert "ROUTE_NOT_PERMITTED" in codes
    assert "OUTBOUND_WITH_NONTERMINAL_DISPOSITION" in codes


def test_pressure_material_revision_cannot_silently_substitute_subject_identity():
    current = RoutingSnapshot(
        "ARTIFACT-A",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("CONTENT_REPAIR_REQUIRED",),
    )
    revised = RoutingSnapshot(
        "ARTIFACT-A-REV1",
        "R1",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("REVISED_VERSION",),
        predecessor_state_id="D1",
    )
    violations = validate_routing_transition(
        current,
        revised,
        _transition(current, revised, basis="material revision created successor artifact", operations=("REVISE",)),
    )
    assert "SUBJECT_ID_CHANGED" in {v.code for v in violations}


def test_router_does_not_infer_disposition_from_findings():
    current = RoutingSnapshot(
        "ADVERSE-FINDING-SUBJECT",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=("SOURCE_INCOMPLETE", "AUTHORITY_NOT_ESTABLISHED"),
    )
    assert allowed_next_phases(current) == (RoutePhase.OUTBOUND,)


def test_resolution_cannot_skip_redetermination_even_after_repair_operation():
    current = RoutingSnapshot(
        "REPAIR-NO-PROMOTION",
        "R1",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("SOURCE_INCOMPLETE",),
    )
    outbound = RoutingSnapshot(
        "REPAIR-NO-PROMOTION",
        "O1",
        RoutePhase.OUTBOUND,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=("SOURCE_REESTABLISHED",),
        predecessor_state_id="R1",
    )
    violations = validate_routing_transition(
        current,
        outbound,
        _transition(current, outbound, basis="repair completed", operations=("REPAIR",)),
    )
    assert "ROUTE_NOT_PERMITTED" in {v.code for v in violations}


def test_archive_only_preserves_failure_findings_at_outbound():
    current = RoutingSnapshot(
        "HISTORICAL-FAILED-ATTEMPT",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.ARCHIVE_ONLY,
        findings=("FAILED_ATTEMPT", "HISTORICALLY_ADDRESSABLE", "NOT_DEFAULT_ROUTE"),
    )
    outbound = RoutingSnapshot(
        "HISTORICAL-FAILED-ATTEMPT",
        "O1",
        RoutePhase.OUTBOUND,
        RouteDisposition.ARCHIVE_ONLY,
        findings=current.findings,
        predecessor_state_id="D1",
    )
    assert validate_routing_transition(
        current,
        outbound,
        _transition(current, outbound, basis="retain historical failure outside active routing"),
    ) == ()


def test_discard_only_is_terminal_routing_not_event_erasure():
    current = RoutingSnapshot(
        "INVALID-INGRESS",
        "D1",
        RoutePhase.DETERMINE,
        RouteDisposition.DISCARD_ONLY,
        findings=("INVALID_FORMAT", "RECEIPT_EVENT_PRESERVED"),
    )
    outbound = RoutingSnapshot(
        "INVALID-INGRESS",
        "O1",
        RoutePhase.OUTBOUND,
        RouteDisposition.DISCARD_ONLY,
        findings=current.findings,
        predecessor_state_id="D1",
    )
    assert validate_routing_transition(
        current,
        outbound,
        _transition(current, outbound, basis="invalid ingress excluded from active use; receipt retained"),
    ) == ()
