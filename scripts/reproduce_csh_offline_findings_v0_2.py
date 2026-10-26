#!/usr/bin/env python3
"""Reproduce predecessor weaknesses using mocks and temporary packet copies only."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import preflight_csh_s001_receivers_v0_1 as old
import build_csh_s001_packets_v0_1 as builder
import check_csh_s001_packet_binding_v0_2 as successor
RECORD = ROOT / 'docs/current-standing/CSH_OFFLINE_FINDINGS_20261026.json'


def examine():
    rows = []
    for provider in ('groq', 'deepseek'):
        model = old.CONFIGS[provider]['model']
        def response(content, returned=model, finish='stop'):
            return {'model': returned, 'choices': [{'finish_reason': finish,
                    'message': {'role': 'assistant', 'content': content}}]}
        cases = {
            'expected': response('{"preflight":"ok"}'),
            'wrong_content': response('{}'),
            'length_finish': response('{"preflight":"ok"}', finish='length'),
            'substring_identity': response('{"preflight":"ok"}', returned='not-'+model),
            'missing_output': {'model': model},
            'array_response': [],
            'bad_json': b'not-json',
        }
        for name, payload in cases.items():
            raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            context = MagicMock()
            context.__enter__.return_value.status = 200
            context.__enter__.return_value.read.return_value = raw
            with patch.dict(os.environ, {old.CONFIGS[provider]['env']: 'dummy-only'}, clear=True), \
                 patch.object(old.urllib.request, 'urlopen', return_value=context):
                try:
                    status = old.call(provider)['status']
                except Exception as exc:
                    status = 'UNCAUGHT_' + type(exc).__name__
            rows.append({'provider': provider, 'case': name, 'response_utf8': raw.decode(),
                         'observed_predecessor_status': status})
    with tempfile.TemporaryDirectory() as directory:
        candidate = Path(directory)
        manifest = builder.build(ROOT, candidate)
        target = candidate / manifest['records'][0]['projection']['path']
        target.write_bytes(target.read_bytes()+b' ')
        result = subprocess.run([sys.executable, str(ROOT/'tools/check_csh_s001_packet_binding_v0_1.py'),
            str(candidate), '--root', str(ROOT), '--json'], capture_output=True, check=True)
        original_result = json.loads(result.stdout)
        tamper = {'mutation': 'append one ASCII space to first projection; leave declared hashes unchanged',
                  'predecessor_failed_checks': original_result['failed'],
                  'successor_status': successor.evaluate(ROOT, candidate)['status']}
    paths = ['tools/preflight_csh_s001_receivers_v0_1.py',
             'tools/check_csh_s001_packet_binding_v0_1.py']
    return {'kind': 'offline_mock_and_temporary_file_observation', 'hosted_requests': 0,
            'predecessor_source_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            'preflight_observations': rows, 'packet_tamper_observation': tamper,
            'boundary': 'No provider behavior or CSH hypothesis tested; candidate acceptance contract is stricter than predecessor.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    observed = examine()
    if args.check:
        expected = json.loads(RECORD.read_text(encoding='utf-8'))
        matches = observed == expected
        print(json.dumps({'record_matches': matches, 'hosted_requests': 0}))
        return int(not matches)
    if RECORD.exists():
        raise SystemExit('Refusing to overwrite existing observation')
    RECORD.write_bytes((json.dumps(observed, indent=2)+'\n').encode())
    print('Preserved '+str(RECORD))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
