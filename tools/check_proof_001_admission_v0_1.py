#!/usr/bin/env python3
"""Verify the bounded Proof 001 admission successor."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

CHECKER_ID = "FORK_PROOF_001_ADMISSION_CHECKER_v0_1"
ADMISSION = Path("docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/ADMISSION_v0_1.json")
STANDING = Path("docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/STANDING.json")
MANIFEST = Path("docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/PROOF-MANIFEST.json")
INDEX = Path("docs/proof-atlas/PROOF_INDEX_v0_1.json")
WRAPPER = Path("tools/run_proof_001_review_does_not_silently_travel_v0_1.py")
EXPECTED_WRAPPER_RESULT = "PROOF_001_REPRODUCED_PACKAGING_CANDIDATE_NOT_ADMITTED"


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def add(findings: list[dict[str, str]], code: str, detail: str, path: Path) -> None:
    findings.append({"code": code, "detail": detail, "path": path.as_posix()})


def verify(root: Path, run_wrapper: bool = True) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for relative in (ADMISSION, STANDING, MANIFEST, INDEX, WRAPPER):
        target = root / relative
        if target.is_symlink() or not target.is_file():
            add(findings, "REQUIRED_FILE_MISSING_OR_UNSAFE", "regular file required", relative)
    if findings:
        return findings

    try:
        admission = load(root / ADMISSION)
        standing = load(root / STANDING)
        manifest = load(root / MANIFEST)
        index = load(root / INDEX)
    except Exception as exc:
        add(findings, "STRICT_JSON_INVALID", str(exc), ADMISSION)
        return findings

    package = admission.get("preserved_package", {})
    verification = admission.get("deterministic_verification", {})
    exterior = admission.get("exterior_recomputation", {})
    claim = admission.get("admitted_claim", {})
    effect = admission.get("admission_effect", {})
    admission_ok = (
        admission.get("schema_version") == "v0.1"
        and admission.get("record_kind") == "fork_public_proof_admission"
        and admission.get("proof_id") == "PROOF-001"
        and admission.get("status") == "ADMISSION_CANDIDATE_REVIEWED_MERGE_REQUIRED"
        and admission.get("governed_line", {}).get("predecessor_tip") == "85448bee5b78396bae58e4f270b12990547edb02"
        and admission.get("governed_line", {}).get("proof_packaging_merge_commit") == "ded38bf56f950b8813614132c92bf531553a8b34"
        and package.get("packaging_standing") == "BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED"
        and package.get("wrapper_result") == EXPECTED_WRAPPER_RESULT
        and package.get("package_bytes_rewritten") is False
        and verification.get("mutation_case") == "FLR-ADV-003"
        and verification.get("mutation_expected_result") == "CURRENT_HEAD_REVIEW_STALE"
        and exterior.get("disposition") == "REPRODUCED_WITH_CORRECTION_REQUIRED"
        and exterior.get("independence_claim") == "EXTERIOR_RECOMPUTATION_EVIDENCE_NOT_UNQUALIFIED_INDEPENDENT_AUTHORITY"
        and exterior.get("correction_retained") == "ORIGINAL_PUBLIC_TEST_COUNT_NOT_REPRODUCED"
        and claim.get("scope") == "EXACT_BOUND_REPLAY_INTERVAL_AND_FLR_ADV_003_ONLY"
        and claim.get("standing_on_reviewed_merge") == "ADMITTED_BOUNDED_PUBLIC_PROOF_SLICE_WITH_CORRECTION_REQUIRED_RETAINED"
        and claim.get("generalization_outside_scope") == "NONE"
        and effect.get("effective_only_on_reviewed_merge_to_governed_branch") is True
        and effect.get("source_evidence_admitted") is True
        and effect.get("deterministic_verifier_admitted") is True
        and effect.get("mutation_failure_admitted") is True
        and effect.get("exterior_receipt_admitted_with_correction_retained") is True
        and effect.get("limitations_admitted") is True
        and effect.get("wider_proof_portfolio_admitted") is False
        and effect.get("authority_delta") == "NONE"
        and effect.get("execution_effect") == "NONE"
        and effect.get("provider_calls") == 0
        and effect.get("pair_001_calls") == 0
    )
    if not admission_ok:
        add(findings, "PROOF_ADMISSION_SEMANTICS_INVALID", "bounded admission contract violated", ADMISSION)

    if standing.get("packaging_candidate", {}).get("standing") != "BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED":
        add(findings, "ORIGINAL_PACKAGING_STANDING_REWRITTEN", "original packaging standing must remain unchanged", STANDING)
    if standing.get("exterior_recomputation", {}).get("disposition") != "REPRODUCED_WITH_CORRECTION_REQUIRED":
        add(findings, "EXTERIOR_CORRECTION_LOST", "correction-bearing disposition must remain visible", STANDING)

    bindings = manifest.get("bindings")
    roles = {item.get("role") for item in bindings if isinstance(item, dict)} if isinstance(bindings, list) else set()
    required_roles = {
        "PR91_SOURCE_EXTERIOR_RETURN",
        "PR91_NORMALIZED_EXTERIOR_RETURN",
        "PROOF_001_TESTS",
        "PROOF_001_ONE_COMMAND_WRAPPER",
        "UNDERLYING_REPLAY_CHECKER",
        "UNDERLYING_ADVERSARIAL_REGISTER",
        "PROOF_001_HUMAN_ROUTE",
        "PROOF_001_STANDING_RECORD",
    }
    if not required_roles.issubset(roles):
        add(findings, "PROOF_MANIFEST_REQUIRED_ROLE_MISSING", f"missing={sorted(required_roles - roles)}", MANIFEST)

    proofs = index.get("proofs")
    entry = proofs[0] if isinstance(proofs, list) and len(proofs) == 1 and isinstance(proofs[0], dict) else {}
    if not (
        entry.get("proof_id") == "PROOF-001"
        and entry.get("admission_path") == ADMISSION.as_posix()
        and entry.get("admission_standing_on_reviewed_merge") == "ADMITTED_BOUNDED_PUBLIC_PROOF_SLICE_WITH_CORRECTION_REQUIRED_RETAINED"
        and entry.get("wider_portfolio_admitted") is False
        and entry.get("expected_result") == EXPECTED_WRAPPER_RESULT
    ):
        add(findings, "PROOF_INDEX_ADMISSION_ROUTE_INVALID", "index does not expose bounded admission successor", INDEX)

    if run_wrapper and not findings:
        completed = subprocess.run(
            [sys.executable, str(root / WRAPPER)],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if completed.returncode != 0 or EXPECTED_WRAPPER_RESULT not in completed.stdout:
            add(findings, "PROOF_WRAPPER_RECOMPUTATION_FAILED", completed.stderr[-1000:] or completed.stdout[-1000:], WRAPPER)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--skip-wrapper", action="store_true")
    args = parser.parse_args()
    findings = verify(args.repo_root.resolve(), run_wrapper=not args.skip_wrapper)
    print(json.dumps({
        "checker_id": CHECKER_ID,
        "result": "PROOF_001_ADMISSION_CANDIDATE_CONFORMS_NOT_ADMITTED" if not findings else "NONCONFORMING",
        "findings": findings,
        "non_effects": {"provider_calls": 0, "pair_001_calls": 0, "admission": "NONE_BY_CHECKER"},
    }, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
