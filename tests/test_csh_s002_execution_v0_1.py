import copy
import json
from pathlib import Path
import shutil
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import run_csh_s002_v0_1 as run
import prepare_csh_s002_v0_1 as prep
import analyze_csh_s001_v0_1 as analysis
import classify_unsupported_inheritance_s001_v0_1 as classifier


def response(model):
    return {'id': 'synthetic', 'created_at': 1, 'object': 'response', 'status': 'completed',
            'model': model, 'tools': [], 'tool_choice': 'auto',
            'output': [{'type': 'message', 'id': 'm', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': '{"transfer":"fixture"}', 'annotations': []}]}],
            'usage': {'cost': {'currency': 'USD', 'total_cost': 0.00001}}}


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    verified = run.verify()
    monkeypatch.setattr(run, 'ROOT', tmp_path)
    monkeypatch.setattr(run, 'verify', lambda package, expected: verified)
    return verified


def client_for(handler):
    import httpx
    perplexity = pytest.importorskip('perplexity')
    return perplexity.Perplexity(api_key='synthetic-secret', max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler), trust_env=False))


def test_frozen_population_recomputes_and_neutral_hashes():
    freeze, plan, sha = run.verify()
    assert len(plan['units']) == 24 and len(sha) == 64
    assert freeze['budget']['corpus_reserved_usd'] == '0.72'
    evidence = ROOT / 'docs/current-standing/CSH_S002_NEUTRAL_20261026'
    for receiver in ('A', 'B'):
        receipt = run.read(evidence / receiver / 'receipt.json')
        for name in ('request.json', 'response.bin'):
            assert prep.digest((evidence / receiver / name).read_bytes()) == receipt[name + '_sha256']
        d = run.read(evidence / receiver / 'response.bin')
        result, text = run.assess(d, receipt['requested_model'])
        assert result['status'] == 'PASS' and json.loads(text) == {'preflight': 'ok'}
        assert d['tool_choice'] == 'auto'
        assert run.read(evidence / receiver / 'request.json')['tool_choice'] == 'none'


def test_wrong_freeze_digest_blocks():
    with pytest.raises(ValueError, match='freeze digest'): run.verify(expected='0' * 64)


def test_request_tamper_blocks(tmp_path):
    package = tmp_path / 'package'; shutil.copytree(run.PACKAGE, package)
    request = next((package / 'requests').glob('*.json')); request.write_bytes(b'{}')
    with pytest.raises(ValueError, match='package binding'): run.verify(package)


def test_source_tamper_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(run, 'ROOT', tmp_path)
    with pytest.raises((ValueError, FileNotFoundError)): run.verify()


def test_full_mock_campaign_and_no_repeat(isolated, tmp_path):
    import httpx
    calls = []
    out = tmp_path / 'results'
    def handle(req):
        calls.append(req.content)
        ledger = run.read(out / 'ledger.json')
        assert ledger['results'][-1]['status'] == 'RESERVED_OUTCOME_UNKNOWN'
        assert ledger['gross_committed_usd'] == str(run.Decimal('0.06') + run.Decimal('0.03') * len(calls))
        assert len(calls) <= 24
        return httpx.Response(200, json=response(json.loads(req.content)['model']))
    with client_for(handle) as client:
        result = run.execute(out, isolated[2], client)
        with pytest.raises(FileExistsError): run.execute(tmp_path / 'other-output', isolated[2], client)
    assert result['status'] == 'COMPLETED_PENDING_CODING'
    assert result['gross_committed_usd'] == '0.78'
    assert result['known_corpus_cost_usd'] == '0.00024'
    assert len(calls) == 24
    assert calls == [run.wire(u['request']) for u in isolated[1]['units']]
    for r in run.read(out / 'ledger.json')['results']:
        for name in ('request.json', 'response.bin', 'output.txt'):
            assert prep.digest((out / r['unit_id'] / name).read_bytes()) == r[name + '_sha256']
    summary = analysis.summarize(run.read(out / 'analysis-pending.json'))
    assert summary['run_count'] == 24 and summary['classifiable_run_count'] == 0
    assert all(r['U'] is None for r in summary['run_rows'])
    assert 'synthetic-secret' not in ''.join(p.read_text() for p in out.rglob('*') if p.is_file())


@pytest.mark.parametrize('status', [401, 402, 429, 500])
def test_http_failures_never_retry(isolated, tmp_path, status):
    import httpx
    calls = []
    def handle(req):
        calls.append(req); return httpx.Response(status, json={'error': 'synthetic'})
    with client_for(handle) as client:
        result = run.execute(tmp_path / 'result', isolated[2], client)
    assert len(calls) == 1 and result['status'] == 'STOPPED'
    assert result['unknown_cost_requests'] == 1 and result['gross_committed_usd'] == '0.09'
    assert len(run.read(tmp_path / 'result' / 'analysis-pending.json')) == 24


@pytest.mark.parametrize('change,error', [
    ({'status': 'incomplete'}, 'completion_status'),
    ({'model': 'substitute'}, 'model_identity'),
    ({'output': []}, 'output_structure'),
    ({'output': [{'type': 'web_search_call'}]}, 'unexpected_output_or_tool_activity'),
    ({'tools': [{'type': 'web_search'}]}, 'unexpected_tools_or_history'),
    ({'previous_response_id': 'previous'}, 'unexpected_tools_or_history'),
    ({'usage': {}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 'NaN'}}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': -1}}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'EUR', 'total_cost': 0.01}}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 0.04}}}, 'cost_above_reservation'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 0.01}, 'tool_calls_details': {'search': {'invocation': 1}}}}, 'tool_usage'),
])
def test_response_rejections(change, error):
    data = response('expected'); data.update(change)
    assert error in run.assess(data, 'expected')[0]['errors']


@pytest.mark.parametrize('text', ['not JSON', '[]', '{"a":1,"a":2}', '```json\n{}\n```'])
def test_answer_object_required(text):
    data = response('expected'); data['output'][0]['content'][0]['text'] = text
    assert 'transfer_json_object' in run.assess(data, 'expected')[0]['errors']


def test_overrun_stops_and_charges_actual(isolated, tmp_path):
    import httpx
    calls = []
    def handle(req):
        calls.append(req)
        data = response(json.loads(req.content)['model']); data['usage']['cost']['total_cost'] = 0.08
        return httpx.Response(200, json=data)
    with client_for(handle) as client:
        result = run.execute(tmp_path / 'result', isolated[2], client)
    assert result['gross_committed_usd'] == '0.14' and len(calls) == 1
    assert result['known_corpus_cost_usd'] == '0.08' and result['status'] == 'STOPPED'


def test_crash_retains_reservation_and_blocks_restart(isolated, tmp_path):
    def handle(req): raise KeyboardInterrupt()
    with client_for(handle) as client:
        with pytest.raises(KeyboardInterrupt): run.execute(tmp_path / 'result', isolated[2], client)
        with pytest.raises(FileExistsError): run.execute(tmp_path / 'new-result', isolated[2], client)
    ledger = run.read(tmp_path / 'result' / 'ledger.json')
    assert ledger['gross_committed_usd'] == '0.09'
    assert ledger['results'][0]['status'] == 'RESERVED_OUTCOME_UNKNOWN'


def test_missing_key_does_not_claim(isolated, tmp_path, monkeypatch):
    monkeypatch.delenv('PERPLEXITY_API_KEY', raising=False)
    assert run.execute(tmp_path / 'result', isolated[2])['status'] == 'CREDENTIAL_UNAVAILABLE'
    assert not (tmp_path / run.CAMPAIGN).exists()


def test_wire_mutation_stops_before_transport(isolated, tmp_path):
    calls = []
    with client_for(lambda req: calls.append(req)) as client:
        def mutate(req): req.url = req.url.copy_with(path='/wrong')
        client._client.event_hooks['request'].append(mutate)
        result = run.execute(tmp_path / 'result', isolated[2], client)
    assert not calls and result['status'] == 'STOPPED'


def test_s002_coding_schema_and_paired_analysis_compatibility():
    template = run.read(ROOT / 'tests/fixtures/csh_s001/classifier_input_clean.json')
    rows = []
    for condition in ('control_h0', 'instrumented_h1'):
        item = copy.deepcopy(template)
        item.update(receiver_run_id='S002-A-A-' + condition + '-R1',
                    classification_run_id='S002-synthetic-' + condition, condition=condition)
        classifier.validate(item, run.read(ROOT / classifier.INPUT_SCHEMA), 'synthetic S002 input')
        result = classifier.classify(item)
        classifier.validate(result, run.read(ROOT / classifier.OUTPUT_SCHEMA), 'synthetic S002 output')
        rows.append({'receiver_run_id': item['receiver_run_id'], 'pairing_key': 'S002-A-A-R1',
                     'scenario_id': item['scenario']['scenario_id'], 'receiver_class_id': 'A',
                     'condition': condition, 'terminal_state': 'COMPLETED_CLASSIFIABLE',
                     'task_state': item['task_state'], 'classification': result})
    summary = analysis.summarize(rows)
    assert summary['classifiable_run_count'] == 2
    assert len(summary['paired_differences']) == 1
    assert summary['paired_differences'][0]['D_pair'] == 0


@pytest.mark.parametrize('failure', ['timeout', 'incomplete', 'malformed', 'missing_cost'])
def test_uncertain_or_invalid_outcomes_stop(isolated, tmp_path, failure):
    import httpx
    calls = []
    def handle(req):
        calls.append(req)
        if failure == 'timeout': raise httpx.ReadTimeout('synthetic', request=req)
        if failure == 'malformed': return httpx.Response(200, content=b'not JSON')
        data = response(json.loads(req.content)['model'])
        if failure == 'incomplete': data['status'] = 'incomplete'
        if failure == 'missing_cost': data['usage'] = {}
        return httpx.Response(200, json=data)
    with client_for(handle) as client:
        result = run.execute(tmp_path / 'result', isolated[2], client)
    assert len(calls) == 1 and result['status'] == 'STOPPED'
    assert result['gross_committed_usd'] == '0.09'


def test_failed_reservation_write_never_sends(isolated, tmp_path, monkeypatch):
    original = run.save
    def fail_ledger(path, data):
        if path.name == 'ledger.json' and data.get('results'):
            raise OSError('synthetic disk failure')
        return original(path, data)
    monkeypatch.setattr(run, 'save', fail_ledger)
    calls = []
    with client_for(lambda req: calls.append(req)) as client:
        with pytest.raises(OSError): run.execute(tmp_path / 'result', isolated[2], client)
    assert not calls and (tmp_path / run.CAMPAIGN).exists()
