from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2_1.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v021_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

V2 = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.2"
CASE = V2 / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ForkCadCorrectionSuccessorV021Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.events = load(CASE / "OBSERVABLE_EVENT_REGISTER_v0_2.json")
        self.ledger = load(CASE / "CLAIM_LEDGER_v0_2.json")
        self.effects = load(V2 / "CONTROL_EFFECTS_v0_2.json")

    def claim(self, cid: str):
        return next(c for c in self.ledger["claims"] if c["claim_id"] == cid)

    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_exterior_residual_out_of_band_event_fields_rejected(self) -> None:
        event = next(e for e in self.events["events"] if e["source_role"] == "MODEL_SELF_REPORT")
        event["verified_mechanism_confidence"] = "HIGH"
        event["mechanism_established_by_reviewer"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register_v0_2_1(self.events)

    def test_exterior_residual_non_claude_self_report_causal_promotion_rejected(self) -> None:
        event = copy.deepcopy(next(e for e in self.events["events"] if e["source_role"] == "MODEL_SELF_REPORT"))
        event["event_id"] = "CAD-004-E999"
        event["statement_origin"] = "GPT-4"
        event["causal_standing"] = "MECHANISM_CONFIRMED_BY_SELF_REPORT"
        self.events["events"].append(event)
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register_v0_2_1(self.events)

    def test_model_self_report_unresolved_rule_is_origin_agnostic(self) -> None:
        event = copy.deepcopy(next(e for e in self.events["events"] if e["source_role"] == "MODEL_SELF_REPORT"))
        event["event_id"] = "CAD-004-E998"
        event["statement_origin"] = "OTHER_MODEL"
        event["causal_standing"] = "UNRESOLVED"
        self.events["events"].append(event)
        CHECKER.validate_event_register_v0_2_1(self.events)

    def test_c005_supported_scope_cannot_be_promoted(self) -> None:
        self.claim("CAD-004-C005")["current_disposition"] = "FULLY_ESTABLISHED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.PREDECESSOR.validate_claim_ledger(self.ledger)

    def test_c008_cannot_create_automatic_proof_promotion(self) -> None:
        self.claim("CAD-004-C008")["automatic_proof_promotion"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.PREDECESSOR.validate_claim_ledger(self.ledger)

    def test_every_control_effect_field_is_mechanically_fixed(self) -> None:
        for key, original in list(self.effects.items()):
            if isinstance(original, bool):
                mutated = not original
            elif isinstance(original, int):
                mutated = original + 1
            elif isinstance(original, str):
                mutated = original + "_MUTATED"
            else:
                self.fail(f"unexpected CONTROL_EFFECTS value type for {key}: {type(original)}")
            candidate = copy.deepcopy(self.effects)
            candidate[key] = mutated
            with self.subTest(key=key):
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.PREDECESSOR.validate_control_effects(candidate)

    def test_event_schema_requires_all_controlled_keys(self) -> None:
        del self.events["events"][0]["causal_standing"]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register_v0_2_1(self.events)


if __name__ == "__main__":
    unittest.main()
