#!/usr/bin/env python3
"""Build exact candidate CSH-S001 source/treatment packets from preserved v0.1 prompt artifacts."""
from __future__ import annotations
import argparse, copy, hashlib, json
from pathlib import Path

PRE=Path('docs/experiments/cross-system-claim-handoff-v0.1/prompts')
SCENARIOS=(
 'SIM_A_BOUNDARY_PRESERVED','SIM_B_BOUNDARY_NARROWED','SIM_C_NON_CLAIM_DROPPED',
 'SIM_D_EXPANSION_WITHOUT_AUTHORITY','SIM_F_POINTER_UNRESOLVED','SIM_H_CASCADING_INHERITANCE')
EXP='CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1'
METHOD='csh_s001_projection_from_predecessor_v0_1'

def sha256(path:Path)->str: return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path:Path): return json.loads(path.read_text(encoding='utf-8'))
def write_json(path:Path,obj):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

def build(root:Path,out:Path):
 records=[]
 for sid in SCENARIOS:
  cpath=root/PRE/f'PROMPT_PACKET_{sid}_control_h0_v0_1.json'
  ipath=root/PRE/f'PROMPT_PACKET_{sid}_instrumented_h1_v0_1.json'
  c=load(cpath); i=load(ipath)
  if c['source_artifact']!=i['source_artifact'] or c['workflow_task']!=i['workflow_task']:
   raise ValueError(f'{sid}: predecessor pair content mismatch')
  if c.get('handoff_state_artifact') is not None or not isinstance(i.get('handoff_state_artifact'),dict):
   raise ValueError(f'{sid}: predecessor treatment shape mismatch')
  projection=copy.deepcopy(i['handoff_state_artifact'])
  projection['handoff_id']=f'CSH-S001-HANDOFF-{sid}-v0.1'
  proj_path=out/'projections'/f'HANDOFF_{sid}_s001_v0_1.json'; write_json(proj_path,projection)
  common={
   'packet_type':'csh_s001_receiver_prompt_packet','schema_version':'s001-v0.1','experiment_id':EXP,
   'scenario_id':sid,'workflow_task':c['workflow_task'],'source_artifact':copy.deepcopy(c['source_artifact'])}
  control={**common,'handoff_state_artifact':None}
  instrumented={**common,'handoff_state_artifact':copy.deepcopy(projection)}
  cp=out/'packets'/f'PROMPT_PACKET_{sid}_control_h0_s001_v0_1.json'; write_json(cp,control)
  hp=out/'packets'/f'PROMPT_PACKET_{sid}_instrumented_h1_s001_v0_1.json'; write_json(hp,instrumented)
  records.append({
   'scenario_id':sid,
   'predecessor_control':{'path':cpath.relative_to(root).as_posix(),'sha256':sha256(cpath)},
   'predecessor_instrumented':{'path':ipath.relative_to(root).as_posix(),'sha256':sha256(ipath)},
   'projection_method_id':METHOD,
   'projection':{'path':proj_path.relative_to(out).as_posix(),'sha256':sha256(proj_path)},
   'control_packet':{'path':cp.relative_to(out).as_posix(),'sha256':sha256(cp)},
   'instrumented_packet':{'path':hp.relative_to(out).as_posix(),'sha256':sha256(hp)}
  })
 manifest={'experiment_id':EXP,'schema_version':'v0.1','status':'CANDIDATE_NOT_FROZEN',
           'projection_method_id':METHOD,'scenario_count':len(records),'records':records,
           'non_claims':['Candidate materialization does not authorize execution.','Later regeneration is not evidence of bytes delivered in an executed run; executed packet bytes must be preserved separately.']}
 write_json(out/'PACKET_MATERIALIZATION_MANIFEST_v0_1.json',manifest)
 return manifest

def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,default=Path.cwd()); p.add_argument('--output-dir',type=Path,required=True); p.add_argument('--json',action='store_true')
 a=p.parse_args(); m=build(a.root.resolve(),a.output_dir.resolve())
 if a.json: print(json.dumps(m,indent=2,sort_keys=True))
 return 0
if __name__=='__main__': raise SystemExit(main())
