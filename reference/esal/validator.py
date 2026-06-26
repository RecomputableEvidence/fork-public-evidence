# reference/esal/validator.py

from .errors import StructuralError


REQUIRED_COMMON_FIELDS = ["event_type", "event_id", "timestamp"]
BDR_REQUIRED_FIELDS = [
    "bdr_id",
    "boundary_id",
    "delegated_authority",
    "authority_delta_type",
    "constraints",
    "obligations",
]
EXEC_REQUIRED_FIELDS = [
    "bdr_id",
    "action",
    "result",
    "constraint_checks",
]


def _validate_common(event: dict, index: int) -> None:
    for field in REQUIRED_COMMON_FIELDS:
        if field not in event:
            raise StructuralError(f"Event[{index}] missing required field: {field}")
    # Basic type checks
    if not isinstance(event["event_type"], str):
        raise StructuralError(f"Event[{index}] event_type must be string")
    if not isinstance(event["event_id"], str):
        raise StructuralError(f"Event[{index}] event_id must be string")
    try:
        int(event["timestamp"])
    except Exception:
        raise StructuralError(f"Event[{index}] timestamp must be an integer epoch")


def _validate_bdr(event: dict, index: int) -> None:
    for field in BDR_REQUIRED_FIELDS:
        if field not in event:
            raise StructuralError(
                f"Event[{index}] BDR_CREATED missing required field: {field}"
            )
    if not isinstance(event["delegated_authority"], list):
        raise StructuralError(
            f"Event[{index}] delegated_authority must be a list"
        )
    if not isinstance(event["constraints"], list):
        raise StructuralError(f"Event[{index}] constraints must be a list")
    if not isinstance(event["obligations"], list):
        raise StructuralError(f"Event[{index}] obligations must be a list")


def _validate_execution(event: dict, index: int) -> None:
    for field in EXEC_REQUIRED_FIELDS:
        if field not in event:
            raise StructuralError(
                f"Event[{index}] EXECUTION missing required field: {field}"
            )
    if not isinstance(event["constraint_checks"], list):
        raise StructuralError(
            f"Event[{index}] constraint_checks must be a list"
        )


def _validate_lineage(events: list[dict]) -> None:
    """
    Minimal lineage check:
    - parent_event_id, if present and not null, must refer to an earlier event_id.
    """
    seen_ids: set[str] = set()
    for idx, e in enumerate(events):
        eid = e.get("event_id")
        if eid is not None:
            seen_ids.add(eid)

        parent_eid = e.get("parent_event_id")
        if parent_eid not in (None, "", "null"):
            if parent_eid not in seen_ids:
                raise StructuralError(
                    f"Event[{idx}] references unknown parent_event_id: {parent_eid}"
                )


def validate_events(events: list[dict]) -> None:
    """
    Schema + minimal lineage validation for ESAL events.
    Raises StructuralError on any problem.
    """
    if not isinstance(events, list):
        raise StructuralError("Events must be a list")

    for idx, e in enumerate(events):
        if not isinstance(e, dict):
            raise StructuralError(f"Event[{idx}] must be an object")

        _validate_common(e, idx)

        etype = e["event_type"]
        if etype == "BDR_CREATED":
            _validate_bdr(e, idx)
        elif etype == "EXECUTION":
            _validate_execution(e, idx)
        else:
            raise StructuralError(f"Event[{idx}] unknown event_type: {etype!r}")

    _validate_lineage(events)