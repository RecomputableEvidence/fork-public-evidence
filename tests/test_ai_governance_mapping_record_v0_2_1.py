import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_ai_governance_mapping_record_v0_2_1.py"
SCHEMA = REPO_ROOT / "schemas" / "ai_governance_system_mapping_record_v0_2_1.schema.json"
RECORDS = REPO_ROOT / "examples" / "ai_governance_system_mapping" / "records_v0_2_1"


def run_checker(record_name: str, schema_path: Path = SCHEMA, normalized: bool = False):
    with tempfile.TemporaryDirectory() as td:
        output = Path(td) / "result.json"
        normalized_output = Path(td) / "normalized_result.json"
        cmd = [
            sys.executable,
            str(CHECKER),
            "--record",
            str(RECORDS / record_name),
            "--schema",
            str(schema_path),
            "--output",
            str(output),
        ]
        if normalized:
            cmd.extend(["--normalized-output", str(normalized_output)])
        proc = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if not output.is_file():
            raise AssertionError(f"checker did not write output. stdout={proc.stdout} stderr={proc.stderr}")
        payload = json.loads(output.read_text(encoding="utf-8"))
        normalized_payload = None
        if normalized:
            normalized_payload = json.loads(normalized_output.read_text(encoding="utf-8"))
        return proc, payload, normalized_payload


def run_checker_for_temp_record(record_text: str):
    with tempfile.TemporaryDirectory() as td:
        record = Path(td) / "record.json"
        output = Path(td) / "result.json"
        record.write_text(record_text, encoding="utf-8")
        proc = subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--record",
                str(record),
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


class TestAIGovernanceMappingRecordCheckerV021(unittest.TestCase):
    def test_valid_fork_record_passes_and_normalizes(self):
        proc, payload, normalized = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_1.json", normalized=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(payload["overall_status"], "PASS")
        self.assertEqual(normalized["overall_status"], "PASS")
        self.assertEqual(normalized["checker_version"], "v0.2.1")
        for excluded in ["checked_at_utc", "environment", "record_path", "schema_path", "record_size_bytes", "schema_size_bytes"]:
            self.assertNotIn(excluded, normalized)

    def test_duplicate_id_fails(self):
        proc, payload, _ = run_checker("INVALID_DUPLICATE_ID_v0_2_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(any(c["check_id"] == "UNIQUE_BOUNDARY_ITEM_IDS" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_safe_handoff_self_reference_fails(self):
        proc, payload, _ = run_checker("INVALID_SAFE_HANDOFF_SELF_REFERENCE_v0_2_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(payload["overall_status"], "FAIL")
        self.assertTrue(any(c["check_id"] == "SAFE_HANDOFF_SELF_REFERENCE_GUARD" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_combined_failure_mode_reports_multiple_failures(self):
        proc, payload, _ = run_checker("INVALID_COMBINED_FAILURE_MODES_v0_2_1.json")
        self.assertEqual(proc.returncode, 1)
        failed = {c["check_id"] for c in payload["checks"] if c["status"] == "FAIL"}
        self.assertIn("SCHEMA_EQUIVALENT_VALIDATION", failed)
        self.assertIn("RESTRICTED_AUTHORITY_CLAIM_GUARD", failed)
        self.assertIn("SAFE_HANDOFF_ID_REFERENCE_INTEGRITY", failed)
        self.assertGreaterEqual(len(failed), 3)

    def test_schema_version_mismatch_fails(self):
        proc, payload, _ = run_checker("INVALID_SCHEMA_VERSION_MISMATCH_v0_2_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "SCHEMA_VERSION_PIN" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_unicode_restricted_claim_bypass_fails(self):
        proc, payload, _ = run_checker("INVALID_UNICODE_RESTRICTED_CLAIM_BYPASS_v0_2_1.json")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "RESTRICTED_AUTHORITY_CLAIM_GUARD" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_active_unresolved_unknown_is_indeterminate(self):
        proc, payload, _ = run_checker("INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2_1.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["overall_status"], "INDETERMINATE")
        self.assertTrue(any(c["check_id"] == "INDETERMINATE_SIGNALS" and c["status"] == "INDETERMINATE" for c in payload["checks"]))

    def test_missing_schema_file_fails_gracefully(self):
        missing_schema = Path(tempfile.gettempdir()) / "missing_ai_governance_schema_v0_2_1.schema.json"
        if missing_schema.exists():
            missing_schema.unlink()
        proc, payload, _ = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_1.json", schema_path=missing_schema)
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "SCHEMA_FILE_PRESENT" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_empty_object_fails_required_fields(self):
        proc, payload = run_checker_for_temp_record("{}\n")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "REQUIRED_FIELDS_PRESENT" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_non_object_json_fails_parse_contract(self):
        proc, payload = run_checker_for_temp_record("[]\n")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "JSON_PARSE" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_malformed_json_fails_parse_contract(self):
        proc, payload = run_checker_for_temp_record("{\n")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(any(c["check_id"] == "JSON_PARSE" and c["status"] == "FAIL" for c in payload["checks"]))

    def test_checker_and_schema_files_exist(self):
        self.assertTrue(CHECKER.is_file())
        self.assertTrue(SCHEMA.is_file())


if __name__ == "__main__":
    unittest.main()