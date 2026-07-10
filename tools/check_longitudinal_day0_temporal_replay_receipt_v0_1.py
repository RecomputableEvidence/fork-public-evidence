#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Temporal Replay Receipt Checker v0.1.

This checker validates the temporal replay receipt surface. It does not replay
the original worktree itself. It verifies that the receipt records a bounded
Day-0 replay against a detached subject commit, with expected pass signals and
explicit non-authority language.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, validation, schema
conformance, production readiness, procurement approval, external anchoring,
or institutional authority.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from typing import Any, Dict, List


RECEIPT_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.json")
README_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/README.md")
INTERPRETATION_PATH = pathlib.Path("docs/reconstruction/longitudinal/day0/replay/DAY0_TEMPORAL_REPLAY_RECEIPT_INTERPRETATION_v0_1.md")
SCHEMA_PATH = pathlib.Path("schemas/longitudinal_day0_temporal_replay_receipt_v0_1.schema.json")
RESPONSE_RECEIPT_PATH = pathlib.Path("docs/review/public-rounds/round-005/ROUND005_RESPONSE_DAY0_TEMPORAL_REPLAY_RECEIPT_v0_1.md")

NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "validation",
    "schema conformance",
    "production readiness",
    "authority",
]

DOES_NOT_PROVE_TERMS = [
    "truth",
    "compliance",
    "legal sufficiency",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "validation",
    "schema conformance",
    "production readiness",
    "procurement approval",
    "institutional authority",
    "external original-sealing anchor",
]


def result(name: str, passed: bool, detail: str, data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "detail": detail,
        "data": data,
    }


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def missing_terms(text: str, terms: List[str]) -> List[str]:
    lower = text.lower()
    return [term for term in terms if term not in lower]


def git_commit_exists(commit: str) -> bool:
    try:
        subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return True
    except Exception:
        return False


def git_commit_is_ancestor(commit: str) -> bool:
    try:
        completed = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return completed.returncode == 0
    except Exception:
        return False


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    checks: List[Dict[str, Any]] = []

    for name, path in [
        ("path:receipt", RECEIPT_PATH),
        ("path:readme", README_PATH),
        ("path:interpretation", INTERPRETATION_PATH),
        ("path:schema", SCHEMA_PATH),
        ("path:round005-response", RESPONSE_RECEIPT_PATH),
    ]:
        checks.append(result(name, path.is_file(), "present" if path.is_file() else "missing", str(path).replace("\\", "/")))

    receipt = None
    try:
        receipt = load_json(RECEIPT_PATH)
        checks.append(result("receipt:parse", isinstance(receipt, dict), "receipt parses as JSON object"))
    except Exception as exc:
        checks.append(result("receipt:parse", False, str(exc)))

    try:
        schema = load_json(SCHEMA_PATH)
        checks.append(result("schema:parse", isinstance(schema, dict), "schema parses as JSON object"))
    except Exception as exc:
        checks.append(result("schema:parse", False, str(exc)))

    if isinstance(receipt, dict):
        checks.append(result(
            "receipt:classification",
            receipt.get("receipt_classification") == "temporal_replay_receipt",
            "receipt_classification is temporal_replay_receipt",
            receipt.get("receipt_classification"),
        ))

        subject = receipt.get("replay_subject", {})
        commit = str(subject.get("subject_commit", ""))
        checks.append(result(
            "receipt:subject-commit-format",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)),
            "subject_commit is 40 hex characters",
            commit,
        ))

        checks.append(result(
            "receipt:subject-commit-exists",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)) and git_commit_exists(commit),
            "subject_commit exists in local git object database",
            commit,
        ))

        checks.append(result(
            "receipt:subject-commit-is-ancestor",
            bool(re.fullmatch(r"[0-9a-fA-F]{40}", commit)) and git_commit_is_ancestor(commit),
            "subject_commit is ancestor of current HEAD",
            commit,
        ))

        scope = receipt.get("replay_scope", {})
        checks.append(result(
            "receipt:detached-worktree-mode",
            subject.get("replay_worktree_mode") == "detached_git_worktree_at_subject_commit",
            "receipt records detached replay worktree mode",
            subject.get("replay_worktree_mode"),
        ))

        checks.append(result(
            "receipt:replay-scope-non-mutating",
            scope.get("replay_does_not_mutate_packet") is True,
            "receipt says replay does not mutate packet",
            scope.get("replay_does_not_mutate_packet"),
        ))

        observed = receipt.get("observed_execution", {})
        checks.append(result(
            "receipt:day0-checker-passed",
            observed.get("day0_checker_failed") == 0 and observed.get("day0_checker_passed") == observed.get("day0_checker_total"),
            "Day-0 checker replay passed",
            observed,
        ))

        checks.append(result(
            "receipt:expected-day0-total",
            observed.get("day0_checker_total") == 27 and observed.get("day0_checker_passed") == 27 and observed.get("day0_checker_failed") == 0,
            "Day-0 checker expected 27/27 replay signal present",
            observed,
        ))

        checks.append(result(
            "receipt:git-diff-check",
            observed.get("git_diff_check_exit_code") == 0,
            "detached replay worktree git diff --check exited 0",
            observed.get("git_diff_check_exit_code"),
        ))

        hashes = receipt.get("observed_hashes", {})
        manifest_hash = str(hashes.get("packet_manifest_sha256", ""))
        outer_hash = str(hashes.get("outer_receipt_packet_manifest_sha256", ""))
        sidecar_text = str(hashes.get("packet_manifest_sidecar_text", ""))

        checks.append(result(
            "receipt:manifest-hash-format",
            bool(re.fullmatch(r"[0-9a-f]{64}", manifest_hash)),
            "packet manifest SHA-256 is 64 lowercase hex characters",
            manifest_hash,
        ))

        checks.append(result(
            "receipt:sidecar-binds-manifest-hash",
            manifest_hash in sidecar_text,
            "sidecar text contains packet manifest hash",
            sidecar_text,
        ))

        checks.append(result(
            "receipt:outer-binds-manifest-hash",
            manifest_hash == outer_hash,
            "outer receipt manifest hash equals observed manifest hash",
            {"manifest_hash": manifest_hash, "outer_hash": outer_hash},
        ))

        interpretation = receipt.get("interpretation", {})
        does_not_prove_text = " ".join(str(x) for x in interpretation.get("does_not_prove", []))
        missing_does_not_prove = missing_terms(does_not_prove_text, DOES_NOT_PROVE_TERMS)
        checks.append(result(
            "receipt:does-not-prove-boundary",
            len(missing_does_not_prove) == 0,
            "does_not_prove list contains required boundary terms" if not missing_does_not_prove else "missing boundary terms",
            missing_does_not_prove,
        ))

        non_authority = str(receipt.get("non_authority_statement", ""))
        missing_non_authority = missing_terms(non_authority, NON_AUTHORITY_TERMS)
        checks.append(result(
            "receipt:non-authority-statement",
            len(missing_non_authority) == 0,
            "non-authority statement contains required terms" if not missing_non_authority else "missing non-authority terms",
            missing_non_authority,
        ))
    else:
        checks.append(result("receipt:content", False, "receipt unavailable"))

    for name, path in [
        ("readme:non-authority", README_PATH),
        ("interpretation:non-authority", INTERPRETATION_PATH),
        ("round005-response:non-authority", RESPONSE_RECEIPT_PATH),
    ]:
        try:
            text = read_text(path)
            missing = missing_terms(text, NON_AUTHORITY_TERMS)
            checks.append(result(
                name,
                len(missing) == 0,
                "non-authority terms present" if not missing else "missing non-authority terms",
                missing,
            ))
        except Exception as exc:
            checks.append(result(name, False, str(exc)))

    failed = sum(1 for item in checks if not item["passed"])

    summary = {
        "checker": "check_longitudinal_day0_temporal_replay_receipt_v0_1.py",
        "total": len(checks),
        "passed": len(checks) - failed,
        "failed": failed,
        "results": checks,
        "interpretation": (
            "A pass confirms a bounded Day-0 temporal replay receipt is present and internally consistent. "
            "It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, "
            "certification, endorsement, validation, schema conformance, production readiness, procurement "
            "approval, external anchoring, or institutional authority."
        ),
        "non_authority_statement": (
            "This checker validates temporal replay receipt structure only; it does not validate truth, compliance, "
            "legal sufficiency, safety, authorization, approval, certification, endorsement, validation, schema "
            "conformance, production readiness, procurement approval, external anchoring, or institutional authority."
        ),
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 temporal replay receipt checks: {summary['passed']}/{summary['total']} passed")
        for item in checks:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} {item['name']}: {item['detail']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))