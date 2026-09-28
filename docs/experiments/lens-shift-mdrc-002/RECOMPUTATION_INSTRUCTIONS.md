# LS-MDRC-002 Recomputation Instructions

**Document:** RECOMPUTATION_INSTRUCTIONS.md  
**Version:** v0.1  
**Bound commit:** `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`  

---

## Purpose

These instructions allow a fresh context (Bob or any other system) to independently verify the LS-MDRC-002 construction package without access to the original constructor's reasoning.

Recomputation is **not** independent scientific validation. A second context obtaining the same result constitutes mechanical re-traversal of frozen evidence, not independent experimental confirmation.

---

## Required inputs (only these)

1. This instruction document
2. The frozen LS-MDRC-002 package (`docs/experiments/lens-shift-mdrc-002/`)
3. The normative specification (LS-MDRC-002 prompt §1–§24)
4. The source repository at the bound commit: `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`
5. Raw test evidence from the TEST RECEIPT

Do **not** rely on remembered construction intent. Do not access any repository state beyond the bound commit.

---

## Step 1: Verify repository coordinate

```bash
git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
cd fork-public-evidence
git checkout 2dab684fc904f43ca0d35d1c1bbc500e92156ec4
git rev-parse HEAD
# Must output: 2dab684fc904f43ca0d35d1c1bbc500e92156ec4
git status
# Must output: HEAD detached at 2dab684, nothing to commit
```

If the commit does not match, stop. Do not proceed with a different commit.

---

## Step 2: Verify package population

List all files in `docs/experiments/lens-shift-mdrc-002/` and compare against `SHA256SUMS`.

```bash
cd docs/experiments/lens-shift-mdrc-002
sha256sum -c SHA256SUMS
# All files should show: OK
```

If any file shows FAILED, record the mismatch and classify the affected result as `MISMATCH` or `ENVIRONMENT_DEPENDENT`.

---

## Step 3: Run structural tests

```bash
cd docs/experiments/lens-shift-mdrc-002
python ls_mdrc_002_structural_tests.py --package-root .
```

Compare output against `receipts/testing/TEST_RECEIPT.json`:
- Total test count must match
- Pass/fail counts must match
- Violation codes must match

Classify each item per the recomputation classification table (§22 of spec).

---

## Step 4: Verify schema JSON validity

For each file in `schemas/`:
- Confirm it is valid JSON
- Confirm `bound_commit` field equals `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`
- Confirm `$id` field matches the filename (without .json extension)

---

## Step 5: Verify branch lifecycle invariants

For each fixture in `fixtures/` that contains `branch_records`:
1. Verify `selected_candidate` is in `eligible_candidates` (or eligible is empty and non-qualifying result is expected)
2. Verify `eligible_candidates` is a subset of raw candidate IDs
3. Verify all excluded candidates have ≥1 rejection code from `{B-1..B-9}`
4. Verify `BSR = |eligible| / |raw|` within 0.001 tolerance

---

## Step 6: Verify EPR values

For each fixture with a `claim_ledger`:
1. Count transitions where `prior_claim_status` is not null and `claim_status` is stronger in the partial order
2. Count those where `promotion_licensed ≠ true`
3. Verify `EPR.N_unlicensed_promotions` equals this count

---

## Step 7: Verify entropy records

For each `entropy_record` in each fixture:
- Confirm all four components (H_s, H_g, H_r, H_c) are present and non-null
- Confirm delta values are computed correctly for n > 0: `delta_H_j = H_j(n) - H_j(n-1)`

---

## Step 8: Verify holdout lifecycle

Read `fixtures/holdout/HOLDOUT_MANIFEST.json`:
- All fixtures should have `lifecycle_status = SEALED`
- `opened_at` and `consumed_at` should be null
- No fixture should show `CONSUMED` status

If any holdout is not SEALED, record as `HOLDOUT_LIFECYCLE_VIOLATION`.

---

## Step 9: Verify negative control and sentinel expected results

For each fixture in `fixtures/negative-controls/` and `fixtures/sentinels/`:
- `expected_result.instrument_classification` should contain `NOT_qualifying` or `PROTOCOL_NONCONFORMANT`
- If it contains `qualifying_recursive_transition`, that is a structural defect

---

## Step 10: Verify adversarial mutation behavior

Run the test suite; it includes in-memory mutation tests T18–T22. Verify:
- T18: PCC-01 violation detected (selected not in eligible)
- T19: PCC-06 violation detected (unlicensed promotion)
- T20: PCC-08 violation detected (wrong commit)
- T21: PCC-13 violation detectable (hash change on raw branch removal)
- T22: PCC-12 violation detected (CONSUMED->SEALED)

---

## Recomputation classification table

| Category | Meaning |
|---|---|
| `MECHANICALLY_REPRODUCED` | Result independently recovered from frozen evidence; identical to receipt |
| `SEMANTICALLY_MATCHED` | Result equivalent in substance but not byte-identical |
| `PARTIAL` | Some elements match; others cannot be resolved |
| `MISMATCH` | Frozen evidence does not produce the claimed result |
| `AMBIGUOUS` | Result cannot be clearly classified as match or mismatch |
| `ENVIRONMENT_DEPENDENT` | Result depends on environment (Python version, OS, etc.) |
| `NOT_TESTED` | Not verified in this recomputation pass |

---

## Non-claims

- Recomputation does not constitute independent validation of Lens Shift.
- A matching result means the frozen package is internally consistent; it does not prove the specification is correct.
- Inability to reproduce is not a substantive failure of Lens Shift; it is a finding about the package.
- This instruction document does not authorize any institutional reliance on LS-MDRC-002 results.
