from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
CHECKER = load_module(ROOT / "tools/check_cross_system_claim_handoff_execution_v0_1_1.py", "csh_execution_v011")
STATE_PATH = ROOT / CHECKER.STATE
SEAL_PATH = ROOT / CHECKER.SEAL
FREEZE_PATH = ROOT / CHECKER.INSTRUMENTATION_FREEZE
FIXTURES = ROOT / "tests/fixtures/csh-execution-v0.1.1"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def test_repository_surface_passes_before_repeat_requirement():
    result = CHECKER.evaluate(ROOT, require_repeat=False)
    assert result["failed"] == 0, result


def test_original_attempt_cannot_be_replaced():
    state = load(STATE_PATH)
    seal = load(SEAL_PATH)
    freeze = load(FREEZE_PATH)
    changed = copy.deepcopy(state)
    changed["original_attempts"][0]["replaced"] = True
    errors = CHECKER.semantic_errors(changed, seal, freeze)
    assert any("cannot be replaced" in item for item in errors)


def test_repeat_cannot_reuse_original_identifier():
    state = load(STATE_PATH)
    seal = load(SEAL_PATH)
    freeze = load(FREEZE_PATH)
    changed = copy.deepcopy(state)
    repeated = copy.deepcopy(changed["original_attempts"][0])
    repeated["role"] = "post_repair_repetition"
    repeated["linked_original_run_id"] = "CSH-RUN-001"
    changed["repeat_runs"] = [repeated]
    errors = CHECKER.semantic_errors(changed, seal, freeze)
    assert any("must not reuse original" in item for item in errors)


def test_mutable_execution_state_is_not_in_immutable_freeze():
    state = load(STATE_PATH)
    seal = load(SEAL_PATH)
    freeze = load(FREEZE_PATH)
    changed = copy.deepcopy(freeze)
    changed["immutable_artifacts"].append({
        "path": CHECKER.STATE.as_posix(),
        "sha256": "0" * 64,
        "size_bytes": 1,
    })
    errors = CHECKER.semantic_errors(state, seal, changed)
    assert any("must not be listed as immutable" in item for item in errors)


def test_valid_fixture_has_bounded_semantics():
    fixture = load(FIXTURES / "valid_execution_state.json")
    seal = load(SEAL_PATH)
    freeze = load(FREEZE_PATH)
    assert CHECKER.semantic_errors(fixture, seal, freeze) == []


def test_invalid_fixtures_are_rejected():
    seal = load(SEAL_PATH)
    freeze = load(FREEZE_PATH)
    cases = {
        "invalid_original_replaced.json": "cannot be replaced",
        "invalid_repeat_reuses_original_id.json": "must not reuse original",
    }
    for name, expected in cases.items():
        errors = CHECKER.semantic_errors(load(FIXTURES / name), seal, freeze)
        assert any(expected in item for item in errors), (name, errors)
