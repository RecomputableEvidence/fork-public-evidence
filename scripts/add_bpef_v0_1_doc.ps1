# scripts/add_bpef_v0_1_doc.ps1
# Adds BPEF v0.1 doc only.
# No schema, fixtures, checker, receipts, or reviewer harness are created by this patch.

$ErrorActionPreference = "Stop"

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $normalized = $Content -replace "`r`n", "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $normalized, $utf8NoBom)
}

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

Assert-RepoRoot

$docDir = "docs/research"
$docPath = Join-Path $docDir "BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md"

if (-not (Test-Path $docDir)) {
    New-Item -ItemType Directory -Path $docDir -Force | Out-Null
}

if (Test-Path $docPath) {
    throw "Target document already exists: $docPath. Remove it or intentionally edit the script before rerunning."
}

$content = @'
# BPEF v0.1 — Boundary Pressure Evaluation Framework

## 1. Purpose

BPEF, the Boundary Pressure Evaluation Framework, evaluates whether an evidence-preserving architecture continues to preserve distinguishable boundaries under pressure.

The primary research question for BPEF v0.1 is:

> Under what conditions can independent reviewers no longer reliably distinguish preserved evidence, preserved boundaries, and external interpretation?

BPEF is intended to support empirical evaluation of boundary preservation. It is not intended to expand the authority of the evidence layer.

## 2. Non-Claims

BPEF does not determine whether an execution, workflow, artifact, or decision was:

- lawful;
- compliant;
- legitimate;
- safe;
- correct;
- authorized;
- approved;
- admissible;
- production-ready; or
- sufficient for any legal, regulatory, operational, or procurement purpose.

BPEF evaluates whether the evidence and boundaries needed for later independent inspection remain distinguishable.

A BPEF result is not an endorsement, certification, compliance determination, legal conclusion, safety finding, or production-readiness assessment.

## 3. Responsibility Boundary

BPEF preserves a strict separation between pressure and responsibility.

The fact that a pressure case reveals authorization, governance, compliance, or legitimacy risk does not mean the evidence layer is responsible for resolving that risk.

Canonical responsibility boundary:

```text
Fork / Evidence Layer:
Preserve → Expose → Enable Independent Verification

Governance / Admission Layer:
Interpret → Decide → Act
```

The evidence layer may preserve, expose, and enable independent verification of records.
The governance or admission layer may interpret evidence, decide whether execution is justified, and act on that decision.

Fork must not absorb responsibility for interpretation, authorization, compliance, approval, renewal, enforcement, or action.

A BPEF boundary failure occurs when an evidence-preserving system either:
- loses inspectable boundary clarity; or
- absorbs responsibility for interpretation, authorization, compliance, approval, renewal, enforcement, or action.

## 4. Pressure Classes

BPEF v0.1 defines three primary pressure classes.

- Information Pressure — Can independent reviewers reconstruct what was observable? (Epistemic Fidelity)
- Structural Pressure — Do evidence, authority, reliance, and interpretation remain distinguishable? (Boundary Integrity)
- Temporal Pressure — Can historical context still be inspected after time, policy, schema, or authority changes? (Context Inspectability)

## 4.1 Information Pressure

Information pressure tests whether independent reviewers can reconstruct what was actually observable from the preserved record.

Typical examples include:
- retrieval distortion;
- incomplete packets;
- missing referenced artifacts;
- conflicting available evidence;
- overread from summaries, receipts, or exterior observations.

The evidence layer may report observability limits.
The evidence layer must not infer missing authority, reconstruct absent facts as if observed, or upgrade partial access into complete verification.

## 4.2 Structural Pressure

Structural pressure tests whether architectural roles remain distinguishable under stress.

Typical examples include:
- exterior observations treated as authority;
- reviewer receipts treated as endorsement;
- evidence references treated as compliance findings;
- preserved claims treated as validated truth;
- downstream reliance expanding upstream authority.

The evidence layer may preserve how a claim, receipt, or observation was used.
The evidence layer must not convert observation into validation, validation into approval, or evidence into authority.

## 4.3 Temporal Pressure

Temporal pressure tests whether historical context remains inspectable after time passes or surrounding conditions change.

Typical examples include:
- policy changes after admission;
- deprecated schemas;
- authority changes;
- expired approvals;
- stale reliance on historical records;
- unavailable referenced context.

The evidence layer may preserve the historical reference and expose whether the referenced context remains available.
The evidence layer must not decide whether historical authorization remains valid in the present.

## 5. Supporting Invariants

BPEF v0.1 defines supporting invariants that may apply across more than one pressure class.

- Reference Continuity — References remain resolvable or explicitly unresolved.
- Canonical Identity — Artifacts retain stable identity across recomputation.
- Deterministic Replay — Equivalent inputs produce the same structural result.
- Non-Authority Absorption — The evidence layer does not act as authority.

## 6. Minimal Failing Examples

BPEF v0.1 uses minimal failing examples to make pressure observable.

## 7. Non-Failing Counterexamples

BPEF also requires non-failing counterexamples so that pressure cases do not become one-sided demonstrations.

## 8. Cross-Class Pressure Cases

Real-world failures often arise from interaction between pressure classes.

## 9. Evaluation Outcomes

Representative outcomes include:
- BOUNDARY_PRESERVED
- REFERENCE_CONTINUITY_FAILURE_RECORDED
- AUTHORITY_ABSORPTION_ATTEMPT_RECORDED
- TEMPORAL_CONTEXT_INSPECTABLE
- TEMPORAL_CONTEXT_INSPECTABILITY_FAILURE_RECORDED
- OBSERVATION_RECORDED_WITHOUT_AUTHORITY_INHERITANCE
- INCOMPLETE_OBSERVABILITY_RECORDED
- DETERMINISTIC_REPLAY_CONFIRMED
- DETERMINISTIC_REPLAY_DIVERGENCE_RECORDED

## 10. Future Work

Future BPEF work may include:
- a JSON schema for boundary pressure cases;
- minimal fixtures for each pressure class;
- a structural checker for BPEF fixtures;
- recomputation receipts;
- reviewer-oriented execution instructions;
- cross-class pressure cases;
- reference continuity receipts;
- deterministic replay receipts;
- exterior observation receipts;
- integration examples at the admission-to-evidence seam.

Future work should preserve the v0.1 responsibility boundary:

Fork / Evidence Layer:
Preserve → Expose → Enable Independent Verification

Governance / Admission Layer:
Interpret → Decide → Act

BPEF should continue to evaluate boundary inspectability without becoming a governance, compliance, authorization, approval, or enforcement mechanism.
'@

Write-Utf8NoBomLf -Path $docPath -Content $content

Write-Host "Created $docPath"
Write-Host ""
Write-Host "Next review commands:"
Write-Host " git status -sb"
Write-Host " git diff -- $docPath"