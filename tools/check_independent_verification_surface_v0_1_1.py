#!/usr/bin/env python3
"""Harden and recompute Fork Independent Verification Surface v0.1 evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

import check_independent_verification_surface_v0_1 as legacy

CHECKER_ID = "FORK_INDEPENDENT_VERIFICATION_SURFACE_v0_1_1"
POLICY_PATH = Path("policies/independent-verification/INDEPENDENT_VERIFICATION_POLICY_v0_1_1.json")
POLICY_SCHEMA_PATH = Path("schemas/independent_verification_policy_v0_1_1.schema.json")
PLAN_SCHEMA_PATH = Path("schemas/independent_verification_plan_v0_1_1.schema.json")
RECEIPT_SCHEMA_PATH = Path("schemas/independent_verification_receipt_v0_1_1.schema.json")
MAX_PLAN_BYTES = 1024 * 1024
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
REGULAR_MODES = {"100644", "100755"}
PRECEDENCE_RENDERED = (
    "INCONCLUSIVE_EVIDENCE_GAP>INVALIDATED_BY_RECOMPUTATION>"
    "VERIFIED_WITHIN_DECLARED_SCOPE"
)


class DuplicateKeyError(ValueError):
    pass


class EvidenceUnavailable(RuntimeError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def reject_non_finite(value: str) -> None:
    raise ValueError(f"Non-finite JSON number is prohibited: {value}")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not UTF-8: {exc}") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_non_finite,
        )
    except DuplicateKeyError as exc:
        raise ValueError(f"{label} contains duplicate key {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{label} is invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc
    assert_finite(value, label)
    return value


def assert_finite(value: Any, label: str) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{label} contains a non-finite number")
    if isinstance(value, dict):
        for child in value.values():
            assert_finite(child, label)
    elif isinstance(value, list):
        for child in value:
            assert_finite(child, label)


def strict_json_file(path: Path, maximum_bytes: int | None = None) -> Any:
    raw = path.read_bytes()
    if maximum_bytes is not None and len(raw) > maximum_bytes:
        raise ValueError(f"{path} exceeds {maximum_bytes} bytes")
    return strict_json_bytes(raw, str(path))


def canonical_bytes(value: Any) -> bytes:
    assert_finite(value, "canonical value")
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    assert_finite(value, "receipt")
    return (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def safe_git_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return env


def run_git(
    root: Path,
    args: list[str],
    *,
    check: bool = True,
    text: bool = False,
) -> subprocess.CompletedProcess[Any]:
    completed = subprocess.run(
        [
            "git",
            "-c",
            f"core.hooksPath={os.devnull}",
            "-c",
            "protocol.file.allow=never",
            *args,
        ],
        cwd=str(root),
        env=safe_git_env(),
        capture_output=True,
        text=text,
        check=False,
    )
    if check and completed.returncode != 0:
        stderr = completed.stderr if text else completed.stderr.decode("utf-8", errors="replace")
        raise EvidenceUnavailable(stderr.strip() or f"git {' '.join(args)} failed")
    return completed


def git_object_blob(root: Path, commit: str, path: str) -> str:
    value = run_git(root, ["rev-parse", f"{commit}:{path}"], text=True).stdout.strip()
    if not SHA1_RE.fullmatch(value):
        raise EvidenceUnavailable(f"Invalid Git object identity for {commit}:{path}: {value!r}")
    return value


def git_tree_entry(root: Path, commit: str, path: str) -> dict[str, str]:
    raw = run_git(root, ["ls-tree", "-z", commit, "--", path]).stdout
    if not raw:
        raise EvidenceUnavailable(f"Git tree entry is unavailable: {commit}:{path}")
    entries = [entry for entry in raw.split(b"\0") if entry]
    if len(entries) != 1:
        raise EvidenceUnavailable(f"Expected one Git tree entry for {commit}:{path}")
    try:
        metadata, observed_path = entries[0].split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split(" ", 2)
        decoded_path = observed_path.decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise EvidenceUnavailable(f"Malformed Git tree entry for {commit}:{path}") from exc
    return {
        "path": decoded_path,
        "mode": mode,
        "object_type": object_type,
        "object_id": object_id,
    }


def schema_validate(instance: Any, schema_path: Path) -> None:
    schema = strict_json_file(schema_path)
    jsonschema.Draft7Validator.check_schema(schema)
    validator = jsonschema.Draft7Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    if errors:
        rendered = "; ".join(error.message for error in errors[:8])
        raise jsonschema.ValidationError(rendered)


def empty_receipt(plan_path: Path) -> dict[str, Any]:
    return {
        "checker_id": CHECKER_ID,
        "schema_version": "0.1.1",
        "mode": "CONTRIBUTION_VERIFICATION_HARDENING",
        "plan": {
            "available": False,
            "plan_id": None,
            "path": str(plan_path),
            "git_blob_sha1": None,
        },
        "verifier_provenance": {
            "available": False,
            "repository": None,
            "source_commit": None,
            "component_count": 0,
            "component_mismatches": [],
            "running_checker_matches_declared_blob": None,
        },
        "legacy_evidence": {
            "available": False,
            "plan_path": None,
            "plan_git_blob_sha1": None,
            "receipt_path": None,
            "receipt_git_blob_sha1": None,
            "recomputed_verdict": None,
            "committed_receipt_byte_exact": None,
        },
        "subject": {
            "available": False,
            "repository": None,
            "base_commit": None,
            "candidate_commit": None,
            "merge_base": None,
            "changed_path_count": 0,
        },
        "observations": {"count": 0, "contract_errors": []},
        "git_modes": {
            "checked_path_count": 0,
            "regular_blob_count": 0,
            "non_regular_paths": [],
        },
        "result": {
            "ok": False,
            "verdict": "INCONCLUSIVE_EVIDENCE_GAP",
            "precedence_applied": PRECEDENCE_RENDERED,
            "contradicted_count": 0,
            "inconclusive_count": 1,
            "control_error_count": 0,
            "merge_effect": "NONE",
            "repository_standing_effect": "NONE",
            "experiment_execution_effect": "NONE",
        },
        "control_errors": [],
        "non_claims": [
            "No merge approval",
            "No repository standing",
            "No security certification",
            "No producer-intent determination",
            "No universal semantic correctness claim",
            "No independent human review unless separately attributed",
            "No experiment execution authorization",
            "No endorsement",
        ],
    }


def classify(
    *,
    control_errors: list[str],
    contradicted_count: int,
    inconclusive_count: int,
) -> tuple[str, bool]:
    if control_errors or inconclusive_count:
        return "INCONCLUSIVE_EVIDENCE_GAP", False
    if contradicted_count:
        return "INVALIDATED_BY_RECOMPUTATION", False
    return "VERIFIED_WITHIN_DECLARED_SCOPE", True


def duplicate_assertion_ids(plan: dict[str, Any]) -> list[str]:
    assertions = plan.get("assertions", [])
    seen: set[str] = set()
    duplicates: list[str] = []
    for item in assertions:
        if not isinstance(item, dict) or not isinstance(item.get("assertion_id"), str):
            continue
        assertion_id = item["assertion_id"]
        if assertion_id in seen and assertion_id not in duplicates:
            duplicates.append(assertion_id)
        seen.add(assertion_id)
    return duplicates


def strict_candidate_json_assertions(
    root: Path,
    candidate: str,
    legacy_plan: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    for assertion in legacy_plan.get("assertions", []):
        if not isinstance(assertion, dict) or assertion.get("type") != "JSON_POINTER_EQUALS":
            continue
        path = assertion.get("path")
        if not isinstance(path, str):
            errors.append("JSON_POINTER_EQUALS assertion has no valid path")
            continue
        try:
            raw = run_git(root, ["show", f"{candidate}:{path}"]).stdout
            strict_json_bytes(raw, f"{candidate}:{path}")
        except (EvidenceUnavailable, ValueError) as exc:
            errors.append(str(exc))
    return errors


def verify(root: Path, plan_path: Path) -> dict[str, Any]:
    receipt = empty_receipt(plan_path)
    control_errors: list[str] = []
    contradictions: list[str] = []
    inconclusive_count = 0

    try:
        policy = strict_json_file(root / POLICY_PATH)
        schema_validate(policy, root / POLICY_SCHEMA_PATH)
    except (OSError, ValueError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        control_errors.append(f"Policy unavailable or invalid: {exc}")
        policy = None

    try:
        plan = strict_json_file(plan_path, maximum_bytes=MAX_PLAN_BYTES)
        schema_validate(plan, root / PLAN_SCHEMA_PATH)
        if not isinstance(plan, dict):
            raise ValueError("Plan root must be a JSON object")
    except (OSError, ValueError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        control_errors.append(f"Plan unavailable or invalid: {exc}")
        plan = None

    if plan is None:
        receipt["control_errors"] = control_errors
        receipt["result"]["control_error_count"] = len(control_errors)
        schema_validate(receipt, root / RECEIPT_SCHEMA_PATH)
        return receipt

    receipt["plan"] = {
        "available": True,
        "plan_id": plan["plan_id"],
        "path": plan_path.relative_to(root).as_posix() if plan_path.is_relative_to(root) else str(plan_path),
        "git_blob_sha1": git_blob_sha1(plan_path.read_bytes()),
    }
    receipt["observations"]["count"] = len(plan["external_observations"])

    if (plan["verdict_precedence"] != policy.get("verdict_precedence")) if isinstance(policy, dict) else True:
        contradictions.append("Plan verdict precedence does not match policy")

    release = plan["verifier_release"]
    component_mismatches: list[dict[str, Any]] = []
    running_checker_matches: bool | None = None
    try:
        run_git(root, ["cat-file", "-e", f"{release['source_commit']}^{{commit}}"])
        roles: set[str] = set()
        paths: set[str] = set()
        for component in release["components"]:
            role = component["role"]
            path = component["path"]
            if role in roles:
                component_mismatches.append({"role": role, "error": "DUPLICATE_ROLE"})
            if path in paths:
                component_mismatches.append({"path": path, "error": "DUPLICATE_PATH"})
            roles.add(role)
            paths.add(path)
            try:
                observed = git_object_blob(root, release["source_commit"], path)
            except EvidenceUnavailable as exc:
                inconclusive_count += 1
                component_mismatches.append({"role": role, "path": path, "error": str(exc)})
                continue
            if observed != component["git_blob_sha1"]:
                component_mismatches.append(
                    {
                        "role": role,
                        "path": path,
                        "expected": component["git_blob_sha1"],
                        "observed": observed,
                    }
                )
        checker_component = next(
            (item for item in release["components"] if item["role"] == "HARDENED_CHECKER"),
            None,
        )
        if checker_component is None:
            component_mismatches.append({"role": "HARDENED_CHECKER", "error": "MISSING"})
            running_checker_matches = False
        else:
            running_checker_matches = (
                git_blob_sha1(Path(__file__).read_bytes()) == checker_component["git_blob_sha1"]
            )
            if not running_checker_matches:
                component_mismatches.append(
                    {
                        "role": "HARDENED_CHECKER",
                        "error": "RUNNING_BYTES_DO_NOT_MATCH_DECLARED_BLOB",
                    }
                )
    except (EvidenceUnavailable, KeyError, OSError, ValueError) as exc:
        control_errors.append(f"Verifier provenance could not be resolved: {exc}")

    receipt["verifier_provenance"] = {
        "available": not any(error.startswith("Verifier provenance") for error in control_errors),
        "repository": release.get("repository"),
        "source_commit": release.get("source_commit"),
        "component_count": len(release.get("components", [])),
        "component_mismatches": component_mismatches,
        "running_checker_matches_declared_blob": running_checker_matches,
    }
    contradictions.extend("verifier component mismatch" for _ in component_mismatches)

    lineage = plan["legacy_lineage"]
    legacy_plan_path = root / lineage["plan_path"]
    legacy_receipt_path = root / lineage["receipt_path"]
    legacy_output: dict[str, Any] | None = None
    try:
        legacy_plan_raw = legacy_plan_path.read_bytes()
        legacy_receipt_raw = legacy_receipt_path.read_bytes()
        observed_plan_blob = git_blob_sha1(legacy_plan_raw)
        observed_receipt_blob = git_blob_sha1(legacy_receipt_raw)
        if observed_plan_blob != lineage["plan_git_blob_sha1"]:
            contradictions.append("Legacy plan blob mismatch")
        if observed_receipt_blob != lineage["receipt_git_blob_sha1"]:
            contradictions.append("Legacy receipt blob mismatch")
        legacy_plan = strict_json_bytes(legacy_plan_raw, str(legacy_plan_path))
        committed_legacy_receipt = strict_json_bytes(legacy_receipt_raw, str(legacy_receipt_path))
        duplicates = duplicate_assertion_ids(legacy_plan)
        if duplicates:
            contradictions.extend(f"Duplicate assertion id: {item}" for item in duplicates)
        strict_json_errors = strict_candidate_json_assertions(
            root,
            plan["subject"]["candidate_commit"],
            legacy_plan,
        )
        if strict_json_errors:
            control_errors.extend(strict_json_errors)
            inconclusive_count += len(strict_json_errors)
        legacy_output = legacy.verify(root, legacy_plan_path, fetch=False)
        byte_exact = pretty_bytes(legacy_output) == legacy_receipt_raw
        if not byte_exact:
            contradictions.append("Recomputed legacy receipt is not byte-exact")
        if legacy_output.get("result", {}).get("verdict") != lineage["expected_verdict"]:
            contradictions.append("Legacy verdict does not match expected verdict")
        receipt["legacy_evidence"] = {
            "available": True,
            "plan_path": lineage["plan_path"],
            "plan_git_blob_sha1": observed_plan_blob,
            "receipt_path": lineage["receipt_path"],
            "receipt_git_blob_sha1": observed_receipt_blob,
            "recomputed_verdict": legacy_output.get("result", {}).get("verdict"),
            "committed_receipt_byte_exact": byte_exact,
        }
        if committed_legacy_receipt != legacy_output:
            contradictions.append("Committed legacy receipt object differs from recomputation")
    except (OSError, ValueError, KeyError, EvidenceUnavailable) as exc:
        control_errors.append(f"Legacy evidence could not be resolved: {exc}")
        inconclusive_count += 1

    subject = plan["subject"]
    changed_paths: list[str] = []
    merge_base: str | None = None
    if legacy_output is not None and isinstance(legacy_output.get("subject"), dict):
        legacy_subject = legacy_output["subject"]
        changed_paths = list(legacy_subject.get("changed_paths", []))
        merge_base = legacy_subject.get("merge_base")
        for field in ("repository", "base_commit", "candidate_commit"):
            if legacy_subject.get(field) != subject.get(field):
                contradictions.append(f"Subject mismatch: {field}")
        if merge_base != subject.get("expected_merge_base"):
            contradictions.append("Subject mismatch: expected_merge_base")
        receipt["subject"] = {
            "available": True,
            "repository": legacy_subject.get("repository"),
            "base_commit": legacy_subject.get("base_commit"),
            "candidate_commit": legacy_subject.get("candidate_commit"),
            "merge_base": merge_base,
            "changed_path_count": len(changed_paths),
        }

    non_regular: list[dict[str, Any]] = []
    regular_count = 0
    for path in changed_paths:
        try:
            entry = git_tree_entry(root, subject["candidate_commit"], path)
        except EvidenceUnavailable as exc:
            inconclusive_count += 1
            non_regular.append({"path": path, "error": str(exc)})
            continue
        if entry["object_type"] == "blob" and entry["mode"] in REGULAR_MODES:
            regular_count += 1
        else:
            non_regular.append(entry)
    if non_regular:
        contradictions.extend("non-regular changed path" for _ in non_regular)
    receipt["git_modes"] = {
        "checked_path_count": len(changed_paths),
        "regular_blob_count": regular_count,
        "non_regular_paths": non_regular,
    }

    contradicted_count = len(contradictions)
    if legacy_output is not None:
        legacy_result = legacy_output.get("result", {})
        contradicted_count += int(legacy_result.get("contradicted_assertion_count", 0))
        inconclusive_count += int(legacy_result.get("inconclusive_assertion_count", 0))
        if int(legacy_result.get("control_error_count", 0)):
            control_errors.append("Legacy verifier reported control errors")

    verdict, ok = classify(
        control_errors=control_errors,
        contradicted_count=contradicted_count,
        inconclusive_count=inconclusive_count,
    )
    receipt["control_errors"] = control_errors
    receipt["result"] = {
        "ok": ok,
        "verdict": verdict,
        "precedence_applied": PRECEDENCE_RENDERED,
        "contradicted_count": contradicted_count,
        "inconclusive_count": inconclusive_count,
        "control_error_count": len(control_errors),
        "merge_effect": "NONE",
        "repository_standing_effect": "NONE",
        "experiment_execution_effect": "NONE",
    }
    schema_validate(receipt, root / RECEIPT_SCHEMA_PATH)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    plan_path = args.plan if args.plan.is_absolute() else root / args.plan
    output = verify(root, plan_path.resolve())
    rendered = pretty_bytes(output)
    if args.write_receipt:
        destination = args.write_receipt if args.write_receipt.is_absolute() else root / args.write_receipt
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(rendered)
    sys.stdout.buffer.write(rendered)
    verdict = output["result"]["verdict"]
    if verdict == "VERIFIED_WITHIN_DECLARED_SCOPE":
        return 0
    if verdict == "INVALIDATED_BY_RECOMPUTATION":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
