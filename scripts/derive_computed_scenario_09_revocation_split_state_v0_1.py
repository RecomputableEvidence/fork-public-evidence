#!/usr/bin/env python3
"""
derive_computed_scenario_09_revocation_split_state_v0_1.py

Deterministically derives Scenario 09 revocation visibility and split-state classifications
from independent System A, System B, System C, and freshness-policy fixtures.

This checker records only bounded state-divergence classifications. It does not decide
negligence, fault, excuse, legal sufficiency, compliance, authorization, correctness,
or execution eligibility.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


SCENARIO_ID = "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY"
VERSION = "v0.1"

NON_CLAIMS = [
    "does_not_decide_negligence",
    "does_not_decide_fault",
    "does_not_decide_excuse",
    "does_not_decide_legal_sufficiency",
    "does_not_decide_compliance",
    "does_not_decide_authorization",
    "does_not_decide_correctness",
    "does_not_decide_execution_eligibility",
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: str) -> datetime:
    if value is None:
        raise ValueError("timestamp is required")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def minutes_between(older: datetime, newer: datetime) -> float:
    return (newer - older).total_seconds() / 60.0


def derive(case_dir: Path) -> Dict[str, Any]:
    system_a = load_json(case_dir / "system_a_current_revocation_state.json")
    system_b = load_json(case_dir / "system_b_visibility_sync_state.json")
    system_c = load_json(case_dir / "system_c_consumption_attempt_state.json")
    policy = load_json(case_dir / "freshness_policy.json")

    case_id = system_a["case_id"]
    claim_id = system_a["claim_id"]
    revocation = system_a["revocation_event"]
    revocation_id = revocation["revocation_id"]

    effective_at = parse_time(revocation["effective_at"])
    b_last_sync_at = parse_time(system_b["last_sync_at"])
    b_known_state_as_of = parse_time(system_b["known_state_as_of"])
    c_attempted_at = parse_time(system_c["attempted_at"])

    visible_to_b = revocation_id in system_b.get("visible_revocation_ids", [])
    b_sync_precedes_revocation = b_last_sync_at < effective_at

    visibility_age = minutes_between(b_known_state_as_of, c_attempted_at)
    max_visibility_age = float(policy["max_visibility_age_minutes"])

    upstream_revocation_current_before_consumption = (
        system_a.get("current_validity", {}).get("status") == "REVOKED"
        and effective_at <= c_attempted_at
    )

    system_b_revocation_not_visible = upstream_revocation_current_before_consumption and not visible_to_b
    system_b_state_stale_at_consumption = (
        upstream_revocation_current_before_consumption
        and (b_known_state_as_of < effective_at or visibility_age > max_visibility_age)
    )

    basis_seen = system_c.get("basis_seen_by_consumer", {})
    c_visible_revocations = basis_seen.get("visible_revocation_ids", [])
    c_saw_revocation = revocation_id in c_visible_revocations
    system_c_revalidation_present = bool(basis_seen.get("revalidation_event_id")) and bool(basis_seen.get("revalidated_at"))

    if basis_seen.get("revalidated_at"):
        revalidated_at = parse_time(basis_seen["revalidated_at"])
        system_c_revalidation_present = system_c_revalidation_present and revalidated_at >= b_last_sync_at and revalidated_at >= effective_at

    current_revalidation_required = bool(
        policy.get("require_revalidation_after_upstream_revocation")
        and upstream_revocation_current_before_consumption
    )

    system_c_consumed_without_revocation_visibility = (
        upstream_revocation_current_before_consumption
        and not c_saw_revocation
        and basis_seen.get("local_validity_status") == "VALID"
    )

    derived_flags = {
        "upstream_revocation_current_before_consumption": upstream_revocation_current_before_consumption,
        "system_b_revocation_not_visible": system_b_revocation_not_visible,
        "system_b_sync_precedes_revocation": b_sync_precedes_revocation,
        "system_b_state_stale_at_consumption": system_b_state_stale_at_consumption,
        "system_c_consumed_without_revocation_visibility": system_c_consumed_without_revocation_visibility,
        "current_revalidation_required": current_revalidation_required,
        "system_c_revalidation_present": system_c_revalidation_present,
    }

    gap_types: List[str] = []
    if system_b_revocation_not_visible or system_b_state_stale_at_consumption:
        gap_types.append("REVOCATION_VISIBILITY_GAP")
    if system_c_consumed_without_revocation_visibility:
        gap_types.append("SPLIT_STATE_CONSUMPTION_GAP")
    if current_revalidation_required and not system_c_revalidation_present:
        gap_types.append("CURRENT_REVALIDATION_REQUIRED")

    if gap_types:
        derivation_status = "COMPUTED_GAP_RECORDED"
        closure_requirements = [
            "revocation_visible_to_system_b",
            "system_b_sync_after_revocation_effective_at",
            "system_c_revalidation_after_visibility",
            "new_boundary_record_for_downstream_reliance",
        ]
    else:
        derivation_status = "NO_COMPUTED_GAP_RECORDED"
        closure_requirements = []

    return {
        "case_id": case_id,
        "scenario_id": SCENARIO_ID,
        "computed_scenario_version": VERSION,
        "derivation_status": derivation_status,
        "inspectability": "INSPECTABLE",
        "timeline": {
            "revocation_effective_at": revocation["effective_at"],
            "system_b_last_sync_at": system_b["last_sync_at"],
            "system_b_known_state_as_of": system_b["known_state_as_of"],
            "system_c_attempted_at": system_c["attempted_at"],
        },
        "derived_flags": derived_flags,
        "gap_types": gap_types,
        "closure_requirements": closure_requirements,
        "non_claims": NON_CLAIMS,
    }


def canonical_json(value: Dict[str, Any]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def check_case(case_dir: Path, write: bool) -> bool:
    result = derive(case_dir)
    output_path = case_dir / "derived_result.json"
    expected_path = case_dir / "expected_derived_result.json"

    if write:
        output_path.write_text(canonical_json(result), encoding="utf-8", newline="\n")

    expected = load_json(expected_path)

    if result != expected:
        print(f"FAIL: derived result mismatch for {case_dir}")
        print("Computed:")
        print(canonical_json(result))
        print("Expected:")
        print(canonical_json(expected))
        return False

    print(f"PASS: {case_dir.name} -> {result['derivation_status']}")
    if write:
        print(f"WROTE: {output_path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cases-root",
        default="examples/simulations/governance-proof-surface/computed_scenario_09/cases",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    cases_root = Path(args.cases_root)
    if not cases_root.exists():
        raise SystemExit(f"FAIL: cases root not found: {cases_root}")

    case_dirs = sorted([p for p in cases_root.iterdir() if p.is_dir()])
    if not case_dirs:
        raise SystemExit(f"FAIL: no case directories found under {cases_root}")

    all_ok = True
    for case_dir in case_dirs:
        all_ok = check_case(case_dir, args.write) and all_ok

    if not all_ok:
        raise SystemExit(1)

    print("PASS: computed Scenario 09 revocation split-state derivation verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
