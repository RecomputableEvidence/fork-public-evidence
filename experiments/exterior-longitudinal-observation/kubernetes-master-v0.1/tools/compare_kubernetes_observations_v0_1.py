#!/usr/bin/env python3
"""Compare two preserved Kubernetes observation packages without live access."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CHECKER_PATH = HERE / "check_kubernetes_observation_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("k8s_obs_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_time(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def retrieval_by_role(record: dict[str, Any], role: str) -> dict[str, Any] | None:
    return next((x for x in record["retrievals"] if x.get("role") == role), None)


def derive_comparison(left: dict[str, Any], left_raw: bytes,
                      right: dict[str, Any], right_raw: bytes) -> dict[str, Any]:
    left_time = parse_time(left["timing"]["started_at_utc"])
    right_time = parse_time(right["timing"]["started_at_utc"])
    if not left_time < right_time:
        raise ValueError("left observation must precede right observation")

    left_status = left["retrieval_status"]
    right_status = right["retrieval_status"]
    gap = left_status != "OBSERVED" or right_status != "OBSERVED"

    parser_changed = left["observer"]["parser_version"] != right["observer"]["parser_version"]
    left_branch = retrieval_by_role(left, "BRANCH_REPRESENTATION")
    right_branch = retrieval_by_role(right, "BRANCH_REPRESENTATION")
    left_commit = retrieval_by_role(left, "COMMIT_REPRESENTATION")
    right_commit = retrieval_by_role(right, "COMMIT_REPRESENTATION")

    branch_raw_changed = None
    commit_raw_changed = None
    semantic_changed = None
    head_changed = None
    tree_changed = None

    if left_branch and right_branch:
        branch_raw_changed = left_branch["raw_sha256"] != right_branch["raw_sha256"]
    if left_commit and right_commit:
        commit_raw_changed = left_commit["raw_sha256"] != right_commit["raw_sha256"]
    if not gap:
        semantic_changed = left["projection_sha256"] != right["projection_sha256"]
        head_changed = left["projection"]["head_sha"] != right["projection"]["head_sha"]
        tree_changed = left["projection"]["head_tree_sha"] != right["projection"]["head_tree_sha"]

    if parser_changed:
        classification = "PARSER_VERSION_CHANGED_UNRESOLVED"
    elif gap:
        classification = "OBSERVATION_GAP"
    elif semantic_changed:
        classification = "OBSERVED_REPRESENTATION_CHANGED"
    elif branch_raw_changed or commit_raw_changed:
        classification = "RAW_BYTES_CHANGED_SEMANTICS_STABLE"
    else:
        classification = "OBSERVED_REPRESENTATION_UNCHANGED"

    comparison_seed = f"{left['observation_id']}|{right['observation_id']}|{classification}".encode()
    return {
        "schema_version": "0.1",
        "experiment_id": "FORK_ELO_KUBERNETES_MASTER_v0_1",
        "comparison_id": "K8S-MASTER-CMP-" + digest(comparison_seed)[:16],
        "left": {
            "observation_id": left["observation_id"],
            "record_sha256": digest(left_raw),
            "started_at_utc": left["timing"]["started_at_utc"],
        },
        "right": {
            "observation_id": right["observation_id"],
            "record_sha256": digest(right_raw),
            "started_at_utc": right["timing"]["started_at_utc"],
        },
        "classification": classification,
        "differences": {
            "branch_raw_bytes_changed": branch_raw_changed,
            "commit_raw_bytes_changed": commit_raw_changed,
            "semantic_projection_changed": semantic_changed,
            "head_sha_changed": head_changed,
            "head_tree_sha_changed": tree_changed,
        },
        "observation_gap_present": gap,
        "underlying_change_time": "UNRESOLVED",
        "cause": "UNRESOLVED",
        "intermediate_state_completeness": "UNRESOLVED",
        "effects": {
            "source_modification": "NONE",
            "authority": "NONE",
            "admission": "NONE",
            "execution": "NONE",
            "truth": "NONE",
            "causality": "NONE",
            "endorsement": "NONE",
        },
        "non_claims": [
            "No exact transition time is established.",
            "No cause or project approval is established.",
            "No authority is inherited from either observation.",
            "No unobserved intermediate state is inferred.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left_record", type=Path)
    parser.add_argument("right_record", type=Path)
    parser.add_argument("--left-root", type=Path)
    parser.add_argument("--right-root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    checker = load_checker()
    left, left_raw = checker.load_json(args.left_record)
    right, right_raw = checker.load_json(args.right_record)
    left_root = (args.left_root or args.left_record.parent).resolve()
    right_root = (args.right_root or args.right_record.parent).resolve()
    findings = [
        *(f"LEFT:{x}" for x in checker.validate_record(left, left_root)),
        *(f"RIGHT:{x}" for x in checker.validate_record(right, right_root)),
    ]
    if findings:
        print("KUBERNETES_EXTERIOR_COMPARISON_NONCONFORMING_INPUT")
        for finding in findings:
            print(f"- {finding}")
        return 1

    result = derive_comparison(left, left_raw, right, right_raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(canonical_bytes(result))
    print("KUBERNETES_EXTERIOR_COMPARISON_REPRODUCED")
    print(f"classification: {result['classification']}")
    print(f"comparison_id: {result['comparison_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
