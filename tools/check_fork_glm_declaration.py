#!/usr/bin/env python3
import argparse
import hashlib
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

CHECKER_NAME = "check_fork_glm_declaration"
CHECKER_VERSION = "0.1"

REQUIRED_NON_CLAIMS = [
    "does_not_claim_approval",
    "does_not_claim_truth",
    "does_not_claim_safety",
    "does_not_claim_compliance",
    "does_not_claim_legal_sufficiency",
    "does_not_claim_policy_satisfaction",
    "does_not_claim_risk_acceptance",
    "does_not_claim_control_effectiveness",
    "does_not_claim_deployment_readiness",
    "does_not_claim_institutional_authority",
]

REQUIRED_FORBIDDEN_INTERPRETATIONS = [
    "approval_status",
    "truth_validation",
    "safety_validation",
    "compliance_certification",
    "legal_sufficiency",
    "risk_acceptance",
    "deployment_authorization",
    "authority_transfer",
    "claim_expansion_without_new_authority",
    "ci_cd_blocking_gate",
    "host_native_scoring_input",
    "dashboard_assurance_signal",
    "workflow_completion_signal",
    "human_prose_green_signal",
]

def repo_root() -> Path:
    invoked = Path(sys.argv[0]).resolve()
    if invoked.parent.name == "tools":
        return invoked.parents[1]
    return Path.cwd()

def canonical_digest_without_manifest_digest(payload: dict[str, Any]) -> str:
    clone = json.loads(json.dumps(payload, ensure_ascii=False))
    clone.pop("manifest_digest", None)
    canonical = json.dumps(clone, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()

def finding(code: str, message: str, path: str = "$") -> dict[str, str]:
    return {"code": code, "message": message, "path": path}

def load_json(path: Path) -> tuple[Any | None, list[dict[str, str]]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except FileNotFoundError:
        return None, [finding("INPUT_FILE_NOT_FOUND", f"Input file not found: {path}")]
    except json.JSONDecodeError as exc:
        return None, [finding("INPUT_JSON_PARSE_ERROR", f"Input is not valid JSON: {exc.msg}", f"line {exc.lineno}, column {exc.colno}")]

def schema_errors(payload: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, str]]:
    if jsonschema is None:
        return [finding("JSONSCHEMA_IMPORT_ERROR", f"jsonschema could not be imported: {JSONSCHEMA_IMPORT_ERROR}")]
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path))
    out = []
    for err in errors:
        path = "$"
        for part in err.absolute_path:
            path += f"[{part}]" if isinstance(part, int) else f".{part}"
        out.append(finding("SCHEMA_VALIDATION_ERROR", err.message, path))
    return out

def contract_errors(manifest: dict[str, Any]) -> list[dict[str, str]]:
    errors = []

    if manifest.get("schema_version") != "1.3":
        errors.append(finding("FORK_GLM_SCHEMA_VERSION_UNSUPPORTED", "Fork GLM declaration v0.1 expects schema_version 1.3.", "$.schema_version"))

    if manifest.get("manifest_kind") != "layer":
        errors.append(finding("FORK_GLM_MANIFEST_KIND_INVALID", "Fork GLM declaration must be a layer manifest.", "$.manifest_kind"))

    layer = manifest.get("layer", {})
    if layer.get("vendor_layer_name") != "Fork":
        errors.append(finding("FORK_GLM_LAYER_NAME_INVALID", "layer.vendor_layer_name must be Fork.", "$.layer.vendor_layer_name"))

    if layer.get("layer_type") != "cross_cutting":
        errors.append(finding("FORK_GLM_LAYER_TYPE_INVALID", "Fork declares GLM layer_type cross_cutting.", "$.layer.layer_type"))

    timing = manifest.get("timing_axis", {})
    if timing.get("not_runtime_gate") is not True:
        errors.append(finding("FORK_GLM_RUNTIME_GATE_BOUNDARY_MISSING", "timing_axis.not_runtime_gate must be true.", "$.timing_axis.not_runtime_gate"))

    claims = manifest.get("claims_boundary", {})
    non_claims = set(claims.get("explicit_non_claims", []))
    missing_non_claims = [item for item in REQUIRED_NON_CLAIMS if item not in non_claims]
    if missing_non_claims:
        errors.append(finding("FORK_GLM_NON_CLAIMS_INCOMPLETE", "Missing explicit_non_claims: " + ", ".join(missing_non_claims), "$.claims_boundary.explicit_non_claims"))

    forbidden = set(claims.get("forbidden_interpretations", []))
    missing_forbidden = [item for item in REQUIRED_FORBIDDEN_INTERPRETATIONS if item not in forbidden]
    if missing_forbidden:
        errors.append(finding("FORK_GLM_FORBIDDEN_INTERPRETATIONS_INCOMPLETE", "Missing forbidden_interpretations: " + ", ".join(missing_forbidden), "$.claims_boundary.forbidden_interpretations"))

    status = manifest.get("machine_readable_status", {})
    if status.get("safe_to_automate") is not False:
        errors.append(finding("FORK_GLM_AUTOMATION_BOUNDARY_INVALID", "machine_readable_status.safe_to_automate must be false.", "$.machine_readable_status.safe_to_automate"))
    if status.get("requires_human_interpretation_before_any_automation") is not True:
        errors.append(finding("FORK_GLM_HUMAN_INTERPRETATION_BOUNDARY_MISSING", "machine_readable_status.requires_human_interpretation_before_any_automation must be true.", "$.machine_readable_status.requires_human_interpretation_before_any_automation"))

    digest = manifest.get("manifest_digest", {})
    expected_digest = canonical_digest_without_manifest_digest(manifest)
    if digest.get("sha256") != expected_digest:
        errors.append(finding("FORK_GLM_DIGEST_MISMATCH", "manifest_digest.sha256 does not match canonical digest excluding manifest_digest.", "$.manifest_digest.sha256"))

    return errors

def make_output(path: Path, manifest: dict[str, Any] | None, result_kind: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "checker": {
            "name": CHECKER_NAME,
            "version": CHECKER_VERSION
        },
        "manifest": {
            "path": str(path),
            "schema_version": manifest.get("schema_version") if isinstance(manifest, dict) else None,
            "manifest_kind": manifest.get("manifest_kind") if isinstance(manifest, dict) else None,
            "manifest_version": manifest.get("manifest_version") if isinstance(manifest, dict) else None,
            "layer": manifest.get("layer", {}).get("vendor_layer_name") if isinstance(manifest, dict) else None
        },
        "actionability": "NON_ACTIONABLE_STRUCTURAL_DECLARATION_ONLY",
        "result": {
            "result_kind": result_kind,
            "safe_to_automate": False,
            "requires_human_interpretation_before_any_automation": True
        },
        "scope": {
            "validates": [
                "json_parseability",
                "fork_glm_declaration_schema_conformance",
                "required_non_claims_presence",
                "required_forbidden_interpretations_presence",
                "timing_axis_boundary_presence",
                "machine_readable_status_boundary_presence",
                "manifest_digest_recomputability"
            ],
            "does_not_validate": [
                "truth_of_fork_claims",
                "legal_sufficiency",
                "compliance",
                "safety",
                "risk_acceptance",
                "external_glm_certification",
                "host_platform_behavior",
                "human_prose_or_dashboard_framing",
                "reciprocal_interoperability_by_adjacent_layers"
            ]
        },
        "errors": errors
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", default=".well-known/governance-layer-manifest.json")
    args = parser.parse_args()

    path = Path(args.manifest)
    if not path.is_absolute():
        path = repo_root() / path

    manifest, load_errors = load_json(path)
    if load_errors:
        print(json.dumps(make_output(path, None, "INPUT_ERROR", load_errors), indent=2))
        return 1

    schema_path = repo_root() / "schemas" / "fork_glm_declaration_v0_1.schema.json"
    schema, schema_load_errors = load_json(schema_path)
    if schema_load_errors:
        print(json.dumps(make_output(path, manifest, "INPUT_ERROR", schema_load_errors), indent=2))
        return 1

    errors = schema_errors(manifest, schema) + contract_errors(manifest)
    result_kind = "STRUCTURAL_CONFORMANCE_RECORDED" if not errors else "CONTRACT_VALIDATION_FAILED"
    output = make_output(path, manifest, result_kind, errors)
    print(json.dumps(output, indent=2))
    return 0 if result_kind == "STRUCTURAL_CONFORMANCE_RECORDED" else 1

if __name__ == "__main__":
    raise SystemExit(main())
