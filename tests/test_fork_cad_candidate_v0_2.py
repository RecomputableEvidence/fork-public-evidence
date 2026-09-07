from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v02_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

V2 = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.2"
CASE = V2 / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
SUPP = V2 / "supplements/SUPPLEMENT_001_META_ASSESSMENT"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ForkCadCorrectionSuccessorV02Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.lineage = load(V2 / "HISTORICAL_LINEAGE_v0_2.json")
        self.case = load(CASE / "CASE_RECORD_v0_2.json")
        self.ledger = load(CASE / "CLAIM_LEDGER_v0_2.json")
        self.events = load(CASE / "OBSERVABLE_EVENT_REGISTER_v0_2.json")
        self.effects = load(V2 / "CONTROL_EFFECTS_v0_2.json")
        self.families = load(SUPP / "FAMILY_GROUNDING_REGISTER_v0_2.json")
        self.assessor = load(SUPP / "ASSESSOR_CORRECTION_EVENT_v0_2.json")

    def claim(self, cid: str):
        return next(c for c in self.ledger["claims"] if c["claim_id"] == cid)

    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_historical_pr84_cannot_be_rewritten_or_direct_merged(self) -> None:
        item = next(x for x in self.lineage["historical_surfaces"] if x["pull_request"] == 84)
        item["rewritten"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_lineage(self.lineage)

    def test_case_admission_promotion_fails(self) -> None:
        self.case["admission_effect"] = "ADMITTED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_case_record(self.case)

    def test_case_provider_call_promotion_fails(self) -> None:
        self.case["provider_calls_performed"] = 99
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_case_record(self.case)

    def test_access_state_cannot_be_recollapsed(self) -> None:
        del self.claim("CAD-004-C001")["dimensions"]["EARLIER_TURN_ACCESS"]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_attributed_execution_cannot_be_promoted_without_receipt(self) -> None:
        c2 = self.claim("CAD-004-C002")
        c2["current_disposition"] = "VERIFIED_EXECUTION"
        c2["verified_execution_receipt_present"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_role_binding_cannot_be_collapsed_to_one_role(self) -> None:
        self.claim("CAD-004-C003")["roles"] = ["TAXONOMY_DISCUSSION_CONTENT"]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_scope_equivalence_cannot_be_promoted(self) -> None:
        self.claim("CAD-004-C004")["scope_equivalence_established"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_register_presence_cannot_become_behavioral_influence(self) -> None:
        self.claim("CAD-004-C006")["behavioral_influence"] = "ESTABLISHED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_artifact_presence_cannot_become_completeness(self) -> None:
        self.claim("CAD-004-C007")["completeness"]["contextual"] = "COMPLETE"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_claim_ledger(self.ledger)

    def test_event_origin_is_required(self) -> None:
        del self.events["events"][0]["statement_origin"]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register(self.events)

    def test_event_observable_summary_is_required(self) -> None:
        del self.events["events"][0]["observable_text_summary"]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register(self.events)

    def test_renamed_model_self_report_cannot_verify_mechanism(self) -> None:
        event = next(e for e in self.events["events"] if e["source_role"] == "MODEL_SELF_REPORT")
        event["event_type"] = "TEXTUAL_CORRECTION"
        event["mechanism_verified"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register(self.events)

    def test_undeclared_event_type_fails(self) -> None:
        self.events["events"][0]["event_type"] = "RENAMED_SELF_REPORT"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_event_register(self.events)

    def test_pair001_execution_promotion_fails(self) -> None:
        self.effects["pair_001_effect"] = "EXECUTED"
        self.effects["pair_001_execution_authorized"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_control_effects(self.effects)

    def test_readiness_promotion_fails(self) -> None:
        self.effects["readiness_effect"] = "READY"
        self.effects["readiness_promoted"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_control_effects(self.effects)

    def test_proof_admission_promotion_fails(self) -> None:
        self.effects["proof_admission_effect"] = "ADMITTED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_control_effects(self.effects)

    def test_family_grounding_cannot_be_claimed_complete_without_sources(self) -> None:
        self.families["families"][0]["grounding_status"] = "COMPLETE"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_family_grounding(self.families)

    def test_family_source_spans_cannot_be_invented_inside_incomplete_successor(self) -> None:
        self.families["families"][0]["source_spans"] = [{"source_id": "SRC-X", "span": "1-10"}]
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_family_grounding(self.families)

    def test_family_case_ids_cannot_be_assigned(self) -> None:
        self.families["canonical_case_ids_assigned"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_family_grounding(self.families)

    def test_unresolved_artifact_existence_cannot_be_promoted_to_absence(self) -> None:
        q = self.families["unresolved_artifact_question"]
        q["disposition"] = "ARTIFACT_ABSENT"
        q["absence_inferred"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_family_grounding(self.families)

    def test_assessor_correction_cannot_claim_complete_binding_without_source_ref(self) -> None:
        self.assessor["status"] = "CORRECTION_BOUND"
        self.assessor["binding_state"] = "COMPLETE"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_assessor_correction(self.assessor)

    def test_assessor_correction_cannot_invent_source_ref(self) -> None:
        self.assessor["source_addressable_original_statement_ref"] = {"path": "unknown", "span": "unknown"}
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_assessor_correction(self.assessor)


if __name__ == "__main__":
    unittest.main()
