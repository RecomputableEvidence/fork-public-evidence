#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'12_PACKAGE_MANIFEST.json'
SUMS=ROOT/'SHA256SUMS'
CONTROL={'12_PACKAGE_MANIFEST.json','SHA256SUMS'}

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    failures=[]
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    declared={x['path'] for x in manifest['files']}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    if declared!=actual:
        failures.append({'code':'PACKAGE_FILE_SET_MISMATCH','missing_from_package':sorted(declared-actual),'undeclared_in_manifest':sorted(actual-declared)})
    for x in manifest['files']:
        p=ROOT/x['path']
        if not p.exists(): continue
        if x.get('sha256') is not None and sha256(p)!=x['sha256']:
            failures.append({'code':'MANIFEST_HASH_MISMATCH','path':x['path']})
        if x.get('bytes') is not None and p.stat().st_size!=x['bytes']:
            failures.append({'code':'MANIFEST_SIZE_MISMATCH','path':x['path']})
    lines=[ln.strip() for ln in SUMS.read_text(encoding='utf-8').splitlines() if ln.strip()]
    listed=set()
    for ln in lines:
        digest,path=ln.split('  ',1); listed.add(path)
        p=ROOT/path
        if not p.exists() or sha256(p)!=digest:
            failures.append({'code':'SHA256SUMS_MISMATCH','path':path})
    expected_sums=actual-{'SHA256SUMS'}
    if listed!=expected_sums:
        failures.append({'code':'SHA256SUMS_FILE_SET_MISMATCH','missing_from_sums':sorted(expected_sums-listed),'unexpected_in_sums':sorted(listed-expected_sums)})
    bad=[x for x in actual if x.endswith('.pyc') or '/__pycache__/' in '/'+x or x.startswith('__pycache__/')]
    if bad: failures.append({'code':'RUNTIME_BYTECODE_PRESENT','paths':sorted(bad)})
    report={'package_id':manifest['package_id'],'actual_file_count':len(actual),'manifest_declared_file_count':len(declared),'manifest_exhaustive':declared==actual,'sha256sums_expected_entry_count':len(expected_sums),'sha256sums_listed_entry_count':len(listed),'no_runtime_bytecode':not bad,'result':'PASS' if not failures else 'FAIL','failures':failures}
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
