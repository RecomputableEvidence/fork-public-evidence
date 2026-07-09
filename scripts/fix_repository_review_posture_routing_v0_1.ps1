# scripts/fix_repository_review_posture_routing_v0_1.ps1
# Restores safe UTF-8/LF routing blocks without mojibake.
# PowerShell 5.1 compatible.

$ErrorActionPreference = "Stop"

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Utf8 {
    param([Parameter(Mandatory=$true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Add-RoutingBlock {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Title,
        [Parameter(Mandatory=$true)][string]$RelativeLink
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_START -->"
    $end = "<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_END -->"

    $existing = Read-Utf8 -Path $Path

    if ($existing -match [regex]::Escape($start)) {
        Write-Host "Routing block already present in $Path"
        return
    }

    $block = @"

$start

## Repository review posture

Fork's repository-specific review posture is maintained here:

- [$Title]($RelativeLink)

This guide explains how reviewers and contributors should interpret Fork artifacts, recomputation receipts, exterior observations, PR history, non-claims, and boundary-pressure concerns without converting evidence into authority, endorsement, certification, production readiness, legal sufficiency, or compliance conclusions.

$end
"@

    $updated = $existing.TrimEnd() + "`n" + $block + "`n"
    Write-Utf8Lf -Path $Path -Content $updated
    Write-Host "Updated routing target: $Path"
}

if (-not (Test-Path "docs\review\FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md")) {
    throw "Missing posture file: docs\review\FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md"
}

Add-RoutingBlock `
    -Path "README.md" `
    -Title "Fork Repository Review Posture v0.1" `
    -RelativeLink "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md"

Add-RoutingBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -Title "Fork Repository Review Posture v0.1" `
    -RelativeLink "review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md"

Add-RoutingBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -Title "Fork Repository Review Posture v0.1" `
    -RelativeLink "review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md"

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Done."
