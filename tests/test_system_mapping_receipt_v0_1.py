from __future__ import annotations

import copy
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
PROVISIONAL_KIND = "STRUCTURAL_MAPPING_PROVISIONAL_RECORDED"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checker_path(path: Path) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    result = subprocess.run(
        [sys.executable, str(CHECKER), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.stdout, result.stderr
    payload = json.loads(result.stdout)
    return result, payload


def run_checker(name: str) -> tuple[subprocess.CompletedProcess[str], dict[str, Any]]:
    return run_checker_path(EXAMPLES / name)


def write_temp_receipt(tmp_path: Path, payload: dict[str, Any], filename: str) -> Path:
    path = tmp_path / filename
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_schema_is_draft7() -> None:
    Draft7Validator.check_schema(load_json(SCHEMA))


def test_examples_have_receipt_declared_source_coverage() -> None:
    for path in EXAMPLES.glob("*.json"):
        payload = load_json(path)
        assert "source_claim_refs" in payload
        assert "source_non_claim_refs" in payload


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


def test_example_mixed_boundary_records_structural_mapping() -> None:
    result, payload = run_checker("example_mixed_boundary.json")

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == RECORDED_KIND
    assert payload["errors"] == []


def test_example_unresolved_carried_forward_records_provisional_mapping() -> None:
    result, payload = run_checker("example_unresolved_carried_forward.json")

    assert result.returncode == 0, payload
    assert payload["result"]["result_kind"] == PROVISIONAL_KIND
    assert payload["errors"] == []


def test_counterexample_expansion_without_authority_records_authority_gap() -> None:
    result, payload = run_checker("counterexample_expansion_without_authority.json")

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "EXPANSION_AUTHORITY_GAP_RECORDED"
    codes = {error["code"] for error in payload["errors"]}
    assert "EXPANDED_CLAIM_EVIDENCE_REF_MISSING" in codes
    assert "EXPANSION_AUTHORITY_REF_MISSING" in codes


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


def test_expanded_authority_ref_must_not_self_reference_consumer(tmp_path: Path) -> None:
    receipt = copy.deepcopy(load_json(EXAMPLES / "example_expanded_with_authority.json"))
    added_claim = receipt["boundary_behavior_records"][0]["consumer_added_claims"][0]
    added_claim["authority_ref"] = receipt["consumer_system_ref"]

    result, payload = run_checker_path(write_temp_receipt(tmp_path, receipt, "self_authority.json"))

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "EXPANSION_AUTHORITY_GAP_RECORDED"
    assert "EXPANSION_AUTHORITY_REF_SELF_REFERENTIAL" in {
        error["code"] for error in payload["errors"]
    }


def test_expanded_authority_ref_must_not_point_to_fork_structural_receipt(tmp_path: Path) -> None:
    receipt = copy.deepcopy(load_json(EXAMPLES / "example_expanded_with_authority.json"))
    added_claim = receipt["boundary_behavior_records"][0]["consumer_added_claims"][0]
    added_claim["authority_ref"] = "fork:structural-receipt-only"

    result, payload = run_checker_path(write_temp_receipt(tmp_path, receipt, "structural_authority.json"))

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "EXPANSION_AUTHORITY_GAP_RECORDED"
    assert "EXPANSION_AUTHORITY_REF_STRUCTURAL_ONLY" in {
        error["code"] for error in payload["errors"]
    }


def test_receipt_declared_source_claims_require_mapping_records(tmp_path: Path) -> None:
    receipt = copy.deepcopy(load_json(EXAMPLES / "example_preserved_boundary.json"))
    receipt["source_claim_refs"].append("claim:omitted-upstream-claim")

    result, payload = run_checker_path(write_temp_receipt(tmp_path, receipt, "unmapped_claim.json"))

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "MAPPING_INCOMPLETE_RECORDED"
    assert "SOURCE_CLAIM_UNMAPPED" in {error["code"] for error in payload["errors"]}


def test_receipt_declared_source_non_claims_require_preserve_or_drop_disposition(tmp_path: Path) -> None:
    receipt = copy.deepcopy(load_json(EXAMPLES / "example_preserved_boundary.json"))
    receipt["source_non_claim_refs"].append("does_not_claim_unmapped_non_claim")

    result, payload = run_checker_path(write_temp_receipt(tmp_path, receipt, "unmapped_non_claim.json"))

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "NON_CLAIM_DROP_RECORDED"
    assert "SOURCE_NON_CLAIM_UNMAPPED" in {error["code"] for error in payload["errors"]}


def test_mixed_declaration_requires_distinct_per_claim_behaviors(tmp_path: Path) -> None:
    receipt = copy.deepcopy(load_json(EXAMPLES / "example_preserved_boundary.json"))
    receipt["consumer_declared_boundary_behavior"] = "MIXED"

    result, payload = run_checker_path(write_temp_receipt(tmp_path, receipt, "bad_mixed.json"))

    assert result.returncode == 1
    assert payload["result"]["result_kind"] == "MAPPING_INCOMPLETE_RECORDED"
    assert "MIXED_DECLARATION_WITHOUT_MIXED_RECORDS" in {
        error["code"] for error in payload["errors"]
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


def test_checker_documents_receipt_declared_coverage_limitation() -> None:
    _, payload = run_checker("example_preserved_boundary.json")

    assert payload["limitations"]["does_not_independently_fetch_upstream_source_record"] is True
    assert payload["limitations"]["validates_receipt_declared_source_coverage_only"] is True


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
