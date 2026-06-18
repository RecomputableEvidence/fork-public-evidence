from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "CONTROLLED_PILOT_SYNTHETIC_DRY_RUN_CORPUS_v0_1.md"
HARDENING_DOC = ROOT / "docs" / "CONTROLLED_PILOT_SYNTHETIC_CORPUS_STRUCTURAL_OUTCOME_HARDENING_v0_1_1.md"
SCHEMA = ROOT / "schemas" / "controlled_pilot_synthetic_dry_run_corpus_v0_1.schema.json"
MANIFEST = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "manifest_v0_1.json"
EXPORTS = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus" / "exports"
EXAMPLE_ROOT = ROOT / "examples" / "controlled_pilot_synthetic_dry_run_corpus"

STATUTORY_NON_CLAIM = "does_not_claim_statutory_review_process"
NEW_EXPORT_NAME = "synthetic_evidence_boundary_records_v0_1.jsonl"
OLD_EXPORT_NAME = "synthetic_prior_auth_denial_internal_appeals_batch_v0_1.jsonl"

STRUCTURAL_OUTCOMES = {
    "BOUNDARY_PRESERVED",
    "POINTER_UNRESOLVED",
    "EXPANSION_DETECTED",
}

LEGACY_OUTCOMES = {
    "PASS",
    "INDETERMINATE",
    "FAIL",
}


def _all_machine_artifacts():
    yield SCHEMA
    yield MANIFEST
    for path in EXAMPLE_ROOT.rglob("*"):
        if path.suffix in {".json", ".jsonl"}:
            yield path


def _json_values(value):
    if isinstance(value, dict):
        for key, inner in value.items():
            yield key
            yield from _json_values(inner)
    elif isinstance(value, list):
        for inner in value:
            yield from _json_values(inner)
    else:
        yield value


def _outcome_like_values(value):
    if isinstance(value, dict):
        for key, inner in value.items():
            key_lower = str(key).lower()
            if any(token in key_lower for token in ("outcome", "status", "result", "validation")):
                if not isinstance(inner, (dict, list)):
                    yield str(inner)
            yield from _outcome_like_values(inner)
    elif isinstance(value, list):
        for inner in value:
            yield from _outcome_like_values(inner)


def test_primary_export_filename_removes_batch_surface():
    assert not (EXPORTS / OLD_EXPORT_NAME).exists()
    assert (EXPORTS / NEW_EXPORT_NAME).exists()

    for path in _all_machine_artifacts():
        text = path.read_text(encoding="utf-8")
        assert OLD_EXPORT_NAME not in text
        assert "internal_appeals_batch" not in text


def test_statutory_process_non_claim_is_visible_and_machine_readable():
    assert STATUTORY_NON_CLAIM in DOC.read_text(encoding="utf-8")
    assert STATUTORY_NON_CLAIM in HARDENING_DOC.read_text(encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_values = {str(v) for v in _json_values(manifest)}
    assert STATUTORY_NON_CLAIM in manifest_values


def test_machine_artifacts_use_fork_native_structural_outcomes():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _all_machine_artifacts())

    for expected in STRUCTURAL_OUTCOMES:
        assert expected in combined

    for legacy in LEGACY_OUTCOMES:
        assert f'": "{legacy}"' not in combined
        assert f'"{legacy}",' not in combined


def test_pointer_unresolved_never_collapses_to_boundary_preserved():
    for path in EXAMPLE_ROOT.rglob("*.jsonl"):
        for raw in path.read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue

            record = json.loads(raw)
            outcome_values = set(_outcome_like_values(record))

            if "POINTER_UNRESOLVED" in outcome_values:
                assert "BOUNDARY_PRESERVED" not in outcome_values, (
                    f"Unresolved pointer state collapsed into preserved outcome in {path}"
                )


def test_expansion_detected_is_structural_not_domain_denial():
    text = HARDENING_DOC.read_text(encoding="utf-8")
    assert "not clinical denial" in text
    assert "not claim approval" in text
    assert "not approval with warnings" in text
