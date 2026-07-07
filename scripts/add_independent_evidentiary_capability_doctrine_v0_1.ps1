param(
    [string]$RepoRoot = "C:\N\fork-public-evidence",
    [string]$BranchName = "doctrine/independent-evidentiary-capability-v0-1",
    [switch]$AllowDirty,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

function Fail {
    param([string]$Message)
    throw $Message
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        Fail "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Get-Text {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }

    return [System.IO.File]::ReadAllText($Path)
}

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    $normalized = $normalized -replace "`r", "`n"

    if (-not $normalized.EndsWith("`n")) {
        $normalized = $normalized + "`n"
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $normalized, $encoding)
}

function Add-Unique {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Value
    )

    if (-not $List.Contains($Value)) {
        [void]$List.Add($Value)
    }
}

function Append-LightCrossLink {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,
        [Parameter(Mandatory = $true)]
        [string]$SectionText,
        [Parameter(Mandatory = $true)]
        [string]$Needle,
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.List[string]]$Touched
    )

    $path = Join-Path $RepoRoot $RelativePath

    if (-not (Test-Path -LiteralPath $path)) {
        Write-Host "Skipping missing file: $RelativePath"
        return
    }

    $existing = Get-Text -Path $path

    if ($existing -match [regex]::Escape($Needle)) {
        Write-Host "Cross-link already present: $RelativePath"
        return
    }

    $updated = $existing.TrimEnd() + "`n`n" + $SectionText.Trim() + "`n"
    Write-Utf8NoBomLf -Path $path -Content $updated

    Add-Unique -List $Touched -Value $RelativePath
    Write-Host "Updated cross-link: $RelativePath"
}

function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-OptionalChecks {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Files
    )

    Write-Host ""
    Write-Host "Running available checks..."

    Write-Host "Running git diff --check..."
    & git diff --check -- $Files
    if ($LASTEXITCODE -ne 0) {
        Fail "git diff --check failed"
    }

    if (Test-CommandExists "markdownlint-cli2") {
        Write-Host "Running markdownlint-cli2..."
        & markdownlint-cli2 $Files
        if ($LASTEXITCODE -ne 0) {
            Fail "markdownlint-cli2 failed"
        }
    }
    elseif (Test-CommandExists "markdownlint") {
        Write-Host "Running markdownlint..."
        & markdownlint $Files
        if ($LASTEXITCODE -ne 0) {
            Fail "markdownlint failed"
        }
    }
    else {
        Write-Host "No markdownlint command found; skipping markdown lint."
    }

    $linkCheckScripts = @(
        "scripts\check_markdown_links.ps1",
        "scripts\check_links.ps1",
        "scripts\run_markdown_link_checks.ps1"
    )

    $ranLinkScript = $false

    foreach ($candidate in $linkCheckScripts) {
        $candidatePath = Join-Path $RepoRoot $candidate
        if (Test-Path -LiteralPath $candidatePath) {
            Write-Host "Running link check script: $candidate"
            powershell -ExecutionPolicy Bypass -File $candidatePath
            if ($LASTEXITCODE -ne 0) {
                Fail "$candidate failed"
            }
            $ranLinkScript = $true
            break
        }
    }

    if (-not $ranLinkScript) {
        if (Test-CommandExists "lychee") {
            Write-Host "Running lychee on changed markdown files..."
            & lychee $Files
            if ($LASTEXITCODE -ne 0) {
                Fail "lychee failed"
            }
        }
        else {
            Write-Host "No repo link-check script or lychee command found; skipping link check."
        }
    }
}

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    Fail "Repo root does not exist: $RepoRoot"
}

Push-Location $RepoRoot

try {
    Invoke-Git @("rev-parse", "--show-toplevel") | Out-Null

    $preStatus = (& git status --porcelain)
    if ($preStatus -and -not $AllowDirty) {
        Write-Host "Working tree has existing changes:"
        Write-Host $preStatus
        Fail "Refusing to mix doctrine update with existing changes. Re-run with -AllowDirty to override."
    }

    $currentBranch = (& git branch --show-current).Trim()

    if ($currentBranch -ne $BranchName) {
        $localBranch = (& git branch --list $BranchName).Trim()

        if ($localBranch) {
            Write-Host "Switching to existing branch: $BranchName"
            Invoke-Git @("switch", $BranchName)
        }
        else {
            Write-Host "Creating branch: $BranchName"
            Invoke-Git @("switch", "-c", $BranchName)
        }
    }
    else {
        Write-Host "Already on branch: $BranchName"
    }

    $Touched = New-Object System.Collections.Generic.List[string]

    $DoctrineRel = "docs/doctrine/FORK_INDEPENDENT_EVIDENTIARY_CAPABILITY_v0_1.md"
    $DoctrinePath = Join-Path $RepoRoot $DoctrineRel

    $DoctrineContent = @'
# Fork Independent Evidentiary Capability v0.1

## Status

This note records Fork's v0.1 doctrinal framing around
independent evidentiary capability.

It is bounded by the exterior recomputation evidence available to date,
especially the boundary-state interoperability checker and evidence packet
v0.1.1. It should not be read as a universal theorem about evidence systems
or as a claim that Fork proves truth, legal sufficiency, compliance, safety,
authorization, or institutional correctness.

## Observed Facts

Exterior recomputation evidence has demonstrated that independent reviewers,
using published Fork materials, have been able to:

- Verify artifact integrity by recomputing hashes and comparing them against
  manifests and SHA inventories for published ZIP artifacts, including the
  profile, checker, and adversarial payload pack.
- Reconstruct the intended checker environment from authoritative source
  artifacts, including nested source artifacts under `source_artifacts/`.
- Produce a clean reconstructed checker tree with the expected topology,
  including profile materials, adversarial payloads, reviewer regressions,
  receipts, tests, tools, schemas, and fixtures.
- Execute the checker in an external environment and reproduce expected
  structural outcomes on canonical and adversarial suites.
- Perform those steps without relying on the originating development machine
  or unpublished local state.

These are observed facts about demonstrated packets and runs. They do not
assert that every future Fork packet is automatically independently
recomputable.

## Architectural Principle

Fork is infrastructure for preserving independent evidentiary capability.

The central architectural object is not only the artifact, manifest, hash,
receipt, or checker. The object is the ability of an independent party to
reconstruct, verify, and exercise the evidence system from published materials
after the evidence leaves the institution, environment, or author that
produced it.

Fork preserves the conditions under which governance evidence can remain
independently evaluable after it leaves the institution, environment, or
author that produced it.

## Purpose

Fork helps trust migrate from institutional assertion toward reproducible
evidence.

This does not mean institutions are unnecessary or unimportant. It means the
amount of institutional trust required to evaluate governance evidence can be
reduced when independent parties can reconstruct, verify, and exercise the
published evidence system for themselves.

The desired confidence target is not "trust Fork" or "trust the author."
The desired confidence target is evidence that remains structurally
evaluable through independent recomputation.

## Evidential Publication

Fork distinguishes public access from evidential completeness.

- Public access means artifacts are available to download or inspect.
- Evidential completeness means independent recomputation is achievable from
  the published artifacts.

Publication is evidentially complete when independent recomputation is
achievable from the published artifacts.

For a Fork packet, evidential completeness requires at least a plausible and
documented path for an external party to:

- Verify integrity from manifests, hashes, and SHA inventories.
- Reconstruct the intended environment topology from authoritative source
  artifacts rather than relying on convenience copies alone.
- Execute the relevant checker and fixtures.
- Observe expected structural behavior, including adversarial rejection where
  applicable.

Exterior recomputation receipts are proof objects showing that this threshold
has been met for a given packet or release surface.

## Four Preservation Functions

Fork's major components can be understood as serving four preservation
functions:

| Function | What Fork preserves |
| --- | --- |
| Meaning | Claims, non-claims, boundaries, semantic classes. |
| Context | Transitions, authority movement, reliance setting. |
| Verification | Hashes, manifests, checkers, receipts. |
| Independence | Reproduction guides, evidence packets, exterior recomputation. |

The fourth function, preserve independence, is the relevant v0.1 doctrinal
addition. Fork is not only preserving evidence and verification artifacts.
It is preserving the ability for an outside party to take possession of the
evidence system and exercise it independently.

## Independence Principle

The ability of independent parties to reconstruct, verify, and exercise a
Fork record increases confidence that the preserved evidence can be evaluated
without continued reliance on the originating authority.

This principle is intentionally bounded. It does not claim a formal
proportional law and does not imply that recomputation proves the truth,
safety, legality, compliance status, authorization, or institutional
correctness of the underlying activity.

It states that independent recomputation increases confidence that preserved
evidence can be structurally evaluated without continued dependence on the
originating institution, environment, or author.

## Non-Claims

Fork does not claim to:

- Prove truth.
- Prove legal sufficiency.
- Prove safety.
- Prove compliance.
- Provide authorization decisions.
- Provide production approvals.
- Act as a policy engine.
- Act as a compliance oracle.
- Guarantee institutional correctness.
- Transfer authority from one system to another.

Fork preserves the conditions under which evidence can be independently
reconstructed, inspected, executed, and structurally verified by others.

## Current Evidence

As of this v0.1 doctrine note, the primary evidence base for this framing is
the exterior recomputation of the boundary-state interoperability
profile/checker/evidence-packet family, including:

- Boundary-state interoperability profile v0.1.4.
- Boundary-state interoperability checker v0.1.1.
- Boundary-state interoperability evidence packet v0.1.1.
- Adversarial payload pack v0.1.0.
- Manifest and SHA inventory verification.
- Nested source-artifact extraction from `source_artifacts/`.
- Clean checker topology reconstruction.
- Matching structural verification outcomes in an external environment.

Future packets should be evaluated against the same bounded question:

Can an independent party, using only published artifacts, reconstruct, verify,
and exercise the evidence system without relying on the originating authority?
'@

    Write-Utf8NoBomLf -Path $DoctrinePath -Content $DoctrineContent
    Add-Unique -List $Touched -Value $DoctrineRel
    Write-Host "Created/updated doctrine file: $DoctrineRel"

    $RootLink = "docs/doctrine/FORK_INDEPENDENT_EVIDENTIARY_CAPABILITY_v0_1.md"
    $SurfaceLink = "../doctrine/FORK_INDEPENDENT_EVIDENTIARY_CAPABILITY_v0_1.md"
    $Needle = "FORK_INDEPENDENT_EVIDENTIARY_CAPABILITY_v0_1.md"

    $ReadmeSection = @"
## Doctrine

- [Independent Evidentiary Capability]($RootLink) describes Fork's evidence
  trust model: preserving the conditions under which governance evidence can
  remain independently evaluable after it leaves the institution, environment,
  or author that produced it.
"@

    Append-LightCrossLink `
        -RelativePath "README.md" `
        -SectionText $ReadmeSection `
        -Needle $Needle `
        -Touched $Touched

    $ReviewerSection = @"
## Independent Evidentiary Capability

For reviewers evaluating Fork's trust model, see
[Independent Evidentiary Capability]($RootLink). This doctrine note explains
why exterior recomputation matters and how Fork distinguishes public access
from evidential completeness.
"@

    Append-LightCrossLink `
        -RelativePath "REVIEWER_START_HERE_v0_1.md" `
        -SectionText $ReviewerSection `
        -Needle $Needle `
        -Touched $Touched

    $IndexSection = @"
## Independent Evidentiary Capability

The public review package includes a doctrine note on
[Independent Evidentiary Capability]($RootLink), which explains how exterior
recomputation receipts support Fork's evidential publication model.
"@

    Append-LightCrossLink `
        -RelativePath "PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
        -SectionText $IndexSection `
        -Needle $Needle `
        -Touched $Touched

    $SurfaceSection = @"
## Independent Evidentiary Capability

Fork's modular surfaces collectively support
[Independent Evidentiary Capability]($SurfaceLink): preserving meaning,
context, verification, and independence so governance evidence can remain
independently reconstructable, verifiable, and exercisable after it leaves
the institution, environment, or author that produced it.
"@

    Append-LightCrossLink `
        -RelativePath "docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md" `
        -SectionText $SurfaceSection `
        -Needle $Needle `
        -Touched $Touched

    $Files = @($Touched | Select-Object -Unique)

    if ($Files.Count -eq 0) {
        Write-Host "No files changed."
        Invoke-Git @("status", "-sb")
        exit 0
    }

    Invoke-OptionalChecks -Files $Files

    Write-Host ""
    Write-Host "Preparing diff..."
    & git add -N -- $Files 2>$null

    Write-Host ""
    Write-Host "git status -sb"
    Invoke-Git @("status", "-sb")

    Write-Host ""
    Write-Host "git diff --stat"
    & git diff --stat -- $Files

    Write-Host ""
    Write-Host "git diff"
    & git diff -- $Files

    Write-Host ""
    Write-Host "Staging files..."
    $addArgs = @("add", "--") + $Files
    Invoke-Git $addArgs

    $staged = (& git diff --cached --name-only)
    if (-not $staged) {
        Write-Host "No staged changes to commit."
        Invoke-Git @("status", "-sb")
        exit 0
    }

    Write-Host ""
    Write-Host "Staged files:"
    Write-Host $staged

    Invoke-Git @("commit", "-m", "Add independent evidentiary capability doctrine")

    if ($NoPush) {
        Write-Host "NoPush specified; skipping push."
    }
    else {
        Invoke-Git @("push", "-u", "origin", $BranchName)
    }

    Write-Host ""
    Write-Host "Done."
    Invoke-Git @("status", "-sb")
}
finally {
    Pop-Location
}