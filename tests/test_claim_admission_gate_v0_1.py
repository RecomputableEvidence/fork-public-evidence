from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import jsonschema


pytest.importorskip(
    "yaml",
    reason="claim-admission tests require the claim-admission dependency lock",
    exc_type=ImportError,
)


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_claim_admission_gate_v0_1.py"
POLICY = Path("policies/claim-admission/CONSUMER_OWNED_CLAIM_ADMISSION_POLICY_v0_1.json")
BRANCH_RULES = Path("policies/repository-hardening/BRANCH_RULESET_REQUIREMENTS_v0_1.json")
EVIDENCE_WORKFLOW = Path(".github/workflows/fork-evidence-ci.yml")
TRUSTED_WORKFLOW = Path(".github/workflows/consumer-owned-claim-admission.yml")
SEALED_CSH_WORKFLOW = Path(".github/workflows/cross-system-claim-handoff-v0-1.yml")
SPECIMEN = Path(
    "docs/preservation/failure-mode-archive-v0.1/incidents/"
    "FORK-INC-2026-07-13-001/specimens/fork-evidence-ci.7080e198.malformed.yml.txt"
)
POLICY_SCHEMA = ROOT / "schemas/consumer_owned_claim_admission_policy_v0_1.schema.json"
STAGE = ROOT / "docs/preservation/control-stages/CLAIM_ADMISSION_HARDENING_STAGE_v0_1.json"
STAGE_SCHEMA = ROOT / "schemas/claim_admission_hardening_stage_v0_1.schema.json"
RECEIPT = ROOT / "receipts/claim-admission/FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json"
INSTRUMENTATION_FREEZE = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/amendments/"
    "CSH-AMEND-002/INSTRUMENTATION_FREEZE_v0_1_1.json"
)


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


def materialize(tmp_path: Path) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    repo.mkdir()
    for directory in (".github", "docs/preservation", "policies"):
        shutil.copytree(ROOT / directory, repo / directory)
    (repo / INSTRUMENTATION_FREEZE.parent).mkdir(parents=True)
    shutil.copy2(ROOT / INSTRUMENTATION_FREEZE, repo / INSTRUMENTATION_FREEZE)
    (repo / "schemas").mkdir()
    for name in (
        "consumer_owned_claim_admission_policy_v0_1.schema.json",
        "claim_admission_hardening_stage_v0_1.schema.json",
    ):
        shutil.copy2(ROOT / "schemas" / name, repo / "schemas" / name)
    (repo / "tools").mkdir()
    shutil.copy2(CHECKER, repo / "tools/check_claim_admission_gate_v0_1.py")
    for source in ROOT.glob("requirements-*"):
        shutil.copy2(source, repo / source.name)

    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Fork Gate Test")
    git(repo, "config", "user.email", "fork-gate-test@example.invalid")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "trusted base")
    return repo, git(repo, "rev-parse", "HEAD").stdout.strip()


def commit_all(repo: Path, message: str = "candidate") -> str:
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def run_checker(repo: Path, base: str, candidate: str) -> tuple[int, dict]:
    completed = subprocess.run(
        [
            sys.executable,
            str(CHECKER),
            "--repo-root",
            str(repo),
            "--base-sha",
            base,
            "--candidate-sha",
            candidate,
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.stdout.strip(), completed.stderr
    return completed.returncode, json.loads(completed.stdout)


def error_codes(payload: dict) -> set[str]:
    return {item["code"] for item in payload["errors"]}


def mutate_text(repo: Path, relative: Path, old: str, new: str) -> None:
    path = repo / relative
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def restore_trusted_file(repo: Path, base: str, relative: Path) -> None:
    content = subprocess.run(
        ["git", "show", f"{base}:{relative.as_posix()}"],
        cwd=str(repo),
        capture_output=True,
        check=True,
    ).stdout
    (repo / relative).write_bytes(content)


def test_valid_candidate_is_review_eligible_but_not_admitted(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    (repo / "candidate-note.md").write_text("bounded candidate\n", encoding="utf-8")
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code == 0
    assert payload["result"] == {
        "admission_effect": "REVIEW_ELIGIBLE_NOT_ADMITTED",
        "ok": True,
        "repository_standing_effect": "NONE",
        "result_kind": "STRUCTURAL_PASS",
    }
    assert payload["execution_boundary"]["candidate_checkout"] == "NONE"
    assert payload["execution_boundary"]["candidate_code_execution"] == "NONE"
    assert payload["non_claims"]["does_not_approve_merge"] is True


def test_policy_and_stage_records_conform_to_schemas() -> None:
    policy_schema = json.loads(POLICY_SCHEMA.read_text(encoding="utf-8"))
    stage_schema = json.loads(STAGE_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(policy_schema)
    jsonschema.Draft7Validator.check_schema(stage_schema)
    jsonschema.Draft7Validator(policy_schema).validate(
        json.loads((ROOT / POLICY).read_text(encoding="utf-8"))
    )
    jsonschema.Draft7Validator(stage_schema).validate(
        json.loads(STAGE.read_text(encoding="utf-8"))
    )


def test_committed_self_check_receipt_matches_current_checker_output() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--repo-root", str(ROOT), "--self-check"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout
    assert json.loads(completed.stdout) == json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_candidate_is_read_from_git_objects_not_worktree(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    (repo / "candidate-note.md").write_text("committed state\n", encoding="utf-8")
    candidate = commit_all(repo)
    mutate_text(repo, EVIDENCE_WORKFLOW, "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0", "actions/checkout@v7")
    code, payload = run_checker(repo, base, candidate)
    assert code == 0
    assert payload["result"]["ok"] is True


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        (
            "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
            "actions/checkout@v7",
            "MUTABLE_ACTION_REFERENCE",
        ),
        ("contents: read", "contents: write", "WORKFLOW_PERMISSIONS_NOT_LEAST_PRIVILEGE"),
        ("persist-credentials: false", "persist-credentials: true", "CHECKOUT_CREDENTIALS_PERSISTED"),
        ("runs-on: ubuntu-latest", "runs-on: self-hosted", "SELF_HOSTED_RUNNER_PROHIBITED"),
        ("    timeout-minutes: 30\n", "", "JOB_TIMEOUT_INVALID"),
        (
            "python -m pip install --require-hashes\n"
            "          -r requirements-proof-surface.lock.txt\n"
            "          -r requirements-claim-admission.lock.txt",
            "python -m pip install pytest",
            "UNHASHED_PYTHON_INSTALL",
        ),
    ],
)
def test_workflow_hardening_regressions_fail_closed(
    tmp_path: Path,
    old: str,
    new: str,
    expected: str,
) -> None:
    repo, base = materialize(tmp_path)
    mutate_text(repo, EVIDENCE_WORKFLOW, old, new)
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert expected in error_codes(payload)


def test_duplicate_yaml_key_fails_closed(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    mutate_text(
        repo,
        EVIDENCE_WORKFLOW,
        "permissions:\n  contents: read",
        "permissions:\n  contents: read\n\npermissions:\n  contents: read",
    )
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "DUPLICATE_YAML_KEY" in error_codes(payload)


def test_untrusted_pull_request_expression_in_run_script_fails(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    mutate_text(
        repo,
        TRUSTED_WORKFLOW,
        'run: python -m pip install --require-hashes -r requirements-claim-admission.lock.txt',
        'run: echo "${{ github.event.pull_request.title }}"',
    )
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "UNTRUSTED_CONTEXT_IN_RUN_SCRIPT" in error_codes(payload)


def test_candidate_ref_cannot_be_checked_out_by_trusted_workflow(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    mutate_text(
        repo,
        TRUSTED_WORKFLOW,
        "ref: ${{ github.event.pull_request.base.sha }}",
        "ref: ${{ github.event.pull_request.head.sha }}",
    )
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "CANDIDATE_CHECKOUT_PROHIBITED" in error_codes(payload)


def test_quarantined_workflow_digest_cannot_recur(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    (repo / EVIDENCE_WORKFLOW).write_bytes((repo / SPECIMEN).read_bytes())
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "QUARANTINED_DIGEST_IN_LIVE_WORKFLOW" in error_codes(payload)


def test_byte_sealed_workflow_exception_is_exact_digest_only(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    mutate_text(repo, SEALED_CSH_WORKFLOW, "actions/checkout@v4", "actions/checkout@v4 # changed")
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "SEALED_WORKFLOW_DIGEST_MISMATCH" in error_codes(payload)


def test_symbolic_link_fails_closed(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    link = repo / "unsafe-link"
    try:
        os.symlink(POLICY.as_posix(), link)
    except (OSError, NotImplementedError):
        pytest.skip("Symbolic links are unavailable on this platform")
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "CANDIDATE_FILE_MODE_PROHIBITED" in error_codes(payload)


def test_gitlink_submodule_entry_fails_closed(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    git(repo, "update-index", "--add", "--cacheinfo", f"160000,{base},vendor/untrusted")
    git(repo, "commit", "-q", "-m", "candidate gitlink")
    candidate = git(repo, "rev-parse", "HEAD").stdout.strip()
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert {"GIT_SUBMODULE_PROHIBITED", "CANDIDATE_FILE_MODE_PROHIBITED"} <= error_codes(payload)


def test_duplicate_json_key_fails_closed(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    path = repo / BRANCH_RULES
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '  "schema_version": "0.1",',
        '  "schema_version": "0.1",\n  "schema_version": "0.1",',
        1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")
    candidate = commit_all(repo)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "DUPLICATE_JSON_KEY" in error_codes(payload)


def test_candidate_policy_cannot_change_experiment_state(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    path = repo / POLICY
    value = json.loads(path.read_text(encoding="utf-8"))
    value["experiment_effect"]["baseline_execution_started"] = True
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    candidate = commit_all(repo)
    restore_trusted_file(repo, base, POLICY)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "EXPERIMENT_BOUNDARY_EFFECT" in error_codes(payload)


def test_candidate_policy_cannot_claim_gate_is_already_active(tmp_path: Path) -> None:
    repo, base = materialize(tmp_path)
    path = repo / POLICY
    value = json.loads(path.read_text(encoding="utf-8"))
    value["activation_state"] = "ACTIVE"
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    candidate = commit_all(repo)
    restore_trusted_file(repo, base, POLICY)
    code, payload = run_checker(repo, base, candidate)
    assert code != 0
    assert "ACTIVATION_STATE_OVERCLAIM" in error_codes(payload)
