from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_system_mapping_simulations.py"
MANIFEST = ROOT / "examples" / "system_mapping_simulations" / "manifest_v0_1.json"
SIM_DIR = ROOT / "examples" / "system_mapping_simulations"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_harness() -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.stdout, result.stderr
    return result, json.loads(result.stdout)


def test_manifest_lists_all_simulation_fixtures() -> None:
    manifest = load_json(MANIFEST)
    paths = {Path(entry["path"]).name for entry in manifest["simulations"]}

    assert paths == {
        "simulation_clean_preserve.json",
        "simulation_safe_narrowing.json",
        "simulation_explicit_expansion_with_authority.json",
        "simulation_unsafe_expansion_without_authority.json",
        "simulation_non_claim_drop.json",
        "simulation_unresolved_laundering.json",
    }


def test_each_simulation_has_market_system_analogue_and_non_claims() -> None:
    for path in SIM_DIR.glob("simulation_*.json"):
        payload = load_json(path)
        assert payload["market_system_analogue"]["stored_as"]
        assert payload["market_system_analogue"]["fork_gap_tested"]
        assert "does_not_represent_real_vendor_behavior" in payload["simulation_non_claims"]


def test_harness_records_expected_outcomes() -> None:
    result, payload = run_harness()

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == "SIMULATION_MAPPING_RECORDED"
    assert payload["result"]["decision_boundary"] == "NON_DECISIONAL_SYNTHETIC_SIMULATION_RECORD_ONLY"
    assert payload["result"]["safe_to_automate_decisions"] is False
    assert payload["result"]["requires_human_interpretation_before_any_automation"] is True

    results = payload["simulation_results"]
    assert len(results) == 6
    assert all(item["expectation_recorded"] is True for item in results)


def test_simulation_classes_cover_core_handoff_failures() -> None:
    _, payload = run_harness()

    classes = {item["simulation_class"] for item in payload["simulation_results"]}

    assert classes == {
        "CLEAN_PRESERVE",
        "SAFE_NARROWING",
        "EXPLICIT_EXPANSION_WITH_AUTHORITY",
        "UNSAFE_EXPANSION_WITHOUT_AUTHORITY",
        "NON_CLAIM_DROP",
        "UNRESOLVED_LAUNDERING",
    }


def test_unsafe_expansion_records_expansion_gap() -> None:
    _, payload = run_harness()

    item = next(
        result
        for result in payload["simulation_results"]
        if result["simulation_class"] == "UNSAFE_EXPANSION_WITHOUT_AUTHORITY"
    )

    assert item["observed_result_kind"] == "SIMULATION_EXPANSION_GAP_RECORDED"
    assert item["checker_result_kind"] == "EXPANSION_AUTHORITY_GAP_RECORDED"


def test_non_claim_drop_records_non_claim_gap() -> None:
    _, payload = run_harness()

    item = next(
        result
        for result in payload["simulation_results"]
        if result["simulation_class"] == "NON_CLAIM_DROP"
    )

    assert item["observed_result_kind"] == "SIMULATION_NON_CLAIM_DROP_RECORDED"
    assert item["checker_result_kind"] == "NON_CLAIM_DROP_RECORDED"


def test_unresolved_laundering_records_unresolved_pointer_gap() -> None:
    _, payload = run_harness()

    item = next(
        result
        for result in payload["simulation_results"]
        if result["simulation_class"] == "UNRESOLVED_LAUNDERING"
    )

    assert item["observed_result_kind"] == "SIMULATION_UNRESOLVED_POINTER_GAP_RECORDED"
    assert item["checker_result_kind"] == "UNRESOLVED_POINTER_MAPPING_GAP_RECORDED"


def test_harness_output_avoids_direct_automation_shortcut_fields() -> None:
    _, payload = run_harness()

    direct_shortcut_keys = {
        "".join(["o", "k"]),
        "approved",
        "authorized",
        "compliant",
        "ready",
        "passed",
        "success",
        "is_approved",
        "is_authorized",
        "is_compliant",
        "is_ready",
    }

    assert not (set(payload["result"].keys()) & direct_shortcut_keys)
    assert payload["result"]["result_kind"] != "PASS"
    assert payload["result"]["result_kind"] != "OK"
    assert payload["result"]["result_kind"] != "SUCCESS"


def test_compact_output_is_parseable_json() -> None:
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--compact"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["result"]["result_kind"] == "SIMULATION_MAPPING_RECORDED"
