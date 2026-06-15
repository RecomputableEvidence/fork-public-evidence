#!/usr/bin/env python3
"""
Remote verifier for AI Governance Mapping System v0.1.

This verifier does not trust the caller's local working tree.
It clones the public GitHub repository into a temporary directory,
checks out the declared commit, verifies expected files and doctrine
sentinels, computes SHA-256 hashes, and emits a JSON verification result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_REPO_URL = "https://github.com/RecomputableEvidence/fork-public-evidence.git"
DEFAULT_COMMIT = "9d96961"
DEFAULT_SUBJECT = "Add AI governance mapping system v0.1"

EXPECTED_CHANGED_PATHS = [
    "README.md",
    "docs/AI_GOVERNANCE_MAPPING_SYSTEM_v0_1.md",
    "docs/AI_GOVERNANCE_SYSTEM_MAPPING_RECORD_TEMPLATE_v0_1.md",
    "docs/CLAIM_BOUNDARY_PLACEMENT_LAYER_v0_1.md",
    "examples/ai_governance_system_mapping/FORK_SYSTEM_MAPPING_RECORD_v0_1.md",
    "examples/ai_governance_system_mapping/GENERIC_PRE_EXECUTION_GOVERNANCE_SYSTEM_MAPPING_RECORD_v0_1.md",
    "examples/ai_governance_system_mapping/GENERIC_RUNTIME_ANCHORING_SYSTEM_MAPPING_RECORD_v0_1.md",
    "examples/ai_governance_system_mapping/README.md",
]

REQUIRED_DEPENDENCY_PATHS = [
    "docs/AI_GOVERNANCE_BOUNDARY_MAPPING_PROTOCOL_v0_1.md",
    "docs/CLAIM_SAFE_INTEROPERABILITY_CONTRACT_v0_1.md",
]

SENTINELS: dict[str, list[str]] = {
    "docs/AI_GOVERNANCE_MAPPING_SYSTEM_v0_1.md": [
        "AI governance cannot be made safe merely by connecting systems.",
        "It requires claim-boundary placement before handoff.",
        "Otherwise, interoperability becomes silent claim inheritance.",
        "Fork is the recomputable evidence-boundary layer inside the mapped architecture.",
        "This v0.1 artifact is an architecture scaffold only.",
    ],
    "docs/CLAIM_BOUNDARY_PLACEMENT_LAYER_v0_1.md": [
        "The output of this layer is not integration.",
        "Handoffs move artifacts.",
        "Boundaries control claim inheritance.",
        "It is a doctrine artifact for claim-safe architecture.",
    ],
    "docs/AI_GOVERNANCE_SYSTEM_MAPPING_RECORD_TEMPLATE_v0_1.md": [
        "This mapping record is a placement artifact.",
        "It exists to make claim boundaries explicit before artifact handoff.",
        "PROHIBITED_CLAIM_INHERITANCE:",
    ],
    "examples/ai_governance_system_mapping/FORK_SYSTEM_MAPPING_RECORD_v0_1.md": [
        "Fork preserves declared evidence boundaries around AI-assisted workflows.",
        "Fork does not claim:",
        "AI output correctness",
        "Successful Fork verification means the preserved record verifies against its declared evidence boundary.",
    ],
    "examples/ai_governance_system_mapping/GENERIC_RUNTIME_ANCHORING_SYSTEM_MAPPING_RECORD_v0_1.md": [
        "Named third-party mapping: No",
        "It is not a canonical mapping of any named third-party system.",
        "The evidence layer must not infer output correctness",
    ],
    "examples/ai_governance_system_mapping/GENERIC_PRE_EXECUTION_GOVERNANCE_SYSTEM_MAPPING_RECORD_v0_1.md": [
        "Named third-party mapping: No",
        "It is not a canonical mapping of any named third-party system.",
        "The evidence layer must not inherit permissioning authority",
    ],
    "examples/ai_governance_system_mapping/README.md": [
        "Named third-party systems should not be mapped as canonical records unless the relevant system owner provides or approves the mapping.",
    ],
    "README.md": [
        "AI Governance Mapping System v0.1",
        "Fork now includes an architecture scaffold for placing AI-governance systems before integration or artifact handoff.",
    ],
}


def run_cmd(args: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command failed ({proc.returncode}): {' '.join(args)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def add_check(checks: list[dict[str, Any]], check_id: str, status: str, detail: Any = None) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": status,
            "detail": detail,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify remote AI Governance Mapping System v0.1 commit.")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL)
    parser.add_argument("--commit", default=DEFAULT_COMMIT)
    parser.add_argument("--expected-subject", default=DEFAULT_SUBJECT)
    parser.add_argument("--output", default="remote_mapping_system_v0_1_verification_result.json")
    parser.add_argument("--keep-clone", action="store_true")
    args = parser.parse_args()

    result: dict[str, Any] = {
        "verifier_name": "verify_remote_mapping_system_v0_1",
        "verifier_version": "v0.1",
        "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo_url": args.repo_url,
        "requested_commit": args.commit,
        "expected_subject": args.expected_subject,
        "overall_status": "UNKNOWN",
        "checks": [],
        "files": [],
        "clone_path": None,
    }

    checks: list[dict[str, Any]] = result["checks"]

    temp_dir = Path(tempfile.mkdtemp(prefix="fork_remote_verify_"))
    clone_dir = temp_dir / "repo"
    result["clone_path"] = str(clone_dir)

    try:
        git_version = run_cmd(["git", "--version"])
        add_check(checks, "GIT_AVAILABLE", "PASS", git_version)

        run_cmd(["git", "clone", "--quiet", args.repo_url, str(clone_dir)])
        add_check(checks, "REMOTE_CLONE", "PASS", {"repo_url": args.repo_url})

        run_cmd(["git", "checkout", "--quiet", args.commit], cwd=clone_dir)
        resolved_commit = run_cmd(["git", "rev-parse", "HEAD"], cwd=clone_dir)
        result["resolved_commit"] = resolved_commit
        add_check(checks, "COMMIT_CHECKOUT", "PASS", {"requested": args.commit, "resolved": resolved_commit})

        subject = run_cmd(["git", "log", "-1", "--format=%s"], cwd=clone_dir)
        result["actual_subject"] = subject
        if subject == args.expected_subject:
            add_check(checks, "COMMIT_SUBJECT", "PASS", subject)
        else:
            add_check(
                checks,
                "COMMIT_SUBJECT",
                "FAIL",
                {"expected": args.expected_subject, "actual": subject},
            )

        changed = run_cmd(["git", "show", "--name-only", "--format=", "HEAD"], cwd=clone_dir)
        changed_paths = sorted([line.strip() for line in changed.splitlines() if line.strip()])
        result["changed_paths"] = changed_paths

        expected_changed = sorted(EXPECTED_CHANGED_PATHS)
        if changed_paths == expected_changed:
            add_check(checks, "CHANGED_FILE_SET_EXACT", "PASS", changed_paths)
        else:
            add_check(
                checks,
                "CHANGED_FILE_SET_EXACT",
                "FAIL",
                {
                    "expected": expected_changed,
                    "actual": changed_paths,
                    "missing": sorted(set(expected_changed) - set(changed_paths)),
                    "unexpected": sorted(set(changed_paths) - set(expected_changed)),
                },
            )

        all_required = EXPECTED_CHANGED_PATHS + REQUIRED_DEPENDENCY_PATHS
        missing_required: list[str] = []
        for rel in all_required:
            p = clone_dir / rel
            if not p.is_file():
                missing_required.append(rel)
        if missing_required:
            add_check(checks, "REQUIRED_FILES_PRESENT", "FAIL", {"missing": missing_required})
        else:
            add_check(checks, "REQUIRED_FILES_PRESENT", "PASS", all_required)

        for rel in all_required:
            p = clone_dir / rel
            if p.is_file():
                result["files"].append(
                    {
                        "path": rel,
                        "size_bytes": p.stat().st_size,
                        "sha256": sha256_file(p),
                    }
                )

        sentinel_failures: list[dict[str, Any]] = []
        for rel, required_strings in SENTINELS.items():
            p = clone_dir / rel
            if not p.is_file():
                sentinel_failures.append({"path": rel, "missing_file": True})
                continue
            text = p.read_text(encoding="utf-8")
            missing = [s for s in required_strings if s not in text]
            if missing:
                sentinel_failures.append({"path": rel, "missing_sentinels": missing})

        if sentinel_failures:
            add_check(checks, "CONTENT_SENTINELS", "FAIL", sentinel_failures)
        else:
            add_check(checks, "CONTENT_SENTINELS", "PASS", list(SENTINELS.keys()))

        generic_files = [
            "examples/ai_governance_system_mapping/GENERIC_RUNTIME_ANCHORING_SYSTEM_MAPPING_RECORD_v0_1.md",
            "examples/ai_governance_system_mapping/GENERIC_PRE_EXECUTION_GOVERNANCE_SYSTEM_MAPPING_RECORD_v0_1.md",
        ]
        generic_boundary_failures: list[str] = []
        for rel in generic_files:
            text = (clone_dir / rel).read_text(encoding="utf-8")
            if "Named third-party mapping: No" not in text:
                generic_boundary_failures.append(rel)
        if generic_boundary_failures:
            add_check(
                checks,
                "GENERIC_EXAMPLES_NOT_THIRD_PARTY_MAPPINGS",
                "FAIL",
                generic_boundary_failures,
            )
        else:
            add_check(
                checks,
                "GENERIC_EXAMPLES_NOT_THIRD_PARTY_MAPPINGS",
                "PASS",
                generic_files,
            )

        failed = [c for c in checks if c["status"] != "PASS"]
        result["overall_status"] = "PASS" if not failed else "FAIL"

    except Exception as exc:
        add_check(checks, "VERIFIER_EXCEPTION", "FAIL", str(exc))
        result["overall_status"] = "FAIL"

    finally:
        output_path = Path(args.output).resolve()
        output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        if not args.keep_clone:
            shutil.rmtree(temp_dir, ignore_errors=True)
            result["clone_path"] = None
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if result["overall_status"] == "PASS":
        print("REMOTE_MAPPING_SYSTEM_V0_1_VERIFICATION_PASS")
        print(f"result_path={Path(args.output).resolve()}")
        return 0

    print("REMOTE_MAPPING_SYSTEM_V0_1_VERIFICATION_FAIL")
    print(f"result_path={Path(args.output).resolve()}")
    return 1


if __name__ == "__main__":
    sys.exit(main())