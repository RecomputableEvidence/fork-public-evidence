#!/usr/bin/env python3
"""Verify the bounded PR #107 provider-result admission candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CHECKER_ID = "FORK_PR107_PROVIDER_RESULT_ADMISSION_CHECKER_v0_1"
BASE = Path("docs/preservation/admission/pr107-provider-result")
RECORD = BASE / "PR107_PROVIDER_RESULT_ADMISSION_RECORD_v0_1.json"
RECEIPT = BASE / "PROVIDER_VALIDATION_ATTESTATION_v0_1_2.json"
RUN = BASE / "RUN_METADATA.json"
ARTIFACT = BASE / "ARTIFACT_METADATA.json"
RECONCILIATION = BASE / "OPEN_PR_RECONCILIATION_AFTER_PR107_v0_1.json"
CI_WORKFLOW = Path(".github/workflows/fork-evidence-ci.yml")
MERGE_SHA = "5cf581c7b95c5ea4e9b662e089fc89f5b552696f"
REQUEST_SHA = "d2c8aabbdda4f17509395aa8a55f607b2b0d52138a251e8da92bb8384a05bcef"
RECEIPT_SHA = "ba8ee806312288f0259e19e43cd84f71e364fdfcbdb8cb1abf68e1fddf09a899"
RUN_SHA = "ec05b0c5ca4a476662f8a45a9159e51e75a2aba24add37115b74ae9eb6ce15ed"
ARTIFACT_SHA = "4d9615d45374c79d3605143cd75e7b2d442b7e2e435f55beed5755a2fd52670a"
EXPECTED_OPEN_PRS = {65, 84, 86, 100, 105, 106}


class DuplicateKeyError(ValueError):
    pass


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicates,
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON token: {token}")
        ),
    )
    if not isinstance(value, dict):
        raise ValueError(f"{path.as_posix()} must contain an object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(findings: list[dict[str, str]], code: str, detail: str, path: Path) -> None:
    findings.append({"code": code, "detail": detail, "path": path.as_posix()})


def verify(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    paths = [RECORD, RECEIPT, RUN, ARTIFACT, RECONCILIATION, CI_WORKFLOW]
    for relative in paths:
        target = root / relative
        if target.is_symlink() or not target.is_file():
            add(findings, "REQUIRED_FILE_MISSING_OR_UNSAFE", "regular file required", relative)
    if findings:
        return findings

    try:
        record = load_json(root / RECORD)
        receipt = load_json(root / RECEIPT)
        run = load_json(root / RUN)
        artifact = load_json(root / ARTIFACT)
        reconciliation = load_json(root / RECONCILIATION)
    except Exception as exc:
        add(findings, "STRICT_JSON_INVALID", str(exc), RECORD)
        return findings

    expected_digests = {
        RECEIPT: RECEIPT_SHA,
        RUN: RUN_SHA,
        ARTIFACT: ARTIFACT_SHA,
    }
    for relative, expected in expected_digests.items():
        observed = digest(root / relative)
        if observed != expected:
            add(findings, "SOURCE_DIGEST_MISMATCH", f"expected={expected}; observed={observed}", relative)

    source = record.get("source_artifact")
    request = record.get("authorized_request")
    observed = record.get("observed_result")
    disposition = record.get("disposition")
    effect = record.get("admission_effect")
    if not all(isinstance(item, dict) for item in (source, request, observed, disposition, effect)):
        add(findings, "ADMISSION_RECORD_SHAPE_INVALID", "required control objects missing", RECORD)
    else:
        record_ok = (
            record.get("schema_version") == "v0.1"
            and record.get("record_kind") == "provider_result_admission_record"
            and record.get("status") == "ADMISSION_CANDIDATE_REVIEWED_MERGE_REQUIRED"
            and record.get("governed_line", {}).get("request_admission_merge_commit") == MERGE_SHA
            and source.get("receipt_sha256") == RECEIPT_SHA
            and source.get("run_metadata_sha256") == RUN_SHA
            and source.get("artifact_metadata_sha256") == ARTIFACT_SHA
            and request.get("validation_mode") == "UPPERCASE_DEEPSEEK_ONLY"
            and request.get("requested_model") == "deepseek/DeepSeek-V3-0324"
            and request.get("request_sha256") == REQUEST_SHA
            and request.get("maximum_provider_calls") == 1
            and request.get("provider_calls_performed") == 1
            and request.get("remaining_authorized_calls") == 0
            and request.get("pair_001_calls_performed") == 0
            and observed.get("receipt_status") == "FAIL"
            and observed.get("http_status") == 410
            and observed.get("sanitized_error_code") == "github_models_retirement_brownout"
            and observed.get("classification") == "DIFFERENT_OUTCOME_PROVIDER_LIFECYCLE_SIGNAL_CAUSE_NOT_INFERRED"
            and observed.get("precommitted_transition_id") == "FSS-PAIR001-T016"
            and observed.get("resulting_state") == "UPPERCASE_RETRY_DIFFERENT_OUTCOME_CLASSIFICATION_REQUIRED"
            and disposition.get("uppercase_retry_consumed") is True
            and disposition.get("additional_uppercase_retry_authorized") is False
            and disposition.get("lowercase_diagnostic_authorized") is False
            and disposition.get("replacement_endpoint_or_model_authorized") is False
            and disposition.get("pair_001_execution_authorized") is False
            and disposition.get("readiness_promotion_authorized") is False
            and disposition.get("freshness_validated") is False
            and disposition.get("cause") == "UNRESOLVED"
            and effect.get("effective_only_on_reviewed_merge_to_governed_branch") is True
            and effect.get("admits_exact_provider_result_as_bounded_negative_evidence") is True
            and effect.get("admits_provider_or_model_availability_claim") is False
            and effect.get("admits_pair_001_result") is False
            and effect.get("authority_delta") == "NONE"
            and effect.get("execution_effect") == "NONE"
        )
        if not record_ok:
            add(findings, "ADMISSION_RECORD_SEMANTICS_INVALID", "bounded T016 admission contract violated", RECORD)

    calls = receipt.get("calls")
    authorization = receipt.get("authorization")
    receipt_ok = (
        receipt.get("receipt_id") == "CSH_PROVIDER_VALIDATION_RECEIPT_v0_1_2"
        and receipt.get("schema_version") == "v0.1.2"
        and receipt.get("classification") == "PROVIDER_VALIDATION_ONLY_EXCLUDED_FROM_CSH_BASELINE"
        and receipt.get("validation_mode") == "UPPERCASE_DEEPSEEK_ONLY"
        and receipt.get("status") == "FAIL"
        and receipt.get("subject_commit") == MERGE_SHA
        and receipt.get("workflow_run_id") == 30711931234
        and receipt.get("provider_validation_calls_performed") == 1
        and receipt.get("pair_001_calls_performed") == 0
        and receipt.get("experiment_run_ids_created") == []
        and isinstance(calls, list)
        and len(calls) == 1
        and calls[0].get("requested_model") == "deepseek/DeepSeek-V3-0324"
        and calls[0].get("request_sha256") == REQUEST_SHA
        and calls[0].get("http_status") == 410
        and calls[0].get("passed") is False
        and calls[0].get("response_body_written") is False
        and calls[0].get("sanitized_error", {}).get("error_code") == "github_models_retirement_brownout"
        and calls[0].get("sanitized_error", {}).get("raw_body_persisted") is False
        and isinstance(authorization, dict)
        and authorization.get("maximum_provider_calls") == 1
        and authorization.get("request_sha256") == REQUEST_SHA
        and authorization.get("pair_001_execution_authorized") is False
        and authorization.get("readiness_promotion_authorized") is False
    )
    if not receipt_ok:
        add(findings, "PROVIDER_RECEIPT_BOUNDARY_INVALID", "exact one-call failure receipt contract violated", RECEIPT)

    run_ok = (
        run.get("id") == 30711931234
        and run.get("name") == "CSH Provider Validation v0.1.2"
        and run.get("event") == "push"
        and run.get("head_sha") == MERGE_SHA
        and run.get("status") == "completed"
        and run.get("conclusion") == "failure"
    )
    if not run_ok:
        add(findings, "WORKFLOW_RUN_BINDING_INVALID", "run metadata does not bind exact merge-triggered run", RUN)

    artifact_ok = (
        artifact.get("id") == 8822142294
        and artifact.get("name") == f"csh-provider-validation-{MERGE_SHA}"
        and artifact.get("expired") is False
        and artifact.get("workflow_run", {}).get("id") == 30711931234
        and artifact.get("workflow_run", {}).get("head_sha") == MERGE_SHA
        and artifact.get("workflow_run", {}).get("head_branch") == "preservation/clean-continuance-v0.1"
    )
    if not artifact_ok:
        add(findings, "WORKFLOW_ARTIFACT_BINDING_INVALID", "artifact metadata does not bind exact run", ARTIFACT)

    entries = reconciliation.get("pull_requests")
    if not isinstance(entries, list):
        add(findings, "OPEN_PR_RECONCILIATION_INVALID", "pull_requests must be a list", RECONCILIATION)
    else:
        numbers = {item.get("number") for item in entries if isinstance(item, dict)}
        safe = all(
            isinstance(item, dict)
            and item.get("automatic_rebase") is False
            and item.get("merge_authorized") is False
            for item in entries
        )
        if (
            reconciliation.get("canonical_line", {}).get("tip_after_pr107") != MERGE_SHA
            or numbers != EXPECTED_OPEN_PRS
            or not safe
            or reconciliation.get("effects", {}).get("standing_promotions") != 0
            or reconciliation.get("effects", {}).get("merge_authorizations") != 0
        ):
            add(findings, "OPEN_PR_RECONCILIATION_INVALID", "draft reconciliation set or non-effects changed", RECONCILIATION)

    workflow_text = (root / CI_WORKFLOW).read_text(encoding="utf-8")
    if "- preservation/clean-continuance-v0.1" not in workflow_text:
        add(findings, "PRESERVATION_TIP_CI_ROUTE_MISSING", "Fork Evidence CI must run on governed preservation pushes", CI_WORKFLOW)

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.repo_root.resolve()
    findings = verify(root)
    payload = {
        "checker_id": CHECKER_ID,
        "result": "PR107_PROVIDER_RESULT_ADMISSION_CANDIDATE_CONFORMS_NOT_ADMITTED" if not findings else "NONCONFORMING",
        "findings": findings,
        "non_effects": {
            "provider_calls": 0,
            "pair_001_calls": 0,
            "admission": "NONE_BY_CHECKER",
            "repository_settings": "NONE",
        },
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
