#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


EXPECTED_CANONICALIZATION_METHOD = (
    "repo-local JSON canonicalization using sorted keys and compact separators, "
    "excluding manifest_digest to avoid self-reference"
)

SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: set[str] = set()
    result: dict[str, Any] = {}

    for key, value in pairs:
        if key in seen:
            raise ValueError(f"Duplicate JSON key detected: {key}")
        seen.add(key)
        result[key] = value

    return result


def load_manifest(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("Manifest must be UTF-8 without BOM.")

    data = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )

    if not isinstance(data, dict):
        raise ValueError("Manifest root must be a JSON object.")

    return data


def canonical_manifest_bytes_excluding_digest(data: dict[str, Any]) -> bytes:
    digest_input = dict(data)
    digest_input.pop("manifest_digest", None)

    return json.dumps(
        digest_input,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def compute_sha256(path: Path) -> dict[str, Any]:
    data = load_manifest(path)
    manifest_digest = data.get("manifest_digest")

    if not isinstance(manifest_digest, dict):
        raise ValueError("manifest_digest must be present and must be an object.")

    declared_type = manifest_digest.get("type")
    declared_value = manifest_digest.get("value")
    canonicalization_method = manifest_digest.get("canonicalization_method")

    type_ok = declared_type == "sha256"
    method_ok = canonicalization_method == EXPECTED_CANONICALIZATION_METHOD
    value_shape_ok = isinstance(declared_value, str) and bool(SHA256_HEX_RE.fullmatch(declared_value))

    canonical_bytes = canonical_manifest_bytes_excluding_digest(data)
    computed_value = hashlib.sha256(canonical_bytes).hexdigest()

    value_match = declared_value == computed_value

    return {
        "artifact_path": str(path),
        "canonicalization_scope": "top-level JSON object excluding manifest_digest",
        "canonicalization_serialization": {
            "sort_keys": True,
            "separators": [",", ":"],
            "ensure_ascii": False,
            "encoding": "utf-8",
            "bom_allowed": False,
            "duplicate_keys_allowed": False,
        },
        "declared": {
            "type": declared_type,
            "value": declared_value,
            "canonicalization_method": canonicalization_method,
        },
        "computed": {
            "type": "sha256",
            "value": computed_value,
        },
        "checks": {
            "type_ok": type_ok,
            "canonicalization_method_ok": method_ok,
            "value_shape_ok": value_shape_ok,
            "value_match": value_match,
        },
        "ok": type_ok and method_ok and value_shape_ok and value_match,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recompute and verify the Fork GLM manifest digest using the repo-local canonicalization method."
    )
    parser.add_argument("manifest", help="Path to governance-layer-manifest.json")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    try:
        result = compute_sha256(Path(args.manifest))
    except Exception as exc:
        error = {
            "ok": False,
            "error": type(exc).__name__,
            "message": str(exc),
        }
        print(json.dumps(error, sort_keys=True, separators=(",", ":")))
        return 2

    if args.compact:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
