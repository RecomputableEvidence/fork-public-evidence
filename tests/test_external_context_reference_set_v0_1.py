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

class ExternalContextTests(unittest.TestCase):
    def test_external_context_is_opaque_and_valid(self):
        self.assertEqual("CONFORMING", run(VALID / "09_external_context_supplied.json", ROOT)["state"])

    def test_fork_inferred_risk_is_rejected(self):
        res = run(INVALID / "07_fork_generated_risk_tier.json", ROOT)
        self.assertIn("RISK_TIER_INFERRED_BY_FORK", {d["code"] for d in res["defects"]})

    def test_declared_profile_is_enforced_without_selecting_it(self):
        res = run(INVALID / "10_high_depth_profile_with_p1.json", ROOT)
        self.assertIn("DECLARED_PROVENANCE_PROFILE_NOT_SATISFIED", {d["code"] for d in res["defects"]})

if __name__ == "__main__":
    unittest.main()
