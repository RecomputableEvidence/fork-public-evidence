#!/usr/bin/env python3
"""Verify the preserved PR #92 exterior-recomputation return and raw ZIP."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/exterior-observations/reviews/pr92-chatgpt-codex-20260726")
RECEIPT = BASE / (
    "EXTERIOR_RECOMPUTATION_RECEIPT_PR92_CHATGPT_CODEX_20260726_v0_1.json"
)
ARCHIVE = BASE / "RETURN_PACKAGE_PR92_CHATGPT_CODEX_20260726_v0_1.zip"
README = BASE / "README.md"
MANIFEST = BASE / "PRESERVATION_MANIFEST_v0_1.json"
RETURN_CHECKER = Path(
    "tools/check_longitudinal_exterior_recomputation_return_v0_1.py"
)
SCHEMA = Path(
    "schemas/fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json"
)
EXPECTED_PATHS = {RECEIPT.as_posix(), ARCHIVE.as_posix(), README.as_posix()}
EXPECTED_EFFECTS = {
    "provider_calls": 0,
    "pair_001_calls": 0,
    "pair_001_repetitions": 0,
    "admission": "NONE",
    "merge_authorization": "NONE",
    "publication": "NONE",
    "authority_transfer": "NONE",
    "execution_permission": "NONE",
}


def strict_load(path: Path) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_member(name: str) -> bool:
    pure = PurePosixPath(name)
    return bool(
        name
        and "\\" not in name
        and not pure.is_absolute()
        and all(part not in ("", ".", "..") for part in pure.parts)
    )


def load_return_checker(root: Path) -> Any:
    path = root / RETURN_CHECKER
    spec = importlib.util.spec_from_file_location("fork_pr92_return_checker", path)
    if spec is None or spec.loader is None:
        raise ValueError("return checker could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str = "$",
) -> None:
    findings.append({"code": code, "path": path, "detail": detail})


def evaluate(root: Path) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    try:
        manifest = strict_load(root / MANIFEST)
        receipt = strict_load(root / RECEIPT)
        return_checker = load_return_checker(root)
        schema = return_checker.strict_load(root / SCHEMA)
    except Exception as error:
        add(findings, "PRESERVATION_INPUT_INVALID", str(error))
        return finish(findings)

    entries = manifest.get("entries", [])
    declared_paths = {
        item.get("path")
        for item in entries
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    if declared_paths != EXPECTED_PATHS:
        add(
            findings,
            "PRESERVATION_MANIFEST_SCOPE_MISMATCH",
            f"expected {sorted(EXPECTED_PATHS)}, found {sorted(declared_paths)}",
            MANIFEST.as_posix(),
        )
    for item in entries:
        if not isinstance(item, dict):
            continue
        relative = item.get("path")
        if relative not in EXPECTED_PATHS:
            continue
        path = root / relative
        if not path.is_file():
            add(findings, "PRESERVED_FILE_MISSING", str(relative), str(relative))
            continue
        if item.get("size_bytes") != path.stat().st_size:
            add(findings, "PRESERVED_SIZE_MISMATCH", str(relative), str(relative))
        if item.get("sha256") != sha256_file(path):
            add(findings, "PRESERVED_DIGEST_MISMATCH", str(relative), str(relative))

    if manifest.get("self_exclusion", {}).get("path") != MANIFEST.as_posix():
        add(
            findings,
            "PRESERVATION_SELF_EXCLUSION_MISSING",
            "manifest must declare its own circular-digest exclusion",
            MANIFEST.as_posix(),
        )

    return_result = return_checker.validate_return(
        receipt,
        schema,
        artifact_root=None,
        allow_pending=False,
    )
    if not return_result.get("ok"):
        add(
            findings,
            "RECEIPT_RETURN_NONCONFORMING",
            json.dumps(return_result.get("findings", []), sort_keys=True),
            RECEIPT.as_posix(),
        )
    if receipt.get("disposition") != "REPRODUCED_WITHIN_DECLARED_SCOPE":
        add(
            findings,
            "RECEIPT_DISPOSITION_MISMATCH",
            str(receipt.get("disposition")),
            RECEIPT.as_posix(),
        )
    if receipt.get("effects") != EXPECTED_EFFECTS:
        add(
            findings,
            "RECEIPT_EFFECT_PROMOTION",
            "preserved return effects differ from the no-effect boundary",
            RECEIPT.as_posix(),
        )
    disclosure = receipt.get("reviewer_disclosure", {})
    if disclosure.get("independence_class") != "NOT_INDEPENDENT_AUTHOR_ASSISTED":
        add(
            findings,
            "REVIEWER_DISCLOSURE_DRIFT",
            "preserved reviewer relationship changed",
            RECEIPT.as_posix(),
        )

    archive_path = root / ARCHIVE
    if not archive_path.is_file():
        add(findings, "RETURN_ARCHIVE_MISSING", ARCHIVE.as_posix())
        return finish(findings)
    try:
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                add(findings, "RETURN_ARCHIVE_DUPLICATE_MEMBER", "duplicate ZIP member")
            unsafe = sorted(name for name in names if not canonical_member(name))
            if unsafe:
                add(
                    findings,
                    "RETURN_ARCHIVE_UNSAFE_MEMBER",
                    repr(unsafe),
                    ARCHIVE.as_posix(),
                )
            receipt_name = RECEIPT.name
            raw = receipt.get("raw_output_artifacts", [])
            expected_members = {receipt_name} | {
                item.get("path") for item in raw if isinstance(item, dict)
            }
            if set(names) != expected_members:
                add(
                    findings,
                    "RETURN_ARCHIVE_SCOPE_MISMATCH",
                    f"missing={sorted(expected_members - set(names))!r}; "
                    f"extra={sorted(set(names) - expected_members)!r}",
                    ARCHIVE.as_posix(),
                )
            if receipt_name in names and archive.read(receipt_name) != (root / RECEIPT).read_bytes():
                add(
                    findings,
                    "RETURN_ARCHIVE_RECEIPT_DIVERGENCE",
                    "archived receipt differs from separately preserved receipt",
                    ARCHIVE.as_posix(),
                )
            for item in raw:
                if not isinstance(item, dict) or item.get("path") not in names:
                    continue
                data = archive.read(item["path"])
                if len(data) != item.get("size_bytes"):
                    add(
                        findings,
                        "ZIP_RAW_ARTIFACT_SIZE_MISMATCH",
                        item["path"],
                        ARCHIVE.as_posix(),
                    )
                if sha256_bytes(data) != item.get("sha256"):
                    add(
                        findings,
                        "ZIP_RAW_ARTIFACT_DIGEST_MISMATCH",
                        item["path"],
                        ARCHIVE.as_posix(),
                    )
    except (OSError, zipfile.BadZipFile, KeyError) as error:
        add(findings, "RETURN_ARCHIVE_INVALID", str(error), ARCHIVE.as_posix())

    artifact_hashes = {
        item.get("sha256")
        for item in receipt.get("raw_output_artifacts", [])
        if isinstance(item, dict)
    }
    for index, execution in enumerate(receipt.get("executions", [])):
        for field in ("stdout_sha256", "stderr_sha256"):
            if execution.get(field) not in artifact_hashes:
                add(
                    findings,
                    "EXECUTION_RAW_BINDING_MISSING",
                    f"{field} is not present in the raw artifact set",
                    f"$.executions[{index}].{field}",
                )
    return finish(findings)


def finish(findings: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "status": (
            "PR92_EXTERIOR_RECOMPUTATION_PRESERVATION_CONFORMS"
            if not findings
            else "PR92_EXTERIOR_RECOMPUTATION_PRESERVATION_NONCONFORMING"
        ),
        "ok": not findings,
        "finding_codes": sorted({item["code"] for item in findings}),
        "findings": findings,
        "substantive_recomputation_inferred": False,
        "admission_or_execution_inferred": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.repo_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(result["status"])
        for finding in result["findings"]:
            print(f"{finding['code']}: {finding['path']}: {finding['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
