#!/usr/bin/env python3
"""Read pinned Git blobs; verify this observation, not the historical freeze.

Does not execute the package, write receipts, or inspect any later PR head.
Requires the source commit locally (fetch the preservation branch if needed).
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

SOURCE = "ca28599b7ca411060e1fc3667ef97596244ed9bb"
ROOT = "docs/experiments/lens-shift-mdrc-002/"
HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPOSITORY)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def observe():
    inventory, blobs = [], {}
    for entry in git("ls-tree", "-rz", SOURCE, "--", ROOT).split(b"\0"):
        if not entry:
            continue
        meta, path = entry.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        if kind != "blob" or mode != "100644":
            raise ValueError("Unexpected package entry")
        rel = path.decode()[len(ROOT):]
        data = git("cat-file", "blob", oid)
        blobs[rel] = data
        inventory.append({"path": rel, "git_blob": oid, "size_bytes": len(data),
                          "sha256": digest(data)})
    manifest = blobs["SHA256SUMS"]
    entries = []
    for line in manifest.decode("utf-8-sig").splitlines():
        expected, path = line.split(None, 1)
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValueError("Malformed digest")
        actual = digest(blobs[path]) if path in blobs else None
        entries.append({"path": path, "expected_sha256": expected,
                        "actual_sha256": actual, "matches": actual == expected})
    freeze = json.loads(blobs["receipts/LS_MDRC_002_CONSTRUCTION_FREEZE_001.json"])
    bindings, non_digest_bindings = [], []
    for path, expected in freeze["key_digest_bindings"].items():
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            non_digest_bindings.append({"path": path, "value": expected})
            continue
        actual = digest(blobs[path]) if path in blobs else None
        bindings.append({"path": path, "expected_sha256": expected,
                         "actual_sha256": actual, "matches": actual == expected})
    manifest_paths = [e["path"] for e in entries]
    holdout = json.loads(blobs["fixtures/holdout/HOLDOUT_MANIFEST.json"])
    return {
        "source_commit": SOURCE, "package_root": ROOT,
        "package_tree": git("rev-parse", SOURCE + ":" + ROOT.rstrip("/")).decode().strip(),
        "inventory": inventory,
        "manifest_has_utf8_bom": manifest.startswith(b"\xef\xbb\xbf"),
        "manifest_entries": entries,
        "manifest_duplicate_paths": sorted({p for p in manifest_paths if manifest_paths.count(p) > 1}),
        "unlisted_package_files": sorted(set(blobs) - set(manifest_paths)),
        "freeze_digest_bindings": bindings,
        "freeze_non_digest_bindings": non_digest_bindings,
        "population": {
            "observed_files_including_manifest": len(blobs),
            "observed_files_excluding_manifest": len(blobs) - 1,
            "manifest_entries": len(entries),
            "freeze_list_entries": len(freeze["package_population"]),
            "freeze_list_matches_observed_paths": sorted(freeze["package_population"]) == sorted(blobs),
            "declared_including_manifest": freeze["package_population_count_including_sha256sums"],
            "declared_excluding_manifest": freeze["package_population_count_excluding_sha256sums"],
            "declared_unsuffixed_count": freeze["package_population_count"],
            "declared_entries_checked": freeze["sha256sums_verification"]["entries_checked"],
        },
        "holdout_manifest_declarations": holdout["holdout_fixtures"],
        "tracked_run_files": sorted(p for p in blobs if p.startswith("runs/")),
        "tracked_specification_files": sorted(p for p in blobs if p.startswith("SPECIFICATION/")),
        "package_at_source_evidence_commit": git("ls-tree", "-r", freeze["source_evidence_commit"], "--", ROOT).decode(),
        "package_at_admission_base_commit": git("ls-tree", "-r", freeze["admission_base_commit"], "--", ROOT).decode(),
    }


def main():
    observed = observe()
    expected = json.loads((HERE / "OBSERVED_PACKAGE.json").read_text(encoding="utf-8"))
    if observed != expected:
        print("FAIL: observation differs from pinned Git bytes")
        return 1
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected_hash, rel = line.split(None, 1)
        if digest((HERE / rel).read_bytes()) != expected_hash:
            print("FAIL: reconciliation artifact differs: " + rel)
            return 1
    print("PASS: reconciliation artifacts and observation match pinned source bytes")
    print("Historical manifest: 28/29 entries match; freeze qualification remains withheld")
    return 0


if __name__ == "__main__":
    sys.exit(main())
