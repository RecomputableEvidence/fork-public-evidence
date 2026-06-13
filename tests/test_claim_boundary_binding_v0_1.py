from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINDER = ROOT / "tools" / "bind_claim_boundary.py"
ARTIFACT_CHECKER = ROOT / "tools" / "check_artifact_claim_boundary.py"
PROFILE = ROOT / "claim_profiles" / "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY_v0_1.json"
UNBOUND = ROOT / "examples" / "claim_boundary_binding" / "verification_result_unbound_invalid.json"
BOUND = ROOT / "examples" / "claim_boundary_binding" / "verification_result_bound_valid.json"


def run_command(*args: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(arg) for arg in args],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_unbound_verification_result_fails_artifact_checker() -> None:
    result = run_command(sys.executable, ARTIFACT_CHECKER, UNBOUND)

    assert result.returncode != 0
    assert "CLAIM_BOUNDARY_BLOCK_MISSING" in result.stderr


def test_static_bound_verification_result_passes_artifact_checker() -> None:
    result = run_command(sys.executable, ARTIFACT_CHECKER, BOUND)

    assert result.returncode == 0, result.stderr
    assert "ARTIFACT_CLAIM_BOUNDARY_PASS" in result.stdout


def test_bind_tool_emits_bound_artifact_that_passes_checker(tmp_path: Path) -> None:
    output = tmp_path / "bound_output.json"

    bind_result = run_command(
        sys.executable,
        BINDER,
        UNBOUND,
        "--output",
        output,
    )

    assert bind_result.returncode == 0, bind_result.stderr
    assert "CLAIM_BOUNDARY_BOUND" in bind_result.stdout

    data = json.loads(output.read_text(encoding="utf-8"))
    assert "claim_boundary" in data
    assert data["claim_boundary"]["claim_type"] == "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY"

    check_result = run_command(sys.executable, ARTIFACT_CHECKER, output)

    assert check_result.returncode == 0, check_result.stderr
    assert "ARTIFACT_CLAIM_BOUNDARY_PASS" in check_result.stdout


def test_bind_tool_refuses_existing_claim_boundary_without_replace_flag(tmp_path: Path) -> None:
    output = tmp_path / "should_not_bind.json"

    result = run_command(
        sys.executable,
        BINDER,
        BOUND,
        "--output",
        output,
    )

    assert result.returncode != 0
    assert "BINDING_REFUSAL_EXISTING_CLAIM_BOUNDARY" in result.stderr


def test_bind_tool_can_replace_existing_claim_boundary_with_explicit_flag(tmp_path: Path) -> None:
    output = tmp_path / "rebound_output.json"

    result = run_command(
        sys.executable,
        BINDER,
        BOUND,
        "--output",
        output,
        "--replace-existing-claim-boundary",
    )

    assert result.returncode == 0, result.stderr
    assert "CLAIM_BOUNDARY_BOUND" in result.stdout

    check_result = run_command(sys.executable, ARTIFACT_CHECKER, output)

    assert check_result.returncode == 0, check_result.stderr
    assert "ARTIFACT_CLAIM_BOUNDARY_PASS" in check_result.stdout


def test_bind_tool_rejects_overclaiming_profile(tmp_path: Path) -> None:
    bad_profile = tmp_path / "bad_profile.json"
    output = tmp_path / "bad_bound_output.json"

    profile_data = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile_data["allowed_inferences"][0] = "This proves the workflow was compliant and lawful."
    bad_profile.write_text(json.dumps(profile_data, indent=2) + "\n", encoding="utf-8")

    result = run_command(
        sys.executable,
        BINDER,
        UNBOUND,
        "--profile",
        bad_profile,
        "--output",
        output,
    )

    assert result.returncode != 0
    assert "CLAIM_EXPANSION_DEFECT" in result.stderr
    assert (
        "compliant" in result.stderr.lower()
        or "lawful" in result.stderr.lower()
    )