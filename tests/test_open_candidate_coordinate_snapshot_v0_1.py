from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_open_candidate_coordinate_snapshot_v0_1.py"
SPEC = importlib.util.spec_from_file_location("open_candidate_snapshot_checker", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def copied_surface(tmp_path: Path) -> Path:
    target = tmp_path / "repo"
    destination = target / CHECKER.SNAPSHOT
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / CHECKER.SNAPSHOT, destination)
    return target


def mutate(tmp_path: Path, update) -> list[str]:
    root = copied_surface(tmp_path)
    path = root / CHECKER.SNAPSHOT
    payload = json.loads(path.read_text(encoding="utf-8"))
    update(payload)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return CHECKER.check(root)


def pr(payload: dict, number: int) -> dict:
    return next(item for item in payload["pull_requests"] if item["pull_request"] == number)


def relationship(payload: dict, relationship_id: str) -> dict:
    return next(
        item
        for item in payload["dependency_and_precedence"]
        if item["relationship_id"] == relationship_id
    )


def test_exact_snapshot_conforms_without_admission() -> None:
    assert CHECKER.check(ROOT) == []


def test_lane_count_cannot_repeat_source_arithmetic_error(tmp_path: Path) -> None:
    errors = mutate(tmp_path, lambda payload: payload.__setitem__("lane_count", 5))
    assert any("six enumerated lanes required" in error for error in errors)


def test_all_eight_pull_requests_are_required(tmp_path: Path) -> None:
    errors = mutate(tmp_path, lambda payload: payload["pull_requests"].pop())
    assert any("exact eight pull requests required" in error for error in errors)


def test_open_status_cannot_be_promoted_to_admission(tmp_path: Path) -> None:
    errors = mutate(tmp_path, lambda payload: pr(payload, 65).__setitem__("admission_effect", "ADMITTED"))
    assert any("PR #65 admission effect must be NONE" in error for error in errors)


def test_green_checks_cannot_create_merge_authorization(tmp_path: Path) -> None:
    def update(payload: dict) -> None:
        payload["non_inheritance_invariants"].remove(
            "GREEN_CHECKS_DO_NOT_CONFER_MERGE_AUTHORIZATION"
        )

    errors = mutate(tmp_path, update)
    assert any("non-inheritance invariant set mismatch" in error for error in errors)


def test_mergeability_cannot_carry_standing(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: pr(payload, 100).__setitem__("mechanics_carry_standing", True),
    )
    assert any("PR #100 GitHub mechanics cannot carry standing" in error for error in errors)


def test_pr105_nonmergeable_observation_is_preserved_without_governance_inference(
    tmp_path: Path,
) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: pr(payload, 105).__setitem__("mergeable_observed", True),
    )
    assert any("PR #105 non-mergeable observation must be preserved" in error for error in errors)


def test_pr84_exact_parent_head_for_pr86_is_required(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: pr(payload, 86).__setitem__("base_sha", "0" * 40),
    )
    assert any("PR #86 base_sha mismatch" in error for error in errors)


def test_chronology_cannot_resolve_pr110_pr111_lineage(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: relationship(payload, "PR110_PR111_LINEAGE_UNRESOLVED").__setitem__(
            "relationship", "PR111_STRICT_SUCCESSOR_TO_PR110"
        ),
    )
    assert any("lineage must remain unresolved" in error for error in errors)


def test_proof001_admission_cannot_promote_wider_portfolio(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: payload["governed_coordinate"].__setitem__(
            "wider_proof_portfolio_admitted", True
        ),
    )
    assert any("Proof 001 cannot promote the wider portfolio" in error for error in errors)


def test_pr106_historical_validity_cannot_become_current_reliance(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: pr(payload, 106).__setitem__(
            "snapshot_classification", "CURRENT_PROOF_PORTFOLIO"
        ),
    )
    assert any("PR #106 temporal classification mismatch" in error for error in errors)


def test_snapshot_is_not_admitted_before_reviewed_merge(tmp_path: Path) -> None:
    errors = mutate(
        tmp_path,
        lambda payload: payload.__setitem__(
            "candidate_standing",
            "OPEN_CANDIDATE_COORDINATE_SNAPSHOT_ADMITTED_NO_SOURCE_PR_EFFECT",
        ),
    )
    assert any("must remain a not-admitted candidate" in error for error in errors)


def test_snapshot_admission_cannot_change_source_prs(tmp_path: Path) -> None:
    def update(payload: dict) -> None:
        payload["standing_effect_on_reviewed_merge"]["source_pull_requests"] = "SUPERSEDED"

    errors = mutate(tmp_path, update)
    assert any("reviewed-merge effect mismatch" in error for error in errors)


def test_branch_protection_requires_separate_authorization(tmp_path: Path) -> None:
    def update(payload: dict) -> None:
        payload["candidate_creation_effects"]["branch_protection"] = "ENABLED"

    errors = mutate(tmp_path, update)
    assert any("candidate creation effects mismatch" in error for error in errors)
