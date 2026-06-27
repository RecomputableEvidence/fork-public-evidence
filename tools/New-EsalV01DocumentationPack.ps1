param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "== ESAL v0.1 Documentation Pack Generator =="

# --------------------------------------------------------------------
# Safety checks
# --------------------------------------------------------------------

if (!(Test-Path ".git")) {
    throw "Run this script from the repository root."
}

$requiredPaths = @(
    "reference\esal",
    "esal-tests",
    "tools\esal_verify.ps1",
    "tools\Test-EsalPermutationInvariance.ps1",
    "reports\ESAL_v0_1_RELEASE_GATE.md"
)

foreach ($path in $requiredPaths) {
    if (!(Test-Path $path)) {
        throw "Required path missing: $path"
    }
}

New-Item -ItemType Directory -Force -Path "reports" | Out-Null
New-Item -ItemType Directory -Force -Path "docs" | Out-Null

# --------------------------------------------------------------------
# Metadata
# --------------------------------------------------------------------

$ReleaseTag = "esal-v0.1-rc6"
$ReviewedSubjectCommit = "859d2abe3db324970f0d3af4faffafd22f221b28"
$ReleaseGateArtifactCommit = "f7720f3de9b32a971bf066cc96295065aeae29b0"
$ReleaseMetadataClarificationCommit = "bfde05a9e51e339cf4a6571258455ed6c1e3ab02"

function Get-GitValue {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $value = & git @Args 2>$null
    if ($LASTEXITCODE -ne 0) {
        return ""
    }

    return ($value | Select-Object -First 1).Trim()
}

$CurrentBranch = Get-GitValue @("branch", "--show-current")
$CurrentCommit = Get-GitValue @("rev-parse", "HEAD")
$ReleaseTagCommit = Get-GitValue @("rev-parse", "${ReleaseTag}^{commit}")
$RemoteUrl = Get-GitValue @("config", "--get", "remote.origin.url")

if ([string]::IsNullOrWhiteSpace($RemoteUrl)) {
    $RemoteUrl = "https://github.com/RecomputableEvidence/fork-public-evidence"
}

if ([string]::IsNullOrWhiteSpace($ReleaseTagCommit)) {
    Write-Warning "Could not resolve ${ReleaseTag}. The generated files will still be created, but the release tag commit field will be UNKNOWN."
    $ReleaseTagCommit = "UNKNOWN"
}

$GenerationDateUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# --------------------------------------------------------------------
# Constants from ESAL v0.1 RC6 evidence record
# --------------------------------------------------------------------

$PassCount = "4"
$GCount = "3"
$SCount = "2"
$DCount = "1"

$BaselineLog = "esal-tests\canonical\log1-basic-A-B-C.jsonl"
$BaselineFingerprint = "6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836"
$BaselineCanonicalEventsHash = "a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878"
$ConstraintViolationFingerprint = "bee2ca4f6ef180c915ea84c1aad8fb68f1229fa549585103197f499889736e44"
$PlaceholderFingerprint = "39fde2d6cb76d9409fdf09cb5e76ab2ba8b7174b430cb19c455038f2ded37bb1"
$ConstraintsTightenFingerprint = "50b3d57de240108c39ab25be712114f6efb9ef0903fe1661a931e99fe4fc8393"
$ObligationsAccumulateFingerprint = "95659c757320ac0c0db79154e4f7d06cd9db0284cf2d2413d421c238ccdaf5bb"

# --------------------------------------------------------------------
# File writing helper
# --------------------------------------------------------------------

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Doc {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    if ((Test-Path $Path) -and (-not $Force)) {
        throw "File already exists: $Path. Re-run with -Force to overwrite."
    }

    $normalized = $Content.Replace("`r`n", "`n").TrimEnd() + "`n"
    [System.IO.File]::WriteAllText((Join-Path (Get-Location) $Path), $normalized, $Utf8NoBom)

    Write-Host "Wrote: $Path"
}

function Expand-Template {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Template
    )

    $Template = $Template.Replace("{{REPO_URL}}", $RemoteUrl)
    $Template = $Template.Replace("{{CURRENT_BRANCH}}", $CurrentBranch)
    $Template = $Template.Replace("{{CURRENT_COMMIT}}", $CurrentCommit)
    $Template = $Template.Replace("{{RELEASE_TAG}}", $ReleaseTag)
    $Template = $Template.Replace("{{RELEASE_TAG_COMMIT}}", $ReleaseTagCommit)
    $Template = $Template.Replace("{{REVIEWED_SUBJECT_COMMIT}}", $ReviewedSubjectCommit)
    $Template = $Template.Replace("{{RELEASE_GATE_ARTIFACT_COMMIT}}", $ReleaseGateArtifactCommit)
    $Template = $Template.Replace("{{RELEASE_METADATA_CLARIFICATION_COMMIT}}", $ReleaseMetadataClarificationCommit)
    $Template = $Template.Replace("{{GENERATION_DATE_UTC}}", $GenerationDateUtc)
    $Template = $Template.Replace("{{PASS_COUNT}}", $PassCount)
    $Template = $Template.Replace("{{G_COUNT}}", $GCount)
    $Template = $Template.Replace("{{S_COUNT}}", $SCount)
    $Template = $Template.Replace("{{D_COUNT}}", $DCount)
    $Template = $Template.Replace("{{BASELINE_LOG}}", $BaselineLog)
    $Template = $Template.Replace("{{BASELINE_FINGERPRINT}}", $BaselineFingerprint)
    $Template = $Template.Replace("{{BASELINE_CANONICAL_EVENTS_HASH}}", $BaselineCanonicalEventsHash)
    $Template = $Template.Replace("{{CONSTRAINT_VIOLATION_FINGERPRINT}}", $ConstraintViolationFingerprint)
    $Template = $Template.Replace("{{PLACEHOLDER_FINGERPRINT}}", $PlaceholderFingerprint)
    $Template = $Template.Replace("{{CONSTRAINTS_TIGHTEN_FINGERPRINT}}", $ConstraintsTightenFingerprint)
    $Template = $Template.Replace("{{OBLIGATIONS_ACCUMULATE_FINGERPRINT}}", $ObligationsAccumulateFingerprint)

    return $Template
}

# --------------------------------------------------------------------
# 1. ESAL_v0_1_RELEASE_RECORD.md
# --------------------------------------------------------------------

$ReleaseRecord = @'
# ESAL v0.1 Release Record

**Artifact ID:** ESAL-RELEASE-RECORD-v0.1-001  
**Repository:** `{{REPO_URL}}`  
**Branch at generation:** `{{CURRENT_BRANCH}}`  
**Generation commit:** `{{CURRENT_COMMIT}}`  
**Generated UTC:** `{{GENERATION_DATE_UTC}}`  

---

## 1. Retrieval Anchors

**Release candidate tag:** `{{RELEASE_TAG}}`  
**Release candidate tag commit:** `{{RELEASE_TAG_COMMIT}}`  

**Reviewed ESAL subject commit:** `{{REVIEWED_SUBJECT_COMMIT}}`  
**Release-gate artifact commit:** `{{RELEASE_GATE_ARTIFACT_COMMIT}}`  
**Release metadata clarification commit:** `{{RELEASE_METADATA_CLARIFICATION_COMMIT}}`  

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
- `docs/ESAL_CONFORMANCE_KIT_v0_1.md`
- `docs/ESAL_v0_1_START_HERE.md`
- `docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md`
- `reference/esal/CANONICALIZATION_SPEC_v0_1.md`
- `reference/esal/STATE_SEMANTICS_v0_1.md`
- `reference/esal/`
- `esal-tests/`
- `tools/esal_verify.ps1`
- `tools/Test-EsalPermutationInvariance.ps1`

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
PASS: {{PASS_COUNT}}
G:    {{G_COUNT}}
S:    {{S_COUNT}}
D:    {{D_COUNT}}
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
{{BASELINE_LOG}}
```

Result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

Stable fingerprint:

```text
{{BASELINE_FINGERPRINT}}
```

Stable canonical events hash:

```text
{{BASELINE_CANONICAL_EVENTS_HASH}}
```

---

## 6. Reproduction Commands

From the repository root:

```text
git checkout {{RELEASE_TAG}}
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
```

Expected verification distribution:

```text
PASS: {{PASS_COUNT}}
G:    {{G_COUNT}}
S:    {{S_COUNT}}
D:    {{D_COUNT}}
```

Expected permutation-invariance result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

---

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
'@

# --------------------------------------------------------------------
# 2. ESAL_CONFORMANCE_KIT_v0_1.md
# --------------------------------------------------------------------

$ConformanceKit = @'
# ESAL Conformance Kit v0.1

**Artifact ID:** ESAL-CONFORMANCE-KIT-v0.1-001  
**Release candidate tag:** `{{RELEASE_TAG}}`  
**Release candidate tag commit:** `{{RELEASE_TAG_COMMIT}}`  
**Reviewed ESAL subject commit:** `{{REVIEWED_SUBJECT_COMMIT}}`  

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
git checkout {{RELEASE_TAG}}
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
```

---

## 4. Expected Classification Distribution

```text
PASS: {{PASS_COUNT}}
G:    {{G_COUNT}}
S:    {{S_COUNT}}
D:    {{D_COUNT}}
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
| adversarial  | log4-constraint-violation.jsonl | G   | {{CONSTRAINT_VIOLATION_FINGERPRINT}} | Replayable governance-invalid state                    |
| adversarial  | log5-authority-inflation.jsonl | G   | None                             | GovernanceError: authority inflation (write:data)         |
| adversarial  | log6-lineage-truncation.jsonl | S   | None                             | StructuralError: unknown parent_bdr_id                    |
| adversarial  | log7-event-reordering.jsonl  | D   | None                             | DeterminismError: event_id conflict                       |
| canonical    | C-001-placeholder.jsonl      | PASS | {{PLACEHOLDER_FINGERPRINT}}      | Minimal passing fixture                                   |
| canonical    | log1-basic-A-B-C.jsonl       | PASS | {{BASELINE_FINGERPRINT}}         | Canonical baseline trace                                  |
| canonical    | log2-constraints-tighten.jsonl | PASS | {{CONSTRAINTS_TIGHTEN_FINGERPRINT}} | Valid constraint tightening trace                      |
| canonical    | log3-obligations-accumulate.jsonl | PASS | {{OBLIGATIONS_ACCUMULATE_FINGERPRINT}} | Valid obligation accumulation trace                |
| malformed    | log8-schema-invalid.jsonl    | S   | None                             | StructuralError: missing event_id                         |

---

## 6. Expected Permutation-Invariance Output

Permutation-invariance target:

```text
{{BASELINE_LOG}}
```

Expected result:

```text
PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification.
```

Expected fingerprint:

```text
{{BASELINE_FINGERPRINT}}
```

Expected canonical events hash:

```text
{{BASELINE_CANONICAL_EVENTS_HASH}}
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
'@

# --------------------------------------------------------------------
# 3. ESAL_v0_1_START_HERE.md
# --------------------------------------------------------------------

$StartHere = @'
# ESAL v0.1 â€” Start Here

**Release candidate tag:** `{{RELEASE_TAG}}`  
**Release candidate tag commit:** `{{RELEASE_TAG_COMMIT}}`  

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
git checkout {{RELEASE_TAG}}
powershell .\tools\esal_verify.ps1
.\tools\Test-EsalPermutationInvariance.ps1
```

Expected verification distribution:

```text
PASS: {{PASS_COUNT}}
G:    {{G_COUNT}}
S:    {{S_COUNT}}
D:    {{D_COUNT}}
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
'@

# --------------------------------------------------------------------
# 4. ESAL_v0_1_EXPECTED_OUTPUTS.md
# --------------------------------------------------------------------

$ExpectedOutputs = @'
# ESAL v0.1 Expected Outputs

**Artifact ID:** ESAL-EXPECTED-OUTPUTS-v0.1-001  
**Release candidate tag:** `{{RELEASE_TAG}}`  
**Release candidate tag commit:** `{{RELEASE_TAG_COMMIT}}`  

---

## 1. Purpose

This document records the expected ESAL v0.1 reference-oracle outputs for the current conformance corpus.

These outputs support replay comparison. They do not establish external validity, production sufficiency, legal sufficiency, compliance sufficiency, authorization correctness, approval, endorsement, or independent implementation convergence.

---

## 2. Expected Distribution

```text
PASS: {{PASS_COUNT}}
G:    {{G_COUNT}}
S:    {{S_COUNT}}
D:    {{D_COUNT}}
```

---

## 3. Fixture-Level Expected Outputs

| #  | Corpus group | Log                           | Class | Fingerprint present | Fingerprint                      | Exception class   | Expected message / note                                       |
|----|--------------|------------------------------|-------|---------------------|----------------------------------|-------------------|----------------------------------------------------------------|
| 1  | adversarial  | log2-constraints-tighten.jsonl | G   | no                  | None                             | GovernanceError   | authority inflation without explicit expansion delta: translate |
| 2  | adversarial  | log4-constraint-violation.jsonl | G   | yes                 | {{CONSTRAINT_VIOLATION_FINGERPRINT}} | none          | replayable governance-invalid state                           |
| 3  | adversarial  | log5-authority-inflation.jsonl | G   | no                  | None                             | GovernanceError   | authority inflation without explicit expansion delta: write:data |
| 4  | adversarial  | log6-lineage-truncation.jsonl | S   | no                  | None                             | StructuralError   | unknown parent_bdr_id: bdr-missing-000                        |
| 5  | adversarial  | log7-event-reordering.jsonl  | D   | no                  | None                             | DeterminismError | event_id conflict with differing event content                 |
| 6  | canonical    | C-001-placeholder.jsonl      | PASS | yes                 | {{PLACEHOLDER_FINGERPRINT}}      | none              | minimal passing fixture                                        |
| 7  | canonical    | log1-basic-A-B-C.jsonl       | PASS | yes                 | {{BASELINE_FINGERPRINT}}         | none              | canonical baseline trace                                       |
| 8  | canonical    | log2-constraints-tighten.jsonl | PASS | yes               | {{CONSTRAINTS_TIGHTEN_FINGERPRINT}} | none          | valid constraint tightening trace                             |
| 9  | canonical    | log3-obligations-accumulate.jsonl | PASS | yes           | {{OBLIGATIONS_ACCUMULATE_FINGERPRINT}} | none      | valid obligation accumulation trace                           |
| 10 | malformed    | log8-schema-invalid.jsonl    | S   | no                  | None                             | StructuralError   | missing event_id                                               |

---

## 4. Baseline Permutation-Invariance Expected Output

Target log:

```text
{{BASELINE_LOG}}
```

Expected classification:

```text
PASS
```

Expected fingerprint:

```text
{{BASELINE_FINGERPRINT}}
```

Expected canonical events hash:

```text
{{BASELINE_CANONICAL_EVENTS_HASH}}
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
'@

# --------------------------------------------------------------------
# 5. FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md
# --------------------------------------------------------------------

$Walkthrough = @'
# Fork Evidence Boundary Walkthrough v0.1

**Artifact ID:** FORK-EVIDENCE-BOUNDARY-WALKTHROUGH-v0.1-001  
**Related release candidate:** `{{RELEASE_TAG}}`  

---

## 1. Purpose

This walkthrough explains how Fork evidence-boundary infrastructure can be understood through a concrete AI-assisted workflow.

It is not a product claim, compliance claim, legal sufficiency claim, authorization claim, or external-validity claim.

It shows how claim boundaries can be preserved across a workflow without turning recorded evidence into approval, compliance, or truth.

---

## 2. Example Workflow

Example:

> AI-assisted vendor risk summary

A human team uses an AI system to summarize vendor-risk materials. The organization wants to preserve what happened without treating the AI output, the human review, or the replay result as proof that the decision was correct.

---

## 3. Step-by-Step Evidence Boundary

**Step 1 â€” AI Produces a Summary**

The AI system produces a vendor-risk summary.

Fork records:

- what was requested  
- what the AI produced  
- what input artifacts were referenced  
- what was not claimed  

Fork does **not** claim that the AI summary is true, complete, legally sufficient, compliant, or safe.

**Step 2 â€” Human Reviews and Annotates**

A human reviewer inspects the AI output and adds review notes.

Fork records:

- reviewer identity or role as declared by the workflow  
- review timestamp  
- review notes  
- accepted or rejected claims  
- unresolved unknowns  
- preserved non-claims  

Fork does **not** claim that human review makes the result legally sufficient, compliant, authorized, approved, or correct.

**Step 3 â€” Claim Boundary Is Recorded**

A claim boundary records the scope of what is being asserted.

Example bounded claim:

> The record preserves that this vendor-risk summary was generated, reviewed, and sealed under the stated workflow.

Example non-claims:

- The record does not establish that the vendor is safe.  
- The record does not establish that the decision is legally sufficient.  
- The record does not establish that the review was compliant with all applicable policies.  
- The record does not establish that the underlying facts are true.

**Step 4 â€” BDR Records Boundary Transition**

A Boundary Delta Record can capture a transition between evidence contexts.

Fork preserves:

- what changed  
- what was preserved  
- what narrowed  
- what expanded  
- what became unresolved  
- what evidence references were carried forward  

Fork does not allow authority, compliance, approval, or external validity to silently transfer merely because an adjacent record exists.

**Step 5 â€” ESAL Replays Events and Fingerprints State**

ESAL consumes events and reconstructs state under ESAL v0.1 reference-oracle rules.

ESAL can produce:

- classification  
- reduced state  
- fingerprint  
- replay evidence  

ESAL does **not** determine whether the vendor decision was correct, approved, compliant, legally sufficient, authorized in the world, or externally governance-valid.

**Step 6 â€” Release Gate States What Verified**

The release gate records that the ESAL v0.1 reference-oracle release candidate has a closed review chain, stable verification distribution, stable permutation-invariance evidence, explicit commit-role metadata, and explicit non-claims.

The release gate does **not** make the underlying workflow externally valid.

---

## 4. What Fork Preserves

Fork preserves evidence about:

- requests  
- outputs  
- reviews  
- boundaries  
- transitions  
- non-claims  
- evidence references  
- replay classifications  
- fingerprints  

Fork helps show what was claimed, what was not claimed, and whether the recorded trace still verifies under stated oracle rules.

---

## 5. What Fork Does Not Decide

Fork does **not** decide:

- whether the business decision was right  
- whether the output was true  
- whether the action was legally sufficient  
- whether the workflow was compliant  
- whether a person had real-world authority  
- whether an organization should approve the result  
- whether a vendor is safe  
- whether the process satisfies a regulator  
- whether the evidence is externally governance-valid  

This list is illustrative, not exhaustive.

---

## 6. Buyer-Facing Line

Fork does not tell you the decision was right. It preserves what was claimed, what was not claimed, what evidence was referenced, and whether the recorded trace still verifies under the stated oracle rules.

---

## 7. Boundary Principle

The central boundary is:

- Evidence may be preserved.  
- Replay may be verified.  
- Claims may be bounded.  
- Authority does not silently transfer.  
- External validity is not inherited.

This is the bridge between the technical oracle and the governance value of Fork.
'@

# --------------------------------------------------------------------
# Write files
# --------------------------------------------------------------------

Write-Doc -Path "reports\ESAL_v0_1_RELEASE_RECORD.md" -Content (Expand-Template $ReleaseRecord)
Write-Doc -Path "docs\ESAL_CONFORMANCE_KIT_v0_1.md" -Content (Expand-Template $ConformanceKit)
Write-Doc -Path "docs\ESAL_v0_1_START_HERE.md" -Content (Expand-Template $StartHere)
Write-Doc -Path "reports\ESAL_v0_1_EXPECTED_OUTPUTS.md" -Content (Expand-Template $ExpectedOutputs)
Write-Doc -Path "docs\FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md" -Content (Expand-Template $Walkthrough)

Write-Host ""
Write-Host "Created ESAL v0.1 documentation pack."
Write-Host ""
Write-Host "Suggested review:"
Write-Host " git diff -- reports/ESAL_v0_1_RELEASE_RECORD.md"
Write-Host " git diff -- docs/ESAL_CONFORMANCE_KIT_v0_1.md"
Write-Host " git diff -- docs/ESAL_v0_1_START_HERE.md"
Write-Host " git diff -- reports/ESAL_v0_1_EXPECTED_OUTPUTS.md"
Write-Host " git diff -- docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md"
Write-Host ""
Write-Host "Suggested verification:"
Write-Host " powershell .\tools\esal_verify.ps1"
Write-Host " .\tools\Test-EsalPermutationInvariance.ps1"
Write-Host ""
Write-Host "Suggested commit:"
Write-Host ' git add reports/ESAL_v0_1_RELEASE_RECORD.md docs/ESAL_CONFORMANCE_KIT_v0_1.md docs/ESAL_v0_1_START_HERE.md reports/ESAL_v0_1_EXPECTED_OUTPUTS.md docs/FORK_EVIDENCE_BOUNDARY_WALKTHROUGH_v0_1.md'
Write-Host ' git commit -m "Add ESAL v0.1 release and conformance documentation pack"'
