#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ANCHOR-MANIFEST.json"
RECEIPT = ROOT / "ANCHOR-ROOT-RECEIPT.json"
SIDECAR = ROOT / "ANCHOR-ROOT-RECEIPT.sha256"

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def main() -> int:
    findings = []
    manifest = load("ANCHOR-MANIFEST.json")
    declared = {item["path"] for item in manifest["files"]}
    excluded = set(manifest["excluded_paths"])
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}

    for item in manifest["files"]:
        path = ROOT / item["path"]
        if not path.is_file():
            findings.append("MISSING:" + item["path"])
            continue
        if path.stat().st_size != item["byte_size"]:
            findings.append("SIZE:" + item["path"])
        if sha256(path) != item["sha256"]:
            findings.append("SHA:" + item["path"])

    if actual != declared | excluded:
        findings.append("INVENTORY")

    receipt = load("ANCHOR-ROOT-RECEIPT.json")
    if receipt["manifest_byte_size"] != MANIFEST.stat().st_size:
        findings.append("MANIFEST_SIZE")
    if receipt["manifest_sha256"] != sha256(MANIFEST):
        findings.append("MANIFEST_SHA")
    sidecar = SIDECAR.read_text(encoding="utf-8").strip().split()
    if len(sidecar) < 2 or sidecar[0] != sha256(RECEIPT):
        findings.append("RECEIPT_SIDECAR")

    merge = load("MERGE-EVENT.json")
    if merge["actual_merge_commit"] != "1d6350cd4545e873078e8c088da608416dee3802":
        findings.append("MERGE_COMMIT")
    if merge["ordered_parents"] != [
        "9c779c305be8455f355051a561e9ea89e7feee36",
        "aa07846cdea30ab06ee8c56cbf72946fc9266bca",
    ]:
        findings.append("PARENTS")
    if merge["merge_tree_binding"]["tree_content_relationship"] != "MERGE_COMMIT_TREE_CONTENT_IDENTICAL_TO_REVIEWED_HEAD_TREE":
        findings.append("TREE_RELATION")

    anchor = load("ADMISSION-ANCHOR.json")
    if anchor["current_standing"] != "APPEND_ONLY_ADMISSION_ANCHOR_CANDIDATE_NOT_ADMITTED":
        findings.append("STANDING")
    nonclaims = load("NON-CLAIMS.json")
    if "not self-admission of this anchor candidate" not in nonclaims["non_claims"]:
        findings.append("SELF_ADMISSION")

    if findings:
        print("PR98_TP001_ADMISSION_ANCHOR_CANDIDATE_REJECTED")
        print("\n".join(findings))
        return 1
    print("PR98_TP001_ADMISSION_ANCHOR_CANDIDATE_CONFORMS_NOT_ADMITTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
