from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_root_checksum_manifest_v0_1.py"
FIXTURES = ROOT / "tests/fixtures/root-checksum-manifest-v0.1/adversarial_cases_v0_1.json"
WORKFLOW = ROOT / ".github/workflows/root-checksum-manifest-v0-1.yml"


def load_checker():
    spec = importlib.util.spec_from_file_location("root_checksum_manifest", CHECKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_manifest(root: Path, entries: list[tuple[str, str]]) -> None:
    rendered = "".join(f"{digest}  {path}\n" for path, digest in entries)
    (root / "CHECKSUMS_SHA256.txt").write_bytes(rendered.encode("utf-8"))


def materialize_small_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "fixture"
    (root / "nested").mkdir(parents=True)
    (root / "alpha.txt").write_bytes(b"alpha\n")
    (root / "nested/beta.txt").write_bytes(b"beta\n")
    entries = [
        ("alpha.txt", sha256((root / "alpha.txt").read_bytes())),
        ("nested/beta.txt", sha256((root / "nested/beta.txt").read_bytes())),
    ]
    write_manifest(root, entries)
    return root


def mutate(root: Path, case: dict) -> None:
    manifest = root / "CHECKSUMS_SHA256.txt"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    operation = case["operation"]
    target = case.get("target")
    if operation == "replace_digest":
        lines = [
            f"{case['value']}  {path}" if path == target else f"{digest}  {path}"
            for digest, path in (line.split("  ", 1) for line in lines)
        ]
        write_manifest(root, [(path, digest) for digest, path in (line.split("  ", 1) for line in lines)])
    elif operation == "duplicate_entry":
        duplicate = next(line for line in lines if line.endswith(f"  {target}"))
        manifest.write_text("\n".join(lines + [duplicate]) + "\n", encoding="utf-8", newline="\n")
    elif operation == "replace_path":
        lines = [
            f"{digest}  {case['value'] if path == target else path}"
            for digest, path in (line.split("  ", 1) for line in lines)
        ]
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    elif operation == "uppercase_digest":
        lines = [
            f"{digest.upper() if path == target else digest}  {path}"
            for digest, path in (line.split("  ", 1) for line in lines)
        ]
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    elif operation == "convert_crlf":
        manifest.write_bytes(manifest.read_bytes().replace(b"\n", b"\r\n"))
    elif operation == "remove_final_newline":
        manifest.write_bytes(manifest.read_bytes().removesuffix(b"\n"))
    elif operation == "reverse_entries":
        manifest.write_text("\n".join(reversed(lines)) + "\n", encoding="utf-8", newline="\n")
    elif operation == "delete_target":
        (root / target).unlink()
    elif operation == "replace_target_with_directory":
        path = root / target
        path.unlink()
        path.mkdir()
    elif operation == "append_blank_line":
        manifest.write_bytes(manifest.read_bytes() + b"\n")
    else:
        raise AssertionError(f"unknown operation: {operation}")


def materialize_governed_surface(tmp_path: Path, checker) -> Path:
    root = tmp_path / "governed"
    root.mkdir(parents=True)
    manifest_entries = []
    for line in (ROOT / checker.MANIFEST).read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        source = ROOT / relative
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        manifest_entries.append((relative, digest))
    write_manifest(root, manifest_entries)
    for relative in (
        checker.RECORD,
        checker.SPECIMEN,
        Path("tools/check_root_checksum_manifest_v0_1.py"),
        Path("tests/fixtures/root-checksum-manifest-v0.1/adversarial_cases_v0_1.json"),
        Path(".github/workflows/root-checksum-manifest-v0-1.yml"),
    ):
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    return root


def test_repaired_manifest_and_preserved_discrepancy_conform() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["errors"] == []
    assert result["result"] == {
        "valid": True,
        "status": "ROOT_CHECKSUM_MANIFEST_CONFORMS_DISCREPANCY_PRESERVED",
        "provider_calls_performed": 0,
        "provider_execution_effect": "NONE",
        "readiness_effect": "NONE",
        "pair_001_execution_effect": "NONE",
    }
    assert result["manifest"] == {
        "path": "CHECKSUMS_SHA256.txt",
        "sha256": checker.REPAIRED_MANIFEST_SHA256,
        "declared_entry_count": 51,
        "checked_entry_count": 51,
        "matched_entry_count": 51,
    }
    assert result["preservation"]["prior_ci_evaluation"] == "NOT_EVALUATED_BY_PRIOR_GREEN_RUNS"


def test_original_manifest_is_preserved_byte_exact_and_still_reproduces_failure() -> None:
    checker = load_checker()
    specimen = ROOT / checker.SPECIMEN
    raw = specimen.read_bytes()
    assert checker.sha256_bytes(raw) == checker.ORIGINAL_MANIFEST_SHA256
    assert checker.git_blob_sha1(raw) == checker.ORIGINAL_MANIFEST_GIT_BLOB_SHA1
    result = checker.evaluate(ROOT, manifest=checker.SPECIMEN, verify_preservation=False)
    assert result["manifest"]["matched_entry_count"] == 50
    assert result["manifest"]["checked_entry_count"] == 51
    assert result["error_codes"] == ["TARGET_SHA256_MISMATCH"]
    assert result["errors"][0]["path"] == checker.TARGET_PATH
    assert checker.RECORDED_TARGET_SHA256 in result["errors"][0]["detail"]
    assert checker.ACTUAL_TARGET_SHA256 in result["errors"][0]["detail"]


def test_all_precommitted_adversarial_fixtures_fail_closed(tmp_path: Path) -> None:
    checker = load_checker()
    fixture_set = json.loads(FIXTURES.read_text(encoding="utf-8"))
    observed: set[str] = set()
    for case in fixture_set["cases"]:
        root = materialize_small_fixture(tmp_path / case["case_id"])
        mutate(root, case)
        result = checker.evaluate(root, verify_preservation=False)
        assert result["result"]["valid"] is False, case["case_id"]
        assert case["expected_error"] in result["error_codes"], (case["case_id"], result["errors"])
        observed.add(case["class"])
    assert len(observed) == 12


def test_duplicate_and_nonfinite_preservation_record_values_fail_strictly(tmp_path: Path) -> None:
    checker = load_checker()
    original = (ROOT / checker.RECORD).read_text(encoding="utf-8")
    mutations = {
        "duplicate": original.replace(
            '  "schema_version": "v0.1",',
            '  "schema_version": "v0.1",\n  "schema_version": "v0.1",',
            1,
        ),
        "nonfinite": original.replace('  "append_only": true,', '  "append_only": true,\n  "invalid": NaN,', 1),
    }
    for name, rendered in mutations.items():
        root = materialize_governed_surface(tmp_path / name, checker)
        (root / checker.RECORD).write_text(rendered, encoding="utf-8", newline="\n")
        result = checker.evaluate(root)
        assert result["error_codes"] == ["PRESERVATION_RECORD_STRICT_JSON_INVALID"]


def test_preservation_record_cannot_expand_experiment_effect(tmp_path: Path) -> None:
    checker = load_checker()
    root = materialize_governed_surface(tmp_path, checker)
    record_path = root / checker.RECORD
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["experiment_boundary"]["pair_001_execution_effect"] = "AUTHORIZED"
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert "EXPERIMENT_BOUNDARY_EXPANDED" in result["error_codes"]


def test_ci_is_cross_platform_fail_closed_and_provider_free() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "pull_request:" in text
    assert "preservation/clean-continuance-v0.1" in text
    assert "ubuntu-latest" in text
    assert "windows-latest" in text
    assert "python tools/check_root_checksum_manifest_v0_1.py --json" in text
    assert "permissions:\n  contents: read" in text
    assert "secrets." not in text
    assert "run_csh_provider_validation" not in text
    assert "cross_system_claim_handoff_execution" not in text
