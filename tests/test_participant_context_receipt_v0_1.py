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

class ParticipantContextTests(unittest.TestCase):
    def test_valid_participant_conforms(self):
        reg = load(VALID / "11_authorized_named_attribution.json")
        res = validate_single("participant", reg["participant_context_receipts"][0], ROOT)
        self.assertEqual("CONFORMING", res["state"])

    def test_missing_participant_reference_fails(self):
        res = run(INVALID / "14_missing_participant_context.json", ROOT)
        self.assertIn("PARTICIPANT_CONTEXT_MISSING", {d["code"] for d in res["defects"]})

if __name__ == "__main__":
    unittest.main()
