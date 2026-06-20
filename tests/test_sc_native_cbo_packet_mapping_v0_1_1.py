from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NORMALIZER = ROOT / "tools" / "normalize_sc_native_cbo_packet.py"
CHECKER = ROOT / "tools" / "check_cbo_minimum_packet.py"
VALID_003 = ROOT / "examples" / "sc_native_cbo_packet" / "sc_workload_003_recomputable_subject_v0_1_1.json"
INVALID_MISSING_SUBJECT = ROOT / "examples" / "sc_native_cbo_packet" / "invalid_recompute_missing_subject_v0_1_1.json"
INVALID_CANONICALIZATION = ROOT / "examples" / "sc_native_cbo_packet" / "invalid_unsupported_canonicalization_v0_1_1.json"


def expected_digest_for_workload_003() -> str:
    payload = {
        "authority_transfer": False,
        "continuity_identity": "CID-003",
        "execution_state": "EMITTED",
        "issuer": "Supreme Computation",
        "workload_id": "sc-workload-003",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


class ScNativeCboRecomputableSubjectTests(unittest.TestCase):
    def run_normalizer(self, path: Path, out: Path | None = None) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(NORMALIZER), str(path)]
        if out is not None:
            command.extend(["--out", str(out)])
        else:
            command.append("--compact")
        return subprocess.run(command, text=True, capture_output=True)

    def test_recomputable_subject_normalizes_with_computed_digest(self) -> None:
        proc = self.run_normalizer(VALID_003)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        expected = expected_digest_for_workload_003()
        self.assertEqual(payload["integrity_metadata"]["digest_status"], "PRESENT")
        self.assertEqual(payload["integrity_metadata"]["digest_value"], expected)
        self.assertEqual(payload["recomputation_metadata"]["computed_digest_value"], expected)
        self.assertEqual(payload["recomputation_metadata"]["canonicalization_method"], "UTF8_JSON_MINIFIED_SORTED_KEYS")
        self.assertIn("seal://sc/workload-003", payload["integrity_metadata"]["seal_refs"])
        self.assertFalse(payload["boundary_semantics"]["fork_validates_issuer_governance"])
        self.assertTrue(payload["boundary_semantics"]["issuer_invariant_refs_are_opaque_to_fork"])

    def test_recomputed_normalized_packet_passes_cbo_checker(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "normalized.json"
            proc = self.run_normalizer(VALID_003, out=out)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            meta = json.loads(proc.stdout)
            self.assertTrue(meta["recomputation_performed"])
            self.assertEqual(meta["computed_digest_value"], expected_digest_for_workload_003())

            check = subprocess.run(
                [sys.executable, str(CHECKER), str(out), "--compact"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            payload = json.loads(check.stdout)
            self.assertTrue(payload["result"]["ok"])
            self.assertEqual(payload["result"]["computed_outcome"], "CBO_MINIMUM_PACKET_STRUCTURALLY_VALID")

    def test_recompute_instruction_without_digest_subject_fails(self) -> None:
        proc = self.run_normalizer(INVALID_MISSING_SUBJECT)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")
        self.assertIn("digest_subject", payload["message"])

    def test_unsupported_canonicalization_fails(self) -> None:
        proc = self.run_normalizer(INVALID_CANONICALIZATION)
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["computed_outcome"], "SC_NATIVE_CBO_MAPPING_INPUT_ERROR")
        self.assertIn("Unsupported canonicalization_method", payload["message"])


if __name__ == "__main__":
    unittest.main()
