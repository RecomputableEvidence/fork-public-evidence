from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "tools" / "check_fork_thesis_manifestation_v0_1.py"
spec = importlib.util.spec_from_file_location("ftm_checker", CHECKER_PATH)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def copied_repo(parent: Path) -> Path:
    target = parent / "repo"
    shutil.copytree(REPO_ROOT, target)
    return target


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class ThesisManifestationCheckerTests(unittest.TestCase):
    def test_exact_candidate_conforms(self) -> None:
        self.assertEqual(checker.check(REPO_ROOT), [])

    def test_duplicate_json_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = copied_repo(Path(directory))
            path = root / "docs/research/fork-thesis-manifestation-v0.1/BASE_COORDINATE_v0_1.json"
            path.write_text('{"candidate_id":"first","candidate_id":"second"}\n', encoding="utf-8")
            errors = checker.check(root)
            self.assertTrue(any("duplicate JSON key" in error for error in errors))

    def test_package_digest_tampering_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = copied_repo(Path(directory))
            path = root / "docs/research/fork-thesis-manifestation-v0.1/ALTERNATIVE_INTERPRETATIONS_AND_FALSIFIERS_v0_1.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nundigested mutation\n", encoding="utf-8")
            errors = checker.check(root)
            self.assertTrue(any("ALTERNATIVE_INTERPRETATIONS_AND_FALSIFIERS_v0_1.md sha256" in error for error in errors))

    def test_causal_promotion_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = copied_repo(Path(directory))
            path = root / "docs/research/fork-thesis-manifestation-v0.1/THESIS_MANIFESTATION_RECORD_v0_1.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["causal_hypothesis"]["status"] = "PROVEN"
            write_json(path, value)
            errors = checker.check(root)
            self.assertTrue(any("causal hypothesis status" in error for error in errors))

    def test_forbidden_effect_promotions_are_rejected(self) -> None:
        mutations = (
            ("pair_001_effects", "pair_001_repetitions_added", 1),
            ("pair_001_effects", "execution_effect", "AUTHORIZED"),
            ("repository_effects", "existing_pull_requests_mutated", True),
        )
        for section, field, value in mutations:
            with self.subTest(section=section, field=field), tempfile.TemporaryDirectory() as directory:
                root = copied_repo(Path(directory))
                path = root / "docs/research/fork-thesis-manifestation-v0.1/NO_ADMISSION_OR_EXECUTION_EFFECT_v0_1.json"
                record = json.loads(path.read_text(encoding="utf-8"))
                record[section][field] = value
                write_json(path, record)
                errors = checker.check(root)
                self.assertTrue(any(field in error for error in errors))

    def test_post_base_case_cannot_be_promoted_to_causal_proof(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = copied_repo(Path(directory))
            path = root / "docs/research/fork-thesis-manifestation-v0.1/THESIS_MANIFESTATION_RECORD_v0_1.json"
            value = json.loads(path.read_text(encoding="utf-8"))
            value["post_base_endogenous_cases"][0]["classification"] = "CAUSAL_PROOF"
            write_json(path, value)
            errors = checker.check(root)
            self.assertTrue(any("endogenous case classification" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
