#!/usr/bin/env python3
"""Deterministic semantic checker for Governed Handoff Cadence Harness v0.1."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from ghch_common_v0_1 import (  # noqa: E402
    CANONICAL_PROFILE,
    EXPECTED_ACTORS,
    EXPECTED_STAGES,
    REQUIRED_NON_CLAIMS,
    sha256_value,
)

ALLOWED_PROFILES = {
    "CLEAN_ROUND_TRIP",
    "PERMISSIBLE_NARROWING",
    "SIDECAR_UNAVAILABLE_FAIL_OPEN",
}

LOCAL_EFFECT_RULES = {
    "PREREGISTER": ("NONE", "NONE", "NONE"),
    "UPSTREAM_EMIT": ("LOCAL_ONLY", "PREEXISTING_LOCAL_GOVERNANCE", "NONE"),
    "FORK_CAPTURE_INGRESS": ("NONE", "NONE", "NONE"),
    "DOWNSTREAM_INGEST": ("NONE", "NONE", "NONE"),
    "DOWNSTREAM_LOCAL_DISPOSITION": (
        "LOCAL_ONLY",
        "PREEXISTING_LOCAL_GOVERNANCE",
        "LOCAL_REASSESSMENT",
    ),
    "FORK_CAPTURE_EGRESS": ("NONE", "NONE", "NONE"),
    "UPSTREAM_RECONCILE": ("NONE", "NONE", "NONE"),
    "CADENCE_CLOSE": ("NONE", "NONE", "NONE"),
}

FLAG_CODES = {
    "authority_transfer": "AUTHORITY_TRANSFER",
    "authority_inheritance": "AUTHORITY_INHERITANCE",
    "standing_inheritance": "STANDING_INHERITANCE",
    "endorsement_inheritance": "ENDORSEMENT_INHERITANCE",
    "evidence_reference_promotion": "EVIDENCE_REFERENCE_PROMOTION",
    "unresolved_resolved_by_assumption": "UNRESOLVED_RESOLVED_BY_ASSUMPTION",
    "declared_vs_observed_mismatch": "DECLARED_VS_OBSERVED_MISMATCH",
}

def _digest_without(obj: Dict[str, Any], key: str) -> str:
    return sha256_value({k: v for k, v in obj.items() if k != key})

def evaluate(record: Dict[str, Any]) -> Tuple[str, List[str]]:
    findings: List[str] = []

    if record.get("schema_version") != "0.1":
        findings.append("SCHEMA_VERSION")
    if record.get("artifact_type") != "GHCH_CADENCE_RECORD":
        findings.append("ARTIFACT_TYPE")
    if record.get("canonicalization_profile") != CANONICAL_PROFILE:
        findings.append("CANONICAL_PROFILE")
    profile = record.get("profile")
    if profile not in ALLOWED_PROFILES:
        findings.append("PROFILE")

    participants = record.get("participants")
    expected_participants = {
        "HARNESS-001": ("SIMULATION_HARNESS", "NONE"),
        "UPSTREAM-001": ("UPSTREAM_GOVERNANCE", "UPSTREAM_LOCAL_ONLY"),
        "FORK-001": ("FORK_EVIDENCE_SIDECAR", "NONE"),
        "DOWNSTREAM-001": ("DOWNSTREAM_GOVERNANCE", "DOWNSTREAM_LOCAL_ONLY"),
    }
    observed_participants = {}
    if isinstance(participants, list):
        for item in participants:
            if isinstance(item, dict) and isinstance(item.get("participant_id"), str):
                pid = item["participant_id"]
                if pid in observed_participants:
                    findings.append("DUPLICATE_PARTICIPANT")
                observed_participants[pid] = (
                    item.get("role"),
                    item.get("authority_domain"),
                )
    else:
        findings.append("PARTICIPANTS_TYPE")
    if observed_participants != expected_participants:
        findings.append("PARTICIPANTS")

    claim_bundle = record.get("claim_bundle")
    policy = record.get("exchange_policy")
    nonclaims = record.get("non_claim_set")
    if not isinstance(claim_bundle, dict):
        findings.append("CLAIM_BUNDLE")
        claim_bundle = {}
    if not isinstance(policy, dict):
        findings.append("EXCHANGE_POLICY")
        policy = {}
    if not isinstance(nonclaims, dict):
        findings.append("NON_CLAIM_SET")
        nonclaims = {}

    if claim_bundle.get("canonical_sha256") != _digest_without(claim_bundle, "canonical_sha256"):
        findings.append("CLAIM_BUNDLE_DIGEST")
    if policy.get("canonical_sha256") != _digest_without(policy, "canonical_sha256"):
        findings.append("POLICY_DIGEST")
    if nonclaims.get("canonical_sha256") != _digest_without(nonclaims, "canonical_sha256"):
        findings.append("NON_CLAIM_DIGEST")

    if nonclaims.get("non_claims") != REQUIRED_NON_CLAIMS:
        findings.append("NON_CLAIM_GAP")
    required_policy = {
        "authority_transfer_permitted": False,
        "authority_inheritance_permitted": False,
        "standing_inheritance_permitted": False,
        "endorsement_inheritance_permitted": False,
        "evidence_reference_promotion_permitted": False,
        "unresolved_resolution_by_assumption_permitted": False,
        "fork_mode": "READ_ONLY_OUT_OF_BAND_FAIL_OPEN",
    }
    for key, expected in required_policy.items():
        if policy.get(key) != expected:
            findings.append("POLICY_" + key.upper())

    events = record.get("events")
    if not isinstance(events, list):
        findings.append("EVENTS_TYPE")
        events = []

    if [e.get("stage") for e in events if isinstance(e, dict)] != EXPECTED_STAGES:
        findings.append("STAGE_ORDER")
    event_ids = [e.get("event_id") for e in events if isinstance(e, dict)]
    if len(event_ids) != len(set(event_ids)):
        findings.append("DUPLICATE_EVENT_ID")
    if event_ids != [f"GHCH-EVT-{i:03d}" for i in range(1, 9)]:
        findings.append("EVENT_ID_SEQUENCE")

    predecessor = None
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            findings.append(f"EVENT_TYPE:{index}")
            continue
        stage = event.get("stage")
        if event.get("actor_id") != EXPECTED_ACTORS.get(stage):
            findings.append("ACTOR:" + str(stage))
        if event.get("predecessor_ref") != predecessor:
            findings.append("LINEAGE:" + str(stage))

        integrity = event.get("event_integrity")
        if not isinstance(integrity, dict):
            findings.append("EVENT_INTEGRITY:" + str(stage))
            event_sha = None
        else:
            event_sha = integrity.get("canonical_event_sha256")
            if integrity.get("canonicalization_profile") != CANONICAL_PROFILE:
                findings.append("EVENT_CANONICAL_PROFILE:" + str(stage))
            if event_sha != _digest_without(event, "event_integrity"):
                findings.append("EVENT_DIGEST:" + str(stage))

        if event.get("claim_bundle_ref") != {
            "bundle_id": claim_bundle.get("bundle_id"),
            "sha256": claim_bundle.get("canonical_sha256"),
        }:
            findings.append("CLAIM_REF:" + str(stage))
        if event.get("exchange_policy_ref") != {
            "policy_id": policy.get("policy_id"),
            "sha256": policy.get("canonical_sha256"),
        }:
            findings.append("POLICY_REF:" + str(stage))
        if event.get("non_claim_set_ref") != {
            "non_claim_set_id": nonclaims.get("non_claim_set_id"),
            "sha256": nonclaims.get("canonical_sha256"),
        }:
            findings.append("NON_CLAIM_REF:" + str(stage))

        effects = event.get("local_effects", {})
        expected_effects = LOCAL_EFFECT_RULES.get(stage)
        if expected_effects is None:
            findings.append("UNKNOWN_STAGE:" + str(stage))
        else:
            observed_effects = (
                effects.get("authority_action"),
                effects.get("authority_source"),
                effects.get("standing_action"),
            )
            if observed_effects != expected_effects:
                findings.append("LOCAL_EFFECTS:" + str(stage))
        if effects.get("standing_action") == "LOCAL_REASSESSMENT":
            if not isinstance(effects.get("standing_basis"), str) or not effects["standing_basis"]:
                findings.append("LOCAL_STANDING_BASIS:" + str(stage))
        elif effects.get("standing_basis") is not None:
            findings.append("UNDECLARED_STANDING_BASIS:" + str(stage))

        flags = event.get("detected_flags")
        if not isinstance(flags, dict):
            findings.append("FLAGS:" + str(stage))
        else:
            if set(flags) != set(FLAG_CODES):
                findings.append("FLAG_SET:" + str(stage))
            for key, code in FLAG_CODES.items():
                if flags.get(key) is True:
                    findings.append(code + ":" + str(stage))
                elif flags.get(key) is not False:
                    findings.append("FLAG_VALUE:" + key + ":" + str(stage))

        delta = event.get("claim_delta")
        if not isinstance(delta, list):
            findings.append("CLAIM_DELTA_TYPE:" + str(stage))
            delta = []
        if stage != "DOWNSTREAM_LOCAL_DISPOSITION" and delta:
            findings.append("DELTA_OUTSIDE_DISPOSITION:" + str(stage))
        for operation in delta:
            if not isinstance(operation, dict):
                findings.append("DELTA_ENTRY:" + str(stage))
                continue
            if operation.get("operation") != "NARROW":
                findings.append("UNPERMITTED_CLAIM_OPERATION:" + str(operation.get("operation")))
            if operation.get("claim_id") not in {
                c.get("claim_id") for c in claim_bundle.get("claims", []) if isinstance(c, dict)
            }:
                findings.append("UNKNOWN_CLAIM_DELTA")

        if event_sha is not None:
            predecessor = {
                "event_id": event.get("event_id"),
                "sha256": event_sha,
            }

    by_stage = {e.get("stage"): e for e in events if isinstance(e, dict)}
    sidecar_ingress = by_stage.get("FORK_CAPTURE_INGRESS", {})
    sidecar_egress = by_stage.get("FORK_CAPTURE_EGRESS", {})
    close = by_stage.get("CADENCE_CLOSE", {})
    downstream_ingest = by_stage.get("DOWNSTREAM_INGEST", {})
    downstream_disposition = by_stage.get("DOWNSTREAM_LOCAL_DISPOSITION", {})
    reconciliation = record.get("reconciliation", {})
    unresolved = reconciliation.get("unresolved_items")

    if profile == "SIDECAR_UNAVAILABLE_FAIL_OPEN":
        if sidecar_ingress.get("observed_status") != "UNAVAILABLE":
            findings.append("INGRESS_UNAVAILABLE_NOT_PRESERVED")
        if sidecar_egress.get("observed_status") != "UNAVAILABLE":
            findings.append("EGRESS_UNAVAILABLE_NOT_PRESERVED")
        if downstream_ingest.get("observed_status") != "COMPLETED":
            findings.append("FAIL_OPEN_CONTINUITY_INGEST")
        if downstream_disposition.get("observed_status") != "COMPLETED":
            findings.append("FAIL_OPEN_CONTINUITY_DISPOSITION")
        if close.get("observed_status") != "COMPLETED_WITH_OBSERVATION_GAPS":
            findings.append("FAIL_OPEN_CLOSE_STANDING")
        if unresolved != [
            "FORK_INGRESS_CAPTURE_UNAVAILABLE",
            "FORK_EGRESS_CAPTURE_UNAVAILABLE",
        ]:
            findings.append("OBSERVATION_GAPS")
    else:
        if sidecar_ingress.get("observed_status") != "COMPLETED":
            findings.append("INGRESS_CAPTURE")
        if sidecar_egress.get("observed_status") != "COMPLETED":
            findings.append("EGRESS_CAPTURE")
        if close.get("observed_status") != "COMPLETED":
            findings.append("CLOSE_STATUS")
        if unresolved != []:
            findings.append("UNEXPECTED_UNRESOLVED_ITEMS")

    disposition_delta = downstream_disposition.get("claim_delta", [])
    relationship = reconciliation.get("relationship")
    if profile == "PERMISSIBLE_NARROWING":
        if relationship != "NARROWED":
            findings.append("NARROWING_RELATIONSHIP")
        if len(disposition_delta) != 1 or disposition_delta[0].get("operation") != "NARROW":
            findings.append("NARROWING_DELTA")
        if reconciliation.get("downstream_local_disposition") != "ACCEPTED_WITH_NARROWING":
            findings.append("NARROWING_DISPOSITION")
    elif profile in {"CLEAN_ROUND_TRIP", "SIDECAR_UNAVAILABLE_FAIL_OPEN"}:
        if relationship != "PRESERVED":
            findings.append("PRESERVATION_RELATIONSHIP")
        if disposition_delta:
            findings.append("UNDECLARED_DELTA")
        if reconciliation.get("downstream_local_disposition") != "ACCEPTED_FOR_LOCAL_PROCESSING":
            findings.append("LOCAL_DISPOSITION")

    if reconciliation.get("upstream_acknowledgment") != "ACKNOWLEDGED_WITHOUT_ENDORSEMENT":
        findings.append("ACKNOWLEDGMENT_OVERREAD")

    non_effects = record.get("declared_non_effects", {})
    expected_non_effects = {
        "authority_transfer": "NONE",
        "standing_inheritance": "NONE",
        "endorsement_inheritance": "NONE",
        "production_or_compliance_effect": "NONE",
        "provider_calls": 0,
        "pair_001_calls": 0,
    }
    if non_effects != expected_non_effects:
        findings.append("DECLARED_NON_EFFECTS")

    # Deduplicate while preserving deterministic first-seen order.
    findings = list(dict.fromkeys(findings))
    if findings:
        return "GHCH_CADENCE_REJECTED", findings

    if profile == "PERMISSIBLE_NARROWING":
        return "GHCH_CADENCE_CONFORMS_WITH_PERMISSIBLE_NARROWING", []
    if profile == "SIDECAR_UNAVAILABLE_FAIL_OPEN":
        return "GHCH_CADENCE_CONFORMS_WITH_OBSERVATION_GAPS", []
    return "GHCH_CADENCE_CONFORMS_PRESERVED", []

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        result = {
            "disposition": "GHCH_CADENCE_REJECTED",
            "findings": ["UNREADABLE_RECORD:" + str(exc)],
        }
        if args.as_json:
            print(json.dumps(result, indent=2))
        else:
            print(result["disposition"])
            print("\n".join(result["findings"]))
        return 1

    disposition, findings = evaluate(record)
    if args.as_json:
        print(json.dumps({"disposition": disposition, "findings": findings}, indent=2))
    else:
        print(disposition)
        for finding in findings:
            print(finding)
    return 0 if not findings else 1

if __name__ == "__main__":
    raise SystemExit(main())
