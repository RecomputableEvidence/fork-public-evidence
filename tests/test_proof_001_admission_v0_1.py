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
    package_destination = tmp_path / CHECKER.PACKAGE
    package_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / CHECKER.PACKAGE, package_destination)
    for relative in (
        CHECKER.ADMISSION,
        CHECKER.ADMISSION_INDEX,
        CHECKER.INDEX,
        CHECKER.WRAPPER,
    ):
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
    assert "PROOF_ADMISSION_SEMANTICS_INVALID" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )


def test_exterior_correction_cannot_be_erased(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.ADMISSION
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["exterior_recomputation"]["disposition"] = "REPRODUCED"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_ADMISSION_SEMANTICS_INVALID" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )


def test_original_packaging_standing_cannot_be_rewritten(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.STANDING
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["packaging_candidate"]["standing"] = "ADMITTED"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "ORIGINAL_PACKAGING_STANDING_REWRITTEN" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )


def test_mutation_role_is_required(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.MANIFEST
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["bindings"] = [
        item
        for item in payload["bindings"]
        if item.get("role") != "UNDERLYING_ADVERSARIAL_REGISTER"
    ]
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_MANIFEST_REQUIRED_ROLE_MISSING" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )


def test_admission_cannot_be_inserted_into_preserved_package(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    intruder = root / CHECKER.PACKAGE / "ADMISSION.json"
    intruder.write_text("{}\n", encoding="utf-8")
    assert "PRESERVED_PACKAGE_FILE_SET_CHANGED" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )


def test_construction_index_cannot_become_admission_index(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.INDEX
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["proofs"][0]["admission_path"] = CHECKER.ADMISSION.as_posix()
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    findings = CHECKER.verify(root, run_wrapper=False)
    assert "CONSTRUCTION_INDEX_REWRITTEN" in codes(findings)
    assert "CONSTRUCTION_INDEX_ENTRY_CHANGED" in codes(findings)


def test_successor_admission_index_cannot_promote_portfolio(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.ADMISSION_INDEX
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["proof_admissions"][0]["wider_portfolio_admitted"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    assert "PROOF_ADMISSION_INDEX_INVALID" in codes(
        CHECKER.verify(root, run_wrapper=False)
    )
