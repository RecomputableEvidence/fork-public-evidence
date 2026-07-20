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


def write_bound_json(root: Path, checker, relative: str, value: dict) -> dict[str, str]:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(checker.pretty_json(value), encoding="utf-8", newline="\n")
    return {"path": relative, "sha256": checker.sha256(path)}


def valid_uppercase_authorization(root: Path, checker) -> dict[str, str]:
    anchor = {
        "schema_version": "v0.1",
        "record_kind": "explicit_external_authorization_anchor",
        "status": "ACTIVE",
        "authorization_id": "FSS-AUTH-UPPERCASE-RETRY-TEST-001",
        "authorization_kind": "ONE_TIME_UPPERCASE_PROVIDER_VALIDATION_RETRY",
        "subject": {
            "experiment_id": "cross_system_claim_handoff_v0_1",
            "pair_id": "PAIR-001",
        },
        "authorized_transition_ids": sorted(checker.UPPERCASE_AUTH_TRANSITIONS),
        "request_sha256": checker.UPPERCASE_REQUEST_SHA,
        "maximum_provider_calls": 1,
        "authorized_at_utc": "2026-07-19T09:20:00+00:00",
        "not_before_utc": "2026-07-20T07:55:24.374494+00:00",
        "external_source": {
            "source_kind": "EXPLICIT_USER_AUTHORIZATION_TEST_FIXTURE",
            "source_id": "fixture:FSS-AUTH-UPPERCASE-RETRY-TEST-001",
            "source_sha256": "1" * 64,
        },
        "execution_boundary": {
            "automatic_execution": False,
            "pair_001_execution_authorized": False,
            "readiness_promotion_authorized": False,
        },
    }
    return write_bound_json(
        root,
        checker,
        "docs/sequence-surface/authorizations/FSS_AUTH_UPPERCASE_RETRY_TEST_001.json",
        anchor,
    )


def append_transition(
    ledger: dict,
    contract: dict,
    checker,
    transition_id: str,
    occurred_at_utc: str,
    authority_reference: dict[str, str],
    evidence_refs: list[dict],
) -> None:
    transition = checker.transition_map(contract)[transition_id]
    assert ledger["events"][-1]["to_state"] == transition["from_state"]
    ordinal = len(ledger["events"]) + 1
    event = {
        "ordinal": ordinal,
        "event_id": f"FSS-PAIR001-E{ordinal:03d}",
        "transition_id": transition_id,
        "event_type": transition["event_type"],
        "occurred_at_utc": occurred_at_utc,
        "from_state": transition["from_state"],
        "to_state": transition["to_state"],
        "authority": {
            "requirement": "EXPLICIT_EXTERNAL_AUTHORIZATION",
            "present": True,
            "reference": copy.deepcopy(authority_reference),
            "effect": "NONE",
        },
        "effects": copy.deepcopy(transition["expected_effects"]),
        "evidence_refs": copy.deepcopy(evidence_refs),
        "previous_event_sha256": ledger["events"][-1]["event_sha256"],
        "event_sha256": "",
        "non_claims": ["Adversarial fixture event; no provider execution or Pair-001 authority."],
    }
    event["event_sha256"] = checker.event_sha256(event)
    ledger["events"].append(event)


def anchor_evidence(reference: dict[str, str]) -> list[dict]:
    return [
        {
            "path": reference["path"],
            "sha256": reference["sha256"],
            "standing": "EXTERNAL_AUTHORIZATION_ANCHOR",
        }
    ]


def retry_receipt(root: Path, checker, outcome: str) -> dict[str, str]:
    outcomes = {
        "SUCCESS": {
            "status": "PASS",
            "http_status": 200,
            "passed": True,
            "response_body_sha256": "3" * 64,
        },
        "IDENTICAL_FAILURE": {
            "status": "FAIL",
            "http_status": 500,
            "passed": False,
            "response_body_sha256": checker.IDENTICAL_FAILURE_BODY_SHA,
        },
        "DIFFERENT_OUTCOME": {
            "status": "FAIL",
            "http_status": 429,
            "passed": False,
            "response_body_sha256": "4" * 64,
        },
    }
    selected = outcomes[outcome]
    receipt = {
        "schema_version": "v0.1.2",
        "receipt_id": "CSH_PROVIDER_VALIDATION_RECEIPT_v0_1_2",
        "classification": "PROVIDER_VALIDATION_ONLY_EXCLUDED_FROM_CSH_BASELINE",
        "status": selected["status"],
        "observed_at_utc": "2026-07-20T07:56:00+00:00",
        "subject_commit": "2" * 40,
        "workflow_run_id": 999999,
        "pair_001_calls_performed": 0,
        "provider_validation_calls_performed": 1,
        "calls": [
            {
                "provider": "DeepSeek",
                "requested_model": checker.UPPERCASE_MODEL_ID,
                "request_sha256": checker.UPPERCASE_REQUEST_SHA,
                "http_status": selected["http_status"],
                "passed": selected["passed"],
                "response_body_sha256": selected["response_body_sha256"],
                "response_body_written": False,
            }
        ],
    }
    return write_bound_json(
        root,
        checker,
        f"docs/sequence-surface/fixtures/{outcome}_RETRY_RECEIPT.json",
        receipt,
    )


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
        if "mutation" not in case:
            continue
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


def test_bound_authorization_and_retry_branch_adversarial_fixtures(tmp_path: Path) -> None:
    checker = load_checker()
    fixture_set = json.loads(FIXTURES.read_text(encoding="utf-8"))
    cases = [case for case in fixture_set["cases"] if "scenario" in case]
    assert {case["class"] for case in cases} == {
        "FORGED_AUTHORIZATION_REFERENCE",
        "PREMATURE_UPPERCASE_RETRY",
        "FALSE_OUTCOME_CLASSIFICATION",
    }
    for case in cases:
        root = tmp_path / case["case_id"]
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
        ledger = checker.strict_load(root / checker.LEDGER)
        contract = checker.strict_load(root / checker.CONTRACT)
        scenario = case["scenario"]
        if scenario in {
            "append_authorization_with_missing_bound_anchor",
            "append_authorization_with_wrong_digest",
        }:
            if scenario == "append_authorization_with_missing_bound_anchor":
                forged = {
                    "path": "docs/sequence-surface/authorizations/MISSING.json",
                    "sha256": "0" * 64,
                }
            else:
                forged = valid_uppercase_authorization(root, checker)
                forged["sha256"] = "0" * 64
            append_transition(
                ledger,
                contract,
                checker,
                "FSS-PAIR001-T012",
                "2026-07-19T09:30:00+00:00",
                forged,
                copy.deepcopy(ledger["events"][-1]["evidence_refs"]),
            )
        else:
            authorization = valid_uppercase_authorization(root, checker)
            append_transition(
                ledger,
                contract,
                checker,
                "FSS-PAIR001-T012",
                "2026-07-19T09:30:00+00:00",
                authorization,
                anchor_evidence(authorization),
            )
            time_gate = (
                "2026-07-20T07:55:23.374494+00:00"
                if scenario == "append_valid_authorization_and_early_time_gate"
                else "2026-07-20T07:55:24.374494+00:00"
            )
            append_transition(
                ledger,
                contract,
                checker,
                "FSS-PAIR001-T013",
                time_gate,
                authorization,
                anchor_evidence(authorization),
            )
            if scenario == "classify_identical_failure_receipt_as_success":
                receipt = retry_receipt(root, checker, "IDENTICAL_FAILURE")
                append_transition(
                    ledger,
                    contract,
                    checker,
                    "FSS-PAIR001-T014",
                    "2026-07-20T07:57:00+00:00",
                    authorization,
                    [
                        {
                            "path": receipt["path"],
                            "sha256": receipt["sha256"],
                            "standing": "EXCLUDED_DIAGNOSTIC_EVIDENCE",
                        }
                    ],
                )
        result = checker.evaluate(root, ledger_override=ledger, compare_projection=False)
        assert result["result"]["valid"] is False, (case["case_id"], result["errors"])
        assert case["expected_error"] in result["error_codes"], (case["case_id"], result["errors"])


def test_each_retry_outcome_branch_requires_its_matching_bound_receipt(tmp_path: Path) -> None:
    checker = load_checker()
    branches = {
        "FSS-PAIR001-T014": "SUCCESS",
        "FSS-PAIR001-T015": "IDENTICAL_FAILURE",
        "FSS-PAIR001-T016": "DIFFERENT_OUTCOME",
    }
    for transition_id, outcome in branches.items():
        root = tmp_path / outcome
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git"))
        ledger = checker.strict_load(root / checker.LEDGER)
        contract = checker.strict_load(root / checker.CONTRACT)
        authorization = valid_uppercase_authorization(root, checker)
        append_transition(
            ledger,
            contract,
            checker,
            "FSS-PAIR001-T012",
            "2026-07-19T09:30:00+00:00",
            authorization,
            anchor_evidence(authorization),
        )
        append_transition(
            ledger,
            contract,
            checker,
            "FSS-PAIR001-T013",
            "2026-07-20T07:55:24.374494+00:00",
            authorization,
            anchor_evidence(authorization),
        )
        receipt = retry_receipt(root, checker, outcome)
        append_transition(
            ledger,
            contract,
            checker,
            transition_id,
            "2026-07-20T07:57:00+00:00",
            authorization,
            [
                {
                    "path": receipt["path"],
                    "sha256": receipt["sha256"],
                    "standing": "EXCLUDED_DIAGNOSTIC_EVIDENCE",
                }
            ],
        )
        result = checker.evaluate(root, ledger_override=ledger, compare_projection=False)
        assert result["errors"] == [], (transition_id, result["errors"])


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
