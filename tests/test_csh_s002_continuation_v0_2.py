import json
from pathlib import Path
import shutil
import sys
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import continue_csh_s002_v0_2 as cont


def make_prior(path):
    manifest = cont.read(cont.EVIDENCE / 'PRESERVATION_MANIFEST.json')['files']
    for rel in manifest:
        target = path / rel; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cont.EVIDENCE / rel, target)
    return path


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    verified = cont.verify()
    prior = make_prior(tmp_path / 'prior')
    monkeypatch.setattr(cont, 'ROOT', tmp_path)
    monkeypatch.setattr(cont, 'verify', lambda expected=None: verified)
    marker = tmp_path / cont.predecessor.CAMPAIGN; marker.mkdir()
    cont.save(marker / 'claim.json', {'freeze_sha256': cont.ORIGINAL_FREEZE,
        'output_directory': str(prior.resolve()), 'status': 'CLAIMED_NO_AUTOMATIC_RESUME'})
    return verified, prior, marker


def client_for(handler):
    httpx = pytest.importorskip('httpx')
    perplexity = pytest.importorskip('perplexity')
    return perplexity.Perplexity(api_key='fixture-secret', max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler), trust_env=False))


def reply(model):
    return {'id':'fixture','object':'response','created_at':1,'status':'completed','model':model,
        'output':[{'type':'message','id':'m','status':'completed','role':'assistant',
                   'content':[{'type':'output_text','text':'```json\n{"transfer":"fixture"}\n```','annotations':[]}]}],
        'tools':[], 'usage':{'cost':{'currency':'USD','total_cost':0.00001}}}


def test_frozen_continuation_carries_once_and_preserves_order():
    freeze, plan, sha, carried = cont.verify()
    assert len(freeze['remaining_units']) == 23
    assert [u['unit_id'] for u in freeze['remaining_units']] == [u['unit_id'] for u in plan['units'][1:]]
    assert carried['status'] == 'PASS' and carried['original_status'] == 'FAIL'
    assert carried['request_repeated'] is False and carried['actual_usd'] == '0.00059'
    assert len(sha) == 64


def test_wrong_digest_rejected():
    with pytest.raises(ValueError, match='digest'): cont.verify('0' * 64)


def test_reordered_frozen_units_rejected(tmp_path, monkeypatch):
    freeze = cont.read(cont.CONTINUATION)
    freeze['remaining_units'].reverse()
    target = tmp_path / 'freeze.json'; cont.save(target, freeze)
    monkeypatch.setattr(cont, 'CONTINUATION', target)
    with pytest.raises(ValueError, match='order'): cont.verify()


@pytest.mark.parametrize('kind', ['tamper', 'missing', 'extra'])
def test_prior_file_failures(tmp_path, kind):
    prior = make_prior(tmp_path / 'prior')
    if kind == 'tamper': (prior / 'ledger.json').write_bytes(b'{}')
    if kind == 'missing': (prior / 'ledger.json').unlink()
    if kind == 'extra': (prior / 'extra.json').write_bytes(b'{}')
    with pytest.raises(ValueError): cont.verify_prior_output(prior)


def test_full_continuation_only_sends_remaining(isolated, tmp_path):
    httpx = pytest.importorskip('httpx')
    verified, prior, marker = isolated; out = tmp_path / 'out'; calls = []
    before = {p.relative_to(prior).as_posix():p.read_bytes() for p in prior.rglob('*') if p.is_file()}
    def handle(req):
        calls.append(req.content)
        ledger = cont.read(out / 'ledger.json')
        assert ledger['gross_committed_usd'] == str(cont.Decimal('0.09') + len(calls)*cont.Decimal('0.03'))
        assert ledger['results'][-1]['status'] == 'RESERVED_OUTCOME_UNKNOWN'
        return httpx.Response(200, json=reply(json.loads(req.content)['model']))
    with client_for(handle) as client:
        result = cont.execute(out, verified[2], prior, client)
        with pytest.raises(FileExistsError): cont.execute(tmp_path / 'again', verified[2], prior, client)
    assert len(calls) == result['new_requests_attempted'] == 23
    assert calls == [cont.wire(u['request']) for u in verified[1]['units'][1:]]
    assert result['status'] == 'COMPLETED_PENDING_CODING'
    assert result['gross_committed_usd'] == '0.78' and result['known_corpus_cost_usd'] == '0.00082'
    assert result['carried_units'] == 1
    assert cont.read(prior / 'ledger.json')['status'] == 'STOPPED'
    first_id = verified[1]['units'][0]['unit_id']
    assert cont.read(out / first_id / 'receipt.json')['status'] == 'FAIL'
    assert cont.read(out / first_id / 'successor_acceptance.json')['status'] == 'PASS'
    for rel, raw in before.items():
        assert (prior / rel).read_bytes() == (out / 'prior-attempt' / rel).read_bytes() == raw
    rows = cont.read(out / 'analysis-pending.json')
    assert len(rows) == 24 and all(r['task_state'] is None and r['classification'] is None for r in rows)
    assert 'fixture-secret' not in ''.join(p.read_text() for p in out.rglob('*') if p.is_file())


@pytest.mark.parametrize('mode', ['http', 'timeout', 'overrun', 'malformed', 'incomplete'])
def test_stop_and_keep_prior_cost(isolated, tmp_path, mode):
    httpx = pytest.importorskip('httpx')
    verified, prior, _ = isolated; calls = []
    def handle(req):
        calls.append(req)
        if mode == 'http': return httpx.Response(429, json={'error':'fixture'})
        if mode == 'timeout': raise httpx.ReadTimeout('fixture', request=req)
        data = reply(json.loads(req.content)['model'])
        if mode == 'overrun': data['usage']['cost']['total_cost'] = 0.08
        if mode == 'incomplete': data['status'] = 'incomplete'
        if mode == 'malformed': data['output'][0]['content'][0]['text'] = 'prose ```json\n{}\n```'
        return httpx.Response(200, json=data)
    with client_for(handle) as client: result = cont.execute(tmp_path / 'out', verified[2], prior, client)
    assert len(calls) == 1 and result['status'] == 'STOPPED' and result['carried_units'] == 1
    assert result['gross_committed_usd'] == ('0.17' if mode == 'overrun' else '0.12')
    assert result['known_corpus_cost_usd'] == ('0.08059' if mode == 'overrun' else '0.00059' if mode in ('http','timeout') else '0.00060')


def test_crash_retains_continuation_claim(isolated, tmp_path):
    verified, prior, marker = isolated
    def handle(req): raise KeyboardInterrupt()
    with client_for(handle) as client:
        with pytest.raises(KeyboardInterrupt): cont.execute(tmp_path / 'out', verified[2], prior, client)
        with pytest.raises(FileExistsError): cont.execute(tmp_path / 'again', verified[2], prior, client)
    ledger = cont.read(tmp_path / 'out' / 'ledger.json')
    assert ledger['gross_committed_usd'] == '0.12'
    assert ledger['results'][-1]['status'] == 'RESERVED_OUTCOME_UNKNOWN'
    assert (marker / 'claim.json').exists()


@pytest.mark.parametrize('kind', ['missing', 'wrong_freeze', 'wrong_directory'])
def test_bad_original_claim_blocks_transport(isolated, tmp_path, kind):
    verified, prior, marker = isolated
    if kind == 'missing': (marker / 'claim.json').unlink()
    else:
        claim = cont.read(marker / 'claim.json')
        claim['freeze_sha256' if kind == 'wrong_freeze' else 'output_directory'] = 'wrong'
        cont.save(marker / 'claim.json', claim)
    calls = []
    with client_for(lambda req:calls.append(req)) as client:
        with pytest.raises((ValueError, FileNotFoundError)): cont.execute(tmp_path / 'out', verified[2], prior, client)
    assert not calls and not (marker / 'continuation-v0-2').exists()


def test_missing_key_makes_no_continuation_claim(isolated, tmp_path, monkeypatch):
    verified, prior, marker = isolated
    monkeypatch.delenv('PERPLEXITY_API_KEY', raising=False)
    assert cont.execute(tmp_path / 'out', verified[2], prior)['status'] == 'CREDENTIAL_UNAVAILABLE'
    assert not (marker / 'continuation-v0-2').exists()
