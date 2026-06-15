import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "tools" / "check_ai_governance_mapping_record_v0_2_2.py"
SCHEMA = REPO_ROOT / "schemas" / "ai_governance_system_mapping_record_v0_2_2.schema.json"
RECORDS = REPO_ROOT / "examples" / "ai_governance_system_mapping" / "records_v0_2_2"
DOC = REPO_ROOT / "docs" / "AI_GOVERNANCE_MAPPING_RECORD_CHECKER_HARDENING_v0_2_2.md"
GUIDE = REPO_ROOT / "docs" / "CHECKER_NORMALIZED_OUTPUT_COMPARISON_GUIDE_v0_2_2.md"


def run_checker(record_name: str, schema_path: Path = SCHEMA, normalized: bool = False):
    with tempfile.TemporaryDirectory() as td:
        output = Path(td) / "result.json"
        normalized_output = Path(td) / "normalized_result.json"
        cmd = [sys.executable, str(CHECKER), "--record", str(RECORDS / record_name), "--schema", str(schema_path), "--output", str(output)]
        if normalized:
            cmd.extend(["--normalized-output", str(normalized_output)])
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if not output.is_file():
            raise AssertionError(f"checker did not write output. stdout={proc.stdout} stderr={proc.stderr}")
        payload = json.loads(output.read_text(encoding="utf-8"))
        normalized_payload = None
        if normalized:
            normalized_payload = json.loads(normalized_output.read_text(encoding="utf-8"))
        return proc, payload, normalized_payload


def run_checker_for_temp_record(record_text: str, normalized: bool = False):
    with tempfile.TemporaryDirectory() as td:
        record = Path(td) / "record.json"
        output = Path(td) / "result.json"
        normalized_output = Path(td) / "normalized_result.json"
        record.write_text(record_text, encoding="utf-8")
        cmd = [sys.executable, str(CHECKER), "--record", str(record), "--schema", str(SCHEMA), "--output", str(output)]
        if normalized:
            cmd.extend(["--normalized-output", str(normalized_output)])
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        payload = json.loads(output.read_text(encoding="utf-8"))
        normalized_payload = json.loads(normalized_output.read_text(encoding="utf-8")) if normalized else None
        return proc, payload, normalized_payload


def failed_check(payload, check_id):
    return next((c for c in payload["checks"] if c["check_id"] == check_id and c["status"] == "FAIL"), None)


class TestAIGovernanceMappingRecordCheckerV022(unittest.TestCase):
    def test_valid_fork_record_passes_and_normalizes(self):
        proc, payload, normalized = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_2.json", normalized=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(payload["overall_status"], "PASS")
        self.assertEqual(normalized["overall_status"], "PASS")
        self.assertEqual(normalized["checker_version"], "v0.2.2")
        for excluded in ["checked_at_utc", "environment", "record_path", "schema_path", "record_size_bytes", "schema_size_bytes"]:
            self.assertNotIn(excluded, normalized)

    def test_normalized_output_is_deterministic_across_runs(self):
        _, _, normalized_a = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_2.json", normalized=True)
        _, _, normalized_b = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_2.json", normalized=True)
        self.assertEqual(normalized_a, normalized_b)

    def test_duplicate_id_fails_with_static_error_code(self):
        proc, payload, _ = run_checker("INVALID_DUPLICATE_ID_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "UNIQUE_BOUNDARY_ITEM_IDS")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_DUPLICATE_OR_MISSING_ID")
        self.assertTrue(any(e["error_code"] == "ERR_DUPLICATE_OR_MISSING_ID" for e in payload["errors"]))

    def test_safe_handoff_self_reference_fails(self):
        proc, payload, _ = run_checker("INVALID_SAFE_HANDOFF_SELF_REFERENCE_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "SAFE_HANDOFF_SELF_REFERENCE_GUARD")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_SAFE_HANDOFF_SELF_REFERENCE")

    def test_local_multi_hop_handoff_cycle_fails(self):
        proc, payload, _ = run_checker("INVALID_LOCAL_HANDOFF_CYCLE_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "LOCAL_HANDOFF_CYCLE_GUARD")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_LOCAL_HANDOFF_CYCLE")

    def test_combined_failure_mode_reports_multiple_failures_and_error_codes(self):
        proc, payload, _ = run_checker("INVALID_COMBINED_FAILURE_MODES_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        failed = {c["check_id"] for c in payload["checks"] if c["status"] == "FAIL"}
        self.assertIn("SCHEMA_EQUIVALENT_VALIDATION", failed)
        self.assertIn("RESTRICTED_AUTHORITY_CLAIM_GUARD", failed)
        self.assertIn("SAFE_HANDOFF_ID_REFERENCE_INTEGRITY", failed)
        self.assertGreaterEqual(len(failed), 3)
        self.assertTrue(all("error_code" in e for e in payload["errors"]))

    def test_schema_version_downgrade_fails(self):
        proc, payload, _ = run_checker("INVALID_SCHEMA_VERSION_DOWNGRADE_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "SCHEMA_VERSION_PIN")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_SCHEMA_VERSION_MISMATCH")

    def test_unicode_restricted_claim_bypass_fails(self):
        proc, payload, _ = run_checker("INVALID_UNICODE_RESTRICTED_CLAIM_BYPASS_v0_2_2.json")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "RESTRICTED_AUTHORITY_CLAIM_GUARD")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_RESTRICTED_AUTHORITY_CLAIM")

    def test_active_unresolved_unknown_is_indeterminate(self):
        proc, payload, _ = run_checker("INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_2_2.json")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(payload["overall_status"], "INDETERMINATE")
        self.assertTrue(any(c["check_id"] == "INDETERMINATE_SIGNALS" and c["status"] == "INDETERMINATE" for c in payload["checks"]))

    def test_missing_schema_file_fails_gracefully(self):
        missing_schema = Path(tempfile.gettempdir()) / "missing_ai_governance_schema_v0_2_2.schema.json"
        if missing_schema.exists():
            missing_schema.unlink()
        proc, payload, _ = run_checker("VALID_FORK_MAPPING_RECORD_v0_2_2.json", schema_path=missing_schema)
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "SCHEMA_FILE_PRESENT")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_SCHEMA_FILE_MISSING")

    def test_empty_object_fails_required_fields(self):
        proc, payload, _ = run_checker_for_temp_record("{}\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIsNotNone(failed_check(payload, "REQUIRED_FIELDS_PRESENT"))

    def test_non_object_json_fails_parse_contract(self):
        proc, payload, _ = run_checker_for_temp_record("[]\n")
        self.assertEqual(proc.returncode, 1)
        check = failed_check(payload, "JSON_PARSE")
        self.assertIsNotNone(check)
        self.assertEqual(check["error_code"], "ERR_JSON_PARSE")

    def test_malformed_json_fails_parse_contract(self):
        proc, payload, _ = run_checker_for_temp_record("{\n")
        self.assertEqual(proc.returncode, 1)
        self.assertIsNotNone(failed_check(payload, "JSON_PARSE"))

    def test_malformed_escape_fails_parse_contract(self):
        proc, payload, _ = run_checker_for_temp_record('{"record_version": "bad\\uZZZZ"}\n')
        self.assertEqual(proc.returncode, 1)
        self.assertIsNotNone(failed_check(payload, "JSON_PARSE"))

    def test_large_synthetic_record_performance_smoke(self):
        base = json.loads((RECORDS / "VALID_FORK_MAPPING_RECORD_v0_2_2.json").read_text(encoding="utf-8"))
        base["supported_claims"] = [
            {"id": f"SUPPORTED_CLAIM_LARGE_{i:04d}", "statement": f"Fork can preserve bounded evidence item {i}."}
            for i in range(350)
        ]
        base["safe_handoffs"][0]["allowed_claim_ids"] = [item["id"] for item in base["supported_claims"]]
        with tempfile.TemporaryDirectory() as td:
            record = Path(td) / "large_record.json"
            output = Path(td) / "large_result.json"
            record.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")
            start = time.perf_counter()
            proc = subprocess.run([sys.executable, str(CHECKER), "--record", str(record), "--schema", str(SCHEMA), "--output", str(output)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            elapsed = time.perf_counter() - start
            payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(payload["overall_status"], "PASS")
        self.assertLess(elapsed, 15.0)

    def test_v022_docs_preserve_overclaim_boundary(self):
        text = DOC.read_text(encoding="utf-8").lower()
        self.assertIn("does not expand fork into a policy engine", text)
        self.assertIn("not a cross-record dag compiler", text)
        self.assertIn("not semantic intent detection", text)
        risky_phrases = [
            "legally admissible evidence",
            "compliance certified",
            "audit sufficient record",
            "regulator approved",
            "production ready governance system",
        ]
        for phrase in risky_phrases:
            self.assertNotIn(phrase, text)

    def test_output_comparison_guide_exists_and_states_exclusions(self):
        self.assertTrue(GUIDE.is_file())
        text = GUIDE.read_text(encoding="utf-8").lower()
        self.assertIn("checked_at_utc", text)
        self.assertIn("environment.platform", text)
        self.assertIn("does not prove legal admissibility", text)

    def test_checker_and_schema_files_exist(self):
        self.assertTrue(CHECKER.is_file())
        self.assertTrue(SCHEMA.is_file())


if __name__ == "__main__":
    unittest.main()
