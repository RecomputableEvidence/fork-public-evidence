from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_preservation_branch_enforcement_context_repair_v0_1_1.py"
DISPOSITION = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_DISPOSITION_2026_09_06_v0_1_1.json"
READINESS = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1_1.json"
PAYLOAD = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_RULESET_APPLICATION_PAYLOAD_2026_09_06_v0_1_1.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("preservation_context_repair", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def baseline():
    return load_json(DISPOSITION), load_json(READINESS), load_json(PAYLOAD)


def codes(findings):
    return {item["code"] for item in findings}


def test_corrected_o2_surface_conforms_not_applied() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == "PRESERVATION_ENFORCEMENT_CONTEXT_REPAIR_CONFORMS_NOT_APPLIED"
    assert result["required_context_count"] == 6


def test_composite_context_is_rejected_in_disposition() -> None:
    checker = load_checker()
    d, r, p = baseline()
    d["corrected_interim_profile"]["required_status_checks"][0] = (
        "Fork Evidence CI / Claim Boundary and Preservation Checks"
    )
    assert "DISPOSITION_CONTEXTS" in codes(checker.validate(d, r, p))


def test_predecessor_exact_match_promotion_must_remain_invalid() -> None:
    checker = load_checker()
    d, r, p = baseline()
    r["required_check_context_verification"]["predecessor_composite_context_match"] = (
        "6_OF_6_EXACT_NAME_MATCH"
    )
    assert "PREDECESSOR_DEFECT_NOT_PRESERVED" in codes(checker.validate(d, r, p))


def test_ruleset_target_branch_cannot_change() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["conditions"]["ref_name"]["include"] = ["refs/heads/main"]
    assert "PAYLOAD_REF" in codes(checker.validate(d, r, p))


def test_bypass_actor_is_rejected() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["bypass_actors"] = [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
    assert "PAYLOAD_BYPASS" in codes(checker.validate(d, r, p))


def test_strict_status_checks_cannot_be_disabled() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status_rule = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    status_rule["parameters"]["strict_required_status_checks_policy"] = False
    assert "PAYLOAD_STATUS_STRICT" in codes(checker.validate(d, r, p))


def test_required_context_cannot_be_removed() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status_rule = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    status_rule["parameters"]["required_status_checks"].pop()
    assert "PAYLOAD_STATUS_CONTEXTS" in codes(checker.validate(d, r, p))


def test_review_requirement_cannot_be_silently_added() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["rules"][2]["parameters"]["required_approving_review_count"] = 1
    assert "PAYLOAD_PR_PARAMETER" in codes(checker.validate(d, r, p))


def test_conversation_resolution_cannot_be_disabled() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["rules"][2]["parameters"]["required_review_thread_resolution"] = False
    assert "PAYLOAD_PR_PARAMETER" in codes(checker.validate(d, r, p))


def test_extra_unattributed_change_approval_cannot_reappear() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["rules"][2]["parameters"]["require_extra_approval_for_unattributed_changes"] = True
    assert "PAYLOAD_PR_PARAMETER" in codes(checker.validate(d, r, p))


def test_payload_cannot_claim_already_applied() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["status"] = "APPLIED"
    assert "PAYLOAD_STATUS" in codes(checker.validate(d, r, p))


def test_readiness_cannot_claim_live_protection() -> None:
    checker = load_checker()
    d, r, p = baseline()
    r["live_repository_settings_observation"]["branch_protection_observed"] = True
    assert "LIVE_SETTINGS_PROMOTION" in codes(checker.validate(d, r, p))


def test_squash_or_rebase_cannot_be_permitted() -> None:
    checker = load_checker()
    d, r, p = baseline()
    pr_rule = next(x for x in p["request_body"]["rules"] if x["type"] == "pull_request")
    pr_rule["parameters"]["allowed_merge_methods"] = ["merge", "squash", "rebase"]
    assert "PAYLOAD_PR_PARAMETER" in codes(checker.validate(d, r, p))


def test_readiness_merge_method_must_match_lineage_witness() -> None:
    checker = load_checker()
    d, r, p = baseline()
    r["application_profile"]["allowed_merge_methods"] = ["merge", "squash"]
    assert "PROFILE_CONTROL" in codes(checker.validate(d, r, p))


def test_disposition_must_bind_merge_method_repair() -> None:
    checker = load_checker()
    d, r, p = baseline()
    d["change_boundary"]["adds_merge_method_constraint_for_lineage_consistency"] = False
    assert "CHANGE_BOUNDARY_MERGE_METHOD" in codes(checker.validate(d, r, p))
