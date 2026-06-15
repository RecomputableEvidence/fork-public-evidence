import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_ai_governance_mapping_record_v0_1.py"
SCHEMA = REPO_ROOT / "schemas" / "ai_governance_system_mapping_record_v0_1.schema.json"
RECORDS = REPO_ROOT / "examples" / "ai_governance_system_mapping" / "records"


def run_checker(record_name: str):
    with tempfile.TemporaryDirectory() as td:
        output = Path(td) / "result.json"
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
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        payload = json.loads(output.read_text(encoding="utf-8"))
        return proc, payload


class TestAIGovernanceMappingRecordCheckerV01(unittest.TestCase):
    def test_valid_fork_record_passes(self):
        proc, payload = run_checker("VALID_FORK_MAPPING_RECORD_v0_1.json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(payload["overall_status"], "PASS")
        self.assertFalse(payload["errors"])

    def test_missing_non_claims_fails(self):
        proc, payload = run_checker("INVALID_MISSING_NON_CLAIMS_v0_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(
            any(c["check_id"] == "EXPLICIT_NON_CLAIMS_PRESENT" and c["status"] == "FAIL" for c in payload["checks"])
        )

    def test_claim_leakage_fails(self):
        proc, payload = run_checker("INVALID_CLAIM_LEAKAGE_v0_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(
            any(c["check_id"] == "CLAIM_NONCLAIM_DISJOINT" and c["status"] == "FAIL" for c in payload["checks"])
        )

    def test_unresolved_dependency_is_indeterminate(self):
        proc, payload = run_checker("INDETERMINATE_UNRESOLVED_DEPENDENCY_v0_1.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["overall_status"], "INDETERMINATE")
        self.assertTrue(
            any(c["check_id"] == "INDETERMINATE_SIGNALS" and c["status"] == "INDETERMINATE" for c in payload["checks"])
        )

    def test_checker_and_schema_files_exist(self):
        self.assertTrue(CHECKER.is_file())
        self.assertTrue(SCHEMA.is_file())


if __name__ == "__main__":
    unittest.main()