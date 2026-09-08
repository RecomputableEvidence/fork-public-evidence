#!/usr/bin/env python3
"""Validate the bounded 2026-08-05 open-candidate coordinate snapshot."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path, PurePosixPath
import stat
from typing import Any


CHECKER_ID = "FORK_OPEN_CANDIDATE_COORDINATE_SNAPSHOT_CHECKER_v0_1"
SNAPSHOT = Path(
    "docs/preservation/open-candidates/2026-08-05/"
    "OPEN_CANDIDATE_STANDING_SNAPSHOT_v0_1.json"
)
CONFORMING_RESULT = "OPEN_CANDIDATE_COORDINATE_SNAPSHOT_CANDIDATE_CONFORMS_NOT_ADMITTED"
EXPECTED_GOVERNED_SHA = "1ae03971c680e361d2d81cefc8319dfccb50d8d3"
EXPECTED_OBSERVED_AT_UTC = "2026-08-05T21:59:59Z"
EXPECTED_CANDIDATE_STANDING = "OPEN_CANDIDATE_COORDINATE_SNAPSHOT_CANDIDATE_NOT_ADMITTED"
EXPECTED_MERGE_STANDING = "OPEN_CANDIDATE_COORDINATE_SNAPSHOT_ADMITTED_NO_SOURCE_PR_EFFECT"

EXPECTED_PRS = {
    65: {
        "title": "fix(day0): close ADV_003 inventory and packet-root gaps",
        "lane_id": "FOUNDATIONAL_CORRECTION",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": "599d3e193d86a9661fbbec3213ae1921b4959f10",
        "head_branch": "fix/day0-adv-003-inventory-v0-1-1",
        "head_sha": "479de5f929cb37377ccba5ef93f7a4f7b93e1120",
        "declared_standing": "DRAFT_CORRECTED_HEAD_RECOMPUTATION_PENDING_NOT_MERGE_AUTHORIZED",
        "snapshot_classification": "FOUNDATIONAL_CORRECTION_EXACT_HEAD_RECOMPUTATION_REQUIRED",
        "recommended_disposition": "FREEZE_EXACT_HEAD_RECOMPUTE_AND_INTEGRATE_THROUGH_CURRENT_TIP_SUCCESSOR",
    },
    84: {
        "title": "docs(meta-evidence): add conversational authority drift candidate v0.1",
        "lane_id": "META_EVIDENCE_RESEARCH",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": "1241c0084900f2c60f362205525464582e57b4a7",
        "head_branch": "research/conversational-authority-drift-v0-1",
        "head_sha": "46fcd2c2580abd86ffbe215e6c387fee2bcb1b39",
        "declared_standing": None,
        "snapshot_classification": "DRAFT_RESEARCH_PROTOCOL_AND_CANDIDATE_CASE_EXACT_HEAD_EXTERIOR_REVIEW_REQUIRED_NOT_ADMITTED",
        "recommended_disposition": "PRESERVE_FROZEN_HEAD_REVIEW_THEN_CURRENT_TIP_IMPORT",
    },
    86: {
        "title": "docs(meta-evidence): add CAD candidate meta-assessment supplement 001",
        "lane_id": "META_EVIDENCE_RESEARCH",
        "mergeable_observed": True,
        "base_branch": "research/conversational-authority-drift-v0-1",
        "base_sha": "46fcd2c2580abd86ffbe215e6c387fee2bcb1b39",
        "head_branch": "research/conversational-authority-drift-meta-assessment-supplement-001",
        "head_sha": "f72ca3fad82bee068527fe63eaf1c8eba87dd698",
        "declared_standing": "DRAFT_COMPANION_REVIEW_PENDING_NOT_MERGE_AUTHORIZED",
        "snapshot_classification": "STACKED_ASSESSOR_CORRECTION_SUPPLEMENT_PARENT_PR84_REQUIRED",
        "recommended_disposition": "PROCESS_ONLY_AFTER_PR84_REVIEW_AND_CURRENT_TIP_IMPORT",
    },
    100: {
        "title": "feat(interop): add governed handoff cadence harness v0.1",
        "lane_id": "INTEROPERABILITY_EXPERIMENT",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0",
        "head_branch": "experiment/governed-handoff-cadence-v0-1",
        "head_sha": "cdb757a97c2e554cf3df822e4764ac51122ca8eb",
        "declared_standing": "DETERMINISTIC_SIMULATION_CANDIDATE_NOT_ADMITTED",
        "snapshot_classification": "DETERMINISTIC_SIMULATION_EXACT_HEAD_EXTERIOR_RECOMPUTATION_REQUIRED",
        "recommended_disposition": "EXACT_HEAD_EXTERIOR_RECOMPUTATION_THEN_SEPARATE_SIMULATION_ADMISSION",
    },
    105: {
        "title": "docs(verification): preserve Shayne PR #64 recomputation and release bundle",
        "lane_id": "EXTERIOR_EVIDENCE",
        "mergeable_observed": False,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": "cda8c68fd6a930c327b04bcbe72088c4fabd72fd",
        "head_branch": "agent/shayne-pr64-macos-recomputation-v0-1",
        "head_sha": "b5c9d12109055a258b5ef33dac48f4f504b0a212",
        "declared_standing": None,
        "snapshot_classification": "EXTERIOR_RECOMPUTATION_RECORD_AND_TEMPORAL_ATTACHMENT_SUCCESSOR_NOT_ADMITTED",
        "recommended_disposition": "EVIDENCE_ONLY_CURRENT_TIP_SUCCESSOR_WITHOUT_REOPENING_PROOF001",
    },
    106: {
        "title": "feat(proofs): govern sequenced proof portfolio v0.1",
        "lane_id": "PROOF_GOVERNANCE",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": "cda8c68fd6a930c327b04bcbe72088c4fabd72fd",
        "head_branch": "agent/proof-portfolio-sequence-v0-1",
        "head_sha": "1038be6cf56d2b6ed74d2bee888c38cdd6fd0f92",
        "declared_standing": "PROOF_PORTFOLIO_DEVELOPMENT_SEQUENCE_CANDIDATE_NOT_ADMITTED",
        "snapshot_classification": "HISTORICALLY_VALID_V0_1_TEMPORALLY_STALE_FOR_CURRENT_RELIANCE",
        "recommended_disposition": "PRESERVE_V0_1_AND_REPLACE_WITH_TEMPORALLY_CURRENT_V0_2_SUCCESSOR",
    },
    110: {
        "title": "docs(pre-pilot): publish Stage 1 exterior recomputation delivery packet",
        "lane_id": "PRE_PILOT_IMPLEMENTATION",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": EXPECTED_GOVERNED_SHA,
        "head_branch": "agent/complementary-evidence-sidecar-stage-1-exterior-recompute-v0-1",
        "head_sha": "c6cd61270bac4938878df06f0085089c8f61b9dc",
        "declared_standing": "EXTERIOR_RECOMPUTATION_DELIVERY_PACKET_CANDIDATE_NOT_ADMITTED_NOT_MERGE_AUTHORIZED",
        "snapshot_classification": "STAGE1_PREDECESSOR_DELIVERY_PACKET_EXTERIOR_RECOMPUTATION_REQUIRED",
        "recommended_disposition": "EXTERIOR_RECOMPUTE_AS_STAGE1_PREDECESSOR_PACKET",
    },
    111: {
        "title": "feat(pilot): add computable Fork pilot prerequisite candidate",
        "lane_id": "PRE_PILOT_IMPLEMENTATION",
        "mergeable_observed": True,
        "base_branch": "preservation/clean-continuance-v0.1",
        "base_sha": EXPECTED_GOVERNED_SHA,
        "head_branch": "agent/fork-pilot-deployment-prerequisite-v0-1",
        "head_sha": "042f3e1a46d60abe5b5a52d432aa0b47d2606939",
        "declared_standing": "PILOT_DEPLOYMENT_PREREQUISITE_IMPLEMENTATION_CANDIDATE_NOT_ADMITTED_NOT_PILOT_AUTHORIZED",
        "snapshot_classification": "PILOT_PREREQUISITE_IMPLEMENTATION_CANDIDATE_LINEAGE_AND_EXTERIOR_REVIEW_REQUIRED",
        "recommended_disposition": "HOLD_PENDING_PR110_PR111_LINEAGE_RECONCILIATION_AND_EXTERIOR_REVIEW",
    },
}

EXPECTED_LANES = {
    "FOUNDATIONAL_CORRECTION": [65],
    "EXTERIOR_EVIDENCE": [105],
    "INTEROPERABILITY_EXPERIMENT": [100],
    "PROOF_GOVERNANCE": [106],
    "META_EVIDENCE_RESEARCH": [84, 86],
    "PRE_PILOT_IMPLEMENTATION": [110, 111],
}

EXPECTED_RELATIONSHIPS = {
    "PR84_PARENT_OF_PR86",
    "PR65_PRECEDES_PROOF002_SUBSTRATE",
    "PR105_PRECEDES_PROOF003_SUBSTRATE",
    "PR100_PRECEDES_PROOF004_SUBSTRATE",
    "PR84_PR86_PRECEDE_PROOF005_SUBSTRATE",
    "PR110_PR111_LINEAGE_UNRESOLVED",
    "PROOF001_ALREADY_ADMITTED_WITHOUT_PORTFOLIO_INHERITANCE",
}

EXPECTED_INVARIANTS = {
    "OPEN_STATUS_DOES_NOT_CONFER_ADMISSION",
    "GREEN_CHECKS_DO_NOT_CONFER_MERGE_AUTHORIZATION",
    "GITHUB_MERGEABILITY_DOES_NOT_CONFER_GOVERNED_STANDING",
    "REVIEW_DOES_NOT_CONFER_AUTHORITY_ENDORSEMENT_OR_ADMISSION",
    "LATER_CHRONOLOGY_DOES_NOT_CONFER_SUCCESSOR_STANDING",
    "DEPENDENCY_DOES_NOT_CONFER_STANDING_INHERITANCE",
    "SNAPSHOT_ADMISSION_DOES_NOT_CHANGE_ANY_SOURCE_PULL_REQUEST",
    "PROOF001_ADMISSION_DOES_NOT_ADMIT_THE_WIDER_PORTFOLIO",
    "EVIDENCE_ADMISSION_DOES_NOT_CONFER_IMPLEMENTATION_ADMISSION",
    "IMPLEMENTATION_ADMISSION_DOES_NOT_CONFER_EXECUTION_AUTHORIZATION",
}

EXPECTED_CREATION_EFFECTS = {
    "main_ref": "NONE",
    "preservation_ref": "NONE",
    "existing_candidate_refs": "NONE",
    "existing_pull_request_state": "NONE",
    "source_pr_content": "NONE",
    "source_pr_standing": "NONE",
    "repository_settings": "NONE",
    "branch_protection": "NOT_CHANGED_REQUIRES_SEPARATE_AUTHORIZATION",
    "admission": "NONE_BEFORE_REVIEWED_MERGE",
    "authority_delta": "NONE",
    "execution_effect": "NONE",
    "provider_calls": 0,
    "pair_001_calls": 0,
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for item in value.values():
            assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            assert_finite(item)


def safe_regular_file(root: Path, relative: Path) -> Path:
    value = relative.as_posix()
    pure = PurePosixPath(value)
    if not value or pure.is_absolute() or value != pure.as_posix() or ".." in pure.parts:
        raise ValueError(f"unsafe repository-relative path: {value!r}")
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        if stat.S_ISLNK(current.lstat().st_mode):
            raise ValueError(f"symlink substitution rejected: {value}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"regular file required: {value}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def load_snapshot(root: Path) -> dict[str, Any]:
    path = safe_regular_file(root, SNAPSHOT)
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM prohibited")
    if b"\r" in raw:
        raise ValueError("CR bytes prohibited")
    if not raw.endswith(b"\n"):
        raise ValueError("final LF required")
    value = json.loads(
        raw.decode("utf-8", errors="strict"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    assert_finite(value)
    if not isinstance(value, dict):
        raise ValueError("snapshot root must be an object")
    return value


def expect(errors: list[str], condition: bool, detail: str) -> None:
    if not condition:
        errors.append(detail)


def check(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        snapshot = load_snapshot(root.resolve())
    except Exception as exc:
        return [f"snapshot load failed: {exc}"]

    expect(errors, snapshot.get("schema_version") == "v0.1", "schema version mismatch")
    expect(
        errors,
        snapshot.get("record_kind") == "fork_open_candidate_coordinate_snapshot",
        "record kind mismatch",
    )
    expect(
        errors,
        snapshot.get("observed_at_utc") == EXPECTED_OBSERVED_AT_UTC,
        "observation time mismatch",
    )
    expect(
        errors,
        snapshot.get("candidate_standing") == EXPECTED_CANDIDATE_STANDING,
        "snapshot must remain a not-admitted candidate before reviewed merge",
    )
    expect(
        errors,
        snapshot.get("standing_on_reviewed_merge") == EXPECTED_MERGE_STANDING,
        "standing on reviewed merge mismatch",
    )

    governed = snapshot.get("governed_coordinate", {})
    expect(errors, isinstance(governed, dict), "governed coordinate must be an object")
    if isinstance(governed, dict):
        expect(
            errors,
            governed.get("branch") == "preservation/clean-continuance-v0.1",
            "governed branch mismatch",
        )
        expect(errors, governed.get("commit_sha") == EXPECTED_GOVERNED_SHA, "governed SHA mismatch")
        expect(
            errors,
            governed.get("comparison_to_observed_branch_tip") == "IDENTICAL_ZERO_AHEAD_ZERO_BEHIND",
            "governed tip comparison mismatch",
        )
        expect(errors, governed.get("proof_001_admission_merge_pull_request") == 109, "Proof 001 merge PR mismatch")
        expect(errors, governed.get("proof_001_admission_merge_commit") == EXPECTED_GOVERNED_SHA, "Proof 001 merge commit mismatch")
        expect(errors, governed.get("wider_proof_portfolio_admitted") is False, "Proof 001 cannot promote the wider portfolio")

    lanes = snapshot.get("lanes", [])
    observed_lanes: dict[str, list[int]] = {}
    if isinstance(lanes, list):
        for lane in lanes:
            if not isinstance(lane, dict):
                errors.append("lane entry must be an object")
                continue
            lane_id = lane.get("lane_id")
            pull_requests = lane.get("pull_requests")
            if not isinstance(lane_id, str) or lane_id in observed_lanes or not isinstance(pull_requests, list):
                errors.append("invalid or duplicate lane entry")
                continue
            observed_lanes[lane_id] = pull_requests
    else:
        errors.append("lanes must be a list")
    expect(errors, snapshot.get("lane_count") == 6, "six enumerated lanes required")
    expect(errors, observed_lanes == EXPECTED_LANES, "lane mapping mismatch")
    correction = snapshot.get("preserved_source_analysis_correction", {})
    expect(
        errors,
        isinstance(correction, dict)
        and correction.get("enumerated_lane_count") == 6
        and correction.get("snapshot_lane_count") == 6
        and correction.get("disposition")
        == "ARITHMETIC_COUNT_CORRECTED_WITHOUT_COLLAPSING_ANY_ENUMERATED_LANE",
        "five-versus-six lane correction not preserved",
    )

    entries = snapshot.get("pull_requests", [])
    by_number: dict[int, dict[str, Any]] = {}
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("pull-request entry must be an object")
                continue
            number = entry.get("pull_request")
            if not isinstance(number, int) or isinstance(number, bool) or number in by_number:
                errors.append(f"invalid or duplicate pull-request number: {number!r}")
                continue
            by_number[number] = entry
    else:
        errors.append("pull_requests must be a list")
    expect(errors, set(by_number) == set(EXPECTED_PRS), "exact eight pull requests required")

    for number, expected in EXPECTED_PRS.items():
        entry = by_number.get(number, {})
        for key, value in expected.items():
            expect(errors, entry.get(key) == value, f"PR #{number} {key} mismatch")
        expect(errors, entry.get("state_observed") == "OPEN", f"PR #{number} must preserve open observation")
        expect(errors, entry.get("draft_observed") is True, f"PR #{number} must preserve draft observation")
        expect(errors, isinstance(entry.get("mergeable_observed"), bool), f"PR #{number} mergeability observation must be boolean")
        expect(errors, entry.get("mechanics_carry_standing") is False, f"PR #{number} GitHub mechanics cannot carry standing")
        expect(errors, entry.get("direct_merge_unchanged") is False, f"PR #{number} direct merge must remain rejected")
        expect(errors, entry.get("admission_effect") == "NONE", f"PR #{number} admission effect must be NONE")
        expect(errors, entry.get("execution_effect") == "NONE", f"PR #{number} execution effect must be NONE")
        expect(errors, entry.get("source_pr_effect") == "NONE", f"PR #{number} source effect must be NONE")

    pr105 = by_number.get(105, {})
    expect(errors, pr105.get("mergeable_observed") is False, "PR #105 non-mergeable observation must be preserved")
    pr106 = by_number.get(106, {})
    expect(
        errors,
        pr106.get("snapshot_classification")
        == "HISTORICALLY_VALID_V0_1_TEMPORALLY_STALE_FOR_CURRENT_RELIANCE",
        "PR #106 temporal classification mismatch",
    )
    pr111 = by_number.get(111, {})
    expect(
        errors,
        pr111.get("recommended_disposition")
        == "HOLD_PENDING_PR110_PR111_LINEAGE_RECONCILIATION_AND_EXTERIOR_REVIEW",
        "PR #111 cannot gain successor standing from chronology",
    )

    relationships = snapshot.get("dependency_and_precedence", [])
    relationship_ids: set[str] = set()
    relationship_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(relationships, list):
        for relationship in relationships:
            if not isinstance(relationship, dict):
                errors.append("relationship entry must be an object")
                continue
            relationship_id = relationship.get("relationship_id")
            if not isinstance(relationship_id, str) or relationship_id in relationship_ids:
                errors.append("invalid or duplicate relationship id")
                continue
            relationship_ids.add(relationship_id)
            relationship_by_id[relationship_id] = relationship
            expect(
                errors,
                isinstance(relationship.get("standing_inheritance"), str)
                and relationship.get("standing_inheritance", "").startswith("NONE"),
                f"{relationship_id} must reject standing inheritance",
            )
    else:
        errors.append("dependency_and_precedence must be a list")
    expect(errors, relationship_ids == EXPECTED_RELATIONSHIPS, "relationship set mismatch")
    lineage = relationship_by_id.get("PR110_PR111_LINEAGE_UNRESOLVED", {})
    expect(
        errors,
        lineage.get("relationship") == "RELATIONSHIP_UNRESOLVED_COMPUTED_RECONCILIATION_REQUIRED",
        "PR #110/#111 lineage must remain unresolved",
    )

    invariants = snapshot.get("non_inheritance_invariants")
    expect(
        errors,
        isinstance(invariants, list)
        and len(invariants) == len(set(invariants))
        and set(invariants) == EXPECTED_INVARIANTS,
        "non-inheritance invariant set mismatch",
    )
    expect(
        errors,
        snapshot.get("candidate_creation_effects") == EXPECTED_CREATION_EFFECTS,
        "candidate creation effects mismatch",
    )
    merge_effect = snapshot.get("standing_effect_on_reviewed_merge", {})
    expect(
        errors,
        merge_effect
        == {
            "snapshot_record": EXPECTED_MERGE_STANDING,
            "source_pull_requests": "NONE",
            "proof_portfolio": "NONE",
            "implementation": "NONE",
            "execution": "NONE",
            "authority_delta": "NONE",
        },
        "reviewed-merge effect mismatch",
    )
    next_gate = snapshot.get("next_sequence_gate", {})
    expect(
        errors,
        isinstance(next_gate, dict)
        and next_gate.get("target") == "PR65@479de5f929cb37377ccba5ef93f7a4f7b93e1120"
        and next_gate.get("effect_of_this_snapshot")
        == "SEQUENCE_RECOMMENDATION_ONLY_NOT_REVIEW_OR_MERGE_AUTHORIZATION",
        "next gate must remain a recommendation without inherited authorization",
    )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    errors = check(args.repo_root)
    payload = {
        "checker_id": CHECKER_ID,
        "snapshot": SNAPSHOT.as_posix(),
        "status": CONFORMING_RESULT if not errors else "OPEN_CANDIDATE_COORDINATE_SNAPSHOT_INVALID",
        "finding_count": len(errors),
        "findings": errors,
        "interpretation": {
            "proves": [
                "the committed snapshot matches its declared exact-coordinate contract",
                "the snapshot structurally rejects standing inheritance from GitHub mechanics and chronology",
                "the snapshot preserves six enumerated lanes and eight named draft pull requests",
            ],
            "does_not_prove": [
                "that observed GitHub metadata remains current",
                "source pull-request admission or merge authorization",
                "truth, correctness, completeness, authority, compliance, safety, or production readiness",
                "implementation admission, deployment authorization, or execution permission",
            ],
        },
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
