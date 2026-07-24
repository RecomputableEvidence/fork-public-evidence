#!/usr/bin/env python3
"""Validate the Kubernetes exterior-observation construction package."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

EXPERIMENT_ROOT = Path("experiments/exterior-longitudinal-observation/kubernetes-master-v0.1")
WORKFLOW_PATH = Path(".github/workflows/kubernetes-longitudinal-observation-v0-1.yml")
MANIFEST_PATH = EXPERIMENT_ROOT / "PACKAGE_MANIFEST_v0_1.json"


class DuplicateKeyError(ValueError):
    pass


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scoped_files(repo_root: Path) -> set[str]:
    paths = {
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / EXPERIMENT_ROOT).rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }
    workflow = repo_root / WORKFLOW_PATH
    if workflow.is_file():
        paths.add(WORKFLOW_PATH.as_posix())
    return paths


def validate_manifest(repo_root: Path) -> list[str]:
    findings: list[str] = []
    manifest_abs = repo_root / MANIFEST_PATH
    if not manifest_abs.is_file():
        return ["PACKAGE_MANIFEST_MISSING"]
    try:
        manifest = load_json(manifest_abs)
    except Exception as exc:
        return [f"PACKAGE_MANIFEST_PARSE_FAILED:{type(exc).__name__}"]

    exclusion = manifest.get("self_exclusion")
    if not isinstance(exclusion, dict) or exclusion.get("path") != MANIFEST_PATH.as_posix():
        findings.append("MANIFEST_SELF_EXCLUSION_UNDECLARED")

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return findings + ["MANIFEST_ENTRIES_INVALID"]
    if manifest.get("entry_count") != len(entries):
        findings.append("MANIFEST_ENTRY_COUNT_MISMATCH")

    declared: list[str] = []
    for index, entry in enumerate(entries):
        prefix = f"ENTRY_{index}"
        if not isinstance(entry, dict):
            findings.append(f"{prefix}_INVALID")
            continue
        path = entry.get("path")
        if not isinstance(path, str):
            findings.append(f"{prefix}_PATH_INVALID")
            continue
        declared.append(path)
        candidate = (repo_root / path).resolve()
        try:
            candidate.relative_to(repo_root.resolve())
        except ValueError:
            findings.append(f"{prefix}_PATH_ESCAPE")
            continue
        if not candidate.is_file():
            findings.append(f"{prefix}_MISSING")
            continue
        if entry.get("sha256") != sha256(candidate):
            findings.append(f"{prefix}_DIGEST_MISMATCH")
        if entry.get("size_bytes") != candidate.stat().st_size:
            findings.append(f"{prefix}_SIZE_MISMATCH")

    if declared != sorted(declared):
        findings.append("MANIFEST_PATHS_NOT_SORTED")
    if len(declared) != len(set(declared)):
        findings.append("MANIFEST_DUPLICATE_PATH")

    actual = scoped_files(repo_root)
    actual.discard(MANIFEST_PATH.as_posix())
    if set(declared) != actual:
        missing = sorted(actual - set(declared))
        extra = sorted(set(declared) - actual)
        for path in missing:
            findings.append(f"UNDECLARED_SCOPED_FILE:{path}")
        for path in extra:
            findings.append(f"DECLARED_FILE_OUTSIDE_SCOPE_OR_MISSING:{path}")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    findings = validate_manifest(args.repo_root.resolve())
    if findings:
        print("KUBERNETES_EXPERIMENT_PACKAGE_NONCONFORMING")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("KUBERNETES_EXPERIMENT_PACKAGE_CONFORMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
