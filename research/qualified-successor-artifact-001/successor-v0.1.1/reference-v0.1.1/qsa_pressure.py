#!/usr/bin/env python3
from __future__ import annotations
import base64, copy, hashlib, json, tempfile
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import qsa_verify as qv

HERE=Path(__file__).resolve().parent
PKG_DIR=HERE/'reference-package'
SCHEMA=qv.load_json(HERE/'reference-package.schema.json')

def seed(label): return hashlib.sha256(('QSA-001-v0.1.1:'+label).encode()).digest()
PRIV={k:Ed25519PrivateKey.from_private_bytes(seed(k)) for k in ['authority','builder','genesis','inspector','qualification','adversarial']}
def canonical(o): return qv.canonical_bytes(o)
def oh(o): return qv.object_hash(o)
def sh(s): return qv.state_hash(s)
def resign(o,key):
    payload=dict(o); payload.pop('signature',None)
    sig=PRIV[key].sign(o['type'].encode()+b'\n'+canonical(payload))
    o['signature']={'algorithm':'Ed25519','domain':o['type'],'key_id':f'key:qsa-reference:{key}','value':base64.b64encode(sig).decode()}

def load(): return qv.load_package(PKG_DIR)
def result(pid, expected, fn, match=None):
    try:
        fn(); actual='PASS'; err=None
    except qv.VerificationError as e:
        actual='REJECT'; err=str(e)
    ok=(actual==expected and (match is None or (err and match in err)))
    return {'probe_id':pid,'expected':expected,'actual':actual,'error':err,'expectation_match':ok}
def run_verify(p): return qv.verify(p,SCHEMA)
def structural_q(p): return next(q for q in p['qualifications'] if q['change_class']=='STRUCTURAL')

def refresh_transition(obj):
    p,i,a,b=obj['proposal'],obj['inspection'],obj['adoption'],obj['build_mark']
    resign(p,'builder'); i['proposal_hash']=oh(p); resign(i,'inspector')
    a['proposal_hash']=oh(p); a['inspection_receipt_hash']=oh(i); resign(a,'authority')
    b['proposal_hash']=oh(p); b['inspection_receipt_hash']=oh(i); b['adoption_receipt_hash']=oh(a); resign(b,'builder')

def rebind_structural_q(p,new_until):
    q=structural_q(p); q['valid_until']=new_until; q['status']='VALID'; resign(q,'qualification'); qh=oh(q)
    for nm in ['p_seed','p2']:
        t=p[nm]; t['proposal']['qualification_receipt_hash']=qh; t['build_mark']['qualification_receipt_hash']=qh; refresh_transition(t)
    p['p1']['proposal']['qualification_receipt_hash']=qh; resign(p['p1']['proposal'],'builder'); p['p1']['inspection']['proposal_hash']=oh(p['p1']['proposal']); resign(p['p1']['inspection'],'inspector')
    return p

results=[]
# baseline
results.append(result('BASELINE','PASS',lambda:run_verify(load())))
# A1
p=load(); p['p2']['proposal']['proposal_intent']='tampered'; results.append(result('A1','REJECT',lambda p=p:run_verify(p),'signature verification failed: p2-proposal'))
# A2
p=load(); p['trusted_keys']['keys'][1]['public_key_base64']=p['trusted_keys']['keys'][0]['public_key_base64']; results.append(result('A2','REJECT',lambda p=p:run_verify(p),'signature verification failed'))
# A3
p=load(); p['p2']['adoption']['signature']=copy.deepcopy(p['p2']['proposal']['signature']); results.append(result('A3','REJECT',lambda p=p:run_verify(p),'domain/type mismatch'))
# A4 unsigned parent mutation
p=load(); p['states'][2]['parent_state_hash']='sha256:'+'0'*64; results.append(result('A4','REJECT',lambda p=p:run_verify(p),'signature verification failed: state:002'))
# A5 unsigned successor content mutation
p=load(); p['states'][2]['content']['revision']=99; results.append(result('A5','REJECT',lambda p=p:run_verify(p),'signature verification failed: state:002'))
# A6 unsigned qualification expiry mutation
p=load(); structural_q(p)['valid_until']='2026-09-25T16:31:00Z'; results.append(result('A6','REJECT',lambda p=p:run_verify(p),'signature verification failed: qualification:structural:001'))
# A7 unsigned stale parent mutation
p=load(); p['p2']['proposal']['parent_state_hash']=p['states'][0]['state_hash']; results.append(result('A7','REJECT',lambda p=p:run_verify(p),'signature verification failed: p2-proposal'))
# A8 embedded route rejection: verifier PASS entails p3 rejection fixture enforced
p=load(); results.append(result('A8','PASS',lambda p=p:run_verify(p)))
# A9 remove inspection
p=load(); del p['p2']['inspection']; results.append(result('A9','REJECT',lambda p=p:run_verify(p),'schema failure'))
# A10 actor binding mutation
p=load(); p['actor_bindings']['bindings'][0]['key_id']='key:qsa-reference:qualification'; results.append(result('A10','REJECT',lambda p=p:run_verify(p),'genesis actor-binding mismatch'))
# A11 duplicate JSON key parser
with tempfile.NamedTemporaryFile('w+',delete=False,encoding='utf-8') as f:
    f.write('{"artifact_id":"a","artifact_id":"b"}'); a11=Path(f.name)
results.append(result('A11','REJECT',lambda:qv.load_json(a11),'duplicate JSON object key'))
a11.unlink()
# A12 float parser
with tempfile.NamedTemporaryFile('w+',delete=False,encoding='utf-8') as f:
    f.write('{"x":1.25}'); a12=Path(f.name)
results.append(result('A12','REJECT',lambda:qv.load_json(a12),'prohibits floating-point numbers'))
a12.unlink()
# A4-R validly signed wrong state parent with cascaded successor hashes
p=load(); s2=p['states'][2]; s2['parent_state_hash']=p['states'][0]['state_hash']; s2['state_hash']=sh(s2); resign(s2,'authority'); nh=s2['state_hash']; p['manifest']['canonical_chain'][2]=nh; p['manifest']['current_state_hash']=nh; t=p['p2']; t['proposal']['proposed_state_hash']=nh; t['adoption']['successor_state_hash']=nh; t['build_mark']['successor_state_hash']=nh; refresh_transition(t); results.append(result('A4-R','REJECT',lambda p=p:run_verify(p),'canonical chain parent mismatch'))
# A5-R validly signed successor mutation, all downstream updated except build-mark successor hash
p=load(); old=p['states'][2]['state_hash']; s2=p['states'][2]; s2['content']['revision']=3; s2['state_hash']=sh(s2); resign(s2,'authority'); nh=s2['state_hash']; p['manifest']['canonical_chain'][2]=nh; p['manifest']['current_state_hash']=nh; t=p['p2']; t['proposal']['proposed_state_hash']=nh; resign(t['proposal'],'builder'); t['inspection']['proposal_hash']=oh(t['proposal']); resign(t['inspection'],'inspector'); t['adoption']['proposal_hash']=oh(t['proposal']); t['adoption']['inspection_receipt_hash']=oh(t['inspection']); t['adoption']['successor_state_hash']=nh; resign(t['adoption'],'authority'); t['build_mark']['proposal_hash']=oh(t['proposal']); t['build_mark']['inspection_receipt_hash']=oh(t['inspection']); t['build_mark']['adoption_receipt_hash']=oh(t['adoption']); resign(t['build_mark'],'builder'); results.append(result('A5-R','REJECT',lambda p=p:run_verify(p),'successor relation mismatch'))
# A6 focused temporal positions
for pid,until,match in [('A6-R1','2026-09-25T16:29:59Z','qualification interval invalid at p2:submission'),('A6-R2','2026-09-25T16:30:30Z','qualification interval invalid at p2:inspection'),('A6-R3','2026-09-25T16:31:30Z','qualification interval invalid at p2:adoption')]:
    p=rebind_structural_q(load(),until); results.append(result(pid,'REJECT',lambda p=p:run_verify(p),match))
# A7-R valid signatures, p2 stale parent state0 while successor remains state2
p=load(); stale=p['states'][0]['state_hash']; t=p['p2']; t['proposal']['parent_state_hash']=stale; t['adoption']['parent_state_hash']=stale; t['build_mark']['parent_state_hash']=stale; refresh_transition(t); results.append(result('A7-R','REJECT',lambda p=p:run_verify(p),'stale parent not currently adoptable: p2'))

out={'artifact_id':'QSA-001-v0.1.1-SUCCESSOR-REGRESSION-RETURN-001','reference_profile':'QSA-001-v0.1.1-SUCCESSOR-REFERENCE','results':results,'all_expectations_matched':all(r['expectation_match'] for r in results),'nonclaims':['Regression success does not establish production readiness or formal security.','Test-only deterministic private keys are reference-fixture material and confer no external identity or authority.','Passing the declared matrix does not establish semantic truth, governance wisdom, or empirical Fork hypotheses.']}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out['all_expectations_matched'] else 1)
