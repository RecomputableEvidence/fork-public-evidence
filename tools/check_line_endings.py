#!/usr/bin/env python3
"""
Fork Line Ending Checker v0.1

Purpose:
    Fail when governed text artifacts contain CRLF or bare CR line endings.

Exit codes:
    0 = no line-ending defects found
    1 = one or more defects found
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".py",
    ".ps1",
    ".sh",
    ".yml",
    ".yaml",
    ".toml",
    ".cff",
    ".csv",
    ".tsv",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
}

TEXT_FILENAMES = {
    ".gitattributes",
    ".gitignore",
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "COPYRIGHT",
    "CODEOWNERS",
    "SHA256SUMS",
}

SKIP_DIR_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError("not inside a git repository")
    return Path(result.stdout.strip()).resolve()


def git_candidate_paths(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=str(root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    paths: list[Path] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        paths.append((root / line).resolve())
    return paths


def is_governed_text_path(path: Path) -> bool:
    parts = set(path.parts)
    if parts.intersection(SKIP_DIR_PARTS):
        return False

    if path.name in TEXT_FILENAMES:
        return True

    if path.suffix.lower() in TEXT_SUFFIXES:
        return True

    return False


def has_nul_byte(data: bytes) -> bool:
    return b"\x00" in data


def scan_file(path: Path) -> list[str]:
    defects: list[str] = []

    try:
        data = path.read_bytes()
    except Exception as exc:
        return [f"LINE_ENDING_READ_ERROR: {path}: {exc}"]

    if has_nul_byte(data):
        return []

    if b"\r\n" in data:
        defects.append(f"LINE_ENDING_DEFECT: {path}: contains CRLF")

    normalized = data.replace(b"\r\n", b"")
    if b"\r" in normalized:
        defects.append(f"LINE_ENDING_DEFECT: {path}: contains bare CR")

    return defects


def run(paths: list[Path] | None) -> int:
    root = repo_root()

    if paths:
        candidates = [path.resolve() for path in paths]
    else:
        candidates = git_candidate_paths(root)

    defects: list[str] = []

    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        if not is_governed_text_path(path):
            continue
        defects.extend(scan_file(path))

    if defects:
        for defect in defects:
            print(defect, file=sys.stderr)
        return 1

    print("LINE_ENDING_PASS: governed text artifacts use LF")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Fork governed text artifacts for LF line endings")
    parser.add_argument("paths", nargs="*", help="Optional explicit file paths to check")
    args = parser.parse_args()

    return run([Path(p) for p in args.paths] if args.paths else None)


if __name__ == "__main__":
    raise SystemExit(main())
