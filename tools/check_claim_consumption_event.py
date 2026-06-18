#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception as exc:  # pragma: no cover
    jsonschema = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None

CHECKER_NAME = "check_claim_consumption_event"
CHECKER_VERSION = "0.1"

DO_NOT_MAP_TO = [
    "APPROVAL",
    "TRUTH",
    "SAFETY",
    "COMPLIANCE",
    "LEGAL_SUFFICIENCY",
    "INSTITUTIONAL_AUTHORIZATION",
    "POLICY_SATISFACTION",
    "RISK_ACCEPTANCE",
]

LIMITATIONS = {
    "records_local_reliance_behavior_only": True,
    "synthetic_structural_checker_only": True,
    "does_not_validate_approval": True,
    "does_not_validate_truth": True,
    "does_not_validate_safety": True,
    "does_not_validate_compliance": True,
    "does_not_validate_legal_sufficiency": True,
    "does_not_validate_institutional_authorization": True,
    "does_not_validate_policy_satisfaction": True,
    "does_not_validate_risk_acceptance": True,
    "not_runtime_control": True,
    "not_policy_engine": True,
    "not_compliance_oracle": True,
}

NON_CLAIMS = {
    "does_not_approve_reliance": True,
    "does_not_validate_correctness": True,
    "does_not_validate_truth": True,
    "does_not_validate_safety": True,
    "does_not_validate_compliance": True,
    "does_not_validate_legal_sufficiency": True,
    "does_not_validate_authority": True,
    "does_not_validate_policy_fit": True,
}

VALIDATES = [
    "json_parseability",
    "claim_consumption_event_schema_conformance",
    "explicit_receiving_boundary_effect",
    "preserved_non_claim_presence",
    "local_decision_owner_presence",
    "explicit_new_claim_reference_for_boundary_expansion",
    "reliance_action_consistency",
    "forbidden_oracle_field_absence",
    "checker_output_contract_conformance",
]

DOES_NOT_VALIDATE = [
    "truth_of_source_claim",
    "correctness_of_receiving_decision",
    "safety_of_receiving_decision",
    "compliance_of_receiving_decision",
    "legal_sufficiency_of_receiving_decision",
    "institutional_authority_of_decision_owner",
    "policy_satisfaction",
    "risk_acceptance",
]

FORBIDDEN_ORACLE_FIELDS = {
    "approval_status",
    "approved",
    "truth_status",
    "is_true",
    "safety_status",
    "is_safe",
    "compliance_status",
    "is_compliant",
    "legal_sufficiency_status",
    "legally_sufficient",
    "authorization_status",
    "authorized",
    "risk_acceptance_status",
    "risk_accepted",
}

def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]

def event_schema_path() -> Path:
    return repo_root() / "schemas" / "claim_consumption_event_v0_1.schema.json"

def output_schema_path() -> Path:
    return repo_root() / "schemas" / "claim_consumption_event_checker_output_v0_1.schema.json"

def finding(code: str, message: str, path: str | None = None) -> dict[str, str]:
    item = {"code": code, "message": message}
    if path:
        item["path"] = path
    return item

def load_json_file(path: Path) -> tuple[Any | None, list[dict[str, str]]]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, [finding("INPUT_FILE_NOT_FOUND", f"Input file not found: {path}", "$")]
    except OSError as exc:
        return None, [finding("INPUT_FILE_READ_ERROR", f"Could not read input file: {exc}", "$")]

    try:
        return json.loads(text), []
    except json.JSONDecodeError as exc:
        return None, [
            finding(
                "INPUT_JSON_PARSE_ERROR",
                f"Input is not valid JSON: {exc.msg}",
                f"line {exc.lineno}, column {exc.colno}",
            )
        ]

def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def json_path(error: Any) -> str:
    parts = list(error.absolute_path)
    if not parts:
        return "$"

    rendered = "$"
    for part in parts:
        if isinstance(part, int):
            rendered += f"[{part}]"
        else:
            rendered += f".{part}"
    return rendered

def validate_schema(instance: Any, schema: dict[str, Any]) -> list[dict[str, str]]:
    if jsonschema is None:
        return [
            finding(
                "JSONSCHEMA_IMPORT_ERROR",
                f"jsonschema could not be imported: {JSONSCHEMA_IMPORT_ERROR}",
                "$",
            )
        ]

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))
    return [
        finding("SCHEMA_VALIDATION_ERROR", error.message, json_path(error))
        for error in errors
    ]

def walk_forbidden_fields(value: Any, path: str = "$") -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_ORACLE_FIELDS:
                errors.append(
                    finding(
                        "CCE_FORBIDDEN_ORACLE_FIELD",
                        f"Forbidden oracle-like field name '{key}' collapses structural recording into a prohibited status signal.",
                        child_path,
                    )
                )
            errors.extend(walk_forbidden_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(walk_forbidden_fields(child, f"{path}[{index}]"))

    return errors

def contract_errors(event: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    boundary_effect = event.get("boundary_effect")
    new_claim_reference = event.get("new_claim_reference")
    local_decision = event.get("local_reliance_decision", {})
    reliance_action = local_decision.get("reliance_action") if isinstance(local_decision, dict) else None

    if boundary_effect == "EXPANDED" and not isinstance(new_claim_reference, dict):
        errors.append(
            finding(
                "CCE_EXPANSION_REQUIRES_EXPLICIT_NEW_CLAIM",
                "boundary_effect EXPANDED requires an explicit new_claim_reference with expansion reason and accountable owner.",
                "$.new_claim_reference",
            )
        )

    if boundary_effect != "EXPANDED" and new_claim_reference is not None:
        errors.append(
            finding(
                "CCE_NON_EXPANDED_BOUNDARY_MUST_NOT_CREATE_NEW_CLAIM",
                "new_claim_reference must be null unless boundary_effect is EXPANDED.",
                "$.new_claim_reference",
            )
        )

    if reliance_action in {"RELIED_ON", "PARTIALLY_RELIED_ON"} and not event.get("relied_claims"):
        errors.append(
            finding(
                "CCE_RELIANCE_REQUIRES_RELIED_CLAIMS",
                "A relied-on event must identify at least one relied claim.",
                "$.relied_claims",
            )
        )

    if reliance_action == "DID_NOT_RELY" and boundary_effect not in {"REJECTED", "NARROWED"}:
        errors.append(
            finding(
                "CCE_DID_NOT_RELY_BOUNDARY_EFFECT_MISMATCH",
                "DID_NOT_RELY should use boundary_effect REJECTED or NARROWED.",
                "$.boundary_effect",
            )
        )

    decision_owner = event.get("decision_owner")
    decision_owner_ref = local_decision.get("decision_owner_ref") if isinstance(local_decision, dict) else None
    owner_id = decision_owner.get("owner_id") if isinstance(decision_owner, dict) else None

    if decision_owner_ref and owner_id and decision_owner_ref != owner_id:
        errors.append(
            finding(
                "CCE_DECISION_OWNER_REF_MISMATCH",
                "local_reliance_decision.decision_owner_ref must match decision_owner.owner_id.",
                "$.local_reliance_decision.decision_owner_ref",
            )
        )

    limitations = event.get("limitations")
    if isinstance(limitations, dict):
        for key in [
            "records_local_reliance_behavior_only",
            "does_not_validate_approval",
            "does_not_validate_truth",
            "does_not_validate_safety",
            "does_not_validate_compliance",
            "does_not_validate_legal_sufficiency",
            "does_not_validate_institutional_authorization",
            "does_not_validate_policy_satisfaction",
            "does_not_validate_risk_acceptance",
            "not_runtime_control",
            "not_policy_engine",
            "not_compliance_oracle",
        ]:
            if limitations.get(key) is not True:
                errors.append(
                    finding(
                        "CCE_LIMITATION_MUST_BE_TRUE",
                        f"limitations.{key} must be true.",
                        f"$.limitations.{key}",
                    )
                )

        mapped = set(limitations.get("do_not_map_to", []))
        missing = [item for item in DO_NOT_MAP_TO if item not in mapped]
        if missing:
            errors.append(
                finding(
                    "CCE_DO_NOT_MAP_TO_INCOMPLETE",
                    "limitations.do_not_map_to is missing: " + ", ".join(missing),
                    "$.limitations.do_not_map_to",
                )
            )

    errors.extend(walk_forbidden_fields(event))
    return errors

def make_output(
    *,
    input_path: Path,
    result_kind: str,
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return {
        "checker": {"name": CHECKER_NAME, "version": CHECKER_VERSION},
        "input": {"path": str(input_path)},
        "result": {"ok": result_kind == "STRUCTURAL_PASS", "result_kind": result_kind},
        "errors": errors,
        "warnings": warnings or [],
        "scope": {
            "checker_scope": "structural_claim_consumption_event_validation_only",
            "validates": VALIDATES,
            "does_not_validate": DOES_NOT_VALIDATE,
        },
        "limitations": LIMITATIONS,
        "do_not_map_to": DO_NOT_MAP_TO,
        "non_claims": NON_CLAIMS,
    }

def output_contract_errors(output: dict[str, Any]) -> list[dict[str, str]]:
    try:
        schema = load_schema(output_schema_path())
    except Exception as exc:
        return [finding("OUTPUT_SCHEMA_LOAD_ERROR", f"Could not load output schema: {exc}", "$")]
    return validate_schema(output, schema)

def emit(output: dict[str, Any]) -> int:
    output_errors = output_contract_errors(output)
    if output_errors:
        emergency_output = make_output(
            input_path=Path(output.get("input", {}).get("path", "")),
            result_kind="OUTPUT_CONTRACT_VIOLATION",
            errors=[
                finding(
                    "CCE_OUTPUT_CONTRACT_VIOLATION",
                    "Checker output failed its own output contract.",
                    "$",
                ),
                *output_errors,
            ],
        )
        print(json.dumps(emergency_output, indent=2, sort_keys=True))
        return 2

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["result"]["ok"] else 1

def check(path: Path) -> dict[str, Any]:
    event, input_errors = load_json_file(path)
    if input_errors:
        return make_output(input_path=path, result_kind="INPUT_ERROR", errors=input_errors)

    schema = load_schema(event_schema_path())
    schema_errors = validate_schema(event, schema)
    if schema_errors:
        return make_output(input_path=path, result_kind="SCHEMA_VALIDATION_FAILED", errors=schema_errors)

    if not isinstance(event, dict):
        return make_output(
            input_path=path,
            result_kind="SCHEMA_VALIDATION_FAILED",
            errors=[finding("CCE_ROOT_NOT_OBJECT", "Input root must be a JSON object.", "$")],
        )

    extra_errors = contract_errors(event)
    if extra_errors:
        return make_output(input_path=path, result_kind="CONTRACT_VALIDATION_FAILED", errors=extra_errors)

    return make_output(input_path=path, result_kind="STRUCTURAL_PASS", errors=[])

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Claim Consumption Event v0.1 structural contract.")
    parser.add_argument("path", type=Path, help="Path to the CCE JSON file.")
    args = parser.parse_args(argv)

    try:
        output = check(args.path)
    except Exception as exc:
        output = make_output(
            input_path=args.path,
            result_kind="INPUT_ERROR",
            errors=[finding("CHECKER_UNHANDLED_ERROR", str(exc), "$")],
        )

    return emit(output)

if __name__ == "__main__":
    raise SystemExit(main())
