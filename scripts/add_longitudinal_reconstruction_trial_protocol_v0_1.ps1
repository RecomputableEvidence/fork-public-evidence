# scripts\add_longitudinal_reconstruction_trial_protocol_v0_1.ps1
# Adds Fork Longitudinal Reconstruction Trial v0.1 protocol document.
# Doc-only protocol patch. No schemas, fixtures, checkers, receipts, or routing updates.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF line endings. [web:1][web:4][web:10]

param(
    [switch]$Force,
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

# UTF-8 without BOM encoding instance. [web:1][web:10]
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir  = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    # Normalize to LF only, then write as UTF-8 without BOM. [web:1][web:4][web:10]
    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string[]]$Args
    )

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Assert-RepoRoot

$docDir     = "docs/reconstruction"
$docPath    = Join-Path $docDir "FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md"
$scriptPath = "scripts/add_longitudinal_reconstruction_trial_protocol_v0_1.ps1"

if ((Test-Path $docPath) -and -not $Force) {
    throw "Target document already exists: $docPath. Use -Force to overwrite intentionally."
}

$content = @'
# Fork Longitudinal Reconstruction Trial v0.1

Status: Protocol draft.
Scope: Deterministic longitudinal reconstruction trial for a bounded AI-assisted reliance event.
Classification: Research protocol, not validation, certification, authorization, legal conclusion, compliance conclusion, safety finding, or production-readiness assessment.

## 1. Purpose

This protocol defines a bounded empirical trial for Fork's temporal reconstruction claim.

The core claim under test is:

> Fork can reconstruct a preserved AI-assisted reliance event over time from sealed artifacts alone, detect tampering or reference decay, distinguish checker drift from packet failure, and preserve the boundary between reconstruction and authorization.

The trial is designed to demonstrate reconstructability of a preserved event sequence, not truth or legitimacy of the underlying event.

## 2. Non-Claims

This trial does not prove that:

- the original workflow was correct;
- the original admission was valid;
- the AI output was true;
- the human reviewer made the right decision;
- reliance was justified;
- execution was authorized;
- compliance was satisfied;
- legal sufficiency was established;
- safety was established;
- production readiness was established;
- any organization approved the underlying action.

This trial evaluates whether a preserved evidence packet can be reconstructed over time while surfacing tamper, reference decay, missing context, and boundary overread.

A successful trial result is not an endorsement, validation, certification, legal opinion, compliance opinion, safety assessment, procurement approval, audit conclusion, or production-readiness assessment.

## 3. Responsibility Boundary

The trial preserves Fork's responsibility boundary.

```text
Fork / Evidence Layer:
Preserve -> Expose -> Enable Independent Verification

Governance / Admission Layer:
Interpret -> Decide -> Act

Fork may reconstruct preserved evidence state.
Fork must not decide whether the reconstructed event was authorized, lawful, compliant, safe, correct, sufficient, or approved.
Every receipt produced by this trial must include explicit non-authority language.
```

## 4. Determinism Versus Fidelity

A replay hash match proves determinism.
It does not, by itself, prove fidelity to the original event.

This protocol separates two claims:

**Fidelity claim:**
The expected reconstruction faithfully represents the independently defined source event sequence.

**Determinism claim:**
The same sealed packet, under the same pinned checker, reconstructs to the same expected output over time.

The expected reconstruction must have provenance independent from the replay checker.
The same implementation must not create the expected reconstruction and then later prove itself by reproducing it.

## 5. Two Clocks

The trial uses two clocks.

### 5.1 Logical Time

Logical time defines the simulated workflow sequence inside the fixture.

- t0: Admission context created.
- t1: AI-assisted artifact produced.
- t2: Human review and reliance event occurs.
- t3: Fork evidence packet sealed.
- t4: Later replay from preserved packet only.

### 5.2 Real Time

Real time defines the actual delayed replay schedule.

- Day 0: Immediate baseline replay.
- Day 7: First delayed replay.
- Day 30: Second delayed replay.
- Day 90: Final delayed replay.

Each replay must use the sealed packet and must emit a replay receipt.

## 6. Trial Tracks

The trial has four tracks.

### 6.1 Track A: Clean Reconstruction

**Purpose:**
Prove that the clean sealed packet reconstructs under the pinned checker.

**Expected primary outcome:**
`PACKET_RECONSTRUCTION_CONFIRMED_UNDER_PINNED_CHECKER`

### 6.2 Track B: Temporal Replay

**Purpose:**
Prove that the clean sealed packet remains reconstructable after elapsed time.

Track B runs at Day 0, Day 7, Day 30, and Day 90.

Track B must run two checker paths where available:

- **Pinned checker path:** Uses the checker version pinned at t3.
- **Current checker path:** Uses the latest checker version available at replay time.

The pinned checker path tests packet survival.
The current checker path tests checker or schema drift.

### 6.3 Track C: Adverse Variants

**Purpose:**
Prove that controlled failures are surfaced, not hidden, inferred, or converted into authority.

Track C includes at least:

- Active tamper case.
- Manifest-level tamper or outer-manifest hash mismatch case.
- Policy drift case.
- Missing historical reference case.
- Receipt overread case.

Track C adverse variants must be rerun at each real-time checkpoint:

- Day 0
- Day 7
- Day 30
- Day 90

This ensures that detection capability itself remains operational over time, not merely that the clean packet still reconstructs.

### 6.4 Track D: Interpretive Review

**Purpose:**
Test whether external reviewers can distinguish reconstruction from authorization.

Track D may use LLMs and human reviewers.

LLM outputs are exterior interpretive observations.
Human outputs may be human recomputation receipts or human interpretive receipts, depending on what the reviewer actually did.

Track D must not be confused with machine replay.

## 7. Artifact Sequence

The clean fixture packet should contain the following logical sequence.

### 7.1 t0 Admission Context

- `admission_record.json`
- `policy_reference_v1_2.json`
- `admission_non_claims.json`

### 7.2 t1 AI-Assisted Artifact

- `prompt_or_request.json`
- `ai_output.json`
- `model_context_declared.json`
- `output_non_claims.json`

### 7.3 t2 Human Review and Reliance Event

- `human_review_event.json`
- `relied_upon_claims.json`
- `rejected_or_excluded_claims.json`
- `reliance_event.json`

### 7.4 t3 Evidence Packet Seal

- `manifest.json`
- `hashes.sha256`
- `packet_manifest.sha256`
- `packet_manifest_outer_receipt.json`
- `canonical_reconstruction_target.json`
- `expected_reconstruction.json`
- `expected_reconstruction.sha256`
- `non_authority_boundary_statement.md`
- `environment_manifest.json`

### 7.5 t4 Replay Outputs

- `reconstruction_output.json`
- `reconstruction_output.sha256`
- `reference_continuity_report.json`
- `replay_receipt.json`

## 8. Expected Reconstruction Provenance

The expected reconstruction must be independently established before sealing.

Required artifacts:

- `source_event_sequence.json`
- `expected_reconstruction.json`
- `ground_truth_review_receipt.md`

### 8.1 Source Event Sequence

`source_event_sequence.json` is the hand-authored ground truth fixture.
It defines the intended logical event sequence.
It is not produced by the reconstruction checker.

### 8.2 Expected Reconstruction

`expected_reconstruction.json` is the canonical reconstruction target.

It must be produced by one of the following methods:

**Method A:**
Hand-authored independently from `source_event_sequence.json` by a reviewer who did not write the reconstruction checker.

**Method B:**
Generated by a separate implementation, then reviewed by a different human who did not write the reconstruction checker.

**Method C:**
Generated by an LLM or script, then independently reviewed by a human who did not write the reconstruction checker and did not rely on the checker output as authority.

The protocol should record which method was used.

### 8.3 Ground Truth Review Receipt

`ground_truth_review_receipt.md` records the review of `expected_reconstruction.json` against `source_event_sequence.json`.

It must state:

- The reviewer compared `source_event_sequence.json` to `expected_reconstruction.json`.
- The reviewer did not treat the reconstruction checker as authority.
- The review is a human review receipt, not a machine proof.
- The review does not establish correctness, legality, authorization, safety, compliance, or truth.

The receipt must identify whether the reviewer was:

- Author-reviewer.
- Independent human reviewer.
- LLM-assisted human reviewer.
- Other.

The strongest v0.1 result requires at least one independent human review receipt.

If only author-review is available, the protocol must mark the fidelity provenance as author-reviewed, not independently substantiated.

## 9. Manifest and Root-of-Trust Scope

The manifest binds the packet.

At minimum, the manifest must include:

- `trial_id`
- `trial_version`
- `packet_id`
- `schema_versions`
- `checker_versions`
- `pinned_commit`
- `canonicalization_method`
- `artifact_hashes`
- `expected_reconstruction_hash`
- `environment_manifest_hash`
- `non_authority_boundary_statement_hash`
- `created_at_fixed_fixture_time`

### 9.1 Payload Tamper

Payload tamper means an artifact listed in the manifest has been altered after sealing.

Expected outcomes:

- `TAMPER_DETECTED`
- `RECONSTRUCTION_BLOCKED_BY_HASH_MISMATCH`
- `BOUNDARY_PRESERVED`

### 9.2 Manifest-Level Tamper

Manifest-level tamper means the manifest itself has been altered.

v0.1 must not leave manifest-level tamper unstated.

For this protocol, the minimum v0.1 requirement is:

- `packet_manifest.sha256`
- `packet_manifest_outer_receipt.json`

The outer receipt records the manifest hash outside the manifest.

If the manifest hash does not match the outer receipt, the replay must emit:

- `MANIFEST_TAMPER_DETECTED`
- `RECONSTRUCTION_BLOCKED_BY_MANIFEST_HASH_MISMATCH`
- `BOUNDARY_PRESERVED`

### 9.3 Future Anchoring

Future versions may add timestamp authority anchoring, public transparency logs, signed releases, or other external anchoring.

Those mechanisms are out of scope for v0.1 unless separately implemented and documented.

## 10. Checker Tracks

The trial distinguishes packet survival from checker drift.

### 10.1 Pinned Checker Track

The pinned checker track uses the checker version pinned at t3.

It answers:

> Does the packet still reconstruct under the original verification semantics?

Expected outcome for clean packet:

- `PACKET_RECONSTRUCTION_CONFIRMED_UNDER_PINNED_CHECKER`

### 10.2 Current Checker Track

The current checker track uses the latest checker version available at replay time.

It answers:

> Has the checker, schema, or reconstruction semantics changed relative to the pinned checker?

Current checker disagreement must be classified as one of:

- `CURRENT_CHECKER_DOCUMENTED_SEMANTIC_CHANGE_RECORDED`
- `CURRENT_CHECKER_UNDOCUMENTED_SEMANTIC_DRIFT_RECORDED`
- `CURRENT_CHECKER_MATCH_CONFIRMED`

Documented semantic change means the divergence is explained by a changelog, version bump, migration note, schema revision, or other preserved change record.

Undocumented semantic drift means divergence occurred without a preserved explanation.

Both are different from packet tamper.

## 11. Adverse Cases

### 11.1 Active Payload Tamper

A single byte is changed in one sealed artifact after t3.

Expected outcomes:

- `TAMPER_DETECTED`
- `RECONSTRUCTION_BLOCKED_BY_HASH_MISMATCH`
- `BOUNDARY_PRESERVED`

### 11.2 Manifest Tamper

The manifest is changed after t3.

Expected outcomes:

- `MANIFEST_TAMPER_DETECTED`
- `RECONSTRUCTION_BLOCKED_BY_MANIFEST_HASH_MISMATCH`
- `BOUNDARY_PRESERVED`

### 11.3 Policy Drift

At t0, the admission record references Policy v1.2.
At replay time, Policy v1.3 exists.

Expected outcomes:

- `TEMPORAL_CONTEXT_INSPECTABLE`
- `AUTHORITY_REFERENCED_NOT_INHERITED`
- `BOUNDARY_PRESERVED`

Fork must not decide whether Policy v1.3 changes current authorization.

### 11.4 Missing Historical Reference

At replay time, Policy v1.2 is unavailable.

Expected outcomes:

- `REFERENCE_CONTINUITY_FAILURE_RECORDED`
- `TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED`
- `INCOMPLETE_OBSERVABILITY_RECORDED`
- `BOUNDARY_PRESERVED`

Fork must not infer Policy v1.2 from Policy v1.3.

### 11.5 Receipt Overread

A later reviewer has a reconstruction receipt but lacks the underlying artifact.

Expected outcomes:

- `INCOMPLETE_OBSERVABILITY_RECORDED`
- `AUTHORITY_ABSORPTION_ATTEMPT_RECORDED`
- `BOUNDARY_PRESERVED`

Fork must not treat a receipt as replacement evidence for a missing artifact.

## 12. Technical Invariants

Before Day 0, the trial must pass a nondeterminism audit.

Required invariants:

- Canonical JSON serialization.
- Sorted object keys.
- Stable arrays.
- Fixed timestamps inside fixture data.
- No live system lookups.
- No network dependency during replay.
- No current date dependency except replay receipt metadata.
- No filesystem order dependency.
- SHA-256 content addressing for all artifacts.
- Versioned schemas.
- Versioned checkers.
- Pinned commit hashes.
- Environment manifest.

### 12.1 Named Nondeterminism Regression Checks

The audit must specifically check for:

- joining unordered collections into output strings;
- iterating through unordered sets or maps where output order matters;
- filesystem directory listing order without explicit sorting;
- environment-dependent default encodings;
- locale-dependent sorting;
- floating-point formatting instability;
- current-time calls inside reconstruction output;
- platform-specific path separators in canonical output;
- free-text concatenation from unordered collections.

If any of these are present in output-affecting code, Day 0 must not be treated as a valid baseline until repaired.

## 13. Receipt Vocabulary

### 13.1 Machine Receipt Outcomes

- `RECONSTRUCTION_MATCH_CONFIRMED`
- `PACKET_RECONSTRUCTION_CONFIRMED_UNDER_PINNED_CHECKER`
- `REFERENCE_CONTINUITY_CONFIRMED`
- `BOUNDARY_PRESERVED`
- `AUTHORITY_REFERENCED_NOT_INHERITED`
- `NON_CLAIMS_PRESERVED`
- `TAMPER_DETECTED`
- `MANIFEST_TAMPER_DETECTED`
- `RECONSTRUCTION_BLOCKED_BY_HASH_MISMATCH`
- `RECONSTRUCTION_BLOCKED_BY_MANIFEST_HASH_MISMATCH`
- `REFERENCE_CONTINUITY_FAILURE_RECORDED`
- `TEMPORAL_CONTEXT_INSPECTABLE`
- `TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED`
- `INCOMPLETE_OBSERVABILITY_RECORDED`
- `CURRENT_CHECKER_MATCH_CONFIRMED`
- `CURRENT_CHECKER_DOCUMENTED_SEMANTIC_CHANGE_RECORDED`
- `CURRENT_CHECKER_UNDOCUMENTED_SEMANTIC_DRIFT_RECORDED`

### 13.2 Interpretive Receipt Outcomes

- `EXTERIOR_INTERPRETIVE_OBSERVATION`
- `LLM_INTERPRETIVE_STRESS_TEST_RECORDED`
- `HUMAN_RECOMPUTATION_RECEIPT_RECORDED`
- `HUMAN_INTERPRETIVE_RECEIPT_RECORDED`
- `AUTHORITY_ABSORPTION_ATTEMPT_RECORDED`
- `RECEIPT_OVERREAD_ATTEMPT_RECORDED`

Interpretive receipts must be visibly distinguished from machine receipts.

Machine receipts describe artifact state and deterministic replay outcome.
Interpretive receipts describe reviewer behavior, reviewer interpretation, or exterior observations.

Fork must not collapse interpretive receipts into machine proof.

## 14. Required Receipt Fields

Every machine replay receipt must include:

- `receipt_id`
- `receipt_type`
- `trial_id`
- `trial_version`
- `packet_id`
- `replay_day`
- `replay_timestamp`
- `replayer_identity`
- `environment_manifest_hash`
- `packet_manifest_hash`
- `outer_manifest_receipt_hash`
- `reconstruction_hash`
- `expected_reconstruction_hash`
- `checker_track`
- `checker_pinned_commit`
- `checker_current_commit`
- `reference_continuity_report_hash`
- `receipt_outcome_codes`
- `non_authority_boundary_statement`

Every interpretive receipt must include:

- `receipt_id`
- `receipt_type`
- `trial_id`
- `trial_version`
- `reviewer_type`
- `reviewer_identity_or_pseudonym`
- `materials_provided`
- `materials_not_provided`
- `review_timestamp`
- `prompt_or_instruction_hash`
- `review_output_hash`
- `boundary_distinctions_observed`
- `overread_attempts_observed`
- `receipt_outcome_codes`
- `non_authority_boundary_statement`

## 15. Track D Acceptance Criteria

Track D is exploratory unless acceptance criteria are explicitly used.

If Track D is included as part of the v0.1 success claim, it must satisfy:

- At least N of M reviewers, given only the sealed packet and instructions, correctly distinguish reconstruction from authorization.
- At least N of M reviewers correctly distinguish a receipt from underlying evidence.
- At least N of M reviewers correctly distinguish referenced authority from inherited authority.
- At least N of M reviewers correctly distinguish missing reference from substitute evidence.
- All reviewer outputs are preserved as interpretive receipts, not machine proof.

For v0.1, N and M must be declared before the review begins.
If N and M are not declared, Track D results may be preserved only as exterior interpretive observations.

## 16. Acceptance Criteria

The trial succeeds only if all required machine criteria are met.

### 16.1 Required Machine Criteria

- Clean packet reconstructs under the pinned checker at Day 0.
- Clean packet reconstructs under the pinned checker at every delayed replay.
- Expected reconstruction has independently recorded provenance.
- Payload tampering is detected and reconstruction is blocked.
- Manifest tampering is detected or explicitly marked out of scope.
- Missing references are recorded, not inferred or substituted.
- Policy drift is surfaced, not interpreted.
- Receipt overread is blocked or recorded.
- Current-checker drift is distinguished from packet failure.
- Adverse variants are rerun at every delayed checkpoint.
- All machine receipts preserve explicit non-authority language.

### 16.2 Optional Interpretive Criteria

- LLM reviewers identify overread risk without treating reconstruction as authorization.
- Human reviewers reconstruct or interpret from sealed materials without relying on author explanation.
- Reviewer outputs are preserved as interpretive receipts.
- Reviewer outputs do not become validation, certification, compliance conclusion, or approval.

## 17. Empirical Spine and Interpretive Layer

### 17.1 Empirical Spine

The empirical spine is:

- canonical artifacts
- SHA-256 hashes
- manifest
- outer manifest receipt
- pinned checker
- expected reconstruction with independent provenance
- machine replay receipts
- delayed replays
- adverse variant replays

The empirical spine must stand without LLM interpretation.

### 17.2 Interpretive Layer

The interpretive layer may include:

- LLM reviewer simulation
- adversarial interpretation testing
- semantic overread testing
- retrieval distortion testing
- human reviewer replay
- human recomputation receipts
- human interpretive receipts

The interpretive layer can strengthen practical credibility.
It must not replace deterministic replay.

## 18. Build Order

The recommended build order is:

1. Protocol doc.
2. Schema set.
3. Clean fixture packet.
4. Reconstruction script.
5. Checker script.
6. Day 0 machine receipt.
7. Adverse variant fixtures.
8. Reviewer instructions.
9. Day 7 replay receipts.
10. Day 30 replay receipts.
11. Day 90 replay receipts.
12. Interpretive synthesis.

## 19. North Star Test

A reviewer, later, from preserved artifacts alone, should be able to reconstruct what crossed the reliance boundary and distinguish:

- what happened;
- what was preserved;
- what was referenced;
- what was missing;
- what was relied upon;
- what was not claimed;
- what authority was referenced;
- what authority was not inherited.

Fork must not decide whether the underlying action was justified.

If the clean packet, adverse variants, and delayed replays satisfy this protocol, Fork has established a temporal proof surface for bounded reconstruction over time without absorbing authorization.

## 20. Future Work

Future work may include:

- schema definitions;
- fixture packets;
- canonicalization tooling;
- reconstruction script;
- checker script;
- replay receipts;
- human recomputation receipts;
- LLM interpretive stress tests;
- external anchoring;
- timestamp authority receipts;
- public transparency log integration;
- enterprise reference continuity patterns.

Future work must preserve the core boundary:

- Reconstruction is not authorization.
- Structural verification is not truth.
- Reference continuity is not compliance.
- Replay success is not approval.
'@

Write-Utf8Lf -Path $docPath -Content $content

Write-Host "Created or updated: $docPath"
Write-Host ""
Write-Host "Changed files:"
git status --short
Write-Host ""
Write-Host "Review commands:"
Write-Host " git diff -- $docPath"
Write-Host " git diff --check -- $docPath $scriptPath"

if ($Commit) {
    Write-Host ""
    Write-Host "Running path-limited whitespace check..."
    Invoke-Git -Args @("diff", "--check", "--", $docPath, $scriptPath)

    Write-Host ""
    Write-Host "Adding protocol doc and script only..."
    Invoke-Git -Args @("add", "--", $docPath, $scriptPath)

    Write-Host ""
    Write-Host "Checking staged diff..."
    Invoke-Git -Args @("diff", "--cached", "--check")

    Invoke-Git -Args @("commit", "-m", "Add longitudinal reconstruction trial protocol v0.1")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."