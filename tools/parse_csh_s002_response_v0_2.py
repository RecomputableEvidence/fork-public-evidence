#!/usr/bin/env python3
"""Offline CSH-S002 response parser successor; never sends or resumes requests."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

import run_csh_s002_v0_1 as predecessor
from preflight_csh_s001_receivers_v0_2 import strict_json
from prepare_csh_s002_v0_1 import digest

PARSER_ID = 'csh_s002_response_parser_v0.2'


def parse_transfer(text):
    """Accept a bare JSON object or one exact enclosing ```json code fence.

    Only surrounding JSON whitespace is ignored. Fence markers must occupy
    their own lines; the tag is exactly lowercase json. No prose extraction,
    JSON repair, duplicate-key acceptance, or concatenated-value acceptance.
    """
    if not isinstance(text, str): raise ValueError('text required')
    body = text.strip(' \t\r\n')
    form = 'bare_json'
    if body.startswith('```'):
        match = re.fullmatch(r'```json\r?\n(.*?)\r?\n```', body, flags=re.DOTALL)
        if match is None: raise ValueError('unsupported fence')
        body = match.group(1)
        form = 'single_json_fence'
    parsed = strict_json(body)
    if not isinstance(parsed, dict): raise ValueError('JSON object required')
    return parsed, form


def assess_response(data, expected_model):
    """Reuse every v0.1 acceptance check; replace only its JSON-text parser."""
    result, text = predecessor.assess(data, expected_model)
    errors = [e for e in result['errors'] if e != 'transfer_json_object']
    parsed = None
    form = None
    try:
        parsed, form = parse_transfer(text)
    except (ValueError, TypeError):
        errors.append('transfer_json_object')
    result.update(status='PASS' if not errors else 'FAIL', errors=sorted(set(errors)),
                  parser_id=PARSER_ID, parse_form=form,
                  research_standing='PENDING_HUMAN_CODING',
                  corpus_continuation_enabled=False)
    return result, text, parsed


def review(response_path, out, expected_model):
    """Preserve original response bytes before writing a separate derivation."""
    raw = response_path.read_bytes()
    out.mkdir(parents=True, exist_ok=False)
    predecessor.durable_bytes(out / 'response.bin', raw)
    try:
        data = strict_json(raw.decode('utf-8'))
        result, text, parsed = assess_response(data, expected_model)
    except (ValueError, TypeError, UnicodeDecodeError, AttributeError):
        result = {'status': 'FAIL', 'errors': ['response_structure'], 'parser_id': PARSER_ID,
                  'corpus_continuation_enabled': False, 'research_standing': 'UNASSESSED'}
        text, parsed = '', None
    predecessor.durable_bytes(out / 'output.txt', text.encode('utf-8'))
    result['raw_response_sha256'] = digest(raw)
    result['extracted_output_sha256'] = digest(text.encode('utf-8'))
    result['expected_model'] = expected_model
    result['scope'] = 'Offline response-body acceptance only; HTTP status and source provenance require the original receipt. No campaign status or human coding is changed.'
    if parsed is not None:
        predecessor.save(out / 'parsed_transfer.json', parsed)
        result['parsed_transfer_sha256'] = digest((out / 'parsed_transfer.json').read_bytes())
    predecessor.save(out / 'parser_receipt.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--response', type=Path, required=True)
    parser.add_argument('--expected-model', required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    result = review(args.response, args.output_dir, args.expected_model)
    print(json.dumps(result, indent=2))
    return int(result['status'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
