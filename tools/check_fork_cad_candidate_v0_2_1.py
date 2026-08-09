#!/usr/bin/env python3
"""Mechanical checker for Fork CAD / PROOF-005 correction successor v0.2.1."""

from __future__ import annotations

import argparse
import importlib.util
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


def validate_event_register_v0_2_1(register: dict[str, Any]) -> None:
    """Preserve v0.2 checks and close the two exterior-review residuals."""
    PREDECESSOR.validate_event_register(register)
    events = register.get("events")
    assert isinstance(events, list)
    for event in events:
        assert isinstance(event, dict)
        eid = str(event.get("event_id", "<unknown>"))
        keys = set(event)
        missing = EVENT_ALLOWED_KEYS - keys
        extras = keys - EVENT_ALLOWED_KEYS
        if missing:
            raise CandidateError(f"{eid}: event object missing controlled keys {sorted(missing)!r}")
        if extras:
            raise CandidateError(f"{eid}: undeclared event fields are not permitted: {sorted(extras)!r}")
        if event.get("source_role") == "MODEL_SELF_REPORT" and event.get("causal_standing") != "UNRESOLVED":
            raise CandidateError(f"{eid}: model self-report causal standing must remain unresolved regardless of statement_origin")


def validate_candidate(root: Path) -> None:
    PREDECESSOR.validate_candidate(root)
    event_path = (
        root
        / "docs/meta-evidence/conversational-authority-drift-v0.2"
        / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
        / "OBSERVABLE_EVENT_REGISTER_v0_2.json"
    )
    validate_event_register_v0_2_1(PREDECESSOR.load_json(event_path))


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
