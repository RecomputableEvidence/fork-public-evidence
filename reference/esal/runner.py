from __future__ import annotations

import json
import sys
from pathlib import Path

from .canonicalization import canonicalize
from .fingerprint import hash_state
from .models import INITIAL_STATE
from .reducer import reduce_state
from .validator import validate_events
from .taxonomy import classify


def replay(events: list[dict]) -> dict:
    """
    ESAL v0.1 reference replay pipeline:

    RAW EVENTS
        -> validate
        -> canonicalize (C)
        -> reduce (F)
        -> fingerprint (H)
        -> classify
    """

    # 1. Schema / lineage validation
    validate_events(events)

    # 2. Canonical ordering C(E)
    canonical_events = canonicalize(events)

    # 3. State reduction F(S0, E*)
    state = reduce_state(
        INITIAL_STATE,
        canonical_events,
    )

    # 4. Fingerprint H(S)
    fingerprint = hash_state(state)

    # 5. Classification (no exception path here, so exc=None)
    classification = classify(
        state=state,
        exc=None,
    )

    return {
        "canonical_events": canonical_events,
        "state": state,
        "fingerprint": fingerprint,
        "classification": classification,
    }


def main() -> None:
    """
    CLI entrypoint used by:
        python -m reference.esal.runner esal-tests
    """

    if len(sys.argv) != 2:
        print(
            "Usage: python -m reference.esal.runner <tests-root>",
            file=sys.stderr,
        )
        sys.exit(1)

    tests_root = Path(sys.argv[1])
    log_path = tests_root / "canonical" / "log1-basic-A-B-C.jsonl"

    if not log_path.exists():
        print(f"Log file not found: {log_path}", file=sys.stderr)
        sys.exit(1)

    # Load JSONL events
    events: list[dict] = []
    with log_path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))

    # Run replay
    result = replay(events)

    print(f"Log: {log_path.name}")
    print(f"Fingerprint: {result['fingerprint']}")
    print(f"Classification: {result['classification']}")


if __name__ == "__main__":
    main()