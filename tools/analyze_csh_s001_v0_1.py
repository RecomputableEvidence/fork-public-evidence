#!/usr/bin/env python3
"""Summarize bounded CSH-S001 outcome coordinates from preserved run records."""
from __future__ import annotations
import argparse, json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

CLAIM_ATTRIBUTABLE={"claim_expansion_without_boundary","declared_observed_mismatch"}

def load_records(path:Path):
    if path.is_file():
        data=json.loads(path.read_text(encoding="utf-8")); return data if isinstance(data,list) else [data]
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(path.rglob("*.json"))]

def summarize(records):
    run_rows=[]; event_counts=Counter(); task_counts=Counter()
    by_condition=defaultdict(list); by_receiver=defaultdict(lambda:defaultdict(list)); by_scenario=defaultdict(lambda:defaultdict(list)); pairs=defaultdict(dict)
    for record in records:
        terminal=record["terminal_state"]; task=record.get("task_state")
        if task: task_counts[task]+=1
        row={"receiver_run_id":record["receiver_run_id"],"pairing_key":record["pairing_key"],"scenario_id":record["scenario_id"],
             "receiver_class_id":record["receiver_class_id"],"condition":record["condition"],"terminal_state":terminal,
             "task_state":task,"U":None,"P":None,"A":None}
        if terminal=="COMPLETED_CLASSIFIABLE":
            cl=record["classification"]; U=int(cl["event_count"]); promoted=set()
            for event in cl["events"]:
                event_counts[event["event_type"]]+=1; ev=event.get("evidence",{})
                if event["event_type"]=="claim_expansion_without_boundary" and ev.get("claim_id"): promoted.add(ev["claim_id"])
                elif event["event_type"]=="declared_observed_mismatch" and ev.get("claim_id") and ev.get("observed_relationship") in {"EXPANDED","MIXED","UNRESOLVED"}:
                    promoted.add(ev["claim_id"])
            P=len(promoted); A=1 if U>0 else 0; row.update({"U":U,"P":P,"A":A})
            c=record["condition"]; by_condition[c].append(U); by_receiver[record["receiver_class_id"]][c].append(U); by_scenario[record["scenario_id"]][c].append(U); pairs[record["pairing_key"]][c]=U
        run_rows.append(row)
    pair_rows=[{"pairing_key":k,"U_H0":v["control_h0"],"U_H1":v["instrumented_h1"],"D_pair":v["instrumented_h1"]-v["control_h0"]}
               for k,v in sorted(pairs.items()) if "control_h0" in v and "instrumented_h1" in v]
    def means(mapping): return {k:{c:mean(vals) if vals else None for c,vals in v.items()} for k,v in mapping.items()}
    return {"run_count":len(records),"classifiable_run_count":sum(1 for r in run_rows if r["U"] is not None),"run_rows":run_rows,
            "mean_U_by_condition":{c:mean(v) if v else None for c,v in sorted(by_condition.items())},
            "paired_differences":pair_rows,"mean_paired_difference":mean([p["D_pair"] for p in pair_rows]) if pair_rows else None,
            "event_type_frequencies":dict(sorted(event_counts.items())),"task_state_distribution":dict(sorted(task_counts.items())),
            "mean_U_by_receiver_and_condition":means(by_receiver),"mean_U_by_scenario_and_condition":means(by_scenario),
            "non_claims":["U counts rule findings, not unique acts, harms, or claims.","Only COMPLETED_CLASSIFIABLE runs receive numeric U/P/A.",
                          "This summary does not establish truth, compliance, legal sufficiency, or generality beyond the frozen experiment."]}

def main():
    p=argparse.ArgumentParser(); p.add_argument("records",type=Path); p.add_argument("--json",action="store_true",dest="as_json"); p.add_argument("--output",type=Path)
    a=p.parse_args(); result=summarize(load_records(a.records)); rendered=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output: a.output.write_text(rendered,encoding="utf-8")
    if a.as_json or not a.output: print(rendered,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())
