#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ANCHOR-MANIFEST.json"
RECEIPT = ROOT / "ANCHOR-ROOT-RECEIPT.json"
SIDECAR = ROOT / "ANCHOR-ROOT-RECEIPT.sha256"

EXPECTED_RUNS = [
    ("Fork Evidence CI", 30314414968, 448),
    ("Root Checksum Manifest v0.1", 30314415002, 76),
    ("Fork Proof-Surface Integration", 30314414978, 147),
]
EXPECTED_CORRECTION_COMMITS = [
    "43f0541aae324671a9f708087cf1a2956ac86acb",
    "66e9bd67ff3716af856f6abf823a49caabec7065",
    "5473128e61d69b33440d5c30ab75cef9997111df",
    "f85ed9b4c5f6224da4eb1e3e78eaa2aebf27746a",
    "aa07846cdea30ab06ee8c56cbf72946fc9266bca",
]
EXPECTED_SURFACE_DIGESTS = {
    "candidate_manifest": "40825ad8680b225dae1c11bab815f74c8d4ca1ecdf7aa398099a303f62809d4a",
    "candidate_root_receipt": "0c269c6c276062d1ca5c11fbd0295d7268472a0550aaee7c046d13c5df9b08d6",
    "public_restricted_boundary": "3caf1f9489dd712db248f5a2d3c28e8e26186fb589ce3503269b9404ef591c5e",
    "boundary_checker": "d129e670fdf3d1df3dd4fa885df6afc4a24efdc45deb28d7d034e8109a17b1b1",
}

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
    if receipt["branch_base_commit"] != "1d6350cd4545e873078e8c088da608416dee3802":
        findings.append("ANCHOR_BASE")
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
    if merge["branch_tip_verification"] != {
        "comparison_base": "1d6350cd4545e873078e8c088da608416dee3802",
        "comparison_head": "preservation/clean-continuance-v0.1",
        "status": "IDENTICAL",
        "ahead_by": 0,
        "behind_by": 0,
    }:
        findings.append("BRANCH_TIP")
    tree = merge["merge_tree_binding"]
    if tree["tree_content_relationship"] != "MERGE_COMMIT_TREE_CONTENT_IDENTICAL_TO_REVIEWED_HEAD_TREE":
        findings.append("TREE_RELATION")
    if tree["reviewed_head_to_merge_commit_file_delta"] != []:
        findings.append("TREE_DELTA")
    if tree["exact_tree_sha"] is not None or tree["exact_tree_sha_standing"] != "NOT_EXPOSED_BY_AVAILABLE_CONNECTOR":
        findings.append("TREE_SHA_BOUNDARY")

    ci = load("CI-BINDING.json")
    observed_runs = [
        (run["name"], run["run_id"], run["run_number"])
        for run in ci["exact_head_workflows"]
        if run["status"] == "completed" and run["conclusion"] == "success"
    ]
    if observed_runs != EXPECTED_RUNS:
        findings.append("CI_RUNS")
    review = ci["review"]
    if review != {
        "review_id": 4792390081,
        "reviewed_commit": "aa07846cdea30ab06ee8c56cbf72946fc9266bca",
        "disposition": "REVIEWED_WITHIN_DECLARED_PUBLICATION_BOUNDARY_NO_BLOCKING_FINDINGS",
        "reviewer_standing": "NOT_INDEPENDENT_CONSTRUCTION_ASSISTED",
    }:
        findings.append("REVIEW_BINDING")
    post = ci["post_merge_observation"]
    if post["workflow_runs_returned_by_commit_query"] != [] or post["combined_status_entries"] != []:
        findings.append("POST_MERGE_OBSERVATION")
    if post["standing"] != "POST_MERGE_WORKFLOWS_NOT_OBSERVED_BY_AVAILABLE_CONNECTOR":
        findings.append("POST_MERGE_STANDING")

    correction = load("CORRECTION-LINEAGE.json")
    if correction["initial_green_head"] != "54e0632fb298c04afb4f9aadb4a52000d4f1f148":
        findings.append("INITIAL_HEAD")
    if correction["append_only_correction_commits"] != EXPECTED_CORRECTION_COMMITS:
        findings.append("CORRECTION_COMMITS")
    if correction["corrected_reviewed_head"] != "aa07846cdea30ab06ee8c56cbf72946fc9266bca":
        findings.append("CORRECTED_HEAD")
    if correction["history_rewritten"] is not False:
        findings.append("HISTORY_REWRITE")

    surfaces = load("SURFACE-BINDINGS.json")
    for key, digest in EXPECTED_SURFACE_DIGESTS.items():
        if surfaces[key]["sha256"] != digest:
            findings.append("SURFACE_DIGEST:" + key)
    standings = surfaces["surface_standings_if_anchor_admitted"]
    if standings["v0_2_lineage"] != "ADMITTED_LATER_PREDECESSOR_STANDING_RECONCILIATION_WITHOUT_INHERITANCE":
        findings.append("V0_2_INHERITANCE")

    anchor = load("ADMISSION-ANCHOR.json")
    if anchor["current_standing"] != "APPEND_ONLY_ADMISSION_ANCHOR_CANDIDATE_NOT_ADMITTED":
        findings.append("STANDING")
    if anchor["current_effect"]["repository_admission"] != "NONE":
        findings.append("ADMISSION_EFFECT")
    nonclaims = load("NON-CLAIMS.json")
    required_nonclaims = {
        "not organizational or arms-length independence",
        "not production readiness or deployment authorization",
        "not architecture correctness proof",
        "not legal, regulatory, or compliance sufficiency",
        "not authority transfer or execution permission",
        "not v0.2 exterior recomputation",
        "not publication of restricted raw evidence",
        "not a change to main",
        "not provider execution or Pair-001 execution",
        "not self-admission of this anchor candidate",
    }
    if set(nonclaims["non_claims"]) != required_nonclaims:
        findings.append("NON_CLAIMS")

    terminal = (ROOT / "TERMINAL-ANCHOR-RULE.md").read_text(encoding="utf-8")
    if "an immediate recursive self-anchor is not required" not in terminal:
        findings.append("TERMINAL_RULE")

    if findings:
        print("PR98_TP001_ADMISSION_ANCHOR_CANDIDATE_REJECTED")
        print("\n".join(findings))
        return 1
    print("PR98_TP001_ADMISSION_ANCHOR_CANDIDATE_CONFORMS_NOT_ADMITTED")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
