#!/usr/bin/env python3
"""Read-only verification of FPCF-002 public preservation release, Python 3.11+."""
import sys, json, hashlib, zipfile, pathlib

def main(path):
    p=pathlib.Path(path)
    with zipfile.ZipFile(p) as z:
        names=z.namelist()
        assert len(names)==len(set(names)), 'duplicate names'
        assert all(not n.startswith('/') and not any(x in ('..','') for x in pathlib.PurePosixPath(n).parts) and '\\' not in n for n in names), 'unsafe paths'
        m=json.loads(z.read('MANIFEST.json'))
        expected=set(m['objects'])|{'MANIFEST.json'}
        assert set(names)==expected, 'wrong member population'
        for name,v in m['objects'].items():
            b=z.read(name)
            assert len(b)==v['byte_length'] and hashlib.sha256(b).hexdigest()==v['sha256'], name
        orig=[k for k in m['objects'] if k.startswith('originals/')]
        print(json.dumps({'status':'PASS','checked':len(m['objects']),'preserved_originals':len(orig),'zip_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'INTERNAL_MANIFEST_ONLY; VERIFY OUTER SHA256 AGAINST PUBLIC GITHUB PIN'},sort_keys=True))
if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python verify_public_release.py <FPCF-002-PUBLIC.zip>')
    main(sys.argv[1])