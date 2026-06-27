param(
    [switch]$SkipEsalConformance,
    [switch]$SkipBdrEsalHandoff,
    [switch]$VerboseOutput,
    [string]$ReportPath = 'reports\FORK_EVIDENCE_BOUNDARY_REPORT.json'
)

$ErrorActionPreference = 'Stop'

Write-Host '== Fork Evidence Boundary Verification Suite =='

if (!(Test-Path '.git')) {
    throw 'Run this script from the repository root.'
}

$RequiredPaths = @(
    'tools\Test-EsalConformance.ps1',
    'tools\Test-BdrEsalHandoff.ps1',
    'reports\ESAL_v0_1_EXPECTED_OUTPUTS.md',
    'docs\BDR_ESAL_HANDOFF_CONTRACT_v0_1.md'
)

foreach ($Path in $RequiredPaths) {
    if (!(Test-Path $Path)) {
        throw "Required path missing: $Path"
    }
}

New-Item -ItemType Directory -Force -Path 'reports' | Out-Null

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Get-GitValue {
    param([string[]]$Args)

    $Value = & git @Args 2>$null
    if ($LASTEXITCODE -ne 0) {
        return ''
    }

    return ($Value | Select-Object -First 1).Trim()
}

function Read-JsonIfPresent {
    param([string]$Path)

    if (!(Test-Path $Path)) {
        return $null
    }

    try {
        return Get-Content $Path -Raw | ConvertFrom-Json
    }
    catch {
        return [ordered]@{
            parse_error = $_.Exception.Message
            path        = $Path
        }
    }
}

function Run-ChildSuite {
    param(
        [string]$Name,
        [string]$ScriptPath,
        [string]$ExpectedOutputFragment,
        [string]$ExpectedReportPath,
        [string]$ExpectedReportResult
    )

    Write-Host ''
    Write-Host "Running suite: $Name"
    Write-Host "Script: $ScriptPath"

    $Output   = & powershell -NoProfile -ExecutionPolicy Bypass -File $ScriptPath 2>&1
    $ExitCode = $LASTEXITCODE
    $OutputText = ($Output -join "`n")

    if ($VerboseOutput) {
        $Output | Out-Host
    }

    $Issues = New-Object 'System.Collections.Generic.List[string]'

    if ($ExitCode -ne 0) {
        $Issues.Add("Suite exited with code $ExitCode") | Out-Null
    }

    if ($ExpectedOutputFragment -and ($OutputText -notmatch [regex]::Escape($ExpectedOutputFragment))) {
        $Issues.Add("Expected output fragment not found: $ExpectedOutputFragment") | Out-Null
    }

    $Report = Read-JsonIfPresent $ExpectedReportPath

    if ($null -eq $Report) {
        $Issues.Add("Expected report missing: $ExpectedReportPath") | Out-Null
    }
    elseif ($Report.PSObject.Properties.Name -contains 'parse_error') {
        $Issues.Add("Expected report could not be parsed: $ExpectedReportPath") | Out-Null
    }
    elseif ($ExpectedReportResult -and $Report.result -ne $ExpectedReportResult) {
        $Issues.Add("Expected report result $ExpectedReportResult, actual $($Report.result)") | Out-Null
    }

    return [ordered]@{
        name                     = $Name
        script                   = $ScriptPath
        expected_output_fragment = $ExpectedOutputFragment
        expected_report_path     = $ExpectedReportPath
        expected_report_result   = $ExpectedReportResult
        exit_code                = $ExitCode
        passed                   = ($Issues.Count -eq 0)
        issues                   = @($Issues)
        output_excerpt           = @($Output | Select-Object -Last 24)
        report_result            = $(if ($Report -and ($Report.PSObject.Properties.Name -contains 'result')) { $Report.result } else { $null })
        skipped                  = $false
    }
}

$StartedUtc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$Branch     = Get-GitValue @('branch', '--show-current')
$Commit     = Get-GitValue @('rev-parse', 'HEAD')

$SuiteResults = @()

if ($SkipEsalConformance) {
    Write-Host ''
    Write-Host 'Skipping ESAL conformance suite.'
    $SuiteResults += [ordered]@{
        name    = 'ESAL v0.1 conformance'
        skipped = $true
        passed  = $true
        issues  = @()
    }
}
else {
    $SuiteResults += Run-ChildSuite `
        -Name 'ESAL v0.1 conformance' `
        -ScriptPath '.\tools\Test-EsalConformance.ps1' `
        -ExpectedOutputFragment 'CONFORMANCE_PASS' `
        -ExpectedReportPath 'reports\ESAL_v0_1_CONFORMANCE_REPORT.json' `
        -ExpectedReportResult 'CONFORMANCE_PASS'
}

if ($SkipBdrEsalHandoff) {
    Write-Host ''
    Write-Host 'Skipping BDR / ESAL handoff suite.'
    $SuiteResults += [ordered]@{
        name    = 'BDR / ESAL handoff'
        skipped = $true
        passed  = $true
        issues  = @()
    }
}
else {
    $SuiteResults += Run-ChildSuite `
        -Name 'BDR / ESAL handoff' `
        -ScriptPath '.\tools\Test-BdrEsalHandoff.ps1' `
        -ExpectedOutputFragment 'HANDOFF_VALIDATOR_PASS' `
        -ExpectedReportPath 'reports\BDR_ESAL_HANDOFF_VALIDATION_REPORT.json' `
        -ExpectedReportResult 'HANDOFF_VALIDATOR_PASS'
}

$AllIssues = New-Object 'System.Collections.Generic.List[string]'
foreach ($Suite in $SuiteResults) {
    if (-not $Suite.passed) {
        foreach ($Issue in $Suite.issues) {
            $AllIssues.Add("$($Suite.name): $Issue") | Out-Null
        }
    }
}

$Passed = ($AllIssues.Count -eq 0)

$Report = [ordered]@{
    artifact_id = 'FORK-EVIDENCE-BOUNDARY-REPORT-v0.1'
    generated_utc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    started_utc   = $StartedUtc
    branch        = $Branch
    commit        = $Commit
    result        = $(if ($Passed) { 'FORK_EVIDENCE_BOUNDARY_PASS' } else { 'FORK_EVIDENCE_BOUNDARY_FAIL' })
    purpose       = 'Runs the bounded Fork evidence-boundary verification suite without collapsing ESAL conformance and BDR/ESAL handoff semantics.'
    suites        = $SuiteResults
    non_claims    = @(
        'does not establish production completeness',
        'does not establish legal sufficiency',
        'does not establish compliance sufficiency',
        'does not establish authorization correctness',
        'does not establish external governance validity',
        'does not establish endorsement or approval',
        'does not establish safety or truth',
        'does not establish independent implementation convergence',
        'does not make ESAL a policy-enforcement engine',
        'does not validate the underlying BDR transition as externally sufficient'
    )
    issues        = @($AllIssues)
}

$ReportJson      = $Report | ConvertTo-Json -Depth 30
$ReportFullPath  = Join-Path (Get-Location) $ReportPath
$ReportDirectory = Split-Path $ReportFullPath -Parent

if (!(Test-Path $ReportDirectory)) {
    New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
}

[System.IO.File]::WriteAllText($ReportFullPath, $ReportJson + "`n", $Utf8NoBom)

Write-Host ''
Write-Host '== Fork Evidence Boundary Result =='

if ($Passed) {
    Write-Host 'FORK_EVIDENCE_BOUNDARY_PASS'
}
else {
    Write-Host 'FORK_EVIDENCE_BOUNDARY_FAIL'
}

Write-Host ''
foreach ($Suite in $SuiteResults) {
    $Status  = if ($Suite.passed) { 'PASS' } else { 'FAIL' }
    $Skipped = if ($Suite.skipped) { ' skipped' } else { '' }
    Write-Host "$($Suite.name): $Status$Skipped"
}

Write-Host "Report written: $ReportPath"

if ($VerboseOutput -or -not $Passed) {
    Write-Host ''
    Write-Host 'Issues:'
    foreach ($Issue in $AllIssues) {
        Write-Host " - $Issue"
    }
}

if (-not $Passed) {
    exit 1
}

exit 0