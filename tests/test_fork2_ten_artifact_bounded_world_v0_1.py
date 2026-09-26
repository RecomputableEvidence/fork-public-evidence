from dataclasses import dataclass
from typing import Tuple

from fork2.routing import (
    RouteDisposition,
    RoutePhase,
    RoutingSnapshot,
    RoutingTransition,
    validate_routing_transition,
)


@dataclass(frozen=True)
class EvidencePoint:
    artifact_id: str
    coordinate: str
    content_id: str
    authority: str = "NONE"
    claims: Tuple[str, ...] = ()
    findings: Tuple[str, ...] = ()


@dataclass(frozen=True)
class Relation:
    subject_id: str
    relation: str
    object_id: str


def _transition(current: RoutingSnapshot, successor: RoutingSnapshot, *, basis: str) -> RoutingTransition:
    return RoutingTransition(
        transition_id=f"TR-{current.state_id}-{successor.state_id}",
        subject_id=current.subject_id,
        from_state_id=current.state_id,
        to_state_id=successor.state_id,
        from_phase=current.phase,
        to_phase=successor.phase,
        basis=basis,
    )


def _assert_path(path: Tuple[RoutingSnapshot, ...], *, basis_prefix: str) -> None:
    for index, (current, successor) in enumerate(zip(path, path[1:]), start=1):
        violations = validate_routing_transition(
            current,
            successor,
            _transition(current, successor, basis=f"{basis_prefix}-{index}"),
        )
        assert violations == ()


def _standard_path(subject_id: str, findings: Tuple[str, ...] = ()) -> Tuple[RoutingSnapshot, ...]:
    return (
        RoutingSnapshot(subject_id, f"{subject_id}-R0", RoutePhase.INBOUND),
        RoutingSnapshot(
            subject_id,
            f"{subject_id}-R1",
            RoutePhase.EXAMINE,
            findings=findings,
            predecessor_state_id=f"{subject_id}-R0",
        ),
        RoutingSnapshot(
            subject_id,
            f"{subject_id}-R2",
            RoutePhase.DETERMINE,
            RouteDisposition.OUTBOUND_ELIGIBLE,
            findings=findings,
            predecessor_state_id=f"{subject_id}-R1",
        ),
        RoutingSnapshot(
            subject_id,
            f"{subject_id}-R3",
            RoutePhase.OUTBOUND,
            RouteDisposition.OUTBOUND_ELIGIBLE,
            findings=findings,
            predecessor_state_id=f"{subject_id}-R2",
        ),
    )


# Ten deliberately heterogeneous artefact roots. Versions/branches remain separate
# identities and are connected only by explicit relations below.
ROOT_ARTIFACT_IDS = (
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "A6",
    "A7",
    "A8",
    "A9",
    "A10",
)


# A1 — immutable source document.
A1_POINTS = (
    EvidencePoint("A1", "T0", "sha:A1:H1", findings=("SOURCE_RECEIVED",)),
    EvidencePoint("A1", "T4", "sha:A1:H1", findings=("CLAIM_ATTACHED",)),
    EvidencePoint("A1", "T9", "sha:A1:H1", findings=("ARCHIVE_READY",)),
)

# A2 — materially revised report. Each byte-changing revision is a new identity.
A2_POINTS = (
    EvidencePoint("A2.1", "T0", "sha:A2:H1", findings=("DEFECT_PRESENT",)),
    EvidencePoint("A2.2", "T4", "sha:A2:H2", findings=("FIRST_REPAIR_APPLIED",)),
    EvidencePoint("A2.3", "T8", "sha:A2:H3", findings=("SECOND_REPAIR_APPLIED",)),
)
A2_RELATIONS = (
    Relation("A2.2", "SUCCESSOR_OF", "A2.1"),
    Relation("A2.3", "SUCCESSOR_OF", "A2.2"),
)

# A3 — bytes are stable while authority changes over time.
A3_POINTS = (
    EvidencePoint("A3", "T0", "sha:A3:H1", authority="ACTIVE"),
    EvidencePoint("A3", "T5", "sha:A3:H1", authority="EXPIRED"),
    EvidencePoint("A3", "T8", "sha:A3:H1", authority="REESTABLISHED_NEW_BASIS"),
)

# A4 — claim support changes while artefact identity remains stable.
A4_POINTS = (
    EvidencePoint("A4", "T0", "sha:A4:H1", claims=("CLAIM_C1_UNRESOLVED",)),
    EvidencePoint("A4", "T6", "sha:A4:H1", claims=("CLAIM_C1_BOUNDED_SUPPORT",)),
)

# A5 — observation becomes truncated; nearby evidence must not fill the gap.
A5_POINTS = (
    EvidencePoint("A5", "T0", "sha:A5:H1", findings=("OBSERVATION_COMPLETE",)),
    EvidencePoint("A5", "T3", "sha:A5:H1", findings=("OBSERVATION_TRUNCATED",)),
)

# A6 — exterior return remains bounded because source origin is not bound.
A6_POINTS = (
    EvidencePoint(
        "A6",
        "T4",
        "sha:A6:H1",
        findings=("EXTERIOR_RETURN_PRESERVED", "SOURCE_ORIGIN_NOT_BOUND"),
    ),
)

# A7 — failed recomputation remains historical after successor pass.
A7_POINTS = (
    EvidencePoint("A7.1", "T2", "sha:A7:H1", findings=("RECOMPUTATION_FAILED",)),
    EvidencePoint(
        "A7.2",
        "T7",
        "sha:A7:H2",
        findings=("RECOMPUTATION_PASS", "PREDECESSOR_FAILURE_PRESERVED"),
    ),
)
A7_RELATIONS = (Relation("A7.2", "SUCCESSOR_OF", "A7.1"),)

# A8 — branch siblings carry independent standing.
A8_POINTS = (
    EvidencePoint("A8", "T0", "sha:A8:H0"),
    EvidencePoint("A8.B1", "T5", "sha:A8:B1", findings=("RECOMPUTATION_PASS",)),
    EvidencePoint("A8.B2", "T5", "sha:A8:B2", findings=("PROVENANCE_UNRESOLVED",)),
)
A8_RELATIONS = (
    Relation("A8.B1", "DERIVED_FROM", "A8"),
    Relation("A8.B2", "DERIVED_FROM", "A8"),
)

# A9 — merge preserves parent-specific differences rather than flattening them.
A9_POINTS = (
    EvidencePoint(
        "A9",
        "T7",
        "sha:A9:H1",
        findings=(
            "PARENT_A8.B1_RECOMPUTATION_PASS",
            "PARENT_A8.B2_PROVENANCE_UNRESOLVED",
            "MERGE_STANDING_BOUNDED",
        ),
    ),
)
A9_RELATIONS = (
    Relation("A9", "MERGES", "A8.B1"),
    Relation("A9", "MERGES", "A8.B2"),
)

# A10 — identity mismatch is preserved and routed to remediation/disposal.
A10_POINTS = (
    EvidencePoint("A10", "T0", "sha:A10:H1", findings=("BOUND_IDENTITY_PRESENT",)),
    EvidencePoint("A10", "T4", "sha:A10:H2", findings=("BOUND_CONTENT_IDENTITY_MISMATCH",)),
)


ALL_POINTS = (
    *A1_POINTS,
    *A2_POINTS,
    *A3_POINTS,
    *A4_POINTS,
    *A5_POINTS,
    *A6_POINTS,
    *A7_POINTS,
    *A8_POINTS,
    *A9_POINTS,
    *A10_POINTS,
)


# Population-level identity / non-absorption tests.
def test_population_contains_exactly_ten_distinct_root_artifacts():
    assert len(ROOT_ARTIFACT_IDS) == 10
    assert len(set(ROOT_ARTIFACT_IDS)) == 10


def test_all_material_successor_and_branch_identities_remain_distinct():
    ids = [point.artifact_id for point in ALL_POINTS]
    materially_distinct = {
        "A2.1",
        "A2.2",
        "A2.3",
        "A7.1",
        "A7.2",
        "A8",
        "A8.B1",
        "A8.B2",
        "A9",
    }
    assert materially_distinct.issubset(set(ids))
    assert len(materially_distinct) == 9


def test_no_cross_lineage_property_is_inherited_by_adjacency():
    by_id = {point.artifact_id: point for point in ALL_POINTS}
    assert "RECOMPUTATION_PASS" in by_id["A8.B1"].findings
    assert "RECOMPUTATION_PASS" not in by_id["A8.B2"].findings
    assert by_id["A3"].authority != by_id["A4"].authority
    assert "OBSERVATION_TRUNCATED" in by_id["A5"].findings
    assert "OBSERVATION_TRUNCATED" not in by_id["A1"].findings


# Artefact-specific temporal tests.
def test_a1_immutable_source_identity_is_constant_end_to_end():
    assert {point.content_id for point in A1_POINTS} == {"sha:A1:H1"}


def test_a2_material_revisions_create_distinct_successors_without_rewriting_predecessors():
    assert [point.content_id for point in A2_POINTS] == ["sha:A2:H1", "sha:A2:H2", "sha:A2:H3"]
    assert A2_RELATIONS == (
        Relation("A2.2", "SUCCESSOR_OF", "A2.1"),
        Relation("A2.3", "SUCCESSOR_OF", "A2.2"),
    )
    assert "DEFECT_PRESENT" in A2_POINTS[0].findings
    assert "DEFECT_PRESENT" not in A2_POINTS[-1].findings


def test_a3_authority_changes_do_not_mutate_content_identity():
    assert {point.content_id for point in A3_POINTS} == {"sha:A3:H1"}
    assert [point.authority for point in A3_POINTS] == [
        "ACTIVE",
        "EXPIRED",
        "REESTABLISHED_NEW_BASIS",
    ]


def test_a4_claim_state_changes_do_not_mutate_artifact_identity():
    assert {point.content_id for point in A4_POINTS} == {"sha:A4:H1"}
    assert A4_POINTS[0].claims != A4_POINTS[1].claims


def test_a5_truncated_observation_is_not_completed_from_nearby_a1_content():
    assert "OBSERVATION_TRUNCATED" in A5_POINTS[-1].findings
    assert A5_POINTS[-1].content_id != A1_POINTS[-1].content_id
    assert "SOURCE_RECEIVED" not in A5_POINTS[-1].findings


def test_a6_exteriority_does_not_establish_independence_or_bound_source_origin():
    findings = set(A6_POINTS[0].findings)
    assert "EXTERIOR_RETURN_PRESERVED" in findings
    assert "SOURCE_ORIGIN_NOT_BOUND" in findings
    assert "INDEPENDENCE_ESTABLISHED" not in findings
    assert "ACTOR_IDENTITY_ESTABLISHED" not in findings


def test_a7_successor_pass_does_not_erase_predecessor_failure():
    assert "RECOMPUTATION_FAILED" in A7_POINTS[0].findings
    assert "RECOMPUTATION_PASS" in A7_POINTS[1].findings
    assert "PREDECESSOR_FAILURE_PRESERVED" in A7_POINTS[1].findings
    assert A7_RELATIONS == (Relation("A7.2", "SUCCESSOR_OF", "A7.1"),)


def test_a8_branch_siblings_keep_independent_findings():
    b1 = next(point for point in A8_POINTS if point.artifact_id == "A8.B1")
    b2 = next(point for point in A8_POINTS if point.artifact_id == "A8.B2")
    assert "RECOMPUTATION_PASS" in b1.findings
    assert "RECOMPUTATION_PASS" not in b2.findings
    assert "PROVENANCE_UNRESOLVED" in b2.findings
    assert "PROVENANCE_UNRESOLVED" not in b1.findings


def test_a9_merge_preserves_parent_specific_standing_instead_of_flattening_it():
    findings = set(A9_POINTS[0].findings)
    assert "PARENT_A8.B1_RECOMPUTATION_PASS" in findings
    assert "PARENT_A8.B2_PROVENANCE_UNRESOLVED" in findings
    assert "MERGE_STANDING_BOUNDED" in findings
    assert set(A9_RELATIONS) == {
        Relation("A9", "MERGES", "A8.B1"),
        Relation("A9", "MERGES", "A8.B2"),
    }


def test_a10_identity_mismatch_is_preserved_as_observation_not_malice_claim():
    assert A10_POINTS[0].content_id != A10_POINTS[1].content_id
    findings = set(A10_POINTS[1].findings)
    assert "BOUND_CONTENT_IDENTITY_MISMATCH" in findings
    assert "MALICIOUS_TAMPERING" not in findings


# Router-level longitudinal flow simulations.
def test_a1_clean_source_routes_end_to_end_without_promotion_language():
    path = _standard_path("A1", ("HASH_MATCHED", "SOURCE_PRESENT"))
    _assert_path(path, basis_prefix="A1")
    assert path[-1].disposition == RouteDisposition.OUTBOUND_ELIGIBLE


def test_a6_unresolved_exterior_return_requires_resolution_before_archive_outbound():
    path = (
        RoutingSnapshot("A6", "A6-R0", RoutePhase.INBOUND),
        RoutingSnapshot(
            "A6",
            "A6-R1",
            RoutePhase.EXAMINE,
            findings=("EXTERIOR_RETURN_PRESERVED", "SOURCE_ORIGIN_NOT_BOUND"),
            predecessor_state_id="A6-R0",
        ),
        RoutingSnapshot(
            "A6",
            "A6-R2",
            RoutePhase.DETERMINE,
            RouteDisposition.UNRESOLVED,
            findings=("EXTERIOR_RETURN_PRESERVED", "SOURCE_ORIGIN_NOT_BOUND"),
            predecessor_state_id="A6-R1",
        ),
        RoutingSnapshot(
            "A6",
            "A6-R3",
            RoutePhase.RESOLVE,
            RouteDisposition.UNRESOLVED,
            findings=("SOURCE_ORIGIN_NOT_BOUND",),
            predecessor_state_id="A6-R2",
        ),
        RoutingSnapshot(
            "A6",
            "A6-R4",
            RoutePhase.DETERMINE,
            RouteDisposition.ARCHIVE_ONLY,
            findings=("SOURCE_ORIGIN_NOT_BOUND", "UNRESOLVED_HISTORY_PRESERVED"),
            predecessor_state_id="A6-R3",
        ),
        RoutingSnapshot(
            "A6",
            "A6-R5",
            RoutePhase.OUTBOUND,
            RouteDisposition.ARCHIVE_ONLY,
            findings=("SOURCE_ORIGIN_NOT_BOUND", "UNRESOLVED_HISTORY_PRESERVED"),
            predecessor_state_id="A6-R4",
        ),
    )
    _assert_path(path, basis_prefix="A6")


def test_a7_failed_recomputation_requires_redetermination_before_successor_outbound():
    path = (
        RoutingSnapshot("A7.2", "A7-R0", RoutePhase.INBOUND),
        RoutingSnapshot(
            "A7.2",
            "A7-R1",
            RoutePhase.EXAMINE,
            findings=("PREDECESSOR_RECOMPUTATION_FAILED",),
            predecessor_state_id="A7-R0",
        ),
        RoutingSnapshot(
            "A7.2",
            "A7-R2",
            RoutePhase.DETERMINE,
            RouteDisposition.REMEDIATION_REQUIRED,
            findings=("PREDECESSOR_RECOMPUTATION_FAILED",),
            predecessor_state_id="A7-R1",
        ),
        RoutingSnapshot(
            "A7.2",
            "A7-R3",
            RoutePhase.RESOLVE,
            RouteDisposition.REMEDIATION_REQUIRED,
            findings=("RECOMPUTATION_EXECUTED",),
            predecessor_state_id="A7-R2",
        ),
        RoutingSnapshot(
            "A7.2",
            "A7-R4",
            RoutePhase.DETERMINE,
            RouteDisposition.OUTBOUND_ELIGIBLE,
            findings=("RECOMPUTATION_PASS", "PREDECESSOR_FAILURE_PRESERVED"),
            predecessor_state_id="A7-R3",
        ),
        RoutingSnapshot(
            "A7.2",
            "A7-R5",
            RoutePhase.OUTBOUND,
            RouteDisposition.OUTBOUND_ELIGIBLE,
            findings=("RECOMPUTATION_PASS", "PREDECESSOR_FAILURE_PRESERVED"),
            predecessor_state_id="A7-R4",
        ),
    )
    _assert_path(path, basis_prefix="A7")


def test_a10_identity_mismatch_cannot_skip_remediation_and_redetermination():
    determine = RoutingSnapshot(
        "A10",
        "A10-R2",
        RoutePhase.DETERMINE,
        RouteDisposition.REMEDIATION_REQUIRED,
        findings=("BOUND_CONTENT_IDENTITY_MISMATCH",),
    )
    attempted_outbound = RoutingSnapshot(
        "A10",
        "A10-R3",
        RoutePhase.OUTBOUND,
        RouteDisposition.OUTBOUND_ELIGIBLE,
        findings=("BOUND_CONTENT_IDENTITY_MISMATCH",),
        predecessor_state_id="A10-R2",
    )
    violations = validate_routing_transition(
        determine,
        attempted_outbound,
        _transition(determine, attempted_outbound, basis="identity mismatch still open"),
    )
    assert "ROUTE_NOT_PERMITTED" in {violation.code for violation in violations}

    valid_path = (
        determine,
        RoutingSnapshot(
            "A10",
            "A10-R3Q",
            RoutePhase.RESOLVE,
            RouteDisposition.REMEDIATION_REQUIRED,
            findings=("BOUND_CONTENT_IDENTITY_MISMATCH",),
            predecessor_state_id="A10-R2",
        ),
        RoutingSnapshot(
            "A10",
            "A10-R4",
            RoutePhase.DETERMINE,
            RouteDisposition.DISCARD_ONLY,
            findings=("IDENTITY_DISCONTINUITY_UNRESOLVED", "RECEIPT_PRESERVED"),
            predecessor_state_id="A10-R3Q",
        ),
        RoutingSnapshot(
            "A10",
            "A10-R5",
            RoutePhase.OUTBOUND,
            RouteDisposition.DISCARD_ONLY,
            findings=("IDENTITY_DISCONTINUITY_UNRESOLVED", "RECEIPT_PRESERVED"),
            predecessor_state_id="A10-R4",
        ),
    )
    _assert_path(valid_path, basis_prefix="A10")


# Explicit preservation of current seams rather than hidden repair.
def test_current_router_rejects_material_successor_as_silent_subject_substitution():
    current = RoutingSnapshot("A2.1", "A2-R2", RoutePhase.DETERMINE, RouteDisposition.REMEDIATION_REQUIRED)
    successor = RoutingSnapshot(
        "A2.2",
        "A2-R3",
        RoutePhase.RESOLVE,
        RouteDisposition.REMEDIATION_REQUIRED,
        predecessor_state_id="A2-R2",
    )
    violations = validate_routing_transition(
        current,
        successor,
        _transition(current, successor, basis="material repair produced new bytes"),
    )
    assert "SUBJECT_ID_CHANGED" in {violation.code for violation in violations}


def test_current_router_rejects_direct_unresolved_outbound():
    current = RoutingSnapshot("A6", "A6-R2", RoutePhase.DETERMINE, RouteDisposition.UNRESOLVED)
    successor = RoutingSnapshot(
        "A6",
        "A6-R3",
        RoutePhase.OUTBOUND,
        RouteDisposition.UNRESOLVED,
        predecessor_state_id="A6-R2",
    )
    violations = validate_routing_transition(
        current,
        successor,
        _transition(current, successor, basis="preserve unresolved external return"),
    )
    assert "ROUTE_NOT_PERMITTED" in {violation.code for violation in violations}


def test_every_artifact_path_is_longitudinally_reconstructable_from_preserved_coordinates():
    tracks = {
        "A1": A1_POINTS,
        "A2": A2_POINTS,
        "A3": A3_POINTS,
        "A4": A4_POINTS,
        "A5": A5_POINTS,
        "A6": A6_POINTS,
        "A7": A7_POINTS,
        "A8": A8_POINTS,
        "A9": A9_POINTS,
        "A10": A10_POINTS,
    }
    assert set(tracks) == set(ROOT_ARTIFACT_IDS)
    for root_id, points in tracks.items():
        assert points, root_id
        assert all(point.coordinate for point in points)
        assert all(point.content_id for point in points)
