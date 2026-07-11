from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

TOOL_PATH = Path("tools/csh_receiver_deterministic_v0_1.py")
FIXTURE_DIR = Path("tests/fixtures/csh/deterministic_receiver")
SCENARIO_PATH = FIXTURE_DIR / "scenario.json"
HANDOFF_PATH = FIXTURE_DIR / "handoff.json"


def load_receiver():
    spec = importlib.util.spec_from_file_location("csh_receiver_c", TOOL_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_fixture(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_control_response_is_boundary_preserving():
    receiver = load_receiver()
    result = receiver.build_response(
        read_fixture(SCENARIO_PATH),
        None,
        scenario_sha256="1" * 64,
        handoff_sha256=None,
        receiver_source_sha256="2" * 64,
    )
    assert result["condition"] == "control_h0"
    assert result["handoff_artifact_present"] is False
    assert result["response"]["downstream_claims"][0]["relationship_to_source"] == "PRESERVED"
    assert result["response"]["preserved_non_claims"] == [
        "The test fixture does not establish truth.",
        "The test fixture does not transfer authority.",
    ]
    assert result["response"]["reference_resolutions"] == [
        {"reference_id": "TEST_REF_1", "resolution_evidence": [], "status": "unresolved"}
    ]
    assert result["response"]["authority_inherited"] is False
    assert result["response"]["evidence_promotions"] == []
    assert result["response"]["verification_upgrades"] == []
    assert result["response"]["aggregate_state"] == "bounded"


def test_instrumented_response_preserves_context_without_promotion():
    receiver = load_receiver()
    result = receiver.build_response(
        read_fixture(SCENARIO_PATH),
        read_fixture(HANDOFF_PATH),
        scenario_sha256="1" * 64,
        handoff_sha256="3" * 64,
        receiver_source_sha256="2" * 64,
    )
    assert result["condition"] == "instrumented_h1"
    assert result["preserved_context"]["authority_references"] == ["TEST_AUTHORITY_REF"]
    assert result["preserved_context"]["evidence_references"] == ["TEST_EVIDENCE_REF"]
    assert result["response"]["authority_inherited"] is False
    assert result["response"]["evidence_promotions"] == []
    assert result["response"]["reference_resolutions"] == [
        {"reference_id": "TEST_REF_1", "resolution_evidence": [], "status": "unresolved"},
        {"reference_id": "TEST_AUTHORITY_REF", "resolution_evidence": [], "status": "unresolved"},
    ]


def test_canonical_serialization_is_byte_identical_and_lf():
    receiver = load_receiver()
    result = receiver.build_response(
        read_fixture(SCENARIO_PATH),
        read_fixture(HANDOFF_PATH),
        scenario_sha256="1" * 64,
        handoff_sha256="3" * 64,
        receiver_source_sha256="2" * 64,
    )
    first = receiver.canonical_json_bytes(result)
    second = receiver.canonical_json_bytes(result)
    assert first == second
    assert first.endswith(b"\n")
    assert b"\r\n" not in first
    assert not first.startswith(b"\xef\xbb\xbf")


def test_handoff_scenario_mismatch_is_rejected():
    receiver = load_receiver()
    handoff = read_fixture(HANDOFF_PATH)
    handoff["scenario_id"] = "DIFFERENT_SCENARIO"
    with pytest.raises(receiver.ReceiverInputError, match="does not match"):
        receiver.build_response(
            read_fixture(SCENARIO_PATH),
            handoff,
            scenario_sha256="1" * 64,
            handoff_sha256="3" * 64,
            receiver_source_sha256="2" * 64,
        )


def test_cli_repeated_runs_are_byte_identical(tmp_path: Path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    command = [
        sys.executable, str(TOOL_PATH), str(SCENARIO_PATH),
        "--handoff", str(HANDOFF_PATH), "--output",
    ]
    one = subprocess.run(command + [str(first)], capture_output=True, text=True)
    two = subprocess.run(command + [str(second)], capture_output=True, text=True)
    assert one.returncode == 0, one.stderr
    assert two.returncode == 0, two.stderr
    assert first.read_bytes() == second.read_bytes()


def test_receiver_source_avoids_nondeterministic_runtime_inputs():
    source = TOOL_PATH.read_text(encoding="utf-8")
    for token in (
        "import random", "import socket", "import requests", "urllib.request",
        "datetime.now", "time.time", "os.environ", "subprocess.",
    ):
        assert token not in source
