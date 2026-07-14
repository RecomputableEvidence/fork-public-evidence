#!/usr/bin/env python3
"""Restricted RFC 8785 JCS canonicalizer for Corpus 001 ledger JSON.

The ledger schema forbids floating-point values. This implementation accepts
null, booleans, strings, arrays, objects, and I-JSON safe integers only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SAFE_INTEGER_MAX = 9007199254740991


class CanonicalizationError(ValueError):
    pass


def _reject_float(value: str) -> None:
    raise CanonicalizationError(
        f"Floating-point values are outside the declared ledger domain: {value}"
    )


def _parse_integer(value: str) -> int:
    parsed = int(value)
    if abs(parsed) > SAFE_INTEGER_MAX:
        raise CanonicalizationError(
            f"Integer exceeds I-JSON safe range: {value}"
        )
    return parsed


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CanonicalizationError(f"Duplicate object key: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    return json.loads(
        text,
        object_pairs_hook=_object_pairs,
        parse_float=_reject_float,
        parse_int=_parse_integer,
        parse_constant=lambda value: (_ for _ in ()).throw(
            CanonicalizationError(f"Non-finite number is forbidden: {value}")
        ),
    )


def _validate_string(value: str) -> None:
    for character in value:
        codepoint = ord(character)
        if 0xD800 <= codepoint <= 0xDFFF:
            raise CanonicalizationError(
                "Unpaired UTF-16 surrogate code points are forbidden."
            )


def _utf16_sort_key(value: str) -> bytes:
    _validate_string(value)
    return value.encode("utf-16-be")


def _canonicalize(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int) and not isinstance(value, bool):
        if abs(value) > SAFE_INTEGER_MAX:
            raise CanonicalizationError(
                f"Integer exceeds I-JSON safe range: {value}"
            )
        return str(value)
    if isinstance(value, float):
        raise CanonicalizationError(
            "Floating-point values are outside the declared ledger domain."
        )
    if isinstance(value, str):
        _validate_string(value)
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    if isinstance(value, list):
        return "[" + ",".join(_canonicalize(item) for item in value) + "]"
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise CanonicalizationError("JSON object keys must be strings.")
            _validate_string(key)
        ordered_keys = sorted(value.keys(), key=_utf16_sort_key)
        members = [
            _canonicalize(key) + ":" + _canonicalize(value[key])
            for key in ordered_keys
        ]
        return "{" + ",".join(members) + "}"
    raise CanonicalizationError(
        f"Unsupported JSON value type: {type(value).__name__}"
    )


def canonicalize_bytes(value: Any) -> bytes:
    return _canonicalize(value).encode("utf-8")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_expected_digest(path: Path) -> str:
    token = path.read_text(encoding="ascii").strip().split()[0]
    if len(token) != 64 or any(
        character not in "0123456789abcdefABCDEF"
        for character in token
    ):
        raise CanonicalizationError(
            f"Detached digest is not a SHA-256 hexadecimal value: {path}"
        )
    return token.lower()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--digest-output", type=Path)
    parser.add_argument("--verify-digest", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        value = load_json_strict(args.ledger)
        canonical = canonicalize_bytes(value)
        digest = digest_bytes(canonical)

        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_bytes(canonical)

        if args.digest_output is not None:
            args.digest_output.parent.mkdir(parents=True, exist_ok=True)
            args.digest_output.write_text(
                digest + "\n",
                encoding="ascii",
                newline="\n",
            )

        verified = None
        if args.verify_digest is not None:
            expected = read_expected_digest(args.verify_digest)
            verified = digest == expected
            if not verified:
                raise CanonicalizationError(
                    f"Digest mismatch: expected {expected}, computed {digest}"
                )

        result = {
            "canonicalizer": (
                "canonicalize_corpus_source_selection_ledger_v0_1.py"
            ),
            "profile": "JCS_RFC8785",
            "numeric_domain": "I_JSON_SAFE_INTEGER_NO_FLOAT",
            "canonical_byte_length": len(canonical),
            "sha256": digest,
            "detached_digest_verified": verified,
            "state": "PASS",
        }

        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            print(
                f"PASS: {len(canonical)} canonical bytes; SHA-256 {digest}"
            )
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, CanonicalizationError) as exc:
        result = {
            "canonicalizer": (
                "canonicalize_corpus_source_selection_ledger_v0_1.py"
            ),
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