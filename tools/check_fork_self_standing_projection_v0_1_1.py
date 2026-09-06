#!/usr/bin/env python3
"""Validate Fork self-standing projection v0.1.1 without collapsing provenance or independence."""

from __future__ import annotations

import json
import math
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = Path(
    "docs/preservation/current-standing/"
    "FORK_SELF_STANDING_PROJECTION_2026_09_06_v0_1_1_CANDIDATE.json"
)
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")

TOP_KEYS = {
    "schema_version", "record_kind", "record_id", "record_date", "time_basis",
    "projection_observed_at", "projection_nature", "append_only", "repository_coordinate",
    "predecessor_projection", "claims", "record_level_non_claims",
}
CLAIM_KEYS = {
    "claim_id", "subject", "statement", "finding_kind", "temporal_status",
    "historical_coordinate", "assertion_origin", "standing_effect",
    "evidence_provenance", "interpretation_provenance", "verification",
    "independence", "limitations", "non_claims",
}
EVIDENCE_KEYS = {"evidence_id", "kind", "relation", "source", "coordinate", "digest", "observed_at", "clock_domain"}
INTERPRETATION_KEYS = {"present", "kind", "producer_class", "method", "source_evidence_ids"}
VERIFICATION_KEYS = {"status", "independent_verification_records"}
INDEPENDENCE_AXES = {
    "computational", "artifact_acquisition", "contextual_blinding",
    "interpretive", "institutional",
}
AXIS_KEYS = {"state", "reference_class", "evidence_ids"}

FINDING_KINDS = {
    "OBSERVATION", "DERIVED_STANDING", "INFERENCE", "HYPOTHESIS",
    "GOVERNANCE_DISPOSITION",
}
TEMPORAL = {"CURRENT_AT_NAMED_COORDINATE", "HISTORICAL_ONLY"}
ORIGINS = {
    "MECHANICALLY_OBSERVED", "AUTHORIAL_OR_PROGRAMMATIC",
    "EXTERNAL_REVIEWER", "GOVERNANCE_DISPOSITION",
}
STANDING_EFFECTS = {
    "OBSERVATION_ONLY_NO_STANDING_PROMOTION", "HISTORICAL_ONLY",
    "DERIVED_LIMITATION_ONLY", "GOVERNANCE_EFFECT_EXPLICITLY_DECLARED",
}
EVIDENCE_KINDS = {
    "GITHUB_API_OBSERVATION", "GOVERNED_REPOSITORY_RECORD",
    "EXECUTION_RECEIPT", "EXTERNAL_REVIEW", "DERIVED_SUMMARY",
    "CONVERSATIONAL_RECONSTRUCTION",
}
EVIDENCE_RELATIONS = {"DIRECT_SUPPORT", "CONTEXT_ONLY", "INTERPRETIVE_SOURCE"}
INTERPRETATION_KINDS = {
    "NONE", "DERIVED_TEMPORAL_PROJECTION", "BOUNDED_INFERENCE",
    "LENS_SHIFT_SYNTHESIS", "GOVERNANCE_INTERPRETATION",
}
PRODUCER_CLASSES = {
    "NONE", "AI_ASSISTED_AUTHORIAL_WORKFLOW", "EXTERNAL_REVIEWER",
    "GOVERNANCE_ACTOR",
}
VERIFY_STATES = {
    "NOT_INDEPENDENTLY_VERIFIED", "PARTIALLY_VERIFIED",
    "INDEPENDENTLY_VERIFIED", "NOT_APPLICABLE",
}
AXIS_STATES = {"ESTABLISHED", "PARTIAL", "NOT_ESTABLISHED", "NOT_APPLICABLE"}


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
        for child in value.values():
            assert_finite(child)
    elif isinstance(value, list):
        for child in value:
            assert_finite(child)


def strict_load(path: Path) -> Any:
    with (ROOT / path).open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def validate_record(record: Any) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []

    def add(code: str, detail: str, path: str) -> None:
        findings.append({"code": code, "detail": detail, "path": path})

    def exact_keys(value: Any, expected: set[str], path: str, code: str) -> bool:
        if not isinstance(value, dict):
            add(code, "expected object", path)
            return False
        actual = set(value)
        if actual != expected:
            add(
                code,
                f"expected keys {sorted(expected)!r}; found {sorted(actual)!r}",
                path,
            )
            return False
        return True

    if not exact_keys(record, TOP_KEYS, "$", "TOP_LEVEL_KEYS"):
        return findings

    constants = {
        "schema_version": "v0.1.1",
        "record_kind": "fork_self_standing_projection",
        "projection_nature": "NON_AUTHORITATIVE_DERIVED_TEMPORAL_PROJECTION",
        "append_only": True,
    }
    for key, expected in constants.items():
        if record.get(key) != expected:
            add("RECORD_CONSTANT", f"{key} must equal {expected!r}", f"$.{key}")

    if not isinstance(record.get("projection_observed_at"), str) or not record["projection_observed_at"].strip():
        add("PROJECTION_OBSERVED_AT", "projection_observed_at must be a non-empty timestamp string", "$.projection_observed_at")

    repo = record.get("repository_coordinate")
    repo_keys = {"repository", "branch", "commit_sha", "tree_sha"}
    if exact_keys(repo, repo_keys, "$.repository_coordinate", "REPOSITORY_KEYS"):
        if repo["repository"] != "RecomputableEvidence/fork-public-evidence":
            add("REPOSITORY_NAME", "unexpected repository", "$.repository_coordinate.repository")
        if repo["branch"] != "preservation/clean-continuance-v0.1":
            add("GOVERNED_BRANCH", "unexpected governed branch", "$.repository_coordinate.branch")
        for field in ("commit_sha", "tree_sha"):
            if not isinstance(repo[field], str) or SHA1_RE.fullmatch(repo[field]) is None:
                add("REPOSITORY_SHA", "expected 40 lowercase hex characters", f"$.repository_coordinate.{field}")

    predecessor = record.get("predecessor_projection")
    pred_keys = {"path", "git_blob_sha", "temporal_status", "non_rewrite"}
    if exact_keys(predecessor, pred_keys, "$.predecessor_projection", "PREDECESSOR_KEYS"):
        if predecessor["temporal_status"] != "HISTORICAL_PREDECESSOR":
            add("PREDECESSOR_TEMPORAL_STATUS", "predecessor must remain historical", "$.predecessor_projection.temporal_status")
        if predecessor["non_rewrite"] is not True:
            add("PREDECESSOR_REWRITE", "predecessor non_rewrite must be true", "$.predecessor_projection.non_rewrite")
        if not isinstance(predecessor["git_blob_sha"], str) or SHA1_RE.fullmatch(predecessor["git_blob_sha"]) is None:
            add("PREDECESSOR_SHA", "invalid predecessor blob SHA", "$.predecessor_projection.git_blob_sha")

    claims = record.get("claims")
    if not isinstance(claims, list) or not claims:
        add("CLAIMS_EMPTY", "claims must be a non-empty list", "$.claims")
        return findings

    seen_claims: set[str] = set()
    for i, claim in enumerate(claims):
        p = f"$.claims[{i}]"
        if not exact_keys(claim, CLAIM_KEYS, p, "CLAIM_KEYS"):
            continue

        cid = claim["claim_id"]
        if not isinstance(cid, str) or not cid:
            add("CLAIM_ID", "claim_id must be a non-empty string", f"{p}.claim_id")
        elif cid in seen_claims:
            add("CLAIM_ID_DUPLICATE", f"duplicate claim_id {cid}", f"{p}.claim_id")
        else:
            seen_claims.add(cid)

        if claim["finding_kind"] not in FINDING_KINDS:
            add("FINDING_KIND", "undeclared finding_kind", f"{p}.finding_kind")
        if claim["temporal_status"] not in TEMPORAL:
            add("TEMPORAL_STATUS", "undeclared temporal_status", f"{p}.temporal_status")
        if claim["assertion_origin"] not in ORIGINS:
            add("ASSERTION_ORIGIN", "undeclared assertion_origin", f"{p}.assertion_origin")
        if claim["standing_effect"] not in STANDING_EFFECTS:
            add("STANDING_EFFECT", "undeclared standing_effect", f"{p}.standing_effect")

        if claim["temporal_status"] == "HISTORICAL_ONLY":
            if not isinstance(claim["historical_coordinate"], str) or SHA1_RE.fullmatch(claim["historical_coordinate"]) is None:
                add("HISTORICAL_COORDINATE", "historical claim requires exact historical coordinate", f"{p}.historical_coordinate")
        elif claim["temporal_status"] == "CURRENT_AT_NAMED_COORDINATE":
            if claim["historical_coordinate"] is not None:
                add("CURRENT_WITH_HISTORICAL_COORDINATE", "current claim must not silently carry historical coordinate", f"{p}.historical_coordinate")

        if claim["finding_kind"] == "OBSERVATION":
            if claim["assertion_origin"] != "MECHANICALLY_OBSERVED":
                add("OBSERVATION_ORIGIN", "observation must remain mechanically observed", f"{p}.assertion_origin")
            if claim["standing_effect"] != "OBSERVATION_ONLY_NO_STANDING_PROMOTION":
                add("OBSERVATION_PROMOTION", "observation cannot carry stronger standing effect", f"{p}.standing_effect")
        if claim["standing_effect"] == "HISTORICAL_ONLY" and claim["temporal_status"] != "HISTORICAL_ONLY":
            add("HISTORICAL_EFFECT_MISMATCH", "historical standing effect requires historical temporal status", f"{p}.standing_effect")

        evidence = claim["evidence_provenance"]
        if not isinstance(evidence, list) or not evidence:
            add("EVIDENCE_EMPTY", "claim requires evidence provenance", f"{p}.evidence_provenance")
            continue

        evidence_ids: set[str] = set()
        for j, item in enumerate(evidence):
            ep = f"{p}.evidence_provenance[{j}]"
            if not exact_keys(item, EVIDENCE_KEYS, ep, "EVIDENCE_KEYS"):
                continue
            eid = item["evidence_id"]
            if not isinstance(eid, str) or not eid:
                add("EVIDENCE_ID", "evidence_id must be non-empty", f"{ep}.evidence_id")
            elif eid in evidence_ids:
                add("EVIDENCE_ID_DUPLICATE", f"duplicate evidence_id {eid}", f"{ep}.evidence_id")
            else:
                evidence_ids.add(eid)
            if item["kind"] not in EVIDENCE_KINDS:
                add("EVIDENCE_KIND", "undeclared evidence kind", f"{ep}.kind")
            if item["relation"] not in EVIDENCE_RELATIONS:
                add("EVIDENCE_RELATION", "undeclared evidence relation", f"{ep}.relation")
            if not isinstance(item["source"], str) or not item["source"].strip():
                add("EVIDENCE_SOURCE", "source must be non-empty", f"{ep}.source")
            if not isinstance(item["observed_at"], str) or not item["observed_at"].strip():
                add("EVIDENCE_OBSERVED_AT", "evidence observation requires observed_at", f"{ep}.observed_at")
            if not isinstance(item["clock_domain"], str) or not item["clock_domain"].strip():
                add("EVIDENCE_CLOCK_DOMAIN", "evidence observation requires clock_domain", f"{ep}.clock_domain")

        interpretation = claim["interpretation_provenance"]
        if exact_keys(interpretation, INTERPRETATION_KEYS, f"{p}.interpretation_provenance", "INTERPRETATION_KEYS"):
            if interpretation["kind"] not in INTERPRETATION_KINDS:
                add("INTERPRETATION_KIND", "undeclared interpretation kind", f"{p}.interpretation_provenance.kind")
            if interpretation["producer_class"] not in PRODUCER_CLASSES:
                add("INTERPRETATION_PRODUCER", "undeclared producer class", f"{p}.interpretation_provenance.producer_class")
            refs = interpretation["source_evidence_ids"]
            if not isinstance(refs, list) or any(ref not in evidence_ids for ref in refs):
                add("INTERPRETATION_EVIDENCE_REF", "interpretation references must resolve within claim evidence", f"{p}.interpretation_provenance.source_evidence_ids")
            if interpretation["present"] is False:
                if interpretation["kind"] != "NONE" or interpretation["producer_class"] != "NONE" or interpretation["method"] is not None or refs != []:
                    add("INTERPRETATION_NONE_COLLAPSE", "absent interpretation must remain explicitly NONE with no evidence refs", f"{p}.interpretation_provenance")
            else:
                if interpretation["kind"] == "NONE" or interpretation["producer_class"] == "NONE":
                    add("INTERPRETATION_PRESENT_UNTYPED", "present interpretation must identify kind and producer", f"{p}.interpretation_provenance")
                if not isinstance(interpretation["method"], str) or not interpretation["method"].strip():
                    add("INTERPRETATION_METHOD", "present interpretation requires method", f"{p}.interpretation_provenance.method")
                if not refs:
                    add("INTERPRETATION_UNBOUND", "present interpretation requires bound evidence refs", f"{p}.interpretation_provenance.source_evidence_ids")

        if claim["finding_kind"] in {"DERIVED_STANDING", "INFERENCE", "HYPOTHESIS"} and not interpretation.get("present", False):
            add("DERIVED_WITHOUT_INTERPRETATION", "derived/inferential finding requires interpretation provenance", f"{p}.interpretation_provenance")

        verification = claim["verification"]
        if exact_keys(verification, VERIFICATION_KEYS, f"{p}.verification", "VERIFICATION_KEYS"):
            if verification["status"] not in VERIFY_STATES:
                add("VERIFICATION_STATUS", "undeclared verification status", f"{p}.verification.status")
            records = verification["independent_verification_records"]
            if not isinstance(records, list):
                add("VERIFICATION_RECORDS", "verification records must be a list", f"{p}.verification.independent_verification_records")
            elif verification["status"] == "INDEPENDENTLY_VERIFIED" and not records:
                add("VERIFICATION_PROMOTION", "independently verified requires independent verification record", f"{p}.verification")
            elif verification["status"] == "NOT_INDEPENDENTLY_VERIFIED" and records:
                add("VERIFICATION_CONTRADICTION", "not independently verified cannot carry independent verification records", f"{p}.verification")

        independence = claim["independence"]
        if exact_keys(independence, INDEPENDENCE_AXES, f"{p}.independence", "INDEPENDENCE_KEYS"):
            for axis_name in sorted(INDEPENDENCE_AXES):
                axis = independence[axis_name]
                ap = f"{p}.independence.{axis_name}"
                if not exact_keys(axis, AXIS_KEYS, ap, "INDEPENDENCE_AXIS_KEYS"):
                    continue
                if axis["state"] not in AXIS_STATES:
                    add("INDEPENDENCE_STATE", "undeclared independence state", f"{ap}.state")
                if not isinstance(axis["reference_class"], str) or not axis["reference_class"].strip():
                    add("INDEPENDENCE_REFERENCE_CLASS", "independence axis requires explicit reference class", f"{ap}.reference_class")
                refs = axis["evidence_ids"]
                if not isinstance(refs, list) or any(ref not in evidence_ids for ref in refs):
                    add("INDEPENDENCE_EVIDENCE_REF", "independence evidence refs must resolve within claim evidence", f"{ap}.evidence_ids")
                if axis["state"] in {"ESTABLISHED", "PARTIAL"} and not refs:
                    add("INDEPENDENCE_UNEVIDENCED", "established/partial independence requires evidence refs", ap)

    non_claims = record.get("record_level_non_claims")
    if not isinstance(non_claims, list) or not non_claims or any(not isinstance(x, str) or not x.strip() for x in non_claims):
        add("RECORD_NON_CLAIMS", "record_level_non_claims must contain non-empty strings", "$.record_level_non_claims")

    return findings


def evaluate() -> dict[str, Any]:
    try:
        record = strict_load(RECORD_PATH)
    except Exception as exc:
        return {
            "checker": Path(__file__).name,
            "status": "SELF_STANDING_PROJECTION_CANDIDATE_INVALID",
            "findings": [{"code": "INPUT_INVALID", "detail": str(exc), "path": "$input"}],
        }

    findings = validate_record(record)
    return {
        "checker": Path(__file__).name,
        "status": (
            "SELF_STANDING_PROJECTION_CANDIDATE_CONFORMS_NOT_ADMITTED"
            if not findings
            else "SELF_STANDING_PROJECTION_CANDIDATE_INVALID"
        ),
        "record_id": record.get("record_id"),
        "claim_count": len(record.get("claims", [])) if isinstance(record.get("claims"), list) else None,
        "findings": findings,
        "non_claims": [
            "Structural/semantic conformance is not self-admission.",
            "This checker does not independently verify the evidence referenced by the record.",
            "Separate independence dimensions do not combine into a blanket independent standing.",
            "The projection does not authorize repository settings, model changes, external action, or production use.",
        ],
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
