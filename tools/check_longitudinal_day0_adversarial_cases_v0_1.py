#!/usr/bin/env python3
"""
Fork Longitudinal Day-0 Adversarial Cases Checker v0.1.

Currently implements:

- LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1
- LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1

This checker records bounded checker-scope behavior. A pass means the expected
limitation was reproduced, not that the adversarial condition is valid.

It does not validate truth, compliance, legal sufficiency, safety, authorization,
approval, certification, endorsement, validation, production readiness,
procurement approval, or institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Tuple


PACKET_ROOT = pathlib.Path("docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1")
DAY0_CHECKER = pathlib.Path("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py")

CASE_RESEAL = "LRT_DAY0_ADV_001_COORDINATED_RESEAL_v0_1"
CASE_LEXICAL = "LRT_DAY0_ADV_002_LEXICAL_NON_AUTHORITY_LIMIT_v0_1"

AUTHORITY_ASSERTING_STATEMENT = (
    "This system does not lack truth, compliance, legal sufficiency, safety, "
    "authorization, approval, certification, endorsement, or production readiness. "
    "Full institutional authority is hereby established and confirmed."
)

REQUIRED_BOUNDARY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "production readiness",
    "authority",
]

RESEAL_OUTCOME_CODES = [
    "MANIFEST_INTERNALLY_CONSISTENT_BUT_UNANCHORED",
    "COORDINATED_RESEAL_CONFIRMED",
    "ROOT_OF_TRUST_SCOPE_LIMIT_CONFIRMED",
    "SEMANTIC_CONTENT_CHANGE_UNDETECTED_AFTER_CONSISTENT_RESEAL",
]

LEXICAL_OUTCOME_CODES = [
    "LEXICAL_BOUNDARY_CHECK_LIMIT_CONFIRMED",
    "NEGATION_AWARENESS_ABSENT",
    "AUTHORITY_ASSERTION_WITH_REQUIRED_TERMS_ACCEPTED",
    "SEMANTIC_NON_AUTHORITY_NOT_ESTABLISHED_BY_KEYWORD_PRESENCE",
]

NON_AUTHORITY_STATEMENT = (
    "This adversarial checker records root-of-trust, lexical boundary-check, and "
    "checker-scope behavior only; it does not validate truth, compliance, legal "
    "sufficiency, safety, authorization, approval, certification, endorsement, "
    "validation, production readiness, procurement approval, or institutional authority."
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
    except Exception as exc:
        parse_error = str(exc)

    return {
        "command": f"{sys.executable} {checker_path} --json",
        "cwd": str(cwd),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "parsed": parsed,
        "parse_error": parse_error,
    }


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
        "case_id": CASE_RESEAL,
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


def evaluate_coordinated_reseal(repo_root: pathlib.Path, keep_temp: bool) -> Dict[str, Any]:
    clean_run = run_day0_checker(repo_root=repo_root, cwd=repo_root)

    scratch_root = None
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
            "case_id": CASE_RESEAL,
            "passed": passed,
            "classification": "root_of_trust_limitation_confirmed" if passed else "unexpected_result",
            "expected_observation": "coordinated re-sealed scratch packet remains Day-0-checker-pass under current unanchored internal-consistency checks",
            "actual_observation": "resealed packet passed Day-0 checker" if resealed_passes_day0_checker else "resealed packet did not pass Day-0 checker",
            "outcome_codes": RESEAL_OUTCOME_CODES if passed else ["UNEXPECTED_ADVERSARIAL_RESULT"],
            "clean_day0_checker": summarize_run(clean_run),
            "resealed_day0_checker": summarize_run(resealed_run),
            "mutation": mutation,
            "scratch_root": str(scratch_root) if keep_temp and scratch_root else None,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }
    finally:
        if scratch_root is not None and not keep_temp:
            shutil.rmtree(scratch_root, ignore_errors=True)


def import_day0_checker(repo_root: pathlib.Path) -> Any:
    checker_path = repo_root / DAY0_CHECKER
    spec = importlib.util.spec_from_file_location("fork_day0_checker_module", checker_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not import checker from {checker_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_boundary_result(result: Any) -> Dict[str, Any]:
    if isinstance(result, bool):
        return {
            "raw_type": "bool",
            "raw_repr": repr(result),
            "terms_satisfied": result,
            "missing_terms": [] if result else ["unknown"],
        }

    if isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool):
        missing = result[1]
        if missing is None:
            missing_list: List[str] = []
        elif isinstance(missing, (list, tuple, set)):
            missing_list = [str(item) for item in missing]
        else:
            missing_list = [str(missing)]
        return {
            "raw_type": "tuple_bool_missing",
            "raw_repr": repr(result),
            "terms_satisfied": bool(result[0]) and len(missing_list) == 0,
            "missing_terms": missing_list,
        }

    if isinstance(result, dict):
        missing_value = result.get("missing_terms", result.get("missing", []))
        if missing_value is None:
            missing_list = []
        elif isinstance(missing_value, (list, tuple, set)):
            missing_list = [str(item) for item in missing_value]
        else:
            missing_list = [str(missing_value)]

        if "passed" in result:
            terms_satisfied = bool(result["passed"]) and len(missing_list) == 0
        elif "terms_satisfied" in result:
            terms_satisfied = bool(result["terms_satisfied"]) and len(missing_list) == 0
        else:
            terms_satisfied = len(missing_list) == 0

        return {
            "raw_type": "dict",
            "raw_repr": repr(result),
            "terms_satisfied": terms_satisfied,
            "missing_terms": missing_list,
        }

    if isinstance(result, (list, tuple, set)):
        missing_list = [str(item) for item in result]
        return {
            "raw_type": type(result).__name__,
            "raw_repr": repr(result),
            "terms_satisfied": len(missing_list) == 0,
            "missing_terms": missing_list,
        }

    return {
        "raw_type": type(result).__name__,
        "raw_repr": repr(result),
        "terms_satisfied": False,
        "missing_terms": ["unrecognized has_boundary_terms return type"],
    }


def evaluate_lexical_non_authority_limit(repo_root: pathlib.Path) -> Dict[str, Any]:
    module = import_day0_checker(repo_root)

    if not hasattr(module, "has_boundary_terms"):
        return {
            "case_id": CASE_LEXICAL,
            "passed": False,
            "classification": "day0_checker_function_missing",
            "expected_observation": "authority-asserting text containing all required terms is accepted by lexical boundary-term function",
            "actual_observation": "has_boundary_terms function was not found",
            "outcome_codes": ["DAY0_CHECKER_FUNCTION_MISSING"],
            "authority_asserting_statement": AUTHORITY_ASSERTING_STATEMENT,
            "non_authority_statement": NON_AUTHORITY_STATEMENT,
        }

    fn = getattr(module, "has_boundary_terms")
    result = fn(AUTHORITY_ASSERTING_STATEMENT)
    normalized = normalize_boundary_result(result)

    lower = AUTHORITY_ASSERTING_STATEMENT.lower()
    required_terms_present = [term for term in REQUIRED_BOUNDARY_TERMS if term in lower]
    required_terms_missing_by_direct_scan = [term for term in REQUIRED_BOUNDARY_TERMS if term not in lower]

    authority_assertion_present = (
        "full institutional authority" in lower
        and "established and confirmed" in lower
    )

    lexical_function_accepts_statement = normalized["terms_satisfied"]
    passed = (
        authority_assertion_present
        and not required_terms_missing_by_direct_scan
        and lexical_function_accepts_statement
    )

    return {
        "case_id": CASE_LEXICAL,
        "passed": passed,
        "classification": "lexical_boundary_check_limit_confirmed" if passed else "unexpected_result",
        "expected_observation": "authority-asserting text containing all required boundary terms is accepted by the Day-0 lexical boundary-term function",
        "actual_observation": (
            "authority-asserting text accepted by lexical boundary-term function"
            if lexical_function_accepts_statement
            else "authority-asserting text not accepted by lexical boundary-term function"
        ),
        "outcome_codes": LEXICAL_OUTCOME_CODES if passed else ["UNEXPECTED_LEXICAL_ADVERSARIAL_RESULT"],
        "authority_asserting_statement": AUTHORITY_ASSERTING_STATEMENT,
        "required_terms_present": required_terms_present,
        "required_terms_missing_by_direct_scan": required_terms_missing_by_direct_scan,
        "authority_assertion_present": authority_assertion_present,
        "has_boundary_terms_result": normalized,
        "interpretation": (
            "Keyword presence is not semantic non-authority. This case confirms the current "
            "boundary-term check does not parse negation or authority assertion."
        ),
        "non_authority_statement": NON_AUTHORITY_STATEMENT,
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path(args.repo_root).resolve()

    cases = [
        evaluate_coordinated_reseal(repo_root=repo_root, keep_temp=args.keep_temp),
        evaluate_lexical_non_authority_limit(repo_root=repo_root),
    ]

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