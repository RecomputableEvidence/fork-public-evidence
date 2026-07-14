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

class AttributionAuthorizationTests(unittest.TestCase):
    def test_authorized_named_attribution_conforms(self):
        self.assertEqual("CONFORMING", run(VALID / "11_authorized_named_attribution.json", ROOT)["state"])

    def test_public_named_without_authorization_fails(self):
        res = run(INVALID / "11_participant_quoted_without_authorization.json", ROOT)
        self.assertIn("ATTRIBUTION_NOT_AUTHORIZED", {d["code"] for d in res["defects"]})

if __name__ == "__main__":
    unittest.main()
