param(
    [string]$Root = ".",
    [string]$CommitMessage = "Wire modular surface into reviewer path",
    [switch]$AllowDirty,
    [switch]$SkipAddScript,
    [switch]$NoPush
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path -LiteralPath $Root).Path

function Require-GitRepo {
    $Inside = git -C $RepoRoot rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -ne 0 -or $Inside.Trim() -ne "true") {
        throw "Not inside a Git repository: $RepoRoot"
    }
}

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    $FullPath = [System.IO.Path]::GetFullPath($Path)
    $Parent = Split-Path -Parent $FullPath

    if (-not (Test-Path -LiteralPath $Parent)) {
        New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    }

    $Normalized = $Text -replace "`r`n", "`n"
    $Normalized = $Normalized -replace "`r", "`n"
    $Normalized = $Normalized.TrimEnd() + "`n"

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($FullPath, $Normalized, $Utf8NoBom)
}

function Read-RepoText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "Missing expected file: $Path"
    }

    return [System.IO.File]::ReadAllText([System.IO.Path]::GetFullPath($Path))
}

function Upsert-MarkedSection {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Marker,

        [Parameter(Mandatory = $true)]
        [string]$Section,

        [switch]$AtTop
    )

    $Start = "<!-- $Marker`:START -->"
    $End = "<!-- $Marker`:END -->"

    $Text = Read-RepoText -Path $Path
    $SectionBlock = "$Start`n$($Section.TrimEnd())`n$End"

    $EscapedStart = [regex]::Escape($Start)
    $EscapedEnd = [regex]::Escape($End)
    $Pattern = "(?s)$EscapedStart.*?$EscapedEnd"

    if ($Text -match $Pattern) {
        $Updated = [regex]::Replace($Text, $Pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $SectionBlock })
    }
    elseif ($AtTop) {
        $Updated = "$SectionBlock`n`n$Text"
    }
    else {
        $Updated = $Text.TrimEnd() + "`n`n" + $SectionBlock + "`n"
    }

    Write-Utf8NoBomLf -Path $Path -Text $Updated
    Write-Host "Updated $Path" -ForegroundColor Green
}

function Assert-NoOddMarkdownFences {
    param(
        [string[]]$Paths
    )

    foreach ($Path in $Paths) {
        if (Test-Path -LiteralPath $Path) {
            $Count = @(Select-String -Path $Path -Pattern '^```').Count
            Write-Host "$Path fence count: $Count"
            if (($Count % 2) -ne 0) {
                throw "Odd markdown code-fence count detected in $Path"
            }
        }
    }
}

Require-GitRepo

$ReadmePath = Join-Path $RepoRoot "README.md"
$ReviewerStartPath = Join-Path $RepoRoot "docs\REVIEWER_START_HERE_v0_1.md"
$PublicReviewIndexPath = Join-Path $RepoRoot "docs\PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md"
$SurfaceDoctrinePath = Join-Path $RepoRoot "docs\README_SURFACE_DOCTRINE.md"
$CrosswalkPath = Join-Path $RepoRoot "docs\modular-surface\FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md"
$OrphanDraftPath = Join-Path $RepoRoot "README_SURFACE_TOP_LAYER_DRAFT.md"

$PlannedExistingPaths = @(
    "README.md",
    "docs\REVIEWER_START_HERE_v0_1.md",
    "docs\PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
    "docs\README_SURFACE_DOCTRINE.md",
    "README_SURFACE_TOP_LAYER_DRAFT.md"
) | Where-Object { Test-Path -LiteralPath (Join-Path $RepoRoot $_) }

if (-not $AllowDirty) {
    $DirtyTargets = git -C $RepoRoot status --porcelain -- $PlannedExistingPaths
    if ($DirtyTargets) {
        Write-Host "Dirty planned target files detected:" -ForegroundColor Yellow
        $DirtyTargets | ForEach-Object { Write-Host $_ }
        throw "Refusing to continue with dirty planned target files. Commit/stash them first, or rerun with -AllowDirty."
    }

    git -C $RepoRoot diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Refusing to continue because staged changes already exist. Commit/stash them first, or rerun with -AllowDirty."
    }
}

$CrosswalkContent = @'
# Fork Modular Surface Crosswalk v0.1

## Purpose

This document maps Fork's six functional surfaces to existing doctrine, schemas, examples, simulations, and enforcement surfaces.

It exists so reviewers can read the Modular Surface as a concordance across existing work rather than as a competing taxonomy.

The Modular Surface does not replace existing Fork artifacts. It provides a functional map over them.

## Governing Constraint

All surfaces remain governed by preservation without inheritance.

Fork may preserve, reference, inspect, recompute, and reconstruct evidence-boundary records.

Fork does not absorb external authority or convert structural verification into truth, approval, compliance, admissibility, legal sufficiency, safety, or downstream decision correctness.

## Surface-to-Artifact Crosswalk

| Modular surface | Existing repo line | Current enforcement posture |
|---|---|---|
| Evidence Boundary | Claim Boundary Contract line, Required Source Non-Claims, Provenance Tier, Relational Graph Verifier | Checker/CI-backed across core evidence-boundary artifacts |
| Transition | Boundary Delta Record, Transition Integrity materials | Fixture/checker-backed where BDR applies; not yet surfaced as modular-surface enforcement |
| Reliance | Claim Consumption Events, System Mapping Receipt | Checker-backed in existing lines; not yet wired to the modular surface contract |
| Interoperability | CCEC Governance Interoperability Profile, GLM declaration, system mapping materials | Checker-backed in existing profile lines; modular-surface interaction rules not yet separately enforced |
| Simulation | Governance proof-surface scenarios, claim-inheritance simulations, ESAL/RGV-related replay materials | Partially CI-backed through simulation checkers and scenario fixtures |
| Commercial | docs/commercial/*, buyer/discovery materials | Narrative only by design; derivative of technical surfaces |

## Reading Guidance

The crosswalk should be read as a map from function to implementation.

It does not imply that every surface has the same maturity level.

It also does not imply that every surface currently has a dedicated schema, fixture set, checker, or CI workflow.

Fork's recurring hardening pattern remains:

1. Doctrine
2. Schema
3. Fixtures
4. Checker
5. CI
6. Reviewer-facing evidence

The Surface Interaction Contract is currently at the doctrine/design-control stage. Its candidate machine-readable constraints are intended to guide a later schema and fixture pass.

## Reconciling Existing Fork Models

Fork currently contains several organizing models. They are not equivalent, and they should not be read as competing definitions.

### Conceptual Stack

The Conceptual Stack describes dependency order: independent establishment, recomputable evidence, preservation without inheritance, transition integrity, and bounded propagation.

### Six-Layer Evidentiary Model

The Six-Layer Evidentiary Model describes evidentiary interpretation layers: content, attribution, mechanical status, inference boundary, resolution authority, and resolution history.

### Surface Doctrine

The earlier Surface Doctrine describes audience-facing lanes: Reviewer, Pilot, and Proof.

### Reviewer Artifact Set

The Reviewer Artifact Set describes reviewable artifact forms: Evidence Card, Boundary Map, Verification Receipt, Review Packet, and Non-Claim Panel.

### Modular Surface

The Modular Surface describes functional architecture: Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial.

These are different axes.

A reviewer-facing proof artifact may exercise one or more functional surfaces, but audience routing does not define Fork's internal modular architecture.

## Surface Doctrine Reconciliation

The earlier Surface Doctrine remains useful as an audience-lane model.

The Modular Surface is the functional architecture model.

A Proof-surface artifact, for example, may belong to the Simulation Surface if it demonstrates a valid or invalid recomposition. It may also reference the Evidence Boundary Surface if it includes structural verification material.

The important distinction is:

- Surface Doctrine answers: who is this material for?
- Modular Surface answers: what functional role does this material play?

## Next Hardening Milestone

The next natural hardening step is to convert the Surface Interaction Contract into a minimal schema and fixture set.

A small first pass should include:

1. A valid interaction fixture.
2. A Rule 1 Evidence Boundary immutability violation.
3. A Non-Absorption Test failure.
4. A checker that returns structural outcomes only.

This should remain bounded. The checker should not produce truth, approval, compliance, safety, admissibility, legal sufficiency, or authority outcomes.

## Status Boundary

This crosswalk is a reviewer-orientation artifact.

It does not add new authority to Fork.

It does not certify any workflow, artifact, model, organization, policy, or decision.

It maps current repo structure so Fork's existing artifacts can be reviewed as a coherent evidence-boundary architecture.
'@

Write-Utf8NoBomLf -Path $CrosswalkPath -Text $CrosswalkContent
Write-Host "Created $CrosswalkPath" -ForegroundColor Green

$ReadmeSection = @'
## Fork Modular Surface

Fork's current architecture is organized through a modular evidence-boundary surface.

The six functional surfaces are:

- Evidence Boundary
- Transition
- Reliance
- Interoperability
- Simulation
- Commercial

These surfaces are governed by a single constraint: preservation without inheritance.

Fork may preserve, reference, inspect, and reconstruct evidence-boundary records, but it does not absorb external authority or convert structural verification into truth, approval, compliance, admissibility, legal sufficiency, or downstream decision correctness.

Start here:

- `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
- `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
'@

$ReviewerStartSection = @'
## Modular Surface Reading Path

Fork now includes a dedicated modular surface architecture.

Reviewers should read these documents as the current functional map of Fork's evidence-boundary architecture:

1. `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
2. `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
3. `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`

The Modular Surface does not replace existing Fork artifacts.

It explains how existing doctrine, checkers, simulations, review packets, interoperability materials, and commercial-facing documents relate across six functional surfaces: Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial.

Its governing constraint is preservation without inheritance.
'@

$PublicReviewIndexSection = @'
## Modular Surface Package

The Modular Surface package provides the current functional map for Fork's evidence-boundary architecture.

Reviewers should use it to understand how Fork separates Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial surfaces without transferring authority across them.

Package files:

- `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
- `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
'@

$SurfaceDoctrineSection = @'
## Audience Surfaces and Functional Surfaces

This document describes audience-facing lanes: Reviewer, Pilot, and Proof.

The Modular Surface describes functional architecture: Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial.

These are different axes.

A reviewer-facing proof artifact may exercise one or more functional surfaces, but audience routing does not define Fork's internal modular architecture.

See:

- `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
- `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
'@

Upsert-MarkedSection -Path $ReadmePath -Marker "FORK-MODULAR-SURFACE-README" -Section $ReadmeSection
Upsert-MarkedSection -Path $ReviewerStartPath -Marker "FORK-MODULAR-SURFACE-REVIEWER-PATH" -Section $ReviewerStartSection
Upsert-MarkedSection -Path $PublicReviewIndexPath -Marker "FORK-MODULAR-SURFACE-PUBLIC-INDEX" -Section $PublicReviewIndexSection

if (Test-Path -LiteralPath $SurfaceDoctrinePath) {
    Upsert-MarkedSection -Path $SurfaceDoctrinePath -Marker "FORK-MODULAR-SURFACE-RECONCILIATION" -Section $SurfaceDoctrineSection
}

if (Test-Path -LiteralPath $OrphanDraftPath) {
    $DraftNote = @'
> Status: Superseded public-surface draft.
>
> This root-level draft is retained only as historical drafting material. For the current modular evidence-boundary architecture, use:
>
> - `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
> - `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
> - `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
'@

    Upsert-MarkedSection -Path $OrphanDraftPath -Marker "FORK-SUPERSEDED-DRAFT-NOTE" -Section $DraftNote -AtTop
}

$MarkdownPaths = @(
    $ReadmePath,
    $ReviewerStartPath,
    $PublicReviewIndexPath,
    $SurfaceDoctrinePath,
    $CrosswalkPath,
    $OrphanDraftPath
) | Where-Object { Test-Path -LiteralPath $_ }

Assert-NoOddMarkdownFences -Paths $MarkdownPaths

Write-Host ""
Write-Host "Checking diff whitespace..." -ForegroundColor Cyan
git -C $RepoRoot diff --check -- $MarkdownPaths
if ($LASTEXITCODE -ne 0) {
    throw "git diff --check failed."
}

$AddPaths = @(
    "README.md",
    "docs\REVIEWER_START_HERE_v0_1.md",
    "docs\PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
    "docs\modular-surface\FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md"
)

if (Test-Path -LiteralPath $SurfaceDoctrinePath) {
    $AddPaths += "docs\README_SURFACE_DOCTRINE.md"
}

if (Test-Path -LiteralPath $OrphanDraftPath) {
    $AddPaths += "README_SURFACE_TOP_LAYER_DRAFT.md"
}

if (-not $SkipAddScript) {
    $ScriptPath = $MyInvocation.MyCommand.Path
    if ($ScriptPath) {
        $FullScriptPath = [System.IO.Path]::GetFullPath($ScriptPath)
        if ($FullScriptPath.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            $RelativeScriptPath = $FullScriptPath.Substring($RepoRoot.Length).TrimStart('\', '/')
            $AddPaths += $RelativeScriptPath
        }
    }
}

Write-Host ""
Write-Host "Staging planned files..." -ForegroundColor Cyan
git -C $RepoRoot add -- $AddPaths

$StagedFiles = git -C $RepoRoot diff --cached --name-only
if (-not $StagedFiles) {
    Write-Host "No staged changes detected. Nothing to commit." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Staged files:" -ForegroundColor Cyan
$StagedFiles | ForEach-Object { Write-Host " - $_" }

Write-Host ""
Write-Host "Commit diff stat:" -ForegroundColor Cyan
git -C $RepoRoot diff --cached --stat

Write-Host ""
Write-Host "Committing..." -ForegroundColor Cyan
git -C $RepoRoot commit -m $CommitMessage

if (-not $NoPush) {
    Write-Host ""
    Write-Host "Pushing..." -ForegroundColor Cyan
    git -C $RepoRoot push
}
else {
    Write-Host "NoPush specified; skipping git push." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Final status:" -ForegroundColor Cyan
git -C $RepoRoot status -sb
