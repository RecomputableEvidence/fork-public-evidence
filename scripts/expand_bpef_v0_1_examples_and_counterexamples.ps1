# scripts/expand_bpef_v0_1_examples_and_counterexamples.ps1
# Expands BPEF v0.1 Sections 6-8 with concrete minimal failing examples,
# non-failing counterexamples, and cross-class pressure cases.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF line endings.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)

    $full = [System.IO.Path]::GetFullPath($Path)
    if (-not (Test-Path $full)) {
        throw "Missing file: $Path"
    }

    return [System.IO.File]::ReadAllText($full, $Utf8NoBom)
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Assert-Contains {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Needle,
        [Parameter(Mandatory = $true)][string]$Message
    )

    if (-not $Text.Contains($Needle)) {
        throw $Message
    }
}

Assert-RepoRoot

$docPath = "docs/research/BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md"

$existing = Read-Utf8 -Path $docPath

Assert-Contains `
    -Text $existing `
    -Needle "# BPEF v0.1" `
    -Message "Target file does not appear to be the BPEF v0.1 framework document."

Assert-Contains `
    -Text $existing `
    -Needle "## 6. Minimal Failing Examples" `
    -Message "Could not find Section 6 heading."

Assert-Contains `
    -Text $existing `
    -Needle "## 9. Evaluation Outcomes" `
    -Message "Could not find Section 9 heading."

$replacement = @'
## 6. Minimal Failing Examples

BPEF v0.1 uses minimal failing examples to make pressure observable without requiring a large harness.

A minimal failing example should identify:

- the pressure class;
- the invariant under stress;
- the smallest meaningful perturbation;
- the expected observable failure signature;
- what Fork may expose; and
- what Fork must not decide.

The examples below are not production scenarios, compliance scenarios, legal scenarios, or safety determinations. They are small boundary-pressure specimens.

## 6.1 Information Pressure Failure: Missing Referenced Artifact

Pressure class: Information Pressure
Invariant under stress: Epistemic Fidelity / Reference Continuity
Representative outcome: INCOMPLETE_OBSERVABILITY_RECORDED or REFERENCE_CONTINUITY_FAILURE_RECORDED

Baseline:

```text
A preserved record references Artifact A, Artifact B, and Receipt R.
Artifact A and Artifact B are available.
Receipt R identifies both artifacts without replacing them.
An independent reviewer can inspect the referenced artifacts directly.
```

Perturbation:

```text
Artifact B is missing.
Receipt R remains available and summarizes Artifact B.
A downstream reviewer treats Receipt R as sufficient replacement for Artifact B.
```

Boundary-preserving result:

- The system records that Artifact B is missing or unresolved.
- The system preserves Receipt R as a receipt, not as replacement evidence.
- The system does not treat partial access as complete observability.

Fork may expose:

- Artifact B is referenced but unavailable.
- Receipt R exists and may be inspected as a receipt.
- The record has incomplete observability.

Fork must not decide:

- That Artifact B existed in the claimed form.
- That Receipt R proves the missing artifact.
- That the reviewer should rely on the incomplete record.
- That the underlying decision remains valid, compliant, lawful, safe, or correct.

## 6.2 Structural Pressure Failure: Exterior Observation Upgraded Into Authority

Pressure class: Structural Pressure
Invariant under stress: Boundary Integrity / Non-Authority Absorption
Representative outcome: AUTHORITY_ABSORPTION_ATTEMPT_RECORDED

Baseline:

```text
An exterior reviewer states that an architecture appears disciplined.
The statement is preserved as an exterior observation.
The record does not classify the observation as validation, certification, approval, endorsement, or proof.
```

Perturbation:

```text
A downstream artifact cites the exterior observation as proof that the architecture is correct, approved, compliant, production-ready, or legally sufficient.
```

Boundary-preserving result:

- The system records an attempted authority upgrade.
- The system preserves the original observation classification.
- The system does not convert observation into validation or authority.

Fork may expose:

- The observation exists.
- The observation was made by an exterior reviewer.
- The downstream artifact attempted to rely on the observation as authority.
- The observation did not itself carry that authority.

Fork must not decide:

- That the architecture is correct.
- That the reviewer endorsed Fork.
- That the observation establishes production readiness.
- That the observation establishes legal, compliance, audit, procurement, or security sufficiency.

## 6.3 Temporal Pressure Failure: Historical Policy Reference Unresolved

Pressure class: Temporal Pressure
Invariant under stress: Context Inspectability / Reference Continuity
Representative outcome: TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED or REFERENCE_CONTINUITY_FAILURE_RECORDED

Baseline:

```text
A workflow was admitted at time t0 under Policy v1.2.
The preserved record references Policy v1.2.
Policy v1.2 is archived, hash-bound, or otherwise inspectable.
A later reviewer can inspect the historical admission context.
```

Perturbation:

```text
At time t1, Policy v1.2 is unavailable, overwritten, renamed, or semantically redefined.
The preserved record still references Policy v1.2.
A downstream artifact presents the original admission context as fully inspectable.
```

Boundary-preserving result:

- The system records that the historical policy reference is unresolved or no longer inspectable.
- The system distinguishes original admission context from present-day policy context.
- The system does not silently reinterpret the t0 record under t1 conditions.

Fork may expose:

- The record referenced Policy v1.2 at time t0.
- The current reference state of Policy v1.2 is unresolved, superseded, unavailable, or changed.
- Historical context inspectability is impaired.

Fork must not decide:

- That the original admission remains valid today.
- That the original admission is invalid today.
- That Policy v1.3 replaces Policy v1.2 for purposes of the historical record.
- That execution should continue, stop, renew, or be reauthorized.

## 7. Non-Failing Counterexamples

BPEF also requires non-failing counterexamples so that pressure cases do not become one-sided demonstrations.

A non-failing counterexample shows that a boundary can remain intact under pressure.

Each counterexample should identify:

- the pressure class;
- the invariant preserved;
- the observable preservation behavior;
- what Fork may expose; and
- what Fork must not decide.

## 7.1 Information Pressure Counterexample: Receipt Does Not Replace Artifact

Pressure class: Information Pressure
Invariant preserved: Epistemic Fidelity / Reference Continuity
Representative outcome: BOUNDARY_PRESERVED

Scenario:

```text
A packet includes all referenced artifacts.
A receipt identifies the artifacts and records a prior run.
An independent reviewer recomputes from the artifacts rather than relying on receipt prose.
The recomputation result is structurally consistent.
```

Boundary-preserving result:

- Artifacts remain directly inspectable.
- Receipt text remains classified as receipt text.
- The reviewer can distinguish artifact evidence from receipt summary.

Fork may expose:

- The artifacts are available.
- The receipt is available.
- The recomputation path is independently inspectable.

Fork must not decide:

- That the artifact content is true.
- That the reviewer should rely on the artifact.
- That successful recomputation proves compliance, safety, legality, or production readiness.

## 7.2 Structural Pressure Counterexample: Observation Preserved Without Authority Inheritance

Pressure class: Structural Pressure
Invariant preserved: Boundary Integrity / Non-Authority Absorption
Representative outcome: OBSERVATION_RECORDED_WITHOUT_AUTHORITY_INHERITANCE

Scenario:

```text
An exterior reviewer states that Fork maintains clear architectural boundaries.
The statement is filed as an exterior observation.
The observation is not cited as approval, validation, certification, correctness, or buyer acceptance.
```

Boundary-preserving result:

- The observation remains inspectable.
- Its classification remains exterior observation.
- No downstream artifact inherits authority from it.

Fork may expose:

- Who made the observation, if preserved.
- What the observation said, if preserved.
- How the observation was classified.
- Whether any downstream artifact attempted to overread it.

Fork must not decide:

- That the observation is correct.
- That the reviewer has authority over Fork.
- That the observation validates the architecture.
- That the observation creates consensus, endorsement, certification, or approval.

## 7.3 Temporal Pressure Counterexample: Historical Context Remains Inspectable

Pressure class: Temporal Pressure
Invariant preserved: Context Inspectability / Reference Continuity
Representative outcome: TEMPORAL_CONTEXT_INSPECTABLE

Scenario:

```text
A preserved record references Policy v1.2 at time t0.
At time t1, Policy v1.3 exists.
Policy v1.2 remains archived, hash-bound, or otherwise inspectable.
The record exposes that Policy v1.2, not Policy v1.3, was the historical reference.
```

Boundary-preserving result:

- A later reviewer can inspect the historical authority context.
- The record distinguishes historical reference from current policy state.
- Fork does not decide whether the original admission remains valid under Policy v1.3.

Fork may expose:

- Policy v1.2 was the historical reference.
- Policy v1.2 remains inspectable.
- Policy v1.3 exists as a later policy version, if preserved or referenced.

Fork must not decide:

- Whether Policy v1.3 should govern the prior record.
- Whether the historical admission remains legitimate today.
- Whether execution should be renewed, revoked, continued, or constrained.

## 8. Cross-Class Pressure Cases

Real-world failures often arise from interaction between pressure classes.

BPEF v0.1 identifies cross-class pressure cases for later fixture development. These examples are not yet executable fixtures. They define the intended pressure shape for future schema and checker work.

## 8.1 Information × Structural: Partial Retrieval Causes Authority Inference

Pressure classes: Information Pressure and Structural Pressure
Invariants under stress: Epistemic Fidelity / Boundary Integrity / Non-Authority Absorption
Representative outcome: INCOMPLETE_OBSERVABILITY_RECORDED or AUTHORITY_ABSORPTION_ATTEMPT_RECORDED

Scenario:

```text
A reviewer can access a summary receipt but cannot access the underlying evidence packet.
The receipt says that a prior checker passed.
A downstream artifact treats the receipt as proof that the underlying evidence was complete, authoritative, and sufficient.
```

Boundary-preserving result:

- The system records incomplete observability.
- The system preserves the receipt as a receipt.
- The system records any attempt to treat the receipt as authority.

Fork may expose:

- The receipt was accessible.
- The underlying packet was inaccessible.
- The downstream artifact attempted to infer authority from partial access.

Fork must not decide:

- That the missing packet would have verified.
- That the receipt proves the missing packet.
- That the downstream reliance was justified.
- That the underlying decision was correct, compliant, lawful, safe, or authorized.

## 8.2 Structural × Temporal: Prior Admission Treated As Continuing Authorization

Pressure classes: Structural Pressure and Temporal Pressure
Invariants under stress: Boundary Integrity / Context Inspectability / Non-Authority Absorption
Representative outcome: AUTHORITY_ABSORPTION_ATTEMPT_RECORDED or TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED

Scenario:

```text
A workflow was admitted under a policy at time t0.
At time t1, the policy changes or the admitting authority changes.
A downstream artifact treats the t0 admission record as continuing authorization at t1 without exposing the changed context.
```

Boundary-preserving result:

- The system preserves the t0 admission reference.
- The system exposes whether the t0 context remains inspectable.
- The system records the attempted conversion of historical admission into present authorization.

Fork may expose:

- The historical admission record exists.
- The later context differs or is unresolved.
- The downstream artifact relied on historical admission as if it were continuing authorization.

Fork must not decide:

- Whether authorization continues.
- Whether re-admission is required.
- Whether the workflow should stop or continue.
- Whether the governance layer should approve, revoke, renew, or constrain execution.

## 8.3 Information × Temporal: Schema Meaning Changes After Preservation

Pressure classes: Information Pressure and Temporal Pressure
Invariants under stress: Epistemic Fidelity / Context Inspectability / Reference Continuity
Representative outcome: REFERENCE_CONTINUITY_FAILURE_RECORDED or TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED

Scenario:

```text
A preserved artifact references Schema S v1.0.
At time t1, Schema S v1.1 redefines a term used in the artifact.
The artifact bytes still verify.
A later reviewer cannot determine whether the original record used the v1.0 or v1.1 meaning.
```

Boundary-preserving result:

- The system exposes the schema reference used by the historical record.
- The system surfaces unresolved schema-version or interpretability continuity.
- The system does not silently reinterpret the historical artifact under the later schema.

Fork may expose:

- The artifact bytes still verify.
- The schema reference is missing, unresolved, or changed.
- The semantic context needed for independent interpretation is impaired.

Fork must not decide:

- Which schema meaning should control if the reference is unresolved.
- Whether the artifact remains substantively valid under the later schema.
- Whether the original decision should be accepted, rejected, renewed, or escalated.
'@

# Regex pattern: multi-line (Singleline) from section 6 heading up to before section 9 heading
$pattern = "(?s)## 6\. Minimal Failing Examples.*?(?=## 9\. Evaluation Outcomes)"

if (-not [regex]::IsMatch($existing, $pattern)) {
    throw "Could not isolate Sections 6-8 for replacement."
}

# Replace once, and append a single blank line before section 9
$updated = [regex]::Replace(
    $existing,
    $pattern,
    $replacement.TrimEnd() + "`n`n",
    1
)

Write-Utf8Lf -Path $docPath -Content $updated

Write-Host "Rewrote Sections 6-8 in: $docPath"
Write-Host ""
Write-Host "Changed files:"
git status --short
Write-Host ""
Write-Host "Review commands:"
Write-Host " git diff -- $docPath"
Write-Host " git diff --check"

if ($Commit) {
    git add $docPath
    git add "scripts/expand_bpef_v0_1_examples_and_counterexamples.ps1"
    git diff --cached --check
    git commit -m "Expand BPEF v0.1 examples and counterexamples"

    if ($Push) {
        git push
    }
}

Write-Host ""
Write-Host "Done."