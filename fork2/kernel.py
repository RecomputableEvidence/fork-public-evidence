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
    """Enforce R5 without evaluating rule correctness or rule-bound results.

    The projection carries an asserted later-rule context so the historical
    transition's bound rule is not mechanically inert. This check does not
    establish temporal ordering between rules and does not implement R4.
    """

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

    if projection.later_rule_id == transition.bound_rule_id:
        violations.append(
            Violation(
                relation_id="R5",
                code="LATER_RULE_CONTEXT_NOT_DISTINCT",
                subject_id=transition.transition_id,
                detail="An R5 later-rule projection must identify a rule context distinct from the historical transition's bound rule.",
            )
        )

    if projection.projected_result != transition.preserved_result:
        violations.append(
            Violation(
                relation_id="R5",
                code="HISTORICAL_RESULT_REWRITE",
                subject_id=transition.transition_id,
                detail="A later-rule projection may not rewrite the preserved historical result.",
            )
        )

    if projection.projected_disposition != transition.preserved_disposition:
        violations.append(
            Violation(
                relation_id="R5",
                code="HISTORICAL_DISPOSITION_REWRITE",
                subject_id=transition.transition_id,
                detail="A later-rule projection may not rewrite the preserved historical disposition.",
            )
        )

    return violations


def check_attempt_routing(
    attempt: AttemptRecord,
    routing: RoutingState,
) -> List[Violation]:
    """Enforce the two conjuncts of R7a/R7b only.

    Qualification semantics themselves remain outside this first kernel.
    FAILED and UNRESOLVED attempts must remain addressable and must not appear
    in the default qualified-state route.
    """

    violations: List[Violation] = []

    if attempt.result == AttemptResult.FAILED:
        if not attempt.addressable:
            violations.append(
                Violation(
                    relation_id="R7a",
                    code="FAILED_ATTEMPT_NOT_ADDRESSABLE",
                    subject_id=attempt.attempt_id,
                    detail="A preserved failed attempt must remain addressable.",
                )
            )
        if attempt.candidate_state_id in routing.default_qualified_state_ids:
            violations.append(
                Violation(
                    relation_id="R7a",
                    code="FAILED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
                    subject_id=attempt.attempt_id,
                    detail="A preserved failed attempt may not enter the default qualified-state route.",
                )
            )
        return violations

    if attempt.result == AttemptResult.UNRESOLVED:
        if not attempt.addressable:
            violations.append(
                Violation(
                    relation_id="R7b",
                    code="UNRESOLVED_ATTEMPT_NOT_ADDRESSABLE",
                    subject_id=attempt.attempt_id,
                    detail="A preserved unresolved attempt must remain addressable.",
                )
            )
        if attempt.candidate_state_id in routing.default_qualified_state_ids:
            violations.append(
                Violation(
                    relation_id="R7b",
                    code="UNRESOLVED_ATTEMPT_IN_DEFAULT_QUALIFIED_ROUTE",
                    subject_id=attempt.attempt_id,
                    detail="A preserved unresolved attempt may not enter the default qualified-state route.",
                )
            )
        return violations

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
