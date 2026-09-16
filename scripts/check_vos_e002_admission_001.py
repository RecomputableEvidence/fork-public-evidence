#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'admissions'/'FORK-VOS-001'/'E002'
EXPECTED={"GEOMETRY":"ESTABLISHED_FOR_DECLARED_PAIR","LUMINANCE":"CONDITION_DEPENDENT_PARTIAL","REFLECTION":"SPATIALLY_NONUNIFORM_AND_VANTAGE_DEPENDENT","SPATIAL_FREQUENCY":"FREQUENCY_DEPENDENT_NOT_EQUIVALENT_TO_COARSE_FIDELITY","MISSINGNESS":"NO_TILE_LOSS_OBSERVED_BUT_ABSENCE_SEPARATION_NOT_FULLY_CHALLENGED","INDEPENDENCE":"NOT_ESTABLISHED"}
def fail(m): print('FAIL:',m); raise SystemExit(1)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:fail(f'{p.relative_to(ROOT)} invalid JSON: {e}')
def verify_sums(d):
    for ln in (d/'SHA256SUMS').read_text().splitlines():
        if not ln.strip():continue
        m=re.match(r'^([0-9a-f]{64})\s+(.+)$',ln.strip())
        if not m:fail(f'malformed checksum in {d}')
        h,n=m.groups(); p=d/n
        if p.is_file() and sha(p)!=h:fail(f'hash mismatch {p.relative_to(ROOT)}')
def states(v): return {k:x.get('state') if isinstance(x,dict) else x for k,x in v.items()}
def main():
    for d in [BASE/'confirmatory-closeout-001',BASE/'assessment-fulfillment-001']:
        if not d.is_dir():fail(f'missing {d.relative_to(ROOT)}')
        verify_sums(d)
    cand=load(BASE/'FORK-VOS-001-E002-REPOSITORY-ADMISSION-CANDIDATE-001.json')
    if cand.get('execution_state')!='CONFIRMATORY_EXECUTION_COMPLETE':fail('execution drift')
    if cand.get('source_disposition')!='CLOSED_WITH_BOUNDED_STANDING_VECTOR':fail('disposition drift')
    if cand.get('assessment')!='CLOSEOUT_ACCEPTED_AS_BOUNDED_EXECUTION_RECORD':fail('assessment drift')
    if cand.get('standing_vector')!=EXPECTED:fail('candidate standing vector drift')
    h=load(BASE/'assessment-fulfillment-001'/'VOS-TC-E002-BOUNDED-HANDOFF-001.json')
    if h.get('handoff_state')!='AUTHORIZED_BOUNDED_INPUT_ONLY':fail('handoff drift')
    if h.get('standing_vector')!=EXPECTED:fail('handoff vector drift')
    if h.get('independent_raw_recomputation_completed_by_this_assessment') is not False:fail('independence promotion')
    close=load(BASE/'confirmatory-closeout-001'/'FORK-VOS-001-E002-STANDING-VECTOR-001.json')
    if states(close.get('standing_vector',{}))!=EXPECTED:fail('closeout vector drift')
    b=load(BASE/'FORK-VOS-001-E002-REPOSITORY-BYTE-BINDINGS-001.json')
    for key in ['development_package_material_state','binary_support_material_state','raw_capture_archives_material_state']:
        if b.get(key)!='HASH_BOUND_NOT_BYTE_ADMITTED':fail(f'{key} promoted')
    target='7b39c369875bf1fa23edac6a5919847410a06e60e78cb3d6e99cb07e8d7c1718'
    if h.get('target_sha256')!=target:fail('target identity drift')
    bound={x['filename']:x['sha256'] for x in b.get('bindings',[])}
    if bound.get('E002_STIMULUS_02_SPATIAL_IDENTITY_MISSINGNESS.png')!=target:fail('target binding drift')
    print('PASS: E002 terminal repository admission candidate structurally consistent')
    print('boundary: terminal native records only; predecessor/binary/raw-capture bytes remain hash-bound, not byte-admitted')
    return 0
if __name__=='__main__':sys.exit(main())
