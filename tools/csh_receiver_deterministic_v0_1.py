#!/usr/bin/env python3
"""Deterministic boundary-preserving receiver for CSH v0.1."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

RECEIVER_ID = "csh_deterministic_boundary_preserver_v0_1"
RECEIVER_VERSION = "0.1.0"
RECEIVER_CLASS_ID = "deterministic_receiver"
OUTPUT_SCHEMA_VERSION = "v0.1"


class ReceiverInputError(ValueError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def parse_json_bytes(raw: bytes, label: str) -> Mapping[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ReceiverInputError(f"{label} must be UTF-8 without BOM")
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiverInputError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ReceiverInputError(f"{label} must be a JSON object")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReceiverInputError(f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str, min_items: int = 0) -> list[str]:
    if not isinstance(value, list):
        raise ReceiverInputError(f"{label} must be an array")
    result = [require_string(item, f"{label}[{i}]") for i, item in enumerate(value)]
    if len(result) < min_items:
        raise ReceiverInputError(f"{label} must contain at least {min_items} item(s)")
    return result


def require_object_list(value: Any, label: str) -> list[Mapping[str, Any]]:
    if not isinstance(value, list):
        raise ReceiverInputError(f"{label} must be an array")
    result: list[Mapping[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ReceiverInputError(f"{label}[{index}] must be an object")
        result.append(item)
    return result


def validate_claims(value: Any, label: str) -> list[dict[str, str]]:
    claims = require_object_list(value, label)
    if not claims:
        raise ReceiverInputError(f"{label} must contain at least one claim")
    seen: set[str] = set()
    result: list[dict[str, str]] = []
    for index, claim in enumerate(claims):
        claim_id = require_string(claim.get("claim_id"), f"{label}[{index}].claim_id")
        text = require_string(claim.get("text"), f"{label}[{index}].text")
        if claim_id in seen:
            raise ReceiverInputError(f"{label} contains duplicate claim_id {claim_id!r}")
        seen.add(claim_id)
        result.append({"claim_id": claim_id, "text": text})
    return result


def validate_scenario(value: Mapping[str, Any]) -> dict[str, Any]:
    required = (
        "scenario_id", "schema_version", "pressure_class", "source_claims",
        "source_non_claims", "expected_relationship", "permitted_transformations",
        "unresolved_references", "prohibited_outcomes",
    )
    missing = [name for name in required if name not in value]
    if missing:
        raise ReceiverInputError("scenario is missing: " + ", ".join(missing))
    version = require_string(value["schema_version"], "scenario.schema_version")
    if version != "v0.1":
        raise ReceiverInputError("scenario.schema_version must equal 'v0.1'")
    return {
        "scenario_id": require_string(value["scenario_id"], "scenario.scenario_id"),
        "schema_version": version,
        "pressure_class": require_string(value["pressure_class"], "scenario.pressure_class"),
        "source_claims": validate_claims(value["source_claims"], "scenario.source_claims"),
        "source_non_claims": require_string_list(
            value["source_non_claims"], "scenario.source_non_claims", 1
        ),
        "expected_relationship": require_string(
            value["expected_relationship"], "scenario.expected_relationship"
        ),
        "permitted_transformations": require_string_list(
            value["permitted_transformations"], "scenario.permitted_transformations"
        ),
        "unresolved_references": require_string_list(
            value["unresolved_references"], "scenario.unresolved_references"
        ),
        "prohibited_outcomes": require_string_list(
            value["prohibited_outcomes"], "scenario.prohibited_outcomes", 1
        ),
    }


def validate_handoff(
    value: Mapping[str, Any], expected_scenario_id: str
) -> dict[str, Any]:
    required = (
        "handoff_id", "schema_version", "scenario_id", "emitted_claims",
        "non_claims", "upstream_relationships", "authority_references",
        "evidence_references", "unresolved_state", "permitted_narrowing",
        "prohibited_inferences", "required_local_revalidation",
    )
    missing = [name for name in required if name not in value]
    if missing:
        raise ReceiverInputError("handoff is missing: " + ", ".join(missing))
    version = require_string(value["schema_version"], "handoff.schema_version")
    if version != "v0.1":
        raise ReceiverInputError("handoff.schema_version must equal 'v0.1'")
    scenario_id = require_string(value["scenario_id"], "handoff.scenario_id")
    if scenario_id != expected_scenario_id:
        raise ReceiverInputError("handoff.scenario_id does not match scenario.scenario_id")
    return {
        "handoff_id": require_string(value["handoff_id"], "handoff.handoff_id"),
        "schema_version": version,
        "scenario_id": scenario_id,
        "emitted_claims": validate_claims(value["emitted_claims"], "handoff.emitted_claims"),
        "non_claims": require_string_list(value["non_claims"], "handoff.non_claims", 1),
        "upstream_relationships": require_object_list(
            value["upstream_relationships"], "handoff.upstream_relationships"
        ),
        "authority_references": require_string_list(
            value["authority_references"], "handoff.authority_references"
        ),
        "evidence_references": require_string_list(
            value["evidence_references"], "handoff.evidence_references"
        ),
        "unresolved_state": require_string_list(
            value["unresolved_state"], "handoff.unresolved_state"
        ),
        "permitted_narrowing": require_string_list(
            value["permitted_narrowing"], "handoff.permitted_narrowing"
        ),
        "prohibited_inferences": require_string_list(
            value["prohibited_inferences"], "handoff.prohibited_inferences", 1
        ),
        "required_local_revalidation": require_string_list(
            value["required_local_revalidation"], "handoff.required_local_revalidation"
        ),
    }


def build_response(
    scenario: Mapping[str, Any],
    handoff: Mapping[str, Any] | None,
    *,
    scenario_sha256: str,
    handoff_sha256: str | None,
    receiver_source_sha256: str,
) -> dict[str, Any]:
    checked_scenario = validate_scenario(scenario)
    checked_handoff = (
        validate_handoff(handoff, checked_scenario["scenario_id"])
        if handoff is not None else None
    )

    if checked_handoff is None:
        claims = checked_scenario["source_claims"]
        non_claims = checked_scenario["source_non_claims"]
        unresolved = checked_scenario["unresolved_references"]
        prohibited = checked_scenario["prohibited_outcomes"]
        authority_references: list[str] = []
        evidence_references: list[str] = []
        local_revalidation: list[str] = []
        basis = "scenario_descriptor"
        condition = "control_h0"
    else:
        claims = checked_handoff["emitted_claims"]
        non_claims = checked_handoff["non_claims"]
        unresolved = checked_handoff["unresolved_state"]
        prohibited = checked_handoff["prohibited_inferences"]
        authority_references = checked_handoff["authority_references"]
        evidence_references = checked_handoff["evidence_references"]
        local_revalidation = checked_handoff["required_local_revalidation"]
        basis = "explicit_handoff_state_artifact"
        condition = "instrumented_h1"

    downstream_claims = [
        {
            "authority_references": [],
            "claim_id": f"DOWN_{claim['claim_id']}",
            "evidence_references": [],
            "new_boundary_contract_id": None,
            "relationship_to_source": "PRESERVED",
            "source_claim_id": claim["claim_id"],
            "text": claim["text"],
        }
        for claim in claims
    ]
    reference_resolutions = [
        {"reference_id": ref, "resolution_evidence": [], "status": "unresolved"}
        for ref in unresolved
    ]

    return {
        "condition": condition,
        "handoff_artifact_present": checked_handoff is not None,
        "input_basis": basis,
        "input_bindings": {
            "handoff_sha256": handoff_sha256,
            "scenario_sha256": scenario_sha256,
        },
        "preserved_context": {
            "authority_references": authority_references,
            "evidence_references": evidence_references,
            "prohibited_inferences": prohibited,
            "required_local_revalidation": local_revalidation,
        },
        "receiver_class_id": RECEIVER_CLASS_ID,
        "receiver_id": RECEIVER_ID,
        "receiver_source_sha256": receiver_source_sha256,
        "receiver_version": RECEIVER_VERSION,
        "response": {
            "aggregate_state": "bounded",
            "authority_inherited": False,
            "downstream_claims": downstream_claims,
            "evidence_promotions": [],
            "preserved_non_claims": non_claims,
            "reference_resolutions": reference_resolutions,
            "verification_upgrades": [],
        },
        "scenario_id": checked_scenario["scenario_id"],
        "schema_version": OUTPUT_SCHEMA_VERSION,
    }


def write_output(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(payload))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", type=Path)
    parser.add_argument("--handoff", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        scenario_raw = args.scenario.read_bytes()
        scenario = parse_json_bytes(scenario_raw, "scenario")
        handoff_raw = args.handoff.read_bytes() if args.handoff is not None else None
        handoff = (
            parse_json_bytes(handoff_raw, "handoff")
            if handoff_raw is not None else None
        )
        protected = {args.scenario.resolve(), Path(__file__).resolve()}
        if args.handoff is not None:
            protected.add(args.handoff.resolve())
        if args.output.resolve() in protected:
            raise ReceiverInputError("output path must not overwrite an input or source")
        result = build_response(
            scenario,
            handoff,
            scenario_sha256=sha256_bytes(scenario_raw),
            handoff_sha256=sha256_bytes(handoff_raw) if handoff_raw is not None else None,
            receiver_source_sha256=sha256_bytes(Path(__file__).read_bytes()),
        )
        write_output(args.output, result)
    except (OSError, ReceiverInputError) as exc:
        print(f"CSH_DETERMINISTIC_RECEIVER_ERROR: {exc}", file=sys.stderr)
        return 2
    print("CSH_DETERMINISTIC_RECEIVER_PASS")
    print(f"OUTPUT: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
