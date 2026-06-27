from .canonicalization import normalize_event
from .errors import StructuralError


def validate_event_shape(events: list[dict]) -> None:
    for event in events:
        normalize_event(event)


def _bdr_id(event: dict) -> str:
    return str(event["body"].get("bdr_id", event["event_id"]))


def _parent_id(event: dict) -> str | None:
    body = event["body"]
    parent = body.get("parent_bdr_id", body.get("parent_event_id"))

    if parent in (None, ""):
        return None

    return str(parent)


def validate_lineage(canonical_events: list[dict]) -> None:
    seen_bdr_ids: set[str] = set()
    seen_event_ids: set[str] = set()

    for event in canonical_events:
        event_id = event["event_id"]
        seen_event_ids.add(event_id)

        if event["event_type"] != "BDR_CREATED":
            body = event["body"]
            governed_by = body.get("governed_by_bdr_id", body.get("bdr_id"))

            if governed_by not in (None, ""):
                governed_by = str(governed_by)

                if governed_by not in seen_bdr_ids and governed_by not in seen_event_ids:
                    raise StructuralError(
                        f"execution references unknown governing BDR: {governed_by}",
                        error_code="UNKNOWN_GOVERNING_BDR",
                        offending_event_id=event_id,
                    )

            continue

        bdr_id = _bdr_id(event)
        parent = _parent_id(event)

        if bdr_id in seen_bdr_ids:
            raise StructuralError(
                f"duplicate bdr_id: {bdr_id}",
                error_code="DUPLICATE_BDR_ID",
                offending_event_id=event_id,
            )

        if parent is not None:
            if parent == bdr_id or parent == event_id:
                raise StructuralError(
                    "BDR cannot reference itself as parent",
                    error_code="SELF_PARENT_BDR",
                    offending_event_id=event_id,
                )

            if parent not in seen_bdr_ids and parent not in seen_event_ids:
                raise StructuralError(
                    f"unknown parent_bdr_id: {parent}",
                    error_code="UNKNOWN_PARENT_BDR",
                    offending_event_id=event_id,
                )

        seen_bdr_ids.add(bdr_id)


def validate_events(events: list[dict]) -> None:
    """
    Backward-compatible validator.

    For permutation-safe replay, runner.py intentionally performs:

        validate_event_shape(raw_events)
        canonicalize(raw_events)
        validate_lineage(canonical_events)

    This function is retained for direct callers.
    """

    validate_event_shape(events)