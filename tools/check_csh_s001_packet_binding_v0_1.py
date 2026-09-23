#!/usr/bin/env python3
"""Verify regenerated CSH-S001 candidate packet bytes against the preserved packet binding."""
from __future__ import annotations
import argparse, json
from pathlib import Path

BINDING=Path("docs/experiments/cross-system-claim-handoff-successor-001-v0.1/PACKET_BINDING_v0_1.json")


def repo_root(start:Path)->Path:
    cur=start.resolve()
    for candidate in (cur,*cur.parents):
        if (candidate/".git").exists() and (candidate/"README.md").exists(): return candidate
    raise RuntimeError("repository root not found")


def load(path:Path): return json.loads(path.read_text(encoding="utf-8"))


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("materialized_dir",type=Path); p.add_argument("--root",type=Path,default=Path.cwd()); p.add_argument("--json",action="store_true",dest="as_json")
    a=p.parse_args(); root=repo_root(a.root); binding=load(root/BINDING); manifest=load(a.materialized_dir/"PACKET_MATERIALIZATION_MANIFEST_v0_1.json")
    expected={r["scenario_id"]:r for r in binding["records"]}; observed={r["scenario_id"]:r for r in manifest["records"]}
    checks=[]
    checks.append({"name":"scenario_population","passed":set(expected)==set(observed),"detail":f"expected={len(expected)} observed={len(observed)}"})
    for sid in sorted(set(expected)|set(observed)):
        if sid not in expected or sid not in observed: continue
        e,o=expected[sid],observed[sid]
        for name,obs_key,exp_key in (("projection","projection","projection_sha256"),("control_packet","control_packet","control_packet_sha256"),("instrumented_packet","instrumented_packet","instrumented_packet_sha256")):
            actual=o[obs_key]["sha256"]; wanted=e[exp_key]
            checks.append({"name":f"{sid}:{name}","passed":actual==wanted,"detail":f"expected={wanted} observed={actual}"})
    failed=[c for c in checks if not c["passed"]]
    result={"checker":Path(__file__).name,"binding":BINDING.as_posix(),"materialization_manifest":str(a.materialized_dir/"PACKET_MATERIALIZATION_MANIFEST_v0_1.json"),
            "checks":checks,"passed":len(checks)-len(failed),"failed":len(failed),
            "interpretation":{"proves":["current deterministic materialization reproduces the hash-bound candidate projection/control/instrumented packet bytes"],
                              "does_not_prove":["that these bytes were delivered to a receiver","provider availability","semantic correctness","the CSH hypothesis"]}}
    if a.as_json: print(json.dumps(result,indent=2,sort_keys=True))
    else:
        for c in checks: print(f"[{'PASS' if c['passed'] else 'FAIL'}] {c['name']}: {c['detail']}")
    return 1 if failed else 0

if __name__=="__main__": raise SystemExit(main())
