#!/usr/bin/env python3
"""Immutable GHCH v0.1 protocol vocabulary and structural contracts."""

from __future__ import annotations

from ghch_common_v0_1 import CANONICAL_PROFILE

ALLOWED_PROFILES = {
    "CLEAN_ROUND_TRIP",
    "PERMISSIBLE_NARROWING",
    "SIDECAR_UNAVAILABLE_FAIL_OPEN",
}

PROFILE_CADENCE_IDS = {
    "CLEAN_ROUND_TRIP": "GHCH-CAD-001",
    "PERMISSIBLE_NARROWING": "GHCH-CAD-002",
    "SIDECAR_UNAVAILABLE_FAIL_OPEN": "GHCH-CAD-003",
}

TOP_LEVEL_KEYS = {
    "schema_version",
    "artifact_type",
    "cadence_id",
    "profile",
    "canonicalization_profile",
    "participants",
    "claim_bundle",
    "exchange_policy",
    "non_claim_set",
    "events",
    "reconciliation",
    "declared_non_effects",
    "record_integrity",
}
PARTICIPANT_KEYS = {"participant_id", "role", "authority_domain"}
CLAIM_BUNDLE_KEYS = {
    "bundle_id",
    "claims",
    "canonicalization_profile",
    "canonical_sha256",
}
CLAIM_KEYS = {"claim_id", "statement", "standing", "scope", "evidence_refs"}
EVIDENCE_REF_KEYS = {"artifact_id", "sha256"}
POLICY_KEYS = {
    "policy_id",
    "authority_transfer_permitted",
    "authority_inheritance_permitted",
    "standing_inheritance_permitted",
    "endorsement_inheritance_permitted",
    "evidence_reference_promotion_permitted",
    "unresolved_resolution_by_assumption_permitted",
    "fork_mode",
    "canonicalization_profile",
    "canonical_sha256",
}
NON_CLAIM_KEYS = {
    "non_claim_set_id",
    "non_claims",
    "canonicalization_profile",
    "canonical_sha256",
}
EVENT_KEYS = {
    "event_id",
    "stage",
    "actor_id",
    "predecessor_ref",
    "claim_bundle_ref",
    "exchange_policy_ref",
    "non_claim_set_ref",
    "claim_delta",
    "local_effects",
    "observed_status",
    "detected_flags",
    "notes",
    "event_integrity",
}
PREDECESSOR_KEYS = {"event_id", "sha256"}
CLAIM_REF_KEYS = {"bundle_id", "sha256"}
POLICY_REF_KEYS = {"policy_id", "sha256"}
NON_CLAIM_REF_KEYS = {"non_claim_set_id", "sha256"}
DELTA_KEYS = {"operation", "claim_id", "basis"}
LOCAL_EFFECT_KEYS = {
    "authority_action",
    "authority_source",
    "standing_action",
    "standing_basis",
}
EVENT_INTEGRITY_KEYS = {"canonicalization_profile", "canonical_event_sha256"}
RECORD_INTEGRITY_KEYS = {"canonicalization_profile", "canonical_record_sha256"}
RECONCILIATION_KEYS = {
    "relationship",
    "downstream_local_disposition",
    "upstream_acknowledgment",
    "unresolved_items",
}
NON_EFFECT_KEYS = {
    "authority_transfer",
    "standing_inheritance",
    "endorsement_inheritance",
    "production_or_compliance_effect",
    "provider_calls",
    "pair_001_calls",
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

EXPECTED_PARTICIPANTS = {
    "HARNESS-001": ("SIMULATION_HARNESS", "NONE"),
    "UPSTREAM-001": ("UPSTREAM_GOVERNANCE", "UPSTREAM_LOCAL_ONLY"),
    "FORK-001": ("FORK_EVIDENCE_SIDECAR", "NONE"),
    "DOWNSTREAM-001": ("DOWNSTREAM_GOVERNANCE", "DOWNSTREAM_LOCAL_ONLY"),
}

EXPECTED_CLAIMS = [
    {
        "claim_id": "GHCH-CLM-001",
        "statement": "A bounded enterprise AI workflow event occurred under the declared source scope.",
        "standing": "ASSERTED",
        "scope": "SIMULATED_ENTERPRISE_WORKFLOW_ONLY",
        "evidence_refs": [{"artifact_id": "SIM-SOURCE-001", "sha256": "1" * 64}],
    },
    {
        "claim_id": "GHCH-CLM-002",
        "statement": "Fork observed or failed to observe the declared handoff stages as recorded.",
        "standing": "OBSERVATION_CANDIDATE",
        "scope": "SIDECAR_CAPTURE_SURFACE_ONLY",
        "evidence_refs": [],
    },
]

EXPECTED_POLICY_BODY = {
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

EXPECTED_NOTES = {
    "PREREGISTER": ["Frozen simulated route, roles, policies, and expected stage order."],
    "UPSTREAM_EMIT": ["Upstream authorizes only release within its own declared governance domain."],
    "FORK_CAPTURE_INGRESS": [
        "No runtime block is introduced.",
        "Negative capture evidence is preserved when unavailable.",
    ],
    "DOWNSTREAM_INGEST": ["Receipt does not import upstream authority or standing."],
    "DOWNSTREAM_LOCAL_DISPOSITION": [],
    "FORK_CAPTURE_EGRESS": ["Fork records the downstream declaration without approving it."],
    "UPSTREAM_RECONCILE": [
        "Acknowledgment is not endorsement and does not bind downstream local authority."
    ],
    "CADENCE_CLOSE": ["Closure is a simulation record, not an authority or admission act."],
}

EXPECTED_NARROWING_DELTA = [
    {
        "operation": "NARROW",
        "claim_id": "GHCH-CLM-001",
        "basis": "Downstream scope excludes unobserved source-system state.",
    }
]

EXPECTED_NON_EFFECTS = {
    "authority_transfer": "NONE",
    "standing_inheritance": "NONE",
    "endorsement_inheritance": "NONE",
    "production_or_compliance_effect": "NONE",
    "provider_calls": 0,
    "pair_001_calls": 0,
}
