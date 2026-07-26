#!/usr/bin/env python3
"""Recompute vector-valued evidentiary standing across an exact Git interval."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BASE = Path("docs/state/longitudinal-recomputation-v0.2")
CONTRACT = BASE / "LONGITUDINAL_REPLAY_CONTRACT_v0_2.json"
REGISTRY = BASE / "LONGITUDINAL_EVENT_REGISTRY_v0_2.json"
PROJECTION = BASE / "LONGITUDINAL_CURRENT_PROJECTION_v0_2.json"
COVERAGE = BASE / "LONGITUDINAL_EVENT_COVERAGE_RECEIPT_v0_1.json"
TRANSITION = BASE / "STANDING_TRANSITION_RECEIPT_v0_1.json"
MANIFEST = BASE / "PACKAGE_MANIFEST_v0_2.json"
SCHEMA = Path("schemas/fork_longitudinal_event_registry_v0_2.schema.json")
SEQUENCE_CHECKER = Path("tools/check_fork_sequence_surface_v0_1.py")
TEMPORAL_CHECKER = Path("tools/check_temporal_succession_v0_1.py")
ADVERSARIAL_CASES = BASE / "ADVERSARIAL_CASES_v0_2.json"
README = BASE / "README.md"
NON_CLAIMS = BASE / "NON_CLAIMS_AND_LIMITS_v0_2.md"
CLAIM_ADMISSION_CORRECTION = BASE / "CLAIM_ADMISSION_RECEIPT_RECOMPUTATION_v0_1.md"
CLAIM_ADMISSION_RECEIPT = Path(
    "receipts/claim-admission/"
    "FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json"
)
STATE_ROUTE = Path("docs/state/FORK_STATE_ROUTING_v0_2.json")
STATE_README = Path("docs/state/README.md")
TEST_PATH = Path("tests/test_longitudinal_recomputation_v0_2.py")
TOOL_PATH = Path("tools/check_longitudinal_recomputation_v0_2.py")

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_PACKAGE_PATHS = {
    ADVERSARIAL_CASES.as_posix(),
    CLAIM_ADMISSION_CORRECTION.as_posix(),
    CLAIM_ADMISSION_RECEIPT.as_posix(),
    CONTRACT.as_posix(),
    COVERAGE.as_posix(),
    NON_CLAIMS.as_posix(),
    PROJECTION.as_posix(),
    README.as_posix(),
    REGISTRY.as_posix(),
    SCHEMA.as_posix(),
    STATE_README.as_posix(),
    STATE_ROUTE.as_posix(),
    TEST_PATH.as_posix(),
    TOOL_PATH.as_posix(),
    TRANSITION.as_posix(),
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def assert_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if isinstance(value, dict):
        for item in value.values():
            assert_finite(item)
    elif isinstance(value, list):
        for item in value:
            assert_finite(item)


def strict_load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    assert_finite(value)
    return value


def pretty_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ) + "\n"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def state_sha256(state: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(state))


def add_finding(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str = "",
) -> None:
    findings.append({"code": code, "detail": detail, "path": path})


def safe_regular_file(root: Path, relative: Any) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValueError("path must be a non-empty repository-relative string")
    pure = PurePosixPath(relative)
    if (
        pure.is_absolute()
        or "." in pure.parts
        or ".." in pure.parts
        or "\\" in relative
        or relative != pure.as_posix()
    ):
        raise ValueError(f"unsafe or non-canonical path: {relative!r}")
    root_real = root.resolve(strict=True)
    current = root
    for part in pure.parts:
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"symlink substitution rejected: {relative}")
    if not stat.S_ISREG(current.stat().st_mode):
        raise ValueError(f"not a regular file: {relative}")
    current.resolve(strict=True).relative_to(root_real)
    return current


def parse_time(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: timestamp must be a non-empty string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"{label}: timestamp must include a timezone")
    return parsed.astimezone(timezone.utc)


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed ({completed.returncode}): "
            f"{completed.stderr.strip()}"
        )
    return completed.stdout


def git_commit_metadata(root: Path, commit: str) -> dict[str, Any]:
    if SHA1_RE.fullmatch(commit) is None:
        raise ValueError(f"invalid commit SHA: {commit!r}")
    raw = run_git(
        root,
        "show",
        "-s",
        "--format=%H%x00%T%x00%P%x00%cI%x00%s",
        commit,
    ).rstrip("\n")
    fields = raw.split("\x00")
    if len(fields) != 5:
        raise RuntimeError(f"unexpected git metadata shape for {commit}")
    changed = sorted(
        {
            line.strip()
            for line in run_git(
                root,
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                "--root",
                commit,
            ).splitlines()
            if line.strip()
        }
    )
    return {
        "commit_sha": fields[0],
        "tree_sha": fields[1],
        "parent_commits": fields[2].split() if fields[2] else [],
        "committed_at_utc": parse_time(fields[3], f"commit {commit}")
        .isoformat()
        .replace("+00:00", "Z"),
        "subject": fields[4],
        "changed_paths": changed,
    }


def interval_inventory(
    root: Path,
    base_commit: str,
    closure_commit: str,
) -> list[dict[str, Any]]:
    if SHA1_RE.fullmatch(base_commit) is None or SHA1_RE.fullmatch(closure_commit) is None:
        raise ValueError("coverage interval requires full lowercase commit SHAs")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_commit, closure_commit],
        cwd=root,
        check=False,
        capture_output=True,
    )
    if ancestor.returncode != 0:
        raise ValueError("coverage base is not an ancestor of the closure commit")
    commits = [
        line.strip()
        for line in run_git(
            root,
            "rev-list",
            "--reverse",
            "--topo-order",
            "--ancestry-path",
            f"{base_commit}..{closure_commit}",
        ).splitlines()
        if line.strip()
    ]
    return [git_commit_metadata(root, commit) for commit in commits]


def validate_registry_schema(
    root: Path,
    registry: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    try:
        schema = strict_load(safe_regular_file(root, SCHEMA.as_posix()))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(registry), key=lambda item: list(item.path))
        for error in errors:
            location = "/".join(str(item) for item in error.path)
            add_finding(
                findings,
                "EVENT_SCHEMA_INVALID",
                error.message,
                f"{REGISTRY.as_posix()}:{location}",
            )
    except Exception as exc:
        add_finding(findings, "EVENT_SCHEMA_INVALID", str(exc), SCHEMA.as_posix())


def derive_sequence_contribution(
    root: Path,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    try:
        checker = load_module(root / SEQUENCE_CHECKER, "fork_sequence_surface_for_longitudinal")
        result = checker.evaluate(root)
    except Exception as exc:
        add_finding(
            findings,
            "SURFACE_REDUCER_FAILED",
            str(exc),
            SEQUENCE_CHECKER.as_posix(),
        )
        return {}
    if result.get("errors"):
        for error in result["errors"]:
            add_finding(
                findings,
                "SURFACE_REDUCER_FAILED",
                f"{error.get('code')}: {error.get('detail')}",
                error.get("path", SEQUENCE_CHECKER.as_posix()),
            )
        return {}
    projection = result.get("projection")
    if not isinstance(projection, dict):
        add_finding(
            findings,
            "SURFACE_REDUCER_FAILED",
            "Sequence Surface did not return a projection",
            SEQUENCE_CHECKER.as_posix(),
        )
        return {}
    return {
        "standing": projection.get("publication_and_control", {}).get(
            "pre_execution_status"
        ),
        "reducer_id": "FORK_SEQUENCE_SURFACE_REDUCER_v0_1",
        "reducer_result": result.get("result", {}).get("status"),
        "source": copy.deepcopy(projection.get("source")),
        "sequence": copy.deepcopy(projection.get("sequence")),
        "observed_history": copy.deepcopy(projection.get("observed_history")),
        "execution_boundary": copy.deepcopy(projection.get("execution_boundary")),
        "retry": copy.deepcopy(projection.get("retry")),
        "drift": copy.deepcopy(projection.get("drift")),
        "freshness": "DERIVED_FROM_BOUND_PRIMARY_EVIDENCE",
    }


def validate_predecessor_temporal_surface(
    root: Path,
    findings: list[dict[str, str]],
) -> None:
    try:
        checker = load_module(root / TEMPORAL_CHECKER, "temporal_surface_for_longitudinal")
        errors = checker.check(root)
    except Exception as exc:
        add_finding(
            findings,
            "PREDECESSOR_TEMPORAL_SURFACE_INVALID",
            str(exc),
            TEMPORAL_CHECKER.as_posix(),
        )
        return
    for error in errors:
        add_finding(
            findings,
            "PREDECESSOR_TEMPORAL_SURFACE_INVALID",
            error,
            TEMPORAL_CHECKER.as_posix(),
        )


def validate_state_route(
    root: Path,
    contract: dict[str, Any],
    registry: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    try:
        route = strict_load(safe_regular_file(root, STATE_ROUTE.as_posix()))
        historical = strict_load(
            safe_regular_file(root, "docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json")
        )
        governed = strict_load(
            safe_regular_file(
                root,
                "docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json",
            )
        )
        readme = safe_regular_file(root, STATE_README.as_posix()).read_text(
            encoding="utf-8"
        )
    except Exception as exc:
        add_finding(findings, "STATE_ROUTE_INVALID", str(exc), STATE_ROUTE.as_posix())
        return
    expected_historical = {
        "path": "docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json",
        "sha256": sha256_file(
            safe_regular_file(root, "docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json")
        ),
        "standing": (
            "HISTORICAL_PROJECTION_VALID_AT_RECORDED_TEMPORAL_CLOSURE_"
            "NOT_CURRENT_RELIANCE_STANDING"
        ),
    }
    expected_governed = {
        "path": "docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json",
        "source_commit": governed.get("source_coordinate", {}).get("commit_sha"),
        "standing": governed.get("projection_standing"),
    }
    expected_candidate = {
        "path": PROJECTION.as_posix(),
        "base_commit": contract.get("initial_coordinate", {}).get("commit_sha"),
        "closure_commit": registry.get("coverage_interval", {}).get(
            "closure_commit_inclusive"
        ),
        "standing": "RESEARCH_CANDIDATE_NOT_ADMITTED",
    }
    comparisons = (
        ("historical_projection", route.get("historical_projection"), expected_historical),
        ("governed_projection", route.get("governed_projection"), expected_governed),
        (
            "longitudinal_replay_candidate",
            route.get("longitudinal_replay_candidate"),
            expected_candidate,
        ),
    )
    for label, actual, expected in comparisons:
        if actual != expected:
            add_finding(
                findings,
                "STATE_ROUTE_INVALID",
                f"{label}: expected {expected!r}, found {actual!r}",
                STATE_ROUTE.as_posix(),
            )
    if historical.get("as_of_date") != "2026-07-11":
        add_finding(
            findings,
            "STATE_ROUTE_INVALID",
            "historical projection no longer carries its July 11 closure",
            "docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json",
        )
    required_readme_routes = (
        STATE_ROUTE.as_posix(),
        expected_historical["path"],
        expected_governed["path"],
        expected_candidate["path"].removeprefix("docs/state/"),
    )
    for required in required_readme_routes:
        if required not in readme:
            add_finding(
                findings,
                "STATE_ROUTE_README_DIVERGENCE",
                f"state README does not route to {required}",
                STATE_README.as_posix(),
            )


def validate_evidence_refs(
    root: Path,
    registry: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    for event in registry.get("events", []):
        if not isinstance(event, dict):
            continue
        for reference in event.get("evidence_refs", []):
            if not isinstance(reference, dict):
                continue
            relative = reference.get("path")
            try:
                path = safe_regular_file(root, relative)
                if path.stat().st_size != reference.get("size_bytes"):
                    add_finding(
                        findings,
                        "EVIDENCE_SIZE_MISMATCH",
                        f"expected {reference.get('size_bytes')}, found {path.stat().st_size}",
                        str(relative),
                    )
                if sha256_file(path) != reference.get("sha256"):
                    add_finding(
                        findings,
                        "EVIDENCE_DIGEST_MISMATCH",
                        "bound evidence bytes differ",
                        str(relative),
                    )
            except Exception as exc:
                add_finding(
                    findings,
                    "EVIDENCE_DIGEST_MISMATCH",
                    str(exc),
                    str(relative),
                )


def derive_coverage_receipt(
    root: Path,
    registry: dict[str, Any],
    findings: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    interval = registry.get("coverage_interval", {})
    base_commit = interval.get("base_commit_exclusive")
    closure_commit = interval.get("closure_commit_inclusive")
    try:
        inventory = interval_inventory(root, base_commit, closure_commit)
    except Exception as exc:
        add_finding(findings, "EVENT_COVERAGE_UNRESOLVED", str(exc), REGISTRY.as_posix())
        inventory = []

    events = [item for item in registry.get("events", []) if isinstance(item, dict)]
    events_by_commit: dict[str, dict[str, Any]] = {}
    duplicate_commits: list[str] = []
    duplicate_event_ids: list[str] = []
    seen_event_ids: set[str] = set()
    for event in events:
        event_id = event.get("event_id")
        source_commit = event.get("source_commit")
        if event_id in seen_event_ids:
            duplicate_event_ids.append(str(event_id))
        elif isinstance(event_id, str):
            seen_event_ids.add(event_id)
        if source_commit in events_by_commit:
            duplicate_commits.append(str(source_commit))
        elif isinstance(source_commit, str):
            events_by_commit[source_commit] = event

    inventory_by_commit = {item["commit_sha"]: item for item in inventory}
    unclassified = sorted(set(inventory_by_commit) - set(events_by_commit))
    out_of_interval = sorted(set(events_by_commit) - set(inventory_by_commit))
    if unclassified:
        add_finding(
            findings,
            "EVENT_COVERAGE_UNRESOLVED",
            f"unclassified interval commits: {', '.join(unclassified)}",
            REGISTRY.as_posix(),
        )
    if out_of_interval:
        add_finding(
            findings,
            "EVENT_OUTSIDE_DECLARED_INTERVAL",
            f"registered event commits outside interval: {', '.join(out_of_interval)}",
            REGISTRY.as_posix(),
        )
    if duplicate_commits or duplicate_event_ids:
        add_finding(
            findings,
            "EVENT_REGISTRY_DUPLICATE",
            f"duplicate commits={duplicate_commits}; duplicate event ids={duplicate_event_ids}",
            REGISTRY.as_posix(),
        )

    for commit_sha in sorted(set(inventory_by_commit).intersection(events_by_commit)):
        metadata = inventory_by_commit[commit_sha]
        event = events_by_commit[commit_sha]
        comparisons = (
            ("source_tree", event.get("source_tree"), metadata["tree_sha"]),
            (
                "source_parent_commits",
                event.get("source_parent_commits"),
                metadata["parent_commits"],
            ),
            ("changed_paths", sorted(event.get("changed_paths", [])), metadata["changed_paths"]),
        )
        for label, actual, expected in comparisons:
            if actual != expected:
                add_finding(
                    findings,
                    "EVENT_GIT_BINDING_MISMATCH",
                    f"{label}: expected {expected!r}, found {actual!r}",
                    f"{REGISTRY.as_posix()}:{event.get('event_id')}",
                )
        try:
            event_time = parse_time(event.get("occurred_at_utc"), str(event.get("event_id")))
            parent_times = [
                parse_time(
                    git_commit_metadata(root, parent)["committed_at_utc"],
                    f"parent {parent}",
                )
                for parent in metadata["parent_commits"]
            ]
            if parent_times and event_time < max(parent_times):
                add_finding(
                    findings,
                    "EVENT_TIME_PRECEDES_PARENT",
                    "event time precedes its latest parent closure",
                    str(event.get("event_id")),
                )
        except Exception as exc:
            add_finding(findings, "EVENT_TIME_INVALID", str(exc), str(event.get("event_id")))

    classifications: dict[str, list[str]] = {
        "ACCOUNTED_EVIDENCE_PRESERVATION_EVENT_NOT_ADMISSION": [],
        "ACCOUNTED_ADMITTED_STATE_CHANGE": [],
        "ACCOUNTED_EXCLUDED_WITH_REASON": [],
        "ACCOUNTED_UNRESOLVED": [],
    }
    for event in events:
        classification = event.get("coverage_classification")
        if classification in classifications:
            classifications[classification].append(event.get("source_commit"))

    receipt = {
        "schema_version": "v0.1",
        "record_kind": "fork_longitudinal_event_coverage_receipt",
        "receipt_id": "FORK_LONGITUDINAL_EVENT_COVERAGE_PR90_REVIEW_SUCCESSION_v0_1",
        "interval": copy.deepcopy(interval),
        "git_inventory": inventory,
        "classification": {
            key: sorted(value) for key, value in classifications.items()
        },
        "commit_count": len(inventory),
        "classified_commit_count": len(set(inventory_by_commit).intersection(events_by_commit)),
        "unclassified_commits": unclassified,
        "registered_commits_outside_interval": out_of_interval,
        "result": (
            "BOUNDED_EVENT_COVERAGE_REPRODUCED"
            if not unclassified
            and not out_of_interval
            and not duplicate_commits
            and not duplicate_event_ids
            else "EVENT_COVERAGE_UNRESOLVED"
        ),
        "interpretation": {
            "proves": [
                "every Git commit in the exact declared ancestry-path interval is classified",
                "registered commits bind their exact tree, parents, and changed paths",
            ],
            "does_not_prove": [
                "semantic event completeness outside the interval",
                "correct event classification",
                "admission",
                "authority",
                "truth",
                "execution permission",
            ],
        },
    }
    return receipt, inventory_by_commit


def materialize_initial_state(
    contract: dict[str, Any],
    sequence_contribution: dict[str, Any],
) -> dict[str, Any]:
    state = copy.deepcopy(contract["initial_state"])
    state["execution_state"] = copy.deepcopy(sequence_contribution)
    return state


def validate_effect_boundary(
    event: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    event_id = str(event.get("event_id"))
    admission_changed = before.get("admission_state") != after.get("admission_state")
    authority_changed = before.get("authority_state") != after.get("authority_state")
    execution_changed = before.get("execution_state") != after.get("execution_state")
    if admission_changed and event.get("admission_effect") == "NONE":
        add_finding(
            findings,
            "ADMISSION_EFFECT_MISMATCH",
            "admission_state changed without a declared admission effect",
            event_id,
        )
    if (
        event.get("event_kind") == "EVIDENCE_PRESERVATION"
        and event.get("admission_effect") != "NONE"
    ):
        add_finding(
            findings,
            "ADMISSION_EFFECT_MISMATCH",
            "evidence preservation cannot confer or revoke admission",
            event_id,
        )
    if authority_changed and event.get("authority_effect") == "NONE":
        add_finding(
            findings,
            "AUTHORITY_EFFECT_MISMATCH",
            "authority_state changed without a declared authority effect",
            event_id,
        )
    if execution_changed and event.get("execution_effect") == "NONE":
        add_finding(
            findings,
            "EXECUTION_EFFECT_MISMATCH",
            "execution_state changed without a declared execution effect",
            event_id,
        )


def validate_review_freshness(
    state: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    artifact_head = state.get("artifact_state", {}).get("basis_commit")
    verification = state.get("verification_state", {})
    standing = verification.get("standing")
    if (
        standing == "CURRENT_HEAD_INDEPENDENTLY_RECOMPUTED"
        and verification.get("reviewed_head") != artifact_head
    ):
        add_finding(
            findings,
            "CURRENT_HEAD_REVIEW_STALE",
            "current-head recomputation standing is attached to a different reviewed head",
            "verification_state",
        )


def validate_authority_freshness(
    state: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    authority = state.get("authority_state", {})
    closure = state.get("temporal_closure", {})
    if authority.get("standing") != "ACTIVE":
        return
    valid_until = authority.get("valid_until_utc")
    if valid_until is None:
        return
    try:
        if parse_time(valid_until, "authority valid_until") < parse_time(
            closure.get("as_of_utc"), "temporal closure"
        ):
            add_finding(
                findings,
                "AUTHORITY_EXPIRED_OR_REVOKED",
                "authority remains ACTIVE after its declared validity window",
                "authority_state",
            )
    except Exception as exc:
        add_finding(findings, "AUTHORITY_WINDOW_INVALID", str(exc), "authority_state")


def replay(
    contract: dict[str, Any],
    registry: dict[str, Any],
    sequence_contribution: dict[str, Any],
    findings: list[dict[str, str]],
    *,
    as_of: str | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    dimensions = contract.get("dimensions", [])
    if (
        not isinstance(dimensions, list)
        or len(dimensions) != len(set(dimensions))
        or set(contract.get("initial_state", {})) != set(dimensions)
    ):
        add_finding(
            findings,
            "STANDING_VECTOR_CONTRACT_INVALID",
            "dimensions must be unique and exactly match initial_state keys",
            CONTRACT.as_posix(),
        )
    state = materialize_initial_state(contract, sequence_contribution)
    initial_state = copy.deepcopy(state)
    events = [item for item in registry.get("events", []) if isinstance(item, dict)]
    events.sort(key=lambda item: item.get("ordinal", 0))
    base_commit = contract.get("initial_coordinate", {}).get("commit_sha")
    valid_targets = {base_commit, *(event.get("source_commit") for event in events)}
    if as_of is not None and as_of not in valid_targets:
        add_finding(
            findings,
            "EVENT_COVERAGE_UNRESOLVED",
            f"as-of coordinate is not a replay closure: {as_of}",
            REGISTRY.as_posix(),
        )
        return state, [], initial_state
    if as_of == base_commit:
        return state, [], initial_state

    transitions: list[dict[str, Any]] = []
    event_heads: set[str] = set()
    seen_ids: set[str] = set()
    for expected_ordinal, event in enumerate(events, start=1):
        event_id = event.get("event_id")
        if event.get("ordinal") != expected_ordinal:
            add_finding(
                findings,
                "EVENT_ORDINAL_INVALID",
                f"expected ordinal {expected_ordinal}, found {event.get('ordinal')}",
                str(event_id),
            )
        predecessor_ids = set(event.get("predecessor_event_ids", []))
        if event_heads and predecessor_ids != event_heads:
            add_finding(
                findings,
                "CONCURRENT_SUCCESSOR_UNRECONCILED",
                f"expected predecessors {sorted(event_heads)}, found {sorted(predecessor_ids)}",
                str(event_id),
            )
        elif not event_heads and predecessor_ids:
            add_finding(
                findings,
                "CONCURRENT_SUCCESSOR_UNRECONCILED",
                "first event cannot name an unknown predecessor event",
                str(event_id),
            )
        unknown_predecessors = predecessor_ids - seen_ids
        if unknown_predecessors:
            add_finding(
                findings,
                "EVENT_PREDECESSOR_UNKNOWN",
                f"unknown predecessor ids: {sorted(unknown_predecessors)}",
                str(event_id),
            )

        effects = event.get("dimension_effects", {})
        affected = event.get("affected_dimensions", [])
        effect_keys = set(effects) if isinstance(effects, dict) else set()
        if effect_keys != set(affected):
            add_finding(
                findings,
                "UNDECLARED_DIMENSION_CHANGE",
                f"affected dimensions {sorted(affected)} differ from effects {sorted(effect_keys)}",
                str(event_id),
            )
        unknown_dimensions = effect_keys - set(dimensions)
        if unknown_dimensions:
            add_finding(
                findings,
                "UNDECLARED_DIMENSION_CHANGE",
                f"unknown dimensions: {sorted(unknown_dimensions)}",
                str(event_id),
            )

        before = copy.deepcopy(state)
        for dimension, effect in effects.items():
            if dimension not in state or not isinstance(effect, dict):
                continue
            operation = effect.get("operation")
            after_value = copy.deepcopy(effect.get("after"))
            if operation == "PRESERVE" and after_value != state[dimension]:
                add_finding(
                    findings,
                    "PRESERVED_DIMENSION_CHANGED",
                    f"{dimension} changed under PRESERVE operation",
                    str(event_id),
                )
            elif operation == "REPLACE":
                state[dimension] = after_value
            elif operation != "PRESERVE":
                add_finding(
                    findings,
                    "DIMENSION_OPERATION_INVALID",
                    f"unsupported operation: {operation!r}",
                    str(event_id),
                )

        validate_effect_boundary(event, before, state, findings)
        validate_review_freshness(state, findings)
        validate_authority_freshness(state, findings)
        transitions.append(
            {
                "event_id": event_id,
                "source_commit": event.get("source_commit"),
                "before_state_sha256": state_sha256(before),
                "after_state_sha256": state_sha256(state),
                "changed_dimensions": sorted(
                    dimension
                    for dimension in dimensions
                    if before.get(dimension) != state.get(dimension)
                ),
                "preserved_dimensions": sorted(
                    dimension
                    for dimension in dimensions
                    if before.get(dimension) == state.get(dimension)
                ),
            }
        )
        event_heads.difference_update(predecessor_ids)
        if isinstance(event_id, str):
            event_heads.add(event_id)
            seen_ids.add(event_id)
        if as_of == event.get("source_commit"):
            break

    return state, transitions, initial_state


def currentness_summary(state: dict[str, Any]) -> dict[str, Any]:
    return {
        dimension: {
            "standing": value.get("standing") if isinstance(value, dict) else None,
            "freshness": value.get("freshness") if isinstance(value, dict) else None,
            "basis_commit": (
                value.get("basis_commit")
                or value.get("reviewed_head")
                or value.get("commit_sha")
                if isinstance(value, dict)
                else None
            ),
        }
        for dimension, value in state.items()
    }


def derive_projection(
    contract: dict[str, Any],
    registry: dict[str, Any],
    state: dict[str, Any],
    transitions: list[dict[str, Any]],
    sequence_contribution: dict[str, Any],
) -> dict[str, Any]:
    interval = copy.deepcopy(registry["coverage_interval"])
    effective_closure = state.get("temporal_closure", {}).get("commit_sha")
    if isinstance(effective_closure, str):
        interval["closure_commit_inclusive"] = effective_closure
    return {
        "schema_version": "v0.2",
        "record_kind": "fork_longitudinal_recomputed_projection",
        "projection_id": "FORK_LONGITUDINAL_CURRENT_PROJECTION_PR90_REVIEW_SUCCESSION_v0_2",
        "status": "RESEARCH_CANDIDATE_NOT_ADMITTED",
        "projection_standing": "CURRENT_ONLY_FOR_EXACT_REPLAY_CLOSURE_NOT_DEFAULT_BRANCH",
        "replay_interval": copy.deepcopy(interval),
        "state_vector": copy.deepcopy(state),
        "state_vector_sha256": state_sha256(state),
        "currentness_by_dimension": currentness_summary(state),
        "applied_event_ids": [item["event_id"] for item in transitions],
        "transition_chain": copy.deepcopy(transitions),
        "source_contributions": [
            {
                "reducer_id": sequence_contribution.get("reducer_id"),
                "result": sequence_contribution.get("reducer_result"),
                "contributed_dimensions": ["execution_state"],
                "source": copy.deepcopy(sequence_contribution.get("source")),
            },
            {
                "reducer_id": "FORK_TEMPORAL_SUCCESSION_VALIDATOR_v0_1",
                "result": "PREDECESSOR_SURFACE_CONFORMS",
                "contributed_dimensions": [],
                "role": "PREDECESSOR_SURFACE_CONFORMANCE_ONLY",
            },
        ],
        "effects": copy.deepcopy(contract["expected_non_effects"]),
        "non_claims": [
            "A committed projection is a recomputable cache, not authority for its own conclusions.",
            "Review standing remains bound to the exact reviewed head.",
            "Current means current only for the exact replay closure.",
            "The projection does not establish event completeness outside its interval.",
            "The projection does not authorize admission, publication, merge, provider calls, retries, readiness, or execution.",
        ],
    }


def derive_transition_receipt(
    contract: dict[str, Any],
    registry: dict[str, Any],
    initial_state: dict[str, Any],
    final_state: dict[str, Any],
    transitions: list[dict[str, Any]],
) -> dict[str, Any]:
    dimensions = contract["dimensions"]
    return {
        "schema_version": "v0.1",
        "record_kind": "fork_standing_transition_receipt",
        "receipt_id": "FORK_STANDING_TRANSITION_PR90_REVIEW_SUCCESSION_v0_1",
        "from_coordinate": copy.deepcopy(contract["initial_coordinate"]),
        "to_coordinate": {
            "commit_sha": final_state["temporal_closure"]["commit_sha"],
            "tree_sha": final_state["temporal_closure"]["tree_sha"],
        },
        "before_state_sha256": state_sha256(initial_state),
        "after_state_sha256": state_sha256(final_state),
        "applied_events": copy.deepcopy(transitions),
        "dimension_deltas": {
            dimension: {
                "changed": initial_state[dimension] != final_state[dimension],
                "before_standing": initial_state[dimension].get("standing"),
                "after_standing": final_state[dimension].get("standing"),
            }
            for dimension in dimensions
        },
        "changed_dimensions": sorted(
            dimension
            for dimension in dimensions
            if initial_state[dimension] != final_state[dimension]
        ),
        "preserved_dimensions": sorted(
            dimension
            for dimension in dimensions
            if initial_state[dimension] == final_state[dimension]
        ),
        "effects": copy.deepcopy(contract["expected_non_effects"]),
        "result": "STANDING_TRANSITION_RECOMPUTED",
        "non_claims": [
            "The receipt does not admit either coordinate.",
            "The receipt does not transfer review standing to an unreviewed head.",
            "The receipt performs no provider call or Pair-001 repetition.",
        ],
    }


def validate_package_manifest(
    root: Path,
    findings: list[dict[str, str]],
) -> None:
    try:
        manifest = strict_load(safe_regular_file(root, MANIFEST.as_posix()))
    except Exception as exc:
        add_finding(findings, "PACKAGE_MANIFEST_INVALID", str(exc), MANIFEST.as_posix())
        return
    entries = manifest.get("entries", [])
    listed = {
        item.get("path")
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    if listed != EXPECTED_PACKAGE_PATHS:
        add_finding(
            findings,
            "PACKAGE_FILE_SET_MISMATCH",
            f"expected {sorted(EXPECTED_PACKAGE_PATHS)}, found {sorted(listed)}",
            MANIFEST.as_posix(),
        )
    if manifest.get("self_exclusion") != {
        "path": MANIFEST.as_posix(),
        "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
    }:
        add_finding(
            findings,
            "PACKAGE_MANIFEST_SELF_EXCLUSION_INVALID",
            "manifest self-exclusion must be explicit",
            MANIFEST.as_posix(),
        )
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        relative = entry.get("path")
        if relative in seen:
            add_finding(
                findings,
                "PACKAGE_DUPLICATE_PATH",
                "duplicate package entry",
                str(relative),
            )
            continue
        seen.add(relative)
        try:
            path = safe_regular_file(root, relative)
            if path.stat().st_size != entry.get("size_bytes"):
                add_finding(
                    findings,
                    "PACKAGE_SIZE_MISMATCH",
                    f"expected {entry.get('size_bytes')}, found {path.stat().st_size}",
                    str(relative),
                )
            if sha256_file(path) != entry.get("sha256"):
                add_finding(
                    findings,
                    "PACKAGE_DIGEST_MISMATCH",
                    "package entry digest differs",
                    str(relative),
                )
        except Exception as exc:
            add_finding(findings, "PACKAGE_DIGEST_MISMATCH", str(exc), str(relative))


def compare_cache(
    root: Path,
    relative: Path,
    derived: dict[str, Any],
    code: str,
    findings: list[dict[str, str]],
) -> None:
    try:
        committed = strict_load(safe_regular_file(root, relative.as_posix()))
    except Exception as exc:
        add_finding(findings, code, str(exc), relative.as_posix())
        return
    if committed != derived:
        add_finding(
            findings,
            code,
            "committed cache differs from deterministic recomputation",
            relative.as_posix(),
        )


def evaluate(
    root: Path,
    *,
    contract_override: dict[str, Any] | None = None,
    registry_override: dict[str, Any] | None = None,
    verify_committed: bool = True,
    as_of: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    try:
        contract = (
            copy.deepcopy(contract_override)
            if contract_override is not None
            else strict_load(safe_regular_file(root, CONTRACT.as_posix()))
        )
        registry = (
            copy.deepcopy(registry_override)
            if registry_override is not None
            else strict_load(safe_regular_file(root, REGISTRY.as_posix()))
        )
    except Exception as exc:
        add_finding(findings, "REPLAY_INPUT_INVALID", str(exc))
        return finish(findings, None, None, None)

    if not isinstance(contract, dict) or not isinstance(registry, dict):
        add_finding(findings, "REPLAY_INPUT_INVALID", "contract and registry must be objects")
        return finish(findings, None, None, None)

    validate_registry_schema(root, registry, findings)
    validate_evidence_refs(root, registry, findings)
    validate_predecessor_temporal_surface(root, findings)
    validate_state_route(root, contract, registry, findings)
    sequence_contribution = derive_sequence_contribution(root, findings)
    coverage, _ = derive_coverage_receipt(root, registry, findings)
    state, transitions, initial_state = replay(
        contract,
        registry,
        sequence_contribution,
        findings,
        as_of=as_of,
    )
    projection = derive_projection(
        contract,
        registry,
        state,
        transitions,
        sequence_contribution,
    )
    transition = derive_transition_receipt(
        contract,
        registry,
        initial_state,
        state,
        transitions,
    )

    if verify_committed and as_of is None:
        compare_cache(
            root,
            PROJECTION,
            projection,
            "PROJECTION_REDUCER_DIVERGENCE",
            findings,
        )
        compare_cache(
            root,
            COVERAGE,
            coverage,
            "EVENT_COVERAGE_RECEIPT_DIVERGENCE",
            findings,
        )
        compare_cache(
            root,
            TRANSITION,
            transition,
            "TRANSITION_RECEIPT_DIVERGENCE",
            findings,
        )
        validate_package_manifest(root, findings)

    return finish(findings, projection, coverage, transition)


def finish(
    findings: list[dict[str, str]],
    projection: dict[str, Any] | None,
    coverage: dict[str, Any] | None,
    transition: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "checker": TOOL_PATH.name,
        "status": (
            "LONGITUDINAL_STATE_REPRODUCED"
            if not findings
            else "LONGITUDINAL_RECOMPUTATION_INVALID"
        ),
        "finding_count": len(findings),
        "finding_codes": sorted({item["code"] for item in findings}),
        "findings": findings,
        "projection": projection,
        "coverage_receipt": coverage,
        "transition_receipt": transition,
        "effects": {
            "provider_calls": 0,
            "pair_001_calls": 0,
            "pair_001_repetitions": 0,
            "admission": "NONE",
            "authority": "NONE",
            "execution": "NONE",
        },
        "interpretation": {
            "proves": [
                "bounded Git-interval commit coverage",
                "evidence-byte bindings",
                "deterministic standing-vector replay",
                "per-dimension changed and preserved state",
                "exact-head review non-inheritance",
            ],
            "does_not_prove": [
                "semantic event completeness outside the interval",
                "truth",
                "correctness",
                "causality",
                "approval",
                "authority",
                "compliance",
                "legal sufficiency",
                "safety",
                "production readiness",
                "execution permission",
            ],
        },
    }


def build_package_manifest(root: Path) -> dict[str, Any]:
    entries = []
    for relative in sorted(EXPECTED_PACKAGE_PATHS):
        path = safe_regular_file(root, relative)
        entries.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "schema_version": "v0.2",
        "record_kind": "fork_longitudinal_recomputation_package_manifest",
        "package_id": "FORK_LONGITUDINAL_RECOMPUTATION_REPLAY_v0_2",
        "entries": entries,
        "self_exclusion": {
            "path": MANIFEST.as_posix(),
            "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
        },
        "non_claims": [
            "Package integrity is not admission, authority, correctness, or execution permission."
        ],
    }


def write_derived(root: Path) -> int:
    result = evaluate(root, verify_committed=False)
    if result["findings"]:
        print(pretty_json(result), end="")
        return 1
    outputs = {
        PROJECTION: result["projection"],
        COVERAGE: result["coverage_receipt"],
        TRANSITION: result["transition_receipt"],
    }
    for relative, value in outputs.items():
        path = root / relative
        path.write_text(pretty_json(value), encoding="utf-8", newline="\n")
    manifest = build_package_manifest(root)
    (root / MANIFEST).write_text(
        pretty_json(manifest),
        encoding="utf-8",
        newline="\n",
    )
    print("LONGITUDINAL_DERIVED_ARTIFACTS_WRITTEN")
    return 0


def state_diff(
    root: Path,
    from_commit: str,
    to_commit: str,
) -> dict[str, Any]:
    before = evaluate(root, verify_committed=False, as_of=from_commit)
    after = evaluate(root, verify_committed=False, as_of=to_commit)
    findings = [*before["findings"], *after["findings"]]
    if findings:
        return {
            "status": "LONGITUDINAL_DIFF_UNRESOLVED",
            "finding_count": len(findings),
            "findings": findings,
        }
    before_state = before["projection"]["state_vector"]
    after_state = after["projection"]["state_vector"]
    dimensions = sorted(before_state)
    return {
        "status": "LONGITUDINAL_DIFF_REPRODUCED",
        "from_commit": from_commit,
        "to_commit": to_commit,
        "changed_dimensions": [
            dimension
            for dimension in dimensions
            if before_state[dimension] != after_state[dimension]
        ],
        "preserved_dimensions": [
            dimension
            for dimension in dimensions
            if before_state[dimension] == after_state[dimension]
        ],
        "dimension_deltas": {
            dimension: {
                "before": before_state[dimension],
                "after": after_state[dimension],
            }
            for dimension in dimensions
            if before_state[dimension] != after_state[dimension]
        },
        "effects": {
            "provider_calls": 0,
            "pair_001_calls": 0,
            "admission": "NONE",
            "authority": "NONE",
            "execution": "NONE",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--derive-projection", action="store_true")
    parser.add_argument("--write-derived", action="store_true")
    parser.add_argument("--as-of")
    parser.add_argument("--diff-from")
    parser.add_argument("--diff-to")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()

    if bool(args.diff_from) != bool(args.diff_to):
        parser.error("--diff-from and --diff-to must be supplied together")
    if args.write_derived:
        return write_derived(root)
    if args.diff_from and args.diff_to:
        result = state_diff(root, args.diff_from, args.diff_to)
        print(pretty_json(result), end="")
        return 0 if result["status"] == "LONGITUDINAL_DIFF_REPRODUCED" else 1

    result = evaluate(
        root,
        verify_committed=not args.derive_projection and args.as_of is None,
        as_of=args.as_of,
    )
    if args.derive_projection or args.as_of is not None:
        print(pretty_json(result["projection"]), end="")
    elif args.json:
        print(pretty_json(result), end="")
    else:
        for finding in result["findings"]:
            print(f"[{finding['code']}] {finding['path']}: {finding['detail']}")
        print(result["status"])
    return 0 if not result["findings"] else 1


if __name__ == "__main__":
    sys.exit(main())
