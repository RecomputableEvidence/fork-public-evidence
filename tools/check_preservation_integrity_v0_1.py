#!/usr/bin/env python3
"""Verify Fork incident-preservation records and quarantined specimens."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import jsonschema
except Exception as exc:  # pragma: no cover - exercised only without dependencies
    jsonschema = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None


CHECKER_ID = "FORK_PRESERVATION_INTEGRITY_CHECKER_v0_1"
INCIDENT_ID = "FORK-INC-2026-07-13-001"
FAILURE_CLASS_ID = "CCF-001_AI_CHANGE_READINESS_PROMOTION"
PRE_INCIDENT_COMMIT = "fc3a100563eb354924787759accfc7ecd39ae94d"
INCIDENT_COMMIT = "7080e198e6f87e918121af6097a6ef36fd8e7a07"
POST_INCIDENT_DESCENDANT = "fd93d051235ec43bee925878bc916d09179b3c90"

ARCHIVE_ROOT = Path("docs/preservation/failure-mode-archive-v0.1")
INCIDENT_ROOT = ARCHIVE_ROOT / "incidents" / INCIDENT_ID
RECORD_PATHS = {
    "incident": INCIDENT_ROOT / "INCIDENT_RECORD_v0_1.json",
    "classification": INCIDENT_ROOT / "CLAIM_CONSUMPTION_FAILURE_CLASSIFICATION_v0_1.json",
    "continuance": INCIDENT_ROOT / "CONTINUANCE_BASIS_v0_1.json",
    "manifest": INCIDENT_ROOT / "PRESERVATION_MANIFEST_v0_1.json",
    "residual": INCIDENT_ROOT / "RESIDUAL_CONDITIONS_v0_1.json",
    "failure_registry": ARCHIVE_ROOT / "FAILURE_CLASS_REGISTRY_v0_1.json",
    "path_registry": ARCHIVE_ROOT / "CONTINUANCE_PATH_REGISTRY_v0_1.json",
}
SCHEMA_BINDINGS = {
    "incident": Path("schemas/preservation_incident_record_v0_1.schema.json"),
    "classification": Path("schemas/claim_consumption_failure_classification_v0_1.schema.json"),
    "manifest": Path("schemas/preservation_manifest_v0_1.schema.json"),
}


class DuplicateKeyError(ValueError):
    pass


def finding(code: str, message: str, path: str) -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load_json(root: Path, relative: Path, errors: list[dict[str, str]]) -> Any | None:
    path = root / relative
    label = relative.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(finding("REQUIRED_FILE_MISSING", "Required file is absent.", label))
        return None
    except OSError as exc:
        errors.append(finding("FILE_READ_ERROR", str(exc), label))
        return None

    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_keys)
    except DuplicateKeyError as exc:
        errors.append(finding("DUPLICATE_JSON_KEY", f"Duplicate JSON key: {exc}", label))
    except json.JSONDecodeError as exc:
        errors.append(
            finding(
                "JSON_PARSE_ERROR",
                f"{exc.msg} at line {exc.lineno}, column {exc.colno}",
                label,
            )
        )
    return None


def json_path(error: Any) -> str:
    rendered = "$"
    for part in error.absolute_path:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def validate_schema(
    name: str,
    instance: Any,
    root: Path,
    errors: list[dict[str, str]],
) -> None:
    if instance is None:
        return
    schema_path = SCHEMA_BINDINGS[name]
    schema = load_json(root, schema_path, errors)
    if schema is None:
        return
    if jsonschema is None:
        errors.append(
            finding(
                "JSONSCHEMA_DEPENDENCY_UNAVAILABLE",
                f"jsonschema could not be imported: {JSONSCHEMA_IMPORT_ERROR}",
                schema_path.as_posix(),
            )
        )
        return
    try:
        jsonschema.Draft7Validator.check_schema(schema)
    except jsonschema.SchemaError as exc:
        errors.append(finding("SCHEMA_INVALID", exc.message, schema_path.as_posix()))
        return
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        errors.append(
            finding(
                "SCHEMA_VALIDATION_ERROR",
                error.message,
                f"{RECORD_PATHS[name].as_posix()}:{json_path(error)}",
            )
        )


def expect(
    condition: bool,
    code: str,
    message: str,
    path: str,
    errors: list[dict[str, str]],
) -> None:
    if not condition:
        errors.append(finding(code, message, path))


def git_blob_sha1(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def check_records(root: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    records = {name: load_json(root, path, errors) for name, path in RECORD_PATHS.items()}
    for name in SCHEMA_BINDINGS:
        validate_schema(name, records[name], root, errors)

    incident = records["incident"]
    classification = records["classification"]
    continuance = records["continuance"]
    manifest = records["manifest"]
    residual = records["residual"]
    registry = records["failure_registry"]
    path_registry = records["path_registry"]

    if isinstance(incident, dict):
        affected = incident.get("affected_artifact", {})
        actor = incident.get("producing_actor", {})
        expect(incident.get("incident_id") == INCIDENT_ID, "INCIDENT_ID_MISMATCH", "Incident ID is not canonical.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(actor.get("intent") == "NOT_EVALUATED", "INTENT_MUST_REMAIN_NOT_EVALUATED", "Preservation evidence does not establish actor intent.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(affected.get("incident_commit") == INCIDENT_COMMIT, "INCIDENT_COMMIT_MISMATCH", "Incident commit changed.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(affected.get("incident_parent") == PRE_INCIDENT_COMMIT, "INCIDENT_PARENT_MISMATCH", "Pre-incident commit changed.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(incident.get("historical_rewrite_authority") == "NONE", "HISTORICAL_REWRITE_AUTHORITY_EXPANDED", "Preservation grants no authority to rewrite history.", RECORD_PATHS["incident"].as_posix(), errors)
        effect = incident.get("experiment_effect", {})
        expect(isinstance(effect, dict) and bool(effect), "EXPERIMENT_BOUNDARY_MISSING", "Experiment-effect boundary must be explicit.", RECORD_PATHS["incident"].as_posix(), errors)
        if isinstance(effect, dict):
            for key, value in sorted(effect.items()):
                expect(value is False, "EXPERIMENT_BOUNDARY_EFFECT", f"Preservation must not change experiment state: {key}.", f"{RECORD_PATHS['incident'].as_posix()}:$.experiment_effect.{key}", errors)
        related = {
            item.get("number"): item
            for item in incident.get("related_pull_requests", [])
            if isinstance(item, dict)
        }
        pr58 = related.get(58, {})
        observations = pr58.get("status_observations", []) if isinstance(pr58, dict) else []
        states = {
            item.get("observed_state")
            for item in observations
            if isinstance(item, dict)
        }
        expect(pr58.get("disposition") == "CLOSED_WITHOUT_MERGE_PRESERVED_AS_PRE_ADMISSION_EVIDENCE", "PR58_DISPOSITION_MISMATCH", "PR #58 must remain closed without merge in the preservation record.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(states == {"OPEN", "CLOSED"}, "PR58_TEMPORAL_STATES_COLLAPSED", "PR #58 must preserve both its screenshot-visible open state and its later closed state.", RECORD_PATHS["incident"].as_posix(), errors)
        screenshot_observation = next(
            (
                item
                for item in observations
                if isinstance(item, dict)
                and item.get("observation_source") == "USER_SUPPLIED_SCREENSHOT"
            ),
            {},
        )
        expect(screenshot_observation.get("source_sha256") == "67ad5b72ecf1d43427a997aa7da0a4579a69ea3aa3315c54287c8c9e4ee92a49", "PR58_SCREENSHOT_DIGEST_MISMATCH", "PR #58 screenshot digest changed.", RECORD_PATHS["incident"].as_posix(), errors)
        expect(screenshot_observation.get("check_summary") == {"failure": 5, "success": 4}, "PR58_SCREENSHOT_CHECK_SUMMARY_MISMATCH", "PR #58 screenshot check counts changed.", RECORD_PATHS["incident"].as_posix(), errors)

    if isinstance(classification, dict):
        expect(classification.get("incident_id") == INCIDENT_ID, "CLASSIFICATION_INCIDENT_MISMATCH", "Classification points to another incident.", RECORD_PATHS["classification"].as_posix(), errors)
        expect(classification.get("failure_class_id") == FAILURE_CLASS_ID, "FAILURE_CLASS_MISMATCH", "Failure class is not CCF-001.", RECORD_PATHS["classification"].as_posix(), errors)
        expect(classification.get("intent") == "NOT_EVALUATED", "INTENT_MUST_REMAIN_NOT_EVALUATED", "Classification must not infer actor intent.", RECORD_PATHS["classification"].as_posix(), errors)
        expect(classification.get("authority_effect") == "NONE", "CLASSIFICATION_AUTHORITY_EXPANDED", "Classification grants no authority.", RECORD_PATHS["classification"].as_posix(), errors)

    if isinstance(continuance, dict):
        expect(continuance.get("incident_id") == INCIDENT_ID, "CONTINUANCE_INCIDENT_MISMATCH", "Continuance basis points to another incident.", RECORD_PATHS["continuance"].as_posix(), errors)
        expect(continuance.get("selected_path_class") == "EXACT_PRESERVED_STATE", "CONTINUANCE_PATH_MISMATCH", "Incident uses the exact preserved-state path.", RECORD_PATHS["continuance"].as_posix(), errors)
        expect(continuance.get("exact_pre_incident_commit") == PRE_INCIDENT_COMMIT, "CONTINUANCE_COMMIT_MISMATCH", "Continuance basis changed.", RECORD_PATHS["continuance"].as_posix(), errors)
        expect(continuance.get("preserved_post_incident_descendant") == POST_INCIDENT_DESCENDANT, "DESCENDANT_REFERENCE_MISMATCH", "Preserved descendant reference changed.", RECORD_PATHS["continuance"].as_posix(), errors)
        expect(continuance.get("main_ref_effect") == "NONE", "MAIN_REF_EFFECT_PROHIBITED", "Preservation must not move main.", RECORD_PATHS["continuance"].as_posix(), errors)
        expect(continuance.get("continuation_validity_authority") == "EXTERNAL_TO_FORK", "CONTINUATION_AUTHORITY_COLLAPSE", "Fork does not decide continuation validity.", RECORD_PATHS["continuance"].as_posix(), errors)

    if isinstance(residual, dict):
        conditions = residual.get("conditions")
        expect(residual.get("status") == "OPEN", "RESIDUAL_STATUS_NOT_OPEN", "Unresolved conditions remain open.", RECORD_PATHS["residual"].as_posix(), errors)
        expect(isinstance(conditions, list) and len(conditions) > 0, "RESIDUAL_CONDITIONS_EMPTY", "Residual conditions may not be erased.", RECORD_PATHS["residual"].as_posix(), errors)

    class_ids: set[str] = set()
    if isinstance(registry, dict) and isinstance(registry.get("classes"), list):
        class_ids = {entry.get("failure_class_id") for entry in registry["classes"] if isinstance(entry, dict)}
    expect(FAILURE_CLASS_ID in class_ids, "FAILURE_CLASS_UNREGISTERED", "CCF-001 is absent from the failure-class registry.", RECORD_PATHS["failure_registry"].as_posix(), errors)

    path_classes: set[str] = set()
    if isinstance(path_registry, dict) and isinstance(path_registry.get("paths"), list):
        path_classes = {entry.get("path_class") for entry in path_registry["paths"] if isinstance(entry, dict)}
    for required in {"EXACT_PRESERVED_STATE", "AMENDED_SAFE_PATH", "RECONSTRUCTED_WITH_DECLARED_GAPS", "NO_VERIFIED_SAFE_PATH_ESTABLISHED"}:
        expect(required in path_classes, "CONTINUANCE_PATH_CLASS_MISSING", f"Required path class missing: {required}.", RECORD_PATHS["path_registry"].as_posix(), errors)

    specimen_facts: list[dict[str, Any]] = []
    specimens = manifest.get("specimens", []) if isinstance(manifest, dict) else []
    if isinstance(manifest, dict):
        expect(manifest.get("incident_id") == INCIDENT_ID, "MANIFEST_INCIDENT_MISMATCH", "Manifest points to another incident.", RECORD_PATHS["manifest"].as_posix(), errors)
        expect(manifest.get("historical_rewrite_authority") == "NONE", "HISTORICAL_REWRITE_AUTHORITY_EXPANDED", "Manifest grants no authority to rewrite history.", RECORD_PATHS["manifest"].as_posix(), errors)

    if isinstance(specimens, list):
        for index, specimen in enumerate(specimens):
            if not isinstance(specimen, dict):
                continue
            base = f"{RECORD_PATHS['manifest'].as_posix()}:$.specimens[{index}]"
            archive_value = specimen.get("archive_path")
            archive_path = PurePosixPath(archive_value) if isinstance(archive_value, str) else None
            inert = (
                archive_path is not None
                and not archive_path.is_absolute()
                and ".." not in archive_path.parts
                and archive_path.suffix == ".txt"
                and PurePosixPath(".github/workflows") not in list(archive_path.parents)
            )
            expect(inert, "ARCHIVE_PATH_NOT_INERT", "Specimen must be stored as .txt outside .github/workflows.", base, errors)
            expect(specimen.get("archive_execution_state") == "INERT_DATA_ONLY", "ARCHIVE_EXECUTION_STATE_INVALID", "Archived specimens are inert data only.", base, errors)
            expect(specimen.get("live_path_reintroduction_prohibited") is True, "LIVE_REINTRODUCTION_NOT_PROHIBITED", "The quarantined digest may not return to a live workflow path.", base, errors)
            expect(specimen.get("source_commit") == INCIDENT_COMMIT, "SPECIMEN_SOURCE_COMMIT_MISMATCH", "Specimen source commit changed.", base, errors)
            if not inert or archive_path is None:
                continue
            disk_path = root.joinpath(*archive_path.parts)
            if disk_path.is_symlink():
                errors.append(finding("ARCHIVE_SPECIMEN_SYMLINK_PROHIBITED", "Archived specimens must be regular repository files, not symbolic links.", archive_path.as_posix()))
                continue
            try:
                content = disk_path.read_bytes()
            except FileNotFoundError:
                errors.append(finding("SPECIMEN_MISSING", "Archived specimen is absent.", archive_path.as_posix()))
                continue
            sha256 = hashlib.sha256(content).hexdigest()
            blob = git_blob_sha1(content)
            expect(sha256 == specimen.get("sha256"), "SPECIMEN_SHA256_MISMATCH", "Archived specimen bytes do not match the manifest SHA-256.", archive_path.as_posix(), errors)
            expect(blob == specimen.get("git_blob_sha1"), "SPECIMEN_GIT_BLOB_MISMATCH", "Archived specimen bytes do not match the manifest Git blob.", archive_path.as_posix(), errors)
            if isinstance(incident, dict):
                affected = incident.get("affected_artifact", {})
                expect(affected.get("sha256") == sha256, "INCIDENT_SPECIMEN_SHA256_MISMATCH", "Incident record and specimen bytes differ.", RECORD_PATHS["incident"].as_posix(), errors)
                expect(affected.get("git_blob_sha1") == blob, "INCIDENT_SPECIMEN_BLOB_MISMATCH", "Incident record and specimen bytes differ.", RECORD_PATHS["incident"].as_posix(), errors)
            specimen_facts.append({
                "specimen_id": specimen.get("specimen_id"),
                "archive_path": archive_path.as_posix(),
                "sha256": sha256,
                "git_blob_sha1": blob,
                "bytes": len(content),
            })

            workflows = root / ".github" / "workflows"
            if workflows.is_dir():
                for live in sorted(path for path in workflows.iterdir() if path.is_file()):
                    live_sha256 = hashlib.sha256(live.read_bytes()).hexdigest()
                    expect(live_sha256 != sha256, "QUARANTINED_DIGEST_IN_LIVE_WORKFLOW", "A quarantined specimen digest is present in the live workflow directory.", live.relative_to(root).as_posix(), errors)

    details = {
        "incident_id": INCIDENT_ID,
        "failure_class_id": FAILURE_CLASS_ID,
        "pre_incident_commit": PRE_INCIDENT_COMMIT,
        "incident_commit": INCIDENT_COMMIT,
        "preserved_post_incident_descendant": POST_INCIDENT_DESCENDANT,
        "specimens": specimen_facts,
        "record_count": sum(value is not None for value in records.values()),
        "schema_count": len(SCHEMA_BINDINGS),
    }
    errors.sort(key=lambda item: (item["code"], item["path"], item["message"]))
    return details, errors


def build_output(root: Path) -> dict[str, Any]:
    details, errors = check_records(root)
    return {
        "checker_id": CHECKER_ID,
        "result": {
            "ok": not errors,
            "result_kind": "STRUCTURAL_PASS" if not errors else "PRESERVATION_INTEGRITY_FAILED",
        },
        "verification": details,
        "errors": errors,
        "non_claims": {
            "does_not_evaluate_intent": True,
            "does_not_certify_security": True,
            "does_not_authorize_execution": True,
            "does_not_validate_experiment_results": True,
            "does_not_move_repository_refs": True,
            "does_not_determine_continuation_validity": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    output = build_output(root)
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.write_receipt:
        receipt_path = args.write_receipt
        if not receipt_path.is_absolute():
            receipt_path = root / receipt_path
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if output["result"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
