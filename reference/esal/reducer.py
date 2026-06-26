# reference/esal/reducer.py

from .models import State, ViolationRecord, INITIAL_STATE
from .errors import StructuralError, GovernanceError


def apply_bdr(state: State, event: dict) -> State:
    """
    Apply a BDR_CREATED event.
    This is intentionally minimal and conservative:
    - authority: union with delegated_authority
    - constraints: union with constraints
    - obligations: union with obligations
    - lineage: append bdr_id
    """
    payload_authority = set(event.get("delegated_authority", []))
    payload_constraints = set(event.get("constraints", []))
    payload_obligations = set(event.get("obligations", []))

    # Very simple authority containment check:
    # if there is a parent_bdr_id, ensure delegated_authority does not exceed parent.
    # (For now we assume parent authority == current state's authority.)
    parent_bdr_id = event.get("parent_bdr_id")
    if parent_bdr_id is not None:
        # Any authority in payload_authority that is not already in state.authority
        # is treated as inflation.
        inflation = payload_authority.difference(state.authority)
        if inflation:
            raise GovernanceError(
                f"Delegated authority exceeds parent envelope: {sorted(inflation)}"
            )

    new_authority = state.authority.union(payload_authority)
    new_constraints = state.constraints.union(payload_constraints)
    new_obligations = state.obligations.union(payload_obligations)
    new_lineage = state.lineage + (event.get("bdr_id"),)

    return State(
        authority=new_authority,
        constraints=new_constraints,
        obligations=new_obligations,
        lineage=new_lineage,
        validity=state.validity,
        violations=state.violations,
    )


def apply_execution(state: State, event: dict) -> State:
    """
    Apply an EXECUTION event.
    Rules:
    - May ONLY change validity and violations.
    - authority / constraints / obligations / lineage must be preserved.
    - If any constraint status == 'fail', mark validity false and add violation.
    """
    # Extract constraint checks
    checks = event.get("constraint_checks", [])
    violations = list(state.violations)
    validity = state.validity

    for check in checks:
        constraint_name = check.get("constraint")
        status = check.get("status")
        if status == "fail":
            validity = False
            violations.append(
                ViolationRecord(
                    constraint_id=constraint_name or "",
                    event_id=event.get("event_id", ""),
                    boundary_id=event.get("boundary_id", ""),
                    severity="G",
                    timestamp=int(event.get("timestamp", 0)),
                )
            )

    # Return new state with updated validity/violations only
    return State(
        authority=state.authority,
        constraints=state.constraints,
        obligations=state.obligations,
        lineage=state.lineage,
        validity=validity,
        violations=tuple(violations),
    )


def transition(state: State, event: dict) -> State:
    etype = event.get("event_type")
    if etype == "BDR_CREATED":
        return apply_bdr(state, event)
    elif etype == "EXECUTION":
        return apply_execution(state, event)
    else:
        raise StructuralError(f"Unknown event type: {etype!r}")


def reduce_state(initial_state: State, canonical_events: list[dict]) -> State:
    """
    F(S0, E*): fold(transition, S0, E*).
    """
    state = initial_state
    for e in canonical_events:
        state = transition(state, e)
    return state