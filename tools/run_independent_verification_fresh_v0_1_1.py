#!/usr/bin/env python3
"""Recompute an IVS v0.1.1 package from an empty disposable Git repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def safe_git_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def run(
    args: list[str],
    *,
    cwd: Path,
    check: bool = True,
    text: bool = False,
) -> subprocess.CompletedProcess[Any]:
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        env=safe_git_env(),
        capture_output=True,
        text=text,
        check=False,
    )
    if check and completed.returncode != 0:
        stderr = completed.stderr if text else completed.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(stderr.strip() or f"Command failed: {' '.join(args)}")
    return completed


def git(repo: Path, *args: str, text: bool = False) -> subprocess.CompletedProcess[Any]:
    return run(
        [
            "git",
            "-c",
            f"core.hooksPath={os.devnull}",
            "-c",
            "protocol.file.allow=never",
            *args,
        ],
        cwd=repo,
        text=text,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="GitHub owner/name repository slug")
    parser.add_argument("--package-commit", required=True, help="Full commit SHA containing the review package")
    parser.add_argument("--plan", required=True, help="Repository-relative v0.1.1 plan path")
    parser.add_argument("--expected-receipt", required=True, help="Repository-relative committed receipt path")
    args = parser.parse_args()

    if "/" not in args.repository or len(args.package_commit) != 40:
        parser.error("repository and full package commit SHA are required")
    remote = f"https://github.com/{args.repository}.git"

    with tempfile.TemporaryDirectory(prefix="fork-ivs-fresh-") as temp:
        root = Path(temp)
        object_repo = root / "objects"
        worktree = root / "package"
        object_repo.mkdir()
        git(object_repo, "init", "--bare", "-q")
        git(object_repo, "remote", "add", "origin", remote)
        git(
            object_repo,
            "fetch",
            "--no-tags",
            "--no-recurse-submodules",
            "origin",
            args.package_commit,
        )
        plan_raw = git(
            object_repo,
            "show",
            f"{args.package_commit}:{args.plan}",
        ).stdout
        plan = json.loads(plan_raw.decode("utf-8"))
        commits = {
            plan["subject"]["base_commit"],
            plan["subject"]["candidate_commit"],
            plan["verifier_release"]["source_commit"],
        }
        git(
            object_repo,
            "fetch",
            "--no-tags",
            "--no-recurse-submodules",
            "origin",
            *sorted(commits),
        )
        git(object_repo, "worktree", "add", "--detach", str(worktree), args.package_commit)
        checker = worktree / "tools/check_independent_verification_surface_v0_1_1.py"
        completed = run(
            [
                sys.executable,
                str(checker),
                "--repo-root",
                str(worktree),
                "--plan",
                args.plan,
            ],
            cwd=worktree,
            check=False,
        )
        expected = (worktree / args.expected_receipt).read_bytes()
        byte_exact = completed.stdout == expected
        summary = {
            "checker": "FORK_INDEPENDENT_VERIFICATION_FRESH_REPOSITORY_RUNNER_v0_1_1",
            "package_commit": args.package_commit,
            "candidate_checkout": "NONE",
            "candidate_code_execution": "NONE",
            "disposable_repository": True,
            "checker_exit_code": completed.returncode,
            "receipt_byte_exact": byte_exact,
            "result": "FRESH_RECOMPUTATION_PASS" if completed.returncode == 0 and byte_exact else "FRESH_RECOMPUTATION_FAIL",
        }
        sys.stdout.write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        if completed.returncode != 0:
            sys.stderr.buffer.write(completed.stderr)
        shutil.rmtree(worktree, ignore_errors=True)
        return 0 if summary["result"] == "FRESH_RECOMPUTATION_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
