# ESAL Reproduction Vector Bundle v0.1

**Document ID:** `ESAL_REPRODUCTION_VECTOR_BUNDLE_v0_1`
**Status:** Draft v0.1
**Intended path:** `esal-tests/reproduction/README_v0_1.md`
**Primary spec:** `spec/BDR-ESAL-v0.1.md`
**Profile:** `BDR_ESAL_BASELINE_REPLAY_v0_1`
**Boundary posture:** Preservation without inheritance.

---

## 1. Purpose

This directory contains the first ESAL v0.1 reproduction vector bundle.

It packages branch-visible ESAL event logs, expected state artifacts, expected failure artifacts, SHA-256 fingerprint records, failure expectation records, a manifest, and a generation receipt for use by independent implementers or evaluators.

This bundle is a reproduction input corpus.

It is not an independent reproduction result.

---

## 2. Directory layout

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

---

## 3. Included vector classes

The bundle includes:

- basic replay
- constraint accumulation
- obligation accumulation
- validity false / violation preservation
- authority inflation recorded
- lineage truncation failure
- event reordering failure or gap
- malformed event failure

---

## 4. Fingerprint semantics

Successful replay vectors include fingerprint records under:

```text
esal-tests/reproduction/fingerprints/
```

Each fingerprint record preserves:

- vector ID
- input path
- expected state path
- input file SHA-256
- expected state file SHA-256
- canonical state SHA-256
- generation branch
- generation commit
- generation timestamp
- non-claims

The canonical state SHA-256 is computed from the expected state JSON after JSON canonicalization using sorted object keys and compact separators.

---

## 5. Failure expectation semantics

Failing vectors include expected failure records under:

```text
esal-tests/reproduction/failures/
```

Each failure expectation record preserves:

- vector ID
- input path
- expected failure path
- expected result
- expected error scope
- expected error code or review-required marker
- input file SHA-256
- expected failure file SHA-256
- generation branch
- generation commit
- generation timestamp
- non-claims

---

## 6. Reproduction use

A second implementation SHOULD:

1. Read `spec/BDR-ESAL-v0.1.md`.
2. Implement the baseline replay profile.
3. Run the vectors in this bundle.
4. Compare successful replay canonical states and fingerprints.
5. Compare failing replay error classes and failure scopes.
6. Record implementation provenance, command, environment, commit, result, mismatches, limitations, and non-claims.

---

## 7. Current boundary

This bundle establishes that a first-party reproduction corpus exists.

It does not establish that ESAL has been independently reproduced.

Independent reproduction requires a separate second-implementation execution artifact.

---

## 8. Non-claims

This bundle does not establish:

- Legal sufficiency.
- Regulatory compliance.
- Audit acceptance.
- Safety.
- Truth.
- Approval.
- Runtime authorization.
- External endorsement.
- Host-system conformance.
- Independent reproduction.
- Claim inheritance.

Preservation without inheritance remains the controlling rule.
