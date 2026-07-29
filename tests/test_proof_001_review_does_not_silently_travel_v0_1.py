from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    ROOT / "tools/run_proof_001_review_does_not_silently_travel_v0_1.py"
)
ROUTE_CHECKER_PATH = ROOT / "tools/check_public_route_freshness_v0_1.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_proof_001_package_recomputes() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_package")
    result = runner.evaluate_package(ROOT)
    assert result["findings"] == []
    assert result["status"] == (
        "PROOF_001_REPRODUCED_PACKAGING_CANDIDATE_NOT_ADMITTED"
    )
    assert result["source_replay_status"] == "LONGITUDINAL_STATE_REPRODUCED"
    assert result["diff_status"] == "LONGITUDINAL_DIFF_REPRODUCED"


def test_proof_001_changed_and_preserved_dimensions_are_derived() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_dimensions")
    result = runner.evaluate_package(ROOT)
    assert result["changed_dimensions"] == [
        "artifact_state",
        "review_state",
        "temporal_closure",
        "unresolved_state",
        "verification_state",
    ]
    assert result["preserved_dimensions"] == [
        "admission_state",
        "authority_state",
        "execution_state",
    ]
    assert result["effects"] == {
        "admission": "NONE",
        "authority": "NONE",
        "execution": "NONE",
        "pair_001_calls": 0,
        "provider_calls": 0,
    }


def test_proof_001_rejects_review_promotion() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_adversarial")
    result = runner.evaluate_package(ROOT)
    assert result["adversarial"]["case_id"] == "FLR-ADV-003"
    assert result["adversarial"]["required_code_observed"] is True
    assert "CURRENT_HEAD_REVIEW_STALE" in result["adversarial"]["finding_codes"]


def test_proof_001_summary_is_mechanically_reproduced() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_summary")
    evidence, rendered = runner.derive_evidence(ROOT)
    committed = (ROOT / runner.SUMMARY_PATH).read_text(encoding="utf-8")
    assert evidence["findings"] == []
    assert committed == rendered


def test_public_route_staleness_is_detected_without_rewriting_history() -> None:
    checker = load_module(ROUTE_CHECKER_PATH, "proof_001_route")
    result = checker.evaluate(ROOT)
    assert result["findings"] == []
    assert result["status"] == "PUBLIC_ROUTE_STALE"
    assert result["expectation_matches"] is True
    assert result["latest_admitted_checkpoint"]["commit_sha"] == (
        "96e17cd5ae8a923b9074cfdfe6718cf0e15611b0"
    )
    assert {item["declared_coordinate"] for item in result["routes"]} == {
        "1241c0084900f2c60f362205525464582e57b4a7"
    }


def test_proof_index_contains_only_proof_001() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_index")
    longitudinal = load_module(
        ROOT / runner.LONGITUDINAL_CHECKER_PATH,
        "proof_001_longitudinal_for_index",
    )
    findings: list[dict[str, str]] = []
    index = runner.validate_index(ROOT, longitudinal, findings)
    assert findings == []
    assert index["proofs"][0]["proof_id"] == "PROOF-001"
    assert len(index["proofs"]) == 1


def test_proof_manifest_binds_complete_candidate_surface() -> None:
    runner = load_module(RUNNER_PATH, "proof_001_manifest")
    longitudinal = load_module(
        ROOT / runner.LONGITUDINAL_CHECKER_PATH,
        "proof_001_longitudinal_for_manifest",
    )
    findings: list[dict[str, str]] = []
    manifest = runner.validate_manifest(ROOT, longitudinal, findings)
    assert findings == []
    assert manifest["standing"] == (
        "BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED"
    )
