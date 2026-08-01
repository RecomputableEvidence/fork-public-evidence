from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/check_pr107_provider_result_admission_v0_1.py"
SPEC = importlib.util.spec_from_file_location("pr107_admission_checker", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def copy_surface(tmp_path: Path) -> Path:
    files = [
        CHECKER.RECORD,
        CHECKER.RECEIPT,
        CHECKER.RUN,
        CHECKER.ARTIFACT,
        CHECKER.RECONCILIATION,
        CHECKER.CI_WORKFLOW,
    ]
    for relative in files:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, destination)
    return tmp_path


def codes(findings: list[dict[str, str]]) -> set[str]:
    return {item["code"] for item in findings}


def test_clean_candidate_conforms() -> None:
    assert CHECKER.verify(ROOT) == []


def test_receipt_cannot_be_promoted_to_pass(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.RECEIPT
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["status"] = "PASS"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    findings = CHECKER.verify(root)
    assert "SOURCE_DIGEST_MISMATCH" in codes(findings)
    assert "PROVIDER_RECEIPT_BOUNDARY_INVALID" in codes(findings)


def test_retry_budget_cannot_be_replenished(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.RECORD
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["authorized_request"]["remaining_authorized_calls"] = 1
    payload["disposition"]["additional_uppercase_retry_authorized"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    findings = CHECKER.verify(root)
    assert "ADMISSION_RECORD_SEMANTICS_INVALID" in codes(findings)


def test_pair_001_cannot_be_authorized(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.RECORD
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["disposition"]["pair_001_execution_authorized"] = True
    payload["admission_effect"]["admits_pair_001_result"] = True
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    findings = CHECKER.verify(root)
    assert "ADMISSION_RECORD_SEMANTICS_INVALID" in codes(findings)


def test_preservation_tip_ci_route_is_required(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.CI_WORKFLOW
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("      - preservation/clean-continuance-v0.1\n", ""),
        encoding="utf-8",
    )
    findings = CHECKER.verify(root)
    assert "PRESERVATION_TIP_CI_ROUTE_MISSING" in codes(findings)


def test_draft_reconciliation_cannot_authorize_merge(tmp_path: Path) -> None:
    root = copy_surface(tmp_path)
    path = root / CHECKER.RECONCILIATION
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["pull_requests"][0]["merge_authorized"] = True
    payload["effects"]["merge_authorizations"] = 1
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    findings = CHECKER.verify(root)
    assert "OPEN_PR_RECONCILIATION_INVALID" in codes(findings)
