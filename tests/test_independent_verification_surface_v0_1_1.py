from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

pytest.importorskip(
    "yaml",
    reason="independent verification requires the claim-admission dependency lock",
    exc_type=ImportError,
)

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_independent_verification_surface_v0_1_1.py"
POLICY = ROOT / "policies/independent-verification/INDEPENDENT_VERIFICATION_POLICY_v0_1_1.json"
POLICY_SCHEMA = ROOT / "schemas/independent_verification_policy_v0_1_1.schema.json"
PLAN_SCHEMA = ROOT / "schemas/independent_verification_plan_v0_1_1.schema.json"
RECEIPT_SCHEMA = ROOT / "schemas/independent_verification_receipt_v0_1_1.schema.json"
PLAN = ROOT / "verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json"
RECEIPT = ROOT / "receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json"


def load_module():
    sys.path.insert(0, str(ROOT / "tools"))
    spec = importlib.util.spec_from_file_location("ivs_v011", CHECKER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IVS = load_module()


def strict(path: Path):
    return IVS.strict_json_file(path)


def test_schemas_policy_plan_and_receipt_are_valid() -> None:
    for path in (POLICY_SCHEMA, PLAN_SCHEMA, RECEIPT_SCHEMA):
        jsonschema.Draft7Validator.check_schema(strict(path))
    jsonschema.Draft7Validator(strict(POLICY_SCHEMA), format_checker=jsonschema.FormatChecker()).validate(strict(POLICY))
    jsonschema.Draft7Validator(strict(PLAN_SCHEMA), format_checker=jsonschema.FormatChecker()).validate(strict(PLAN))
    jsonschema.Draft7Validator(strict(RECEIPT_SCHEMA), format_checker=jsonschema.FormatChecker()).validate(strict(RECEIPT))


def test_non_finite_json_and_duplicate_keys_are_rejected(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"a":1,"a":2}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate key"):
        strict(duplicate)
    non_finite = tmp_path / "nan.json"
    non_finite.write_text('{"a":NaN}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="Non-finite"):
        strict(non_finite)


def test_inconclusive_receipt_is_schema_valid() -> None:
    receipt = IVS.empty_receipt(Path("missing-plan.json"))
    receipt["control_errors"] = ["plan missing"]
    receipt["result"]["control_error_count"] = 1
    IVS.schema_validate(receipt, RECEIPT_SCHEMA)
    assert receipt["result"]["verdict"] == "INCONCLUSIVE_EVIDENCE_GAP"


def test_precedence_preserves_mixed_contradiction_as_inconclusive() -> None:
    verdict, ok = IVS.classify(
        control_errors=["missing evidence"],
        contradicted_count=2,
        inconclusive_count=1,
    )
    assert verdict == "INCONCLUSIVE_EVIDENCE_GAP"
    assert ok is False


def test_assertion_ids_must_be_unique() -> None:
    plan = {"assertions": [{"assertion_id": "A"}, {"assertion_id": "A"}]}
    assert IVS.duplicate_assertion_ids(plan) == ["A"]


def test_external_observation_requires_time_and_attribution() -> None:
    schema = strict(PLAN_SCHEMA)
    plan = strict(PLAN)
    damaged = json.loads(json.dumps(plan))
    damaged["external_observations"][0].pop("observed_at_utc")
    assert list(jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker()).iter_errors(damaged))


def test_git_mode_distinguishes_symlink(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "IVS Test"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "ivs@example.invalid"], cwd=repo, check=True)
    target = repo / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    link = repo / "link.txt"
    try:
        link.symlink_to("target.txt")
    except OSError:
        pytest.skip("symlink creation is unavailable")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=repo, check=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    entry = IVS.git_tree_entry(repo, commit, "link.txt")
    assert entry["mode"] == "120000"
    assert entry["mode"] not in IVS.REGULAR_MODES


def test_committed_receipt_recomputes_byte_exactly() -> None:
    completed = subprocess.run(
        [sys.executable, str(CHECKER), "--repo-root", str(ROOT), "--plan", str(PLAN.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout.decode() + completed.stderr.decode()
    assert completed.stdout == RECEIPT.read_bytes()
