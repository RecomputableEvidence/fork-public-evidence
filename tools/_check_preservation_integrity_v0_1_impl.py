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
DEPENDENCY_EXAMPLE_ID = "FORK-EXAMPLE-2026-07-17-001"
DEPENDENCY_FAILURE_CLASS_ID = "VDF-001_VERIFICATION_DEPENDENCY_SCOPE_ASSUMPTION"
PRE_INCIDENT_COMMIT = "fc3a100563eb354924787759accfc7ecd39ae94d"
INCIDENT_COMMIT = "7080e198e6f87e918121af6097a6ef36fd8e7a07"
POST_INCIDENT_DESCENDANT = "fd93d051235ec43bee925878bc916d09179b3c90"
DEPENDENCY_EXAMPLE_BASE_COMMIT = "599d3e193d86a9661fbbec3213ae1921b4959f10"
DEPENDENCY_EXAMPLE_FAILING_COMMIT = "425ea7af804c3da331fd7eb6cbfe644b64a36a24"
DEPENDENCY_EXAMPLE_FAILING_TREE = "3eabf2f6c4db18af2cbdd98d28d4d59857d3c34a"
DEPENDENCY_EXAMPLE_REPAIR_COMMIT = "ed2f4d1f176b63d6d2e6a4a2c77c351593253478"
DEPENDENCY_EXAMPLE_REPAIR_TREE = "56be860091e04c9e02db1ada66124a908cbf95b0"

ARCHIVE_ROOT = Path("docs/preservation/failure-mode-archive-v0.1")
INCIDENT_ROOT = ARCHIVE_ROOT / "incidents" / INCIDENT_ID
DEPENDENCY_EXAMPLE_ROOT = ARCHIVE_ROOT / "examples" / DEPENDENCY_EXAMPLE_ID
RECORD_PATHS = {
    "incident": INCIDENT_ROOT / "INCIDENT_RECORD_v0_1.json",
    "classification": INCIDENT_ROOT / "CLAIM_CONSUMPTION_FAILURE_CLASSIFICATION_v0_1.json",
    "continuance": INCIDENT_ROOT / "CONTINUANCE_BASIS_v0_1.json",
    "manifest": INCIDENT_ROOT / "PRESERVATION_MANIFEST_v0_1.json",
    "residual": INCIDENT_ROOT / "RESIDUAL_CONDITIONS_v0_1.json",
    "failure_registry": ARCHIVE_ROOT / "FAILURE_CLASS_REGISTRY_v0_1.json",
    "path_registry": ARCHIVE_ROOT / "CONTINUANCE_PATH_REGISTRY_v0_1.json",
    "dependency_example": DEPENDENCY_EXAMPLE_ROOT / "FAILURE_MODE_EXAMPLE_v0_1.json",
}
SCHEMA_BINDINGS = {
    "incident": Path("schemas/preservation_incident_record_v0_1.schema.json"),
    "classification": Path("schemas/claim_consumption_failure_classification_v0_1.schema.json"),
    "manifest": Path("schemas/preservation_manifest_v0_1.schema.json"),
    "dependency_example": Path("schemas/verification_dependency_scope_example_v0_1.schema.json"),
}

EXPECTED_DEPENDENCY_EXAMPLE_OBSERVATIONS = {
    "failing_attempt": {
        "observation_source": "GITHUB_ACTIONS_CHECK_RUNS",
        "evidence_run": 29559246618,
        "evidence_run_url": "https://github.com/RecomputableEvidence/fork-public-evidence/actions/runs/29559246618",
        "proof_run": 29559246805,
        "proof_run_url": "https://github.com/RecomputableEvidence/fork-public-evidence/actions/runs/29559246805",
        "jobs": [
            {"job_id": 87817972943, "name": "Claim Boundary and Preservation Checks", "conclusion": "success"},
            {"job_id": 87817973433, "name": "CSH execution instrumentation v0.1.1 (ubuntu-latest)", "conclusion": "success"},
            {"job_id": 87817973445, "name": "Python proof surface (windows-latest)", "conclusion": "failure"},
            {"job_id": 87817973464, "name": "PowerShell 5.1 proof-surface entry point", "conclusion": "failure"},
            {"job_id": 87817973492, "name": "Python proof surface (ubuntu-latest)", "conclusion": "failure"},
            {"job_id": 87817973498, "name": "CSH execution instrumentation v0.1.1 (windows-latest)", "conclusion": "success"},
        ],
    },
    "repair_attempt": {
        "observation_source": "GITHUB_ACTIONS_CHECK_RUNS",
        "evidence_run": 29559491579,
        "evidence_run_url": "https://github.com/RecomputableEvidence/fork-public-evidence/actions/runs/29559491579",
        "proof_run": 29559491483,
        "proof_run_url": "https://github.com/RecomputableEvidence/fork-public-evidence/actions/runs/29559491483",
        "jobs": [
            {"job_id": 87818704030, "name": "Claim Boundary and Preservation Checks", "conclusion": "success"},
            {"job_id": 87818703703, "name": "PowerShell 5.1 proof-surface entry point", "conclusion": "success"},
            {"job_id": 87818703721, "name": "CSH execution instrumentation v0.1.1 (windows-latest)", "conclusion": "success"},
            {"job_id": 87818703729, "name": "CSH execution instrumentation v0.1.1 (ubuntu-latest)", "conclusion": "success"},
            {"job_id": 87818703732, "name": "Python proof surface (windows-latest)", "conclusion": "success"},
            {"job_id": 87818703750, "name": "Python proof surface (ubuntu-latest)", "conclusion": "success"},
        ],
    },
}

EXPECTED_DEPENDENCY_EXAMPLE_SPECIMENS = {
    "FAILING_TEST_MODULE": {
        "source_commit": DEPENDENCY_EXAMPLE_FAILING_COMMIT,
        "sha256": "748779671f2dac51509b52b087b405f9af139b8f4aa7afbc8e401443004104e4",
        "git_blob_sha1": "ae0676e37d91542598b4f0f65ee61fcc5b9dd116",
        "size_bytes": 11359,
    },
    "REPAIRED_TEST_MODULE": {
        "source_commit": DEPENDENCY_EXAMPLE_REPAIR_COMMIT,
        "sha256": "cfe393cf9f739e6e993ae2a17966127953c800224101c7f39c8d833a65563e64",
        "git_blob_sha1": "2b0d703f80a459faeb824d1c2d11b6a15d6927fb",
        "size_bytes": 11539,
    },
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
    dependency_example = records["dependency_example"]

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
    expect(DEPENDENCY_FAILURE_CLASS_ID in class_ids, "DEPENDENCY_FAILURE_CLASS_UNREGISTERED", "VDF-001 is absent from the failure-class registry.", RECORD_PATHS["failure_registry"].as_posix(), errors)

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

    example_specimen_facts: list[dict[str, Any]] = []
    if isinstance(dependency_example, dict):
        example_path = RECORD_PATHS["dependency_example"].as_posix()
        expect(dependency_example.get("example_id") == DEPENDENCY_EXAMPLE_ID, "DEPENDENCY_EXAMPLE_ID_MISMATCH", "Dependency-scope example ID changed.", example_path, errors)
        expect(dependency_example.get("status") == "PRESERVED_RESOLVED", "DEPENDENCY_EXAMPLE_STATUS_MISMATCH", "The classified example must remain preserved and resolved.", example_path, errors)
        expect(dependency_example.get("failure_class_id") == DEPENDENCY_FAILURE_CLASS_ID, "DEPENDENCY_EXAMPLE_CLASS_MISMATCH", "The example is not classified as VDF-001.", example_path, errors)
        expect(dependency_example.get("intent") == "NOT_EVALUATED", "DEPENDENCY_EXAMPLE_INTENT_INFERRED", "The classified example may not infer intent.", example_path, errors)

        subject = dependency_example.get("subject", {})
        expected_subject = {
            "pull_request": "https://github.com/RecomputableEvidence/fork-public-evidence/pull/64",
            "base_commit": DEPENDENCY_EXAMPLE_BASE_COMMIT,
            "failing_commit": DEPENDENCY_EXAMPLE_FAILING_COMMIT,
            "failing_tree": DEPENDENCY_EXAMPLE_FAILING_TREE,
            "repair_commit": DEPENDENCY_EXAMPLE_REPAIR_COMMIT,
            "repair_tree": DEPENDENCY_EXAMPLE_REPAIR_TREE,
            "affected_path": "tests/test_independent_verification_surface_v0_1.py",
        }
        expect(subject == expected_subject, "DEPENDENCY_EXAMPLE_SUBJECT_MISMATCH", "The preserved PR, commit, tree, or affected-path boundary changed.", f"{example_path}:$.subject", errors)
        expect(dependency_example.get("observations") == EXPECTED_DEPENDENCY_EXAMPLE_OBSERVATIONS, "DEPENDENCY_EXAMPLE_OBSERVATIONS_MISMATCH", "The exact first-run or repair-run observations changed.", f"{example_path}:$.observations", errors)

        surfaces = {
            item.get("surface_id"): item
            for item in dependency_example.get("dependency_surfaces", [])
            if isinstance(item, dict)
        }
        expect(surfaces.get("FORK_EVIDENCE_CI", {}).get("locks") == ["requirements-proof-surface.lock.txt", "requirements-claim-admission.lock.txt"], "DEPENDENCY_SCOPE_EVIDENCE_LOCKS_MISMATCH", "Evidence CI must retain both declared locks.", f"{example_path}:$.dependency_surfaces", errors)
        expect(surfaces.get("FORK_EVIDENCE_CI", {}).get("pyyaml_expected") is True, "DEPENDENCY_SCOPE_EVIDENCE_EXPECTATION_MISMATCH", "PyYAML is expected on the claim-admission surface.", f"{example_path}:$.dependency_surfaces", errors)
        expect(surfaces.get("FORK_PROOF_SURFACE_INTEGRATION", {}).get("locks") == ["requirements-proof-surface.lock.txt"], "DEPENDENCY_SCOPE_PROOF_LOCKS_MISMATCH", "Proof-Surface Integration must retain the proof-only lock contract.", f"{example_path}:$.dependency_surfaces", errors)
        expect(surfaces.get("FORK_PROOF_SURFACE_INTEGRATION", {}).get("pyyaml_expected") is False, "DEPENDENCY_SCOPE_PROOF_EXPECTATION_MISMATCH", "PyYAML is not part of the proof-only lock contract.", f"{example_path}:$.dependency_surfaces", errors)

        safe_path = dependency_example.get("safe_path", {})
        expect(safe_path.get("path_class") == "AMENDED_SAFE_PATH", "DEPENDENCY_EXAMPLE_SAFE_PATH_MISMATCH", "The dependency edge uses the amended safe path.", f"{example_path}:$.safe_path", errors)
        walkthrough = safe_path.get("walkthrough")
        if isinstance(walkthrough, str):
            walkthrough_path = PurePosixPath(walkthrough)
            expect(not walkthrough_path.is_absolute() and ".." not in walkthrough_path.parts and root.joinpath(*walkthrough_path.parts).is_file(), "DEPENDENCY_EXAMPLE_WALKTHROUGH_MISSING", "The safe-path walkthrough must be a repository file.", f"{example_path}:$.safe_path.walkthrough", errors)

        effects = dependency_example.get("authority_effects", {})
        for boundary in ("pr_63", "main", "repository_settings", "experiment_execution", "merge"):
            expect(effects.get(boundary) == "NONE", "DEPENDENCY_EXAMPLE_AUTHORITY_EXPANDED", f"The example grants no authority over {boundary}.", f"{example_path}:$.authority_effects.{boundary}", errors)

        example_specimens = dependency_example.get("specimens", [])
        roles = {item.get("role") for item in example_specimens if isinstance(item, dict)}
        expect(roles == set(EXPECTED_DEPENDENCY_EXAMPLE_SPECIMENS), "DEPENDENCY_EXAMPLE_SPECIMEN_ROLES_MISMATCH", "The failing and repaired specimen roles must both be preserved.", f"{example_path}:$.specimens", errors)
        for index, specimen in enumerate(example_specimens):
            if not isinstance(specimen, dict):
                continue
            base = f"{example_path}:$.specimens[{index}]"
            role = specimen.get("role")
            expected = EXPECTED_DEPENDENCY_EXAMPLE_SPECIMENS.get(role, {})
            archive_value = specimen.get("archive_path")
            archive_path = PurePosixPath(archive_value) if isinstance(archive_value, str) else None
            inert = (
                archive_path is not None
                and not archive_path.is_absolute()
                and ".." not in archive_path.parts
                and archive_path.suffix == ".txt"
                and PurePosixPath(".github/workflows") not in list(archive_path.parents)
                and DEPENDENCY_EXAMPLE_ROOT in archive_path.parents
            )
            expect(inert, "DEPENDENCY_EXAMPLE_ARCHIVE_PATH_NOT_INERT", "Example specimens must be .txt data within the classified example archive.", base, errors)
            expect(specimen.get("execution_state") == "INERT_TEXT_DATA_ONLY", "DEPENDENCY_EXAMPLE_EXECUTION_STATE_INVALID", "Example specimens are inert text data only.", base, errors)
            for field in ("source_commit", "sha256", "git_blob_sha1", "size_bytes"):
                expect(specimen.get(field) == expected.get(field), "DEPENDENCY_EXAMPLE_SPECIMEN_FACT_MISMATCH", f"Preserved {role} {field} changed.", f"{base}.{field}", errors)
            if not inert or archive_path is None:
                continue
            disk_path = root.joinpath(*archive_path.parts)
            if disk_path.is_symlink():
                errors.append(finding("DEPENDENCY_EXAMPLE_SPECIMEN_SYMLINK_PROHIBITED", "Example specimens must be regular repository files.", archive_path.as_posix()))
                continue
            try:
                content = disk_path.read_bytes()
            except FileNotFoundError:
                errors.append(finding("DEPENDENCY_EXAMPLE_SPECIMEN_MISSING", "Classified example specimen is absent.", archive_path.as_posix()))
                continue
            sha256 = hashlib.sha256(content).hexdigest()
            blob = git_blob_sha1(content)
            expect(sha256 == specimen.get("sha256"), "DEPENDENCY_EXAMPLE_SPECIMEN_SHA256_MISMATCH", "Example specimen bytes do not match the recorded SHA-256.", archive_path.as_posix(), errors)
            expect(blob == specimen.get("git_blob_sha1"), "DEPENDENCY_EXAMPLE_SPECIMEN_GIT_BLOB_MISMATCH", "Example specimen bytes do not match the recorded Git blob.", archive_path.as_posix(), errors)
            expect(len(content) == specimen.get("size_bytes"), "DEPENDENCY_EXAMPLE_SPECIMEN_SIZE_MISMATCH", "Example specimen byte count changed.", archive_path.as_posix(), errors)
            example_specimen_facts.append({
                "role": role,
                "archive_path": archive_path.as_posix(),
                "sha256": sha256,
                "git_blob_sha1": blob,
                "bytes": len(content),
            })

    details = {
        "incident_id": INCIDENT_ID,
        "failure_class_id": FAILURE_CLASS_ID,
        "pre_incident_commit": PRE_INCIDENT_COMMIT,
        "incident_commit": INCIDENT_COMMIT,
        "preserved_post_incident_descendant": POST_INCIDENT_DESCENDANT,
        "specimens": specimen_facts,
        "classified_examples": [{
            "example_id": DEPENDENCY_EXAMPLE_ID,
            "failure_class_id": DEPENDENCY_FAILURE_CLASS_ID,
            "status": dependency_example.get("status") if isinstance(dependency_example, dict) else None,
            "specimens": example_specimen_facts,
        }],
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
