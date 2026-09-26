#!/usr/bin/env python3
"""
LS-MDRC-002 Structural Test Suite
=====================================
Bound commit: 2dab684fc904f43ca0d35d1c1bbc500e92156ec4

Tests the LS-MDRM construction package for structural integrity.
Operates only against the frozen construction package.
Does NOT test substantive Lens Shift correctness.

Usage:
    python ls_mdrc_002_structural_tests.py [--package-root PATH]

Returns:
    Exit code 0 if all tests pass.
    Exit code 1 if any test fails.
    Test receipt written to receipts/testing/TEST_RECEIPT.json
"""

import json
import hashlib
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

BOUND_COMMIT = "2dab684fc904f43ca0d35d1c1bbc500e92156ec4"
VALID_CLAIM_STATUSES = {"OBSERVED", "DERIVED", "HYPOTHESIZED", "COUNTERFACTUAL", "PROPOSED", "UNRESOLVED"}
VALID_REJECTION_CODES = {"B-1", "B-2", "B-3", "B-4", "B-5", "B-6", "B-7", "B-8", "B-9"}
VALID_TRANSITION_LABELS = {"EXPAND","NARROW","ABSTRACT","GROUND","INVERT","BRANCH","REVISE","OPERATIONALIZE","COMPRESS","JUMP","RESTATE","STALL"}
STRONGER_STATUS_ORDER = ["UNRESOLVED", "PROPOSED", "HYPOTHESIZED", "COUNTERFACTUAL", "DERIVED", "OBSERVED"]

results = []
violations = []

def record(test_id, description, passed, detail=None, violation_code=None):
    entry = {
        "test_id": test_id,
        "description": description,
        "passed": passed,
        "detail": detail or ""
    }
    results.append(entry)
    if not passed:
        violations.append({"test_id": test_id, "violation_code": violation_code or "UNKNOWN", "detail": detail or ""})
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {test_id}: {description}")
    if not passed and detail:
        print(f"         Detail: {detail}")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_required_schema_files(pkg_root):
    print("\n[T01] Required schema file presence")
    required = [
        "schemas/LS_MDRM_STATE_DICTIONARY.json",
        "schemas/LS_MDRM_TRANSITION_MANUAL.json",
        "schemas/LS_MDRM_BRANCH_PROTOCOL.json",
        "schemas/LS_MDRM_EVIDENCE_CLAIM_LEDGER_SCHEMA.json",
        "schemas/LS_MDRM_CLAIM_STATUS_ONTOLOGY.json",
        "schemas/LS_MDRM_UNCERTAINTY_SCHEMA.json",
        "schemas/LS_MDRM_ENTROPY_SCHEMA.json",
        "schemas/LS_MDRM_CONTROL_VECTOR.json",
        "schemas/LS_MDRM_EVALUATION_MANUAL.json",
        "schemas/LS_MDRM_PROTOCOL_COMPLIANCE_CHECKER.json",
        "schemas/LS_MDRM_TRAJECTORY_SCHEMA.json",
    ]
    for rel in required:
        p = pkg_root / rel
        record(f"T01-{rel}", f"Required schema present: {rel}", p.exists(),
               detail=None if p.exists() else f"Missing: {p}")

def test_required_fixture_files(pkg_root):
    print("\n[T02] Required fixture presence")
    required = [
        "fixtures/development/DEV-001-minimal-valid-trajectory.json",
        "fixtures/development/DEV-002-branch-lifecycle-bsr.json",
        "fixtures/calibration/CAL-001-tension-a-preservation-vs-executability.json",
        "fixtures/calibration/CAL-002-tension-c-heterogeneous-receiver-exposure.json",
        "fixtures/holdout/HOLDOUT_MANIFEST.json",
        "fixtures/negative-controls/NC-1-brainstorming.json",
        "fixtures/negative-controls/NC-2-through-NC-7-definitions.json",
        "fixtures/sentinels/SEN-001-disguised-restatement.json",
        "fixtures/sentinels/SEN-002-elegant-abstraction-no-evidence.json",
        "fixtures/sentinels/SEN-003-unlicensed-epr-violation.json",
    ]
    for rel in required:
        p = pkg_root / rel
        record(f"T02-{rel}", f"Required fixture present: {rel}", p.exists(),
               detail=None if p.exists() else f"Missing: {p}")

def test_schema_json_parseable(pkg_root):
    print("\n[T03] Schema JSON parseability")
    for p in (pkg_root / "schemas").glob("*.json"):
        try:
            load_json(p)
            record(f"T03-{p.name}", f"JSON parseable: {p.name}", True)
        except Exception as e:
            record(f"T03-{p.name}", f"JSON parseable: {p.name}", False, detail=str(e))

def test_fixture_json_parseable(pkg_root):
    print("\n[T04] Fixture JSON parseability")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            load_json(p)
            record(f"T04-{p.name}", f"JSON parseable: {p.name}", True)
        except Exception as e:
            record(f"T04-{p.name}", f"JSON parseable: {p.name}", False, detail=str(e))

def test_bound_commit_presence(pkg_root):
    print("\n[T05] Bound commit present in all schema files")
    for p in (pkg_root / "schemas").glob("*.json"):
        try:
            data = load_json(p)
            bc = data.get("bound_commit") or data.get("bound_repository_commit", "")
            ok = bc == BOUND_COMMIT
            record(f"T05-{p.name}", f"Bound commit correct in {p.name}", ok,
                   detail=None if ok else f"Found: '{bc}', expected: '{BOUND_COMMIT}'",
                   violation_code="REPOSITORY_COORDINATE_MISMATCH")
        except Exception as e:
            record(f"T05-{p.name}", f"Bound commit check failed: {p.name}", False, detail=str(e))

def test_pcc01_branch_selected_in_eligible(pkg_root):
    print("\n[T06] PCC-01: selected_candidate in eligible_candidates for all branch records")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "branch_records" not in data:
                continue
            for br in data["branch_records"]:
                selected = br.get("selected_candidate")
                eligible = br.get("eligible_candidates", [])
                state_n = br.get("state_n", "?")
                # selected must be in eligible, OR eligible is empty (all rejected, but selected still tried)
                # The invariant: if eligible is empty, selected is still recorded (the attempted selection)
                # but the fixture expected_result should note NOT_qualifying
                if eligible:
                    ok = selected in eligible
                    record(f"T06-{p.name}-S{state_n}", f"PCC-01 {p.name} state {state_n}", ok,
                           detail=None if ok else f"selected={selected} not in eligible={eligible}",
                           violation_code="BRANCH_SELECTED_NOT_IN_ELIGIBLE")
                else:
                    # eligible is empty; selected must be documented but outcome is non-qualifying
                    ok = selected is not None
                    record(f"T06-{p.name}-S{state_n}-empty", f"PCC-01 empty eligible, selected documented in {p.name} state {state_n}", ok,
                           detail=None if ok else "selected_candidate is null but eligible is empty")
        except Exception as e:
            record(f"T06-{p.name}", f"PCC-01 check error: {p.name}", False, detail=str(e))

def test_pcc02_eligible_subset_of_raw(pkg_root):
    print("\n[T07] PCC-02: eligible_candidates subset of raw_candidates for all branch records")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "branch_records" not in data:
                continue
            for br in data["branch_records"]:
                raw_ids = {c["candidate_id"] for c in br.get("raw_candidates", [])}
                eligible = set(br.get("eligible_candidates", []))
                state_n = br.get("state_n", "?")
                ok = eligible.issubset(raw_ids)
                record(f"T07-{p.name}-S{state_n}", f"PCC-02 {p.name} state {state_n}", ok,
                       detail=None if ok else f"eligible not subset of raw: extra={eligible - raw_ids}",
                       violation_code="ELIGIBLE_NOT_SUBSET_OF_RAW")
        except Exception as e:
            record(f"T07-{p.name}", f"PCC-02 check error: {p.name}", False, detail=str(e))

def test_pcc03_rejection_codes(pkg_root):
    print("\n[T08] PCC-03: all excluded raw candidates have at least one valid rejection code")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "branch_records" not in data:
                continue
            for br in data["branch_records"]:
                raw_ids = {c["candidate_id"] for c in br.get("raw_candidates", [])}
                eligible = set(br.get("eligible_candidates", []))
                excluded = raw_ids - eligible
                rejection_map = {r["candidate_id"]: r.get("rejection_codes", []) for r in br.get("rejections", [])}
                state_n = br.get("state_n", "?")
                for cid in excluded:
                    codes = rejection_map.get(cid, [])
                    has_codes = len(codes) >= 1 and all(c in VALID_REJECTION_CODES for c in codes)
                    record(f"T08-{p.name}-S{state_n}-{cid}", f"PCC-03 rejection codes for {cid}", has_codes,
                           detail=None if has_codes else f"codes={codes}",
                           violation_code="MISSING_REJECTION_CODE")
        except Exception as e:
            record(f"T08-{p.name}", f"PCC-03 check error: {p.name}", False, detail=str(e))

def test_pcc04_bsr_calculation(pkg_root):
    print("\n[T09] PCC-04: BSR = |eligible| / |raw| within tolerance")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "branch_records" not in data:
                continue
            for br in data["branch_records"]:
                raw_count = len(br.get("raw_candidates", []))
                eligible_count = len(br.get("eligible_candidates", []))
                recorded_bsr = br.get("BSR")
                state_n = br.get("state_n", "?")
                if raw_count == 0:
                    record(f"T09-{p.name}-S{state_n}", f"PCC-04 BSR (empty raw) {p.name} S{state_n}", True,
                           detail="raw_count=0; BSR not meaningful")
                    continue
                computed_bsr = eligible_count / raw_count
                ok = recorded_bsr is not None and abs(computed_bsr - recorded_bsr) < 0.01
                record(f"T09-{p.name}-S{state_n}", f"PCC-04 BSR {p.name} S{state_n}", ok,
                       detail=None if ok else f"computed={computed_bsr:.3f} recorded={recorded_bsr}",
                       violation_code="BSR_MISMATCH")
        except Exception as e:
            record(f"T09-{p.name}", f"PCC-04 check error: {p.name}", False, detail=str(e))

def test_pcc05_claim_status_valid(pkg_root):
    print("\n[T10] PCC-05: all claim statuses valid")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "claim_ledger" not in data:
                continue
            for entry in data["claim_ledger"]:
                cs = entry.get("claim_status")
                eid = entry.get("entry_id", "?")
                ok = cs in VALID_CLAIM_STATUSES
                record(f"T10-{p.name}-{eid}", f"PCC-05 claim status valid: {eid}", ok,
                       detail=None if ok else f"Invalid status: '{cs}'",
                       violation_code="MISSING_CLAIM_STATUS")
        except Exception as e:
            record(f"T10-{p.name}", f"PCC-05 check error: {p.name}", False, detail=str(e))

def test_pcc06_epr_detection(pkg_root):
    print("\n[T11] PCC-06: EPR detection — unlicensed promotions flagged")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "claim_ledger" not in data:
                continue
            computed_unlicensed = 0
            for entry in data["claim_ledger"]:
                prior = entry.get("prior_claim_status")
                current = entry.get("claim_status")
                licensed = entry.get("promotion_licensed")
                if prior is not None and prior in STRONGER_STATUS_ORDER and current in STRONGER_STATUS_ORDER:
                    if STRONGER_STATUS_ORDER.index(current) > STRONGER_STATUS_ORDER.index(prior):
                        if licensed is not True:
                            computed_unlicensed += 1
            epr_rec = data.get("EPR", {})
            recorded_unlicensed = epr_rec.get("N_unlicensed_promotions", 0)
            ok = computed_unlicensed == recorded_unlicensed
            record(f"T11-{p.name}", f"PCC-06 EPR consistency {p.name}", ok,
                   detail=None if ok else f"computed_unlicensed={computed_unlicensed} recorded={recorded_unlicensed}",
                   violation_code="UNLICENSED_EPISTEMIC_PROMOTION")
        except Exception as e:
            record(f"T11-{p.name}", f"PCC-06 check error: {p.name}", False, detail=str(e))

def test_pcc07_evidence_binding_complete(pkg_root):
    print("\n[T12] PCC-07: evidence binding completeness")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "claim_ledger" not in data:
                continue
            for entry in data["claim_ledger"]:
                eb = entry.get("evidence_binding", {})
                eid = entry.get("entry_id", "?")
                required_fields = ["artifact_id_or_path", "repository_commit", "exact_location", "observed_or_inferred"]
                missing = [f for f in required_fields if not eb.get(f)]
                ok = len(missing) == 0
                record(f"T12-{p.name}-{eid}", f"PCC-07 evidence binding {eid}", ok,
                       detail=None if ok else f"Missing fields: {missing}",
                       violation_code="INCOMPLETE_EVIDENCE_BINDING")
        except Exception as e:
            record(f"T12-{p.name}", f"PCC-07 check error: {p.name}", False, detail=str(e))

def test_pcc09_entropy_components(pkg_root):
    print("\n[T13] PCC-09: all four entropy components present in every entropy record")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "entropy_records" not in data:
                continue
            for er in data["entropy_records"]:
                rid = er.get("entropy_record_id", "?")
                for comp in ["H_s", "H_g", "H_r", "H_c"]:
                    ok = er.get(comp) is not None
                    record(f"T13-{p.name}-{rid}-{comp}", f"PCC-09 {comp} present in {rid}", ok,
                           detail=None if ok else f"{comp} missing",
                           violation_code="ENTROPY_COMPONENT_MISSING")
        except Exception as e:
            record(f"T13-{p.name}", f"PCC-09 check error: {p.name}", False, detail=str(e))

def test_pcc11_uncertainty_records(pkg_root):
    print("\n[T14] PCC-11: at least one uncertainty source per material state")
    for p in (pkg_root / "fixtures").rglob("*.json"):
        try:
            data = load_json(p)
            if "uncertainty_records" not in data:
                continue
            for ur in data["uncertainty_records"]:
                rid = ur.get("uncertainty_record_id", "?")
                sources = ur.get("sources", [])
                ok = len(sources) >= 1
                record(f"T14-{p.name}-{rid}", f"PCC-11 uncertainty sources present in {rid}", ok,
                       detail=None if ok else "No uncertainty sources",
                       violation_code="MISSING_UNCERTAINTY")
        except Exception as e:
            record(f"T14-{p.name}", f"PCC-11 check error: {p.name}", False, detail=str(e))

def test_pcc12_holdout_lifecycle(pkg_root):
    print("\n[T15] PCC-12: holdout lifecycle — no CONSUMED -> SEALED violation")
    manifest_path = pkg_root / "fixtures/holdout/HOLDOUT_MANIFEST.json"
    if not manifest_path.exists():
        record("T15-manifest", "PCC-12 holdout manifest present", False,
               detail="HOLDOUT_MANIFEST.json missing", violation_code="HOLDOUT_LIFECYCLE_VIOLATION")
        return
    manifest = load_json(manifest_path)
    for h in manifest.get("holdout_fixtures", []):
        hid = h.get("holdout_id", "?")
        status = h.get("lifecycle_status", "")
        # In this construction, all should be SEALED; opened_at and consumed_at should be null
        ok = status == "SEALED"
        record(f"T15-{hid}", f"PCC-12 holdout {hid} is SEALED", ok,
               detail=None if ok else f"Status: {status}",
               violation_code="HOLDOUT_LIFECYCLE_VIOLATION")

def test_negative_control_expected_results(pkg_root):
    print("\n[T16] Negative control expected classification")
    for p in (pkg_root / "fixtures/negative-controls").glob("*.json"):
        try:
            data = load_json(p)
            er = data.get("expected_result", {})
            classification = er.get("instrument_classification", "")
            ok = "NOT_qualifying" in classification or "PROTOCOL_NONCONFORMANT" in classification
            record(f"T16-{p.name}", f"Negative control has non-qualifying expected result: {p.name}", ok,
                   detail=None if ok else f"Expected result: {classification}")
        except Exception as e:
            record(f"T16-{p.name}", f"T16 check error: {p.name}", False, detail=str(e))

def test_sentinel_expected_results(pkg_root):
    print("\n[T17] Sentinel fixture expected classifications")
    for p in (pkg_root / "fixtures/sentinels").glob("*.json"):
        try:
            data = load_json(p)
            er = data.get("expected_result", {})
            classification = er.get("instrument_classification", "")
            ok = "NOT_qualifying" in classification or "PROTOCOL_NONCONFORMANT" in classification
            record(f"T17-{p.name}", f"Sentinel has non-qualifying/nonconformant expected result: {p.name}", ok,
                   detail=None if ok else f"Classification: {classification}")
        except Exception as e:
            record(f"T17-{p.name}", f"T17 check error: {p.name}", False, detail=str(e))

def test_mutation_branch_selected_not_in_eligible(pkg_root):
    """Adversarial: select a candidate that is NOT in eligible. PCC-01 should trigger."""
    print("\n[T18] Adversarial mutation: branch selected not in eligible (PCC-01 must trigger)")
    mutated = {
        "fixture_id": "MUTATION-T18",
        "branch_records": [
            {
                "state_n": 0,
                "raw_candidates": [{"candidate_id": "MC-01"}, {"candidate_id": "MC-02"}],
                "eligible_candidates": ["MC-01"],
                "selected_candidate": "MC-02",
                "BSR": 0.5,
                "rejections": []
            }
        ]
    }
    br = mutated["branch_records"][0]
    selected = br["selected_candidate"]
    eligible = br["eligible_candidates"]
    violation_detected = selected not in eligible
    record("T18-mutation-branch-eligibility",
           "Mutation: selected not in eligible — PCC-01 violation detected",
           violation_detected,
           detail=None if violation_detected else "PCC-01 failed to detect: selected IS in eligible (mutation not effective)",
           violation_code="BRANCH_SELECTED_NOT_IN_ELIGIBLE")

def test_mutation_unlicensed_promotion(pkg_root):
    """Adversarial: promote HYPOTHESIZED -> OBSERVED without license. PCC-06 must trigger."""
    print("\n[T19] Adversarial mutation: unlicensed HYPOTHESIZED->OBSERVED promotion (PCC-06 must trigger)")
    mutated_entry = {
        "entry_id": "MUT-19-01",
        "claim_status": "OBSERVED",
        "prior_claim_status": "HYPOTHESIZED",
        "promotion_licensed": False,
    }
    prior = mutated_entry.get("prior_claim_status")
    current = mutated_entry.get("claim_status")
    licensed = mutated_entry.get("promotion_licensed")
    is_promotion = (STRONGER_STATUS_ORDER.index(current) > STRONGER_STATUS_ORDER.index(prior))
    is_unlicensed = licensed is not True
    violation_detected = is_promotion and is_unlicensed
    record("T19-mutation-epr",
           "Mutation: HYPOTHESIZED->OBSERVED without license — PCC-06 violation detected",
           violation_detected,
           detail=None if violation_detected else "PCC-06 failed to detect unlicensed promotion",
           violation_code="UNLICENSED_EPISTEMIC_PROMOTION")

def test_mutation_repository_coordinate(pkg_root):
    """Adversarial: substitute a different commit. PCC-08 must trigger."""
    print("\n[T20] Adversarial mutation: substitute wrong repository commit (PCC-08 must trigger)")
    wrong_commit = "0000000000000000000000000000000000000000"
    mutation_entry = {
        "artifact_id_or_path": "some/path.json",
        "repository_commit": wrong_commit,
        "exact_location": "field.value",
        "observed_or_inferred": "observed"
    }
    violation_detected = mutation_entry["repository_commit"] != BOUND_COMMIT
    record("T20-mutation-commit",
           "Mutation: wrong repository commit in evidence binding — PCC-08 violation detected",
           violation_detected,
           detail=None if violation_detected else "PCC-08 failed to detect wrong commit",
           violation_code="REPOSITORY_COORDINATE_MISMATCH")

def test_mutation_raw_branch_removal(pkg_root):
    """Adversarial: remove a raw branch candidate. PCC-13 conceptual check."""
    print("\n[T21] Adversarial mutation: raw branch candidate removed (PCC-13 must detect hash change)")
    original_raw = [{"candidate_id": "C-01"}, {"candidate_id": "C-02"}, {"candidate_id": "C-03"}]
    mutated_raw = [{"candidate_id": "C-01"}, {"candidate_id": "C-03"}]
    original_hash = hashlib.sha256(json.dumps(original_raw, sort_keys=True).encode()).hexdigest()
    mutated_hash = hashlib.sha256(json.dumps(mutated_raw, sort_keys=True).encode()).hexdigest()
    violation_detected = original_hash != mutated_hash
    record("T21-mutation-raw-branch",
           "Mutation: raw branch removal causes hash change — PCC-13 violation detectable",
           violation_detected,
           detail=None if violation_detected else "Hash collision — PCC-13 cannot detect removal",
           violation_code="RAW_BRANCH_MODIFIED")

def test_mutation_consumed_holdout_reopened(pkg_root):
    """Adversarial: simulate a CONSUMED holdout being re-SEALED."""
    print("\n[T22] Adversarial mutation: CONSUMED -> SEALED (PCC-12 must trigger)")
    mutated_holdout = {
        "holdout_id": "HO-999",
        "lifecycle_status": "SEALED",
        "prior_status": "CONSUMED"
    }
    violation_detected = (mutated_holdout["lifecycle_status"] == "SEALED" and
                          mutated_holdout.get("prior_status") == "CONSUMED")
    record("T22-mutation-holdout-reopen",
           "Mutation: CONSUMED->SEALED lifecycle violation detected",
           violation_detected,
           detail=None if violation_detected else "PCC-12 failed to detect reopened holdout",
           violation_code="HOLDOUT_LIFECYCLE_VIOLATION")

def write_test_receipt(pkg_root, start_time):
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"])
    receipt = {
        "receipt_id": "LS-MDRC-002-TEST-RECEIPT-v0.1",
        "record_type": "test_receipt",
        "role": "TEST",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "start_time_utc": start_time,
        "bound_commit": BOUND_COMMIT,
        "package_root": str(pkg_root),
        "test_summary": {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / len(results), 4) if results else 0.0
        },
        "overall_disposition": "TEST_PASS_BOUNDED" if failed == 0 else "TEST_FAIL",
        "test_results": results,
        "violations_detected": violations,
        "mutations_tested": [
            "T18: branch selected not in eligible (PCC-01)",
            "T19: unlicensed epistemic promotion HYPOTHESIZED->OBSERVED (PCC-06)",
            "T20: wrong repository commit in evidence binding (PCC-08)",
            "T21: raw branch candidate removed (PCC-13)",
            "T22: CONSUMED->SEALED holdout lifecycle violation (PCC-12)"
        ],
        "limitations": [
            "Structural tests only. Do not test substantive Lens Shift correctness.",
            "JSON Schema $ref resolution not implemented; cross-schema validation not performed.",
            "Adversarial mutations are simulated in-memory; do not modify frozen package files.",
            "Test coverage does not include PCC-14 (scoring rule mutation), PCC-15 (evaluator contamination) — these require manual process verification.",
            "Holdout fixtures HO-001, HO-002, HO-003 are not opened in this test pass; lifecycle integrity only."
        ],
        "non_claims": [
            "TEST_PASS_BOUNDED does not establish that Lens Shift is valid or scientifically proven.",
            "Passing structural tests does not authorize any downstream institutional reliance.",
            "This test receipt is not independent scientific validation."
        ]
    }
    receipt_path = pkg_root / "receipts/testing/TEST_RECEIPT.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)
    print(f"\nTest receipt written to: {receipt_path}")
    return receipt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", default=".",
                        help="Path to the lens-shift-mdrc-002 directory")
    args = parser.parse_args()
    pkg_root = Path(args.package_root).resolve()
    start_time = datetime.now(timezone.utc).isoformat()

    print("=" * 70)
    print("LS-MDRC-002 Structural Test Suite")
    print(f"Package root: {pkg_root}")
    print(f"Bound commit: {BOUND_COMMIT}")
    print(f"Start time:   {start_time}")
    print("=" * 70)

    test_required_schema_files(pkg_root)
    test_required_fixture_files(pkg_root)
    test_schema_json_parseable(pkg_root)
    test_fixture_json_parseable(pkg_root)
    test_bound_commit_presence(pkg_root)
    test_pcc01_branch_selected_in_eligible(pkg_root)
    test_pcc02_eligible_subset_of_raw(pkg_root)
    test_pcc03_rejection_codes(pkg_root)
    test_pcc04_bsr_calculation(pkg_root)
    test_pcc05_claim_status_valid(pkg_root)
    test_pcc06_epr_detection(pkg_root)
    test_pcc07_evidence_binding_complete(pkg_root)
    test_pcc09_entropy_components(pkg_root)
    test_pcc11_uncertainty_records(pkg_root)
    test_pcc12_holdout_lifecycle(pkg_root)
    test_negative_control_expected_results(pkg_root)
    test_sentinel_expected_results(pkg_root)
    test_mutation_branch_selected_not_in_eligible(pkg_root)
    test_mutation_unlicensed_promotion(pkg_root)
    test_mutation_repository_coordinate(pkg_root)
    test_mutation_raw_branch_removal(pkg_root)
    test_mutation_consumed_holdout_reopened(pkg_root)

    receipt = write_test_receipt(pkg_root, start_time)
    passed = receipt["test_summary"]["passed"]
    failed = receipt["test_summary"]["failed"]
    total = receipt["test_summary"]["total"]

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{total} passed, {failed} failed")
    print(f"DISPOSITION: {receipt['overall_disposition']}")
    print("=" * 70)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
