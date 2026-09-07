#!/usr/bin/env python3
"""Mechanical checker for Fork CAD / PROOF-005 bounded F3 type-strictness successor v0.2.3."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V022_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2_2.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v022_predecessor", V022_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load v0.2.2 predecessor checker")
V022 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V022)
CandidateError = V022.CandidateError

EXPECTED_CONTROL_EFFECTS: dict[str, Any] = {
    "status": "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED",
    "pull_request_effect": "REVIEW_SURFACE_ONLY",
    "admission": False,
    "publication": False,
    "endorsement": False,
    "provider_calls": 0,
    "pair_001_effect": "NONE",
    "pair_001_execution_authorized": False,
    "readiness_effect": "NONE",
    "readiness_promoted": False,
    "proof_admission_effect": "NONE",
    "model_standing_effect": "NONE",
    "authority_effect": "NONE",
}


def require_exact_type_and_value(obj: dict[str, Any], key: str, expected: Any, label: str) -> None:
    """Require exact Python type and value, avoiding bool/int equality collapse after JSON parsing."""
    if key not in obj:
        raise CandidateError(f"{label}: missing governed field {key!r}")
    actual = obj[key]
    if type(actual) is not type(expected):
        raise CandidateError(
            f"{label}: {key} must have exact JSON type {type(expected).__name__}; "
            f"got {type(actual).__name__}"
        )
    if actual != expected:
        raise CandidateError(f"{label}: {key} must equal {expected!r}")


def validate_control_effect_type_strictness(record: dict[str, Any]) -> None:
    """F3-only invariant: all thirteen governed effect fields are exact in type and value."""
    V022.validate_control_effects_schema(record)
    governed = set(V022.CONTROL_EFFECT_KEYS) - {"record_id"}
    if governed != set(EXPECTED_CONTROL_EFFECTS):
        raise CandidateError("effects: declared F3 governed-key set does not match predecessor schema")
    for key, expected in EXPECTED_CONTROL_EFFECTS.items():
        require_exact_type_and_value(record, key, expected, "effects")


def validate_candidate(root: Path) -> None:
    V022.validate_candidate(root)
    effects = V022.V021.load_json_strict(root / V022.GOVERNED_PATHS["effects"])
    validate_control_effect_type_strictness(effects)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        validate_candidate(args.root)
    except CandidateError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: Fork CAD / PROOF-005 bounded F3 type-strictness successor v0.2.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
