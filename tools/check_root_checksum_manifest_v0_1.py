#!/usr/bin/env python3
"""Strict, cross-platform verifier for Fork's root checksum manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


CHECKER_ID = "FORK_ROOT_CHECKSUM_MANIFEST_VERIFIER_v0_1"
MANIFEST = Path("CHECKSUMS_SHA256.txt")
RECORD = Path(
    "docs/preservation/root-checksum-integrity-v0.1/"
    "ROOT_CHECKSUM_DISCREPANCY_RECORD_v0_1.json"
)
SPECIMEN = Path(
    "docs/preservation/root-checksum-integrity-v0.1/specimens/"
    "CHECKSUMS_SHA256.8f3f07e.pre-repair.txt"
)
ORIGINAL_MANIFEST_SHA256 = "bebcd503b519804c29680115bd2783cd8ae7dd9709a56b580b38af30de1b3122"
ORIGINAL_MANIFEST_GIT_BLOB_SHA1 = "95d9bc6e1f8ae79975dbfed6b9d247aa249c5c70"
REPAIRED_MANIFEST_SHA256 = "05cb0a9f1f67d9364bafad8641c99e89545edbdf0e85c8c0db30079b8a0cecc4"
ORIGINATING_COMMIT = "8f3f07e89947bbb14b132cf663a7564fdf3b380c"
TARGET_PATH = "research/standards/README.md"
RECORDED_TARGET_SHA256 = "f134c55f5fd927a2c9564352eafed4e58b2145f7432bd18b5b3bb79b8e3ddc9c"
ACTUAL_TARGET_SHA256 = "c69ce9f411313ec5738b4b99d21d385a2498a3519182a38489e1bbe04ee158b2"
LINE_RE = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>[^\r\n]+)$")


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def strict_json_load(path: Path) -> Any:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM prohibited")
    if b"\r" in raw:
        raise ValueError("CR bytes prohibited")
    if not raw.endswith(b"\n"):
        raise ValueError("final LF required")
    text = raw.decode("utf-8", errors="strict")
    return json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON value prohibited: {value}")
        ),
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_sha1(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("ascii")
    return hashlib.sha1(header + value).hexdigest()  # noqa: S324 - Git object identity


def add_error(
    errors: list[dict[str, Any]],
    code: str,
    detail: str,
    *,
    path: str = "",
    line: int | None = None,
) -> None:
    item: dict[str, Any] = {"code": code, "detail": detail, "path": path}
    if line is not None:
        item["line"] = line
    errors.append(item)


def canonical_relative_path(value: str) -> PurePosixPath | None:
    if not value or "\\" in value or "\x00" in value:
        return None
    pure = PurePosixPath(value)
    if pure.is_absolute() or value != pure.as_posix():
        return None
    if any(part in {"", ".", ".."} for part in pure.parts):
        return None
    return pure


def resolved_regular_file(
    root: Path,
    pure: PurePosixPath,
) -> tuple[Path | None, str | None]:
    cursor = root
    for part in pure.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            return None, "SYMLINK"
    try:
        cursor.resolve().relative_to(root.resolve())
    except (OSError, ValueError):
        return None, "ESCAPE"
    if not cursor.exists():
        return None, "MISSING"
    if not cursor.is_file():
        return None, "NOT_REGULAR_FILE"
    return cursor, None


def read_manifest(
    root: Path,
    relative: Path,
    errors: list[dict[str, Any]],
) -> tuple[bytes | None, list[tuple[str, str]]]:
    label = relative.as_posix()
    pure = canonical_relative_path(label)
    if pure is None:
        add_error(errors, "MANIFEST_PATH_UNSAFE", label, path=label)
        return None, []
    manifest_path, problem = resolved_regular_file(root, pure)
    if problem is not None or manifest_path is None:
        add_error(errors, f"MANIFEST_{problem or 'MISSING'}", label, path=label)
        return None, []
    raw = manifest_path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        add_error(errors, "MANIFEST_UTF8_BOM_PROHIBITED", "UTF-8 BOM is not canonical", path=label)
    if b"\r" in raw:
        add_error(errors, "MANIFEST_LINE_ENDINGS_INVALID", "CR bytes are prohibited", path=label)
    if not raw.endswith(b"\n"):
        add_error(errors, "MANIFEST_FINAL_NEWLINE_MISSING", "manifest must end in LF", path=label)
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        add_error(errors, "MANIFEST_NOT_UTF8", str(exc), path=label)
        return raw, []

    entries: list[tuple[str, str]] = []
    observed_paths: set[str] = set()
    for number, line in enumerate(text.splitlines(), start=1):
        match = LINE_RE.fullmatch(line)
        if match is None:
            add_error(
                errors,
                "MANIFEST_LINE_INVALID",
                "expected 64 lowercase hex characters, two spaces, and a path",
                path=label,
                line=number,
            )
            continue
        digest = match.group("digest")
        target = match.group("path")
        pure_target = canonical_relative_path(target)
        if pure_target is None:
            add_error(errors, "TARGET_PATH_UNSAFE", target, path=label, line=number)
            continue
        if target in observed_paths:
            add_error(errors, "TARGET_PATH_DUPLICATE", target, path=label, line=number)
            continue
        observed_paths.add(target)
        entries.append((target, digest))

    paths = [path for path, _ in entries]
    if paths != sorted(paths):
        add_error(errors, "MANIFEST_ORDER_NONCANONICAL", "paths must be ascending", path=label)
    return raw, entries


def verify_entries(
    root: Path,
    entries: list[tuple[str, str]],
    errors: list[dict[str, Any]],
) -> list[dict[str, str]]:
    checked: list[dict[str, str]] = []
    for target, expected in entries:
        pure = canonical_relative_path(target)
        if pure is None:
            continue
        path, problem = resolved_regular_file(root, pure)
        if problem is not None or path is None:
            code = {
                "SYMLINK": "TARGET_SYMLINK_PROHIBITED",
                "ESCAPE": "TARGET_PATH_ESCAPE",
                "MISSING": "TARGET_MISSING",
                "NOT_REGULAR_FILE": "TARGET_NOT_REGULAR_FILE",
            }.get(problem or "", "TARGET_INVALID")
            add_error(errors, code, target, path=target)
            continue
        actual = sha256_bytes(path.read_bytes())
        status = "MATCH" if actual == expected else "MISMATCH"
        checked.append({"path": target, "expected_sha256": expected, "actual_sha256": actual, "status": status})
        if status == "MISMATCH":
            add_error(
                errors,
                "TARGET_SHA256_MISMATCH",
                f"expected={expected} actual={actual}",
                path=target,
            )
    return checked


def expect_equal(
    errors: list[dict[str, Any]],
    actual: Any,
    expected: Any,
    code: str,
    path: str,
) -> None:
    if actual != expected:
        add_error(errors, code, f"expected={expected!r} actual={actual!r}", path=path)


def verify_preservation_record(
    root: Path,
    manifest_raw: bytes | None,
    entries: list[tuple[str, str]],
    errors: list[dict[str, Any]],
) -> dict[str, Any]:
    initial_error_count = len(errors)
    record_path = root / RECORD
    if record_path.is_symlink() or not record_path.is_file():
        add_error(errors, "PRESERVATION_RECORD_MISSING_OR_SYMLINK", RECORD.as_posix(), path=RECORD.as_posix())
        return {"record_path": RECORD.as_posix(), "verified": False}
    try:
        record = strict_json_load(record_path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        add_error(errors, "PRESERVATION_RECORD_STRICT_JSON_INVALID", str(exc), path=RECORD.as_posix())
        return {"record_path": RECORD.as_posix(), "verified": False}
    if not isinstance(record, dict):
        add_error(errors, "PRESERVATION_RECORD_ROOT_INVALID", "record must be an object", path=RECORD.as_posix())
        return {"record_path": RECORD.as_posix(), "verified": False}

    expect_equal(errors, record.get("record_id"), "FORK_ROOT_CHECKSUM_DISCREPANCY_2026_07_19_v0_1", "PRESERVATION_RECORD_ID_MISMATCH", RECORD.as_posix())
    expect_equal(errors, record.get("append_only"), True, "PRESERVATION_APPEND_ONLY_MISMATCH", RECORD.as_posix())
    expect_equal(errors, record.get("status"), "PRESERVED_REPAIR_ENFORCEMENT_CANDIDATE", "PRESERVATION_STATUS_MISMATCH", RECORD.as_posix())

    origin = record.get("origin", {})
    mismatch = record.get("mismatch", {})
    specimen_ref = record.get("preserved_specimen", {})
    gap = record.get("prior_ci_evaluation_gap", {})
    remediation = record.get("remediation", {})
    boundary = record.get("experiment_boundary", {})
    expect_equal(errors, origin.get("originating_commit"), ORIGINATING_COMMIT, "ORIGIN_COMMIT_MISMATCH", RECORD.as_posix())
    expect_equal(errors, mismatch.get("recorded_sha256"), RECORDED_TARGET_SHA256, "RECORDED_DIGEST_MISMATCH", RECORD.as_posix())
    expect_equal(errors, mismatch.get("actual_sha256_at_origin_and_detection"), ACTUAL_TARGET_SHA256, "ACTUAL_DIGEST_MISMATCH", RECORD.as_posix())
    expect_equal(errors, mismatch.get("original_manifest_sha256"), ORIGINAL_MANIFEST_SHA256, "ORIGINAL_MANIFEST_DIGEST_MISMATCH", RECORD.as_posix())
    expect_equal(errors, specimen_ref.get("path"), SPECIMEN.as_posix(), "SPECIMEN_PATH_MISMATCH", RECORD.as_posix())
    expect_equal(errors, specimen_ref.get("sha256"), ORIGINAL_MANIFEST_SHA256, "SPECIMEN_DIGEST_BINDING_MISMATCH", RECORD.as_posix())
    expect_equal(errors, specimen_ref.get("git_blob_sha1"), ORIGINAL_MANIFEST_GIT_BLOB_SHA1, "SPECIMEN_GIT_BLOB_BINDING_MISMATCH", RECORD.as_posix())
    expect_equal(errors, gap.get("status"), "NOT_EVALUATED_BY_PRIOR_GREEN_RUNS", "PRIOR_CI_GAP_STATUS_MISMATCH", RECORD.as_posix())
    expect_equal(errors, remediation.get("repaired_manifest_sha256"), REPAIRED_MANIFEST_SHA256, "REPAIRED_MANIFEST_BINDING_MISMATCH", RECORD.as_posix())
    expect_equal(errors, remediation.get("checker"), "tools/check_root_checksum_manifest_v0_1.py", "CHECKER_PATH_BINDING_MISMATCH", RECORD.as_posix())
    expect_equal(errors, remediation.get("ci_workflow"), ".github/workflows/root-checksum-manifest-v0-1.yml", "CI_PATH_BINDING_MISMATCH", RECORD.as_posix())
    expect_equal(
        errors,
        boundary,
        {
            "provider_calls_performed": 0,
            "provider_execution_effect": "NONE",
            "readiness_effect": "NONE",
            "pair_001_execution_effect": "NONE",
            "pair_001_repetitions_added": 0,
            "current_blocking_controls_modified": False,
        },
        "EXPERIMENT_BOUNDARY_EXPANDED",
        RECORD.as_posix(),
    )

    prior_runs = gap.get("representative_green_runs", [])
    expected_runs = {
        (29684833954, "Fork Evidence CI"),
        (29684833959, "Fork Proof-Surface Integration"),
    }
    observed_runs = {
        (item.get("run_id"), item.get("workflow"))
        for item in prior_runs
        if isinstance(item, dict)
        and item.get("head") == "c6bb2df424193e7ef043ee3c0436bf97ba10fc6e"
        and item.get("conclusion") == "success"
        and item.get("manifest_evaluation") == "NONE"
    }
    expect_equal(errors, observed_runs, expected_runs, "PRIOR_GREEN_RUN_BINDING_MISMATCH", RECORD.as_posix())

    specimen_path, problem = resolved_regular_file(root, PurePosixPath(SPECIMEN.as_posix()))
    if problem is not None or specimen_path is None:
        add_error(errors, "SPECIMEN_MISSING_OR_UNSAFE", str(problem), path=SPECIMEN.as_posix())
    else:
        specimen_raw = specimen_path.read_bytes()
        expect_equal(errors, sha256_bytes(specimen_raw), ORIGINAL_MANIFEST_SHA256, "SPECIMEN_SHA256_MISMATCH", SPECIMEN.as_posix())
        expect_equal(errors, git_blob_sha1(specimen_raw), ORIGINAL_MANIFEST_GIT_BLOB_SHA1, "SPECIMEN_GIT_BLOB_MISMATCH", SPECIMEN.as_posix())
        specimen_lines = specimen_raw.decode("utf-8", errors="strict").splitlines()
        expected_old_line = f"{RECORDED_TARGET_SHA256}  {TARGET_PATH}"
        if expected_old_line not in specimen_lines:
            add_error(errors, "SPECIMEN_ADVERSE_ENTRY_MISSING", expected_old_line, path=SPECIMEN.as_posix())

    entry_map = dict(entries)
    expect_equal(errors, entry_map.get(TARGET_PATH), ACTUAL_TARGET_SHA256, "REPAIRED_TARGET_ENTRY_MISMATCH", MANIFEST.as_posix())
    if manifest_raw is not None:
        expect_equal(errors, sha256_bytes(manifest_raw), REPAIRED_MANIFEST_SHA256, "REPAIRED_MANIFEST_SHA256_MISMATCH", MANIFEST.as_posix())
    for required in (
        Path("tools/check_root_checksum_manifest_v0_1.py"),
        Path("tests/fixtures/root-checksum-manifest-v0.1/adversarial_cases_v0_1.json"),
        Path(".github/workflows/root-checksum-manifest-v0-1.yml"),
    ):
        if not (root / required).is_file():
            add_error(errors, "REMEDIATION_SURFACE_MISSING", required.as_posix(), path=required.as_posix())

    return {
        "record_path": RECORD.as_posix(),
        "record_id": record.get("record_id"),
        "originating_commit": origin.get("originating_commit"),
        "recorded_sha256": mismatch.get("recorded_sha256"),
        "actual_sha256": mismatch.get("actual_sha256_at_origin_and_detection"),
        "prior_ci_evaluation": gap.get("status"),
        "verified": len(errors) == initial_error_count,
    }


def evaluate(
    root: Path,
    *,
    manifest: Path = MANIFEST,
    verify_preservation: bool = True,
) -> dict[str, Any]:
    root = root.resolve()
    errors: list[dict[str, Any]] = []
    raw, entries = read_manifest(root, manifest, errors)
    checked = verify_entries(root, entries, errors)
    preservation = (
        verify_preservation_record(root, raw, entries, errors)
        if verify_preservation
        else {"record_path": None, "verified": False, "reason": "MANIFEST_ONLY_MODE"}
    )
    errors.sort(key=lambda item: (item["code"], item.get("path", ""), item.get("line", 0)))
    valid = not errors
    return {
        "checker_id": CHECKER_ID,
        "result": {
            "valid": valid,
            "status": (
                "ROOT_CHECKSUM_MANIFEST_CONFORMS_DISCREPANCY_PRESERVED"
                if valid
                else "ROOT_CHECKSUM_MANIFEST_INVALID"
            ),
            "provider_calls_performed": 0,
            "provider_execution_effect": "NONE",
            "readiness_effect": "NONE",
            "pair_001_execution_effect": "NONE",
        },
        "manifest": {
            "path": manifest.as_posix(),
            "sha256": sha256_bytes(raw) if raw is not None else None,
            "declared_entry_count": len(entries),
            "checked_entry_count": len(checked),
            "matched_entry_count": sum(item["status"] == "MATCH" for item in checked),
        },
        "preservation": preservation,
        "errors": errors,
        "error_codes": sorted({item["code"] for item in errors}),
        "non_claims": {
            "does_not_establish_manifest_completeness": True,
            "does_not_establish_semantic_truth": True,
            "does_not_retroactively_evaluate_prior_ci": True,
            "does_not_authorize_provider_calls": True,
            "does_not_promote_readiness": True,
            "does_not_execute_pair_001": True,
        },
    }


def repository_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root not found")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = repository_root(args.repo_root)
    result = evaluate(
        root,
        manifest=args.manifest,
        verify_preservation=not args.manifest_only,
    )
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for error in result["errors"]:
            print(f"[{error['code']}] {error.get('path', '')}: {error['detail']}")
        print(result["result"]["status"])
    return 0 if result["result"]["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
