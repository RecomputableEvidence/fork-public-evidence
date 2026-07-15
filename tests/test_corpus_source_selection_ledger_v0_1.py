from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEDGER = REPO_ROOT / (
    "manifests/experiment-meta-evidence/corpus-001/"
    "FORK_META_EVIDENCE_CORPUS_001_SOURCE_SELECTION_LEDGER_v0_1.json"
)
DIGEST = LEDGER.with_suffix(".jcs.sha256")
CHECKER = REPO_ROOT / "tools/check_corpus_source_selection_ledger_v0_1.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("corpus_checker", CHECKER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_initial_draft_ledger_conforms():
    checker_source = CHECKER.read_text(encoding="utf-8")
    assert "RefResolver" not in checker_source
    assert "from referencing import Registry, Resource" in checker_source
    assert "registry=registry" in checker_source

    checker = load_checker()
    result = checker.check_ledger(LEDGER, DIGEST)
    assert result["state"] == "CONFORMING"
    assert result["defect_count"] == 0
    assert result["observation_count"] == 6
    assert result["detached_digest_state"] == "PASS"
    assert result["selection_cutoff_utc"] is not None
    assert result["acquisition_opening_transition_state"] == "PASS"

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    opening = [
        transition
        for transition in ledger["transition_history"]
        if transition["transition_id"] == "C001-TRANSITION-002"
    ]
    assert len(opening) == 1
    assert (
        opening[0]["occurred_at_utc"]
        == ledger["experiment_definition"]["selection_cutoff_utc"]
    )
    assert (
        opening[0]["previous_ledger_digest"]
        == "c4de5c6f6dfdbb00b251453bbe414b47cf6a4388d13f8f1f4841f4d2970a1382"
    )
    assert opening[0]["resulting_ledger_digest"] is None


def test_open_null_slot_blocks_admission_freeze(tmp_path: Path):
    checker = load_checker()
    canonicalizer = checker.load_module(
        checker.CANONICALIZER_PATH,
        "test_canonicalizer_freeze",
    )
    ledger = canonicalizer.load_json_strict(LEDGER)
    ledger["ledger_status"] = "ADMISSION_FROZEN"

    candidate = tmp_path / "ledger.json"
    candidate.write_text(
        json.dumps(ledger, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    digest = tmp_path / "ledger.jcs.sha256"
    digest.write_text(
        canonicalizer.digest_bytes(
            canonicalizer.canonicalize_bytes(ledger)
        )
        + "\n",
        encoding="ascii",
        newline="\n",
    )

    result = checker.check_ledger(candidate, digest)
    codes = {defect["code"] for defect in result["defects"]}
    assert result["state"] == "NON_CONFORMING"
    assert "ADMISSION_FREEZE_BLOCKED_BY_OPEN_SLOT" in codes


def test_candidate_cannot_be_admitted_without_metadata(tmp_path: Path):
    checker = load_checker()
    canonicalizer = checker.load_module(
        checker.CANONICALIZER_PATH,
        "test_canonicalizer_admission",
    )
    ledger = canonicalizer.load_json_strict(LEDGER)
    observation = ledger["observations"][0]
    observation["selection_status"] = "ADMITTED"
    observation["admitted"] = True

    candidate = tmp_path / "ledger.json"
    candidate.write_text(
        json.dumps(ledger, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    digest = tmp_path / "ledger.jcs.sha256"
    digest.write_text(
        canonicalizer.digest_bytes(
            canonicalizer.canonicalize_bytes(ledger)
        )
        + "\n",
        encoding="ascii",
        newline="\n",
    )

    result = checker.check_ledger(candidate, digest)
    codes = {defect["code"] for defect in result["defects"]}
    assert result["state"] == "NON_CONFORMING"
    assert "ADMITTED_SOURCE_METADATA_INCOMPLETE" in codes
    assert "ADMITTED_WITHOUT_CONFIRMED_ELIGIBILITY" in codes


def test_absolute_private_path_is_rejected(tmp_path: Path):
    checker = load_checker()
    canonicalizer = checker.load_module(
        checker.CANONICALIZER_PATH,
        "test_canonicalizer_private_path",
    )
    ledger = canonicalizer.load_json_strict(LEDGER)
    ledger["observations"][0]["admission"][
        "admission_reason"
    ] = "Source located at C:\\private\\source.txt"

    candidate = tmp_path / "ledger.json"
    candidate.write_text(
        json.dumps(ledger, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    digest = tmp_path / "ledger.jcs.sha256"
    digest.write_text(
        canonicalizer.digest_bytes(
            canonicalizer.canonicalize_bytes(ledger)
        )
        + "\n",
        encoding="ascii",
        newline="\n",
    )

    result = checker.check_ledger(candidate, digest)
    codes = {defect["code"] for defect in result["defects"]}
    assert result["state"] == "NON_CONFORMING"
    assert "ABSOLUTE_PRIVATE_PATH_DISCLOSED" in codes