from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_fork_cad_candidate_v0_1.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ForkCadCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case_dir = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.1/cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
        self.manifest = json.loads((self.case_dir / "SOURCE_MANIFEST_v0_1.json").read_text(encoding="utf-8"))
        self.supplement = json.loads((self.case_dir / "SOURCE_MANIFEST_SUPPLEMENT_001_v0_1.json").read_text(encoding="utf-8"))
        self.ledger = json.loads((self.case_dir / "CLAIM_LEDGER_v0_1.json").read_text(encoding="utf-8"))
        self.events = json.loads((self.case_dir / "OBSERVABLE_EVENT_REGISTER_SUPPLEMENT_001_v0_1.json").read_text(encoding="utf-8"))

    def all_source_ids(self) -> set[str]:
        base = CHECKER.validate_manifest(self.manifest)
        return base | CHECKER.validate_manifest_supplement(self.supplement, base)

    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_unknown_source_reference_fails(self) -> None:
        self.ledger["claims"][0]["source_refs"].append("SRC-999")
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_ledger(self.ledger, self.all_source_ids())

    def test_canonicalization_flag_fails(self) -> None:
        self.ledger["candidate_classifications_are_canonical"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_ledger(self.ledger, self.all_source_ids())

    def test_duplicate_supplement_source_fails(self) -> None:
        self.supplement["sources"][0]["source_id"] = "SRC-001"
        base = CHECKER.validate_manifest(self.manifest)
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_manifest_supplement(self.supplement, base)

    def test_model_self_report_cannot_verify_mechanism(self) -> None:
        event = next(item for item in self.events["events"] if item["event_type"] == "MODEL_CAUSAL_SELF_REPORT")
        event["mechanism_verified"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register(self.events, self.all_source_ids())


if __name__ == "__main__":
    unittest.main()
