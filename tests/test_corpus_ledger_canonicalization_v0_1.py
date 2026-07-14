from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICALIZER = (
    REPO_ROOT / "tools/canonicalize_corpus_source_selection_ledger_v0_1.py"
)
LEDGER = REPO_ROOT / (
    "manifests/experiment-meta-evidence/corpus-001/"
    "FORK_META_EVIDENCE_CORPUS_001_SOURCE_SELECTION_LEDGER_v0_1.json"
)
DIGEST = LEDGER.with_suffix(".jcs.sha256")


def load_canonicalizer():
    spec = importlib.util.spec_from_file_location(
        "corpus_canonicalizer",
        CANONICALIZER,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_canonicalization_is_deterministic_and_digest_matches():
    canonicalizer = load_canonicalizer()
    value = canonicalizer.load_json_strict(LEDGER)

    first = canonicalizer.canonicalize_bytes(value)
    second = canonicalizer.canonicalize_bytes(value)

    assert first == second
    actual = hashlib.sha256(first).hexdigest()
    expected = DIGEST.read_text(encoding="ascii").strip()
    assert actual == expected


def test_object_key_order_is_canonical():
    canonicalizer = load_canonicalizer()
    value = {"z": 1, "a": 2, "nested": {"b": True, "a": None}}
    canonical = canonicalizer.canonicalize_bytes(value)
    assert canonical == b'{"a":2,"nested":{"a":null,"b":true},"z":1}'


def test_duplicate_keys_and_floats_are_rejected(tmp_path: Path):
    canonicalizer = load_canonicalizer()

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        '{"a":1,"a":2}',
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(canonicalizer.CanonicalizationError):
        canonicalizer.load_json_strict(duplicate)

    floating = tmp_path / "floating.json"
    floating.write_text(
        '{"value":1.5}',
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(canonicalizer.CanonicalizationError):
        canonicalizer.load_json_strict(floating)