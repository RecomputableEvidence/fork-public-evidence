from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest


pytest.importorskip(
    "yaml",
    reason="independent verification workflow assertions require the claim-admission dependency lock",
    exc_type=ImportError,
)


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_independent_verification_surface_v0_1.py"
POLICY = ROOT / "policies/independent-verification/INDEPENDENT_VERIFICATION_POLICY_v0_1.json"
POLICY_SCHEMA = ROOT / "schemas/independent_verification_policy_v0_1.schema.json"
PLAN_SCHEMA = ROOT / "schemas/independent_verification_plan_v0_1.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/independent_verification_receipt_v0_1.schema.json"
SELF_CHECK_RECEIPT = ROOT / "receipts/independent-verification/FORK_INDEPENDENT_VERIFICATION_SURFACE_SELF_CHECK_v0_1.json"
PR63_PLAN = ROOT / "verification/plans/PR_63_CSH_AMENDMENT_v0_1.json"
PR63_RECEIPT = ROOT / "receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1.json"
INSTRUMENTATION_FREEZE = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/amendments/"
    "CSH-AMEND-002/INSTRUMENTATION_FREEZE_v0_1_1.json"
)


def load_module():
    sys.path.insert(0, str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location("ivs_checker", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IVS = load_module()


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        list(args),
        cwd=str(repo),
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode != 0:
        raise AssertionError(completed.stderr or completed.stdout)
    return completed


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(repo, "git", *args, check=check)


def commit_all(repo: Path, message: str) -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def copy_trusted_surface(repo: Path) -> None:
    for directory in (".github", "docs/preservation", "policies"):
        shutil.copytree(ROOT / directory, repo / directory)
    (repo / INSTRUMENTATION_FREEZE.parent).mkdir(parents=True)
    shutil.copy2(ROOT / INSTRUMENTATION_FREEZE, repo / INSTRUMENTATION_FREEZE)
    (repo / "schemas").mkdir()
    for source in ROOT.glob("schemas/*verification*v0_1.schema.json"):
        shutil.copy2(source, repo / "schemas" / source.name)
    for name in (
        "consumer_owned_claim_admission_policy_v0_1.schema.json",
        "claim_admission_hardening_stage_v0_1.schema.json",
    ):
        shutil.copy2(ROOT / "schemas" / name, repo / "schemas" / name)
    (repo / "tools").mkdir()
    for name in (
        "check_claim_admission_gate_v0_1.py",
        "check_independent_verification_surface_v0_1.py",
        "check_preservation_integrity_v0_1.py",
    ):
        shutil.copy2(ROOT / "tools" / name, repo / "tools" / name)
    for source in ROOT.glob("requirements-*"):
        shutil.copy2(source, repo / source.name)


def materialize(tmp_path: Path) -> tuple[Path, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    copy_trusted_surface(repo)
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Independent Surface Test")
    git(repo, "config", "user.email", "independent-surface@example.invalid")
    base = commit_all(repo, "trusted verifier base")
    (repo / "candidate-note.md").write_text("bounded candidate\n", encoding="utf-8", newline="\n")
    candidate = commit_all(repo, "candidate")
    return repo, base, candidate


def plan_for(repo: Path, base: str, candidate: str, expected_sha256: str | None = None) -> dict:
    note = (repo / "candidate-note.md").read_bytes()
    expected_sha256 = expected_sha256 or hashlib.sha256(note).hexdigest()
    return {
        "plan_id": "FORK_IVS_TEST_PLAN_V0_1",
        "schema_version": "0.1",
        "scope_statement": "Verify one bounded candidate note.",
        "subject": {
            "repository": "example/fork",
            "base_commit": base,
            "base_tree": git(repo, "rev-parse", f"{base}^{{tree}}").stdout.strip(),
            "candidate_commit": candidate,
            "candidate_tree": git(repo, "rev-parse", f"{candidate}^{{tree}}").stdout.strip(),
            "expected_merge_base": base,
        },
        "expected_claim_admission": {
            "result_kind": "STRUCTURAL_PASS",
            "findings": [],
            "interpretation": "The bounded note must not weaken any trusted control.",
        },
        "assertions": [
            {
                "assertion_id": "EXACT_CHANGED_PATHS",
                "type": "CHANGED_PATH_SET_EQUALS",
                "expected_paths": ["candidate-note.md"],
            },
            {
                "assertion_id": "NOTE_PRESENT",
                "type": "PATH_PRESENT",
                "path": "candidate-note.md",
            },
            {
                "assertion_id": "NOTE_SHA256",
                "type": "SHA256_EQUALS",
                "path": "candidate-note.md",
                "expected_sha256": expected_sha256,
            },
        ],
        "external_evidence": [],
        "independence_boundary": {
            "plan_origin": "TRUSTED_VERIFIER_CONTROL_PLANE",
            "candidate_tree_controls_plan": False,
            "human_verifier": "UNASSIGNED_EXTERNAL_REVIEWER",
            "self_certification_prohibited": True,
        },
    }


def write_plan(repo: Path, plan: dict) -> Path:
    path = repo / "verification-plan.json"
    path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def test_policy_plan_and_receipt_schemas_are_valid() -> None:
    policy_schema = json.loads(POLICY_SCHEMA.read_text(encoding="utf-8"))
    plan_schema = json.loads(PLAN_SCHEMA.read_text(encoding="utf-8"))
    receipt_schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    for schema in (policy_schema, plan_schema, receipt_schema):
        jsonschema.Draft7Validator.check_schema(schema)
    jsonschema.Draft7Validator(policy_schema).validate(json.loads(POLICY.read_text(encoding="utf-8")))
    jsonschema.Draft7Validator(plan_schema).validate(json.loads(PR63_PLAN.read_text(encoding="utf-8")))
    jsonschema.Draft7Validator(receipt_schema).validate(json.loads(PR63_RECEIPT.read_text(encoding="utf-8")))


def test_committed_self_check_receipt_recomputes_exactly() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--repo-root", str(ROOT), "--self-check"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert json.loads(completed.stdout) == json.loads(SELF_CHECK_RECEIPT.read_text(encoding="utf-8"))


def test_supported_plan_verifies_without_candidate_checkout_or_execution(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    plan_path = write_plan(repo, plan_for(repo, base, candidate))
    receipt = IVS.verify(repo, plan_path, fetch=False)
    assert receipt["result"]["verdict"] == "VERIFIED_WITHIN_DECLARED_SCOPE"
    assert receipt["claim_admission"]["candidate_checkout"] == "NONE"
    assert receipt["claim_admission"]["candidate_code_execution"] == "NONE"
    assert all(item["status"] == "SUPPORTED" for item in receipt["assertions"])


def test_mismatched_evidence_invalidates_contribution(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    plan = plan_for(repo, base, candidate, expected_sha256="0" * 64)
    receipt = IVS.verify(repo, write_plan(repo, plan), fetch=False)
    assert receipt["result"]["verdict"] == "INVALIDATED_BY_RECOMPUTATION"
    assert receipt["result"]["contradicted_assertion_count"] == 1
    assert next(item for item in receipt["assertions"] if item["assertion_id"] == "NOTE_SHA256")["status"] == "CONTRADICTED"


def test_candidate_worktree_mutation_does_not_change_git_object_result(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    plan = plan_for(repo, base, candidate)
    plan_path = write_plan(repo, plan)
    (repo / "candidate-note.md").write_text("uncommitted mutation\n", encoding="utf-8", newline="\n")
    receipt = IVS.verify(repo, plan_path, fetch=False)
    assert receipt["result"]["verdict"] == "VERIFIED_WITHIN_DECLARED_SCOPE"
    observed = next(item for item in receipt["assertions"] if item["assertion_id"] == "NOTE_SHA256")
    assert observed["evidence"]["sha256"] == plan["assertions"][2]["expected_sha256"]


def test_subject_tree_mismatch_invalidates_before_authority(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    plan = plan_for(repo, base, candidate)
    plan["subject"]["candidate_tree"] = "0" * 40
    receipt = IVS.verify(repo, write_plan(repo, plan), fetch=False)
    assert receipt["result"]["verdict"] == "INVALIDATED_BY_RECOMPUTATION"
    assert receipt["result"]["subject_binding_contradictions"][0]["field"] == "candidate_tree"
    assert receipt["result"]["merge_effect"] == "NONE"


def test_missing_commit_is_inconclusive_not_verified(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    plan = plan_for(repo, base, candidate)
    plan["subject"]["candidate_commit"] = "f" * 40
    receipt = IVS.verify(repo, write_plan(repo, plan), fetch=False)
    assert receipt["result"]["verdict"] == "INCONCLUSIVE_EVIDENCE_GAP"
    assert receipt["result"]["ok"] is False


def test_duplicate_plan_key_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"plan_id":"A","plan_id":"B"}\n', encoding="utf-8")
    try:
        IVS.strict_json_file(path)
    except ValueError as exc:
        assert "duplicate key" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("duplicate key unexpectedly accepted")


def test_plan_schema_prohibits_commands_and_path_traversal(tmp_path: Path) -> None:
    repo, base, candidate = materialize(tmp_path)
    schema = json.loads(PLAN_SCHEMA.read_text(encoding="utf-8"))
    plan = plan_for(repo, base, candidate)
    plan["assertions"][1]["command"] = "python candidate.py"
    with_command = list(jsonschema.Draft7Validator(schema).iter_errors(plan))
    assert with_command
    plan = plan_for(repo, base, candidate)
    plan["assertions"][1]["path"] = "../outside"
    traversal = list(jsonschema.Draft7Validator(schema).iter_errors(plan))
    assert traversal


def test_pr63_receipt_is_bound_to_plan_and_records_no_human_review() -> None:
    plan = json.loads(PR63_PLAN.read_text(encoding="utf-8"))
    receipt = json.loads(PR63_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["plan"]["plan_id"] == plan["plan_id"]
    assert receipt["plan"]["sha256"] == hashlib.sha256(PR63_PLAN.read_bytes()).hexdigest()
    assert receipt["subject"]["base_commit"] == plan["subject"]["base_commit"]
    assert receipt["subject"]["candidate_commit"] == plan["subject"]["candidate_commit"]
    assert receipt["result"]["verdict"] == "VERIFIED_WITHIN_DECLARED_SCOPE"
    assert receipt["independence_boundary"]["human_independent_review_recorded"] is False
    assert receipt["result"]["experiment_execution_effect"] == "NONE"
