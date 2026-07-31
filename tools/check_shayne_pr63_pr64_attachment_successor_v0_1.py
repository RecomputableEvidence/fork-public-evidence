#!/usr/bin/env python3
"""Verify Shayne's PR #63/#64 release attachment successor without promoting it."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import stat
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(
    "docs/verification/exterior-reviews/SHAYNE_PR64_MACOS_2026_07_30"
)
RECEIPT = PACKAGE / "ATTACHMENT_RECEIPT_v0_1.json"
MANIFEST = PACKAGE / "ATTACHMENT_PRESERVATION_MANIFEST_v0_1.json"
HUMAN = PACKAGE / "ATTACHMENT_SUCCESSOR_v0_1.md"
PREDECESSOR_RECORD = PACKAGE / "RECOMPUTATION_RECORD_v0_1.json"
SOURCE_ROOT = PACKAGE / "source/pr63-pr64-ivs-v0_1_1"
ARCHIVE = SOURCE_ROOT / "pr63-pr64-evidence-bundle.zip"
EXTRACTED_ROOT = SOURCE_ROOT / "extracted/pr63-pr64-evidence-bundle"
MEMO = EXTRACTED_ROOT / "FINDINGS-MEMO-PR63-PR64-IVS-v0_1_1.md"
BUNDLE_NOTE = EXTRACTED_ROOT / "BUNDLE_NOTE.md"
ENVIRONMENT = EXTRACTED_ROOT / "ENVIRONMENT_RECORD.txt"
UPSTREAM_SUMS = EXTRACTED_ROOT / "SHA256SUMS.txt"
RAW = EXTRACTED_ROOT / "raw"
CANONICAL_PLAN = Path("verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json")
ANCHOR = Path(
    "docs/preservation/admission/"
    "FORK_SHAYNE_PR64_RECOMPUTATION_ATTACHMENT_SUCCESSOR_CANDIDATE_"
    "2026_07_30_v0_1.json"
)
PREDECESSOR_ANCHOR = Path(
    "docs/preservation/admission/"
    "FORK_SHAYNE_PR64_RECOMPUTATION_ADMISSION_CANDIDATE_2026_07_30_v0_1.json"
)

EXPECTED_STATUS = "SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_CONFORMS_NOT_ADMITTED"
ARCHIVE_SHA256 = "1ccf11595fcc88b1bab187f2dd301a04e123e02ba92867e90491b619b0a11d2d"
ARCHIVE_SIZE = 16901
RECEIPT_SET_SHA256 = (
    "5baf0e04e06e7bc69efa91ec35dbc5605d6594fcff5830fe02117a300d7fd083"
)
PREDECESSOR_RECORD_SHA256 = (
    "992e77c86d71ba523595a823a32f4452d500ad4e1d888883d21821d63b372df4"
)
PREDECESSOR_ANCHOR_SHA256 = (
    "9b6c8a08143ace887366d808d2f1c1c3a12320f16940c0f0ff8c76a4855a7d46"
)
CANONICAL_PLAN_SHA256 = (
    "4978976bfebe2c8e94af100b1f419f8abe076b7156ee7090ab57d50c5fc8f581"
)
PR63_CANDIDATE = "82c34252d7b8d9e8957fb5a86500e12da6cf363a"
TAMPERED_CANDIDATE = "82c34252d7b8d9e8957fb5a86500e12da6cf363b"
PR63_MERGE_BASE = "1102113556edfc54b43a328317961c4896d6dd6c"

ZIP_PREFIX = "pr63-pr64-evidence-bundle/"
EXPECTED_FILE_MEMBERS = {
    f"{ZIP_PREFIX}BUNDLE_NOTE.md": (
        "d73fcd7373dffe4cfcb66bf1f18aacebbcab626bcd0940f74ef8efb93d87bd69",
        1475,
    ),
    f"{ZIP_PREFIX}ENVIRONMENT_RECORD.txt": (
        "55da2d4d9014c44ebcea8cfc4e7ece181a25d682baabc8f6eb814e7bacbe7de9",
        527,
    ),
    f"{ZIP_PREFIX}FINDINGS-MEMO-PR63-PR64-IVS-v0_1_1.md": (
        "ce87d8edd759b97fd2b4910a1a1cc597cfb07d107ff84f43cc4462f337533e3a",
        6368,
    ),
    f"{ZIP_PREFIX}SHA256SUMS.txt": (
        "667facd44f14b3e7e665772c661d18fbf0ff03e422008465bf62e2bcbbd5358e",
        950,
    ),
    f"{ZIP_PREFIX}raw/PR_63_receipt_mine.json": (RECEIPT_SET_SHA256, 2380),
    f"{ZIP_PREFIX}raw/checker_out.txt": (RECEIPT_SET_SHA256, 2380),
    f"{ZIP_PREFIX}raw/diff_real.txt": (
        "66df3038c620dfcbd5fca7da3bdb691d9321e5a4e44fd7d9d721ec609b159af6",
        1486,
    ),
    f"{ZIP_PREFIX}raw/plan_tampered.json": (
        "8950e9a2abea3e47e96da8d7a0848b7ac75337f29c4578f9b2d2daa19eebe0f5",
        5328,
    ),
    f"{ZIP_PREFIX}raw/r_1.json": (RECEIPT_SET_SHA256, 2380),
    f"{ZIP_PREFIX}raw/r_2.json": (RECEIPT_SET_SHA256, 2380),
    f"{ZIP_PREFIX}raw/r_42.json": (RECEIPT_SET_SHA256, 2380),
    f"{ZIP_PREFIX}raw/tamper_out.txt": (
        "d3382015cc84dfa3b7f58d1cc1bb823075ce56eee51fb89a62b29ff4e084587c",
        6925,
    ),
}
EXPECTED_DIRECTORY_MEMBERS = {ZIP_PREFIX, f"{ZIP_PREFIX}raw/"}
EXPECTED_MEMBERS = set(EXPECTED_FILE_MEMBERS) | EXPECTED_DIRECTORY_MEMBERS
UPSTREAM_EXPECTED = {
    name.removeprefix(ZIP_PREFIX): value
    for name, value in EXPECTED_FILE_MEMBERS.items()
    if name != f"{ZIP_PREFIX}SHA256SUMS.txt"
}
RECEIPT_SET = {
    "raw/PR_63_receipt_mine.json",
    "raw/checker_out.txt",
    "raw/r_1.json",
    "raw/r_2.json",
    "raw/r_42.json",
}

EXPECTED_OUTER: dict[str, tuple[str, int]] = {
    ARCHIVE.as_posix(): (ARCHIVE_SHA256, ARCHIVE_SIZE),
    **{
        (EXTRACTED_ROOT / name.removeprefix(ZIP_PREFIX)).as_posix(): value
        for name, value in EXPECTED_FILE_MEMBERS.items()
    },
}
EXPECTED_ANCHOR_BINDINGS = {
    MANIFEST.as_posix(),
    RECEIPT.as_posix(),
    HUMAN.as_posix(),
    ARCHIVE.as_posix(),
}
EXPECTED_EFFECTS = {
    "main": "NONE",
    "existing_pull_requests": "NONE",
    "repository_settings": "NONE",
    "provider_calls": 0,
    "pair_001_calls": 0,
    "authority": "NONE",
    "execution": "NONE",
}
REQUIRED_NON_CLAIMS = {
    "No claim that the original fresh-runner JSON stdout bytes were recovered or reconstructed",
    "No endorsement",
    "No GitHub-native approval or merge authority",
    "No execution authorization or Pair-001 permission",
    "No authority transfer from evidence, recomputation, review, preservation, admission, or a future merge",
}


class DuplicateKeyError(ValueError):
    """Raised when strict JSON parsing encounters a duplicate key."""


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


def strict_json_bytes(raw: bytes) -> Any:
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


def strict_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes())


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def finding(code: str, detail: str, path: Path | str) -> dict[str, str]:
    return {
        "code": code,
        "detail": detail,
        "path": path.as_posix() if isinstance(path, Path) else path,
    }


def expect(
    condition: bool,
    code: str,
    detail: str,
    path: Path | str,
    findings: list[dict[str, str]],
) -> None:
    if not condition:
        findings.append(finding(code, detail, path))


def safe_member(name: str) -> bool:
    normalized = name[:-1] if name.endswith("/") else name
    if not normalized or "\\" in normalized or "\x00" in normalized:
        return False
    pure = PurePosixPath(normalized)
    return (
        not pure.is_absolute()
        and normalized == pure.as_posix()
        and all(part not in {"", ".", ".."} for part in pure.parts)
    )


def load_object(
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
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        findings.append(finding("STRICT_JSON_INVALID", str(error), relative))
        return None
    if not isinstance(value, dict):
        findings.append(finding("TOP_LEVEL_JSON_NOT_OBJECT", type(value).__name__, relative))
        return None
    return value


def nested(value: dict[str, Any], *keys: str) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def validate_outer_manifest(
    root: Path,
    manifest: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    expect(
        manifest.get("record_kind")
        == "fork_shayne_pr63_pr64_attachment_preservation_manifest",
        "MANIFEST_KIND_MISMATCH",
        str(manifest.get("record_kind")),
        MANIFEST,
        findings,
    )
    entries = manifest.get("entries")
    observed: dict[str, dict[str, Any]] = {}
    if isinstance(entries, list):
        for item in entries:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                observed[item["path"]] = item
    expect(
        set(observed) == set(EXPECTED_OUTER) and len(entries or []) == len(EXPECTED_OUTER),
        "MANIFEST_SCOPE_MISMATCH",
        f"expected={sorted(EXPECTED_OUTER)!r}; observed={sorted(observed)!r}",
        MANIFEST,
        findings,
    )
    for relative, (expected_hash, expected_size) in EXPECTED_OUTER.items():
        item = observed.get(relative, {})
        path = root / relative
        expect(
            path.is_file() and not path.is_symlink(),
            "PRESERVED_FILE_MISSING_OR_SYMLINK",
            relative,
            relative,
            findings,
        )
        if not path.is_file() or path.is_symlink():
            continue
        expect(
            item.get("sha256") == expected_hash
            and sha256(path) == expected_hash,
            "PRESERVED_DIGEST_MISMATCH",
            relative,
            relative,
            findings,
        )
        expect(
            item.get("size_bytes") == expected_size
            and path.stat().st_size == expected_size,
            "PRESERVED_SIZE_MISMATCH",
            relative,
            relative,
            findings,
        )
    expect(
        nested(manifest, "self_exclusion", "path") == MANIFEST.as_posix(),
        "MANIFEST_SELF_EXCLUSION_MISSING",
        repr(manifest.get("self_exclusion")),
        MANIFEST,
        findings,
    )
    scope = manifest.get("archive_scope")
    expect(
        isinstance(scope, dict)
        and scope.get("member_count") == 14
        and scope.get("regular_file_member_count") == 12
        and scope.get("directory_member_count") == 2
        and scope.get("unsafe_member_count") == 0
        and scope.get("extracted_copies_match_archive_members_byte_for_byte") is True
        and scope.get("git_does_not_preserve_extracted_file_mtime_semantics") is True,
        "MANIFEST_ARCHIVE_SCOPE_MISMATCH",
        repr(scope),
        MANIFEST,
        findings,
    )


def validate_archive(root: Path, findings: list[dict[str, str]]) -> None:
    archive_path = root / ARCHIVE
    if archive_path.is_symlink() or not archive_path.is_file():
        findings.append(finding("ARCHIVE_MISSING_OR_SYMLINK", ARCHIVE.as_posix(), ARCHIVE))
        return
    expect(
        sha256(archive_path) == ARCHIVE_SHA256,
        "ARCHIVE_SHA256_MISMATCH",
        sha256(archive_path),
        ARCHIVE,
        findings,
    )
    expect(
        archive_path.stat().st_size == ARCHIVE_SIZE,
        "ARCHIVE_SIZE_MISMATCH",
        str(archive_path.stat().st_size),
        ARCHIVE,
        findings,
    )
    try:
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = [item.filename for item in infos]
            expect(
                len(names) == len(set(names)),
                "ARCHIVE_DUPLICATE_MEMBER",
                repr(names),
                ARCHIVE,
                findings,
            )
            expect(
                set(names) == EXPECTED_MEMBERS and len(names) == 14,
                "ARCHIVE_MEMBER_SCOPE_MISMATCH",
                f"missing={sorted(EXPECTED_MEMBERS - set(names))!r}; "
                f"extra={sorted(set(names) - EXPECTED_MEMBERS)!r}",
                ARCHIVE,
                findings,
            )
            unsafe = sorted(name for name in names if not safe_member(name))
            expect(
                not unsafe,
                "ARCHIVE_UNSAFE_MEMBER",
                repr(unsafe),
                ARCHIVE,
                findings,
            )
            expect(
                archive.testzip() is None,
                "ARCHIVE_CRC_FAILURE",
                "zipfile.testzip reported a bad member",
                ARCHIVE,
                findings,
            )
            for info in infos:
                mode = info.external_attr >> 16
                if info.filename in EXPECTED_DIRECTORY_MEMBERS:
                    expect(
                        stat.S_ISDIR(mode),
                        "ARCHIVE_DIRECTORY_MODE_MISMATCH",
                        f"{info.filename}: {oct(mode)}",
                        ARCHIVE,
                        findings,
                    )
                    continue
                expect(
                    stat.S_ISREG(mode),
                    "ARCHIVE_NONREGULAR_FILE_MODE",
                    f"{info.filename}: {oct(mode)}",
                    ARCHIVE,
                    findings,
                )
                if info.filename not in EXPECTED_FILE_MEMBERS:
                    continue
                expected_hash, expected_size = EXPECTED_FILE_MEMBERS[info.filename]
                data = archive.read(info.filename)
                expect(
                    len(data) == expected_size
                    and info.file_size == expected_size,
                    "ARCHIVE_MEMBER_SIZE_MISMATCH",
                    info.filename,
                    ARCHIVE,
                    findings,
                )
                expect(
                    sha256_bytes(data) == expected_hash,
                    "ARCHIVE_MEMBER_DIGEST_MISMATCH",
                    info.filename,
                    ARCHIVE,
                    findings,
                )
                extracted = root / EXTRACTED_ROOT / info.filename.removeprefix(ZIP_PREFIX)
                expect(
                    extracted.is_file()
                    and not extracted.is_symlink()
                    and extracted.read_bytes() == data,
                    "ARCHIVE_EXTRACTED_COPY_DIVERGENCE",
                    info.filename,
                    extracted.relative_to(root) if extracted.exists() else EXTRACTED_ROOT,
                    findings,
                )
    except (OSError, zipfile.BadZipFile, KeyError, RuntimeError) as error:
        findings.append(finding("ARCHIVE_INVALID", str(error), ARCHIVE))


def parse_upstream_manifest(raw: bytes) -> dict[str, tuple[str, int]]:
    text = raw.decode("ascii", errors="strict")
    if "\r" in text or not text.endswith("\n"):
        raise ValueError("upstream manifest requires LF termination")
    result: dict[str, tuple[str, int]] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\x00\r\n]+)", line)
        if match is None:
            raise ValueError(f"invalid SHA256SUMS line: {line!r}")
        name = match.group(2)
        if name in result or not safe_member(name):
            raise ValueError(f"duplicate or unsafe SHA256SUMS path: {name!r}")
        result[name] = (match.group(1), 0)
    return result


def validate_upstream_manifest(root: Path, findings: list[dict[str, str]]) -> None:
    path = root / UPSTREAM_SUMS
    try:
        declared = parse_upstream_manifest(path.read_bytes())
    except (OSError, UnicodeError, ValueError) as error:
        findings.append(finding("UPSTREAM_MANIFEST_INVALID", str(error), UPSTREAM_SUMS))
        return
    expect(
        set(declared) == set(UPSTREAM_EXPECTED) and len(declared) == 11,
        "UPSTREAM_MANIFEST_SCOPE_MISMATCH",
        f"expected={sorted(UPSTREAM_EXPECTED)!r}; observed={sorted(declared)!r}",
        UPSTREAM_SUMS,
        findings,
    )
    expect(
        "SHA256SUMS.txt" not in declared,
        "UPSTREAM_MANIFEST_SELF_ENTRY_UNEXPECTED",
        repr(sorted(declared)),
        UPSTREAM_SUMS,
        findings,
    )
    for name, (expected_hash, expected_size) in UPSTREAM_EXPECTED.items():
        target = root / EXTRACTED_ROOT / name
        expect(
            declared.get(name, (None, 0))[0] == expected_hash
            and target.is_file()
            and target.stat().st_size == expected_size
            and sha256(target) == expected_hash,
            "UPSTREAM_DECLARED_ARTIFACT_MISMATCH",
            name,
            UPSTREAM_SUMS,
            findings,
        )


def validate_predecessor(root: Path, findings: list[dict[str, str]]) -> None:
    record = load_object(root, PREDECESSOR_RECORD, findings)
    anchor = load_object(root, PREDECESSOR_ANCHOR, findings)
    expect(
        (root / PREDECESSOR_RECORD).is_file()
        and sha256(root / PREDECESSOR_RECORD) == PREDECESSOR_RECORD_SHA256,
        "PREDECESSOR_RECORD_DIGEST_MISMATCH",
        PREDECESSOR_RECORD_SHA256,
        PREDECESSOR_RECORD,
        findings,
    )
    expect(
        (root / PREDECESSOR_ANCHOR).is_file()
        and sha256(root / PREDECESSOR_ANCHOR) == PREDECESSOR_ANCHOR_SHA256,
        "PREDECESSOR_ANCHOR_DIGEST_MISMATCH",
        PREDECESSOR_ANCHOR_SHA256,
        PREDECESSOR_ANCHOR,
        findings,
    )
    if record is not None:
        attachment = nested(record, "source", "referenced_full_findings_attachment")
        expect(
            isinstance(attachment, dict)
            and attachment.get("status") == "REFERENCED_NOT_RECEIVED"
            and attachment.get("repository_bytes_received") is False
            and attachment.get("not_reconstructed_from_summary") is True,
            "PREDECESSOR_NEGATIVE_STATE_REWRITTEN",
            repr(attachment),
            PREDECESSOR_RECORD,
            findings,
        )
    if anchor is not None:
        expect(
            anchor.get("status") == "PROPOSED_APPEND_ONLY_ADMISSION"
            and nested(anchor, "admission_effect_if_merged", "referenced_full_attachment_admitted")
            is False,
            "PREDECESSOR_CANDIDATE_REWRITTEN",
            repr(anchor.get("admission_effect_if_merged")),
            PREDECESSOR_ANCHOR,
            findings,
        )


def validate_receipt(
    receipt: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    expect(
        receipt.get("receipt_id")
        == "FORK_SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_RECEIPT_2026_07_30_v0_1"
        and receipt.get("status") == "PROPOSED_APPEND_ONLY_ATTACHMENT_SUCCESSOR_RECEIPT",
        "RECEIPT_ID_OR_STATUS_MISMATCH",
        repr((receipt.get("receipt_id"), receipt.get("status"))),
        RECEIPT,
        findings,
    )
    transition = receipt.get("successor_transition")
    expect(
        isinstance(transition, dict)
        and transition.get("transition_from")
        == "TRANSMISSION_SUMMARY_PRESERVED_REFERENCED_ATTACHMENT_NOT_RECEIVED"
        and transition.get("transition_to")
        == "EXACT_RELEASE_ATTACHMENT_RECEIVED_AND_VERIFIED_WITH_INTERNAL_CAPTURE_GAP"
        and transition.get("external_attachment_availability_gap_resolved") is True
        and transition.get("original_fresh_runner_stdout_gap_resolved") is False
        and transition.get("prior_negative_state_preserved") is True
        and transition.get("retroactive_rewrite_effect") == "NONE",
        "TEMPORAL_SUCCESSOR_TRANSITION_MISMATCH",
        repr(transition),
        RECEIPT,
        findings,
    )
    provenance = receipt.get("release_provenance")
    expect(
        isinstance(provenance, dict)
        and provenance.get("repository") == "Icon369/verdict-evidence-transfers"
        and provenance.get("release_tag") == "pr63-pr64-ivs-v0_1_1"
        and provenance.get("tag_target_commit")
        == "c9ddbe6f81dd06a719cd0c72da7a38d242e8b362"
        and provenance.get("release_id") == 362827531
        and provenance.get("asset_id") == 496157418
        and provenance.get("exact_local_shell_transcript_authenticated") is False
        and provenance.get("reviewer_identity_authentication")
        == "NOT_PERFORMED_BY_THIS_REPOSITORY_RECORD",
        "RELEASE_PROVENANCE_MISMATCH",
        repr(provenance),
        RECEIPT,
        findings,
    )
    correspondence = receipt.get("transfer_correspondence")
    expect(
        isinstance(correspondence, dict)
        and correspondence.get("recipient_supplied_linkedin_screenshot_observed") is True
        and correspondence.get("preserved_in_public_repository") is False
        and correspondence.get("non_preservation_reason")
        == "PRIVACY_MINIMIZATION_UNRELATED_CONTACTS_AND_PERSONAL_EMAIL_VISIBLE"
        and correspondence.get("cryptographic_subject_binding_basis")
        == "PUBLIC_RELEASE_ASSET_AND_DIGESTS_NOT_SCREENSHOT"
        and correspondence.get("identity_authentication_effect") == "NONE",
        "CORRESPONDENCE_PRIVACY_BOUNDARY_MISMATCH",
        repr(correspondence),
        RECEIPT,
        findings,
    )
    archive = receipt.get("archive_verification")
    expect(
        isinstance(archive, dict)
        and archive.get("path") == ARCHIVE.as_posix()
        and archive.get("size_bytes") == ARCHIVE_SIZE
        and archive.get("reviewer_quoted_sha256") == ARCHIVE_SHA256
        and archive.get("github_release_asset_digest") == f"sha256:{ARCHIVE_SHA256}"
        and archive.get("recipient_computed_sha256") == ARCHIVE_SHA256
        and archive.get("all_three_digest_coordinates_match") is True
        and archive.get("member_count") == 14
        and archive.get("regular_file_member_count") == 12
        and archive.get("directory_member_count") == 2
        and archive.get("exact_release_asset_bytes_preserved") is True,
        "RECEIPT_ARCHIVE_VERIFICATION_MISMATCH",
        repr(archive),
        RECEIPT,
        findings,
    )
    determinism = nested(receipt, "raw_evidence_adjudication", "determinism")
    expect(
        isinstance(determinism, dict)
        and set(determinism.get("byte_identical_paths", [])) == RECEIPT_SET
        and len(determinism.get("byte_identical_paths", [])) == len(RECEIPT_SET)
        and determinism.get("sha256") == RECEIPT_SET_SHA256
        and determinism.get("size_bytes_each") == 2380
        and determinism.get("byte_identity_recomputed_by_recipient") is True,
        "DETERMINISM_ADJUDICATION_MISMATCH",
        repr(determinism),
        RECEIPT,
        findings,
    )
    changed = nested(receipt, "raw_evidence_adjudication", "changed_path_inventory")
    expect(
        isinstance(changed, dict)
        and changed.get("line_count") == 20
        and changed.get("byte_exact_to_recipient_git_object_recomputation") is True
        and changed.get("successor_effect")
        == "FIRST_CLASS_ARTIFACT_NOW_PRESERVED_AND_DIGEST_BOUND"
        and changed.get("plan_schema_retroactive_effect") == "NONE",
        "CHANGED_PATH_SUCCESSOR_ADJUDICATION_MISMATCH",
        repr(changed),
        RECEIPT,
        findings,
    )
    tamper = nested(receipt, "raw_evidence_adjudication", "tamper_probe")
    expect(
        isinstance(tamper, dict)
        and tamper.get("canonical_plan_sha256") == CANONICAL_PLAN_SHA256
        and tamper.get("semantic_change")
        == "ONE_CANDIDATE_SHA_FINAL_NIBBLE_A_TO_B_PROPAGATED_ACROSS_REDUNDANT_COORDINATES"
        and tamper.get("file_byte_difference_count") == 6
        and tamper.get("each_difference") == "ASCII_a_TO_ASCII_b"
        and tamper.get("reviewer_single_byte_language_literal_file_effect")
        == "NARROWED_BY_RAW_BYTES"
        and tamper.get("tamper_output_verdict") == "INCONCLUSIVE_EVIDENCE_GAP"
        and tamper.get("tamper_output_ok") is False
        and tamper.get("reported_process_exit_code") == 2
        and tamper.get("exit_code_evidence_basis")
        == "REVIEWER_MEMO_AND_BUNDLE_NOTE_NOT_SEPARATE_MACHINE_EXIT_CODE_CAPTURE"
        and tamper.get("fail_closed_result_effect") == "UNCHANGED",
        "TAMPER_PRECISION_ADJUDICATION_MISMATCH",
        repr(tamper),
        RECEIPT,
        findings,
    )
    gap = receipt.get("preserved_capture_gap")
    expect(
        isinstance(gap, dict)
        and gap.get("artifact") == "FRESH_RUNNER_JSON_STDOUT"
        and gap.get("original_bytes_preserved") is False
        and gap.get("memo_account_is_transcription") is True
        and gap.get("rerun_performed_to_fill_gap") is False
        and gap.get("gap_standing") == "PRESERVED_NOT_REPAIRED",
        "FRESH_RUNNER_GAP_SILENTLY_FILLED",
        repr(gap),
        RECEIPT,
        findings,
    )
    scope = receipt.get("source_scope_correction")
    expect(
        isinstance(scope, dict)
        and scope.get("memo_command_column_label") == "Command (abbreviated)"
        and scope.get("complete_shell_command_transcript_received") is False
        and scope.get("complete_raw_stdout_and_stderr_set_received") is False
        and scope.get("complete_machine_exit_code_record_received") is False
        and scope.get("exact_memo_and_listed_surviving_raw_artifacts_received") is True
        and scope.get("classification")
        == "ATTACHMENT_RECEIVED_RAW_COVERAGE_PARTIAL_AS_DISCLOSED",
        "SOURCE_SCOPE_INFLATION",
        repr(scope),
        RECEIPT,
        findings,
    )
    standing = receipt.get("standing")
    expect(
        isinstance(standing, dict)
        and standing.get("reviewer_declared_disposition")
        == "REPRODUCED_WITHIN_DECLARED_SCOPE"
        and standing.get("admission_state") == "REVIEW_ELIGIBLE_NOT_ADMITTED"
        and standing.get("pr_63_continuing_state")
        == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
        and standing.get("execution_authority_delta") == "NONE"
        and standing.get("pair_001_execution_authorized") is False
        and standing.get("provider_calls_performed_by_receipt") == 0,
        "RECEIPT_STANDING_PROMOTION",
        repr(standing),
        RECEIPT,
        findings,
    )
    expect(
        receipt.get("effects") == EXPECTED_EFFECTS,
        "RECEIPT_EFFECT_PROMOTION",
        repr(receipt.get("effects")),
        RECEIPT,
        findings,
    )
    non_claims = set(receipt.get("non_claims", []))
    expect(
        REQUIRED_NON_CLAIMS <= non_claims,
        "RECEIPT_NON_CLAIMS_INCOMPLETE",
        repr(sorted(REQUIRED_NON_CLAIMS - non_claims)),
        RECEIPT,
        findings,
    )


def validate_raw_evidence(
    root: Path,
    findings: list[dict[str, str]],
    verify_git_correlations: bool,
) -> None:
    receipt_bytes = [(root / RAW / Path(name).name).read_bytes() for name in RECEIPT_SET]
    expect(
        len(set(receipt_bytes)) == 1
        and all(sha256_bytes(value) == RECEIPT_SET_SHA256 for value in receipt_bytes),
        "RECEIPT_SET_NOT_BYTE_IDENTICAL",
        repr(sorted(sha256_bytes(value) for value in receipt_bytes)),
        RAW,
        findings,
    )
    try:
        parsed_receipt = strict_json_bytes(receipt_bytes[0])
        expect(
            isinstance(parsed_receipt, dict)
            and nested(parsed_receipt, "result", "verdict")
            == "VERIFIED_WITHIN_DECLARED_SCOPE"
            and nested(parsed_receipt, "result", "ok") is True
            and nested(parsed_receipt, "subject", "candidate_commit") == PR63_CANDIDATE,
            "RAW_RECEIPT_SEMANTICS_MISMATCH",
            repr(parsed_receipt),
            RAW,
            findings,
        )
    except (UnicodeError, ValueError, json.JSONDecodeError) as error:
        findings.append(finding("RAW_RECEIPT_STRICT_JSON_INVALID", str(error), RAW))

    canonical_path = root / CANONICAL_PLAN
    tampered_path = root / RAW / "plan_tampered.json"
    canonical = canonical_path.read_bytes()
    tampered = tampered_path.read_bytes()
    differences = [
        (index, left, right)
        for index, (left, right) in enumerate(zip(canonical, tampered, strict=False), start=1)
        if left != right
    ]
    if len(canonical) != len(tampered):
        differences.append((max(len(canonical), len(tampered)), -1, -1))
    expect(
        sha256_bytes(canonical) == CANONICAL_PLAN_SHA256,
        "CANONICAL_PLAN_DIGEST_MISMATCH",
        sha256_bytes(canonical),
        CANONICAL_PLAN,
        findings,
    )
    expect(
        len(canonical) == len(tampered) == 5328
        and len(differences) == 6
        and all(left == ord("a") and right == ord("b") for _, left, right in differences),
        "TAMPER_FILE_DIFF_NOT_SIX_PROPAGATED_NIBBLES",
        repr(differences),
        RAW / "plan_tampered.json",
        findings,
    )
    try:
        canonical_json = strict_json_bytes(canonical)
        tampered_json = strict_json_bytes(tampered)
        expect(
            nested(canonical_json, "subject", "candidate_commit") == PR63_CANDIDATE
            and nested(tampered_json, "subject", "candidate_commit") == TAMPERED_CANDIDATE,
            "TAMPERED_SUBJECT_COORDINATE_MISMATCH",
            repr(
                (
                    nested(canonical_json, "subject", "candidate_commit"),
                    nested(tampered_json, "subject", "candidate_commit"),
                )
            ),
            RAW / "plan_tampered.json",
            findings,
        )
    except (UnicodeError, ValueError, json.JSONDecodeError) as error:
        findings.append(finding("PLAN_STRICT_JSON_INVALID", str(error), CANONICAL_PLAN))

    try:
        tamper_output = strict_json(root / RAW / "tamper_out.txt")
        expect(
            isinstance(tamper_output, dict)
            and nested(tamper_output, "result", "ok") is False
            and nested(tamper_output, "result", "verdict") == "INCONCLUSIVE_EVIDENCE_GAP"
            and nested(tamper_output, "result", "control_error_count") == 8
            and nested(tamper_output, "result", "repository_standing_effect") == "NONE"
            and nested(tamper_output, "result", "experiment_execution_effect") == "NONE",
            "TAMPER_OUTPUT_SEMANTICS_MISMATCH",
            repr(tamper_output.get("result") if isinstance(tamper_output, dict) else tamper_output),
            RAW / "tamper_out.txt",
            findings,
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        findings.append(finding("TAMPER_OUTPUT_STRICT_JSON_INVALID", str(error), RAW / "tamper_out.txt"))

    diff_path = root / RAW / "diff_real.txt"
    diff_bytes = diff_path.read_bytes()
    expect(
        sha256_bytes(diff_bytes)
        == "66df3038c620dfcbd5fca7da3bdb691d9321e5a4e44fd7d9d721ec609b159af6"
        and len(diff_bytes.splitlines()) == 20
        and diff_bytes.endswith(b"\n"),
        "CHANGED_PATH_ARTIFACT_MISMATCH",
        sha256_bytes(diff_bytes),
        RAW / "diff_real.txt",
        findings,
    )
    if verify_git_correlations:
        completed = subprocess.run(
            ["git", "diff", "--name-only", PR63_MERGE_BASE, PR63_CANDIDATE],
            cwd=root,
            check=False,
            capture_output=True,
        )
        expect(
            completed.returncode == 0 and completed.stdout == diff_bytes,
            "CHANGED_PATH_GIT_RECOMPUTATION_DIVERGENCE",
            completed.stderr.decode("utf-8", errors="replace")
            or sha256_bytes(completed.stdout),
            RAW / "diff_real.txt",
            findings,
        )

    memo = (root / MEMO).read_bytes()
    note = (root / BUNDLE_NOTE).read_bytes()
    environment = (root / ENVIRONMENT).read_bytes()
    for phrase in (
        b"**Disposition:** **REPRODUCED_WITHIN_DECLARED_SCOPE**",
        b"Command (abbreviated)",
        b"checker **exit 2**",
        b"**8 passed**",
        b"5/5 pass.**",
    ):
        expect(
            phrase in memo,
            "MEMO_REQUIRED_PHRASE_MISSING",
            phrase.decode("utf-8"),
            MEMO,
            findings,
        )
    for phrase in (
        b"NOT redirected to a file at run time",
        b"original bytes are not preserved here",
        b"nothing was rerun to fill this gap",
    ):
        expect(
            phrase in note,
            "BUNDLE_NOTE_GAP_DISCLOSURE_MISSING",
            phrase.decode("utf-8"),
            BUNDLE_NOTE,
            findings,
        )
    for phrase in (
        b"generated 2026-07-30 at bundle-assembly time",
        b"post-run, same session/host",
        b"reviewed_commit: d911ad5c33e0ec32037414effa7749326983d5ff",
    ):
        expect(
            phrase in environment,
            "ENVIRONMENT_TIME_BASIS_MISSING",
            phrase.decode("utf-8"),
            ENVIRONMENT,
            findings,
        )


def validate_anchor(
    root: Path,
    anchor: dict[str, Any],
    findings: list[dict[str, str]],
) -> None:
    expect(
        anchor.get("anchor_id")
        == "FORK_SHAYNE_PR64_RECOMPUTATION_ATTACHMENT_SUCCESSOR_CANDIDATE_2026_07_30_v0_1"
        and anchor.get("status") == "PROPOSED_APPEND_ONLY_SUCCESSOR_ADMISSION"
        and anchor.get("append_only") is True,
        "ANCHOR_ID_OR_STATUS_MISMATCH",
        repr((anchor.get("anchor_id"), anchor.get("status"))),
        ANCHOR,
        findings,
    )
    predecessor = anchor.get("candidate_predecessor")
    expect(
        isinstance(predecessor, dict)
        and predecessor.get("commit") == "e245f86457ac9ed9d4e52c76edc5c395970492d9"
        and predecessor.get("tree") == "21ea6ba69b09925f37d816258a538fc80e2f564c"
        and predecessor.get("anchor_sha256") == PREDECESSOR_ANCHOR_SHA256
        and predecessor.get("record_sha256") == PREDECESSOR_RECORD_SHA256
        and predecessor.get("attachment_state") == "REFERENCED_NOT_RECEIVED"
        and predecessor.get("historical_state_preserved") is True
        and predecessor.get("rewritten") is False,
        "ANCHOR_PREDECESSOR_BINDING_MISMATCH",
        repr(predecessor),
        ANCHOR,
        findings,
    )
    bindings = anchor.get("artifact_bindings")
    observed: dict[str, dict[str, Any]] = {}
    if isinstance(bindings, list):
        for item in bindings:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                observed[item["path"]] = item
    expect(
        set(observed) == EXPECTED_ANCHOR_BINDINGS
        and len(bindings or []) == len(EXPECTED_ANCHOR_BINDINGS),
        "ANCHOR_BINDING_SCOPE_MISMATCH",
        repr(sorted(observed)),
        ANCHOR,
        findings,
    )
    for relative, item in observed.items():
        path = root / relative
        expect(
            path.is_file()
            and not path.is_symlink()
            and item.get("size_bytes") == path.stat().st_size
            and item.get("sha256") == sha256(path),
            "ANCHOR_BOUND_ARTIFACT_MISMATCH",
            relative,
            ANCHOR,
            findings,
        )
    scope = anchor.get("source_completeness")
    expect(
        isinstance(scope, dict)
        and scope.get("exact_findings_memo_received") is True
        and scope.get("listed_surviving_raw_artifacts_received") is True
        and scope.get("complete_shell_transcript_received") is False
        and scope.get("complete_raw_stdout_and_stderr_set_received") is False
        and scope.get("complete_machine_exit_code_record_received") is False
        and scope.get("fresh_runner_json_stdout_original_bytes_received") is False
        and scope.get("standing") == "ATTACHMENT_RECEIVED_RAW_COVERAGE_PARTIAL_AS_DISCLOSED",
        "ANCHOR_SOURCE_SCOPE_INFLATION",
        repr(scope),
        ANCHOR,
        findings,
    )
    precision = anchor.get("precision_adjudications")
    expect(
        nested(precision or {}, "tamper_probe", "file_byte_difference_count") == 6
        and nested(precision or {}, "tamper_probe", "fail_closed_result_effect") == "UNCHANGED"
        and nested(precision or {}, "tamper_probe", "separate_machine_exit_code_artifact_present")
        is False
        and nested(precision or {}, "fresh_runner_stdout", "status")
        == "ORIGINAL_BYTES_NOT_PRESERVED"
        and nested(precision or {}, "changed_path_inventory", "status")
        == "FIRST_CLASS_SUCCESSOR_ARTIFACT_DIGEST_BOUND",
        "ANCHOR_PRECISION_ADJUDICATION_MISMATCH",
        repr(precision),
        ANCHOR,
        findings,
    )
    order = anchor.get("admission_order")
    expect(
        isinstance(order, list)
        and len(order) == 2
        and all(isinstance(item, dict) for item in order)
        and [item.get("ordinal") for item in order] == [1, 2],
        "ANCHOR_ADMISSION_ORDER_MISMATCH",
        repr(order),
        ANCHOR,
        findings,
    )
    if isinstance(order, list) and len(order) == 2:
        expect(
            order[0].get("state")
            == "INITIAL_TRANSMISSION_WITH_REFERENCED_ATTACHMENT_NOT_RECEIVED"
            and order[1].get("state")
            == "EXACT_RELEASE_ATTACHMENT_RECEIVED_WITH_INTERNAL_CAPTURE_GAP_PRESERVED",
            "ANCHOR_ADMISSION_ORDER_STATE_MISMATCH",
            repr(order),
            ANCHOR,
            findings,
        )
    effect = anchor.get("admission_effect_if_merged")
    expect(
        isinstance(effect, dict)
        and effect.get("standing")
        == "ADMITTED_ATTRIBUTABLE_EXTERIOR_RECOMPUTATION_WITH_EXACT_ATTACHMENT_BUNDLE_AND_DECLARED_INTERNAL_CAPTURE_GAP"
        and effect.get("initial_attachment_gap_preserved_as_historical_state") is True
        and effect.get("exact_release_attachment_admitted") is True
        and effect.get("complete_raw_execution_record_admitted") is False
        and effect.get("fresh_runner_stdout_original_bytes_admitted") is False
        and effect.get("pr_63_continuing_state")
        == "STRUCTURALLY_READY_EXECUTION_BLOCKED"
        and effect.get("does_not_authorize_pair_001_execution") is True
        and effect.get("does_not_transfer_authority") is True,
        "ANCHOR_ADMISSION_EFFECT_PROMOTION",
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


def evaluate(
    root: Path = ROOT,
    *,
    verify_git_correlations: bool = True,
) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    manifest = load_object(root, MANIFEST, findings)
    receipt = load_object(root, RECEIPT, findings)
    anchor = load_object(root, ANCHOR, findings)
    if manifest is not None:
        validate_outer_manifest(root, manifest, findings)
    validate_archive(root, findings)
    validate_upstream_manifest(root, findings)
    validate_predecessor(root, findings)
    if receipt is not None:
        validate_receipt(receipt, findings)
    validate_raw_evidence(root, findings, verify_git_correlations)
    if anchor is not None:
        validate_anchor(root, anchor, findings)
    findings.sort(key=lambda item: (item["code"], item["path"], item["detail"]))
    return {
        "checker_id": "FORK_SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_CHECKER_v0_1",
        "status": (
            EXPECTED_STATUS
            if not findings
            else "SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_NONCONFORMING"
        ),
        "ok": not findings,
        "finding_count": len(findings),
        "finding_codes": sorted({item["code"] for item in findings}),
        "findings": findings,
        "source": {
            "release": "Icon369/verdict-evidence-transfers@pr63-pr64-ivs-v0_1_1",
            "asset_sha256": ARCHIVE_SHA256,
            "predecessor_attachment_state": "REFERENCED_NOT_RECEIVED",
            "successor_attachment_state": (
                "EXACT_RELEASE_ATTACHMENT_RECEIVED_AND_VERIFIED_WITH_INTERNAL_CAPTURE_GAP"
            ),
        },
        "standing": {
            "reviewer_declared_disposition": "REPRODUCED_WITHIN_DECLARED_SCOPE",
            "admission_state": "REVIEW_ELIGIBLE_NOT_ADMITTED",
            "pr_63_state": "STRUCTURALLY_READY_EXECUTION_BLOCKED",
            "execution_authority_delta": "NONE",
            "pair_001_execution_authorized": False,
        },
        "effects": EXPECTED_EFFECTS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = evaluate(args.repo_root)
    print(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)
        if args.json
        else result["status"]
    )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
