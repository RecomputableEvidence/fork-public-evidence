from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_cbo_minimum_packet.py"
VALID = ROOT / "examples" / "cbo_minimum_packet" / "sc_workload_001_candidate_v0_1.json"
INVALID_AUTHORITY = ROOT / "examples" / "cbo_minimum_packet" / "invalid_authority_transfer_v0_1.json"
INVALID_PENDING = ROOT / "examples" / "cbo_minimum_packet" / "invalid_pending_or_present_status_v0_1.json"
INVALID_FORK_VALIDATES = ROOT / "examples" / "cbo_minimum_packet" / "invalid_fork_validates_governance_v0_1.json"


class CboMinimumPacketTests(unittest.TestCase):
    def run_tool(self, path: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), str(path), "--compact"],
            text=True,
            capture_output=True,
        )

    def test_valid_packet_passes(self) -> None:
        proc = self.run_tool(VALID)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["result"]["ok"])
        self.assertEqual(payload["result"]["computed_outcome"], "CBO_MINIMUM_PACKET_STRUCTURALLY_VALID")
        self.assertTrue(payload["limitations"]["does_not_validate_issuer_governance"])
        self.assertTrue(payload["limitations"]["issuer_invariant_refs_are_opaque"])

    def test_invalid_authority_transfer_fails(self) -> None:
        proc = self.run_tool(INVALID_AUTHORITY)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        codes = {finding["code"] for finding in payload["result"]["findings"]}
        self.assertIn("AUTHORITY_BOUNDARY_VIOLATION", codes)

    def test_invalid_pending_or_present_status_fails(self) -> None:
        proc = self.run_tool(INVALID_PENDING)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        codes = {finding["code"] for finding in payload["result"]["findings"]}
        self.assertIn("AMBIGUOUS_STATUS_VALUE", codes)

    def test_invalid_fork_validates_governance_fails(self) -> None:
        proc = self.run_tool(INVALID_FORK_VALIDATES)
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        paths = {finding["path"] for finding in payload["result"]["findings"]}
        self.assertIn("boundary_semantics.fork_validates_issuer_governance", paths)

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
