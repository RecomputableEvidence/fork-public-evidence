#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = [
    "cbo_version",
    "cbo_id",
    "emitted_at",
    "issuer_system",
    "authority_domain",
    "stable_workload_id",
    "admission_decision_ref",
    "sc_declared_invariant_refs",
    "state_transition_refs",
    "execution_event_refs",
    "emitted_artifact_refs",
    "digest_seal_anchor_metadata",
    "preservation_refs",
    "recomputation_refs",
    "authority_boundary",
    "sc_claims",
    "sc_non_claims",
    "downstream_do_not_infer",
    "unresolved_or_excluded_refs",
]

CANONICAL_DO_NOT_INFER = [
    "GOVERNANCE_AUTHORITY",
    "ADMISSIBILITY_AUTHORITY",
    "AUTHORIZATION_AUTHORITY",
    "RUNTIME_CONTROL_AUTHORITY",
    "COMPLIANCE_APPROVAL",
    "SAFETY_APPROVAL",
    "CAUSAL_AUTHORITY",
    "ISSUER_GOVERNANCE_VALIDITY",
    "FORK_RUNTIME_PARTICIPATION",
]

CANONICAL_SC_NON_CLAIMS = [
    "This packet does not require Fork to validate SC governance authority.",
    "This packet does not grant Fork admission authority.",
    "This packet does not grant Fork authorization authority.",
    "This packet does not grant Fork safety authority.",
    "This packet does not grant Fork compliance authority.",
    "This packet does not grant Fork causal authority.",
]

VALID_STATUS_NORMALIZATION = {
    "absent": "ABSENT",
    "pending": "PENDING",
    "present": "PRESENT",
    "unresolved": "UNRESOLVED",
    "ABSENT": "ABSENT",
    "PENDING": "PENDING",
    "PRESENT": "PRESENT",
    "UNRESOLVED": "UNRESOLVED",
}

DISALLOWED_STATUS_VALUES = {
    "pending-or-present",
    "pending_or_present",
    "PENDING_OR_PRESENT",
    "PENDING-OR-PRESENT",
}

SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Duplicate JSON key detected: {key}")
        seen.add(key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("SC-native CBO packet JSON must be UTF-8 without BOM.")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    if not isinstance(data, dict):
        raise ValueError("SC-native CBO packet root must be a JSON object.")
    return data


def require_keys(data: dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_TOP_LEVEL if key not in data]
    if missing:
        raise ValueError(f"Missing required SC-native field(s): {', '.join(missing)}")


def require_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string.")
    return value


def require_array(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list):
        raise ValueError(f"{key} must be an array.")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{key} must contain only non-empty strings.")
    return value


def normalize_status(value: Any, field_path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_path} must be a non-empty string.")
    if value in DISALLOWED_STATUS_VALUES:
        raise ValueError(f"{field_path} cannot be ambiguous value: {value}")
    if value not in VALID_STATUS_NORMALIZATION:
        raise ValueError(f"{field_path} has unsupported status value: {value}")
    return VALID_STATUS_NORMALIZATION[value]


def normalize_digest_status(digest_value: Any) -> str:
    if digest_value is None or digest_value == "":
        return "NOT_PROVIDED"
    if isinstance(digest_value, str) and digest_value.lower() == "pending":
        return "PENDING"
    if isinstance(digest_value, str) and digest_value.lower() == "unresolved":
        return "UNRESOLVED"
    if isinstance(digest_value, str) and SHA256_HEX_RE.match(digest_value):
        return "PRESENT"
    return "UNRESOLVED"


def validate_authority_boundary(boundary: Any) -> dict[str, bool]:
    if not isinstance(boundary, dict):
        raise ValueError("authority_boundary must be an object.")

    required_false = [
        "authority_transfer",
        "fork_validates_sc_governance",
        "fork_validates_causality",
        "fork_participates_in_runtime_control",
    ]

    for key in required_false:
        if boundary.get(key) is not False:
            raise ValueError(f"authority_boundary.{key} must be false.")

    return boundary


def unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def normalize_sc_native_packet(native: dict[str, Any]) -> dict[str, Any]:
    require_keys(native)

    if native.get("cbo_version") != "0.1":
        raise ValueError("cbo_version must be 0.1.")

    metadata = native.get("digest_seal_anchor_metadata")
    if not isinstance(metadata, dict):
        raise ValueError("digest_seal_anchor_metadata must be an object.")

    boundary = validate_authority_boundary(native.get("authority_boundary"))

    sc_non_claims = require_array(native, "sc_non_claims")
    normalized_non_claims = unique_preserving_order(sc_non_claims + CANONICAL_SC_NON_CLAIMS)

    return {
        "profile_id": "CBO_MINIMUM_PACKET_REQUIREMENTS_v0_1",
        "cbo_version": native["cbo_version"],
        "cbo_id": require_string(native, "cbo_id"),
        "packet_id": f"fork-normalized-{require_string(native, 'cbo_id')}",
        "issuer_system": require_string(native, "issuer_system"),
        "authority_domain": require_string(native, "authority_domain"),
        "stable_workload_id": require_string(native, "stable_workload_id"),
        "emitted_at": require_string(native, "emitted_at"),
        "continuity_chain": {
            "admission_decision_ref": require_string(native, "admission_decision_ref"),
            "invariant_binding_refs": require_array(native, "sc_declared_invariant_refs"),
            "state_transition_refs": require_array(native, "state_transition_refs"),
            "execution_event_refs": require_array(native, "execution_event_refs"),
            "emitted_artifact_refs": require_array(native, "emitted_artifact_refs"),
        },
        "integrity_metadata": {
            "digest_algorithm": str(metadata.get("digest_algorithm", "")).lower().replace("-", ""),
            "digest_value": "" if metadata.get("digest_value") == "pending" else str(metadata.get("digest_value", "")),
            "digest_status": normalize_digest_status(metadata.get("digest_value")),
            "seal_status": normalize_status(metadata.get("seal_status"), "digest_seal_anchor_metadata.seal_status"),
            "anchor_status": normalize_status(metadata.get("anchor_status"), "digest_seal_anchor_metadata.anchor_status"),
            "anchor_refs": metadata.get("anchor_refs") if isinstance(metadata.get("anchor_refs"), list) else [],
        },
        "preservation_refs": require_array(native, "preservation_refs"),
        "recomputation_refs": require_array(native, "recomputation_refs"),
        "boundary_semantics": {
            "authority_transfer": boundary["authority_transfer"],
            "fork_validates_issuer_governance": boundary["fork_validates_sc_governance"],
            "fork_validates_causality": boundary["fork_validates_causality"],
            "fork_participates_in_runtime_control": boundary["fork_participates_in_runtime_control"],
            "fork_accepts_runtime_credentials": False,
            "fork_claims_control_path_authority": False,
            "issuer_invariant_refs_are_opaque_to_fork": True,
        },
        "issuer_claims": require_array(native, "sc_claims"),
        "issuer_non_claims": normalized_non_claims,
        "fork_permissions": [
            "preserve emitted continuity evidence",
            "recompute declared metadata when present",
            "compare preserved references",
            "report structural continuity loss",
            "identify missing unresolved or excluded references",
        ],
        "fork_restrictions": [
            "do not infer issuer governance authority",
            "do not infer admissibility authority",
            "do not infer authorization authority",
            "do not infer runtime control authority",
            "do not infer safety approval",
            "do not infer compliance approval",
            "do not infer causal authority beyond emitted continuity evidence",
            "do not validate semantic meaning of issuer-declared invariant references",
        ],
        "downstream_constraints": {
            "do_not_infer": CANONICAL_DO_NOT_INFER,
            "requires_human_or_institutional_interpretation": True,
        },
        "unresolved_or_excluded_refs": require_array(native, "unresolved_or_excluded_refs"),
        "expected_fork_evaluation": {
            "structural_continuity_test_only": True,
            "can_preserve": True,
            "can_compare": True,
            "can_report_continuity_loss": True,
            "can_recompute_when_metadata_present": True,
            "does_not_validate_issuer_governance": True,
            "does_not_validate_causality": True,
            "does_not_join_runtime_control_path": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize an SC-native CBO packet into Fork's CBO minimum packet envelope.")
    parser.add_argument("artifact", help="Path to SC-native CBO packet JSON.")
    parser.add_argument("--out", help="Write normalized CBO minimum packet JSON to this path.")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON to stdout when --out is not provided.")
    args = parser.parse_args()

    try:
        native = load_json(Path(args.artifact))
        normalized = normalize_sc_native_packet(native)
    except Exception as exc:
        error = {
            "ok": False,
            "computed_outcome": "SC_NATIVE_CBO_MAPPING_INPUT_ERROR",
            "artifact_path": args.artifact,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "limitations": {
                "scope": "SC_NATIVE_TO_FORK_CBO_NORMALIZATION_ONLY",
                "does_not_validate_sc_governance": True,
                "does_not_validate_causality": True,
                "does_not_validate_runtime_execution": True,
                "does_not_validate_invariant_meaning": True,
            },
        }
        print(json.dumps(error, sort_keys=True, separators=(",", ":")))
        return 2

    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({
            "ok": True,
            "computed_outcome": "SC_NATIVE_CBO_PACKET_NORMALIZED",
            "artifact_path": args.artifact,
            "normalized_output_path": str(output_path),
            "limitations": {
                "scope": "SC_NATIVE_TO_FORK_CBO_NORMALIZATION_ONLY",
                "does_not_validate_sc_governance": True,
                "does_not_validate_causality": True,
                "does_not_validate_runtime_execution": True,
                "does_not_validate_invariant_meaning": True,
            },
        }, sort_keys=True, separators=(",", ":")))
    else:
        if args.compact:
            print(json.dumps(normalized, sort_keys=True, separators=(",", ":")))
        else:
            print(json.dumps(normalized, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
