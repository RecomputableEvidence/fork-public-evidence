from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from csh_evidence_common_v0_1 import (
    check_execution_receipt,
    check_integrated_manifest,
    check_pair_comparison,
    check_reviewer_receipt,
    check_run_classification,
)

FIXTURES = ROOT / "fixtures" / "cross-system-claim-handoff" / "post-repair-evidence-v0_1"


def json_files(path: Path):
    return sorted(
        item for item in path.rglob("*.json")
        if "raw" not in item.parts and "config" not in item.parts
    )


class FixtureContractMixin:
    checker = None
    valid_dir: Path
    invalid_dir: Path

    def test_valid_fixtures(self):
        files = json_files(self.valid_dir)
        self.assertTrue(files, f"No valid fixtures under {self.valid_dir}")
        for path in files:
            with self.subTest(path=path):
                errors = self.checker(path, ROOT)
                self.assertEqual([], errors, "\n".join(errors))

    def test_invalid_fixtures(self):
        files = json_files(self.invalid_dir)
        self.assertTrue(files, f"No invalid fixtures under {self.invalid_dir}")
        for path in files:
            with self.subTest(path=path):
                errors = self.checker(path, ROOT)
                self.assertTrue(errors, f"Expected rejection for {path}")