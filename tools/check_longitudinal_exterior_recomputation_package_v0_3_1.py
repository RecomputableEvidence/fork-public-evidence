#!/usr/bin/env python3
"""Validate the v0.3.1 exterior-recomputation package and returned receipts."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft7Validator


ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/state/longitudinal-recomputation-v0.3.1")
MANIFEST = BASE / "EXTERIOR_RECOMPUTATION_PACKAGE_MANIFEST_v0_3_1.json"
STACK = BASE / "STACK_REVIEW_COORDINATES_v0_1.json"
ENVELOPE_91 = BASE / "EXTERIOR_RECOMPUTATION_ENVELOPE_PR91_v0_1.md"
ENVELOPE_92 = BASE / "EXTERIOR_RECOMPUTATION_ENVELOPE_PR92_v0_1.md"
TEMPLATE_91 = BASE / "EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR91_v0_1.json"
TEMPLATE_92 = BASE / "EXTERIOR_RECOMPUTATION_RECEIPT_TEMPLATE_PR92_v0_1.json"
README = BASE / "README.md"
SCHEMA = Path("schemas/fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json")
TOOL = Path("tools/check_longitudinal_exterior_recomputation_package_v0_3_1.py")
TEST = Path("tests/test_longitudinal_exterior_recomputation_package_v0_3_1.py")
RETURN_TOOL = Path("tools/check_longitudinal_exterior_recomputation_return_v0_1.py")
RETURN_TEST = Path("tests/test_longitudinal_exterior_recomputation_return_v0_1.py")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_PACKAGE_PATHS = {
    ENVELOPE_91.as_posix(),
    ENVELOPE_92.as_posix(),
    TEMPLATE_91.as_posix(),
    TEMPLATE_92.as_posix(),
    README.as_posix(),
    STACK.as_posix(),
    SCHEMA.as_posix(),
    TOOL.as_posix(),
    TEST.as_posix(),
    RETURN_TOOL.as_posix(),
    RETURN_TEST.as_posix(),
}

EXPECTED_TARGETS = {
    91: {
        "target_id": "PR91_LINEAR_REPLAY_V0_2",
        "head_sha": "e848ea0825bafc1aa3754d89e719d71b5a9f3982",
        "tree_sha": "0b5f11eb6c1cd8c90b4cacce2a747045da917741",
        "checker_status": "LONGITUDINAL_STATE_REPRODUCED",
        "state_vector_sha256": "9ce7d9b07df71481eb3020152084dce6e58b8172d7cea9f11d8bb6ec11f7a496",
        "closure_node_digest_sha256": "NOT_APPLICABLE",
        "focused_passed": 16,
    },
    92: {
        "target_id": "PR92_CAUSAL_RECONCILIATION_V0_3",
        "head_sha": "353c1b8159cfe0b4e1f3710b11a3c7f1aeb1bc84",
        "tree_sha": "a85af6ef1c7db88dcddbc709944d9872320cdb96",
        "checker_status": "CAUSAL_RECONCILIATION_REPRODUCED",
        "state_vector_sha256": "356a64ee2dd317d752c5cbba2457942de4baa0506b9a0a2b119dce45a6f831c1",
        "closure_node_digest_sha256": "28f504cdc071bd0b15767a3c41fc4511ae1bd7455bfef4d362c01eff8ca403d7",
        "focused_passed": 18,
    },
}

EXPECTED_STACK = [
    {
        "order": 1,
        "pull_request": 89,
        "url": "https://github.com/RecomputableEvidence/fork-public-evidence/pull/89",
        "branch": "research/fork-thesis-manifestation-v0-1",
        "head_sha": "b93f9a1bce094e8c65e0d1ef04dbe52a11aab0b1",
        "tree_sha": "78703afea0d4b4208f6226207e8a2e44bdaed6a0",
        "depends_on_pull_request": None,
        "exact_predecessor": "1241c0084900f2c60f362205525464582e57b4a7",
        "standing": "OPEN_DRAFT_RESEARCH_CANDIDATE_NOT_ADMITTED",
    },
    {
        "order": 2,
        "pull_request": 90,
        "url": "https://github.com/RecomputableEvidence/fork-public-evidence/pull/90",
        "branch": "research/temporal-succession-observation-v0-1",
        "head_sha": "f955834681d2f2ee257276acbf68afde0ae0e69d",
        "tree_sha": "52ca08a41173e031ade01b9b6ec529cc80776380",
        "depends_on_pull_request": 89,
        "exact_predecessor": "b93f9a1bce094e8c65e0d1ef04dbe52a11aab0b1",
        "standing": "OPEN_DRAFT_PRESERVATION_DELTA_VERIFIED_WITHIN_DECLARED_SCOPE_NOT_ADMITTED",
    },
    {
        "order": 3,
        "pull_request": 91,
        "url": "https://github.com/RecomputableEvidence/fork-public-evidence/pull/91",
        "branch": "agent/longitudinal-recomputation-replay-v0-2",
        "head_sha": EXPECTED_TARGETS[91]["head_sha"],
        "tree_sha": EXPECTED_TARGETS[91]["tree_sha"],
        "depends_on_pull_request": 90,
        "exact_predecessor": "f955834681d2f2ee257276acbf68afde0ae0e69d",
        "standing": "OPEN_DRAFT_REPRODUCED_WITH_CORRECTION_REQUIRED_RECEIPT_NORMALIZED_NOT_ADMITTED",
    },
    {
        "order": 4,
        "pull_request": 92,
        "url": "https://github.com/RecomputableEvidence/fork-public-evidence/pull/92",
        "branch": "agent/longitudinal-causal-reconciliation-v0-3",
        "head_sha": EXPECTED_TARGETS[92]["head_sha"],
        "tree_sha": EXPECTED_TARGETS[92]["tree_sha"],
        "depends_on_pull_request": 91,
        "exact_predecessor": EXPECTED_TARGETS[91]["head_sha"],
        "standing": "OPEN_DRAFT_EXTERIOR_RECOMPUTATION_PENDING_NOT_ADMITTED",
    },
]

REQUIRED_NON_CLAIMS = {
    "Package conformance is not substantive recomputation.",
    "A reviewer receipt is not admission or merge authorization.",
    "Recomputation does not establish truth, legal sufficiency, compliance, safety, or institutional authority.",
    "Expected values must not replace observed commands, outputs, exit codes, and digests.",
}

EXPECTED_EFFECTS = {
    "provider_calls": 0,
    "pair_001_calls": 0,
    "pair_001_repetitions": 0,
    "admission": "NONE",
    "merge_authorization": "NONE",
    "publication": "NONE",
    "authority_transfer": "NONE",
    "execution_permission": "NONE",
}


def add_finding(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str = "$",
) -> None:
    findings.append({"code": code, "path": path, "detail": detail})


def strict_load(path: Path) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def pretty_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def canonical_sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def safe_file(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if (
        not relative
        or "\\" in relative
        or pure.is_absolute()
        or any(part in ("", ".", "..") for part in pure.parts)
    ):
        raise ValueError(f"non-canonical relative path: {relative!r}")
    path = root.joinpath(*pure.parts)
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink is not permitted: {relative}")
    if not path.is_file():
        raise ValueError(f"regular file is missing: {relative}")
    return path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest(root: Path) -> dict[str, Any]:
    entries = []
    for relative in sorted(EXPECTED_PACKAGE_PATHS):
        path = safe_file(root, relative)
        entries.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "schema_version": "v0.3.1",
        "record_kind": "fork_longitudinal_exterior_recomputation_package_manifest",
        "package_id": "FORK_LONGITUDINAL_EXTERIOR_RECOMPUTATION_v0_3_1",
        "entries": entries,
        "predecessor_package": {
            "path": "docs/state/longitudinal-recomputation-v0.3/PACKAGE_MANIFEST_v0_3.json",
            "sha256": "0f00137a91b34206aa844b41bae951ef19157bdbc8095b6ed1b69ec2cff0a677",
            "standing": "PRESERVED_UNCHANGED_AT_PR92_SOURCE_COORDINATE",
        },
        "external_moving_dependencies_not_package_members": [
            {
                "path": "docs/state/README.md",
                "reason": "SHARED_FRONT_DOOR_ACCUMULATES_SUCCESSOR_ROUTES",
            },
            {
                "path": "receipts/claim-admission/FORK_CLAIM_ADMISSION_HARDENING_SELF_CHECK_RECEIPT_v0_1.json",
                "reason": "GLOBAL_SELF_CHECK_RECEIPT_CHANGES_WITH_SUCCESSOR_TREE_INVENTORY",
            },
        ],
        "self_exclusion": {
            "path": MANIFEST.as_posix(),
            "reason": "AVOIDS_CIRCULAR_FULL_FILE_DIGEST",
        },
        "non_claims": [
            "Package conformance is not exterior recomputation.",
            "A valid adverse receipt remains adverse evidence.",
            "This package does not authorize admission, merge, publication, authority, or execution.",
        ],
    }


def load_schema(root: Path) -> dict[str, Any]:
    schema = strict_load(safe_file(root, SCHEMA.as_posix()))
    Draft7Validator.check_schema(schema)
    return schema


def receipt_integrity_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(receipt)
    integrity = payload.get("integrity")
    if isinstance(integrity, dict):
        integrity.pop("receipt_payload_sha256", None)
    return payload


def validate_receipt(
    receipt: dict[str, Any],
    schema: dict[str, Any],
    *,
    allow_pending: bool,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    validator = Draft7Validator(schema)
    for error in sorted(validator.iter_errors(receipt), key=lambda item: list(item.path)):
        location = "$" + "".join(f"[{value!r}]" for value in error.path)
        add_finding(findings, "RECEIPT_SCHEMA_INVALID", error.message, location)
    if findings:
        return findings

    target = receipt["review_target"]
    expected = EXPECTED_TARGETS.get(target["pull_request"])
    if expected is None:
        add_finding(findings, "REVIEW_TARGET_UNREGISTERED", "target PR is not registered")
        return findings
    for field in ("target_id", "head_sha", "tree_sha"):
        if target[field] != expected[field]:
            add_finding(
                findings,
                "REVIEW_TARGET_COORDINATE_MISMATCH",
                f"{field} expected {expected[field]!r}, found {target[field]!r}",
                f"$.review_target.{field}",
            )
    if receipt["effects"] != EXPECTED_EFFECTS:
        add_finding(
            findings,
            "RECEIPT_EFFECT_PROMOTION",
            "receipt effects differ from the no-effect boundary",
            "$.effects",
        )
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - set(receipt["non_claims"]))
    if missing_non_claims:
        add_finding(
            findings,
            "REQUIRED_NON_CLAIM_MISSING",
            f"missing {missing_non_claims!r}",
            "$.non_claims",
        )

    pending = receipt["disposition"] == "UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION"
    if pending:
        if not allow_pending:
            add_finding(
                findings,
                "PENDING_RECEIPT_NOT_RESULT",
                "pending template is not a completed exterior result",
                "$.disposition",
            )
        return findings

    disclosure = receipt["reviewer_disclosure"]
    unresolved_values = {
        disclosure["reviewer_id"],
        disclosure["affiliation"],
        disclosure["relationship_to_fork"],
        disclosure["prior_exposure"],
    }
    if any(value.startswith("UNRESOLVED") for value in unresolved_values):
        add_finding(
            findings,
            "REVIEWER_DISCLOSURE_INCOMPLETE",
            "completed receipt retains unresolved reviewer disclosure",
            "$.reviewer_disclosure",
        )
    if disclosure["independence_class"] == "UNRESOLVED_PENDING_DISCLOSURE":
        add_finding(
            findings,
            "REVIEWER_DISCLOSURE_INCOMPLETE",
            "completed receipt has no independence classification",
            "$.reviewer_disclosure.independence_class",
        )
    attestation = receipt["reviewer_attestation"]
    if any(
        value.startswith("UNRESOLVED")
        for value in (attestation["statement"], attestation["recorded_at_utc"])
    ):
        add_finding(
            findings,
            "REVIEWER_ATTESTATION_INCOMPLETE",
            "returned receipt retains an unresolved attestation",
            "$.reviewer_attestation",
        )

    declared_integrity = receipt["integrity"]["receipt_payload_sha256"]
    if not SHA256_RE.fullmatch(declared_integrity):
        add_finding(
            findings,
            "RECEIPT_PAYLOAD_DIGEST_MISSING",
            "returned receipt must carry a SHA-256 payload digest",
            "$.integrity.receipt_payload_sha256",
        )
    elif canonical_sha256(receipt_integrity_payload(receipt)) != declared_integrity:
        add_finding(
            findings,
            "RECEIPT_PAYLOAD_DIGEST_MISMATCH",
            "receipt payload digest does not recompute",
            "$.integrity.receipt_payload_sha256",
        )

    if receipt["disposition"] == "UNRESOLVED_INCOMPLETE":
        if not receipt["findings"]:
            add_finding(
                findings,
                "UNRESOLVED_DISPOSITION_FINDING_MISSING",
                "incomplete receipt must preserve the blocking condition",
                "$.findings",
            )
        return findings

    if target["acquired_head_sha"] != expected["head_sha"]:
        add_finding(
            findings,
            "ACQUIRED_HEAD_MISMATCH",
            "acquired head does not equal the declared exact target",
            "$.review_target.acquired_head_sha",
        )
    if target["acquired_tree_sha"] != expected["tree_sha"]:
        add_finding(
            findings,
            "ACQUIRED_TREE_MISMATCH",
            "acquired tree does not equal the declared exact target",
            "$.review_target.acquired_tree_sha",
        )
    if receipt["environment"]["dependency_install_exit_code"] != 0:
        add_finding(
            findings,
            "DEPENDENCY_INSTALL_NOT_REPRODUCED",
            "completed receipt does not record a successful locked dependency install",
            "$.environment.dependency_install_exit_code",
        )
    if len(receipt["executions"]) < 2:
        add_finding(
            findings,
            "RAW_EXECUTION_RECORD_INCOMPLETE",
            "completed receipt requires at least checker and focused-test executions",
            "$.executions",
        )
    if not receipt["raw_output_artifacts"]:
        add_finding(
            findings,
            "RAW_OUTPUT_ARTIFACT_MISSING",
            "completed receipt must bind at least one raw output artifact",
            "$.raw_output_artifacts",
        )
    for index, execution in enumerate(receipt["executions"]):
        for stream in ("stdout_sha256", "stderr_sha256"):
            if not SHA256_RE.fullmatch(execution[stream]):
                add_finding(
                    findings,
                    "RAW_EXECUTION_DIGEST_MISSING",
                    f"completed execution lacks a {stream} digest",
                    f"$.executions[{index}].{stream}",
                )

    if receipt["disposition"] == "REPRODUCED_WITHIN_DECLARED_SCOPE":
        measurements = receipt["measurements"]
        comparisons = {
            "checker_status": expected["checker_status"],
            "state_vector_sha256": expected["state_vector_sha256"],
            "closure_node_digest_sha256": expected["closure_node_digest_sha256"],
        }
        for field, value in comparisons.items():
            if measurements[field] != value:
                add_finding(
                    findings,
                    "CONFORMANCE_DISPOSITION_CONTRADICTS_MEASUREMENT",
                    f"{field} expected {value!r}, found {measurements[field]!r}",
                    f"$.measurements.{field}",
                )
        focused = measurements["focused_tests"]
        if (
            focused["passed"] != expected["focused_passed"]
            or focused["failed"] != 0
            or focused["exit_code"] != 0
        ):
            add_finding(
                findings,
                "CONFORMANCE_DISPOSITION_CONTRADICTS_TESTS",
                f"expected {expected['focused_passed']} focused passes and zero failures",
                "$.measurements.focused_tests",
            )
        if receipt["findings"]:
            add_finding(
                findings,
                "CONFORMANCE_DISPOSITION_CONTRADICTS_FINDINGS",
                "unqualified conformance cannot retain substantive findings",
                "$.findings",
            )
    elif receipt["disposition"] in {
        "REPRODUCED_WITH_CORRECTION_REQUIRED",
        "NOT_REPRODUCED",
    } and not receipt["findings"]:
        add_finding(
            findings,
            "ADVERSE_DISPOSITION_FINDING_MISSING",
            "adverse disposition must preserve at least one finding",
            "$.findings",
        )
    return findings


def evaluate(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    try:
        schema = load_schema(root)
        manifest = strict_load(safe_file(root, MANIFEST.as_posix()))
        expected_manifest = build_manifest(root)
        if manifest != expected_manifest:
            add_finding(
                findings,
                "PACKAGE_MANIFEST_DIVERGENCE",
                "committed manifest differs from current package bytes",
                MANIFEST.as_posix(),
            )
        stack = strict_load(safe_file(root, STACK.as_posix()))
        if stack.get("stack") != EXPECTED_STACK:
            add_finding(
                findings,
                "STACK_COORDINATE_DIVERGENCE",
                "stack entries differ from registered exact coordinates",
                STACK.as_posix(),
            )
        expected_stack_header = {
            "schema_version": "v0.1",
            "record_kind": "fork_longitudinal_recomputation_stack_review_coordinates",
            "repository": "RecomputableEvidence/fork-public-evidence",
            "snapshot_date": "2026-07-24",
        }
        for field, value in expected_stack_header.items():
            if stack.get(field) != value:
                add_finding(
                    findings,
                    "STACK_HEADER_DIVERGENCE",
                    f"{field} expected {value!r}, found {stack.get(field)!r}",
                    STACK.as_posix(),
                )
        if stack.get("exterior_recomputation_order") != [91, 92]:
            add_finding(
                findings,
                "STACK_REVIEW_ORDER_DIVERGENCE",
                "exterior review must route PR #91 before PR #92",
                STACK.as_posix(),
            )
        if stack.get("merge_or_admission_order_if_separately_authorized") != [
            89,
            90,
            91,
            92,
        ]:
            add_finding(
                findings,
                "STACK_DECISION_ORDER_DIVERGENCE",
                "separately authorized decisions must remain bottom-up",
                STACK.as_posix(),
            )
        predecessor = safe_file(
            root,
            "docs/state/longitudinal-recomputation-v0.3/PACKAGE_MANIFEST_v0_3.json",
        )
        predecessor_sha = sha256_file(predecessor)
        if (
            predecessor_sha
            != "0f00137a91b34206aa844b41bae951ef19157bdbc8095b6ed1b69ec2cff0a677"
        ):
            add_finding(
                findings,
                "PREDECESSOR_PACKAGE_DIVERGENCE",
                f"v0.3 package manifest changed to {predecessor_sha}",
                predecessor.relative_to(root).as_posix(),
            )
        for path, pr in ((TEMPLATE_91, 91), (TEMPLATE_92, 92)):
            template = strict_load(safe_file(root, path.as_posix()))
            template_findings = validate_receipt(template, schema, allow_pending=True)
            for finding in template_findings:
                finding["path"] = f"{path.as_posix()}:{finding['path']}"
                findings.append(finding)
            if template.get("review_target", {}).get("pull_request") != pr:
                add_finding(
                    findings,
                    "RECEIPT_TEMPLATE_TARGET_MISMATCH",
                    f"template does not target PR #{pr}",
                    path.as_posix(),
                )
            if template.get("disposition") != "UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION":
                add_finding(
                    findings,
                    "TEMPLATE_CONTAINS_REVIEW_RESULT",
                    "package template must not claim a completed result",
                    path.as_posix(),
                )
        required_tokens = {
            "UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION",
            "PRIOR_EXPOSURE_DISCLOSED",
            "Expected values must not replace",
            "NO_ADMISSION_OR_EXECUTION_EFFECT",
            "check_longitudinal_exterior_recomputation_return_v0_1.py",
            "fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json",
        }
        for envelope in (ENVELOPE_91, ENVELOPE_92):
            text = safe_file(root, envelope.as_posix()).read_text(encoding="utf-8")
            for token in sorted(required_tokens):
                if token not in text:
                    add_finding(
                        findings,
                        "ENVELOPE_REQUIRED_BOUNDARY_MISSING",
                        f"required token {token!r} is absent",
                        envelope.as_posix(),
                    )
            pr = 91 if envelope == ENVELOPE_91 else 92
            expected = EXPECTED_TARGETS[pr]
            for coordinate in (expected["head_sha"], expected["tree_sha"]):
                if coordinate not in text:
                    add_finding(
                        findings,
                        "ENVELOPE_TARGET_COORDINATE_MISSING",
                        f"PR #{pr} coordinate {coordinate} is absent",
                        envelope.as_posix(),
                    )
    except Exception as exc:
        add_finding(findings, "PACKAGE_INPUT_INVALID", str(exc))
    ordered = sorted(
        findings,
        key=lambda item: (item["code"], item["path"], item["detail"]),
    )
    return {
        "status": (
            "EXTERIOR_RECOMPUTATION_PACKAGE_CONFORMS"
            if not ordered
            else "EXTERIOR_RECOMPUTATION_PACKAGE_NONCONFORMING"
        ),
        "ok": not ordered,
        "finding_codes": sorted({item["code"] for item in ordered}),
        "findings": ordered,
        "review_results_present": False,
        "standing": "REVIEW_PACKAGE_CANDIDATE_NO_REVIEW_RESULT",
        "effects": EXPECTED_EFFECTS,
    }


def validate_receipt_path(root: Path, receipt_path: Path) -> dict[str, Any]:
    root = root.resolve()
    schema = load_schema(root)
    receipt = strict_load(receipt_path.resolve())
    findings = validate_receipt(receipt, schema, allow_pending=False)
    ordered = sorted(
        findings,
        key=lambda item: (item["code"], item["path"], item["detail"]),
    )
    return {
        "status": (
            "EXTERIOR_RECOMPUTATION_RECEIPT_CONFORMS_TO_RECORDING_CONTRACT"
            if not ordered
            else "EXTERIOR_RECOMPUTATION_RECEIPT_NONCONFORMING"
        ),
        "ok": not ordered,
        "finding_codes": sorted({item["code"] for item in ordered}),
        "findings": ordered,
        "recorded_disposition": receipt.get("disposition"),
        "substantive_recomputation_inferred": False,
        "effects": EXPECTED_EFFECTS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    result = (
        validate_receipt_path(root, args.receipt)
        if args.receipt is not None
        else evaluate(root)
    )
    if args.json or not result["ok"]:
        print(pretty_json(result), end="")
    else:
        print(result["status"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
