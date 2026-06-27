# ESAL Reproduction Vector Bundle Report v0.1

**Document ID:** `ESAL_REPRODUCTION_VECTOR_BUNDLE_REPORT_v0_1`
**Status:** Draft v0.1
**Intended path:** `reports/ESAL_REPRODUCTION_VECTOR_BUNDLE_REPORT_v0_1.md`
**Primary bundle:** `esal-tests/reproduction/manifest_v0_1.json`
**Primary spec:** `spec/BDR-ESAL-v0.1.md`
**Profile:** `BDR_ESAL_BASELINE_REPLAY_v0_1`
**Boundary posture:** Preservation without inheritance.

---

## 1. Purpose

This report records generation of the ESAL Reproduction Vector Bundle v0.1.

The bundle converts the prior reproduction-readiness documentation into a concrete first-party corpus of replay inputs, expected outputs, fingerprints, failure expectations, manifest metadata, and generation receipt.

---

## 2. Generated artifact set

The bundle adds:

```text
esal-tests/reproduction/
  positive/
  adversarial/
  malformed/
  expected/
  fingerprints/
  failures/
  receipts/
  manifest_v0_1.json
  README_v0_1.md
```

It also adds this report:

```text
reports/ESAL_REPRODUCTION_VECTOR_BUNDLE_REPORT_v0_1.md
```

---

## 3. Expected-output coverage

The bundle includes state-output vectors for:

- basic replay
- constraint accumulation
- obligation accumulation
- validity false / violation preservation
- authority inflation recorded

For each state-output vector, the bundle preserves a SHA-256 fingerprint record.

---

## 4. Failure-expectation coverage

The bundle includes failure-expectation vectors for:

- lineage truncation
- event reordering failure or gap
- malformed event failure

For each failure vector, the bundle preserves an expected failure record.

If a failure code cannot be extracted directly from the expected failure artifact, the generated failure expectation record marks the code status as review-required rather than silently inventing a failure class.

---

## 5. Generation boundary

This is a first-party bundle generated from branch-visible ESAL vectors and expected outputs.

It does not claim:

- independent reproduction
- second implementation execution
- legal sufficiency
- regulatory compliance
- audit acceptance
- safety
- truth
- approval
- runtime authorization
- external endorsement
- host-system conformance

---

## 6. Result

Current result:

```text
ESAL_REPRODUCTION_VECTOR_BUNDLE_GENERATED
```

Next target:

```text
ESAL_REPRODUCTION_VECTOR_BUNDLE_REVIEWED
```

Final independent-reproduction target:

```text
INDEPENDENT_REPRODUCTION_ESTABLISHED_WITH_LIMITATIONS
```

---

## 7. Remaining gaps

The bundle intentionally preserves the following open gaps:

| Gap token | Meaning |
|---|---|
| `INDEPENDENT_REPRODUCTION_NOT_ESTABLISHED` | No second implementation has reproduced the bundle yet |
| `EVENT_REORDERING_INVARIANCE_VECTOR_REVIEW_REQUIRED` | The current branch-visible event-reordering vector is represented as an expected failure; a dedicated positive invariance-pair vector may still be needed |
| `REFERENCE_IMPLEMENTATION_EXECUTION_NOT_RECORDED_HERE` | This bundle binds expected artifacts and fingerprints but does not record a fresh replay run |

---

## 8. Summary

The reproduction-readiness packet defined what an independent evaluator would need.

This bundle begins supplying it.

The next step is either:

1. Review and harden the generated bundle, or
2. Ask a second implementation to reproduce it and preserve the result as an independent execution artifact.
