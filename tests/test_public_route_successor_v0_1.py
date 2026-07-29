from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_public_route_successor_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("public_route_successor", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_proof_first_route_successor_candidate_conforms() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == (
        "PUBLIC_PROOF_FIRST_ROUTE_SUCCESSOR_CANDIDATE_CONFORMS_NOT_ADMITTED"
    )
    assert result["checkpoint"] == "723aa9aee8c329f760bcdabd323fd471a916e822"
