from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools' / 'check_boundary_crossing_evidence_inspectability_layer.py'
EXAMPLES = ROOT / 'examples' / 'boundary_crossing_evidence_inspectability_layer'


def run_checker(example_name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), str(EXAMPLES / example_name), '--compact'],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def payload(cp: subprocess.CompletedProcess[str]) -> dict:
    assert cp.stdout, cp.stderr
    return json.loads(cp.stdout)


def codes(cp: subprocess.CompletedProcess[str]) -> set[str]:
    return {err['code'] for err in payload(cp)['errors']}


def test_valid_glm_sc_handoff_passes() -> None:
    cp = run_checker('valid_glm_sc_handoff_v0_1.json')
    out = payload(cp)
    assert cp.returncode == 0, out
    assert out['ok'] is True
    assert out['result_kind'] == 'BOUNDARY_CROSSING_EVIDENCE_INSPECTABLE'
    assert out['limitations']['does_not_validate_truth'] is True
    assert out['limitations']['does_not_claim_endorsement'] is True


def test_authority_borrowing_fails_closed() -> None:
    cp = run_checker('invalid_authority_borrowing_v0_1.json')
    assert cp.returncode == 1
    assert 'AUTHORITY_BORROWING_ATTEMPTED' in codes(cp)


def test_dropped_non_claim_fails_closed() -> None:
    cp = run_checker('invalid_dropped_non_claim_v0_1.json')
    assert cp.returncode == 1
    assert 'NON_CLAIM_DROPPED' in codes(cp)


def test_public_attribution_leak_fails_closed() -> None:
    cp = run_checker('invalid_public_attribution_leak_v0_1.json')
    assert cp.returncode == 1
    assert 'PUBLIC_ATTRIBUTION_LEAK_DETECTED' in codes(cp)


def test_recomputation_overclaim_fails_closed() -> None:
    cp = run_checker('invalid_recomputation_overclaim_v0_1.json')
    assert cp.returncode == 1
    assert 'RECOMPUTATION_OVERCLAIM' in codes(cp)


def test_duplicate_json_key_fails_closed(tmp_path: Path) -> None:
    dup = tmp_path / 'duplicate.json'
    dup.write_text('{"layer_version":"0.1","layer_version":"0.1"}\n', encoding='utf-8')
    cp = subprocess.run(
        [sys.executable, str(TOOL), str(dup), '--compact'],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert cp.returncode == 1
    assert 'DUPLICATE_JSON_KEY' in codes(cp)


def test_utf8_bom_fails_closed(tmp_path: Path) -> None:
    bom = tmp_path / 'bom.json'
    bom.write_bytes(b'\xef\xbb\xbf{}')
    cp = subprocess.run(
        [sys.executable, str(TOOL), str(bom), '--compact'],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert cp.returncode == 1
    assert 'UTF8_BOM_DETECTED' in codes(cp)
