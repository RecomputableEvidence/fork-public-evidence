#!/usr/bin/env python3
"""
Fork Longitudinal Reconstruction Trial Day-0 Packet Checker v0.1.

Verifies the Day-0 packet manifest, artifact hashes, manifest hash sidecar,
outer receipt binding, expected reconstruction hash, environment manifest hash,
and non-authority boundary statement hash.

This checker does not validate truth, compliance, legal sufficiency, safety,
authorization, approval, certification, endorsement, production readiness, or
institutional authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any, Dict, List


DEFAULT_PACKET_ROOT = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"

NON_AUTHORITY_TERMS = [
    "does not",
    "truth",
    "compliance",
    "legal",
    "safety",
    "authorization",
    "approval",
    "certification",
    "endorsement",
    "production readiness",
    "authority",
]

REQUIRED_PACKET_FILES = [
    "README.md",
    "packet_manifest.json",
    "packet_manifest.sha256",
    "packet_manifest_outer_receipt.json",
    "boundary/day0_non_authority_boundary_statement.txt",
    "evidence/day0_request_record.json",
    "evidence/day0_ai_output_record.json",
    "evidence/day0_human_review_record.json",
    "evidence/day0_boundary_state_record.json",
    "evidence/day0_non_claims_record.json",
    "expected/day0_expected_reconstruction.json",
    "environment/day0_environment_manifest.json",
    "receipts/day0_generation_receipt.json",
    "receipts/day0_expected_reconstruction_provenance_receipt.json",
    "receipts/day0_packet_scope_receipt.json",
]


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: pathlib.Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} root must be object")
    return data


def result(name: str, passed: bool, detail: str = "", data: Any = None) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "detail": detail,
        "data": data,
    }


def has_boundary_terms(text: str) -> List[str]:
    lower = text.lower()
    return [term for term in NON_AUTHORITY_TERMS if term not in lower]


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-root", default=DEFAULT_PACKET_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    packet_root = pathlib.Path(args.packet_root)
    results: List[Dict[str, Any]] = []

    if not packet_root.exists():
        results.append(result("packet-root", False, f"missing: {packet_root}"))
        summary = summarize(packet_root, results)
        print_summary(summary, args.json)
        return 1

    for rel in REQUIRED_PACKET_FILES:
        path = packet_root / rel
        results.append(result(f"path:{rel}", path.exists(), "present" if path.exists() else "missing"))

    manifest_path = packet_root / "packet_manifest.json"
    manifest_sha_path = packet_root / "packet_manifest.sha256"
    outer_receipt_path = packet_root / "packet_manifest_outer_receipt.json"

    manifest: Dict[str, Any] = {}
    outer: Dict[str, Any] = {}

    try:
        manifest = load_json(manifest_path)
        results.append(result("manifest:parse", True, "packet_manifest.json parsed"))
    except Exception as exc:
        results.append(result("manifest:parse", False, str(exc)))

    try:
        outer = load_json(outer_receipt_path)
        results.append(result("outer-receipt:parse", True, "packet_manifest_outer_receipt.json parsed"))
    except Exception as exc:
        results.append(result("outer-receipt:parse", False, str(exc)))

    if manifest:
        required_manifest_fields = [
            "manifest_schema_version",
            "trial_id",
            "packet_id",
            "created_at_fixed_fixture_time",
            "generated_from_base_commit",
            "canonicalization_method",
            "artifact_hashes",
            "expected_reconstruction_hash",
            "environment_manifest_hash",
            "non_authority_boundary_statement_hash",
            "non_authority_statement",
        ]
        missing = [field for field in required_manifest_fields if field not in manifest]
        results.append(result("manifest:required-fields", not missing, "missing: " + ", ".join(missing) if missing else "present"))

        missing_terms = has_boundary_terms(str(manifest.get("non_authority_statement", "")))
        results.append(result("manifest:non-authority-terms", not missing_terms, "missing: " + ", ".join(missing_terms) if missing_terms else "present"))

        artifacts = manifest.get("artifact_hashes", [])
        artifact_errors = []
        if not isinstance(artifacts, list) or not artifacts:
            artifact_errors.append("artifact_hashes must be non-empty array")
        else:
            for item in artifacts:
                if not isinstance(item, dict):
                    artifact_errors.append("artifact entry must be object")
                    continue

                rel_path = item.get("path")
                expected_hash = item.get("sha256")

                if not isinstance(rel_path, str) or not rel_path:
                    artifact_errors.append("artifact path missing")
                    continue

                if not isinstance(expected_hash, str) or not re.match(r"^[a-f0-9]{64}$", expected_hash):
                    artifact_errors.append(f"{rel_path}: invalid sha256")
                    continue

                artifact_path = pathlib.Path(rel_path)
                if not artifact_path.exists():
                    artifact_errors.append(f"{rel_path}: missing")
                    continue

                actual_hash = sha256_file(artifact_path)
                if actual_hash != expected_hash:
                    artifact_errors.append(f"{rel_path}: hash mismatch expected {expected_hash} actual {actual_hash}")

        results.append(result("manifest:artifact-hashes", not artifact_errors, "; ".join(artifact_errors) if artifact_errors else "all artifact hashes match"))

        expected_path = packet_root / "expected/day0_expected_reconstruction.json"
        env_path = packet_root / "environment/day0_environment_manifest.json"
        boundary_path = packet_root / "boundary/day0_non_authority_boundary_statement.txt"

        named_hash_checks = [
            ("manifest:expected-reconstruction-hash", expected_path, manifest.get("expected_reconstruction_hash")),
            ("manifest:environment-manifest-hash", env_path, manifest.get("environment_manifest_hash")),
            ("manifest:non-authority-boundary-statement-hash", boundary_path, manifest.get("non_authority_boundary_statement_hash")),
        ]

        for name, path, expected_hash in named_hash_checks:
            if not path.exists():
                results.append(result(name, False, f"missing: {path}"))
            else:
                actual_hash = sha256_file(path)
                results.append(result(name, actual_hash == expected_hash, f"expected {expected_hash} actual {actual_hash}"))

        if boundary_path.exists():
            boundary_text = boundary_path.read_text(encoding="utf-8")
            missing_boundary_terms = has_boundary_terms(boundary_text)
            results.append(result(
                "boundary-statement:non-authority-terms",
                not missing_boundary_terms,
                "missing: " + ", ".join(missing_boundary_terms) if missing_boundary_terms else "present",
            ))

    if manifest_path.exists() and manifest_sha_path.exists():
        actual_manifest_hash = sha256_file(manifest_path)
        sidecar_text = manifest_sha_path.read_text(encoding="utf-8").strip().lower()
        sidecar_ok = actual_manifest_hash in sidecar_text and "packet_manifest.json" in sidecar_text
        results.append(result("manifest-sidecar:sha256", sidecar_ok, f"actual manifest hash {actual_manifest_hash}"))
    else:
        actual_manifest_hash = ""
        results.append(result("manifest-sidecar:sha256", False, "manifest or sidecar missing"))

    if outer:
        outer_hash = str(outer.get("packet_manifest_sha256", "")).lower()
        outer_ok = bool(actual_manifest_hash) and outer_hash == actual_manifest_hash
        results.append(result("outer-receipt:manifest-hash-binding", outer_ok, f"outer {outer_hash} actual {actual_manifest_hash}"))

        missing_outer_terms = has_boundary_terms(str(outer.get("non_authority_statement", "")))
        results.append(result("outer-receipt:non-authority-terms", not missing_outer_terms, "missing: " + ", ".join(missing_outer_terms) if missing_outer_terms else "present"))

    summary = summarize(packet_root, results)
    print_summary(summary, args.json)
    return 0 if summary["failed"] == 0 else 1


def summarize(packet_root: pathlib.Path, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = sum(1 for item in results if not item["passed"])
    return {
        "checker": "check_longitudinal_reconstruction_day0_packet_v0_1.py",
        "packet_root": str(packet_root).replace("\\", "/"),
        "total": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "results": results,
        "non_authority_statement": (
            "This checker verifies Day-0 packet presence, hash continuity, manifest binding, "
            "and boundary statement presence only; it does not validate truth, compliance, "
            "legal sufficiency, safety, authorization, approval, certification, endorsement, "
            "production readiness, or institutional authority."
        ),
    }


def print_summary(summary: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return

    print(f"Longitudinal Day-0 packet: {summary['passed']}/{summary['total']} passed")
    for item in summary["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"{status} {item['name']}")
        if not item["passed"] and item["detail"]:
            print(f"  - {item['detail']}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))