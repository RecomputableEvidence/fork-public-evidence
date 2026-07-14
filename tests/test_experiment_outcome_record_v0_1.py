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

class OutcomeRecordTests(unittest.TestCase):
    def test_favorable_and_unfavorable_both_conform(self):
        for name in ["01_favorable_professional_recognition.json", "02_unfavorable_independently_reproduced_defect.json"]:
            self.assertEqual("CONFORMING", run(VALID / name, ROOT)["state"])

    def test_polarity_collapse_is_rejected(self):
        res = run(INVALID / "02_unfavorable_demoted_after_repair.json", ROOT)
        codes = {d["code"] for d in res["defects"]}
        self.assertIn("POLARITY_STANDING_COLLAPSE", codes)
        self.assertIn("UNFAVORABLE_OUTCOME_AUTOMATICALLY_DEMOTED", codes)

    def test_historical_overwrite_is_rejected(self):
        res = run(INVALID / "03_historical_failure_overwritten.json", ROOT)
        self.assertIn("HISTORICAL_OUTCOME_OVERWRITTEN", {d["code"] for d in res["defects"]})

if __name__ == "__main__":
    unittest.main()
