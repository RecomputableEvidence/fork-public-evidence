from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = (
    ROOT / "tools/check_pr92_exterior_recomputation_preservation_v0_1.py"
)


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "fork_pr92_exterior_recomputation_preservation_v0_1",
        CHECKER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_surface(checker, tmp_path: Path) -> Path:
    paths = checker.EXPECTED_PATHS | {
        checker.MANIFEST.as_posix(),
        checker.RETURN_CHECKER.as_posix(),
        checker.SCHEMA.as_posix(),
    }
    for relative in paths:
        source = ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def refresh_manifest_entry(checker, root: Path, relative: str) -> None:
    path = root / relative
    manifest_path = root / checker.MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = next(entry for entry in manifest["entries"] if entry["path"] == relative)
    item["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    item["size_bytes"] = path.stat().st_size
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def test_exact_preserved_return_conforms() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["findings"] == []
    assert result["status"] == (
        "PR92_EXTERIOR_RECOMPUTATION_PRESERVATION_CONFORMS"
    )


def test_raw_artifact_mutation_is_rejected_after_outer_rebinding(
    tmp_path: Path,
) -> None:
    checker = load_checker()
    root = copy_surface(checker, tmp_path)
    archive_path = root / checker.ARCHIVE
    replacement = archive_path.with_suffix(".replacement.zip")
    with zipfile.ZipFile(archive_path) as source, zipfile.ZipFile(
        replacement,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as target:
        for name in source.namelist():
            data = source.read(name)
            if name == "raw/13_checker_default.stdout.txt":
                data += b"mutation\n"
            target.writestr(name, data)
    replacement.replace(archive_path)
    refresh_manifest_entry(checker, root, checker.ARCHIVE.as_posix())
    result = checker.evaluate(root)
    assert "ZIP_RAW_ARTIFACT_DIGEST_MISMATCH" in result["finding_codes"]


def test_effect_promotion_is_rejected_even_if_outer_files_are_rebound(
    tmp_path: Path,
) -> None:
    checker = load_checker()
    root = copy_surface(checker, tmp_path)
    receipt_path = root / checker.RECEIPT
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["effects"]["admission"] = "ADMITTED"
    receipt_path.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    archive_path = root / checker.ARCHIVE
    replacement = archive_path.with_suffix(".replacement.zip")
    with zipfile.ZipFile(archive_path) as source, zipfile.ZipFile(
        replacement,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as target:
        for name in source.namelist():
            data = (
                receipt_path.read_bytes()
                if name == checker.RECEIPT.name
                else source.read(name)
            )
            target.writestr(name, data)
    replacement.replace(archive_path)
    refresh_manifest_entry(checker, root, checker.RECEIPT.as_posix())
    refresh_manifest_entry(checker, root, checker.ARCHIVE.as_posix())
    result = checker.evaluate(root)
    assert "RECEIPT_RETURN_NONCONFORMING" in result["finding_codes"]
    assert "RECEIPT_EFFECT_PROMOTION" in result["finding_codes"]
