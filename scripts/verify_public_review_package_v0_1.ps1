# scripts/verify_public_review_package_v0_1.ps1
# Public review package verifier v0.1.
# PowerShell 5.1 compatible.

param(
    [switch]$Json,
    [switch]$SkipGitChecks
)

$ErrorActionPreference = "Stop"

function New-Result {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][bool]$Passed,
        [string]$Detail = "",
        $Data = $null
    )

    return [ordered]@{
        name = $Name
        passed = $Passed
        detail = $Detail
        data = $Data
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

    return $null
}

function Invoke-External {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][string]$Command,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    $output = & $Command @Arguments 2>&1
    $exitCode = $LASTEXITCODE
    $text = ($output | Out-String).Trim()

    return [ordered]@{
        name = $Name
        command = $Command
        arguments = $Arguments
        exit_code = $exitCode
        output = $text
    }
}

function Convert-JsonOutput {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Name
    )

    try {
        return ($Text | ConvertFrom-Json)
    } catch {
        throw "$Name produced non-JSON output: $Text"
    }
}

if (-not (Test-Path ".git")) {
    throw "Run this verifier from the fork-public-evidence repository root."
}

$results = New-Object System.Collections.ArrayList

$requiredPaths = @(
    "README.md",
    "docs/CURRENT_PROOF_SURFACE_v0_1.md",
    "docs/REVIEWER_START_HERE_v0_1.md",
    "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
    "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md",
    "docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md",

    "tools/check_boundary_pressure_review_cases_v0_1.py",
    "schemas/boundary_pressure_review_case_v0_1.schema.json",

    "docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md",
    "docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md",
    "docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md",

    "docs/review/boundary-pressure/fixtures/valid/BPR_RD_VALID_001_access_limitation_preserved_v0_1.json",
    "docs/review/boundary-pressure/fixtures/invalid/BPR_RD_INVALID_001_failed_retrieval_treated_as_review_v0_1.json",
    "docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json",
    "docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json",

    "docs/review/boundary-pressure/fixtures/adversarial/BPR_RD_ADVERSARIAL_001_valid_shaped_content_under_invalid_expectation_v0_1.json",
    "docs/review/boundary-pressure/fixtures/adversarial/BPR_RR_ADVERSARIAL_001_near_empty_invalid_overread_v0_1.json",
    "docs/review/boundary-pressure/fixtures/adversarial/BPR_RR_ADVERSARIAL_002_invalid_without_overread_flags_v0_1.json",
    "docs/review/boundary-pressure/fixtures/adversarial/BPR_UNKNOWN_ADVERSARIAL_001_unknown_family_must_not_pass_by_directory_v0_1.json",

    "docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md",
    "docs/research/BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md",

    "docs/review/public-rounds/README.md",
    "docs/review/public-rounds/round-004/README.md",
    "docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md",
    "docs/review/public-rounds/round-004/observations/ROUND004_OBS_001_copilot_access_path_no_execution_review_v0_1.json",
    "docs/review/public-rounds/round-004/observations/ROUND004_OBS_002_gemini_no_access_exterior_observation_v0_1.json",
    "docs/review/public-rounds/round-004/observations/ROUND004_OBS_003_vibe_access_path_governance_observation_v0_1.json",
    "docs/review/public-rounds/round-004/observations/ROUND004_OBS_004_claude_execution_recomputation_adversarial_observation_v0_1.json",

    "docs/templates/PUBLIC_REVIEW_ROUND_004_INTERACTION_TEMPLATE_v0_1.json",
    "schemas/public_review_round_004_interaction_v0_1.schema.json",
    "tools/check_public_review_round_004_interactions_v0_1.py",

    "scripts/verify_public_review_package_v0_1.ps1"
)

foreach ($path in $requiredPaths) {
    if (Test-Path $path) {
        [void]$results.Add((New-Result -Name "path:$path" -Passed $true -Detail "present"))
    } else {
        [void]$results.Add((New-Result -Name "path:$path" -Passed $false -Detail "missing"))
    }
}

$pythonCommand = Get-PythonCommand

if (-not $pythonCommand) {
    [void]$results.Add((New-Result -Name "runtime:python" -Passed $false -Detail "Python not found on PATH"))
} else {
    [void]$results.Add((New-Result -Name "runtime:python" -Passed $true -Detail $pythonCommand))

    $bpArgs = @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")
    $bpRun = Invoke-External -Name "boundary-pressure" -Command $pythonCommand -Arguments $bpArgs
    $bpPassed = $false
    $bpData = $null

    if ($bpRun.exit_code -eq 0) {
        $bpData = Convert-JsonOutput -Text $bpRun.output -Name "boundary-pressure checker"

        $defaultOk = (
            $bpData.total -eq 4 -and
            $bpData.passed -eq 4 -and
            $bpData.failed -eq 0
        )

        $adversarialOk = (
            $bpData.adversarial -ne $null -and
            $bpData.adversarial.total -eq 4 -and
            $bpData.adversarial.passed -eq 4 -and
            $bpData.adversarial.failed -eq 0
        )

        $bpPassed = ($defaultOk -and $adversarialOk)
    }

    [void]$results.Add((New-Result `
        -Name "checker:boundary-pressure" `
        -Passed $bpPassed `
        -Detail "python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial" `
        -Data $bpData))

    $roundArgs = @("tools/check_public_review_round_004_interactions_v0_1.py", "--json")
    $roundRun = Invoke-External -Name "round004-interactions" -Command $pythonCommand -Arguments $roundArgs
    $roundPassed = $false
    $roundData = $null

    if ($roundRun.exit_code -eq 0) {
        $roundData = Convert-JsonOutput -Text $roundRun.output -Name "Round 004 interaction checker"

        $roundPassed = (
            $roundData.total -eq 4 -and
            $roundData.passed -eq 4 -and
            $roundData.failed -eq 0
        )
    }

    [void]$results.Add((New-Result `
        -Name "checker:round004-interactions" `
        -Passed $roundPassed `
        -Detail "python tools/check_public_review_round_004_interactions_v0_1.py --json" `
        -Data $roundData))
}

if (-not $SkipGitChecks) {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) {
        [void]$results.Add((New-Result -Name "runtime:git" -Passed $false -Detail "git not found on PATH"))
    } else {
        [void]$results.Add((New-Result -Name "runtime:git" -Passed $true -Detail $git.Source))

        $diffCheck = Invoke-External -Name "git-diff-check" -Command $git.Source -Arguments @("diff", "--check")
        [void]$results.Add((New-Result `
            -Name "git:diff-check" `
            -Passed ($diffCheck.exit_code -eq 0) `
            -Detail $diffCheck.output `
            -Data $diffCheck))

        $cachedCheck = Invoke-External -Name "git-diff-cached-check" -Command $git.Source -Arguments @("diff", "--cached", "--check")
        [void]$results.Add((New-Result `
            -Name "git:diff-cached-check" `
            -Passed ($cachedCheck.exit_code -eq 0) `
            -Detail $cachedCheck.output `
            -Data $cachedCheck))
    }
}

$total = $results.Count
$passed = 0
foreach ($result in $results) {
    if ($result.passed) {
        $passed += 1
    }
}
$failed = $total - $passed

$status = "PUBLIC_REVIEW_PACKAGE_VERIFY_PASS"
if ($failed -ne 0) {
    $status = "PUBLIC_REVIEW_PACKAGE_VERIFY_FAIL"
}

$summary = [ordered]@{
    verifier = "verify_public_review_package_v0_1.ps1"
    status = $status
    total = $total
    passed = $passed
    failed = $failed
    results = @($results)
    non_authority_statement = "This verifier checks public review package presence and bounded checker execution only; it does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority."
}

if ($Json) {
    $summary | ConvertTo-Json -Depth 80
} else {
    Write-Host $status
    Write-Host "passed: $passed"
    Write-Host "failed: $failed"
    Write-Host ""

    foreach ($result in $results) {
        $label = "FAIL"
        if ($result.passed) {
            $label = "PASS"
        }

        Write-Host "$label $($result.name)"
        if (-not $result.passed -and $result.detail) {
            Write-Host "  $($result.detail)"
        }
    }

    $bpResult = $null
    foreach ($result in $results) {
        if ($result.name -eq "checker:boundary-pressure") {
            $bpResult = $result
        }
    }

    if ($bpResult -and $bpResult.data) {
        Write-Host ""
        Write-Host "Boundary pressure checker:"
        Write-Host "  total: $($bpResult.data.total)"
        Write-Host "  passed: $($bpResult.data.passed)"
        Write-Host "  failed: $($bpResult.data.failed)"

        if ($bpResult.data.adversarial) {
            Write-Host ""
            Write-Host "Adversarial boundary pressure regression:"
            Write-Host "  total: $($bpResult.data.adversarial.total)"
            Write-Host "  passed: $($bpResult.data.adversarial.passed)"
            Write-Host "  failed: $($bpResult.data.adversarial.failed)"
        }
    }

    $roundResult = $null
    foreach ($result in $results) {
        if ($result.name -eq "checker:round004-interactions") {
            $roundResult = $result
        }
    }

    if ($roundResult -and $roundResult.data) {
        Write-Host ""
        Write-Host "Round 004 interaction checker:"
        Write-Host "  total: $($roundResult.data.total)"
        Write-Host "  passed: $($roundResult.data.passed)"
        Write-Host "  failed: $($roundResult.data.failed)"
    }
}

if ($failed -ne 0) {
    exit 1
}

exit 0