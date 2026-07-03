# scripts/build_ahi_viewer_comparison_data_v0_2.ps1
# Deterministically builds AHI Viewer v0.2 comparison data.
# Run from repository root.

param(
    [switch] $ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from repository root."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

$out = "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json"

if ((Test-Path $out) -and -not $ForceOverwrite) {
    throw "Output exists: $out. Re-run with -ForceOverwrite."
}

python scripts\build_ahi_viewer_comparison_data_v0_2.py

Write-Host ""
Write-Host "PASS: AHI viewer v0.2 comparison data built."
