#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Adversarial Cases Checker v0.1.

Currently implements:

- LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1

The checker copies the Day-0 packet into a disposable temporary repository-shaped
directory, falsifies the expected reconstruction provenance receipt, recomputes
that receipt hash into packet_manifest.json, recomputes packet_manifest.sha256,
updates packet_manifest_outer_receipt.json, and then runs the unmodified Day-0
checker against the disposable copy.

Expected current observation:

- the re-sealed scratch packet still passes the Day-0 checker.

This confirms a bounded root-of-trust limitation: the Day-0 checker verifies
internal consistency relative to the current manifest and outer receipt; it does
not distinguish original sealing from coordinated re-sealing without an external
anchor.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, validation, production
readiness, procurement approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple


PACKET_ROOT = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1")
DAY0_CHECKER = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")
CASE_ID = "LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1"

OUTCOME_CODES = [
    "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
    "COORDINATED_RESEAL_CONFIRMED",
    "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED",
    "SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL",
]

NON_AUTHORITY_STATEMENT = (
    "This adversarial checker records root-of-trust and checker-scope behavior only; "
    "it does not validate truth, compliance, legal sufficiency, safety, authorization, "
    "approval, certification, endorsement, validation, production readiness, "
    "procurement approval, or institutional authority."
)


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def write_json(path: pathlib.Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_day0_checker(repo_root: pathlib.Path, cwd: pathlib.Path) -> Dict[str, Any]:
    checker_path = repo_root / DAY0_CHECKER

    completed = subprocess.run(
        [sys.executable, str(checker_path), "--json"],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    parsed = None
    parse_error = None
    try:
        parsed = json.loads(completed.stdout)
    except Exception as exc:  # pragma: no cover - diagnostic branch
        parse_error = str(exc)

    return {
        "command": f"{sys.executable} {checker_path} --json",
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "parsed": parsed,
        "parse_error": parse_error,
    }


def prepare_scratch_packet(repo_root: pathlib.Path) -> Tuple[pathlib.Path, pathlib.Path]:
    scratch_root = pathlib.Path(tempfile.mkdtemp(prefix="fork_lrt_day0_reseal_"))
    source_packet = repo_root / PACKET_ROOT
    scratch_packet = scratch_root / PACKET_ROOT

    if not source_packet.exists():
        raise FileNotFoundError(f"missing Day-0 packet: {source_packet}")

    scratch_packet.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_packet, scratch_packet)

    return scratch_root, scratch_packet


def mutate_and_reseal(scratch_packet: pathlib.Path) -> Dict[str, Any]:
    receipt_rel = pathlib.Path("receipts/day0_expected_reconstruction_provenance_receipt.json")
    receipt_path = scratch_packet / receipt_rel
    manifest_path = scratch_packet / "packet_manifest.json"
    sidecar_path = scratch_packet / "packet_manifest.sha256"
    outer_receipt_path = scratch_packet / "packet_manifest_outer_receipt.json"

    receipt = load_json(receipt_path)
    original_receipt_hash = sha256_file(receipt_path)

    original_provenance_status = receipt.get("provenance_status")
    original_independence_status = receipt.get("independence_status")

    receipt["provenance_status"] = "independent_external_reviewer_provenance"
    receipt["independence_status"] = "independently_verified_in_v0_1"
    receipt["boundary_note"] = (
        "ADVERSARIAL MUTATION: this scratch-copy value falsely claims independent provenance "
        "to test whether coordinated re-seal is detected by the current Day-0 checker."
    )
    receipt["adversarial_mutation"] = {
        "case_id": CASE_ID,
        "mutation_type": "coordinated_reseal_after_falsified_provenance",
        "not_part_of_clean_packet": True,
    }

    write_json(receipt_path, receipt)
    mutated_receipt_hash = sha256_file(receipt_path)

    manifest = load_json(manifest_path)
    original_manifest_hash = sha256_file(manifest_path)

    artifact_hashes = manifest.get("artifact_hashes", [])
    if not isinstance(artifact_hashes, list):
        raise ValueError("manifest artifact_hashes must be list")

    patched_artifact = False
    for item in artifact_hashes:
        if not isinstance(item, dict):
            continue

        item_path = str(item.get("path", "")).replace("\\", "/")
        if item_path.endswith("receipts/day0_expected_reconstruction_provenance_receipt.json"):
            item["sha256"] = mutated_receipt_hash
            patched_artifact = True

    if not patched_artifact:
        raise ValueError("could not find provenance receipt artifact hash entry in manifest")

    write_json(manifest_path, manifest)
    resealed_manifest_hash = sha256_file(manifest_path)

    sidecar_path.write_text(f"{resealed_manifest_hash}  packet_manifest.json\n", encoding="utf-8")

    outer = load_json(outer_receipt_path)
    original_outer_hash = outer.get("packet_manifest_sha256")
    outer["packet_manifest_sha256"] = resealed_manifest_hash
    outer["adversarial_reseal_note"] = (
        "ADVERSARIAL MUTATION: scratch-copy outer receipt updated to bind the re-sealed manifest."
    )
    write_json(outer_receipt_path, outer)

    return {
        "mutation_target": str(receipt_rel).replace("\\", "/"),
        "original_provenance_status": original_provenance_status,
        "mutated_provenance_status": receipt["provenance_status"],
        "original_independence_status": original_independence_status,
        "mutated_independence_status": receipt["independence_status"],
        "original_receipt_sha256": original_receipt_hash,
        "mutated_receipt_sha256": mutated_receipt_hash,
        "original_manifest_sha256": original_manifest_hash,
        "resealed_manifest_sha256": resealed_manifest_hash,
        "original_outer_receipt_manifest_sha256": original_outer_hash,
        "resealed_outer_receipt_manifest_sha256": outer["packet_manifest_sha256"],
    }


def evaluate_case(repo_root: pathlib.Path, keep_temp: bool) -> Dict[str, Any]:
    clean_run = run_day0_checker(repo_root=repo_root, cwd=repo_root)

    scratch_root = None
    scratch_packet = None
    mutation = None
    resealed_run = None

    try:
        scratch_root, scratch_packet = prepare_scratch_packet(repo_root)
        mutation = mutate_and_reseal(scratch_packet)
        resealed_run = run_day0_checker(repo_root=repo_root, cwd=scratch_root)

        clean_parsed = clean_run.get("parsed") or {}
        resealed_parsed = resealed_run.get("parsed") or {}

        clean_ok = (
            clean_run["exit_code"] == 0
            and clean_parsed.get("failed") == 0
            and clean_parsed.get("passed") == clean_parsed.get("total")
        )

        resealed_passes_day0_checker = (
            resealed_run["exit_code"] == 0
            and resealed_parsed.get("failed") == 0
            and resealed_parsed.get("passed") == resealed_parsed.get("total")
        )

        mutation_ok = (
            mutation["original_provenance_status"] == "author_declared_day0_fixture_baseline"
            and mutation["mutated_provenance_status"] == "independent_external_reviewer_provenance"
            and mutation["original_receipt_sha256"] != mutation["mutated_receipt_sha256"]
            and mutation["original_manifest_sha256"] != mutation["resealed_manifest_sha256"]
            and mutation["resealed_manifest_sha256"] == mutation["resealed_outer_receipt_manifest_sha256"]
        )

        passed = clean_ok and mutation_ok and resealed_passes_day0_checker

        return {
            "case_id": CASE_ID,
            "passed": passed,
            "classification": "root_of_trust_limitation_confirmed" if passed else "unexpected_result",
            "expected_observation": "coordinated re-sealed scratch packet remains Day-0-checker-pass under current unanchored internal-consistency checks",
            "actual_observation": "resealed packet passed Day-0 checker" if resealed_passes_day0_checker else "resealed packet did not pass Day-0 checker",
            "outcome_codes": OUTCOME_CODES if passed else ["UNEXPECTED_ADVERSARIAL_RESULT"],
            "clean_day0_checker": summarize_run(clean_run),
            "resealed_day0_checker": summarize_run(resealed_run),
            "mutation": mutation,
            "scratch_root": str(scratch_root) if keep_temp and scratch_root else None,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }
    finally:
        if scratch_root is not None and not keep_temp:
            shutil.rmtree(scratch_root, ignore_errors=True)


def summarize_run(run: Dict[str, Any] | None) -> Dict[str, Any]:
    if not run:
        return {
            "exit_code": None,
            "parsed": None,
            "parse_error": "run missing",
        }

    parsed = run.get("parsed")
    summary = {
        "exit_code": run.get("exit_code"),
        "parse_error": run.get("parse_error"),
    }

    if isinstance(parsed, dict):
        summary.update({
            "checker": parsed.get("checker"),
            "total": parsed.get("total"),
            "passed": parsed.get("passed"),
            "failed": parsed.get("failed"),
        })
    else:
        summary["stdout"] = run.get("stdout")

    return summary


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path(args.repo_root).resolve()

    cases = [evaluate_case(repo_root=repo_root, keep_temp=args.keep_temp)]
    failed = sum(1 for case in cases if not case["passed"])

    summary = {
        "checker": "check_longitudinal_day0_adversarial_cases_v0_1.py",
        "total": len(cases),
        "passed": len(cases) - failed,
        "failed": failed,
        "cases": cases,
        "non_authority_statement": NON_AUTHORITY_STATEMENT,
    }

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"Longitudinal Day-0 adversarial cases: {summary['passed']}/{summary['total']} passed")
        for case in cases:
            status = "PASS" if case["passed"] else "FAIL"
            print(f"{status} {case['case_id']}: {case['actual_observation']}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))