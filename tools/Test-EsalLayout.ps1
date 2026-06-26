$ErrorActionPreference = "Stop"

$root = Get-Location

$canonicalizationPath = Join-Path $root "reference\esal\canonicalization.py"
$runnerPath = Join-Path $root "reference\esal\runner.py"

if (!(Test-Path (Split-Path $canonicalizationPath))) {
    throw "reference\esal directory not found."
}

Write-Host "Patching ESAL canonicalization.py..."

@'
import hashlib
import json

from .errors import DeterminismError


def normalize_event(event: dict) -> dict:
    return {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "timestamp": int(event["timestamp"]),
        "boundary_id": event["boundary_id"],
        "payload": event["payload"],
    }


def payload_digest(payload: dict) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(
        encoded.encode("utf-8")
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
        payload_digest(event["payload"]),
    )


def canonicalize(events: list[dict]) -> list[dict]:
    normalized = [
        normalize_event(event)
        for event in events
    ]

    seen = {}

    for event in normalized:
        event_id = event["event_id"]

        if event_id in seen:
            if seen[event_id] != event:
                raise DeterminismError(
                    "event_id conflict with differing event content"
                )

        seen[event_id] = event

    return sorted(
        normalized,
        key=canonical_key
    )
'@ | Set-Content -Encoding UTF8 $canonicalizationPath


Write-Host "Patching runner.py..."

@'
from .canonicalization import canonicalize
from .fingerprint import hash_state
from .models import INITIAL_STATE
from .reducer import reduce_state
from .validator import validate_events
from .taxonomy import classify


def replay(events: list[dict]):
    """
    ESAL v0.1 reference replay pipeline:

    RAW EVENTS
        -> validate
        -> canonicalize (C)
        -> reduce (F)
        -> fingerprint (H)
        -> classify
    """

    validate_events(events)

    canonical_events = canonicalize(events)

    state = reduce_state(
        INITIAL_STATE,
        canonical_events,
    )

    fingerprint = hash_state(state)

    classification = classify(
        state=state,
        fingerprint=fingerprint,
    )

    return {
        "canonical_events": canonical_events,
        "state": state,
        "fingerprint": fingerprint,
        "classification": classification,
    }
'@ | Set-Content -Encoding UTF8 $runnerPath


Write-Host ""
Write-Host "ESAL core pipeline patched."
Write-Host ""
Write-Host "Updated:"
Write-Host " - reference\esal\canonicalization.py"
Write-Host " - reference\esal\runner.py"