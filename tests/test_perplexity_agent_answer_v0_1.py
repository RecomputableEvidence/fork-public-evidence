import importlib.util
import json
from pathlib import Path

import pytest

perplexity = pytest.importorskip('perplexity')
import httpx

spec = importlib.util.spec_from_file_location('agent_answer', Path(__file__).resolve().parents[1] / 'tools/perplexity_agent_answer_v0_1.py')
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


def payload(status='completed', text='Answer [1].'):
    return {'id': 'resp_fixture', 'created_at': 1, 'model': agent.DEFAULT_MODEL,
            'object': 'response', 'status': status, 'output': [
                {'type': 'search_results', 'queries': ['Question'], 'results': [{'id': 1, 'snippet': 'Source text', 'source': 'web', 'url': 'https://example.org', 'title': 'Source'}]},
                {'type': 'message', 'id': 'msg_fixture', 'role': 'assistant', 'status': 'completed',
                 'content': [{'type': 'output_text', 'text': text, 'annotations': [
                     {'type': 'url_citation', 'url': 'https://example.org', 'title': 'Source'}]}]}]}


def client_for(handler):
    return perplexity.Perplexity(api_key='fixture-not-a-real-key', max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler), trust_env=False))


def test_wire_request_and_source_preservation():
    def handle(request):
        assert str(request.url) == 'https://api.perplexity.ai/v1/responses'
        assert request.method == 'POST'
        body = json.loads(request.content)
        assert body['tools'] == [{'type': 'web_search'}]
        assert body['previous_response_id'] == 'resp_prior'
        assert body['max_output_tokens'] == 512
        assert body['max_steps'] == 2
        assert body['model'] == agent.DEFAULT_MODEL
        return httpx.Response(200, json=payload())
    with client_for(handle) as client:
        result = agent.answer('Question', previous_response_id='resp_prior', client=client)
    assert result['status'] == 'PASS'
    assert result['output_text'] == 'Answer [1].'
    assert result['search_results'][0]['url'] == 'https://example.org'
    assert result['citations'][0]['url'] == 'https://example.org'


@pytest.mark.parametrize('status,text', [('failed', 'Partial'), ('in_progress', 'Partial'), ('completed', '')])
def test_incomplete_not_success(status, text):
    with client_for(lambda r: httpx.Response(200, json=payload(status, text))) as client:
        assert agent.answer('Question', client=client)['status'] == 'RESPONSE_INCOMPLETE'


@pytest.mark.parametrize('code,expected', [(401, 'AUTHENTICATION_ERROR'), (429, 'RATE_LIMITED'), (500, 'HTTP_ERROR')])
def test_errors_do_not_leak_or_retry(code, expected):
    calls = []
    def handle(request):
        calls.append(request)
        return httpx.Response(code, headers={'Retry-After': '120'}, json={'error': 'sensitive-marker'})
    with client_for(handle) as client:
        result = agent.answer('Question', client=client)
    assert result['status'] == expected
    assert result['retry_after_seconds'] == 120
    assert 'sensitive-marker' not in json.dumps(result)
    assert len(calls) == 1


def test_no_grounding_claim_without_metadata():
    data = payload()
    data['output'] = data['output'][1:]
    data['output'][0]['content'][0]['annotations'] = []
    with client_for(lambda r: httpx.Response(200, json=data)) as client:
        assert not agent.answer('Question', client=client)['grounding_metadata_present']


def test_missing_key_no_request(monkeypatch):
    monkeypatch.delenv('PERPLEXITY_API_KEY', raising=False)
    assert agent.answer('Question') == {'status': 'CREDENTIAL_UNAVAILABLE', 'request_attempted': False}


def test_connection_error():
    def handle(request):
        raise httpx.ConnectError('sensitive-marker', request=request)
    with client_for(handle) as client:
        assert agent.answer('Question', client=client) == {'status': 'CONNECTION_ERROR'}


@pytest.mark.parametrize('header,expected', [('120', 120), ('1.1', 2), ('garbage', None), ('nan', None), (None, None)])
def test_retry_header(header, expected):
    assert agent.retry_delay(header) == expected


def test_smoke_redacts_answer(monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['agent', '--smoke'])
    monkeypatch.setattr(agent, 'answer', lambda *a, **kw: {'status': 'PASS', 'http_status': 200, 'output_text': 'hidden'})
    assert agent.main() == 0
    assert 'hidden' not in capsys.readouterr().out


def test_malformed_response_is_safe():
    with client_for(lambda r: httpx.Response(200, json=['malformed'])) as client:
        assert agent.answer('Question', client=client)['status'] == 'EXECUTION_ERROR'


@pytest.mark.parametrize('question,limit', [('', 512), ('Question', 0), ('Question', 8193)])
def test_invalid_input_no_request(question, limit):
    assert agent.answer(question, max_output_tokens=limit)['status'] == 'INVALID_INPUT'
