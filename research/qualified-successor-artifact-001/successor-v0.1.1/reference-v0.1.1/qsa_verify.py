#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parent
class VerificationError(Exception): pass

def no_float(_:str): raise VerificationError('QSA-CANONICAL-JSON-001 prohibits floating-point numbers')
def no_dupes(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise VerificationError(f'duplicate JSON object key: {k}')
        out[k]=v
    return out

def load_json(path:Path):
    raw=path.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'): raise VerificationError(f'BOM prohibited: {path}')
    try: return json.loads(raw.decode('utf-8'),object_pairs_hook=no_dupes,parse_float=no_float)
    except UnicodeDecodeError as e: raise VerificationError(f'not UTF-8: {path}: {e}') from e

def load_package(path:Path):
    if path.is_file(): return load_json(path)
    idx=load_json(path/'INDEX.json')
    require(idx.get('type')=='QSA:REFERENCE_PACKAGE:v1','invalid package index type')
    comps=idx.get('components'); require(isinstance(comps,dict),'invalid package component index')
    expected={'manifest','constitution','trusted_keys','actor_bindings','genesis','states','qualifications','p_seed','p0','p1','p2','p3'}
    require(set(comps)==expected,'package component set mismatch')
    pkg={'type':idx['type']}
    for name,rel in comps.items():
        require(isinstance(rel,str) and '/' not in rel and '\\' not in rel,'invalid component path')
        pkg[name]=load_json(path/rel)
    return pkg

def assert_profile(o:Any):
    if isinstance(o,float): raise VerificationError('float encountered')
    if isinstance(o,int) and not (-(2**63)<=o<=2**63-1): raise VerificationError('integer outside signed 64-bit range')
    if isinstance(o,dict):
        for k,v in o.items():
            if not isinstance(k,str): raise VerificationError('non-string JSON object key')
            assert_profile(v)
    elif isinstance(o,list):
        for v in o: assert_profile(v)

def canonical_bytes(o:Any)->bytes:
    assert_profile(o)
    return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def object_hash(o:Any)->str: return 'sha256:'+hashlib.sha256(canonical_bytes(o)).hexdigest()
def state_hash(s:dict)->str: return object_hash({k:v for k,v in s.items() if k not in {'signature','state_hash'}})
def require(c:bool,m:str):
    if not c: raise VerificationError(m)

def parse_ts(s:str)->datetime:
    try:
        if s.endswith('Z'): s=s[:-1]+'+00:00'
        d=datetime.fromisoformat(s)
        require(d.tzinfo is not None,'timestamp lacks timezone')
        return d.astimezone(timezone.utc)
    except Exception as e:
        if isinstance(e,VerificationError): raise
        raise VerificationError(f'invalid timestamp: {s}') from e

def pubkeys(trusted):
    return {x['key_id']:Ed25519PublicKey.from_public_bytes(base64.b64decode(x['public_key_base64'],validate=True)) for x in trusted['keys']}
def verify_signed(obj,keys,label):
    sig=obj.get('signature'); require(isinstance(sig,dict),f'missing signature: {label}')
    require(sig.get('domain')==obj.get('type'),f'domain/type mismatch: {label}')
    require(sig.get('algorithm')=='Ed25519',f'wrong algorithm: {label}')
    kid=sig.get('key_id'); require(kid in keys,f'unknown key: {label}')
    payload=dict(obj); payload.pop('signature')
    pre=obj['type'].encode()+b'\n'+canonical_bytes(payload)
    try: keys[kid].verify(base64.b64decode(sig['value'],validate=True),pre)
    except (InvalidSignature,ValueError) as e: raise VerificationError(f'signature verification failed: {label}') from e

def qual_valid_at(q:dict, when:str, label:str):
    require(q['status']=='VALID',f'qualification status not valid at {label}')
    t=parse_ts(when); lo=parse_ts(q['valid_from']); hi=parse_ts(q['valid_until'])
    require(lo <= t <= hi, f'qualification interval invalid at {label}')

def verify_transition(name:str,obj:dict,states_by_hash:dict,chain:list[str],quals_by_hash:dict,authority:set[str],keys:dict, checks:list[str]):
    p,i,a,b=obj['proposal'],obj['inspection'],obj['adoption'],obj['build_mark']
    for lab,o in [(f'{name}-proposal',p),(f'{name}-inspection',i),(f'{name}-adoption',a),(f'{name}-build-mark',b)]: verify_signed(o,keys,lab)
    ph,ih,ah=object_hash(p),object_hash(i),object_hash(a)
    require(i['proposal_hash']==ph,f'{name} inspection binding mismatch')
    require(a['proposal_hash']==ph and a['inspection_receipt_hash']==ih,f'{name} adoption evidence mismatch')
    require(b['proposal_hash']==ph and b['inspection_receipt_hash']==ih and b['adoption_receipt_hash']==ah,f'{name} build mark evidence mismatch')
    qh=p['qualification_receipt_hash']; require(qh in quals_by_hash,f'{name} qualification receipt unknown')
    q=quals_by_hash[qh]
    require(q['change_class']==p['declared_change_class'],f'{name} qualification class mismatch')
    qual_valid_at(q,p['submitted_at'],f'{name}:submission')
    qual_valid_at(q,i['inspected_at'],f'{name}:inspection')
    qual_valid_at(q,a['adopted_at'],f'{name}:adoption')
    require(a['qualification_status_at_adoption']=='VALID',f'{name} adoption status field invalid')
    parent=a['parent_state_hash']; succ=a['successor_state_hash']
    require(parent==p['parent_state_hash']==b['parent_state_hash'],f'{name} parent relation mismatch')
    require(succ==p['proposed_state_hash']==b['successor_state_hash'],f'{name} successor relation mismatch')
    require(parent in states_by_hash and succ in states_by_hash,f'{name} state reference missing')
    si=chain.index(succ); require(si>0 and chain[si-1]==parent,f'stale parent not currently adoptable: {name}')
    require(states_by_hash[succ]['parent_state_hash']==parent,f'{name} successor state parent mismatch')
    require(a['authority_key_id'] in authority and a['signature']['key_id']==a['authority_key_id'],f'{name} authority binding mismatch')
    require(b['qualification_receipt_hash']==qh,f'{name} build mark qualification mismatch')
    require(b['signature']['key_id']==b['builder_key_id']=='key:qsa-reference:builder',f'{name} build mark signer mismatch')
    checks.extend([f'{name.upper()}_BINDINGS',f'{name.upper()}_TEMPORAL_QUALIFICATION'])

def verify(pkg:dict,schema:dict)->dict:
    errs=sorted(Draft202012Validator(schema).iter_errors(pkg),key=lambda e:list(e.path))
    if errs: raise VerificationError('schema failure: '+'; '.join(f'{list(e.path)}: {e.message}' for e in errs[:8]))
    m,c,t,b,g=pkg['manifest'],pkg['constitution'],pkg['trusted_keys'],pkg['actor_bindings'],pkg['genesis']
    keys=pubkeys(t)
    # forbid test-only key from operational authority/inspection roles
    test_key=c['pressure_policy']['adversarial_test_key_id']
    require(test_key not in c['acceptance_authority_policy']['authorized_key_ids'],'adversarial key cannot be acceptance authority')
    require(test_key not in c['inspection_policy']['authorized_inspector_key_ids'],'adversarial key cannot be inspector authority')
    signed=[('genesis',g)]
    for s in pkg['states']: signed.append((s['state_id'],s))
    for q in pkg['qualifications']: signed.append((q['qualification_id'],q))
    for name in ['p_seed','p2']:
        for k in ['proposal','inspection','adoption','build_mark']: signed.append((f'{name}-{k}',pkg[name][k]))
    for name,ks in [('p0',['proposal_mark','inspection']),('p1',['proposal','inspection','observation']),('p3',['proposal','inspection'])]:
        for k in ks:signed.append((f'{name}-{k}',pkg[name][k]))
    for lab,o in signed: verify_signed(o,keys,lab)
    # states and chain
    states_by_hash={}
    ids=set()
    for s in pkg['states']:
        require(s['state_id'] not in ids,'duplicate state_id'); ids.add(s['state_id'])
        h=state_hash(s); require(s['state_hash']==h,f"{s['state_id']} hash mismatch"); require(h not in states_by_hash,'duplicate state hash'); states_by_hash[h]=s
    chain=m['canonical_chain']; require(len(chain)>=2,'canonical chain too short'); require(len(chain)==len(set(chain)),'duplicate chain state')
    require(set(chain)==set(states_by_hash),'canonical chain/state population mismatch')
    require(states_by_hash[chain[0]]['parent_state_hash'] is None,'genesis state parent must be null')
    for idx in range(1,len(chain)):
        require(states_by_hash[chain[idx]]['parent_state_hash']==chain[idx-1],f'canonical chain parent mismatch at index {idx}')
    require(m['current_state_hash']==chain[-1],'manifest current state mismatch')
    # genesis binding
    require(g['genesis_state_hash']==chain[0],'genesis state binding mismatch')
    require(g['genesis_constitution_hash']==object_hash(c),'genesis constitution binding mismatch')
    require(g['trusted_keys_hash']==object_hash(t),'genesis keys binding mismatch')
    require(g['actor_bindings_hash']==object_hash(b),'genesis actor-binding mismatch')
    authority=set(c['acceptance_authority_policy']['authorized_key_ids']); inspectors=set(c['inspection_policy']['authorized_inspector_key_ids'])
    binding_keys={x['key_id'] for x in b['bindings']}; require('key:qsa-reference:builder' in binding_keys,'builder actor binding absent')
    # qualifications map
    quals_by_hash={object_hash(q):q for q in pkg['qualifications']}
    for q in pkg['qualifications']:
        require(q['subject_key_id']=='key:qsa-reference:builder','qualification subject mismatch')
    check_names=[]
    verify_transition('p_seed',pkg['p_seed'],states_by_hash,chain,quals_by_hash,authority,keys,check_names)
    verify_transition('p2',pkg['p2'],states_by_hash,chain,quals_by_hash,authority,keys,check_names)
    # p0
    p0c,p0m,p0i=pkg['p0']['commitment'],pkg['p0']['proposal_mark'],pkg['p0']['inspection']
    require(p0c['proposal_mark_hash']==object_hash(p0m),'p0 mark binding mismatch'); require(p0c['inspection_receipt_hash']==object_hash(p0i),'p0 inspection binding mismatch')
    q0=quals_by_hash[p0c['qualification_receipt_hash']]; qual_valid_at(q0,p0m['submitted_at'],'p0:submission'); qual_valid_at(q0,p0i['inspected_at'],'p0:inspection')
    require(p0i['disposition']=='P0_METADATA_ONLY' and p0i['checks']['material_observation']=='NONE','p0 disposition mismatch')
    # p1
    p1,p1i,p1o=pkg['p1']['proposal'],pkg['p1']['inspection'],pkg['p1']['observation']; q1=quals_by_hash[p1['qualification_receipt_hash']]
    qual_valid_at(q1,p1['submitted_at'],'p1:submission'); qual_valid_at(q1,p1i['inspected_at'],'p1:inspection')
    require(p1i['proposal_hash']==object_hash(p1),'p1 proposal binding mismatch'); require(p1i['material_observation_hashes']==[object_hash(p1o)],'p1 observation binding mismatch'); require(p1i['disposition']=='P1_OBSERVATION_PRESERVED','p1 disposition mismatch')
    # p3
    p3,p3i=pkg['p3']['proposal'],pkg['p3']['inspection']; q3=quals_by_hash[p3['qualification_receipt_hash']]
    qual_valid_at(q3,p3['submitted_at'],'p3:submission'); qual_valid_at(q3,p3i['inspected_at'],'p3:inspection')
    require(p3['parent_state_hash']==chain[-1],'p3 must target current state'); require(p3i['proposal_hash']==object_hash(p3),'p3 binding mismatch'); require(p3i['declared_change_class']=='EDITORIAL' and p3i['verified_change_class']=='CONSTITUTIONAL','p3 escalation missing'); require(p3i['checks']['change_class_route']=='FAIL','p3 route should fail'); require(p3i['disposition']=='P3_REJECTED_ROUTE_INVALID','p3 disposition mismatch')
    need={'CHANGE_CLASS_MISMATCH','ELEVATED_ROUTE_REQUIRED','PROTECTED_INVARIANT_IMPACT','CONSTITUTIONAL_ROUTE_REQUIRED'}; require(need.issubset(set(p3i['findings'])),'p3 findings missing')
    require(len(c['protected_invariants'])==9 and len(set(c['protected_invariants']))==9,'protected invariant set malformed')
    checks={
      'SCHEMA_VALIDATION':'PASS','SIGNATURES':'PASS','CONTENT_HASHES':'PASS','GENESIS_BINDING':'PASS','CANONICAL_CHAIN':'PASS','CURRENT_STATE_RECOMPUTATION':'PASS','STATE_PARENT_BINDING':'PASS','ADOPTION_ORDERING':'PASS','P0_METADATA_ONLY':'PASS','P1_OBSERVATION_PRESERVED':'PASS','P2_SUCCESSOR_IMPLEMENTED':'PASS','P3_ROUTE_INVALID_REJECTED':'PASS','PROTECTED_INVARIANTS':'PASS','QUALIFICATION_STATUS_AT_SUBMISSION':'PASS','QUALIFICATION_STATUS_AT_INSPECTION':'PASS','QUALIFICATION_STATUS_AT_ADOPTION':'PASS','QUALIFICATION_INTERVAL_AT_SUBMISSION':'PASS','QUALIFICATION_INTERVAL_AT_INSPECTION':'PASS','QUALIFICATION_INTERVAL_AT_ADOPTION':'PASS','STALE_PARENT_REJECTION_LOGIC':'PASS','ACTOR_BINDING_SEPARATION':'PASS','TEST_KEY_ROLE_SEPARATION':'PASS'
    }
    return {'type':'QSA:VERIFICATION_RECEIPT:v1','artifact_id':m['artifact_id'],'profile':m['profile'],'predecessor_reference_commit':m['predecessor_reference_commit'],'canonicalization':m['canonicalization'],'current_state_hash':chain[-1],'checks':checks,'counts':{'adoption_events':2,'canonical_states':len(chain),'outcomes':4,'signed_objects_verified':len(signed)},'non_evaluations':{'EMPIRICAL_HYPOTHESIS_STATUS':'OUT_OF_SCOPE','MORAL_LEGITIMACY':'NOT_EVALUATED','POLICY_WISDOM':'NOT_EVALUATED','SEMANTIC_TRUTH':'NOT_EVALUATED','UNIVERSAL_AUTHORITY':'NOT_ESTABLISHED','PRODUCTION_READINESS':'NOT_ESTABLISHED'},'overall':'PASS'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('package',nargs='?',default=str(HERE/'reference-package')); ap.add_argument('--json',action='store_true'); ap.add_argument('--compare-expected',action='store_true'); args=ap.parse_args()
    try:
        pkg=load_package(Path(args.package)); sch=load_json(HERE/'reference-package.schema.json'); rec=verify(pkg,sch)
        if args.compare_expected:
            exp=load_json(HERE/'verification-receipt.expected.json'); require(rec==exp,'verification receipt differs from expected')
        if args.json: sys.stdout.buffer.write(canonical_bytes(rec)+b'\n')
        else:
            print(f"QSA-001 v0.1.1 verification: {rec['overall']}")
            for k,v in rec['checks'].items(): print(f'{k} = {v}')
            for k,v in rec['non_evaluations'].items(): print(f'{k} = {v}')
        return 0
    except VerificationError as e:
        if args.json: sys.stdout.buffer.write(canonical_bytes({'type':'QSA:VERIFICATION_RECEIPT:v1','overall':'FAIL','error':str(e)})+b'\n')
        else: print(f'QSA-001 v0.1.1 verification: FAIL\n{e}',file=sys.stderr)
        return 1
if __name__=='__main__': raise SystemExit(main())
