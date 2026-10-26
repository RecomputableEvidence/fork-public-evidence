#!/usr/bin/env python3
"""Verify preserved S002 collection and prepare unscored human coding materials offline."""
from __future__ import annotations
import argparse
from collections import Counter
from decimal import Decimal
import json
from pathlib import Path
import re
import shutil

import continue_csh_s002_v0_2 as continuation
import parse_csh_s002_response_v0_2 as parser
import prepare_csh_s002_v0_1 as prep
import run_csh_s002_v0_1 as runner
import analyze_csh_s001_v0_1 as analyzer

ROOT = Path(__file__).resolve().parents[1]
COLLECTION = ROOT / 'docs/current-standing/CSH_S002_COLLECTION_20261026'
CONTINUATION_SHA = '31674682367761a325e1f03e94c65015a466ee01ce757f5289c6eb8ec8bd9ec3'


def load(path):
    return prep.strict_json(path.read_text(encoding='utf-8'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    prep.write(path, value)


def verify(collection=COLLECTION):
    manifest = load(collection / 'PRESERVATION_MANIFEST.json')
    raw = collection / 'raw'
    actual = {p.relative_to(raw).as_posix() for p in raw.rglob('*') if p.is_file()}
    if actual != set(manifest['files']) or len(actual) != manifest['member_count']:
        raise ValueError('collection member population mismatch')
    for rel, expected in manifest['files'].items():
        path = (raw / rel).resolve()
        if not path.is_relative_to(raw.resolve()) or prep.digest(path.read_bytes()) != expected:
            raise ValueError('collection member hash mismatch')
    _, plan, _, _ = continuation.verify(CONTINUATION_SHA)
    if (raw / 'CONTINUATION_FREEZE.json').read_bytes() != continuation.CONTINUATION.read_bytes():
        raise ValueError('continuation freeze mismatch')
    ledger = load(raw / 'ledger.json')
    units = plan['units']
    if [r['unit_id'] for r in ledger['results']] != [u['unit_id'] for u in units]:
        raise ValueError('unit population or order mismatch')
    if ledger['freeze_sha256'] != CONTINUATION_SHA or ledger['original_freeze_sha256'] != continuation.ORIGINAL_FREEZE:
        raise ValueError('ledger freeze mismatch')
    prior_manifest = load(continuation.EVIDENCE / 'PRESERVATION_MANIFEST.json')
    for rel, digest in prior_manifest['files'].items():
        if prep.digest((raw / 'prior-attempt' / rel).read_bytes()) != digest:
            raise ValueError('predecessor preservation mismatch')
    rows = []; recorded_hashes = 0; total = Decimal(0)
    for index, (unit, receipt) in enumerate(zip(units, ledger['results'])):
        directory = raw / unit['unit_id']
        expected_request = runner.wire(unit['request'])
        if (directory / 'request.json').read_bytes() != expected_request or (directory / 'intended_request.json').read_bytes() != expected_request:
            raise ValueError('frozen request byte mismatch')
        for name in ('request.json', 'response.bin', 'output.txt', 'parsed_transfer.json'):
            key = name + '_sha256'
            if key in receipt:
                if prep.digest((directory / name).read_bytes()) != receipt[key]:
                    raise ValueError('receipt hash mismatch')
                recorded_hashes += 1
        response = load(directory / 'response.bin')
        result, text, parsed = parser.assess_response(response, unit['request']['model'])
        for key in ('status', 'errors', 'actual_usd', 'returned_model', 'response_status', 'response_id'):
            if result[key] != receipt[key]: raise ValueError('receipt assessment mismatch')
        if receipt['http_status'] != 200 or (directory / 'output.txt').read_bytes() != text.encode('utf-8'):
            raise ValueError('capture mismatch')
        if index:
            if load(directory / 'receipt.json') != receipt: raise ValueError('unit receipt mismatch')
            if parsed is not None and load(directory / 'parsed_transfer.json') != parsed:
                raise ValueError('parsed derivative mismatch')
        else:
            if load(directory / 'successor_acceptance.json') != receipt:
                raise ValueError('carried successor receipt mismatch')
            for p in (continuation.EVIDENCE / unit['unit_id']).iterdir():
                if (directory / p.name).read_bytes() != p.read_bytes():
                    raise ValueError('carried original bytes mismatch')
        total += Decimal(receipt['actual_usd'])
        rows.append({'unit_id':unit['unit_id'], 'receiver':unit['receiver'], 'scenario_id':unit['scenario_id'],
                     'condition':unit['condition'], 'parser_status':receipt['status'], 'errors':receipt['errors'],
                     'model':receipt['returned_model'], 'response_id':receipt['response_id'],
                     'raw_response_sha256':receipt['response.bin_sha256'],
                     'output_sha256':receipt['output.txt_sha256'], 'reported_usd':receipt['actual_usd']})
    if (str(total) != ledger['known_corpus_cost_usd'] or ledger['gross_committed_usd'] != '0.78' or
            ledger['unknown_cost_requests'] != 0 or ledger['status'] != 'STOPPED'):
        raise ValueError('ledger reconciliation mismatch')
    if Counter(r['parser_status'] for r in rows) != {'PASS':23, 'FAIL':1} or rows[-1]['errors'] != ['transfer_json_object']:
        raise ValueError('observed disposition mismatch')
    if load(raw / 'analysis-pending.json') != runner.analysis_rows(units, ledger['results']):
        raise ValueError('pending analysis mismatch')
    summary = {'status':'VERIFIED_COLLECTION', 'planned_units':24, 'unique_requests_captured':24,
               'new_continuation_requests':23, 'carried_units':1, 'parser_accepted':23, 'parser_rejected':1,
               'all_http_200_and_completed':True, 'recorded_file_hashes_verified':recorded_hashes,
               'preserved_archive_members':len(actual), 'known_corpus_cost_usd':str(total),
               'including_neutral_reported_usd':str(total + Decimal(ledger['neutral_reported_usd'])),
               'gross_reserved_usd':ledger['gross_committed_usd'], 'unknown_cost_requests':0,
               'campaign_ledger_status':'STOPPED', 'research_scores_assigned':0,
               'boundary':'Collection is complete; grammar acceptance and semantic coding are separate. Returned identities are strings, not model attestations.'}
    return summary, units, rows


def examine_final(raw_text):
    """Separate offline extraction; never changes the executed parser or its FAIL."""
    text = raw_text.decode('utf-8')
    openings = list(re.finditer(r'^```json\r?$', text, re.MULTILINE))
    closings = list(re.finditer(r'^```\r?$', text, re.MULTILINE))
    if len(openings) != 1 or len(closings) != 1 or openings[0].end() >= closings[0].start():
        raise ValueError('ambiguous offline extraction')
    start = openings[0].end()
    if text[start:start+1] != '\n': raise ValueError('opening fence newline required')
    start += 1; end = closings[0].start()
    body = text[start:end]
    parsed = prep.strict_json(body)
    if not isinstance(parsed, dict): raise ValueError('object required')
    return {'method':'OFFLINE_SINGLE_FENCE_EXAMINATION_v0.1',
            'source_output_sha256':prep.digest(raw_text),
            'body_utf8_start':len(text[:start].encode('utf-8')), 'body_utf8_end':len(text[:end].encode('utf-8')),
            'prefix_text':text[:openings[0].start()], 'suffix_text':text[closings[0].end():],
            'body_sha256':prep.digest(body.encode('utf-8')), 'parsed_object':parsed,
            'original_parser_status':'FAIL', 'primary_eligibility_changed':False,
            'human_review':'Review the entire response, including prefix. Do not equate extracted JSON with the whole answer.'}


def prepare(out, collection=COLLECTION):
    summary, units, rows = verify(collection)
    out.mkdir(parents=True, exist_ok=False)
    raw = collection / 'raw'
    save(out / 'COLLECTION_VERIFICATION.json', summary)
    save(out / 'coordinator' / 'EXECUTION_INVENTORY.json', rows)
    save(out / 'analysis' / 'PRIMARY_PENDING.json', load(raw / 'analysis-pending.json'))
    save(out / 'analysis' / 'UNSCORED_SUMMARY.json', analyzer.summarize(load(raw / 'analysis-pending.json')))
    final_id = units[-1]['unit_id']
    final_raw = (raw / final_id / 'output.txt').read_bytes()
    examination = examine_final(final_raw)
    save(out / 'final-response' / 'EXAMINATION.json', examination)
    (out / 'final-response' / 'output.txt').write_bytes(final_raw)
    save(out / 'final-response' / 'extracted_object.json', examination['parsed_object'])
    ordered = sorted(units, key=lambda u:prep.digest(('S002-coding-order-v1:' + u['unit_id']).encode()))
    key = []
    for i, unit in enumerate(ordered, 1):
        code = f'C{i:03d}'
        row = next(r for r in rows if r['unit_id'] == unit['unit_id'])
        packet = prep.strict_json(unit['request']['input'].split('\n', 1)[1])
        directory = out / 'coder-packets' / code; directory.mkdir(parents=True)
        source = packet['source_artifact']
        save(directory / 'source.json', {'workflow_task':packet['workflow_task'], 'source_artifact':source})
        output = (raw / unit['unit_id'] / 'output.txt').read_bytes()
        (directory / 'output.txt').write_bytes(output)
        template = {'coding_id':code, 'status':'PENDING_HUMAN_CODING', 'normalization_run_id':None,
                    'coder_id':None, 'coding_timestamp_utc':None,
                    'output_sha256':prep.digest(output), 'raw_response_sha256':row['raw_response_sha256'],
                    'source_sha256':prep.digest((directory / 'source.json').read_bytes()),
                    'task_state':None, 'claim_segmentation':None,
                    'normalized_output':{k:None for k in ('downstream_claims','preserved_non_claims','reference_resolutions',
                        'authority_inherited','evidence_promotions','verification_upgrades','aggregate_state')},
                    'boundary_contracts':None, 'semantic_label_evidence_spans':None,
                    'non_claim_survival_mappings':None, 'uncertainty':None,
                    'residual_unblinding':None, 'reviewer_notes':None}
        save(out / 'coder-1-templates' / (code+'.json'), template)
        save(out / 'coder-2-templates' / (code+'.json'), template)
        save(out / 'adjudication-templates' / (code+'.json'),
             {'coding_id':code,'status':'PENDING','coder_1_record_sha256':None,'coder_2_record_sha256':None,
              'adjudicator_id':None,'timestamp_utc':None,'disagreements':None,'resolution_with_evidence':None,
              'primary_eligibility':None,'final_normalization_binding':None})
        # Coordinator-only skeleton; intentionally invalid until all semantic fields are reviewed.
        skeleton={'receiver_run_id':unit['unit_id'],'classification_run_id':None,
                  'classification_method_id':'fork_deterministic_unsupported_inheritance_s001_v0_1',
                  'scenario':source,'condition':{'H0':'control_h0','H1':'instrumented_h1'}[unit['condition']],
                  'raw_output_binding':{'path':(raw / unit['unit_id'] / 'response.bin').relative_to(ROOT).as_posix(),
                                        'sha256':row['raw_response_sha256']},
                  'task_state':None,'boundary_contracts':None,'normalized_output':template['normalized_output']}
        save(out / 'coordinator' / 'classifier-skeletons' / (code+'.json'), skeleton)
        key.append({'coding_id':code,**row,'primary_grammar_eligible':row['parser_status']=='PASS',
                    'note':'Final unit may receive separate exploratory examination; never silently include it in the frozen-grammar primary population.' if row['parser_status']=='FAIL' else None})
    save(out / 'coordinator' / 'CODING_KEY.json', key)
    bindings={p.relative_to(out).as_posix():prep.digest(p.read_bytes()) for p in sorted(out.rglob('*'), key=lambda p: p.relative_to(out).as_posix()) if p.is_file()}
    save(out / 'MATERIALS_MANIFEST.json', {'generator':'tools/prepare_csh_s002_coding_v0_1.py',
          'generator_sha256':prep.digest(Path(__file__).read_bytes()),
          'source_manifest_sha256':prep.digest((collection / 'PRESERVATION_MANIFEST.json').read_bytes()),
          'files':bindings,'boundary':'Generated materials have no completed human coding or semantic scores.'})
    return summary


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path)
    args=p.parse_args()
    result=prepare(args.output_dir) if args.output_dir else verify()[0]
    print(json.dumps(result,indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
