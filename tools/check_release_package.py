#!/usr/bin/env python3
"""Deterministic checksum verifier for Fork release packages.

This tool verifies SHA256SUMS.txt for a release package directory.

Default behavior:
  - verify that SHA256SUMS.txt exactly matches the package file set
  - verify each listed SHA-256 digest against current file bytes
  - verify required package control files exist
  - lightly validate PACKAGE_MANIFEST.json when present

Use --write to regenerate SHA256SUMS.txt deterministically.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


REQUIRED_FILES = {
    "README.md",
    "PACKAGE_MANIFEST.json",
    "CLAIMS_AND_NON_CLAIMS.md",
    "RELEASE_NOTES.md",
    "NEXT_STEPS.md",
    "SHA256SUMS.txt",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def package_files(package_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in package_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name == "SHA256SUMS.txt":
            continue
        files.append(path)
    return sorted(files, key=lambda p: rel_posix(p, package_dir))


def expected_sums(package_dir: Path) -> dict[str, str]:
    return {
        rel_posix(path, package_dir): sha256_file(path)
        for path in package_files(package_dir)
    }


def read_sums(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    sums: dict[str, str] = {}

    if not path.exists():
        return sums, [f"missing checksum file: {path}"]

    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if "  " not in line:
            errors.append(f"line {line_no}: expected '<sha256><two spaces><path>'")
            continue
        digest, rel_path = line.split("  ", 1)
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            errors.append(f"line {line_no}: invalid sha256 digest: {digest}")
            continue
        if rel_path in sums:
            errors.append(f"line {line_no}: duplicate path: {rel_path}")
            continue
        sums[rel_path] = digest

    return sums, errors


def write_sums(package_dir: Path) -> None:
    sums = expected_sums(package_dir)
    lines = [f"{digest}  {rel_path}" for rel_path, digest in sorted(sums.items())]
    (package_dir / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def validate_manifest(package_dir: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = package_dir / "PACKAGE_MANIFEST.json"

    if not manifest_path.exists():
        return ["missing PACKAGE_MANIFEST.json"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"PACKAGE_MANIFEST.json invalid JSON: {exc}"]

    package_files_field = manifest.get("package_files")
    if package_files_field is not None:
        if not isinstance(package_files_field, list):
            errors.append("PACKAGE_MANIFEST.json field package_files must be a list when present")
        else:
            for item in package_files_field:
                if not isinstance(item, str):
                    errors.append("PACKAGE_MANIFEST.json package_files entries must be strings")
                    continue
                if not (package_dir / item).exists():
                    errors.append(f"PACKAGE_MANIFEST.json references missing package file: {item}")

    return errors


def check_package(package_dir: Path) -> int:
    errors: list[str] = []

    if not package_dir.exists() or not package_dir.is_dir():
        print(f"ERROR: package directory does not exist: {package_dir}", file=sys.stderr)
        return 2

    missing_required = sorted(name for name in REQUIRED_FILES if not (package_dir / name).exists())
    for name in missing_required:
        errors.append(f"missing required package file: {name}")

    declared, parse_errors = read_sums(package_dir / "SHA256SUMS.txt")
    errors.extend(parse_errors)

    expected = expected_sums(package_dir)

    declared_paths = set(declared)
    expected_paths = set(expected)

    for rel_path in sorted(expected_paths - declared_paths):
        errors.append(f"SHA256SUMS.txt missing file: {rel_path}")

    for rel_path in sorted(declared_paths - expected_paths):
        errors.append(f"SHA256SUMS.txt lists unexpected file: {rel_path}")

    for rel_path in sorted(expected_paths & declared_paths):
        if declared[rel_path] != expected[rel_path]:
            errors.append(
                f"checksum mismatch: {rel_path} expected {expected[rel_path]} got {declared[rel_path]}"
            )

    errors.extend(validate_manifest(package_dir))

    if errors:
        print("RELEASE_PACKAGE_CHECK: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RELEASE_PACKAGE_CHECK: PASS")
    print(f"package_dir: {package_dir}")
    print(f"verified_files: {len(expected)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_dir", help="Path to release package directory")
    parser.add_argument("--write", action="store_true", help="Regenerate SHA256SUMS.txt before checking")
    args = parser.parse_args()

    package_dir = Path(args.package_dir).resolve()

    if args.write:
        write_sums(package_dir)

    return check_package(package_dir)


if __name__ == "__main__":
    raise SystemExit(main())