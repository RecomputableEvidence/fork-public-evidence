#!/usr/bin/env python3
"""Validate the append-only PR #101 Proof 001 admission-anchor candidate."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("docs/proof-atlas/admission/PR101-PROOF001-ADMISSION-ANCHOR-001")
ANCHOR = PACKAGE / "ADMISSION-ANCHOR.json"
MANIFEST = PACKAGE / "FILE-MANIFEST.json"
README = PACKAGE / "README.md"

BASE_BEFORE = "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0"
REVIEWED_HEAD = "a273ab0a95decb0d43f1c091743a72ac4261027e"
MERGE_COMMIT = "ded38bf56f950b8813614132c92bf531553a8b34"
EXPECTED_PARENTS = [BASE_BEFORE, REVIEWED_HEAD]
EXPECTED_REVIEW_ID = 4804264700
EXPECTED_RUNS = {
    ("Root Checksum Manifest v0.1", 30364643071, 100),
    ("Fork Proof-Surface Integration", 30364639521, 169),
    ("Fork Evidence CI", 30364639476, 470),
}
EXPECTED_BINDINGS = {
    ANCHOR.as_posix(),
    README.as_posix(),
    "tools/check_pr101_proof001_admission_anchor_v0_1.py",
    "tests/test_pr101_proof001_admission_anchor_v0_1.py",
}


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
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def safe_regular_file(relative: Any) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError("path must be a non-empty repository-relative string")
    pure = PurePosixPath(relative)
    if (
        pure.is_absolute()
        or "." in pure.parts
        or ".." in pure.parts
        or "\\" in relative
        or relative != pure.as_posix()
    ):
        raise ValueError(f"unsafe or non-canonical path: {relative!r}")
    root_real = ROOT.resolve(strict=True)
    current = ROOT
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {relative}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"not a regular file: {relative}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def evaluate() -> dict[str, Any]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    try:
        anchor = strict_load(safe_regular_file(ANCHOR.as_posix()))
    except Exception as exc:
        return {
            "status": "PR101_PROOF001_ADMISSION_ANCHOR_CANDIDATE_INVALID",
            "findings": [
                {"code": "ANCHOR_INVALID", "detail": str(exc), "path": ANCHOR.as_posix()}
            ],
        }

    transition = anchor.get("bound_transition", {})
    expected_transition = {
        "pull_request": 101,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_before_merge": BASE_BEFORE,
        "reviewed_head": REVIEWED_HEAD,
        "merge_commit": MERGE_COMMIT,
        "expected_ordered_parents": EXPECTED_PARENTS,
        "merge_method": "merge_commit",
        "reviewed_head_to_merge_commit_file_delta": 0,
        "merge_tree_sha": "NOT_EXPOSED_BY_AVAILABLE_CONNECTOR",
    }
    if transition != expected_transition:
        add(
            "TRANSITION_BINDING_MISMATCH",
            "bound transition differs from the exact expected record",
            ANCHOR.as_posix(),
        )

    review = anchor.get("bounded_review", {})
    if (
        review.get("review_id") != EXPECTED_REVIEW_ID
        or review.get("reviewed_head") != REVIEWED_HEAD
        or review.get("disposition")
        != "REVIEWED_PROOF_PACKAGING_EXACT_HEAD_NO_BLOCKING_FINDINGS"
        or review.get("reviewer_standing")
        != "NOT_INDEPENDENT_CONSTRUCTION_ASSISTED"
        or review.get("independent_local_execution") != "NOT_PERFORMED"
    ):
        add(
            "REVIEW_BINDING_MISMATCH",
            "bounded review standing or coordinates changed",
            ANCHOR.as_posix(),
        )

    runs = anchor.get("exact_head_ci", [])
    observed_runs = {
        (item.get("workflow"), item.get("run_id"), item.get("run_number"))
        for item in runs
        if isinstance(item, dict)
        and item.get("status") == "completed"
        and item.get("conclusion") == "success"
    }
    if observed_runs != EXPECTED_RUNS or len(runs) != 3:
        add(
            "CI_BINDING_MISMATCH",
            f"expected {sorted(EXPECTED_RUNS)!r}, found {sorted(observed_runs)!r}",
            ANCHOR.as_posix(),
        )

    standing = anchor.get("admitted_standing", {})
    expected_standing = {
        "proof_packaging": "PROOF_001_PACKAGING_ADMITTED",
        "underlying_replay": "ADMITTED_LINEAR_REPLAY_WITH_CORRECTION_REQUIRED_RETAINED",
        "underlying_exterior_disposition": "REPRODUCED_WITH_CORRECTION_REQUIRED",
        "review_inheritance_to_merge_commit": "NONE",
        "retroactive_effect_inside_replay_interval": "NONE",
        "public_route_state": "STALE_RECORDED_PENDING_SEPARATE_SUCCESSOR",
    }
    if standing != expected_standing:
        add(
            "STANDING_MISMATCH",
            "admitted standing differs from the bounded expected standing",
            ANCHOR.as_posix(),
        )

    if (
        anchor.get("candidate_anchor_standing")
        != "APPEND_ONLY_ADMISSION_ANCHOR_CANDIDATE_NOT_ADMITTED"
    ):
        add("ANCHOR_SELF_ADMISSION", "anchor candidate standing widened", ANCHOR.as_posix())

    try:
        parents = run_git("show", "-s", "--format=%P", MERGE_COMMIT).stdout.strip().split()
        if parents != EXPECTED_PARENTS:
            add(
                "MERGE_PARENT_MISMATCH",
                f"expected {EXPECTED_PARENTS!r}, found {parents!r}",
                "$git",
            )
        delta = run_git("diff", "--name-only", REVIEWED_HEAD, MERGE_COMMIT).stdout.splitlines()
        if delta:
            add(
                "MERGE_TREE_CONTENT_MISMATCH",
                f"unexpected changed paths: {delta!r}",
                "$git",
            )
        current = run_git("rev-parse", "HEAD").stdout.strip()
        ancestor = run_git(
            "merge-base", "--is-ancestor", MERGE_COMMIT, current, check=False
        )
        if ancestor.returncode != 0:
            add(
                "ANCHOR_NOT_DESCENDED_FROM_MERGE",
                f"HEAD {current} is not descended from {MERGE_COMMIT}",
                "$git",
            )
    except Exception as exc:
        add("GIT_BINDING_UNRESOLVED", str(exc), "$git")

    try:
        manifest = strict_load(safe_regular_file(MANIFEST.as_posix()))
        if manifest.get("self_exclusion") != {
            "path": MANIFEST.as_posix(),
            "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
        }:
            add(
                "MANIFEST_SELF_EXCLUSION_INVALID",
                "manifest self-exclusion changed",
                MANIFEST.as_posix(),
            )
        bindings = manifest.get("bindings", [])
        listed: set[str] = set()
        for binding in bindings:
            path = binding.get("path")
            if not isinstance(path, str) or path in listed:
                add(
                    "MANIFEST_BINDING_INVALID",
                    f"invalid or duplicate path: {path!r}",
                    MANIFEST.as_posix(),
                )
                continue
            listed.add(path)
            try:
                target = safe_regular_file(path)
                if target.stat().st_size != binding.get("size_bytes"):
                    add("MANIFEST_SIZE_MISMATCH", path, path)
                if sha256_file(target) != binding.get("sha256"):
                    add("MANIFEST_DIGEST_MISMATCH", path, path)
            except Exception as exc:
                add("MANIFEST_BINDING_INVALID", str(exc), str(path))
        if listed != EXPECTED_BINDINGS:
            add(
                "MANIFEST_BINDING_SET_MISMATCH",
                f"expected {sorted(EXPECTED_BINDINGS)!r}, found {sorted(listed)!r}",
                MANIFEST.as_posix(),
            )
    except Exception as exc:
        add("MANIFEST_INVALID", str(exc), MANIFEST.as_posix())

    non_effects = anchor.get("non_effects", {})
    if (
        non_effects.get("main") != "NONE"
        or non_effects.get("authority_state") != "NONE"
        or non_effects.get("execution_state") != "NONE"
        or non_effects.get("provider_calls") != 0
        or non_effects.get("pair_001_calls") != 0
    ):
        add("NON_EFFECT_WIDENED", "one or more required non-effects changed", ANCHOR.as_posix())

    status = (
        "PR101_PROOF001_ADMISSION_ANCHOR_CANDIDATE_CONFORMS_NOT_ADMITTED"
        if not findings
        else "PR101_PROOF001_ADMISSION_ANCHOR_CANDIDATE_INVALID"
    )
    return {
        "checker": Path(__file__).name,
        "status": status,
        "bound_merge": MERGE_COMMIT,
        "bound_reviewed_head": REVIEWED_HEAD,
        "findings": findings,
        "non_claims": [
            "Anchor conformance is not self-admission.",
            "Proof packaging admission does not widen the underlying correction-required exterior disposition.",
            "Review standing does not inherit to the merge commit.",
            "Public routing remains a separately governed successor transition.",
        ],
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
