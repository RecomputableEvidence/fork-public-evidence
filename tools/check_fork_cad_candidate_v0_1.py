#!/usr/bin/env python3
"""Bounded structural checker for the Fork CAD candidate v0.1."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class CandidateError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateError(f"{path}: cannot load JSON: {exc}") from exc


def validate_manifest(manifest: dict[str, Any]) -> set[str]:
    if manifest.get("status") != "CANDIDATE_NOT_ADMITTED":
        raise CandidateError("manifest status must be CANDIDATE_NOT_ADMITTED")
    if manifest.get("raw_sources_published") is not False:
        raise CandidateError("raw_sources_published must be false")
    if manifest.get("provider_calls_performed_by_candidate") != 0:
        raise CandidateError("provider call count must be zero")
    if manifest.get("pair_001_effect") != "NONE":
        raise CandidateError("Pair-001 effect must be NONE")

    ids: set[str] = set()
    for item in manifest.get("sources", []):
        source_id = item.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise CandidateError("every source requires source_id")
        if source_id in ids:
            raise CandidateError(f"duplicate source_id: {source_id}")
        ids.add(source_id)

        digest = item.get("sha256")
        if not isinstance(digest, str) or SHA256_RE.fullmatch(digest) is None:
            raise CandidateError(f"{source_id}: invalid SHA-256")
        if not isinstance(item.get("size_bytes"), int) or item["size_bytes"] <= 0:
            raise CandidateError(f"{source_id}: size_bytes must be positive")

    if not ids:
        raise CandidateError("manifest must contain sources")
    return ids


def validate_role_map(role_map: dict[str, Any], source_ids: set[str]) -> None:
    if role_map.get("status") != "CANDIDATE_NOT_ADMITTED":
        raise CandidateError("role map status must be CANDIDATE_NOT_ADMITTED")
    mapped: set[str] = set()
    for item in role_map.get("roles", []):
        source_id = item.get("source_id")
        if source_id not in source_ids:
            raise CandidateError(f"role map references unknown source: {source_id}")
        if source_id in mapped:
            raise CandidateError(f"duplicate role mapping: {source_id}")
        mapped.add(source_id)
        if not item.get("declared_role") or not item.get("role_basis"):
            raise CandidateError(f"{source_id}: declared_role and role_basis required")
    if mapped != source_ids:
        missing = sorted(source_ids - mapped)
        raise CandidateError(f"role map missing sources: {missing}")


def validate_ledger(ledger: dict[str, Any], source_ids: set[str]) -> None:
    if ledger.get("status") != "CANDIDATE_NOT_ADMITTED":
        raise CandidateError("ledger status must be CANDIDATE_NOT_ADMITTED")
    if ledger.get("candidate_classifications_are_canonical") is not False:
        raise CandidateError("candidate classifications must not be canonical")

    claim_ids: set[str] = set()
    for claim in ledger.get("claims", []):
        claim_id = claim.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id:
            raise CandidateError("every claim requires claim_id")
        if claim_id in claim_ids:
            raise CandidateError(f"duplicate claim_id: {claim_id}")
        claim_ids.add(claim_id)
        refs = claim.get("source_refs")
        if not isinstance(refs, list) or not refs:
            raise CandidateError(f"{claim_id}: source_refs required")
        unknown = sorted(set(refs) - source_ids)
        if unknown:
            raise CandidateError(f"{claim_id}: unknown source refs: {unknown}")
        if not claim.get("current_disposition"):
            raise CandidateError(f"{claim_id}: current_disposition required")
        if not claim.get("basis"):
            raise CandidateError(f"{claim_id}: basis required")

    if not claim_ids:
        raise CandidateError("ledger must contain claims")
    if not ledger.get("case_non_claims"):
        raise CandidateError("ledger must preserve case_non_claims")


def validate_candidate(root: Path) -> None:
    case_dir = root / "docs/meta-evidence/conversational-authority-drift-v0.1/cases/CAD_004_CLAUDE_SOURCE_ROLE_BINDING"
    manifest = load_json(case_dir / "SOURCE_MANIFEST_v0_1.json")
    role_map = load_json(case_dir / "SOURCE_ROLE_MAP_v0_1.json")
    ledger = load_json(case_dir / "CLAIM_LEDGER_v0_1.json")

    source_ids = validate_manifest(manifest)
    validate_role_map(role_map, source_ids)
    validate_ledger(ledger, source_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        validate_candidate(args.root)
    except CandidateError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: Fork CAD candidate v0.1 structural checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
