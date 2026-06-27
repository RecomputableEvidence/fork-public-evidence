# ESAL v0.1 â€” Start Here

**Release candidate tag:** `esal-v0.1-rc6`  
**Release candidate tag commit:** `1a99d32a305dd9f295b794c0e95bcd61c2af183d`  

This guide orients readers to the ESAL v0.1 reference-oracle release-candidate package.

---

## 1. What ESAL v0.1 Is

ESAL v0.1 is a reference oracle for replaying event-state traces under defined canonicalization and state-reduction rules.

It helps answer:

> Given this event log and these ESAL v0.1 rules, what reduced state, fingerprint, and oracle classification result?

It does **not** answer:

> Was the underlying action legally sufficient, compliant, approved, safe, true, authorized in the world, or externally governance-valid?

---

## 2. Where to Start

Recommended reading order:

1. `reports/ESAL_v0_1_RELEASE_GATE.md`  
   - Records the release-gate determination and non-claims.  
2. `reports/ESAL_v0_1_RELEASE_RECORD.md`  
   - Summarizes retrieval anchors, review closure, verification evidence, and reproduction commands.  
3. `docs/ESAL_CONFORMANCE_KIT_v0_1.md`  
   - Defines the replay comparison surface and expected outputs.  
4. `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`  
   - Gives fixture-level expected classifications, fingerprints, and exceptions.  
5. `reference/esal/CANONICALIZATION_SPEC_v0_1.md`  
   - Defines event canonicalization behavior.  
6. `reference/esal/STATE_SEMANTICS_v0_1.md`  
   - Defines state reduction semantics and non-claims.  
7. `docs/FORK_ESAL_ROADMAP_v0_1.md`  
   - Describes forward development after RC6.  
8. `docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md`  
   - Gives a concrete evidence-boundary walkthrough.

---

## 3. Quick Verification

From the repository root:

```text
git checkout esal-v0.1-rc6
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
```

Expected verification distribution:

```text
PASS: 4
G:    3
S:    2
D:    1
```

Expected permutation-invariance result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

---

## 4. Core Claim Boundary

ESAL v0.1 verifies behavior of the reference-oracle replay surface.

It does **not** establish production completeness, legal sufficiency, compliance sufficiency, authorization correctness, external governance validity, endorsement, approval, policy adequacy, safety, truth, or independent implementation convergence.

This list is illustrative, not exhaustive.

---

## 5. Reader Guidance

If you are reviewing ESAL v0.1, focus on:

- whether the release-gate artifact preserves its claim boundary  
- whether the expected outputs are reproducible  
- whether the canonicalization and state semantics are internally consistent  
- whether non-claims are preserved  
- whether the conformance surface is clear enough for independent replay comparison  

Do **not** treat PASS as a compliance, authorization, approval, or external-governance signal.
