# scripts/create_ahi_release_index_v0_3.ps1
# Refreshes AHI Release Index v0.3 and Reviewer Packet v0.1 files.
# Does not commit, push, or tag.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

function Write-Utf8NoBom($Path, $Text) {
    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = [System.IO.Path]::GetDirectoryName($full)
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    if ((Test-Path $full) -and (-not $ForceOverwrite)) {
        throw "Refusing to overwrite existing file without -ForceOverwrite: $Path"
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($full, $Text, $utf8NoBom)
}

if (-not (Test-Path ".git")) {
    throw "Run from repository root."
}

$required = @(
  "README_AHI_RELEASE_INDEX_v0_3.md",
  "docs\releases\AHI_RELEASE_INDEX_v0_3.md",
  "docs\releases\AHI_VERIFICATION_MATRIX_v0_3.md",
  "docs\releases\AHI_SCENARIO_LADDER_v0_3.md",
  "docs\releases\AHI_VIEWER_RELEASE_LADDER_v0_3.md",
  "docs\releases\AHI_LOCAL_VERIFICATION_GUIDE_v0_3.md",
  "docs\reviewer\AHI_PROOF_SURFACE_MAP_v0_1.md",
  "docs\reviewer\FORK_AHI_REVIEWER_PACKET_v0_1.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        throw "Missing package file after copy: $path"
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "AHI Release Index v0.3 and Reviewer Packet v0.1 package files are present."
Write-Host "Next validation:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism"
Write-Host "  git diff --check"
