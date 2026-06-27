$ErrorActionPreference = "Stop"

Write-Host "== ESAL v0.1 Reference Oracle Verification =="
Write-Host "Running: python -m reference.esal.runner esal-tests"
Write-Host ""

python -m reference.esal.runner esal-tests

if ($LASTEXITCODE -ne 0) {
    throw "ESAL verification failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "ESAL verification completed."