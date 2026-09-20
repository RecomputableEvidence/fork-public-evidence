#!/usr/bin/env python3
"""Bounded semantic-standing promotion checker candidate v0.1.1 repair.

FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001

The checker evaluates only normalized assertions supplied in a source-bound sidecar.
It does not infer arbitrary prose semantics, adjudicate standing, or mutate source bytes.

v0.1.1 repair boundaries:
  REGISTRY_FIELD_ASSERTED != FIELD_VERIFIED
  STANDING_ENVELOPE_ENTRY != STANDING_PROOF
  EVIDENCE_HASH_MATCH != EVIDENCE_ROLE_SUBJECT_STATUS_MATCH
  SUPERSEDING_TRANSITION_DECLARED != SUPERSEDING_TRANSITION_VERIFIED
  BASIS_REFERENCE_PRESENT != BASIS_VERIFIED
  SOURCE_BOUND_NORMALIZATION != COMPLETE_SOURCE_SEMANTIC_COVERAGE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PASS = "PASS"
WITHHOLD = "WITHHOLD"
INDETERMINATE = "INDETERMINATE"

SUPPORTED_TRANSITION = "SUPPORTED_WITHIN_DECLARED_TRANSITION"
SUPPORTED_ENVELOPE = "SUPPORTED_WITHIN_VERIFIED_ENVELOPE"
WITHHOLD_PROMOTION = "WITHHOLD_UNSUPPORTED_PROMOTION"
WITHHOLD_SCOPE = "WITHHOLD_OUTSIDE_SCOPE"
WITHHOLD_DIMENSION = "WITHHOLD_DIMENSION_MISMATCH"
WITHHOLD_SUBJECT = "WITHHOLD_SUBJECT_MISMATCH"
INDET_EVIDENCE = "INDETERMINATE_UNRESOLVED_EVIDENCE"
INDET_TIME = "INDETERMINATE_TEMPORAL_ANCHOR"
INDET_CONFLICT = "INDETERMINATE_CONFLICTING_TRANSITIONS"
INDET_CONTRACT = "INDETERMINATE_SCHEMA_OR_CONTRACT"
INDET_NORMALIZATION = "INDETERMINATE_NORMALIZATION_COVERAGE"

PROMOTION_CLASSES = {
    "ESTABLISHMENT_PROMOTION",
    "CANONICALITY_PROMOTION",
    "VALIDATION_PROMOTION",
    "GENERALIZATION_PROMOTION",
    "AUTHORITY_PROMOTION",
    "CROSS_OBJECT_PROMOTION",
    "TEMPORAL_PROMOTION",
    "MATURITY_PROMOTION",
    "CONSEQUENCE_PROMOTION",
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class CheckerError(RuntimeError):
    pass


@dataclass(frozen=True)
class SubjectIdentity:
    object_id: str
    version: str
    sha256: str

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SubjectIdentity":
        require_exact_keys(value, {"object_id", "version", "sha256"}, set(), "subject_identity")
        sha = str(value["sha256"])
        if not SHA256_RE.fullmatch(sha):
            raise CheckerError("subject_identity.sha256 must be 64 hex characters")
        return cls(str(value["object_id"]), str(value["version"]), sha.lower())


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise CheckerError(f"expected JSON object: {path}")
    return value


def require_exact_keys(value: Any, required: set[str], optional: set[str], ctx: str) -> None:
    if not isinstance(value, dict):
        raise CheckerError(f"{ctx} must be an object")
    missing = required - set(value)
    extra = set(value) - required - optional
    if missing:
        raise CheckerError(f"{ctx} missing required keys: {sorted(missing)}")
    if extra:
        raise CheckerError(f"{ctx} contains unsupported keys: {sorted(extra)}")


def require_nonempty_string(value: Any, ctx: str) -> str:
    if not isinstance(value, str) or not value:
        raise CheckerError(f"{ctx} must be a non-empty string")
    return value


def parse_time(value: str | None) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise CheckerError("timestamp must be string or null")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise CheckerError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(timezone.utc)


def same_subject(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return SubjectIdentity.from_mapping(left) == SubjectIdentity.from_mapping(right)


def scope_key(value: dict[str, Any]) -> tuple[str, str, str, str]:
    require_exact_keys(
        value,
        {"subject_object_id", "dimension", "surface", "claim"},
        set(),
        "scope_coordinate",
    )
    return (
        require_nonempty_string(value["subject_object_id"], "scope.subject_object_id"),
        require_nonempty_string(value["dimension"], "scope.dimension"),
        require_nonempty_string(value["surface"], "scope.surface"),
        require_nonempty_string(value["claim"], "scope.claim"),
    )


def scope_is_covered(asserted: Iterable[dict[str, Any]], allowed: Iterable[dict[str, Any]]) -> bool:
    return {scope_key(x) for x in asserted}.issubset({scope_key(x) for x in allowed})


def temporal_anchor_value(assertion: dict[str, Any]) -> tuple[str | None, bool, str]:
    anchor = assertion["temporal_anchor"]
    require_exact_keys(
        anchor,
        {"value", "source_class", "verification_status"},
        {"evidence_ref"},
        "temporal_anchor",
    )
    source_class = anchor["source_class"]
    if source_class not in {
        "EXPLICIT_SOURCE",
        "SOURCE_METADATA",
        "REVIEWER_SUPPLIED",
        "INFERRED",
        "ABSENT",
        "AMBIGUOUS",
    }:
        raise CheckerError(f"unsupported temporal source_class: {source_class}")
    verified = (
        anchor["verification_status"] == "VERIFIED"
        and source_class in {"EXPLICIT_SOURCE", "SOURCE_METADATA", "REVIEWER_SUPPLIED"}
        and anchor["value"] is not None
    )
    return anchor["value"], verified, source_class


def temporal_in_window(anchor: str, start: str, end: str | None) -> bool:
    t_anchor = parse_time(anchor)
    t_start = parse_time(start)
    t_end = parse_time(end)
    if t_anchor is None or t_start is None:
        return False
    if t_anchor < t_start:
        return False
    return t_end is None or t_anchor <= t_end


def safe_resolve(base: Path, relative_path: str) -> Path:
    root = base.resolve()
    candidate = (base / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise CheckerError(f"evidence path escapes registry directory: {relative_path}") from exc
    return candidate


def validate_evidence_binding(binding: dict[str, Any]) -> None:
    require_exact_keys(
        binding,
        {"evidence_id", "role", "artifact", "sha256", "subject_identity"},
        set(),
        "evidence_binding",
    )
    for key in ("evidence_id", "role", "artifact"):
        require_nonempty_string(binding[key], f"evidence_binding.{key}")
    if not SHA256_RE.fullmatch(str(binding["sha256"])):
        raise CheckerError("evidence_binding.sha256 must be 64 hex characters")
    SubjectIdentity.from_mapping(binding["subject_identity"])


def validate_evidence_registry(doc: dict[str, Any]) -> None:
    require_exact_keys(doc, {"registry_id", "evidence"}, set(), "evidence_registry")
    require_nonempty_string(doc["registry_id"], "evidence_registry.registry_id")
    if not isinstance(doc["evidence"], list):
        raise CheckerError("evidence_registry.evidence must be an array")
    seen: set[str] = set()
    for idx, item in enumerate(doc["evidence"]):
        require_exact_keys(
            item,
            {"evidence_id", "artifact", "path", "sha256", "role", "subject_identity", "status"},
            set(),
            f"evidence[{idx}]",
        )
        for key in ("evidence_id", "artifact", "path", "role"):
            require_nonempty_string(item[key], f"evidence[{idx}].{key}")
        if item["evidence_id"] in seen:
            raise CheckerError(f"duplicate evidence_id: {item['evidence_id']}")
        seen.add(item["evidence_id"])
        if not SHA256_RE.fullmatch(str(item["sha256"])):
            raise CheckerError(f"evidence[{idx}].sha256 must be 64 hex characters")
        SubjectIdentity.from_mapping(item["subject_identity"])
        if item["status"] not in {"PRESENT", "UNAVAILABLE", "SUPERSEDED", "UNKNOWN"}:
            raise CheckerError(f"unsupported evidence status: {item['status']}")


def validate_scope_coordinate(value: dict[str, Any]) -> None:
    scope_key(value)


def validate_non_effect(value: dict[str, Any]) -> None:
    require_exact_keys(value, {"coordinate", "promotion_class"}, set(), "non_effect")
    validate_scope_coordinate(value["coordinate"])
    if value["promotion_class"] not in PROMOTION_CLASSES:
        raise CheckerError(f"unsupported promotion class: {value['promotion_class']}")


def validate_fact(
    value: dict[str, Any],
    ctx: str,
    allowed_statuses: set[str],
    time_fields: set[str],
) -> None:
    required = {"asserted_status", "verification_status", "evidence_bindings"} | time_fields
    require_exact_keys(value, required, set(), ctx)
    if value["asserted_status"] not in allowed_statuses:
        raise CheckerError(f"unsupported {ctx}.asserted_status: {value['asserted_status']}")
    if value["verification_status"] not in {"VERIFIED", "UNVERIFIED", "UNKNOWN"}:
        raise CheckerError(f"unsupported {ctx}.verification_status")
    if not isinstance(value["evidence_bindings"], list) or not value["evidence_bindings"]:
        raise CheckerError(f"{ctx}.evidence_bindings must be a non-empty array")
    for binding in value["evidence_bindings"]:
        validate_evidence_binding(binding)
    for field in time_fields:
        if value[field] is not None:
            parse_time(value[field])


def validate_transition_registry(doc: dict[str, Any]) -> None:
    require_exact_keys(doc, {"registry_id", "transitions"}, set(), "transition_registry")
    require_nonempty_string(doc["registry_id"], "transition_registry.registry_id")
    if not isinstance(doc["transitions"], list):
        raise CheckerError("transition_registry.transitions must be an array")
    seen: set[str] = set()
    for idx, transition in enumerate(doc["transitions"]):
        ctx = f"transition[{idx}]"
        require_exact_keys(
            transition,
            {
                "transition_id",
                "subject_identity",
                "transition_dimension",
                "transition_basis",
                "from_state",
                "to_state",
                "authorization",
                "occurrence",
                "effectivity",
                "evidence_bindings",
                "scope",
            },
            set(),
            ctx,
        )
        for key in ("transition_id", "transition_dimension", "from_state", "to_state"):
            require_nonempty_string(transition[key], f"{ctx}.{key}")
        if transition["transition_id"] in seen:
            raise CheckerError(f"duplicate transition_id: {transition['transition_id']}")
        seen.add(transition["transition_id"])
        SubjectIdentity.from_mapping(transition["subject_identity"])

        validate_fact(
            transition["authorization"],
            f"{ctx}.authorization",
            {"AUTHORIZED", "NOT_AUTHORIZED", "UNKNOWN"},
            {"authorized_at"},
        )
        validate_fact(
            transition["occurrence"],
            f"{ctx}.occurrence",
            {"OCCURRED", "NOT_OCCURRED", "UNKNOWN"},
            {"occurred_at"},
        )
        validate_fact(
            transition["effectivity"],
            f"{ctx}.effectivity",
            {"EFFECTIVE", "NOT_EFFECTIVE", "TERMINATED", "UNKNOWN"},
            {"effective_from", "effective_until"},
        )

        if not isinstance(transition["evidence_bindings"], list) or not transition["evidence_bindings"]:
            raise CheckerError(f"{ctx}.evidence_bindings must be non-empty")
        for binding in transition["evidence_bindings"]:
            validate_evidence_binding(binding)

        basis = transition["transition_basis"]
        require_exact_keys(
            basis,
            {"type", "evidence_bindings"},
            {"authority_ref", "rule_id", "premise_set_ref"},
            f"{ctx}.transition_basis",
        )
        basis_type = basis["type"]
        if basis_type not in {
            "MECHANICALLY_DERIVED",
            "AUTHORIZED_CONSTITUTIVE_ACT",
            "ADJUDICATED",
            "EXTERNALLY_OBSERVED",
            "CONTRACTUALLY_MATURED",
        }:
            raise CheckerError(f"unsupported transition basis: {basis_type}")
        if basis_type == "MECHANICALLY_DERIVED":
            for key in ("authority_ref", "rule_id", "premise_set_ref"):
                require_nonempty_string(basis.get(key), f"{ctx}.transition_basis.{key}")
        if basis_type in {"AUTHORIZED_CONSTITUTIVE_ACT", "ADJUDICATED"}:
            require_nonempty_string(basis.get("authority_ref"), f"{ctx}.transition_basis.authority_ref")
        if not isinstance(basis["evidence_bindings"], list) or not basis["evidence_bindings"]:
            raise CheckerError(f"{ctx}.transition_basis.evidence_bindings must be non-empty")
        for binding in basis["evidence_bindings"]:
            validate_evidence_binding(binding)

        scope = transition["scope"]
        require_exact_keys(scope, {"applies_to", "explicit_non_effects"}, set(), f"{ctx}.scope")
        if not isinstance(scope["applies_to"], list) or not scope["applies_to"]:
            raise CheckerError(f"{ctx}.scope.applies_to must be non-empty")
        for coordinate in scope["applies_to"]:
            validate_scope_coordinate(coordinate)
        if not isinstance(scope["explicit_non_effects"], list):
            raise CheckerError(f"{ctx}.scope.explicit_non_effects must be an array")
        for item in scope["explicit_non_effects"]:
            validate_non_effect(item)


def validate_standing_envelope(doc: dict[str, Any]) -> None:
    require_exact_keys(doc, {"envelope_id", "subjects"}, set(), "standing_envelope")
    require_nonempty_string(doc["envelope_id"], "standing_envelope.envelope_id")
    if not isinstance(doc["subjects"], list) or not doc["subjects"]:
        raise CheckerError("standing_envelope.subjects must be a non-empty array")
    seen: set[SubjectIdentity] = set()
    for idx, subject in enumerate(doc["subjects"]):
        require_exact_keys(subject, {"subject_identity", "dimensions"}, set(), f"subject[{idx}]")
        identity = SubjectIdentity.from_mapping(subject["subject_identity"])
        if identity in seen:
            raise CheckerError(f"duplicate standing subject: {identity}")
        seen.add(identity)
        if not isinstance(subject["dimensions"], dict) or not subject["dimensions"]:
            raise CheckerError(f"subject[{idx}].dimensions must be a non-empty object")
        for name, dimension in subject["dimensions"].items():
            require_nonempty_string(name, "dimension name")
            require_exact_keys(
                dimension,
                {
                    "current_state",
                    "verification_status",
                    "effective_from",
                    "effective_until",
                    "evidence_bindings",
                    "applies_to",
                    "explicit_non_effects",
                },
                set(),
                f"dimension[{name}]",
            )
            require_nonempty_string(dimension["current_state"], f"dimension[{name}].current_state")
            if dimension["verification_status"] not in {"VERIFIED", "UNVERIFIED", "UNKNOWN"}:
                raise CheckerError(f"dimension[{name}].verification_status invalid")
            parse_time(dimension["effective_from"])
            if dimension["effective_until"] is not None:
                parse_time(dimension["effective_until"])
            if not isinstance(dimension["evidence_bindings"], list) or not dimension["evidence_bindings"]:
                raise CheckerError(f"dimension[{name}].evidence_bindings must be non-empty")
            for binding in dimension["evidence_bindings"]:
                validate_evidence_binding(binding)
            if not isinstance(dimension["applies_to"], list) or not dimension["applies_to"]:
                raise CheckerError(f"dimension[{name}].applies_to must be non-empty")
            for coordinate in dimension["applies_to"]:
                validate_scope_coordinate(coordinate)
            if not isinstance(dimension["explicit_non_effects"], list):
                raise CheckerError(f"dimension[{name}].explicit_non_effects must be an array")
            for item in dimension["explicit_non_effects"]:
                validate_non_effect(item)


def validate_assertion_doc(doc: dict[str, Any]) -> None:
    require_exact_keys(
        doc,
        {"source_sha256", "normalization_provenance", "assertions"},
        set(),
        "normalized_assertions",
    )
    if not SHA256_RE.fullmatch(str(doc["source_sha256"])):
        raise CheckerError("normalized_assertions.source_sha256 must be 64 hex characters")
    provenance = doc["normalization_provenance"]
    require_exact_keys(
        provenance,
        {"normalizer_id", "method", "authority", "coverage_status"},
        {"reviewer_ref"},
        "normalization_provenance",
    )
    require_nonempty_string(provenance["normalizer_id"], "normalization_provenance.normalizer_id")
    require_nonempty_string(provenance["method"], "normalization_provenance.method")
    if provenance["authority"] != "DESCRIPTIVE_MAPPING_ONLY":
        raise CheckerError("normalization authority must be DESCRIPTIVE_MAPPING_ONLY")
    if provenance["coverage_status"] not in {"PARTIAL", "COMPLETE_CLAIMED", "UNKNOWN"}:
        raise CheckerError("unsupported normalization coverage_status")
    if not isinstance(doc["assertions"], list) or not doc["assertions"]:
        raise CheckerError("normalized_assertions.assertions must be non-empty")
    seen: set[str] = set()
    for idx, assertion in enumerate(doc["assertions"]):
        require_exact_keys(
            assertion,
            {
                "assertion_id",
                "exact_text",
                "subject_identity",
                "transition_dimension",
                "asserted_state",
                "temporal_anchor",
                "scope",
            },
            set(),
            f"assertion[{idx}]",
        )
        for key in ("assertion_id", "exact_text", "transition_dimension", "asserted_state"):
            require_nonempty_string(assertion[key], f"assertion[{idx}].{key}")
        if assertion["assertion_id"] in seen:
            raise CheckerError(f"duplicate assertion_id: {assertion['assertion_id']}")
        seen.add(assertion["assertion_id"])
        SubjectIdentity.from_mapping(assertion["subject_identity"])
        temporal_anchor_value(assertion)
        if not isinstance(assertion["scope"], list) or not assertion["scope"]:
            raise CheckerError(f"assertion[{idx}].scope must be non-empty")
        for coordinate in assertion["scope"]:
            validate_scope_coordinate(coordinate)


def verify_evidence_bindings(
    bindings: list[dict[str, Any]],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
    expected_subject: dict[str, Any],
) -> tuple[bool, list[dict[str, Any]]]:
    records = evidence_registry["evidence"]
    results: list[dict[str, Any]] = []
    all_ok = True

    for binding in bindings:
        validate_evidence_binding(binding)
        binding_subject_ok = same_subject(binding["subject_identity"], expected_subject)
        candidates = [
            item
            for item in records
            if item["evidence_id"] == binding["evidence_id"]
            and item["artifact"] == binding["artifact"]
            and item["role"] == binding["role"]
            and str(item["sha256"]).lower() == str(binding["sha256"]).lower()
            and same_subject(item["subject_identity"], binding["subject_identity"])
            and item["status"] == "PRESENT"
        ]
        if not binding_subject_ok or len(candidates) != 1:
            all_ok = False
            results.append(
                {
                    "evidence_id": binding["evidence_id"],
                    "artifact": binding["artifact"],
                    "role": binding["role"],
                    "expected_sha256": str(binding["sha256"]).lower(),
                    "binding_subject_match": binding_subject_ok,
                    "status": "EVIDENCE_BINDING_NOT_VERIFIED",
                    "matches": len(candidates),
                }
            )
            continue

        record = candidates[0]
        path = safe_resolve(evidence_registry_path.parent, str(record["path"]))
        if not path.is_file():
            all_ok = False
            results.append(
                {
                    "evidence_id": binding["evidence_id"],
                    "artifact": binding["artifact"],
                    "role": binding["role"],
                    "status": "EVIDENCE_UNAVAILABLE",
                    "path": str(path),
                }
            )
            continue
        actual = sha256_file(path)
        expected = str(binding["sha256"]).lower()
        ok = actual == expected
        all_ok = all_ok and ok
        results.append(
            {
                "evidence_id": binding["evidence_id"],
                "artifact": binding["artifact"],
                "role": binding["role"],
                "expected_sha256": expected,
                "actual_sha256": actual,
                "status": "VERIFIED" if ok else "HASH_MISMATCH",
            }
        )
    return all_ok, results


def verified_fact_gate(
    gate_name: str,
    fact: dict[str, Any],
    required_status: str,
    transition_subject: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> tuple[dict[str, Any], bool]:
    declared = fact["asserted_status"] == required_status
    verified_status = fact["verification_status"] == "VERIFIED"
    evidence_ok, evidence_details = verify_evidence_bindings(
        fact["evidence_bindings"],
        evidence_registry,
        evidence_registry_path,
        transition_subject,
    )
    passed = declared and verified_status and evidence_ok
    return (
        {
            "gate": gate_name,
            "pass": passed,
            "details": {
                "required_asserted_status": required_status,
                "actual_asserted_status": fact["asserted_status"],
                "verification_status": fact["verification_status"],
                "evidence": evidence_details,
            },
        },
        passed,
    )


def basis_verified(
    transition: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> tuple[bool, dict[str, Any]]:
    basis = transition["transition_basis"]
    basis_type = basis["type"]
    required_roles = {
        "MECHANICALLY_DERIVED": {"AUTHORITY_BASIS", "RULE_DEFINITION", "PREMISE_SET"},
        "AUTHORIZED_CONSTITUTIVE_ACT": {"AUTHORITY_BASIS"},
        "ADJUDICATED": {"AUTHORITY_BASIS"},
        "EXTERNALLY_OBSERVED": {"OBSERVATION_BASIS"},
        "CONTRACTUALLY_MATURED": {"CONTRACT_BASIS"},
    }[basis_type]
    actual_roles = {binding["role"] for binding in basis["evidence_bindings"]}
    roles_ok = required_roles.issubset(actual_roles)
    evidence_ok, details = verify_evidence_bindings(
        basis["evidence_bindings"],
        evidence_registry,
        evidence_registry_path,
        transition["subject_identity"],
    )
    refs_ok = True
    if basis_type == "MECHANICALLY_DERIVED":
        refs_ok = all(basis.get(key) for key in ("authority_ref", "rule_id", "premise_set_ref"))
    elif basis_type in {"AUTHORIZED_CONSTITUTIVE_ACT", "ADJUDICATED"}:
        refs_ok = bool(basis.get("authority_ref"))
    return roles_ok and evidence_ok and refs_ok, {
        "basis_type": basis_type,
        "required_roles": sorted(required_roles),
        "actual_roles": sorted(actual_roles),
        "references_present": refs_ok,
        "evidence": details,
    }


def envelope_subject(envelope: dict[str, Any], subject: dict[str, Any]) -> dict[str, Any] | None:
    matches = [item for item in envelope["subjects"] if same_subject(item["subject_identity"], subject)]
    if len(matches) == 1:
        return matches[0]
    return None


def transition_candidates(
    registry: dict[str, Any], assertion: dict[str, Any], state_field: str
) -> list[dict[str, Any]]:
    return [
        transition
        for transition in registry["transitions"]
        if same_subject(transition["subject_identity"], assertion["subject_identity"])
        and transition["transition_dimension"] == assertion["transition_dimension"]
        and transition[state_field] == assertion["asserted_state"]
    ]


def explicit_non_effect_match(
    asserted_scope: list[dict[str, Any]], non_effects: list[dict[str, Any]]
) -> str | None:
    asserted = {scope_key(x) for x in asserted_scope}
    for item in non_effects:
        if scope_key(item["coordinate"]) in asserted:
            return item["promotion_class"]
    return None


def transition_core_gates(
    transition: dict[str, Any],
    assertion: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> list[dict[str, Any]]:
    gates: list[dict[str, Any]] = [
        {"gate": "G01_EXACT_SUBJECT", "pass": same_subject(transition["subject_identity"], assertion["subject_identity"])},
        {"gate": "G02_EXACT_DIMENSION", "pass": transition["transition_dimension"] == assertion["transition_dimension"]},
    ]
    g4, _ = verified_fact_gate(
        "G04_AUTHORIZATION_VERIFIED",
        transition["authorization"],
        "AUTHORIZED",
        transition["subject_identity"],
        evidence_registry,
        evidence_registry_path,
    )
    g5, _ = verified_fact_gate(
        "G05_OCCURRENCE_VERIFIED",
        transition["occurrence"],
        "OCCURRED",
        transition["subject_identity"],
        evidence_registry,
        evidence_registry_path,
    )
    g6, effectivity_ok = verified_fact_gate(
        "G06_EFFECTIVITY_VERIFIED",
        transition["effectivity"],
        "EFFECTIVE",
        transition["subject_identity"],
        evidence_registry,
        evidence_registry_path,
    )
    anchor, anchor_verified, anchor_class = temporal_anchor_value(assertion)
    temporal_ok = bool(
        effectivity_ok
        and anchor_verified
        and anchor is not None
        and transition["effectivity"]["effective_from"] is not None
        and temporal_in_window(
            anchor,
            transition["effectivity"]["effective_from"],
            transition["effectivity"]["effective_until"],
        )
    )
    g7 = {
        "gate": "G07_TEMPORAL_ALIGNMENT",
        "pass": temporal_ok,
        "details": {"anchor_source_class": anchor_class, "anchor_verified": anchor_verified},
    }
    g8_ok, g8_details = verify_evidence_bindings(
        transition["evidence_bindings"],
        evidence_registry,
        evidence_registry_path,
        transition["subject_identity"],
    )
    g8 = {"gate": "G08_TRANSITION_EVIDENCE", "pass": g8_ok, "details": g8_details}
    g9_ok = scope_is_covered(assertion["scope"], transition["scope"]["applies_to"])
    g9 = {"gate": "G09_SCOPE", "pass": g9_ok}
    non_effect_class = explicit_non_effect_match(assertion["scope"], transition["scope"]["explicit_non_effects"])
    g10 = {
        "gate": "G10_EXPLICIT_NON_EFFECTS",
        "pass": non_effect_class is None,
        "details": {"promotion_class": non_effect_class},
    }
    g11_ok, g11_details = basis_verified(transition, evidence_registry, evidence_registry_path)
    g11 = {"gate": "G11_BASIS_VERIFIED", "pass": g11_ok, "details": g11_details}
    gates.extend([g4, g5, g6, g7, g8, g9, g10, g11])
    return gates


def fully_verified_transition_for_assertion(
    transition: dict[str, Any],
    assertion: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> tuple[bool, list[dict[str, Any]]]:
    gates = transition_core_gates(transition, assertion, evidence_registry, evidence_registry_path)
    return all(gate["pass"] for gate in gates), gates


def verified_superseding_transitions(
    registry: dict[str, Any],
    assertion: dict[str, Any],
    evidence_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> list[dict[str, Any]]:
    verified: list[dict[str, Any]] = []
    for transition in transition_candidates(registry, assertion, "from_state"):
        ok, gates = fully_verified_transition_for_assertion(
            transition, assertion, evidence_registry, evidence_registry_path
        )
        if ok:
            verified.append({"transition": transition, "gates": gates})
    return verified


def finding(
    assertion_id: str,
    action: str,
    disposition: str,
    *,
    reason: str | None = None,
    promotion_class: str | None = None,
    matched_transition_id: str | None = None,
    matched_transition_ids: list[str] | None = None,
    gates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "assertion_id": assertion_id,
        "action": action,
        "disposition": disposition,
    }
    if reason is not None:
        out["reason"] = reason
    if promotion_class is not None:
        out["promotion_class"] = promotion_class
    if matched_transition_id is not None:
        out["matched_transition_id"] = matched_transition_id
    if matched_transition_ids is not None:
        out["matched_transition_ids"] = matched_transition_ids
    if gates is not None:
        out["gates"] = gates
    return out


def evaluate_assertion(
    assertion: dict[str, Any],
    envelope: dict[str, Any],
    evidence_registry: dict[str, Any],
    transition_registry: dict[str, Any],
    evidence_registry_path: Path,
) -> dict[str, Any]:
    assertion_id = assertion["assertion_id"]
    anchor, anchor_verified, _ = temporal_anchor_value(assertion)
    if not anchor_verified or anchor is None:
        return finding(
            assertion_id,
            INDETERMINATE,
            INDET_TIME,
            reason="temporal anchor is absent, ambiguous, inferred, or unverified",
        )

    subject_record = envelope_subject(envelope, assertion["subject_identity"])
    if subject_record is None:
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_SUBJECT,
            promotion_class="CROSS_OBJECT_PROMOTION",
            reason="exact subject identity not present uniquely in standing envelope",
        )

    dimension = subject_record["dimensions"].get(assertion["transition_dimension"])
    if dimension is None:
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_DIMENSION,
            promotion_class="AUTHORITY_PROMOTION",
            reason="asserted standing dimension is not declared for the exact subject",
        )

    superseding = verified_superseding_transitions(
        transition_registry, assertion, evidence_registry, evidence_registry_path
    )
    if superseding:
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_PROMOTION,
            promotion_class="TEMPORAL_PROMOTION",
            reason="asserted predecessor state is historical at the verified temporal anchor",
            matched_transition_ids=[x["transition"]["transition_id"] for x in superseding],
        )

    exact = transition_candidates(transition_registry, assertion, "to_state")
    verified_exact: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    failed_exact: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    for transition in exact:
        ok, gates = fully_verified_transition_for_assertion(
            transition, assertion, evidence_registry, evidence_registry_path
        )
        if ok:
            verified_exact.append((transition, gates))
        else:
            failed_exact.append((transition, gates))

    if len(verified_exact) > 1:
        return finding(
            assertion_id,
            INDETERMINATE,
            INDET_CONFLICT,
            reason="multiple independently verified exact transitions matched without a resolver",
            matched_transition_ids=[x[0]["transition_id"] for x in verified_exact],
        )
    if len(verified_exact) == 1:
        transition, gates = verified_exact[0]
        return finding(
            assertion_id,
            PASS,
            SUPPORTED_TRANSITION,
            matched_transition_id=transition["transition_id"],
            gates=gates,
        )
    if exact:
        for transition, gates in failed_exact:
            non_effect = next((g for g in gates if g["gate"] == "G10_EXPLICIT_NON_EFFECTS"), None)
            if non_effect and not non_effect["pass"]:
                return finding(
                    assertion_id,
                    WITHHOLD,
                    WITHHOLD_PROMOTION,
                    promotion_class=non_effect["details"]["promotion_class"],
                    reason="assertion intersects an explicit non-effect",
                    matched_transition_id=transition["transition_id"],
                    gates=gates,
                )
        unresolved_evidence = any(
            any(
                g["gate"] in {
                    "G04_AUTHORIZATION_VERIFIED",
                    "G05_OCCURRENCE_VERIFIED",
                    "G06_EFFECTIVITY_VERIFIED",
                    "G08_TRANSITION_EVIDENCE",
                    "G11_BASIS_VERIFIED",
                }
                and not g["pass"]
                for g in gates
            )
            for _, gates in failed_exact
        )
        if unresolved_evidence:
            return finding(
                assertion_id,
                INDETERMINATE,
                INDET_EVIDENCE,
                reason="declared transition exists but one or more evidentiary verification gates were not satisfied",
                matched_transition_ids=[x[0]["transition_id"] for x in failed_exact],
                gates=failed_exact[0][1] if len(failed_exact) == 1 else [],
            )
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_PROMOTION,
            promotion_class="ESTABLISHMENT_PROMOTION",
            reason="declared transition does not support the assertion within verified time/scope",
            matched_transition_ids=[x[0]["transition_id"] for x in failed_exact],
        )

    envelope_non_effect = explicit_non_effect_match(assertion["scope"], dimension["explicit_non_effects"])
    if envelope_non_effect is not None:
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_PROMOTION,
            promotion_class=envelope_non_effect,
            reason="assertion intersects an explicit standing-envelope non-effect",
        )
    envelope_scope = scope_is_covered(assertion["scope"], dimension["applies_to"])
    envelope_time = temporal_in_window(anchor, dimension["effective_from"], dimension["effective_until"])
    envelope_state = dimension["current_state"] == assertion["asserted_state"]
    envelope_declared_verified = dimension["verification_status"] == "VERIFIED"
    envelope_evidence_ok, envelope_evidence_details = verify_evidence_bindings(
        dimension["evidence_bindings"],
        evidence_registry,
        evidence_registry_path,
        assertion["subject_identity"],
    )

    if envelope_state and envelope_scope and envelope_time and envelope_declared_verified and envelope_evidence_ok:
        return finding(
            assertion_id,
            PASS,
            SUPPORTED_ENVELOPE,
            gates=[
                {"gate": "E01_ENVELOPE_STATE_ALIGNMENT", "pass": True},
                {"gate": "E02_ENVELOPE_VERIFICATION_STATUS", "pass": True},
                {"gate": "E03_ENVELOPE_EVIDENCE", "pass": True, "details": envelope_evidence_details},
                {"gate": "E04_ENVELOPE_TEMPORAL_ALIGNMENT", "pass": True},
                {"gate": "E05_ENVELOPE_SCOPE", "pass": True},
                {"gate": "E06_ENVELOPE_NON_EFFECTS", "pass": True},
            ],
        )

    if envelope_state and (not envelope_declared_verified or not envelope_evidence_ok):
        return finding(
            assertion_id,
            INDETERMINATE,
            INDET_EVIDENCE,
            reason="standing envelope declares the state but its verification/evidence binding is unresolved",
            gates=[
                {"gate": "E02_ENVELOPE_VERIFICATION_STATUS", "pass": envelope_declared_verified},
                {"gate": "E03_ENVELOPE_EVIDENCE", "pass": envelope_evidence_ok, "details": envelope_evidence_details},
            ],
        )
    if not envelope_scope:
        return finding(
            assertion_id,
            WITHHOLD,
            WITHHOLD_SCOPE,
            promotion_class="GENERALIZATION_PROMOTION",
            reason="asserted scope exceeds the verified subject/dimension envelope",
        )
    return finding(
        assertion_id,
        WITHHOLD,
        WITHHOLD_PROMOTION,
        promotion_class="ESTABLISHMENT_PROMOTION",
        reason="no verified transition or evidence-backed standing-envelope state supports the assertion",
    )


def preserve_output_cluster(
    output_dir: Path,
    source_path: Path,
    source_bytes: bytes,
    findings: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise CheckerError(f"output directory must be absent or empty: {output_dir}")
    source_dir = output_dir / "source"
    analysis_dir = output_dir / "analysis"
    disposition_dir = output_dir / "disposition"
    source_dir.mkdir(parents=True, exist_ok=True)
    analysis_dir.mkdir(parents=True, exist_ok=True)
    disposition_dir.mkdir(parents=True, exist_ok=True)

    preserved_source = source_dir / f"original_ai_output{source_path.suffix or '.txt'}"
    preserved_source.write_bytes(source_bytes)
    if preserved_source.read_bytes() != source_bytes:
        raise CheckerError("source preservation byte comparison failed")

    (analysis_dir / "promotion_findings.json").write_text(
        json.dumps(findings, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (analysis_dir / "promotion_receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (disposition_dir / "reviewer_decision.json").write_text(
        json.dumps(
            {
                "status": "PENDING_AUTHORIZED_DISPOSITION",
                "checker_did_not_adjudicate": True,
                "source_sha256": receipt["source_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--standing-envelope", required=True, type=Path)
    parser.add_argument("--evidence-registry", required=True, type=Path)
    parser.add_argument("--transition-registry", required=True, type=Path)
    parser.add_argument(
        "--assertions",
        type=Path,
        help="Source-bound normalized assertion sidecar. Omission remains INDETERMINATE.",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        source_bytes = args.source.read_bytes()
        source_sha = sha256_bytes(source_bytes)
        envelope = load_json(args.standing_envelope)
        evidence = load_json(args.evidence_registry)
        transitions = load_json(args.transition_registry)

        validate_standing_envelope(envelope)
        validate_evidence_registry(evidence)
        validate_transition_registry(transitions)

        if args.assertions is None:
            result = {
                "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
                "candidate_status": "NOT_EMPIRICALLY_QUALIFIED",
                "source_sha256": source_sha,
                "overall_action": INDETERMINATE,
                "source_assurance": "SUPPLIED_ASSERTIONS_ONLY",
                "reason": "normalized assertion extraction not supplied; checker will not infer semantics from arbitrary prose",
                "findings": [],
            }
        else:
            assertion_doc = load_json(args.assertions)
            validate_assertion_doc(assertion_doc)
            if assertion_doc["source_sha256"].lower() != source_sha:
                raise CheckerError("normalized assertion sidecar does not bind to source SHA-256")

            source_text = source_bytes.decode("utf-8")
            findings: list[dict[str, Any]] = []
            for assertion in assertion_doc["assertions"]:
                exact_text = assertion["exact_text"]
                if exact_text not in source_text:
                    findings.append(
                        finding(
                            assertion["assertion_id"],
                            INDETERMINATE,
                            INDET_NORMALIZATION,
                            reason="normalized assertion exact_text not found in preserved source",
                        )
                    )
                    continue
                findings.append(
                    evaluate_assertion(
                        assertion,
                        envelope,
                        evidence,
                        transitions,
                        args.evidence_registry,
                    )
                )

            actions = {item["action"] for item in findings}
            if WITHHOLD in actions:
                overall = WITHHOLD
            elif INDETERMINATE in actions:
                overall = INDETERMINATE
            else:
                overall = PASS

            result = {
                "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
                "candidate_status": "NOT_EMPIRICALLY_QUALIFIED",
                "source_sha256": source_sha,
                "overall_action": overall,
                "source_assurance": "SUPPLIED_ASSERTIONS_ONLY",
                "normalization_provenance": assertion_doc["normalization_provenance"],
                "findings": findings,
                "boundaries": [
                    "PROMOTION_DETECTED != SOURCE_REWRITTEN",
                    "CHECKER_FINDING != FINAL_SEMANTIC_ADJUDICATION",
                    "REGISTRY_ENTRY != PROOF_OF_TRANSITION",
                    "REGISTRY_FIELD_ASSERTED != FIELD_VERIFIED",
                    "SOURCE_BOUND_NORMALIZATION != COMPLETE_SOURCE_SEMANTIC_COVERAGE",
                ],
            }

        receipt = {
            "checker": "FORK-SEMANTIC-STANDING-PROMOTION-CHECKER-001",
            "candidate_version": "v0.1.1-repair",
            "executed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source_path": str(args.source),
            "source_sha256": source_sha,
            "standing_envelope_sha256": sha256_file(args.standing_envelope),
            "evidence_registry_sha256": sha256_file(args.evidence_registry),
            "transition_registry_sha256": sha256_file(args.transition_registry),
            "assertions_sha256": sha256_file(args.assertions) if args.assertions else None,
            "source_modified": False,
            "semantic_adjudication_authority": "NONE",
        }

        if args.output_dir:
            preserve_output_cluster(args.output_dir, args.source, source_bytes, result, receipt)

        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"{result['overall_action']}: semantic-standing promotion checker candidate v0.1.1 repair")
            for item in result.get("findings", []):
                print(f"- {item.get('assertion_id')}: {item.get('action')} {item.get('disposition')}")

        return 0 if result["overall_action"] == PASS else 2 if result["overall_action"] == WITHHOLD else 3

    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, CheckerError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
