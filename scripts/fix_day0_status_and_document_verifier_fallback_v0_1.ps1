# scripts/fix_day0_status_and_document_verifier_fallback_v0_1.ps1
# Fixes Day-0 stale status contradictions and documents public verifier platform fallback.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF.

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

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Replace-OrAppendBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BlockId,
        [Parameter(Mandatory = $true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start    = "<!-- $($BlockId):START -->"
    $end      = "<!-- $($BlockId):END -->"
    $existing = Read-Utf8 -Path $Path

$block = @"
$start

$Content

$end
"@

    $pattern = "(?s)" + [regex]::Escape($start) + ".*?" + [regex]::Escape($end)

    if ($existing -match $pattern) {
        $updated = [regex]::Replace($existing, $pattern, $block.Trim())
        Write-Host "Replaced routing block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block + "`n"
        Write-Host "Added routing block in $Path"
    }

    Write-Utf8Lf -Path $Path -Content $updated
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Python {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw "Python was not found on PATH."
    }

    & $python.Source @Args
    if ($LASTEXITCODE -ne 0) {
        throw "python $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Replace-StaleDay0Text {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing file: $Path"
        return
    }

    $text     = Read-Utf8 -Path $Path
    $original = $text

    $patterns = @(
        @{
            Pattern     = "(?im)^\s*[-*]\s*Day-0 fixture not yet implemented\.?\s*$"
            Replacement = "- Day-0 packet implemented at `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`; replay receipts are not yet implemented."
        },
        @{
            Pattern     = "(?im)^\s*[-*]\s*Day-0 packet not yet implemented\.?\s*$"
            Replacement = "- Day-0 packet implemented at `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`; replay receipts are not yet implemented."
        },
        @{
            Pattern     = "(?im)^\s*[-*]\s*Day-0 fixture is not yet implemented\.?\s*$"
            Replacement = "- Day-0 packet is implemented at `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`; replay receipts are not yet implemented."
        },
        @{
            Pattern     = "(?im)^\s*[-*]\s*Day-0 packet is not yet implemented\.?\s*$"
            Replacement = "- Day-0 packet is implemented at `docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/`; replay receipts are not yet implemented."
        },
        @{
            Pattern     = "(?i)Day-0 fixture not yet implemented"
            Replacement = "Day-0 packet implemented; replay receipts not yet implemented"
        },
        @{
            Pattern     = "(?i)Day-0 packet not yet implemented"
            Replacement = "Day-0 packet implemented; replay receipts not yet implemented"
        }
    )

    foreach ($item in $patterns) {
        $text = [regex]::Replace($text, $item.Pattern, $item.Replacement)
    }

    if ($text -ne $original) {
        Write-Utf8Lf -Path $Path -Content $text
        Write-Host "Patched stale Day-0 status language in $Path"
    } else {
        Write-Host "No stale Day-0 status phrase matched in $Path"
    }
}

Assert-RepoRoot

$scriptPath          = "scripts/fix_day0_status_and_document_verifier_fallback_v0_1.ps1"
$fallbackDocPath     = "docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md"
$responseReceiptPath = "docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md"
$verifierPath        = "scripts/verify_public_review_package_v0_1.ps1"

$fallbackDoc = @'
# Public Verifier Platform Fallback v0.1

Status: Public review accessibility note.
Scope: Platform fallback for reviewers who cannot execute the PowerShell public verifier.

## 1. Background

The primary public review verifier is:

- `scripts/verify_public_review_package_v0_1.ps1`

Run on Windows PowerShell or PowerShell Core:

- `powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1`
- `pwsh -File ./scripts/verify_public_review_package_v0_1.ps1`

Public Review Round 005 showed that a Linux reviewer may not have `pwsh` available. In that case, the reviewer cannot claim to have executed the named PowerShell verifier.

## 2. Fallback classification

If the PowerShell verifier cannot run, use this classification:

- manual public-verifier reconstruction

Do not classify it as:

- public verifier execution

Manual reconstruction is useful evidence, but it is not identical to running the named verifier artifact.

## 3. Linux/macOS fallback commands

From repo root, run:

```bash
git status -sb
git log -1 --oneline

python3 tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial
python3 tools/check_public_review_round_004_interactions_v0_1.py --json
python3 tools/check_public_review_round_005_interactions_v0_1.py --json
python3 tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

git diff --check
git diff --cached --check
```

If `python3` is unavailable but `python` is available, substitute `python`.

## 4. Expected current signals

Boundary pressure checker:

- default total: 4
- default passed: 4
- default failed: 0
- adversarial total: 4
- adversarial passed: 4
- adversarial failed: 0

Round 004 interaction checker:

- total: 4
- passed: 4
- failed: 0

Round 005 interaction checker:

- total: 1
- passed: 1
- failed: 0

Longitudinal Day-0 checker:

- total: 27
- passed: 27
- failed: 0

Git checks:

- `git diff --check` exits 0
- `git diff --cached --check` exits 0

## 5. What this fallback does not prove

This fallback does not execute the PowerShell verifier.
It reconstructs the underlying currently documented checker and Git conditions using cross-platform commands.
A reviewer should record: operating system; shell; Python version; Git version; whether `powershell` or `pwsh` was available; whether the PowerShell verifier actually executed; whether manual reconstruction was used instead.

## 6. Boundary statement

A successful fallback reconstruction does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
It only records that the reviewer independently executed the listed underlying checks in their environment.
'@

$responseReceipt = @'
Round 005 Response: Day-0 Status and Verifier Fallback v0.1
Status: Engineering response receipt.
Round: Public Review Round 005.
Response class: Documentation repair and access-path clarification.

1. Finding addressed

Round 005 found two immediate access-path defects:
- Read-first documents contained stale Day-0 status language stating that the Day-0 fixture was not yet implemented.
- The primary one-command public verifier path was PowerShell-only, with no documented Linux/macOS fallback for reviewers without `pwsh`.

2. Repair

This response:
- replaces stale Day-0 status language with the current status: Day-0 packet implemented, replay receipts not yet implemented;
- adds `docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md`;
- routes the fallback document through current proof surface, reviewer start, public review quickstart, public package index, and Round 005 synthesis context;
- preserves the distinction between executing the named PowerShell verifier and manually reconstructing its underlying checks.

3. Correct status after repair

Current Day-0 status:
- Day-0 packet: implemented.
- Day-0 checker: implemented.
- Day-0 replay receipt: not yet implemented.
- Day-7 / Day-30 / Day-90 replay receipts: not yet implemented.
- External anchoring: not yet implemented.
- Independent expected-reconstruction provenance: not yet implemented.

4. Correct fallback classification

When `scripts/verify_public_review_package_v0_1.ps1` cannot run because PowerShell or `pwsh` is unavailable, the review should be classified as:

- manual public-verifier reconstruction

It should not be classified as:

- public verifier execution

5. Non-authority statement

This response repairs documentation and reviewer-access guidance only. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
'@

Write-Utf8Lf -Path $fallbackDocPath     -Content $fallbackDoc
Write-Utf8Lf -Path $responseReceiptPath -Content $responseReceipt

Replace-StaleDay0Text -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md"
Replace-StaleDay0Text -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"

$fallbackRoutingBlock = @'
Public verifier platform fallback
Primary public verifier:
scripts/verify_public_review_package_v0_1.ps1
For Linux/macOS reviewers without PowerShell or pwsh, use:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Important distinction:
executing the PowerShell verifier is public verifier execution;
running the documented cross-platform commands is manual public-verifier reconstruction.
Manual reconstruction is useful review evidence, but it is not identical to executing the named verifier artifact.
'@

$currentProofBlock = @'
Day-0 status and verifier fallback repair
Round 005 identified stale Day-0 status language and a PowerShell-only verifier access gap.
Current status:
Day-0 packet: implemented.
Day-0 checker: implemented.
Day-0 replay receipt: not yet implemented.
Day-7 / Day-30 / Day-90 replay receipts: not yet implemented.
Platform fallback:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Response receipt:
docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md
Boundary:
manual public-verifier reconstruction is useful evidence but not identical to executing scripts/verify_public_review_package_v0_1.ps1.
neither path establishes truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, or institutional authority.
'@

$quickstartBlock = @'
Platform fallback for public verifier
Primary verifier path:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
If PowerShell / pwsh is unavailable, use:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Classification rule:
PowerShell verifier ran: public verifier execution.
Fallback commands ran: manual public-verifier reconstruction.
Do not describe fallback reconstruction as execution of the named PowerShell verifier.
'@

$indexBlock = @'
Public verifier platform fallback
Fallback guidance for reviewers without PowerShell / pwsh:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Round 005 response receipt:
docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md
'@

$round005Block = @'
Round 005 response: status repair and verifier fallback
Response receipt:
docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md
Public verifier fallback:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
This response fixes stale Day-0 status language and documents manual public-verifier reconstruction for reviewers who cannot execute the PowerShell verifier.
'@

Replace-OrAppendBlock -Path "README.md" `
    -BlockId "FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK" `
    -Content $fallbackRoutingBlock

Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK" `
    -Content $fallbackRoutingBlock

Replace-OrAppendBlock -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" `
    -BlockId "FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE" `
    -Content $currentProofBlock

Replace-OrAppendBlock -Path "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md" `
    -BlockId "FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK" `
    -Content $quickstartBlock

Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK" `
    -Content $indexBlock

Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md" `
    -BlockId "FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE" `
    -Content $round005Block

Replace-OrAppendBlock -Path "docs/review/public-rounds/round-005/README.md" `
    -BlockId "FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE" `
    -Content $round005Block

# Add new docs to public verifier coverage.
if (Test-Path $verifierPath) {
    $verifier = Read-Utf8 -Path $verifierPath

    if ($verifier -notlike '*docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md*') {
        $anchor = '    "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",'
        $insert = @'
    "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",
    "docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md",
'@

        if ($verifier -notlike $anchor) {
            Write-Host "Quickstart anchor not found in verifier; skipping fallback doc path insertion."
        } else {
            $verifier = $verifier.Replace($anchor, $insert)
        }
    }

    if ($verifier -notlike '*docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md*') {
        $anchor2 = '    "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md",'
        $insert2 = @'
    "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md",
    "docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md",
'@

        if ($verifier -notlike $anchor2) {
            Write-Host "Round 005 synthesis anchor not found in verifier; skipping Round 005 response path insertion."
        } else {
            $verifier = $verifier.Replace($anchor2, $insert2)
        }
    }

    Write-Utf8Lf -Path $verifierPath -Content $verifier
}

Write-Host ""
Write-Host "Running Round 005 checker..."
Invoke-Python -Args @("tools/check_public_review_round_005_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Running Day-0 checker..."
Invoke-Python -Args @("tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json")

Write-Host ""
Write-Host "Running boundary-pressure checker with adversarial regression..."
Invoke-Python -Args @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")

Write-Host ""
Write-Host "Running Round 004 checker..."
Invoke-Python -Args @("tools/check_public_review_round_004_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Checking for stale Day-0 status phrases..."
$staleFiles = @(
    "docs/CURRENT_PROOF_SURFACE_v0_1.md",
    "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"
)
$stalePatterns = @(
    "Day-0 fixture not yet implemented",
    "Day-0 packet not yet implemented",
    "Day-0 fixture is not yet implemented",
    "Day-0 packet is not yet implemented"
)
$staleFound = $false

foreach ($file in $staleFiles) {
    if (-not (Test-Path $file)) { continue }
    $text = Read-Utf8 -Path $file
    foreach ($pattern in $stalePatterns) {
        if ($text -match [regex]::Escape($pattern)) {
            Write-Host "STALE STATUS FOUND: $pattern in $file"
            $staleFound = $true
        }
    }
}

if ($staleFound) {
    throw "Stale Day-0 status language remains in read-first docs."
}
Write-Host "No stale Day-0 status phrases found in read-first docs."

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host " git diff -- docs\CURRENT_PROOF_SURFACE_v0_1.md docs\review\PUBLIC_REVIEW_QUICKSTART_v0_1.md"
Write-Host " git diff -- docs\review\PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md"
Write-Host " git diff -- docs\review\public-rounds\round-005\ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md"
Write-Host " git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host " powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host " python tools\check_public_review_round_005_interactions_v0_1.py --json"
Write-Host " python tools\check_longitudinal_reconstruction_day0_packet_v0_1.py --json"
Write-Host " git diff --check"

if ($Commit) {
    Invoke-Git -Args @(
        "add", "--",
        $scriptPath,
        $fallbackDocPath,
        $responseReceiptPath,
        "README.md",
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",
        "docs/review/public-rounds/round-005/README.md",
        "docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md",
        $verifierPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Fix Day-0 status contradictions and document verifier fallback")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."