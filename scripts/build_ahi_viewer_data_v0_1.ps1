# scripts/build_ahi_viewer_data_v0_1.ps1
# Builds the static data bundle for docs/viewer/ahi-viewer-v0_1.
# Delegates JSON handling to scripts/build_ahi_viewer_data_v0_1.py to avoid PowerShell 5.1 serialization issues.
# Does not stage, commit, push, tag, or modify source artifacts.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw "Python was not found on PATH. The viewer builder requires Python."
}

$builder = "scripts/build_ahi_viewer_data_v0_1.py"
if (-not (Test-Path $builder)) {
    throw "Missing Python builder: $builder"
}

python $builder
exit $LASTEXITCODE
