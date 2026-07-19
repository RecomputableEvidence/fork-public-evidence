from __future__ import annotations

import copy
import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_fork_sequence_surface_v0_1.py"
FIXTURES = ROOT / "tests/fixtures/fork-sequence-surface-v0.1/adversarial_cases_v0_1.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("fork_sequence_surface", CHECKER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def set_nested(target: dict, path: list[str], value) -> None:
    current = target
    for part in path[:-1]:
        current = current[part]
    current[path[-1]] = value


def mutate(ledger: dict, mutation: dict) -> dict:
    changed = copy.deepcopy(ledger)
    events = changed["events"]
    operation = mutation["operation"]
    if operation == "remove_event":
        changed["events"] = [item for item in events if item["event_id"] != mutation["event_id"]]
    elif operation == "swap_events":
        by_id = {item["event_id"]: index for index, item in enumerate(events)}
        left = by_id[mutation["left_event_id"]]
        right = by_id[mutation["right_event_id"]]
        events[left], events[right] = events[right], events[left]
    elif operation == "set_event_field":
        event = next(item for item in events if item["event_id"] == mutation["event_id"])
        set_nested(event, mutation["field_path"], mutation["value"])
    else:
        raise AssertionError(f"unknown mutation operation: {operation}")
    return changed


def test_sequence_surface_recomputes_exact_candidate_projection() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["errors"] == []
    assert result["result"] == {
        "anchor_status": "SEPARATE_SUCCESSOR_REQUIRED",
        "pair_001_execution_effect": "NONE",
        "provider_calls_performed_by_checker": 0,
        "readiness_effect": "NONE",
        "status": "SEQUENCE_SURFACE_CONFORMS_CANDIDATE_NOT_ADMITTED",
        "valid": True,
    }
    assert result["projection"] == checker.strict_load(ROOT / checker.PROJECTION)


def test_projection_exposes_sequence_without_promoting_action() -> None:
    checker = load_checker()
    projection = checker.evaluate(ROOT)["projection"]
    assert projection["sequence"] == {
        "append_only": True,
        "current_state": "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED",
        "currently_eligible_successor_transition_ids": [],
        "declared_successor_transition_ids": ["FSS-PAIR001-T012"],
        "event_count": 11,
        "last_event_id": "FSS-PAIR001-E011",
        "last_event_sha256": "6a6764bd759fb8be972c7e09321369d241164a7ca0bab4cb1bc2aba1c5780b45",
    }
    assert projection["observed_history"]["provider_calls"] == 8
    assert projection["observed_history"]["pair_001_original_attempts"] == 2
    assert projection["observed_history"]["pair_001_repetitions"] == 0
    assert projection["execution_boundary"]["provider_calls_performed_by_sequence_surface_publication"] == 0
    assert projection["execution_boundary"]["pair_001_calls_performed_by_sequence_surface_publication"] == 0
    assert projection["execution_boundary"]["execution_effect"] == "NONE"


def test_event_hash_chain_is_exact() -> None:
    checker = load_checker()
    ledger = checker.strict_load(ROOT / checker.LEDGER)
    previous = checker.GENESIS_HASH
    for event in ledger["events"]:
        assert event["previous_event_sha256"] == previous
        assert event["event_sha256"] == checker.event_sha256(event)
        previous = event["event_sha256"]


def test_all_precommitted_adversarial_cases_fail_closed() -> None:
    checker = load_checker()
    ledger = checker.strict_load(ROOT / checker.LEDGER)
    fixture_set = json.loads(FIXTURES.read_text(encoding="utf-8"))
    observed: set[str] = set()
    for case in fixture_set["cases"]:
        changed = mutate(ledger, case["mutation"])
        result = checker.evaluate(ROOT, ledger_override=changed, compare_projection=False)
        assert result["result"]["valid"] is False, case["case_id"]
        assert case["expected_error"] in result["error_codes"], (case["case_id"], result["errors"])
        observed.add(case["class"])
    assert observed == {
        "SKIPPED_GATE",
        "REORDERED_EVENTS",
        "FORGED_AUTHORIZATION",
        "SILENT_RETRY",
        "FALSE_COMPLETION",
    }


def test_projection_tampering_does_not_change_recomputed_state(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
    checker = load_checker()
    projection_path = root / checker.PROJECTION
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    projection["sequence"]["current_state"] = "PAIR_001_EXECUTION_ELIGIBLE"
    projection_path.write_text(json.dumps(projection, indent=2) + "\n", encoding="utf-8", newline="\n")
    result = checker.evaluate(root)
    assert "PROJECTION_MISMATCH" in result["error_codes"]
    assert result["projection"]["sequence"]["current_state"] == "DRIFT_CLASSIFIED_RETRY_NOT_AUTHORIZED"
    assert result["result"]["pair_001_execution_effect"] == "NONE"


def test_path_escape_is_rejected_before_evidence_read() -> None:
    checker = load_checker()
    ledger = checker.strict_load(ROOT / checker.LEDGER)
    changed = copy.deepcopy(ledger)
    changed["events"][0]["evidence_refs"][0]["path"] = "../outside.json"
    result = checker.evaluate(ROOT, ledger_override=changed, compare_projection=False)
    assert "EVIDENCE_PATH_INVALID" in result["error_codes"]


def test_source_digest_divergence_is_rejected() -> None:
    checker = load_checker()
    ledger = checker.strict_load(ROOT / checker.LEDGER)
    changed = copy.deepcopy(ledger)
    changed["events"][0]["evidence_refs"][0]["sha256"] = "0" * 64
    result = checker.evaluate(ROOT, ledger_override=changed, compare_projection=False)
    assert "SOURCE_ARTIFACT_DIGEST_MISMATCH" in result["error_codes"]


def test_duplicate_keys_and_nonfinite_values_fail_at_parser_boundary(tmp_path: Path) -> None:
    checker = load_checker()
    original = (ROOT / checker.LEDGER).read_text(encoding="utf-8")
    mutations = {
        "duplicate": original.replace(
            '  "schema_version": "v0.1",',
            '  "schema_version": "v0.1",\n  "schema_version": "v0.1",',
            1,
        ),
        "nonfinite": original.replace('  "append_only": true,', '  "append_only": true,\n  "invalid_number": NaN,', 1),
    }
    for name, rendered in mutations.items():
        root = tmp_path / name
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
        (root / checker.LEDGER).write_text(rendered, encoding="utf-8", newline="\n")
        result = checker.evaluate(root)
        assert result["error_codes"] == ["STRICT_JSON_INVALID"]


def test_surface_remains_candidate_and_anchor_is_separate() -> None:
    checker = load_checker()
    contract = checker.strict_load(ROOT / checker.CONTRACT)
    assert contract["status"] == "CANDIDATE_NOT_ADMITTED"
    assert contract["surface_kind"] == "CROSS_SURFACE_SEQUENCE_PROJECTION"
    assert contract["anchor_boundary"] == {
        "status": "REQUIRED_AS_SEPARATE_SUCCESSOR_AFTER_SURFACE_MERGE",
        "must_bind_exact_merge_commit": True,
        "must_bind_successful_workflow_runs": True,
        "provider_call_effect": "NONE",
        "pair_001_execution_effect": "NONE",
        "readiness_effect": "NONE",
    }
    assert "not an admitted seventh modular surface" in contract["non_claims"][0]
