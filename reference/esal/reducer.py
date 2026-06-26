from .models import State, ViolationRecord
from .errors import StructuralError, GovernanceError


def apply_bdr(state: State, event: dict) -> State:
    """
    Apply a BDR_CREATED event.

    Semantics:
    - Read envelope fields from event["body"].
    - Enforce simple authority containment when parent_bdr_id is present.
    - Union authority/constraints/obligations into the state.
    - Append bdr_id to lineage.
    """
    body = event.get("body", {})

    delegated_authority = set(body.get("delegated_authority", []))
    constraints = set(body.get("constraints", []))
    obligations = set(body.get("obligations", []))

    parent_bdr_id = body.get("parent_bdr_id")
    bdr_id = body.get("bdr_id")

    # Authority containment check:
    # If there is a parent_bdr_id, delegated_authority must not exceed current state's authority.
    if parent_bdr_id is not None:
        inflation = delegated_authority.difference(state.authority)
        if inflation:
            raise GovernanceError(
                f"Delegated authority exceeds parent envelope: {sorted(inflation)}"
            )

    new_authority = state.authority.union(delegated_authority)
    new_constraints = state.constraints.union(constraints)
    new_obligations = state.obligations.union(obligations)
    new_lineage = state.lineage + (bdr_id,)

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

    Semantics:
    - Read constraint_checks from event["body"].
    - May ONLY change validity and violations.
    - For each check with status == "fail":
      - Mark validity False.
      - Append a violation record.
    """
    body = event.get("body", {})

    checks = body.get("constraint_checks", [])
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

    # EXECUTION is pure with respect to envelope: authority/constraints/obligations/lineage unchanged.
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
    F(S0, E*): fold(transition, S0, E*)
    """
    state = initial_state
    for e in canonical_events:
        state = transition(state, e)
    return state