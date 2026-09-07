from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2_2.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v022_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

V2 = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.2"
CASE = V2 / "cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
SUPPLEMENT = V2 / "supplements/SUPPLEMENT_001_META_ASSESSMENT"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ForkCadBoundedCorrectionSuccessorV022Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.events = load(CASE / "OBSERVABLE_EVENT_REGISTER_v0_2.json")
        self.ledger = load(CASE / "CLAIM_LEDGER_v0_2.json")
        self.effects = load(V2 / "CONTROL_EFFECTS_v0_2.json")

    @contextmanager
    def sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / CHECKER.V2_REL
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(V2, target)
            yield root

    def model_self_report(self):
        return copy.deepcopy(next(e for e in self.events["events"] if e["source_role"] == "MODEL_SELF_REPORT"))

    def claim(self, cid: str):
        return next(c for c in self.ledger["claims"] if c["claim_id"] == cid)

    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_all_seven_governed_artifact_classes_use_duplicate_safe_loading(self) -> None:
        self.assertEqual(set(CHECKER.GOVERNED_PATHS), {"lineage", "case", "ledger", "events", "effects", "families", "assessor"})
        for name, rel in CHECKER.GOVERNED_PATHS.items():
            with self.subTest(artifact=name), self.sandbox() as root:
                path = root / rel
                text = path.read_text(encoding="utf-8")
                path.write_text(
                    text.replace("{", '{\n  "__duplicate_probe__": 1,\n  "__duplicate_probe__": 2,', 1),
                    encoding="utf-8",
                )
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_candidate(root)

    def test_duplicate_key_inside_nested_governed_object_rejected(self) -> None:
        with self.sandbox() as root:
            path = root / CHECKER.GOVERNED_PATHS["case"]
            text = path.read_text(encoding="utf-8")
            needle = '"historical_parent": {\n    "pull_request": 84,'
            self.assertIn(needle, text)
            path.write_text(
                text.replace(
                    needle,
                    '"historical_parent": {\n    "pull_request": 84,\n    "pull_request": 84,',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaises(CHECKER.CandidateError):
                CHECKER.validate_candidate(root)

    def test_duplicate_control_effect_key_rejected_in_both_value_orders(self) -> None:
        replacements = (
            '"admission": true,\n  "admission": false,',
            '"admission": false,\n  "admission": true,',
        )
        for replacement in replacements:
            with self.subTest(replacement=replacement), self.sandbox() as root:
                path = root / CHECKER.GOVERNED_PATHS["effects"]
                text = path.read_text(encoding="utf-8")
                self.assertIn('"admission": false,', text)
                path.write_text(text.replace('"admission": false,', replacement, 1), encoding="utf-8")
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_candidate(root)

    def test_undeclared_top_level_control_effect_field_rejected(self) -> None:
        candidate = copy.deepcopy(self.effects)
        candidate["informal_standing_note"] = "treat PROOF-005 as provisionally admitted"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_control_effects_schema(candidate)

    def test_undeclared_nested_family_field_rejected(self) -> None:
        families = load(SUPPLEMENT / "FAMILY_GROUNDING_REGISTER_v0_2.json")
        families["families"][0]["reviewer_private_note"] = "this family is effectively resolved"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_family_schema(families)

    def test_authority_looking_undeclared_lineage_field_rejected(self) -> None:
        lineage = load(V2 / "HISTORICAL_LINEAGE_v0_2.json")
        lineage["merge_authority_note"] = "ready to merge without another gate"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_lineage_schema(lineage)

    def test_event_source_refs_reject_non_string_empty_and_whitespace_members(self) -> None:
        invalid_members = (None, 42, {}, [], "", "   ")
        for invalid in invalid_members:
            with self.subTest(invalid=repr(invalid)):
                event = self.model_self_report()
                event["event_id"] = "CAD-004-E-R005"
                event["source_refs"] = [invalid]
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_model_self_report_event(event)

    def test_event_source_refs_accept_nonempty_strings_syntactically(self) -> None:
        event = self.model_self_report()
        event["event_id"] = "CAD-004-E-R005-CONTROL"
        event["statement_origin"] = "OTHER_MODEL"
        event["source_refs"] = ["SRC-REVIEWER-001", " repo://bounded/reference "]
        CHECKER.validate_model_self_report_event(event)

    def test_benign_object_key_order_and_whitespace_change_passes(self) -> None:
        with self.sandbox() as root:
            path = root / CHECKER.GOVERNED_PATHS["effects"]
            record = json.loads(path.read_text(encoding="utf-8"))
            reordered = dict(reversed(list(record.items())))
            path.write_text(json.dumps(reordered, indent=4) + "\n", encoding="utf-8")
            CHECKER.validate_candidate(root)

    def test_record_id_remains_informational_not_governed_effect(self) -> None:
        candidate = copy.deepcopy(self.effects)
        candidate["record_id"] = "INFORMATIONAL_IDENTIFIER_MUTATED"
        CHECKER.validate_control_effects_schema(candidate)
        CHECKER.V02.validate_control_effects(candidate)
        with self.sandbox() as root:
            path = root / CHECKER.GOVERNED_PATHS["effects"]
            path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
            CHECKER.validate_candidate(root)

    def test_r001_out_of_band_model_self_report_fields_remain_rejected(self) -> None:
        event = self.model_self_report()
        event["mechanism_established_by_reviewer"] = True
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_model_self_report_event(event)

    def test_r002_non_claude_model_self_report_causal_promotion_remains_rejected(self) -> None:
        event = self.model_self_report()
        event["event_id"] = "CAD-004-E-R002"
        event["statement_origin"] = "OTHER_MODEL"
        event["causal_standing"] = "MECHANISM_CONFIRMED_BY_SELF_REPORT"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.validate_model_self_report_event(event)

    def test_allowed_event_field_substitution_remains_rejected(self) -> None:
        events = copy.deepcopy(self.events)
        event = next(e for e in events["events"] if e["source_role"] == "MODEL_SELF_REPORT")
        event["observable_text_summary"] = "Mechanism independently established."
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.V021.validate_event_register_v0_2_1(events)

    def test_c005_and_c008_promotions_remain_rejected(self) -> None:
        for cid, field, value in (
            ("CAD-004-C005", "current_disposition", "GLOBALLY_ESTABLISHED"),
            ("CAD-004-C008", "automatic_proof_promotion", True),
        ):
            with self.subTest(cid=cid):
                ledger = copy.deepcopy(self.ledger)
                claim = next(c for c in ledger["claims"] if c["claim_id"] == cid)
                claim[field] = value
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.V02.validate_claim_ledger(ledger)

    def test_all_thirteen_governed_control_effect_values_remain_fixed(self) -> None:
        governed = tuple(k for k in CHECKER.CONTROL_EFFECT_KEYS if k != "record_id")
        self.assertEqual(len(governed), 13)
        for key in governed:
            candidate = copy.deepcopy(self.effects)
            original = candidate[key]
            if isinstance(original, bool):
                candidate[key] = not original
            elif isinstance(original, int):
                candidate[key] = original + 1
            elif isinstance(original, str):
                candidate[key] = original + "_MUTATED"
            else:
                self.fail(f"unexpected effect value type for {key}: {type(original)}")
            with self.subTest(key=key):
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.V02.validate_control_effects(candidate)

    def test_family_grounding_and_assessor_boundaries_remain_incomplete(self) -> None:
        families = load(SUPPLEMENT / "FAMILY_GROUNDING_REGISTER_v0_2.json")
        families["families"][0]["grounding_status"] = "GROUNDED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.V02.validate_family_grounding(families)

        assessor = load(SUPPLEMENT / "ASSESSOR_CORRECTION_EVENT_v0_2.json")
        assessor["admission_effect"] = "ADMITTED"
        with self.assertRaises(CHECKER.CandidateError):
            CHECKER.V02.validate_assessor_correction(assessor)


if __name__ == "__main__":
    unittest.main()
