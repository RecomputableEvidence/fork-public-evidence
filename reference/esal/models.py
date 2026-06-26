from dataclasses import dataclass
from typing import FrozenSet, Tuple


@dataclass(frozen=True)
class ViolationRecord:
    constraint_id: str
    event_id: str
    boundary_id: str
    severity: str
    timestamp: int


@dataclass(frozen=True)
class State:
    authority: FrozenSet[str]
    constraints: FrozenSet[str]
    obligations: FrozenSet[str]
    lineage: Tuple[str, ...]
    validity: bool
    violations: Tuple[ViolationRecord, ...]


INITIAL_STATE = State(
    authority=frozenset(),
    constraints=frozenset(),
    obligations=frozenset(),
    lineage=tuple(),
    validity=True,
    violations=tuple(),
)
