#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 f=[];m=json.loads((ROOT/'CANDIDATE-MANIFEST.json').read_text())
 for e in m['files']:
  p=ROOT/e['path']
  if not p.is_file(): f.append('MISSING:'+e['path']);continue
  if p.stat().st_size!=e['byte_size']: f.append('SIZE:'+e['path'])
  if h(p)!=e['sha256']: f.append('SHA:'+e['path'])
 b=json.loads((ROOT/'PUBLIC-RESTRICTED-EVIDENCE-BOUNDARY.json').read_text())
 names={p.name for p in ROOT.rglob('*') if p.is_file()}
 for n in ['TP001-V01-EXTERIOR-RECOMPUTATION-ENVELOPE-001-RETURN.zip','REVIEWER-DISCLOSURE.json','SUPPLEMENTARY-FIRST-CLAUDE-TRANSCRIPT.txt']:
  if n in names:f.append('RESTRICTED:'+n)
 l=json.loads((ROOT/'v0.2/EXTERIOR-STANDING-LINEAGE-ANCHOR.json').read_text())
 if l['temporal_reconciliation']['v0_2_exterior_verification_established'] is not False:f.append('INHERITANCE')
 print('TP001_PUBLIC_BOUNDARY_CANDIDATE_CONFORMS_NOT_ADMITTED' if not f else 'TP001_PUBLIC_BOUNDARY_CANDIDATE_REJECTED')
 if f: print('\n'.join(f))
 return 1 if f else 0
if __name__=='__main__':raise SystemExit(main())
