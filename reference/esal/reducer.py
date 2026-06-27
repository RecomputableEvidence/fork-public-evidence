import json
from typing import Any

from .errors import GovernanceError, StructuralError
from .models import State, ViolationRecord


FAIL_STATUSES = {
    "fail",
    "failed",
    "false",
    "violation",
    "violated",
    "deny",
    "denied",
    "noncompliant",
    "non_compliant",
}

DEFERRED_STATUSES = {
    "deferred",
    "unknown",
    "unresolved",
}


def _stable_token(value: Any) -> str:
    if isinstance(value, str):
        return value

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _token_set(value: Any) -> set[str]:
    if value in (None, ""):
        return set()

    if isinstance(value, dict):
        tokens: set[str] = set()

        for key, item in value.items():
            if item is True:
                tokens.add(str(key))
            else:
                tokens.add(_stable_token({key: item}))

        return tokens

    if isinstance(value, (list, tuple, set)):
        return {
            _stable_token(item)
            for item in value
        }

    return {_stable_token(value)}


def _parent_id(body: dict) -> str | None:
    parent = body.get("parent_bdr_id", body.get("parent_event_id"))

    if parent in (None, ""):
        return None

    return str(parent)


def _explicit_authority_expansion(body: dict) -> bool:
    if body.get("expanded_authority") is True:
        return True

    delta_type = str(body.get("authority_delta_type", "")).lower()

    return delta_type in {
        "expand",
        "expanded",
        "expanded_authority",
        "authority_expansion",
    }


def apply_bdr(state: State, event: dict) -> State:
    body = event["body"]

    bdr_id = str(body.get("bdr_id", event["event_id"]))
    parent_id = _parent_id(body)

    delegated_authority = _token_set(body.get("delegated_authority", body.get("authority")))
    constraints = _token_set(body.get("constraints"))
    obligations = _token_set(body.get("obligations"))

    if parent_id is not None:
        inflated = delegated_authority.difference(state.authority)

        if inflated and not _explicit_authority_expansion(body):
            raise GovernanceError(
                "authority inflation without explicit expansion delta: "
                + ", ".join(sorted(inflated)),
                error_code="AUTHORITY_INFLATION",
                offending_event_id=event["event_id"],
            )

    return State(
        authority=frozenset(set(state.authority).union(delegated_authority)),
        constraints=frozenset(set(state.constraints).union(constraints)),
        obligations=frozenset(set(state.obligations).union(obligations)),
        lineage=tuple(list(state.lineage) + [bdr_id]),
        validity=state.validity,
        violations=state.violations,
    )


def _check_status(check: Any) -> tuple[str, str, str]:
    if isinstance(check, dict):
        constraint_id = str(
            check.get(
                "constraint",
                check.get(
                    "constraint_id",
                    check.get("name", "unknown_constraint"),
                ),
            )
        )

        status = str(
            check.get(
                "status",
                check.get(
                    "evaluation_result",
                    check.get("result", "pass"),
                ),
            )
        ).lower()

        detail = str(check.get("detail", check.get("message", "")))

        return constraint_id, status, detail

    return _stable_token(check), "pass", ""


def apply_execution(state: State, event: dict) -> State:
    body = event["body"]

    action = body.get("action")

    if action not in (None, ""):
        action = str(action)

        if state.authority and action not in state.authority:
            raise GovernanceError(
                f"execution action outside authority envelope: {action}",
                error_code="ACTION_OUTSIDE_AUTHORITY",
                offending_event_id=event["event_id"],
            )

    raw_checks = body.get("constraint_checks", [])

    if isinstance(raw_checks, dict):
        checks = [raw_checks]
    elif isinstance(raw_checks, list):
        checks = raw_checks
    else:
        raise StructuralError(
            "constraint_checks must be a list or object",
            error_code="INVALID_CONSTRAINT_CHECKS",
            offending_event_id=event["event_id"],
        )

    violations = list(state.violations)
    validity = state.validity

    for check in checks:
        constraint_id, status, detail = _check_status(check)

        if status in DEFERRED_STATUSES:
            raise StructuralError(
                f"deferred constraint without encoded policy treatment: {constraint_id}",
                error_code="DEFERRED_CONSTRAINT_WITHOUT_POLICY",
                offending_event_id=event["event_id"],
            )

        if status in FAIL_STATUSES:
            validity = False

            violations.append(
                ViolationRecord(
                    constraint_id=constraint_id,
                    event_id=event["event_id"],
                    boundary_id=event["boundary_id"],
                    status=status,
                    timestamp=int(event["timestamp"]),
                    detail=detail,
                )
            )

    return State(
        authority=state.authority,
        constraints=state.constraints,
        obligations=state.obligations,
        lineage=state.lineage,
        validity=validity,
        violations=tuple(violations),
    )


def transition(state: State, event: dict) -> State:
    event_type = event["event_type"]

    if event_type == "BDR_CREATED":
        return apply_bdr(state, event)

    if event_type == "EXECUTION":
        return apply_execution(state, event)

    raise StructuralError(
        f"unknown event_type: {event_type}",
        error_code="UNKNOWN_EVENT_TYPE",
        offending_event_id=event.get("event_id"),
    )


def reduce_state(initial_state: State, canonical_events: list[dict]) -> State:
    state = initial_state

    for event in canonical_events:
        state = transition(state, event)

    return state