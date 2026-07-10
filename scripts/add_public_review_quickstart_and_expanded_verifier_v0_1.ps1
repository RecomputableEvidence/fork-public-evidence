# scripts/add_public_review_quickstart_and_expanded_verifier_v0_1.ps1
# Adds public review quickstart and expands public verifier coverage.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF.

param(
    [switch]$Commit,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the fork-public-evidence repository root."
    }
}

function Write-Utf8Lf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $full = [System.IO.Path]::GetFullPath($Path)
    $dir = Split-Path -Parent $full

    if ($dir -and -not (Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    [System.IO.File]::WriteAllText($full, $normalized, $Utf8NoBom)
}

function Read-Utf8 {
    param([Parameter(Mandatory = $true)][string]$Path)
    return [System.IO.File]::ReadAllText((Resolve-Path $Path).Path, $Utf8NoBom)
}

function Replace-OrAppendBlock {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$BlockId,
        [Parameter(Mandatory = $true)][string]$Content
    )

    if (-not (Test-Path $Path)) {
        Write-Host "Skipping missing routing target: $Path"
        return
    }

    $start = "<!-- $($BlockId):START -->"
    $end = "<!-- $($BlockId):END -->"
    $existing = Read-Utf8 -Path $Path

    $block = @"

$start

$Content

$end
"@

    $pattern = "(?s)" + [regex]::Escape($start) + ".*?" + [regex]::Escape($end)

    if ($existing -match $pattern) {
        $updated = [regex]::Replace($existing, $pattern, $block.Trim())
        Write-Host "Replaced routing block in $Path"
    } else {
        $updated = $existing.TrimEnd() + "`n" + $block + "`n"
        Write-Host "Added routing block in $Path"
    }

    Write-Utf8Lf -Path $Path -Content $updated
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    & git @Args
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Invoke-Python {
    param([Parameter(Mandatory = $true)][string[]]$Args)

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        $python = Get-Command py -ErrorAction SilentlyContinue
    }
    if (-not $python) {
        throw "Python was not found on PATH."
    }

    & $python.Source @Args
    if ($LASTEXITCODE -ne 0) {
        throw "python $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Assert-RepoRoot

$quickstartPath = "docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"
$scriptPath = "scripts/add_public_review_quickstart_and_expanded_verifier_v0_1.ps1"

$quickstart = @'
# Fork Public Review Quickstart v0.1

Status: Reviewer quickstart.
Scope: Public GitHub review path, verification commands, expected outputs, and objective review data.

## 1. Purpose

This quickstart gives outside reviewers a short path through Fork's current public proof surface.

It is intended for:

- access-path reviewers;
- exterior governance reviewers;
- recomputation reviewers;
- no-access reviewers documenting execution barriers;
- reviewers proposing adversarial fixtures.

This quickstart is not an endorsement request, certification request, compliance request, legal sufficiency request, safety request, production-readiness request, procurement approval request, or authority-transfer request.

## 2. Start from a clean clone

From a working directory outside the repo:

- git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
- cd fork-public-evidence
- git status -sb
- git log -1 --oneline

Record:

- commit hash;
- operating system;
- shell;
- Python version;
- Git version;
- whether PowerShell was already available.

## 3. Primary proof surface

Read first:

- docs/CURRENT_PROOF_SURFACE_v0_1.md

Then read:

- docs/REVIEWER_START_HERE_v0_1.md
- docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md
- docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md

Reviewer question:

Can you tell what Fork currently demonstrates and what it explicitly does not demonstrate?

## 4. One-command public verifier

From repo root, run:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

Expected signal:

- PUBLIC_REVIEW_PACKAGE_VERIFY_PASS

The verifier now checks:

- core public proof-surface files;
- boundary-pressure checker and fixtures;
- boundary-pressure adversarial regression fixtures;
- Round 004 interaction filing schema and observations;
- longitudinal reconstruction protocol presence;
- BPEF framework presence;
- Git whitespace checks.

This verifier checks public review package presence and bounded checker execution. It does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.

## 5. JSON verifier output

For structured output:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json

Record:

- total;
- passed;
- failed;
- boundary-pressure default count;
- boundary-pressure adversarial count;
- Round 004 filing count;
- any failure reason.

## 6. Run the boundary-pressure checker directly

Default suite:

- python tools/check_boundary_pressure_review_cases_v0_1.py --json

Expected current signal:

- total: 4
- passed: 4
- failed: 0

Default plus adversarial regression:

- python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial

Expected current adversarial signal:

- adversarial.total: 4
- adversarial.passed: 4
- adversarial.failed: 0

Boundary-pressure fixtures are under:

- docs/review/boundary-pressure/fixtures/

Adversarial fixtures are under:

- docs/review/boundary-pressure/fixtures/adversarial/

## 7. Run the Round 004 interaction checker directly

Run:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

Expected current signal:

- total: 4
- passed: 4
- failed: 0

Filed observations are under:

- docs/review/public-rounds/round-004/observations/

Round 004 synthesis is:

- docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md

## 8. Inspect one experiment

Recommended first inspection:

- docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
- docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
- docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md

Reviewer question:

Can you explain why the valid fixture remains valid and why the invalid fixture is rejected without treating rejection as approval, truth, compliance, legal sufficiency, safety, or production readiness?

## 9. Optional adversarial interaction

The boundary-pressure checker supports an adversarial regression mode.

A reviewer may construct a separate fixture root and run:

- python tools/check_boundary_pressure_review_cases_v0_1.py --fixtures-root path\to\scratch_fixtures --json --run-adversarial

Suggested adversarial fixture types:

- valid-shaped content placed under invalid expectation;
- invalid fixture without explicit boundary-pressure signal;
- malformed or content-free fixture;
- unknown fixture family;
- receipt overread without overread flags;
- retrieval limitation upgraded into review, approval, authorization, validation, or compliance.

Do not edit shipped fixtures unless the review purpose is to test a proposed patch.

## 10. Longitudinal reconstruction protocol

Read:

- docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md

Current status:

- protocol exists;
- Day-0 packet is not yet implemented;
- Day-7/30/90 replay receipts are not yet produced.

Reviewer question:

What would Fork need to preserve today so that a future reviewer could answer the same question later without inheriting today's authority?

## 11. Objective review data to record

Recommended fields:

- review round;
- reviewer role;
- operating system;
- shell;
- Python version;
- Git version;
- PowerShell version, if used;
- whether repo clone succeeded;
- whether current proof surface was found;
- whether verifier was found;
- whether boundary-pressure cases were found;
- whether longitudinal protocol was found;
- verifier attempted;
- verifier passed;
- failure reason, if any;
- time to first verifier run;
- whether command was run unmodified;
- whether underlying Python checker was run directly;
- whether adversarial fixture was constructed;
- points of confusion;
- overclaim risks noticed;
- what an exterior governance model would consume;
- what it would refuse to inherit;
- required boundary state;
- missing longitudinal artifacts;
- checker drift concerns;
- packet failure concerns;
- final review classification.

## 12. Filing template

Use:

- docs/templates/PUBLIC_REVIEW_ROUND_004_INTERACTION_TEMPLATE_v0_1.json

Schema:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Checker:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

## 13. Review classifications

Use one or more:

- access-path review;
- no-access observation;
- execution receipt;
- recomputation receipt;
- adversarial boundary-pressure observation;
- exterior governance articulation;
- usability review;
- longitudinal readiness observation;
- mixed review.

## 14. Boundary statement

A public verifier pass means the bounded public review package is present and the included structural checkers passed under the reviewer environment.

It does not mean Fork is true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production ready, or institutionally authoritative.
'@

$verifier = @'
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
'@

Write-Utf8Lf -Path $quickstartPath -Content $quickstart
Write-Utf8Lf -Path $verifierPath -Content $verifier

$readmeBlock = @'
## Public review quickstart

For a one-page reviewer path, use:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

The public verifier is:

- scripts/verify_public_review_package_v0_1.ps1

Run from repo root:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

This path is for public inspection, structural verification, and exterior review. It is not endorsement, certification, compliance approval, legal sufficiency, safety approval, production readiness, or authority transfer.
'@

$reviewerStartBlock = @'
## Public review quickstart

Use this first when reviewing the repository from the outside:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

Primary verifier:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier now includes expanded coverage for boundary-pressure adversarial regression and Round 004 interaction filings.
'@

$publicIndexBlock = @'
## Public review quickstart and expanded verifier coverage

Quickstart:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

Expanded public verifier:

- scripts/verify_public_review_package_v0_1.ps1

The verifier checks core proof-surface files, boundary-pressure fixtures, adversarial regression fixtures, Round 004 interaction filings, longitudinal protocol presence, BPEF presence, and Git whitespace checks.
'@

$currentProofBlock = @'
## Public review quickstart and expanded verifier coverage

A one-page reviewer path is now available:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

The public verifier now includes expanded coverage for:

- current proof-surface routing;
- boundary-pressure default fixtures;
- boundary-pressure adversarial regression fixtures;
- Round 004 structured interaction filings;
- longitudinal reconstruction protocol presence;
- BPEF framework presence;
- Git whitespace checks.

Run:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

A pass remains bounded. It means required public review artifacts are present and included structural checkers passed. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.
'@

Replace-OrAppendBlock `
    -Path "README.md" `
    -BlockId "FORK_PUBLIC_REVIEW_QUICKSTART" `
    -Content $readmeBlock

Replace-OrAppendBlock `
    -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_QUICKSTART" `
    -Content $reviewerStartBlock

Replace-OrAppendBlock `
    -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_QUICKSTART" `
    -Content $publicIndexBlock

Replace-OrAppendBlock `
    -Path "docs/CURRENT_PROOF_SURFACE_v0_1.md" `
    -BlockId "FORK_PUBLIC_REVIEW_QUICKSTART" `
    -Content $currentProofBlock

Write-Host ""
Write-Host "Running expanded public verifier..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Expanded public verifier failed."
}

Write-Host ""
Write-Host "Running expanded public verifier JSON output..."
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json
if ($LASTEXITCODE -ne 0) {
    throw "Expanded public verifier JSON run failed."
}

Write-Host ""
Write-Host "Running direct boundary-pressure checker with adversarial regression..."
Invoke-Python -Args @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial")

Write-Host ""
Write-Host "Running Round 004 interaction checker..."
Invoke-Python -Args @("tools/check_public_review_round_004_interactions_v0_1.py", "--json")

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host "  git diff -- docs\review\PUBLIC_REVIEW_QUICKSTART_v0_1.md"
Write-Host "  git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  git diff -- README.md docs\REVIEWER_START_HERE_v0_1.md docs\PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md docs\CURRENT_PROOF_SURFACE_v0_1.md"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json"
Write-Host "  python tools\check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial"
Write-Host "  python tools\check_public_review_round_004_interactions_v0_1.py --json"
Write-Host "  git diff --check"

if ($Commit) {
    Invoke-Git -Args @("add", "--",
        $quickstartPath,
        $verifierPath,
        "README.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/CURRENT_PROOF_SURFACE_v0_1.md",
        $scriptPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add public review quickstart and expanded verifier coverage")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."