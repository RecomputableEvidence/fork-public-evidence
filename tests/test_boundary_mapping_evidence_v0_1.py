import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_boundary_mapping_evidence.py"
EXAMPLE_DIR = REPO_ROOT / "examples" / "fork_boundary_mapping_evidence"


class BoundaryMappingEvidenceCheckerTests(unittest.TestCase):
    def run_checker(self, *paths):
        cmd = [sys.executable, str(CHECKER)]
        cmd.extend(str(path) for path in paths)
        return subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_all_boundary_mapping_examples_pass(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "STRUCTURAL_PASS")
        self.assertEqual(payload["record_count"], 3)

        determinations = {record["determination"] for record in payload["records"]}
        self.assertEqual(determinations, {"STRUCTURAL_PASS"})

    def test_expected_boundary_mapping_examples_are_present(self):
        expected = {
            "agent_tool_permission_to_action_authority_v0_1.json",
            "benchmark_to_deployment_safety_v0_1.json",
            "vendor_report_to_compliance_status_v0_1.json",
        }
        actual = {path.name for path in EXAMPLE_DIR.glob("*.json")}
        self.assertEqual(expected, actual)

    def test_missing_non_inheritance_result_fails(self):
        source = EXAMPLE_DIR / "agent_tool_permission_to_action_authority_v0_1.json"
        record = json.loads(source.read_text(encoding="utf-8"))
        record["fork_non_inheritance_result"] = []

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_missing_non_inheritance.json"
            invalid_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

            result = self.run_checker(invalid_path)
            self.assertNotEqual(result.returncode, 0)

            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "STRUCTURAL_FAIL")
            flattened_errors = [
                error["code"]
                for checked_record in payload["records"]
                for error in checked_record["errors"]
            ]
            self.assertIn("MISSING_AUTHORITY_NON_INHERITANCE_RESULT", flattened_errors)

    def test_missing_legal_sufficiency_non_claim_fails(self):
        source = EXAMPLE_DIR / "benchmark_to_deployment_safety_v0_1.json"
        record = json.loads(source.read_text(encoding="utf-8"))
        record["non_claims"] = [
            item for item in record["non_claims"]
            if "legal sufficiency" not in item.lower()
        ]

        with tempfile.TemporaryDirectory() as tmp:
            invalid_path = Path(tmp) / "invalid_missing_legal_non_claim.json"
            invalid_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

            result = self.run_checker(invalid_path)
            self.assertNotEqual(result.returncode, 0)

            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "STRUCTURAL_FAIL")
            flattened_errors = [
                error["code"]
                for checked_record in payload["records"]
                for error in checked_record["errors"]
            ]
            self.assertIn("MISSING_LEGAL_SUFFICIENCY_NON_CLAIM", flattened_errors)


if __name__ == "__main__":
    unittest.main()
