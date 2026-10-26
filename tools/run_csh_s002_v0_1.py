#!/usr/bin/env python3
"""Verify or execute the frozen 24-request CSH-S002 pilot (live is opt-in)."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import sys

import prepare_csh_s002_v0_1 as prep

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'docs/experiments/cross-system-claim-handoff-successor-002-v0.1/execution-v0.1'
CAMPAIGN = '.csh-s002-campaign-v0-1'


def wire(body):
    return json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def durable_bytes(path, data):
    """Replace a local record only after its bytes have been flushed to disk."""
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)
    if os.name != 'nt':
        fd = os.open(path.parent, os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)


def save(path, data):
    durable_bytes(path, (json.dumps(data, indent=2, ensure_ascii=True) + '\n').encode())


def read(path):
    return prep.strict_json(path.read_text(encoding='utf-8'))


def verify(package=PACKAGE, expected=None):
    freeze_path = package / 'FREEZE.json'
    sha = prep.digest(freeze_path.read_bytes())
    if expected is not None and sha != expected:
        raise ValueError('freeze digest mismatch')
    freeze = read(freeze_path)
    for rel, digest in freeze['repository_bindings'].items():
        p = (ROOT / rel).resolve()
        if not p.is_relative_to(ROOT.resolve()) or prep.digest(p.read_bytes()) != digest:
            raise ValueError('repository binding mismatch')
    for rel, digest in freeze['package_bindings'].items():
        p = (package / rel).resolve()
        if not p.is_relative_to(package.resolve()) or prep.digest(p.read_bytes()) != digest:
            raise ValueError('package binding mismatch')
    plan = read(package / 'PLAN.json')
    if plan != prep.plan(prep.candidate()):
        raise ValueError('frozen plan does not recompute')
    if len(plan['units']) != 24 or len({u['unit_id'] for u in plan['units']}) != 24:
        raise ValueError('unit population mismatch')
    if freeze['budget'] != {'campaign_usd': '1.00', 'prior_neutral_reserved_usd': '0.06',
                            'prior_neutral_reported_usd': '0.00003', 'per_request_usd': '0.03',
                            'corpus_reserved_usd': '0.72'}:
        raise ValueError('budget mismatch')
    for u in plan['units']:
        rel = 'requests/' + u['unit_id'] + '.json'
        if rel not in freeze['package_bindings'] or (package / rel).read_bytes() != wire(u['request']):
            raise ValueError('request byte mismatch')
    return freeze, plan, sha


def assess(data, model):
    errors = []
    if not isinstance(data, dict):
        return {'status': 'FAIL', 'errors': ['response_structure'], 'actual_usd': None}, ''
    if data.get('status') != 'completed' or data.get('error') or data.get('incomplete_details'):
        errors.append('completion_status')
    if data.get('model') != model: errors.append('model_identity')
    output = data.get('output')
    texts = []
    if not isinstance(output, list) or not output: errors.append('output_structure')
    for item in output if isinstance(output, list) else []:
        if not isinstance(item, dict):
            errors.append('output_structure'); continue
        if item.get('type') == 'reasoning': continue
        if item.get('type') != 'message':
            errors.append('unexpected_output_or_tool_activity'); continue
        if item.get('role') != 'assistant' or item.get('status') != 'completed':
            errors.append('message_structure')
        content = item.get('content')
        if not isinstance(content, list):
            errors.append('content_structure'); continue
        for part in content:
            if not isinstance(part, dict) or part.get('type') != 'output_text' or not isinstance(part.get('text'), str):
                errors.append('content_structure')
            else: texts.append(part['text'])
    text = ''.join(texts)
    try:
        if not isinstance(prep.strict_json(text), dict): raise ValueError('object required')
    except (ValueError, TypeError): errors.append('transfer_json_object')
    # No provider tool-choice attestation is inferred from the response echo.
    if data.get('tools') or data.get('search_results') or data.get('previous_response_id'):
        errors.append('unexpected_tools_or_history')
    usage = data.get('usage')
    usage = usage if isinstance(usage, dict) else {}
    actual = None
    try:
        cost = usage['cost']
        actual = Decimal(str(cost['total_cost']))
        if cost.get('currency') != 'USD' or not actual.is_finite() or actual < 0:
            raise ValueError('invalid cost')
    except (KeyError, TypeError, AttributeError, InvalidOperation, ValueError):
        actual = None; errors.append('cost_unavailable')
    if actual is not None and actual > Decimal('0.03'): errors.append('cost_above_reservation')
    details = usage.get('tool_calls_details')
    if details:
        if not isinstance(details, dict) or any(not isinstance(v, dict) or v.get('invocation', 0) != 0 for v in details.values()):
            errors.append('tool_usage')
    return {'status': 'PASS' if not errors else 'FAIL', 'errors': sorted(set(errors)),
            'actual_usd': str(actual) if actual is not None else None,
            'returned_model': data.get('model'), 'response_status': data.get('status'),
            'response_id': data.get('id'), 'returned_tool_choice': data.get('tool_choice')}, text


def analysis_rows(units, results):
    by_id = {r['unit_id']: r for r in results}
    return [{'receiver_run_id': u['unit_id'], 'pairing_key': f"S002-{u['scenario_id']}-{u['receiver']}-R1",
             'scenario_id': u['scenario_id'], 'receiver_class_id': u['receiver'],
             'condition': {'H0': 'control_h0', 'H1': 'instrumented_h1'}[u['condition']],
             'terminal_state': ('COMPLETED_PENDING_CODING' if by_id[u['unit_id']]['status'] == 'PASS' else 'EXECUTION_FAILED')
                if u['unit_id'] in by_id else 'NOT_ATTEMPTED',
             'task_state': None, 'classification': None} for u in units]


def execute(out, expected, client=None, package=PACKAGE):
    freeze, plan, sha = verify(package, expected)
    owned = client is None
    if owned and not os.environ.get('PERPLEXITY_API_KEY'):
        return {'status': 'CREDENTIAL_UNAVAILABLE', 'request_attempted': False}
    if importlib.metadata.version('perplexityai') != '0.46.1':
        raise ValueError('SDK version mismatch; install requirements-perplexity-agent.txt')
    # An atomic, never-deleted claim blocks concurrent or later runs across output dirs.
    # Copies/checkouts/machines are outside this local enforcement boundary.
    if out.exists(): raise FileExistsError('output directory already exists')
    claim = ROOT / CAMPAIGN
    claim.mkdir(exist_ok=False)
    save(claim / 'claim.json', {'freeze_sha256': sha, 'output_directory': str(out.resolve()),
                               'status': 'CLAIMED_NO_AUTOMATIC_RESUME'})
    out.mkdir(parents=True, exist_ok=False)
    durable_bytes(out / 'FREEZE.json', (package / 'FREEZE.json').read_bytes())
    ledger = {'freeze_sha256': sha, 'status': 'RUNNING', 'campaign_limit_usd': '1.00',
              'neutral_reserved_usd': '0.06', 'neutral_reported_usd': '0.00003',
              'gross_committed_usd': '0.06', 'results': []}
    save(out / 'ledger.json', ledger)
    from perplexity import Perplexity, APIStatusError
    for name in ('perplexity', 'httpx', 'httpcore'):
        logging.getLogger(name).setLevel(logging.WARNING)
    if owned:
        client = Perplexity(api_key=os.environ['PERPLEXITY_API_KEY'], base_url='https://api.perplexity.ai',
                            max_retries=0, timeout=60)
    # Injected clients are for offline tests; live CLI always constructs the pinned client.
    try:
        for u in plan['units']:
            reserved = Decimal(ledger['gross_committed_usd']) + Decimal('0.03')
            if reserved > Decimal('1.00'):
                raise ValueError('campaign admission budget exhausted')
            directory = out / u['unit_id']; directory.mkdir()
            expected_body = (package / 'requests' / (u['unit_id'] + '.json')).read_bytes()
            if expected_body != wire(u['request']): raise ValueError('request changed before send')
            durable_bytes(directory / 'intended_request.json', expected_body)
            receipt = {'unit_id': u['unit_id'], 'status': 'RESERVED_OUTCOME_UNKNOWN', 'reserved_usd': '0.03',
                       'started_at_utc': datetime.now(timezone.utc).isoformat(), 'actual_usd': None}
            ledger['gross_committed_usd'] = str(reserved)
            ledger['results'].append(receipt)
            # The reservation survives process termination and is never refunded for admission.
            save(out / 'ledger.json', ledger)
            save(directory / 'receipt.json', receipt)
            def capture(req):
                if str(req.url) != 'https://api.perplexity.ai/v1/responses' or req.method != 'POST' or req.content != expected_body:
                    raise ValueError('wire request differs from freeze')
                durable_bytes(directory / 'request.json', req.content)
            client._client.event_hooks['request'].append(capture)
            try:
                raw = client.responses.with_raw_response.create(**u['request'])
                durable_bytes(directory / 'response.bin', raw.http_response.content)
                data = prep.strict_json(raw.http_response.content.decode('utf-8'))
                result, text = assess(data, u['request']['model'])
                receipt.update(result, http_status=raw.status_code)
                if raw.status_code != 200:
                    receipt.update(status='FAIL', errors=['http_status'])
                durable_bytes(directory / 'output.txt', text.encode('utf-8'))
            except APIStatusError as exc:
                durable_bytes(directory / 'response.bin', exc.response.content)
                receipt.update(status='HTTP_ERROR', http_status=exc.status_code)
            except Exception as exc:
                receipt.update(status='EXECUTION_ERROR', error_type=type(exc).__name__)
            finally:
                client._client.event_hooks['request'].remove(capture)
            for name in ('request.json', 'response.bin', 'output.txt'):
                if (directory / name).exists(): receipt[name + '_sha256'] = prep.digest((directory / name).read_bytes())
            receipt['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
            save(directory / 'receipt.json', receipt)
            # Above-reservation observed costs are charged in full, then execution stops.
            if receipt.get('actual_usd') is not None:
                extra = max(Decimal(receipt['actual_usd']) - Decimal('0.03'), Decimal(0))
                ledger['gross_committed_usd'] = str(Decimal(ledger['gross_committed_usd']) + extra)
            save(out / 'ledger.json', ledger)
            save(out / 'analysis-pending.json', analysis_rows(plan['units'], ledger['results']))
            if receipt['status'] != 'PASS': break
        ledger['status'] = 'COMPLETED_PENDING_CODING' if len(ledger['results']) == 24 and all(r['status'] == 'PASS' for r in ledger['results']) else 'STOPPED'
        ledger['known_corpus_cost_usd'] = str(sum((Decimal(r['actual_usd']) for r in ledger['results'] if r.get('actual_usd') is not None), Decimal(0)))
        ledger['unknown_cost_requests'] = sum(r.get('actual_usd') is None for r in ledger['results'])
        save(out / 'ledger.json', ledger)
        save(out / 'coding-handoff.json', {'status': 'HUMAN_CODING_REQUIRED', 'freeze_sha256': sha,
             'instructions': 'Follow bound CODING_HANDOFF.md. Preserve raw output. Never substitute model self-labels for reviewed coding.',
             'units': [{'unit_id': r['unit_id'], 'raw_output_binding': {'path': r['unit_id'] + '/response.bin',
                        'sha256': r.get('response.bin_sha256')}, 'normalized_output': None, 'reviewer': None,
                        'adjudication': None} for r in ledger['results']]})
        return {'status': ledger['status'], 'attempted': len(ledger['results']),
                'known_corpus_cost_usd': ledger['known_corpus_cost_usd'],
                'unknown_cost_requests': ledger['unknown_cost_requests'],
                'gross_committed_usd': ledger['gross_committed_usd'], 'freeze_sha256': sha}
    finally:
        if owned: client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--expected-freeze-sha256')
    args = parser.parse_args()
    if args.live and (not args.output_dir or not args.expected_freeze_sha256):
        parser.error('--live requires --output-dir and --expected-freeze-sha256')
    try:
        if args.live:
            result = execute(args.output_dir, args.expected_freeze_sha256)
        else:
            _, plan, sha = verify(expected=args.expected_freeze_sha256)
            result = {'status': 'VERIFIED_OFFLINE', 'hosted_units': len(plan['units']), 'freeze_sha256': sha}
        print(json.dumps(result, indent=2))
        return int(result['status'] not in ('VERIFIED_OFFLINE', 'COMPLETED_PENDING_CODING'))
    except Exception as exc:
        # No exception body: provider/network exceptions can contain sensitive context.
        print(json.dumps({'status': 'BLOCKED', 'error_type': type(exc).__name__,
                          'action': 'Preserve output and campaign marker; inspect offline before any further attempt.'}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
