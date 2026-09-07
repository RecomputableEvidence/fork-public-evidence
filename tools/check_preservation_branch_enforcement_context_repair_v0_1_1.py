#!/usr/bin/env python3
"""Validate corrected preservation-branch enforcement application surface v0.1.1."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DISPOSITION = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_DISPOSITION_2026_09_06_v0_1_1.json"
READINESS = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1_1.json"
PAYLOAD = ROOT / "policies/repository-hardening/PRESERVATION_BRANCH_RULESET_APPLICATION_PAYLOAD_2026_09_06_v0_1_1.json"

EXPECTED_CONTEXTS = [
    "Claim Boundary and Preservation Checks",
    "Root checksum manifest (ubuntu-latest)",
    "Root checksum manifest (windows-latest)",
    "Python proof surface (ubuntu-latest)",
    "Python proof surface (windows-latest)",
    "PowerShell 5.1 proof-surface entry point",
]
EXPECTED_REF = "refs/heads/preservation/clean-continuance-v0.1"


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise DuplicateKeyError(f"duplicate JSON key: {k}")
        out[k] = v
    return out


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=reject_duplicate_keys)


def codes(findings: list[dict[str, str]]) -> set[str]:
    return {f["code"] for f in findings}


def validate(disposition: Any, readiness: Any, payload: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    if disposition.get("record_kind") != "repository_enforcement_disposition_successor":
        add("DISPOSITION_KIND", "unexpected disposition kind", "$disposition.record_kind")
    if disposition.get("schema_version") != "0.1.1":
        add("DISPOSITION_VERSION", "unexpected disposition version", "$disposition.schema_version")
    if disposition.get("disposition", {}).get("repository_settings_effect") != "NONE":
        add("DISPOSITION_EFFECT_PROMOTION", "successor cannot claim settings already applied", "$disposition.disposition.repository_settings_effect")
    if disposition.get("disposition", {}).get("administrator_application_authorized_by_this_record") is not False:
        add("DISPOSITION_AUTHORITY_PROMOTION", "successor cannot self-authorize admin application", "$disposition.disposition.administrator_application_authorized_by_this_record")

    corrected = disposition.get("corrected_interim_profile", {}).get("required_status_checks")
    if corrected != EXPECTED_CONTEXTS:
        add("DISPOSITION_CONTEXTS", "corrected status contexts must exactly match check-run names", "$disposition.corrected_interim_profile.required_status_checks")
    if any(" / " in x for x in corrected or []):
        add("COMPOSITE_CONTEXT_REINTRODUCED", "workflow/job composite labels are not valid application identifiers here", "$disposition.corrected_interim_profile.required_status_checks")

    boundary = disposition.get("change_boundary", {})
    if boundary.get("changes_only_required_check_application_identifiers") is not False:
        add("CHANGE_BOUNDARY_IDENTIFIER_ONLY", "successor must preserve that repair is no longer identifier-only", "$disposition.change_boundary")
    if boundary.get("adds_merge_method_constraint_for_lineage_consistency") is not True:
        add("CHANGE_BOUNDARY_MERGE_METHOD", "successor must bind merge-method consistency repair", "$disposition.change_boundary")
    if disposition.get("corrected_interim_profile", {}).get("allowed_merge_methods") != ["merge"]:
        add("DISPOSITION_MERGE_METHOD", "preservation lineage permits merge commits only", "$disposition.corrected_interim_profile.allowed_merge_methods")

    if readiness.get("record_kind") != "preservation_branch_enforcement_application_readiness":
        add("READINESS_KIND", "unexpected readiness kind", "$readiness.record_kind")
    if readiness.get("status") != "READY_FOR_SEPARATE_ADMIN_APPLICATION_NOT_APPLIED":
        add("READINESS_STATUS", "readiness must remain not-applied", "$readiness.status")
    live = readiness.get("live_repository_settings_observation", {})
    if live.get("branch_protection_observed") is not False or live.get("branch_protection_enforcement_observed") != "OFF":
        add("LIVE_SETTINGS_PROMOTION", "readiness cannot claim preventive enforcement already applied", "$readiness.live_repository_settings_observation")

    verification = readiness.get("required_check_context_verification", {})
    if verification.get("corrected_required_contexts") != EXPECTED_CONTEXTS:
        add("READINESS_CONTEXTS", "readiness contexts mismatch", "$readiness.required_check_context_verification.corrected_required_contexts")
    if verification.get("observed_successful_contexts") != EXPECTED_CONTEXTS:
        add("OBSERVED_CONTEXTS", "observed successful check-run names mismatch", "$readiness.required_check_context_verification.observed_successful_contexts")
    if verification.get("corrected_required_context_match") != "6_OF_6_EXACT_CHECK_RUN_NAME_MATCH":
        add("READINESS_MATCH_STANDING", "exact match standing changed", "$readiness.required_check_context_verification.corrected_required_context_match")
    if verification.get("predecessor_composite_context_match") != "INVALID_AS_APPLICATION_IDENTIFIER":
        add("PREDECESSOR_DEFECT_NOT_PRESERVED", "predecessor identifier defect must remain explicit", "$readiness.required_check_context_verification.predecessor_composite_context_match")

    profile = readiness.get("application_profile", {})
    if profile.get("required_status_checks") != EXPECTED_CONTEXTS:
        add("PROFILE_CONTEXTS", "application profile contexts mismatch", "$readiness.application_profile.required_status_checks")
    expected_controls = {
        "pull_request_required": True,
        "required_approving_reviews": 0,
        "code_owner_review_required": False,
        "dismiss_stale_approvals": False,
        "require_last_push_approval": False,
        "require_extra_approval_for_unattributed_changes": False,
        "conversation_resolution_required": True,
        "require_branches_up_to_date_before_merge": True,
        "force_push_prohibited": True,
        "branch_deletion_prohibited": True,
        "administrator_bypass": "NONE",
        "allowed_merge_methods": ["merge"],
    }
    for key, expected in expected_controls.items():
        if profile.get(key) != expected:
            add("PROFILE_CONTROL", f"{key} must equal {expected!r}", f"$readiness.application_profile.{key}")

    if payload.get("record_kind") != "preservation_branch_ruleset_application_payload":
        add("PAYLOAD_KIND", "unexpected payload kind", "$payload.record_kind")
    if payload.get("status") != "PROPOSED_NOT_APPLIED":
        add("PAYLOAD_STATUS", "payload must remain proposed/not applied", "$payload.status")
    req = payload.get("request_body", {})
    if req.get("target") != "branch" or req.get("enforcement") != "active":
        add("PAYLOAD_TARGET", "ruleset must target an active branch ruleset", "$payload.request_body")
    if req.get("bypass_actors") != []:
        add("PAYLOAD_BYPASS", "no bypass actor is authorized", "$payload.request_body.bypass_actors")
    ref = req.get("conditions", {}).get("ref_name", {})
    if ref.get("include") != [EXPECTED_REF] or ref.get("exclude") != []:
        add("PAYLOAD_REF", "ruleset ref target changed", "$payload.request_body.conditions.ref_name")

    rules = req.get("rules")
    if not isinstance(rules, list):
        add("PAYLOAD_RULES", "rules must be a list", "$payload.request_body.rules")
        return findings

    by_type: dict[str, Any] = {}
    for rule in rules:
        if not isinstance(rule, dict) or "type" not in rule:
            add("PAYLOAD_RULE", "invalid rule object", "$payload.request_body.rules")
            continue
        if rule["type"] in by_type:
            add("PAYLOAD_DUPLICATE_RULE", f"duplicate rule type {rule['type']}", "$payload.request_body.rules")
        by_type[rule["type"]] = rule

    if set(by_type) != {"deletion", "non_fast_forward", "pull_request", "required_status_checks"}:
        add("PAYLOAD_RULE_SET", f"unexpected rule types {sorted(by_type)}", "$payload.request_body.rules")

    pr_params = by_type.get("pull_request", {}).get("parameters", {})
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
    for key, expected in expected_pr.items():
        if pr_params.get(key) != expected:
            add("PAYLOAD_PR_PARAMETER", f"{key} must equal {expected!r}", f"$payload.request_body.rules.pull_request.parameters.{key}")

    sc_params = by_type.get("required_status_checks", {}).get("parameters", {})
    if sc_params.get("strict_required_status_checks_policy") is not True:
        add("PAYLOAD_STATUS_STRICT", "required status checks must be strict", "$payload.request_body.rules.required_status_checks.parameters.strict_required_status_checks_policy")
    if sc_params.get("do_not_enforce_on_create") is not False:
        add("PAYLOAD_STATUS_CREATE", "do_not_enforce_on_create must remain false", "$payload.request_body.rules.required_status_checks.parameters.do_not_enforce_on_create")
    contexts = [x.get("context") for x in sc_params.get("required_status_checks", []) if isinstance(x, dict)]
    if contexts != EXPECTED_CONTEXTS:
        add("PAYLOAD_STATUS_CONTEXTS", "payload status contexts mismatch", "$payload.request_body.rules.required_status_checks.parameters.required_status_checks")
    if any(" / " in x for x in contexts if isinstance(x, str)):
        add("PAYLOAD_COMPOSITE_CONTEXT", "composite context identifier reintroduced", "$payload.request_body.rules.required_status_checks.parameters.required_status_checks")

    return findings


def evaluate() -> dict[str, Any]:
    try:
        disposition = load(DISPOSITION)
        readiness = load(READINESS)
        payload = load(PAYLOAD)
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": "PRESERVATION_ENFORCEMENT_CONTEXT_REPAIR_INVALID",
            "findings": [{"code": "INPUT_INVALID", "detail": str(exc), "path": "$input"}],
        }

    findings = validate(disposition, readiness, payload)
    return {
        "checker": Path(__file__).name,
        "status": (
            "PRESERVATION_ENFORCEMENT_CONTEXT_REPAIR_CONFORMS_NOT_APPLIED"
            if not findings
            else "PRESERVATION_ENFORCEMENT_CONTEXT_REPAIR_INVALID"
        ),
        "findings": findings,
        "required_context_count": len(EXPECTED_CONTEXTS),
        "non_claims": [
            "Conformance does not apply repository settings.",
            "Conformance does not independently verify GitHub's live effective ruleset state.",
            "Correct context names do not establish substantive correctness or independent governance.",
        ],
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
