#!/usr/bin/env python3
"""Shared validation utilities for the CSH post-repair evidence architecture v0.1."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from jsonschema import Draft202012Validator, FormatChecker

PROFILE = "FORK-JCS-v0.1"
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

SCHEMAS = {
    "execution": SCHEMA_DIR / "csh_execution_receipt_v0_1_1.schema.json",
    "classification": SCHEMA_DIR / "csh_run_classification_v0_1.schema.json",
    "pair": SCHEMA_DIR / "csh_pair_comparison_v0_1.schema.json",
    "reviewer": SCHEMA_DIR / "csh_reviewer_receipt_v0_1.schema.json",
    "manifest": SCHEMA_DIR / "csh_integrated_evidence_chain_manifest_v0_1.schema.json",
}

FORBIDDEN_REVIEW_PATTERNS = [
    re.compile(r"\bi endorse fork\b", re.IGNORECASE),
    re.compile(r"\bthis (?:receipt|review) endorses fork\b", re.IGNORECASE),
    re.compile(r"\bauthority (?:is|was|has been) transferred\b", re.IGNORECASE),
    re.compile(r"\bconfers authority\b", re.IGNORECASE),
    re.compile(r"\bproves (?:the )?claim (?:is )?true\b", re.IGNORECASE),
    re.compile(r"\bcertifies compliance\b", re.IGNORECASE),
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_projection(record: Dict[str, Any]) -> Dict[str, Any]:
    projected = copy.deepcopy(record)
    integrity = projected.get("record_integrity")
    if isinstance(integrity, dict):
        integrity.pop("canonical_record_sha256", None)
    return projected


def canonical_bytes(record: Dict[str, Any]) -> bytes:
    projected = canonical_projection(record)
    # Schemas prohibit floating-point values in digest-bearing fields used here.
    encoded = json.dumps(
        projected,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return encoded.encode("utf-8")


def canonical_sha256(record: Dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(record))


def verify_canonical_hash(record: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    integrity = record.get("record_integrity")
    if not isinstance(integrity, dict):
        return ["record_integrity is absent or not an object"]
    if integrity.get("canonicalization_profile") != PROFILE:
        errors.append(
            f"canonicalization_profile must be {PROFILE!r}"
        )
    declared = integrity.get("canonical_record_sha256")
    actual = canonical_sha256(record)
    if declared != actual:
        errors.append(
            f"canonical_record_sha256 mismatch: declared={declared!r} actual={actual}"
        )
    return errors


def validate_schema(record: Dict[str, Any], schema_path: Path) -> List[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
        location = "$"
        if error.absolute_path:
            location += "." + ".".join(str(part) for part in error.absolute_path)
        errors.append(f"{location}: {error.message}")
    return errors


def safe_repo_path(repo_root: Path, relative_path: str) -> Tuple[Optional[Path], Optional[str]]:
    candidate = (repo_root / relative_path).resolve()
    root = repo_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None, f"path escapes repository root: {relative_path}"
    return candidate, None


def verify_hash_ref(repo_root: Path, ref: Dict[str, Any], label: str) -> List[str]:
    errors: List[str] = []
    relative_path = ref.get("path")
    declared_hash = ref.get("sha256")
    if not isinstance(relative_path, str):
        return [f"{label}.path is not a string"]
    resolved, path_error = safe_repo_path(repo_root, relative_path)
    if path_error:
        return [f"{label}: {path_error}"]
    assert resolved is not None
    if not resolved.is_file():
        return [f"{label}: referenced file does not exist: {relative_path}"]
    actual = sha256_file(resolved)
    if actual != declared_hash:
        errors.append(
            f"{label}: sha256 mismatch for {relative_path}: declared={declared_hash!r} actual={actual}"
        )
    return errors


def verify_artifact_ref(repo_root: Path, ref: Dict[str, Any], label: str) -> List[str]:
    present = ref.get("present")
    path = ref.get("path")
    digest = ref.get("sha256")
    if present is True:
        if not isinstance(path, str) or not isinstance(digest, str):
            return [f"{label}: present artifact must provide path and sha256"]
        return verify_hash_ref(repo_root, {"path": path, "sha256": digest}, label)
    if present is False:
        errors = []
        if path is not None:
            errors.append(f"{label}: absent artifact path must be null")
        if digest is not None:
            errors.append(f"{label}: absent artifact sha256 must be null")
        return errors
    return [f"{label}.present must be boolean"]


def _timestamp_order_errors(record: Dict[str, Any]) -> List[str]:
    timestamps = record.get("timestamps")
    if not isinstance(timestamps, dict):
        return []
    start = timestamps.get("requested_at")
    end = timestamps.get("completed_at")
    if isinstance(start, str) and isinstance(end, str) and end < start:
        return ["timestamps.completed_at precedes timestamps.requested_at"]
    return []


def check_execution_receipt(
    record_path: Path,
    repo_root: Path,
    verify_links: bool = True,
) -> List[str]:
    record = load_json(record_path)
    errors = validate_schema(record, SCHEMAS["execution"])
    errors.extend(verify_canonical_hash(record))
    errors.extend(_timestamp_order_errors(record))

    state = record.get("execution_state")
    outcome = record.get("transport_outcome", {})
    code = outcome.get("status_code") if isinstance(outcome, dict) else None
    if state == "COMPLETED" and not (isinstance(code, int) and 200 <= code <= 299):
        errors.append("COMPLETED execution must have a 2xx transport status_code")
    if state == "UNAVAILABLE" and isinstance(code, int) and 200 <= code <= 299:
        errors.append("UNAVAILABLE execution cannot have a 2xx transport status_code")

    if verify_links and isinstance(record.get("artifacts"), dict):
        errors.extend(
            verify_artifact_ref(repo_root, record["artifacts"].get("request", {}), "artifacts.request")
        )
        errors.extend(
            verify_artifact_ref(repo_root, record["artifacts"].get("response", {}), "artifacts.response")
        )
    if verify_links and isinstance(record.get("config_links"), dict):
        for key in ("frozen_config", "amendment", "instrumentation_patch"):
            ref = record["config_links"].get(key)
            if isinstance(ref, dict):
                errors.extend(verify_hash_ref(repo_root, ref, f"config_links.{key}"))
    return errors


def check_run_classification(record_path: Path, repo_root: Path) -> List[str]:
    del repo_root
    record = load_json(record_path)
    errors = validate_schema(record, SCHEMAS["classification"])
    errors.extend(verify_canonical_hash(record))
    return errors


def check_pair_comparison(record_path: Path, repo_root: Path) -> List[str]:
    del repo_root
    record = load_json(record_path)
    errors = validate_schema(record, SCHEMAS["pair"])
    errors.extend(verify_canonical_hash(record))
    return errors


def _walk_strings(value: Any, path: str = "$") -> Iterable[Tuple[str, str]]:
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _walk_strings(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            if path == "$" and key == "non_endorsement":
                continue
            yield from _walk_strings(item, f"{path}.{key}")


def check_reviewer_receipt(record_path: Path, repo_root: Path) -> List[str]:
    del repo_root
    record = load_json(record_path)
    errors = validate_schema(record, SCHEMAS["reviewer"])
    errors.extend(verify_canonical_hash(record))
    for location, text in _walk_strings(record):
        for pattern in FORBIDDEN_REVIEW_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{location}: prohibited endorsement or authority language matched {pattern.pattern!r}"
                )
    return errors


def check_manifest_local(record_path: Path, repo_root: Path) -> List[str]:
    del repo_root
    record = load_json(record_path)
    errors = validate_schema(record, SCHEMAS["manifest"])
    errors.extend(verify_canonical_hash(record))
    return errors


def _read_ref(repo_root: Path, ref: Dict[str, Any], label: str) -> Tuple[Optional[Path], Optional[Dict[str, Any]], List[str]]:
    errors = verify_hash_ref(repo_root, ref, label)
    relative_path = ref.get("path")
    if errors or not isinstance(relative_path, str):
        return None, None, errors
    path, path_error = safe_repo_path(repo_root, relative_path)
    if path_error or path is None:
        return None, None, [f"{label}: {path_error}"]
    try:
        return path, load_json(path), []
    except Exception as exc:
        return path, None, [f"{label}: cannot read JSON: {exc}"]


def expected_relationship(control: str, instrumented: str) -> str:
    if control == "UNRESOLVED" and instrumented == "UNRESOLVED":
        return "BOTH_UNRESOLVED"
    if control == "UNRESOLVED":
        return "CONTROL_UNRESOLVED"
    if instrumented == "UNRESOLVED":
        return "INSTRUMENTED_UNRESOLVED"
    if control == instrumented:
        return "TRANSITIONS_EQUAL"
    return "TRANSITIONS_DIFFER"


def check_integrated_manifest(manifest_path: Path, repo_root: Path) -> List[str]:
    manifest = load_json(manifest_path)
    errors = validate_schema(manifest, SCHEMAS["manifest"])
    errors.extend(verify_canonical_hash(manifest))
    if errors:
        return errors

    pair_id = manifest["pair_id"]
    repetition_index = manifest["repetition_index"]

    execution_by_arm: Dict[str, Tuple[Path, Dict[str, Any]]] = {}
    classification_by_arm: Dict[str, Tuple[Path, Dict[str, Any]]] = {}

    for index, ref in enumerate(manifest["execution_receipts"]):
        arm = ref["arm_id"]
        if arm in execution_by_arm:
            errors.append(f"duplicate execution arm in manifest: {arm}")
        path, record, ref_errors = _read_ref(repo_root, ref, f"execution_receipts[{index}]")
        errors.extend(ref_errors)
        if path is None or record is None:
            continue
        local_errors = check_execution_receipt(path, repo_root, verify_links=True)
        errors.extend(f"{ref['path']}: {item}" for item in local_errors)
        execution_by_arm[arm] = (path, record)

    for index, ref in enumerate(manifest["run_classifications"]):
        arm = ref["arm_id"]
        if arm in classification_by_arm:
            errors.append(f"duplicate classification arm in manifest: {arm}")
        path, record, ref_errors = _read_ref(repo_root, ref, f"run_classifications[{index}]")
        errors.extend(ref_errors)
        if path is None or record is None:
            continue
        local_errors = check_run_classification(path, repo_root)
        errors.extend(f"{ref['path']}: {item}" for item in local_errors)
        classification_by_arm[arm] = (path, record)

    required_arms = {"CONTROL", "FORK_INSTRUMENTED"}
    if set(execution_by_arm) != required_arms:
        errors.append(
            f"execution arms must be exactly {sorted(required_arms)}; found {sorted(execution_by_arm)}"
        )
    if set(classification_by_arm) != required_arms:
        errors.append(
            f"classification arms must be exactly {sorted(required_arms)}; found {sorted(classification_by_arm)}"
        )

    pair_path, pair_record, pair_ref_errors = _read_ref(
        repo_root, manifest["pair_comparison"], "pair_comparison"
    )
    errors.extend(pair_ref_errors)
    if pair_path is not None and pair_record is not None:
        local_errors = check_pair_comparison(pair_path, repo_root)
        errors.extend(f"{manifest['pair_comparison']['path']}: {item}" for item in local_errors)

    reviewers: List[Tuple[Path, Dict[str, Any]]] = []
    for index, ref in enumerate(manifest["reviewer_receipts"]):
        path, record, ref_errors = _read_ref(repo_root, ref, f"reviewer_receipts[{index}]")
        errors.extend(ref_errors)
        if path is None or record is None:
            continue
        local_errors = check_reviewer_receipt(path, repo_root)
        errors.extend(f"{ref['path']}: {item}" for item in local_errors)
        reviewers.append((path, record))

    if errors:
        return errors

    # Cross-record identity and repetition checks.
    for arm in required_arms:
        execution = execution_by_arm[arm][1]
        classification = classification_by_arm[arm][1]
        for label, record in (("execution", execution), ("classification", classification)):
            if record["pair_id"] != pair_id:
                errors.append(f"{arm} {label} pair_id mismatch")
            if record["repetition_index"] != repetition_index:
                errors.append(f"{arm} {label} repetition_index mismatch")
            if record["arm_id"] != arm:
                errors.append(f"{arm} {label} arm_id mismatch")
        if classification["run_id"] != execution["run_id"]:
            errors.append(f"{arm} classification run_id does not match execution run_id")

        expected_exec_path = execution_by_arm[arm][0].relative_to(repo_root).as_posix()
        expected_exec_hash = sha256_file(execution_by_arm[arm][0])
        exec_ref = classification["execution_receipt_ref"]
        if exec_ref["path"] != expected_exec_path:
            errors.append(f"{arm} classification execution_receipt_ref.path mismatch")
        if exec_ref["sha256"] != expected_exec_hash:
            errors.append(f"{arm} classification execution_receipt_ref.sha256 mismatch")

        response_present = execution["artifacts"]["response"]["present"]
        if classification["observed_receiver_output"] != response_present:
            errors.append(f"{arm} observed_receiver_output disagrees with execution response presence")

        if classification["classification_disposition"] == "CLASSIFIED":
            if execution["execution_state"] != "COMPLETED" or not response_present:
                errors.append(f"{arm} CLASSIFIED record requires completed execution with receiver output")
        if execution["execution_state"] == "UNAVAILABLE" and not response_present:
            if not (
                classification["classification_disposition"] == "NOT_CLASSIFIABLE"
                and classification["classification_reason"] == "NO_RECEIVER_OUTPUT"
            ):
                errors.append(
                    f"{arm} unavailable execution without output must be NOT_CLASSIFIABLE/NO_RECEIVER_OUTPUT"
                )

    # Same frozen configuration for a paired comparison.
    control_exec = execution_by_arm["CONTROL"][1]
    instrumented_exec = execution_by_arm["FORK_INSTRUMENTED"][1]
    control_cfg = control_exec["config_links"]["frozen_config"]["sha256"]
    instrumented_cfg = instrumented_exec["config_links"]["frozen_config"]["sha256"]

    assert pair_record is not None
    if pair_record["pair_id"] != pair_id:
        errors.append("pair comparison pair_id mismatch")
    if pair_record["repetition_index"] != repetition_index:
        errors.append("pair comparison repetition_index mismatch")
    if pair_record["control_run_id"] != control_exec["run_id"]:
        errors.append("pair comparison control_run_id mismatch")
    if pair_record["instrumented_run_id"] != instrumented_exec["run_id"]:
        errors.append("pair comparison instrumented_run_id mismatch")

    for arm, field in (
        ("CONTROL", "control_classification_ref"),
        ("FORK_INSTRUMENTED", "instrumented_classification_ref"),
    ):
        expected_path = classification_by_arm[arm][0].relative_to(repo_root).as_posix()
        expected_hash = sha256_file(classification_by_arm[arm][0])
        ref = pair_record[field]
        if ref["path"] != expected_path:
            errors.append(f"pair comparison {field}.path mismatch")
        if ref["sha256"] != expected_hash:
            errors.append(f"pair comparison {field}.sha256 mismatch")

    control_class = classification_by_arm["CONTROL"][1]
    instrumented_class = classification_by_arm["FORK_INSTRUMENTED"][1]
    disposition = pair_record["pair_comparison_disposition"]
    semantic = pair_record["semantic_comparison"]

    if disposition == "COMPARABLE":
        if control_cfg != instrumented_cfg:
            errors.append("COMPARABLE pair uses different frozen configuration hashes")
        if control_class["classification_disposition"] != "CLASSIFIED":
            errors.append("COMPARABLE pair requires CLASSIFIED control arm")
        if instrumented_class["classification_disposition"] != "CLASSIFIED":
            errors.append("COMPARABLE pair requires CLASSIFIED instrumented arm")
        if isinstance(semantic, dict):
            control_transition = control_class["boundary_transition"]
            instrumented_transition = instrumented_class["boundary_transition"]
            if semantic["control_transition"] != control_transition:
                errors.append("semantic_comparison.control_transition mismatch")
            if semantic["instrumented_transition"] != instrumented_transition:
                errors.append("semantic_comparison.instrumented_transition mismatch")
            expected = expected_relationship(control_transition, instrumented_transition)
            if semantic["relationship"] != expected:
                errors.append(
                    f"semantic_comparison.relationship mismatch: expected {expected}"
                )
    elif disposition == "PARTIALLY_COMPARABLE":
        if semantic is not None:
            errors.append("PARTIALLY_COMPARABLE pair cannot contain semantic comparison")
        if (
            control_class["classification_disposition"] == "CLASSIFIED"
            and instrumented_class["classification_disposition"] == "CLASSIFIED"
            and control_cfg == instrumented_cfg
        ):
            errors.append(
                "PARTIALLY_COMPARABLE is unsupported when both arms are fully classified under the same configuration"
            )
        ops = set(pair_record["operational_comparisons"])
        if "EXECUTION_AVAILABILITY_DIFFERED" in ops:
            c_available = control_exec["execution_state"] == "COMPLETED"
            i_available = instrumented_exec["execution_state"] == "COMPLETED"
            if c_available == i_available:
                errors.append("EXECUTION_AVAILABILITY_DIFFERED is not supported by execution states")
    elif disposition == "NOT_COMPARABLE":
        if semantic is not None:
            errors.append("NOT_COMPARABLE pair cannot contain semantic comparison")
    elif disposition == "QUARANTINED":
        if semantic is not None:
            errors.append("QUARANTINED pair cannot contain semantic comparison")
        if not (
            control_class["classification_disposition"] == "QUARANTINED"
            or instrumented_class["classification_disposition"] == "QUARANTINED"
        ):
            errors.append("QUARANTINED pair requires at least one quarantined arm")

    core_refs = {
        execution_by_arm["CONTROL"][0].relative_to(repo_root).as_posix(),
        execution_by_arm["FORK_INSTRUMENTED"][0].relative_to(repo_root).as_posix(),
        classification_by_arm["CONTROL"][0].relative_to(repo_root).as_posix(),
        classification_by_arm["FORK_INSTRUMENTED"][0].relative_to(repo_root).as_posix(),
        pair_path.relative_to(repo_root).as_posix() if pair_path else "",
    }
    for path, reviewer in reviewers:
        if reviewer["pair_id"] != pair_id:
            errors.append(f"{path}: reviewer pair_id mismatch")
        if reviewer["repetition_index"] != repetition_index:
            errors.append(f"{path}: reviewer repetition_index mismatch")
        reviewed_paths = {item["path"] for item in reviewer["reviewed_artifacts"]}
        if not core_refs.issubset(reviewed_paths):
            missing = sorted(core_refs - reviewed_paths)
            errors.append(f"{path}: reviewer receipt omits core artifacts: {missing}")

    return errors


def result_payload(checker: str, target: Path, errors: List[str]) -> Dict[str, Any]:
    return {
        "checker": checker,
        "target": target.as_posix(),
        "valid": not errors,
        "error_count": len(errors),
        "errors": errors,
    }


def run_cli(
    checker_name: str,
    check_function,
    description: str,
) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    repo_root = args.repo_root.resolve()
    try:
        errors = check_function(target, repo_root)
    except Exception as exc:
        errors = [f"checker exception: {type(exc).__name__}: {exc}"]
    payload = result_payload(checker_name, target, errors)
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"{checker_name}: {'PASS' if not errors else 'FAIL'}")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1