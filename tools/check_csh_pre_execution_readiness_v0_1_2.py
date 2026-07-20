#!/usr/bin/env python3
"""Verify the frozen CSH input context and fail closed at the execution boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


BASE = Path("docs/experiments/cross-system-claim-handoff-v0.1")
BINDING = BASE / "pre-execution" / "PRE_EXECUTION_BINDING_v0_1_2.json"
ANCHOR = BASE / "pre-execution" / "INSTRUMENTATION_RELEASE_ANCHOR_v0_1_2.json"
MANIFEST = BASE / "EXPERIMENT_MANIFEST_v0_1.json"
RUN_ORDER = BASE / "prompts" / "RUN_ORDER_v0_1.json"
STATE = BASE / "execution-state" / "PAIR-001_EXECUTION_STATE_v0_1_1.json"
PROVENANCE = BASE / "amendments" / "CSH-AMEND-003" / "WORKFLOW_SUCCESSOR_PROVENANCE_v0_1_2.json"
AMENDMENT = BASE / "amendments" / "CSH-AMEND-003" / "CSH-AMEND-003_v0_1_2.json"

EXPECTED_HYPOTHESIS = {
    "expression": "E[U | H = 1] < E[U | H = 0]",
    "u_definition": "unsupported-inheritance events per receiver run",
    "h_definition": "presence of explicit Fork handoff-state artifact",
}
EXPECTED_PREREQUISITES = {
    "PRESERVATION_PR_61_ADMITTED",
    "CLAIM_ADMISSION_PR_62_ADMITTED",
    "CSH_AMENDMENT_PR_ADMITTED",
    "INSTRUMENTATION_RELEASE_ANCHOR_PUBLISHED",
    "PROVIDER_IDENTITY_CREDENTIAL_SCOPE_QUOTA_AND_RECEIPT_PATH_VALIDATED",
}
PUBLISHED_PHASE = "instrumentation_repair_published_execution_blocked_provider_validation"
PATCH_COMMIT = "1ab4316b5de6100674695912a077b168cc36651b"
PATCH_HEAD = "82c34252d7b8d9e8957fb5a86500e12da6cf363a"
PATCH_CI = {
    29556486787: "Fork Evidence CI",
    29556486800: "Cross-System Claim Handoff v0.1",
    29556486836: "Fork Proof-Surface Integration",
}
ANCHOR_COMMIT = "b877a4e455429f5c30f78219d6c8f767c744cfba"
ANCHOR_HEAD = "2e41242d87e4c1914f0859b4261d8587c6bfedaa"
ANCHOR_CI = {
    29677346156: "Fork Evidence CI",
    29677346126: "Cross-System Claim Handoff v0.1",
    29677346129: "Fork Proof-Surface Integration",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("Repository root not found")


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate(root: Path) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    required = [BINDING, ANCHOR, MANIFEST, RUN_ORDER, STATE, PROVENANCE, AMENDMENT]
    missing = [path.as_posix() for path in required if not (root / path).is_file()]
    record("required_surface", not missing, "present" if not missing else "; ".join(missing))
    if missing:
        return finish(checks, executable=False, prerequisites={})

    try:
        binding = load(root / BINDING)
        anchor = load(root / ANCHOR)
        manifest = load(root / MANIFEST)
        run_order = load(root / RUN_ORDER)
        state = load(root / STATE)
        provenance = load(root / PROVENANCE)
        amendment = load(root / AMENDMENT)
    except (OSError, json.JSONDecodeError, DuplicateKeyError) as exc:
        record("strict_json", False, str(exc))
        return finish(checks, executable=False, prerequisites={})
    record("strict_json", True, "all control records parse without duplicate keys")

    identity_ok = (
        binding.get("binding_id") == "CSH_PRE_EXECUTION_BINDING_v0_1_2"
        and binding.get("experiment_id") == "cross_system_claim_handoff_v0_1"
        and binding.get("amendment_id") == "CSH-AMEND-003"
        and amendment.get("status") == "proposed_not_admitted"
        and provenance.get("amendment_id") == "CSH-AMEND-003"
    )
    record("control_identity", identity_ok, "v0.1.2 controls bound" if identity_ok else "control identity mismatch")

    hypothesis_ok = binding.get("bound_hypothesis") == EXPECTED_HYPOTHESIS and manifest.get("hypothesis") == EXPECTED_HYPOTHESIS
    record("predetermined_hypothesis", hypothesis_ok, EXPECTED_HYPOTHESIS["expression"] if hypothesis_ok else "hypothesis mismatch")

    design = binding.get("design", {})
    units = run_order.get("units", [])
    pair_ordinals = {item.get("pair_block_ordinal") for item in units if isinstance(item, dict)}
    design_ok = (
        manifest.get("status") == "frozen_not_executed"
        and design.get("scenario_count") == 6
        and design.get("conditions") == ["control_h0", "instrumented_h1"]
        and design.get("receiver_classes") == ["llm_receiver_a", "llm_receiver_b", "deterministic_receiver"]
        and design.get("replicates_per_cell") == 3
        and design.get("planned_run_units") == 108
        and design.get("pair_blocks") == 54
        and len(units) == 108
        and pair_ordinals == set(range(1, 55))
        and [item.get("ordinal") for item in units] == list(range(1, 109))
    )
    record("frozen_design_and_order", design_ok, "108 units in 54 fixed pairs" if design_ok else "design or fixed-order mismatch")

    digest_errors: list[str] = []
    for item in binding.get("immutable_artifact_bindings", []):
        if not isinstance(item, dict):
            digest_errors.append("non-mapping binding")
            continue
        relative = item.get("path")
        path = root / str(relative)
        if not path.is_file():
            digest_errors.append(f"missing {relative}")
        elif sha256(path) != item.get("sha256"):
            digest_errors.append(f"digest mismatch {relative}")
    record("immutable_input_digests", not digest_errors, "verified" if not digest_errors else "; ".join(digest_errors))

    first_bound = binding.get("affected_pair_001", {}).get("first_units", [])
    first_ordered = units[:2]
    pair_errors: list[str] = []
    for index, bound in enumerate(first_bound):
        if index >= len(first_ordered):
            pair_errors.append(f"missing run-order unit {index + 1}")
            continue
        ordered = first_ordered[index]
        for key in ("ordinal", "planned_run_id", "condition", "receiver_class_id", "replicate_id"):
            if bound.get(key) != ordered.get(key):
                pair_errors.append(f"unit {index + 1} {key} mismatch")
        request_path = root / BASE / "receipts" / "baseline" / "pair-001" / str(bound.get("planned_run_id")) / "exact-request.json"
        if not request_path.is_file() or sha256(request_path) != bound.get("exact_request_sha256"):
            pair_errors.append(f"unit {index + 1} exact-request mismatch")
    if len(first_bound) != 2:
        pair_errors.append("exactly two Pair-001 units must be bound")
    record("pair_001_exact_request_lineage", not pair_errors, "byte-bound" if not pair_errors else "; ".join(pair_errors))

    publication = state.get("publication", {})
    patch_ci = publication.get("patch_ci", [])
    anchor_ci = publication.get("anchor_ci", [])

    def ci_records_match(records: Any, *, scope: str, head: str, expected: dict[int, str]) -> bool:
        if not isinstance(records, list) or len(records) != len(expected):
            return False
        actual: dict[int, str] = {}
        for item in records:
            if (
                not isinstance(item, dict)
                or item.get("scope") != scope
                or item.get("head_commit") != head
                or item.get("conclusion") != "success"
                or not isinstance(item.get("run_id"), int)
                or not isinstance(item.get("workflow"), str)
            ):
                return False
            actual[item["run_id"]] = item["workflow"]
        return actual == expected

    publication_ok = (
        state.get("current_phase") == PUBLISHED_PHASE
        and publication.get("status") == "anchor_ci_green"
        and publication.get("patch_commit") == anchor.get("admitted_commit") == PATCH_COMMIT
        and ci_records_match(patch_ci, scope="PR_63_REVIEWED_HEAD", head=PATCH_HEAD, expected=PATCH_CI)
        and publication.get("anchor_commit") == ANCHOR_COMMIT
        and ci_records_match(anchor_ci, scope="PR_70_RELEASE_ANCHOR_HEAD", head=ANCHOR_HEAD, expected=ANCHOR_CI)
    )
    record(
        "publication_state_reconciled",
        publication_ok,
        "anchor-ci-green state is bound to admitted patch, published release anchor, and successful checks"
        if publication_ok
        else "publication state does not match the published release anchor",
    )

    transitions = state.get("transitions", [])
    transition_by_id = {
        item.get("transition_id"): item
        for item in transitions
        if isinstance(item, dict) and isinstance(item.get("transition_id"), str)
    }
    publication_transition = transition_by_id.get("CSH-TRANSITION-AMEND-003-PUBLISH", {})
    transition_ok = (
        len(transitions) == 2
        and transition_by_id.get("CSH-TRANSITION-AMEND-002-INSTALL", {}).get("to_phase")
        == "instrumentation_repair_installed_not_published"
        and publication_transition.get("occurred_at_utc") == "2026-07-19T07:02:11Z"
        and publication_transition.get("cause") == "instrumentation_release_anchor_published"
        and publication_transition.get("from_phase") == "instrumentation_repair_installed_not_published"
        and publication_transition.get("to_phase") == PUBLISHED_PHASE
        and PATCH_COMMIT in publication_transition.get("evidence", [])
        and ANCHOR_COMMIT in publication_transition.get("evidence", [])
    )
    record(
        "append_only_publication_transition",
        transition_ok,
        "installation retained and publication appended" if transition_ok else "publication transition mismatch",
    )

    affected = binding.get("affected_pair_001", {})
    original_attempts = state.get("original_attempts", [])
    originals_retained = (
        isinstance(original_attempts, list)
        and [item.get("run_id") for item in original_attempts if isinstance(item, dict)]
        == ["CSH-RUN-001", "CSH-RUN-002"]
        and all(
            item.get("immutable") is True
            and item.get("replaced") is False
            and item.get("superseded") is False
            for item in original_attempts
            if isinstance(item, dict)
        )
    )
    state_ok = (
        affected.get("originals_immutable") is True
        and affected.get("originals_replaced") is False
        and affected.get("originals_superseded") is False
        and affected.get("repeat_count_required") == 2
        and originals_retained
        and state.get("repeat_runs") == []
    )
    record("original_attempt_and_repeat_boundary", state_ok, "originals preserved; two new repetitions required" if state_ok else "Pair-001 state mismatch")

    provenance_errors: list[str] = []
    for item in provenance.get("successions", []):
        original = item.get("original", {}) if isinstance(item, dict) else {}
        successor = item.get("successor", {}) if isinstance(item, dict) else {}
        archive_path = root / str(original.get("archive_path", ""))
        live_path = root / str(item.get("live_path", "")) if isinstance(item, dict) else root
        if not archive_path.is_file() or sha256(archive_path) != original.get("sha256"):
            provenance_errors.append(f"archived predecessor mismatch {original.get('archive_path')}")
        if not live_path.is_file() or sha256(live_path) != successor.get("sha256"):
            provenance_errors.append(f"live successor mismatch {item.get('live_path') if isinstance(item, dict) else None}")
        if successor.get("semantic_change") is not False:
            provenance_errors.append("successor semantic-change boundary violated")
    if len(provenance.get("successions", [])) != 2:
        provenance_errors.append("exactly two workflow successions required")
    record("workflow_successor_provenance", not provenance_errors, "predecessors and successors verified" if not provenance_errors else "; ".join(provenance_errors))

    prerequisite_items = binding.get("prerequisites", [])
    prerequisite_map = {
        item.get("id"): item.get("satisfied")
        for item in prerequisite_items
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    prerequisite_shape_ok = set(prerequisite_map) == EXPECTED_PREREQUISITES and all(isinstance(value, bool) for value in prerequisite_map.values())
    record("prerequisite_set", prerequisite_shape_ok, "complete" if prerequisite_shape_ok else "missing, duplicated, or invalid prerequisite")

    anchor_published = (
        anchor.get("status") == "published"
        and isinstance(anchor.get("admitted_commit"), str)
        and len(anchor.get("admitted_commit")) == 40
        and anchor.get("all_required_checks_successful") is True
    )
    all_prerequisites = prerequisite_shape_ok and all(prerequisite_map.values())
    execution_permitted = binding.get("provider_execution_permitted") is True
    zero_calls = binding.get("provider_calls_performed_by_this_stage") == 0
    record("stage_performed_no_provider_calls", zero_calls, "zero" if zero_calls else "provider-call count must remain zero")

    executable = all_prerequisites and anchor_published and execution_permitted
    boundary_consistent = (
        prerequisite_map.get("INSTRUMENTATION_RELEASE_ANCHOR_PUBLISHED", False) == anchor_published
        and execution_permitted == (all_prerequisites and anchor_published)
        and zero_calls
    )
    record("fail_closed_execution_boundary", boundary_consistent, "executable" if executable else "execution blocked")
    provisional_structural_ok = all(item["passed"] for item in checks)
    expected_declared_status = (
        "EXECUTION_READY"
        if provisional_structural_ok and executable
        else (
            "STRUCTURALLY_READY_EXECUTION_BLOCKED"
            if provisional_structural_ok
            else "PRE_EXECUTION_BINDING_FAILED"
        )
    )
    declared_status = binding.get("status")
    record(
        "declared_status_consistency",
        declared_status == expected_declared_status,
        (
            f"declared and recomputed status agree: {expected_declared_status}"
            if declared_status == expected_declared_status
            else (
                "declared status contradiction: "
                f"declared={declared_status!r}; recomputed={expected_declared_status!r}"
            )
        ),
    )
    return finish(checks, executable=executable, prerequisites=prerequisite_map)


def finish(checks: list[dict[str, Any]], *, executable: bool, prerequisites: dict[str, bool]) -> dict[str, Any]:
    failed = [item for item in checks if not item["passed"]]
    structural_ok = not failed
    return {
        "checker": Path(__file__).name,
        "result": {
            "structural_ok": structural_ok,
            "executable": structural_ok and executable,
            "status": "EXECUTION_READY" if structural_ok and executable else (
                "STRUCTURALLY_READY_EXECUTION_BLOCKED" if structural_ok else "PRE_EXECUTION_BINDING_FAILED"
            ),
            "provider_calls_performed": 0,
        },
        "checks": checks,
        "total": len(checks),
        "passed": len(checks) - len(failed),
        "failed": len(failed),
        "prerequisites": prerequisites,
        "non_claims": {
            "does_not_establish_hypothesis": True,
            "does_not_approve_merge": True,
            "does_not_supply_provider_credentials": True,
            "does_not_authorize_execution_while_blocked": True,
            "does_not_replace_original_attempts": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--require-executable", action="store_true")
    args = parser.parse_args()
    result = evaluate(repo_root(args.root))
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in result["checks"]:
            print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']}: {item['detail']}")
        print(result["result"]["status"])
    if result["failed"]:
        return 1
    if args.require_executable and not result["result"]["executable"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
