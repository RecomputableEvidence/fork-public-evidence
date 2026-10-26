#!/usr/bin/env python3
"""Strict, opt-in neutral preflight; predecessor remains unchanged."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
import urllib.error
import urllib.request

from preflight_csh_s001_receivers_v0_1 import CONFIGS

# Exact identities only. Aliases require a separately reviewed policy change.
PERMITTED_MODELS = {provider: (config['model'],) for provider, config in CONFIGS.items()}
EXPECTED_CONTENT = {'preflight': 'ok'}


def strict_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON member')
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('non-JSON numeric constant')
    return json.loads(data, object_pairs_hook=unique, parse_constant=invalid_constant)


def assess_response(provider, http_status, raw):
    """Total disposition for JSON shape/content errors, without promoting identity claims."""
    if provider not in PERMITTED_MODELS:
        raise ValueError('unknown provider')
    result = {'status': 'RESPONSE_INCOMPATIBLE', 'http_status': http_status,
              'response_sha256': hashlib.sha256(raw).hexdigest(), 'errors': []}
    if http_status != 200:
        result.update(status='HTTP_ERROR', errors=['http_status'])
        return result
    try:
        parsed = strict_json(raw.decode('utf-8'))
    except (ValueError, UnicodeError):
        result.update(status='RESPONSE_NOT_JSON', errors=['response_json'])
        return result
    errors = result['errors']
    if not isinstance(parsed, dict):
        errors.append('response_object')
        return result
    model = parsed.get('model')
    result['returned_model'] = model if isinstance(model, str) else None
    if not isinstance(model, str) or model not in PERMITTED_MODELS[provider]:
        errors.append('model_identity')
    choices = parsed.get('choices')
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        errors.append('single_choice_object')
        return result
    choice = choices[0]
    if choice.get('finish_reason') != 'stop':
        errors.append('completion_status')
    message = choice.get('message')
    if not isinstance(message, dict):
        errors.append('message_object')
        return result
    if message.get('role') != 'assistant':
        errors.append('assistant_role')
    if message.get('refusal') not in (None, '') or message.get('tool_calls'):
        errors.append('non_text_response')
    content = message.get('content')
    if not isinstance(content, str):
        errors.append('content_string')
    else:
        try:
            if strict_json(content) != EXPECTED_CONTENT:
                errors.append('expected_content')
        except ValueError:
            errors.append('content_json')
    if not errors:
        result['status'] = 'PASS'
    return result


def call(provider, output_dir, timeout=45, opener=None):
    """One live request at most, no retries; preserve exact request/response bytes."""
    config = CONFIGS[provider]
    directory = Path(output_dir) / provider
    directory.mkdir(parents=True, exist_ok=False)
    request_bytes = json.dumps(config['payload'], separators=(',', ':')).encode('utf-8')
    (directory / 'request.json').write_bytes(request_bytes)
    result = {'provider': provider, 'requested_model': config['model'],
              'permitted_returned_models': list(PERMITTED_MODELS[provider]),
              'endpoint': config['endpoint'], 'started_at_utc': datetime.now(timezone.utc).isoformat(),
              'request_sha256': hashlib.sha256(request_bytes).hexdigest(),
              'contains_csh_corpus': False, 'request_attempted': False,
              'identity_scope': 'exact returned string match; not provider/model attestation'}
    key = os.environ.get(config['env'])
    if not key:
        result['status'] = 'CREDENTIAL_UNAVAILABLE'
    else:
        request = urllib.request.Request(config['endpoint'], data=request_bytes, method='POST',
            headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
        result['request_attempted'] = True
        try:
            with (opener or urllib.request.urlopen)(request, timeout=timeout) as response:
                raw = response.read()
                status = response.status
        except urllib.error.HTTPError as exc:
            raw, status = exc.read(), exc.code
        except Exception as exc:
            # Exception text may echo credentials; preserve only its class.
            result.update(status='EXECUTION_ERROR', error_type=type(exc).__name__)
        else:
            result.update(assess_response(provider, status, raw))
            (directory / 'response.bin').write_bytes(raw)
        if 'raw' in locals() and 'status' not in result:
            result.update(assess_response(provider, status, raw))
            (directory / 'response.bin').write_bytes(raw)
    result['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
    (directory / 'receipt.json').write_bytes((json.dumps(result, indent=2) + '\n').encode('utf-8'))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true', help='Explicitly permit neutral provider calls')
    parser.add_argument('--provider', choices=sorted(CONFIGS), action='append')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if not args.live:
        print(json.dumps({'status': 'NOT_EXECUTED', 'reason': 'explicit --live required',
                          'permitted_models': PERMITTED_MODELS}, indent=2))
        return 2
    if args.output_dir is None or not args.provider:
        parser.error('--live requires --provider and --output-dir')
    args.output_dir.mkdir(parents=True, exist_ok=False)
    results = [call(p, args.output_dir) for p in dict.fromkeys(args.provider)]
    print(json.dumps(results, indent=2))
    return int(any(r['status'] != 'PASS' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
