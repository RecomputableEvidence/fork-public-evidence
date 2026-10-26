#!/usr/bin/env python3
"""Prepare the CSH-S002 pilot offline; opt-in neutral calls only, never corpus execution."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import logging
import os
from pathlib import Path
import tempfile

from build_csh_s001_packets_v0_1 import build, SCENARIOS
from check_csh_s001_packet_binding_v0_2 import evaluate
from preflight_csh_s001_receivers_v0_2 import strict_json

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'docs/experiments/cross-system-claim-handoff-successor-002-v0.1/CANDIDATE_v0_1.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.write_bytes((json.dumps(data, indent=2, ensure_ascii=True) + '\n').encode())


def candidate():
    c = strict_json(CANDIDATE.read_text())
    for name, expected in c['source_bindings'].items():
        if digest((ROOT / name).read_bytes()) != expected:
            raise ValueError('predecessor source binding mismatch')
    return c


def request(c, receiver, content):
    return {'model': receiver['model'], 'input': content,
            'max_output_tokens': c['max_output_tokens'], **c['request_settings']}


def plan(c):
    with tempfile.TemporaryDirectory() as temp:
        packets = Path(temp)
        m = build(ROOT, packets)
        if evaluate(ROOT, packets)['status'] != 'PASS':
            raise ValueError('source packet verification failed')
        records = {r['scenario_id']: r for r in m['records']}
        pairs = [(s, r) for s in SCENARIOS for r in c['receivers']]
        pairs.sort(key=lambda p: digest((c['order_seed'] + p[0] + p[1]['id']).encode()))
        units = []
        for pair_index, (sid, receiver) in enumerate(pairs):
            conditions = [('H0', 'control_packet'), ('H1', 'instrumented_packet')]
            if pair_index % 2:
                conditions.reverse()
            for condition, role in conditions:
                packet = (packets / records[sid][role]['path']).read_bytes()
                content = ('Perform the workflow_task using only the supplied packet. '
                           'Do not retrieve external information. Return your transfer record as JSON.\n'
                           + packet.decode('utf-8'))
                body = request(c, receiver, content)
                units.append({'unit_id': f'S002-{sid}-{receiver["id"]}-{condition}-R1',
                              'scenario_id': sid, 'receiver': receiver['id'], 'condition': condition,
                              'source_packet_sha256': digest(packet), 'request': body,
                              'input_utf8_bytes': len(content.encode())})
    estimated = sum((Decimal(u['input_utf8_bytes'] + 2048) * Decimal('0.10') +
                     Decimal(c['max_output_tokens']) * Decimal('0.50')) / Decimal(1000000)
                    for u in units)
    return {'experiment_id': c['experiment_id'], 'status': 'CANDIDATE_NOT_FROZEN',
            'candidate_sha256': digest(CANDIDATE.read_bytes()), 'units': units,
            'hosted_units': len(units), 'nominal_token_cost_usd': str(estimated),
            'estimate_basis': 'Input UTF-8 bytes plus 2048-token overhead assumption, output cap, low-context published rates; excludes unreported overhead/cache charges and is not a billing guarantee.',
            'reserved_corpus_allowance_usd': str(len(units) * Decimal(c['budget']['corpus_reservation_usd_per_request'])),
            'corpus_execution_enabled': False}


def assess(c, receiver, status, response):
    data = response.model_dump(mode='json')
    errors = []
    if status != 200: errors.append('http_status')
    if data.get('status') != 'completed' or data.get('error') or data.get('incomplete_details'):
        errors.append('completion_status')
    if data.get('model') != receiver['model']: errors.append('model_identity')
    for item in data.get('output') or []:
        if item.get('type') == 'message' and (item.get('role') != 'assistant' or item.get('status') != 'completed'):
            errors.append('message_structure')
        if item.get('type') not in ('message', 'reasoning'):
            errors.append('unexpected_output_or_tool_activity')
    try:
        if strict_json(response.output_text) != {'preflight': 'ok'}:
            errors.append('expected_content')
    except (ValueError, TypeError):
        errors.append('expected_content')
    usage = data.get('usage') or {}
    cost = usage.get('cost') or {}
    try:
        actual = Decimal(str(cost['total_cost']))
        if cost.get('currency') != 'USD' or not actual.is_finite() or actual < 0:
            raise ValueError('cost')
        if actual > Decimal(c['budget']['neutral_reservation_usd_per_request']):
            errors.append('cost_above_reservation')
        if any((v or {}).get('invocation', 0) for v in (usage.get('tool_calls_details') or {}).values()):
            errors.append('tool_usage')
    except (KeyError, ValueError, InvalidOperation):
        actual = None
        errors.append('cost_unavailable')
    return {'status': 'PASS' if not errors else 'FAIL', 'errors': sorted(set(errors)),
            'returned_model': data.get('model'), 'response_id': data.get('id'),
            'response_status': data.get('status'), 'actual_usd': str(actual) if actual is not None else None}


def neutral(c, out, client=None):
    """One fresh, two-request qualification batch; stop on first unsuccessful result."""
    out.mkdir(parents=True, exist_ok=False)
    owned = client is None
    if owned and not os.environ.get('PERPLEXITY_API_KEY'):
        result = {'status': 'CREDENTIAL_UNAVAILABLE', 'request_attempted': False}
        write(out / 'batch.json', result)
        return result
    from perplexity import Perplexity, APIStatusError
    for name in ('perplexity', 'httpx', 'httpcore'):
        logging.getLogger(name).setLevel(logging.WARNING)
    if owned:
        client = Perplexity(api_key=os.environ['PERPLEXITY_API_KEY'], base_url='https://api.perplexity.ai',
                            max_retries=0, timeout=60)
    results = []
    try:
        for receiver in c['receivers']:
            directory = out / receiver['id']; directory.mkdir()
            body = request(c, receiver, 'Return JSON only: {"preflight":"ok"}')
            write(directory / 'intended_request.json', body)
            receipt = {'receiver': receiver['id'], 'requested_model': receiver['model'],
                       'candidate_sha256': digest(CANDIDATE.read_bytes()),
                       'started_at_utc': datetime.now(timezone.utc).isoformat(),
                       'reserved_usd': c['budget']['neutral_reservation_usd_per_request'],
                       'status': 'RESERVED_OUTCOME_UNKNOWN', 'contains_csh_corpus': False}
            write(directory / 'receipt.json', receipt)
            def capture(req):
                (directory / 'request.json').write_bytes(req.content)
            client._client.event_hooks['request'].append(capture)
            try:
                raw = client.responses.with_raw_response.create(**body)
                (directory / 'response.bin').write_bytes(raw.http_response.content)
                receipt.update(http_status=raw.status_code, **assess(c, receiver, raw.status_code, raw.parse()))
            except APIStatusError as exc:
                (directory / 'response.bin').write_bytes(exc.response.content)
                receipt.update(status='HTTP_ERROR', http_status=exc.status_code)
            except Exception as exc:
                receipt.update(status='EXECUTION_ERROR', error_type=type(exc).__name__)
            finally:
                client._client.event_hooks['request'].remove(capture)
            for name in ('request.json', 'response.bin'):
                if (directory / name).exists():
                    receipt[name + '_sha256'] = digest((directory / name).read_bytes())
            receipt['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
            write(directory / 'receipt.json', receipt)
            results.append(receipt)
            if receipt['status'] != 'PASS': break
    finally:
        if owned: client.close()
    result = {'status': 'PASS' if len(results) == 2 and all(r['status'] == 'PASS' for r in results) else 'BLOCKED',
              'results': results, 'corpus_execution_enabled': False}
    write(out / 'batch.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--neutral-live', action='store_true')
    args = parser.parse_args()
    c = candidate()
    if args.neutral_live:
        result = neutral(c, args.output_dir)
        print(json.dumps(result, indent=2))
        return int(result['status'] != 'PASS')
    result = plan(c)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    write(args.output_dir / 'PLAN.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'units'}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
