import hashlib
import json
from typing import Any

from .models import State, state_to_dict


def canonical_state_encoding(state: State) -> str:
    return json.dumps(
        state_to_dict(state),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def hash_state(state: State) -> str:
    return hashlib.sha256(
        canonical_state_encoding(state).encode("utf-8")
    ).hexdigest()


def canonical_event_sequence_hash(events: list[dict[str, Any]]) -> str:
    encoded = json.dumps(
        events,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()