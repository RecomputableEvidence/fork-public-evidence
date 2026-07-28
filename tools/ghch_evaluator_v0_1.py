#!/usr/bin/env python3
"""GHCH v0.1 semantic evaluation orchestration and reconciliation."""
from __future__ import annotations
from typing import Any, Dict, List, Tuple
from ghch_contract_v0_1 import *  # noqa: F403,F401
from ghch_evaluator_record_v0_1 import exact_keys, evaluate_record
from ghch_evaluator_events_v0_1 import evaluate_events

def evaluate(record: Dict[str,Any]) -> Tuple[str,List[str]]:
    findings: List[str]=[]
    ctx=evaluate_record(record,findings); profile=ctx["profile"]
    by_stage=evaluate_events(ctx,findings)
    disposition=by_stage.get("DOWNSTREAM_LOCAL_DISPOSITION",{})
    reconciliation=record.get("reconciliation"); exact_keys(reconciliation,RECONCILIATION_KEYS,"RECONCILIATION",findings); reconciliation=reconciliation if isinstance(reconciliation,dict) else {}
    unresolved=reconciliation.get("unresolved_items")
    if not isinstance(unresolved,list) or any(not isinstance(item,str) for item in unresolved): findings.append("UNRESOLVED_ITEMS_TYPE")
    if profile=="SIDECAR_UNAVAILABLE_FAIL_OPEN":
        if unresolved != ["FORK_INGRESS_CAPTURE_UNAVAILABLE","FORK_EGRESS_CAPTURE_UNAVAILABLE"]: findings.append("OBSERVATION_GAPS")
    elif unresolved != []: findings.append("UNEXPECTED_UNRESOLVED_ITEMS")
    delta=disposition.get("claim_delta",[]); relationship=reconciliation.get("relationship")
    if profile=="PERMISSIBLE_NARROWING":
        if relationship!="NARROWED": findings.append("NARROWING_RELATIONSHIP")
        if delta != EXPECTED_NARROWING_DELTA: findings.append("NARROWING_DELTA_SEMANTICS")
        if reconciliation.get("downstream_local_disposition")!="ACCEPTED_WITH_NARROWING": findings.append("NARROWING_DISPOSITION")
    elif profile in {"CLEAN_ROUND_TRIP","SIDECAR_UNAVAILABLE_FAIL_OPEN"}:
        if relationship!="PRESERVED": findings.append("PRESERVATION_RELATIONSHIP")
        if delta: findings.append("UNDECLARED_DELTA")
        if reconciliation.get("downstream_local_disposition")!="ACCEPTED_FOR_LOCAL_PROCESSING": findings.append("LOCAL_DISPOSITION")
    if reconciliation.get("upstream_acknowledgment")!="ACKNOWLEDGED_WITHOUT_ENDORSEMENT": findings.append("ACKNOWLEDGMENT_OVERREAD")
    non_effects=record.get("declared_non_effects"); exact_keys(non_effects,NON_EFFECT_KEYS,"DECLARED_NON_EFFECTS",findings)
    if non_effects != EXPECTED_NON_EFFECTS: findings.append("DECLARED_NON_EFFECT_VALUES")
    findings=list(dict.fromkeys(findings))
    if findings: return "GHCH_CADENCE_REJECTED",findings
    if profile=="PERMISSIBLE_NARROWING": return "GHCH_CADENCE_CONFORMS_WITH_PERMISSIBLE_NARROWING",[]
    if profile=="SIDECAR_UNAVAILABLE_FAIL_OPEN": return "GHCH_CADENCE_CONFORMS_WITH_OBSERVATION_GAPS",[]
    return "GHCH_CADENCE_CONFORMS_PRESERVED",[]
