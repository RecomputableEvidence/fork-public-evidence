from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_shayne_pr63_pr64_attachment_successor_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("shayne_attachment_successor", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def copy_file(root: Path, relative: Path) -> None:
    source = ROOT / relative
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def materialize(tmp_path: Path, checker) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / checker.PACKAGE, root / checker.PACKAGE)
    for relative in (
        checker.ANCHOR,
        checker.PREDECESSOR_ANCHOR,
        checker.CANONICAL_PLAN,
    ):
        copy_file(root, relative)
    return root


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_manifest_entry(root: Path, checker, relative: Path) -> None:
    manifest_path = root / checker.MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = next(entry for entry in manifest["entries"] if entry["path"] == relative.as_posix())
    path = root / relative
    item["sha256"] = digest(path)
    item["size_bytes"] = path.stat().st_size
    write_json(manifest_path, manifest)


def refresh_anchor_binding(root: Path, checker, relative: Path) -> None:
    anchor_path = root / checker.ANCHOR
    anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
    item = next(
        entry for entry in anchor["artifact_bindings"] if entry["path"] == relative.as_posix()
    )
    path = root / relative
    item["sha256"] = digest(path)
    item["size_bytes"] = path.stat().st_size
    write_json(anchor_path, anchor)


def rebind_manifest(root: Path, checker, relative: Path) -> None:
    refresh_manifest_entry(root, checker, relative)
    refresh_anchor_binding(root, checker, checker.MANIFEST)


def rebind_receipt(root: Path, checker) -> None:
    refresh_anchor_binding(root, checker, checker.RECEIPT)


def codes(result: dict) -> set[str]:
    return set(result["finding_codes"])


def test_exact_attachment_successor_conforms() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["ok"] is True
    assert result["finding_count"] == 0
    assert result["status"] == (
        "SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_CONFORMS_NOT_ADMITTED"
    )
    assert result["standing"] == {
        "reviewer_declared_disposition": "REPRODUCED_WITHIN_DECLARED_SCOPE",
        "admission_state": "REVIEW_ELIGIBLE_NOT_ADMITTED",
        "pr_63_state": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
        "execution_authority_delta": "NONE",
        "pair_001_execution_authorized": False,
    }


def test_release_asset_and_all_internal_digests_are_exact() -> None:
    checker = load_checker()
    assert digest(ROOT / checker.ARCHIVE) == checker.ARCHIVE_SHA256
    assert (ROOT / checker.ARCHIVE).stat().st_size == 16901
    with zipfile.ZipFile(ROOT / checker.ARCHIVE) as archive:
        assert set(archive.namelist()) == checker.EXPECTED_MEMBERS
        assert archive.testzip() is None
        for name, (expected_hash, expected_size) in checker.EXPECTED_FILE_MEMBERS.items():
            value = archive.read(name)
            assert len(value) == expected_size
            assert hashlib.sha256(value).hexdigest() == expected_hash


def test_extracted_mutation_fails_after_outer_manifest_rebinding(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    relative = checker.RAW / "r_1.json"
    path = root / relative
    path.write_bytes(path.read_bytes() + b"mutation\n")
    rebind_manifest(root, checker, relative)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "ARCHIVE_EXTRACTED_COPY_DIVERGENCE" in codes(result)
    assert "RECEIPT_SET_NOT_BYTE_IDENTICAL" in codes(result)


def test_unsafe_archive_member_is_rejected_after_outer_rebinding(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    archive_path = root / checker.ARCHIVE
    replacement = archive_path.with_suffix(".replacement.zip")
    with zipfile.ZipFile(archive_path) as source, zipfile.ZipFile(
        replacement,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as target:
        for info in source.infolist():
            target.writestr(info, source.read(info.filename))
        target.writestr("../escape.txt", b"not extracted\n")
    replacement.replace(archive_path)
    rebind_manifest(root, checker, checker.ARCHIVE)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "ARCHIVE_UNSAFE_MEMBER" in codes(result)
    assert "ARCHIVE_MEMBER_SCOPE_MISMATCH" in codes(result)


def test_fresh_runner_gap_cannot_be_silently_filled(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    receipt_path = root / checker.RECEIPT
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["preserved_capture_gap"]["original_bytes_preserved"] = True
    receipt["preserved_capture_gap"]["gap_standing"] = "REPAIRED"
    write_json(receipt_path, receipt)
    rebind_receipt(root, checker)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "FRESH_RUNNER_GAP_SILENTLY_FILLED" in codes(result)


def test_literal_single_byte_overclaim_is_rejected(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    receipt_path = root / checker.RECEIPT
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    tamper = receipt["raw_evidence_adjudication"]["tamper_probe"]
    tamper["file_byte_difference_count"] = 1
    tamper["reviewer_single_byte_language_literal_file_effect"] = "CONFIRMED"
    write_json(receipt_path, receipt)
    rebind_receipt(root, checker)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "TAMPER_PRECISION_ADJUDICATION_MISMATCH" in codes(result)


def test_execution_authority_promotion_is_rejected(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    anchor_path = root / checker.ANCHOR
    anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
    effect = anchor["admission_effect_if_merged"]
    effect["pr_63_continuing_state"] = "EXECUTION_AUTHORIZED"
    effect["does_not_authorize_pair_001_execution"] = False
    effect["does_not_transfer_authority"] = False
    write_json(anchor_path, anchor)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "ANCHOR_ADMISSION_EFFECT_PROMOTION" in codes(result)


def test_predecessor_negative_state_cannot_be_rewritten(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    record_path = root / checker.PREDECESSOR_RECORD
    record = json.loads(record_path.read_text(encoding="utf-8"))
    attachment = record["source"]["referenced_full_findings_attachment"]
    attachment["status"] = "RECEIVED"
    attachment["repository_bytes_received"] = True
    write_json(record_path, record)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "PREDECESSOR_NEGATIVE_STATE_REWRITTEN" in codes(result)
    assert "PREDECESSOR_RECORD_DIGEST_MISMATCH" in codes(result)


def test_private_correspondence_screenshot_is_not_promoted_to_public_artifact(
    tmp_path: Path,
) -> None:
    checker = load_checker()
    root = materialize(tmp_path, checker)
    receipt_path = root / checker.RECEIPT
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    correspondence = receipt["transfer_correspondence"]
    correspondence["preserved_in_public_repository"] = True
    correspondence["cryptographic_subject_binding_basis"] = "LINKEDIN_SCREENSHOT"
    write_json(receipt_path, receipt)
    rebind_receipt(root, checker)
    result = checker.evaluate(root, verify_git_correlations=False)
    assert "CORRESPONDENCE_PRIVACY_BOUNDARY_MISMATCH" in codes(result)
