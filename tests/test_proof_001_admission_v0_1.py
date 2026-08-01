from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_proof_001_admission_v0_1.py"
SPEC = importlib.util.spec_from_file_location("proof_001_admission_checker", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def copy_surface(tmp_path: Path) -> Path:
    for relative in (CHECKER.ADMISSION, CHECKER.STANDING, CHECKER.MANIFEST, CHECKER.INDEX, CHECKER.WRAPPER):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    return tmp_path


def codes(findings: list[dict[str, str]]) -> set[str]:
    return {item["code"] for item in findings}


def test_clean_admission_candidate_conforms() -> None:
    assert CHECKER.verify(ROOT, run_wrapper=False) == []


def test_wider_portfolio_cannot_inherit_admission(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.ADMISSION
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["admission_effect"]["wider_proof_portfolio_admitted"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_ADMISSION_SEMANTICS_INVALID" in codes(CHECKER.verify(root, run_wrapper=False))


def test_exterior_correction_cannot_be_erased(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.ADMISSION
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["exterior_recomputation"]["disposition"] = "REPRODUCED"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_ADMISSION_SEMANTICS_INVALID" in codes(CHECKER.verify(root, run_wrapper=False))


def test_original_packaging_standing_cannot_be_rewritten(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.STANDING
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["packaging_candidate"]["standing"] = "ADMITTED"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "ORIGINAL_PACKAGING_STANDING_REWRITTEN" in codes(CHECKER.verify(root, run_wrapper=False))


def test_mutation_role_is_required(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.MANIFEST
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["bindings"] = [item for item in payload["bindings"] if item.get("role") != "UNDERLYING_ADVERSARIAL_REGISTER"]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_MANIFEST_REQUIRED_ROLE_MISSING" in codes(CHECKER.verify(root, run_wrapper=False))
