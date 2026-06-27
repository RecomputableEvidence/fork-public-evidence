from dataclasses import asdict, dataclass
from typing import Any, FrozenSet, Tuple


@dataclass(frozen=True)
class ViolationRecord:
    constraint_id: str
    event_id: str
    boundary_id: str
    status: str
    timestamp: int
    detail: str = ""


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


def state_to_dict(state: State) -> dict[str, Any]:
    return {
        "authority": sorted(state.authority),
        "constraints": sorted(state.constraints),
        "obligations": sorted(state.obligations),
        "lineage": list(state.lineage),
        "validity": state.validity,
        "violations": [
            asdict(v)
            for v in sorted(
                state.violations,
                key=lambda v: (
                    v.timestamp,
                    v.event_id,
                    v.boundary_id,
                    v.constraint_id,
                    v.status,
                    v.detail,
                ),
            )
        ],
    }