from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_pr101_proof001_admission_anchor_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("pr101_proof001_anchor", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pr101_proof001_admission_anchor_candidate_conforms() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == (
        "PR101_PROOF001_ADMISSION_ANCHOR_CANDIDATE_CONFORMS_NOT_ADMITTED"
    )
    assert result["bound_merge"] == "ded38bf56f950b8813614132c92bf531553a8b34"
    assert result["bound_reviewed_head"] == (
        "a273ab0a95decb0d43f1c091743a72ac4261027e"
    )
