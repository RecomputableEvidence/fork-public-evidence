#!/usr/bin/env python3
"""Mechanical checker for Fork CAD / PROOF-005 correction successor v0.2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class CandidateError(ValueError):
    pass


EXPECTED_PR84 = "46fcd2c2580abd86ffbe215e6c387fee2bcb1b39"
EXPECTED_PR86 = "f72ca3fad82bee068527fe63eaf1c8eba87dd698"
EXPECTED_BASE = "eb195950eb8c383e94c9ba75df81615d69dd0ad2"
ALLOWED_EVENT_TYPES = {
    "PUBLIC_REVIEW_SCOPE_EXPANSION",
    "TEXTUAL_CORRECTION",
    "MODEL_SELF_REPORT",
    "MODEL_SELF_REPORT_WITHDRAWAL",
    "ANALYST_OVERINTERPRETATION_AND_CORRECTION",
}
ALLOWED_SOURCE_ROLES = {
    "REVIEWER_STATEMENT",
    "MODEL_SELF_REPORT",
    "ANALYST_STATEMENT",
}


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateError(f"{path}: cannot load JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise CandidateError(f"{path}: top-level JSON must be object")
    return value


def require_equal(obj: dict[str, Any], key: str, expected: Any, label: str) -> None:
    if obj.get(key) != expected:
        raise CandidateError(f"{label}: {key} must equal {expected!r}")


def require_nonempty_str(obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value:
        raise CandidateError(f"{label}: {key} must be non-empty string")
    return value


def validate_lineage(record: dict[str, Any]) -> None:
    require_equal(record, "status", "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED", "lineage")
    base = record.get("construction_base")
    if not isinstance(base, dict) or base.get("commit_sha") != EXPECTED_BASE:
        raise CandidateError("lineage: construction base must bind exact governed coordinate")
    surfaces = record.get("historical_surfaces")
    if not isinstance(surfaces, list) or len(surfaces) != 2:
        raise CandidateError("lineage: exactly two historical surfaces required")
    by_pr = {item.get("pull_request"): item for item in surfaces if isinstance(item, dict)}
    expected = {
        84: (EXPECTED_PR84, "REPRODUCED_WITH_CORRECTIONS_REQUIRED"),
        86: (EXPECTED_PR86, "REVIEW_INCONCLUSIVE"),
    }
    for pr, (head, disposition) in expected.items():
        item = by_pr.get(pr)
        if item is None:
            raise CandidateError(f"lineage: missing PR #{pr}")
        if item.get("exact_head") != head or item.get("review_disposition") != disposition:
            raise CandidateError(f"lineage: PR #{pr} exact head/review disposition mismatch")
        if item.get("rewritten") is not False or item.get("direct_merge_selected") is not False:
            raise CandidateError(f"lineage: PR #{pr} must remain historical and unmerged")
    standing = record.get("standing")
    if not isinstance(standing, dict):
        raise CandidateError("lineage: standing object required")
    require_equal(standing, "proof_packaging_state", "NOT_ADMITTED", "lineage.standing")
    require_equal(standing, "execution_authorized", False, "lineage.standing")


def validate_case_record(record: dict[str, Any]) -> None:
    require_equal(record, "status", "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED", "case")
    require_equal(record, "candidate_labels_are_canonical", False, "case")
    require_equal(record, "raw_sources_published", False, "case")
    require_equal(record, "provider_calls_performed", 0, "case")
    require_equal(record, "pair_001_effect", "NONE", "case")
    require_equal(record, "admission_effect", "NONE", "case")
    require_equal(record, "readiness_effect", "NONE", "case")
    parent = record.get("historical_parent")
    if not isinstance(parent, dict) or parent.get("exact_head") != EXPECTED_PR84:
        raise CandidateError("case: historical PR #84 head must remain bound")


def _claim_map(ledger: dict[str, Any]) -> dict[str, dict[str, Any]]:
    claims = ledger.get("claims")
    if not isinstance(claims, list):
        raise CandidateError("ledger: claims must be list")
    result: dict[str, dict[str, Any]] = {}
    for claim in claims:
        if not isinstance(claim, dict):
            raise CandidateError("ledger: claim entries must be objects")
        cid = require_nonempty_str(claim, "claim_id", "ledger.claim")
        if cid in result:
            raise CandidateError(f"ledger: duplicate claim_id {cid}")
        refs = claim.get("source_refs")
        if not isinstance(refs, list) or not refs or not all(isinstance(v, str) and v for v in refs):
            raise CandidateError(f"ledger: {cid} source_refs required")
        require_nonempty_str(claim, "source_binding_state", f"ledger.{cid}")
        require_nonempty_str(claim, "current_disposition", f"ledger.{cid}")
        result[cid] = claim
    expected_ids = {f"CAD-004-C00{i}" for i in range(1, 9)}
    if set(result) != expected_ids:
        raise CandidateError("ledger: corrected C001-C008 set required")
    return result


def validate_claim_ledger(ledger: dict[str, Any]) -> None:
    require_equal(ledger, "status", "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED", "ledger")
    require_equal(ledger, "candidate_classifications_are_canonical", False, "ledger")
    claims = _claim_map(ledger)

    c1 = claims["CAD-004-C001"]
    require_equal(c1, "current_disposition", "ACCESS_STATE_DECOMPOSED", "C001")
    expected_dims = {
        "NOT_SUPPLIED": "CONTRADICTED",
        "VISIBLE_ATTACHMENT_PRESENCE": "OBSERVED",
        "EARLIER_TURN_ACCESS": "UNRESOLVED",
        "LATER_DIRECT_READ": "OBSERVED",
    }
    if c1.get("dimensions") != expected_dims:
        raise CandidateError("C001: access dimensions must remain explicitly decomposed")

    c2 = claims["CAD-004-C002"]
    require_equal(c2, "current_disposition", "ATTRIBUTED_UNVERIFIED_EXECUTION_REPORT", "C002")
    require_equal(c2, "verified_execution_receipt_present", False, "C002")

    c3 = claims["CAD-004-C003"]
    require_equal(c3, "current_disposition", "ROLE_BINDING_INCOMPLETE_MULTI_ROLE", "C003")
    roles = c3.get("roles")
    if not isinstance(roles, list) or len(set(roles)) < 2:
        raise CandidateError("C003: at least two preserved artifact roles required")
    require_equal(c3, "role_equivalence_established", False, "C003")

    c4 = claims["CAD-004-C004"]
    require_equal(c4, "current_disposition", "UNRESOLVED_NO_SCOPE_CROSSWALK", "C004")
    require_equal(c4, "scope_equivalence_established", False, "C004")

    require_equal(
        claims["CAD-004-C005"],
        "current_disposition",
        "SUPPORTED_WITHIN_DECLARED_SOURCE_INSPECTION_SCOPE",
        "C005",
    )

    c6 = claims["CAD-004-C006"]
    require_equal(c6, "register_observed", "OBSERVED", "C006")
    require_equal(c6, "behavioral_influence", "UNTESTED", "C006")

    c7 = claims["CAD-004-C007"]
    require_equal(c7, "artifact_presence", "SUPPORTED", "C007")
    expected_completeness = {
        "contextual": "UNRESOLVED",
        "chronological": "UNRESOLVED",
        "parse_state": "UNRESOLVED",
        "evidentiary": "UNRESOLVED",
    }
    if c7.get("completeness") != expected_completeness:
        raise CandidateError("C007: presence must not promote completeness")

    c8 = claims["CAD-004-C008"]
    require_equal(c8, "current_disposition", "MIXED_THESIS_SUPPORTED_ONLY_WITH_DECOMPOSED_ACCESS_STATE", "C008")
    require_equal(c8, "automatic_proof_promotion", False, "C008")

    non_claims = ledger.get("case_non_claims")
    if not isinstance(non_claims, list) or not non_claims:
        raise CandidateError("ledger: case_non_claims required")


def validate_event_register(register: dict[str, Any]) -> None:
    require_equal(register, "status", "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED", "events")
    if set(register.get("controlled_event_types", [])) != ALLOWED_EVENT_TYPES:
        raise CandidateError("events: controlled event vocabulary mismatch")
    events = register.get("events")
    if not isinstance(events, list) or not events:
        raise CandidateError("events: nonempty events list required")
    ids: set[str] = set()
    for event in events:
        if not isinstance(event, dict):
            raise CandidateError("events: event entries must be objects")
        eid = require_nonempty_str(event, "event_id", "events.event")
        if eid in ids:
            raise CandidateError(f"events: duplicate event_id {eid}")
        ids.add(eid)
        etype = event.get("event_type")
        if etype not in ALLOWED_EVENT_TYPES:
            raise CandidateError(f"{eid}: undeclared event_type {etype!r}")
        origin = require_nonempty_str(event, "statement_origin", eid)
        role = event.get("source_role")
        if role not in ALLOWED_SOURCE_ROLES:
            raise CandidateError(f"{eid}: invalid source_role")
        refs = event.get("source_refs")
        if not isinstance(refs, list) or not refs:
            raise CandidateError(f"{eid}: source_refs required")
        require_nonempty_str(event, "observable_text_summary", eid)
        require_nonempty_str(event, "artifact_grounded_disposition", eid)
        if not isinstance(event.get("mechanism_verified"), bool):
            raise CandidateError(f"{eid}: mechanism_verified must be boolean")
        require_nonempty_str(event, "causal_standing", eid)
        if role == "MODEL_SELF_REPORT" and event.get("mechanism_verified") is not False:
            raise CandidateError(f"{eid}: model self-report cannot verify mechanism")
        if etype in {"MODEL_SELF_REPORT", "MODEL_SELF_REPORT_WITHDRAWAL"} and role != "MODEL_SELF_REPORT":
            raise CandidateError(f"{eid}: model self-report event must carry MODEL_SELF_REPORT source_role")
        if origin == "CLAUDE" and role == "MODEL_SELF_REPORT" and event.get("causal_standing") != "UNRESOLVED":
            raise CandidateError(f"{eid}: model self-report causal standing must remain unresolved")
    non_claims = register.get("non_claims")
    if not isinstance(non_claims, list) or not non_claims:
        raise CandidateError("events: non_claims required")


def validate_control_effects(record: dict[str, Any]) -> None:
    expected = {
        "status": "CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED",
        "pull_request_effect": "REVIEW_SURFACE_ONLY",
        "admission": False,
        "publication": False,
        "endorsement": False,
        "provider_calls": 0,
        "pair_001_effect": "NONE",
        "pair_001_execution_authorized": False,
        "readiness_effect": "NONE",
        "readiness_promoted": False,
        "proof_admission_effect": "NONE",
        "model_standing_effect": "NONE",
        "authority_effect": "NONE",
    }
    for key, value in expected.items():
        require_equal(record, key, value, "effects")


def validate_family_grounding(record: dict[str, Any]) -> None:
    require_equal(record, "status", "SOURCE_GROUNDING_INCOMPLETE_NOT_CLASSIFIED_NOT_ADMITTED", "families")
    families = record.get("families")
    if not isinstance(families, list) or len(families) != 15:
        raise CandidateError("families: exactly fifteen historical proposals required")
    expected_ids = {f"CAD-META-FAM-{i:03d}" for i in range(1, 16)}
    ids: set[str] = set()
    for family in families:
        if not isinstance(family, dict):
            raise CandidateError("families: entries must be objects")
        fid = require_nonempty_str(family, "family_id", "families.family")
        ids.add(fid)
        require_equal(family, "grounding_status", "INCOMPLETE", fid)
        for key in ("original_suggested_instance_ids", "source_refs", "source_spans", "chronology_bindings", "version_bindings"):
            if family.get(key) != []:
                raise CandidateError(f"{fid}: {key} must remain empty until source-addressable grounding exists")
        for key in (
            "merge_or_separation_rationale_status",
            "strongest_non_failure_interpretation_status",
            "contrary_evidence_status",
            "domain_expertise_status",
            "disposition_basis_status",
        ):
            require_equal(family, key, "MISSING", fid)
        require_equal(family, "classification_effect", "NONE", fid)
    if ids != expected_ids:
        raise CandidateError("families: family ID set mismatch")
    unresolved = record.get("unresolved_artifact_question")
    if not isinstance(unresolved, dict):
        raise CandidateError("families: unresolved artifact question required")
    require_equal(unresolved, "disposition", "UNRESOLVED_ARTIFACT_EXISTENCE", "families.unresolved")
    require_equal(unresolved, "absence_inferred", False, "families.unresolved")
    require_equal(record, "canonical_case_ids_assigned", False, "families")
    require_equal(record, "finding_codes_assigned", False, "families")
    require_equal(record, "admitted", False, "families")


def validate_assessor_correction(record: dict[str, Any]) -> None:
    require_equal(record, "status", "CORRECTION_BINDING_INCOMPLETE_NOT_ADMITTED", "assessor")
    parent = record.get("historical_parent")
    if not isinstance(parent, dict) or parent.get("exact_head") != EXPECTED_PR86:
        raise CandidateError("assessor: historical PR #86 head must remain bound")
    require_equal(
        record,
        "binding_state",
        "INCOMPLETE_ORIGINAL_STATEMENT_NOT_SOURCE_ADDRESSED_IN_AVAILABLE_REPOSITORY_SURFACE",
        "assessor",
    )
    if record.get("source_addressable_original_statement_ref") is not None:
        raise CandidateError("assessor: do not invent a source-addressable original statement reference")
    require_equal(record, "historical_statement_erased", False, "assessor")
    require_equal(record, "independent_review_required", True, "assessor")
    require_equal(record, "admission_effect", "NONE", "assessor")


def validate_candidate(root: Path) -> None:
    v2 = root / "docs/meta-evidence/conversational-authority-drift-v0.2"
    case = v2 / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
    supplement = v2 / "supplements/SUPPLEMENT_001_META_ASSESSMENT"
    validate_lineage(load_json(v2 / "HISTORICAL_LINEAGE_v0_2.json"))
    validate_case_record(load_json(case / "CASE_RECORD_v0_2.json"))
    validate_claim_ledger(load_json(case / "CLAIM_LEDGER_v0_2.json"))
    validate_event_register(load_json(case / "OBSERVABLE_EVENT_REGISTER_v0_2.json"))
    validate_control_effects(load_json(v2 / "CONTROL_EFFECTS_v0_2.json"))
    validate_family_grounding(load_json(supplement / "FAMILY_GROUNDING_REGISTER_v0_2.json"))
    validate_assessor_correction(load_json(supplement / "ASSESSOR_CORRECTION_EVENT_v0_2.json"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        validate_candidate(args.root)
    except CandidateError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: Fork CAD / PROOF-005 correction successor v0.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
