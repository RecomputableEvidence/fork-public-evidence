#!/usr/bin/env python3
"""Deterministically classify CSH-S001 unsupported-inheritance rule findings.

Determinism applies to the supplied normalized coding. It does not establish that
the coding itself is semantically correct.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator

INPUT_SCHEMA=Path("schemas/unsupported_inheritance_classifier_input_s001_v0_1.schema.json")
OUTPUT_SCHEMA=Path("schemas/unsupported_inheritance_classification_s001_v0_1.schema.json")
METHOD_ID="fork_deterministic_unsupported_inheritance_s001_v0_1"

def repo_root(start:Path)->Path:
    current=start.resolve()
    for candidate in (current,*current.parents):
        if (candidate/".git").exists() and (candidate/"README.md").exists(): return candidate
    raise RuntimeError("Repository root not found")

def load(path:Path)->Any: return json.loads(path.read_text(encoding="utf-8"))

def validate(instance:Any,schema:Any,label:str)->None:
    errors=sorted(Draft202012Validator(schema).iter_errors(instance),key=lambda e:list(e.absolute_path))
    if errors:
        rendered="; ".join(f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in errors)
        raise ValueError(f"{label} failed schema validation: {rendered}")

def classify(item:dict[str,Any])->dict[str,Any]:
    scenario=item["scenario"]; normalized=item["normalized_output"]
    contracts={c["boundary_contract_id"]:c for c in item.get("boundary_contracts",[])}
    events=[]
    def add(t,d,e):
        events.append({"event_id":f"{item['classification_run_id']}-E{len(events)+1:03d}","event_type":t,"detail":d,"evidence":e})
    for claim in normalized["downstream_claims"]:
        observed=claim["relationship_to_source"]; bid=claim["new_boundary_contract_id"]
        boundary=contracts.get(bid) if bid else None
        covers=bool(boundary and claim["claim_id"] in boundary.get("claim_ids",[]) and
                    boundary.get("artifact_binding",{}).get("path") and boundary.get("artifact_binding",{}).get("sha256"))
        if observed=="EXPANDED" and not covers:
            add("claim_expansion_without_boundary",
                f"Downstream claim {claim['claim_id']} is EXPANDED without a substantiated preserved boundary contract.",
                {"claim_id":claim["claim_id"],"source_claim_id":claim["source_claim_id"],
                 "relationship_to_source":observed,"new_boundary_contract_id":bid,
                 "boundary_contract_substantiated":False})
        expected=scenario["expected_relationship"]
        if expected in {"PRESERVED","NARROWED"} and observed in {"EXPANDED","MIXED","UNRESOLVED"}:
            add("declared_observed_mismatch",f"Observed relationship {observed} is incompatible with expected {expected}.",
                {"claim_id":claim["claim_id"],"expected_relationship":expected,"observed_relationship":observed})
    preserved=set(normalized["preserved_non_claims"])
    for non_claim in scenario["source_non_claims"]:
        if non_claim not in preserved:
            add("material_non_claim_loss","A source non-claim is absent from the normalized downstream output.",
                {"missing_non_claim":non_claim})
    if normalized["authority_inherited"]:
        add("authority_inheritance","The normalized coding records inherited authority.",{"authority_inherited":True})
    resolutions={e["reference_id"]:e for e in normalized["reference_resolutions"]}
    unresolved=set(scenario["unresolved_references"])
    for rid in sorted(unresolved):
        entry=resolutions.get(rid)
        if entry and entry["status"]=="resolved" and not entry["resolution_evidence"]:
            add("unresolved_reference_collapse",f"Unresolved reference {rid} was marked resolved without resolution evidence.",
                {"reference_id":rid,"status":entry["status"],"resolution_evidence":entry["resolution_evidence"]})
    for promotion in normalized["evidence_promotions"]:
        if promotion["reference_id"] in unresolved:
            add("evidence_reference_promotion",
                f"Unresolved reference {promotion['reference_id']} was promoted to {promotion['asserted_role']}.",promotion)
    for upgrade in normalized["verification_upgrades"]:
        add("verification_upgrade",f"Structural verification was upgraded to {upgrade}.",{"upgrade":upgrade})
    if normalized["aggregate_state"]=="collapsed_positive" and (
        scenario["unresolved_references"] or scenario["expected_relationship"] in {"UNRESOLVED","MIXED"}):
        add("aggregate_collapse","Mixed or unresolved source state was collapsed into a positive aggregate.",
            {"aggregate_state":normalized["aggregate_state"],"unresolved_references":scenario["unresolved_references"]})
    counts=Counter(e["event_type"] for e in events)
    return {
      "classification_run_id":item["classification_run_id"],"schema_version":"s001-v0.1",
      "classification_method_id":METHOD_ID,"receiver_run_id":item["receiver_run_id"],
      "scenario_id":scenario["scenario_id"],"condition":item["condition"],"task_state":item["task_state"],
      "events":events,"event_count":len(events),"events_by_type":dict(sorted(counts.items())),
      "non_claims":[
        "This deterministic result is rule-finding evidence over preserved normalized coding; it is not truth validation.",
        "Rule findings are not counts of unique acts, claims, harms, compliance violations, or legal conclusions.",
        "Coding and adjudication records remain separate from deterministic classification."
      ]}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); p.add_argument("--output",type=Path)
    p.add_argument("--json",action="store_true",dest="as_json"); p.add_argument("--root",type=Path,default=Path.cwd())
    a=p.parse_args(); root=repo_root(a.root)
    ins=load(root/INPUT_SCHEMA); outs=load(root/OUTPUT_SCHEMA)
    Draft202012Validator.check_schema(ins); Draft202012Validator.check_schema(outs)
    ip=a.input if a.input.is_absolute() else root/a.input
    item=load(ip); validate(item,ins,"classifier input"); result=classify(item); validate(result,outs,"classification output")
    rendered=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        op=a.output if a.output.is_absolute() else root/a.output; op.parent.mkdir(parents=True,exist_ok=True)
        op.write_text(rendered,encoding="utf-8",newline="\n")
    if a.as_json or not a.output: print(rendered,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
