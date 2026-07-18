from __future__ import annotations

import json
import pathlib
import subprocess
import sys


def test_adv_003_post_fix_recomputation() -> None:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [
            sys.executable,
            str(repo_root / "tools/check_longitudinal_day0_adv_003_recomputation_v0_1.py"),
            "--repo-root",
            str(repo_root),
            "--json",
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["total"] == 7
    assert payload["passed"] == 7
    assert payload["failed"] == 0
    outcome_codes = {
        code
        for item in payload["cases"]
        for code in item["outcome_codes"]
    }
    assert {
        "CLEAN_PACKET_STILL_VERIFIES",
        "ADV_003_A_INVENTORY_ADDITION_DETECTED",
        "ADV_003_B_PACKET_ROOT_HASH_BASE_ENFORCED",
        "PACKET_ROOT_CONTROLS_ARTIFACT_RESOLUTION",
        "PATH_ESCAPE_REJECTED",
        "SYMLINK_SUBSTITUTION_REJECTED",
        "EXISTING_ADVERSARIAL_STANDING_UNCHANGED",
    } <= outcome_codes
