import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_ai_governance_mapping_record_v0_2.py"
SCHEMA = REPO_ROOT / "schemas" / "ai_governance_system_mapping_record_v0_2.schema.json"
RECORDS = REPO_ROOT / "examples" / "ai_governance_system_mapping" / "records_v0_2"


def run_checker(record_name: str):
    with tempfile.TemporaryDirectory() as td:
        output = Path(td) / "result.json"
        normalized = Path(td) / "normalized_result.json"
        proc = subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--record",
                str(RECORDS / record_name),
                "--schema",
                str(SCHEMA),
                "--output",
                str(output),
                "--normalized-output",
                str(normalized),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        payload = json.loads(output.read_text(encoding="utf-8"))
        normalized_payload = json.loads(normalized.read_text(encoding="utf-8"))
        return proc, payload, normalized_payload


class TestAIGovernanceMappingRecordCheckerV02(unittest.TestCase):
    def test_valid_fork_record_passes(self):
        proc, payload, normalized = run_checker("VALID_FORK_MAPPING_RECORD_v0_2.json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(payload["overall_status"], "PASS")
        self.assertEqual(normalized["overall_status"], "PASS")
        self.assertFalse(payload["errors"])

    def test_paraphrased_claim_inheritance_fails(self):
        proc, payload, _ = run_checker("INVALID_PARAPHRASED_CLAIM_INHERITANCE_v0_2.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(
            any(c["check_id"] == "RESTRICTED_AUTHORITY_CLAIM_GUARD" and c["status"] == "FAIL" for c in payload["checks"])
        )

    def test_safe_handoff_reference_gap_fails(self):
        proc, payload, _ = run_checker("INVALID_SAFE_HANDOFF_REFERENCE_GAP_v0_2.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(
            any(c["check_id"] == "SAFE_HANDOFF_ID_REFERENCE_INTEGRITY" and c["status"] == "FAIL" for c in payload["checks"])
        )

    def test_nested_schema_violation_fails(self):
        proc, payload, _ = run_checker("INVALID_SCHEMA_NESTED_ADDITIONAL_PROPERTY_v0_2.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(
            any(c["check_id"] == "SCHEMA_EQUIVALENT_VALIDATION" and c["status"] == "FAIL" for c in payload["checks"])
        )

    def test_active_unresolved_unknown_is_indeterminate(self):
        proc, payload, _ = run_checker("INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["overall_status"], "INDETERMINATE")
        self.assertTrue(
            any(c["check_id"] == "INDETERMINATE_SIGNALS" and c["status"] == "INDETERMINATE" for c in payload["checks"])
        )

    def test_normalized_result_excludes_environment_specific_fields(self):
        proc, payload, normalized = run_checker("VALID_FORK_MAPPING_RECORD_v0_2.json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        for field in ["checked_at_utc", "record_path", "schema_path", "environment", "record_size_bytes", "schema_size_bytes"]:
            self.assertNotIn(field, normalized)
        self.assertIn("record_sha256", normalized)
        self.assertIn("schema_sha256", normalized)
        self.assertEqual(normalized["checks"], payload["checks"])

    def test_checker_and_schema_files_exist(self):
        self.assertTrue(CHECKER.is_file())
        self.assertTrue(SCHEMA.is_file())


if __name__ == "__main__":
    unittest.main()