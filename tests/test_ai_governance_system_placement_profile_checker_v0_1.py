import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_ai_governance_system_placement_profile_v0_1.py"
SCHEMA = ROOT / "schemas" / "ai_governance_system_placement_profile_v0_1.schema.json"
FIXTURES = ROOT / "examples" / "ai_governance_system_placement_profile" / "records_v0_1"
OUTPUT_DIR = ROOT / "output" / "ai_governance_system_placement_profile_checks_v0_1"
DOC = ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_CHECKER_v0_1.md"

EXPECTED = {
    "valid_evaluation_system_placement": "PASS",
    "valid_monitoring_system_placement": "PASS",
    "valid_compliance_mapping_placement": "PASS",
    "invalid_missing_required_field": "FAIL",
    "invalid_claim_nonclaim_overlap": "FAIL",
    "invalid_restricted_claim": "FAIL",
    "invalid_duplicate_id": "FAIL",
    "invalid_role_classification": "FAIL",
    "invalid_handoff_reference": "FAIL",
    "indeterminate_active_unresolved_unknown": "INDETERMINATE",
}

EXPECTED_FAILING_CHECKS = {
    "invalid_missing_required_field": ("REQUIRED_FIELDS_PRESENT", "ERR_REQUIRED_FIELDS_MISSING"),
    "invalid_claim_nonclaim_overlap": ("CLAIM_NONCLAIM_DISJOINT", "ERR_CLAIM_NONCLAIM_OVERLAP"),
    "invalid_restricted_claim": ("RESTRICTED_AUTHORITY_CLAIM_GUARD", "ERR_RESTRICTED_AUTHORITY_CLAIM"),
    "invalid_duplicate_id": ("UNIQUE_IDS", "ERR_DUPLICATE_ID"),
    "invalid_role_classification": ("ROLE_CLASSIFICATION_VALID", "ERR_ROLE_CLASSIFICATION_INVALID"),
    "invalid_handoff_reference": ("LOCAL_REFERENCE_INTEGRITY", "ERR_LOCAL_REFERENCE_GAP"),
    "indeterminate_active_unresolved_unknown": ("UNRESOLVED_UNKNOWNS_STATUS", "ERR_ACTIVE_UNRESOLVED_UNKNOWN"),
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_checker(record_name, output_path=None, normalized_path=None, schema=SCHEMA):
    cmd = [sys.executable, str(CHECKER), "--record", str(FIXTURES / record_name), "--schema", str(schema)]
    if output_path:
        cmd += ["--output", str(output_path)]
    if normalized_path:
        cmd += ["--normalized-output", str(normalized_path)]
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=20)


class TestAIGovernanceSystemPlacementProfileCheckerV01(unittest.TestCase):
    def test_checker_schema_doc_and_outputs_exist(self):
        self.assertTrue(CHECKER.exists())
        self.assertTrue(SCHEMA.exists())
        self.assertTrue(DOC.exists())
        self.assertTrue(OUTPUT_DIR.exists())

    def test_committed_fixture_outputs_have_expected_statuses(self):
        for stem, expected_status in EXPECTED.items():
            result_path = OUTPUT_DIR / f"{stem}_result.json"
            normalized_path = OUTPUT_DIR / f"{stem}_normalized_result.json"
            self.assertTrue(result_path.exists(), result_path)
            self.assertTrue(normalized_path.exists(), normalized_path)
            result = load_json(result_path)
            normalized = load_json(normalized_path)
            self.assertEqual(result["overall_status"], expected_status, stem)
            self.assertEqual(normalized["overall_status"], expected_status, stem)
            self.assertNotIn("environment", normalized)
            self.assertNotIn("checked_at_utc", normalized)
            self.assertNotIn("record_path", normalized)
            self.assertNotIn("schema_path", normalized)

    def test_expected_failure_checks_are_reported(self):
        for stem, (check_id, error_code) in EXPECTED_FAILING_CHECKS.items():
            result = load_json(OUTPUT_DIR / f"{stem}_result.json")
            check = next(c for c in result["checks"] if c["check_id"] == check_id)
            if stem.startswith("indeterminate"):
                self.assertEqual(check["status"], "INDETERMINATE")
            else:
                self.assertEqual(check["status"], "FAIL")
            self.assertEqual(check["error_code"], error_code)

    def test_valid_fixture_runs_end_to_end(self):
        proc = run_checker("VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json")
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_V0_1_CHECK_PASS", proc.stdout)

    def test_indeterminate_fixture_exits_two(self):
        proc = run_checker("INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_1.json")
        self.assertEqual(proc.returncode, 2, proc.stdout + proc.stderr)
        self.assertIn("AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_V0_1_CHECK_INDETERMINATE", proc.stdout)

    def test_missing_schema_file_fails_gracefully(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "result.json"
            missing_schema = Path(tmpdir) / "missing.schema.json"
            proc = run_checker("VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json", output_path=output, schema=missing_schema)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            result = load_json(output)
            check = next(c for c in result["checks"] if c["check_id"] == "SCHEMA_FILE_PRESENT")
            self.assertEqual(check["status"], "FAIL")
            self.assertEqual(check["error_code"], "ERR_SCHEMA_FILE_MISSING")

    def test_normalized_output_is_deterministic_across_runs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            norm_a = tmpdir / "a.json"
            norm_b = tmpdir / "b.json"
            proc_a = run_checker("VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json", normalized_path=norm_a)
            proc_b = run_checker("VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json", normalized_path=norm_b)
            self.assertEqual(proc_a.returncode, 0, proc_a.stdout + proc_a.stderr)
            self.assertEqual(proc_b.returncode, 0, proc_b.stdout + proc_b.stderr)
            self.assertEqual(norm_a.read_text(encoding="utf-8"), norm_b.read_text(encoding="utf-8"))

    def test_checker_non_claims_preserve_boundary(self):
        result = load_json(OUTPUT_DIR / "valid_evaluation_system_placement_result.json")
        text = "\n".join(result["non_claims"])
        self.assertIn("Does not validate semantic truth", text)
        self.assertIn("Does not validate legal sufficiency", text)
        self.assertIn("Does not provide runtime enforcement", text)
        self.assertIn("Does not perform cross-record graph validation", text)

    def test_claim_evidence_basis_present_on_valid_fixture(self):
        result = load_json(OUTPUT_DIR / "valid_evaluation_system_placement_result.json")
        check = next(c for c in result["checks"] if c["check_id"] == "CLAIM_EVIDENCE_BASIS_PRESENT")
        self.assertEqual(check["status"], "PASS")


if __name__ == "__main__":
    unittest.main()