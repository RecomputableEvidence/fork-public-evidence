#!/usr/bin/env python3
"""Fork Longitudinal Reconstruction Trial Day-0 Packet Checker v0.1.1.

Successor to v0.1. Preserves the historical v0.1 checker unchanged and adds:

* packet-root-bound artifact resolution;
* exact packet inventory comparison;
* path-escape rejection; and
* symlink substitution rejection.

This checker verifies bounded packet structure and integrity only. It does not
validate truth, compliance, legal sufficiency, safety, authorization, approval,
certification, endorsement, production readiness, procurement approval, or
institutional authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

DEFAULT_PACKET_ROOT = "docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1"
PACKET_METADATA_FILES = {
    "packet_manifest.json",
    "packet_manifest.sha256",
    "packet_manifest_outer_receipt.json",
}
NON_AUTHORITY_TERMS = [
    "does not", "truth", "compliance", "legal", "safety", "authorization",
    "approval", "certification", "endorsement", "production readiness", "authority",
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
    return {"name": name, "passed": passed, "detail": detail, "data": data}


def has_boundary_terms(text: str) -> List[str]:
    lower = text.lower()
    return [term for term in NON_AUTHORITY_TERMS if term not in lower]


def normalize_rel(path_text: str) -> str:
    return pathlib.PurePosixPath(path_text.replace("\\", "/")).as_posix()


def packet_relative_manifest_path(path_text: str) -> Tuple[Optional[str], Optional[str]]:
    normalized = normalize_rel(path_text)
    pure = pathlib.PurePosixPath(normalized)
    if pure.is_absolute():
        return None, "absolute path prohibited"
    if not pure.parts or any(part in {"", ".", ".."} for part in pure.parts):
        return None, "path traversal or non-canonical segment prohibited"

    prefix = pathlib.PurePosixPath(DEFAULT_PACKET_ROOT)
    if tuple(pure.parts[: len(prefix.parts)]) == prefix.parts:
        remainder = pure.parts[len(prefix.parts):]
        if not remainder:
            return None, "artifact path identifies packet root, not a file"
        return pathlib.PurePosixPath(*remainder).as_posix(), None
    return pure.as_posix(), None


def path_has_symlink(packet_root: pathlib.Path, rel_path: str) -> bool:
    current = packet_root
    for part in pathlib.PurePosixPath(rel_path).parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def resolve_packet_file(packet_root: pathlib.Path, rel_path: str) -> Tuple[Optional[pathlib.Path], Optional[str]]:
    if path_has_symlink(packet_root, rel_path):
        return None, "symlink substitution prohibited"
    candidate = packet_root.joinpath(*pathlib.PurePosixPath(rel_path).parts)
    try:
        root_resolved = packet_root.resolve(strict=True)
        candidate_resolved = candidate.resolve(strict=False)
        candidate_resolved.relative_to(root_resolved)
    except (FileNotFoundError, RuntimeError, ValueError, OSError) as exc:
        return None, f"path escapes or cannot be resolved beneath packet root: {exc}"
    return candidate, None


def enumerate_packet(packet_root: pathlib.Path) -> Tuple[Set[str], List[str]]:
    files: Set[str] = set()
    symlinks: List[str] = []
    if packet_root.is_symlink():
        symlinks.append(".")
        return files, symlinks
    for dirpath, dirnames, filenames in os.walk(packet_root, followlinks=False):
        base = pathlib.Path(dirpath)
        retained_dirs = []
        for name in dirnames:
            p = base / name
            rel = p.relative_to(packet_root).as_posix()
            if p.is_symlink():
                symlinks.append(rel)
            else:
                retained_dirs.append(name)
        dirnames[:] = retained_dirs
        for name in filenames:
            p = base / name
            rel = p.relative_to(packet_root).as_posix()
            if p.is_symlink():
                symlinks.append(rel)
            else:
                files.add(rel)
    return files, sorted(symlinks)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-root", default=DEFAULT_PACKET_ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    packet_root = pathlib.Path(args.packet_root)
    results: List[Dict[str, Any]] = []
    if not packet_root.exists() or not packet_root.is_dir():
        results.append(result("packet-root", False, f"missing or not a directory: {packet_root}"))
        summary = summarize(packet_root, results)
        print_summary(summary, args.json)
        return 1
    if packet_root.is_symlink():
        results.append(result("packet-root:symlink", False, "packet root must not be a symlink"))
    else:
        results.append(result("packet-root:symlink", True, "packet root is a real directory"))

    for rel in REQUIRED_PACKET_FILES:
        path = packet_root / rel
        ok = path.exists() and path.is_file() and not path.is_symlink()
        results.append(result(f"path:{rel}", ok, "present regular file" if ok else "missing, non-file, or symlink"))

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

    expected_inventory: Set[str] = set(PACKET_METADATA_FILES)
    if manifest:
        required_manifest_fields = [
            "manifest_schema_version", "trial_id", "packet_id", "created_at_fixed_fixture_time",
            "generated_from_base_commit", "canonicalization_method", "artifact_hashes",
            "expected_reconstruction_hash", "environment_manifest_hash",
            "non_authority_boundary_statement_hash", "non_authority_statement",
        ]
        missing = [field for field in required_manifest_fields if field not in manifest]
        results.append(result("manifest:required-fields", not missing, "missing: " + ", ".join(missing) if missing else "present"))
        missing_terms = has_boundary_terms(str(manifest.get("non_authority_statement", "")))
        results.append(result("manifest:non-authority-terms", not missing_terms, "missing: " + ", ".join(missing_terms) if missing_terms else "present"))

        artifacts = manifest.get("artifact_hashes", [])
        artifact_errors: List[str] = []
        path_errors: List[str] = []
        if not isinstance(artifacts, list) or not artifacts:
            artifact_errors.append("artifact_hashes must be non-empty array")
        else:
            for item in artifacts:
                if not isinstance(item, dict):
                    artifact_errors.append("artifact entry must be object")
                    continue
                path_text = item.get("path")
                expected_hash = item.get("sha256")
                if not isinstance(path_text, str) or not path_text:
                    path_errors.append("artifact path missing")
                    continue
                rel_path, rel_error = packet_relative_manifest_path(path_text)
                if rel_error or rel_path is None:
                    path_errors.append(f"{path_text}: {rel_error}")
                    continue
                expected_inventory.add(rel_path)
                if not isinstance(expected_hash, str) or not re.fullmatch(r"[a-f0-9]{64}", expected_hash):
                    artifact_errors.append(f"{path_text}: invalid sha256")
                    continue
                artifact_path, resolution_error = resolve_packet_file(packet_root, rel_path)
                if resolution_error or artifact_path is None:
                    path_errors.append(f"{path_text}: {resolution_error}")
                    continue
                if not artifact_path.exists() or not artifact_path.is_file():
                    artifact_errors.append(f"{path_text}: missing regular file beneath packet root")
                    continue
                actual_hash = sha256_file(artifact_path)
                if actual_hash != expected_hash:
                    artifact_errors.append(f"{path_text}: hash mismatch expected {expected_hash} actual {actual_hash}")
        results.append(result("manifest:artifact-paths", not path_errors, "; ".join(path_errors) if path_errors else "all artifact paths are packet-root-bound"))
        results.append(result("manifest:artifact-hashes", not artifact_errors, "; ".join(artifact_errors) if artifact_errors else "all packet-root-bound artifact hashes match"))

        expected_path = packet_root / "expected/day0_expected_reconstruction.json"
        env_path = packet_root / "environment/day0_environment_manifest.json"
        boundary_path = packet_root / "boundary/day0_non_authority_boundary_statement.txt"
        for name, path, expected_hash in [
            ("manifest:expected-reconstruction-hash", expected_path, manifest.get("expected_reconstruction_hash")),
            ("manifest:environment-manifest-hash", env_path, manifest.get("environment_manifest_hash")),
            ("manifest:non-authority-boundary-statement-hash", boundary_path, manifest.get("non_authority_boundary_statement_hash")),
        ]:
            if not path.exists() or not path.is_file() or path.is_symlink():
                results.append(result(name, False, f"missing, non-file, or symlink: {path}"))
            else:
                actual_hash = sha256_file(path)
                results.append(result(name, actual_hash == expected_hash, f"expected {expected_hash} actual {actual_hash}"))
        if boundary_path.exists() and boundary_path.is_file() and not boundary_path.is_symlink():
            missing_boundary_terms = has_boundary_terms(boundary_path.read_text(encoding="utf-8"))
            results.append(result("boundary-statement:non-authority-terms", not missing_boundary_terms, "missing: " + ", ".join(missing_boundary_terms) if missing_boundary_terms else "present"))

    actual_inventory, symlinks = enumerate_packet(packet_root)
    results.append(result("inventory:symlinks", not symlinks, "symlinks: " + ", ".join(symlinks) if symlinks else "none"))
    missing_inventory = sorted(expected_inventory - actual_inventory)
    unexpected_inventory = sorted(actual_inventory - expected_inventory)
    results.append(result("inventory:missing-files", not missing_inventory, "missing: " + ", ".join(missing_inventory) if missing_inventory else "none"))
    results.append(result("inventory:unexpected-files", not unexpected_inventory, "unexpected: " + ", ".join(unexpected_inventory) if unexpected_inventory else "none"))
    results.append(result("inventory:exact-set", not missing_inventory and not unexpected_inventory and not symlinks, "actual packet file set equals declared file set" if not missing_inventory and not unexpected_inventory and not symlinks else "packet inventory differs from declared set"))

    if manifest_path.exists() and manifest_sha_path.exists() and not manifest_path.is_symlink() and not manifest_sha_path.is_symlink():
        actual_manifest_hash = sha256_file(manifest_path)
        sidecar_text = manifest_sha_path.read_text(encoding="utf-8").strip().lower()
        sidecar_ok = actual_manifest_hash in sidecar_text and "packet_manifest.json" in sidecar_text
        results.append(result("manifest-sidecar:sha256", sidecar_ok, f"actual manifest hash {actual_manifest_hash}"))
    else:
        actual_manifest_hash = ""
        results.append(result("manifest-sidecar:sha256", False, "manifest or sidecar missing/symlinked"))
    if outer:
        outer_hash = str(outer.get("packet_manifest_sha256", "")).lower()
        results.append(result("outer-receipt:manifest-hash-binding", bool(actual_manifest_hash) and outer_hash == actual_manifest_hash, f"outer {outer_hash} actual {actual_manifest_hash}"))
        missing_outer_terms = has_boundary_terms(str(outer.get("non_authority_statement", "")))
        results.append(result("outer-receipt:non-authority-terms", not missing_outer_terms, "missing: " + ", ".join(missing_outer_terms) if missing_outer_terms else "present"))

    summary = summarize(packet_root, results)
    print_summary(summary, args.json)
    return 0 if summary["failed"] == 0 else 1


def summarize(packet_root: pathlib.Path, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed = sum(1 for item in results if not item["passed"])
    return {
        "checker": "check_longitudinal_reconstruction_day0_packet_v0_1_1.py",
        "checker_version": "0.1.1",
        "packet_root": str(packet_root).replace("\\", "/"),
        "total": len(results), "passed": len(results) - failed, "failed": failed,
        "results": results,
        "invariants": ["PACKET_ROOT_CONTROLS_ARTIFACT_RESOLUTION", "ACTUAL_PACKET_FILE_SET_EQUALS_DECLARED_FILE_SET"],
        "non_authority_statement": (
            "This checker verifies bounded Day-0 packet structure, packet-root-bound hashes, exact inventory, and boundary-statement presence only; it does not validate truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, procurement approval, or institutional authority."
        ),
    }


def print_summary(summary: Dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    print(f"Longitudinal Day-0 packet v0.1.1: {summary['passed']}/{summary['total']} passed")
    for item in summary["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(f"{status} {item['name']}")
        if not item["passed"] and item["detail"]:
            print(f"  - {item['detail']}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
