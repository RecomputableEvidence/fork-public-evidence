#!/usr/bin/env python3
"""
Fork Line Ending Normalizer v0.1

Purpose:
    Convert governed text artifacts from CRLF or bare CR to LF.

Exit codes:
    0 = normalization completed
    1 = normalization failed
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


def normalize_file(path: Path) -> bool:
    data = path.read_bytes()

    if b"\x00" in data:
        return False

    normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")

    if normalized == data:
        return False

    path.write_bytes(normalized)
    return True


def run(paths: list[Path] | None) -> int:
    root = repo_root()

    if paths:
        candidates = [path.resolve() for path in paths]
    else:
        candidates = git_candidate_paths(root)

    changed = 0

    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        if not is_governed_text_path(path):
            continue
        if normalize_file(path):
            changed += 1
            print(f"LINE_ENDING_NORMALIZED: {path}")

    print(f"LINE_ENDING_NORMALIZATION_COMPLETE: changed={changed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Fork governed text artifacts to LF")
    parser.add_argument("paths", nargs="*", help="Optional explicit file paths to normalize")
    args = parser.parse_args()

    return run([Path(p) for p in args.paths] if args.paths else None)


if __name__ == "__main__":
    raise SystemExit(main())
