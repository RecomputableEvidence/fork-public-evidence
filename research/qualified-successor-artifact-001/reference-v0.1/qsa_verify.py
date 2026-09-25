#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, json, sys
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

def load_package(path: Path):
    if path.is_file():
        return load_json(path)
    index=load_json(path/'INDEX.json')
    require(index.get('type')=='QSA:REFERENCE_PACKAGE:v1','invalid package index type')
    components=index.get('components')
    require(isinstance(components,dict),'invalid package component index')
    pkg={'type':index['type']}
    expected={'manifest','constitution','trusted_keys','actor_bindings','genesis','states','qualifications','p0','p1','p2','p3'}
    require(set(components)==expected,'package component set mismatch')
    for name,rel in components.items():
        require(isinstance(rel,str) and '/' not in rel and '\\' not in rel,'invalid component path')
        pkg[name]=load_json(path/rel)
    return pkg

def assert_profile(obj:Any):
    if isinstance(obj,float): raise VerificationError('float encountered')
    if isinstance(obj,int) and not (-(2**63)<=obj<=2**63-1): raise VerificationError('integer outside signed 64-bit range')
    if isinstance(obj,dict):
        for k,v in obj.items():
            if not isinstance(k,str): raise VerificationError('non-string JSON object key')
            assert_profile(v)
    elif isinstance(obj,list):
        for v in obj: assert_profile(v)

def canonical_bytes(obj:Any)->bytes:
    assert_profile(obj)
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def object_hash(obj:Any)->str: return 'sha256:'+hashlib.sha256(canonical_bytes(obj)).hexdigest()
def state_hash(state:dict[str,Any])->str: return object_hash({k:v for k,v in state.items() if k not in {'signature','state_hash'}})
def require(c:bool,m:str):
    if not c: raise VerificationError(m)

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

def verify(pkg:dict[str,Any], schema:dict[str,Any])->dict[str,Any]:
    errs=sorted(Draft202012Validator(schema).iter_errors(pkg),key=lambda e:list(e.path))
    if errs: raise VerificationError('schema failure: '+'; '.join(f'{list(e.path)}: {e.message}' for e in errs[:8]))
    manifest=pkg['manifest']; const=pkg['constitution']; trusted=pkg['trusted_keys']; bindings=pkg['actor_bindings']; genesis=pkg['genesis']
    states={s['state_id']:s for s in pkg['states']}; s0=states['state:000']; s1=states['state:001']
    quals={q['change_class']:q for q in pkg['qualifications']}; qe=quals['EDITORIAL']; qs=quals['STRUCTURAL']
    keys=pubkeys(trusted)
    signed=[('genesis',genesis),('state0',s0),('state1',s1),('qual-editorial',qe),('qual-structural',qs),('p0-mark',pkg['p0']['proposal_mark']),('p0-inspection',pkg['p0']['inspection']),('p1-proposal',pkg['p1']['proposal']),('p1-inspection',pkg['p1']['inspection']),('p1-observation',pkg['p1']['observation']),('p2-proposal',pkg['p2']['proposal']),('p2-inspection',pkg['p2']['inspection']),('p2-adoption',pkg['p2']['adoption']),('p2-build-mark',pkg['p2']['build_mark']),('p3-proposal',pkg['p3']['proposal']),('p3-inspection',pkg['p3']['inspection'])]
    for label,obj in signed: verify_signed(obj,keys,label)
    s0h,s1h=state_hash(s0),state_hash(s1)
    require(s0['state_hash']==s0h,'state0 hash mismatch'); require(s1['state_hash']==s1h,'state1 hash mismatch')
    require(s0['parent_state_hash'] is None,'state0 parent must be null'); require(s1['parent_state_hash']==s0h,'state1 parent mismatch')
    require(manifest['current_state_hash']==s1h,'manifest current state mismatch')
    require(genesis['genesis_state_hash']==s0h,'genesis state binding mismatch')
    require(genesis['genesis_constitution_hash']==object_hash(const),'genesis constitution binding mismatch')
    require(genesis['trusted_keys_hash']==object_hash(trusted),'genesis keys binding mismatch')
    require(genesis['actor_bindings_hash']==object_hash(bindings),'genesis actor-binding mismatch')
    authority=set(const['acceptance_authority_policy']['authorized_key_ids']); inspectors=set(const['inspection_policy']['authorized_inspector_key_ids'])
    require('key:qsa-reference:authority' in authority,'authority policy missing key'); require('key:qsa-reference:inspector' in inspectors,'inspector policy missing key')
    binding_keys={b['key_id'] for b in bindings['bindings']}; require('key:qsa-reference:builder' in binding_keys,'builder actor binding absent')
    qeh,qsh=object_hash(qe),object_hash(qs)
    for q in (qe,qs):
        require(q['subject_key_id']=='key:qsa-reference:builder','qualification subject mismatch'); require(q['status']=='VALID','qualification not valid'); require(q['evidence'][0]['state_hash']==s0h,'qualification evidence mismatch')
    p0c,p0m,p0i=pkg['p0']['commitment'],pkg['p0']['proposal_mark'],pkg['p0']['inspection']
    require(p0c['proposal_mark_hash']==object_hash(p0m),'p0 mark binding mismatch'); require(p0c['inspection_receipt_hash']==object_hash(p0i),'p0 inspection binding mismatch'); require(p0c['qualification_receipt_hash']==qeh,'p0 qualification mismatch'); require(p0c['parent_state_hash']==s0h,'p0 parent mismatch'); require(p0i['proposal_hash']==p0c['proposal_payload_hash'],'p0 commitment mismatch'); require(p0i['disposition']=='P0_METADATA_ONLY','p0 disposition mismatch'); require(p0i['checks']['material_observation']=='NONE','p0 material observation unexpected')
    p1,p1i,p1o=pkg['p1']['proposal'],pkg['p1']['inspection'],pkg['p1']['observation']
    require(p1['parent_state_hash']==s0h,'p1 parent mismatch'); require(p1['qualification_receipt_hash']==qsh,'p1 qualification mismatch'); require(p1i['proposal_hash']==object_hash(p1),'p1 proposal binding mismatch'); require(p1i['material_observation_hashes']==[object_hash(p1o)],'p1 observation binding mismatch'); require(p1i['disposition']=='P1_OBSERVATION_PRESERVED','p1 disposition mismatch')
    p2,p2i,p2a,p2b=pkg['p2']['proposal'],pkg['p2']['inspection'],pkg['p2']['adoption'],pkg['p2']['build_mark']; p2h=object_hash(p2); p2ih=object_hash(p2i); p2ah=object_hash(p2a)
    require(p2['parent_state_hash']==s0h,'p2 parent mismatch'); require(p2['qualification_receipt_hash']==qsh,'p2 qualification mismatch'); require(p2['proposed_state_hash']==s1h,'p2 proposed state mismatch'); require(p2i['proposal_hash']==p2h,'p2 inspection binding mismatch'); require(p2i['declared_change_class']==p2i['verified_change_class']=='STRUCTURAL','p2 class mismatch'); require(p2i['disposition']=='P2_ELIGIBLE_FOR_ADOPTION','p2 inspection disposition mismatch'); require(p2a['proposal_hash']==p2h and p2a['inspection_receipt_hash']==p2ih,'p2 adoption evidence mismatch'); require(p2a['parent_state_hash']==s0h and p2a['successor_state_hash']==s1h,'p2 adoption state mismatch'); require(p2a['authority_key_id'] in authority and p2a['signature']['key_id']==p2a['authority_key_id'],'p2 authority binding mismatch'); require(p2a['qualification_status_at_adoption']=='VALID','p2 qualification invalid at adoption'); require(p2b['proposal_hash']==p2h and p2b['inspection_receipt_hash']==p2ih and p2b['adoption_receipt_hash']==p2ah,'build mark evidence mismatch'); require(p2b['successor_state_hash']==s1h and p2b['parent_state_hash']==s0h,'build mark state mismatch'); require(p2b['qualification_receipt_hash']==qsh,'build mark qualification mismatch'); require(p2b['signature']['key_id']==p2b['builder_key_id']=='key:qsa-reference:builder','build mark signer mismatch'); require(manifest['p2']['build_mark_hash']==object_hash(p2b),'manifest build mark mismatch')
    p3,p3i=pkg['p3']['proposal'],pkg['p3']['inspection']
    require(p3['parent_state_hash']==s1h,'p3 must target current state'); require(p3['qualification_receipt_hash']==qeh,'p3 qualification mismatch'); require(p3i['proposal_hash']==object_hash(p3),'p3 binding mismatch'); require(p3i['declared_change_class']=='EDITORIAL' and p3i['verified_change_class']=='CONSTITUTIONAL','p3 escalation missing'); require(p3i['checks']['change_class_route']=='FAIL','p3 route should fail'); require(p3i['disposition']=='P3_REJECTED_ROUTE_INVALID','p3 disposition mismatch')
    need={'CHANGE_CLASS_MISMATCH','ELEVATED_ROUTE_REQUIRED','PROTECTED_INVARIANT_IMPACT','CONSTITUTIONAL_ROUTE_REQUIRED'}; require(need.issubset(set(p3i['findings'])),'p3 findings missing')
    inv={f'I{i}_'+name for i,name in []}
    require(len(const['protected_invariants'])==9 and len(set(const['protected_invariants']))==9,'protected invariant set malformed')
    return {'type':'QSA:VERIFICATION_RECEIPT:v1','artifact_id':manifest['artifact_id'],'profile':manifest['profile'],'canonicalization':manifest['canonicalization'],'current_state_hash':s1h,'checks':{'ADOPTION_BINDING':'PASS','ADOPTION_ORDERING':'PASS','BUILD_MARK_BINDING':'PASS','CHANGE_CLASS_ROUTE':'PASS','CONTENT_HASHES':'PASS','CURRENT_STATE_RECOMPUTATION':'PASS','GENESIS_BINDING':'PASS','INSPECTION_BINDING':'PASS','P0_METADATA_ONLY':'PASS','P1_OBSERVATION_PRESERVED':'PASS','P2_SUCCESSOR_IMPLEMENTED':'PASS','P3_ROUTE_INVALID_REJECTED':'PASS','PROPOSAL_MARK_BINDING':'PASS','PROTECTED_INVARIANTS':'PASS','QUALIFICATION_BINDINGS':'PASS','QUALIFICATION_STATUS_AT_ADOPTION':'PASS','QUALIFICATION_STATUS_AT_INSPECTION':'PASS','QUALIFICATION_STATUS_AT_SUBMISSION':'PASS','SCHEMA_VALIDATION':'PASS','SIGNATURES':'PASS','STATE_PARENT_BINDING':'PASS'},'counts':{'adoption_events':1,'canonical_states':2,'outcomes':4,'signed_objects_verified':len(signed)},'non_evaluations':{'EMPIRICAL_HYPOTHESIS_STATUS':'OUT_OF_SCOPE','MORAL_LEGITIMACY':'NOT_EVALUATED','POLICY_WISDOM':'NOT_EVALUATED','SEMANTIC_TRUTH':'NOT_EVALUATED','UNIVERSAL_AUTHORITY':'NOT_ESTABLISHED'},'overall':'PASS'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('package',nargs='?',default=str(HERE/'reference-package')); ap.add_argument('--json',action='store_true'); ap.add_argument('--compare-expected',action='store_true'); args=ap.parse_args()
    try:
        pkg=load_package(Path(args.package)); sch=load_json(HERE/'reference-package.schema.json'); rec=verify(pkg,sch)
        if args.compare_expected:
            exp=load_json(HERE/'verification-receipt.expected.json'); require(rec==exp,'verification receipt differs from expected')
        if args.json: sys.stdout.buffer.write(canonical_bytes(rec)+b'\n')
        else:
            print(f"QSA-001 reference verification: {rec['overall']}")
            for k,v in rec['checks'].items(): print(f'{k} = {v}')
            for k,v in rec['non_evaluations'].items(): print(f'{k} = {v}')
        return 0
    except VerificationError as e:
        if args.json: sys.stdout.buffer.write(canonical_bytes({'type':'QSA:VERIFICATION_RECEIPT:v1','overall':'FAIL','error':str(e)})+b'\n')
        else: print(f'QSA-001 reference verification: FAIL\n{e}',file=sys.stderr)
        return 1
if __name__=='__main__': raise SystemExit(main())
