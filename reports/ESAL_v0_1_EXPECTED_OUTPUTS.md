# ESAL v0.1 Expected Outputs

**Artifact ID:** ESAL-EXPECTED-OUTPUTS-v0.1-001  
**Release candidate tag:** `esal-v0.1-rc6`  
**Release candidate tag commit:** `1a99d32a305dd9f295b794c0e95bcd61c2af183d`  

---

## 1. Purpose

This document records the expected ESAL v0.1 reference-oracle outputs for the current conformance corpus.

These outputs support replay comparison. They do not establish external validity, production sufficiency, legal sufficiency, compliance sufficiency, authorization correctness, approval, endorsement, or independent implementation convergence.

---

## 2. Expected Distribution

```text
PASS: 4
G:    3
S:    2
D:    1
```

---

## 3. Fixture-Level Expected Outputs

| #  | Corpus group | Log                           | Class | Fingerprint present | Fingerprint                      | Exception class   | Expected message / note                                       |
|----|--------------|------------------------------|-------|---------------------|----------------------------------|-------------------|----------------------------------------------------------------|
| 1  | adversarial  | log2-constraints-tighten.jsonl | G   | no                  | None                             | GovernanceError   | authority inflation without explicit expansion delta: translate |
| 2  | adversarial  | log4-constraint-violation.jsonl | G   | yes                 | bee2ca4f6ef180c915ea84c1aad8fb68f1229fa549585103197f499889736e44 | none          | replayable governance-invalid state                           |
| 3  | adversarial  | log5-authority-inflation.jsonl | G   | no                  | None                             | GovernanceError   | authority inflation without explicit expansion delta: write:data |
| 4  | adversarial  | log6-lineage-truncation.jsonl | S   | no                  | None                             | StructuralError   | unknown parent_bdr_id: bdr-missing-000                        |
| 5  | adversarial  | log7-event-reordering.jsonl  | D   | no                  | None                             | DeterminismError | event_id conflict with differing event content                 |
| 6  | canonical    | C-001-placeholder.jsonl      | PASS | yes                 | 39fde2d6cb76d9409fdf09cb5e76ab2ba8b7174b430cb19c455038f2ded37bb1      | none              | minimal passing fixture                                        |
| 7  | canonical    | log1-basic-A-B-C.jsonl       | PASS | yes                 | 6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836         | none              | canonical baseline trace                                       |
| 8  | canonical    | log2-constraints-tighten.jsonl | PASS | yes               | 50b3d57de240108c39ab25be712114f6efb9ef0903fe1661a931e99fe4fc8393 | none          | valid constraint tightening trace                             |
| 9  | canonical    | log3-obligations-accumulate.jsonl | PASS | yes           | 95659c757320ac0c0db79154e4f7d06cd9db0284cf2d2413d421c238ccdaf5bb | none      | valid obligation accumulation trace                           |
| 10 | malformed    | log8-schema-invalid.jsonl    | S   | no                  | None                             | StructuralError   | missing event_id                                               |

---

## 4. Baseline Permutation-Invariance Expected Output

Target log:

```text
esal-tests\canonical\log1-basic-A-B-C.jsonl
```

Expected classification:

```text
PASS
```

Expected fingerprint:

```text
6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836
```

Expected canonical events hash:

```text
a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878
```

Expected run result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

---

## 5. Expected Classification Meanings

- PASS means the trace replayed successfully under ESAL v0.1 reference-oracle rules.  
- G means governance-class failure or governance-invalid replayable state under ESAL v0.1 reference-oracle rules.  
- S means structural/substrate-class failure.  
- D means determinism-class failure.  

These classifications do not constitute external legal, compliance, authorization, approval, safety, truth, or governance-validity determinations.

---

## 6. Non-Claims

This expected-output record does not establish independent implementation convergence.

It provides a reference comparison surface. Convergence requires at least one independent implementation to reproduce the expected outputs over the same corpus.

This record also does not establish production completeness, legal sufficiency, compliance sufficiency, authorization correctness, external governance validity, endorsement, approval, policy adequacy, safety, or truth.

This list is illustrative, not exhaustive.
