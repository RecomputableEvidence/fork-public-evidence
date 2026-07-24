#!/usr/bin/env python3
"""Deterministic validator for Kubernetes exterior observation records."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

EXPERIMENT_ID = "FORK_ELO_KUBERNETES_MASTER_v0_1"
OBS_ID = re.compile(r"^K8S-MASTER-OBS-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{12}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SHA1 = re.compile(r"^[0-9a-f]{40}$")
NONE_EFFECTS = {
    "source_modification", "fork_repository_mutation", "authority", "admission",
    "execution", "truth", "causality", "endorsement",
}


class DuplicateKeyError(ValueError):
    pass


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError("record must be a JSON object")
    return value, raw


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_rel(path: str) -> bool:
    p = Path(path)
    return not p.is_absolute() and ".." not in p.parts and path.replace("\\", "/") == path


def parse_json_object(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates)
    except Exception as exc:
        raise ValueError(f"{label} is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def derive_projection(branch_body: bytes, commit_body: bytes) -> dict[str, Any]:
    branch = parse_json_object(branch_body, "branch response")
    commit = parse_json_object(commit_body, "commit response")
    branch_commit = branch.get("commit")
    commit_tree = commit.get("commit", {}).get("tree", {})
    parents = commit.get("parents")
    if not isinstance(branch_commit, dict) or not isinstance(branch_commit.get("sha"), str):
        raise ValueError("branch response missing commit.sha")
    if commit.get("sha") != branch_commit["sha"]:
        raise ValueError("commit response SHA does not match branch head SHA")
    if not isinstance(commit_tree.get("sha"), str):
        raise ValueError("commit response missing commit.tree.sha")
    if not isinstance(parents, list) or any(
        not isinstance(parent, dict) or not isinstance(parent.get("sha"), str)
        for parent in parents
    ):
        raise ValueError("commit response parents malformed")
    return {
        "branch_name": branch.get("name"),
        "head_sha": branch_commit["sha"],
        "head_tree_sha": commit_tree["sha"],
        "parent_shas": [parent["sha"] for parent in parents],
        "protected": branch.get("protected"),
    }


def validate_record(record: dict[str, Any], artifact_root: Path) -> list[str]:
    findings: list[str] = []
    if record.get("schema_version") != "0.1":
        findings.append("SCHEMA_VERSION_INVALID")
    if record.get("experiment_id") != EXPERIMENT_ID:
        findings.append("EXPERIMENT_ID_INVALID")
    if not isinstance(record.get("observation_id"), str) or not OBS_ID.fullmatch(record["observation_id"]):
        findings.append("OBSERVATION_ID_INVALID")

    source = record.get("source")
    if not isinstance(source, dict) or source.get("repository") != "kubernetes/kubernetes" or source.get("branch") != "master":
        findings.append("SOURCE_COORDINATE_INVALID")

    policy = record.get("request_policy")
    if not isinstance(policy, dict):
        findings.append("REQUEST_POLICY_MISSING")
    else:
        expected = {
            "method": "GET", "authenticated": False, "automatic_retries": 0,
            "redirects_followed": False, "maximum_requests": 2,
        }
        for key, value in expected.items():
            if policy.get(key) != value:
                findings.append(f"REQUEST_POLICY_INVALID:{key}")

    effects = record.get("effects")
    if not isinstance(effects, dict):
        findings.append("EFFECTS_MISSING")
    else:
        for key in sorted(NONE_EFFECTS):
            if effects.get(key) != "NONE":
                findings.append(f"EFFECT_PROMOTION_FORBIDDEN:{key}")

    retrievals = record.get("retrievals")
    if not isinstance(retrievals, list) or len(retrievals) > 2:
        findings.append("RETRIEVALS_INVALID")
        retrievals = []
    roles = set()
    raw_by_role: dict[str, bytes] = {}
    for index, item in enumerate(retrievals):
        prefix = f"RETRIEVAL_{index}"
        if not isinstance(item, dict):
            findings.append(f"{prefix}_INVALID")
            continue
        role = item.get("role")
        if role in roles:
            findings.append(f"{prefix}_DUPLICATE_ROLE")
        roles.add(role)
        if item.get("method") != "GET":
            findings.append(f"{prefix}_METHOD_INVALID")
        raw_path = item.get("raw_path")
        if not isinstance(raw_path, str) or not safe_rel(raw_path):
            findings.append(f"{prefix}_RAW_PATH_INVALID")
            continue
        candidate = (artifact_root / raw_path).resolve()
        try:
            candidate.relative_to(artifact_root.resolve())
        except ValueError:
            findings.append(f"{prefix}_RAW_PATH_ESCAPE")
            continue
        if not candidate.is_file():
            findings.append(f"{prefix}_RAW_MISSING")
            continue
        raw = candidate.read_bytes()
        if isinstance(role, str):
            raw_by_role[role] = raw
        if item.get("raw_sha256") != digest(raw):
            findings.append(f"{prefix}_RAW_DIGEST_MISMATCH")
        if item.get("raw_size_bytes") != len(raw):
            findings.append(f"{prefix}_RAW_SIZE_MISMATCH")

    status = record.get("retrieval_status")
    projection = record.get("projection")
    projection_sha = record.get("projection_sha256")
    if status == "OBSERVED":
        if roles != {"BRANCH_REPRESENTATION", "COMMIT_REPRESENTATION"}:
            findings.append("OBSERVED_REQUIRES_TWO_RETRIEVALS")
        if not isinstance(projection, dict):
            findings.append("OBSERVED_PROJECTION_MISSING")
        else:
            if projection.get("branch_name") != "master":
                findings.append("PROJECTION_BRANCH_INVALID")
            if not isinstance(projection.get("head_sha"), str) or not SHA1.fullmatch(projection["head_sha"]):
                findings.append("PROJECTION_HEAD_SHA_INVALID")
            if not isinstance(projection.get("head_tree_sha"), str) or not SHA1.fullmatch(projection["head_tree_sha"]):
                findings.append("PROJECTION_TREE_SHA_INVALID")
            parents = projection.get("parent_shas")
            if not isinstance(parents, list) or any(not isinstance(x, str) or not SHA1.fullmatch(x) for x in parents):
                findings.append("PROJECTION_PARENTS_INVALID")
            computed = digest(canonical_bytes(projection))
            if projection_sha != computed:
                findings.append("PROJECTION_DIGEST_MISMATCH")
            try:
                derived = derive_projection(
                    raw_by_role["BRANCH_REPRESENTATION"],
                    raw_by_role["COMMIT_REPRESENTATION"],
                )
                if projection != derived:
                    findings.append("PROJECTION_DIVERGES_FROM_RAW_BYTES")
                expected_commit_url = (
                    "https://api.github.com/repos/kubernetes/kubernetes/commits/"
                    + derived["head_sha"]
                )
                commit_retrieval = next(
                    (item for item in retrievals if item.get("role") == "COMMIT_REPRESENTATION"),
                    None,
                )
                if not isinstance(commit_retrieval, dict) or commit_retrieval.get("url") != expected_commit_url:
                    findings.append("COMMIT_ENDPOINT_NOT_BOUND_TO_OBSERVED_HEAD")
            except (KeyError, ValueError, DuplicateKeyError) as exc:
                findings.append(f"RAW_DERIVATION_FAILED:{type(exc).__name__}")
    elif status in {"RETRIEVAL_FAILED", "WINDOW_INACTIVE"}:
        if projection is not None or projection_sha is not None:
            findings.append("FAILED_OBSERVATION_MUST_NOT_HAVE_PROJECTION")
    else:
        findings.append("RETRIEVAL_STATUS_INVALID")

    unresolved = record.get("unresolved")
    required_unresolved = {
        "UNDERLYING_CHANGE_TIME", "CAUSE", "INTERMEDIATE_STATE_COMPLETENESS",
        "SOURCE_TRUTH_AND_COMPLETENESS", "EXTERNAL_AUTHORITY_EFFECT",
    }
    if not isinstance(unresolved, list) or not required_unresolved.issubset(set(unresolved)):
        findings.append("UNRESOLVED_BOUNDARY_INCOMPLETE")

    previous = record.get("previous_observation")
    if previous is not None:
        if not isinstance(previous, dict) or not isinstance(previous.get("record_sha256"), str) or not SHA256.fullmatch(previous["record_sha256"]):
            findings.append("PREVIOUS_OBSERVATION_BINDING_INVALID")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    parser.add_argument("--artifact-root", type=Path)
    args = parser.parse_args()
    root = (args.artifact_root or args.record.parent).resolve()
    record, _ = load_json(args.record)
    findings = validate_record(record, root)
    if findings:
        print("KUBERNETES_EXTERIOR_OBSERVATION_NONCONFORMING")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("KUBERNETES_EXTERIOR_OBSERVATION_CONFORMS")
    print(f"observation_id: {record['observation_id']}")
    print(f"retrieval_status: {record['retrieval_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
