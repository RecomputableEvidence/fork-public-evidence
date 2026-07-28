#!/usr/bin/env python3
"""Compare declared public routes with an exact admitted checkpoint."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Any


PACKAGE_ROOT = Path(
    "docs/proof-atlas/"
    "PROOF-001-review-does-not-silently-travel-v0.1"
)
CONTRACT_PATH = PACKAGE_ROOT / "PUBLIC-ROUTE-FRESHNESS-CONTRACT.json"
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


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
        for item in value.values():
            assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            assert_finite(item)


def strict_load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def safe_regular_file(root: Path, relative: Any) -> Path:
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
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {relative}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"not a regular file: {relative}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def run_git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and completed.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed


def resolve_json_keys(value: Any, keys: list[Any]) -> Any:
    current = value
    for key in keys:
        if not isinstance(key, str) or not isinstance(current, dict):
            raise ValueError(f"invalid JSON key route at {key!r}")
        if key not in current:
            raise ValueError(f"missing JSON key {key!r}")
        current = current[key]
    return current


def extract_route_coordinate(root: Path, route: dict[str, Any]) -> str:
    path = safe_regular_file(root, route.get("path"))
    selector = route.get("selector")
    if not isinstance(selector, dict):
        raise ValueError("route selector must be an object")
    kind = selector.get("kind")
    if kind == "json_keys":
        value = strict_load(path)
        coordinate = resolve_json_keys(value, selector.get("keys", []))
    elif kind == "markdown_branch_coordinate":
        branch = selector.get("branch")
        if not isinstance(branch, str) or not branch:
            raise ValueError("markdown branch selector requires a branch")
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(re.escape(branch) + r"@([0-9a-f]{40})")
        matches = pattern.findall(text)
        if len(matches) != 1:
            raise ValueError(
                f"expected one {branch!r} coordinate, found {len(matches)}"
            )
        coordinate = matches[0]
    else:
        raise ValueError(f"unsupported route selector kind: {kind!r}")
    if not isinstance(coordinate, str) or SHA1_RE.fullmatch(coordinate) is None:
        raise ValueError(f"route coordinate is not a full lowercase SHA: {coordinate!r}")
    return coordinate


def evaluate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    try:
        contract = strict_load(safe_regular_file(root, CONTRACT_PATH.as_posix()))
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": "PUBLIC_ROUTE_UNRESOLVED",
            "expected_status": None,
            "expectation_matches": False,
            "latest_admitted_checkpoint": None,
            "candidate_head": None,
            "routes": [],
            "findings": [
                {
                    "code": "ROUTE_CONTRACT_INVALID",
                    "detail": str(exc),
                    "path": CONTRACT_PATH.as_posix(),
                }
            ],
        }

    checkpoint = contract.get("latest_admitted_checkpoint", {})
    checkpoint_sha = checkpoint.get("commit_sha")
    checkpoint_tree = checkpoint.get("tree_sha")
    candidate_head: str | None = None
    if (
        not isinstance(checkpoint_sha, str)
        or SHA1_RE.fullmatch(checkpoint_sha) is None
        or not isinstance(checkpoint_tree, str)
        or SHA1_RE.fullmatch(checkpoint_tree) is None
    ):
        findings.append(
            {
                "code": "CHECKPOINT_COORDINATE_INVALID",
                "detail": "checkpoint commit and tree must be full lowercase SHA-1 values",
                "path": CONTRACT_PATH.as_posix(),
            }
        )
    else:
        try:
            observed = run_git(
                root,
                "show",
                "-s",
                "--format=%H%x00%T",
                checkpoint_sha,
            ).stdout.strip().split("\x00")
            if observed != [checkpoint_sha, checkpoint_tree]:
                findings.append(
                    {
                        "code": "CHECKPOINT_GIT_BINDING_MISMATCH",
                        "detail": (
                            f"expected {[checkpoint_sha, checkpoint_tree]!r}, "
                            f"found {observed!r}"
                        ),
                        "path": CONTRACT_PATH.as_posix(),
                    }
                )
            candidate_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
            descendant = run_git(
                root,
                "merge-base",
                "--is-ancestor",
                checkpoint_sha,
                candidate_head,
                check=False,
            )
            if descendant.returncode != 0:
                findings.append(
                    {
                        "code": "CANDIDATE_NOT_DESCENDED_FROM_CHECKPOINT",
                        "detail": (
                            f"candidate HEAD {candidate_head} is not descended from "
                            f"{checkpoint_sha}"
                        ),
                        "path": "$git",
                    }
                )
        except Exception as exc:
            findings.append(
                {
                    "code": "CHECKPOINT_GIT_BINDING_MISMATCH",
                    "detail": str(exc),
                    "path": "$git",
                }
            )

    route_results: list[dict[str, Any]] = []
    for route in contract.get("routes", []):
        if not isinstance(route, dict):
            findings.append(
                {
                    "code": "ROUTE_DEFINITION_INVALID",
                    "detail": "route entry must be an object",
                    "path": CONTRACT_PATH.as_posix(),
                }
            )
            continue
        route_id = str(route.get("route_id"))
        try:
            coordinate = extract_route_coordinate(root, route)
            ancestry = "UNRESOLVED"
            if isinstance(checkpoint_sha, str) and SHA1_RE.fullmatch(checkpoint_sha):
                relationship = run_git(
                    root,
                    "merge-base",
                    "--is-ancestor",
                    coordinate,
                    checkpoint_sha,
                    check=False,
                )
                ancestry = (
                    "ANCESTOR_OF_LATEST_ADMITTED_CHECKPOINT"
                    if relationship.returncode == 0
                    else "NOT_ANCESTOR_OF_LATEST_ADMITTED_CHECKPOINT"
                )
                if relationship.returncode != 0:
                    findings.append(
                        {
                            "code": "ROUTE_COORDINATE_NOT_IN_ADMITTED_LINEAGE",
                            "detail": (
                                f"{route_id} coordinate {coordinate} is not an "
                                f"ancestor of {checkpoint_sha}"
                            ),
                            "path": str(route.get("path")),
                        }
                    )
            route_results.append(
                {
                    "route_id": route_id,
                    "path": route.get("path"),
                    "declared_coordinate": coordinate,
                    "checkpoint_match": coordinate == checkpoint_sha,
                    "lineage_relationship": ancestry,
                }
            )
        except Exception as exc:
            findings.append(
                {
                    "code": "ROUTE_COORDINATE_UNRESOLVED",
                    "detail": str(exc),
                    "path": str(route.get("path")),
                }
            )

    if findings or len(route_results) != len(contract.get("routes", [])):
        status = "PUBLIC_ROUTE_UNRESOLVED"
    elif all(item["checkpoint_match"] for item in route_results):
        status = "PUBLIC_ROUTE_CURRENT"
    else:
        status = "PUBLIC_ROUTE_STALE"

    expected_status = contract.get("expected_status")
    return {
        "checker": Path(__file__).name,
        "status": status,
        "expected_status": expected_status,
        "expectation_matches": status == expected_status,
        "latest_admitted_checkpoint": checkpoint,
        "candidate_head": candidate_head,
        "routes": route_results,
        "findings": findings,
        "interpretation": {
            "proves": [
                "declared public route coordinates were compared with the exact configured admitted checkpoint",
                "configured Git commit and tree bindings were recomputed locally",
            ],
            "does_not_prove": [
                "that the configured checkpoint is globally latest outside the bound admission record",
                "that an older exact-coordinate projection is invalid",
                "truth",
                "correctness",
                "authority",
                "approval",
                "admission of this packaging candidate",
            ],
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--require-current",
        action="store_true",
        help="Return nonzero unless every declared route matches the checkpoint.",
    )
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    result = evaluate(root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for route in result["routes"]:
            print(
                f"{route['route_id']}: {route['declared_coordinate']} "
                f"(checkpoint_match={str(route['checkpoint_match']).lower()})"
            )
    if result["findings"] or not result["expectation_matches"]:
        return 1
    if args.require_current and result["status"] != "PUBLIC_ROUTE_CURRENT":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
