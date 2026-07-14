#!/usr/bin/env python3
"""Verify the frozen Fork Meta-Evidence v0.1 package SHA-256 boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

MANIFEST_RELATIVE_PATH = Path(
    "receipts/experiment-meta-evidence/v0.1/SHA256SUMS.txt"
)
EXPECTED_ENTRY_COUNT = 60
LINE_PATTERN = re.compile(r"^([0-9a-fA-F]{64})\s+\*?(.+)$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_package(
    repo_root: Path,
    manifest_relative_path: Path = MANIFEST_RELATIVE_PATH,
    expected_entry_count: int = EXPECTED_ENTRY_COUNT,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    manifest_path = repo_root / manifest_relative_path

    defects: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    if not manifest_path.is_file():
        return {
            "checker": "check_fork_meta_evidence_package_v0_1.py",
            "manifest": manifest_relative_path.as_posix(),
            "entry_count": 0,
            "defect_count": 1,
            "defects": [
                {
                    "code": "MANIFEST_MISSING",
                    "path": manifest_relative_path.as_posix(),
                }
            ],
            "state": "NON_CONFORMING",
        }

    raw_lines = manifest_path.read_text(encoding="utf-8").splitlines()

    for line_number, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = LINE_PATTERN.fullmatch(line)
        if match is None:
            defects.append(
                {
                    "code": "MALFORMED_MANIFEST_LINE",
                    "line_number": line_number,
                }
            )
            continue

        expected_hash = match.group(1).lower()
        relative_path_text = match.group(2).replace("\\", "/")
        relative_path = Path(relative_path_text)

        if relative_path_text in seen_paths:
            defects.append(
                {
                    "code": "DUPLICATE_MANIFEST_PATH",
                    "path": relative_path_text,
                }
            )
            continue

        seen_paths.add(relative_path_text)

        if relative_path == manifest_relative_path:
            defects.append(
                {
                    "code": "MANIFEST_SELF_REFERENCE",
                    "path": relative_path_text,
                }
            )
            continue

        full_path = repo_root / relative_path

        if not full_path.is_file():
            defects.append(
                {
                    "code": "PACKAGE_FILE_MISSING",
                    "path": relative_path_text,
                }
            )
            entries.append(
                {
                    "path": relative_path_text,
                    "expected_sha256": expected_hash,
                    "actual_sha256": None,
                    "state": "MISSING",
                }
            )
            continue

        actual_hash = sha256_file(full_path)
        entry_state = "PASS" if actual_hash == expected_hash else "FAIL"

        entries.append(
            {
                "path": relative_path_text,
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "state": entry_state,
            }
        )

        if entry_state == "FAIL":
            defects.append(
                {
                    "code": "SHA256_MISMATCH",
                    "path": relative_path_text,
                    "expected_sha256": expected_hash,
                    "actual_sha256": actual_hash,
                }
            )

    if len(entries) != expected_entry_count:
        defects.append(
            {
                "code": "MANIFEST_ENTRY_COUNT_MISMATCH",
                "expected": expected_entry_count,
                "actual": len(entries),
            }
        )

    result = {
        "checker": "check_fork_meta_evidence_package_v0_1.py",
        "manifest": manifest_relative_path.as_posix(),
        "manifest_sha256": sha256_file(manifest_path),
        "entry_count": len(entries),
        "entries_passed": sum(
            1 for entry in entries if entry["state"] == "PASS"
        ),
        "defect_count": len(defects),
        "defects": defects,
        "state": "CONFORMING" if not defects else "NON_CONFORMING",
    }
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=MANIFEST_RELATIVE_PATH,
    )
    parser.add_argument(
        "--expected-entry-count",
        type=int,
        default=EXPECTED_ENTRY_COUNT,
    )
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = verify_package(
        repo_root=args.repo_root,
        manifest_relative_path=args.manifest,
        expected_entry_count=args.expected_entry_count,
    )

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"{result['state']}: "
            f"{result['entry_count']} entries, "
            f"{result['defect_count']} defects"
        )

    return 0 if result["state"] == "CONFORMING" else 1


if __name__ == "__main__":
    sys.exit(main())