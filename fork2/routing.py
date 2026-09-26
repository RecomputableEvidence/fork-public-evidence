"""Minimal temporal routing prototype for Fork 2.

This module does not define artifact truth, authority, qualification, or a
universal evidence taxonomy. It only models a small temporal route and the
conditions under which a routing snapshot may advance to the next phase.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class RoutePhase(str, Enum):
    INBOUND = "INBOUND"
    EXAMINE = "EXAMINE"
    DETERMINE = "DETERMINE"
    RESOLVE = "RESOLVE"
    OUTBOUND = "OUTBOUND"


class RouteDisposition(str, Enum):
    UNDETERMINED = "UNDETERMINED"
    OUTBOUND_ELIGIBLE = "OUTBOUND_ELIGIBLE"
    REMEDIATION_REQUIRED = "REMEDIATION_REQUIRED"
    UNRESOLVED = "UNRESOLVED"
    ARCHIVE_ONLY = "ARCHIVE_ONLY"
    DISCARD_ONLY = "DISCARD_ONLY"


@dataclass(frozen=True)
class RoutingSnapshot:
    """One immutable temporal view of a routed subject.

    ``findings`` intentionally uses open strings. The prototype tests the
    five-phase routing shape without freezing a global finding vocabulary.
    """

    subject_id: str
    state_id: str
    phase: RoutePhase
    disposition: RouteDisposition = RouteDisposition.UNDETERMINED
    findings: Tuple[str, ...] = ()
    predecessor_state_id: str | None = None


@dataclass(frozen=True)
class RoutingTransition:
    """A declared transition between two routing snapshots."""

    transition_id: str
    subject_id: str
    from_state_id: str
    to_state_id: str
    from_phase: RoutePhase
    to_phase: RoutePhase
    basis: str
    operations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RoutingViolation:
    code: str
    subject_id: str
    detail: str


_RESOLUTION_DISPOSITIONS = {
    RouteDisposition.REMEDIATION_REQUIRED,
    RouteDisposition.UNRESOLVED,
}

_OUTBOUND_DISPOSITIONS = {
    RouteDisposition.OUTBOUND_ELIGIBLE,
    RouteDisposition.ARCHIVE_ONLY,
    RouteDisposition.DISCARD_ONLY,
}


def allowed_next_phases(snapshot: RoutingSnapshot) -> Tuple[RoutePhase, ...]:
    """Return the phases this snapshot may advance to.

    The routing spine is intentionally small:

    INBOUND -> EXAMINE -> DETERMINE -> [RESOLVE -> DETERMINE]* -> OUTBOUND

    DETERMINE routes to RESOLVE or OUTBOUND according to current disposition.
    """

    if snapshot.phase == RoutePhase.INBOUND:
        return (RoutePhase.EXAMINE,)
    if snapshot.phase == RoutePhase.EXAMINE:
        return (RoutePhase.DETERMINE,)
    if snapshot.phase == RoutePhase.DETERMINE:
        if snapshot.disposition in _RESOLUTION_DISPOSITIONS:
            return (RoutePhase.RESOLVE,)
        if snapshot.disposition in _OUTBOUND_DISPOSITIONS:
            return (RoutePhase.OUTBOUND,)
        return ()
    if snapshot.phase == RoutePhase.RESOLVE:
        return (RoutePhase.DETERMINE,)
    return ()


def validate_routing_transition(
    current: RoutingSnapshot,
    successor: RoutingSnapshot,
    transition: RoutingTransition,
) -> Tuple[RoutingViolation, ...]:
    """Validate one temporal routing transition without conferring standing."""

    violations: list[RoutingViolation] = []

    if current.subject_id != successor.subject_id:
        violations.append(
            RoutingViolation(
                "SUBJECT_ID_CHANGED",
                current.subject_id,
                "Routing may not silently substitute a different subject.",
            )
        )

    if transition.subject_id != current.subject_id:
        violations.append(
            RoutingViolation(
                "TRANSITION_SUBJECT_MISMATCH",
                current.subject_id,
                "Transition subject does not match the routed subject.",
            )
        )

    if transition.from_state_id != current.state_id:
        violations.append(
            RoutingViolation(
                "FROM_STATE_MISMATCH",
                current.subject_id,
                "Transition does not bind the current routing snapshot.",
            )
        )

    if transition.to_state_id != successor.state_id:
        violations.append(
            RoutingViolation(
                "TO_STATE_MISMATCH",
                current.subject_id,
                "Transition does not bind the successor routing snapshot.",
            )
        )

    if transition.from_phase != current.phase or transition.to_phase != successor.phase:
        violations.append(
            RoutingViolation(
                "PHASE_BINDING_MISMATCH",
                current.subject_id,
                "Transition phase binding disagrees with one or both snapshots.",
            )
        )

    if current.state_id == successor.state_id:
        violations.append(
            RoutingViolation(
                "STATE_ID_REUSED",
                current.subject_id,
                "A temporal routing transition must produce a distinct routing state.",
            )
        )

    if successor.predecessor_state_id != current.state_id:
        violations.append(
            RoutingViolation(
                "PREDECESSOR_BINDING_MISMATCH",
                current.subject_id,
                "Successor snapshot must point to the state it follows.",
            )
        )

    if successor.phase not in allowed_next_phases(current):
        violations.append(
            RoutingViolation(
                "ROUTE_NOT_PERMITTED",
                current.subject_id,
                f"{current.phase.value} with disposition {current.disposition.value} may not route to {successor.phase.value}.",
            )
        )

    if current.phase in {RoutePhase.INBOUND, RoutePhase.EXAMINE}:
        if current.disposition != RouteDisposition.UNDETERMINED:
            violations.append(
                RoutingViolation(
                    "PREMATURE_DISPOSITION",
                    current.subject_id,
                    "Inbound and examination snapshots may not carry a final routing disposition.",
                )
            )

    if successor.phase == RoutePhase.EXAMINE:
        if successor.disposition != RouteDisposition.UNDETERMINED:
            violations.append(
                RoutingViolation(
                    "EXAMINE_DISPOSITION_NOT_UNDETERMINED",
                    current.subject_id,
                    "Examination remains disposition-neutral until determination.",
                )
            )

    if successor.phase == RoutePhase.DETERMINE:
        if successor.disposition == RouteDisposition.UNDETERMINED:
            violations.append(
                RoutingViolation(
                    "DETERMINATION_MISSING_DISPOSITION",
                    current.subject_id,
                    "A determination snapshot must state a disposition.",
                )
            )

    if successor.phase == RoutePhase.RESOLVE:
        if successor.disposition not in _RESOLUTION_DISPOSITIONS:
            violations.append(
                RoutingViolation(
                    "RESOLUTION_WITHOUT_RESOLUTION_DISPOSITION",
                    current.subject_id,
                    "Resolution is entered only for remediation-required or unresolved subjects.",
                )
            )

    if successor.phase == RoutePhase.OUTBOUND:
        if successor.disposition not in _OUTBOUND_DISPOSITIONS:
            violations.append(
                RoutingViolation(
                    "OUTBOUND_WITH_NONTERMINAL_DISPOSITION",
                    current.subject_id,
                    "Outbound requires OUTBOUND_ELIGIBLE, ARCHIVE_ONLY, or DISCARD_ONLY disposition.",
                )
            )

    if not transition.basis.strip():
        violations.append(
            RoutingViolation(
                "TRANSITION_BASIS_MISSING",
                current.subject_id,
                "Every routing transition requires an explicit basis.",
            )
        )

    return tuple(violations)
