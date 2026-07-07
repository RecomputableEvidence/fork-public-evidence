#requires -Version 5.1
<#
.SYNOPSIS
  Apply correction patch to stage_boundary_state_interop_v0_1_1.ps1.

.DESCRIPTION
  Fixes:
    1. Invalid PowerShell regex replacement:
         $TargetRelGit = $TargetRelPath -replace '\','/'
       becomes:
         $TargetRelGit = $TargetRelPath -replace '\\','/'

    2. Adds preflight usage guidance near the top of the script.

    3. Strengthens required source-file validation so all missing files are
       reported together before the script exits.

  This patch does not stage, commit, push, relocate artifacts, or modify any
  recomputation artifacts. It only patches the staging script.
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = "C:\N\fork-public-evidence",

    [string]$TargetScriptRelPath = "scripts\stage_boundary_state_interop_v0_1_1.ps1"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "OK: $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "WARN: $Message" -ForegroundColor Yellow
}

function Fail {
    param([string]$Message)
    throw $Message
}

Write-Step "Validate target script path"

if (-not (Test-Path $RepoRoot)) {
    Fail "RepoRoot does not exist: $RepoRoot"
}

$RepoRoot = (Resolve-Path $RepoRoot).Path
$TargetScript = Join-Path $RepoRoot $TargetScriptRelPath

if (-not (Test-Path $TargetScript)) {
    Fail "Target script does not exist: $TargetScript"
}

$TargetScript = (Resolve-Path $TargetScript).Path
Write-Ok "Target script: $TargetScript"

Write-Step "Create backup"

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "$TargetScript.bak_$timestamp"
Copy-Item -LiteralPath $TargetScript -Destination $backupPath -Force
Write-Ok "Backup created: $backupPath"

Write-Step "Load script"

$content = Get-Content -LiteralPath $TargetScript -Raw
$originalContent = $content

Write-Step "Patch 1: fix TargetRelGit regex replacement"

$oldTargetRelGit = "`$TargetRelGit = `$TargetRelPath -replace '\','/'"
$newTargetRelGit = "`$TargetRelGit = `$TargetRelPath -replace '\\','/'"

if ($content.Contains($oldTargetRelGit)) {
    $content = $content.Replace($oldTargetRelGit, $newTargetRelGit)
    Write-Ok "Fixed TargetRelGit regex replacement"
}
elseif ($content.Contains($newTargetRelGit)) {
    Write-Warn "TargetRelGit regex replacement already patched"
}
else {
    Write-Warn "Could not find exact TargetRelGit line. No replacement applied for Patch 1."
}

Write-Step "Patch 2: add preflight usage guidance"

$preflightMarker = "# Preflight usage:"
$preflightBlock = @'
# Preflight usage:
#
# Before running this script, create the source drop folder and place the
# required recomputation artifacts in it:
#
#   C:\N\boundary-state-interop-v0.1.1-drop\
#     boundary_state_interop_evidence_packet_v0_1_1.zip
#     boundary_state_interop_checker_v0_1_1.zip
#     RECOMPUTATION_CHAIN_NOTE_v0_1_1_2026-07-06.md
#
# This script intentionally refuses to run if the git working tree is dirty.
# Commit, stash, or restore unrelated changes before staging the recomputation state.

'@

if ($content.Contains($preflightMarker)) {
    Write-Warn "Preflight usage guidance already present"
}
else {
    $strictModeLine = "Set-StrictMode -Version Latest"

    if (-not $content.Contains($strictModeLine)) {
        Write-Warn "Could not find Set-StrictMode line. No preflight guidance inserted."
    }
    else {
        $content = $content.Replace($strictModeLine, $preflightBlock + $strictModeLine)
        Write-Ok "Inserted preflight usage guidance"
    }
}

Write-Step "Patch 3: strengthen required source-file validation"

$requiredBlockStart = 'Write-Step "Preflight: validate required source files"'
$optionalBlockStart = '$optionalItems = @('

$startIndex = $content.IndexOf($requiredBlockStart, [System.StringComparison]::Ordinal)
$endIndex = -1

if ($startIndex -ge 0) {
    $endIndex = $content.IndexOf($optionalBlockStart, $startIndex, [System.StringComparison]::Ordinal)
}

if ($startIndex -lt 0 -or $endIndex -lt 0) {
    Write-Warn "Could not locate required-file validation block. No replacement applied for Patch 3."
}
else {
    $existingRequiredBlock = $content.Substring($startIndex, $endIndex - $startIndex)

    if ($existingRequiredBlock.Contains('$missingRequiredFiles')) {
        Write-Warn "Required-file validation block already strengthened"
    }
    else {
        $newRequiredBlock = @'
Write-Step "Preflight: validate required source files"

$requiredFiles = @(
    "boundary_state_interop_evidence_packet_v0_1_1.zip",
    "boundary_state_interop_checker_v0_1_1.zip",
    "RECOMPUTATION_CHAIN_NOTE_v0_1_1_2026-07-06.md"
)

$missingRequiredFiles = @()

foreach ($name in $requiredFiles) {
    $candidate = Join-Path $SourceRoot $name
    if (-not (Test-Path $candidate)) {
        $missingRequiredFiles += $candidate
    }
    else {
        Write-Ok "Found required source file: $name"
    }
}

if ($missingRequiredFiles.Count -gt 0) {
    Write-Warn "Missing required source files:"
    foreach ($missing in $missingRequiredFiles) {
        Write-Warn "  $missing"
    }

    Fail "Required recomputation source files are missing. Create the source drop folder and place all required files before running this script."
}

'@

        $content =
            $content.Substring(0, $startIndex) +
            $newRequiredBlock +
            $content.Substring($endIndex)

        Write-Ok "Replaced required-file validation block"
    }
}

Write-Step "Write patched script"

if ($content -eq $originalContent) {
    Write-Warn "No textual changes were applied"
}
else {
    Set-Content -LiteralPath $TargetScript -Value $content -Encoding UTF8
    Write-Ok "Patched script written"
}

Write-Step "Parse-check patched script"

$tokens = $null
$parseErrors = $null

[System.Management.Automation.Language.Parser]::ParseFile(
    $TargetScript,
    [ref]$tokens,
    [ref]$parseErrors
) | Out-Null

if ($parseErrors -and $parseErrors.Count -gt 0) {
    Write-Warn "PowerShell parser reported errors:"
    foreach ($err in $parseErrors) {
        Write-Warn "  $($err.Message)"
    }

    Fail "Patched script has parse errors. Backup remains at: $backupPath"
}

Write-Ok "Patched script parsed successfully"

Write-Step "Patch complete"

Write-Host "Patched: $TargetScript"
Write-Host "Backup:  $backupPath"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Ensure git working tree is clean."
Write-Host "  2. Create C:\N\boundary-state-interop-v0.1.1-drop."
Write-Host "  3. Place the three required recomputation files in that folder."
Write-Host "  4. Run scripts\stage_boundary_state_interop_v0_1_1.ps1 end-to-end."