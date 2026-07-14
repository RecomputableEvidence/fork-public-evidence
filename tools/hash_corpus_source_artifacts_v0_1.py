#!/usr/bin/env python3
"""Hash exact Corpus 001 source-artifact bytes without modifying the source."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        if not args.source.is_file():
            raise ValueError(f"Source is not a regular file: {args.source}")

        stat_before = args.source.stat()
        digest = sha256_file(args.source)
        stat_after = args.source.stat()

        unchanged = (
            stat_before.st_size == stat_after.st_size
            and stat_before.st_mtime_ns == stat_after.st_mtime_ns
        )
        if not unchanged:
            raise RuntimeError(
                "Source metadata changed while it was being hashed."
            )

        result = {
            "tool": "hash_corpus_source_artifacts_v0_1.py",
            "artifact_id": args.artifact_id,
            "source_byte_length": stat_after.st_size,
            "source_sha256": digest,
            "source_modified": False,
            "state": "PASS",
        }

        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"{digest}  {args.artifact_id}")
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        result = {
            "tool": "hash_corpus_source_artifacts_v0_1.py",
            "artifact_id": args.artifact_id,
            "state": "FAIL",
            "error": str(exc),
        }
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())