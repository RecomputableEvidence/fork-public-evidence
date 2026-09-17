#!/usr/bin/env python3
"""Verify the bounded Lens Shift Protocol v0.1 Blind Epoch 003 repository admission."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

EXPECTED_EXTERNAL = {
    "BLIND_EPOCH_003_FROZEN_REVIEWER_PACKAGE_ZIP": "c25f708943fb50aabb312afee1e1cbda583005de573aea81c4bdde1575a46347",
    "BLIND_EPOCH_003_FREEZE_MANIFEST": "6ef956be2da1d48a21d9b14ea68fd5fc3c819e803360f8bfef2654fd3a476ba0",
    "BLIND_EPOCH_003_FIXTURES": "1ce848f415bf1614508e6809d86d7866e01cc63378b13fbe72916507a55b85f7",
    "EPOCH_002_REVIEWER_ZIP": "b64bbed62d51f8cb10db032e53152bd5b5baa7b10a167c9f9c566f7e70bbc6e6",
    "HARNESS_v0_1_2_REVIEWER_CANDIDATE_ZIP": "20cca9aad3eb524eecc37a81c88086e3aa598c629cb963b15b4ab2151a0153a6",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    sums = {}
    for line in (HERE / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        sums[name] = digest
    for name, digest in sums.items():
        path = HERE / name
        if not path.is_file():
            fail(f"missing admitted native record: {name}")
        actual = sha256(path)
        if actual != digest:
            fail(f"sha256 mismatch for {name}: {actual} != {digest}")

    first = read_jsonl(HERE / "FIRST_EXECUTION_RESULT.jsonl")
    oracle = read_jsonl(HERE / "ORACLE_COMPARISON.jsonl")
    if len(first) != 24 or len({r["id"] for r in first}) != 24:
        fail("first execution must contain 24 unique fixture IDs")
    if Counter(r["verdict"] for r in first) != Counter({"CONFORMS": 12, "DOES_NOT_CONFORM": 12}):
        fail("first execution verdict split must be 12 CONFORMS / 12 DOES_NOT_CONFORM")
    if len(oracle) != 24 or len({r["id"] for r in oracle}) != 24:
        fail("oracle comparison must contain 24 unique fixture IDs")
    if [r["id"] for r in first] != [r["id"] for r in oracle]:
        fail("first execution and oracle comparison ID order differs")
    if any(a["verdict"] != b["actual_verdict"] for a, b in zip(first, oracle)):
        fail("oracle actual_verdict does not preserve first execution")
    if sum(bool(r["match"]) for r in oracle) != 24:
        fail("oracle comparison is not 24/24")
    if any(r["actual_verdict"] != r["expected_verdict"] for r in oracle):
        fail("oracle comparison contains a verdict mismatch")

    closure = json.loads((HERE / "BLIND-EPOCH-003-CLOSURE-VERIFICATION.json").read_text(encoding="utf-8"))
    standing = closure["standing"]
    if standing["protocol_v0_1"] != "QUALIFIED_WITHIN_BLIND_EPOCH_003_DECLARED_24_PROBE_SCOPE":
        fail("unexpected protocol standing")
    if standing["semantic_repair_warranted"] is not False:
        fail("semantic repair must remain not warranted")
    if closure["historical_preservation"]["epoch_002_unchanged"] is not True:
        fail("Epoch 002 historical preservation not asserted")
    if closure["historical_preservation"]["harness_v0_1_2_unchanged"] is not True:
        fail("harness v0.1.2 historical preservation not asserted")

    candidate = json.loads((HERE / "LENS-SHIFT-v0.1-BLIND-EPOCH-003-REPOSITORY-ADMISSION-CANDIDATE-001.json").read_text(encoding="utf-8"))
    if candidate["hash_bound_not_byte_admitted"] != EXPECTED_EXTERNAL:
        fail("external hash-bound lineage changed")
    if candidate["semantic_repair_warranted"] is not False:
        fail("candidate improperly warrants protocol semantic repair")

    print("PASS: Lens Shift v0.1 Blind Epoch 003 bounded repository admission verified")
    print("24/24 oracle matches; 12 CONFORMS; 12 DOES_NOT_CONFORM")
    print("historical Epoch 002 preserved; harness v0.1.2 preserved; semantic repair not warranted")


if __name__ == "__main__":
    main()
