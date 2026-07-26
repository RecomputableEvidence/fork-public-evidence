#!/usr/bin/env python3
"""Mechanically normalize the preserved PR #91 rich return into schema v0.1.

The source receipt and its delivery ZIP remain unchanged. The successor keeps
the source disclosure, observations, disposition, non-claims, effects, and
attestation while translating only fields whose richer source shape is not
accepted by the v0.1 return schema.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


EXPECTED_SOURCE_RECEIPT_SHA256 = (
    "51d8249fe85fff34d288c1bfd7198639eecbd11e6fc4ae4872666fe63fcfacb9"
)
EXPECTED_SOURCE_ZIP_SHA256 = (
    "cb37f93be096d80f0f8ec5bc6082829ba4273bc1b214608da341949d46625155"
)

SEVERITY_BY_CLASSIFICATION = {
    "METHODOLOGICAL_LIMITATION": "INFO",
    "REVIEW_PACKAGE_CORRECTION_REQUIRED": "MINOR",
    "PUBLIC_METADATA_CORRECTION_REQUIRED": "MINOR",
    "PRESERVED_ADDITIONAL_NEGATIVE_EVIDENCE": "INFO",
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
    payload["integrity"].pop("receipt_payload_sha256", None)
    return payload


def verify_source_integrity(source: dict[str, Any]) -> None:
    declared = source["integrity"]["receipt_payload_sha256"]
    observed = canonical_sha256(receipt_integrity_payload(source))
    if declared != observed:
        raise ValueError(
            f"source receipt payload digest mismatch: declared {declared}, observed {observed}"
        )


def normalize_execution(execution: dict[str, Any]) -> dict[str, Any]:
    record_id = execution["record_id"]
    stdout = execution["stdout"]
    stderr = execution["stderr"]
    return {
        "command": execution["command"],
        "exit_code": execution["exit_code"],
        "stdout_sha256": stdout["sha256"],
        "stderr_sha256": stderr["sha256"],
        "observed_result": (
            f"record_id={record_id}; exit_code={execution['exit_code']}; "
            f"stdout={stdout['path']}; stderr={stderr['path']}"
        ),
    }


def normalize_adversarial(item: dict[str, Any]) -> dict[str, Any]:
    finding_codes = ",".join(item["finding_codes"]) or "NONE"
    return {
        "case_id": item["case_id"],
        "expected": f"REJECT_WITH_{item['required_code']}",
        "observed": (
            f"status={item['checker_status']}; finding_codes={finding_codes}"
        ),
        "conforms": item["rejected_as_required"],
    }


def normalize_finding(item: dict[str, Any]) -> dict[str, Any]:
    correction = item.get("correction")
    detail = item["detail"]
    if correction:
        detail = f"{detail} Correction: {correction}"
    return {
        "code": item["code"],
        "severity": SEVERITY_BY_CLASSIFICATION.get(
            item["classification"],
            "UNRESOLVED",
        ),
        "detail": detail,
        "evidence": (
            "Preserved source receipt finding "
            f"{item['finding_id']}; effect_on_core_reproduction="
            f"{item['effect_on_core_reproduction']}"
        ),
    }


def normalize(
    source_receipt_path: Path,
    source_zip_path: Path,
) -> dict[str, Any]:
    source_receipt_path = source_receipt_path.resolve()
    source_zip_path = source_zip_path.resolve()
    source_receipt_sha256 = sha256_file(source_receipt_path)
    source_zip_sha256 = sha256_file(source_zip_path)
    if source_receipt_sha256 != EXPECTED_SOURCE_RECEIPT_SHA256:
        raise ValueError(
            "source receipt does not match the registered original: "
            f"{source_receipt_sha256}"
        )
    if source_zip_sha256 != EXPECTED_SOURCE_ZIP_SHA256:
        raise ValueError(
            f"source ZIP does not match the registered original: {source_zip_sha256}"
        )

    source = strict_load(source_receipt_path)
    verify_source_integrity(source)
    measurements = source["measurements"]
    normalized = {
        "schema_version": source["schema_version"],
        "record_kind": source["record_kind"],
        "receipt_id": (
            "FORK_EXTERIOR_RECOMPUTATION_PR91_CHATGPT_20260724_NORMALIZED_v0_1_1"
        ),
        "review_target": source["review_target"],
        "reviewer_disclosure": source["reviewer_disclosure"],
        "environment": source["environment"],
        "executions": [
            normalize_execution(execution) for execution in source["executions"]
        ],
        "measurements": {
            "checker_status": measurements["checker_status"],
            "state_vector_sha256": measurements["state_vector_sha256"],
            "closure_node_digest_sha256": measurements[
                "closure_node_digest_sha256"
            ],
            "focused_tests": measurements["focused_tests"],
            "full_suite": measurements["full_suite"],
            "adversarial_results": [
                normalize_adversarial(item)
                for item in measurements["adversarial_results"]
            ],
        },
        "findings": [
            normalize_finding(item) for item in source["findings"]
        ]
        + [
            {
                "code": "SOURCE_RETURN_RECEIPT_SCHEMA_NORMALIZED",
                "severity": "INFO",
                "detail": (
                    "The sealed source return contained richer execution, finding, "
                    "measurement, and adversarial objects than schema v0.1 accepts. "
                    "This successor mechanically projects those objects into the "
                    "registered compact shapes without rerunning commands or "
                    "changing the recorded disposition."
                ),
                "evidence": (
                    f"source_receipt_sha256={source_receipt_sha256}; "
                    f"source_zip_sha256={source_zip_sha256}"
                ),
            }
        ],
        "raw_output_artifacts": [
            {
                "path": source_receipt_path.name,
                "sha256": source_receipt_sha256,
                "size_bytes": source_receipt_path.stat().st_size,
            },
            {
                "path": source_zip_path.name,
                "sha256": source_zip_sha256,
                "size_bytes": source_zip_path.stat().st_size,
            },
        ],
        "disposition": source["disposition"],
        "effects": source["effects"],
        "non_claims": source["non_claims"],
        "reviewer_attestation": source["reviewer_attestation"],
        "integrity": {"receipt_payload_sha256": ""},
    }
    normalized["integrity"]["receipt_payload_sha256"] = canonical_sha256(
        receipt_integrity_payload(normalized)
    )
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-receipt", type=Path, required=True)
    parser.add_argument("--source-zip", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    normalized = normalize(args.source_receipt, args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(normalized, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
