#!/usr/bin/env python3
"""Reconstruct and safely extract the Fork pilot prerequisite source archive."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path, PurePosixPath

MANIFEST = "DELIVERY_MANIFEST_v0_1.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_member(name: str) -> bool:
    if not name or "\\" in name or "\x00" in name:
        return False
    path = PurePosixPath(name)
    if path.is_absolute() or name != path.as_posix():
        return False
    return all(part not in {"", ".", ".."} for part in path.parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("FORK_PILOT_DEPLOYMENT_PREREQUISITE_v0_1.zip"))
    parser.add_argument("--extract", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    chunks: list[bytes] = []
    for entry in manifest["base64_parts"]:
        path = root / entry["path"]
        raw = path.read_bytes()
        if len(raw) != entry["bytes"]:
            raise SystemExit(f"PART_SIZE_MISMATCH:{entry['path']}")
        if sha256(raw) != entry["sha256"]:
            raise SystemExit(f"PART_SHA256_MISMATCH:{entry['path']}")
        chunks.append(raw)

    encoded = b"".join(chunks)
    if len(encoded) != manifest["aggregate_base64"]["bytes"]:
        raise SystemExit("AGGREGATE_BASE64_SIZE_MISMATCH")
    if sha256(encoded) != manifest["aggregate_base64"]["sha256"]:
        raise SystemExit("AGGREGATE_BASE64_SHA256_MISMATCH")

    try:
        archive = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f"BASE64_INVALID:{exc}") from exc
    expected = manifest["decoded_archive"]
    if len(archive) != expected["bytes"]:
        raise SystemExit("ARCHIVE_SIZE_MISMATCH")
    if sha256(archive) != expected["sha256"]:
        raise SystemExit("ARCHIVE_SHA256_MISMATCH")

    output = args.output.resolve()
    output.write_bytes(archive)

    with zipfile.ZipFile(output) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise SystemExit("ZIP_DUPLICATE_MEMBER")
        if any(not safe_member(name) for name in names):
            raise SystemExit("ZIP_UNSAFE_MEMBER")
        if len(names) != expected["member_count"]:
            raise SystemExit("ZIP_MEMBER_COUNT_MISMATCH")
        bad = zf.testzip()
        if bad is not None:
            raise SystemExit(f"ZIP_CRC_FAILURE:{bad}")
        if args.extract is not None:
            destination = args.extract.resolve()
            destination.mkdir(parents=True, exist_ok=True)
            for info in zf.infolist():
                target = (destination / PurePosixPath(info.filename)).resolve()
                try:
                    target.relative_to(destination)
                except ValueError as exc:
                    raise SystemExit(f"ZIP_PATH_ESCAPE:{info.filename}") from exc
                target.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info) as source, target.open("wb") as sink:
                    sink.write(source.read())

    result = {
        "status": "FORK_PILOT_PREREQUISITE_ARCHIVE_RECONSTRUCTED_AND_VERIFIED",
        "archive": os.fspath(output),
        "bytes": len(archive),
        "sha256": sha256(archive),
        "member_count": expected["member_count"],
        "extracted_to": os.fspath(args.extract.resolve()) if args.extract else None,
        "pilot_authorized": False,
        "admission_effect": "NONE",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
