#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ARTIFACT_TYPE = "FORK_USE_CASE_BOUNDARY_RECORD"
ARTIFACT_VERSION = "v0.1"
CHECKER_SEMANTICS_VERSION = "v0.1.1"
FORK_ROLE = "EVIDENCE_BOUNDARY_INFRASTRUCTURE"
STRUCTURAL_SCOPE = "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"

FIELDS = {
    "AUDIT_COMPLIANCE",
    "VENDOR_RISK",
    "AI_BENCHMARK_CONSUMPTION",
    "CYBER_TRIAGE",
    "HEALTHCARE_PRIOR_AUTH_SYNTHETIC",
}

OUTCOMES = {
    "BOUNDARY_PRESERVED",
    "POINTER_UNRESOLVED",
    "BOUNDARY_EXPANSION_DETECTED",
    "NON_CLAIM_DROPPED",
    "EXPANSION_AUTHORITY_REF_MISSING",
    "MAPPING_INCOMPLETE",
}

ADVERSE_OUTCOMES = OUTCOMES - {"BOUNDARY_PRESERVED"}

OUTCOME_REVIEW_REASONS = {
    "BOUNDARY_PRESERVED": "BOUNDARY_STRUCTURALLY_PRESERVED",
    "POINTER_UNRESOLVED": "UNRESOLVED_POINTER_REQUIRES_REVIEW",
    "BOUNDARY_EXPANSION_DETECTED": "BOUNDARY_EXPANSION_REQUIRES_REVIEW",
    "NON_CLAIM_DROPPED": "NON_CLAIM_DROP_REQUIRES_REVIEW",
    "EXPANSION_AUTHORITY_REF_MISSING": "EXPANSION_POINTER_DEFECT_REQUIRES_REVIEW",
    "MAPPING_INCOMPLETE": "INCOMPLETE_MAPPING_REQUIRES_REVIEW",
}

REQUIRED_DO_NOT_MAP_TO = {
    "APPROVAL",
    "AUTHORIZATION",
    "COMPLIANCE",
    "CONTROL_EFFECTIVENESS",
    "LEGAL_SUFFICIENCY",
    "MODEL_SAFETY",
    "PATIENT_SAFETY",
    "PRODUCTION_READINESS",
    "RISK_ACCEPTANCE",
    "TRUTH",
}

REQUIRED_LIMITATION_FLAGS = {
    "does_not_validate_truth",
    "does_not_validate_safety",
    "does_not_validate_compliance",
    "does_not_validate_legal_sufficiency",
    "does_not_validate_approval",
    "automation_interpretation_required",
}

NON_CLAIM_RE = re.compile(r"^does_not_claim_[a-z0-9_]+$")
USE_CASE_ID_RE = re.compile(r"^[a-z0-9_]+_v0_1$")


def load_json(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"INVALID_JSON:{exc.lineno}:{exc.colno}:{exc.msg}"]
    except OSError as exc:
        return None, [f"READ_ERROR:{exc}"]
    if not isinstance(data, dict):
        return None, ["ROOT_NOT_OBJECT"]
    return data, []


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_object(parent: dict[str, Any], key: str, findings: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        findings.append(f"{key}:REQUIRED_OBJECT")
        return {}
    return value


def require_array(parent: dict[str, Any], key: str, findings: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        findings.append(f"{key}:REQUIRED_ARRAY")
        return []
    return value


def require_string(parent: dict[str, Any], key: str, findings: list[str], label: str | None = None) -> str:
    value = parent.get(key)
    if not is_non_empty_string(value):
        findings.append(f"{label or key}:REQUIRED_NON_EMPTY_STRING")
        return ""
    return value


def validate_non_claim_list(label: str, values: list[Any], findings: list[str], *, require_nonempty: bool = False) -> list[str]:
    if require_nonempty and not values:
        findings.append(f"{label}:REQUIRED_NON_EMPTY")
    normalized: list[str] = []
    seen: set[str] = set()
    for idx, item in enumerate(values):
        if not isinstance(item, str) or not NON_CLAIM_RE.match(item):
            findings.append(f"{label}[{idx}]:INVALID_NON_CLAIM_TOKEN")
            continue
        if item in seen:
            findings.append(f"{label}[{idx}]:DUPLICATE_NON_CLAIM")
        seen.add(item)
        normalized.append(item)
    return normalized


def validate_string_array(label: str, values: list[Any], findings: list[str], *, require_nonempty: bool = False) -> list[str]:
    if require_nonempty and not values:
        findings.append(f"{label}:REQUIRED_NON_EMPTY")
    normalized: list[str] = []
    for idx, item in enumerate(values):
        if not is_non_empty_string(item):
            findings.append(f"{label}[{idx}]:REQUIRED_NON_EMPTY_STRING")
            continue
        normalized.append(item)
    return normalized


def validate_limitations(limitations: dict[str, Any], findings: list[str]) -> None:
    for flag in sorted(REQUIRED_LIMITATION_FLAGS):
        if limitations.get(flag) is not True:
            findings.append(f"limitations.{flag}:REQUIRED_TRUE")
    do_not_map_to = limitations.get("do_not_map_to")
    if not isinstance(do_not_map_to, list):
        findings.append("limitations.do_not_map_to:REQUIRED_ARRAY")
        return
    actual = {item for item in do_not_map_to if isinstance(item, str)}
    missing = sorted(REQUIRED_DO_NOT_MAP_TO - actual)
    if missing:
        findings.append("limitations.do_not_map_to:MISSING:" + ",".join(missing))


def compute_outcome(record: dict[str, Any], findings: list[str]) -> str:
    supported_claim = require_object(record, "supported_claim", findings)
    downstream = require_object(record, "downstream_consumption", findings)

    claim_id = supported_claim.get("claim_id")
    relied_claim_ids = downstream.get("relied_claim_ids", [])
    if isinstance(claim_id, str) and isinstance(relied_claim_ids, list):
        if claim_id not in relied_claim_ids:
            findings.append("downstream_consumption.relied_claim_ids:SUPPORTED_CLAIM_NOT_RELIED")
    else:
        findings.append("downstream_consumption.relied_claim_ids:INVALID")

    non_claims = validate_non_claim_list("non_claims", require_array(record, "non_claims", findings), findings, require_nonempty=True)
    preserved = validate_non_claim_list(
        "downstream_consumption.preserved_non_claims",
        require_array(downstream, "preserved_non_claims", findings),
        findings,
    )
    dropped = validate_non_claim_list(
        "downstream_consumption.dropped_non_claims",
        require_array(downstream, "dropped_non_claims", findings),
        findings,
    )
    unresolved = validate_string_array(
        "downstream_consumption.unresolved_pointers",
        require_array(downstream, "unresolved_pointers", findings),
        findings,
    )

    non_claim_set = set(non_claims)
    preserved_set = set(preserved)
    dropped_set = set(dropped)

    unknown_preserved = sorted(preserved_set - non_claim_set)
    unknown_dropped = sorted(dropped_set - non_claim_set)
    if unknown_preserved:
        findings.append("downstream_consumption.preserved_non_claims:UNKNOWN:" + ",".join(unknown_preserved))
    if unknown_dropped:
        findings.append("downstream_consumption.dropped_non_claims:UNKNOWN:" + ",".join(unknown_dropped))

    overlap = sorted(preserved_set & dropped_set)
    if overlap:
        findings.append("downstream_consumption.non_claim_mapping:OVERLAP:" + ",".join(overlap))

    mapped = preserved_set | dropped_set
    missing_mapping = sorted(non_claim_set - mapped)
    if missing_mapping:
        findings.append("downstream_consumption.non_claim_mapping:INCOMPLETE:" + ",".join(missing_mapping))
        return "MAPPING_INCOMPLETE"

    if dropped:
        return "NON_CLAIM_DROPPED"

    added_claims = require_array(downstream, "consumer_added_claims", findings)
    if added_claims:
        missing_authority = False
        for idx, claim in enumerate(added_claims):
            if not isinstance(claim, dict):
                findings.append(f"downstream_consumption.consumer_added_claims[{idx}]:REQUIRED_OBJECT")
                missing_authority = True
                continue
            if not is_non_empty_string(claim.get("claim")):
                findings.append(f"downstream_consumption.consumer_added_claims[{idx}].claim:REQUIRED_NON_EMPTY_STRING")
                missing_authority = True
            if not is_non_empty_string(claim.get("authority_ref")):
                findings.append(f"downstream_consumption.consumer_added_claims[{idx}].authority_ref:REQUIRED_FOR_EXPANSION")
                missing_authority = True
            evidence_refs = claim.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not validate_string_array(
                f"downstream_consumption.consumer_added_claims[{idx}].evidence_refs",
                evidence_refs if isinstance(evidence_refs, list) else [],
                findings,
                require_nonempty=True,
            ):
                findings.append(f"downstream_consumption.consumer_added_claims[{idx}].evidence_refs:REQUIRED_FOR_EXPANSION")
                missing_authority = True
        if missing_authority:
            return "EXPANSION_AUTHORITY_REF_MISSING"
        return "BOUNDARY_EXPANSION_DETECTED"

    if unresolved:
        return "POINTER_UNRESOLVED"

    return "BOUNDARY_PRESERVED"


def validate_record(record: dict[str, Any]) -> tuple[bool, str, list[str]]:
    findings: list[str] = []

    if record.get("artifact_type") != ARTIFACT_TYPE:
        findings.append("artifact_type:INVALID")
    if record.get("artifact_version") != ARTIFACT_VERSION:
        findings.append("artifact_version:INVALID")
    if not isinstance(record.get("use_case_id"), str) or not USE_CASE_ID_RE.match(record.get("use_case_id", "")):
        findings.append("use_case_id:INVALID")
    if not is_non_empty_string(record.get("title")):
        findings.append("title:REQUIRED_NON_EMPTY_STRING")
    if record.get("field") not in FIELDS:
        findings.append("field:INVALID")
    if not isinstance(record.get("synthetic"), bool):
        findings.append("synthetic:REQUIRED_BOOLEAN")
    if record.get("field") == "HEALTHCARE_PRIOR_AUTH_SYNTHETIC" and record.get("synthetic") is not True:
        findings.append("synthetic:REQUIRED_TRUE_FOR_HEALTHCARE_PRIOR_AUTH_SYNTHETIC")
    if record.get("fork_role") != FORK_ROLE:
        findings.append("fork_role:INVALID")

    source_event = require_object(record, "source_event", findings)
    if source_event:
        for key in ["event_id", "producer", "event_type", "timestamp"]:
            require_string(source_event, key, findings, f"source_event.{key}")
        validate_string_array("source_event.artifact_refs", require_array(source_event, "artifact_refs", findings), findings, require_nonempty=True)

    supported_claim = require_object(record, "supported_claim", findings)
    if supported_claim:
        require_string(supported_claim, "claim_id", findings, "supported_claim.claim_id")
        require_string(supported_claim, "statement", findings, "supported_claim.statement")
        validate_string_array("supported_claim.evidence_refs", require_array(supported_claim, "evidence_refs", findings), findings, require_nonempty=True)

    downstream = require_object(record, "downstream_consumption", findings)
    if downstream:
        require_string(downstream, "consumer_identity", findings, "downstream_consumption.consumer_identity")
        require_string(downstream, "consumed_as", findings, "downstream_consumption.consumed_as")
        validate_string_array("downstream_consumption.relied_claim_ids", require_array(downstream, "relied_claim_ids", findings), findings, require_nonempty=True)

    boundary_result = require_object(record, "boundary_result", findings)
    declared_outcome = boundary_result.get("outcome") if boundary_result else None
    if declared_outcome not in OUTCOMES:
        findings.append("boundary_result.outcome:INVALID")
        declared_outcome = "INVALID"
    if boundary_result.get("structural_verification_scope") != STRUCTURAL_SCOPE:
        findings.append("boundary_result.structural_verification_scope:INVALID")
    require_array(boundary_result, "findings", findings)

    limitations = require_object(record, "limitations", findings)
    if limitations:
        validate_limitations(limitations, findings)

    public_language = require_object(record, "public_language", findings)
    if public_language:
        require_string(public_language, "clean_boundary_sentence", findings, "public_language.clean_boundary_sentence")
        validate_string_array("public_language.prohibited_readings", require_array(public_language, "prohibited_readings", findings), findings, require_nonempty=True)

    require_string(record, "created_at", findings)

    computed = compute_outcome(record, findings)
    if declared_outcome != computed:
        findings.append(f"boundary_result.outcome:MISMATCH_DECLARED_{declared_outcome}_COMPUTED_{computed}")

    return not findings, computed, findings


def build_output(path: Path, ok: bool, declared: str | None, computed: str | None, findings: list[str]) -> dict[str, Any]:
    boundary_preserved = ok and computed == "BOUNDARY_PRESERVED"
    outcome_requires_review = computed != "BOUNDARY_PRESERVED"
    return {
        "limitations": {
            "limitations_code": "FORK_USE_CASE_BOUNDARY_CHECKER_LIMITATIONS_v0_1_1",
            "checker_semantics_version": CHECKER_SEMANTICS_VERSION,
            "scope": STRUCTURAL_SCOPE,
            "does_not_validate_truth": True,
            "does_not_validate_safety": True,
            "does_not_validate_compliance": True,
            "does_not_validate_legal_sufficiency": True,
            "does_not_validate_approval": True,
            "automation_interpretation_required": True,
            "do_not_map_to": sorted(REQUIRED_DO_NOT_MAP_TO),
        },
        "result": {
            "artifact_path": str(path),
            "ok": ok,
            "boundary_preserved": boundary_preserved,
            "outcome_requires_review": outcome_requires_review,
            "review_reason": OUTCOME_REVIEW_REASONS.get(computed, "UNKNOWN_OR_INVALID_OUTCOME_REQUIRES_REVIEW"),
            "result_semantics": "ok means structurally valid and interpretable only; boundary_preserved is the machine-readable preserved-boundary signal; no result field is an approval, compliance, safety, legal-sufficiency, control-effectiveness, risk-acceptance, or truth verdict.",
            "declared_outcome": declared,
            "computed_outcome": computed,
            "findings": findings,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Fork use case boundary record v0.1")
    parser.add_argument("path", help="Path to a Fork use case boundary JSON record")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args(argv)

    path = Path(args.path)
    record, load_findings = load_json(path)
    if record is None:
        output = build_output(path, False, None, None, load_findings)
        print(json.dumps(output, sort_keys=True, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
        return 1

    ok, computed, findings = validate_record(record)
    declared = None
    if isinstance(record.get("boundary_result"), dict):
        declared = record["boundary_result"].get("outcome")
    output = build_output(path, ok, declared, computed, findings)
    print(json.dumps(output, sort_keys=True, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())