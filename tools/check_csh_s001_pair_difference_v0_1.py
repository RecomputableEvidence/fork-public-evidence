#!/usr/bin/env python3
"""Verify CSH-S001 candidate pair packets differ only by exact handoff-state instrumentation."""
from __future__ import annotations
import argparse, json
from pathlib import Path
SCENARIOS=('SIM_A_BOUNDARY_PRESERVED','SIM_B_BOUNDARY_NARROWED','SIM_C_NON_CLAIM_DROPPED','SIM_D_EXPANSION_WITHOUT_AUTHORITY','SIM_F_POINTER_UNRESOLVED','SIM_H_CASCADING_INHERITANCE')

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def evaluate(base:Path):
 checks=[]
 for sid in SCENARIOS:
  cp=base/'packets'/f'PROMPT_PACKET_{sid}_control_h0_s001_v0_1.json'; hp=base/'packets'/f'PROMPT_PACKET_{sid}_instrumented_h1_s001_v0_1.json'; pp=base/'projections'/f'HANDOFF_{sid}_s001_v0_1.json'
  c=load(cp); h=load(hp); proj=load(pp)
  h_without=dict(h); h_without['handoff_state_artifact']=None
  passed=(c==h_without and h.get('handoff_state_artifact')==proj and c.get('handoff_state_artifact') is None)
  checks.append({'scenario_id':sid,'passed':passed,'detail':'only handoff_state_artifact differs' if passed else 'pair differs outside declared treatment field'})
 failed=[x for x in checks if not x['passed']]
 return {'checker':Path(__file__).name,'total':len(checks),'passed':len(checks)-len(failed),'failed':len(failed),'checks':checks,
         'interpretation':{'proves':['candidate H0/H1 JSON packet objects differ only by the handoff_state_artifact field and H1 embeds the exact preserved projection object'],
                           'does_not_prove':['provider request envelopes are identical','receiver behavior','the CSH hypothesis','truth','compliance']}}
def main():
 p=argparse.ArgumentParser(); p.add_argument('candidate_dir',type=Path); p.add_argument('--json',action='store_true'); a=p.parse_args(); r=evaluate(a.candidate_dir)
 print(json.dumps(r,indent=2,sort_keys=True) if a.json else '\n'.join(f"[{'PASS' if x['passed'] else 'FAIL'}] {x['scenario_id']}: {x['detail']}" for x in r['checks']))
 return 1 if r['failed'] else 0
if __name__=='__main__': raise SystemExit(main())
