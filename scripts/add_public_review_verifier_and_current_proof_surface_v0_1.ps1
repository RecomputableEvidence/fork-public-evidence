# scripts\add_public_review_verifier_and_current_proof_surface_v0_1.ps1
# Adds public review verifier and current proof surface index v0.1.
# PowerShell 5.1 compatible. Writes UTF-8 without BOM and LF line endings.

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

Assert-RepoRoot

$proofSurfacePath = "docs/CURRENT_PROOF_SURFACE_v0_1.md"
$verifierPath = "scripts/verify_public_review_package_v0_1.ps1"
$addScriptPath = "scripts/add_public_review_verifier_and_current_proof_surface_v0_1.ps1"

$proofSurface = @'
# Current Proof Surface v0.1

Status: Current proof-surface index.
Scope: Public review orientation for currently available Fork evidence, checkers, protocols, and exterior observations.
Classification: Proof-surface index, not certification, validation, endorsement, legal conclusion, compliance conclusion, procurement approval, audit conclusion, safety assessment, or production-readiness assessment.

## 1. Purpose

This document states what the public repository currently demonstrates, what remains experimental, and what must not be inferred.

Its role is to help reviewers distinguish:

```text
machine-checkable proof surfaces;
doc-only protocols;
exterior observations;
interpretive reviews;
boundary-pressure experiments;
future work;
non-claims.
```

Fork's current public claim is bounded:
Fork preserves and tests evidence-boundary structures for AI-assisted workflows without absorbing authority from governance, legal, compliance, risk, audit, security, procurement, or institutional decision layers.

## 2. How to Verify the Current Public Review Package

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

Expected high-level result:

```text
PUBLIC_REVIEW_PACKAGE_VERIFY_PASS
```

The verifier currently checks required public-review files and runs the stable boundary-pressure checker.

## 3. Stable Machine-Checkable Surface

### 3.1 Boundary Pressure Review Checker v0.1

Primary checker:

```text
tools/check_boundary_pressure_review_cases_v0_1.py
```

Run directly:

```bash
python tools/check_boundary_pressure_review_cases_v0_1.py --json
```

Current checked fixture families:

- boundary_pressure_retrieval_distortion
- boundary_pressure_recomputation_receipt_overread

Current expected result:

```text
total: 4
passed: 4
failed: 0
```

### 3.2 What This Checker Demonstrates

The checker demonstrates that selected boundary-pressure fixtures are classified according to preserved boundary rules.

It currently tests whether:

- failed or partial retrieval is preserved as access limitation rather than upgraded into review or authority;
- a recomputation receipt is preserved as structural evidence rather than upgraded into validation, truth, approval, compliance, legal sufficiency, production readiness, or replacement evidence.

### 3.3 What This Checker Does Not Demonstrate

The checker does not demonstrate that:

- Fork is complete;
- Fork is production ready;
- Fork is legally sufficient;
- Fork establishes compliance;
- Fork validates truth;
- Fork approves any workflow;
- Fork authorizes execution;
- Fork proves safety;
- Fork replaces institutional controls;
- Fork provides a SIEM, GRC, audit, compliance, or policy-control system.

## 4. Boundary-Pressure Proof Surface

Boundary-pressure cases are preserved under:

```text
docs/review/boundary-pressure/
```

Current cases:

```text
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
```

Current fixtures:

```text
docs/review/boundary-pressure/fixtures/valid/BPR_RD_VALID_001_access_limitation_preserved_v0_1.json
docs/review/boundary-pressure/fixtures/invalid/BPR_RD_INVALID_001_failed_retrieval_treated_as_review_v0_1.json
docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json
docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json
```

Boundary-pressure cases are experimental. They exercise failure modes where evidence, receipts, access state, or exterior observations may be overread as authority.

## 5. Protocol-Only Surfaces

### 5.1 Longitudinal Reconstruction Trial Protocol v0.1

Protocol document:

```text
docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md
```

This is currently a protocol surface, not yet a completed reconstruction trial.

It defines the target temporal claim:

```text
Fork can reconstruct a preserved AI-assisted reliance event over time from sealed artifacts alone, detect tampering or reference decay, distinguish checker drift from packet failure, and preserve the boundary between reconstruction and authorization.
```

Current status:

- protocol defined;
- schemas not yet implemented;
- Day-0 fixture not yet implemented;
- longitudinal replay receipts not yet produced.

Do not cite the longitudinal protocol as evidence that Fork has already demonstrated delayed replay over time.

### 5.2 Boundary Pressure Evaluation Framework v0.1

Framework document:

```text
docs/research/BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md
```

BPEF is a framework surface. It defines pressure classes, invariants, examples, counterexamples, and cross-class cases.

Current status:

- framework documented;
- examples and counterexamples defined;
- not a certification or compliance framework;
- not a legal, safety, or production-readiness assessment.

## 6. Commercial and Buyer-Facing Surfaces

Commercial orientation files:

```text
docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md
docs/commercial/COMMERCIAL_SURFACE_LANGUAGE_SWEEP_v0_1.md
docs/commercial/README.md
```

These materials are buyer-facing orientation surfaces.

They do not establish:

- production readiness;
- legal admissibility;
- legal sufficiency;
- compliance sufficiency;
- security-control effectiveness;
- procurement approval;
- audit approval;
- buyer approval.

Their purpose is to reduce misclassification risk for legal, security, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers.

## 7. Exterior Observations

Exterior observations are preserved under:

```text
docs/exterior-observations/
```

Commercial-surface exterior observations include:

```text
docs/exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md
```

Exterior observations may be useful as interpretive feedback.

They are not:

- recomputation receipts;
- execution receipts;
- certifications;
- endorsements;
- legal opinions;
- compliance opinions;
- security assessments;
- production-readiness assessments;
- procurement approvals;
- audit conclusions.

## 8. Repository Review Posture

Repository review posture document:

```text
docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md
```

This document explains how reviewers should interpret Fork artifacts, recomputation receipts, exterior observations, pull request history, non-claims, and boundary-pressure concerns.

Review posture rule:

```text
Evidence may be preserved.
Authority is not inherited.
Reconstruction is not approval.
Structural verification is not truth.
Exterior observation is not endorsement.
```

## 9. Current Claims Ladder

The current repository contains proof surfaces at different maturity levels.

```text
Level 0: Framing / doctrine
Level 1: Static artifact exists
Level 2: Checker executes locally
Level 3: Deterministic replay passes for bounded fixture set
Level 4: Independent reviewer recomputes
Level 5: Delayed replay succeeds over time
Level 6: Adverse cases remain detectable over time
```

Current approximate placement:

- Boundary-pressure checker: Level 2 to Level 3 for its bounded fixture set.
- Human recomputation sandbox receipts: Level 4 where preserved as exterior receipts and where execution actually occurred.
- Longitudinal reconstruction protocol: Level 1 protocol surface only.
- BPEF: Level 1 framework surface only.
- Commercial buyer surface: orientation surface only, not proof of production readiness.

This ladder is descriptive. It does not upgrade any artifact into authority.

## 10. What Fork Currently Does Not Prove

Fork currently does not prove that:

- an AI-assisted decision was correct;
- an AI-assisted artifact was true;
- an admission event was valid;
- a workflow was authorized;
- a system was compliant;
- an artifact was legally sufficient;
- a system was safe;
- a deployment was production ready;
- a buyer should approve procurement;
- a reviewer endorsed Fork;
- a receipt replaces missing source evidence;
- a failed retrieval equals review;
- reconstruction equals approval.

## 11. Screenshots and Live Systems

Screenshots may support orientation.

Screenshots are not recomputation receipts, execution receipts, source artifacts, canonical evidence packets, or proof that a sealed record reconstructs.

Live-system state is not a substitute for preserved artifacts unless the live state was itself captured, identified, and preserved according to the relevant evidence boundary.

## 12. Reviewer First Path

Recommended one-command verification:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

Recommended reading path:

1. docs/CURRENT_PROOF_SURFACE_v0_1.md
2. docs/REVIEWER_START_HERE_v0_1.md
3. docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md
4. docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
5. docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
6. docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md

## 13. Non-Authority Boundary

This current proof-surface index does not validate Fork, certify Fork, endorse Fork, approve Fork, establish compliance, establish legal sufficiency, establish safety, establish production readiness, or assert that any underlying AI-assisted workflow was correct.

It exists to make the public proof surface inspectable and to reduce overread.
'@

$verifier = @'
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
        name   = $Name
        passed = $Passed
        detail = $Detail
        data   = $Data
    }
}

function Test-RequiredPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (Test-Path $Path) {
        return New-Result -Name "path:$Path" -Passed $true -Detail "present"
    }

    return New-Result -Name "path:$Path" -Passed $false -Detail "missing"
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
        name      = $Name
        command   = $Command
        arguments = $Arguments
        exit_code = $exitCode
        output    = ($output -join "`n")
    }
}

Assert-RepoRoot

$results = New-Object System.Collections.Generic.List[object]

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
    $results.Add((Test-RequiredPath -Path $path)) | Out-Null
}

$pythonCmd = Get-PythonCommand

$boundaryChecker = Invoke-External `
    -Name "boundary-pressure-checker" `
    -Command $pythonCmd `
    -Arguments @("tools/check_boundary_pressure_review_cases_v0_1.py", "--json")

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

$results.Add((
    New-Result `
        -Name "checker:boundary-pressure" `
        -Passed $checkerPassed `
        -Detail "python tools/check_boundary_pressure_review_cases_v0_1.py --json" `
        -Data $checkerData
)) | Out-Null

if (-not $SkipGitChecks) {
    $gitDiffCheck = Invoke-External `
        -Name "git-diff-check" `
        -Command "git" `
        -Arguments @("diff", "--check")

    $results.Add((
        New-Result `
            -Name "git:diff-check" `
            -Passed ($gitDiffCheck.exit_code -eq 0) `
            -Detail $gitDiffCheck.output `
            -Data $gitDiffCheck
    )) | Out-Null

    $gitCachedDiffCheck = Invoke-External `
        -Name "git-diff-cached-check" `
        -Command "git" `
        -Arguments @("diff", "--cached", "--check")

    $results.Add((
        New-Result `
            -Name "git:diff-cached-check" `
            -Passed ($gitCachedDiffCheck.exit_code -eq 0) `
            -Detail $gitCachedDiffCheck.output `
            -Data $gitCachedDiffCheck
    )) | Out-Null
}

$passedCount = @($results | Where-Object { $_.passed }).Count
$totalCount = @($results).Count
$failedCount = $totalCount - $passedCount

$summary = [ordered]@{
    verifier                = "verify_public_review_package_v0_1.ps1"
    status                  = $(if ($failedCount -eq 0) { "PUBLIC_REVIEW_PACKAGE_VERIFY_PASS" } else { "PUBLIC_REVIEW_PACKAGE_VERIFY_FAIL" })
    total                   = $totalCount
    passed                  = $passedCount
    failed                  = $failedCount
    results                 = $results
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
        $mark = if ($result.passed) { "PASS" } else { "FAIL" }
        Write-Host "$mark $($result.name)"
        if (-not $result.passed -and $result.detail) {
            Write-Host "  $($result.detail)"
        }
    }

    if ($checkerData -and $checkerData.total -ne $null) {
        Write-Host ""
        Write-Host "Boundary pressure checker:"
        Write-Host "  total: $($checkerData.total)"
        Write-Host "  passed: $($checkerData.passed)"
        Write-Host "  failed: $($checkerData.failed)"
    }
}

if ($failedCount -ne 0) {
    exit 1
}

exit 0
'@

Write-Utf8Lf -Path $proofSurfacePath -Content $proofSurface
Write-Utf8Lf -Path $verifierPath -Content $verifier

$readmeBlock = @'
Current proof surface and public verifier
Reviewers can inspect the current bounded proof surface here:
docs/CURRENT_PROOF_SURFACE_v0_1.md

Run the current public review verifier from the repository root:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier checks required public-review files and executes the stable boundary-pressure checker. It does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, or institutional authority.
'@

$publicIndexBlock = @'
Current proof surface and verifier
Start here for the current public proof surface:
docs/CURRENT_PROOF_SURFACE_v0_1.md

Run the public review verifier:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier checks the current public-review routing surface and runs the stable boundary-pressure checker. Passing verification is not certification, endorsement, legal sufficiency, compliance sufficiency, safety, production readiness, procurement approval, or institutional authority.
'@

$reviewerStartBlock = @'
One-command public verification
From the repository root, run:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

Then read:
docs/CURRENT_PROOF_SURFACE_v0_1.md

The verifier checks the public review package surface and the stable boundary-pressure checker only. It does not validate truth, compliance, legal sufficiency, authorization, approval, safety, or production readiness.
'@

Replace-OrAppendBlock -Path "README.md" `
    -BlockId "FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER" `
    -Content $readmeBlock

Replace-OrAppendBlock -Path "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
    -BlockId "FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER" `
    -Content $publicIndexBlock

Replace-OrAppendBlock -Path "docs/REVIEWER_START_HERE_v0_1.md" `
    -BlockId "FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER" `
    -Content $reviewerStartBlock

Write-Host ""
Write-Host "Created or updated:"
Write-Host " $proofSurfacePath"
Write-Host " $verifierPath"
Write-Host " README.md"
Write-Host " docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md"
Write-Host " docs/REVIEWER_START_HERE_v0_1.md"
Write-Host ""
Write-Host "Running public verifier..."

powershell -ExecutionPolicy Bypass -File $verifierPath

if ($LASTEXITCODE -ne 0) {
    throw "Public verifier failed."
}

Write-Host ""
Write-Host "Running whitespace check..."
Invoke-Git -Args @("diff", "--check")

Write-Host ""
Write-Host "Changed files:"
git status --short

Write-Host ""
Write-Host "Review commands:"
Write-Host " git diff -- docs\CURRENT_PROOF_SURFACE_v0_1.md"
Write-Host " git diff -- scripts\verify_public_review_package_v0_1.ps1"
Write-Host " git diff -- README.md docs\PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md docs\REVIEWER_START_HERE_v0_1.md"
Write-Host " powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1"
Write-Host " git diff --check"

if ($Commit) {
    Invoke-Git -Args @(
        "add", "--",
        $proofSurfacePath,
        $verifierPath,
        "README.md",
        "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        $addScriptPath
    )

    Invoke-Git -Args @("diff", "--cached", "--check")
    Invoke-Git -Args @("commit", "-m", "Add public review verifier and current proof surface index")

    if ($Push) {
        Invoke-Git -Args @("push")
    }
}

Write-Host ""
Write-Host "Done."

# This commit should be clean and compact: one verifier, one proof-surface index, and three routing blocks.