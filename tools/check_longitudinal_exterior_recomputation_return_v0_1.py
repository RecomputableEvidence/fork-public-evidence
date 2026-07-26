#!/usr/bin/env python3
"""Validate a returned longitudinal exterior-recomputation receipt.

This checker is intentionally separable from the full v0.3.1 package checker.
It can travel with a receipt template and schema, and it can optionally verify
the receipt's declared raw artifacts against an extracted delivery directory.
"""

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
SCHEMA_NAME = "fork_longitudinal_exterior_recomputation_receipt_v0_1.schema.json"
DEFAULT_REPO_SCHEMA = ROOT / "schemas" / SCHEMA_NAME
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_TARGETS = {
    91: {
        "target_id": "PR91_LINEAR_REPLAY_V0_2",
        "head_sha": "e848ea0825bafc1aa3754d89e719d71b5a9f3982",
        "tree_sha": "0b5f11eb6c1cd8c90b4cacce2a747045da917741",
        "checker_status": "LONGITUDINAL_STATE_REPRODUCED",
        "state_vector_sha256": (
            "9ce7d9b07df71481eb3020152084dce6e58b8172d7cea9f11d8bb6ec11f7a496"
        ),
        "closure_node_digest_sha256": "NOT_APPLICABLE",
        "focused_passed": 16,
    },
    92: {
        "target_id": "PR92_CAUSAL_RECONCILIATION_V0_3",
        "head_sha": "353c1b8159cfe0b4e1f3710b11a3c7f1aeb1bc84",
        "tree_sha": "a85af6ef1c7db88dcddbc709944d9872320cdb96",
        "checker_status": "CAUSAL_RECONCILIATION_REPRODUCED",
        "state_vector_sha256": (
            "356a64ee2dd317d752c5cbba2457942de4baa0506b9a0a2b119dce45a6f831c1"
        ),
        "closure_node_digest_sha256": (
            "28f504cdc071bd0b15767a3c41fc4511ae1bd7455bfef4d362c01eff8ca403d7"
        ),
        "focused_passed": 18,
    },
}

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


def canonical_sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def receipt_integrity_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(receipt)
    integrity = payload.get("integrity")
    if isinstance(integrity, dict):
        integrity.pop("receipt_payload_sha256", None)
    return payload


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_file(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if (
        not relative
        or "\\" in relative
        or pure.is_absolute()
        or any(part in ("", ".", "..") for part in pure.parts)
    ):
        raise ValueError(f"non-canonical relative path: {relative!r}")
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink is not permitted: {relative}")
    if not current.is_file():
        raise ValueError(f"regular file is missing: {relative}")
    return current


def add_finding(
    findings: list[dict[str, str]],
    code: str,
    detail: str,
    path: str = "$",
) -> None:
    findings.append({"code": code, "path": path, "detail": detail})


def default_schema_path() -> Path:
    sibling = Path(__file__).resolve().with_name(SCHEMA_NAME)
    return sibling if sibling.is_file() else DEFAULT_REPO_SCHEMA


def validate_return(
    receipt: dict[str, Any],
    schema: dict[str, Any],
    *,
    artifact_root: Path | None,
    allow_pending: bool,
) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    validator = Draft7Validator(schema)
    for error in sorted(validator.iter_errors(receipt), key=lambda item: list(item.path)):
        location = "$" + "".join(f"[{value!r}]" for value in error.path)
        add_finding(findings, "RECEIPT_SCHEMA_INVALID", error.message, location)
    if findings:
        return {
            "status": "EXTERIOR_RECOMPUTATION_RETURN_NONCONFORMING",
            "ok": False,
            "artifact_bindings_verified": False,
            "findings": findings,
        }

    target = receipt["review_target"]
    expected = EXPECTED_TARGETS.get(target["pull_request"])
    if expected is None:
        add_finding(findings, "REVIEW_TARGET_UNREGISTERED", "target PR is not registered")
    else:
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

    declared_integrity = receipt["integrity"]["receipt_payload_sha256"]
    derived_integrity = canonical_sha256(receipt_integrity_payload(receipt))
    if declared_integrity != derived_integrity:
        add_finding(
            findings,
            "RECEIPT_PAYLOAD_DIGEST_MISMATCH",
            f"declared {declared_integrity}, derived {derived_integrity}",
            "$.integrity.receipt_payload_sha256",
        )

    pending = receipt["disposition"] == "UNRESOLVED_PENDING_EXTERIOR_RECOMPUTATION"
    if pending and not allow_pending:
        add_finding(
            findings,
            "PENDING_RECEIPT_NOT_RESULT",
            "pending template is not a completed exterior result",
            "$.disposition",
        )

    if not pending and expected is not None:
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

    if (
        not pending
        and receipt["disposition"] == "REPRODUCED_WITHIN_DECLARED_SCOPE"
        and expected is not None
    ):
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
                "CONFORMANCE_DISPOSITION_CONTRADICTS_FOCUSED_TESTS",
                "focused-test measurement does not match the registered target",
                "$.measurements.focused_tests",
            )
        if receipt["findings"]:
            add_finding(
                findings,
                "CONFORMANCE_DISPOSITION_HAS_FINDINGS",
                "within-scope conformance cannot retain substantive findings",
                "$.findings",
            )

    artifact_bindings_verified = artifact_root is not None
    if artifact_root is not None:
        root = artifact_root.resolve()
        seen: set[str] = set()
        for index, artifact in enumerate(receipt["raw_output_artifacts"]):
            relative = artifact["path"]
            if relative in seen:
                add_finding(
                    findings,
                    "RAW_ARTIFACT_PATH_DUPLICATE",
                    f"duplicate artifact path {relative!r}",
                    f"$.raw_output_artifacts[{index}].path",
                )
                continue
            seen.add(relative)
            try:
                path = safe_file(root, relative)
            except ValueError as error:
                add_finding(
                    findings,
                    "RAW_ARTIFACT_MISSING_OR_UNSAFE",
                    str(error),
                    f"$.raw_output_artifacts[{index}].path",
                )
                continue
            if path.stat().st_size != artifact["size_bytes"]:
                add_finding(
                    findings,
                    "RAW_ARTIFACT_SIZE_MISMATCH",
                    f"{relative}: declared {artifact['size_bytes']}, observed {path.stat().st_size}",
                    f"$.raw_output_artifacts[{index}].size_bytes",
                )
            observed_sha256 = sha256_file(path)
            if observed_sha256 != artifact["sha256"]:
                add_finding(
                    findings,
                    "RAW_ARTIFACT_DIGEST_MISMATCH",
                    f"{relative}: declared {artifact['sha256']}, observed {observed_sha256}",
                    f"$.raw_output_artifacts[{index}].sha256",
                )

    if findings:
        status = "EXTERIOR_RECOMPUTATION_RETURN_NONCONFORMING"
    elif pending:
        status = "EXTERIOR_RECOMPUTATION_RETURN_TEMPLATE_CONFORMS"
    elif artifact_bindings_verified:
        status = "EXTERIOR_RECOMPUTATION_RETURN_CONFORMS"
    else:
        status = "EXTERIOR_RECOMPUTATION_RETURN_CONFORMS_ARTIFACTS_NOT_CHECKED"
    return {
        "status": status,
        "ok": not findings,
        "artifact_bindings_verified": artifact_bindings_verified and not findings,
        "recorded_disposition": receipt["disposition"],
        "receipt_payload_sha256": declared_integrity,
        "finding_codes": sorted({item["code"] for item in findings}),
        "findings": findings,
        "effects": receipt["effects"],
        "substantive_recomputation_inferred": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--schema", type=Path, default=default_schema_path())
    parser.add_argument("--artifact-root", type=Path)
    parser.add_argument("--allow-pending", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        schema = strict_load(args.schema.resolve())
        Draft7Validator.check_schema(schema)
        receipt = strict_load(args.receipt.resolve())
        result = validate_return(
            receipt,
            schema,
            artifact_root=args.artifact_root,
            allow_pending=args.allow_pending,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {
            "status": "EXTERIOR_RECOMPUTATION_RETURN_NONCONFORMING",
            "ok": False,
            "artifact_bindings_verified": False,
            "finding_codes": ["RETURN_VALIDATION_INPUT_INVALID"],
            "findings": [
                {
                    "code": "RETURN_VALIDATION_INPUT_INVALID",
                    "path": "$",
                    "detail": str(error),
                }
            ],
            "substantive_recomputation_inferred": False,
        }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(result["status"])
        for finding in result["findings"]:
            print(f"{finding['code']}: {finding['path']}: {finding['detail']}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
