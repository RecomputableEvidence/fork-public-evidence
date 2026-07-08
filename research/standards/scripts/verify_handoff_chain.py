#!/usr/bin/env python3
from __future__ import annotations
import json, hashlib, sys
from pathlib import Path

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))

def canon_without_hash(obj: dict) -> bytes:
    x = dict(obj)
    x.pop('receipt_sha256', None)
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

def main() -> int:
    standards = Path(__file__).resolve().parents[1]
    manifest_path = standards / 'handoff-chain/HANDOFF_CHAIN_MANIFEST_v0_1.json'
    manifest = load(manifest_path)
    prev = None
    head = None
    for expected, item in enumerate(manifest['receipts']):
        rpath = standards / item['path']
        if not rpath.exists():
            print(f'ERROR missing receipt: {rpath}', file=sys.stderr)
            return 1
        r = load(rpath)
        if r.get('sequence') != expected:
            print(f'ERROR sequence mismatch: {rpath}', file=sys.stderr)
            return 1
        rh = sha256(canon_without_hash(r))
        if rh != r.get('receipt_sha256'):
            print(f'ERROR receipt hash mismatch: {rpath}', file=sys.stderr)
            return 1
        if item.get('receipt_sha256') != rh:
            print(f'ERROR manifest receipt hash mismatch: {rpath}', file=sys.stderr)
            return 1
        if r.get('previous_receipt_sha256') != prev:
            print(f'ERROR chain link mismatch: {rpath}', file=sys.stderr)
            return 1
        if r.get('document_path'):
            dpath = standards / r['document_path']
            if not dpath.exists():
                print(f'ERROR missing document: {dpath}', file=sys.stderr)
                return 1
            data = dpath.read_bytes()
            dh = sha256(data)
            if dh != r.get('document_sha256'):
                print(f'ERROR document hash mismatch: {dpath}', file=sys.stderr)
                return 1
            expected_bytes = r.get('document_bytes')
            if expected_bytes is not None and expected_bytes != len(data):
                print(f'ERROR document byte-count mismatch: {dpath}', file=sys.stderr)
                return 1
        prev = rh
        head = rh
    if manifest.get('chain_head_sha256') != head:
        print('ERROR chain head mismatch', file=sys.stderr)
        return 1
    print('Fork handoff chain verification: PASS')
    print(f'Receipts verified: {len(manifest["receipts"])}')
    print(f'Chain head: {head}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
