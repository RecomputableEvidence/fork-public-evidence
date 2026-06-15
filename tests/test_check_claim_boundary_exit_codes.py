from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_claim_boundary.py"


def write_payload(path: Path, claim_statement: str, allowed_inferences: list[str]) -> None:
    payload = {
        "claim_type": "OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY",
        "claim_statement": claim_statement,
        "allowed_inferences": allowed_inferences,
        "forbidden_inferences": [
            "Does not prove AI output correctness.",
            "Does not prove legal admissibility.",
            "Does not prove compliance satisfaction.",
        ],
        "not_checked": [
            "Source completeness was not checked.",
            "Legal admissibility was not checked.",
        ],
        "non_claims": [
            "No decision correctness claim is made.",
            "No legal admissibility claim is made.",
            "No compliance satisfaction claim is made.",
        ],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_checker(payload_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), str(payload_path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_clean_claim_boundary_exits_zero(tmp_path: Path) -> None:
    payload_path = tmp_path / "clean_claim_boundary.json"
    write_payload(
        payload_path,
        "This boundary asserts observed workflow event integrity only.",
        [
            "The referenced artifacts may be checked against declared hashes.",
            "The preserved record may be inspected within its declared boundary.",
        ],
    )

    result = run_checker(payload_path)

    assert result.returncode == 0
    assert "CLAIM_BOUNDARY_PASS" in result.stdout
    assert "CLAIM_EXPANSION_DEFECT" not in result.stderr


def test_overclaim_defect_exits_nonzero(tmp_path: Path) -> None:
    payload_path = tmp_path / "overclaim_boundary.json"
    write_payload(
        payload_path,
        "This boundary proves the workflow was compliant and correct.",
        [
            "The workflow result is complete and validated.",
        ],
    )

    result = run_checker(payload_path)

    assert result.returncode != 0
    assert "CLAIM_EXPANSION_DEFECT" in result.stderr
    assert "CLAIM_BOUNDARY_FAIL" in result.stderr