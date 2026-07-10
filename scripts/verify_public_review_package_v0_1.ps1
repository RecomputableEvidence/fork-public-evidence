# scripts/verify_public_review_package_v0_1.ps1
# Verifies the current public review package surface.
# PowerShell 5.1 compatible.

param(
    [switch]$Json,
    [switch]$SkipGitChecks
)

$ErrorActionPreference = "Stop"

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

function Get-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        return $python.Source
    }

    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) {
        return $py.Source
    }

    throw "Python was not found on PATH."
}

function New-Result {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][bool]$Passed,
        [string]$Detail = "",
        [object]$Data = $null
    )

    return [ordered]@{
        name = $Name
        passed = $Passed
        detail = $Detail
        data = $Data
    }
}

function Invoke-External {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $output = & $Command @Arguments 2>&1
    $exitCode = $LASTEXITCODE

    return [ordered]@{
        name = $Name
        command = $Command
        arguments = $Arguments
        exit_code = $exitCode
        output = ($output -join "`n")
    }
}

Assert-RepoRoot

$results = New-Object System.Collections.ArrayList

$requiredPaths = @(
    "docs/CURRENT_PROOF_SURFACE_v0_1.md",
    "docs/REVIEWER_START_HERE_v0_1.md",
    "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
    "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md",
    "tools/check_boundary_pressure_review_cases_v0_1.py",
    "schemas/boundary_pressure_review_case_v0_1.schema.json",
    "docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md",
    "docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md",
    "docs/review/boundary-pressure/fixtures/valid/BPR_RD_VALID_001_access_limitation_preserved_v0_1.json",
    "docs/review/boundary-pressure/fixtures/invalid/BPR_RD_INVALID_001_failed_retrieval_treated_as_review_v0_1.json",
    "docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json",
    "docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json",
    "docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md",
    "docs/research/BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md"
)

foreach ($path in $requiredPaths) {
    if (Test-Path $path) {
        [void]$results.Add((New-Result -Name "path:$path" -Passed $true -Detail "present"))
    } else {
        [void]$results.Add((New-Result -Name "path:$path" -Passed $false -Detail "missing"))
    }
}

$pythonCmd = Get-PythonCommand
$boundaryChecker = Invoke-External `
    -Name "boundary-pressure-checker" `
    -Command $pythonCmd `
    -Arguments @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")

$checkerPassed = $boundaryChecker.exit_code -eq 0
$checkerData = $null

try {
    $checkerData = $boundaryChecker.output | ConvertFrom-Json
    if ($checkerData.failed -ne 0) {
        $checkerPassed = $false
    }
} catch {
    $checkerPassed = $false
}

[void]$results.Add((New-Result `
    -Name "checker:boundary-pressure" `
    -Passed $checkerPassed `
    -Detail "python tools/check_boundary_pressure_review_cases_v0_1.py --json" `
    -Data $checkerData))

if (-not $SkipGitChecks) {
    $gitDiffCheck = Invoke-External `
        -Name "git-diff-check" `
        -Command "git" `
        -Arguments @("diff", "--check")

    [void]$results.Add((New-Result `
        -Name "git:diff-check" `
        -Passed ($gitDiffCheck.exit_code -eq 0) `
        -Detail $gitDiffCheck.output `
        -Data $gitDiffCheck))

    $gitCachedDiffCheck = Invoke-External `
        -Name "git-diff-cached-check" `
        -Command "git" `
        -Arguments @("diff", "--cached", "--check")

    [void]$results.Add((New-Result `
        -Name "git:diff-cached-check" `
        -Passed ($gitCachedDiffCheck.exit_code -eq 0) `
        -Detail $gitCachedDiffCheck.output `
        -Data $gitCachedDiffCheck))
}

$passedCount = 0
$totalCount = $results.Count

foreach ($result in $results) {
    if ($result["passed"] -eq $true) {
        $passedCount++
    }
}

$failedCount = $totalCount - $passedCount

$summary = [ordered]@{
    verifier = "verify_public_review_package_v0_1.ps1"
    status = $(if ($failedCount -eq 0) { "PUBLIC_REVIEW_PACKAGE_VERIFY_PASS" } else { "PUBLIC_REVIEW_PACKAGE_VERIFY_FAIL" })
    total = $totalCount
    passed = $passedCount
    failed = $failedCount
    results = @($results)
    non_authority_statement = "This verifier checks public review package presence and bounded checker execution only; it does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, or institutional authority."
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 20
} else {
    Write-Host $summary.status
    Write-Host "passed: $passedCount"
    Write-Host "failed: $failedCount"
    Write-Host ""

    foreach ($result in $results) {
        $mark = if ($result["passed"]) { "PASS" } else { "FAIL" }
        Write-Host "$mark $($result["name"])"
        if (-not $result["passed"] -and $result["detail"]) {
            Write-Host "  $($result["detail"])"
        }
    }

    if ($checkerData -and $checkerData.total -ne $null) {
        Write-Host ""
        Write-Host "Boundary pressure checker:"
        Write-Host "  total: $($checkerData.total)"
        Write-Host "  passed: $($checkerData.passed)"
        Write-Host "  failed: $($checkerData.failed)"
    }

    if ($checkerData -and $checkerData.adversarial -and $checkerData.adversarial.total -ne $null) {
        Write-Host ""
        Write-Host "Adversarial boundary pressure regression:"
        Write-Host "  total: $($checkerData.adversarial.total)"
        Write-Host "  passed: $($checkerData.adversarial.passed)"
        Write-Host "  failed: $($checkerData.adversarial.failed)"
    }
}

if ($failedCount -ne 0) {
    exit 1
}

exit 0