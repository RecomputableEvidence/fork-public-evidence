#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "CANDIDATE-MANIFEST.json"
ROOT_RECEIPT_PATH = ROOT / "CANDIDATE-ROOT-RECEIPT.json"
ROOT_RECEIPT_SIDECAR_PATH = ROOT / "CANDIDATE-ROOT-RECEIPT.sha256"
BOUNDARY_PATH = ROOT / "PUBLIC-RESTRICTED-EVIDENCE-BOUNDARY.json"
LINEAGE_PATH = ROOT / "v0.2/EXTERIOR-STANDING-LINEAGE-ANCHOR.json"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    findings = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    declared = {entry["path"] for entry in manifest["files"]}
    excluded = set(manifest.get("excluded_paths", []))
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }

    for entry in manifest["files"]:
        path = ROOT / entry["path"]
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

    root_receipt = json.loads(ROOT_RECEIPT_PATH.read_text(encoding="utf-8"))
    if root_receipt.get("manifest_path") != MANIFEST_PATH.name:
        findings.append("ROOT_RECEIPT_MANIFEST_PATH")
    if root_receipt.get("manifest_byte_size") != MANIFEST_PATH.stat().st_size:
        findings.append("ROOT_RECEIPT_MANIFEST_SIZE")
    if root_receipt.get("manifest_sha256") != sha256(MANIFEST_PATH):
        findings.append("ROOT_RECEIPT_MANIFEST_SHA")
    sidecar_tokens = ROOT_RECEIPT_SIDECAR_PATH.read_text(encoding="utf-8").strip().split()
    if len(sidecar_tokens) < 2 or sidecar_tokens[0] != sha256(ROOT_RECEIPT_PATH):
        findings.append("ROOT_RECEIPT_SIDECAR")

    boundary = json.loads(BOUNDARY_PATH.read_text(encoding="utf-8"))
    if set(boundary.get("public_paths", [])) != actual:
        findings.append("PUBLIC_PATH_INVENTORY")
    actual_names = {Path(path).name for path in actual}
    for artifact in boundary.get("restricted_artifacts", []):
        name = Path(artifact["artifact"]).name
        digest = artifact.get("sha256")
        if not isinstance(digest, str) or re.fullmatch(r"[0-9a-f]{64}", digest) is None:
            findings.append("RESTRICTED_DIGEST:" + name)
        if name in actual_names:
            findings.append("RESTRICTED_PRESENT:" + name)

    lineage = json.loads(LINEAGE_PATH.read_text(encoding="utf-8"))
    if lineage["temporal_reconciliation"]["v0_2_exterior_verification_established"] is not False:
        findings.append("INHERITANCE")

    if findings:
        print("TP001_PUBLIC_BOUNDARY_CANDIDATE_REJECTED")
        print("\n".join(findings))
        return 1

    print("TP001_PUBLIC_BOUNDARY_CANDIDATE_CONFORMS_NOT_ADMITTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
