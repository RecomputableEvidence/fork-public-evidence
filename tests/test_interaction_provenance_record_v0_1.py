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

class InteractionProvenanceTests(unittest.TestCase):
    def test_valid_interaction_conforms(self):
        reg = load(VALID / "02_unfavorable_independently_reproduced_defect.json")
        res = validate_single("interaction", reg["interaction_provenance_records"][0], ROOT)
        self.assertEqual("CONFORMING", res["state"])

    def test_missing_interaction_reference_fails(self):
        res = run(INVALID / "15_missing_interaction_provenance.json", ROOT)
        self.assertIn("INTERACTION_PROVENANCE_MISSING", {d["code"] for d in res["defects"]})

if __name__ == "__main__":
    unittest.main()
