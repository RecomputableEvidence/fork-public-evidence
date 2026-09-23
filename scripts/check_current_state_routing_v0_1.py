#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

ROUTING=Path("docs/state/CURRENT_STATE_ROUTING_v0_1.json")
README=Path("README.md")
CURRENT_STANDING=Path("CURRENT_STANDING.md")
CURRENT_DIR_README=Path("docs/current-standing/README.md")
PROOF_STATE=Path("docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json")
VERSIONS=(5,6,7)

def repo_root(start:Path)->Path:
    current=start.resolve()
    for candidate in (current,*current.parents):
        if (candidate/".git").exists() and (candidate/"README.md").exists():
            return candidate
    raise RuntimeError("Repository root not found")

def load(path:Path)->Any:
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def evaluate(root:Path)->dict[str,Any]:
    checks=[]
    def record(name,passed,detail): checks.append({"name":name,"passed":passed,"detail":detail})
    if not (root/ROUTING).is_file():
        record("routing_record_present",False,ROUTING.as_posix()); return finish(checks)
    routing=load(root/ROUTING); record("routing_record_present",True,ROUTING.as_posix())
    info=routing.get("current_program_standing",{})
    current_path=root/str(info.get("path",""))
    if not current_path.is_file():
        record("current_source_present",False,str(info.get("path"))); return finish(checks)
    current=load(current_path)
    record("current_source_identity",
        current.get("schema_id")==info.get("schema_id") and current.get("snapshot_date")==info.get("snapshot_date"),
        f"{current.get('schema_id')} @ {current.get('snapshot_date')}")
    csh=next((x for x in current.get("delta_objects",[]) if x.get("id")==info.get("csh_object_id")),None)
    record("current_csh_object_present",csh is not None,str(info.get("csh_object_id")))
    if csh:
        ok=(csh.get("research_state")==info.get("expected_research_state")
            and csh.get("gate")==info.get("expected_gate")
            and csh.get("continue_frozen_baseline")==info.get("expected_continue_frozen_baseline"))
        record("current_csh_shared_fields",ok,
               f"research_state={csh.get('research_state')} gate={csh.get('gate')} continue_frozen_baseline={csh.get('continue_frozen_baseline')}")
    chain=[]
    for version in VERSIONS:
        path=root/f"docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_{version}.json"
        predecessor=root/f"docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_{version-1}.json"
        try:
            item=load(path); expected=predecessor.relative_to(root).as_posix()
            if item.get("record_form")!="PREDECESSOR_PLUS_DELTA": chain.append(f"v0.{version}: record_form")
            if item.get("predecessor_register")!=expected: chain.append(f"v0.{version}: predecessor pointer")
            binding=item.get("predecessor_binding",{})
            if binding.get("path")!=expected: chain.append(f"v0.{version}: predecessor binding path")
            expected_sha=binding.get("sha256")
            if expected_sha and sha256(predecessor)!=expected_sha: chain.append(f"v0.{version}: predecessor sha256")
        except Exception as exc: chain.append(f"v0.{version}: {exc}")
    record("successor_chain_v0_5_through_v0_7",not chain,"bindings verified" if not chain else "; ".join(chain))
    readme=(root/README).read_text(encoding="utf-8")
    record("root_readme_routes_to_current_standing","[`CURRENT_STANDING.md`](CURRENT_STANDING.md)" in readme,
           "README routes reviewers to CURRENT_STANDING.md")
    cs=(root/CURRENT_STANDING).read_text(encoding="utf-8")
    record("current_standing_routes_v0_7","FORK_CURRENT_WORK_REGISTER_v0_7.json" in cs and "CSH baseline blocked" in cs,
           "CURRENT_STANDING.md routes v0.7 and blocked CSH")
    record("current_standing_qualifies_historical_snapshots",
           "Earlier proof-surface state files, generated summaries, and embedded README status blocks retain their own historical coordinates." in cs,
           "historical embedded status is explicitly subordinated to current route")
    record("current_standing_declares_s001_candidate",
           "CSH-S001-v0.1" in cs and "not frozen or executed" in cs,
           "CSH-S001 candidate is explicitly non-executed")
    dr=(root/CURRENT_DIR_README).read_text(encoding="utf-8")
    record("current_directory_routes_v0_7","Current successor overlay:** v0.7" in dr and "CSH baseline blocked" in dr,
           "docs/current-standing/README.md routes v0.7")
    proof=load(root/PROOF_STATE)
    hist=next((x for x in routing.get("historical_snapshots",[]) if x.get("path")==PROOF_STATE.as_posix()),None)
    record("proof_state_explicitly_historical",hist is not None and hist.get("historical_coordinate")==proof.get("as_of_date"),
           f"proof-state as_of={proof.get('as_of_date')}")
    return finish(checks)

def finish(checks):
    failed=[x for x in checks if not x["passed"]]
    return {"checker":Path(__file__).name,"total":len(checks),"passed":len(checks)-len(failed),"failed":len(failed),
            "checks":checks,
            "interpretation":{"proves":[
                "declared current program-standing source and selected current-facing routes agree on shared CSH state",
                "v0.5-v0.7 successor bindings preserve predecessor bytes",
                "the July proof-state record is explicitly routed as a dated historical snapshot"],
                "does_not_prove":["the CSH hypothesis","truth","compliance","legal sufficiency","authorization","production readiness","institutional authority"]}}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path.cwd()); p.add_argument("--json",action="store_true",dest="as_json")
    a=p.parse_args(); result=evaluate(repo_root(a.root))
    if a.as_json: print(json.dumps(result,indent=2,sort_keys=True))
    else:
        for item in result["checks"]: print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print("CURRENT_STATE_ROUTING_PASS" if result["failed"]==0 else "CURRENT_STATE_ROUTING_FAIL")
    return 1 if result["failed"] else 0
if __name__=="__main__": raise SystemExit(main())
