import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_surface_interaction_v0_1.py"
VALID_FIXTURE = ROOT / "examples" / "surface-interaction" / "valid" / "valid_reliance_references_evidence_boundary_v0_1.json"
INVALID_FIXTURES = {
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_evidence_boundary_mutation_attempt_v0_1.json": "SURFACE_INTERACTION_NOT_INSPECTABLE",
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_interop_semantic_adoption_attempt_v0_1.json": "SEMANTIC_ADOPTION_ATTEMPTED",
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_authority_absorption_attempt_v0_1.json": "AUTHORITY_ABSORPTION_ATTEMPTED",
}


def run_checker(*args):
    return subprocess.run(
        [sys.executable, str(CHECKER), *[str(arg) for arg in args]],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def combined_output(result):
    return (result.stdout or "") + (result.stderr or "")


def test_valid_surface_interaction_fixture_conforms():
    result = run_checker(VALID_FIXTURE)
    output = combined_output(result)

    assert result.returncode == 0, output
    assert "SURFACE_INTERACTION_CONFORMS" in output
    assert "DECLARED_OUTCOME_MISMATCH" not in output


def test_invalid_surface_interaction_fixtures_match_declared_outcomes():
    for fixture, expected_outcome in INVALID_FIXTURES.items():
        result = run_checker(fixture)
        output = combined_output(result)

        assert result.returncode != 0, output
        assert expected_outcome in output
        assert "DECLARED_OUTCOME_MISMATCH" not in output


def test_invalid_surface_interaction_fixtures_pass_with_expect_invalid():
    result = run_checker(*INVALID_FIXTURES.keys(), "--expect-invalid")
    output = combined_output(result)

    assert result.returncode == 0, output
    for expected_outcome in INVALID_FIXTURES.values():
        assert expected_outcome in output
    assert "DECLARED_OUTCOME_MISMATCH" not in output
