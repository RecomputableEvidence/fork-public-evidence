import copy
import hashlib
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import parse_csh_s002_response_v0_2 as parser
import run_csh_s002_v0_1 as original

EVIDENCE = ROOT / 'docs/current-standing/CSH_S002_STOPPED_ATTEMPT_20261026'
UNIT = 'S002-SIM_F_POINTER_UNRESOLVED-B-H0-R1'
MODEL = 'anthropic/claude-haiku-5-5'


@pytest.mark.parametrize('text,form', [
    ('{}', 'bare_json'), (' \t\n{"a":1}\r\n', 'bare_json'),
    ('```json\n{"a":1}\n```', 'single_json_fence'),
    (' \n```json\r\n{"a":1}\r\n```\t', 'single_json_fence'),
    ('```json\n{"literal":"```"}\n```', 'single_json_fence'),
])
def test_valid_forms(text, form):
    parsed, actual_form = parser.parse_transfer(text)
    assert isinstance(parsed, dict) and actual_form == form


@pytest.mark.parametrize('text', [
    '```\n{}\n```', '```JSON\n{}\n```', '```python\n{}\n```',
    '```json {} ```', '```json\n{}', '```json\n{}\n````',
    'Explanation\n```json\n{}\n```', '```json\n{}\n```\nExplanation',
    '```json\n{}\n```\n```json\n{}\n```', '```json\n```json\n{}\n```\n```',
    '[]', '```json\n[]\n```', 'null', '```json\n{"x":NaN}\n```',
    '```json\n{"x":1,"x":2}\n```', '```json\n{"a":{"x":1,"x":2}}\n```',
    '{} {}', '```json\n{} {}\n```', '```json\n{"a":1,}\n```',
    '\ufeff```json\n{}\n```', None,
])
def test_reject_ambiguous_or_invalid_inputs(text):
    with pytest.raises((ValueError, TypeError)): parser.parse_transfer(text)


def test_original_evidence_preserved_and_old_failure_reproduces():
    manifest = json.loads((EVIDENCE / 'PRESERVATION_MANIFEST.json').read_text())
    assert len(manifest['files']) == 9
    for rel, expected in manifest['files'].items():
        assert hashlib.sha256((EVIDENCE / rel).read_bytes()).hexdigest() == expected
    freeze = original.PACKAGE / 'FREEZE.json'
    assert (EVIDENCE / 'FREEZE.json').read_bytes() == freeze.read_bytes()
    unit = EVIDENCE / UNIT
    assert (unit / 'request.json').read_bytes() == (original.PACKAGE / 'requests' / (UNIT + '.json')).read_bytes()
    ledger = json.loads((EVIDENCE / 'ledger.json').read_text())
    assert ledger['status'] == 'STOPPED' and len(ledger['results']) == 1
    data = json.loads((unit / 'response.bin').read_bytes())
    old, text = original.assess(data, MODEL)
    new, unchanged_text, parsed = parser.assess_response(data, MODEL)
    assert old['status'] == 'FAIL' and old['errors'] == ['transfer_json_object']
    assert new['status'] == 'PASS' and new['parse_form'] == 'single_json_fence'
    assert text == unchanged_text == (unit / 'output.txt').read_text()
    assert parsed['scenario_id'] == 'SIM_F_POINTER_UNRESOLVED'
    assert not new['corpus_continuation_enabled']


@pytest.mark.parametrize('change,error', [
    ({'status': 'incomplete'}, 'completion_status'),
    ({'model': 'substitute'}, 'model_identity'),
    ({'tools': [{'type': 'web_search'}]}, 'unexpected_tools_or_history'),
    ({'usage': {}}, 'cost_unavailable'),
    ({'usage': {'cost': {'currency': 'USD', 'total_cost': 0.04}}}, 'cost_above_reservation'),
])
def test_fence_repair_does_not_waive_other_checks(change, error):
    data = json.loads((EVIDENCE / UNIT / 'response.bin').read_bytes()); data.update(change)
    result, _, _ = parser.assess_response(data, MODEL)
    assert result['status'] == 'FAIL' and error in result['errors']


def test_review_retains_raw_bytes_and_does_not_overwrite(tmp_path):
    source = EVIDENCE / UNIT / 'response.bin'
    before = source.read_bytes()
    result = parser.review(source, tmp_path / 'review', MODEL)
    assert source.read_bytes() == before == (tmp_path / 'review' / 'response.bin').read_bytes()
    assert result['raw_response_sha256'] == hashlib.sha256(before).hexdigest()
    assert result['parsed_transfer_sha256'] == hashlib.sha256((tmp_path / 'review' / 'parsed_transfer.json').read_bytes()).hexdigest()
    with pytest.raises(FileExistsError): parser.review(source, tmp_path / 'review', MODEL)


def test_invalid_envelope_still_preserved(tmp_path):
    source = tmp_path / 'response.bin'; source.write_bytes(b'not-json')
    result = parser.review(source, tmp_path / 'review', MODEL)
    assert result['status'] == 'FAIL'
    assert (tmp_path / 'review' / 'response.bin').read_bytes() == b'not-json'
    assert not (tmp_path / 'review' / 'parsed_transfer.json').exists()
