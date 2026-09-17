#!/usr/bin/env python3
"""Verify the bounded UEM v0.1 Epoch 010 CRII repository admission."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPOCH = "UEM-v0.1-CANONICAL-RESULT-IDENTITY-INTERCHANGE-PRESSURE-EPOCH-010"
EXPECTED_EXTERNAL = {'EPOCH_010_CLOSEOUT_ZIP': 'f93be72a7b6223633a88257435260f54d67c140f83505d9a16a3166473c3d8f5', 'ORIGINAL_EXECUTOR_HANDOFF_16_FIXTURE_CORPUS': 'b67538bb7f4ed5a128881350582825c6b40ddb08afa66bafb1c057691e348af8', 'VERIFIER_AUTHOR_HANDOFF_PACKAGE': 'dd9338841273756023d8963887ec73a32804d655f7d012ed38e4a7f1765f4eee', 'PRE_EXPOSURE_FREEZE_MANIFEST': '38fc4df4e75333055990819fac186f9ece2b36f32937efb4baeddf2cf4920af9', 'CLOSED_CRII_RULE_REGISTRY': '3910283db6012a16e0ca3652d03ace50a1c4d720690d0d49f26f744b70e9e27a', 'SEALED_EXPECTATIONS': '8e2873d848904fb8f33a7ff789c93ccd1bcf712c2ac2f61b27113acbab396931', 'VERIFIER_SOURCE': '7a2fdc4bd2e66091035394cddffb36bcadf7b518385a0648562c27b6883a972c', 'VERIFIER_TESTS': '44695581a0fc3946c48d6c39cd794ecf52ddc0551b953a73667ff356ddb91060', 'INDEPENDENT_REPRODUCTION_BINDING_ZIP': 'c1ce9b5655fae0907efb467f081125f800cdd2df3434439bb8eb292ab45370ac'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    executor = json.loads((HERE / "EXECUTOR_RESULTS.json").read_text(encoding="utf-8"))
    if executor.get("epoch") != EPOCH:
        fail("executor epoch identity drift")
    results = executor.get("results", [])
    ids = [r.get("fixture_id") for r in results]
    if len(results) != 16 or len(set(ids)) != 16:
        fail("executor results must contain 16 unique fixture IDs")
    if Counter(r.get("validation") for r in results) != Counter({"ACCEPT": 4, "REJECT": 12}):
        fail("executor validation split must be 4 ACCEPT / 12 REJECT")
    if any(r.get("violated_rule_ids") for r in results if r.get("validation") == "ACCEPT"):
        fail("observed ACCEPT rows must retain empty violation lists")

    receipt = json.loads((HERE / "REPRODUCED_VERIFICATION_RECEIPT.json").read_text(encoding="utf-8"))
    if receipt.get("epoch") != EPOCH or receipt.get("status") != "PASS":
        fail("reproduced receipt epoch/status drift")
    checks = receipt.get("fixture_checks", [])
    if len(checks) != 16 or len({r.get("fixture_id") for r in checks}) != 16:
        fail("receipt must contain 16 unique fixture checks")
    if [r["fixture_id"] for r in results] != [r["fixture_id"] for r in checks]:
        fail("executor/receipt fixture order differs")
    if any(a["validation"] != b["validation"] for a, b in zip(results, checks)):
        fail("executor/receipt validation differs")
    if receipt["binding"].get("executor_results_sha256") != sha256(HERE / "EXECUTOR_RESULTS.json"):
        fail("receipt does not bind exact admitted executor-result bytes")

    candidate = json.loads((HERE / "UEM-v0.1-EPOCH-010-CRII-REPOSITORY-ADMISSION-CANDIDATE-001.json").read_text(encoding="utf-8"))
    if candidate.get("disposition") != "BOUNDED_CANONICAL_RESULT_IDENTITY_INTERCHANGE_PASS":
        fail("candidate disposition drift")
    if candidate.get("hash_bound_not_byte_admitted") != EXPECTED_EXTERNAL:
        fail("external hash-bound lineage changed")

    bindings = json.loads((HERE / "UEM-v0.1-EPOCH-010-CRII-REPOSITORY-BYTE-BINDINGS-001.json").read_text(encoding="utf-8"))
    inv = bindings.get("verification_invariants", {})
    if inv.get("independent_executor_from_fixture_reproduction") != "NOT_ESTABLISHED_FROM_CLOSEOUT_ARCHIVE_ALONE":
        fail("executor-from-fixture independence boundary was promoted")
    if inv.get("trusted_timestamp_pre_exposure_proof") != "NOT_ESTABLISHED":
        fail("pre-exposure chronology boundary was promoted")

    print("PASS: UEM v0.1 Epoch 010 bounded CRII repository admission verified")
    print("16 unique fixtures; 4 ACCEPT; 12 REJECT; reproduced receipt status PASS")
    print("executor-from-fixtures independence and trusted-timestamp chronology remain not established")


if __name__ == "__main__":
    main()
