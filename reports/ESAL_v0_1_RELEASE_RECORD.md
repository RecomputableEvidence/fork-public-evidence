# ESAL v0.1 Release Record

**Artifact ID:** ESAL-RELEASE-RECORD-v0.1-001  
**Repository:** `https://github.com/RecomputableEvidence/fork-public-evidence.git`  
**Branch at generation:** `esal-v0.1-roadmap-v0_1`  
**Generation commit:** `718f1cebf4684ea65e3460ac92ba5773cae696be`  
**Generated UTC:** `2026-06-27T08:21:17Z`  

---

## 1. Retrieval Anchors

**Release candidate tag:** `esal-v0.1-rc6`  
**Release candidate tag commit:** `1a99d32a305dd9f295b794c0e95bcd61c2af183d`  

**Reviewed ESAL subject commit:** `859d2abe3db324970f0d3af4faffafd22f221b28`  
**Release-gate artifact commit:** `f7720f3de9b32a971bf066cc96295065aeae29b0`  
**Release metadata clarification commit:** `bfde05a9e51e339cf4a6571258455ed6c1e3ab02`  

The reviewed ESAL subject commit is the commit at which the reference-oracle specification review findings, delta residuals, and advisories were closed.

The release-gate artifact commit records that closure as an evidence artifact.

The release candidate tag is the retrieval anchor for the release-candidate package.

These identifiers have different roles and should not be interpreted as conflicting release identifiers.

---

## 2. Release Package Contents

The ESAL v0.1 release-candidate package is composed of:

- `reports/ESAL_v0_1_RELEASE_GATE.md`
- `reports/ESAL_v0_1_RELEASE_RECORD.md`
- `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`
- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`
- `docs/ESAL_CONFORMANCE_KIT_v0_1.md`
- `docs/ESAL_v0_1_START_HERE.md`
- `docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md`
- `reference/esal/CANONICALIZATION_SPEC_v0_1.md`
- `reference/esal/STATE_SEMANTICS_v0_1.md`
- `reference/esal/`
- `esal-tests/`
- `tools/esal_verify.ps1`
- `tools/Test-EsalPermutationInvariance.ps1`
- `tools/Test-EsalConformance.ps1`

---

## 3. Review Closure Summary

Initial cold-pass findings:

```text
F-1 through F-11: CLOSED
```

Delta residuals:

```text
bc25436: CLOSED
8d2a0e0: CLOSED
6513203: CLOSED
859d2ab: CLOSED
```

Release-gate artifact review:

```text
esal-v0.1-rc6: SIGNED OFF FOR RELEASE RECORD INCLUSION
```

Open findings:

```text
NONE
```

---

## 4. Verification Evidence

Latest ESAL v0.1 reference-oracle verification distribution:

```text
PASS: 4
G:    3
S:    2
D:    1
```

Interpretation:

- PASS indicates replay that is structurally valid and valid under ESAL v0.1 oracle rules.  
- G indicates governance-class failure or governance-invalid replayable state under ESAL v0.1 oracle rules.  
- S indicates structural/substrate-class failure.  
- D indicates determinism-class failure.  

These are oracle classifications. They are not external legal, compliance, authorization, safety, policy, approval, or governance-validity determinations.

---

## 5. Permutation Invariance Evidence

Permutation invariance was executed against:

```text
esal-tests\canonical\log1-basic-A-B-C.jsonl
```

Result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

Stable fingerprint:

```text
6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836
```

Stable canonical events hash:

```text
a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878
```

---

## 6. Reproduction Commands

From the repository root:

```text
git checkout esal-v0.1-rc6
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
.\tools\Test-EsalConformance.ps1
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

## Executable Conformance Evidence

The ESAL v0.1 executable conformance harness is:

```text id="na5j07"
tools/Test-EsalConformance.ps1
```

It checks the ESAL v0.1 reference oracle against the expected-output surface and writes:

```text
reports/ESAL_v0_1_CONFORMANCE_REPORT.json
```

A passing run emits:

```text
CONFORMANCE_PASS
```

This establishes executable reference-oracle conformance checking only. It does not establish independent implementation convergence.

## 7. Non-Claims

This release record does not establish:

- production completeness  
- legal sufficiency  
- compliance sufficiency  
- authorization correctness  
- external governance validity  
- endorsement or approval  
- policy adequacy  
- safety or truth  
- independent implementation convergence  
- buyer-readiness  

This list is illustrative, not exhaustive.

This record is limited to the ESAL v0.1 reference-oracle release-candidate evidence surface and its review-closure record.

---

## 8. Determination

```text
ESAL_v0_1_RC_RELEASE_RECORD_CREATED
```

The release candidate is preserved as a reviewed reference-oracle checkpoint. Any later semantic changes should occur in future branches or release candidates, not by mutating the release-candidate anchor.
