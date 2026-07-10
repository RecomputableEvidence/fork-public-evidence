#!/usr/bin/env python3
"""
Fork Public Review Round 005 Interaction Checker v0.1.

Validates structured Round 005 exterior review filings.

This checker validates filing structure only. It does not validate truth,
compliance, legal sufficiency, safety, authorization, approval, certification,
endorsement, production readiness, validation, or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


DEFAULT_ROOT = "docs/review/public-rounds/round-005/observations"

REQUIRED_TOP_LEVEL = [
    "review_round",
    "observation_id",
    "reviewer_id",
    "reviewer_type",
    "reviewed_object",
    "reviewed_commit",
    "environment",
    "review_classification",
    "evidence_weight",
    "verifier_execution",
    "checker_results",
    "findings",
    "adversarial_cases",
    "recommended_next_actions",
    "non_authority_statement",
]

REQUIRED_NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "production readiness",
    "authority",
]


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def check_observation(path: pathlib.Path) -> Dict[str, Any]:
    errors: List[str] = []

    try:
        data = load_json(path)
    except Exception as exc:
        return {
            "path": str(path).replace("\\", "/"),
            "passed": False,
            "errors": [str(exc)],
        }

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing required field: {key}")

    commit = data.get("reviewed_commit")
    if not isinstance(commit, dict):
        errors.append("reviewed_commit must be object")
    else:
        full = commit.get("full")
        if not isinstance(full, str) or not re.match(r"^[a-f0-9]{40}$", full):
            errors.append("reviewed_commit.full must be 40 lowercase hex characters")

    classifications = data.get("review_classification")
    if not isinstance(classifications, list) or not classifications:
        errors.append("review_classification must be non-empty array")

    findings = data.get("findings")
    if not isinstance(findings, list) or not findings:
        errors.append("findings must be non-empty array")

    adversarial_cases = data.get("adversarial_cases")
    if not isinstance(adversarial_cases, list) or not adversarial_cases:
        errors.append("adversarial_cases must be non-empty array")

    next_actions = data.get("recommended_next_actions")
    if not isinstance(next_actions, list) or not next_actions:
        errors.append("recommended_next_actions must be non-empty array")

    verifier = data.get("verifier_execution")
    if not isinstance(verifier, dict):
        errors.append("verifier_execution must be object")
    else:
        if verifier.get("public_verifier_executed") is False and verifier.get("manual_reconstruction_performed") is not True:
            errors.append("manual reconstruction must be recorded when public verifier did not execute")

    checker_results = data.get("checker_results")
    if not isinstance(checker_results, dict):
        errors.append("checker_results must be object")
    else:
        day0 = checker_results.get("longitudinal_day0")
        if not isinstance(day0, dict):
            errors.append("checker_results.longitudinal_day0 must be object")
        else:
            if day0.get("passed") != 27 or day0.get("failed") != 0:
                errors.append("longitudinal_day0 expected 27 passed and 0 failed for this filing")

    non_auth = str(data.get("non_authority_statement", "")).lower()
    for term in REQUIRED_NON_AUTHORITY_TERMS:
        if term not in non_auth:
            errors.append(f"non_authority_statement missing boundary term: {term}")

    return {
        "path": str(path).replace("\\", "/"),
        "observation_id": data.get("observation_id"),
        "reviewer_id": data.get("reviewer_id"),
        "evidence_weight": data.get("evidence_weight"),
        "passed": not errors,
        "errors": errors,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations-root", default=DEFAULT_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.observations_root)
    results: List[Dict[str, Any]] = []

    if not root.exists():
        results.append({
            "path": str(root).replace("\\", "/"),
            "passed": False,
            "errors": ["observations root missing"],
        })
    else:
        paths = sorted(root.glob("*.json"))
        if not paths:
            results.append({
                "path": str(root).replace("\\", "/"),
                "passed": False,
                "errors": ["no observation json files found"],
            })
        else:
            results = [check_observation(path) for path in paths]

    failed = sum(1 for item in results if not item["passed"])
    summary = {
        "checker": "check_public_review_round_005_interactions_v0_1.py",
        "round": "public_review_round_005_longitudinal_day0_packet_accessibility_reconstruction_boundary_replay_readiness",
        "observations_root": str(root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker validates Round 005 filing structure only; it does not validate truth, "
            "compliance, legal sufficiency, safety, authorization, approval, certification, "
            "endorsement, production readiness, validation, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Round 005 filings: {summary['passed']}/{summary['total']} passed")
        for item in results:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item.get('observation_id')} {item['path']}")
            for error in item["errors"]:
                print(f"  - {error}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))