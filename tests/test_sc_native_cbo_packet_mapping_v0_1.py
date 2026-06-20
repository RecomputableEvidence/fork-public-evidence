from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NORMALIZER = ROOT / "tools" / "normalize_sc_native_cbo_packet.py"
CHECKER = ROOT / "tools" / "check_cbo_minimum_packet.py"
VALID_NATIVE = ROOT / "examples" / "sc_native_cbo_packet" / "sc_workload_001_native_v0_1.json"
INVALID_AMBIGUOUS = ROOT / "examples" / "sc_native_cbo_packet" / "invalid_ambiguous_status_v0_1.json"
INVALID_AUTHORITY = ROOT / "examples" / "sc_native_cbo_packet" / "invalid_authority_transfer_v0_1.json"


class ScNativeCboPacketMappingTests(unittest.TestCase):
    def run_normalizer(self, path: Path, out: Path | None = None) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(NORMALIZER), str(path)]
        if out is not None:
            command.extend(["--out", str(out)])
        else:
            command.append("--compact")
        return subprocess.run(command, text=True, capture_output=True)

    def test_valid_native_packet_normalizes(self) -> None:
        proc = self.run_normalizer(VALID_NATIVE)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["profile_id"], "CBO_MINIMUM_PACKET_REQUIREMENTS_v0_1")
        self.assertEqual(payload["integrity_metadata"]["seal_status"], "PENDING")
        self.assertTrue(payload["boundary_semantics"]["issuer_invariant_refs_are_opaque_to_fork"])
        self.assertFalse(payload["boundary_semantics"]["fork_validates_issuer_governance"])

    def test_normalized_packet_passes_cbo_checker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "normalized.json"
            proc = self.run_normalizer(VALID_NATIVE, out=out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            check = subprocess.run(
                [sys.executable, str(CHECKER), str(out), "--compact"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            payload = json.loads(check.stdout)
            self.assertTrue(payload["result"]["ok"])
            self.assertEqual(payload["result"]["computed_outcome"], "CBO_MINIMUM_PACKET_STRUCTURALLY_VALID")

    def test_ambiguous_status_fails(self) -> None:
        proc = self.run_normalizer(INVALID_AMBIGUOUS)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")
        self.assertIn("pending-or-present", payload["message"])

    def test_authority_transfer_fails(self) -> None:
        proc = self.run_normalizer(INVALID_AUTHORITY)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")
        self.assertIn("authority_boundary.authority_transfer must be false", payload["message"])

    def test_duplicate_key_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "duplicate.json"
            path.write_text('{"cbo_version":"0.1","cbo_version":"0.1"}', encoding="utf-8", newline="\n")
            proc = self.run_normalizer(path)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")

    def test_bom_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bom.json"
            path.write_bytes(b"\xef\xbb\xbf{}")
            proc = self.run_normalizer(path)
            self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
            payload = json.loads(proc.stdout)
            self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")


if __name__ == "__main__":
    unittest.main()
