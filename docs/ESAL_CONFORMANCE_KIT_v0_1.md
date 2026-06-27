# ESAL Conformance Kit v0.1

**Artifact ID:** ESAL-CONFORMANCE-KIT-v0.1-001  
**Release candidate tag:** `esal-v0.1-rc6`  
**Release candidate tag commit:** `1a99d32a305dd9f295b794c0e95bcd61c2af183d`  
**Reviewed ESAL subject commit:** `859d2abe3db324970f0d3af4faffafd22f221b28`  

---

## 1. Purpose

This document defines the ESAL v0.1 reference conformance surface.

The goal is to allow another implementation or reviewer to compare replay behavior against the ESAL v0.1 reference oracle.

This is a conformance surface for replay comparison. It is not evidence of independent implementation convergence until at least one independent implementation reproduces the expected outputs.

---

## 2. Required Repository Surface

A conforming ESAL v0.1 replay comparison should use:

- `reference/esal/`  
- `esal-tests/`  
- `tools/esal_verify.ps1`  
- `tools/Test-EsalPermutationInvariance.ps1`  
- `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`

---

## 3. Reproduction Commands

From the repository root:

```text
git checkout esal-v0.1-rc6
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
```

---

## 4. Expected Classification Distribution

```text
PASS: 4
G:    3
S:    2
D:    1
```

The classification labels are oracle-internal replay classifications:

- PASS: structurally valid and valid under ESAL v0.1 oracle rules.  
- G: governance-class failure or governance-invalid replayable state.  
- S: structural/substrate-class failure.  
- D: determinism-class failure.  

These labels do not establish external validity, legal sufficiency, compliance sufficiency, authorization correctness, approval, or endorsement.

---

## 5. Expected Fixture-Level Outputs

| Corpus group | Log                           | Class | Fingerprint                      | Exception / note                                           |
|--------------|------------------------------|-------|----------------------------------|-----------------------------------------------------------|
| adversarial  | log2-constraints-tighten.jsonl | G   | None                             | GovernanceError: authority inflation (translate)          |
| adversarial  | log4-constraint-violation.jsonl | G   | bee2ca4f6ef180c915ea84c1aad8fb68f1229fa549585103197f499889736e44 | Replayable governance-invalid state                    |
| adversarial  | log5-authority-inflation.jsonl | G   | None                             | GovernanceError: authority inflation (write:data)         |
| adversarial  | log6-lineage-truncation.jsonl | S   | None                             | StructuralError: unknown parent_bdr_id                    |
| adversarial  | log7-event-reordering.jsonl  | D   | None                             | DeterminismError: event_id conflict                       |
| canonical    | C-001-placeholder.jsonl      | PASS | 39fde2d6cb76d9409fdf09cb5e76ab2ba8b7174b430cb19c455038f2ded37bb1      | Minimal passing fixture                                   |
| canonical    | log1-basic-A-B-C.jsonl       | PASS | 6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836         | Canonical baseline trace                                  |
| canonical    | log2-constraints-tighten.jsonl | PASS | 50b3d57de240108c39ab25be712114f6efb9ef0903fe1661a931e99fe4fc8393 | Valid constraint tightening trace                      |
| canonical    | log3-obligations-accumulate.jsonl | PASS | 95659c757320ac0c0db79154e4f7d06cd9db0284cf2d2413d421c238ccdaf5bb | Valid obligation accumulation trace                |
| malformed    | log8-schema-invalid.jsonl    | S   | None                             | StructuralError: missing event_id                         |

---

## 6. Expected Permutation-Invariance Output

Permutation-invariance target:

```text
esal-tests\canonical\log1-basic-A-B-C.jsonl
```

Expected result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

Expected fingerprint:

```text
6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836
```

Expected canonical events hash:

```text
a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878
```

---

## 7. Expected Fingerprint Availability

Fingerprint availability is part of the conformance surface.

Expected behavior:

- PASS traces produce fingerprints.  
- Replayable governance-invalid G traces may produce fingerprints.  
- Halted G traces do not produce fingerprints.  
- S traces do not produce fingerprints.  
- D traces do not produce fingerprints.  

This is ESAL v0.1 reference-oracle behavior, not a general rule for future ESAL versions.

---

## 8. Platform and Dependency Constraints

A conformance replay should not depend on:

- network calls  
- wall-clock time  
- random sources  
- environment-specific ordering  
- external policy engines  
- external authorization systems  
- external legal/compliance determinations  

Expected behavior should be reproducible from the repository contents at the release-candidate tag.

---

## 9. Correct and Incorrect Claims

Correct claim:

> ESAL v0.1 provides a reference conformance surface for independent replay comparison.

Incorrect claim:

> ESAL v0.1 proves independent implementation convergence.

Independent implementation convergence is not established until at least one independently implemented oracle reproduces the expected canonical event hashes, reduced states, fingerprints, classifications, and exception classes over the same corpus.

---

## 10. Non-Claims

This conformance kit does not establish production completeness, legal sufficiency, compliance sufficiency, authorization correctness, external governance validity, safety, truth, approval, endorsement, or independent implementation convergence.

This list is illustrative, not exhaustive.
