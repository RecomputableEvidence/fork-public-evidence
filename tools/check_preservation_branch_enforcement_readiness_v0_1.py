#!/usr/bin/env python3
"""Verify preservation-branch governance lineage and enforcement-application readiness."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
READINESS_PATH = Path(
    "policies/repository-hardening/"
    "PRESERVATION_BRANCH_ENFORCEMENT_APPLICATION_READINESS_2026_09_06_v0_1.json"
)
DISPOSITION_PATH = Path(
    "policies/repository-hardening/"
    "PRESERVATION_BRANCH_ENFORCEMENT_DISPOSITION_2026_08_08_v0_1.json"
)
ANCHOR = "fd395540cf82c3e578510172d500c9e03ba1a86b"
EXPECTED_DISPOSITION_BLOB = "b03728ad5c149e725add07fdea32b56bbe394fe6"
EXPECTED_CONTEXTS = [
    "Fork Evidence CI / Claim Boundary and Preservation Checks",
    "Root Checksum Manifest v0.1 / Root checksum manifest (ubuntu-latest)",
    "Root Checksum Manifest v0.1 / Root checksum manifest (windows-latest)",
    "Fork Proof-Surface Integration / Python proof surface (ubuntu-latest)",
    "Fork Proof-Surface Integration / Python proof surface (windows-latest)",
    "Fork Proof-Surface Integration / PowerShell 5.1 proof-surface entry point",
]
PR_MARKER = re.compile(r"(?:#\d+|Merge PR #\d+|Merge pull request #\d+)", re.IGNORECASE)


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            assert_finite(child)
    elif isinstance(value, list):
        for child in value:
            assert_finite(child)


def strict_load(path: Path) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if check and completed.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed


def topology_findings(rows: list[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for row in rows:
        parts = row.split()
        if not parts:
            continue
        commit = parts[0]
        parent_count = len(parts) - 1
        if parent_count == 1:
            findings.append(
                {
                    "code": "NON_MERGE_FIRST_PARENT_COMMIT",
                    "detail": f"{commit} has one parent",
                    "path": "$lineage",
                }
            )
        elif parent_count == 0:
            findings.append(
                {
                    "code": "PARENTLESS_DESCENDANT_COMMIT",
                    "detail": f"{commit} has no parent",
                    "path": "$lineage",
                }
            )
        elif parent_count > 2:
            findings.append(
                {
                    "code": "OCTOPUS_FIRST_PARENT_COMMIT",
                    "detail": f"{commit} has {parent_count} parents",
                    "path": "$lineage",
                }
            )
    return findings


def subject_has_pr_marker(subject: str) -> bool:
    return PR_MARKER.search(subject) is not None


def inspect_lineage(target: str) -> dict[str, Any]:
    anchor_exists = run_git("cat-file", "-e", f"{ANCHOR}^{{commit}}", check=False)
    if anchor_exists.returncode != 0:
        return {
            "target": target,
            "rows": [],
            "findings": [
                {
                    "code": "ANCHOR_UNAVAILABLE",
                    "detail": ANCHOR,
                    "path": "$git",
                }
            ],
        }

    target_exists = run_git("cat-file", "-e", f"{target}^{{commit}}", check=False)
    if target_exists.returncode != 0:
        return {
            "target": target,
            "rows": [],
            "findings": [
                {
                    "code": "TARGET_UNAVAILABLE",
                    "detail": target,
                    "path": "$git",
                }
            ],
        }

    descendant = run_git("merge-base", "--is-ancestor", ANCHOR, target, check=False)
    if descendant.returncode != 0:
        return {
            "target": target,
            "rows": [],
            "findings": [
                {
                    "code": "ANCHOR_NOT_ANCESTOR",
                    "detail": f"{ANCHOR} is not an ancestor of {target}",
                    "path": "$git",
                }
            ],
        }

    raw = run_git(
        "rev-list",
        "--first-parent",
        "--parents",
        f"{ANCHOR}..{target}",
    ).stdout.strip()
    rows = [line for line in raw.splitlines() if line.strip()]
    findings = topology_findings(rows)

    for row in rows:
        commit = row.split()[0]
        subject = run_git("show", "-s", "--format=%s", commit).stdout.strip()
        if not subject_has_pr_marker(subject):
            findings.append(
                {
                    "code": "MERGE_WITHOUT_PR_MARKER",
                    "detail": f"{commit}: {subject}",
                    "path": "$lineage",
                }
            )

    return {
        "target": target,
        "rows": rows,
        "descendant_count": len(rows),
        "findings": findings,
    }


def validate_record(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    if not isinstance(record, dict):
        return [{"code": "RECORD_NOT_OBJECT", "detail": "expected object", "path": "$"}]

    expected_top = {
        "schema_version",
        "record_kind",
        "record_id",
        "record_date",
        "time_basis",
        "observed_at",
        "append_only",
        "status",
        "basis",
        "governing_disposition",
        "live_repository_settings_observation",
        "required_check_context_verification",
        "governed_lineage_audit",
        "application_profile",
        "activation_precondition_results",
        "application_capability",
        "post_application_verification_requirements",
        "non_claims",
    }
    if set(record) != expected_top:
        add(
            "TOP_LEVEL_KEYS",
            f"expected {sorted(expected_top)!r}; found {sorted(record)!r}",
            "$",
        )
        return findings

    constants = {
        "schema_version": "0.1",
        "record_kind": "preservation_branch_enforcement_application_readiness",
        "status": "READY_FOR_SEPARATE_ADMIN_APPLICATION_NOT_APPLIED",
        "append_only": True,
    }
    for key, expected in constants.items():
        if record.get(key) != expected:
            add("RECORD_CONSTANT", f"{key} must equal {expected!r}", f"$.{key}")

    basis = record["basis"]
    if basis.get("repository") != "RecomputableEvidence/fork-public-evidence":
        add("REPOSITORY_MISMATCH", "unexpected repository", "$.basis.repository")
    if basis.get("governed_branch") != "preservation/clean-continuance-v0.1":
        add("BRANCH_MISMATCH", "unexpected governed branch", "$.basis.governed_branch")

    disposition = record["governing_disposition"]
    if disposition.get("path") != DISPOSITION_PATH.as_posix():
        add("DISPOSITION_PATH", "unexpected governing disposition path", "$.governing_disposition.path")
    if disposition.get("git_blob_sha") != EXPECTED_DISPOSITION_BLOB:
        add("DISPOSITION_DECLARED_BLOB", "unexpected governing disposition blob", "$.governing_disposition.git_blob_sha")
    if disposition.get("superseded") is not False:
        add("DISPOSITION_SUPERSESSION", "readiness record must not silently supersede governing disposition", "$.governing_disposition.superseded")

    try:
        observed_blob = run_git("rev-parse", f"HEAD:{DISPOSITION_PATH.as_posix()}").stdout.strip()
        if observed_blob != EXPECTED_DISPOSITION_BLOB:
            add("DISPOSITION_BLOB_MISMATCH", f"found {observed_blob}", "$git")
    except Exception as exc:
        add("DISPOSITION_BLOB_UNRESOLVED", str(exc), "$git")

    live = record["live_repository_settings_observation"]
    if (
        live.get("branch_protection_observed") is not False
        or live.get("branch_protection_enforcement_observed") != "OFF"
        or live.get("standing") != "PREVENTIVE_REPOSITORY_ENFORCEMENT_NOT_APPLIED"
    ):
        add(
            "LIVE_SETTINGS_PROMOTION",
            "readiness record cannot represent branch protection as already applied",
            "$.live_repository_settings_observation",
        )

    contexts = record["required_check_context_verification"]
    if contexts.get("declared_required_contexts") != EXPECTED_CONTEXTS:
        add("DECLARED_CONTEXTS_MISMATCH", "required context list changed", "$.required_check_context_verification.declared_required_contexts")
    if contexts.get("observed_successful_contexts") != EXPECTED_CONTEXTS:
        add("OBSERVED_CONTEXTS_MISMATCH", "observed successful required contexts do not exactly match declared contexts", "$.required_check_context_verification.observed_successful_contexts")
    if contexts.get("declared_required_context_match") != "6_OF_6_EXACT_NAME_MATCH":
        add("CONTEXT_MATCH_STANDING", "required check match standing changed", "$.required_check_context_verification.declared_required_context_match")

    profile = record["application_profile"]
    if profile.get("required_status_checks") != EXPECTED_CONTEXTS:
        add("PROFILE_CONTEXTS_MISMATCH", "application profile contexts changed", "$.application_profile.required_status_checks")
    for key in (
        "pull_request_required",
        "conversation_resolution_required",
        "require_branches_up_to_date_before_merge",
        "force_push_prohibited",
        "branch_deletion_prohibited",
    ):
        if profile.get(key) is not True:
            add("PROFILE_REQUIRED_CONTROL", f"{key} must remain true", f"$.application_profile.{key}")
    if profile.get("required_approving_reviews") != 0:
        add("PROFILE_APPROVAL_COUNT", "interim profile requires zero approving reviews", "$.application_profile.required_approving_reviews")
    if profile.get("code_owner_review_required") is not False:
        add("PROFILE_CODEOWNER", "interim profile defers CODEOWNER review", "$.application_profile.code_owner_review_required")

    capability = record["application_capability"]
    if capability.get("connected_github_repository_permission") != "ADMIN":
        add("ADMIN_PERMISSION", "connected repository permission must reflect observed ADMIN", "$.application_capability.connected_github_repository_permission")
    if capability.get("branch_protection_write_action_available_in_connected_tool_surface") is not False:
        add("TOOLING_CAPABILITY_PROMOTION", "connected tool surface does not expose branch-protection write", "$.application_capability.branch_protection_write_action_available_in_connected_tool_surface")
    if capability.get("application_state") != "BLOCKED_ON_SEPARATE_ADMIN_REPOSITORY_SETTINGS_ACT":
        add("APPLICATION_STATE", "application must remain blocked pending separate admin settings act", "$.application_capability.application_state")

    lineage = record["governed_lineage_audit"]
    target = lineage.get("target_commit")
    if lineage.get("anchor_commit") != ANCHOR:
        add("LINEAGE_ANCHOR", "unexpected lineage anchor", "$.governed_lineage_audit.anchor_commit")
    if not isinstance(target, str):
        add("LINEAGE_TARGET", "missing lineage target", "$.governed_lineage_audit.target_commit")
    else:
        inspected = inspect_lineage(target)
        findings.extend(inspected["findings"])
        if inspected.get("descendant_count") != lineage.get("first_parent_descendants_after_anchor"):
            add("LINEAGE_COUNT", f"observed {inspected.get('descendant_count')}", "$.governed_lineage_audit.first_parent_descendants_after_anchor")
        if inspected.get("findings") == []:
            if lineage.get("two_parent_merge_commits") != inspected.get("descendant_count"):
                add("MERGE_COUNT", "two-parent merge count does not match recomputation", "$.governed_lineage_audit.two_parent_merge_commits")
            if lineage.get("non_merge_first_parent_commits") != 0:
                add("NON_MERGE_COUNT", "non-merge count must be zero", "$.governed_lineage_audit.non_merge_first_parent_commits")
            if lineage.get("octopus_first_parent_commits") != 0:
                add("OCTOPUS_COUNT", "octopus count must be zero", "$.governed_lineage_audit.octopus_first_parent_commits")

    try:
        tree = run_git("show", "-s", "--format=%T", basis["governed_tip"]).stdout.strip()
        if tree != basis.get("governed_tip_tree"):
            add("BASIS_TREE_MISMATCH", f"found {tree}", "$.basis.governed_tip_tree")
    except Exception as exc:
        add("BASIS_TREE_UNRESOLVED", str(exc), "$git")

    return findings


def evaluate() -> dict[str, Any]:
    try:
        record = strict_load(READINESS_PATH)
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": "PRESERVATION_ENFORCEMENT_READINESS_INVALID",
            "findings": [{"code": "INPUT_INVALID", "detail": str(exc), "path": "$input"}],
        }

    findings = validate_record(record)
    return {
        "checker": Path(__file__).name,
        "status": (
            "PRESERVATION_ENFORCEMENT_READINESS_CONFORMS_NOT_APPLIED"
            if not findings
            else "PRESERVATION_ENFORCEMENT_READINESS_INVALID"
        ),
        "findings": findings,
        "non_claims": [
            "Readiness is not repository-settings application.",
            "Merge-only historical topology is detective evidence, not preventive enforcement.",
            "Required status checks are mechanical gates and do not establish substantive correctness or independent governance.",
        ],
    }


def evaluate_lineage(target: str) -> dict[str, Any]:
    result = inspect_lineage(target)
    return {
        "checker": Path(__file__).name,
        "status": (
            "PRESERVATION_GOVERNED_LINEAGE_MERGE_TOPOLOGY_CONFORMS"
            if not result["findings"]
            else "PRESERVATION_GOVERNED_LINEAGE_VIOLATION_OBSERVED"
        ),
        "anchor": ANCHOR,
        "target": target,
        "first_parent_descendants": result.get("descendant_count"),
        "findings": result["findings"],
        "non_claims": [
            "This detector does not prevent mutation of the governed branch.",
            "Two-parent merge topology does not independently prove GitHub pull-request provenance or authorization.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lineage-only", action="store_true")
    parser.add_argument("--target", default="HEAD")
    args = parser.parse_args()

    result = evaluate_lineage(args.target) if args.lineage_only else evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
