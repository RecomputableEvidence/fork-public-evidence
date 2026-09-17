#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_3.json'
V4 = ROOT / 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_4.json'
ADMISSION = ROOT / 'admissions/UEM-v0.1/EPOCH-010-CRII'
EXECUTOR = ADMISSION / 'EXECUTOR_RESULTS.json'
REPRODUCED = ADMISSION / 'REPRODUCED_VERIFICATION_RECEIPT.json'
CANDIDATE = ADMISSION / 'UEM-v0.1-EPOCH-010-CRII-REPOSITORY-ADMISSION-CANDIDATE-001.json'
RECEIPT = ROOT / 'docs/current-standing/UEM_v0_1_EPOCH_010_CRII_ADMISSION_MERGE_RECEIPT_2026_09_17.md'

EXPECTED_ID = 'UEM_CRII_1_0_EPOCH_010'
EXPECTED_EPOCH = 'UEM-v0.1-CANONICAL-RESULT-IDENTITY-INTERCHANGE-PRESSURE-EPOCH-010'
EXPECTED_MERGE = '61ce462e131c3c2687abd1d7744cd9ffaf238552'
EXPECTED_EXECUTOR_SHA = '0203efb6644ad6d4026622ae41655bbfc0f18c47e8f2fad95d540ccdc8bfbf02'
EXPECTED_RECEIPT_SHA = '685d20363f58e477aef2963c3d76e432e753e6f1057f88005c9078ef11e3823c'
EXPECTED_MATERIAL = 'TERMINAL_NATIVE_RECORDS_ADMITTED__ORIGINAL_EXECUTOR_HANDOFF_CLOSEOUT_AND_FROZEN_VERIFIER_BUNDLES_HASH_BOUND_NOT_ADMITTED'


def fail(message: str) -> None:
    print('FAIL:', message)
    raise SystemExit(1)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'{path.relative_to(ROOT)} invalid JSON: {exc}')


def main() -> int:
    v3, v4 = load(V3), load(V4)
    if v4.get('record_form') != 'PREDECESSOR_PLUS_DELTA': fail('v0.4 is not predecessor-plus-delta')
    if v4.get('predecessor_register') != 'docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_3.json': fail('v0.4 predecessor pointer drift')
    if v4.get('snapshot_base_commit') != EXPECTED_MERGE: fail('v0.4 snapshot merge coordinate drift')
    delta = v4.get('delta_objects', [])
    if len(delta) != 1 or v4.get('delta_object_count') != 1: fail('unexpected v0.4 delta population')
    e = delta[0]
    predecessor_ids = {x.get('id') for x in v3.get('delta_objects', [])}
    if e.get('id') in predecessor_ids: fail('v0.4 delta silently rewrites v0.3 delta object')
    if e.get('id') != EXPECTED_ID: fail('unexpected v0.4 delta object')
    if e.get('epoch') != EXPECTED_EPOCH: fail('Epoch 010 identity drift')
    if e.get('admission_pr') != 149: fail('UEM Epoch 010 admission PR drift')
    if e.get('admission_merge_commit') != EXPECTED_MERGE: fail('UEM Epoch 010 merge coordinate drift')
    if e.get('material_state') != EXPECTED_MATERIAL: fail('UEM Epoch 010 material state promotion')
    if e.get('research_state') != 'CLOSED_FOR_EPOCH_010_SCOPE': fail('research state drift')
    if e.get('disposition') != 'BOUNDED_CANONICAL_RESULT_IDENTITY_INTERCHANGE_PASS': fail('bounded disposition drift')
    if e.get('verifier_receipt_replay') != 'PASS_REPRODUCED_BYTE_FOR_BYTE': fail('verifier replay state drift')
    if e.get('fixture_population') != 16: fail('fixture population drift')
    if e.get('validation_counts') != {'ACCEPT': 4, 'REJECT': 12}: fail('validation counts drift')
    if e.get('receipt_status') != 'PASS': fail('receipt status drift')
    if e.get('executor_results_sha256') != EXPECTED_EXECUTOR_SHA: fail('executor hash drift')
    if e.get('reproduced_receipt_sha256') != EXPECTED_RECEIPT_SHA: fail('reproduced receipt hash drift')
    if e.get('independent_executor_from_fixture_reproduction') != 'NOT_ESTABLISHED_FROM_CLOSEOUT_ARCHIVE_ALONE': fail('executor independence promotion')
    if e.get('trusted_timestamp_pre_exposure_proof') != 'NOT_ESTABLISHED': fail('chronology proof promotion')
    if e.get('universal_uem_correctness') != 'NOT_ESTABLISHED': fail('universal UEM correctness promotion')
    if e.get('independent_surface_generalization') != 'NOT_ESTABLISHED': fail('independent-surface generalization promotion')
    if e.get('epoch_011_generalization') != 'NOT_ESTABLISHED_BY_THIS_RESULT': fail('Epoch 011 generalization promotion')
    if e.get('accept_zero_violations_as_universal_contract_invariant') != 'NOT_ESTABLISHED': fail('ACCEPT contract edge promoted')
    if not ADMISSION.is_dir(): fail('UEM Epoch 010 admission path missing')
    if not RECEIPT.is_file(): fail('UEM Epoch 010 post-merge receipt missing')

    executor = load(EXECUTOR)
    if executor.get('epoch') != EXPECTED_EPOCH: fail('admitted executor epoch drift')
    results = executor.get('results', [])
    ids = [r.get('fixture_id') for r in results]
    if len(results) != 16 or len(set(ids)) != 16: fail('admitted executor population is not 16 unique IDs')
    if Counter(r.get('validation') for r in results) != Counter({'ACCEPT': 4, 'REJECT': 12}): fail('admitted executor validation distribution drift')
    if any(r.get('violated_rule_ids') for r in results if r.get('validation') == 'ACCEPT'): fail('observed ACCEPT rows no longer have empty violation lists')

    reproduced = load(REPRODUCED)
    if reproduced.get('epoch') != EXPECTED_EPOCH or reproduced.get('status') != 'PASS': fail('admitted reproduced receipt drift')
    checks = reproduced.get('fixture_checks', [])
    if len(checks) != 16 or len({r.get('fixture_id') for r in checks}) != 16: fail('admitted receipt population drift')
    if [r.get('fixture_id') for r in results] != [r.get('fixture_id') for r in checks]: fail('executor/receipt fixture order drift')
    if any(a.get('validation') != b.get('validation') for a,b in zip(results, checks)): fail('executor/receipt validation drift')
    if reproduced.get('binding', {}).get('executor_results_sha256') != EXPECTED_EXECUTOR_SHA: fail('receipt executor-byte binding drift')

    candidate = load(CANDIDATE)
    if candidate.get('admission_state') != 'CANDIDATE_PENDING_PR_CHECKS_AND_MAIN_MERGE': fail('historical pre-merge candidate was rewritten')
    if candidate.get('disposition') != 'BOUNDED_CANONICAL_RESULT_IDENTITY_INTERCHANGE_PASS': fail('historical candidate disposition drift')

    print('PASS: v0.4 current-standing successor overlay preserves v0.3 and records bounded UEM Epoch 010 CRII admission')
    print('boundary: verifier receipt replay != independent executor reproduction; bounded CRII pass != universal UEM correctness or generalization')
    return 0

if __name__ == '__main__':
    sys.exit(main())
