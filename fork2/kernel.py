"""Executable semantic checks for the Fork 2 kernel v0.1.

Only the four relations already frozen by the Fork 2 decision/authorization
sequence are enforced here: R3, R5, R7a, and R7b.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from fork2.model import (
    AttemptRecord,
    AttemptResult,
    RoutingState,
    SelectionRecord,
    StandingEffect,
    TransitionProjection,
    TransitionRecord,
)


@dataclass(frozen=True)
class Violation:
    relation_id: str
    code: str
    subject_id: str
    detail: str


def check_r3_selection_no_standing_expansion(
    selection: SelectionRecord,
) -> List[Violation]:
    if selection.standing_effect == StandingEffect.NONE:
        return []
    return [
        Violation(
            relation_id="R3",
            code="SELECTION_STANDING_EXPANSION",
            subject_id=selection.selection_id,
            detail="Selecting a state may not by itself expand epistemic standing.",
        )
    ]


def check_r5_no_retroactive_reinterpretation(
    transition: TransitionRecord,
    projection: TransitionProjection,
) -> List[Violation]:
    violations: List[Violation] = []

    if projection.transition_id != transition.transition_id:
        violations.append(
            Violation(
                relation_id="R5",
                code="TRANSITION_ID_MISMATCH",
                subject_id=projection.transition_id,
                detail="Projection is not bound to the historical transition it claims to represent.",
            )
        )
        return violations

    if projection.projected_result != transition.preserved_result:
        violations.append(
            Violation(
                relation_id="R5",
                code="HISTORICAL_RESULT_REWRITE",
                subject_id=transition.transition_id,
                detail="A later projection may not rewrite the preserved historical result.",
            )
        )

    if projection.projected_disposition != transition.preserved_disposition:
        violations.append(
            Violation(
                relation_id="R5",
                code="HISTORICAL_DISPOSITION_REWRITE",
                subject_id=transition.transition_id,
                detail="A later projection may not rewrite the preserved historical disposition.",
            )
        )

    return violations


def check_attempt_routing(
    attempt: AttemptRecord,
    routing: RoutingState,
) -> List[Violation]:
    """Enforce R7a/R7b only.

    Qualification semantics themselves remain outside this first kernel. The
    check is intentionally narrower: a candidate already recorded as FAILED or
    UNRESOLVED must not appear in the default qualified-state route.
    """

    if attempt.candidate_state_id not in routing.default_qualified_state_ids:
        return []

    if attempt.result == AttemptResult.FAILED:
        return [
            Violation(
                relation_id="R7a",
                code="FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
                subject_id=attempt.attempt_id,
                detail="A preserved failed attempt may remain addressable but may not enter the default qualified-state route.",
            )
        ]

    if attempt.result == AttemptResult.UNRESOLVED:
        return [
            Violation(
                relation_id="R7b",
                code="UNRESOLVED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
                subject_id=attempt.attempt_id,
                detail="A preserved unresolved attempt may remain addressable but may not enter the default qualified-state route.",
            )
        ]

    return []


def validate_kernel(
    *,
    selections: Iterable[SelectionRecord] = (),
    historical_projections: Iterable[tuple[TransitionRecord, TransitionProjection]] = (),
    attempts: Iterable[AttemptRecord] = (),
    routing: RoutingState,
) -> List[Violation]:
    violations: List[Violation] = []

    for selection in selections:
        violations.extend(check_r3_selection_no_standing_expansion(selection))

    for transition, projection in historical_projections:
        violations.extend(check_r5_no_retroactive_reinterpretation(transition, projection))

    for attempt in attempts:
        violations.extend(check_attempt_routing(attempt, routing))

    return violations
