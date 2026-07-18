#!/usr/bin/env python3
"""Fork-admitted repository-shaped derivative harness for M87 ADV_003.

Runs seven bounded checks against the versioned Day-0 v0.1.1 successor checker:
clean pass, unmanifested-addition rejection, manifested scratch mutation rejection,
packet-root/cwd separation, path-escape rejection, symlink rejection, and unchanged
standing of historical ADV_001/ADV_002 cases.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple

PACKET_REL = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1")
CHECKER_REL = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1_1.py")
HISTORICAL_ADV_REL = pathlib.Path("tools/check_longitudinal_day0_adversarial_cases_v0_1.py")
MUTATION_REL = pathlib.Path("evidence/day0_injected_extra_v0_1.json")
MANIFESTED_REL = pathlib.Path("evidence/day0_request_record.json")


def run_json(command: List[str], cwd: pathlib.Path) -> Dict[str, Any]:
    proc = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True)
    try:
        payload = json.loads(proc.stdout)
    except Exception as exc:
        return {"_parse_error": str(exc), "_stdout": proc.stdout[:1000], "_stderr": proc.stderr[:1000], "_exit": proc.returncode}
    payload["_exit"] = proc.returncode
    return payload


def result_names(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("name")): item for item in payload.get("results", []) if isinstance(item, dict)}


def copy_repo_shaped_packet(repo_root: pathlib.Path, temp_root: pathlib.Path, name: str) -> Tuple[pathlib.Path, pathlib.Path]:
    shaped_root = temp_root / name
    packet = shaped_root / PACKET_REL
    packet.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root / PACKET_REL, packet)
    return shaped_root, packet


def run_successor(repo_root: pathlib.Path, packet: pathlib.Path, cwd: pathlib.Path) -> Dict[str, Any]:
    return run_json([sys.executable, str(repo_root / CHECKER_REL), "--packet-root", str(packet), "--json"], cwd)


def case(case_id: str, passed: bool, expected: str, actual: str, outcome_codes: List[str], evidence: Any) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": passed, "expected_observation": expected, "actual_observation": actual, "outcome_codes": outcome_codes if passed else ["UNEXPECTED_RESULT"], "evidence": evidence}


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)
    repo_root = pathlib.Path(args.repo_root).resolve()
    if not (repo_root / CHECKER_REL).exists() or not (repo_root / PACKET_REL).exists():
        print(json.dumps({"status": "TOOL_ERROR", "detail": "successor checker or Day-0 packet missing", "repo_root": str(repo_root)}, indent=2))
        return 3

    temp_root = pathlib.Path(tempfile.mkdtemp(prefix="fork_adv003_postfix_"))
    cases: List[Dict[str, Any]] = []
    try:
        clean_root, clean_packet = copy_repo_shaped_packet(repo_root, temp_root, "clean")
        clean = run_successor(repo_root, clean_packet, clean_root)
        clean_ok = clean.get("_exit") == 0 and clean.get("failed") == 0
        cases.append(case("ADV_003_POST_FIX_CLEAN_PACKET", clean_ok, "clean isolated packet passes", "clean packet passed" if clean_ok else "clean packet failed", ["CLEAN_PACKET_STILL_VERIFIES"], clean))

        add_root, add_packet = copy_repo_shaped_packet(repo_root, temp_root, "unmanifested")
        injected = add_packet / MUTATION_REL
        injected.write_text(json.dumps({"case_id": "LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1", "purpose": "post-fix rejection check"}, indent=2) + "\n", encoding="utf-8")
        add_run = run_successor(repo_root, add_packet, add_root)
        add_names = result_names(add_run)
        add_ok = add_run.get("_exit") == 1 and add_names.get("inventory:unexpected-files", {}).get("passed") is False and MUTATION_REL.as_posix() in add_names.get("inventory:unexpected-files", {}).get("detail", "")
        cases.append(case("LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_POST_FIX", add_ok, "unmanifested addition is rejected", "unmanifested addition rejected" if add_ok else "unmanifested addition was not rejected as expected", ["ADV_003_A_INVENTORY_ADDITION_DETECTED"], add_run))

        mut_root, mut_packet = copy_repo_shaped_packet(repo_root, temp_root, "manifested_mutation")
        target = mut_packet / MANIFESTED_REL
        target.write_bytes(target.read_bytes() + b"\nADV_003_MANIFESTED_SCRATCH_MUTATION\n")
        mut_run = run_successor(repo_root, mut_packet, mut_root)
        mut_names = result_names(mut_run)
        mut_ok = mut_run.get("_exit") == 1 and mut_names.get("manifest:artifact-hashes", {}).get("passed") is False and "hash mismatch" in mut_names.get("manifest:artifact-hashes", {}).get("detail", "")
        cases.append(case("ADV_003_B_MANIFESTED_SCRATCH_MUTATION", mut_ok, "manifested mutation in scratch packet is detected", "scratch mutation detected" if mut_ok else "scratch mutation not detected", ["ADV_003_B_PACKET_ROOT_HASH_BASE_ENFORCED"], mut_run))

        root_a, packet_a = copy_repo_shaped_packet(repo_root, temp_root, "packet_root_source")
        root_b, packet_b = copy_repo_shaped_packet(repo_root, temp_root, "cwd_decoy")
        decoy = packet_b / MANIFESTED_REL
        decoy.write_bytes(decoy.read_bytes() + b"\nCWD_DECOY_MUTATION\n")
        cwd_run = run_successor(repo_root, packet_a, root_b)
        cwd_ok = cwd_run.get("_exit") == 0 and cwd_run.get("failed") == 0
        cases.append(case("ADV_003_B_CWD_DECOY_IGNORED", cwd_ok, "hashes resolve beneath supplied packet root, not cwd", "cwd decoy ignored" if cwd_ok else "cwd influenced supplied packet-root verification", ["PACKET_ROOT_CONTROLS_ARTIFACT_RESOLUTION"], cwd_run))

        esc_root, esc_packet = copy_repo_shaped_packet(repo_root, temp_root, "path_escape")
        manifest_path = esc_packet / "packet_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifact_hashes"][0]["path"] = "../outside.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        esc_run = run_successor(repo_root, esc_packet, esc_root)
        esc_names = result_names(esc_run)
        esc_ok = esc_run.get("_exit") == 1 and esc_names.get("manifest:artifact-paths", {}).get("passed") is False and "prohibited" in esc_names.get("manifest:artifact-paths", {}).get("detail", "")
        cases.append(case("ADV_003_PATH_ESCAPE_REJECTION", esc_ok, "manifest path escape is rejected", "path escape rejected" if esc_ok else "path escape was not rejected as expected", ["PATH_ESCAPE_REJECTED"], esc_run))

        sym_root, sym_packet = copy_repo_shaped_packet(repo_root, temp_root, "symlink")
        sym_target = sym_packet / MANIFESTED_REL
        backup = temp_root / "symlink_target.json"
        shutil.copy2(sym_target, backup)
        sym_target.unlink()
        symlink_created = False
        symlink_error = None
        try:
            os.symlink(backup, sym_target)
            symlink_created = True
        except OSError as exc:
            symlink_error = str(exc)
        if symlink_created:
            sym_run = run_successor(repo_root, sym_packet, sym_root)
            sym_names = result_names(sym_run)
            sym_ok = sym_run.get("_exit") == 1 and sym_names.get("inventory:symlinks", {}).get("passed") is False and MANIFESTED_REL.as_posix() in sym_names.get("inventory:symlinks", {}).get("detail", "")
            evidence: Any = sym_run
            actual = "symlink substitution rejected" if sym_ok else "symlink substitution not rejected"
        else:
            sym_ok = False
            evidence = {"environment_error": symlink_error}
            actual = "environment could not create required symlink test fixture"
        cases.append(case("ADV_003_SYMLINK_SUBSTITUTION_REJECTION", sym_ok, "symlink substitution is rejected", actual, ["SYMLINK_SUBSTITUTION_REJECTED"], evidence))

        historical = run_json([sys.executable, str(repo_root / HISTORICAL_ADV_REL), "--repo-root", str(repo_root), "--json"], repo_root)
        historical_cases = historical.get("cases", []) if isinstance(historical, dict) else []
        ids = {item.get("case_id"): item.get("passed") for item in historical_cases if isinstance(item, dict)}
        historical_ok = historical.get("_exit") == 0 and historical.get("failed") == 0 and ids.get("LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1") is True and ids.get("LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1") is True
        cases.append(case("ADV_001_ADV_002_STANDING_UNCHANGED", historical_ok, "historical ADV_001 and ADV_002 still reproduce", "historical standings unchanged" if historical_ok else "historical standing changed or could not be recomputed", ["EXISTING_ADVERSARIAL_STANDING_UNCHANGED"], historical))

        failed = sum(1 for item in cases if not item["passed"])
        payload = {
            "checker": "check_longitudinal_day0_adv_003_recomputation_v0_1.py",
            "case_family": "LRT_DAY0_ADV_003_UNMANIFESTED_ADDITION_v0_1",
            "total": len(cases), "passed": len(cases) - failed, "failed": failed,
            "cases": cases,
            "source_harness_preserved_unchanged": True,
            "derivative_harness": "repository_shaped_complete_isolation",
            "non_authority_statement": "This derivative harness records bounded checker behavior only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.",
            "scratch_root": str(temp_root) if args.keep_temp else None,
        }
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True))
        else:
            print(f"ADV_003 post-fix recomputation: {payload['passed']}/{payload['total']} passed")
            for item in cases:
                print(("PASS" if item["passed"] else "FAIL") + " " + item["case_id"])
        return 0 if failed == 0 else 1
    finally:
        if not args.keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
