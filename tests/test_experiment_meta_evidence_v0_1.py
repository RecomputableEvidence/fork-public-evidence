from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
from check_experiment_meta_evidence_v0_1 import run, validate_single

VALID = ROOT / "fixtures" / "experiment-meta-evidence" / "v0.1" / "valid"
INVALID = ROOT / "fixtures" / "experiment-meta-evidence" / "v0.1" / "invalid"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

import subprocess

EXPECTED = {
    "01_favorable_endorsement_as_validation.json": "TECHNICAL_VALIDATION_INFERRED_FROM_RECOGNITION",
    "02_unfavorable_demoted_after_repair.json": "UNFAVORABLE_OUTCOME_AUTOMATICALLY_DEMOTED",
    "03_historical_failure_overwritten.json": "HISTORICAL_OUTCOME_OVERWRITTEN",
    "04_channel_negative_as_absence.json": "CHANNEL_NEGATIVE_TREATED_AS_ABSENCE",
    "05_prose_as_compiled_behavior.json": "MECHANISM_CLAIM_BELOW_RAW_FILE_FIDELITY",
    "06_raw_file_as_execution.json": "EXECUTION_CLAIM_WITHOUT_P4",
    "07_fork_generated_risk_tier.json": "RISK_TIER_INFERRED_BY_FORK",
    "08_fork_generated_impact_assessment.json": "IMPACT_ASSESSMENT_INFERRED_BY_FORK",
    "09_aims_phase_inferred_from_timestamp.json": "AIMS_PHASE_INFERRED_BY_FORK",
    "10_high_depth_profile_with_p1.json": "DECLARED_PROVENANCE_PROFILE_NOT_SATISFIED",
    "11_participant_quoted_without_authorization.json": "ATTRIBUTION_NOT_AUTHORIZED",
    "12_collaboration_interest_as_partnership.json": "ENDORSEMENT_INFERRED_FROM_PARTICIPATION",
    "13_commercial_interest_as_product_validation.json": "COMMERCIAL_INTEREST_INFERRED_AS_PRODUCT_VALIDATION",
    "14_missing_participant_context.json": "PARTICIPANT_CONTEXT_MISSING",
    "15_missing_interaction_provenance.json": "INTERACTION_PROVENANCE_MISSING",
    "16_broken_lineage_reference.json": "BROKEN_REFERENCE",
    "17_duplicate_outcome_identifier.json": "DUPLICATE_RECORD_ID",
    "18_malformed_registry.json": "MALFORMED_JSON",
    "19_schema_version_mismatch.json": "SCHEMA_VERSION_MISMATCH",
    "20_multiple_simultaneous_defects.json": "POLARITY_STANDING_COLLAPSE",
}

class IntegratedCheckerTests(unittest.TestCase):
    def test_all_valid_fixtures_conform(self):
        for path in sorted(VALID.glob("*.json")):
            with self.subTest(path=path.name):
                self.assertEqual("CONFORMING", run(path, ROOT)["state"])

    def test_all_invalid_fixtures_fail_with_expected_code(self):
        for name, code in EXPECTED.items():
            with self.subTest(path=name):
                res = run(INVALID / name, ROOT)
                self.assertNotEqual("CONFORMING", res["state"])
                self.assertIn(code, {d["code"] for d in res["defects"]})

    def test_output_is_deterministic(self):
        path = INVALID / "20_multiple_simultaneous_defects.json"
        first = json.dumps(run(path, ROOT), sort_keys=True)
        second = json.dumps(run(path, ROOT), sort_keys=True)
        self.assertEqual(first, second)

    def test_exit_codes(self):
        checker = TOOLS / "check_experiment_meta_evidence_v0_1.py"
        good = subprocess.run([sys.executable, str(checker), str(VALID / "02_unfavorable_independently_reproduced_defect.json"), "--json"], cwd=ROOT)
        bad = subprocess.run([sys.executable, str(checker), str(INVALID / "03_historical_failure_overwritten.json"), "--json"], cwd=ROOT)
        self.assertEqual(0, good.returncode)
        self.assertNotEqual(0, bad.returncode)

    def test_multi_defect_aggregation(self):
        res = run(INVALID / "20_multiple_simultaneous_defects.json", ROOT)
        self.assertGreaterEqual(res["defect_count"], 4)

if __name__ == "__main__":
    unittest.main()
