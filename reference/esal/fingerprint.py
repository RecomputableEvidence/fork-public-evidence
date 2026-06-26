# reference/esal/fingerprint.py

import json
import hashlib
from .models import State, ViolationRecord


def _state_to_canonical_dict(state: State) -> dict:
    """
    Convert State into a canonical JSON-serializable dict.
    All sets/tuples are turned into sorted lists so the JSON is stable.
    """
    return {
        "authority": sorted(state.authority),
        "constraints": sorted(state.constraints),
        "obligations": sorted(state.obligations),
        "lineage": list(state.lineage),
        "validity": state.validity,
        "violations": [
            {
                "constraint_id": v.constraint_id,
                "event_id": v.event_id,
                "boundary_id": v.boundary_id,
                "severity": v.severity,
                "timestamp": v.timestamp,
            }
            for v in state.violations
        ],
    }


def hash_state(state: State) -> str:
    """
    H(S): canonical JSON encoding + SHA-256 digest hex string.
    """
    canonical = _state_to_canonical_dict(state)
    payload = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return digest