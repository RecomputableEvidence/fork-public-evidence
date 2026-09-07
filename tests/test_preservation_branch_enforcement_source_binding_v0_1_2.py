from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_preservation_branch_enforcement_source_binding_v0_1_2.py"
DISPOSITION = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_DISPOSITION_2026_09_06_v0_1_2.json"
READINESS = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1_2.json"
PAYLOAD = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_RULESET_APPLICATION_PAYLOAD_2026_09_06_v0_1_2.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("preservation_source_binding", CHECKER)
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


def test_source_binding_surface_conforms_not_applied() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == "PRESERVATION_ENFORCEMENT_SOURCE_BINDING_CONFORMS_NOT_APPLIED"
    assert result["required_check_count"] == 6
    assert result["integration_id"] == 15368


def test_required_check_cannot_drop_integration_id() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    del status["parameters"]["required_status_checks"][0]["integration_id"]
    found = codes(checker.validate(d, r, p))
    assert "PAYLOAD_CHECK_BINDINGS" in found
    assert "PAYLOAD_UNBOUND_CHECK_SOURCE" in found


def test_required_check_cannot_change_integration_id() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    status["parameters"]["required_status_checks"][0]["integration_id"] = 999
    assert "PAYLOAD_CHECK_BINDINGS" in codes(checker.validate(d, r, p))


def test_context_name_cannot_change() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    status["parameters"]["required_status_checks"][0]["context"] = "Fork Evidence CI / Claim Boundary and Preservation Checks"
    assert "PAYLOAD_CHECK_BINDINGS" in codes(checker.validate(d, r, p))


def test_merge_only_must_survive() -> None:
    checker = load_checker()
    d, r, p = baseline()
    pr = next(x for x in p["request_body"]["rules"] if x["type"] == "pull_request")
    pr["parameters"]["allowed_merge_methods"] = ["merge", "squash"]
    assert "PAYLOAD_PR_PARAMETERS" in codes(checker.validate(d, r, p))


def test_bypass_actor_is_rejected() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["request_body"]["bypass_actors"] = [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}]
    assert "PAYLOAD_BYPASS" in codes(checker.validate(d, r, p))


def test_workflow_identity_limitation_cannot_be_removed_from_payload() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["known_limitation"]["statement"] = "RESOLVED"
    assert "PAYLOAD_LIMITATION" in codes(checker.validate(d, r, p))


def test_workflow_identity_limitation_cannot_be_promoted_to_resolved() -> None:
    checker = load_checker()
    d, r, p = baseline()
    p["known_limitation"]["standing"] = "RESOLVED"
    assert "PAYLOAD_LIMITATION_STANDING" in codes(checker.validate(d, r, p))


def test_readiness_cannot_claim_ruleset_applied() -> None:
    checker = load_checker()
    d, r, p = baseline()
    r["live_repository_settings_observation"]["branch_protection_observed"] = True
    assert "LIVE_SETTINGS_PROMOTION" in codes(checker.validate(d, r, p))


def test_connected_tool_surface_cannot_be_promoted_to_writer() -> None:
    checker = load_checker()
    d, r, p = baseline()
    r["application_capability"]["branch_ruleset_write_action_available_in_connected_tool_surface"] = True
    assert "TOOLING_CAPABILITY_PROMOTION" in codes(checker.validate(d, r, p))


def test_disposition_cannot_self_authorize_admin_action() -> None:
    checker = load_checker()
    d, r, p = baseline()
    d["disposition"]["administrator_application_authorized_by_this_record"] = True
    assert "DISPOSITION_AUTHORITY_PROMOTION" in codes(checker.validate(d, r, p))


def test_strict_required_checks_cannot_be_disabled() -> None:
    checker = load_checker()
    d, r, p = baseline()
    status = next(x for x in p["request_body"]["rules"] if x["type"] == "required_status_checks")
    status["parameters"]["strict_required_status_checks_policy"] = False
    assert "PAYLOAD_STRICT" in codes(checker.validate(d, r, p))
