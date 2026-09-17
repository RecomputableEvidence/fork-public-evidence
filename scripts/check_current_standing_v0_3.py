#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_2.json'
V3 = ROOT / 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_3.json'
ADMISSION = ROOT / 'admissions/LENS-SHIFT-v0.1/BLIND-EPOCH-003'
CLOSURE = ADMISSION / 'BLIND-EPOCH-003-CLOSURE-VERIFICATION.json'
FIRST = ADMISSION / 'FIRST_EXECUTION_RESULT.jsonl'
ORACLE = ADMISSION / 'ORACLE_COMPARISON.jsonl'
RECEIPT = ROOT / 'docs/current-standing/LENS_SHIFT_v0_1_BLIND_EPOCH_003_ADMISSION_MERGE_RECEIPT_2026_09_17.md'

EXPECTED_ID = 'LENS_SHIFT_PROTOCOL_v0_1'
EXPECTED_MERGE = '816431ec6479418680837a9a3b685d74b36d8fb3'
EXPECTED_MATERIAL = 'TERMINAL_NATIVE_RECORDS_ADMITTED__FROZEN_REVIEWER_PACKAGE_EPOCH002_AND_HARNESS_ARCHIVES_HASH_BOUND_NOT_ADMITTED'
EXPECTED_QUAL = 'QUALIFIED_WITHIN_BLIND_EPOCH_003_DECLARED_24_PROBE_SCOPE'
EXPECTED_BLIND = 'PASS_24_OF_24_WITHIN_FROZEN_SCOPE'


def fail(message: str) -> None:
    print('FAIL:', message)
    raise SystemExit(1)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'{path.relative_to(ROOT)} invalid JSON: {exc}')


def load_jsonl(path: Path):
    try:
        return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    except Exception as exc:
        fail(f'{path.relative_to(ROOT)} invalid JSONL: {exc}')


def main() -> int:
    v2, v3 = load(V2), load(V3)
    if v3.get('record_form') != 'PREDECESSOR_PLUS_DELTA': fail('v0.3 is not predecessor-plus-delta')
    if v3.get('predecessor_register') != 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_2.json': fail('v0.3 predecessor pointer drift')
    if v3.get('snapshot_base_commit') != EXPECTED_MERGE: fail('v0.3 snapshot merge coordinate drift')
    delta = v3.get('delta_objects', [])
    if len(delta) != 1 or v3.get('delta_object_count') != 1: fail('unexpected v0.3 delta population')
    e = delta[0]
    predecessor_ids = {x.get('id') for x in v2.get('delta_objects', [])}
    if e.get('id') in predecessor_ids: fail('v0.3 delta silently rewrites v0.2 delta object')
    if e.get('id') != EXPECTED_ID: fail('unexpected v0.3 delta object')
    if e.get('admission_pr') != 147: fail('Lens Shift admission PR drift')
    if e.get('admission_merge_commit') != EXPECTED_MERGE: fail('Lens Shift admission merge coordinate drift')
    if e.get('material_state') != EXPECTED_MATERIAL: fail('Lens Shift material state promotion')
    if e.get('research_state') != 'CLOSED_FOR_PRESENT_SCOPE': fail('Lens Shift research state drift')
    if e.get('protocol_state') != 'FROZEN': fail('Lens Shift protocol state drift')
    if e.get('qualification_state') != EXPECTED_QUAL: fail('Lens Shift qualification state drift')
    if e.get('blind_epoch_003_execution') != EXPECTED_BLIND: fail('Blind Epoch 003 execution state drift')
    if e.get('historical_adverse_result') != 'EPOCH_002_8_OF_12_PRESERVED_UNCHANGED': fail('Epoch 002 adverse result not preserved')
    if e.get('harness_state') != 'v0.1.2_REVIEWER_REPRODUCED_REPAIR_ACCEPTED': fail('harness v0.1.2 state drift')
    if e.get('semantic_repair_warranted') is not False: fail('protocol semantic repair promotion')
    if e.get('universal_or_exhaustive_protocol_proof') != 'NOT_ESTABLISHED': fail('universal proof promotion')
    if not ADMISSION.is_dir(): fail('Lens Shift admission path missing')
    if not RECEIPT.is_file(): fail('Lens Shift post-merge receipt missing')

    closure = load(CLOSURE)
    standing = closure.get('standing', {})
    if standing.get('protocol_v0_1') != EXPECTED_QUAL: fail('admitted closure protocol standing drift')
    if standing.get('blind_epoch_003_execution') != EXPECTED_BLIND: fail('admitted closure execution drift')
    if standing.get('semantic_repair_warranted') is not False: fail('admitted closure semantic repair promotion')
    if closure.get('historical_preservation', {}).get('epoch_002_unchanged') is not True: fail('Epoch 002 preservation assertion missing')
    if closure.get('historical_preservation', {}).get('harness_v0_1_2_unchanged') is not True: fail('harness preservation assertion missing')

    first = load_jsonl(FIRST)
    oracle = load_jsonl(ORACLE)
    if len(first) != 24 or len({r.get('id') for r in first}) != 24: fail('first execution is not 24 unique IDs')
    counts = {v: sum(1 for r in first if r.get('verdict') == v) for v in ('CONFORMS','DOES_NOT_CONFORM')}
    if counts != {'CONFORMS': 12, 'DOES_NOT_CONFORM': 12}: fail('first execution verdict distribution drift')
    if len(oracle) != 24 or len({r.get('id') for r in oracle}) != 24: fail('oracle comparison is not 24 unique IDs')
    if [r.get('id') for r in first] != [r.get('id') for r in oracle]: fail('execution/oracle ID order drift')
    if any(a.get('verdict') != b.get('actual_verdict') for a,b in zip(first, oracle)): fail('oracle no longer preserves first execution')
    if any(r.get('match') is not True or r.get('actual_verdict') != r.get('expected_verdict') for r in oracle): fail('oracle comparison no longer 24/24')

    print('PASS: v0.3 current-standing successor overlay preserves v0.2 and records bounded Lens Shift v0.1 admission')
    print('boundary: 24/24 scope qualification != universal validation; repository admission != generalization')
    return 0

if __name__ == '__main__':
    sys.exit(main())
