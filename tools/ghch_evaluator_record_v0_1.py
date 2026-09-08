#!/usr/bin/env python3
"""GHCH v0.1 top-level, participant, and canonical-object evaluation."""
from __future__ import annotations
from typing import Any, Dict, List, Set, Tuple
from ghch_common_v0_1 import CANONICAL_PROFILE, REQUIRED_NON_CLAIMS, sha256_value
from ghch_contract_v0_1 import *  # noqa: F403,F401

def digest_without(obj: Dict[str, Any], key: str) -> str:
    return sha256_value({k: v for k, v in obj.items() if k != key})

def exact_keys(value: Any, expected: Set[str], code: str, findings: List[str]) -> bool:
    if not isinstance(value, dict):
        findings.append(code + "_TYPE")
        return False
    if set(value) != expected:
        findings.append(code + "_KEYS")
        return False
    return True

def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)

def evaluate_record(record: Dict[str, Any], findings: List[str]) -> Dict[str, Any]:
    exact_keys(record, TOP_LEVEL_KEYS, "TOP_LEVEL", findings)
    if record.get("schema_version") != "0.1": findings.append("SCHEMA_VERSION")
    if record.get("artifact_type") != "GHCH_CADENCE_RECORD": findings.append("ARTIFACT_TYPE")
    if record.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("CANONICAL_PROFILE")
    profile = record.get("profile")
    if profile not in ALLOWED_PROFILES: findings.append("PROFILE")
    if record.get("cadence_id") != PROFILE_CADENCE_IDS.get(profile): findings.append("CADENCE_ID")
    integrity=record.get("record_integrity")
    if exact_keys(integrity, RECORD_INTEGRITY_KEYS, "RECORD_INTEGRITY", findings):
        if integrity.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("RECORD_CANONICAL_PROFILE")
        if integrity.get("canonical_record_sha256") != sha256_value({k:v for k,v in record.items() if k!="record_integrity"}): findings.append("RECORD_DIGEST")
    participants=record.get("participants")
    observed={}
    if isinstance(participants,list) and len(participants)==4:
        for item in participants:
            if not exact_keys(item, PARTICIPANT_KEYS, "PARTICIPANT", findings): continue
            pid=item.get("participant_id")
            if not nonempty_string(pid): findings.append("PARTICIPANT_ID"); continue
            if pid in observed: findings.append("DUPLICATE_PARTICIPANT")
            observed[pid]=(item.get("role"),item.get("authority_domain"))
    else: findings.append("PARTICIPANTS_TYPE_OR_COUNT")
    if observed != EXPECTED_PARTICIPANTS: findings.append("PARTICIPANTS")
    claim_bundle=record.get("claim_bundle"); policy=record.get("exchange_policy"); nonclaims=record.get("non_claim_set")
    if not exact_keys(claim_bundle, CLAIM_BUNDLE_KEYS, "CLAIM_BUNDLE", findings): claim_bundle=claim_bundle if isinstance(claim_bundle,dict) else {}
    if not exact_keys(policy, POLICY_KEYS, "EXCHANGE_POLICY", findings): policy=policy if isinstance(policy,dict) else {}
    if not exact_keys(nonclaims, NON_CLAIM_KEYS, "NON_CLAIM_SET", findings): nonclaims=nonclaims if isinstance(nonclaims,dict) else {}
    if claim_bundle.get("canonical_sha256") != digest_without(claim_bundle,"canonical_sha256"): findings.append("CLAIM_BUNDLE_DIGEST")
    if policy.get("canonical_sha256") != digest_without(policy,"canonical_sha256"): findings.append("POLICY_DIGEST")
    if nonclaims.get("canonical_sha256") != digest_without(nonclaims,"canonical_sha256"): findings.append("NON_CLAIM_DIGEST")
    claims=claim_bundle.get("claims")
    if claim_bundle.get("bundle_id") != "GHCH-CB-001": findings.append("CLAIM_BUNDLE_ID")
    if claim_bundle.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("CLAIM_BUNDLE_PROFILE")
    if not isinstance(claims,list): findings.append("CLAIMS_TYPE"); claims=[]
    else:
        for claim in claims:
            if not exact_keys(claim, CLAIM_KEYS, "CLAIM", findings): continue
            refs=claim.get("evidence_refs")
            if not isinstance(refs,list): findings.append("EVIDENCE_REFS_TYPE")
            else:
                for ref in refs:
                    if not exact_keys(ref,EVIDENCE_REF_KEYS,"EVIDENCE_REF",findings): continue
                    if not nonempty_string(ref.get("artifact_id")): findings.append("EVIDENCE_REF_ARTIFACT_ID")
                    if not isinstance(ref.get("sha256"),str) or len(ref["sha256"])!=64: findings.append("EVIDENCE_REF_SHA")
    if claims != EXPECTED_CLAIMS: findings.append("CLAIM_BUNDLE_SEMANTICS")
    if {k:policy.get(k) for k in EXPECTED_POLICY_BODY} != EXPECTED_POLICY_BODY: findings.append("POLICY_SEMANTICS")
    if policy.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("POLICY_PROFILE")
    if nonclaims.get("non_claim_set_id") != "GHCH-NC-001": findings.append("NON_CLAIM_SET_ID")
    if nonclaims.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("NON_CLAIM_PROFILE")
    if nonclaims.get("non_claims") != REQUIRED_NON_CLAIMS: findings.append("NON_CLAIM_GAP")
    events=record.get("events")
    if not isinstance(events,list): findings.append("EVENTS_TYPE"); events=[]
    elif len(events)!=8: findings.append("EVENT_COUNT")
    return {"profile":profile,"claim_bundle":claim_bundle,"policy":policy,"nonclaims":nonclaims,"events":events}
