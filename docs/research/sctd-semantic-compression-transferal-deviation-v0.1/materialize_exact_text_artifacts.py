#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/'ARTIFACT_RECONSTRUCTION_MANIFEST.json').read_text(encoding='utf-8'))
OUT=ROOT/'materialized'; errors=[]
def h(b): return hashlib.sha256(b).hexdigest()
for a in M['artifacts']:
    data=b''
    for c in a['chunks']:
        p=ROOT/c['path']
        b=p.read_bytes()
        if len(b)!=c['bytes'] or h(b)!=c['sha256']: errors.append(str(p))
        data += b
    if len(data)!=a['bytes'] or h(data)!=a['sha256']: errors.append(a['logical_path'])
    p=OUT/a['logical_path']; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(data)
if errors:
 print(json.dumps({'status':'FAIL','errors':errors},indent=2)); sys.exit(2)
print(json.dumps({'status':'PASS','artifacts':[{'path':a['logical_path'],'sha256':a['sha256']} for a in M['artifacts']]},indent=2))
