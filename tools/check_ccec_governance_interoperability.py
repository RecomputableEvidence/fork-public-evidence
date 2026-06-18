#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import jsonschema
except Exception as exc:
    jsonschema = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None

CHECKER_NAME = "check_ccec_governance_interoperability"
CHECKER_VERSION = "0.1"

PROHIBITED_MAPPINGS = [
    "APPROVAL_STATUS",
    "TRUTH_STATUS",
    "SAFETY_STATUS",
    "COMPLIANCE_STATUS",
    "LEGAL_SUFFICIENCY_STATUS",
    "INSTITUTIONAL_AUTHORIZATION_STATUS",
    "POLICY_SATISFACTION_STATUS",
    "RISK_ACCEPTANCE_STATUS",
    "AUTHORITY_TRANSFER",
    "CLAIM_EXPANSION_BY_MAPPING",
    "AUTOMATED_CONTROL_DECISION",
]

DO_NOT_MAP_TO = [
    "APPROVAL",
    "TRUTH",
    "SAFETY",
    "COMPLIANCE",
    "LEGAL_SUFFICIENCY",
    "INSTITUTIONAL_AUTHORIZATION",
    "POLICY_SATISFACTION",
    "RISK_ACCEPTANCE",
    "AUTHORITY_TRANSFER",
]

LIMITATIONS = {
    "safe_to_automate": False,
    "automation_interpretation_required": True,
    "bounded_reference_only": True,
    "synthetic_structural_checker_only": True,
    "does_not_validate_approval": True,
    "does_not_validate_truth": True,
    "does_not_validate_safety": True,
    "does_not_validate_compliance": True,
    "does_not_validate_legal_sufficiency": True,
    "does_not_validate_institutional_authorization": True,
    "does_not_validate_policy_satisfaction": True,
    "does_not_validate_risk_acceptance": True,
    "does_not_transfer_authority": True,
    "not_runtime_control": True,
    "not_policy_engine": True,
    "not_compliance_oracle": True,
}

NON_CLAIMS = {
    "does_not_create_approval_status": True,
    "does_not_create_compliance_status": True,
    "does_not_create_safety_status": True,
    "does_not_create_truth_status": True,
    "does_not_create_legal_sufficiency_status": True,
    "does_not_transfer_authority": True,
    "does_not_close_unresolved_gaps": True,
    "does_not_accept_risk": True,
}

VALIDATES = [
    "json_parseability",
    "ccec_governance_interoperability_schema_conformance",
    "permitted_mapping_consistency",
    "prohibited_mapping_completeness",
    "forbidden_oracle_target_field_absence",
    "authority_inheritance_prohibition",
    "unresolved_gap_preservation",
    "checker_output_contract_conformance",
]

DOES_NOT_VALIDATE = [
    "truth_of_source_ccec",
    "correctness_of_external_governance_decision",
    "compliance_of_external_system",
    "safety_of_external_system",
    "legal_sufficiency_of_external_decision",
    "institutional_authority_of_external_owner",
    "policy_satisfaction",
    "risk_acceptance",
]

FORBIDDEN_FIELD_NAMES = {
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
    "authority_transfer",
}

FORBIDDEN_TARGET_FRAGMENTS = [
    "approval_status",
    "approved_status",
    "truth_status",
    "safety_status",
    "compliance_status",
    "legal_sufficiency",
    "authorization_status",
    "authorized_status",
    "policy_satisfaction",
    "risk_acceptance",
    "risk_accepted",
    "authority_transfer",
]

def repo_root() -> Path:
    invoked = Path(sys.argv[0]).resolve()
    if invoked.parent.name == "tools":
        return invoked.parents[1]
    return Path.cwd()

def profile_schema_path() -> Path:
    return repo_root() / "schemas" / "ccec_governance_interoperability_profile_v0_1.schema.json"

def output_schema_path() -> Path:
    return repo_root() / "schemas" / "ccec_governance_interoperability_checker_output_v0_1.schema.json"

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
        return None, [finding("INPUT_JSON_PARSE_ERROR", f"Input is not valid JSON: {exc.msg}", f"line {exc.lineno}, column {exc.colno}")]

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
        return [finding("JSONSCHEMA_IMPORT_ERROR", f"jsonschema could not be imported: {JSONSCHEMA_IMPORT_ERROR}", "$")]

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.absolute_path))
    return [finding("SCHEMA_VALIDATION_ERROR", error.message, json_path(error)) for error in errors]

def walk_forbidden_fields(value: Any, path: str = "$") -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_FIELD_NAMES:
                errors.append(
                    finding(
                        "CCEC_INTEROP_FORBIDDEN_ORACLE_FIELD",
                        f"Forbidden oracle-like field name '{key}' is not allowed in an interoperability profile.",
                        child_path,
                    )
                )
            errors.extend(walk_forbidden_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(walk_forbidden_fields(child, f"{path}[{index}]"))

    return errors

def contract_errors(profile: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    permitted = set(profile.get("permitted_mappings", []))
    prohibited = set(profile.get("prohibited_mappings", []))

    missing_prohibited = [item for item in PROHIBITED_MAPPINGS if item not in prohibited]
    if missing_prohibited:
        errors.append(
            finding(
                "CCEC_INTEROP_PROHIBITED_MAPPINGS_INCOMPLETE",
                "prohibited_mappings is missing: " + ", ".join(missing_prohibited),
                "$.prohibited_mappings",
            )
        )

    accord_limitations = profile.get("accord_limitations")
    if isinstance(accord_limitations, dict):
        mapped = set(accord_limitations.get("do_not_map_to", []))
        missing = [item for item in DO_NOT_MAP_TO if item not in mapped]
        if missing:
            errors.append(
                finding(
                    "CCEC_INTEROP_DO_NOT_MAP_TO_INCOMPLETE",
                    "accord_limitations.do_not_map_to is missing: " + ", ".join(missing),
                    "$.accord_limitations.do_not_map_to",
                )
            )

        for key, expected in [
            ("safe_to_automate", False),
            ("automation_interpretation_required", True),
            ("bounded_reference_only", True),
            ("does_not_validate_approval", True),
            ("does_not_validate_truth", True),
            ("does_not_validate_safety", True),
            ("does_not_validate_compliance", True),
            ("does_not_validate_legal_sufficiency", True),
            ("does_not_validate_institutional_authorization", True),
            ("does_not_validate_policy_satisfaction", True),
            ("does_not_validate_risk_acceptance", True),
            ("does_not_transfer_authority", True),
            ("not_runtime_control", True),
            ("not_policy_engine", True),
            ("not_compliance_oracle", True),
        ]:
            if accord_limitations.get(key) is not expected:
                errors.append(
                    finding(
                        "CCEC_INTEROP_LIMITATION_VALUE_INVALID",
                        f"accord_limitations.{key} must be {expected}.",
                        f"$.accord_limitations.{key}",
                    )
                )

    for index, rule in enumerate(profile.get("mapping_rules", [])):
        if not isinstance(rule, dict):
            continue

        mapping_kind = rule.get("mapping_kind")
        if mapping_kind not in permitted:
            errors.append(
                finding(
                    "CCEC_INTEROP_MAPPING_KIND_NOT_PERMITTED",
                    f"mapping rule uses {mapping_kind}, but that kind is not listed in permitted_mappings.",
                    f"$.mapping_rules[{index}].mapping_kind",
                )
            )

        target = str(rule.get("external_target_field", "")).lower()
        for fragment in FORBIDDEN_TARGET_FRAGMENTS:
            if fragment in target:
                errors.append(
                    finding(
                        "CCEC_INTEROP_ORACLE_TARGET_FIELD",
                        f"external_target_field '{rule.get('external_target_field')}' would map a bounded CCEC reference into a prohibited oracle-like target.",
                        f"$.mapping_rules[{index}].external_target_field",
                    )
                )
                break

    local_authority = profile.get("local_authority_boundary")
    if isinstance(local_authority, dict):
        if local_authority.get("external_status_change_basis") == "INHERITED_FROM_CCEC":
            errors.append(
                finding(
                    "CCEC_INTEROP_AUTHORITY_INHERITANCE_PROHIBITED",
                    "external_status_change_basis must not be INHERITED_FROM_CCEC.",
                    "$.local_authority_boundary.external_status_change_basis",
                )
            )

    gap_handling = profile.get("unresolved_gaps_handling")
    if isinstance(gap_handling, dict):
        if gap_handling.get("may_close_gaps_by_mapping") is not False:
            errors.append(
                finding(
                    "CCEC_INTEROP_GAPS_MUST_NOT_CLOSE_BY_MAPPING",
                    "Unresolved gaps may not be closed by interoperability mapping.",
                    "$.unresolved_gaps_handling.may_close_gaps_by_mapping",
                )
            )

    errors.extend(walk_forbidden_fields(profile))
    return errors

def make_output(input_path: Path, result_kind: str, errors: list[dict[str, str]], warnings: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "checker": {"name": CHECKER_NAME, "version": CHECKER_VERSION},
        "input": {"path": str(input_path)},
        "result": {"ok": result_kind == "STRUCTURAL_PASS", "result_kind": result_kind},
        "errors": errors,
        "warnings": warnings or [],
        "scope": {
            "checker_scope": "structural_ccec_governance_interoperability_validation_only",
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
            Path(output.get("input", {}).get("path", "")),
            "OUTPUT_CONTRACT_VIOLATION",
            [
                finding("CCEC_INTEROP_OUTPUT_CONTRACT_VIOLATION", "Checker output failed its own output contract.", "$"),
                *output_errors,
            ],
        )
        print(json.dumps(emergency_output, indent=2, sort_keys=True))
        return 2

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["result"]["ok"] else 1

def check(path: Path) -> dict[str, Any]:
    profile, input_errors = load_json_file(path)
    if input_errors:
        return make_output(path, "INPUT_ERROR", input_errors)

    schema = load_schema(profile_schema_path())
    schema_errors = validate_schema(profile, schema)
    if schema_errors:
        return make_output(path, "SCHEMA_VALIDATION_FAILED", schema_errors)

    if not isinstance(profile, dict):
        return make_output(path, "SCHEMA_VALIDATION_FAILED", [finding("CCEC_INTEROP_ROOT_NOT_OBJECT", "Input root must be a JSON object.", "$")])

    extra_errors = contract_errors(profile)
    if extra_errors:
        return make_output(path, "CONTRACT_VALIDATION_FAILED", extra_errors)

    return make_output(path, "STRUCTURAL_PASS", [])

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a CCEC Governance Interoperability Profile v0.1 structural contract.")
    parser.add_argument("path", type=Path, help="Path to the CCEC governance interoperability profile JSON file.")
    args = parser.parse_args(argv)

    try:
        output = check(args.path)
    except Exception as exc:
        output = make_output(args.path, "INPUT_ERROR", [finding("CHECKER_UNHANDLED_ERROR", str(exc), "$")])

    return emit(output)

raise SystemExit(main())
