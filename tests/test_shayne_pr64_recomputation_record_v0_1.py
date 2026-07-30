from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_shayne_pr64_recomputation_record_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("shayne_pr64_record", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_candidate_recomputes_without_findings() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["ok"] is True
    assert result["findings"] == []
    assert result["status"] == (
        "SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_CONFORMS_NOT_ADMITTED"
    )
    assert result["standing"] == {
        "reviewer_declared_disposition": "REPRODUCED_WITHIN_DECLARED_SCOPE",
        "admission_state": "REVIEW_ELIGIBLE_NOT_ADMITTED",
        "pr_63_state": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
        "execution_authority_delta": "NONE",
        "pair_001_execution_authorized": False,
    }


def test_source_is_exact_and_attachment_gap_is_not_filled() -> None:
    checker = load_checker()
    source = ROOT / checker.SOURCE
    record = json.loads((ROOT / checker.RECORD).read_text(encoding="utf-8"))
    assert source.stat().st_size == 2672
    assert checker.sha256(source) == checker.SOURCE_SHA256
    attachment = record["source"]["referenced_full_findings_attachment"]
    assert attachment["status"] == "REFERENCED_NOT_RECEIVED"
    assert attachment["repository_bytes_received"] is False
    assert attachment["not_reconstructed_from_summary"] is True
    assert record["source"]["source_class"] == (
        "ATTRIBUTABLE_REVIEWER_TRANSMISSION_SUMMARY"
    )


def test_changed_path_observation_remains_non_defect() -> None:
    checker = load_checker()
    record = json.loads((ROOT / checker.RECORD).read_text(encoding="utf-8"))
    observation = record["changed_path_observation"]
    assert observation["classification"] == (
        "CHANGED_PATH_INVENTORY_TRANSITIVELY_BOUND_NOT_FIRST_CLASS_ENUMERATED"
    )
    assert observation["standing"] == "OBSERVATION_NOT_DEFECT"
    assert set(observation["effects"]) == {
        "NO_INTEGRITY_GAP",
        "NO_RECOMPUTATION_FAILURE",
        "REVIEWER_DERIVATION_REQUIRED",
    }
    assert observation["pr_64_standing_effect"] == "NONE"


def test_withdrawn_heuristic_is_preserved_as_process_evidence() -> None:
    checker = load_checker()
    process = json.loads((ROOT / checker.PROCESS).read_text(encoding="utf-8"))
    assert process["status"] == "PRESERVED_WITHDRAWN_FALSE_FINDING"
    assert [item["state"] for item in process["sequence"]] == [
        "CRUDE_REPRESENTATION",
        "APPARENT_COVERAGE_DEFECT",
        "CANONICAL_BINDING_INSPECTED",
        "FALSE_FINDING_WITHDRAWN_BEFORE_TRANSMISSION",
    ]
    assert process["classification"]["review_defect_created"] is False
    assert process["classification"]["pr_64_integrity_effect"] == "NONE"


def materialize_candidate_files(tmp_path: Path, checker) -> Path:
    root = tmp_path / "repo"
    for relative in (
        checker.PACKAGE,
        checker.ANCHOR.parent,
        checker.PREDECESSOR_ANCHOR.parent,
        checker.PLAN.parent,
        checker.IVS_RECEIPT.parent,
        checker.READINESS.parent,
    ):
        source = ROOT / relative
        destination = root / relative
        if destination.exists():
            continue
        shutil.copytree(source, destination)
    return root


def test_source_tamper_fails_closed(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize_candidate_files(tmp_path, checker)
    source = root / checker.SOURCE
    source.write_bytes(source.read_bytes() + b"tamper\n")
    result = checker.evaluate(root)
    codes = {item["code"] for item in result["findings"]}
    assert result["ok"] is False
    assert result["status"] == (
        "SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_NONCONFORMING"
    )
    assert "SOURCE_SHA256_MISMATCH" in codes
    assert "BOUND_ARTIFACT_SHA256_MISMATCH" in codes


def test_attachment_promotion_and_execution_promotion_fail_closed(
    tmp_path: Path,
) -> None:
    checker = load_checker()
    root = materialize_candidate_files(tmp_path, checker)
    record_path = root / checker.RECORD
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["source"]["referenced_full_findings_attachment"]["status"] = "RECEIVED"
    record["source"]["referenced_full_findings_attachment"][
        "repository_bytes_received"
    ] = True
    record_path.write_text(
        json.dumps(record, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    anchor_path = root / checker.ANCHOR
    anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
    anchor["admission_effect_if_merged"]["referenced_full_attachment_admitted"] = True
    anchor["admission_effect_if_merged"]["does_not_authorize_pair_001_execution"] = False
    anchor_path.write_text(
        json.dumps(anchor, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    result = checker.evaluate(root)
    codes = {item["code"] for item in result["findings"]}
    assert "ATTACHMENT_STATUS_MISMATCH" in codes
    assert "ANCHOR_ADMISSION_EFFECT_EXPANDED" in codes


def test_anchor_is_candidate_only_and_non_authorizing() -> None:
    checker = load_checker()
    anchor = json.loads((ROOT / checker.ANCHOR).read_text(encoding="utf-8"))
    assert anchor["status"] == "PROPOSED_APPEND_ONLY_ADMISSION"
    assert anchor["terminal_rule"] == {
        "candidate_cannot_prebind_its_own_future_merge": True,
        "opening_or_passing_ci_does_not_admit_candidate": True,
        "merge_requires_separate_explicit_authorization": True,
        "immediate_recursive_self_anchor_required": False,
    }
    effect = anchor["admission_effect_if_merged"]
    assert effect["pr_63_continuing_state"] == (
        "STRUCTURALLY_READY_EXECUTION_BLOCKED"
    )
    assert effect["referenced_full_attachment_admitted"] is False
    assert effect["does_not_authorize_pair_001_execution"] is True
    assert effect["does_not_transfer_authority"] is True
