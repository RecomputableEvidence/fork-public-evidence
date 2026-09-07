#!/usr/bin/env python3
"""Mechanical checker for Fork CAD / PROOF-005 correction successor v0.2.1."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v02_predecessor", PREDECESSOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load v0.2 predecessor checker")
PREDECESSOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREDECESSOR)

CandidateError = PREDECESSOR.CandidateError

EVENT_ALLOWED_KEYS = {
    "event_id",
    "event_type",
    "statement_origin",
    "source_role",
    "source_refs",
    "observable_text_summary",
    "artifact_grounded_disposition",
    "mechanism_verified",
    "causal_standing",
}

EXPECTED_EVENT_REGISTER_CANONICAL_SHA256 = (
    "cd107b7ab2da6e49d4e1f2bd1f4f75e3dd4e7718a83592eeeb65735b6ebe36bb"
)


def reject_duplicate_object_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CandidateError(f"json: duplicate object key {key!r} is not permitted")
        result[key] = value
    return result


def load_json_strict(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
        value = json.loads(text, object_pairs_hook=reject_duplicate_object_keys)
    except CandidateError:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateError(f"{path}: cannot load strict JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise CandidateError(f"{path}: top-level JSON must be object")
    return value


def canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_model_self_report_event(event: dict[str, Any]) -> None:
    """General non-promotion invariant for any model-self-report event."""
    keys = set(event)
    missing = EVENT_ALLOWED_KEYS - keys
    extras = keys - EVENT_ALLOWED_KEYS
    eid = str(event.get("event_id", "<unknown>"))
    if missing:
        raise CandidateError(f"{eid}: event object missing controlled keys {sorted(missing)!r}")
    if extras:
        raise CandidateError(f"{eid}: undeclared event fields are not permitted: {sorted(extras)!r}")
    if event.get("source_role") != "MODEL_SELF_REPORT":
        raise CandidateError(f"{eid}: generic model-self-report validator requires MODEL_SELF_REPORT source_role")
    if event.get("mechanism_verified") is not False:
        raise CandidateError(f"{eid}: model self-report cannot verify mechanism")
    if event.get("causal_standing") != "UNRESOLVED":
        raise CandidateError(
            f"{eid}: model self-report causal standing must remain unresolved regardless of statement_origin"
        )


def validate_event_register_v0_2_1(register: dict[str, Any]) -> None:
    """Preserve v0.2 checks and bind the reviewed historical register structurally."""
    PREDECESSOR.validate_event_register(register)

    try:
        actual = canonical_json_sha256(register)
    except (TypeError, ValueError) as exc:
        raise CandidateError(f"events: cannot canonicalize reviewed event register: {exc}") from exc
    if actual != EXPECTED_EVENT_REGISTER_CANONICAL_SHA256:
        raise CandidateError(
            "events: reviewed v0.2 event register structural fingerprint mismatch"
        )

    events = register.get("events")
    assert isinstance(events, list)
    for event in events:
        assert isinstance(event, dict)
        if event.get("source_role") == "MODEL_SELF_REPORT":
            validate_model_self_report_event(event)


def validate_candidate(root: Path) -> None:
    PREDECESSOR.validate_candidate(root)
    event_path = (
        root
        / "docs/meta-evidence/conversational-authority-drift-v0.2"
        / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
        / "OBSERVABLE_EVENT_REGISTER_v0_2.json"
    )
    validate_event_register_v0_2_1(load_json_strict(event_path))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        validate_candidate(args.root)
    except CandidateError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: Fork CAD / PROOF-005 correction successor v0.2.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
