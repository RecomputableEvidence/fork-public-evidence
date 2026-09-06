from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_fork_self_standing_projection_v0_1.py"
RECORD = ROOT / (
    "docs/preservation/current-standing/"
    "FORK_SELF_STANDING_PROJECTION_2026_09_06_v0_1_CANDIDATE.json"
)


def load_checker():
    spec = importlib.util.spec_from_file_location("self_standing_projection", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def codes(findings):
    return {item["code"] for item in findings}


def test_self_standing_projection_candidate_conforms() -> None:
    result = load_checker().evaluate()
    assert result["findings"] == []
    assert result["status"] == "SELF_STANDING_PROJECTION_CANDIDATE_CONFORMS_NOT_ADMITTED"
    assert result["claim_count"] == 5


def test_interpretation_provenance_is_required() -> None:
    checker = load_checker()
    record = load_record()
    del record["claims"][4]["interpretation_provenance"]
    assert "CLAIM_KEYS" in codes(checker.validate_record(record))


def test_independence_cannot_collapse_to_blanket_flag() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][0]["independence"] = {"independent": True}
    assert "INDEPENDENCE_KEYS" in codes(checker.validate_record(record))


def test_independent_verification_requires_record() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][0]["verification"]["status"] = "INDEPENDENTLY_VERIFIED"
    assert "VERIFICATION_PROMOTION" in codes(checker.validate_record(record))


def test_current_and_historical_standing_do_not_collapse() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][0]["historical_coordinate"] = "b29b7d95a0f2bfcd3a93ff318359df904a384b05"
    assert "CURRENT_WITH_HISTORICAL_COORDINATE" in codes(checker.validate_record(record))


def test_historical_claim_requires_exact_coordinate() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][3]["historical_coordinate"] = None
    assert "HISTORICAL_COORDINATE" in codes(checker.validate_record(record))


def test_inference_cannot_be_reclassified_as_observation_without_origin_change() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][4]["finding_kind"] = "OBSERVATION"
    found = codes(checker.validate_record(record))
    assert "OBSERVATION_ORIGIN" in found
    assert "OBSERVATION_PROMOTION" in found


def test_derived_claim_requires_interpretation_provenance() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][4]["interpretation_provenance"] = {
        "present": False,
        "kind": "NONE",
        "producer_class": "NONE",
        "method": None,
        "source_evidence_ids": [],
    }
    assert "DERIVED_WITHOUT_INTERPRETATION" in codes(checker.validate_record(record))


def test_interpretation_evidence_refs_must_resolve() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][4]["interpretation_provenance"]["source_evidence_ids"] = ["NO-SUCH-EVIDENCE"]
    assert "INTERPRETATION_EVIDENCE_REF" in codes(checker.validate_record(record))


def test_established_independence_requires_evidence() -> None:
    checker = load_checker()
    record = load_record()
    record["claims"][0]["independence"]["artifact_acquisition"]["evidence_ids"] = []
    assert "INDEPENDENCE_UNEVIDENCED" in codes(checker.validate_record(record))
