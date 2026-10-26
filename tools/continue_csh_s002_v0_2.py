#!/usr/bin/env python3
"""CSH-S002 v0.2 continuation: carry the first response and attempt only units 2–24."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import shutil
import sys

import prepare_csh_s002_v0_1 as prep
import run_csh_s002_v0_1 as predecessor
import parse_csh_s002_response_v0_2 as successor
from run_csh_s002_v0_1 import durable_bytes, save, read, wire, analysis_rows

ROOT = Path(__file__).resolve().parents[1]
CONTINUATION = ROOT / 'docs/experiments/cross-system-claim-handoff-successor-002-v0.1/CONTINUATION_FREEZE_v0_2.json'
EVIDENCE = ROOT / 'docs/current-standing/CSH_S002_STOPPED_ATTEMPT_20261026'
ORIGINAL_FREEZE = '95857e56d8cf563fb313a439e85dfb40c4d9ae298dce9aee6c12e811a01b77c2'


def verify(expected=None):
    sha = prep.digest(CONTINUATION.read_bytes())
    if expected is not None and sha != expected:
        raise ValueError('continuation digest mismatch')
    freeze = read(CONTINUATION)
    for rel, digest in freeze['repository_bindings'].items():
        path = (ROOT / rel).resolve()
        if not path.is_relative_to(ROOT.resolve()) or prep.digest(path.read_bytes()) != digest:
            raise ValueError('continuation source binding mismatch')
    _, plan, _ = predecessor.verify(expected=ORIGINAL_FREEZE)
    ledger = read(EVIDENCE / 'ledger.json')
    first = plan['units'][0]
    if (ledger['status'] != 'STOPPED' or len(ledger['results']) != 1 or
            ledger['gross_committed_usd'] != '0.09' or ledger['known_corpus_cost_usd'] != '0.00059' or
            ledger['unknown_cost_requests'] != 0):
        raise ValueError('prior campaign mismatch')
    receipt = read(EVIDENCE / first['unit_id'] / 'receipt.json')
    if (receipt != ledger['results'][0] or receipt['unit_id'] != first['unit_id'] or
            receipt['status'] != 'FAIL' or receipt['errors'] != ['transfer_json_object'] or receipt['http_status'] != 200):
        raise ValueError('prior receipt mismatch')
    if (EVIDENCE / first['unit_id'] / 'request.json').read_bytes() != wire(first['request']):
        raise ValueError('prior request mismatch')
    data = read(EVIDENCE / first['unit_id'] / 'response.bin')
    result, text, parsed = successor.assess_response(data, first['request']['model'])
    if result['status'] != 'PASS' or result['actual_usd'] != '0.00059':
        raise ValueError('prior successor acceptance failed')
    if text.encode('utf-8') != (EVIDENCE / first['unit_id'] / 'output.txt').read_bytes():
        raise ValueError('prior extracted text mismatch')
    remaining = [{'unit_id': u['unit_id'], 'request_sha256': prep.digest(wire(u['request']))} for u in plan['units'][1:]]
    if len(remaining) != 23 or freeze['remaining_units'] != remaining:
        raise ValueError('continuation order mismatch')
    if freeze['budget'] != {'campaign_usd': '1.00', 'starting_gross_committed_usd': '0.09',
                           'per_request_reserved_usd': '0.03', 'remaining_reserved_usd': '0.69',
                           'planned_final_gross_usd': '0.78', 'prior_total_reported_usd': '0.00062'}:
        raise ValueError('continuation budget mismatch')
    carried = dict(receipt)
    carried.update(result, original_status='FAIL', original_errors=['transfer_json_object'],
                   acceptance_basis='OFFLINE_V0_2_REPARSE_OF_PRESERVED_FIRST_RESPONSE',
                   request_repeated=False, original_receipt_path='prior-attempt/' + first['unit_id'] + '/receipt.json')
    return freeze, plan, sha, carried


def verify_prior_output(prior_output):
    manifest = read(EVIDENCE / 'PRESERVATION_MANIFEST.json')['files']
    actual = {p.relative_to(prior_output).as_posix() for p in prior_output.rglob('*') if p.is_file()}
    if actual != set(manifest):
        raise ValueError('prior output population mismatch')
    for rel, digest in manifest.items():
        if prep.digest((prior_output / rel).read_bytes()) != digest:
            raise ValueError('prior output bytes mismatch')


def execute(out, expected, prior_output, client=None):
    freeze, plan, sha, carried = verify(expected)
    verify_prior_output(prior_output)
    owned = client is None
    if owned and not os.environ.get('PERPLEXITY_API_KEY'):
        return {'status': 'CREDENTIAL_UNAVAILABLE', 'request_attempted': False}
    if importlib.metadata.version('perplexityai') != '0.46.1':
        raise ValueError('SDK version mismatch; install requirements-perplexity-agent.txt')
    # An atomic, never-deleted claim blocks concurrent or later runs across output dirs.
    # Copies/checkouts/machines are outside this local enforcement boundary.
    if out.exists(): raise FileExistsError('output directory already exists')
    original_claim = ROOT / predecessor.CAMPAIGN
    claim_record = read(original_claim / 'claim.json')
    if (claim_record.get('freeze_sha256') != ORIGINAL_FREEZE or
            Path(claim_record.get('output_directory', '')).resolve() != prior_output.resolve() or
            claim_record.get('status') != 'CLAIMED_NO_AUTOMATIC_RESUME'):
        raise ValueError('original campaign claim mismatch')
    claim = original_claim / 'continuation-v0-2'
    claim.mkdir(exist_ok=False)
    save(claim / 'claim.json', {'freeze_sha256': sha, 'output_directory': str(out.resolve()),
                               'status': 'CLAIMED_NO_AUTOMATIC_RESUME'})
    out.mkdir(parents=True, exist_ok=False)
    durable_bytes(out / 'CONTINUATION_FREEZE.json', CONTINUATION.read_bytes())
    shutil.copytree(prior_output, out / 'prior-attempt')
    first = out / plan['units'][0]['unit_id']
    shutil.copytree(prior_output / plan['units'][0]['unit_id'], first)
    save(first / 'successor_acceptance.json', carried)
    ledger = {'freeze_sha256': sha, 'status': 'RUNNING', 'campaign_limit_usd': '1.00',
              'neutral_reserved_usd': '0.06', 'neutral_reported_usd': '0.00003',
              'gross_committed_usd': '0.09', 'results': [carried],
              'original_freeze_sha256': ORIGINAL_FREEZE,
              'prior_corpus_reported_usd': '0.00059',
              'carried_units': 1, 'new_request_limit': 23}
    save(out / 'ledger.json', ledger)
    from perplexity import Perplexity, APIStatusError
    for name in ('perplexity', 'httpx', 'httpcore'):
        logging.getLogger(name).setLevel(logging.WARNING)
    if owned:
        client = Perplexity(api_key=os.environ['PERPLEXITY_API_KEY'], base_url='https://api.perplexity.ai',
                            max_retries=0, timeout=60)
    # Injected clients are for offline tests; live CLI always constructs the pinned client.
    try:
        for u in plan['units'][1:]:
            reserved = Decimal(ledger['gross_committed_usd']) + Decimal('0.03')
            if reserved > Decimal('1.00'):
                raise ValueError('campaign admission budget exhausted')
            directory = out / u['unit_id']; directory.mkdir()
            expected_body = (predecessor.PACKAGE / 'requests' / (u['unit_id'] + '.json')).read_bytes()
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
                result, text, parsed = successor.assess_response(data, u['request']['model'])
                if parsed is not None:
                    save(directory / 'parsed_transfer.json', parsed)
                result.pop('corpus_continuation_enabled', None)
                receipt.update(result, http_status=raw.status_code, execution_phase='CONTINUATION_V0_2')
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
            for name in ('request.json', 'response.bin', 'output.txt', 'parsed_transfer.json'):
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
        return {'status': ledger['status'], 'new_requests_attempted': len(ledger['results']) - 1,
                'carried_units': 1,
                'known_corpus_cost_usd': ledger['known_corpus_cost_usd'],
                'unknown_cost_requests': ledger['unknown_cost_requests'],
                'gross_committed_usd': ledger['gross_committed_usd'], 'freeze_sha256': sha}
    finally:
        if owned: client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--prior-output-dir', type=Path)
    parser.add_argument('--expected-continuation-sha256')
    args = parser.parse_args()
    if args.live and not all((args.output_dir, args.prior_output_dir, args.expected_continuation_sha256)):
        parser.error('--live requires output-dir, prior-output-dir and expected-continuation-sha256')
    try:
        if args.live:
            result = execute(args.output_dir, args.expected_continuation_sha256, args.prior_output_dir)
        else:
            _, _, sha, _ = verify(args.expected_continuation_sha256)
            if args.prior_output_dir: verify_prior_output(args.prior_output_dir)
            result = {'status': 'VERIFIED_OFFLINE', 'remaining_requests': 23, 'carried_units': 1,
                      'continuation_sha256': sha, 'starting_gross_committed_usd': '0.09',
                      'planned_final_gross_usd': '0.78'}
        print(json.dumps(result, indent=2))
        return int(result['status'] not in ('VERIFIED_OFFLINE', 'COMPLETED_PENDING_CODING'))
    except Exception as exc:
        print(json.dumps({'status': 'BLOCKED', 'error_type': type(exc).__name__,
                          'action': 'Preserve all output and both campaign claims; no automatic retry or resume.'}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
