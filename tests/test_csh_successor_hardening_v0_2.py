"""Offline regression contract: no credentials or live network required."""
import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock
from urllib.error import HTTPError

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import preflight_csh_s001_receivers_v0_2 as preflight
import check_csh_s001_packet_binding_v0_2 as binding
import build_csh_s001_packets_v0_1 as builder

FIXTURES = json.loads((ROOT / 'tests/fixtures/csh_s001/preflight_regression_v0_2.json').read_text())

@pytest.fixture(autouse=True)
def no_live_network(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError('Live network forbidden in regression tests')
    monkeypatch.setattr(preflight.urllib.request, 'urlopen', forbidden)
    monkeypatch.delenv('GROQ_API_KEY', raising=False)
    monkeypatch.delenv('DEEPSEEK_API_KEY', raising=False)


def response(provider):
    return {'model': preflight.CONFIGS[provider]['model'], 'choices': [
        {'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': '{"preflight":"ok"}'}}]}


def fake_http(raw, status=200):
    context = MagicMock()
    context.__enter__.return_value.read.return_value = raw
    context.__enter__.return_value.status = status
    return lambda *args, **kwargs: context


@pytest.mark.parametrize('provider', ['groq', 'deepseek'])
@pytest.mark.parametrize('case', FIXTURES, ids=[c['id'] for c in FIXTURES])
def test_response_contract(provider, case):
    data = copy.deepcopy(case['response'])
    if isinstance(data, dict) and data.get('model') == '$MODEL':
        data['model'] = preflight.CONFIGS[provider]['model']
    elif isinstance(data, dict) and data.get('model') == '$PREFIXED_MODEL':
        data['model'] = 'not-' + preflight.CONFIGS[provider]['model']
    result = preflight.assess_response(provider, 200, json.dumps(data).encode())
    assert result['status'] == case['expected_status']
    if 'expected_error' in case:
        assert case['expected_error'] in result['errors']


@pytest.mark.parametrize('raw', [b'not-json', b'\xff', b'{"model":1,"model":2}'])
def test_invalid_response_bytes(raw):
    assert preflight.assess_response('groq', 200, raw)['status'] == 'RESPONSE_NOT_JSON'


def test_duplicate_content_rejected():
    data = response('groq')
    data['choices'][0]['message']['content'] = '{"preflight":"wrong","preflight":"ok"}'
    assert 'content_json' in preflight.assess_response('groq', 200, json.dumps(data).encode())['errors']


def test_whitespace_json_content_is_valid():
    data = response('groq')
    data['choices'][0]['message']['content'] = '  { "preflight" : "ok" } \n'
    assert preflight.assess_response('groq', 200, json.dumps(data).encode())['status'] == 'PASS'


def test_missing_credentials_never_calls_opener(tmp_path):
    def forbidden(*a, **k):
        pytest.fail('opener called without credential')
    result = preflight.call('groq', tmp_path, opener=forbidden)
    assert result['status'] == 'CREDENTIAL_UNAVAILABLE'
    assert not result['request_attempted']


@pytest.mark.parametrize('provider', ['groq', 'deepseek'])
def test_valid_mock_call_preserves_exact_bytes(provider, tmp_path, monkeypatch):
    monkeypatch.setenv(preflight.CONFIGS[provider]['env'], 'dummy-only')
    raw = json.dumps(response(provider)).encode()
    result = preflight.call(provider, tmp_path, opener=fake_http(raw))
    assert result['status'] == 'PASS'
    assert (tmp_path / provider / 'response.bin').read_bytes() == raw
    assert b'dummy-only' not in (tmp_path / provider / 'request.json').read_bytes()
    assert b'dummy-only' not in (tmp_path / provider / 'receipt.json').read_bytes()
    with pytest.raises(FileExistsError):
        preflight.call(provider, tmp_path, opener=fake_http(raw))


def test_http_error_preserved(tmp_path, monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'dummy-only')
    def fail(*a, **k):
        raise HTTPError('https://example.invalid', 410, 'Gone', {}, io.BytesIO(b'gone'))
    result = preflight.call('groq', tmp_path, opener=fail)
    assert result['status'] == 'HTTP_ERROR' and result['http_status'] == 410
    assert (tmp_path / 'groq/response.bin').read_bytes() == b'gone'


def test_timeout_is_recorded_without_exception_secrets(tmp_path, monkeypatch):
    monkeypatch.setenv('GROQ_API_KEY', 'dummy-only')
    def fail(*a, **k):
        raise TimeoutError('dummy-only')
    result = preflight.call('groq', tmp_path, opener=fail)
    assert result['status'] == 'EXECUTION_ERROR'
    assert 'dummy-only' not in json.dumps(result)


def test_cli_default_is_not_success_or_live():
    result = subprocess.run([sys.executable, str(ROOT/'tools/preflight_csh_s001_receivers_v0_2.py')], capture_output=True)
    assert result.returncode == 2
    assert json.loads(result.stdout)['status'] == 'NOT_EXECUTED'


@pytest.fixture
def packets(tmp_path):
    builder.build(ROOT, tmp_path)
    return tmp_path


def test_actual_packet_bytes_match(packets):
    result = binding.evaluate(ROOT, packets)
    assert result['status'] == 'PASS', result
    assert result['passed'] == 20


@pytest.mark.parametrize('role', ['projection', 'control_packet', 'instrumented_packet'])
@pytest.mark.parametrize('reseal', [False, True])
def test_tampered_bytes_fail_even_when_manifest_resealed(packets, role, reseal):
    manifest_path = packets / binding.MANIFEST
    manifest = json.loads(manifest_path.read_text())
    entry = manifest['records'][0][role]
    path = packets / entry['path']
    path.write_bytes(path.read_bytes() + b' ')
    if reseal:
        import hashlib
        entry['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
    result = binding.evaluate(ROOT, packets)
    assert result['status'] == 'FAIL'
    assert any(c['name'].endswith(':'+role) and not c['passed'] for c in result['checks'])


@pytest.mark.parametrize('mutation', ['missing', 'extra', 'duplicate_scenario', 'wrong_count', 'path_escape', 'bad_json', 'wrong_hash', 'wrong_shape'])
def test_packet_input_rejections(packets, mutation):
    path = packets / binding.MANIFEST
    manifest = json.loads(path.read_text())
    entry = manifest['records'][0]['projection']
    if mutation == 'missing':
        (packets/entry['path']).unlink()
    elif mutation == 'extra':
        (packets/'unexpected.json').write_text('{}')
    elif mutation == 'duplicate_scenario':
        manifest['records'].append(manifest['records'][0])
    elif mutation == 'wrong_count':
        manifest['scenario_count'] = 0
    elif mutation == 'path_escape':
        entry['path'] = '../outside.json'
    elif mutation == 'wrong_hash':
        entry['sha256'] = '0'*64
    elif mutation == 'wrong_shape':
        manifest = []
    if mutation == 'bad_json':
        path.write_text('{')
    else:
        path.write_text(json.dumps(manifest))
    assert binding.evaluate(ROOT, packets)['status'] == 'FAIL'


def test_symlink_rejected(packets):
    path = next((packets/'projections').glob('*.json'))
    target = packets / 'target.json'
    target.write_bytes(path.read_bytes())
    path.unlink()
    try:
        path.symlink_to(target)
    except OSError:
        pytest.skip('OS does not permit symlink creation')
    assert binding.evaluate(ROOT, packets)['status'] == 'FAIL'
