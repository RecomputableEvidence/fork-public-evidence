from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_system_mapping_receipt.py"
SCHEMA = ROOT / "schemas" / "system_mapping_receipt_v0_1.schema.json"
EXAMPLES = ROOT / "examples" / "system_mapping_receipt"

RECORDED_KIND = "STRUCTURAL_MAPPING_RECORDED"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checker(name: str) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    result = subprocess.run(
        [sys.executable, str(CHECKER), str(EXAMPLES / name)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.stdout, result.stderr
    payload = json.loads(result.stdout)
    return result, payload


def test_schema_is_draft7() -> None:
    Draft7Validator.check_schema(load_json(SCHEMA))


def test_example_preserved_boundary_records_structural_mapping() -> None:
    result, payload = run_checker("example_preserved_boundary.json")

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == RECORDED_KIND
    assert payload["result"]["decision_boundary"] == "NON_DECISIONAL_STRUCTURAL_MAPPING_RECORD_ONLY"
    assert payload["result"]["safe_to_automate_decisions"] is False
    assert payload["result"]["requires_human_interpretation_before_any_automation"] is True
    assert payload["errors"] == []


def test_example_narrowed_boundary_records_structural_mapping() -> None:
    result, payload = run_checker("example_narrowed_boundary.json")

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == RECORDED_KIND
    assert payload["errors"] == []


def test_example_expanded_with_authority_records_structural_mapping() -> None:
    result, payload = run_checker("example_expanded_with_authority.json")

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == RECORDED_KIND
    assert payload["errors"] == []


def test_counterexample_expansion_without_authority_records_authority_gap() -> None:
    result, payload = run_checker("counterexample_expansion_without_authority.json")

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "EXPANSION_AUTHORITY_GAP_RECORDED"
    assert {error["code"] for error in payload["errors"]} == {
        "EXPANDED_CLAIM_EVIDENCE_REF_MISSING",
        "EXPANSION_AUTHORITY_REF_MISSING",
    }


def test_counterexample_non_claim_drop_records_disclosure_gap() -> None:
    result, payload = run_checker("counterexample_non_claim_dropped_without_disclosure.json")

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "NON_CLAIM_DROP_RECORDED"
    assert {error["code"] for error in payload["errors"]} == {
        "NON_CLAIM_DROPPED_WITHOUT_DISCLOSURE"
    }


def test_counterexample_unresolved_pointer_records_silent_resolution_gap() -> None:
    result, payload = run_checker("counterexample_unresolved_pointer_silently_resolved.json")

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "UNRESOLVED_POINTER_MAPPING_GAP_RECORDED"
    assert {error["code"] for error in payload["errors"]} == {
        "UNRESOLVED_POINTER_SILENTLY_RESOLVED"
    }


def test_checker_output_result_has_no_direct_automation_shortcut_fields() -> None:
    _, payload = run_checker("example_preserved_boundary.json")

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

    result_keys = set(payload["result"].keys())
    assert not (result_keys & direct_shortcut_keys)
    assert payload["result"]["result_kind"] != "STRUCTURAL_PASS"
    assert payload["result"]["result_kind"] != "STRUCTURAL_FAIL"


def test_defensive_do_not_map_tokens_are_present_only_as_limitations() -> None:
    _, payload = run_checker("example_preserved_boundary.json")

    assert "APPROVAL" in payload["limitations"]["do_not_map_to"]
    assert "COMPLIANCE" in payload["limitations"]["do_not_map_to"]
    assert "AUTHORIZATION" in payload["limitations"]["do_not_map_to"]
    assert "SAFETY" in payload["limitations"]["do_not_map_to"]
    assert "TRUTH" in payload["limitations"]["do_not_map_to"]


def test_compact_output_is_parseable_json() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            str(EXAMPLES / "example_preserved_boundary.json"),
            "--compact",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["result"]["result_kind"] == RECORDED_KIND