import importlib.util
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import prepare_csh_s002_v0_1 as prep


def test_plan_reproducible_balanced_and_offline():
    c = prep.candidate()
    first = prep.plan(c)
    assert first == prep.plan(c)
    assert len(first['units']) == 24
    assert len({u['unit_id'] for u in first['units']}) == 24
    assert not first['corpus_execution_enabled']
    for i in range(0, 24, 2):
        a, b = first['units'][i:i+2]
        assert a['scenario_id'] == b['scenario_id']
        assert a['receiver'] == b['receiver']
        assert {a['condition'], b['condition']} == {'H0', 'H1'}
    for u in first['units']:
        r = u['request']
        assert r['tools'] == [] and r['tool_choice'] == 'none'
        assert r['max_steps'] == 1 and r['store'] is False
        assert 'previous_response_id' not in r and 'effort' not in r
    assert first['reserved_corpus_allowance_usd'] == '0.72'


def test_source_tamper_rejected(tmp_path, monkeypatch):
    c = prep.candidate()
    c['source_bindings'] = {'tampered': '0' * 64}
    (tmp_path / 'tampered').write_text('changed')
    path = tmp_path / 'candidate.json'; path.write_text(json.dumps(c))
    monkeypatch.setattr(prep, 'ROOT', tmp_path)
    monkeypatch.setattr(prep, 'CANDIDATE', path)
    with pytest.raises(ValueError, match='binding mismatch'): prep.candidate()


def test_missing_key_no_call(tmp_path, monkeypatch):
    monkeypatch.delenv('PERPLEXITY_API_KEY', raising=False)
    assert prep.neutral(prep.candidate(), tmp_path / 'missing')['status'] == 'CREDENTIAL_UNAVAILABLE'


class Response:
    def __init__(self, data, text): self.data, self.output_text = data, text
    def model_dump(self, **kw): return self.data


def valid(c):
    return {'status': 'completed', 'model': c['receivers'][0]['model'], 'id': 'fixture',
            'output': [], 'usage': {'cost': {'currency': 'USD', 'total_cost': 0.001}}}


@pytest.mark.parametrize('change,error', [
    ({'status': 'incomplete'}, 'completion_status'),
    ({'output': [{'type': 'message', 'role': 'user', 'status': 'completed'}]}, 'message_structure'),
    ({'model': 'alias'}, 'model_identity'),
    ({'output': [{'type': 'search_results', 'results': []}]}, 'unexpected_output_or_tool_activity'),
    ({'usage': {}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 0.04}}}, 'cost_above_reservation'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 'NaN'}}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'EUR', 'total_cost': 0.001}}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 0.001}, 'tool_calls_details': {'search': {'invocation': 1}}}}, 'tool_usage'),
])
def test_rejection(change, error):
    c = prep.candidate(); d = valid(c); d.update(change)
    assert error in prep.assess(c, c['receivers'][0], 200, Response(d, '{"preflight":"ok"}'))['errors']


@pytest.mark.parametrize('text', ['{}', '[]', 'no', '{"preflight":"ok","preflight":"ok"}'])
def test_neutral_content(text):
    c = prep.candidate()
    assert 'expected_content' in prep.assess(c, c['receivers'][0], 200, Response(valid(c), text))['errors']


def test_sdk_wire_capture_and_stop(tmp_path):
    perplexity = pytest.importorskip('perplexity')
    import httpx
    calls = []
    def handle(req):
        calls.append(req)
        body = json.loads(req.content)
        assert body['tools'] == [] and body['tool_choice'] == 'none'
        assert body['input'] == 'Return JSON only: {"preflight":"ok"}'
        return httpx.Response(402, json={'error': {'message': 'fixture'}})
    with perplexity.Perplexity(api_key='fixture-only', max_retries=0,
          http_client=httpx.Client(transport=httpx.MockTransport(handle), trust_env=False)) as client:
        result = prep.neutral(prep.candidate(), tmp_path / 'batch', client)
    assert result['status'] == 'BLOCKED' and len(calls) == 1
    receipt = result['results'][0]
    for name in ('request.json', 'response.bin'):
        assert prep.digest((tmp_path / 'batch' / 'A' / name).read_bytes()) == receipt[name + '_sha256']
    assert 'fixture-only' not in (tmp_path / 'batch' / 'A' / 'request.json').read_text()
    with pytest.raises(FileExistsError): prep.neutral(prep.candidate(), tmp_path / 'batch')


def test_sdk_two_successful_neutral_responses(tmp_path):
    perplexity = pytest.importorskip('perplexity')
    import httpx
    def handle(req):
        body = json.loads(req.content)
        d = valid(prep.candidate()); d.update(created_at=1, object='response', model=body['model'])
        d['output'] = [{'type': 'message', 'id': 'm', 'role': 'assistant', 'status': 'completed',
                        'content': [{'type': 'output_text', 'text': '{"preflight":"ok"}', 'annotations': []}]}]
        return httpx.Response(200, json=d)
    with perplexity.Perplexity(api_key='fixture-only', max_retries=0,
          http_client=httpx.Client(transport=httpx.MockTransport(handle), trust_env=False)) as client:
        result = prep.neutral(prep.candidate(), tmp_path / 'batch', client)
    assert result['status'] == 'PASS' and len(result['results']) == 2
    assert not result['corpus_execution_enabled']
