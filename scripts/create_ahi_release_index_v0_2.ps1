# scripts/create_ahi_release_index_v0_2.ps1
# Creates AHI release-index v0.2 docs.
# This script does not commit, push, or tag.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

function Write-Utf8NoBom($Path, $Text) {
    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if ((Test-Path $Path) -and (-not $ForceOverwrite)) {
        throw "Refusing to overwrite existing file without -ForceOverwrite: $Path"
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $Text = $Text -replace "`r`n", "`n"
    $Text = $Text -replace "`r", "`n"
    if (-not $Text.EndsWith("`n")) {
        $Text += "`n"
    }

    [System.IO.File]::WriteAllText((Join-Path (Get-Location) $Path), $Text, $utf8NoBom)
    Write-Host "WROTE: $Path"
}

if (-not (Test-Path ".git")) {
    throw "Run this script from repository root."
}

# This script expects the v0.2 markdown files from the package to already be copied into docs/releases.
# It normalizes them to UTF-8 without BOM and LF line endings so Git diffs remain clean.
$files = @(
  "docs/releases/AHI_RELEASE_INDEX_v0_2.md",
  "docs/releases/AHI_VERIFICATION_MATRIX_v0_2.md",
  "docs/releases/AHI_SCENARIO_LADDER_v0_2.md",
  "docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_2.md",
  "docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_2.md"
)

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        throw "Missing expected release doc: $file"
    }
    $text = Get-Content -Raw -Path $file
    Write-Utf8NoBom $file $text
}

Write-Host ""
Write-Host "PASS: AHI release-index v0.2 docs created and normalized."
Write-Host "Next:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism"
