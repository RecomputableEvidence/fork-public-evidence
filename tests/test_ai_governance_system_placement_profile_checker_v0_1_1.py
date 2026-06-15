import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_ai_governance_system_placement_profile_v0_1_1.py"
SCHEMA = ROOT / "schemas" / "ai_governance_system_placement_profile_v0_1.schema.json"
FIXTURES_V01 = ROOT / "examples" / "ai_governance_system_placement_profile" / "records_v0_1"
FIXTURES_V011 = ROOT / "examples" / "ai_governance_system_placement_profile" / "records_v0_1_1"
OUTPUT_DIR = ROOT / "output" / "ai_governance_system_placement_profile_checks_v0_1_1"
DOC = ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_CHECKER_HARDENING_v0_1_1.md"
GUIDE = ROOT / "docs" / "AI_GOVERNANCE_SYSTEM_PLACEMENT_PROFILE_NORMALIZED_OUTPUT_COMPARISON_GUIDE_v0_1_1.md"

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
    "invalid_unicode_restricted_claim_bypass": "FAIL",
}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_checker(record_path, output_path=None, normalized_path=None, schema=SCHEMA, timeout=20):
    cmd = [sys.executable, str(CHECKER), "--record", str(record_path), "--schema", str(schema)]
    if output_path:
        cmd += ["--output", str(output_path)]
    if normalized_path:
        cmd += ["--normalized-output", str(normalized_path)]
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def load_checker_module():
    spec = importlib.util.spec_from_file_location("placement_profile_checker_v011", CHECKER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestAIGovernanceSystemPlacementProfileCheckerV011(unittest.TestCase):
    def test_checker_docs_and_outputs_exist(self):
        self.assertTrue(CHECKER.exists())
        self.assertTrue(SCHEMA.exists())
        self.assertTrue(DOC.exists())
        self.assertTrue(GUIDE.exists())
        self.assertTrue(OUTPUT_DIR.exists())

    def test_committed_fixture_outputs_have_expected_statuses(self):
        for stem, expected_status in EXPECTED.items():
            result = load_json(OUTPUT_DIR / f"{stem}_result.json")
            normalized = load_json(OUTPUT_DIR / f"{stem}_normalized_result.json")
            self.assertEqual(result["overall_status"], expected_status, stem)
            self.assertEqual(normalized["overall_status"], expected_status, stem)
            self.assertNotIn("environment", normalized)
            self.assertNotIn("checked_at_utc", normalized)
            self.assertNotIn("record_path", normalized)
            self.assertNotIn("schema_path", normalized)

    def test_unicode_restricted_claim_bypass_fails(self):
        result = load_json(OUTPUT_DIR / "invalid_unicode_restricted_claim_bypass_result.json")
        guard = next(c for c in result["checks"] if c["check_id"] == "RESTRICTED_AUTHORITY_CLAIM_GUARD")
        self.assertEqual(result["overall_status"], "FAIL")
        self.assertEqual(guard["status"], "FAIL")
        self.assertEqual(guard["error_code"], "ERR_RESTRICTED_AUTHORITY_CLAIM")
        hits = guard["details"]["hits"]
        self.assertTrue(any("compliance" in hit["matched_text"] or "legally" in hit["matched_text"] or "approved" in hit["matched_text"] for hit in hits))

    def test_exit_code_contract_is_documented_and_enforced(self):
        doc = DOC.read_text(encoding="utf-8")
        self.assertIn("PASS = 0", doc)
        self.assertIn("FAIL = 1", doc)
        self.assertIn("INDETERMINATE = 2", doc)
        valid = run_checker(FIXTURES_V01 / "VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json")
        invalid = run_checker(FIXTURES_V01 / "INVALID_DUPLICATE_ID_v0_1.json")
        indeterminate = run_checker(FIXTURES_V01 / "INDETERMINATE_ACTIVE_UNRESOLVED_UNKNOWN_v0_1.json")
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        self.assertEqual(invalid.returncode, 1, invalid.stdout + invalid.stderr)
        self.assertEqual(indeterminate.returncode, 2, indeterminate.stdout + indeterminate.stderr)

    def test_parser_boundary_fuzz_inputs_fail_safely(self):
        module = load_checker_module()
        cases = {
            "empty.json": ("", "ERR_JSON_PARSE"),
            "null.json": ("null\n", "ERR_JSON_TOP_LEVEL_NOT_OBJECT"),
            "boolean.json": ("true\n", "ERR_JSON_TOP_LEVEL_NOT_OBJECT"),
            "number.json": ("123\n", "ERR_JSON_TOP_LEVEL_NOT_OBJECT"),
            "array.json": ("[]\n", "ERR_JSON_TOP_LEVEL_NOT_OBJECT"),
            "malformed.json": ("{\n", "ERR_JSON_PARSE"),
            "malformed_escape.json": ('{"profile_version": "\\uZZZZ"}\n', "ERR_JSON_PARSE"),
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            for filename, (content, expected_error) in cases.items():
                record_path = tmpdir / filename
                record_path.write_text(content, encoding="utf-8")
                record, parse_error = module.load_json_record(record_path)
                checks = module.run_checks(record, record_path, SCHEMA)
                if parse_error is not None:
                    for item in checks:
                        if item["check_id"] == "JSON_PARSE" and item["status"] == "FAIL":
                            item["details"] = {"parse_error": parse_error}
                result = module.make_result(record if isinstance(record, dict) else None, record_path, SCHEMA, checks)
                self.assertEqual(result["overall_status"], "FAIL", filename)
                parse_check = next(c for c in result["checks"] if c["check_id"] == "JSON_PARSE")
                self.assertEqual(parse_check["status"], "FAIL")
                self.assertEqual(parse_check["error_code"], expected_error)

    def test_missing_schema_path_edge_cases_fail(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            valid = FIXTURES_V01 / "VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json"
            missing_schema = tmpdir / "missing.schema.json"
            dir_schema = tmpdir / "schema-directory"
            dir_schema.mkdir()
            for schema_path in [missing_schema, dir_schema]:
                output = tmpdir / (schema_path.name + ".result.json")
                proc = run_checker(valid, output_path=output, schema=schema_path)
                self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
                result = load_json(output)
                check = next(c for c in result["checks"] if c["check_id"] == "SCHEMA_FILE_PRESENT")
                self.assertEqual(check["status"], "FAIL")
                self.assertEqual(check["error_code"], "ERR_SCHEMA_FILE_MISSING")

    def test_normalized_output_comparison_guide_and_determinism(self):
        guide = GUIDE.read_text(encoding="utf-8")
        for phrase in ["Semantic fields retained", "Environment-specific fields excluded", "checked_at_utc", "record_path", "schema_path"]:
            self.assertIn(phrase, guide)
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            norm_a = tmpdir / "a.json"
            norm_b = tmpdir / "b.json"
            record = FIXTURES_V01 / "VALID_MONITORING_SYSTEM_PLACEMENT_v0_1.json"
            proc_a = run_checker(record, normalized_path=norm_a)
            proc_b = run_checker(record, normalized_path=norm_b)
            self.assertEqual(proc_a.returncode, 0, proc_a.stdout + proc_a.stderr)
            self.assertEqual(proc_b.returncode, 0, proc_b.stdout + proc_b.stderr)
            self.assertEqual(norm_a.read_text(encoding="utf-8"), norm_b.read_text(encoding="utf-8"))

    def test_large_synthetic_record_performance_smoke(self):
        base = load_json(FIXTURES_V01 / "VALID_EVALUATION_SYSTEM_PLACEMENT_v0_1.json")
        evidence_id = base["evidence_inputs"][0]["evidence_input_id"]
        claims = []
        for index in range(1000):
            claims.append({
                "claim_id": f"claim:large_record:{index:04d}",
                "statement": f"Large synthetic placement claim {index:04d} remains bounded to declared evidence.",
                "scope": "synthetic performance smoke test",
                "evidence_basis": [evidence_id],
                "conditions": ["synthetic local performance fixture"],
                "limitations": ["not a real governance claim"],
            })
        base["supported_claims"] = claims
        base["evidence_outputs"][0]["supports_claim_ids"] = [claim["claim_id"] for claim in claims]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            record = tmpdir / "large.json"
            output = tmpdir / "large.result.json"
            record.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")
            start = time.perf_counter()
            proc = run_checker(record, output_path=output, timeout=15)
            elapsed = time.perf_counter() - start
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertLess(elapsed, 10.0, f"large-record smoke test took {elapsed:.3f}s")

    def test_overclaim_language_regression_for_outputs(self):
        for path in OUTPUT_DIR.glob("*_result.json"):
            if path.name.endswith("_normalized_result.json"):
                continue
            result = load_json(path)
            self.assertEqual(result["claim_boundary"], "STRUCTURAL_AND_BOUNDARY_VALIDATION_ONLY")
            for item in result["non_claims"]:
                self.assertTrue(item.startswith("Does not "), f"non-claim must remain negative: {item}")
            status_text = result["status_meaning"].lower()
            forbidden_positive = ["certified", "compliant", "admissible", "approved", "audit-ready", "regulator-ready"]
            for term in forbidden_positive:
                self.assertNotIn(term, status_text, f"positive overclaim term {term} leaked into status_meaning for {path}")

    def test_missing_schema_file_still_fails_gracefully_in_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "result.json"
            missing_schema = Path(tmpdir) / "missing.schema.json"
            proc = run_checker(FIXTURES_V01 / "VALID_COMPLIANCE_MAPPING_PLACEMENT_v0_1.json", output_path=output, schema=missing_schema)
            self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
            result = load_json(output)
            check = next(c for c in result["checks"] if c["check_id"] == "SCHEMA_FILE_PRESENT")
            self.assertEqual(check["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()