#!/usr/bin/env python3
"""Verify Shayne's bounded PR #64 recomputation transmission and admission candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(
    "docs/verification/exterior-reviews/SHAYNE_PR64_MACOS_2026_07_30"
)
SOURCE = PACKAGE / "source/SHAYNE_PR64_RECOMPUTATION_TRANSMISSION_2026_07_30.txt"
SIDECAR = PACKAGE / "SHA256SUMS"
RECORD = PACKAGE / "RECOMPUTATION_RECORD_v0_1.json"
PROCESS = PACKAGE / "PROCESS_EVIDENCE_v0_1.json"
README = PACKAGE / "README.md"
ANCHOR = Path(
    "docs/preservation/admission/"
    "FORK_SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_2026_07_30_v0_1.json"
)
PREDECESSOR_ANCHOR = Path(
    "docs/preservation/admission/FORK_PRESERVATION_ADMISSION_ANCHOR_2026_07_18_v0_1.json"
)
PREDECESSOR_README = Path(
    "docs/preservation/admission/FORK_PRESERVATION_ADMISSION_ANCHOR_2026_07_18_v0_1.md"
)
PLAN = Path("verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json")
IVS_RECEIPT = Path(
    "receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json"
)
READINESS = Path(
    "docs/experiments/cross-system-claim-handoff-v0.1/"
    "pre-execution/PRE_EXECUTION_BINDING_v0_1_2.json"
)

SOURCE_SHA256 = "ae4c6bc553f8aaf1073bd846fb72ffca10fd5acccc3de798af609d99346c5eb0"
SOURCE_SIZE = 2672
PR64_HEAD = "d911ad5c33e0ec32037414effa7749326983d5ff"
PR64_MERGE = "528f4306acf75b9b4e349aaf191fcda2c1c1430b"
PR63_CANDIDATE = "82c34252d7b8d9e8957fb5a86500e12da6cf363a"
PR63_MERGE_BASE = "1102113556edfc54b43a328317961c4896d6dd6c"
ANCHOR_BASE = "cda8c68fd6a930c327b04bcbe72088c4fabd72fd"
ANCHOR_BASE_TREE = "69ffb59b56790ed202108c7c81ca172e8f2a4922"
PLAN_SHA256 = "4978976bfebe2c8e94af100b1f419f8abe076b7156ee7090ab57d50c5fc8f581"
IVS_RECEIPT_SHA256 = "5baf0e04e06e7bc69efa91ec35dbc5605d6594fcff5830fe02117a300d7fd083"
PREDECESSOR_ANCHOR_SHA256 = (
    "573f4bfc0eaff0f895979230c827bb97c88bdc82ce4dc0dfdea6799addd54d20"
)
PREDECESSOR_README_SHA256 = (
    "98d004d7c842673a11ac862a8b5d0c41b8861ed5234f1018e4caebf1426d9601"
)
EXPECTED_STATUS = (
    "SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_CONFORMS_NOT_ADMITTED"
)

EXPECTED_FINDING_IDS = {
    f"SHAYNE_PR64_RF_{number:03d}_{suffix}"
    for number, suffix in (
        (1, "EXACT_ACQUISITION"),
        (2, "HASH_LOCKS"),
        (3, "FRESH_RUNNER"),
        (4, "BYTE_EXACT_RECEIPT"),
        (5, "IVS_TESTS"),
        (6, "HASH_SEED_DETERMINISM"),
        (7, "MERGE_BASE"),
        (8, "CANDIDATE_SHA_TAMPER"),
        (9, "EXIT_CODE_COMPARISON"),
        (10, "VERDICT_PRECEDENCE"),
        (11, "PREDECESSOR_WORKFLOWS"),
        (12, "PR63_READINESS"),
        (13, "PR63_READINESS_TESTS"),
    )
}
EXPECTED_OBSERVATION_EFFECTS = {
    "NO_INTEGRITY_GAP",
    "NO_RECOMPUTATION_FAILURE",
    "REVIEWER_DERIVATION_REQUIRED",
}
REQUIRED_NON_CLAIMS = {
    "No endorsement",
    "No GitHub-native approval or merge authority",
    "No execution authorization or Pair-001 permission",
    "No live revalidation of recorded external observations",
    "No cross-platform or cross-version universality",
    "No claim that the referenced full findings attachment is present, preserved, or digest-bound",
    "No authority transfer from evidence, recomputation, review, preservation, admission, or a future merge",
}


class DuplicateKeyError(ValueError):
    pass


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(key)
        result[key] = value
    return result


def reject_nonfinite(value: str) -> Any:
    raise ValueError(f"non-finite JSON value prohibited: {value}")


def reject_nested_nonfinite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON value prohibited")
    if isinstance(value, dict):
        for item in value.values():
            reject_nested_nonfinite(item)
    elif isinstance(value, list):
        for item in value:
            reject_nested_nonfinite(item)


def strict_json(path: Path) -> Any:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM prohibited")
    if b"\r" in raw:
        raise ValueError("CR bytes prohibited")
    if not raw.endswith(b"\n"):
        raise ValueError("final LF required")
    parsed = json.loads(
        raw.decode("utf-8", errors="strict"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_nonfinite,
    )
    reject_nested_nonfinite(parsed)
    return parsed


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finding(code: str, detail: str, path: Path | str) -> dict[str, str]:
    label = path.as_posix() if isinstance(path, Path) else path
    return {"code": code, "detail": detail, "path": label}


def expect(
    condition: bool,
    code: str,
    detail: str,
    path: Path | str,
    findings: list[dict[str, str]],
) -> None:
    if not condition:
        findings.append(finding(code, detail, path))


def safe_path(value: str) -> bool:
    if not value or "\\" in value or "\x00" in value:
        return False
    pure = PurePosixPath(value)
    return (
        not pure.is_absolute()
        and value == pure.as_posix()
        and all(part not in {"", ".", ".."} for part in pure.parts)
    )


def load_record(
    root: Path,
    relative: Path,
    findings: list[dict[str, str]],
) -> dict[str, Any] | None:
    path = root / relative
    if path.is_symlink() or not path.is_file():
        findings.append(finding("REQUIRED_FILE_MISSING_OR_SYMLINK", relative.as_posix(), relative))
        return None
    try:
        value = strict_json(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DuplicateKeyError, ValueError) as exc:
        findings.append(finding("STRICT_JSON_INVALID", str(exc), relative))
        return None
    if not isinstance(value, dict):
        findings.append(finding("JSON_ROOT_NOT_OBJECT", "expected object", relative))
        return None
    return value


def nested(value: dict[str, Any], *keys: str) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(
        {
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return subprocess.run(
        [
            "git",
            "-c",
            f"core.hooksPath={os.devnull}",
            "-c",
            "protocol.file.allow=never",
            *args,
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def validate_source(root: Path, findings: list[dict[str, str]]) -> None:
    source = root / SOURCE
    if source.is_symlink() or not source.is_file():
        findings.append(finding("SOURCE_MISSING_OR_SYMLINK", SOURCE.as_posix(), SOURCE))
        return
    raw = source.read_bytes()
    expect(len(raw) == SOURCE_SIZE, "SOURCE_SIZE_MISMATCH", str(len(raw)), SOURCE, findings)
    expect(
        hashlib.sha256(raw).hexdigest() == SOURCE_SHA256,
        "SOURCE_SHA256_MISMATCH",
        hashlib.sha256(raw).hexdigest(),
        SOURCE,
        findings,
    )
    expect(b"\r" not in raw, "SOURCE_CR_BYTES_PROHIBITED", "source must use LF", SOURCE, findings)
    expect(raw.endswith(b"\n"), "SOURCE_FINAL_LF_MISSING", "final LF required", SOURCE, findings)
    required_phrases = (
        b"Disposition: REPRODUCED_WITHIN_DECLARED_SCOPE",
        b"macOS 15.7.7",
        b"Python 3.14.4",
        b"FRESH_RECOMPUTATION_PASS",
        b"STRUCTURALLY_READY_EXECUTION_BLOCKED",
        b'false "19 of 20 paths missing" finding',
        b"Shayne\n",
    )
    for phrase in required_phrases:
        expect(
            phrase in raw,
            "SOURCE_REQUIRED_PHRASE_MISSING",
            phrase.decode("utf-8"),
            SOURCE,
            findings,
        )

    sidecar = root / SIDECAR
    expected = (
        f"{SOURCE_SHA256}  "
        "source/SHAYNE_PR64_RECOMPUTATION_TRANSMISSION_2026_07_30.txt\n"
    ).encode("utf-8")
    if sidecar.is_symlink() or not sidecar.is_file():
        findings.append(finding("SOURCE_SIDECAR_MISSING_OR_SYMLINK", SIDECAR.as_posix(), SIDECAR))
    else:
        expect(
            sidecar.read_bytes() == expected,
            "SOURCE_SIDECAR_MISMATCH",
            "expected exact one-entry SHA256SUMS",
            SIDECAR,
            findings,
        )


def validate_record(
    record: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    expect(
        record.get("record_id")
        == "FORK_SHAYNE_PR64_MACOS_RECOMPUTATION_2026_07_30_v0_1",
        "RECORD_ID_MISMATCH",
        str(record.get("record_id")),
        RECORD,
        findings,
    )
    expect(
        record.get("status") == "PROPOSED_APPEND_ONLY_EXTERIOR_RECOMPUTATION_RECORD",
        "RECORD_STATUS_MISMATCH",
        str(record.get("status")),
        RECORD,
        findings,
    )
    expect(
        nested(record, "source", "sha256") == SOURCE_SHA256,
        "RECORD_SOURCE_DIGEST_MISMATCH",
        str(nested(record, "source", "sha256")),
        RECORD,
        findings,
    )
    expect(
        nested(record, "source", "size_bytes") == SOURCE_SIZE,
        "RECORD_SOURCE_SIZE_MISMATCH",
        str(nested(record, "source", "size_bytes")),
        RECORD,
        findings,
    )
    attachment = nested(record, "source", "referenced_full_findings_attachment")
    expect(
        isinstance(attachment, dict)
        and attachment.get("status") == "REFERENCED_NOT_RECEIVED"
        and attachment.get("repository_bytes_received") is False
        and attachment.get("not_reconstructed_from_summary") is True,
        "ATTACHMENT_STATUS_MISMATCH",
        repr(attachment),
        RECORD,
        findings,
    )
    expect(
        nested(record, "subject", "repository_resolved_exact_head") == PR64_HEAD,
        "RECORD_PR64_HEAD_MISMATCH",
        str(nested(record, "subject", "repository_resolved_exact_head")),
        RECORD,
        findings,
    )
    expect(
        record.get("reviewer_declared_disposition") == "REPRODUCED_WITHIN_DECLARED_SCOPE",
        "DISPOSITION_MISMATCH",
        str(record.get("reviewer_declared_disposition")),
        RECORD,
        findings,
    )
    reported = record.get("reported_findings")
    observed_ids = {
        item.get("finding_id")
        for item in reported
        if isinstance(reported, list) and isinstance(item, dict)
    } if isinstance(reported, list) else set()
    expect(
        observed_ids == EXPECTED_FINDING_IDS and len(reported or []) == len(EXPECTED_FINDING_IDS),
        "REPORTED_FINDING_SET_MISMATCH",
        repr(sorted(observed_ids)),
        RECORD,
        findings,
    )
    observation = record.get("changed_path_observation")
    expect(
        isinstance(observation, dict)
        and observation.get("classification")
        == "CHANGED_PATH_INVENTORY_TRANSITIVELY_BOUND_NOT_FIRST_CLASS_ENUMERATED"
        and observation.get("standing") == "OBSERVATION_NOT_DEFECT"
        and set(observation.get("effects", [])) == EXPECTED_OBSERVATION_EFFECTS
        and observation.get("pr_64_standing_effect") == "NONE",
        "CHANGED_PATH_OBSERVATION_MISMATCH",
        repr(observation),
        RECORD,
        findings,
    )
    standing = record.get("standing")
    expect(
        isinstance(standing, dict)
        and standing.get("pr_63_continuing_state")
        == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
        and standing.get("execution_authority_delta") == "NONE"
        and standing.get("pair_001_execution_authorized") is False
        and standing.get("admission_state") == "REVIEW_ELIGIBLE_NOT_ADMITTED",
        "RECORD_STANDING_EXPANDED",
        repr(standing),
        RECORD,
        findings,
    )


def validate_process(process: dict[str, Any], findings: list[dict[str, str]]) -> None:
    expected_sequence = [
        "CRUDE_REPRESENTATION",
        "APPARENT_COVERAGE_DEFECT",
        "CANONICAL_BINDING_INSPECTED",
        "FALSE_FINDING_WITHDRAWN_BEFORE_TRANSMISSION",
    ]
    sequence = process.get("sequence")
    observed = [
        item.get("state")
        for item in sequence
        if isinstance(sequence, list) and isinstance(item, dict)
    ] if isinstance(sequence, list) else []
    expect(
        process.get("status") == "PRESERVED_WITHDRAWN_FALSE_FINDING",
        "PROCESS_STATUS_MISMATCH",
        str(process.get("status")),
        PROCESS,
        findings,
    )
    expect(
        observed == expected_sequence,
        "PROCESS_SEQUENCE_MISMATCH",
        repr(observed),
        PROCESS,
        findings,
    )
    classification = process.get("classification")
    expect(
        isinstance(classification, dict)
        and classification.get("failure_mode") == "DEGRADED_REPRESENTATION_NEAR_MISS"
        and classification.get("review_defect_created") is False
        and classification.get("pr_64_integrity_effect") == "NONE"
        and classification.get("execution_effect") == "NONE",
        "PROCESS_EFFECT_EXPANDED",
        repr(classification),
        PROCESS,
        findings,
    )


def validate_anchor(
    root: Path,
    anchor: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    expect(
        anchor.get("anchor_id")
        == "FORK_SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_2026_07_30_v0_1",
        "ANCHOR_ID_MISMATCH",
        str(anchor.get("anchor_id")),
        ANCHOR,
        findings,
    )
    expect(
        anchor.get("status") == "PROPOSED_APPEND_ONLY_ADMISSION"
        and anchor.get("append_only") is True,
        "ANCHOR_STATUS_MISMATCH",
        repr((anchor.get("status"), anchor.get("append_only"))),
        ANCHOR,
        findings,
    )
    expect(
        anchor.get("anchor_base_commit") == ANCHOR_BASE
        and anchor.get("anchor_base_tree") == ANCHOR_BASE_TREE,
        "ANCHOR_BASE_MISMATCH",
        repr((anchor.get("anchor_base_commit"), anchor.get("anchor_base_tree"))),
        ANCHOR,
        findings,
    )
    expect(
        nested(anchor, "review_subject", "reviewed_head") == PR64_HEAD
        and nested(anchor, "review_evidence", "reviewer_declared_disposition")
        == "REPRODUCED_WITHIN_DECLARED_SCOPE"
        and nested(anchor, "review_evidence", "source_completeness")
        == "TRANSMISSION_SUMMARY_PRESERVED_REFERENCED_ATTACHMENT_NOT_RECEIVED",
        "ANCHOR_REVIEW_EVIDENCE_MISMATCH",
        repr(anchor.get("review_evidence")),
        ANCHOR,
        findings,
    )
    effect = anchor.get("admission_effect_if_merged")
    expect(
        isinstance(effect, dict)
        and effect.get("standing")
        == "ADMITTED_ATTRIBUTABLE_EXTERIOR_RECOMPUTATION_TRANSMISSION_WITH_ATTACHMENT_GAP_PRESERVED"
        and effect.get("referenced_full_attachment_admitted") is False
        and effect.get("pr_63_continuing_state")
        == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
        and effect.get("does_not_authorize_pair_001_execution") is True
        and effect.get("does_not_transfer_authority") is True,
        "ANCHOR_ADMISSION_EFFECT_EXPANDED",
        repr(effect),
        ANCHOR,
        findings,
    )
    terminal = anchor.get("terminal_rule")
    expect(
        isinstance(terminal, dict)
        and terminal.get("candidate_cannot_prebind_its_own_future_merge") is True
        and terminal.get("opening_or_passing_ci_does_not_admit_candidate") is True
        and terminal.get("merge_requires_separate_explicit_authorization") is True,
        "ANCHOR_TERMINAL_RULE_MISMATCH",
        repr(terminal),
        ANCHOR,
        findings,
    )
    non_claims = set(anchor.get("non_claims", []))
    expect(
        REQUIRED_NON_CLAIMS <= non_claims,
        "ANCHOR_NON_CLAIMS_INCOMPLETE",
        repr(sorted(REQUIRED_NON_CLAIMS - non_claims)),
        ANCHOR,
        findings,
    )

    bindings = anchor.get("artifact_bindings")
    expected_paths = {SOURCE.as_posix(), SIDECAR.as_posix(), RECORD.as_posix(), PROCESS.as_posix(), README.as_posix()}
    observed_paths = {
        item.get("path")
        for item in bindings
        if isinstance(bindings, list) and isinstance(item, dict)
    } if isinstance(bindings, list) else set()
    expect(
        observed_paths == expected_paths and len(bindings or []) == len(expected_paths),
        "ARTIFACT_BINDING_SET_MISMATCH",
        repr(sorted(observed_paths)),
        ANCHOR,
        findings,
    )
    for item in bindings if isinstance(bindings, list) else []:
        if not isinstance(item, dict):
            continue
        value = item.get("path")
        if not isinstance(value, str) or not safe_path(value):
            findings.append(finding("ARTIFACT_BINDING_PATH_UNSAFE", repr(value), ANCHOR))
            continue
        path = root / value
        if path.is_symlink() or not path.is_file():
            findings.append(finding("BOUND_ARTIFACT_MISSING_OR_SYMLINK", value, value))
            continue
        expect(
            path.stat().st_size == item.get("size_bytes"),
            "BOUND_ARTIFACT_SIZE_MISMATCH",
            f"expected={item.get('size_bytes')} actual={path.stat().st_size}",
            value,
            findings,
        )
        expect(
            sha256(path) == item.get("sha256"),
            "BOUND_ARTIFACT_SHA256_MISMATCH",
            f"expected={item.get('sha256')} actual={sha256(path)}",
            value,
            findings,
        )

    predecessor = anchor.get("predecessor_admission_context")
    expect(
        isinstance(predecessor, dict)
        and predecessor.get("machine_record_sha256") == PREDECESSOR_ANCHOR_SHA256
        and predecessor.get("human_record_sha256") == PREDECESSOR_README_SHA256
        and predecessor.get("prior_record_rewritten") is False,
        "PREDECESSOR_BINDING_MISMATCH",
        repr(predecessor),
        ANCHOR,
        findings,
    )
    for relative, expected in (
        (PREDECESSOR_ANCHOR, PREDECESSOR_ANCHOR_SHA256),
        (PREDECESSOR_README, PREDECESSOR_README_SHA256),
    ):
        path = root / relative
        expect(
            path.is_file() and not path.is_symlink() and sha256(path) == expected,
            "PREDECESSOR_ARTIFACT_MISMATCH",
            expected,
            relative,
            findings,
        )


def validate_repository_correlations(
    root: Path,
    findings: list[dict[str, str]],
) -> None:
    for commit in (PR64_HEAD, PR64_MERGE, PR63_CANDIDATE, PR63_MERGE_BASE, ANCHOR_BASE):
        completed = run_git(root, ["cat-file", "-e", f"{commit}^{{commit}}"])
        expect(
            completed.returncode == 0,
            "BOUND_COMMIT_UNAVAILABLE",
            completed.stderr.strip() or commit,
            "$git",
            findings,
        )

    prefix = run_git(root, ["rev-parse", "d911ad5c^{commit}"])
    expect(
        prefix.returncode == 0 and prefix.stdout.strip() == PR64_HEAD,
        "PR64_HEAD_PREFIX_RESOLUTION_MISMATCH",
        prefix.stdout.strip() or prefix.stderr.strip(),
        "$git",
        findings,
    )
    base_tree = run_git(root, ["rev-parse", f"{ANCHOR_BASE}^{{tree}}"])
    expect(
        base_tree.returncode == 0 and base_tree.stdout.strip() == ANCHOR_BASE_TREE,
        "ANCHOR_BASE_TREE_MISMATCH",
        base_tree.stdout.strip() or base_tree.stderr.strip(),
        "$git",
        findings,
    )
    changed = run_git(root, ["diff", "--name-only", PR63_MERGE_BASE, PR63_CANDIDATE])
    changed_paths = [line for line in changed.stdout.splitlines() if line]
    expect(
        changed.returncode == 0 and len(changed_paths) == 20 and len(set(changed_paths)) == 20,
        "PR63_CHANGED_PATH_COUNT_MISMATCH",
        repr(changed_paths),
        "$git",
        findings,
    )

    plan = load_record(root, PLAN, findings)
    if plan is not None:
        expect(sha256(root / PLAN) == PLAN_SHA256, "PLAN_SHA256_MISMATCH", sha256(root / PLAN), PLAN, findings)
        expect(
            nested(plan, "subject", "candidate_commit") == PR63_CANDIDATE
            and nested(plan, "subject", "expected_merge_base") == PR63_MERGE_BASE,
            "PLAN_SUBJECT_MISMATCH",
            repr(plan.get("subject")),
            PLAN,
            findings,
        )
        expect(
            plan.get("verdict_precedence")
            == [
                "INCONCLUSIVE_EVIDENCE_GAP",
                "INVALIDATED_BY_RECOMPUTATION",
                "VERIFIED_WITHIN_DECLARED_SCOPE",
            ],
            "PLAN_VERDICT_PRECEDENCE_MISMATCH",
            repr(plan.get("verdict_precedence")),
            PLAN,
            findings,
        )
        expect(
            all(
                key not in plan
                for key in ("changed_paths", "changed_path_inventory", "expected_changed_paths")
            ),
            "PLAN_CHANGED_PATHS_NOW_FIRST_CLASS",
            "successor semantics require a new observation record",
            PLAN,
            findings,
        )

    receipt = load_record(root, IVS_RECEIPT, findings)
    if receipt is not None:
        expect(
            sha256(root / IVS_RECEIPT) == IVS_RECEIPT_SHA256,
            "IVS_RECEIPT_SHA256_MISMATCH",
            sha256(root / IVS_RECEIPT),
            IVS_RECEIPT,
            findings,
        )
        expect(
            nested(receipt, "result", "verdict") == "VERIFIED_WITHIN_DECLARED_SCOPE"
            and nested(receipt, "subject", "changed_path_count") == 20
            and nested(receipt, "git_modes", "regular_blob_count") == 20,
            "IVS_RECEIPT_RESULT_MISMATCH",
            repr(receipt.get("result")),
            IVS_RECEIPT,
            findings,
        )

    readiness = load_record(root, READINESS, findings)
    if readiness is not None:
        expect(
            readiness.get("status") == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
            and readiness.get("provider_execution_permitted") is False
            and readiness.get("provider_calls_performed_by_this_stage") == 0,
            "CURRENT_READINESS_STATE_MISMATCH",
            repr(
                (
                    readiness.get("status"),
                    readiness.get("provider_execution_permitted"),
                    readiness.get("provider_calls_performed_by_this_stage"),
                )
            ),
            READINESS,
            findings,
        )


def evaluate(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    validate_source(root, findings)
    record = load_record(root, RECORD, findings)
    process = load_record(root, PROCESS, findings)
    anchor = load_record(root, ANCHOR, findings)
    if record is not None:
        validate_record(record, findings)
    if process is not None:
        validate_process(process, findings)
    if anchor is not None:
        validate_anchor(root, anchor, findings)
    validate_repository_correlations(root, findings)
    findings.sort(key=lambda item: (item["code"], item["path"], item["detail"]))
    return {
        "checker_id": "FORK_SHAYNE_PR64_RECOMPUTATION_RECORD_CHECKER_v0_1",
        "status": EXPECTED_STATUS if not findings else "SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_NONCONFORMING",
        "ok": not findings,
        "finding_count": len(findings),
        "findings": findings,
        "source": {
            "path": SOURCE.as_posix(),
            "sha256": SOURCE_SHA256,
            "source_class": "ATTRIBUTABLE_REVIEWER_TRANSMISSION_SUMMARY",
            "referenced_attachment": "REFERENCED_NOT_RECEIVED",
        },
        "standing": {
            "reviewer_declared_disposition": "REPRODUCED_WITHIN_DECLARED_SCOPE",
            "admission_state": "REVIEW_ELIGIBLE_NOT_ADMITTED",
            "pr_63_state": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
            "execution_authority_delta": "NONE",
            "pair_001_execution_authorized": False,
        },
        "effects": {
            "main": "NONE",
            "existing_pull_requests": "NONE",
            "repository_settings": "NONE",
            "provider_calls": 0,
            "pair_001_calls": 0,
            "authority": "NONE",
            "execution": "NONE",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.repo_root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["status"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
