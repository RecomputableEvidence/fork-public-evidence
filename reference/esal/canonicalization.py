import hashlib
import json
from typing import Any

from .errors import DeterminismError, StructuralError


EVENT_TYPE_ALIASES = {
    "BDR": "BDR_CREATED",
    "BDR_CREATED": "BDR_CREATED",
    "EXECUTION": "EXECUTION",
}

ENVELOPE_KEYS = {
    "event_id",
    "id",
    "event_type",
    "type",
    "timestamp",
    "boundary_id",
    "boundary",
    "payload",
    "body",
}


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def _event_type(raw_type: Any) -> str:
    if raw_type is None:
        raise StructuralError(
            "missing event_type",
            error_code="MISSING_EVENT_TYPE",
        )

    normalized = EVENT_TYPE_ALIASES.get(str(raw_type))

    if normalized is None:
        raise StructuralError(
            f"unknown event_type: {raw_type}",
            error_code="UNKNOWN_EVENT_TYPE",
        )

    return normalized


def _event_body(event: dict) -> dict:
    if "body" in event:
        body = event["body"]
        if not isinstance(body, dict):
            raise StructuralError(
                "event body must be an object",
                error_code="INVALID_BODY",
                offending_event_id=str(event.get("event_id", "")),
            )
        return dict(body)

    if "payload" in event:
        payload = event["payload"]
        if not isinstance(payload, dict):
            raise StructuralError(
                "event payload must be an object",
                error_code="INVALID_PAYLOAD",
                offending_event_id=str(event.get("event_id", "")),
            )
        return dict(payload)

    return {
        key: value
        for key, value in event.items()
        if key not in ENVELOPE_KEYS
    }


def _first_string(*values: Any) -> str | None:
    for value in values:
        if value not in (None, ""):
            return str(value)

    return None


def _infer_boundary_id(event: dict, body: dict, normalized_event_type: str, event_id: str) -> str:
    explicit = _first_string(
        event.get("boundary_id"),
        event.get("boundary"),
        body.get("boundary_id"),
        body.get("boundary"),
        body.get("boundary_ref"),
        body.get("boundary_reference"),
    )

    if explicit is not None:
        return explicit

    boundary_pairs = [
        ("source_boundary", "target_boundary"),
        ("from_boundary", "to_boundary"),
        ("source_context", "target_context"),
        ("from_context", "to_context"),
        ("source_system", "target_system"),
        ("from_system", "to_system"),
        ("source", "target"),
        ("from", "to"),
    ]

    for left_key, right_key in boundary_pairs:
        left = _first_string(body.get(left_key), event.get(left_key))
        right = _first_string(body.get(right_key), event.get(right_key))

        if left is not None and right is not None:
            return f"{left}->{right}"

    bdr_id = _first_string(body.get("bdr_id"), body.get("governed_by_bdr_id"))

    if bdr_id is not None:
        return f"bdr:{bdr_id}"

    if normalized_event_type == "BDR_CREATED":
        return f"bdr-event:{event_id}"

    if normalized_event_type == "EXECUTION":
        return f"execution-event:{event_id}"

    raise StructuralError(
        "missing boundary_id",
        error_code="MISSING_BOUNDARY_ID",
        offending_event_id=event_id,
    )


def normalize_event(event: dict) -> dict:
    if not isinstance(event, dict):
        raise StructuralError(
            "event must be a JSON object",
            error_code="EVENT_NOT_OBJECT",
        )

    raw_event_id = event.get("event_id", event.get("id"))
    if raw_event_id in (None, ""):
        raise StructuralError(
            "missing event_id",
            error_code="MISSING_EVENT_ID",
        )

    event_id = str(raw_event_id)

    raw_timestamp = event.get("timestamp")
    if raw_timestamp is None:
        raise StructuralError(
            "missing timestamp",
            error_code="MISSING_TIMESTAMP",
            offending_event_id=event_id,
        )

    try:
        timestamp = int(raw_timestamp)
    except Exception as exc:
        raise StructuralError(
            f"invalid timestamp: {raw_timestamp}",
            error_code="INVALID_TIMESTAMP",
            offending_event_id=event_id,
        ) from exc

    event_type = _event_type(event.get("event_type", event.get("type")))
    body = _event_body(event)
    boundary_id = _infer_boundary_id(event, body, event_type, event_id)

    return {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp": timestamp,
        "boundary_id": boundary_id,
        "body": body,
    }


def payload_digest(payload: dict) -> str:
    return hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest()


def event_digest(event: dict) -> str:
    return hashlib.sha256(
        canonical_json(event).encode("utf-8")
    ).hexdigest()


def canonical_key(event: dict):
    event_priority = {
        "BDR_CREATED": 0,
        "EXECUTION": 1,
    }

    return (
        event["timestamp"],
        event_priority.get(event["event_type"], 99),
        event["event_id"],
        event["boundary_id"],
        payload_digest(event["body"]),
    )


def canonicalize(events: list[dict]) -> list[dict]:
    normalized = [
        normalize_event(event)
        for event in events
    ]

    seen: dict[str, dict] = {}

    for event in normalized:
        event_id = event["event_id"]

        if event_id in seen and seen[event_id] != event:
            raise DeterminismError(
                "event_id conflict with differing event content",
                error_code="EVENT_ID_CONFLICT",
                offending_event_id=event_id,
            )

        seen[event_id] = event

    return sorted(normalized, key=canonical_key)