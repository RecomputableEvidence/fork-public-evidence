#!/usr/bin/env python3
"""Inspect a candidate Git tree as data from a consumer-owned trusted base."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - dependency failure is reported by main
    yaml = None
    YAML_IMPORT_ERROR = exc
else:
    YAML_IMPORT_ERROR = None


CHECKER_ID = "FORK_CONSUMER_OWNED_CLAIM_ADMISSION_GATE_v0_1"
POLICY_PATH = Path("policies/claim-admission/CONSUMER_OWNED_CLAIM_ADMISSION_POLICY_v0_1.json")
ACTION_REGISTRY_PATH = Path("policies/repository-hardening/ACTION_PIN_REGISTRY_v0_1.json")
PRESERVATION_MANIFEST_PATH = Path(
    "docs/preservation/failure-mode-archive-v0.1/incidents/"
    "FORK-INC-2026-07-13-001/PRESERVATION_MANIFEST_v0_1.json"
)
SUCCESSOR_PROVENANCE_PATH = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/amendments/"
    "CSH-AMEND-003/WORKFLOW_SUCCESSOR_PROVENANCE_v0_1_2.json"
)
TRUSTED_WORKFLOW = ".github/workflows/consumer-owned-claim-admission.yml"
POLICY_ID = "FORK_CONSUMER_OWNED_CLAIM_ADMISSION_POLICY_v0_1"
FAILURE_CLASS_ID = "CCF-001_AI_CHANGE_READINESS_PROMOTION"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
ACTION_RE = re.compile(r"^([^@\s]+)@([0-9a-f]{40})$")
UNTRUSTED_RUN_EXPRESSION_RE = re.compile(r"\$\{\{\s*github\.event\.pull_request\.", re.IGNORECASE)
LOCKED_INSTALL_RE = re.compile(r"\bpip\s+install\b", re.IGNORECASE)
NETWORK_FETCH_RE = re.compile(r"(^|[\s|;&])(curl|wget|Invoke-WebRequest)(\s|$)", re.IGNORECASE)
ORIGINAL_WORKFLOW_PATHS = {
    ".github/workflows/cross-system-claim-handoff-v0-1.yml": "b2b589665bed12a4ca3028b2e48fcebd97c7e6f6b5128c59fb196e5ed5fbc30d",
    ".github/workflows/fork-proof-surface-integration.yml": "7a1fbc7b3e97bf0946e018b5be6613f5d8329238d5347cf444abe28e5aaae166",
}
SUCCESSOR_WORKFLOW_PATHS = {
    ".github/workflows/cross-system-claim-handoff-v0-1.yml": "46ffa57dde40955bb7ed5b517b2de397b3d0056a0e8e9bfd4593f4dd2ef38c23",
    ".github/workflows/fork-proof-surface-integration.yml": "5a09b805c0b59f3d211c01eb55ac61fbde3c7ae2ab3eb19d689bc863cd3fb29e",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


if yaml is not None:
    class StrictBaseLoader(yaml.BaseLoader):
        pass


    def construct_unique_mapping(loader: Any, node: Any, deep: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise DuplicateKeyError(f"non-string YAML key {key!r}")
            if key in result:
                raise DuplicateKeyError(key)
            result[key] = loader.construct_object(value_node, deep=deep)
        return result


    StrictBaseLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_unique_mapping,
    )


def finding(code: str, message: str, path: str) -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def expect(
    condition: bool,
    code: str,
    message: str,
    path: str,
    errors: list[dict[str, str]],
) -> None:
    if not condition:
        errors.append(finding(code, message, path))


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
        raise RuntimeError(stderr.strip() or f"git {' '.join(args)} failed")
    return completed


def load_trusted_json(
    root: Path,
    relative: Path,
    errors: list[dict[str, str]],
) -> Any | None:
    path = root / relative
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(finding("TRUSTED_CONTROL_FILE_MISSING", "Trusted control file is absent.", relative.as_posix()))
        return None
    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_json_keys)
    except DuplicateKeyError as exc:
        errors.append(finding("DUPLICATE_JSON_KEY", f"Duplicate JSON key: {exc}", relative.as_posix()))
    except json.JSONDecodeError as exc:
        errors.append(finding("JSON_PARSE_ERROR", f"{exc.msg} at line {exc.lineno}, column {exc.colno}", relative.as_posix()))
    return None


def load_candidate_json(
    view: "CandidateView",
    relative: Path,
    errors: list[dict[str, str]],
) -> Any | None:
    label = relative.as_posix()
    try:
        text = view.read_bytes(label).decode("utf-8", errors="strict")
    except (FileNotFoundError, RuntimeError):
        errors.append(finding("CANDIDATE_CONTROL_FILE_MISSING", "Candidate control file is absent.", label))
        return None
    except UnicodeDecodeError as exc:
        errors.append(finding("JSON_NOT_UTF8", str(exc), label))
        return None
    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_json_keys)
    except DuplicateKeyError as exc:
        errors.append(finding("DUPLICATE_JSON_KEY", f"Duplicate JSON key: {exc}", label))
    except json.JSONDecodeError as exc:
        errors.append(finding("JSON_PARSE_ERROR", f"{exc.msg} at line {exc.lineno}, column {exc.colno}", label))
    return None


def valid_repo_path(path: str) -> bool:
    if not path or "\x00" in path or "\\" in path:
        return False
    pure = PurePosixPath(path)
    return not pure.is_absolute() and ".." not in pure.parts and all(ord(char) >= 32 for char in path)


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    object_type: str
    object_sha: str
    path: str


class CandidateView:
    def paths(self) -> list[str]:
        raise NotImplementedError

    def entries(self) -> list[TreeEntry]:
        raise NotImplementedError

    def read_bytes(self, path: str) -> bytes:
        raise NotImplementedError


class GitTreeView(CandidateView):
    def __init__(self, root: Path, commit_sha: str):
        self.root = root
        self.commit_sha = commit_sha
        self._entries: list[TreeEntry] | None = None

    def entries(self) -> list[TreeEntry]:
        if self._entries is None:
            raw = run_git(self.root, ["ls-tree", "-r", "-z", self.commit_sha]).stdout
            entries: list[TreeEntry] = []
            for record in raw.split(b"\0"):
                if not record:
                    continue
                metadata, path_bytes = record.split(b"\t", 1)
                mode, object_type, object_sha = metadata.decode("ascii").split(" ")
                path = path_bytes.decode("utf-8", errors="strict")
                entries.append(TreeEntry(mode, object_type, object_sha, path))
            self._entries = entries
        return self._entries

    def paths(self) -> list[str]:
        return [entry.path for entry in self.entries()]

    def read_bytes(self, path: str) -> bytes:
        if not valid_repo_path(path):
            raise ValueError(f"Unsafe repository path: {path}")
        return run_git(self.root, ["show", f"{self.commit_sha}:{path}"]).stdout


class WorktreeView(CandidateView):
    def __init__(self, root: Path):
        self.root = root
        self._paths: list[str] | None = None

    def paths(self) -> list[str]:
        if self._paths is None:
            raw = run_git(
                self.root,
                ["ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            ).stdout
            self._paths = sorted(
                value.decode("utf-8", errors="strict")
                for value in raw.split(b"\0")
                if value
            )
        return self._paths

    def entries(self) -> list[TreeEntry]:
        entries: list[TreeEntry] = []
        for relative in self.paths():
            path = self.root / relative
            mode = "120000" if path.is_symlink() else "100644"
            entries.append(TreeEntry(mode, "blob", "WORKTREE", relative))
        return entries

    def read_bytes(self, path: str) -> bytes:
        if not valid_repo_path(path):
            raise ValueError(f"Unsafe repository path: {path}")
        return (self.root / path).read_bytes()


def fetch_candidate(root: Path, repository: str, candidate_sha: str) -> None:
    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError("Candidate repository must be an owner/name GitHub slug.")
    if not SHA_RE.fullmatch(candidate_sha):
        raise ValueError("Candidate SHA must be a lowercase full-length commit SHA.")
    url = f"https://github.com/{repository}.git"
    run_git(
        root,
        [
            "fetch",
            "--no-tags",
            "--no-recurse-submodules",
            "--depth=1",
            url,
            candidate_sha,
        ],
    )


def changed_files(root: Path, base_sha: str, candidate_sha: str) -> tuple[list[str], list[dict[str, str]]]:
    errors: list[dict[str, str]] = []
    merge_base = run_git(root, ["merge-base", base_sha, candidate_sha], text=True).stdout.strip()
    raw = run_git(root, ["diff", "--name-only", "-z", merge_base, candidate_sha]).stdout
    paths: list[str] = []
    for value in raw.split(b"\0"):
        if not value:
            continue
        try:
            path = value.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            errors.append(finding("NON_UTF8_PATH", "Changed path is not UTF-8.", "$candidate_tree"))
            continue
        paths.append(path)
    whitespace = run_git(root, ["diff", "--check", merge_base, candidate_sha], check=False, text=True)
    if whitespace.returncode != 0:
        for line in whitespace.stdout.splitlines() or whitespace.stderr.splitlines():
            errors.append(finding("GIT_DIFF_CHECK_FAILED", line, "$candidate_diff"))
    return sorted(paths), errors


def policy_checks(policy: Any, errors: list[dict[str, str]]) -> None:
    path = POLICY_PATH.as_posix()
    if not isinstance(policy, dict):
        return
    expect(policy.get("policy_id") == POLICY_ID, "POLICY_ID_MISMATCH", "Trusted policy ID changed.", path, errors)
    expect(policy.get("failure_class_addressed") == FAILURE_CLASS_ID, "FAILURE_CLASS_MISMATCH", "The gate must remain bound to CCF-001.", path, errors)
    expect(policy.get("repository_settings_effect") == "NONE", "REPOSITORY_SETTINGS_EFFECT_PROHIBITED", "The policy may not mutate repository settings.", path, errors)
    expect(policy.get("historical_rewrite_authority") == "NONE", "HISTORICAL_REWRITE_AUTHORITY_PROHIBITED", "The policy grants no historical rewrite authority.", path, errors)
    expect(policy.get("activation_state") == "IMPLEMENTED_DORMANT_UNTIL_PRESENT_ON_DEFAULT_BRANCH", "ACTIVATION_STATE_OVERCLAIM", "The gate must remain dormant until present on the repository default branch.", path, errors)
    trusted = policy.get("trusted_base_contract", {})
    for key in ("candidate_checkout", "candidate_code_execution", "secret_use"):
        expect(trusted.get(key) == "PROHIBITED", "TRUSTED_BASE_CONTRACT_WEAKENED", f"{key} must remain prohibited.", path, errors)
    semantics = policy.get("admission_semantics", {})
    expect(semantics.get("structural_pass_effect") == "REVIEW_ELIGIBLE_NOT_ADMITTED", "ADMISSION_SEMANTICS_COLLAPSED", "A pass may establish review eligibility only.", path, errors)
    expect(semantics.get("repository_standing_effect") == "NONE", "REPOSITORY_STANDING_EXPANDED", "The automated gate grants no repository standing.", path, errors)
    effect = policy.get("experiment_effect", {})
    expect(isinstance(effect, dict) and bool(effect), "EXPERIMENT_BOUNDARY_MISSING", "Experiment effects must be explicit.", path, errors)
    if isinstance(effect, dict):
        for key, value in sorted(effect.items()):
            expect(value is False, "EXPERIMENT_BOUNDARY_EFFECT", f"Admission control must not change experiment state: {key}.", f"{path}:$.experiment_effect.{key}", errors)


def action_pins(registry: Any, errors: list[dict[str, str]]) -> dict[str, str]:
    pins: dict[str, str] = {}
    if not isinstance(registry, dict):
        return pins
    for index, item in enumerate(registry.get("pins", [])):
        if not isinstance(item, dict):
            continue
        action = item.get("action")
        sha = item.get("commit_sha")
        source = item.get("source_repository")
        if not isinstance(action, str) or not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            errors.append(finding("ACTION_PIN_INVALID", "Action registry entry must contain an action and full commit SHA.", f"{ACTION_REGISTRY_PATH.as_posix()}:$.pins[{index}]"))
            continue
        expect(source == f"https://github.com/{action}", "ACTION_PIN_SOURCE_MISMATCH", "Action pin source must match the named GitHub repository.", f"{ACTION_REGISTRY_PATH.as_posix()}:$.pins[{index}]", errors)
        pins[action] = sha
    for required in ("actions/checkout", "actions/setup-python"):
        expect(required in pins, "REQUIRED_ACTION_PIN_MISSING", f"Required action pin missing: {required}.", ACTION_REGISTRY_PATH.as_posix(), errors)
    return pins


def provenance_bound_workflow_successors(
    policy: Any,
    provenance: Any,
    view: CandidateView,
    errors: list[dict[str, str]],
) -> dict[str, str]:
    policy_path = POLICY_PATH.as_posix()
    if not isinstance(policy, dict):
        return {}
    records = policy.get("provenance_bound_workflow_successors")
    if not isinstance(records, list):
        errors.append(finding("WORKFLOW_SUCCESSOR_POLICY_MISSING", "The provenance-bound workflow successor policy is absent.", policy_path))
        return {}

    provenance_records: dict[str, dict[str, Any]] = {}
    if isinstance(provenance, dict):
        expect(provenance.get("amendment_id") == "CSH-AMEND-003", "WORKFLOW_SUCCESSOR_AMENDMENT_MISMATCH", "Workflow successor provenance must bind CSH-AMEND-003.", SUCCESSOR_PROVENANCE_PATH.as_posix(), errors)
        expect(provenance.get("execution_authority") == "NONE_UNTIL_ALL_PRE_EXECUTION_PREREQUISITES_TRUE", "WORKFLOW_SUCCESSOR_AUTHORITY_EXPANSION", "Workflow successor provenance may not grant execution authority.", SUCCESSOR_PROVENANCE_PATH.as_posix(), errors)
        provenance_records = {
            item.get("live_path"): item
            for item in provenance.get("successions", [])
            if isinstance(item, dict) and isinstance(item.get("live_path"), str)
        }

    observed: dict[str, str] = {}
    for index, item in enumerate(records):
        item_path = f"{policy_path}:$.provenance_bound_workflow_successors[{index}]"
        if not isinstance(item, dict):
            errors.append(finding("WORKFLOW_SUCCESSOR_POLICY_INVALID", "Workflow successor entry must be a mapping.", item_path))
            continue
        path = item.get("path")
        digest = item.get("successor_sha256")
        original_digest = item.get("original_sha256")
        archive_path = item.get("archive_path")
        expect(isinstance(path, str) and path in SUCCESSOR_WORKFLOW_PATHS, "WORKFLOW_SUCCESSOR_PATH_INVALID", "Only the two v0.1 provenance-bound workflow successors may be recognized.", item_path, errors)
        expect(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, "WORKFLOW_SUCCESSOR_DIGEST_INVALID", "Successor workflow digest must be SHA-256.", item_path, errors)
        expect(isinstance(original_digest, str) and re.fullmatch(r"[0-9a-f]{64}", original_digest) is not None, "WORKFLOW_PREDECESSOR_DIGEST_INVALID", "Archived predecessor digest must be SHA-256.", item_path, errors)
        expect(item.get("provenance_path") == SUCCESSOR_PROVENANCE_PATH.as_posix(), "WORKFLOW_SUCCESSOR_PROVENANCE_PATH_MISMATCH", "Successor must cite the trusted provenance record.", item_path, errors)
        expect(item.get("classification") == "PROVENANCE_BOUND_HARDENED_EXPERIMENT_INSTRUMENTATION_SUCCESSOR", "WORKFLOW_SUCCESSOR_CLASSIFICATION_MISMATCH", "Workflow successor classification changed.", item_path, errors)
        expect(item.get("disposition") == "FULL_HARDENING_REQUIRED_AND_EXECUTION_SEPARATELY_GATED", "WORKFLOW_SUCCESSOR_DISPOSITION_MISMATCH", "Workflow successor disposition changed.", item_path, errors)
        if isinstance(path, str) and isinstance(digest, str):
            expect(path not in observed, "WORKFLOW_SUCCESSOR_DUPLICATE", "Workflow successor path is duplicated.", item_path, errors)
            observed[path] = digest
            expect(SUCCESSOR_WORKFLOW_PATHS.get(path) == digest, "WORKFLOW_SUCCESSOR_POLICY_DIGEST_MISMATCH", "Policy successor digest does not match the checker-bound digest.", item_path, errors)
            expect(ORIGINAL_WORKFLOW_PATHS.get(path) == original_digest, "WORKFLOW_PREDECESSOR_POLICY_DIGEST_MISMATCH", "Policy predecessor digest does not match the checker-bound digest.", item_path, errors)
            provenance_item = provenance_records.get(path, {})
            expect(provenance_item.get("successor", {}).get("sha256") == digest, "WORKFLOW_SUCCESSOR_PROVENANCE_DIGEST_MISMATCH", "Policy successor digest does not match provenance.", item_path, errors)
            expect(provenance_item.get("original", {}).get("sha256") == original_digest, "WORKFLOW_PREDECESSOR_PROVENANCE_DIGEST_MISMATCH", "Policy predecessor digest does not match provenance.", item_path, errors)
            expect(provenance_item.get("original", {}).get("archive_path") == archive_path, "WORKFLOW_PREDECESSOR_ARCHIVE_PATH_MISMATCH", "Policy archive path does not match provenance.", item_path, errors)
            if isinstance(archive_path, str):
                try:
                    archived = view.read_bytes(archive_path)
                except (FileNotFoundError, RuntimeError):
                    errors.append(finding("WORKFLOW_PREDECESSOR_ARCHIVE_MISSING", "Archived predecessor is absent from the candidate tree.", archive_path))
                else:
                    expect(hashlib.sha256(archived).hexdigest() == original_digest, "WORKFLOW_PREDECESSOR_ARCHIVE_DIGEST_MISMATCH", "Archived predecessor bytes do not match provenance.", archive_path, errors)

    expect(observed == SUCCESSOR_WORKFLOW_PATHS, "WORKFLOW_SUCCESSOR_SET_MISMATCH", "The successor set must contain exactly the two checker-bound paths and digests.", policy_path, errors)
    return observed


def parse_yaml(content: bytes, path: str, errors: list[dict[str, str]]) -> Any | None:
    if yaml is None:
        errors.append(finding("PYYAML_DEPENDENCY_UNAVAILABLE", str(YAML_IMPORT_ERROR), path))
        return None
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        errors.append(finding("WORKFLOW_NOT_UTF8", str(exc), path))
        return None
    try:
        return yaml.load(text, Loader=StrictBaseLoader)
    except DuplicateKeyError as exc:
        errors.append(finding("DUPLICATE_YAML_KEY", f"Duplicate YAML key: {exc}", path))
    except (yaml.YAMLError, ValueError) as exc:
        errors.append(finding("YAML_PARSE_ERROR", str(exc), path))
    return None


def scalar_false(value: Any) -> bool:
    return isinstance(value, str) and value.lower() == "false"


def check_run_script(run: str, path: str, errors: list[dict[str, str]]) -> None:
    if UNTRUSTED_RUN_EXPRESSION_RE.search(run):
        errors.append(finding("UNTRUSTED_CONTEXT_IN_RUN_SCRIPT", "Pull-request context must enter scripts only through an intermediate environment variable.", path))
    if NETWORK_FETCH_RE.search(run):
        errors.append(finding("UNPINNED_NETWORK_FETCH_IN_WORKFLOW", "Direct curl, wget, or Invoke-WebRequest fetches are prohibited in workflows.", path))
    if LOCKED_INSTALL_RE.search(run):
        expect("--require-hashes" in run and ".lock.txt" in run, "UNHASHED_PYTHON_INSTALL", "Workflow Python installs must use a hash-locked requirements file.", path, errors)
        expect("--upgrade pip" not in run, "PIP_SELF_UPGRADE_PROHIBITED", "Workflow bootstrap may not replace pip from an unhashed network resolution.", path, errors)


def check_workflow(
    workflow: Any,
    path: str,
    pins: dict[str, str],
    errors: list[dict[str, str]],
) -> None:
    if not isinstance(workflow, dict):
        errors.append(finding("WORKFLOW_ROOT_NOT_MAPPING", "Workflow root must be a mapping.", path))
        return
    expect("on" in workflow, "WORKFLOW_TRIGGER_MISSING", "Workflow must declare triggers.", path, errors)
    expect(workflow.get("permissions") == {"contents": "read"}, "WORKFLOW_PERMISSIONS_NOT_LEAST_PRIVILEGE", "Workflow permissions must be exactly contents: read.", path, errors)
    concurrency = workflow.get("concurrency")
    expect(isinstance(concurrency, dict) and str(concurrency.get("cancel-in-progress", "")).lower() == "true", "WORKFLOW_CONCURRENCY_MISSING", "Workflow must cancel superseded runs.", path, errors)
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        errors.append(finding("WORKFLOW_JOBS_INVALID", "Workflow jobs must be a non-empty mapping.", path))
        return

    for job_name, job in jobs.items():
        job_path = f"{path}:$.jobs.{job_name}"
        if not isinstance(job, dict):
            errors.append(finding("WORKFLOW_JOB_NOT_MAPPING", "Workflow job must be a mapping.", job_path))
            continue
        runs_on = str(job.get("runs-on", ""))
        expect(bool(runs_on), "RUNNER_MISSING", "Workflow job must declare runs-on.", job_path, errors)
        expect("self-hosted" not in runs_on.lower(), "SELF_HOSTED_RUNNER_PROHIBITED", "Admission-controlled workflows must use ephemeral GitHub-hosted runners.", job_path, errors)
        timeout = str(job.get("timeout-minutes", ""))
        expect(timeout.isdigit() and 1 <= int(timeout) <= 60, "JOB_TIMEOUT_INVALID", "Workflow job timeout must be between 1 and 60 minutes.", job_path, errors)
        steps = job.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(finding("WORKFLOW_STEPS_INVALID", "Workflow job steps must be a non-empty sequence.", job_path))
            continue
        for index, step in enumerate(steps):
            step_path = f"{job_path}.steps[{index}]"
            if not isinstance(step, dict):
                errors.append(finding("WORKFLOW_STEP_NOT_MAPPING", "Workflow step must be a mapping.", step_path))
                continue
            uses = step.get("uses")
            if isinstance(uses, str):
                if uses.startswith("./"):
                    pass
                elif uses.startswith("docker://"):
                    expect("@sha256:" in uses, "MUTABLE_DOCKER_ACTION_REFERENCE", "Docker actions must use a digest.", step_path, errors)
                else:
                    match = ACTION_RE.fullmatch(uses)
                    expect(match is not None, "MUTABLE_ACTION_REFERENCE", "External actions must use a full-length commit SHA.", step_path, errors)
                    if match:
                        action, sha = match.groups()
                        if action in pins:
                            expect(pins[action] == sha, "ACTION_PIN_REGISTRY_MISMATCH", f"{action} does not match the admitted pin registry.", step_path, errors)
                        if action == "actions/checkout":
                            with_values = step.get("with")
                            persist = with_values.get("persist-credentials") if isinstance(with_values, dict) else None
                            expect(scalar_false(persist), "CHECKOUT_CREDENTIALS_PERSISTED", "actions/checkout must set persist-credentials: false.", step_path, errors)
            run = step.get("run")
            if isinstance(run, str):
                check_run_script(run, step_path, errors)

    triggers = workflow.get("on")
    has_pr_target = isinstance(triggers, dict) and "pull_request_target" in triggers
    if path == TRUSTED_WORKFLOW:
        expect(has_pr_target, "TRUSTED_WORKFLOW_TRIGGER_MISMATCH", "Trusted admission workflow must use pull_request_target.", path, errors)
        expect(isinstance(triggers, dict) and set(triggers) == {"pull_request_target"}, "TRUSTED_WORKFLOW_TRIGGER_EXPANDED", "Trusted admission workflow may have no additional trigger.", path, errors)
        serialized = json.dumps(workflow, sort_keys=True)
        expect("${{ secrets." not in serialized, "SECRET_REFERENCE_PROHIBITED", "Trusted admission workflow may not reference secrets.", path, errors)
        expect("allow-unsafe-pr-checkout" not in serialized, "UNSAFE_PR_CHECKOUT_PROHIBITED", "Trusted admission workflow may not opt out of checkout protections.", path, errors)
        expect("github.event.pull_request.head.sha" not in json.dumps([step.get("with", {}) for job in jobs.values() if isinstance(job, dict) for step in job.get("steps", []) if isinstance(step, dict)]), "CANDIDATE_CHECKOUT_PROHIBITED", "Candidate refs may not be passed to actions/checkout.", path, errors)
        expect("tools/check_claim_admission_gate_v0_1.py" in serialized, "TRUSTED_CHECKER_INVOCATION_MISSING", "Trusted workflow must invoke the consumer-owned checker.", path, errors)
    else:
        expect(not has_pr_target, "PULL_REQUEST_TARGET_OUTSIDE_TRUSTED_GATE", "Only the consumer-owned gate may use pull_request_target.", path, errors)


def check_candidate_json(
    view: CandidateView,
    candidate_paths: set[str],
    errors: list[dict[str, str]],
) -> None:
    for path in sorted(candidate_paths):
        if not path.endswith(".json"):
            continue
        try:
            text = view.read_bytes(path).decode("utf-8", errors="strict")
            json.loads(text, object_pairs_hook=reject_duplicate_json_keys)
        except (FileNotFoundError, RuntimeError):
            continue
        except UnicodeDecodeError as exc:
            errors.append(finding("JSON_NOT_UTF8", str(exc), path))
        except DuplicateKeyError as exc:
            errors.append(finding("DUPLICATE_JSON_KEY", f"Duplicate JSON key: {exc}", path))
        except json.JSONDecodeError as exc:
            errors.append(finding("JSON_PARSE_ERROR", f"{exc.msg} at line {exc.lineno}, column {exc.colno}", path))


def build_output(
    root: Path,
    view: CandidateView,
    *,
    base_sha: str | None,
    candidate_sha: str | None,
    changed: list[str],
    initial_errors: list[dict[str, str]],
) -> dict[str, Any]:
    errors = list(initial_errors)
    trusted_policy = load_trusted_json(root, POLICY_PATH, errors)
    manifest = load_trusted_json(root, PRESERVATION_MANIFEST_PATH, errors)
    successor_provenance = load_trusted_json(root, SUCCESSOR_PROVENANCE_PATH, errors)
    candidate_policy = load_candidate_json(view, POLICY_PATH, errors)
    candidate_registry = load_candidate_json(view, ACTION_REGISTRY_PATH, errors)
    policy_checks(trusted_policy, errors)
    policy_checks(candidate_policy, errors)
    if isinstance(trusted_policy, dict) and isinstance(candidate_policy, dict):
        expect(
            candidate_policy.get("provenance_bound_workflow_successors") == trusted_policy.get("provenance_bound_workflow_successors"),
            "WORKFLOW_SUCCESSOR_POLICY_MUTATION",
            "A candidate may not add, remove, or alter a trusted workflow-successor binding.",
            POLICY_PATH.as_posix(),
            errors,
        )
    pins = action_pins(candidate_registry, errors)
    successor_workflows = provenance_bound_workflow_successors(trusted_policy, successor_provenance, view, errors)

    entries = view.entries()
    for entry in entries:
        expect(valid_repo_path(entry.path), "UNSAFE_REPOSITORY_PATH", "Candidate path is unsafe.", entry.path, errors)
        expect(entry.object_type == "blob", "GIT_SUBMODULE_PROHIBITED", "Candidate tree may contain blobs only.", entry.path, errors)
        expect(entry.mode == "100644", "CANDIDATE_FILE_MODE_PROHIBITED", "Candidate files must use regular non-executable mode 100644.", entry.path, errors)

    available_paths = set(view.paths())
    required_control_files = {
        ".github/CODEOWNERS",
        ".github/dependabot.yml",
        TRUSTED_WORKFLOW,
        POLICY_PATH.as_posix(),
        ACTION_REGISTRY_PATH.as_posix(),
        PRESERVATION_MANIFEST_PATH.as_posix(),
        SUCCESSOR_PROVENANCE_PATH.as_posix(),
        "docs/preservation/control-stages/CLAIM_ADMISSION_HARDENING_STAGE_v0_1.json",
        "policies/repository-hardening/BRANCH_RULESET_REQUIREMENTS_v0_1.json",
        "requirements-claim-admission.in",
        "requirements-claim-admission.lock.txt",
        "requirements-proof-surface.lock.txt",
        "schemas/consumer_owned_claim_admission_policy_v0_1.schema.json",
        "schemas/claim_admission_hardening_stage_v0_1.schema.json",
        "tools/check_claim_admission_gate_v0_1.py",
    }
    for required in sorted(required_control_files):
        expect(required in available_paths, "REQUIRED_CONTROL_FILE_MISSING", "Required claim-admission control file is absent.", required, errors)

    for lock_path in ("requirements-claim-admission.lock.txt", "requirements-proof-surface.lock.txt"):
        if lock_path not in available_paths:
            continue
        lock_text = view.read_bytes(lock_path).decode("utf-8", errors="replace")
        expect("--hash=sha256:" in lock_text, "DEPENDENCY_LOCK_HASH_MISSING", "Dependency lock must contain SHA-256 hashes.", lock_path, errors)
        expect("--index-url" not in lock_text and "--trusted-host" not in lock_text and "://" not in lock_text, "DEPENDENCY_LOCK_INDEX_BOUNDARY_INVALID", "Dependency locks may not embed an alternate index or direct URL.", lock_path, errors)

    workflow_paths = sorted(
        path for path in available_paths
        if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml"))
    )
    expect(TRUSTED_WORKFLOW in workflow_paths, "TRUSTED_WORKFLOW_MISSING", "Consumer-owned trusted-base workflow is absent.", TRUSTED_WORKFLOW, errors)
    for successor_path in sorted(successor_workflows):
        expect(successor_path in workflow_paths, "WORKFLOW_SUCCESSOR_MISSING", "A provenance-bound workflow successor is absent from its live path.", successor_path, errors)

    quarantined: set[str] = set()
    if isinstance(manifest, dict):
        quarantined = {
            item.get("sha256")
            for item in manifest.get("specimens", [])
            if isinstance(item, dict) and isinstance(item.get("sha256"), str)
        }
    for path in workflow_paths:
        content = view.read_bytes(path)
        digest = hashlib.sha256(content).hexdigest()
        expect(digest not in quarantined, "QUARANTINED_DIGEST_IN_LIVE_WORKFLOW", "A quarantined digest is present in the live workflow directory.", path, errors)
        workflow = parse_yaml(content, path, errors)
        if workflow is not None:
            if path in successor_workflows:
                expect(digest == successor_workflows[path], "WORKFLOW_SUCCESSOR_DIGEST_MISMATCH", "A provenance-bound live successor changed bytes; a new reviewed amendment is required.", path, errors)
            check_workflow(workflow, path, pins, errors)

    candidate_json_paths = (set(changed) & available_paths) if base_sha else {
        POLICY_PATH.as_posix(),
        ACTION_REGISTRY_PATH.as_posix(),
        PRESERVATION_MANIFEST_PATH.as_posix(),
        "policies/repository-hardening/BRANCH_RULESET_REQUIREMENTS_v0_1.json",
        "docs/preservation/control-stages/CLAIM_ADMISSION_HARDENING_STAGE_v0_1.json",
    }
    check_candidate_json(view, candidate_json_paths, errors)

    protected_paths: list[str] = []
    if isinstance(trusted_policy, dict):
        protected_paths = [value for value in trusted_policy.get("protected_control_paths", []) if isinstance(value, str)]
    changed_controls = sorted(
        path for path in changed
        if any(path == protected or (protected.endswith("/") and path.startswith(protected)) for protected in protected_paths)
    )

    errors.sort(key=lambda item: (item["code"], item["path"], item["message"]))
    return {
        "checker_id": CHECKER_ID,
        "result": {
            "ok": not errors,
            "result_kind": "STRUCTURAL_PASS" if not errors else "CLAIM_ADMISSION_GATE_FAILED",
            "admission_effect": "REVIEW_ELIGIBLE_NOT_ADMITTED" if not errors else "NOT_REVIEW_ELIGIBLE",
            "repository_standing_effect": "NONE",
        },
        "execution_boundary": {
            "mode": "TRUSTED_BASE_GIT_OBJECT_INSPECTION" if base_sha else "LOCAL_SELF_CHECK",
            "base_sha": base_sha or "WORKTREE",
            "candidate_sha": candidate_sha or "WORKTREE",
            "candidate_checkout": "NONE",
            "candidate_code_execution": "NONE",
            "repository_settings_effect": "NONE",
            "control_activation_effect": "NONE",
        },
        "verification": {
            "policy_id": POLICY_ID,
            "policy_activation_state": "IMPLEMENTED_DORMANT_UNTIL_PRESENT_ON_DEFAULT_BRANCH",
            "failure_class_id": FAILURE_CLASS_ID,
            "workflow_count": len(workflow_paths),
            "tree_entry_count": len(entries),
            "changed_file_count": len(changed),
            "changed_control_paths": changed_controls,
            "action_pins": pins,
            "provenance_bound_workflow_successors": [
                {
                    "path": path,
                    "sha256": digest,
                    "effect": "HARDENED_LIVE_SUCCESSOR_BOUND_TO_ARCHIVED_ORIGINAL",
                    "execution_separately_gated": True,
                }
                for path, digest in sorted(successor_workflows.items())
            ],
        },
        "errors": errors,
        "non_claims": {
            "does_not_approve_merge": True,
            "does_not_certify_security": True,
            "does_not_determine_semantic_correctness": True,
            "does_not_evaluate_producer_intent": True,
            "does_not_authorize_experiment_execution": True,
            "does_not_apply_repository_settings": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--base-sha")
    parser.add_argument("--candidate-sha")
    parser.add_argument("--fetch-repository")
    parser.add_argument("--write-receipt", type=Path)
    args = parser.parse_args()

    root = args.repo_root.resolve()
    initial_errors: list[dict[str, str]] = []
    if args.self_check:
        if args.base_sha or args.candidate_sha or args.fetch_repository:
            parser.error("--self-check cannot be combined with Git candidate arguments")
        view: CandidateView = WorktreeView(root)
        base_sha = None
        candidate_sha = None
        changed: list[str] = []
    else:
        if not args.base_sha or not args.candidate_sha:
            parser.error("--base-sha and --candidate-sha are required outside --self-check")
        base_sha = args.base_sha.lower()
        candidate_sha = args.candidate_sha.lower()
        if not SHA_RE.fullmatch(base_sha) or not SHA_RE.fullmatch(candidate_sha):
            parser.error("base and candidate SHAs must be lowercase full-length commit SHAs")
        try:
            if args.fetch_repository:
                fetch_candidate(root, args.fetch_repository, candidate_sha)
            run_git(root, ["cat-file", "-e", f"{base_sha}^{{commit}}"])
            run_git(root, ["cat-file", "-e", f"{candidate_sha}^{{commit}}"])
            changed, diff_errors = changed_files(root, base_sha, candidate_sha)
            initial_errors.extend(diff_errors)
        except (RuntimeError, ValueError) as exc:
            initial_errors.append(finding("CANDIDATE_GIT_RESOLUTION_FAILED", str(exc), "$candidate"))
            changed = []
        view = GitTreeView(root, candidate_sha)

    try:
        output = build_output(
            root,
            view,
            base_sha=base_sha,
            candidate_sha=candidate_sha,
            changed=changed,
            initial_errors=initial_errors,
        )
    except (RuntimeError, ValueError, UnicodeDecodeError) as exc:
        output = {
            "checker_id": CHECKER_ID,
            "result": {
                "ok": False,
                "result_kind": "CLAIM_ADMISSION_GATE_FAILED",
                "admission_effect": "NOT_REVIEW_ELIGIBLE",
                "repository_standing_effect": "NONE",
            },
            "execution_boundary": {
                "mode": "TRUSTED_BASE_GIT_OBJECT_INSPECTION" if not args.self_check else "LOCAL_SELF_CHECK",
                "candidate_checkout": "NONE",
                "candidate_code_execution": "NONE",
                "repository_settings_effect": "NONE",
                "control_activation_effect": "NONE",
            },
            "verification": {},
            "errors": [finding("CHECKER_INTERNAL_BOUNDARY_FAILURE", str(exc), "$")],
            "non_claims": {
                "does_not_approve_merge": True,
                "does_not_certify_security": True,
                "does_not_determine_semantic_correctness": True,
                "does_not_evaluate_producer_intent": True,
                "does_not_authorize_experiment_execution": True,
                "does_not_apply_repository_settings": True,
            },
        }

    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.write_receipt:
        path = args.write_receipt if args.write_receipt.is_absolute() else root / args.write_receipt
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if output["result"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
