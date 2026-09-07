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
CHECKER_PATH = ROOT / "tools/check_fork_cad_candidate_v0_2_3.py"
SPEC = importlib.util.spec_from_file_location("fork_cad_v023_checker", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

V2 = ROOT / "docs/meta-evidence/conversational-authority-drift-v0.2"
EFFECTS = V2 / "CONTROL_EFFECTS_v0_2.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ForkCadF3TypeStrictnessSuccessorV023Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.effects = load(EFFECTS)

    @contextmanager
    def sandbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / CHECKER.V022.V2_REL
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(V2, target)
            yield root

    def write_effects(self, root: Path, candidate: dict) -> None:
        path = root / CHECKER.V022.GOVERNED_PATHS["effects"]
        path.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")

    def test_repository_candidate_passes(self) -> None:
        CHECKER.validate_candidate(ROOT)

    def test_f3_governs_exactly_thirteen_effect_fields_and_excludes_record_id(self) -> None:
        governed = set(CHECKER.V022.CONTROL_EFFECT_KEYS) - {"record_id"}
        self.assertEqual(len(governed), 13)
        self.assertEqual(governed, set(CHECKER.EXPECTED_CONTROL_EFFECTS))

    def test_predecessor_reproduces_bool_for_int_f3_gap_but_successor_rejects(self) -> None:
        candidate = copy.deepcopy(self.effects)
        candidate["provider_calls"] = False
        with self.sandbox() as root:
            self.write_effects(root, candidate)
            CHECKER.V022.validate_candidate(root)
            with self.assertRaises(CHECKER.CandidateError):
                CHECKER.validate_candidate(root)

    def test_predecessor_reproduces_int_for_bool_f3_gap_but_successor_rejects(self) -> None:
        bool_fields = (
            "admission",
            "publication",
            "endorsement",
            "pair_001_execution_authorized",
            "readiness_promoted",
        )
        for key in bool_fields:
            with self.subTest(key=key), self.sandbox() as root:
                candidate = copy.deepcopy(self.effects)
                candidate[key] = 0
                self.write_effects(root, candidate)
                CHECKER.V022.validate_candidate(root)
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_candidate(root)

    def test_python_equal_float_zero_is_also_rejected_by_exact_type_boundary(self) -> None:
        for key in ("provider_calls", "admission", "publication", "endorsement", "pair_001_execution_authorized", "readiness_promoted"):
            with self.subTest(key=key), self.sandbox() as root:
                candidate = copy.deepcopy(self.effects)
                candidate[key] = 0.0
                self.write_effects(root, candidate)
                CHECKER.V022.validate_candidate(root)
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_candidate(root)

    def test_correct_canonical_types_and_values_pass(self) -> None:
        CHECKER.validate_control_effect_type_strictness(copy.deepcopy(self.effects))
        self.assertIs(type(self.effects["provider_calls"]), int)
        for key in (
            "admission",
            "publication",
            "endorsement",
            "pair_001_execution_authorized",
            "readiness_promoted",
        ):
            self.assertIs(type(self.effects[key]), bool)

    def test_escalated_values_remain_rejected(self) -> None:
        mutations = {
            "admission": True,
            "publication": True,
            "endorsement": True,
            "provider_calls": 1,
            "pair_001_execution_authorized": True,
            "readiness_promoted": True,
            "authority_effect": "GRANTED",
        }
        for key, value in mutations.items():
            with self.subTest(key=key), self.sandbox() as root:
                candidate = copy.deepcopy(self.effects)
                candidate[key] = value
                self.write_effects(root, candidate)
                with self.assertRaises(CHECKER.CandidateError):
                    CHECKER.validate_candidate(root)

    def test_record_id_remains_informational_and_outside_f3(self) -> None:
        candidate = copy.deepcopy(self.effects)
        candidate["record_id"] = "INFORMATIONAL_IDENTIFIER_MUTATED_V023"
        with self.sandbox() as root:
            self.write_effects(root, candidate)
            CHECKER.validate_candidate(root)

    def test_f2_unicode_source_ref_behavior_is_deliberately_unchanged(self) -> None:
        event = {"event_id": "F2-NON-SCOPE-CONTROL", "source_refs": ["\u200b"]}
        CHECKER.V022.validate_event_source_refs(event)

    def test_predecessor_candidate_still_passes_before_f3_layer(self) -> None:
        CHECKER.V022.validate_candidate(ROOT)


if __name__ == "__main__":
    unittest.main()
