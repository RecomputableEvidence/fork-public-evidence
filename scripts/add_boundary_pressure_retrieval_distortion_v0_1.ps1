# scripts/add_boundary_pressure_retrieval_distortion_v0_1.ps1
# Maintained wrapper. Runs the repair-safe Boundary Pressure Review v0.1 installer.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"

$repair = Join-Path $PSScriptRoot "repair_boundary_pressure_retrieval_distortion_v0_1.ps1"

if (-not (Test-Path $repair)) {
    throw "Missing repair script: $repair"
}

$argsList = @()

if ($Commit) {
    $argsList += "-Commit"
}

if ($Push) {
    $argsList += "-Push"
}

& powershell -ExecutionPolicy Bypass -File $repair @argsList
exit $LASTEXITCODE