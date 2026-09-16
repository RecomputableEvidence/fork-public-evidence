#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
V1=ROOT/'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_1.json'
V2=ROOT/'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_2.json'
ADMISSION=ROOT/'admissions/FORK-VOS-001/E002'
HANDOFF=ADMISSION/'assessment-fulfillment-001/VOS-TC-E002-BOUNDED-HANDOFF-001.json'
STANDING=ADMISSION/'confirmatory-closeout-001/FORK-VOS-001-E002-STANDING-VECTOR-001.json'
EXPECTED={
 'GEOMETRY':'ESTABLISHED_FOR_DECLARED_PAIR',
 'LUMINANCE':'CONDITION_DEPENDENT_PARTIAL',
 'REFLECTION':'SPATIALLY_NONUNIFORM_AND_VANTAGE_DEPENDENT',
 'SPATIAL_FREQUENCY':'FREQUENCY_DEPENDENT_NOT_EQUIVALENT_TO_COARSE_FIDELITY',
 'MISSINGNESS':'NO_TILE_LOSS_OBSERVED_BUT_ABSENCE_SEPARATION_NOT_FULLY_CHALLENGED',
 'INDEPENDENCE':'NOT_ESTABLISHED'}
def fail(m): print('FAIL:',m); raise SystemExit(1)
def load(p):
 try:return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e:fail(f'{p.relative_to(ROOT)} invalid JSON: {e}')
def states(v): return {k:(x.get('state') if isinstance(x,dict) else x) for k,x in v.items()}
def main():
 v1,v2=load(V1),load(V2)
 objs=v1.get('objects',[])
 if len(objs)!=19: fail('predecessor object population drift')
 ids=[x.get('id') for x in objs]
 if len(ids)!=len(set(ids)): fail('duplicate predecessor object id')
 if v2.get('record_form')!='PREDECESSOR_PLUS_DELTA': fail('v0.2 is not predecessor-plus-delta')
 if v2.get('predecessor_object_count')!=len(objs): fail('predecessor count mismatch')
 d=v2.get('delta_objects',[])
 if len(d)!=1 or v2.get('delta_object_count')!=1: fail('unexpected delta population')
 e=d[0]
 if e.get('id') in ids: fail('delta silently rewrites predecessor object')
 if e.get('id')!='FORK_VOS_001_E002': fail('unexpected delta object')
 if e.get('admission_merge_commit')!='73228007910f0e4781005133e9a4e9484fd2969a': fail('admission merge coordinate drift')
 if e.get('admission_pr')!=145: fail('admission PR drift')
 if e.get('material_state')!='TERMINAL_NATIVE_RECORDS_ADMITTED__DEVELOPMENT_BINARY_AND_RAW_CAPTURE_BYTES_HASH_BOUND_NOT_ADMITTED': fail('material state promotion')
 if e.get('execution_state')!='CONFIRMATORY_EXECUTION_COMPLETE': fail('execution state drift')
 if e.get('current_disposition')!='CLOSED_WITH_BOUNDED_STANDING_VECTOR': fail('disposition drift')
 if e.get('assessment_state')!='CLOSEOUT_ACCEPTED_AS_BOUNDED_EXECUTION_RECORD': fail('assessment drift')
 if e.get('handoff_state')!='AUTHORIZED_BOUNDED_INPUT_ONLY': fail('handoff drift')
 if e.get('independence_state')!='NOT_ESTABLISHED': fail('independence promotion')
 if e.get('standing_vector')!=EXPECTED: fail('overlay standing vector drift')
 if not ADMISSION.is_dir(): fail('admission path missing')
 h=load(HANDOFF); s=load(STANDING)
 if h.get('handoff_state')!='AUTHORIZED_BOUNDED_INPUT_ONLY': fail('admitted handoff drift')
 if h.get('standing_vector')!=EXPECTED: fail('admitted handoff vector drift')
 if h.get('independent_raw_recomputation_completed_by_this_assessment') is not False: fail('independent recomputation promotion')
 if states(s.get('standing_vector',{}))!=EXPECTED: fail('admitted standing vector drift')
 print('PASS: v0.2 current-standing successor overlay preserves v0.1 and records bounded E002 admission')
 print('boundary: status overlay != stronger scientific standing; E002 admission != raw capture byte admission or independence')
 return 0
if __name__=='__main__':sys.exit(main())
