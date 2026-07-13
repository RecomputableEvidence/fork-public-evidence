[CmdletBinding()]
param(
    [string]$RepoRoot = "",
    [switch]$SkipLegacyPublicVerifier
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-RepoRoot {
    param([string]$Candidate)
    if ($Candidate) {
        return (Resolve-Path -LiteralPath $Candidate).Path
    }
    $current = (Get-Location).Path
    while ($current) {
        if ((Test-Path -LiteralPath (Join-Path $current ".git")) -and
            (Test-Path -LiteralPath (Join-Path $current "README.md"))) {
            return $current
        }
        $parent = Split-Path -Parent $current
        if ($parent -eq $current) { break }
        $current = $parent
    }
    throw "Could not locate repository root."
}

function Resolve-PythonCommand {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return @("python")
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        return @("py", "-3")
    }
    throw "Python 3 was not found."
}

function Invoke-PythonStep {
    param(
        [string]$Name,
        [string[]]$Arguments,
        [switch]$Optional
    )
    $target = $Arguments[0]
    if ($Optional -and -not (Test-Path -LiteralPath (Join-Path $script:Root $target))) {
        Write-Host "[SKIP] $Name - missing optional path $target"
        return
    }

    Write-Host ""
    Write-Host "== $Name =="
    $pythonCommand = @($script:Python)
    if ($pythonCommand.Count -lt 1) {
        throw "Python command resolution returned no executable."
    }
    $exe = [string]$pythonCommand[0]
    $prefix = @()
    if ($pythonCommand.Count -gt 1) {
        $prefix = $pythonCommand[1..($pythonCommand.Count - 1)]
    }
    & $exe @prefix @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE."
    }
    Write-Host "[PASS] $Name"
}

$script:Root = Resolve-RepoRoot -Candidate $RepoRoot
Set-Location -LiteralPath $script:Root
$script:Python = @(Resolve-PythonCommand)

Write-Host "Fork proof-surface verification"
Write-Host "Repository: $script:Root"

if (-not $SkipLegacyPublicVerifier) {
    $legacy = Join-Path $script:Root "scripts\verify_public_review_package_v0_1.ps1"
    if (Test-Path -LiteralPath $legacy) {
        Write-Host ""
        Write-Host "== Existing public-review verifier =="
        & powershell -NoProfile -ExecutionPolicy Bypass -File $legacy
        if ($LASTEXITCODE -ne 0) {
            throw "Existing public-review verifier failed with exit code $LASTEXITCODE."
        }
        Write-Host "[PASS] Existing public-review verifier"
    }
}

Invoke-PythonStep -Name "Canonical proof-surface state" -Arguments @(
    "tools/check_fork_proof_surface_state_v0_1.py", "--json", "--check-summary"
)
Invoke-PythonStep -Name "Mechanical JSON Schema bundle" -Arguments @(
    "tools/validate_json_schema_bundle_v0_1.py", "--json"
)
Invoke-PythonStep -Name "Reviewer access-path integrity v0.1.2" -Arguments @(
    "tools/check_reviewer_access_path_integrity_v0_1.py", "--json"
)
Invoke-PythonStep -Name "Public Review Round 006" -Arguments @(
    "tools/check_public_review_round_006_observations_v0_1.py", "--json"
)
Invoke-PythonStep -Name "Cross-System Claim Handoff scaffold" -Arguments @(
    "tools/check_cross_system_claim_handoff_v0_1.py", "--json"
)

Invoke-PythonStep -Name "Cross-System Claim Handoff configuration" -Arguments @(
    "tools/check_csh_configuration_v0_1.py",
    "--json"
)

# ASI_POWERSHELL_INTEGRATION_START
Invoke-PythonStep -Name "Authority State Invariance and Transition Model" -Arguments @(
    "tools/check_authority_state_invariance_v0_1.py", "--json"
)
# ASI_POWERSHELL_INTEGRATION_END
Invoke-PythonStep -Name "Boundary-pressure default and adversarial suite" -Arguments @(
    "tools/check_boundary_pressure_review_cases_v0_1.py", "--json", "--run-adversarial"
) -Optional
Invoke-PythonStep -Name "Longitudinal Day-0 packet" -Arguments @(
    "tools/check_longitudinal_reconstruction_day0_packet_v0_1.py", "--json"
) -Optional
Invoke-PythonStep -Name "Longitudinal Day-0 adversarial cases" -Arguments @(
    "tools/check_longitudinal_day0_adversarial_cases_v0_1.py", "--json"
) -Optional
Invoke-PythonStep -Name "Longitudinal Day-0 schema scope" -Arguments @(
    "tools/check_longitudinal_day0_schema_scope_v0_1.py", "--json"
) -Optional
Invoke-PythonStep -Name "Longitudinal Day-0 temporal replay receipt" -Arguments @(
    "tools/check_longitudinal_day0_temporal_replay_receipt_v0_1.py", "--json"
) -Optional
Invoke-PythonStep -Name "Public Review Round 005" -Arguments @(
    "tools/check_public_review_round_005_interactions_v0_1.py", "--json"
) -Optional

if (Test-Path -LiteralPath (Join-Path $script:Root "tools\check_claim_inheritance_simulation_model.py")) {
    Invoke-PythonStep -Name "Claim-inheritance valid synthetic bundle" -Arguments @(
        "tools/check_claim_inheritance_simulation_model.py",
        "examples/claim_inheritance_simulation_model/synthetic_claim_inheritance_simulation_bundle_v0_1.json",
        "--pretty"
    )
    Invoke-PythonStep -Name "Claim-inheritance invalid manifest harness" -Arguments @(
        "tools/check_claim_inheritance_simulation_model.py", "--invalid-manifest", "--pretty"
    )
}

Invoke-PythonStep -Name "New convergence regression tests" -Arguments @(
    "-m", "pytest",
    "tests/test_reviewer_access_path_integrity_v0_1.py",
    "tests/test_public_review_round_006_observations_v0_1.py",
    "tests/test_cross_system_claim_handoff_v0_1.py",
    "tests/test_csh_configuration_v0_1.py",
    "tests/test_experimental_convergence_v0_1.py",
    "tests/test_authority_state_invariance_v0_1.py",
    "-q"
)

Write-Host ""
Write-Host "FORK_PROOF_SURFACE_INTEGRATION_PASS"
Write-Host "Bounded interpretation: required convergence artifacts and available structural checkers passed."
Write-Host "No truth, compliance, legal sufficiency, safety, authorization, approval, certification,"
Write-Host "endorsement, production readiness, or institutional authority is established."

# BEGIN CSH_EXECUTION_INSTRUMENTATION_V0_1_1
Write-Host ""
Write-Host "== CSH v0.1.1 execution instrumentation =="
& python tools/check_cross_system_claim_handoff_execution_v0_1_1.py --json
if ($LASTEXITCODE -ne 0) {
    throw "CSH v0.1.1 execution instrumentation checker failed with exit code $LASTEXITCODE."
}
& python -m pytest tests/test_cross_system_claim_handoff_execution_v0_1_1.py -q
if ($LASTEXITCODE -ne 0) {
    throw "CSH v0.1.1 execution instrumentation tests failed with exit code $LASTEXITCODE."
}
# END CSH_EXECUTION_INSTRUMENTATION_V0_1_1
