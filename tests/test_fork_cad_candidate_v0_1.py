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
    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_unknown_source_reference_fails(self) -> None:
        case_dir = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.1/cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
        manifest = json.loads((case_dir / "SOURCE_MANIFEST_v0_1.json").read_text(encoding="utf-8"))
        ledger = json.loads((case_dir / "CLAIM_LEDGER_v0_1.json").read_text(encoding="utf-8"))
        ledger["claims"][0]["source_refs"].append("SRC-999")
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_ledger(ledger, CHECKER.validate_manifest(manifest))

    def test_canonicalization_flag_fails(self) -> None:
        case_dir = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.1/cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
        manifest = json.loads((case_dir / "SOURCE_MANIFEST_v0_1.json").read_text(encoding="utf-8"))
        ledger = json.loads((case_dir / "CLAIM_LEDGER_v0_1.json").read_text(encoding="utf-8"))
        ledger["candidate_classifications_are_canonical"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_ledger(ledger, CHECKER.validate_manifest(manifest))


if __name__ == "__main__":
    unittest.main()
