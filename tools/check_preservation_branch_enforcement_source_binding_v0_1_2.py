#!/usr/bin/env python3
"""Validate O2 preservation-ruleset source binding v0.1.2."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DISPOSITION = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_DISPOSITION_2026_09_06_v0_1_2.json"
READINESS = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1_2.json"
PAYLOAD = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_RULESET_APPLICATION_PAYLOAD_2026_09_06_v0_1_2.json"

EXPECTED_INTEGRATION_ID = 15368
EXPECTED_REF = "refs/heads/preservation/clean-continuance-v0.1"
EXPECTED_CONTEXTS = [
    "Claim Boundary and Preservation Checks",
    "Root checksum manifest (ubuntu-latest)",
    "Root checksum manifest (windows-latest)",
    "Python proof surface (ubuntu-latest)",
    "Python proof surface (windows-latest)",
    "PowerShell 5.1 proof-surface entry point",
]
EXPECTED_CHECKS = [
    {"context": context, "integration_id": EXPECTED_INTEGRATION_ID}
    for context in EXPECTED_CONTEXTS
]


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def validate(disposition: Any, readiness: Any, payload: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    if disposition.get("schema_version") != "0.1.2":
        add("DISPOSITION_VERSION", "unexpected disposition version", "$disposition.schema_version")
    if disposition.get("disposition", {}).get("type") != "APPLICATION_SOURCE_BINDING_HARDENING":
        add("DISPOSITION_TYPE", "unexpected disposition", "$disposition.disposition.type")
    if disposition.get("disposition", {}).get("repository_settings_effect") != "NONE":
        add("DISPOSITION_EFFECT_PROMOTION", "disposition cannot claim settings application", "$disposition.disposition.repository_settings_effect")
    if disposition.get("disposition", {}).get("administrator_application_authorized_by_this_record") is not False:
        add("DISPOSITION_AUTHORITY_PROMOTION", "disposition cannot self-authorize admin action", "$disposition.disposition.administrator_application_authorized_by_this_record")
    if disposition.get("evidence", {}).get("github_actions_integration_id") != EXPECTED_INTEGRATION_ID:
        add("DISPOSITION_INTEGRATION", "unexpected GitHub Actions integration id", "$disposition.evidence.github_actions_integration_id")
    if disposition.get("application_profile", {}).get("required_status_checks") != EXPECTED_CHECKS:
        add("DISPOSITION_CHECK_BINDINGS", "required check bindings changed", "$disposition.application_profile.required_status_checks")
    if disposition.get("application_profile", {}).get("allowed_merge_methods") != ["merge"]:
        add("DISPOSITION_MERGE_METHOD", "preservation lineage permits merge commits only", "$disposition.application_profile.allowed_merge_methods")

    residuals = {
        item.get("statement"): item.get("standing")
        for item in disposition.get("residuals", [])
        if isinstance(item, dict)
    }
    if residuals.get("CHECK_NAME_PLUS_APP_ID_DOES_NOT_ESTABLISH_WORKFLOW_IDENTITY") != "PRESERVED_LIMITATION":
        add("WORKFLOW_IDENTITY_RESIDUAL", "workflow identity limitation must remain explicit", "$disposition.residuals")

    if readiness.get("schema_version") != "0.1.2":
        add("READINESS_VERSION", "unexpected readiness version", "$readiness.schema_version")
    if readiness.get("status") != "READY_FOR_SEPARATE_ADMIN_APPLICATION_NOT_APPLIED":
        add("READINESS_STATUS", "readiness must remain not applied", "$readiness.status")
    live = readiness.get("live_repository_settings_observation", {})
    if live.get("branch_protection_observed") is not False or live.get("branch_protection_enforcement_observed") != "OFF":
        add("LIVE_SETTINGS_PROMOTION", "readiness cannot claim protection is applied", "$readiness.live_repository_settings_observation")

    verification = readiness.get("required_check_source_verification", {})
    expected_observed = [
        {**binding, "observed_conclusion": "success"}
        for binding in EXPECTED_CHECKS
    ]
    if verification.get("expected_integration", {}).get("integration_id") != EXPECTED_INTEGRATION_ID:
        add("READINESS_INTEGRATION", "unexpected expected integration", "$readiness.required_check_source_verification.expected_integration")
    if verification.get("required_checks") != expected_observed:
        add("READINESS_CHECK_BINDINGS", "observed check/source bindings changed", "$readiness.required_check_source_verification.required_checks")
    if verification.get("match") != "6_OF_6_CONTEXT_AND_INTEGRATION_ID_MATCH":
        add("READINESS_MATCH", "source-binding match standing changed", "$readiness.required_check_source_verification.match")
    if readiness.get("application_profile", {}).get("required_status_checks") != EXPECTED_CHECKS:
        add("READINESS_PROFILE_CHECKS", "readiness application checks changed", "$readiness.application_profile.required_status_checks")
    if readiness.get("application_profile", {}).get("allowed_merge_methods") != ["merge"]:
        add("READINESS_MERGE_METHOD", "readiness must preserve merge-only lineage", "$readiness.application_profile.allowed_merge_methods")
    if readiness.get("application_capability", {}).get("branch_ruleset_write_action_available_in_connected_tool_surface") is not False:
        add("TOOLING_CAPABILITY_PROMOTION", "connected tool surface cannot be promoted to ruleset writer", "$readiness.application_capability.branch_ruleset_write_action_available_in_connected_tool_surface")

    if payload.get("schema_version") != "0.1.2":
        add("PAYLOAD_VERSION", "unexpected payload version", "$payload.schema_version")
    if payload.get("status") != "PROPOSED_NOT_APPLIED":
        add("PAYLOAD_STATUS", "payload must remain proposed/not applied", "$payload.status")
    req = payload.get("request_body", {})
    if req.get("target") != "branch" or req.get("enforcement") != "active":
        add("PAYLOAD_TARGET", "unexpected ruleset target/enforcement", "$payload.request_body")
    if req.get("bypass_actors") != []:
        add("PAYLOAD_BYPASS", "no bypass actor is authorized", "$payload.request_body.bypass_actors")
    ref = req.get("conditions", {}).get("ref_name", {})
    if ref.get("include") != [EXPECTED_REF] or ref.get("exclude") != []:
        add("PAYLOAD_REF", "target ref changed", "$payload.request_body.conditions.ref_name")

    rules = req.get("rules")
    if not isinstance(rules, list):
        add("PAYLOAD_RULES", "rules must be a list", "$payload.request_body.rules")
        return findings
    by_type = {rule.get("type"): rule for rule in rules if isinstance(rule, dict)}
    if set(by_type) != {"deletion", "non_fast_forward", "pull_request", "required_status_checks"}:
        add("PAYLOAD_RULE_SET", f"unexpected rule set {sorted(by_type)}", "$payload.request_body.rules")

    pr = by_type.get("pull_request", {}).get("parameters", {})
    expected_pr = {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": False,
        "require_code_owner_review": False,
        "require_last_push_approval": False,
        "required_review_thread_resolution": True,
        "required_reviewers": [],
        "allowed_merge_methods": ["merge"],
        "require_extra_approval_for_unattributed_changes": False,
    }
    if pr != expected_pr:
        add("PAYLOAD_PR_PARAMETERS", "pull-request parameters changed", "$payload.request_body.rules.pull_request.parameters")

    status = by_type.get("required_status_checks", {}).get("parameters", {})
    if status.get("strict_required_status_checks_policy") is not True:
        add("PAYLOAD_STRICT", "required checks must remain strict", "$payload.request_body.rules.required_status_checks.parameters.strict_required_status_checks_policy")
    if status.get("do_not_enforce_on_create") is not False:
        add("PAYLOAD_CREATE", "do_not_enforce_on_create changed", "$payload.request_body.rules.required_status_checks.parameters.do_not_enforce_on_create")
    if status.get("required_status_checks") != EXPECTED_CHECKS:
        add("PAYLOAD_CHECK_BINDINGS", "payload check/source bindings changed", "$payload.request_body.rules.required_status_checks.parameters.required_status_checks")
    for item in status.get("required_status_checks", []):
        if item.get("integration_id") != EXPECTED_INTEGRATION_ID:
            add("PAYLOAD_UNBOUND_CHECK_SOURCE", f"check lacks integration {EXPECTED_INTEGRATION_ID}", "$payload.request_body.rules.required_status_checks.parameters.required_status_checks")

    limitation = payload.get("known_limitation", {})
    if limitation.get("statement") != "CHECK_NAME_PLUS_APP_ID_DOES_NOT_ESTABLISH_WORKFLOW_IDENTITY":
        add("PAYLOAD_LIMITATION", "workflow identity limitation removed", "$payload.known_limitation.statement")
    if limitation.get("standing") != "PRESERVED_NOT_RESOLVED_BY_THIS_PAYLOAD":
        add("PAYLOAD_LIMITATION_STANDING", "workflow identity limitation standing changed", "$payload.known_limitation.standing")

    return findings


def evaluate() -> dict[str, Any]:
    try:
        disposition = load(DISPOSITION)
        readiness = load(READINESS)
        payload = load(PAYLOAD)
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": "PRESERVATION_ENFORCEMENT_SOURCE_BINDING_INVALID",
            "findings": [{"code": "INPUT_INVALID", "detail": str(exc), "path": "$input"}],
        }

    findings = validate(disposition, readiness, payload)
    return {
        "checker": Path(__file__).name,
        "status": (
            "PRESERVATION_ENFORCEMENT_SOURCE_BINDING_CONFORMS_NOT_APPLIED"
            if not findings
            else "PRESERVATION_ENFORCEMENT_SOURCE_BINDING_INVALID"
        ),
        "findings": findings,
        "required_check_count": len(EXPECTED_CHECKS),
        "integration_id": EXPECTED_INTEGRATION_ID,
        "non_claims": [
            "Conformance does not apply repository settings.",
            "Context plus integration ID does not establish workflow identity.",
            "This checker does not activate the dormant consumer-owned trusted-base gate.",
        ],
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
