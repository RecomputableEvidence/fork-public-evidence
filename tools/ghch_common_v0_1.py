#!/usr/bin/env python3
"""Shared deterministic helpers for Governed Handoff Cadence Harness v0.1."""

from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Dict, List, Optional

CANONICAL_PROFILE = "GHCH-CANONICAL-JSON-v0.1"

REQUIRED_NON_CLAIMS = [
    "NO_AUTHORITY_TRANSFER",
    "NO_AUTHORITY_INHERITANCE",
    "NO_STANDING_INHERITANCE",
    "NO_ENDORSEMENT_INHERITANCE",
    "NO_EVIDENCE_REFERENCE_PROMOTION",
    "NO_UNRESOLVED_RESOLUTION_BY_ASSUMPTION",
    "NO_PRODUCTION_OR_COMPLIANCE_EFFECT",
]

EXPECTED_STAGES = [
    "PREREGISTER",
    "UPSTREAM_EMIT",
    "FORK_CAPTURE_INGRESS",
    "DOWNSTREAM_INGEST",
    "DOWNSTREAM_LOCAL_DISPOSITION",
    "FORK_CAPTURE_EGRESS",
    "UPSTREAM_RECONCILE",
    "CADENCE_CLOSE",
]

EXPECTED_ACTORS = {
    "PREREGISTER": "HARNESS-001",
    "UPSTREAM_EMIT": "UPSTREAM-001",
    "FORK_CAPTURE_INGRESS": "FORK-001",
    "DOWNSTREAM_INGEST": "DOWNSTREAM-001",
    "DOWNSTREAM_LOCAL_DISPOSITION": "DOWNSTREAM-001",
    "FORK_CAPTURE_EGRESS": "FORK-001",
    "UPSTREAM_RECONCILE": "UPSTREAM-001",
    "CADENCE_CLOSE": "HARNESS-001",
}

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def add_record_integrity(record: Dict[str, Any]) -> Dict[str, Any]:
    record = copy.deepcopy(record)
    record.pop("record_integrity", None)
    record["record_integrity"] = {
        "canonicalization_profile": CANONICAL_PROFILE,
        "canonical_record_sha256": sha256_value(record),
    }
    return record

def add_integrity(event: Dict[str, Any]) -> Dict[str, Any]:
    event = copy.deepcopy(event)
    event.pop("event_integrity", None)
    event["event_integrity"] = {
        "canonicalization_profile": CANONICAL_PROFILE,
        "canonical_event_sha256": sha256_value(event),
    }
    return event

def recompute_chain(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rebuilt: List[Dict[str, Any]] = []
    predecessor: Optional[Dict[str, str]] = None
    for source in events:
        event = copy.deepcopy(source)
        event["predecessor_ref"] = predecessor
        event = add_integrity(event)
        rebuilt.append(event)
        predecessor = {
            "event_id": event["event_id"],
            "sha256": event["event_integrity"]["canonical_event_sha256"],
        }
    return rebuilt

def base_claim_bundle() -> Dict[str, Any]:
    body = {
        "bundle_id": "GHCH-CB-001",
        "claims": [
            {
                "claim_id": "GHCH-CLM-001",
                "statement": "A bounded enterprise AI workflow event occurred under the declared source scope.",
                "standing": "ASSERTED",
                "scope": "SIMULATED_ENTERPRISE_WORKFLOW_ONLY",
                "evidence_refs": [
                    {
                        "artifact_id": "SIM-SOURCE-001",
                        "sha256": "1" * 64,
                    }
                ],
            },
            {
                "claim_id": "GHCH-CLM-002",
                "statement": "Fork observed or failed to observe the declared handoff stages as recorded.",
                "standing": "OBSERVATION_CANDIDATE",
                "scope": "SIDECAR_CAPTURE_SURFACE_ONLY",
                "evidence_refs": [],
            },
        ],
    }
    body["canonicalization_profile"] = CANONICAL_PROFILE
    body["canonical_sha256"] = sha256_value(
        {k: v for k, v in body.items() if k != "canonical_sha256"}
    )
    return body

def exchange_policy() -> Dict[str, Any]:
    body = {
        "policy_id": "GHCH-POL-001",
        "authority_transfer_permitted": False,
        "authority_inheritance_permitted": False,
        "standing_inheritance_permitted": False,
        "endorsement_inheritance_permitted": False,
        "evidence_reference_promotion_permitted": False,
        "unresolved_resolution_by_assumption_permitted": False,
        "fork_mode": "READ_ONLY_OUT_OF_BAND_FAIL_OPEN",
        "canonicalization_profile": CANONICAL_PROFILE,
    }
    body["canonical_sha256"] = sha256_value(
        {k: v for k, v in body.items() if k != "canonical_sha256"}
    )
    return body

def non_claim_set() -> Dict[str, Any]:
    body = {
        "non_claim_set_id": "GHCH-NC-001",
        "non_claims": list(REQUIRED_NON_CLAIMS),
        "canonicalization_profile": CANONICAL_PROFILE,
    }
    body["canonical_sha256"] = sha256_value(
        {k: v for k, v in body.items() if k != "canonical_sha256"}
    )
    return body

def participants() -> List[Dict[str, Any]]:
    return [
        {
            "participant_id": "HARNESS-001",
            "role": "SIMULATION_HARNESS",
            "authority_domain": "NONE",
        },
        {
            "participant_id": "UPSTREAM-001",
            "role": "UPSTREAM_GOVERNANCE",
            "authority_domain": "UPSTREAM_LOCAL_ONLY",
        },
        {
            "participant_id": "FORK-001",
            "role": "FORK_EVIDENCE_SIDECAR",
            "authority_domain": "NONE",
        },
        {
            "participant_id": "DOWNSTREAM-001",
            "role": "DOWNSTREAM_GOVERNANCE",
            "authority_domain": "DOWNSTREAM_LOCAL_ONLY",
        },
    ]

def _event(
    index: int,
    stage: str,
    actor_id: str,
    claim_bundle: Dict[str, Any],
    policy: Dict[str, Any],
    nonclaims: Dict[str, Any],
    observed_status: str = "COMPLETED",
    authority_action: str = "NONE",
    authority_source: str = "NONE",
    standing_action: str = "NONE",
    standing_basis: Optional[str] = None,
    claim_delta: Optional[List[Dict[str, Any]]] = None,
    notes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "event_id": f"GHCH-EVT-{index:03d}",
        "stage": stage,
        "actor_id": actor_id,
        "predecessor_ref": None,
        "claim_bundle_ref": {
            "bundle_id": claim_bundle["bundle_id"],
            "sha256": claim_bundle["canonical_sha256"],
        },
        "exchange_policy_ref": {
            "policy_id": policy["policy_id"],
            "sha256": policy["canonical_sha256"],
        },
        "non_claim_set_ref": {
            "non_claim_set_id": nonclaims["non_claim_set_id"],
            "sha256": nonclaims["canonical_sha256"],
        },
        "claim_delta": claim_delta or [],
        "local_effects": {
            "authority_action": authority_action,
            "authority_source": authority_source,
            "standing_action": standing_action,
            "standing_basis": standing_basis,
        },
        "observed_status": observed_status,
        "detected_flags": {
            "authority_transfer": False,
            "authority_inheritance": False,
            "standing_inheritance": False,
            "endorsement_inheritance": False,
            "evidence_reference_promotion": False,
            "unresolved_resolved_by_assumption": False,
            "declared_vs_observed_mismatch": False,
        },
        "notes": notes or [],
    }

def build_cadence(profile: str) -> Dict[str, Any]:
    claim_bundle = base_claim_bundle()
    policy = exchange_policy()
    nonclaims = non_claim_set()
    sidecar_unavailable = profile == "SIDECAR_UNAVAILABLE_FAIL_OPEN"
    narrowed = profile == "PERMISSIBLE_NARROWING"

    events = [
        _event(
            1,
            "PREREGISTER",
            "HARNESS-001",
            claim_bundle,
            policy,
            nonclaims,
            notes=["Frozen simulated route, roles, policies, and expected stage order."],
        ),
        _event(
            2,
            "UPSTREAM_EMIT",
            "UPSTREAM-001",
            claim_bundle,
            policy,
            nonclaims,
            authority_action="LOCAL_ONLY",
            authority_source="PREEXISTING_LOCAL_GOVERNANCE",
            notes=["Upstream authorizes only release within its own declared governance domain."],
        ),
        _event(
            3,
            "FORK_CAPTURE_INGRESS",
            "FORK-001",
            claim_bundle,
            policy,
            nonclaims,
            observed_status="UNAVAILABLE" if sidecar_unavailable else "COMPLETED",
            notes=[
                "No runtime block is introduced.",
                "Negative capture evidence is preserved when unavailable.",
            ],
        ),
        _event(
            4,
            "DOWNSTREAM_INGEST",
            "DOWNSTREAM-001",
            claim_bundle,
            policy,
            nonclaims,
            notes=["Receipt does not import upstream authority or standing."],
        ),
        _event(
            5,
            "DOWNSTREAM_LOCAL_DISPOSITION",
            "DOWNSTREAM-001",
            claim_bundle,
            policy,
            nonclaims,
            authority_action="LOCAL_ONLY",
            authority_source="PREEXISTING_LOCAL_GOVERNANCE",
            standing_action="LOCAL_REASSESSMENT",
            standing_basis=(
                "NARROWED_TO_DOWNSTREAM_DECLARED_SCOPE"
                if narrowed
                else "REASSESSMENT_WITHIN_DOWNSTREAM_DECLARED_SCOPE"
            ),
            claim_delta=(
                [
                    {
                        "operation": "NARROW",
                        "claim_id": "GHCH-CLM-001",
                        "basis": "Downstream scope excludes unobserved source-system state.",
                    }
                ]
                if narrowed
                else []
            ),
        ),
        _event(
            6,
            "FORK_CAPTURE_EGRESS",
            "FORK-001",
            claim_bundle,
            policy,
            nonclaims,
            observed_status="UNAVAILABLE" if sidecar_unavailable else "COMPLETED",
            notes=["Fork records the downstream declaration without approving it."],
        ),
        _event(
            7,
            "UPSTREAM_RECONCILE",
            "UPSTREAM-001",
            claim_bundle,
            policy,
            nonclaims,
            notes=[
                "Acknowledgment is not endorsement and does not bind downstream local authority."
            ],
        ),
        _event(
            8,
            "CADENCE_CLOSE",
            "HARNESS-001",
            claim_bundle,
            policy,
            nonclaims,
            observed_status=(
                "COMPLETED_WITH_OBSERVATION_GAPS"
                if sidecar_unavailable
                else "COMPLETED"
            ),
            notes=["Closure is a simulation record, not an authority or admission act."],
        ),
    ]
    events = recompute_chain(events)

    record = {
        "schema_version": "0.1",
        "artifact_type": "GHCH_CADENCE_RECORD",
        "cadence_id": {
            "CLEAN_ROUND_TRIP": "GHCH-CAD-001",
            "PERMISSIBLE_NARROWING": "GHCH-CAD-002",
            "SIDECAR_UNAVAILABLE_FAIL_OPEN": "GHCH-CAD-003",
        }[profile],
        "profile": profile,
        "canonicalization_profile": CANONICAL_PROFILE,
        "participants": participants(),
        "claim_bundle": claim_bundle,
        "exchange_policy": policy,
        "non_claim_set": nonclaims,
        "events": events,
        "reconciliation": {
            "relationship": "NARROWED" if narrowed else "PRESERVED",
            "downstream_local_disposition": (
                "ACCEPTED_WITH_NARROWING" if narrowed else "ACCEPTED_FOR_LOCAL_PROCESSING"
            ),
            "upstream_acknowledgment": "ACKNOWLEDGED_WITHOUT_ENDORSEMENT",
            "unresolved_items": (
                ["FORK_INGRESS_CAPTURE_UNAVAILABLE", "FORK_EGRESS_CAPTURE_UNAVAILABLE"]
                if sidecar_unavailable
                else []
            ),
        },
        "declared_non_effects": {
            "authority_transfer": "NONE",
            "standing_inheritance": "NONE",
            "endorsement_inheritance": "NONE",
            "production_or_compliance_effect": "NONE",
            "provider_calls": 0,
            "pair_001_calls": 0,
        },
    }
    return add_record_integrity(record)

def refresh_record(record: Dict[str, Any]) -> Dict[str, Any]:
    record = copy.deepcopy(record)
    record["claim_bundle"]["canonical_sha256"] = sha256_value(
        {k: v for k, v in record["claim_bundle"].items() if k != "canonical_sha256"}
    )
    record["exchange_policy"]["canonical_sha256"] = sha256_value(
        {k: v for k, v in record["exchange_policy"].items() if k != "canonical_sha256"}
    )
    record["non_claim_set"]["canonical_sha256"] = sha256_value(
        {k: v for k, v in record["non_claim_set"].items() if k != "canonical_sha256"}
    )
    for event in record["events"]:
        event["claim_bundle_ref"]["sha256"] = record["claim_bundle"]["canonical_sha256"]
        event["exchange_policy_ref"]["sha256"] = record["exchange_policy"]["canonical_sha256"]
        event["non_claim_set_ref"]["sha256"] = record["non_claim_set"]["canonical_sha256"]
    record["events"] = recompute_chain(record["events"])
    return add_record_integrity(record)

def pretty_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
