from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HASHER = REPO_ROOT / "tools/hash_corpus_source_artifacts_v0_1.py"
RENDERER = REPO_ROOT / "tools/render_corpus_source_selection_ledger_v0_1.py"
LEDGER = REPO_ROOT / (
    "manifests/experiment-meta-evidence/corpus-001/"
    "FORK_META_EVIDENCE_CORPUS_001_SOURCE_SELECTION_LEDGER_v0_1.json"
)


def test_source_hashing_preserves_exact_bytes(tmp_path: Path):
    source = tmp_path / "source.bin"
    original = b"\x00\x01\r\nCorpus-001\xff\x10"
    source.write_bytes(original)

    completed = subprocess.run(
        [
            sys.executable,
            str(HASHER),
            str(source),
            "--artifact-id",
            "SRC-C001-999",
            "--json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert source.read_bytes() == original
    assert hashlib.sha256(original).hexdigest() in completed.stdout


def test_markdown_rendering_does_not_modify_ledger(tmp_path: Path):
    before = LEDGER.read_bytes()
    output = tmp_path / "projection.md"

    completed = subprocess.run(
        [
            sys.executable,
            str(RENDERER),
            str(LEDGER),
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert LEDGER.read_bytes() == before

    projection = output.read_text(encoding="utf-8")
    assert "canonical_private_locator" not in projection
    assert "PRIVATE_CORPUS_001/" not in projection
    assert "Non-canonical human-readable projection" in projection