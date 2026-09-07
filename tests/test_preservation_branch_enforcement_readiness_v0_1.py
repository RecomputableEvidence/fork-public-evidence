from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_preservation_branch_enforcement_readiness_v0_1.py"
RECORD = ROOT / (
    "policies/repository-hardening/"
    "PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1.json"
)


def load_checker():
    spec = importlib.util.spec_from_file_location("preservation_enforcement", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def codes(findings):
    return {item["code"] for item in findings}


def test_readiness_record_conforms_not_applied() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == "PRESERVATION_ENFORCEMENT_READINESS_CONFORMS_NOT_APPLIED"


def test_direct_first_parent_commit_is_detected() -> None:
    checker = load_checker()
    rows = ["a" * 40 + " " + "b" * 40]
    assert "NON_MERGE_FIRST_PARENT_COMMIT" in codes(checker.topology_findings(rows))


def test_octopus_merge_is_detected() -> None:
    checker = load_checker()
    rows = ["a" * 40 + " " + "b" * 40 + " " + "c" * 40 + " " + "d" * 40]
    assert "OCTOPUS_FIRST_PARENT_COMMIT" in codes(checker.topology_findings(rows))


def test_two_parent_merge_topology_is_accepted() -> None:
    checker = load_checker()
    rows = ["a" * 40 + " " + "b" * 40 + " " + "c" * 40]
    assert checker.topology_findings(rows) == []


def test_merge_subject_requires_pr_marker() -> None:
    checker = load_checker()
    assert checker.subject_has_pr_marker("Merge PR #137: example")
    assert checker.subject_has_pr_marker("Preserve example (#123)")
    assert not checker.subject_has_pr_marker("Merge an unbound local branch")


def test_readiness_cannot_claim_protection_already_applied() -> None:
    checker = load_checker()
    record = load_record()
    record["live_repository_settings_observation"]["branch_protection_observed"] = True
    assert "LIVE_SETTINGS_PROMOTION" in codes(checker.validate_record(record))


def test_required_context_list_cannot_silently_change() -> None:
    checker = load_checker()
    record = load_record()
    record["required_check_context_verification"]["declared_required_contexts"].pop()
    assert "DECLARED_CONTEXTS_MISMATCH" in codes(checker.validate_record(record))


def test_application_profile_cannot_add_approval_requirement() -> None:
    checker = load_checker()
    record = load_record()
    record["application_profile"]["required_approving_reviews"] = 1
    assert "PROFILE_APPROVAL_COUNT" in codes(checker.validate_record(record))


def test_tool_surface_cannot_be_promoted_to_branch_protection_write() -> None:
    checker = load_checker()
    record = load_record()
    record["application_capability"]["branch_protection_write_action_available_in_connected_tool_surface"] = True
    assert "TOOLING_CAPABILITY_PROMOTION" in codes(checker.validate_record(record))


def test_governing_disposition_cannot_be_silently_superseded() -> None:
    checker = load_checker()
    record = load_record()
    record["governing_disposition"]["superseded"] = True
    assert "DISPOSITION_SUPERSESSION" in codes(checker.validate_record(record))
