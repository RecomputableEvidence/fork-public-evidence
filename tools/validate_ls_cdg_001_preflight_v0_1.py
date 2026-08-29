#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

EXPECTED_GRADES = {
    "C1":"CONFIRMED_MATERIAL_GAIN",
    "C2":"CONFIRMED_NONMATERIAL_EFFECT",
    "C3":"DUPLICATE_GAIN",
    "C4":"UNSUPPORTED_GAIN",
    "C5":"FALSE_ACTIVATION",
    "C6":"NOVEL_UNKEYED_CANDIDATE",
    "C7":"INSUFFICIENT_EVIDENCE",
}
REQUIRED_FINDING_FIELDS = {"local_finding_id","claim_challenged","event_ids","structural_problem","proposed_corrected_standing","confidence"}
EXPECTED_CAL_IDS = {"CAL-IDENTITY","CAL-HUMAN","CAL-AUTHORITY"}

def load_json_text(path: Path):
    text = path.read_text(encoding="utf-8").strip()
    if text.startswith("```"):
        raise ValueError("markdown fence prohibited")
    return json.loads(text)

def validate_budget(root: Path):
    results=[]
    selected=None
    for cap in (256,384,512):
        d=root/f"budget-{cap}"
        rec={"cap":cap,"pass":False}
        try:
            meta=json.loads((d/"metadata.json").read_text(encoding="utf-8"))
            value=load_json_text(d/"response_text.txt")
            findings=value.get("candidate_findings")
            if not isinstance(findings,list) or len(findings)!=3:
                raise ValueError("expected exactly three candidate_findings")
            ids=set()
            for item in findings:
                missing=REQUIRED_FINDING_FIELDS-set(item)
                if missing: raise ValueError(f"missing fields: {sorted(missing)}")
                ids.add(item["local_finding_id"])
                if not item["claim_challenged"].strip() or not item["event_ids"] or not item["structural_problem"].strip() or not item["proposed_corrected_standing"].strip():
                    raise ValueError("required semantic field empty")
                if item["confidence"] not in {"LOW","MEDIUM","HIGH"}: raise ValueError("bad confidence")
            if ids != EXPECTED_CAL_IDS: raise ValueError(f"unexpected calibration IDs: {sorted(ids)}")
            usage=meta.get("usage") or {}
            completion=usage.get("completion_tokens")
            rec.update({"pass":True,"completion_tokens":completion,"returned_model":meta.get("returned_model"),"execution_status":meta.get("execution_status")})
            if selected is None: selected=cap
        except Exception as exc:
            rec["error"]=str(exc)
        results.append(rec)
    return {"results":results,"selected_cap":selected,"pass":selected is not None}

def validate_graders(root: Path):
    results=[]
    for model in ("llama","deepseek"):
        d=root/f"grader-{model}"
        rec={"model":model,"pass":False}
        try:
            meta=json.loads((d/"metadata.json").read_text(encoding="utf-8"))
            value=load_json_text(d/"response_text.txt")
            got=value.get("classifications")
            if got != EXPECTED_GRADES:
                raise ValueError(f"classification mismatch: {got}")
            rec.update({"pass":True,"returned_model":meta.get("returned_model"),"execution_status":meta.get("execution_status"),"usage":meta.get("usage")})
        except Exception as exc:
            rec["error"]=str(exc)
        results.append(rec)
    return {"results":results,"pass":all(r["pass"] for r in results),"independence_class":"MODEL_FAMILY_INDEPENDENT" if all(r["pass"] for r in results) else "NOT_ESTABLISHED_INDEPENDENT"}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root",type=Path); args=ap.parse_args()
    budget=validate_budget(args.root); graders=validate_graders(args.root)
    out={
        "artifact_id":"LS-CDG-001-HOSTED-PREFLIGHT-RESULT-v0.1.1",
        "budget_calibration":budget,
        "grader_calibration":graders,
        "epoch0_generation_gate":"PASS" if budget["pass"] and graders["pass"] else "BLOCKED",
        "bound_treatment_runtime": "meta/Llama-4-Scout-17B-16E-Instruct" if budget["pass"] else None,
        "bound_graders": ["meta/Llama-4-Scout-17B-16E-Instruct","deepseek/DeepSeek-V3-0324"] if graders["pass"] else [],
    }
    (args.root/"preflight_result.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
    return 0 if out["epoch0_generation_gate"]=="PASS" else 2
if __name__=="__main__": raise SystemExit(main())
