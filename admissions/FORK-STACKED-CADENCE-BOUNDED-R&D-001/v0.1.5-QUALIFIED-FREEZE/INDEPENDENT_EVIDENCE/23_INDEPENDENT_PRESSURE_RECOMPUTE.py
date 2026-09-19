#!/usr/bin/env python3
"""
Independent pressure recomputation with independent receipt.
Does NOT read 09_EXPECTED_SUMMARY.json or 22_INTERNAL_REPAIR_RECEIPT.json.
All scenario metrics are rederived from scratch by running the harness twice
per scenario (determinism check) and independently verifying every numeric
field against the normative contract.
"""
import hashlib, importlib.util, json, sys, tempfile, subprocess
from pathlib import Path
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent

# --- load harness independently ---
sp = importlib.util.spec_from_file_location('h', ROOT / '07_HARNESS.py')
h = importlib.util.module_from_spec(sp)
sp.loader.exec_module(h)

fail = []
receipt_checks = []

def ch(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def req(name, cond, detail=''):
    ok = bool(cond)
    receipt_checks.append({'check': name, 'pass': ok, 'detail': detail})
    if not ok:
        fail.append(name + (f':{detail}' if detail else ''))

# ── SECTION 1: Harness byte identity ──────────────────────────────────────────
harness_bytes = (ROOT / '07_HARNESS.py').read_bytes()
harness_sha = hashlib.sha256(harness_bytes).hexdigest()
req('harness_sha256_independent',
    harness_sha == h.IMPLEMENTATION_DIGEST.replace('sha256:', ''),
    harness_sha)

# ── SECTION 2: Normative contract self-consistency ────────────────────────────
c = h.CONTRACT
req('contract_tolerance_multiplier_is_1_0',
    float(c['temporal_fidelity']['on_time_tolerance_multiplier']) == 1.0)
req('contract_promotion_threshold_is_3',
    int(c['promotion_candidate_derivation']['success_count_threshold']) == 3)
req('contract_qualifying_ops_exact',
    sorted(c['promotion_candidate_derivation']['qualifying_operations']) == ['deterministic_check', 'reproduce'])
req('contract_max_consecutive_4',
    int(c['fairness']['max_consecutive_same_class']) == 4)
req('contract_starvation_threshold_3600',
    float(c['fairness']['starvation_aging_threshold_seconds']) == 3600.0)
req('contract_coalescing_active_first',
    c['coalescing_target_selection_order'][0] == 'active_same_work')
req('contract_resolution_precedes_terminal',
    c['coalescing_resolution_event_precedes_target_terminal_event'] is True)
req('contract_replay_excluded_exact',
    sorted(c['replay_equivalence']['excluded_fields']) == ['checkpoint_resume_count', 'replay_digest'])

# ── SECTION 3: Per-scenario independent recomputation ─────────────────────────
# For each scenario: run twice, verify digest equality, then independently
# recompute every reported summary field from the raw result.

TIMED_CADENCES = {c_['cadence_id'] for c_ in h.CAD}
TOL = {c_['cadence_id']: float(c_['tolerance_seconds']) for c_ in h.CAD}

scenario_receipts = {}

for sid in sorted(h.SC):
    r1 = h.run(sid)
    r2 = h.run(sid)
    scenario_receipts[sid] = r1

    # 3a determinism
    req(f'{sid}:determinism', r1['replay_digest'] == r2['replay_digest'],
        f"r1={r1['replay_digest'][:16]} r2={r2['replay_digest'][:16]}")

    # 3b receipt closure
    req(f'{sid}:receipt_closure',
        r1['accounted_current_or_terminal'] == r1['triggered'],
        f"{r1['accounted_current_or_terminal']}/{r1['triggered']}")

    # 3c single executor (no overlap)
    req(f'{sid}:no_overlap', r1['overlap_count'] == 0, str(r1['overlap_count']))

    # 3d causal ordering
    req(f'{sid}:causal_start', r1['start_before_trigger_count'] == 0,
        str(r1['start_before_trigger_count']))

    # 3e boundary version invariant
    req(f'{sid}:boundary_b_v1', r1['boundary_versions'] == ['B-v1'],
        str(r1['boundary_versions']))

    # 3f semantic + implementation digest binding
    req(f'{sid}:semantic_digest', r1['semantic_profile_digest'] == h.SEMANTIC_DIGEST)
    req(f'{sid}:impl_digest', r1['implementation_digest'] == h.IMPLEMENTATION_DIGEST)

    # 3g Independent temporal fidelity recompute at exactly 1.0× tolerance
    scheduled = [x for x in r1['receipts'] if x['cadence_id'] in TIMED_CADENCES]
    completed_timed = [x for x in scheduled if x['disposition'] == 'COMPLETED']
    all_triggered = len(scheduled)
    ontime_count = sum(
        1 for x in completed_timed
        if x['timestamps']['start_time'] - x['timestamps']['trigger_time']
           <= TOL[x['cadence_id']] * 1.0 + 1e-9
    )
    ind_all = round(ontime_count / all_triggered, 6) if all_triggered else 1.0
    ind_exec = round(ontime_count / len(completed_timed), 6) if completed_timed else 1.0
    req(f'{sid}:temporal_fidelity_independent',
        r1['on_time_all_trigger_rate'] == ind_all and
        r1['on_time_among_executed'] == ind_exec,
        f"reported={r1['on_time_all_trigger_rate']}/{r1['on_time_among_executed']} "
        f"independent={ind_all}/{ind_exec}")

    # 3h Service formula binding for every completed receipt
    bad_svc = []
    for x in r1['receipts']:
        if x['disposition'] == 'COMPLETED' and x['work_id'] in h.WD:
            exp = float(h.WORK_UNITS[x['work_id']]) * 3600.0 / float(r1['capacity_work_units_per_hour'])
            act = float(x['timestamps']['finish_time']) - float(x['timestamps']['start_time'])
            if abs(act - exp) > 1e-7:
                bad_svc.append(x['receipt_id'])
    req(f'{sid}:service_formula', not bad_svc, bad_svc[0] if bad_svc else '')

    # 3i Queue event vocabulary confinement
    obs_events = sorted(set(q['event'] for q in r1['queue_history']))
    req(f'{sid}:queue_event_vocab',
        set(obs_events) <= set(h.CONTRACT['queue_history_event_vocabulary']),
        ','.join(obs_events))

    # 3j Replay digest closure: independently hash every non-excluded field
    ind_digest = ch({k: v for k, v in r1.items()
                     if k not in set(c['replay_equivalence']['excluded_fields'])})
    req(f'{sid}:replay_digest_independent', r1['replay_digest'] == ind_digest,
        f"reported={r1['replay_digest'][:16]} independent={ind_digest[:16]}")

    # 3k Content-addressed evidence: every artifact ref must equal sha256 of its content
    art_bad = []
    for ref, a in r1['evidence_artifacts'].items():
        if ref != 'sha256:' + ch(a):
            art_bad.append(ref[:24])
    req(f'{sid}:content_addressed_evidence', not art_bad, art_bad[0] if art_bad else '')

    # 3l All artifact types must be known
    unknown_types = sorted({a.get('artifact_type') for a in r1['evidence_artifacts'].values()}
                           - set(c['evidence_artifact_types']))
    req(f'{sid}:artifact_type_closure', not unknown_types, ','.join(unknown_types))

    # 3m Coalescing resolution precedes target terminal event
    ev_idx = {(q['event'], q['receipt_id']): i for i, q in enumerate(r1['queue_history'])}
    by_r = {x['receipt_id']: x for x in r1['receipts']}
    terminal_event = {'COMPLETED': 'COMPLETE', 'DEFERRED': 'DEFER', 'EXPIRED': 'EXPIRE'}
    coal_bad = []
    for x in r1['receipts']:
        if x['disposition'] in {'COALESCED_EXECUTED', 'DEFERRED_VIA_COALESCING', 'EXPIRED_VIA_COALESCING'}:
            tgt = by_r[x['coalesced_into']]
            ri = ev_idx.get(('COALESCE_RESOLVE', x['receipt_id']))
            ti = ev_idx.get((terminal_event.get(tgt['disposition']), tgt['receipt_id']))
            if ri is None or ti is None or ri >= ti:
                coal_bad.append(x['receipt_id'])
    req(f'{sid}:coalescing_resolution_order', not coal_bad, coal_bad[0] if coal_bad else '')

# ── SECTION 4: Cross-scenario scenario-specific claims ────────────────────────
s = scenario_receipts

req('S01:all_trigger_on_time_gte_095',
    s['S01_BASELINE_CAPACITY']['on_time_all_trigger_rate'] >= 0.95,
    str(s['S01_BASELINE_CAPACITY']['on_time_all_trigger_rate']))

req('S02:overload_backlog_nonzero',
    s['S02_CONTROLLED_OVERLOAD']['deferred'] > 0,
    str(s['S02_CONTROLLED_OVERLOAD']['deferred']))

req('S02:all_trigger_denominator_exceeds_executed',
    s['S02_CONTROLLED_OVERLOAD']['scheduled_triggered'] >
    s['S02_CONTROLLED_OVERLOAD']['timed_completed'])

req('S02:all_trigger_rate_less_than_executed_rate',
    s['S02_CONTROLLED_OVERLOAD']['on_time_all_trigger_rate'] <
    s['S02_CONTROLLED_OVERLOAD']['on_time_among_executed'])

req('S03:coalescing_exercised',
    (s['S03_COALESCING']['coalesced_executed'] +
     s['S03_COALESCING']['deferred_via_coalescing'] +
     s['S03_COALESCING']['expired_via_coalescing']) > 0)

req('S03:coalescing_identity_idempotence',
    all(h.WD[by_r['work_id']]['idempotent']
        for r in [s['S03_COALESCING']]
        for x in r['receipts']
        if x['disposition'] in {'COALESCED_EXECUTED', 'DEFERRED_VIA_COALESCING', 'EXPIRED_VIA_COALESCING'}
        for by_r in [next(y for y in r['receipts'] if y['receipt_id'] == x['coalesced_into'])]))

req('S04:expiry_observed',
    (s['S04_EXPIRY']['expired'] + s['S04_EXPIRY']['expired_via_coalescing']) > 0)

req('S04:expired_not_started',
    all(x['timestamps']['start_time'] is None
        for x in s['S04_EXPIRY']['receipts']
        if x['disposition'] == 'EXPIRED'))

req('S05:all_classes_served',
    set(h.CONTRACT['arbitration_order']) <=
    set(k for k, v in s['S05_STARVATION_FAIRNESS']['class_execution_counts'].items() if v > 0))

req('S06:conflict_preserved',
    any(x['outcome']['conflict_preserved'] and x['outcome']['preferred_conclusion'] is None
        for x in s['S06_ADVERSARIAL_CONFLICT']['receipts']
        if x['work_id'] == 'W-CONFLICT-RECONCILIATION' and x['disposition'] == 'COMPLETED'))

req('S07:promotion_candidate_derived',
    s['S07_PROMOTION_PRESSURE']['promotion_candidates'] > 0)

req('S07:no_promoted_state',
    s['S07_PROMOTION_PRESSURE']['promoted'] == 0)

# M03: promotion derives exactly at ≥3 successes per qualifying operation
r7 = s['S07_PROMOTION_PRESSURE']
by_finish = sorted(
    [x for x in r7['receipts']
     if x['disposition'] == 'COMPLETED' and x['outcome']['success_signal']],
    key=lambda x: x['timestamps']['finish_time'])
op_counts = {}
m03_bad = []
for x in by_finish:
    op = h.WD[x['work_id']]['operation']
    op_counts[op] = op_counts.get(op, 0) + 1
    expected = op in {'reproduce', 'deterministic_check'} and op_counts[op] >= 3
    if (x['promotion_state'] == 'PROMOTION_CANDIDATE') != expected:
        m03_bad.append(x['receipt_id'])
req('M03:promotion_derivation_exact_independent', not m03_bad,
    m03_bad[0] if m03_bad else '')

req('S08:scope_gate_path',
    any(x['gate_request'] and x['disposition'] == 'SKIPPED_BY_POLICY'
        for x in s['S08_SCOPE_PRESSURE']['receipts']
        if x['work_id'] == 'AUTHORIZATION-REQUEST'))

req('S09:identity_gate_path',
    any(x['gate_request'] and x['disposition'] == 'SKIPPED_BY_POLICY'
        for x in s['S09_IDENTITY_PRESSURE']['receipts']
        if x['work_id'] == 'AUTHORIZATION-REQUEST'))

req('S10:daily_recurrence_gte_6',
    s['S10_RECOVERY_LONGITUDINAL']['daily_trigger_count'] >= 6,
    str(s['S10_RECOVERY_LONGITUDINAL']['daily_trigger_count']))

# ── SECTION 5: Queue event vocabulary full coverage across all scenarios ───────
all_events = sorted({q['event'] for r in s.values() for q in r['queue_history']})
req('queue_event_vocabulary_full_coverage',
    set(all_events) == set(h.CONTRACT['queue_history_event_vocabulary']),
    ','.join(all_events))

# ── SECTION 6: M02 burst-alternative selection (independent adversary) ─────────
reps = {}
for wid, w in h.WD.items():
    reps.setdefault(w['priority_class'], wid)
st = h.initial_state('S05_STARVATION_FAIRNESS')
st['last_class'] = 'safety_or_integrity_work'
st['run_len'] = int(h.QP['fairness']['max_consecutive_same_class'])
amap = {}; seq = 0
for pc, enq_t in [('evidence_preservation', 100.0), ('scheduled_comparison', 0.0)]:
    seq += 1
    wid = reps[pc]
    rid = f'IND-BURST-{seq}'
    sp2 = {'time': enq_t, 'seq': seq, 'kind': 'work', 'work_id': wid, 'cadence_id': 'IND',
           'receipt': h.receipt_template('IND', seq, wid, 'IND', enq_t, h.WD[wid], 20)}
    sp2['receipt']['receipt_id'] = rid
    sp2['receipt']['timestamps']['enqueue_time'] = enq_t
    amap[rid] = sp2
    st['receipts'][rid] = sp2['receipt']
    st['ready_ids'].append(rid)
chosen = h.choose_ready(st, amap, 200.0)
req('M02:burst_alt_greatest_wait_independent',
    h.WD[chosen['work_id']]['priority_class'] == 'scheduled_comparison',
    h.WD[chosen['work_id']]['priority_class'])

# ── SECTION 7: M04 coalescing active-target precedence (independent adversary) ─
wid_c = 'W-OBSERVE-DELTA'
st2 = h.initial_state('S03_COALESCING')
amap2 = {}
for seq2, rid2, t2 in [(1, 'IND-ACTIVE', 0.0), (2, 'IND-READY', 1.0), (3, 'IND-NEW', 2.0)]:
    sp3 = {'time': t2, 'seq': seq2, 'kind': 'work', 'work_id': wid_c, 'cadence_id': 'IND',
           'receipt': h.receipt_template('IND', seq2, wid_c, 'IND', t2, h.WD[wid_c], 20)}
    sp3['receipt']['receipt_id'] = rid2
    amap2[rid2] = sp3
    if rid2 != 'IND-NEW':
        st2['receipts'][rid2] = sp3['receipt']
        st2['receipts'][rid2]['timestamps']['enqueue_time'] = t2
st2['active'] = {'receipt_id': 'IND-ACTIVE', 'start': 0.0, 'finish': 10.0}
st2['ready_ids'] = ['IND-READY']
h.instantiate_arrival(st2, amap2['IND-NEW'], {'coalescing_enabled': True}, amap2)
req('M04:coalescing_active_precedence_independent',
    st2['receipts']['IND-NEW']['coalesced_into'] == 'IND-ACTIVE',
    str(st2['receipts']['IND-NEW']['coalesced_into']))

# ── SECTION 8: Equal-aged starvation rotation (independent adversary) ──────────
st3 = h.initial_state('S05_STARVATION_FAIRNESS')
amap3 = {}; seq3 = 0
for pc3 in h.CONTRACT['arbitration_order']:
    for _ in range(20 if pc3 == 'safety_or_integrity_work' else 1):
        seq3 += 1
        wid3 = reps[pc3]
        rid3 = f'IND-EA-{seq3:03d}'
        sp4 = {'time': 0.0, 'seq': seq3, 'kind': 'work', 'work_id': wid3, 'cadence_id': 'IND',
               'receipt': h.receipt_template('IND', seq3, wid3, 'IND', 0.0, h.WD[wid3], 20)}
        sp4['receipt']['receipt_id'] = rid3
        amap3[rid3] = sp4
        st3['receipts'][rid3] = sp4['receipt']
        st3['receipts'][rid3]['timestamps']['enqueue_time'] = 0.0
        st3['ready_ids'].append(rid3)
clock3 = float(h.CONTRACT['fairness']['starvation_aging_threshold_seconds']) + 1.0
seen3 = []
for _ in range(12):
    chosen3 = h.choose_ready(st3, amap3, clock3)
    rid_c3 = chosen3['receipt']['receipt_id']
    pc_c3 = h.WD[chosen3['work_id']]['priority_class']
    seen3.append(pc_c3)
    st3['ready_ids'].remove(rid_c3)
    st3['service_sequence'] += 1
    st3['class_last_service_sequence'][pc_c3] = st3['service_sequence']
    st3['last_class'] = pc_c3
    st3['run_len'] = 1
req('M01_EA:all_classes_served_in_12_steps',
    set(h.CONTRACT['arbitration_order']) <= set(seen3),
    'seen=' + ','.join(seen3))

# ── SECTION 9: Checkpoint clean-process recovery (independent subprocess run) ──
sid_r = 'S10_RECOVERY_LONGITUDINAL'
ctl_r = h.run(sid_r)
cps_times = h.SC[sid_r]['checkpoint_times_seconds']
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    prev = None; prev_digest = None; active_flags = []
    for i, t in enumerate(cps_times):
        cp = td / f'ind_cp{i}.json'
        cmd = [sys.executable, str(ROOT / '07_HARNESS.py'),
               '--scenario', sid_r, '--until', str(t), '--checkpoint-out', str(cp)]
        if prev:
            cmd += ['--resume', str(prev)]
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        req(f'ind_checkpoint_process_{i}', p.returncode == 0, p.stderr[-120:])
        body = json.load(open(cp))
        active_flags.append(body['state']['active'] is not None)
        req(f'ind_checkpoint_semantic_{i}',
            body['semantic_profile_digest'] == h.SEMANTIC_DIGEST)
        req(f'ind_checkpoint_chain_{i}',
            body['predecessor_checkpoint_digest'] == prev_digest)
        prev_digest = body['checkpoint_digest']
        prev = cp
    out_r = td / 'ind_resumed.json'
    p2 = subprocess.run(
        [sys.executable, str(ROOT / '07_HARNESS.py'),
         '--scenario', sid_r, '--resume', str(prev), '--out', str(out_r)],
        capture_output=True, text=True, cwd=ROOT)
    req('ind_resume_process', p2.returncode == 0, p2.stderr[-120:])
    resumed_r = json.load(open(out_r))
    req('ind_recovery_trace_equivalence',
        resumed_r['replay_digest'] == ctl_r['replay_digest'],
        f"resumed={resumed_r['replay_digest'][:16]} ctl={ctl_r['replay_digest'][:16]}")
    req('ind_checkpoint_during_active', all(active_flags), str(active_flags))
    # Tamper: modify state without recomputing digests
    bad_cp = td / 'ind_tampered.json'
    tamper_body = json.load(open(prev))
    tamper_body['state']['run_len'] = 9999
    bad_cp.write_text(json.dumps(tamper_body, sort_keys=True, indent=2) + '\n')
    p3 = subprocess.run(
        [sys.executable, str(ROOT / '07_HARNESS.py'),
         '--scenario', sid_r, '--resume', str(bad_cp)],
        capture_output=True, text=True, cwd=ROOT)
    req('ind_checkpoint_tamper_rejected', p3.returncode != 0)

# ── Emit independent receipt ───────────────────────────────────────────────────
scenario_summaries = {sid: h.summary(r) for sid, r in scenario_receipts.items()}
replay_digests = {sid: r['replay_digest'] for sid, r in scenario_receipts.items()}

receipt = {
    'receipt_id': 'INDEPENDENT-PRESSURE-RECOMPUTE-v0.1.5',
    'object': 'FORK-STACKED-CADENCE-BOUNDED-R&D-001',
    'version': 'v0.1.5',
    'method': 'independent_recomputation_no_expected_summary_oracle',
    'harness_sha256': harness_sha,
    'semantic_profile_digest': h.SEMANTIC_DIGEST,
    'implementation_digest': h.IMPLEMENTATION_DIGEST,
    'passed': not fail,
    'check_count': len(receipt_checks),
    'failure_count': len(fail),
    'failures': fail,
    'replay_digests_rederived': replay_digests,
    'scenario_summaries_rederived': scenario_summaries,
    'checks': receipt_checks,
}
print(json.dumps(receipt, indent=2))
raise SystemExit(0 if not fail else 1)
