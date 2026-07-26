from __future__ import annotations

import copy
import importlib.util
import json
import shutil
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = (
    ROOT / "tools/check_longitudinal_exterior_recomputation_package_v0_3_1.py"
)


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "fork_longitudinal_exterior_recomputation_package_v0_3_1",
        CHECKER_PATH,
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_template(checker, pr: int) -> dict:
    relative = checker.TEMPLATE_91 if pr == 91 else checker.TEMPLATE_92
    return checker.strict_load(ROOT / relative)


def completed_receipt(checker, pr: int, *, disposition: str) -> dict:
    receipt = load_template(checker, pr)
    expected = checker.EXPECTED_TARGETS[pr]
    receipt["receipt_id"] = f"FORK_EXTERIOR_RECOMPUTATION_PR{pr}_TEST_v0_1"
    receipt["review_target"]["acquired_head_sha"] = expected["head_sha"]
    receipt["review_target"]["acquired_tree_sha"] = expected["tree_sha"]
    receipt["review_target"]["acquisition_method"] = "FRESH_EXACT_COMMIT_CHECKOUT"
    receipt["reviewer_disclosure"] = {
        "reviewer_id": "TEST_REVIEWER",
        "affiliation": "TEST_ONLY",
        "relationship_to_fork": "NONE",
        "prior_exposure": "NONE",
        "independence_class": "ARMS_LENGTH_DISCLOSED",
    }
    receipt["environment"]["observed_os"] = "TEST_OS"
    receipt["environment"]["python_version"] = "Python 3.12.0"
    receipt["environment"]["dependency_install_exit_code"] = 0
    receipt["executions"] = [
        {
            "command": "python checker.py",
            "exit_code": 0,
            "stdout_sha256": "1" * 64,
            "stderr_sha256": "2" * 64,
            "observed_result": expected["checker_status"],
        },
        {
            "command": "python -m pytest focused.py -q",
            "exit_code": 0,
            "stdout_sha256": "3" * 64,
            "stderr_sha256": "4" * 64,
            "observed_result": f"{expected['focused_passed']} passed",
        },
    ]
    receipt["measurements"]["checker_status"] = expected["checker_status"]
    receipt["measurements"]["state_vector_sha256"] = expected[
        "state_vector_sha256"
    ]
    receipt["measurements"]["closure_node_digest_sha256"] = expected[
        "closure_node_digest_sha256"
    ]
    receipt["measurements"]["focused_tests"] = {
        "passed": expected["focused_passed"],
        "failed": 0,
        "skipped": 0,
        "exit_code": 0,
        "not_run_reason": None,
    }
    receipt["raw_output_artifacts"] = [
        {
            "path": f"pr{pr}-checker.stdout",
            "sha256": "5" * 64,
            "size_bytes": 100,
        }
    ]
    receipt["disposition"] = disposition
    receipt["reviewer_attestation"] = {
        "statement": "Recorded from the commands and artifacts identified here.",
        "recorded_at_utc": "2026-07-24T12:00:00Z",
    }
    return receipt


def seal(checker, receipt: dict) -> None:
    receipt["integrity"]["receipt_payload_sha256"] = checker.canonical_sha256(
        checker.receipt_integrity_payload(receipt)
    )


def materialize_package(checker, tmp_path: Path) -> Path:
    for relative in checker.EXPECTED_PACKAGE_PATHS | {checker.MANIFEST.as_posix()}:
        source = ROOT / relative
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return tmp_path


def test_exact_review_package_conforms_without_claiming_review() -> None:
    checker = load_checker()
    result = checker.evaluate(ROOT)
    assert result["findings"] == []
    assert result["status"] == "EXTERIOR_RECOMPUTATION_PACKAGE_CONFORMS"
    assert result["review_results_present"] is False
    assert result["standing"] == "REVIEW_PACKAGE_CANDIDATE_NO_REVIEW_RESULT"


def test_receipt_schema_is_valid_and_templates_are_pending() -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    jsonschema.Draft7Validator.check_schema(schema)
    for pr in (91, 92):
        template = load_template(checker, pr)
        jsonschema.Draft7Validator(schema).validate(template)
        assert template["disposition"] == (
            "UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION"
        )
        assert template["executions"] == []
        assert template["raw_output_artifacts"] == []


@pytest.mark.parametrize("pr", [91, 92])
def test_completed_conformance_receipt_recomputes(pr: int) -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    receipt = completed_receipt(
        checker,
        pr,
        disposition="REPRODUCED_WITHIN_DECLARED_SCOPE",
    )
    seal(checker, receipt)
    assert checker.validate_receipt(receipt, schema, allow_pending=False) == []


def test_false_conformance_is_rejected() -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    receipt = completed_receipt(
        checker,
        92,
        disposition="REPRODUCED_WITHIN_DECLARED_SCOPE",
    )
    receipt["measurements"]["closure_node_digest_sha256"] = "0" * 64
    seal(checker, receipt)
    codes = {
        item["code"]
        for item in checker.validate_receipt(receipt, schema, allow_pending=False)
    }
    assert "CONFORMANCE_DISPOSITION_CONTRADICTS_MEASUREMENT" in codes


def test_adverse_receipt_is_preserved_not_forced_to_pass() -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    receipt = completed_receipt(
        checker,
        91,
        disposition="REPRODUCED_WITH_CORRECTION_REQUIRED",
    )
    receipt["measurements"]["state_vector_sha256"] = "0" * 64
    receipt["findings"] = [
        {
            "code": "REVIEWER_OBSERVED_MISMATCH",
            "severity": "MINOR",
            "detail": "Observed state vector differs from the comparison value.",
            "evidence": "pr91-checker.stdout",
        }
    ]
    seal(checker, receipt)
    assert checker.validate_receipt(receipt, schema, allow_pending=False) == []


def test_incomplete_receipt_preserves_acquisition_blocker() -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    receipt = load_template(checker, 92)
    receipt["receipt_id"] = "FORK_EXTERIOR_RECOMPUTATION_PR92_INCOMPLETE_v0_1"
    receipt["reviewer_disclosure"] = {
        "reviewer_id": "TEST_REVIEWER",
        "affiliation": "TEST_ONLY",
        "relationship_to_fork": "NONE",
        "prior_exposure": "NONE",
        "independence_class": "ARMS_LENGTH_DISCLOSED",
    }
    receipt["findings"] = [
        {
            "code": "TARGET_ACQUISITION_BLOCKED",
            "severity": "UNRESOLVED",
            "detail": "Exact target could not be acquired.",
            "evidence": "git-fetch.stderr",
        }
    ]
    receipt["disposition"] = "UNRESOLVED_INCOMPLETE"
    receipt["reviewer_attestation"] = {
        "statement": "The unresolved acquisition result is recorded as observed.",
        "recorded_at_utc": "2026-07-24T12:00:00Z",
    }
    seal(checker, receipt)
    assert checker.validate_receipt(receipt, schema, allow_pending=False) == []


def test_effect_promotion_is_rejected_by_schema() -> None:
    checker = load_checker()
    schema = checker.load_schema(ROOT)
    receipt = load_template(checker, 91)
    receipt["effects"]["admission"] = "ADMITTED"
    errors = list(jsonschema.Draft7Validator(schema).iter_errors(receipt))
    assert errors


def test_package_byte_mutation_breaks_manifest(tmp_path: Path) -> None:
    checker = load_checker()
    package_root = materialize_package(checker, tmp_path)
    readme = package_root / checker.README
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nmutation\n",
        encoding="utf-8",
    )
    result = checker.evaluate(package_root)
    assert "PACKAGE_MANIFEST_DIVERGENCE" in result["finding_codes"]


def test_stack_coordinates_are_bottom_up_and_exact() -> None:
    checker = load_checker()
    stack = checker.strict_load(ROOT / checker.STACK)
    assert [item["pull_request"] for item in stack["stack"]] == [89, 90, 91, 92]
    assert stack["exterior_recomputation_order"] == [91, 92]
    assert stack["stack"][3]["exact_predecessor"] == (
        checker.EXPECTED_TARGETS[91]["head_sha"]
    )


def test_reviewer_environments_are_required_outside_checkout() -> None:
    checker = load_checker()
    for relative in (checker.ENVELOPE_91, checker.ENVELOPE_92):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "outside the repository checkout" in text
        assert 'review_env_root="$(mktemp -d)"' in text
        assert "[IO.Path]::GetTempPath()" in text
        assert "git status --short --untracked-files=all" in text
        assert ".venv-fork-review" not in text
