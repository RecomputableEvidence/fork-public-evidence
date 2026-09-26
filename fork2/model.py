"""Immutable record types for the Fork 2 semantic kernel v0.1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class AttemptResult(str, Enum):
    QUALIFIED = "QUALIFIED"
    FAILED = "FAILED"
    UNRESOLVED = "UNRESOLVED"


class StandingEffect(str, Enum):
    NONE = "NONE"
    EXPAND = "EXPAND"


@dataclass(frozen=True)
class TransitionRecord:
    transition_id: str
    parent_state_id: str
    candidate_state_id: str
    bound_rule_id: str
    preserved_result: AttemptResult
    preserved_disposition: AttemptResult
    standing_effect: StandingEffect = StandingEffect.NONE


@dataclass(frozen=True)
class TransitionProjection:
    """A later representation of one historical transition.

    Fork 2 v0.1 does not claim that the bound rule itself is correct or sufficient.
    It only checks that a later projection does not rewrite the already-preserved
    result/disposition of the historical transition.
    """

    transition_id: str
    projected_result: AttemptResult
    projected_disposition: AttemptResult


@dataclass(frozen=True)
class SelectionRecord:
    selection_id: str
    selected_state_id: str
    standing_effect: StandingEffect = StandingEffect.NONE


@dataclass(frozen=True)
class AttemptRecord:
    attempt_id: str
    candidate_state_id: str
    result: AttemptResult
    addressable: bool = True


@dataclass(frozen=True)
class RoutingState:
    default_qualified_state_ids: Tuple[str, ...]
