#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA_VERSION = "0.1"
TIER_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
METHOD_TIER = {
    "CHANNEL_NEGATIVE": "P0", "UNAVAILABLE": "P0",
    "DESCRIPTION": "P1", "SUMMARY": "P1", "QUOTATION": "P1", "REPORTED_OBSERVATION": "P1",
    "RENDERED_ARTIFACT": "P2", "PARTIAL_ARTIFACT": "P2", "INDEXED_ARTIFACT": "P2", "TRANSFORMED_ARTIFACT": "P2",
    "RAW_FILE_INSPECTION": "P3", "DIRECT_EXECUTION": "P4",
}
AUTHORIZED_ATTRIBUTION = {
    "ANONYMOUS_PUBLICATION", "NAMED_PARAPHRASE_AUTHORIZED", "NAMED_QUOTATION_AUTHORIZED",
    "NAMED_TECHNICAL_ATTRIBUTION_AUTHORIZED", "CO_DEVELOPED_ARTIFACT_ATTRIBUTION_AUTHORIZED",
}
REFERENCE_DEFECTS = {
    "BROKEN_REFERENCE", "UNRESOLVED_REFERENCE", "PARTICIPANT_CONTEXT_MISSING",
    "INTERACTION_PROVENANCE_MISSING", "ATTRIBUTION_NOT_AUTHORIZED", "EXTERNAL_CONTEXT_REFERENCE_MISSING",
}
SCHEMA_FILES = {
    "outcome": "experiment_outcome_record_v0_1.schema.json",
    "participant": "participant_context_receipt_v0_1.schema.json",
    "interaction": "interaction_provenance_record_v0_1.schema.json",
    "attribution": "attribution_authorization_record_v0_1.schema.json",
    "external": "external_context_reference_set_v0_1.schema.json",
    "profile": "provenance_profile_v0_1.schema.json",
    "registry": "experiment_meta_evidence_registry_v0_1.schema.json",
}


def add(defects: List[Dict[str, str]], code: str, path: str, detail: str) -> None:
    item = {"code": code, "path": path, "detail": detail}
    if item not in defects:
        defects.append(item)


def load_json(path: Path) -> Tuple[Optional[Any], List[Dict[str, str]]]:
    defects: List[Dict[str, str]] = []
    try:
        with path.open("r", encoding="utf-8-sig") as f:
            obj = json.load(f)
    except json.JSONDecodeError as exc:
        add(defects, "MALFORMED_JSON", "$", f"{exc.msg} at line {exc.lineno}, column {exc.colno}")
        return None, defects
    except OSError as exc:
        add(defects, "BROKEN_REFERENCE", "$", str(exc))
        return None, defects
    if not isinstance(obj, dict):
        add(defects, "NON_OBJECT_JSON", "$", "Top-level JSON value must be an object")
        return None, defects
    return obj, defects


def schema_path(repo_root: Path, kind: str) -> Path:
    return repo_root / "schemas" / SCHEMA_FILES[kind]


def type_ok(value: Any, expected: Any) -> bool:
    types = expected if isinstance(expected, list) else [expected]
    for t in types:
        if t == "null" and value is None:
            return True
        if t == "object" and isinstance(value, dict):
            return True
        if t == "array" and isinstance(value, list):
            return True
        if t == "string" and isinstance(value, str):
            return True
        if t == "integer" and isinstance(value, int) and not isinstance(value, bool):
            return True
        if t == "boolean" and isinstance(value, bool):
            return True
        if t == "number" and isinstance(value, (int, float)) and not isinstance(value, bool):
            return True
    return False


def simple_validate(instance: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    errors: List[str] = []
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
        return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} is not in enum")
    if "type" in schema and not type_ok(instance, schema["type"]):
        errors.append(f"{path}: expected type {schema['type']!r}")
        return errors
    if isinstance(instance, dict):
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}.{req}: required property missing")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}.{key}: additional property not allowed")
        for key, subschema in props.items():
            if key in instance:
                errors.extend(simple_validate(instance[key], subschema, f"{path}.{key}"))
    elif isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: minimum item count is {schema['minItems']}")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(v, sort_keys=True, ensure_ascii=False) for v in instance]
            if len(rendered) != len(set(rendered)):
                errors.append(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, value in enumerate(instance):
                errors.extend(simple_validate(value, item_schema, f"{path}[{idx}]"))
    elif isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: minimum length is {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path}: maximum length is {schema['maxLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: value does not match pattern")
        if schema.get("format") == "date-time":
            try:
                dt.datetime.fromisoformat(instance.replace("Z", "+00:00"))
            except ValueError:
                errors.append(f"{path}: invalid date-time")
    elif isinstance(instance, int) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{path}: minimum is {schema['minimum']}")
    return errors


def validate_schema(kind: str, obj: Dict[str, Any], repo_root: Path) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    sp = schema_path(repo_root, kind)
    try:
        with sp.open("r", encoding="utf-8-sig") as f:
            schema = json.load(f)
    except Exception as exc:
        add(defects, "BROKEN_REFERENCE", "$schema", f"Unable to load {sp}: {exc}")
        return defects
    try:
        import jsonschema  # type: ignore
        validator = jsonschema.Draft202012Validator(schema)
        for err in sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path)):
            p = "$" + "".join(f"[{i}]" if isinstance(i, int) else f".{i}" for i in err.absolute_path)
            add(defects, "REGISTRY_SCHEMA_FAILURE" if kind == "registry" else "SCHEMA_VALIDATION_FAILURE", p, err.message)
    except ImportError:
        for message in simple_validate(obj, schema):
            add(defects, "REGISTRY_SCHEMA_FAILURE" if kind == "registry" else "SCHEMA_VALIDATION_FAILURE", "$", message)
    return defects


def validate_outcome(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("record_id", "<unknown>"))
    basis = record.get("standing_basis") if isinstance(record.get("standing_basis"), dict) else {}
    if basis.get("derived_from_outcome_polarity") is True:
        add(defects, "POLARITY_STANDING_COLLAPSE", f"{rid}.standing_basis", "Evidence standing declares derivation from outcome polarity")
        if record.get("outcome_polarity") == "FAVORABLE":
            add(defects, "FAVORABLE_OUTCOME_AUTOMATICALLY_PROMOTED", f"{rid}.evidence_standing", "Favorable polarity cannot promote standing")
        if record.get("outcome_polarity") == "UNFAVORABLE":
            add(defects, "UNFAVORABLE_OUTCOME_AUTOMATICALLY_DEMOTED", f"{rid}.evidence_standing", "Unfavorable polarity cannot demote standing")
    if record.get("history_treatment") == "OVERWRITE":
        add(defects, "HISTORICAL_OUTCOME_OVERWRITTEN", f"{rid}.history_treatment", "Historical outcomes must be append-only or linked by correction/supersession")
    if record.get("history_treatment") in {"CORRECTION_WITH_LINEAGE", "SUPERSESSION_WITH_LINEAGE"} and not record.get("lineage"):
        add(defects, "MISSING_LINEAGE_EDGE", f"{rid}.lineage", "Correction or supersession requires a lineage edge")

    method = record.get("observation_method")
    tier = record.get("provenance_tier")
    expected = METHOD_TIER.get(method)
    if expected and tier != expected:
        add(defects, "PROVENANCE_TIER_OVERCLAIM", f"{rid}.provenance_tier", f"{method} maps to {expected}, not {tier}")
    assertion = record.get("observation_assertion_type")
    if tier == "P0" and assertion == "ABSENT":
        add(defects, "CHANNEL_NEGATIVE_TREATED_AS_ABSENCE", f"{rid}.observation_assertion_type", "P0 channel-negative evidence cannot establish absence")
    if assertion == "MECHANISM_BEHAVIOR" and TIER_RANK.get(str(tier), -1) < 3:
        add(defects, "MECHANISM_CLAIM_BELOW_RAW_FILE_FIDELITY", f"{rid}.provenance_tier", "Mechanism claims require at least P3 raw-file fidelity")
    if assertion == "EXECUTION_BEHAVIOR" and tier != "P4":
        add(defects, "EXECUTION_CLAIM_WITHOUT_P4", f"{rid}.provenance_tier", "Execution behavior claims require P4")
    if record.get("reproduction_status") in {"REPRODUCED", "FAILED_TO_REPRODUCE", "PARTIALLY_REPRODUCED"} and tier != "P4":
        add(defects, "EXECUTION_CLAIM_WITHOUT_P4", f"{rid}.reproduction_status", "Reproduction status requires P4 direct execution")

    supported = {str(x).upper() for x in record.get("supported_claims", [])}
    prohibited = {str(x).upper() for x in record.get("prohibited_inferences", [])}
    outcome_type = record.get("outcome_type")
    if outcome_type == "PROFESSIONAL_RECOGNITION":
        if "TECHNICAL_VALIDATION" in supported or "TECHNICAL_VALIDATION" not in prohibited:
            add(defects, "TECHNICAL_VALIDATION_INFERRED_FROM_RECOGNITION", f"{rid}.supported_claims", "Professional recognition must not establish technical validation")
    if outcome_type == "ATTRIBUTION_PERMISSION":
        if "ENDORSEMENT" in supported or "ENDORSEMENT" not in prohibited:
            add(defects, "ENDORSEMENT_INFERRED_FROM_PARTICIPATION", f"{rid}.supported_claims", "Attribution permission must not establish endorsement")
    if outcome_type == "COLLABORATION_INTEREST":
        if "PARTNERSHIP" in supported or "PARTNERSHIP" not in prohibited:
            add(defects, "ENDORSEMENT_INFERRED_FROM_PARTICIPATION", f"{rid}.supported_claims", "Collaboration interest must not establish partnership")
    if outcome_type == "COMMERCIAL_INTEREST":
        if "PRODUCT_MARKET_VALIDATION" in supported or "PRODUCT_MARKET_VALIDATION" not in prohibited:
            add(defects, "COMMERCIAL_INTEREST_INFERRED_AS_PRODUCT_VALIDATION", f"{rid}.supported_claims", "Commercial interest must not establish product-market validation")

    if record.get("source_relationship") == "PARTICIPANT":
        if not record.get("participant_context_id"):
            add(defects, "PARTICIPANT_CONTEXT_MISSING", f"{rid}.participant_context_id", "Participant-sourced outcome requires participant context")
        if not record.get("interaction_provenance_id"):
            add(defects, "INTERACTION_PROVENANCE_MISSING", f"{rid}.interaction_provenance_id", "Participant-sourced outcome requires interaction provenance")
    if record.get("public_use_status") == "PUBLIC_NAMED" and not record.get("attribution_authorization_id"):
        add(defects, "ATTRIBUTION_NOT_AUTHORIZED", f"{rid}.attribution_authorization_id", "Named public use requires attribution authorization")
    return defects


def validate_participant(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("participant_context_id", "<unknown>"))
    if record.get("participant_identifier_type") == "ANONYMOUS" and record.get("participant_identifier") not in (None, ""):
        add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.participant_identifier", "Anonymous participant should not carry a named identifier")
    if record.get("execution_access") is True and record.get("artifact_access_level") != "P4_EXECUTION":
        add(defects, "PROVENANCE_TIER_OVERCLAIM", f"{rid}.artifact_access_level", "Execution access requires P4_EXECUTION access level")
    return defects


def validate_interaction(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("interaction_id", "<unknown>"))
    if record.get("inclusion_status") == "EXCLUDED" and not record.get("exclusion_reason"):
        add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.exclusion_reason", "Excluded interaction requires a reason")
    if record.get("non_response_status") in {"INVITED_NO_RESPONSE", "DECLINED"} and record.get("inclusion_status") == "INCLUDED":
        add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.inclusion_status", "Non-response or decline cannot be included as a substantive observation")
    return defects


def validate_attribution(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("attribution_authorization_id", "<unknown>"))
    if record.get("authorization_status") in {"NOT_AUTHORIZED", "WITHDRAWN", "PRIVATE_ONLY"} and "NO_PUBLIC_ENDORSEMENT" not in {str(x).upper() for x in record.get("prohibited_inferences", [])}:
        add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.prohibited_inferences", "Restricted authorization must prohibit public endorsement inference")
    return defects


def validate_external(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("external_context_set_id", "<unknown>"))
    slots = ["risk_tier_ref", "impact_assessment_id", "aims_process_phase", "required_provenance_profile_id"]
    if record.get("external_context_status") == "SUPPLIED" and not record.get("external_context_owner"):
        add(defects, "EXTERNAL_REFERENCE_OWNER_MISSING", f"{rid}.external_context_owner", "Supplied context requires an external owner")
    for slot_name in slots:
        slot = record.get(slot_name)
        if not isinstance(slot, dict):
            continue
        status = slot.get("status")
        origin = slot.get("origin")
        if status == "SUPPLIED":
            if not slot.get("value"):
                add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.{slot_name}.value", "Supplied context requires a value")
            if not slot.get("owner"):
                add(defects, "EXTERNAL_REFERENCE_OWNER_MISSING", f"{rid}.{slot_name}.owner", "Supplied context requires an owner")
            if origin != "EXTERNAL":
                code = {
                    "risk_tier_ref": "RISK_TIER_INFERRED_BY_FORK",
                    "impact_assessment_id": "IMPACT_ASSESSMENT_INFERRED_BY_FORK",
                    "aims_process_phase": "AIMS_PHASE_INFERRED_BY_FORK",
                    "required_provenance_profile_id": "DECLARED_PROVENANCE_PROFILE_NOT_SATISFIED",
                }[slot_name]
                add(defects, code, f"{rid}.{slot_name}.origin", "Supplied external context must originate outside Fork")
        else:
            if slot.get("value") not in (None, ""):
                add(defects, "SCHEMA_VALIDATION_FAILURE", f"{rid}.{slot_name}.value", "Non-supplied context must not carry a substitute value")
            if origin == "FORK_INFERRED":
                code = {
                    "risk_tier_ref": "RISK_TIER_INFERRED_BY_FORK",
                    "impact_assessment_id": "IMPACT_ASSESSMENT_INFERRED_BY_FORK",
                    "aims_process_phase": "AIMS_PHASE_INFERRED_BY_FORK",
                    "required_provenance_profile_id": "DECLARED_PROVENANCE_PROFILE_NOT_SATISFIED",
                }[slot_name]
                add(defects, code, f"{rid}.{slot_name}.origin", "Fork may not infer missing external context")
    return defects


def validate_profile(record: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    rid = str(record.get("profile_id", "<unknown>"))
    if record.get("applicability_assigned_by") != "EXTERNAL_CONTEXT_ONLY":
        add(defects, "RISK_TIER_INFERRED_BY_FORK", f"{rid}.applicability_assigned_by", "Fork may define a profile but may not assign its applicability")
    return defects


def validate_schema_version(obj: Dict[str, Any]) -> List[Dict[str, str]]:
    defects: List[Dict[str, str]] = []
    if obj.get("schema_version") != SCHEMA_VERSION:
        add(defects, "SCHEMA_VERSION_MISMATCH", "$.schema_version", f"Expected {SCHEMA_VERSION}, observed {obj.get('schema_version')!r}")
    return defects


def semantic_validate(kind: str, obj: Dict[str, Any]) -> List[Dict[str, str]]:
    version_defects = validate_schema_version(obj)
    version_defects.extend({
        "outcome": validate_outcome,
        "participant": validate_participant,
        "interaction": validate_interaction,
        "attribution": validate_attribution,
        "external": validate_external,
        "profile": validate_profile,
    }.get(kind, lambda _obj: [])(obj))
    return version_defects


def id_for(kind: str, obj: Dict[str, Any]) -> Optional[str]:
    return {
        "outcome": obj.get("record_id"),
        "participant": obj.get("participant_context_id"),
        "interaction": obj.get("interaction_id"),
        "attribution": obj.get("attribution_authorization_id"),
        "external": obj.get("external_context_set_id"),
        "profile": obj.get("profile_id"),
    }.get(kind)


def validate_single(kind: str, obj: Dict[str, Any], repo_root: Path) -> Dict[str, Any]:
    defects = validate_schema(kind, obj, repo_root)
    if not any(d["code"] in {"MALFORMED_JSON", "NON_OBJECT_JSON"} for d in defects):
        defects.extend(semantic_validate(kind, obj))
    return result(kind, id_for(kind, obj), defects)


def result(kind: str, record_id: Optional[str], defects: List[Dict[str, str]]) -> Dict[str, Any]:
    defects = sorted(defects, key=lambda d: (d["code"], d["path"], d["detail"]))
    if not defects:
        state = "CONFORMING"
    elif all(d["code"] in REFERENCE_DEFECTS for d in defects):
        state = "UNRESOLVED_REFERENCE"
    else:
        state = "NON_CONFORMING"
    return {
        "checker": "check_experiment_meta_evidence_v0_1.py",
        "schema_version": SCHEMA_VERSION,
        "kind": kind,
        "record_id": record_id,
        "state": state,
        "defect_count": len(defects),
        "defects": defects,
    }


def validate_registry(obj: Dict[str, Any], repo_root: Path) -> Dict[str, Any]:
    defects = validate_schema("registry", obj, repo_root)
    groups = [
        ("profile", "provenance_profiles"),
        ("external", "external_context_reference_sets"),
        ("participant", "participant_context_receipts"),
        ("interaction", "interaction_provenance_records"),
        ("attribution", "attribution_authorization_records"),
        ("outcome", "experiment_outcome_records"),
    ]
    indices: Dict[str, Dict[str, Dict[str, Any]]] = {k: {} for k, _ in groups}
    global_ids: Dict[str, str] = {}
    for kind, key in groups:
        values = obj.get(key, [])
        if not isinstance(values, list):
            continue
        for idx, record in enumerate(values):
            if not isinstance(record, dict):
                continue
            defects.extend(validate_schema(kind, record, repo_root))
            defects.extend(semantic_validate(kind, record))
            rid = id_for(kind, record)
            if isinstance(rid, str):
                if rid in global_ids:
                    add(defects, "DUPLICATE_RECORD_ID", f"$.{key}[{idx}]", f"{rid} duplicates {global_ids[rid]}")
                else:
                    global_ids[rid] = f"{kind}:{idx}"
                indices[kind][rid] = record

    profiles = indices["profile"]
    externals = indices["external"]
    participants = indices["participant"]
    interactions = indices["interaction"]
    attributions = indices["attribution"]
    outcomes = indices["outcome"]

    for iid, interaction in interactions.items():
        pid = interaction.get("participant_context_id")
        if pid not in participants:
            add(defects, "PARTICIPANT_CONTEXT_MISSING", f"{iid}.participant_context_id", f"Unknown participant context {pid}")

    for aid, attribution in attributions.items():
        pid = attribution.get("participant_context_id")
        if pid not in participants:
            add(defects, "PARTICIPANT_CONTEXT_MISSING", f"{aid}.participant_context_id", f"Unknown participant context {pid}")

    for eid, external in externals.items():
        slot = external.get("required_provenance_profile_id")
        if isinstance(slot, dict) and slot.get("status") == "SUPPLIED":
            profile_id = slot.get("value")
            if profile_id not in profiles:
                add(defects, "BROKEN_REFERENCE", f"{eid}.required_provenance_profile_id.value", f"Unknown provenance profile {profile_id}")

    for oid, outcome in outcomes.items():
        pid = outcome.get("participant_context_id")
        iid = outcome.get("interaction_provenance_id")
        aid = outcome.get("attribution_authorization_id")
        if pid and pid not in participants:
            add(defects, "PARTICIPANT_CONTEXT_MISSING", f"{oid}.participant_context_id", f"Unknown participant context {pid}")
        if iid:
            if iid not in interactions:
                add(defects, "INTERACTION_PROVENANCE_MISSING", f"{oid}.interaction_provenance_id", f"Unknown interaction provenance {iid}")
            elif pid and interactions[iid].get("participant_context_id") != pid:
                add(defects, "BROKEN_REFERENCE", f"{oid}.interaction_provenance_id", "Interaction provenance points to a different participant")
        if outcome.get("public_use_status") == "PUBLIC_NAMED":
            if aid not in attributions:
                add(defects, "ATTRIBUTION_NOT_AUTHORIZED", f"{oid}.attribution_authorization_id", f"Unknown attribution authorization {aid}")
            elif attributions[aid].get("authorization_status") not in AUTHORIZED_ATTRIBUTION:
                add(defects, "ATTRIBUTION_NOT_AUTHORIZED", f"{oid}.attribution_authorization_id", "Authorization state does not permit named public use")
            elif pid and attributions[aid].get("participant_context_id") != pid:
                add(defects, "ATTRIBUTION_NOT_AUTHORIZED", f"{oid}.attribution_authorization_id", "Authorization belongs to a different participant")

        ext_ref = outcome.get("external_context")
        if isinstance(ext_ref, dict) and ext_ref.get("status") == "REFERENCED":
            ext_id = ext_ref.get("external_context_set_id")
            if ext_id not in externals:
                add(defects, "EXTERNAL_CONTEXT_REFERENCE_MISSING", f"{oid}.external_context.external_context_set_id", f"Unknown external context set {ext_id}")
            else:
                external = externals[ext_id]
                profile_slot = external.get("required_provenance_profile_id")
                if isinstance(profile_slot, dict) and profile_slot.get("status") == "SUPPLIED":
                    profile_id = profile_slot.get("value")
                    profile = profiles.get(profile_id)
                    if profile:
                        failures: List[str] = []
                        if TIER_RANK.get(str(outcome.get("provenance_tier")), -1) < TIER_RANK.get(str(profile.get("minimum_provenance_tier")), 99):
                            failures.append("minimum provenance tier")
                        methods = profile.get("required_observation_methods", [])
                        if methods and outcome.get("observation_method") not in methods:
                            failures.append("required observation method")
                        required_checks = set(profile.get("required_integrity_checks", []))
                        observed_checks = set(outcome.get("integrity_checks", []))
                        if not required_checks.issubset(observed_checks):
                            failures.append("required integrity checks")
                        if int(outcome.get("reproduction_count", 0)) < int(profile.get("required_reproduction_count", 0)):
                            failures.append("required reproduction count")
                        if failures:
                            add(defects, "DECLARED_PROVENANCE_PROFILE_NOT_SATISFIED", f"{oid}.provenance_tier", ", ".join(failures))

        for idx, edge in enumerate(outcome.get("lineage", [])):
            target = edge.get("target_record_id") if isinstance(edge, dict) else None
            if target not in outcomes:
                add(defects, "BROKEN_REFERENCE", f"{oid}.lineage[{idx}].target_record_id", f"Unknown outcome record {target}")

    return result("registry", obj.get("registry_id"), defects)


def emit(res: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(res, indent=2, sort_keys=True, ensure_ascii=False))
        return
    print(f"{res['state']}: {res.get('record_id') or '<unknown>'} ({res['defect_count']} defect(s))")
    for defect in res["defects"]:
        print(f"- {defect['code']} | {defect['path']} | {defect['detail']}")


def parse_args(kind_default: Optional[str] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Fork meta-evidence v0.1 records and registries")
    parser.add_argument("path", help="JSON record or registry path")
    parser.add_argument("--kind", choices=sorted(SCHEMA_FILES), default=kind_default)
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def infer_kind(obj: Dict[str, Any]) -> str:
    if "registry_id" in obj:
        return "registry"
    if "record_id" in obj:
        return "outcome"
    if "participant_context_id" in obj and "relationship_to_fork" in obj:
        return "participant"
    if "interaction_id" in obj:
        return "interaction"
    if "attribution_authorization_id" in obj:
        return "attribution"
    if "external_context_set_id" in obj:
        return "external"
    if "profile_id" in obj:
        return "profile"
    return "registry"


def run(path: Path, repo_root: Path, kind: Optional[str] = None) -> Dict[str, Any]:
    obj, defects = load_json(path)
    if obj is None:
        return result(kind or "unknown", None, defects)
    actual_kind = kind or infer_kind(obj)
    if actual_kind == "registry":
        return validate_registry(obj, repo_root)
    return validate_single(actual_kind, obj, repo_root)


def main_for_kind(kind: str) -> int:
    args = parse_args(kind)
    path = Path(args.path).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    res = run(path, repo_root, kind)
    emit(res, args.as_json)
    return 0 if res["state"] == "CONFORMING" else 1


def main() -> int:
    args = parse_args(None)
    path = Path(args.path).resolve()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    res = run(path, repo_root, args.kind)
    emit(res, args.as_json)
    return 0 if res["state"] == "CONFORMING" else 1


if __name__ == "__main__":
    raise SystemExit(main())
