# scripts/add_commercial_surface_exterior_reviews_v0_1.ps1
# Adds commercial-surface exterior observations and buyer quick start.
# PowerShell 5.1 compatible.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Read-Utf8 {
    param([Parameter(Mandatory=$true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Replace-OrAppendBlock {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$BlockId,
        [Parameter(Mandatory=$true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- $($BlockId):START -->"
    $end = "<!-- $($BlockId):END -->"
    $existing = Read-Utf8 -Path $Path

    $block = "`n$start`n`n$Content`n`n$end`n"
    $pattern = "(?s)" + [regex]::Escape($start) + ".*?" + [regex]::Escape($end)

    if ($existing -match $pattern) {
        $updated = [regex]::Replace($existing, $pattern, $block.Trim())
        Write-Host "Replaced routing block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block
        Write-Host "Added routing block in $Path"
    }

    Write-Utf8Lf -Path $Path -Content $updated
}

function Add-IfExists {
    param([Parameter(Mandatory=$true)][string]$Path)
    if (Test-Path $Path) {
        git add $Path
    }
}

Write-Host "Repo root: $(Get-Location)"

$obsDir = "docs/exterior-observations/commercial-surface"
$commercialDir = "docs/commercial"

New-Item -ItemType Directory -Force -Path $obsDir | Out-Null
New-Item -ItemType Directory -Force -Path $commercialDir | Out-Null

$perplexityPath = "$obsDir/PERPLEXITY_COMMERCIAL_SURFACE_BUYER_READINESS_REVIEW_v0_1.md"
$copilotPath = "$obsDir/COPILOT_COMMERCIAL_SURFACE_BUYER_READINESS_REVIEW_v0_1.md"
$indexPath = "$obsDir/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md"
$quickStartPath = "$commercialDir/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md"
$sweepPath = "$commercialDir/COMMERCIAL_SURFACE_LANGUAGE_SWEEP_v0_1.md"

$perplexity = @"
# Perplexity Commercial Surface Buyer Readiness Review v0.1

Status: Exterior commercial-surface review.  
Source: Perplexity.  
Review type: Buyer-readiness / commercial-surface interpretation review.  
Execution status: No checker execution or recomputation claimed.  
Scope: Buyer-facing clarity, commercial routing, CISO / risk / legal interpretation, maturity posture, and residual overclaim risk.  
Classification: Exterior observation, not authority.

## Non-endorsement and non-claims capsule

This exterior review is not an endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, compliance conclusion, procurement conclusion, audit conclusion, or control-effectiveness conclusion.

The review is preserved as an external interpretation of Fork's commercial surface. It does not establish that Fork is complete, correct, compliant, legally sufficient, production ready, secure, approved, or suitable for any specific deployment.

External citations included in the source response are preserved only as part of the received review text. They are not adopted by Fork as authority.

## Executive verdict received

Nearly ready.

## Strengths identified

1. Clear boundary positioning. The commercial surface was read as framing Fork as evidence-boundary infrastructure rather than a runtime control plane or compliance suite.
2. Buyer-oriented routing and packaging. The repository was read as increasingly navigable for GC, CISO, risk, and compliance audiences.
3. Explicit maturity signaling. The post-v0.1 and design-partner posture was read as avoiding enterprise-ready or production-scale overclaim.

## Remaining issues identified

1. Residual compliance-like phrasing risk. Terms such as audit trail, evidence store, or control evidence may be read as compliance-system or audit-system function.
2. Reliance boundary could be more explicit and repeated.
3. CISO / security framing should be distinguished from SIEM, logging, GRC, detection controls, and security telemetry.

## Fork interpretation

This review is useful as commercial-surface feedback. It must not be cited as recomputation, validation, certification, endorsement, buyer approval, production readiness, legal sufficiency, or compliance sufficiency.

The preserved signal is that remaining commercial risk is interpretive: buyer-facing language and routing should reduce opportunities for GC / CISO / risk / audit readers to misclassify Fork as a SIEM, GRC system, audit log-of-record, compliance evidence store, or control platform.
"@

$copilot = @"
# Co-Pilot Commercial Surface Buyer Readiness Review v0.1

Status: Exterior commercial-surface review.  
Source: Co-Pilot.  
Review type: Buyer-readiness / commercial-surface interpretation review.  
Execution status: No checker execution or recomputation claimed.  
Scope: Buyer-facing clarity, commercial routing, legal / security ambiguity, reviewer friction, and maturity posture.  
Classification: Exterior observation, not authority.

## Non-endorsement and non-claims capsule

This exterior review is not an endorsement, validation, certification, approval, production-readiness assessment, legal conclusion, compliance conclusion, procurement conclusion, audit conclusion, or control-effectiveness conclusion.

The review is preserved as an external interpretation of Fork's commercial surface. It does not establish that Fork is complete, correct, compliant, legally sufficient, production ready, secure, approved, or suitable for any specific deployment.

External citations included in the source response are preserved only as part of the received review text. They are not adopted by Fork as authority.

## Executive verdict received

Nearly ready.

The commercial tree was read as clear, bounded, and buyer-appropriate, but wording and navigation fixes were recommended to reduce legal / security ambiguity and reviewer friction.

## Strengths identified

1. Clear boundary posture. Fork is repeatedly framed as a read-only evidence hand-off and its non-claims are explicit.
2. Audience alignment. Executive, buyer, and CISO / security audiences are named in a way that helps route stakeholder concerns.
3. Doctrinal backing. The white paper and reading guide help legal / risk reviewers understand the reconstructive-fidelity basis for Fork's constraints.

## Remaining issues identified

1. Residual language can read as capability claims. Terms such as verification and receipt-binding need immediate qualifiers in buyer-facing contexts.
2. Navigation ambiguity remains for non-technical reviewers.
3. Illustrative reviewer packet examples can be misread as production templates unless clearly labeled non-binding / demo only.

## Fork interpretation

This review is useful as commercial-surface feedback. It must not be cited as recomputation, validation, certification, endorsement, buyer approval, production readiness, legal sufficiency, or compliance sufficiency.

The preserved signal is that buyer-facing navigation should route non-technical reviewers to a single bounded first-read path before they encounter technical artifacts, release notes, checkers, schemas, or implementation detail.
"@

$index = @"
# Commercial Surface Buyer Readiness Observation Index v0.1

Status: Exterior observation index.  
Scope: Commercial-surface buyer-readiness reviews received during post-v0.1 repository hardening.  
Classification: Observation index, not authority.

## Non-endorsement and non-claims capsule

This index does not endorse Fork, validate Fork, certify Fork, approve Fork, establish production readiness, establish legal sufficiency, establish compliance sufficiency, or conclude suitability for any buyer, sector, deployment, or control environment.

The listed reviews are preserved as exterior observations. They are not recomputation receipts, execution receipts, certifications, legal opinions, compliance opinions, procurement approvals, audit conclusions, or security-control assessments.

External citations embedded in source review text are preserved only as part of received observations and are not adopted as Fork authority.

## Filed observations

1. [Perplexity Commercial Surface Buyer Readiness Review v0.1](PERPLEXITY_COMMERCIAL_SURFACE_BUYER_READINESS_REVIEW_v0_1.md)
2. [Co-Pilot Commercial Surface Buyer Readiness Review v0.1](COPILOT_COMMERCIAL_SURFACE_BUYER_READINESS_REVIEW_v0_1.md)

## Shared exterior signal

Both exterior commercial-surface reviews converged on the same high-level posture:

- Overall status: nearly ready.
- Core architecture: generally understood as bounded evidence-preservation infrastructure.
- Main remaining risk: interpretive overread by GC, CISO, risk, compliance, audit, or procurement-adjacent readers.
- Required cleanup: commercial language and buyer routing, not core architecture.

## Review-use guidance

These exterior reviews may be cited only as evidence that external systems/readers identified buyer-facing clarity issues and suggested bounded commercial-surface improvements.

They must not be cited as proof that Fork is ready for production, legally sufficient, compliant, secure, endorsed, certified, validated, approved, or procurement-ready.
"@

$quickStart = @"
# Buyer Quick Start for GC / CISO / Risk v0.1

Status: Buyer-facing orientation guide.  
Audience: General Counsel, CISO / security leadership, risk leadership, compliance leadership, audit-adjacent reviewers, and design-partner evaluators.  
Scope: Commercial first-read path for Fork's evidence-boundary posture.  
Classification: Orientation surface, not certification.

## Buyer note

Fork preserves reconstructable evidence context for AI-assisted reliance.

Fork does not certify compliance, establish legal admissibility, replace institutional controls, operate detection systems, function as a GRC system, replace SIEM or logging platforms, or act as a runtime control plane.

## What Fork is

Fork is evidence-boundary infrastructure for AI-assisted workflows.

It preserves the context needed to reconstruct what was requested, what AI-assisted artifact was produced, what humans reviewed or changed, what was relied upon, what was not relied upon, what authority was referenced, what authority was not transferred, what non-claims were preserved, and whether a sealed record still structurally verifies later.

## What Fork is not

Fork is not a runtime control plane, policy engine, compliance oracle, legal-admissibility engine, SIEM, security telemetry platform, GRC system, system-wide audit log, approval workflow, control-effectiveness assessment, production-readiness certification, or substitute for institutional decision authority.

## Reliance boundary

A reliance boundary is the point at which an AI-assisted artifact is treated as something a person, team, workflow, or downstream record depends on.

Examples include citation in an approval memo, inclusion in a case file, use in a vendor-risk recommendation, attachment to a decision record, or reference during an investigation or risk review.

Fork does not decide what should be relied upon. Fork preserves the reconstructable context around what was in fact relied upon, what was not relied upon, and whether the sealed record still structurally verifies later.

## CISO / security distinction

Fork does not collect security telemetry, operate detection controls, replace SIEM tooling, or function as a GRC system.

Security leadership may use Fork to reconstruct AI-assisted reliance context during investigations, postmortems, risk reviews, and control-design discussions, alongside existing SIEM, logging, GRC, and compliance systems.

## Commercial maturity posture

This package describes an emerging evidence-boundary infrastructure pattern under active development with design partners.

It is not a completed enterprise compliance product, production control system, legal-sufficiency engine, audit certification package, or procurement-ready control framework.

## Recommended first-read path

Read these first:

1. [Buyer overview](BUYER_OVERVIEW_v0_1.md)
2. [Commercial README](README.md)
3. [Public review package index](../PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md)

Then, if the boundary posture is relevant, review the technical or recomputation materials through the public review index rather than treating the repository as a single undifferentiated proof surface.

## What not to infer

Do not infer from Fork materials that an AI-assisted decision was correct, an artifact was legally sufficient, a control operated effectively, a compliance obligation was satisfied, an approval occurred, a reviewer endorsed the system, structural verification proves truth, recomputation proves production readiness, or a preserved observation is a certification.

## Good buyer question

Where in our AI-assisted workflow does an artifact become relied upon, and what would a later reviewer need in order to reconstruct that reliance without trusting memory, screenshots, or a live system?
"@

$sweep = @"
# Commercial Surface Language Sweep v0.1

Status: Language sweep report.  
Scope: README, docs/commercial, and public review index.  
Interpretation: A listed term is not automatically a defect. Buyer-facing uses of these terms should be checked for nearby boundary qualifiers.

## Terms to watch

- audit log
- audit trail
- evidence store
- control evidence
- compliance evidence
- verification
- receipt-binding
- non-repudiation
- production boundary
- production-ready
- validated
- certified
- approved
- SIEM
- GRC

## Replacement pattern

Prefer bounded phrases such as sealed reliance record, context-preserving record, evidence-boundary record, reconstructable reliance context, structural verification record, or evidence hand-off boundary.

## Review note

This sweep is intended to reduce buyer misclassification risk.

It does not establish compliance, non-compliance, legal sufficiency, security sufficiency, production readiness, or control effectiveness.
"@

Write-Utf8Lf -Path $perplexityPath -Content $perplexity
Write-Utf8Lf -Path $copilotPath -Content $copilot
Write-Utf8Lf -Path $indexPath -Content $index
Write-Utf8Lf -Path $quickStartPath -Content $quickStart
Write-Utf8Lf -Path $sweepPath -Content $sweep

Write-Host "Created: $perplexityPath"
Write-Host "Created: $copilotPath"
Write-Host "Created: $indexPath"
Write-Host "Created: $quickStartPath"
Write-Host "Created: $sweepPath"

$readmeBlock = @"
## Buyer-facing overview (GC / CISO / Risk)

For legal, security, risk, compliance, audit-adjacent, and design-partner readers, start here:

- [Buyer Quick Start for GC / CISO / Risk v0.1](docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Fork preserves reconstructable evidence context for AI-assisted reliance. It does not certify compliance, establish legal admissibility, replace institutional controls, operate detection systems, function as a GRC system, replace SIEM or logging platforms, or act as a runtime control plane.
"@

Replace-OrAppendBlock -Path "README.md" -BlockId "FORK_BUYER_QUICK_START_GC_CISO_RISK" -Content $readmeBlock

$commercialBlock = @"
## Buyer note

Fork preserves reconstructable evidence context for AI-assisted reliance.

Fork does not certify compliance, establish legal admissibility, replace institutional controls, operate detection systems, function as a GRC system, replace SIEM or logging platforms, or act as a runtime control plane.

Start here:

- [Buyer Quick Start for GC / CISO / Risk v0.1](BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

## Reliance boundary

A reliance boundary is the point at which an AI-assisted artifact is treated as something a person, team, workflow, or downstream record depends on.

Fork does not decide what should be relied upon. Fork preserves the reconstructable context around what was in fact relied upon, what was not relied upon, and whether the sealed record still structurally verifies later.

## CISO / security distinction

Fork does not collect security telemetry, operate detection controls, replace SIEM tooling, or function as a GRC system.

Security leadership may use Fork to reconstruct AI-assisted reliance context during investigations, postmortems, risk reviews, and control-design discussions, alongside existing SIEM, logging, GRC, and compliance systems.
"@

Replace-OrAppendBlock -Path "docs/commercial/README.md" -BlockId "FORK_COMMERCIAL_BUYER_NOTE_AND_RELIANCE_BOUNDARY" -Content $commercialBlock
Replace-OrAppendBlock -Path "docs/commercial/index.md" -BlockId "FORK_COMMERCIAL_BUYER_NOTE_AND_RELIANCE_BOUNDARY" -Content $commercialBlock

$publicIndexBlock = @"
## Buyer-facing commercial surface

For GC, CISO, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers:

- [Buyer Quick Start for GC / CISO / Risk v0.1](commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Commercial-surface exterior observations are preserved here:

- [Commercial Surface Buyer Readiness Observation Index v0.1](exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md)

These observations are buyer-surface interpretation reviews only. They are not endorsements, validations, certifications, approvals, production-readiness assessments, legal conclusions, compliance conclusions, procurement conclusions, audit conclusions, or control-effectiveness conclusions.
"@

Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" -BlockId "FORK_COMMERCIAL_SURFACE_BUYER_READINESS_ROUTING" -Content $publicIndexBlock

$reviewerStartBlock = @"
## Commercial / buyer-facing review path

For GC, CISO, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers:

- [Buyer Quick Start for GC / CISO / Risk v0.1](commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Exterior commercial-surface reviews are preserved as observations, not endorsements or certifications:

- [Commercial Surface Buyer Readiness Observation Index v0.1](exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md)
"@

Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" -BlockId "FORK_COMMERCIAL_BUYER_REVIEW_PATH" -Content $reviewerStartBlock

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "SHA-256:"
if (Get-Command certutil.exe -ErrorAction SilentlyContinue) {
    certutil -hashfile $perplexityPath SHA256
    certutil -hashfile $copilotPath SHA256
    certutil -hashfile $quickStartPath SHA256
    certutil -hashfile $sweepPath SHA256
}

if ($Commit) {
    Add-IfExists $perplexityPath
    Add-IfExists $copilotPath
    Add-IfExists $indexPath
    Add-IfExists $quickStartPath
    Add-IfExists $sweepPath
    Add-IfExists "README.md"
    Add-IfExists "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md"
    Add-IfExists "docs/REVIEWER_START_HERE_v0_1.md"
    Add-IfExists "docs/commercial/README.md"
    Add-IfExists "docs/commercial/index.md"
    Add-IfExists "scripts/add_commercial_surface_exterior_reviews_v0_1.ps1"

    git commit -m "Add commercial surface exterior reviews and buyer quick start"

    if ($Push) {
        git push
    }
}

Write-Host ""
Write-Host "Done."