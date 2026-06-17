from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install project test dependencies before running this checker."
    ) from exc


READINESS_NON_CLAIMS = [
    "READINESS_GATE_DOES_NOT_AUTHORIZE_LIVE_INGESTION",
    "READINESS_GATE_DOES_NOT_CERTIFY_PRODUCTION_READINESS",
    "READINESS_GATE_DOES_NOT_CERTIFY_SOURCE_TRUTH",
    "READINESS_GATE_DOES_NOT_CERTIFY_COMPLETENESS",
    "READINESS_GATE_DOES_NOT_CERTIFY_LEGAL_ADMISSIBILITY",
    "READINESS_GATE_DOES_NOT_CERTIFY_LAWFULNESS",
    "READINESS_GATE_DOES_NOT_CERTIFY_REGULATORY_COMPLIANCE",
    "READINESS_GATE_DOES_NOT_CERTIFY_HIPAA_COMPLIANCE",
    "READINESS_GATE_DOES_NOT_CERTIFY_MEDICAL_CORRECTNESS",
    "READINESS_GATE_DOES_NOT_CERTIFY_CLINICAL_APPROPRIATENESS",
    "READINESS_GATE_DOES_NOT_CERTIFY_UTILIZATION_MANAGEMENT_SUFFICIENCY",
    "READINESS_GATE_DOES_NOT_REPLACE_INSTITUTIONAL_APPROVAL",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def schema_errors(schema_path: Path, obj: dict[str, Any]) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(obj), key=lambda err: list(err.path))
    messages: list[str] = []
    for err in errors:
        path = ".".join(str(part) for part in err.path)
        if path:
            messages.append(f"{path}: {err.message}")
        else:
            messages.append(err.message)
    return messages


def check_component(root: Path, component: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    component_path = root / component["path"]
    component_type = component["component_type"]

    check = {
        "component_id": component["component_id"],
        "component_type": component_type,
        "path": component["path"],
        "status": "PRESENT",
    }

    finding: dict[str, Any] | None = None

    if not component_path.exists():
        check["status"] = "MISSING"
        finding = {
            "component_id": component["component_id"],
            "path": component["path"],
            "code": "REQUIRED_COMPONENT_MISSING",
        }
        return check, finding

    if component_type == "JSON_SCHEMA":
        try:
            load_json(component_path)
        except Exception:
            check["status"] = "INVALID"
            finding = {
                "component_id": component["component_id"],
                "path": component["path"],
                "code": "JSON_SCHEMA_NOT_PARSEABLE",
            }

    if component_type in {"TEMPLATE_DIRECTORY", "FIXTURE_DIRECTORY"} and not component_path.is_dir():
        check["status"] = "INVALID"
        finding = {
            "component_id": component["component_id"],
            "path": component["path"],
            "code": "DIRECTORY_COMPONENT_NOT_DIRECTORY",
        }

    return check, finding


def write_aligned_synthetic_records(root: Path, output_dir: Path) -> Path:
    manifest = load_json(
        root / "examples" / "nightly_batch_export" / "valid" / "valid_synthetic_dry_run_manifest.json"
    )
    record_text = (
        root
        / "examples"
        / "nightly_batch_export"
        / "valid"
        / "valid_hash_reference_only_records.jsonl"
    ).read_text(encoding="utf-8")
    record = json.loads(record_text.splitlines()[0])
    record["batch_id"] = manifest["batch_id"]
    records_path = output_dir / "aligned_synthetic_records.jsonl"
    records_path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")
    return records_path


def integration_checks(root: Path) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    nightly_checker = load_module(
        "check_nightly_batch_export", root / "tools" / "check_nightly_batch_export.py"
    )
    nightly_receipt = nightly_checker.validate_batch(
        root / "examples" / "nightly_batch_export" / "valid" / "valid_hash_reference_only_manifest.json",
        root / "examples" / "nightly_batch_export" / "valid" / "valid_hash_reference_only_records.jsonl",
    )
    checks.append(
        {
            "check_id": "nightly_batch_checker_valid_fixture",
            "status": "PASS" if nightly_receipt.get("batch_result") == "ACCEPTED" else "FAIL",
            "details": {
                "batch_result": nightly_receipt.get("batch_result"),
                "record_count_accepted": nightly_receipt.get("record_count_accepted"),
            },
        }
    )

    approval_checker = load_module(
        "check_pilot_approval_artifacts", root / "tools" / "check_pilot_approval_artifacts.py"
    )
    approval_receipt = approval_checker.validate_path(
        root / "templates" / "pilot_approval_artifacts",
        require_complete_set=True,
    )
    checks.append(
        {
            "check_id": "pilot_approval_artifacts_complete_set",
            "status": "PASS" if approval_receipt.get("validation_result") == "ACCEPTED" else "FAIL",
            "details": {
                "validation_result": approval_receipt.get("validation_result"),
                "artifact_count_valid": approval_receipt.get("artifact_count_valid"),
                "missing_required_artifact_types": approval_receipt.get("missing_required_artifact_types"),
            },
        }
    )

    dry_run_harness = load_module("run_pilot_dry_run", root / "tools" / "run_pilot_dry_run.py")
    with tempfile.TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        aligned_records = write_aligned_synthetic_records(root, temp_dir)
        summary = dry_run_harness.run_dry_run(
            manifest_path=root
            / "examples"
            / "nightly_batch_export"
            / "valid"
            / "valid_synthetic_dry_run_manifest.json",
            records_path=aligned_records,
            output_dir=temp_dir,
        )
    checks.append(
        {
            "check_id": "pilot_dry_run_harness_aligned_synthetic_batch",
            "status": "PASS" if summary.get("gate_result") == "DRY_RUN_GATE_PASSED" else "FAIL",
            "details": {
                "gate_result": summary.get("gate_result"),
                "batch_result": summary.get("batch_result"),
            },
        }
    )

    return checks


def build_receipt(
    *,
    index_path: Path,
    package_index: dict[str, Any],
    component_checks: list[dict[str, Any]],
    missing_components: list[dict[str, Any]],
    checks: list[dict[str, Any]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    required_count = sum(
        1 for c in package_index.get("package_components", []) if c.get("required") is True
    )
    present_count = sum(1 for c in component_checks if c["status"] == "PRESENT")
    failed_integration = [check for check in checks if check["status"] != "PASS"]

    gate_result = "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY"
    if missing_components or failed_integration or errors:
        gate_result = "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_INCOMPLETE"

    return {
        "record_type": "FORK_CONTROLLED_PILOT_READINESS_RECEIPT",
        "schema_version": "0.1",
        "package_id": package_index.get("package_id", "UNKNOWN"),
        "checked_index_path": str(index_path),
        "gate_result": gate_result,
        "component_count_required": required_count,
        "component_count_present": present_count,
        "component_count_missing": len(missing_components),
        "missing_components": missing_components,
        "component_checks": component_checks,
        "integration_checks": checks,
        "errors": errors,
        "readiness_non_claims": READINESS_NON_CLAIMS,
        "live_ingestion_authorization": {
            "authorization_state": "NOT_ASSERTED_BY_FORK",
            "fork_issued_live_ingestion_authorization": False,
            "external_institutional_authorization_required": True,
            "institutional_live_ingestion_authorization_ref": None,
            "fork_does_not_validate_external_authorization_sufficiency": True,
        },
    }


def validate_readiness(index_path: Path, schema_path: Path | None = None) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    schema_path = schema_path or root / "schemas" / "controlled_pilot_readiness_gate_v0_1.schema.json"

    errors: list[dict[str, Any]] = []
    package_index = load_json(index_path)

    index_errors = schema_errors(schema_path, package_index)
    if index_errors:
        errors.append(
            {
                "scope": "package_index",
                "code": "PACKAGE_INDEX_SCHEMA_INVALID",
                "messages": index_errors,
            }
        )
        return build_receipt(
            index_path=index_path,
            package_index=package_index,
            component_checks=[],
            missing_components=[],
            checks=[],
            errors=errors,
        )

    component_checks: list[dict[str, Any]] = []
    missing_components: list[dict[str, Any]] = []

    for component in package_index["package_components"]:
        check, finding = check_component(root, component)
        component_checks.append(check)
        if finding is not None and component.get("required") is True:
            missing_components.append(finding)

    checks: list[dict[str, Any]] = []
    if not missing_components:
        try:
            checks = integration_checks(root)
        except Exception as exc:
            errors.append(
                {
                    "scope": "integration_checks",
                    "code": "INTEGRATION_CHECK_EXCEPTION",
                    "message": str(exc),
                }
            )

    return build_receipt(
        index_path=index_path,
        package_index=package_index,
        component_checks=component_checks,
        missing_components=missing_components,
        checks=checks,
        errors=errors,
    )


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Check Fork Controlled Pilot Package Readiness Gate v0.1."
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("pilot_package/controlled_pilot_package_index_v0_1.json"),
    )
    parser.add_argument("--schema", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    receipt = validate_readiness(args.index, args.schema)
    output = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)

    return 0 if receipt["gate_result"] == "CONTROLLED_PILOT_PACKAGE_STRUCTURALLY_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
