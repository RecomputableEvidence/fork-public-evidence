#!/usr/bin/env python3
"""Mechanical checker for Fork CAD / PROOF-005 bounded correction successor v0.2.2."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V021_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2_1.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v021_predecessor", V021_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load v0.2.1 predecessor checker")
V021 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V021)
V02 = V021.PREDECESSOR
CandidateError = V021.CandidateError

V2_REL = Path("docs/meta-evidence/conversational-authority-drift-v0.2")
CASE_REL = V2_REL / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
SUPPLEMENT_REL = V2_REL / "supplements/SUPPLEMENT_001_META_ASSESSMENT"

GOVERNED_PATHS = {
    "lineage": V2_REL / "HISTORICAL_LINEAGE_v0_2.json",
    "case": CASE_REL / "CASE_RECORD_v0_2.json",
    "ledger": CASE_REL / "CLAIM_LEDGER_v0_2.json",
    "events": CASE_REL / "OBSERVABLE_EVENT_REGISTER_v0_2.json",
    "effects": V2_REL / "CONTROL_EFFECTS_v0_2.json",
    "families": SUPPLEMENT_REL / "FAMILY_GROUNDING_REGISTER_v0_2.json",
    "assessor": SUPPLEMENT_REL / "ASSESSOR_CORRECTION_EVENT_v0_2.json",
}

LINEAGE_KEYS = {
    "schema_version", "record_id", "status", "construction_base",
    "historical_surfaces", "successor_purpose", "standing",
}
LINEAGE_CONSTRUCTION_BASE_KEYS = {"branch", "commit_sha"}
LINEAGE_SURFACE_KEYS_BY_PR = {
    84: {"pull_request", "exact_head", "review_disposition", "rewritten", "direct_merge_selected"},
    86: {"pull_request", "exact_head", "review_disposition", "secondary_standing", "rewritten", "direct_merge_selected"},
}
LINEAGE_STANDING_KEYS = {
    "proof_id", "source_evidence_state", "proof_packaging_state",
    "exterior_review_state", "model_standing_delta", "execution_authorized",
}

CASE_KEYS = {
    "case_id", "schema_version", "status", "historical_parent", "primary_question",
    "bounded_disposition", "source_grounding_state", "candidate_labels_are_canonical",
    "raw_sources_published", "provider_calls_performed", "pair_001_effect",
    "admission_effect", "readiness_effect", "non_claims",
}
CASE_PARENT_KEYS = {"pull_request", "exact_head", "historical_case_blob_sha"}

LEDGER_KEYS = {
    "ledger_id", "status", "case_id", "candidate_classifications_are_canonical",
    "claims", "case_non_claims",
}
CLAIM_COMMON_KEYS = {
    "claim_id", "historical_claim_id", "source_refs", "source_binding_state", "current_disposition",
}
CLAIM_KEYS_BY_ID = {
    "CAD-004-C001": CLAIM_COMMON_KEYS | {"dimensions", "non_inheritance"},
    "CAD-004-C002": CLAIM_COMMON_KEYS | {"verified_execution_receipt_present", "missing"},
    "CAD-004-C003": CLAIM_COMMON_KEYS | {"roles", "role_equivalence_established"},
    "CAD-004-C004": CLAIM_COMMON_KEYS | {"scope_equivalence_established", "missing"},
    "CAD-004-C005": CLAIM_COMMON_KEYS | {"scope_limit"},
    "CAD-004-C006": CLAIM_COMMON_KEYS | {"register_observed", "behavioral_influence"},
    "CAD-004-C007": CLAIM_COMMON_KEYS | {"artifact_presence", "completeness"},
    "CAD-004-C008": CLAIM_COMMON_KEYS | {"depends_on", "automatic_proof_promotion"},
}
C001_DIMENSION_KEYS = {
    "NOT_SUPPLIED", "VISIBLE_ATTACHMENT_PRESENCE", "EARLIER_TURN_ACCESS", "LATER_DIRECT_READ",
}
C007_COMPLETENESS_KEYS = {"contextual", "chronological", "parse_state", "evidentiary"}

EVENT_REGISTER_KEYS = {"register_id", "status", "case_id", "controlled_event_types", "events", "non_claims"}
EVENT_KEYS = set(V021.EVENT_ALLOWED_KEYS)

CONTROL_EFFECT_KEYS = {
    "record_id", "status", "pull_request_effect", "admission", "publication", "endorsement",
    "provider_calls", "pair_001_effect", "pair_001_execution_authorized", "readiness_effect",
    "readiness_promoted", "proof_admission_effect", "model_standing_effect", "authority_effect",
}

FAMILY_REGISTER_KEYS = {
    "register_id", "version", "status", "historical_parent", "counting_statement", "families",
    "unresolved_artifact_question", "canonical_case_ids_assigned", "finding_codes_assigned", "admitted",
}
FAMILY_PARENT_KEYS = {"pull_request", "exact_head", "historical_register_blob_sha"}
FAMILY_KEYS = {
    "family_id", "historical_label", "grounding_status", "original_suggested_instance_ids",
    "source_refs", "source_spans", "chronology_bindings", "version_bindings",
    "merge_or_separation_rationale_status", "strongest_non_failure_interpretation_status",
    "contrary_evidence_status", "domain_expertise_status", "disposition_basis_status",
    "classification_effect",
}
UNRESOLVED_ARTIFACT_KEYS = {"question_id", "disposition", "absence_inferred"}

ASSESSOR_KEYS = {
    "event_id", "version", "status", "historical_parent", "historical_affected_statement_text",
    "source_addressable_original_statement_ref", "binding_state", "replacement_statement",
    "historical_statement_erased", "independent_review_required", "admission_effect",
}
ASSESSOR_PARENT_KEYS = {"pull_request", "exact_head", "historical_event_blob_sha"}


def require_exact_keys(obj: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(obj, dict):
        raise CandidateError(f"{label}: object required")
    keys = set(obj)
    missing = expected - keys
    extras = keys - expected
    if missing:
        raise CandidateError(f"{label}: missing declared fields {sorted(missing)!r}")
    if extras:
        raise CandidateError(f"{label}: undeclared fields are not permitted: {sorted(extras)!r}")
    return obj


def validate_event_source_refs(event: dict[str, Any]) -> None:
    eid = str(event.get("event_id", "<unknown>"))
    refs = event.get("source_refs")
    if not isinstance(refs, list) or not refs:
        raise CandidateError(f"{eid}: source_refs must be a non-empty list")
    if not all(isinstance(ref, str) and bool(ref.strip()) for ref in refs):
        raise CandidateError(f"{eid}: every source_refs member must be a non-empty string")


def validate_model_self_report_event(event: dict[str, Any]) -> None:
    """v0.2.2 reusable model-self-report validator: v0.2.1 invariants plus source-ref typing."""
    V021.validate_model_self_report_event(event)
    validate_event_source_refs(event)


def validate_lineage_schema(record: dict[str, Any]) -> None:
    require_exact_keys(record, LINEAGE_KEYS, "schema.lineage")
    require_exact_keys(record["construction_base"], LINEAGE_CONSTRUCTION_BASE_KEYS, "schema.lineage.construction_base")
    surfaces = record["historical_surfaces"]
    if not isinstance(surfaces, list):
        raise CandidateError("schema.lineage.historical_surfaces: list required")
    for item in surfaces:
        if not isinstance(item, dict):
            raise CandidateError("schema.lineage.historical_surfaces: object entries required")
        pr = item.get("pull_request")
        expected = LINEAGE_SURFACE_KEYS_BY_PR.get(pr)
        if expected is None:
            raise CandidateError(f"schema.lineage.historical_surfaces: undeclared PR surface {pr!r}")
        require_exact_keys(item, expected, f"schema.lineage.pr{pr}")
    require_exact_keys(record["standing"], LINEAGE_STANDING_KEYS, "schema.lineage.standing")


def validate_case_schema(record: dict[str, Any]) -> None:
    require_exact_keys(record, CASE_KEYS, "schema.case")
    require_exact_keys(record["historical_parent"], CASE_PARENT_KEYS, "schema.case.historical_parent")


def validate_ledger_schema(ledger: dict[str, Any]) -> None:
    require_exact_keys(ledger, LEDGER_KEYS, "schema.ledger")
    claims = ledger["claims"]
    if not isinstance(claims, list):
        raise CandidateError("schema.ledger.claims: list required")
    for claim in claims:
        if not isinstance(claim, dict):
            raise CandidateError("schema.ledger.claims: object entries required")
        cid = claim.get("claim_id")
        expected = CLAIM_KEYS_BY_ID.get(cid)
        if expected is None:
            raise CandidateError(f"schema.ledger: undeclared claim id {cid!r}")
        require_exact_keys(claim, expected, f"schema.{cid}")
        if cid == "CAD-004-C001":
            require_exact_keys(claim["dimensions"], C001_DIMENSION_KEYS, "schema.C001.dimensions")
        if cid == "CAD-004-C007":
            require_exact_keys(claim["completeness"], C007_COMPLETENESS_KEYS, "schema.C007.completeness")


def validate_event_register_schema(register: dict[str, Any]) -> None:
    require_exact_keys(register, EVENT_REGISTER_KEYS, "schema.events")
    events = register["events"]
    if not isinstance(events, list):
        raise CandidateError("schema.events.events: list required")
    for event in events:
        event = require_exact_keys(event, EVENT_KEYS, "schema.events.event")
        validate_event_source_refs(event)
        if event.get("source_role") == "MODEL_SELF_REPORT":
            validate_model_self_report_event(event)


def validate_control_effects_schema(record: dict[str, Any]) -> None:
    require_exact_keys(record, CONTROL_EFFECT_KEYS, "schema.effects")


def validate_family_schema(record: dict[str, Any]) -> None:
    require_exact_keys(record, FAMILY_REGISTER_KEYS, "schema.families")
    require_exact_keys(record["historical_parent"], FAMILY_PARENT_KEYS, "schema.families.historical_parent")
    families = record["families"]
    if not isinstance(families, list):
        raise CandidateError("schema.families.families: list required")
    for family in families:
        family = require_exact_keys(family, FAMILY_KEYS, "schema.families.family")
        fid = str(family.get("family_id", "<unknown>"))
        # Family source_refs are required to remain empty in this frozen predecessor.
        # No source-addressability standing is inferred here.
        if family.get("source_refs") != []:
            raise CandidateError(f"{fid}: source_refs must remain empty until source grounding exists")
    require_exact_keys(
        record["unresolved_artifact_question"],
        UNRESOLVED_ARTIFACT_KEYS,
        "schema.families.unresolved_artifact_question",
    )


def validate_assessor_schema(record: dict[str, Any]) -> None:
    require_exact_keys(record, ASSESSOR_KEYS, "schema.assessor")
    require_exact_keys(record["historical_parent"], ASSESSOR_PARENT_KEYS, "schema.assessor.historical_parent")


def load_governed_records(root: Path) -> dict[str, dict[str, Any]]:
    """Strict-load every governed JSON artifact before any semantic validation."""
    return {name: V021.load_json_strict(root / rel) for name, rel in GOVERNED_PATHS.items()}


def validate_candidate(root: Path) -> None:
    records = load_governed_records(root)

    # Schema closure and syntactic source-ref constraints happen after strict parsing
    # but before predecessor semantic validation.
    validate_lineage_schema(records["lineage"])
    validate_case_schema(records["case"])
    validate_ledger_schema(records["ledger"])
    validate_event_register_schema(records["events"])
    validate_control_effects_schema(records["effects"])
    validate_family_schema(records["families"])
    validate_assessor_schema(records["assessor"])

    # Preserve all v0.2 semantic boundaries using the already strict-loaded objects.
    V02.validate_lineage(records["lineage"])
    V02.validate_case_record(records["case"])
    V02.validate_claim_ledger(records["ledger"])
    V02.validate_control_effects(records["effects"])
    V02.validate_family_grounding(records["families"])
    V02.validate_assessor_correction(records["assessor"])

    # Preserve v0.2.1's fixed-register fingerprint and origin-agnostic model-self-report rules.
    V021.validate_event_register_v0_2_1(records["events"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        validate_candidate(args.root)
    except CandidateError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: Fork CAD / PROOF-005 bounded correction successor v0.2.2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
