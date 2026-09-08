#!/usr/bin/env python3
"""GHCH v0.1 event-chain evaluation."""
from __future__ import annotations
from typing import Any, Dict, List
from ghch_common_v0_1 import CANONICAL_PROFILE, EXPECTED_ACTORS, EXPECTED_STAGES
from ghch_contract_v0_1 import *  # noqa: F403,F401
from ghch_evaluator_record_v0_1 import digest_without, exact_keys, nonempty_string

def evaluate_events(ctx: Dict[str,Any], findings: List[str]) -> Dict[str,Dict[str,Any]]:
    profile=ctx["profile"]; claim_bundle=ctx["claim_bundle"]; policy=ctx["policy"]; nonclaims=ctx["nonclaims"]; events=ctx["events"]
    if [e.get("stage") for e in events if isinstance(e,dict)] != EXPECTED_STAGES: findings.append("STAGE_ORDER")
    ids=[e.get("event_id") for e in events if isinstance(e,dict)]
    if len(ids)!=len(set(ids)): findings.append("DUPLICATE_EVENT_ID")
    if ids != [f"GHCH-EVT-{i:03d}" for i in range(1,9)]: findings.append("EVENT_ID_SEQUENCE")
    statuses={stage:"COMPLETED" for stage in EXPECTED_STAGES}
    if profile=="SIDECAR_UNAVAILABLE_FAIL_OPEN":
        statuses["FORK_CAPTURE_INGRESS"]="UNAVAILABLE"; statuses["FORK_CAPTURE_EGRESS"]="UNAVAILABLE"; statuses["CADENCE_CLOSE"]="COMPLETED_WITH_OBSERVATION_GAPS"
    predecessor=None; claim_ids={item["claim_id"] for item in EXPECTED_CLAIMS}
    for index,event in enumerate(events):
        if not exact_keys(event,EVENT_KEYS,f"EVENT:{index}",findings) and not isinstance(event,dict): continue
        stage=event.get("stage")
        if event.get("actor_id") != EXPECTED_ACTORS.get(stage): findings.append("ACTOR:"+str(stage))
        pred=event.get("predecessor_ref")
        if pred is not None: exact_keys(pred,PREDECESSOR_KEYS,"PREDECESSOR_REF:"+str(stage),findings)
        if pred != predecessor: findings.append("LINEAGE:"+str(stage))
        integrity=event.get("event_integrity"); event_sha=None
        if exact_keys(integrity,EVENT_INTEGRITY_KEYS,"EVENT_INTEGRITY:"+str(stage),findings):
            event_sha=integrity.get("canonical_event_sha256")
            if integrity.get("canonicalization_profile") != CANONICAL_PROFILE: findings.append("EVENT_CANONICAL_PROFILE:"+str(stage))
            if event_sha != digest_without(event,"event_integrity"): findings.append("EVENT_DIGEST:"+str(stage))
        claim_ref=event.get("claim_bundle_ref"); policy_ref=event.get("exchange_policy_ref"); nonclaim_ref=event.get("non_claim_set_ref")
        exact_keys(claim_ref,CLAIM_REF_KEYS,"CLAIM_REF:"+str(stage),findings); exact_keys(policy_ref,POLICY_REF_KEYS,"POLICY_REF:"+str(stage),findings); exact_keys(nonclaim_ref,NON_CLAIM_REF_KEYS,"NON_CLAIM_REF:"+str(stage),findings)
        if claim_ref != {"bundle_id":claim_bundle.get("bundle_id"),"sha256":claim_bundle.get("canonical_sha256")}: findings.append("CLAIM_REF_VALUE:"+str(stage))
        if policy_ref != {"policy_id":policy.get("policy_id"),"sha256":policy.get("canonical_sha256")}: findings.append("POLICY_REF_VALUE:"+str(stage))
        if nonclaim_ref != {"non_claim_set_id":nonclaims.get("non_claim_set_id"),"sha256":nonclaims.get("canonical_sha256")}: findings.append("NON_CLAIM_REF_VALUE:"+str(stage))
        effects=event.get("local_effects"); exact_keys(effects,LOCAL_EFFECT_KEYS,"LOCAL_EFFECTS:"+str(stage),findings); effects=effects if isinstance(effects,dict) else {}
        expected=LOCAL_EFFECT_RULES.get(stage); observed=(effects.get("authority_action"),effects.get("authority_source"),effects.get("standing_action"))
        if expected is None: findings.append("UNKNOWN_STAGE:"+str(stage))
        elif observed != expected: findings.append("LOCAL_EFFECT_VALUES:"+str(stage))
        expected_basis=None
        if stage=="DOWNSTREAM_LOCAL_DISPOSITION": expected_basis="NARROWED_TO_DOWNSTREAM_DECLARED_SCOPE" if profile=="PERMISSIBLE_NARROWING" else "REASSESSMENT_WITHIN_DOWNSTREAM_DECLARED_SCOPE"
        if effects.get("standing_basis") != expected_basis: findings.append("STANDING_BASIS_SEMANTICS:"+str(stage))
        if event.get("observed_status") != statuses.get(stage): findings.append("EVENT_STATUS:"+str(stage))
        flags=event.get("detected_flags")
        if not exact_keys(flags,set(FLAG_CODES),"FLAGS:"+str(stage),findings): flags=flags if isinstance(flags,dict) else {}
        for key,code in FLAG_CODES.items():
            if flags.get(key) is True: findings.append(code+":"+str(stage))
            elif flags.get(key) is not False: findings.append("FLAG_VALUE:"+key+":"+str(stage))
        delta=event.get("claim_delta")
        if not isinstance(delta,list): findings.append("CLAIM_DELTA_TYPE:"+str(stage)); delta=[]
        if stage!="DOWNSTREAM_LOCAL_DISPOSITION" and delta: findings.append("DELTA_OUTSIDE_DISPOSITION:"+str(stage))
        for op in delta:
            if not exact_keys(op,DELTA_KEYS,"DELTA_ENTRY:"+str(stage),findings): continue
            if op.get("operation")!="NARROW": findings.append("UNPERMITTED_CLAIM_OPERATION:"+str(op.get("operation")))
            if op.get("claim_id") not in claim_ids: findings.append("UNKNOWN_CLAIM_DELTA")
            if not nonempty_string(op.get("basis")): findings.append("CLAIM_DELTA_BASIS")
        notes=event.get("notes")
        if not isinstance(notes,list) or any(not isinstance(note,str) for note in notes): findings.append("NOTES_TYPE:"+str(stage))
        elif notes != EXPECTED_NOTES.get(stage): findings.append("NOTES_SEMANTICS:"+str(stage))
        if event_sha is not None: predecessor={"event_id":event.get("event_id"),"sha256":event_sha}
    return {e.get("stage"):e for e in events if isinstance(e,dict)}
