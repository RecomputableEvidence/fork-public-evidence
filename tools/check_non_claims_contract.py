#!/usr/bin/env python3
"""
Check Fork non-claims contract v0.1.

This checker validates a machine-readable non-claims contract and performs
a bounded public-surface scan for prohibited positive assertion patterns.

It does not perform legal review, compliance review, semantic proof,
or natural-language entailment.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT = Path("examples/vendor-risk/non_claims_contract.json")

TEXT_EXTENSIONS = {".md", ".txt"}

NEGATIVE_CONTEXT_MARKERS = [
    "does not",
    "do not",
    "not imply",
    "not establish",
    "not certify",
    "not approve",
    "not authorize",
    "non-claim",
    "non-claims",
    "prohibited",
    "doesn't",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing contract file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path}: {exc}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def iter_scan_files(scan_paths: list[str], contract_path: Path):
    excluded = {
        contract_path.resolve(),
        Path("schemas/non_claims_contract.schema.json").resolve(),
        Path("tools/check_non_claims_contract.py").resolve(),
    }

    for raw in scan_paths:
        root = Path(raw)
        if not root.exists():
            fail(f"Scan path does not exist: {root}")

        if root.is_file():
            candidates = [root]
        else:
            candidates = [p for p in root.rglob("*") if p.is_file()]

        for path in candidates:
            if path.resolve() in excluded:
                continue
            if ".git" in path.parts:
                continue
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            yield path


def line_is_negative_context(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in NEGATIVE_CONTEXT_MARKERS)


def main() -> int:
    contract_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CONTRACT
    contract = load_json(contract_path)

    for key in [
        "contract_id",
        "version",
        "scope",
        "invariant",
        "required_presence_files",
        "scan_paths",
        "non_claims",
    ]:
        require(key in contract, f"Missing required contract key: {key}")

    non_claims = contract["non_claims"]
    require(isinstance(non_claims, list) and non_claims, "non_claims must be a non-empty list")

    required_presence_files = contract["required_presence_files"]
    require(isinstance(required_presence_files, list), "required_presence_files must be a list")

    scan_paths = contract["scan_paths"]
    require(isinstance(scan_paths, list) and scan_paths, "scan_paths must be a non-empty list")

    ids_seen: set[str] = set()

    for item in non_claims:
        for key in ["id", "category", "statement", "positive_assertions_prohibited"]:
            require(key in item, f"Missing key {key} in non-claim item")

        non_claim_id = item["id"]
        require(non_claim_id not in ids_seen, f"Duplicate non-claim id: {non_claim_id}")
        ids_seen.add(non_claim_id)

        statement = item["statement"]
        require(statement.endswith("."), f"Non-claim statement must end with period: {non_claim_id}")

        for rel in required_presence_files:
            path = Path(rel)
            require(path.exists(), f"Required presence file missing: {path}")
            text = path.read_text(encoding="utf-8")
            require(
                statement in text,
                f"Required non-claim statement not found in {path}: {statement}",
            )

    violations: list[str] = []

    prohibited_patterns: list[tuple[str, str]] = []
    for item in non_claims:
        for pattern in item["positive_assertions_prohibited"]:
            prohibited_patterns.append((item["id"], pattern.lower()))

    for path in iter_scan_files(scan_paths, contract_path):
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            if line_is_negative_context(line):
                continue
            for non_claim_id, pattern in prohibited_patterns:
                if pattern in lowered:
                    violations.append(f"{path}:{lineno}: {non_claim_id}: {line}")

    if violations:
        print("Non-claims contract violations detected:")
        for violation in violations:
            print(f" - {violation}")
        return 1

    print("PASS: non-claims contract verified")
    print(f"Contract: {contract['contract_id']} v{contract['version']}")
    print(f"Non-claims checked: {len(non_claims)}")
    print(f"Required presence files: {len(required_presence_files)}")
    print(f"Scan paths: {len(scan_paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
