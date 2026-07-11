from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path

CHECKER_PATH = Path("tools/check_csh_configuration_v0_1.py")
BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")


def load_checker():
    spec = importlib.util.spec_from_file_location("csh_configuration_checker", CHECKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_complete_configuration_passes_while_unfrozen():
    checker = load_checker()
    result = checker.evaluate(Path.cwd())
    assert result["failed"] == 0, result


def test_prompt_pairs_differ_only_by_handoff_state_artifact():
    checker = load_checker()
    for scenario_id in checker.SCENARIO_IDS:
        control = json.loads((checker.prompt_path(scenario_id, "control_h0")).read_text(encoding="utf-8"))
        treatment = json.loads((checker.prompt_path(scenario_id, "instrumented_h1")).read_text(encoding="utf-8"))
        assert control["handoff_state_artifact"] is None
        assert treatment["handoff_state_artifact"] is not None
        control.pop("handoff_state_artifact")
        treatment.pop("handoff_state_artifact")
        assert control == treatment


def test_run_order_is_complete_unique_and_balanced():
    order = json.loads((BASE / "prompts/RUN_ORDER_v0_1.json").read_text(encoding="utf-8"))
    units = order["units"]
    assert len(units) == 108
    assert len({unit["planned_run_id"] for unit in units}) == 108
    assert Counter(unit["condition"] for unit in units) == {"control_h0": 54, "instrumented_h1": 54}
    assert Counter(unit["receiver_class_id"] for unit in units) == {
        "llm_receiver_a": 36,
        "llm_receiver_b": 36,
        "deterministic_receiver": 36,
    }
    assert all(units[i]["pairing_key"] == units[i + 1]["pairing_key"] for i in range(0, 108, 2))


def test_run_order_matches_public_fixed_algorithm():
    checker = load_checker()
    order = json.loads((checker.RUN_ORDER).read_text(encoding="utf-8"))
    assert order["fixed_salt"] == checker.RUN_ORDER_SALT
    assert order["units"] == checker.expected_run_units()
    first = [order["units"][i]["condition"] for i in range(0, 108, 2)]
    assert first.count("control_h0") == 27
    assert first.count("instrumented_h1") == 27


def test_registry_binds_exact_adapter_and_configuration_hashes():
    checker = load_checker()
    registry = json.loads((checker.REGISTRY).read_text(encoding="utf-8"))
    assert registry == checker.expected_registry(Path.cwd(), registry["registry_status"])
    assert "UNASSIGNED" not in json.dumps(registry)


def test_baseline_remains_blocked_before_freeze():
    freeze = json.loads((BASE / "CORPUS_FREEZE_v0_1.json").read_text(encoding="utf-8"))
    manifest = json.loads((BASE / "EXPERIMENT_MANIFEST_v0_1.json").read_text(encoding="utf-8"))
    assert freeze["freeze_status"] == "draft_unfrozen"
    assert freeze["baseline_execution_permitted"] is False
    assert freeze["blocking_unresolved_items"]
    assert manifest["freeze_status"] == "draft_unfrozen"
    assert manifest["baseline_run_status"] == "not_started"
