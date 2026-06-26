from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from .canonicalization import canonicalize
from .fingerprint import hash_state
from .models import INITIAL_STATE
from .reducer import reduce_state
from .validator import validate_events
from .taxonomy import classify
from .errors import GovernanceError, StructuralError, DeterminismError


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
    validate_events(events)
    canonical_events = canonicalize(events)

    state = None
    exc: Exception | None = None

    try:
        state = reduce_state(INITIAL_STATE, canonical_events)
    except (GovernanceError, StructuralError, DeterminismError) as e:
        exc = e

    fingerprint = hash_state(state) if state is not None else None
    classification = classify(state=state, exc=exc)

    return {
        "canonical_events": canonical_events,
        "state": state,
        "fingerprint": fingerprint,
        "classification": classification,
        "exception": exc,
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
    return events


def load_expected(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    """
    CLI entrypoint used by:
        python -m reference.esal.runner esal-tests

    Walks esal-tests/{canonical,adversarial,malformed}/*.jsonl and
    prints observed fingerprints/classifications. If an expected JSON
    exists in esal-tests/expected/, also prints match info.
    """
    if len(sys.argv) != 2:
        print(
            "Usage: python -m reference.esal.runner <tests-root>",
            file=sys.stderr,
        )
        sys.exit(1)

    tests_root = Path(sys.argv[1])
    expected_root = tests_root / "expected"

    if not tests_root.exists():
        print(f"Test root not found: {tests_root}", file=sys.stderr)
        sys.exit(1)

    categories = ["canonical", "adversarial", "malformed"]

    print("== ESAL v0.1 corpus replay ==")

    for cat in categories:
        cat_dir = tests_root / cat
        if not cat_dir.exists():
            continue

        for log_path in sorted(cat_dir.glob("*.jsonl")):
            try:
                events = load_jsonl(log_path)
            except json.JSONDecodeError as e:
                print(f"[{cat}] {log_path.name} -> JSON decode error: {e}")
                continue

            if not events:
                # Skip empty logs quietly for now
                print(f"[{cat}] {log_path.name} -> no events (skipped)")
                continue

            result = replay(events)

            # Expected file convention: same stem under expected/
            expected_path = expected_root / f"{log_path.stem}.json"
            expected = load_expected(expected_path)

            exc = result.get("exception")
            exc_suffix = f" ({exc})" if exc is not None else ""

            print(
                f"[{cat}] {log_path.name} -> "
                f"fp={result['fingerprint']} "
                f"class={result['classification']}{exc_suffix}"
            )

            if expected:
                exp_fp = expected.get("fingerprint")
                exp_cls = expected.get("classification")
                fp_match = (exp_fp == result["fingerprint"]) if exp_fp else None
                cls_match = (exp_cls == result["classification"]) if exp_cls else None

                print(
                    f"    expected={expected_path.name} "
                    f"fp_match={fp_match} "
                    f"class_match={cls_match}"
                )


if __name__ == "__main__":
    main()