#!/usr/bin/env python3
"""Bounded structural checker for the Fork current-standing register.

A PASS means only that the declared current-standing JSON is parseable and
contains the required structural fields/invariants checked here. It does not
validate the truth of status claims, canonical bytes of pending artifacts,
research correctness, independence, compliance, legal sufficiency, safety,
production readiness, procurement approval, or institutional authority.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "current-standing" / "FORK_CURRENT_WORK_REGISTER_v0_1.json"
EXPECTED_SCHEMA = "FORK_CURRENT_WORK_REGISTER_v0_1"
EXPECTED_BASE = "1663674949ec90ff7e8878c27bea9dbde97096d7"
REQUIRED_INVARIANTS = {
    "ARTIFACT_PRESENT != EXECUTED",
    "EXECUTED != PASSED",
    "PASSED != FROZEN",
    "FROZEN != INDEPENDENTLY_REVIEWED",
    "REPOSITORY_ADMITTED != COMMERCIALLY_QUALIFIED",
    "MULTIPLE_PURPOSE_ROUTES != MULTIPLE_INDEPENDENT_CONFIRMATIONS",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    if not REGISTER.is_file():
        fail(f"missing register: {REGISTER.relative_to(ROOT)}")

    try:
        data = json.loads(REGISTER.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"register is not valid UTF-8 JSON: {exc}")

    if data.get("schema_id") != EXPECTED_SCHEMA:
        fail("unexpected schema_id")
    if data.get("snapshot_base_commit") != EXPECTED_BASE:
        fail("unexpected snapshot_base_commit")

    invariants = set(data.get("governing_non_inheritance", []))
    missing_invariants = sorted(REQUIRED_INVARIANTS - invariants)
    if missing_invariants:
        fail(f"missing governing non-inheritance invariants: {missing_invariants}")

    objects = data.get("objects")
    if not isinstance(objects, list) or not objects:
        fail("objects must be a non-empty list")

    seen: set[str] = set()
    for index, obj in enumerate(objects):
        if not isinstance(obj, dict):
            fail(f"object {index} is not a JSON object")
        object_id = obj.get("id")
        if not isinstance(object_id, str) or not object_id.strip():
            fail(f"object {index} missing id")
        if object_id in seen:
            fail(f"duplicate object id: {object_id}")
        seen.add(object_id)
        if not isinstance(obj.get("material_state"), str):
            fail(f"{object_id}: missing material_state")
        if not isinstance(obj.get("next_gate"), str) or not obj["next_gate"].strip():
            fail(f"{object_id}: missing next_gate")
        if not any(key in obj for key in ("result_state", "current_disposition", "freeze_state")):
            fail(f"{object_id}: no result/current/freeze state")

    non_claims = data.get("snapshot_non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        fail("snapshot_non_claims must preserve at least three explicit boundaries")

    print("PASS: current-standing register structural checks passed")
    print(f"schema_id: {EXPECTED_SCHEMA}")
    print(f"objects: {len(objects)}")
    print("boundary: structural consistency only; no stronger standing established")
    return 0


if __name__ == "__main__":
    sys.exit(main())
