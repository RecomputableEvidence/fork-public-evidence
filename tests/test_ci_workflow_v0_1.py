from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "fork-evidence-ci.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_ci_workflow_exists() -> None:
    assert WORKFLOW.exists()


def test_ci_workflow_runs_on_pull_request_and_push() -> None:
    text = workflow_text()

    assert "pull_request:" in text
    assert "push:" in text
    assert "main" in text
    assert '"v0_*"' in text


def test_ci_workflow_runs_required_invariant_tools() -> None:
    text = workflow_text()

    required_commands = [
        "python tools/check_line_endings.py",
        "python tools/check_claim_boundary.py examples/claim_boundary/valid_integrity_only.json",
        "python tools/check_artifact_claim_boundary.py examples/claim_boundary_artifacts/valid_receipt_with_claim_boundary.json",
        "python tools/check_artifact_claim_boundary.py examples/claim_boundary_binding/verification_result_bound_valid.json",
        "python tools/bind_claim_boundary.py",
        "python -m pytest",
    ]

    for command in required_commands:
        assert command in text


def test_ci_workflow_contains_negative_guards() -> None:
    text = workflow_text()

    required_negative_examples = [
        "invalid_overclaim_compliance.json",
        "invalid_receipt_missing_claim_boundary.json",
        "invalid_release_metadata_overclaim.json",
        "verification_result_unbound_invalid.json",
        "unexpectedly passed",
        "failed as expected",
    ]

    for marker in required_negative_examples:
        assert marker in text


def test_ci_workflow_runs_full_local_test_set() -> None:
    text = workflow_text()

    required_tests = [
        "tests/test_claim_boundary_v0_1.py",
        "tests/test_claim_boundary_phase_2.py",
        "tests/test_claim_boundary_binding_v0_1.py",
        "tests/test_line_endings_v0_1.py",
        "tests/test_ci_workflow_v0_1.py",
    ]

    for test_path in required_tests:
        assert test_path in text