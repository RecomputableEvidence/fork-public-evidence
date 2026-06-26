# reference/esal/canonicalization.py

import json
import hashlib
from typing import Any

from .errors import DeterminismError


def normalize_event(e: dict) -> dict:
    """
    Normalize an ESAL event into a canonical structure.

    For now we assume the events are already in the 'flattened' schema used
    in esal-tests, so we:
      - ensure required keys exist
      - coerce timestamp to int
      - leave the rest of the fields as-is
    """
    if "event_type" not in e or "event_id" not in e or "timestamp" not in e:
        raise DeterminismError("Event missing core fields for canonicalization")

    return {
        "event_id": e["event_id"],
        "event_type": e["event_type"],
        "timestamp": int(e["timestamp"]),
        "boundary_id": e.get("boundary_id", ""),
        # everything else stays in 'body'
        "body": {
            k: v
            for k, v in e.items()
            if k not in ("event_id", "event_type", "timestamp", "boundary_id")
        },
    }


def body_digest(body: dict[str, Any]) -> str:
    """
    Deterministic hash of the event 'body' (all fields except the core ones).
    """
    s = json.dumps(
        body,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_key(e: dict) -> tuple:
    """
    Canonical ordering key:

        (timestamp,
         type_priority,
         event_id,
         boundary_id,
         body_hash)
    """
    etype = e["event_type"]
    type_priority = 0 if etype == "BDR_CREATED" else 1

    return (
        e["timestamp"],
        type_priority,
        e["event_id"],
        e["boundary_id"],
        body_digest(e["body"]),
    )


def canonicalize(events: list[dict]) -> list[dict]:
    """
    C(E): normalize and deterministically sort events.
    Also detects conflicting duplicate event_ids (D-class).
    """
    normalized = [normalize_event(e) for e in events]

    seen_by_id: dict[str, dict] = {}
    for e in normalized:
        eid = e["event_id"]
        if eid in seen_by_id and seen_by_id[eid] != e:
            raise DeterminismError(
                f"Conflicting events with same event_id: {eid}"
            )
        seen_by_id[eid] = e

    return sorted(normalized, key=canonical_key)