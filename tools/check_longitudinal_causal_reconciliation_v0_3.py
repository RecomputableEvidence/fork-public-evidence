#!/usr/bin/env python3
"""Recompute frontier-bounded causal state and explicit merge reconciliation."""

from __future__ import annotations

import argparse
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BASE = Path("docs/state/longitudinal-recomputation-v0.3")
CONTRACT = BASE / "CAUSAL_RECONCILIATION_CONTRACT_v0_3.json"
REGISTRY = BASE / "CAUSAL_EVENT_REGISTRY_v0_3.json"
PROJECTION = BASE / "CAUSAL_CURRENT_PROJECTION_v0_3.json"
COVERAGE = BASE / "CAUSAL_FRONTIER_COVERAGE_RECEIPT_v0_1.json"
RECONCILIATION = BASE / "CAUSAL_RECONCILIATION_RECEIPT_v0_1.json"
MANIFEST = BASE / "PACKAGE_MANIFEST_v0_3.json"
ADVERSARIAL_CASES = BASE / "ADVERSARIAL_CASES_v0_3.json"
README = BASE / "README.md"
NON_CLAIMS = BASE / "NON_CLAIMS_AND_LIMITS_v0_3.md"
PREDECESSOR_CORRECTION = (
    BASE / "PREDECESSOR_PACKAGE_SCOPE_RECOMPUTATION_v0_1.md"
)
CLAIM_ADMISSION_RECOMPUTATION = (
    BASE / "CLAIM_ADMISSION_RECEIPT_RECOMPUTATION_v0_2.md"
)
SCHEMA = Path("schemas/fork_longitudinal_causal_registry_v0_3.schema.json")
STATE_ROUTE = Path("docs/state/FORK_STATE_ROUTING_v0_3.json")
STATE_README = Path("docs/state/README.md")
PREDECESSOR_CHECKER = Path("tools/check_longitudinal_recomputation_v0_2.py")
PREDECESSOR_MANIFEST = Path(
    "docs/state/longitudinal-recomputation-v0.2/PACKAGE_MANIFEST_v0_2_1.json"
)
TEST_PATH = Path("tests/test_longitudinal_causal_reconciliation_v0_3.py")
TOOL_PATH = Path("tools/check_longitudinal_causal_reconciliation_v0_3.py")

EXPECTED_PACKAGE_PATHS = {
    ADVERSARIAL_CASES.as_posix(),
    CLAIM_ADMISSION_RECOMPUTATION.as_posix(),
    CONTRACT.as_posix(),
    COVERAGE.as_posix(),
    NON_CLAIMS.as_posix(),
    PREDECESSOR_CORRECTION.as_posix(),
    PREDECESSOR_MANIFEST.as_posix(),
    PROJECTION.as_posix(),
    README.as_posix(),
    RECONCILIATION.as_posix(),
    REGISTRY.as_posix(),
    SCHEMA.as_posix(),
    STATE_ROUTE.as_posix(),
    TEST_PATH.as_posix(),
    TOOL_PATH.as_posix(),
}


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def predecessor(root: Path) -> Any:
    return load_module(
        root / PREDECESSOR_CHECKER,
        "fork_longitudinal_recomputation_v0_2_for_causal_v0_3",
    )


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


def parent_deltas(root: Path, commit: str, parents: list[str]) -> dict[str, list[str]]:
    return {
        parent: sorted(
            line.strip()
            for line in run_git(
                root,
                "diff",
                "--name-only",
                parent,
                commit,
            ).splitlines()
            if line.strip()
        )
        for parent in parents
    }


def git_metadata(root: Path, commit: str, base: Any) -> dict[str, Any]:
    metadata = base.git_commit_metadata(root, commit)
    metadata["parent_deltas"] = parent_deltas(
        root,
        commit,
        metadata["parent_commits"],
    )
    return metadata


def add_finding(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str = "",
) -> None:
    findings.append({"code": code, "detail": detail, "path": path})


def validate_schema(
    root: Path,
    registry: dict[str, Any],
    base: Any,
    findings: list[dict[str, str]],
) -> None:
    try:
        schema = base.strict_load(base.safe_regular_file(root, SCHEMA.as_posix()))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(registry), key=lambda item: list(item.path))
        for error in errors:
            location = "/".join(str(item) for item in error.path)
            add_finding(
                findings,
                "CAUSAL_SCHEMA_INVALID",
                error.message,
                f"{REGISTRY.as_posix()}:{location}",
            )
    except Exception as exc:
        add_finding(findings, "CAUSAL_SCHEMA_INVALID", str(exc), SCHEMA.as_posix())


def validate_predecessor(
    root: Path,
    base: Any,
    findings: list[dict[str, str]],
) -> None:
    try:
        result = base.evaluate(root)
    except Exception as exc:
        add_finding(
            findings,
            "PREDECESSOR_V0_2_INVALID",
            str(exc),
            PREDECESSOR_CHECKER.as_posix(),
        )
        return
    for item in result.get("findings", []):
        add_finding(
            findings,
            "PREDECESSOR_V0_2_INVALID",
            f"{item.get('code')}: {item.get('detail')}",
            item.get("path", PREDECESSOR_CHECKER.as_posix()),
        )


def frontier_inventory(
    root: Path,
    anchors: list[str],
    closure: str,
    base: Any,
) -> list[dict[str, Any]]:
    if not anchors:
        raise ValueError("frontier must contain at least one anchor")
    if len(set(anchors)) != len(anchors):
        raise ValueError("frontier anchors must be unique")
    if base.SHA1_RE.fullmatch(closure) is None:
        raise ValueError("closure must be a full lowercase commit SHA")
    for anchor in anchors:
        if base.SHA1_RE.fullmatch(anchor) is None:
            raise ValueError("frontier anchors must be full lowercase commit SHAs")
        check = subprocess.run(
            ["git", "merge-base", "--is-ancestor", anchor, closure],
            cwd=root,
            check=False,
            capture_output=True,
        )
        if check.returncode != 0:
            raise ValueError(f"frontier anchor is not an ancestor of closure: {anchor}")
    commits = [
        line.strip()
        for line in run_git(
            root,
            "rev-list",
            "--reverse",
            "--topo-order",
            closure,
            "--not",
            *anchors,
        ).splitlines()
        if line.strip()
    ]
    return [git_metadata(root, commit, base) for commit in commits]


def derive_coverage(
    root: Path,
    registry: dict[str, Any],
    base: Any,
    findings: list[dict[str, str]],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    frontier = registry.get("frontier", {})
    anchors = [
        item.get("commit_sha")
        for item in frontier.get("anchors", [])
        if isinstance(item, dict)
    ]
    closure = frontier.get("closure_commit_inclusive")
    try:
        inventory = frontier_inventory(root, anchors, closure, base)
    except Exception as exc:
        add_finding(
            findings,
            "CAUSAL_COVERAGE_UNRESOLVED",
            str(exc),
            REGISTRY.as_posix(),
        )
        inventory = []

    events = [item for item in registry.get("events", []) if isinstance(item, dict)]
    events_by_commit: dict[str, dict[str, Any]] = {}
    event_ids: set[str] = set()
    duplicates: list[str] = []
    for event in events:
        commit = event.get("source_commit")
        event_id = event.get("event_id")
        if commit in events_by_commit or event_id in event_ids:
            duplicates.append(f"{event_id}@{commit}")
        if isinstance(commit, str):
            events_by_commit[commit] = event
        if isinstance(event_id, str):
            event_ids.add(event_id)
    if duplicates:
        add_finding(
            findings,
            "CAUSAL_EVENT_DUPLICATE",
            f"duplicate event coordinates: {sorted(duplicates)}",
            REGISTRY.as_posix(),
        )

    inventory_by_commit = {item["commit_sha"]: item for item in inventory}
    unclassified = sorted(set(inventory_by_commit) - set(events_by_commit))
    outside = sorted(set(events_by_commit) - set(inventory_by_commit))
    if unclassified:
        add_finding(
            findings,
            "CAUSAL_COVERAGE_UNRESOLVED",
            f"unclassified frontier interval commits: {unclassified}",
            REGISTRY.as_posix(),
        )
    if outside:
        add_finding(
            findings,
            "CAUSAL_EVENT_OUTSIDE_FRONTIER",
            f"registered event commits outside frontier interval: {outside}",
            REGISTRY.as_posix(),
        )

    anchor_by_commit = {
        item.get("commit_sha"): item
        for item in frontier.get("anchors", [])
        if isinstance(item, dict)
    }
    for commit, anchor in anchor_by_commit.items():
        try:
            metadata = git_metadata(root, commit, base)
            if anchor.get("tree_sha") != metadata["tree_sha"]:
                add_finding(
                    findings,
                    "FRONTIER_GIT_BINDING_MISMATCH",
                    f"anchor tree expected {metadata['tree_sha']}, "
                    f"found {anchor.get('tree_sha')}",
                    str(commit),
                )
            expected_state_sha = base.state_sha256(anchor.get("state", {}))
            if anchor.get("state_sha256") != expected_state_sha:
                add_finding(
                    findings,
                    "FRONTIER_STATE_DIGEST_MISMATCH",
                    f"expected {expected_state_sha}, found {anchor.get('state_sha256')}",
                    str(commit),
                )
        except Exception as exc:
            add_finding(findings, "FRONTIER_INVALID", str(exc), str(commit))

    known_coordinates = set(anchor_by_commit) | set(inventory_by_commit)
    for commit in sorted(set(inventory_by_commit).intersection(events_by_commit)):
        metadata = inventory_by_commit[commit]
        event = events_by_commit[commit]
        comparisons = (
            ("source_tree", event.get("source_tree"), metadata["tree_sha"]),
            (
                "source_parent_commits",
                event.get("source_parent_commits"),
                metadata["parent_commits"],
            ),
            ("occurred_at_utc", event.get("occurred_at_utc"), metadata["committed_at_utc"]),
            ("subject", event.get("subject"), metadata["subject"]),
            ("parent_deltas", event.get("parent_deltas"), metadata["parent_deltas"]),
        )
        for label, actual, expected in comparisons:
            if actual != expected:
                add_finding(
                    findings,
                    "CAUSAL_EVENT_GIT_BINDING_MISMATCH",
                    f"{label}: expected {expected!r}, found {actual!r}",
                    str(event.get("event_id")),
                )
        unknown_parents = sorted(
            set(metadata["parent_commits"]) - known_coordinates
        )
        if unknown_parents:
            add_finding(
                findings,
                "EVENT_PARENT_OUTSIDE_FRONTIER",
                f"event has parents outside declared frontier: {unknown_parents}",
                str(event.get("event_id")),
            )

    receipt = {
        "schema_version": "v0.1",
        "record_kind": "fork_causal_frontier_coverage_receipt",
        "receipt_id": "FORK_CAUSAL_FRONTIER_COVERAGE_PR81_PR82_v0_1",
        "frontier": copy.deepcopy(frontier),
        "git_inventory": inventory,
        "commit_count": len(inventory),
        "classified_commit_count": len(
            set(inventory_by_commit).intersection(events_by_commit)
        ),
        "unclassified_commits": unclassified,
        "registered_commits_outside_frontier": outside,
        "result": (
            "FRONTIER_BOUNDED_CAUSAL_COVERAGE_REPRODUCED"
            if not unclassified and not outside and not duplicates
            else "CAUSAL_COVERAGE_UNRESOLVED"
        ),
        "interpretation": {
            "proves": [
                "every Git commit reachable from closure and not reachable from any frontier anchor is classified",
                "merge events bind per-parent path deltas instead of an empty combined merge diff",
            ],
            "does_not_prove": [
                "semantic event completeness outside the frontier",
                "correct semantic classification",
                "admission",
                "authority",
                "truth",
                "execution permission",
            ],
        },
    }
    return receipt, inventory_by_commit


def validate_effect_boundary(
    event: dict[str, Any],
    parent_states: list[dict[str, Any]],
    result_state: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    event_id = str(event.get("event_id"))
    boundaries = (
        ("admission_state", "admission_effect", "ADMISSION_EFFECT_MISMATCH"),
        ("authority_state", "authority_effect", "AUTHORITY_EFFECT_MISMATCH"),
        ("execution_state", "execution_effect", "EXECUTION_EFFECT_MISMATCH"),
    )
    for dimension, field, code in boundaries:
        changed = any(
            parent.get(dimension) != result_state.get(dimension)
            for parent in parent_states
        )
        declared = event.get(field)
        if changed and declared == "NONE":
            add_finding(
                findings,
                code,
                f"{dimension} changed while {field}=NONE",
                event_id,
            )
        if not changed and declared != "NONE":
            add_finding(
                findings,
                code,
                f"{field}={declared!r} without a {dimension} change",
                event_id,
            )


def apply_single_parent_event(
    event: dict[str, Any],
    parent_state: dict[str, Any],
    dimensions: list[str],
    base: Any,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    event_id = str(event.get("event_id"))
    result = copy.deepcopy(parent_state)
    decisions = event.get("reconciliation_decisions", {})
    if decisions:
        add_finding(
            findings,
            "SINGLE_PARENT_RECONCILIATION_DECLARED",
            "single-parent events must use dimension effects, not merge decisions",
            event_id,
        )
    effects = event.get("dimension_effects", {})
    unknown = sorted(set(effects) - set(dimensions))
    if unknown:
        add_finding(
            findings,
            "UNDECLARED_DIMENSION_CHANGE",
            f"unknown dimensions: {unknown}",
            event_id,
        )
    for dimension, effect in effects.items():
        if dimension not in dimensions or not isinstance(effect, dict):
            continue
        if effect.get("operation") != "REPLACE":
            add_finding(
                findings,
                "DIMENSION_OPERATION_INVALID",
                f"{dimension} operation must be REPLACE",
                event_id,
            )
            continue
        before_sha = base.state_sha256(parent_state[dimension])
        if effect.get("before_sha256") != before_sha:
            add_finding(
                findings,
                "DIMENSION_PRECONDITION_MISMATCH",
                f"{dimension}: expected before digest {before_sha}, "
                f"found {effect.get('before_sha256')}",
                event_id,
            )
        result[dimension] = copy.deepcopy(effect.get("after"))
        if result[dimension] == parent_state[dimension]:
            add_finding(
                findings,
                "REDUNDANT_DIMENSION_EFFECT",
                f"{dimension} declared changed but remained equal",
                event_id,
            )
    return result


def apply_merge_event(
    event: dict[str, Any],
    parents: list[str],
    states: dict[str, dict[str, Any]],
    dimensions: list[str],
    base: Any,
    findings: list[dict[str, str]],
) -> dict[str, Any]:
    event_id = str(event.get("event_id"))
    if event.get("dimension_effects"):
        add_finding(
            findings,
            "MERGE_EFFECTS_NOT_RECONCILIATION",
            "multi-parent events must use reconciliation decisions",
            event_id,
        )
    decisions = event.get("reconciliation_decisions", {})
    missing = sorted(set(dimensions) - set(decisions))
    unknown = sorted(set(decisions) - set(dimensions))
    if missing:
        add_finding(
            findings,
            "MERGE_DECISION_MISSING",
            f"missing per-dimension decisions: {missing}",
            event_id,
        )
    if unknown:
        add_finding(
            findings,
            "UNDECLARED_DIMENSION_CHANGE",
            f"unknown merge dimensions: {unknown}",
            event_id,
        )
    result: dict[str, Any] = {}
    for dimension in dimensions:
        decision = decisions.get(dimension)
        parent_values = {parent: states[parent][dimension] for parent in parents}
        parent_hashes = {
            parent: base.state_sha256(value)
            for parent, value in parent_values.items()
        }
        if not isinstance(decision, dict):
            result[dimension] = copy.deepcopy(parent_values[parents[0]])
            continue
        if decision.get("parent_state_sha256") != parent_hashes:
            add_finding(
                findings,
                "MERGE_INPUT_DIGEST_MISMATCH",
                f"{dimension}: expected {parent_hashes!r}, "
                f"found {decision.get('parent_state_sha256')!r}",
                event_id,
            )
        rationale = decision.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            add_finding(
                findings,
                "MERGE_RATIONALE_MISSING",
                f"{dimension} lacks a non-empty rationale",
                event_id,
            )
        policy = decision.get("policy")
        output = copy.deepcopy(decision.get("result"))
        values = list(parent_values.values())
        if policy == "REQUIRE_EQUAL":
            if any(value != values[0] for value in values[1:]):
                add_finding(
                    findings,
                    "MERGE_EQUALITY_VIOLATION",
                    f"{dimension} parent states differ under REQUIRE_EQUAL",
                    event_id,
                )
            if output != values[0]:
                add_finding(
                    findings,
                    "MERGE_RESULT_MISMATCH",
                    f"{dimension} output differs from equal parent state",
                    event_id,
                )
        elif policy == "SELECT_PARENT":
            selected = decision.get("selected_parent")
            if selected not in parent_values:
                add_finding(
                    findings,
                    "MERGE_SELECTED_PARENT_INVALID",
                    f"{dimension} selected unknown parent {selected!r}",
                    event_id,
                )
            elif output != parent_values[selected]:
                add_finding(
                    findings,
                    "MERGE_RESULT_MISMATCH",
                    f"{dimension} output differs from selected parent",
                    event_id,
                )
        elif policy == "EXPLICIT_JOIN":
            if all(value == values[0] for value in values[1:]):
                add_finding(
                    findings,
                    "MERGE_POLICY_OVERBROAD",
                    f"{dimension} uses EXPLICIT_JOIN for equal inputs",
                    event_id,
                )
        else:
            add_finding(
                findings,
                "MERGE_POLICY_INVALID",
                f"{dimension} has unsupported policy {policy!r}",
                event_id,
            )
        if decision.get("result_sha256") != base.state_sha256(output):
            add_finding(
                findings,
                "MERGE_RESULT_DIGEST_MISMATCH",
                f"{dimension} result digest does not bind result bytes",
                event_id,
            )
        result[dimension] = output
    return result


def replay(
    contract: dict[str, Any],
    registry: dict[str, Any],
    base: Any,
    findings: list[dict[str, str]],
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, str],
    list[dict[str, Any]],
    list[str],
]:
    dimensions = contract.get("dimensions", [])
    if len(set(dimensions)) != len(dimensions) or not dimensions:
        add_finding(
            findings,
            "CONTRACT_DIMENSIONS_INVALID",
            "dimensions must be a non-empty unique list",
            CONTRACT.as_posix(),
        )
    states: dict[str, dict[str, Any]] = {}
    node_digests: dict[str, str] = {}
    frontier = registry.get("frontier", {})
    for anchor in frontier.get("anchors", []):
        if not isinstance(anchor, dict):
            continue
        commit = anchor.get("commit_sha")
        state = copy.deepcopy(anchor.get("state", {}))
        if set(state) != set(dimensions):
            add_finding(
                findings,
                "FRONTIER_STATE_DIMENSIONS_INVALID",
                f"expected {sorted(dimensions)}, found {sorted(state)}",
                str(commit),
            )
        if isinstance(commit, str):
            states[commit] = state
            node_digests[commit] = base.sha256_bytes(
                base.canonical_json_bytes(
                    {
                        "coordinate": commit,
                        "tree_sha": anchor.get("tree_sha"),
                        "state_sha256": base.state_sha256(state),
                        "kind": "FRONTIER_ANCHOR",
                    }
                )
            )

    pending = {
        event.get("source_commit"): event
        for event in registry.get("events", [])
        if isinstance(event, dict) and isinstance(event.get("source_commit"), str)
    }
    transitions: list[dict[str, Any]] = []
    causal_order: list[str] = []
    while pending:
        ready = sorted(
            commit
            for commit, event in pending.items()
            if all(parent in states for parent in event.get("source_parent_commits", []))
        )
        if not ready:
            unresolved = {
                commit: event.get("source_parent_commits", [])
                for commit, event in sorted(pending.items())
            }
            add_finding(
                findings,
                "CAUSAL_CYCLE_OR_GAP",
                f"no event is causally ready: {unresolved}",
                REGISTRY.as_posix(),
            )
            break
        for commit in ready:
            event = pending.pop(commit)
            parents = event.get("source_parent_commits", [])
            if not parents:
                add_finding(
                    findings,
                    "EVENT_PARENT_OUTSIDE_FRONTIER",
                    "events inside the frontier interval require a known parent",
                    str(event.get("event_id")),
                )
                continue
            parent_states = [states[parent] for parent in parents]
            if len(parents) == 1:
                result_state = apply_single_parent_event(
                    event,
                    parent_states[0],
                    dimensions,
                    base,
                    findings,
                )
            else:
                result_state = apply_merge_event(
                    event,
                    parents,
                    states,
                    dimensions,
                    base,
                    findings,
                )
            validate_effect_boundary(event, parent_states, result_state, findings)
            state_sha = base.state_sha256(result_state)
            node_digest = base.sha256_bytes(
                base.canonical_json_bytes(
                    {
                        "coordinate": commit,
                        "tree_sha": event.get("source_tree"),
                        "parents": {
                            parent: node_digests[parent] for parent in parents
                        },
                        "state_sha256": state_sha,
                        "dimension_effects": event.get("dimension_effects", {}),
                        "reconciliation_decisions": event.get(
                            "reconciliation_decisions",
                            {},
                        ),
                    }
                )
            )
            states[commit] = result_state
            node_digests[commit] = node_digest
            causal_order.append(commit)
            transitions.append(
                {
                    "event_id": event.get("event_id"),
                    "source_commit": commit,
                    "parent_commits": copy.deepcopy(parents),
                    "event_kind": event.get("event_kind"),
                    "state_sha256": state_sha,
                    "node_digest_sha256": node_digest,
                    "reconciliation_kind": (
                        "MULTI_PARENT_EXPLICIT"
                        if len(parents) > 1
                        else "SINGLE_PARENT_EFFECT"
                    ),
                    "dimension_effects": copy.deepcopy(
                        event.get("dimension_effects", {})
                    ),
                    "reconciliation_decisions": copy.deepcopy(
                        event.get("reconciliation_decisions", {})
                    ),
                }
            )
    return states, node_digests, transitions, causal_order


def active_heads(registry: dict[str, Any]) -> list[str]:
    event_commits = {
        item.get("source_commit")
        for item in registry.get("events", [])
        if isinstance(item, dict)
    }
    consumed = {
        parent
        for item in registry.get("events", [])
        if isinstance(item, dict)
        for parent in item.get("source_parent_commits", [])
        if parent in event_commits
    }
    return sorted(event_commits - consumed)


def derive_projection(
    contract: dict[str, Any],
    registry: dict[str, Any],
    states: dict[str, dict[str, Any]],
    node_digests: dict[str, str],
    transitions: list[dict[str, Any]],
    causal_order: list[str],
    base: Any,
) -> dict[str, Any]:
    closure = registry["frontier"]["closure_commit_inclusive"]
    state = copy.deepcopy(states.get(closure, {}))
    return {
        "schema_version": "v0.3",
        "record_kind": "fork_longitudinal_causal_projection",
        "projection_id": "FORK_CAUSAL_RECONCILIATION_PR81_PR82_v0_3",
        "projection_standing": (
            "CURRENT_ONLY_FOR_EXACT_CAUSAL_FRONTIER_CLOSURE_"
            "RESEARCH_CANDIDATE_NOT_ADMITTED"
        ),
        "frontier": copy.deepcopy(registry["frontier"]),
        "causal_order": causal_order,
        "applied_event_ids": [item["event_id"] for item in transitions],
        "coordinate_state_sha256": {
            coordinate: base.state_sha256(value)
            for coordinate, value in sorted(states.items())
        },
        "coordinate_node_digest_sha256": dict(sorted(node_digests.items())),
        "active_event_heads": active_heads(registry),
        "closure_coordinate": closure,
        "closure_node_digest_sha256": node_digests.get(closure),
        "state_vector": state,
        "state_vector_sha256": base.state_sha256(state),
        "effects": copy.deepcopy(contract["expected_non_effects"]),
        "non_claims": [
            "A deterministic causal join is not admission, authority, truth, or execution permission.",
            "The committed projection is a cache; the frontier, Git objects, and reducer decisions are recomputed.",
            "Coverage is bounded to commits reachable from closure but not reachable from the declared frontier anchors.",
            "No review standing, authority, or execution permission inherits through a merge.",
        ],
    }


def derive_reconciliation_receipt(
    registry: dict[str, Any],
    transitions: list[dict[str, Any]],
) -> dict[str, Any]:
    merge_events = [
        item
        for item in transitions
        if item["reconciliation_kind"] == "MULTI_PARENT_EXPLICIT"
    ]
    return {
        "schema_version": "v0.1",
        "record_kind": "fork_causal_reconciliation_receipt",
        "receipt_id": "FORK_CAUSAL_RECONCILIATION_PR81_PR82_v0_1",
        "frontier": copy.deepcopy(registry["frontier"]),
        "merge_event_count": len(merge_events),
        "merge_events": merge_events,
        "active_event_heads": active_heads(registry),
        "result": (
            "EXPLICIT_CAUSAL_RECONCILIATION_REPRODUCED"
            if active_heads(registry)
            == [registry["frontier"]["closure_commit_inclusive"]]
            else "CAUSAL_RECONCILIATION_UNRESOLVED"
        ),
        "non_claims": [
            "Explicit reconciliation records how declared state dimensions join; it does not prove the semantic classification correct.",
            "A Git merge does not itself confer admission, authority, review, or execution standing.",
        ],
    }


def validate_route(
    root: Path,
    registry: dict[str, Any],
    base: Any,
    findings: list[dict[str, str]],
) -> None:
    try:
        route = base.strict_load(base.safe_regular_file(root, STATE_ROUTE.as_posix()))
        predecessor_route = base.strict_load(
            base.safe_regular_file(root, "docs/state/FORK_STATE_ROUTING_v0_2.json")
        )
        readme = base.safe_regular_file(root, STATE_README.as_posix()).read_text(
            encoding="utf-8"
        )
    except Exception as exc:
        add_finding(findings, "STATE_ROUTE_INVALID", str(exc), STATE_ROUTE.as_posix())
        return
    for field in ("historical_projection", "governed_projection"):
        if route.get(field) != predecessor_route.get(field):
            add_finding(
                findings,
                "STATE_ROUTE_INVALID",
                f"{field} diverges from preserved v0.2 routing",
                STATE_ROUTE.as_posix(),
            )
    expected_predecessor = {
        "path": (
            "docs/state/longitudinal-recomputation-v0.2/"
            "LONGITUDINAL_CURRENT_PROJECTION_v0_2.json"
        ),
        "standing": "RESEARCH_PREDECESSOR_CANDIDATE_NOT_ADMITTED",
    }
    if route.get("linear_replay_predecessor") != expected_predecessor:
        add_finding(
            findings,
            "STATE_ROUTE_INVALID",
            "linear_replay_predecessor does not identify v0.2",
            STATE_ROUTE.as_posix(),
        )
    expected_candidate = {
        "path": PROJECTION.as_posix(),
        "frontier_anchor_commits": sorted(
            item["commit_sha"] for item in registry["frontier"]["anchors"]
        ),
        "closure_commit": registry["frontier"]["closure_commit_inclusive"],
        "standing": "RESEARCH_CANDIDATE_NOT_ADMITTED",
    }
    if route.get("causal_reconciliation_candidate") != expected_candidate:
        add_finding(
            findings,
            "STATE_ROUTE_INVALID",
            f"causal candidate expected {expected_candidate!r}",
            STATE_ROUTE.as_posix(),
        )
    for required in (
        STATE_ROUTE.as_posix(),
        expected_predecessor["path"].removeprefix("docs/state/"),
        expected_candidate["path"].removeprefix("docs/state/"),
    ):
        if required not in readme:
            add_finding(
                findings,
                "STATE_ROUTE_README_DIVERGENCE",
                f"state README does not route to {required}",
                STATE_README.as_posix(),
            )


def compare_cache(
    root: Path,
    relative: Path,
    derived: dict[str, Any],
    code: str,
    base: Any,
    findings: list[dict[str, str]],
) -> None:
    try:
        committed = base.strict_load(base.safe_regular_file(root, relative.as_posix()))
    except Exception as exc:
        add_finding(findings, code, str(exc), relative.as_posix())
        return
    if committed != derived:
        add_finding(
            findings,
            code,
            "committed cache differs from deterministic causal recomputation",
            relative.as_posix(),
        )


def build_manifest(root: Path, base: Any) -> dict[str, Any]:
    entries = []
    for relative in sorted(EXPECTED_PACKAGE_PATHS):
        path = base.safe_regular_file(root, relative)
        entries.append(
            {
                "path": relative,
                "sha256": base.sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "schema_version": "v0.3",
        "record_kind": "fork_longitudinal_causal_package_manifest",
        "package_id": "FORK_LONGITUDINAL_CAUSAL_RECONCILIATION_v0_3",
        "entries": entries,
        "self_exclusion": {
            "path": MANIFEST.as_posix(),
            "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
        },
        "external_moving_dependencies_not_package_members": [
            {
                "path": STATE_README.as_posix(),
                "reason": "SHARED_FRONT_DOOR_ACCUMULATES_SUCCESSOR_ROUTES",
            },
            {
                "path": (
                    "receipts/claim-admission/"
                    "FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json"
                ),
                "reason": "GLOBAL_SELF_CHECK_RECEIPT_CHANGES_WITH_SUCCESSOR_TREE_INVENTORY",
            },
        ],
        "non_claims": [
            "Package integrity is not admission, authority, correctness, or execution permission."
        ],
    }


def validate_manifest(
    root: Path,
    base: Any,
    findings: list[dict[str, str]],
) -> None:
    try:
        committed = base.strict_load(base.safe_regular_file(root, MANIFEST.as_posix()))
        derived = build_manifest(root, base)
    except Exception as exc:
        add_finding(findings, "PACKAGE_MANIFEST_INVALID", str(exc), MANIFEST.as_posix())
        return
    if committed != derived:
        add_finding(
            findings,
            "PACKAGE_MANIFEST_DIVERGENCE",
            "committed package manifest differs from current versioned package bytes",
            MANIFEST.as_posix(),
        )


def finish(
    findings: list[dict[str, str]],
    projection: dict[str, Any] | None,
    coverage: dict[str, Any] | None,
    reconciliation: dict[str, Any] | None,
    coordinate_states: dict[str, dict[str, Any]] | None,
) -> dict[str, Any]:
    ordered = sorted(
        findings,
        key=lambda item: (item["code"], item["path"], item["detail"]),
    )
    return {
        "status": (
            "CAUSAL_RECONCILIATION_REPRODUCED"
            if not ordered
            else "CAUSAL_RECONCILIATION_UNRESOLVED"
        ),
        "ok": not ordered,
        "finding_codes": sorted({item["code"] for item in ordered}),
        "findings": ordered,
        "projection": projection,
        "coverage_receipt": coverage,
        "reconciliation_receipt": reconciliation,
        "coordinate_states": coordinate_states,
        "execution_effects": {
            "provider_calls": 0,
            "pair_001_calls": 0,
            "pair_001_repetitions": 0,
            "readiness": "NONE",
            "retry_authorization": "NONE",
            "execution_authority": "NONE",
            "admission": "NONE",
        },
    }


def evaluate(
    root: Path,
    *,
    contract_override: dict[str, Any] | None = None,
    registry_override: dict[str, Any] | None = None,
    verify_committed: bool = True,
    verify_predecessor: bool = True,
) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    try:
        base = predecessor(root)
        contract = (
            copy.deepcopy(contract_override)
            if contract_override is not None
            else base.strict_load(base.safe_regular_file(root, CONTRACT.as_posix()))
        )
        registry = (
            copy.deepcopy(registry_override)
            if registry_override is not None
            else base.strict_load(base.safe_regular_file(root, REGISTRY.as_posix()))
        )
    except Exception as exc:
        add_finding(findings, "CAUSAL_INPUT_INVALID", str(exc))
        return finish(findings, None, None, None, None)
    if not isinstance(contract, dict) or not isinstance(registry, dict):
        add_finding(
            findings,
            "CAUSAL_INPUT_INVALID",
            "contract and registry must be objects",
        )
        return finish(findings, None, None, None, None)

    validate_schema(root, registry, base, findings)
    if verify_predecessor:
        validate_predecessor(root, base, findings)
    coverage, _ = derive_coverage(root, registry, base, findings)
    states, node_digests, transitions, causal_order = replay(
        contract,
        registry,
        base,
        findings,
    )
    projection = derive_projection(
        contract,
        registry,
        states,
        node_digests,
        transitions,
        causal_order,
        base,
    )
    reconciliation = derive_reconciliation_receipt(registry, transitions)
    closure = registry.get("frontier", {}).get("closure_commit_inclusive")
    if active_heads(registry) != [closure]:
        add_finding(
            findings,
            "CAUSAL_HEADS_UNRECONCILED",
            f"expected closure-only head {closure}, found {active_heads(registry)}",
            REGISTRY.as_posix(),
        )
    validate_route(root, registry, base, findings)
    if verify_committed:
        compare_cache(
            root,
            PROJECTION,
            projection,
            "PROJECTION_CACHE_DIVERGENCE",
            base,
            findings,
        )
        compare_cache(
            root,
            COVERAGE,
            coverage,
            "COVERAGE_CACHE_DIVERGENCE",
            base,
            findings,
        )
        compare_cache(
            root,
            RECONCILIATION,
            reconciliation,
            "RECONCILIATION_CACHE_DIVERGENCE",
            base,
            findings,
        )
        validate_manifest(root, base, findings)
    return finish(findings, projection, coverage, reconciliation, states)


def causal_diff(root: Path, left: str, right: str) -> dict[str, Any]:
    result = evaluate(root, verify_committed=False)
    states = result.get("coordinate_states") or {}
    if left not in states or right not in states:
        return {
            "status": "CAUSAL_DIFF_UNRESOLVED",
            "missing_coordinates": sorted(
                coordinate for coordinate in (left, right) if coordinate not in states
            ),
        }
    left_state = states[left]
    right_state = states[right]
    dimensions = sorted(set(left_state) | set(right_state))
    changed = [
        dimension
        for dimension in dimensions
        if left_state.get(dimension) != right_state.get(dimension)
    ]
    return {
        "status": "CAUSAL_DIFF_REPRODUCED",
        "left": left,
        "right": right,
        "divergent_dimensions": changed,
        "equal_dimensions": [
            dimension for dimension in dimensions if dimension not in changed
        ],
        "changes": {
            dimension: {
                "left": left_state.get(dimension),
                "right": right_state.get(dimension),
            }
            for dimension in changed
        },
    }


def write_derived(root: Path) -> int:
    result = evaluate(
        root,
        verify_committed=False,
        verify_predecessor=True,
    )
    if result["findings"]:
        base = predecessor(root.resolve())
        print(base.pretty_json(result), end="")
        return 1
    base = predecessor(root.resolve())
    outputs = {
        PROJECTION: result["projection"],
        COVERAGE: result["coverage_receipt"],
        RECONCILIATION: result["reconciliation_receipt"],
    }
    for relative, value in outputs.items():
        (root / relative).write_text(
            base.pretty_json(value),
            encoding="utf-8",
            newline="\n",
        )
    (root / MANIFEST).write_text(
        base.pretty_json(build_manifest(root, base)),
        encoding="utf-8",
        newline="\n",
    )
    print("CAUSAL_RECONCILIATION_DERIVED_ARTIFACTS_WRITTEN")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--write-derived", action="store_true")
    parser.add_argument("--coordinate")
    parser.add_argument("--compare-left")
    parser.add_argument("--compare-right")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if bool(args.compare_left) != bool(args.compare_right):
        parser.error("--compare-left and --compare-right must be supplied together")
    if args.write_derived:
        return write_derived(root)
    base = predecessor(root)
    if args.compare_left and args.compare_right:
        print(base.pretty_json(causal_diff(root, args.compare_left, args.compare_right)), end="")
        return 0
    result = evaluate(root)
    if args.coordinate:
        state = (result.get("coordinate_states") or {}).get(args.coordinate)
        if state is None:
            print(
                base.pretty_json(
                    {
                        "status": "CAUSAL_COORDINATE_UNRESOLVED",
                        "coordinate": args.coordinate,
                    }
                ),
                end="",
            )
            return 1
        print(base.pretty_json(state), end="")
        return 0
    if result["ok"]:
        print("CAUSAL_RECONCILIATION_REPRODUCED")
        return 0
    print(base.pretty_json(result), end="")
    return 1


if __name__ == "__main__":
    sys.exit(main())
