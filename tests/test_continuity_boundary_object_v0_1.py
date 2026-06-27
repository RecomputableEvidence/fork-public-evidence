from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_continuity_boundary_object.py"
VALID = ROOT / "examples" / "continuity_boundary_object" / "minimal_synthetic_trace_v0_1.json"
INVALID_AUTHORITY = ROOT / "examples" / "continuity_boundary_object" / "invalid_authority_transfer_v0_1.json"
INVALID_RECEIVER = ROOT / "examples" / "continuity_boundary_object" / "invalid_receiver_verifies_governance_v0_1.json"


class ContinuityBoundaryObjectTests(unittest.TestCase):
    def run_tool(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), str(path), "--compact"],
            text=True,
            capture_output=True,
        )

    def test_valid_minimal_trace(self) -> None:
        proc = self.run_tool(VALID)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["result"]["ok"])
        self.assertEqual(payload["result"]["computed_outcome"], "CBO_STRUCTURALLY_VALID")

    def test_invalid_authority_transfer_fails(self) -> None:
        proc = self.run_tool(INVALID_AUTHORITY)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["result"]["ok"])
        codes = {finding["code"] for finding in payload["result"]["findings"]}
        self.assertIn("AUTHORITY_BOUNDARY_VIOLATION", codes)

    def test_invalid_receiver_verifies_governance_fails(self) -> None:
        proc = self.run_tool(INVALID_RECEIVER)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["result"]["ok"])
        paths = {finding["path"] for finding in payload["result"]["findings"]}
        self.assertIn("continuity_object_semantics.receiver_verifies_upstream_governance", paths)

    def test_duplicate_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "duplicate.json"
            path.write_text('{"profile_id":"x","profile_id":"y"}', encoding="utf-8", newline="\n")
            proc = self.run_tool(path)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["result"]["computed_outcome"], "INPUT_ERROR")

    def test_bom_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bom.json"
            path.write_bytes(b"\xef\xbb\xbf{}")
            proc = self.run_tool(path)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["result"]["computed_outcome"], "INPUT_ERROR")


if __name__ == "__main__":
    unittest.main()
