#!/usr/bin/env python3
import base64, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
M=json.loads((ROOT/'TRANSPORT_MANIFEST.json').read_text(encoding='utf-8'))
OUT=ROOT/'materialized'; OUT.mkdir(exist_ok=True)
def h(b): return hashlib.sha256(b).hexdigest()
errors=[]
for pkg in M['packages']:
 parts=[]
 for seg in pkg['segments']:
  p=ROOT/seg['path'].removeprefix('transport/')
  s=p.read_text(encoding='ascii')
  if len(s)!=seg['chars'] or h(s.encode('ascii'))!=seg['sha256_ascii']: errors.append(str(p))
  parts.append(s)
 joined=''.join(parts)
 try: raw=base64.b64decode(joined,validate=True)
 except Exception as e: errors.append(f"{pkg['filename']}: {e}"); continue
 if len(raw)!=pkg['bytes'] or h(raw)!=pkg['sha256']: errors.append(pkg['filename'])
 (OUT/pkg['filename']).write_bytes(raw)
if errors:
 print(json.dumps({'status':'FAIL','errors':errors},indent=2)); sys.exit(2)
print(json.dumps({'status':'PASS','packages':[{'filename':p['filename'],'sha256':p['sha256']} for p in M['packages']]},indent=2))
