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
        "simulation_mixed_boundary_with_expansion.json",
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
    assert len(results) == 7
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
        "MIXED_WITH_EXPANSION",
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


def test_mixed_boundary_with_expansion_records_mapping() -> None:
    _, payload = run_harness()

    item = next(
        result
        for result in payload["simulation_results"]
        if result["simulation_class"] == "MIXED_WITH_EXPANSION"
    )

    assert item["observed_result_kind"] == "SIMULATION_MAPPING_RECORDED"
    assert item["checker_result_kind"] == "STRUCTURAL_MAPPING_RECORDED"


def test_market_analogue_fields_have_interpretation_boundary() -> None:
    for path in SIM_DIR.glob("simulation_*.json"):
        payload = load_json(path)
        analogue = payload["market_system_analogue"]
        boundary = analogue["analogue_interpretation_boundary"]

        assert "does not imply native vendor support" in boundary
        assert "product equivalence" in boundary
        assert "vendor-endorsed integration behavior" in boundary


def test_market_research_doc_clarifies_record_receipt_naming() -> None:
    doc = (ROOT / "docs" / "SYSTEM_MAPPING_RECORD_MARKET_STORAGE_RESEARCH_v0_1.md").read_text(
        encoding="utf-8"
    )

    assert "SYSTEM_MAPPING_RECORD is the broader conceptual category" in doc
    assert "SYSTEM_MAPPING_RECEIPT is the concrete v0.1 artifact" in doc


def test_market_research_doc_has_vendor_language_boundary() -> None:
    doc = (ROOT / "docs" / "SYSTEM_MAPPING_RECORD_MARKET_STORAGE_RESEARCH_v0_1.md").read_text(
        encoding="utf-8"
    )

    assert "not an exhaustive product analysis" in doc
    assert "do not assert product equivalence" in doc
    assert "does not claim that any platform cannot support claim-boundary metadata" in doc


def test_market_research_doc_avoids_unsafe_vendor_capability_claims() -> None:
    doc = (ROOT / "docs" / "SYSTEM_MAPPING_RECORD_MARKET_STORAGE_RESEARCH_v0_1.md").read_text(
        encoding="utf-8"
    ).lower()

    unsafe_phrases = [
        "fork is the only system",
        "vendors cannot",
        "vendor cannot",
        "market systems cannot",
        "market systems do not support claim boundaries",
        "databricks cannot",
        "purview cannot",
        "bedrock cannot",
        "vertex cannot",
        "langsmith cannot",
        "phoenix cannot",
        "w&b cannot",
        "mlflow cannot",
        "openlineage cannot",
        "opentelemetry cannot",
    ]

    for phrase in unsafe_phrases:
        assert phrase not in doc


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
