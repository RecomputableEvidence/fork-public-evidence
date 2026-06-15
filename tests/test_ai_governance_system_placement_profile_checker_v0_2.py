import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_ai_governance_system_placement_profile_v0_2.py"
SCHEMA = ROOT / "schemas" / "ai_governance_system_placement_profile_v0_1.schema.json"
RECORDS = ROOT / "examples" / "ai_governance_system_placement_profile" / "records_v0_1"
OUTPUT = ROOT / "output" / "ai_governance_system_placement_profile_structural_execution_receipts_v0_2"

VALID_RECORD = RECORDS / "VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json"
INVALID_RECORD = RECORDS / "INVALID_CLAIM_NONCLAIM_OVERLAP_v0_1.json"
INDETERMINATE_RECORD = RECORDS / "INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_1.json"

VALID_NORMALIZED = OUTPUT / "valid_evaluation_system_placement_normalized_result.json"
VALID_RECEIPT = OUTPUT / "valid_evaluation_system_placement_structural_execution_receipt.json"
TAMPERED_NORMALIZED = OUTPUT / "tampered_valid_evaluation_system_placement_normalized_result.json"
MALFORMED_RECEIPT = OUTPUT / "malformed_receipt_v0_2.json"
MISSING_HASH_RECEIPT = OUTPUT / "missing_receipt_hash_v0_2.json"
WRONG_ALGORITHM_RECEIPT = OUTPUT / "wrong_hash_algorithm_v0_2.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def deterministic_hash(obj) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def run_tool(args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(TOOL), *map(str, args)],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class TestPlacementProfileStructuralExecutionReceiptsV02(unittest.TestCase):
    def test_files_exist(self):
        expected = [
            TOOL,
            SCHEMA,
            VALID_RECORD,
            INVALID_RECORD,
            INDETERMINATE_RECORD,
            VALID_RECEIPT,
            VALID_NORMALIZED,
            ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_STRUCTURAL_EXECUTION_RECEIPTS_v0_2_IMPLEMENTATION.md",
        ]
        for path in expected:
            self.assertTrue(path.exists(), f"Missing expected artifact: {path}")

    def test_receipt_has_required_bounded_fields(self):
        receipt = load_json(VALID_RECEIPT)
        required = [
            "receipt_type",
            "receipt_artifact_name",
            "receipt_version",
            "receipt_status",
            "checker_id",
            "checker_version",
            "schema_id",
            "schema_version",
            "record_id",
            "system_id",
            "overall_status",
            "checker_exit_code",
            "hash_algorithm",
            "normalized_output_sha256",
            "normalized_output_hash_scope",
            "receipt_environment_fields_excluded_from_hash",
            "non_claims",
        ]
        for field in required:
            self.assertIn(field, receipt)

        self.assertEqual(receipt["receipt_type"], "STRUCTURAL_EXECUTION_RECEIPT")
        self.assertEqual(receipt["receipt_artifact_name"], "Structural Execution Receipt")
        self.assertEqual(receipt["hash_algorithm"], "sha256")
        self.assertEqual(receipt["normalized_output_hash_scope"], "NORMALIZED_CHECKER_OUTPUT_ONLY")
        self.assertEqual(receipt["receipt_status"], "EMITTED")
        self.assertRegex(receipt["normalized_output_sha256"], r"^[0-9a-f]{64}$")

        serialized = json.dumps(receipt, sort_keys=True)
        self.assertNotIn(str(ROOT), serialized)
        self.assertNotIn("C:\\", serialized)
        self.assertNotIn("/mnt/", serialized)

    def test_receipt_hash_matches_committed_normalized_output(self):
        normalized = load_json(VALID_NORMALIZED)
        receipt = load_json(VALID_RECEIPT)
        self.assertEqual(deterministic_hash(normalized), receipt["normalized_output_sha256"])

    def test_receipt_emission_preserves_checker_exit_codes(self):
        cases = [
            (VALID_RECORD, 0, "valid"),
            (INVALID_RECORD, 1, "invalid"),
            (INDETERMINATE_RECORD, 2, "indeterminate"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            for record, expected_code, stem in cases:
                proc = run_tool([
                    "--record", record,
                    "--schema", SCHEMA,
                    "--output", tmpdir / f"{stem}_result.json",
                    "--normalized-output", tmpdir / f"{stem}_normalized.json",
                    "--emit-receipt", tmpdir / f"{stem}_receipt.json",
                ])
                self.assertEqual(proc.returncode, expected_code, proc.stderr + proc.stdout)
                self.assertTrue((tmpdir / f"{stem}_receipt.json").exists())
                receipt = load_json(tmpdir / f"{stem}_receipt.json")
                self.assertEqual(receipt["checker_exit_code"], expected_code)

    def test_normalized_output_hash_comparison_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            match_output = tmpdir / "match.json"
            mismatch_output = tmpdir / "mismatch.json"

            match = run_tool([
                "--normalized-output", VALID_NORMALIZED,
                "--verify-receipt", VALID_RECEIPT,
                "--receipt-verification-output", match_output,
            ])
            self.assertEqual(match.returncode, 0, match.stderr + match.stdout)
            self.assertEqual(load_json(match_output)["verification_status"], "NORMALIZED_OUTPUT_HASH_MATCH")

            mismatch = run_tool([
                "--normalized-output", TAMPERED_NORMALIZED,
                "--verify-receipt", VALID_RECEIPT,
                "--receipt-verification-output", mismatch_output,
            ])
            self.assertEqual(mismatch.returncode, 1, mismatch.stderr + mismatch.stdout)
            self.assertEqual(load_json(mismatch_output)["verification_status"], "NORMALIZED_OUTPUT_HASH_MISMATCH")

    def test_full_source_recompute_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            match_output = tmpdir / "full_match.json"
            recomputed_normalized = tmpdir / "recomputed_normalized.json"

            match = run_tool([
                "--record", VALID_RECORD,
                "--schema", SCHEMA,
                "--verify-receipt", VALID_RECEIPT,
                "--full-recompute",
                "--normalized-output", recomputed_normalized,
                "--receipt-verification-output", match_output,
            ])
            self.assertEqual(match.returncode, 0, match.stderr + match.stdout)
            self.assertEqual(load_json(match_output)["verification_status"], "FULL_RECOMPUTE_MATCH")

            mismatch_output = tmpdir / "full_mismatch.json"
            mismatch = run_tool([
                "--record", INVALID_RECORD,
                "--schema", SCHEMA,
                "--verify-receipt", VALID_RECEIPT,
                "--full-recompute",
                "--normalized-output", tmpdir / "invalid_recomputed_normalized.json",
                "--receipt-verification-output", mismatch_output,
            ])
            self.assertEqual(mismatch.returncode, 1, mismatch.stderr + mismatch.stdout)
            self.assertEqual(load_json(mismatch_output)["verification_status"], "FULL_RECOMPUTE_MISMATCH")

    def test_invalid_receipts_fail_safely(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmpdir = Path(tmp)
            cases = [
                MALFORMED_RECEIPT,
                MISSING_HASH_RECEIPT,
                WRONG_ALGORITHM_RECEIPT,
            ]
            for receipt in cases:
                out = tmpdir / f"{receipt.stem}_verification.json"
                proc = run_tool([
                    "--normalized-output", VALID_NORMALIZED,
                    "--verify-receipt", receipt,
                    "--receipt-verification-output", out,
                ])
                self.assertEqual(proc.returncode, 1)
                result = load_json(out)
                self.assertEqual(result["verification_status"], "RECEIPT_INVALID")
                self.assertIn("errors", result)

    def test_non_claims_are_preserved(self):
        receipt = load_json(VALID_RECEIPT)
        non_claims = "\n".join(receipt["non_claims"])
        required_phrases = [
            "semantic truth",
            "legal sufficiency",
            "compliance sufficiency",
            "audit sufficiency",
            "model safety",
            "runtime enforcement",
            "external artifact existence",
            "cross-record graph validation",
            "institutional authority",
            "governance sufficiency",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, non_claims)

    def test_docs_preserve_structural_execution_receipt_terminology(self):
        doc = (ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_STRUCTURAL_EXECUTION_RECEIPTS_v0_2_IMPLEMENTATION.md").read_text(encoding="utf-8-sig")
        self.assertIn("Structural Execution Receipt", doc)
        self.assertIn("Checker Hash Receipt", doc)
        self.assertIn("NORMALIZED_CHECKER_OUTPUT_ONLY", doc)
        self.assertIn("FULL_SOURCE_RECOMPUTE", doc)
        self.assertIn("does not validate semantic truth", doc)
        self.assertIn("does not validate legal sufficiency", doc)
        self.assertIn("does not grant institutional authority", doc)

    def test_no_schema_change_is_introduced(self):
        schema_v02 = ROOT / "schemas" / "ai_governance_system_placement_profile_v0_2.schema.json"
        self.assertFalse(schema_v02.exists(), "v0.2 receipts should not introduce a Placement Profile schema change.")


if __name__ == "__main__":
    unittest.main()
