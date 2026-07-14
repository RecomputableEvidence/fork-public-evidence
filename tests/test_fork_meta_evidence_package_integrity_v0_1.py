from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = REPO_ROOT / "tools/check_fork_meta_evidence_package_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_fork_meta_evidence_package_v0_1",
        CHECKER_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_canonical_package_integrity_passes():
    checker = load_checker()
    result = checker.verify_package(REPO_ROOT)
    assert result["state"] == "CONFORMING"
    assert result["defect_count"] == 0
    assert result["entry_count"] == 60
    assert result["entries_passed"] == 60


def test_tampered_file_is_detected(tmp_path: Path):
    checker = load_checker()

    payload = tmp_path / "payload.txt"
    payload.write_text("original\n", encoding="utf-8")

    expected_hash = hashlib.sha256(payload.read_bytes()).hexdigest()
    manifest = tmp_path / "SHA256SUMS.txt"
    manifest.write_text(
        f"{expected_hash}  payload.txt\n",
        encoding="utf-8",
    )

    payload.write_text("tampered\n", encoding="utf-8")

    result = checker.verify_package(
        repo_root=tmp_path,
        manifest_relative_path=Path("SHA256SUMS.txt"),
        expected_entry_count=1,
    )

    assert result["state"] == "NON_CONFORMING"
    assert any(
        defect["code"] == "SHA256_MISMATCH"
        for defect in result["defects"]
    )


def test_duplicate_manifest_path_is_detected(tmp_path: Path):
    checker = load_checker()

    payload = tmp_path / "payload.txt"
    payload.write_text("stable\n", encoding="utf-8")
    expected_hash = hashlib.sha256(payload.read_bytes()).hexdigest()

    manifest = tmp_path / "SHA256SUMS.txt"
    manifest.write_text(
        (
            f"{expected_hash}  payload.txt\n"
            f"{expected_hash}  payload.txt\n"
        ),
        encoding="utf-8",
    )

    result = checker.verify_package(
        repo_root=tmp_path,
        manifest_relative_path=Path("SHA256SUMS.txt"),
        expected_entry_count=1,
    )

    assert result["state"] == "NON_CONFORMING"
    assert any(
        defect["code"] == "DUPLICATE_MANIFEST_PATH"
        for defect in result["defects"]
    )