<#
.SYNOPSIS
Run ESAL reference oracle over esal-tests and print a basic report.
#>

Write-Host "== ESAL v0.1 Reference Oracle Verification =="

# Ensure we're in repo root
if (-not (Test-Path ".git")) {
    Write-Error "Run this script from the fork-public-evidence repository root."
    exit 1
}

$testsRoot = "esal-tests"
if (-not (Test-Path $testsRoot)) {
    Write-Error "Test corpus folder '$testsRoot' not found."
    exit 1
}

# Use Python interpreter (assuming it's on PATH) and a small runner entrypoint
$python = "python"

# You can later replace 'esal_cli.py' with a proper Python entrypoint
$cmd = "$python -m reference.esal.runner $testsRoot"

Write-Host "Running: $cmd"
& $python -m reference.esal.runner $testsRoot

if ($LASTEXITCODE -ne 0) {
    Write-Error "ESAL verification failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host "ESAL verification completed."