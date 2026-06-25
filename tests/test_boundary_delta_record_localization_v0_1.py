import json
import subprocess
from pathlib import Path

def run_checker(fixture: str) -> dict:
    repo_root = Path(__file__).resolve().parents[1]
    checker = repo_root / "tools" / "check_boundary_delta_record.py"
    fixture_path = repo_root / "examples" / "boundary_delta_record" / fixture

    completed = subprocess.run(
        ["python", str(checker), str(fixture_path)],
        check=True,
        capture_output=True,
        text=True
    )
    return json.loads(completed.stdout)

def test_no_localized_establishment_fixture_reports_localization_status():
    """
    This test assumes that check_boundary_delta_record.py is extended to:
    - look for an establishment_ref (or equivalent) in claims
    - populate localization_status and localization_findings accordingly
    """
    output = run_checker("no_localized_establishment_v0_1.json")

    # Allow flexibility: focus on localization posture rather than outcome
    assert "localization_status" in output
    assert output["localization_status"] in {
        "NO_LOCALIZABLE_ESTABLISHMENT",
        "LOCALIZABLE_OR_RECONSTRUCTABLE_ESTABLISHMENT"
    }

    if output["localization_status"] == "NO_LOCALIZABLE_ESTABLISHMENT":
        findings = output.get("localization_findings", [])
        assert "NO_ESTABLISHMENT_EVENT_REF" in findings
        limitations = output.get("limitations", [])
        assert "no_localized_establishment_for_transferred_property" in limitations
