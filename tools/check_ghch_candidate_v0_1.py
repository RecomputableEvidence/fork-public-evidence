#!/usr/bin/env python3
"""Verify the GHCH v0.1 repository candidate manifest and root receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOC_ROOT = REPO / "docs/experiments/governed-handoff-cadence-v0.1"
MANIFEST = DOC_ROOT / "CANDIDATE-MANIFEST.json"
RECEIPT = DOC_ROOT / "CANDIDATE-ROOT-RECEIPT.json"
SIDECAR = DOC_ROOT / "CANDIDATE-ROOT-RECEIPT.sha256"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    findings = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    declared = {entry["path"] for entry in manifest["files"]}
    excluded = set(manifest["excluded_paths"])

    actual = set()
    for relative_root in manifest["candidate_roots"]:
        path = REPO / relative_root
        if path.is_file():
            actual.add(path.relative_to(REPO).as_posix())
        elif path.is_dir():
            actual.update(
                item.relative_to(REPO).as_posix()
                for item in path.rglob("*")
                if item.is_file() and "__pycache__" not in item.parts
            )
        else:
            findings.append("MISSING_CANDIDATE_ROOT:" + relative_root)

    for entry in manifest["files"]:
        path = REPO / entry["path"]
        if not path.is_file():
            findings.append("MISSING:" + entry["path"])
            continue
        if path.stat().st_size != entry["byte_size"]:
            findings.append("SIZE:" + entry["path"])
        if sha256(path) != entry["sha256"]:
            findings.append("SHA:" + entry["path"])

    if actual != declared | excluded:
        for path in sorted(actual - declared - excluded):
            findings.append("UNDECLARED:" + path)
        for path in sorted((declared | excluded) - actual):
            findings.append("DECLARED_MISSING:" + path)

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if receipt["manifest_path"] != MANIFEST.relative_to(REPO).as_posix():
        findings.append("RECEIPT_MANIFEST_PATH")
    if receipt["manifest_byte_size"] != MANIFEST.stat().st_size:
        findings.append("RECEIPT_MANIFEST_SIZE")
    if receipt["manifest_sha256"] != sha256(MANIFEST):
        findings.append("RECEIPT_MANIFEST_SHA")
    if receipt["exact_base_commit"] != "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0":
        findings.append("EXACT_BASE")

    tokens = SIDECAR.read_text(encoding="utf-8").strip().split()
    if len(tokens) < 2 or tokens[0] != sha256(RECEIPT):
        findings.append("RECEIPT_SIDECAR")

    if findings:
        print("GHCH_V0_1_REPOSITORY_CANDIDATE_REJECTED")
        print("\n".join(findings))
        return 1
    print("GHCH_V0_1_REPOSITORY_CANDIDATE_CONFORMS_NOT_ADMITTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
