#!/usr/bin/env python3
"""Recompute the Fork thesis-manifestation candidate from its exact evidence base."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from typing import Any

BASE_COMMIT = "1241c0084900f2c60f362205525464582e57b4a7"
CANDIDATE_ID = "FTM-CANDIDATE-2026-07-22-001"
CANDIDATE_DIR = Path("docs/research/fork-thesis-manifestation-v0.1")

EXPECTED_EVIDENCE_ROLES = {
    "README.md": "DECLARED_RESEARCH_HYPOTHESIS_AND_NON_CLAIMS",
    "docs/preservation/FORK_PRESERVATION_INTEGRITY_DOCTRINE_v0_1.md": "HISTORICAL_STATE_AND_CURRENT_PROJECTION_SEPARATION",
    "docs/preservation/failure-mode-archive-v0.1/incidents/FORK-INC-2026-07-13-001/CLAIM_CONSUMPTION_FAILURE_CLASSIFICATION_v0_1.json": "PRESERVED_CLAIM_CONSUMPTION_FAILURE",
    "docs/preservation/CONSUMER_OWNED_CLAIM_ADMISSION_CONTROL_v0_1.md": "PRODUCER_CLAIM_AND_CONSUMER_STANDING_SEPARATION",
    "docs/verification/INDEPENDENT_VERIFICATION_SURFACE_v0_1.md": "VERIFICATION_WITHOUT_CLAIM_CODE_OR_AUTHORITY_INHERITANCE",
    "docs/preservation/admission/FORK_PRESERVATION_ADMISSION_ANCHOR_2026_07_18_v0_1.json": "SUCCESSOR_CONFERRED_PRESERVATION_STANDING",
    "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PRE_EXECUTION_BINDING_v0_1_2.json": "STRUCTURAL_READINESS_AND_EXECUTION_AUTHORITY_SEPARATION",
    "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PROVIDER_VALIDATION_REQUEST_v0_1_2.json": "FAILED_DIAGNOSTICS_EXCLUDED_FROM_EXPERIMENT_REPETITIONS",
    "docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/DEEPSEEK_RECEIVER_DRIFT_CLASSIFICATION_CONTRACT_v0_1_3.json": "OBSERVATION_CAUSE_AND_AUTHORIZATION_SEPARATION",
    "docs/sequence-surface/FORK_SEQUENCE_SURFACE_v0_1.md": "ORDERED_STANDING_TRANSITIONS_AS_INSPECTION_SUBJECT",
    "docs/sequence-surface/PAIR_001_SEQUENCE_LEDGER_v0_1.json": "APPEND_ONLY_LONGITUDINAL_EVENT_LINEAGE",
    "docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json": "DETERMINISTIC_CURRENT_STANDING_PROJECTION",
    "docs/sequence-surface/PAIR_001_SEQUENCE_TRANSITION_CONTRACT_v0_1.json": "EVIDENCE_AUTHORITY_AND_STOPPING_TRANSITION_CONTRACT",
    "docs/preservation/root-checksum-integrity-v0.1/ROOT_CHECKSUM_DISCREPANCY_RECORD_v0_1.json": "PROSPECTIVE_REPAIR_WITHOUT_RETROACTIVE_CI_PROMOTION",
    "docs/preservation/admission/FORK_SEQUENCE_INTEGRITY_ADMISSION_ANCHOR_2026_07_19_v0_1.json": "SUCCESSOR_CONFERRED_SEQUENCE_AND_INTEGRITY_STANDING"
}
EXPECTED_DIMENSIONS = (
    "artifact_state",
    "verification_state",
    "review_state",
    "admission_state",
    "authority_state",
    "execution_state",
    "unresolved_state",
    "temporal_closure",
)
EXPECTED_CLAIM_CATEGORIES = {
    "OBSERVED": {"FTM-C001", "FTM-C002", "FTM-C003", "FTM-C004", "FTM-C005", "FTM-C006", "FTM-C007", "FTM-C008", "FTM-C009", "FTM-C010", "FTM-C011"},
    "REPOSITORY_SUPPORTED_INFERENCE": {"FTM-I001", "FTM-I002", "FTM-I003", "FTM-I004"},
    "UNRESOLVED": {"FTM-U001", "FTM-U002", "FTM-U003", "FTM-U004"},
    "NOT_CLAIMED": {"FTM-N001", "FTM-N002", "FTM-N003", "FTM-N004", "FTM-N005"},
}
EXPECTED_PACKAGE_PATHS = {
    "docs/research/fork-thesis-manifestation-v0.1/README.md",
    "docs/research/fork-thesis-manifestation-v0.1/BASE_COORDINATE_v0_1.json",
    "docs/research/fork-thesis-manifestation-v0.1/THESIS_MANIFESTATION_RECORD_v0_1.json",
    "docs/research/fork-thesis-manifestation-v0.1/EVIDENCE_MAP_v0_1.json",
    "docs/research/fork-thesis-manifestation-v0.1/CLAIM_LEDGER_v0_1.json",
    "docs/research/fork-thesis-manifestation-v0.1/ALTERNATIVE_INTERPRETATIONS_AND_FALSIFIERS_v0_1.md",
    "docs/research/fork-thesis-manifestation-v0.1/NO_ADMISSION_OR_EXECUTION_EFFECT_v0_1.json",
    "tools/check_fork_thesis_manifestation_v0_1.py",
    "tests/test_fork_thesis_manifestation_v0_1.py",
}


class DuplicateKeyError(ValueError):
    pass


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=_object_no_duplicates,
            parse_constant=_reject_constant,
        )
    _assert_finite(value)
    return value


def _assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for item in value.values():
            _assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            _assert_finite(item)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def safe_regular_file(root: Path, rel: str) -> Path:
    pure = PurePosixPath(rel)
    if not rel or pure.is_absolute() or ".." in pure.parts or "\\" in rel:
        raise ValueError(f"unsafe repository-relative path: {rel!r}")
    path = root.joinpath(*pure.parts)
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {rel}")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"not a regular file: {rel}")
    path.resolve(strict=True).relative_to(root_real)
    return path


def expect(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def expect_equal(errors: list[str], actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        errors.append(f"{label}: expected {expected!r}, found {actual!r}")


def check(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    def read_json(rel: str) -> Any:
        try:
            return load_json(safe_regular_file(root, rel))
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            return {}

    base = read_json(f"{CANDIDATE_DIR.as_posix()}/BASE_COORDINATE_v0_1.json")
    evidence_map = read_json(f"{CANDIDATE_DIR.as_posix()}/EVIDENCE_MAP_v0_1.json")
    record = read_json(f"{CANDIDATE_DIR.as_posix()}/THESIS_MANIFESTATION_RECORD_v0_1.json")
    claims = read_json(f"{CANDIDATE_DIR.as_posix()}/CLAIM_LEDGER_v0_1.json")
    no_effect = read_json(f"{CANDIDATE_DIR.as_posix()}/NO_ADMISSION_OR_EXECUTION_EFFECT_v0_1.json")
    manifest = read_json(f"{CANDIDATE_DIR.as_posix()}/PACKAGE_MANIFEST_v0_1.json")

    expect_equal(errors, base.get("candidate_id"), CANDIDATE_ID, "base candidate_id")
    expect_equal(errors, base.get("status"), "RESEARCH_SYNTHESIS_CANDIDATE_NOT_ADMITTED", "base status")
    expect_equal(errors, base.get("exact_base", {}).get("commit_sha"), BASE_COMMIT, "base commit")
    expect_equal(errors, base.get("exact_base", {}).get("binding_kind"), "EXACT_IMMUTABLE_GIT_COMMIT", "base binding kind")
    for field in ("main_ref_effect", "pair_001_effect", "existing_pull_request_effect", "admission_effect", "execution_effect"):
        expect_equal(errors, base.get("construction_scope", {}).get(field), "NONE", f"base construction_scope.{field}")
    expect_equal(errors, base.get("construction_scope", {}).get("source_evidence_mutation"), False, "source evidence mutation")
    expect_equal(errors, base.get("temporal_posture", {}).get("later_repository_state_inherited"), False, "later state inheritance")
    expect_equal(errors, base.get("temporal_posture", {}).get("open_pull_request_state_used_as_evidence"), False, "open PR evidence")

    expect_equal(errors, evidence_map.get("candidate_id"), CANDIDATE_ID, "evidence map candidate_id")
    expect_equal(errors, evidence_map.get("source_commit"), BASE_COMMIT, "evidence map source commit")
    mapped_entries = evidence_map.get("entries", [])
    expect(errors, isinstance(mapped_entries, list), "evidence map entries must be a list")
    by_path: dict[str, dict[str, Any]] = {}
    evidence_ids: set[str] = set()
    if isinstance(mapped_entries, list):
        for index, entry in enumerate(mapped_entries):
            if not isinstance(entry, dict):
                errors.append(f"evidence entry {index} is not an object")
                continue
            rel = entry.get("path")
            evidence_id = entry.get("evidence_id")
            if not isinstance(rel, str):
                errors.append(f"evidence entry {index} has no string path")
                continue
            if rel in by_path:
                errors.append(f"duplicate evidence path: {rel}")
            by_path[rel] = entry
            if not isinstance(evidence_id, str) or evidence_id in evidence_ids:
                errors.append(f"invalid or duplicate evidence_id at {rel}: {evidence_id!r}")
            else:
                evidence_ids.add(evidence_id)
    expect_equal(errors, set(by_path), set(EXPECTED_EVIDENCE_ROLES), "evidence path set")
    expect_equal(errors, len(evidence_ids), 15, "evidence id count")
    for rel, role in EXPECTED_EVIDENCE_ROLES.items():
        entry = by_path.get(rel, {})
        expect_equal(errors, entry.get("role"), role, f"{rel} role")
        expect_equal(errors, entry.get("source_commit"), BASE_COMMIT, f"{rel} source commit")
        try:
            data = safe_regular_file(root, rel).read_bytes()
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            continue
        expect_equal(errors, entry.get("size_bytes"), len(data), f"{rel} size")
        expect_equal(errors, entry.get("sha256"), sha256_bytes(data), f"{rel} sha256")
        expect_equal(errors, entry.get("git_blob_sha1"), git_blob_sha1(data), f"{rel} git blob sha1")

    def text(rel: str) -> str:
        try:
            return safe_regular_file(root, rel).read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            return ""

    root_readme = text("README.md")
    expect(errors, "not a proven general systems theory" in root_readme, "root README must preserve the general-theory non-claim")
    expect(errors, "E[U | H = 1] < E[U | H = 0]" in root_readme, "root README must preserve the declared causal hypothesis")
    expect(errors, "preservation without inheritance" in root_readme, "root README must preserve the governing constraint")

    doctrine = text("docs/preservation/FORK_PRESERVATION_INTEGRITY_DOCTRINE_v0_1.md")
    expect(errors, "Historical rewrite authority:** `NONE`" in doctrine, "preservation doctrine historical rewrite authority")
    expect(errors, "original state, incident state, later corrective state, and current projection remain distinct" in doctrine, "preservation temporal distinction")
    expect(errors, "Those claims do not establish repository standing" in doctrine, "producer claim standing distinction")

    control = text("docs/preservation/CONSUMER_OWNED_CLAIM_ADMISSION_CONTROL_v0_1.md")
    expect(errors, "separates a producer's representation" in control and "repository consumer" in control, "consumer-owned claim separation")

    ivs = text("docs/verification/INDEPENDENT_VERIFICATION_SURFACE_v0_1.md")
    for result in ("VERIFIED_WITHIN_DECLARED_SCOPE", "INVALIDATED_BY_RECOMPUTATION", "INCONCLUSIVE_EVIDENCE_GAP"):
        expect(errors, result in ivs, f"independent verification result missing: {result}")
    expect(errors, "without inheriting the contribution's claims, code, hooks, dependency declarations, workflows, or authority" in ivs, "verification non-inheritance")
    expect(errors, "does not approve a merge, grant repository standing" in ivs, "verification authority boundary")

    sequence_doc = text("docs/sequence-surface/FORK_SEQUENCE_SURFACE_v0_1.md")
    expect(errors, "The sequence itself is the inspection subject" in sequence_doc, "sequence inspection subject")
    expect(errors, "not represented as an admitted seventh surface" in sequence_doc, "sequence seventh-surface non-claim")
    expect(errors, "It may not schedule the successor, satisfy the requirement, create authority" in sequence_doc, "declared successor authority distinction")

    incident = read_json("docs/preservation/failure-mode-archive-v0.1/incidents/FORK-INC-2026-07-13-001/CLAIM_CONSUMPTION_FAILURE_CLASSIFICATION_v0_1.json")
    for field, expected in {
        "failure_class_id": "CCF-001_AI_CHANGE_READINESS_PROMOTION",
        "classification_status": "CONFIRMED_FROM_REPOSITORY_EVIDENCE",
        "consumer_owned_verification_state_at_admission": "INSUFFICIENT_TO_DETECT_INVALID_WORKFLOW_STRUCTURE",
        "governance_defect": "PRODUCER_CLAIM_CONSUMED_WITHOUT_TRUSTED_BASE_VERIFICATION",
        "intent": "NOT_EVALUATED",
        "authority_effect": "NONE",
    }.items():
        expect_equal(errors, incident.get(field), expected, f"incident.{field}")

    binding = read_json("docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PRE_EXECUTION_BINDING_v0_1_2.json")
    expect_equal(errors, binding.get("status"), "STRUCTURALLY_READY_EXECUTION_BLOCKED", "pre-execution status")
    expect_equal(errors, binding.get("provider_execution_permitted"), False, "pre-execution provider permission")

    provider = read_json("docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/PROVIDER_VALIDATION_REQUEST_v0_1_2.json")
    expect_equal(errors, provider.get("status"), "BLOCKED_PROVIDER_VALIDATION_FAILED", "provider-validation status")
    expect_equal(errors, provider.get("execution_boundary", {}).get("provider_validation_calls_performed"), 6, "provider-validation calls")
    expect_equal(errors, provider.get("execution_boundary", {}).get("pair_001_calls_performed"), 0, "provider-validation Pair-001 calls")
    expect_equal(errors, provider.get("execution_boundary", {}).get("pair_001_execution_effect"), "NONE", "provider-validation Pair-001 effect")

    drift = read_json("docs/experiments/cross-system-claim-handoff-v0.1/pre-execution/DEEPSEEK_RECEIVER_DRIFT_CLASSIFICATION_CONTRACT_v0_1_3.json")
    expect_equal(errors, drift.get("cause"), "UNRESOLVED", "drift cause")
    expect_equal(errors, drift.get("status"), "CLASSIFIED_RETRY_NOT_AUTHORIZED", "drift status")
    expect_equal(errors, drift.get("precommitted_stopping_rule", {}).get("authorization", {}).get("present"), False, "retry authorization present")
    expect_equal(errors, drift.get("execution_boundary", {}).get("pair_001_execution_effect"), "NONE", "drift Pair-001 effect")

    projection = read_json("docs/sequence-surface/PAIR_001_SEQUENCE_PROJECTION_v0_1.json")
    expect_equal(errors, projection.get("status"), "CANDIDATE_NOT_ADMITTED", "sequence projection artifact-local status")
    expect_equal(errors, projection.get("sequence", {}).get("current_state"), "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED", "sequence current state")
    expect_equal(errors, projection.get("sequence", {}).get("currently_eligible_successor_transition_ids"), [], "eligible successors")
    expect_equal(errors, projection.get("sequence", {}).get("declared_successor_transition_ids"), ["FSS-PAIR001-T012"], "declared successors")
    for field, expected in {
        "provider_calls": 8,
        "pair_001_original_attempts": 2,
        "provider_validation_calls": 6,
        "pair_001_repetitions": 0,
    }.items():
        expect_equal(errors, projection.get("observed_history", {}).get(field), expected, f"projection history.{field}")
    expect_equal(errors, projection.get("retry", {}).get("authorization_present"), False, "projection retry authorization")
    expect_equal(errors, projection.get("execution_boundary", {}).get("pair_001_execution_permitted"), False, "projection Pair-001 permission")

    contract = read_json("docs/sequence-surface/PAIR_001_SEQUENCE_TRANSITION_CONTRACT_v0_1.json")
    expect_equal(errors, len(contract.get("transitions", [])), 19, "sequence transition count")
    forbidden = contract.get("forbidden_promotions", [])
    expect(errors, any("publication, review, elapsed time" in item for item in forbidden if isinstance(item, str)), "forbidden publication/review/time authority promotion")
    expect(errors, any("diagnostic event" in item and "Pair-001 repetition" in item for item in forbidden if isinstance(item, str)), "forbidden diagnostic repetition promotion")
    expect_equal(errors, contract.get("anchor_boundary", {}).get("pair_001_execution_effect"), "NONE", "transition contract Pair-001 effect")

    discrepancy = read_json("docs/preservation/root-checksum-integrity-v0.1/ROOT_CHECKSUM_DISCREPANCY_RECORD_v0_1.json")
    expect_equal(errors, discrepancy.get("append_only"), True, "checksum discrepancy append-only")
    expect_equal(errors, discrepancy.get("prior_ci_evaluation_gap", {}).get("status"), "NOT_EVALUATED_BY_PRIOR_GREEN_RUNS", "prior green scope gap")
    expect_equal(errors, discrepancy.get("experiment_boundary", {}).get("pair_001_execution_effect"), "NONE", "checksum discrepancy Pair-001 effect")

    anchor = read_json("docs/preservation/admission/FORK_SEQUENCE_INTEGRITY_ADMISSION_ANCHOR_2026_07_19_v0_1.json")
    admission = anchor.get("admission_effect_if_merged", {})
    expect_equal(errors, admission.get("standing"), "ADMITTED_TO_PRESERVATION_LINEAGE", "successor anchor standing")
    expect_equal(errors, admission.get("sequence_surface_standing"), "ADMITTED_CROSS_SURFACE_INSPECTABILITY_PROJECTION_NOT_MODULAR_SURFACE", "sequence successor standing")
    expect_equal(errors, admission.get("does_not_authorize_provider_calls"), True, "anchor provider-call non-effect")
    expect_equal(errors, admission.get("does_not_execute_pair_001"), True, "anchor Pair-001 non-effect")
    expect_equal(errors, anchor.get("current_state_projection", {}).get("pair_001_repetitions"), 0, "anchor Pair-001 repetitions")
    expect_equal(errors, anchor.get("current_state_projection", {}).get("uppercase_retry_authorization_present"), False, "anchor retry authorization")

    expect_equal(errors, record.get("candidate_id"), CANDIDATE_ID, "thesis record candidate_id")
    expect_equal(errors, record.get("status"), "RESEARCH_SYNTHESIS_CANDIDATE_NOT_ADMITTED", "thesis record status")
    thesis = record.get("manifested_thesis", {})
    expect_equal(errors, thesis.get("compact_form"), "EVIDENTIARY_STANDING_IS_VECTOR_VALUED_LONGITUDINAL_RECOMPUTABLE_AND_NON_INHERITING", "thesis compact form")
    expect_equal(errors, thesis.get("mechanism"), "RECOMPUTABLE_EVIDENCE", "thesis mechanism")
    expect_equal(errors, thesis.get("object"), "VECTOR_VALUED_LONGITUDINAL_EVIDENTIARY_STANDING", "thesis object")
    expect_equal(errors, thesis.get("governing_constraint"), "PRESERVATION_WITHOUT_INHERITANCE", "thesis constraint")
    expect_equal(errors, thesis.get("operative_unit"), "EVIDENCE_BOUND_STANDING_TRANSITION", "thesis operative unit")
    expect_equal(errors, record.get("architectural_inference", {}).get("status"), "REPOSITORY_SUPPORTED_INFERENCE_NOT_CAUSAL_PROOF", "architectural inference status")
    expect_equal(errors, record.get("causal_hypothesis", {}).get("status"), "UNRESOLVED_NOT_ESTABLISHED_TO_DECLARED_GENERALITY", "causal hypothesis status")
    expect_equal(errors, record.get("causal_hypothesis", {}).get("expression"), "E[U | H = 1] < E[U | H = 0]", "causal hypothesis expression")
    dimensions = tuple(item.get("dimension") for item in record.get("standing_vector_dimensions", []) if isinstance(item, dict))
    expect_equal(errors, dimensions, EXPECTED_DIMENSIONS, "standing vector dimensions")
    expect_equal(errors, record.get("surface_posture", {}).get("seventh_modular_surface_claimed"), False, "seventh surface claim")
    expect_equal(errors, record.get("surface_posture", {}).get("canonical_theory_claimed"), False, "canonical theory claim")
    expected_effects = {
        "main_ref": "NONE",
        "pair_001": "NONE",
        "provider_calls": 0,
        "pair_001_repetitions": 0,
        "readiness": "NONE",
        "retry_authorization": "NONE",
        "execution_authority": "NONE",
        "admission": "NONE",
        "existing_pull_requests": "NONE",
    }
    expect_equal(errors, record.get("effects"), expected_effects, "thesis record effects")

    expect_equal(errors, claims.get("candidate_id"), CANDIDATE_ID, "claim ledger candidate_id")
    actual_categories: dict[str, set[str]] = {key: set() for key in EXPECTED_CLAIM_CATEGORIES}
    seen_claims: set[str] = set()
    for index, claim in enumerate(claims.get("claims", [])):
        if not isinstance(claim, dict):
            errors.append(f"claim {index} is not an object")
            continue
        claim_id = claim.get("claim_id")
        category = claim.get("category")
        if not isinstance(claim_id, str) or claim_id in seen_claims:
            errors.append(f"invalid or duplicate claim id: {claim_id!r}")
            continue
        seen_claims.add(claim_id)
        if category not in actual_categories:
            errors.append(f"{claim_id}: invalid category {category!r}")
        else:
            actual_categories[category].add(claim_id)
        refs = claim.get("evidence_ids")
        expect(errors, isinstance(refs, list) and bool(refs), f"{claim_id}: evidence_ids must be a non-empty list")
        if isinstance(refs, list):
            unknown = set(refs) - evidence_ids
            expect(errors, not unknown, f"{claim_id}: unknown evidence ids {sorted(unknown)}")
        expect(errors, isinstance(claim.get("statement"), str) and bool(claim.get("statement")), f"{claim_id}: missing statement")
        expect(errors, isinstance(claim.get("boundary"), str) and bool(claim.get("boundary")), f"{claim_id}: missing boundary")
    expect_equal(errors, actual_categories, EXPECTED_CLAIM_CATEGORIES, "claim category membership")
    expect_equal(errors, claims.get("effects"), {"repository_admission": "NONE", "experiment": "NONE", "pair_001": "NONE", "authority": "NONE"}, "claim ledger effects")

    expect_equal(errors, no_effect.get("candidate_id"), CANDIDATE_ID, "no-effect candidate_id")
    repo_effects = no_effect.get("repository_effects", {})
    for field in ("main_ref_mutated", "preservation_base_ref_mutated", "existing_pull_requests_mutated", "existing_pull_request_comments_added", "existing_branch_deleted_or_force_updated"):
        expect_equal(errors, repo_effects.get(field), False, f"no-effect repository.{field}")
    expect_equal(errors, repo_effects.get("admission_or_merge_effect"), "NONE", "no-effect admission")
    pair_effects = no_effect.get("pair_001_effects", {})
    for field in ("provider_calls_performed", "provider_validation_attempts_added", "pair_001_calls_performed", "pair_001_repetitions_added"):
        expect_equal(errors, pair_effects.get(field), 0, f"no-effect Pair-001.{field}")
    for field in ("readiness_effect", "retry_authorization_effect", "execution_effect", "state_transition_effect"):
        expect_equal(errors, pair_effects.get(field), "NONE", f"no-effect Pair-001.{field}")
    expect_equal(errors, no_effect.get("research_effects", {}).get("causal_hypothesis_promoted_to_fact"), False, "causal promotion non-effect")
    expect_equal(errors, no_effect.get("research_effects", {}).get("seventh_modular_surface_created"), False, "seventh surface non-effect")
    expect_equal(errors, no_effect.get("research_effects", {}).get("canonical_theory_admitted"), False, "canonical theory non-effect")

    expect_equal(errors, manifest.get("candidate_id"), CANDIDATE_ID, "manifest candidate_id")
    expect_equal(errors, manifest.get("source_commit"), BASE_COMMIT, "manifest source commit")
    expect_equal(errors, manifest.get("self_exclusion", {}).get("path"), f"{CANDIDATE_DIR.as_posix()}/PACKAGE_MANIFEST_v0_1.json", "manifest self exclusion")
    manifest_entries = manifest.get("entries", [])
    by_manifest_path: dict[str, dict[str, Any]] = {}
    if isinstance(manifest_entries, list):
        for entry in manifest_entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                errors.append("invalid package manifest entry")
                continue
            rel = entry["path"]
            if rel in by_manifest_path:
                errors.append(f"duplicate package manifest path: {rel}")
            by_manifest_path[rel] = entry
    else:
        errors.append("package manifest entries must be a list")
    expect_equal(errors, set(by_manifest_path), EXPECTED_PACKAGE_PATHS, "package manifest path set")
    for rel, entry in by_manifest_path.items():
        try:
            data = safe_regular_file(root, rel).read_bytes()
        except Exception as exc:
            errors.append(f"{rel}: {exc}")
            continue
        expect_equal(errors, entry.get("size_bytes"), len(data), f"package {rel} size")
        expect_equal(errors, entry.get("sha256"), sha256_bytes(data), f"package {rel} sha256")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors = check(args.repo_root)
    payload = {
        "checker": "fork_thesis_manifestation_v0_1",
        "candidate_id": CANDIDATE_ID,
        "base_commit": BASE_COMMIT,
        "status": "THESIS_MANIFESTATION_CANDIDATE_CONFORMS" if not errors else "THESIS_MANIFESTATION_CANDIDATE_INVALID",
        "finding_count": len(errors),
        "findings": errors,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif errors:
        print(payload["status"])
        for error in errors:
            print(f"- {error}")
    else:
        print(payload["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
