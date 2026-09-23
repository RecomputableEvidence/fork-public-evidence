#!/usr/bin/env python3
"""Validate the CSH-S001 execution-attempt schema and terminal-state boundary fixtures."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA=Path("schemas/csh_s001_execution_attempt_v0_1.schema.json")
SHA="0"*64


def root(start:Path)->Path:
    cur=start.resolve()
    for candidate in (cur,*cur.parents):
        if (candidate/".git").exists() and (candidate/"README.md").exists(): return candidate
    raise RuntimeError("repository root not found")


def base_record()->dict:
    return {
      "experiment_id":"CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1",
      "planned_run_id":"CSH-S001-RUN-001",
      "attempt_id":"CSH-S001-RUN-001-A01",
      "pairing_key":"SIM_A_BOUNDARY_PRESERVED|hosted_receiver_a|r1",
      "scenario_id":"SIM_A_BOUNDARY_PRESERVED",
      "receiver_class_id":"hosted_receiver_a",
      "condition":"control_h0",
      "replicate_id":1,
      "terminal_state":"COMPLETED_CLASSIFIABLE",
      "classifiable":True,
      "request_binding":{"path":"receipts/request.json","sha256":SHA},
      "raw_response_binding":{"path":"receipts/raw-response.json","sha256":SHA},
      "error_body_binding":None,
      "requested_model":"candidate-model",
      "returned_model":"candidate-model",
      "provider_response_id":"response-1",
      "backend_fingerprint":None,
      "finish_reason":"stop",
      "http_status":200,
      "started_at_utc":"2026-09-23T03:00:00Z",
      "ended_at_utc":"2026-09-23T03:00:01Z",
      "non_claims":["Fixture validates record shape only."]
    }


def validate(v,record): return list(v.iter_errors(record))


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path.cwd()); p.add_argument("--json",action="store_true",dest="as_json")
    a=p.parse_args(); r=root(a.root); schema=json.loads((r/SCHEMA).read_text(encoding="utf-8")); Draft202012Validator.check_schema(schema); v=Draft202012Validator(schema)
    checks=[]
    good=base_record(); checks.append({"name":"completed_classifiable_valid","passed":not validate(v,good)})
    unavailable=base_record(); unavailable.update({"terminal_state":"EXECUTION_UNAVAILABLE","classifiable":False,"raw_response_binding":None,"returned_model":None,"provider_response_id":None,"finish_reason":None,"http_status":None})
    checks.append({"name":"execution_unavailable_valid","passed":not validate(v,unavailable)})
    bad=base_record(); bad.update({"terminal_state":"EXECUTION_UNAVAILABLE","classifiable":True,"raw_response_binding":None})
    checks.append({"name":"noncompleted_cannot_be_classifiable","passed":bool(validate(v,bad))})
    missing=base_record(); missing["raw_response_binding"]=None
    checks.append({"name":"classifiable_requires_raw_response","passed":bool(validate(v,missing))})
    failed=[c for c in checks if not c["passed"]]
    out={"checker":Path(__file__).name,"schema":SCHEMA.as_posix(),"checks":checks,"passed":len(checks)-len(failed),"failed":len(failed),
         "interpretation":{"proves":["schema is Draft 2020-12 valid","completed/classifiable and noncompleted/nonclassifiable boundaries are mechanically enforced by fixtures"],
                           "does_not_prove":["provider availability","semantic correctness","the CSH hypothesis","truth","compliance","authorization"]}}
    if a.as_json: print(json.dumps(out,indent=2,sort_keys=True))
    else:
        for c in checks: print(f"[{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
    return 1 if failed else 0

if __name__=="__main__": raise SystemExit(main())
