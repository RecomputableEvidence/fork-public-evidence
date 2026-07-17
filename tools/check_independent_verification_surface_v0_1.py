#!/usr/bin/env python3
"""Recompute bounded contribution claims from a trusted verification surface."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import jsonschema

import check_claim_admission_gate_v0_1 as claim_gate


CHECKER_ID = "FORK_INDEPENDENT_VERIFICATION_SURFACE_v0_1"
POLICY_PATH = Path(
    "policies/independent-verification/INDEPENDENT_VERIFICATION_POLICY_v0_1.json"
)
POLICY_SCHEMA_PATH = Path("schemas/independent_verification_policy_v0_1.schema.json")
PLAN_SCHEMA_PATH = Path("schemas/independent_verification_plan_v0_1.schema.json")
RECEIPT_SCHEMA_PATH = Path("schemas/independent_verification_receipt_v0_1.schema.json")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MAX_PLAN_BYTES = 1024 * 1024
MAX_ASSERTED_BLOB_BYTES = 16 * 1024 * 1024


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


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def strict_json_file(path: Path, *, maximum_bytes: int | None = None) -> Any:
    raw = path.read_bytes()
    if maximum_bytes is not None and len(raw) > maximum_bytes:
        raise ValueError(f"{path} exceeds {maximum_bytes} bytes")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path} is not UTF-8: {exc}") from exc
    except DuplicateKeyError as exc:
        raise ValueError(f"{path} contains duplicate key {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{path} is invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc


def validate_with_schema(instance: Any, schema_path: Path) -> None:
    schema = strict_json_file(schema_path)
    jsonschema.Draft7Validator.check_schema(schema)
    jsonschema.Draft7Validator(schema).validate(instance)


def valid_repo_path(value: str) -> bool:
    if not value or "\x00" in value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and all(ord(char) >= 32 for char in value)


def require_repo_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not valid_repo_path(value):
        raise ValueError(f"Unsafe repository path in {label}: {value!r}")
    return value


def ensure_commit(root: Path, commit: str) -> None:
    if not SHA_RE.fullmatch(commit):
        raise ValueError(f"Commit is not a lowercase full SHA: {commit!r}")
    run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"])


def fetch_subject(root: Path, repository: str, commits: list[str]) -> None:
    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError("Repository must be an owner/name GitHub slug.")
    for commit in commits:
        if not SHA_RE.fullmatch(commit):
            raise ValueError("Fetch targets must be lowercase full commit SHAs.")
    run_git(
        root,
        [
            "fetch",
            "--no-tags",
            "--no-recurse-submodules",
            "--depth=1",
            f"https://github.com/{repository}.git",
            *commits,
        ],
    )


def object_exists(root: Path, commit: str, path: str) -> bool:
    completed = run_git(root, ["cat-file", "-e", f"{commit}:{path}"], check=False)
    return completed.returncode == 0


def object_sha(root: Path, commit: str, path: str) -> str:
    return run_git(root, ["rev-parse", f"{commit}:{path}"], text=True).stdout.strip()


def object_bytes(root: Path, commit: str, path: str) -> bytes:
    size_text = run_git(root, ["cat-file", "-s", f"{commit}:{path}"], text=True).stdout.strip()
    try:
        size = int(size_text)
    except ValueError as exc:
        raise EvidenceUnavailable(f"Invalid Git object size for {path}: {size_text!r}") from exc
    if size > MAX_ASSERTED_BLOB_BYTES:
        raise EvidenceUnavailable(
            f"{path} is {size} bytes; asserted blobs are limited to {MAX_ASSERTED_BLOB_BYTES} bytes"
        )
    return run_git(root, ["show", f"{commit}:{path}"]).stdout


def object_metadata(root: Path, commit: str, path: str) -> dict[str, Any]:
    content = object_bytes(root, commit, path)
    return {
        "path": path,
        "git_blob": object_sha(root, commit, path),
        "sha256": sha256_bytes(content),
        "size_bytes": len(content),
    }


def tree_sha(root: Path, commit: str) -> str:
    return run_git(root, ["rev-parse", f"{commit}^{{tree}}"], text=True).stdout.strip()


def changed_paths(root: Path, base: str, candidate: str) -> tuple[str, list[str]]:
    merge_base = run_git(root, ["merge-base", base, candidate], text=True).stdout.strip()
    raw = run_git(root, ["diff", "--name-only", "-z", merge_base, candidate]).stdout
    result: list[str] = []
    for value in raw.split(b"\0"):
        if not value:
            continue
        try:
            path = value.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise EvidenceUnavailable(f"Changed path is not UTF-8: {exc}") from exc
        require_repo_path(path, "changed path")
        result.append(path)
    return merge_base, sorted(result)


def json_pointer(document: Any, pointer: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise ValueError(f"JSON Pointer must be empty or begin with '/': {pointer!r}")
    current = document
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(token)
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit() or int(token) >= len(current):
                raise KeyError(token)
            current = current[int(token)]
        else:
            raise KeyError(token)
    return current


def run_claim_admission(root: Path, base: str, candidate: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(root / "tools/check_claim_admission_gate_v0_1.py"),
            "--repo-root",
            str(root),
            "--base-sha",
            base,
            "--candidate-sha",
            candidate,
        ],
        cwd=str(root),
        env=safe_git_env(),
        text=True,
        capture_output=True,
        check=False,
    )
    if not completed.stdout.strip():
        raise EvidenceUnavailable(
            completed.stderr.strip() or "Claim-admission checker emitted no JSON output."
        )
    try:
        result = json.loads(completed.stdout, object_pairs_hook=reject_duplicate_keys)
    except (json.JSONDecodeError, DuplicateKeyError) as exc:
        raise EvidenceUnavailable(f"Claim-admission output is not strict JSON: {exc}") from exc
    result["process_exit_code"] = completed.returncode
    return result


def normalized_findings(payload: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for item in payload.get("errors", []):
        if isinstance(item, dict) and isinstance(item.get("code"), str) and isinstance(item.get("path"), str):
            findings.append({"code": item["code"], "path": item["path"]})
    return sorted(findings, key=lambda item: (item["code"], item["path"]))


def assertion_result(
    root: Path,
    base: str,
    candidate: str,
    actual_changed_paths: list[str],
    assertion: dict[str, Any],
) -> dict[str, Any]:
    assertion_id = assertion["assertion_id"]
    assertion_type = assertion["type"]
    output: dict[str, Any] = {
        "assertion_id": assertion_id,
        "type": assertion_type,
        "status": "INCONCLUSIVE",
        "evidence": {},
    }
    try:
        if assertion_type == "CHANGED_PATH_SET_EQUALS":
            expected = sorted(assertion["expected_paths"])
            output["evidence"] = {
                "expected_paths": expected,
                "observed_paths": actual_changed_paths,
            }
            output["status"] = "SUPPORTED" if expected == actual_changed_paths else "CONTRADICTED"
        elif assertion_type == "PATH_PRESENT":
            path = require_repo_path(assertion["path"], assertion_id)
            present = object_exists(root, candidate, path)
            output["evidence"] = {"path": path, "present": present}
            if present:
                output["evidence"].update(object_metadata(root, candidate, path))
            output["status"] = "SUPPORTED" if present else "CONTRADICTED"
        elif assertion_type == "PATH_ABSENT":
            path = require_repo_path(assertion["path"], assertion_id)
            present = object_exists(root, candidate, path)
            output["evidence"] = {"path": path, "present": present}
            output["status"] = "SUPPORTED" if not present else "CONTRADICTED"
        elif assertion_type == "SHA256_EQUALS":
            path = require_repo_path(assertion["path"], assertion_id)
            expected = assertion["expected_sha256"]
            if not SHA256_RE.fullmatch(expected):
                raise ValueError(f"Invalid expected SHA-256 in {assertion_id}")
            metadata = object_metadata(root, candidate, path)
            output["evidence"] = {**metadata, "expected_sha256": expected}
            output["status"] = "SUPPORTED" if metadata["sha256"] == expected else "CONTRADICTED"
        elif assertion_type == "UNCHANGED_FROM_BASE":
            path = require_repo_path(assertion["path"], assertion_id)
            base_meta = object_metadata(root, base, path)
            candidate_meta = object_metadata(root, candidate, path)
            output["evidence"] = {"base": base_meta, "candidate": candidate_meta}
            output["status"] = (
                "SUPPORTED" if base_meta["git_blob"] == candidate_meta["git_blob"] else "CONTRADICTED"
            )
        elif assertion_type == "ARCHIVE_EQUALS_BASE_PATH":
            archive_path = require_repo_path(assertion["path"], assertion_id)
            base_path = require_repo_path(assertion["base_path"], assertion_id)
            archive_meta = object_metadata(root, candidate, archive_path)
            base_meta = object_metadata(root, base, base_path)
            output["evidence"] = {"candidate_archive": archive_meta, "base_source": base_meta}
            output["status"] = (
                "SUPPORTED" if archive_meta["sha256"] == base_meta["sha256"] else "CONTRADICTED"
            )
        elif assertion_type == "JSON_POINTER_EQUALS":
            path = require_repo_path(assertion["path"], assertion_id)
            content = object_bytes(root, candidate, path)
            try:
                document = json.loads(content.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
            except (UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
                output["evidence"] = {"path": path, "pointer": assertion["pointer"], "error": str(exc)}
                output["status"] = "CONTRADICTED"
            else:
                try:
                    observed = json_pointer(document, assertion["pointer"])
                except (KeyError, ValueError) as exc:
                    output["evidence"] = {
                        "path": path,
                        "pointer": assertion["pointer"],
                        "error": str(exc),
                    }
                    output["status"] = "CONTRADICTED"
                else:
                    expected = assertion["expected"]
                    output["evidence"] = {
                        "path": path,
                        "pointer": assertion["pointer"],
                        "expected": expected,
                        "observed": observed,
                    }
                    output["status"] = "SUPPORTED" if observed == expected else "CONTRADICTED"
        elif assertion_type == "WORKFLOW_HARDENED":
            path = require_repo_path(assertion["path"], assertion_id)
            trusted_errors: list[dict[str, str]] = []
            registry = claim_gate.load_trusted_json(root, claim_gate.ACTION_REGISTRY_PATH, trusted_errors)
            pins = claim_gate.action_pins(registry, trusted_errors)
            content = object_bytes(root, candidate, path)
            workflow = claim_gate.parse_yaml(content, path, trusted_errors)
            if workflow is not None:
                claim_gate.check_workflow(workflow, path, pins, trusted_errors)
            output["evidence"] = {
                "path": path,
                "sha256": sha256_bytes(content),
                "trusted_static_findings": trusted_errors,
            }
            output["status"] = "SUPPORTED" if not trusted_errors else "CONTRADICTED"
        else:  # pragma: no cover - schema prevents this branch
            raise ValueError(f"Unsupported assertion type: {assertion_type}")
    except (EvidenceUnavailable, FileNotFoundError, ValueError, KeyError) as exc:
        output["evidence"] = {"error": str(exc)}
        output["status"] = "INCONCLUSIVE"
    return output


def policy_checks(root: Path) -> tuple[dict[str, Any], list[dict[str, str]]]:
    checks: list[dict[str, str]] = []
    try:
        policy = strict_json_file(root / POLICY_PATH)
        validate_with_schema(policy, root / POLICY_SCHEMA_PATH)
        checks.append({"check": "policy_schema", "status": "PASS"})
    except (OSError, ValueError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        return {}, [{"check": "policy_schema", "status": "FAIL", "detail": str(exc)}]

    expected = {
        "policy_id": "FORK_INDEPENDENT_VERIFICATION_POLICY_v0_1",
        "candidate_checkout": "PROHIBITED_IN_TRUSTED_LANE",
        "candidate_code_execution": "PROHIBITED_IN_TRUSTED_LANE",
        "self_certification": "PROHIBITED",
        "merge_effect": "NONE",
        "experiment_execution_effect": "NONE",
    }
    observed = {
        "policy_id": policy.get("policy_id"),
        "candidate_checkout": policy.get("trusted_lane", {}).get("candidate_checkout"),
        "candidate_code_execution": policy.get("trusted_lane", {}).get("candidate_code_execution"),
        "self_certification": policy.get("independence_boundary", {}).get("self_certification"),
        "merge_effect": policy.get("authority_effects", {}).get("merge"),
        "experiment_execution_effect": policy.get("authority_effects", {}).get("experiment_execution"),
    }
    checks.append(
        {
            "check": "fail_closed_authority_boundary",
            "status": "PASS" if observed == expected else "FAIL",
            "detail": "exact" if observed == expected else json.dumps(observed, sort_keys=True),
        }
    )
    return policy, checks


def self_check(root: Path) -> dict[str, Any]:
    _policy, checks = policy_checks(root)
    for schema_path in (PLAN_SCHEMA_PATH, RECEIPT_SCHEMA_PATH):
        try:
            schema = strict_json_file(root / schema_path)
            jsonschema.Draft7Validator.check_schema(schema)
            checks.append({"check": schema_path.name, "status": "PASS"})
        except (OSError, ValueError, jsonschema.SchemaError) as exc:
            checks.append({"check": schema_path.name, "status": "FAIL", "detail": str(exc)})
    failed = [item for item in checks if item["status"] != "PASS"]
    return {
        "checker_id": CHECKER_ID,
        "mode": "SELF_CHECK",
        "result": {
            "ok": not failed,
            "verdict": "SURFACE_SELF_CHECK_PASS" if not failed else "SURFACE_SELF_CHECK_FAILED",
            "merge_effect": "NONE",
            "repository_standing_effect": "NONE",
            "experiment_execution_effect": "NONE",
        },
        "checks": checks,
        "non_claims": {
            "does_not_supply_independent_human_identity": True,
            "does_not_approve_merge": True,
            "does_not_certify_security": True,
            "does_not_authorize_experiment_execution": True,
            "does_not_establish_semantic_truth_beyond_declared_assertions": True,
        },
    }


def verify(root: Path, plan_path: Path, fetch: bool) -> dict[str, Any]:
    control_errors: list[str] = []
    plan: dict[str, Any] | None = None
    try:
        plan_value = strict_json_file(plan_path, maximum_bytes=MAX_PLAN_BYTES)
        validate_with_schema(plan_value, root / PLAN_SCHEMA_PATH)
        if not isinstance(plan_value, dict):
            raise ValueError("Plan root must be a JSON object.")
        plan = plan_value
    except (OSError, ValueError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        control_errors.append(str(exc))

    policy, policy_results = policy_checks(root)
    if any(item["status"] != "PASS" for item in policy_results):
        control_errors.extend(item.get("detail", item["check"]) for item in policy_results if item["status"] != "PASS")

    if plan is None:
        return inconclusive_receipt(plan_path, control_errors, policy_results)

    subject = plan["subject"]
    base = subject["base_commit"]
    candidate = subject["candidate_commit"]
    repository = subject["repository"]
    try:
        if fetch:
            fetch_subject(root, repository, [base, candidate])
        ensure_commit(root, base)
        ensure_commit(root, candidate)
        observed_base_tree = tree_sha(root, base)
        observed_candidate_tree = tree_sha(root, candidate)
        merge_base, actual_changed_paths = changed_paths(root, base, candidate)
    except (EvidenceUnavailable, ValueError) as exc:
        control_errors.append(str(exc))
        return inconclusive_receipt(plan_path, control_errors, policy_results, plan=plan)

    subject_contradictions: list[dict[str, Any]] = []
    for field, observed in (
        ("base_tree", observed_base_tree),
        ("candidate_tree", observed_candidate_tree),
        ("expected_merge_base", merge_base),
    ):
        expected = subject[field]
        if observed != expected:
            subject_contradictions.append({"field": field, "expected": expected, "observed": observed})

    try:
        claim_result = run_claim_admission(root, base, candidate)
        observed_gate = {
            "result_kind": claim_result.get("result", {}).get("result_kind"),
            "findings": normalized_findings(claim_result),
        }
        expected_gate = {
            "result_kind": plan["expected_claim_admission"]["result_kind"],
            "findings": sorted(
                plan["expected_claim_admission"]["findings"],
                key=lambda item: (item["code"], item["path"]),
            ),
        }
        gate_matches = observed_gate == expected_gate
    except EvidenceUnavailable as exc:
        claim_result = {"error": str(exc)}
        observed_gate = {"result_kind": None, "findings": []}
        expected_gate = plan["expected_claim_admission"]
        gate_matches = False
        control_errors.append(str(exc))

    assertion_results = [
        assertion_result(root, base, candidate, actual_changed_paths, assertion)
        for assertion in plan["assertions"]
    ]
    contradicted = [item for item in assertion_results if item["status"] == "CONTRADICTED"]
    inconclusive = [item for item in assertion_results if item["status"] == "INCONCLUSIVE"]
    if control_errors or inconclusive:
        verdict = "INCONCLUSIVE_EVIDENCE_GAP"
        ok = False
    elif subject_contradictions or not gate_matches or contradicted:
        verdict = "INVALIDATED_BY_RECOMPUTATION"
        ok = False
    else:
        verdict = "VERIFIED_WITHIN_DECLARED_SCOPE"
        ok = True

    plan_raw = plan_path.read_bytes()
    receipt: dict[str, Any] = {
        "checker_id": CHECKER_ID,
        "mode": "CONTRIBUTION_VERIFICATION",
        "plan": {
            "plan_id": plan["plan_id"],
            "path": plan_path.relative_to(root).as_posix() if plan_path.is_relative_to(root) else str(plan_path),
            "sha256": sha256_bytes(plan_raw),
        },
        "subject": {
            "repository": repository,
            "base_commit": base,
            "base_tree": observed_base_tree,
            "candidate_commit": candidate,
            "candidate_tree": observed_candidate_tree,
            "merge_base": merge_base,
            "changed_paths": actual_changed_paths,
        },
        "claim_admission": {
            "expected": expected_gate,
            "observed": observed_gate,
            "matches_expected": gate_matches,
            "candidate_checkout": "NONE",
            "candidate_code_execution": "NONE",
            "raw_result_sha256": sha256_bytes(canonical_bytes(claim_result)),
        },
        "assertions": assertion_results,
        "external_evidence": plan.get("external_evidence", []),
        "independence_boundary": {
            "plan_origin": plan["independence_boundary"]["plan_origin"],
            "candidate_tree_controls_plan": plan["independence_boundary"]["candidate_tree_controls_plan"],
            "human_verifier": plan["independence_boundary"]["human_verifier"],
            "human_independent_review_recorded": False,
            "self_certification": "PROHIBITED",
        },
        "result": {
            "ok": ok,
            "verdict": verdict,
            "subject_binding_contradictions": subject_contradictions,
            "contradicted_assertion_count": len(contradicted),
            "inconclusive_assertion_count": len(inconclusive),
            "control_error_count": len(control_errors),
            "merge_effect": "NONE",
            "repository_standing_effect": "NONE",
            "experiment_execution_effect": "NONE",
        },
        "control_errors": control_errors,
        "non_claims": policy.get("non_claims", []),
    }
    try:
        validate_with_schema(receipt, root / RECEIPT_SCHEMA_PATH)
    except (OSError, ValueError, jsonschema.ValidationError, jsonschema.SchemaError) as exc:
        receipt["control_errors"].append(f"Receipt schema validation failed: {exc}")
        receipt["result"]["ok"] = False
        receipt["result"]["verdict"] = "INCONCLUSIVE_EVIDENCE_GAP"
        receipt["result"]["control_error_count"] = len(receipt["control_errors"])
    return receipt


def inconclusive_receipt(
    plan_path: Path,
    errors: list[str],
    policy_results: list[dict[str, str]],
    *,
    plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "checker_id": CHECKER_ID,
        "mode": "CONTRIBUTION_VERIFICATION",
        "plan": {
            "plan_id": plan.get("plan_id") if isinstance(plan, dict) else None,
            "path": str(plan_path),
            "sha256": sha256_bytes(plan_path.read_bytes()) if plan_path.is_file() else None,
        },
        "subject": plan.get("subject") if isinstance(plan, dict) else None,
        "claim_admission": None,
        "assertions": [],
        "external_evidence": plan.get("external_evidence", []) if isinstance(plan, dict) else [],
        "independence_boundary": None,
        "result": {
            "ok": False,
            "verdict": "INCONCLUSIVE_EVIDENCE_GAP",
            "subject_binding_contradictions": [],
            "contradicted_assertion_count": 0,
            "inconclusive_assertion_count": 0,
            "control_error_count": len(errors),
            "merge_effect": "NONE",
            "repository_standing_effect": "NONE",
            "experiment_execution_effect": "NONE",
        },
        "control_errors": errors,
        "policy_checks": policy_results,
        "non_claims": [
            "No merge approval",
            "No security certification",
            "No experiment execution authorization",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--fetch-subject", action="store_true")
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    if args.self_check == bool(args.plan):
        parser.error("select exactly one of --self-check or --plan")
    if args.self_check and args.fetch_subject:
        parser.error("--fetch-subject applies only to --plan")

    if args.self_check:
        output = self_check(root)
    else:
        plan_path = args.plan if args.plan.is_absolute() else root / args.plan
        output = verify(root, plan_path.resolve(), args.fetch_subject)

    serialized = json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write_receipt:
        receipt_path = args.write_receipt if args.write_receipt.is_absolute() else root / args.write_receipt
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(serialized, encoding="utf-8", newline="\n")
    sys.stdout.write(serialized)

    verdict = output.get("result", {}).get("verdict")
    if verdict in {"SURFACE_SELF_CHECK_PASS", "VERIFIED_WITHIN_DECLARED_SCOPE"}:
        return 0
    if verdict == "INVALIDATED_BY_RECOMPUTATION":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
