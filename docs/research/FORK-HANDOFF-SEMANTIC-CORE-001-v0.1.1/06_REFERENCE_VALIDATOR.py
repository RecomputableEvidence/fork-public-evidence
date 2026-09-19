#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parent
SCHEMA=json.loads((ROOT/'02_FORK_HANDOFF_CORE_v0_2.schema.json').read_text(encoding='utf-8'))

DIMENSION_MAP={'AUTHORITY':'AUTHORITY'}

def semantic_errors(obj):
    errors=[]
    def err(code,detail): errors.append({'code':code,'detail':detail})
    ri=obj.get('record_identity',{})
    if ri.get('record_id') and ri.get('record_id')==ri.get('predecessor_record_id'):
        err('SELF_PREDECESSOR_FORBIDDEN','record_id equals predecessor_record_id')
    claims=obj.get('claims',[]); evidence=obj.get('evidence',[]); unresolved=obj.get('unresolved',[])
    for label, seq, key, code in [('claim',claims,'claim_id','DUPLICATE_CLAIM_ID'),('evidence',evidence,'evidence_id','DUPLICATE_EVIDENCE_ID'),('unresolved',unresolved,'unresolved_id','DUPLICATE_UNRESOLVED_ID')]:
        vals=[x.get(key) for x in seq if isinstance(x,dict)]
        if len(vals)!=len(set(vals)): err(code,f'duplicate {label} identifier')
    evid_ids={x.get('evidence_id') for x in evidence if isinstance(x,dict)}
    for c in claims:
        for r in c.get('evidence_refs',[]):
            if r not in evid_ids: err('DANGLING_CLAIM_EVIDENCE_REF',f"{c.get('claim_id')} -> {r}")
        if c.get('claim_basis')=='RECOMPUTED' and not c.get('evidence_refs'):
            err('RECOMPUTED_WITHOUT_EVIDENCE',str(c.get('claim_id')))
        if c.get('claim_dimension')=='INDEPENDENT_WITNESSING':
            err('CRYPTOGRAPHIC_LAYER_PREMATURE',str(c.get('claim_id')))
    auth=obj.get('authority_state',{})
    for r in auth.get('basis_evidence_refs',[]):
        if r not in evid_ids: err('DANGLING_AUTHORITY_EVIDENCE_REF',r)
    status=auth.get('transfer_status')
    basis=auth.get('basis_evidence_refs',[])
    if status=='TRANSFER_ASSERTED' and (not basis or not auth.get('target_authority_ref')):
        err('AUTHORITY_TRANSFER_WITHOUT_BASIS','TRANSFER_ASSERTED requires target and evidence basis')
    if status=='NOT_TRANSFERRED' and (basis or auth.get('target_authority_ref') is not None):
        err('NONTRANSFER_WITH_TRANSFER_BASIS','NOT_TRANSFERRED carries transfer basis or target')
    nonclaims=set(obj.get('non_claims',[]))
    for c in claims:
        if c.get('claim_dimension') in nonclaims:
            err('CLAIM_NONCLAIM_CONTRADICTION',str(c.get('claim_dimension')))
    reval=set(obj.get('revalidation_required',[]))
    for u in unresolved:
        dim=u.get('dimension')
        if dim!='OTHER' and DIMENSION_MAP.get(dim,dim) not in reval:
            err('UNRESOLVED_WITHOUT_REVALIDATION',str(dim))
    for e in evidence:
        ds=e.get('disclosure_state'); ac=e.get('access_status'); loc=e.get('locator')
        if ds=='UNAVAILABLE' and (ac!='UNAVAILABLE' or loc is not None):
            err('UNAVAILABLE_EVIDENCE_CONTRADICTION',str(e.get('evidence_id')))
        if ds=='FULL' and (ac!='AVAILABLE' or not loc):
            err('FULL_EVIDENCE_NOT_AVAILABLE',str(e.get('evidence_id')))
    if status=='TRANSFER_ASSERTED' and 'AUTHORIZATION' in nonclaims:
        err('AUTHORITY_NONCLAIM_CONTRADICTION','TRANSFER_ASSERTED with AUTHORIZATION non-claim')
    return errors

def validate_obj(obj):
    schema_errors=[]
    v=Draft202012Validator(SCHEMA, format_checker=FormatChecker())
    for e in sorted(v.iter_errors(obj), key=lambda e:list(e.path)):
        schema_errors.append({'code':'SCHEMA_VALIDATION_ERROR','path':'/'.join(map(str,e.path)),'detail':e.message})
    sem=semantic_errors(obj) if not schema_errors else []
    return {'schema_valid':not schema_errors,'semantic_valid':not sem if not schema_errors else False,'schema_errors':schema_errors,'semantic_errors':sem,'result':'PASS' if not schema_errors and not sem else 'FAIL'}

def run_fixtures():
    rows=[]
    for expected, folder in [('PASS',ROOT/'04_VALID_FIXTURES'),('FAIL',ROOT/'05_ADVERSARIAL_FIXTURES')]:
        for p in sorted(folder.glob('*.json')):
            obj=json.loads(p.read_text(encoding='utf-8')); rep=validate_obj(obj)
            rows.append({'fixture':str(p.relative_to(ROOT)),'expected':expected,'observed':rep['result'],'matched':expected==rep['result'],'errors':rep['schema_errors']+rep['semantic_errors']})
    return {'object':'FORK-HANDOFF-SEMANTIC-CORE-001','fixture_count':len(rows),'matched_count':sum(r['matched'] for r in rows),'all_matched':all(r['matched'] for r in rows),'rows':rows}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path',nargs='?'); ap.add_argument('--fixtures',action='store_true'); args=ap.parse_args()
    if args.fixtures:
        rep=run_fixtures()
    elif args.path:
        rep=validate_obj(json.loads(Path(args.path).read_text(encoding='utf-8')))
    else:
        ap.error('provide --fixtures or path')
    print(json.dumps(rep,indent=2)); raise SystemExit(0 if (rep.get('all_matched',rep.get('result')=='PASS')) else 1)
if __name__=='__main__': main()
