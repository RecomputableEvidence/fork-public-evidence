from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/run_csh_provider_validation_v0_1_2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("csh_provider_validation", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE = load_module()


def valid_receipt(path: Path) -> dict:
    calls = []
    for spec in MODULE.MODEL_SPECS:
        calls.append(
            {
                **spec,
                "passed": True,
                "http_status": 200,
                "quota_headers": {"x-ratelimit-remaining": "99"},
                "quota_evidence": {
                    "available": True,
                    "basis": "RATE_LIMIT_REMAINING_HEADER",
                    "remaining_not_quantified": False,
                },
                "request_sha256": "a" * 64,
                "response_body_sha256": "b" * 64,
                "response_body_written": False,
                "returned_model": spec["expected_returned_model"],
                "response_text_sha256": "c" * 64,
                "usage": {"total_tokens": 4},
            }
        )
    return MODULE.build_receipt(
        calls,
        output=path,
        workflow_run_id="123",
        subject_commit="d" * 40,
        repository="RecomputableEvidence/fork-public-evidence",
    )


def test_probe_is_synthetic_and_not_pair_001() -> None:
    payload = MODULE.build_probe_request(MODULE.MODEL_SPECS[0]["requested_model"])
    rendered = MODULE.canonical_json_bytes(payload)
    assert b"CSH_PROVIDER_VALIDATION_OK" in rendered
    assert b"Pair-001" not in rendered
    assert b"cross_system_claim_handoff" not in rendered
    assert payload["max_tokens"] == 32
    assert payload["stream"] is False


def test_valid_receipt_verifies(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    assert MODULE.verify_receipt(path)["status"] == "PASS"


def test_pair_001_call_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["pair_001_calls_performed"] = 1
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Pair-001"):
        MODULE.verify_receipt(path)


def test_secret_persistence_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["authentication"]["secret_persisted"] = True
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="secret persistence"):
        MODULE.verify_receipt(path)


def test_missing_quota_evidence_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "receipt.json"
    receipt = valid_receipt(path)
    receipt["calls"][0]["quota_headers"] = {}
    receipt["calls"][0].pop("quota_evidence")
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="quota evidence"):
        MODULE.verify_receipt(path)
