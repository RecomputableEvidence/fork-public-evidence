# scripts/run_ahi_sim_v0_1_checks.ps1
# Focused checks for Fork Governance Simulation Proof Surface v0.1.x.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Checking required simulation files..."
$required = @(
    "docs/simulations/FORK_SIMULATION_PROOF_SURFACE_DOCTRINE_v0_1.md",
    "docs/simulations/FORK_GOVERNANCE_SIMULATION_SEQUENCE_v0_1.md",
    "docs/simulations/FORK_SIMULATION_CONTRACTS_AND_INTERFACES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_FAILURE_MODES_v0_1.md",
    "docs/simulations/FORK_SIMULATION_RECONSTRUCTION_GUIDE_v0_1.md",
    "examples/simulations/governance-proof-surface/README.md",
    "examples/simulations/governance-proof-surface/scenario_01_baseline_unbounded_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_02_fork_preserved_handoff.md",
    "examples/simulations/governance-proof-surface/scenario_03_scope_expansion_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_04_authority_leakage_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/scenario_06_multi_system_distributed_handoff.md",
    "examples/simulations/governance-proof-surface/artifacts/README.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_authority_policy_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_non_claims_panel.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating simulation JSON artifacts..."

$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_03_unsupported_inheritance_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json"
)

foreach ($path in $jsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    }
    catch {
        Write-Host "FAIL: invalid JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Checking Scenario 04 semantic classifications..."

$cce04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_claim_consumption_event.json" | ConvertFrom-Json
$uie04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_unsupported_inheritance_event.json" | ConvertFrom-Json
$bdr04 = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_04_boundary_delta_record.json" | ConvertFrom-Json

if ($cce04.classification.consumption_classification -ne "AUTHORITY_LEAKAGE_UNSUPPORTED") {
    Write-Host "FAIL: Scenario 04 CCE must classify consumption as AUTHORITY_LEAKAGE_UNSUPPORTED"
    exit 1
}

if ($uie04.category -ne "AUTHORITY_LEAKAGE") {
    Write-Host "FAIL: Scenario 04 UIE primary category must be AUTHORITY_LEAKAGE"
    exit 1
}

if ($bdr04.delta_classification.authority_context -ne "LEAKED") {
    Write-Host "FAIL: Scenario 04 BDR authority_context must be LEAKED"
    exit 1
}

if ($bdr04.downstream_authority_leakage.new_approval_record_present -ne $false) {
    Write-Host "FAIL: Scenario 04 must not include new approval record in the downstream authority leakage"
    exit 1
}

Write-Host "PASS: Scenario 04 authority leakage classifications are bounded and explicit."
Write-Host ""
Write-Host "Running non-claims contract checker..."
python tools\check_non_claims_contract.py

Write-Host ""
Write-Host "Scanning simulation surface for prohibited overclaim language..."

$scanRoots = @(
    "docs\simulations",
    "examples\simulations"
)

$patterns = @(
    "truth engine",
    "governance oracle",
    "compliance proof",
    "certifies compliance",
    "proves correctness",
    "proves compliance",
    "guarantees trust"
)

$scanFiles = @()
foreach ($root in $scanRoots) {
    if (Test-Path $root) {
        $scanFiles += Get-ChildItem -Path $root -Recurse -File
    }
}

$violations = @()
foreach ($file in $scanFiles) {
    foreach ($pattern in $patterns) {
        $matches = Select-String -Path $file.FullName -Pattern $pattern -SimpleMatch -CaseSensitive:$false
        foreach ($match in $matches) {
            $violations += [PSCustomObject]@{
                Path      = $file.FullName
                LineNumber = $match.LineNumber
                Pattern   = $pattern
                Line      = $match.Line.Trim()
            }
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "FAIL: prohibited simulation overclaim language found:"
    foreach ($v in $violations) {
        Write-Host "$($v.Path):$($v.LineNumber):[$($v.Pattern)] $($v.Line)"
    }
    exit 1
}

Write-Host "PASS: no prohibited simulation overclaim language found."
Write-Host ""

Write-Host ""
Write-Host "Checking Scenario 05 artifacts through main AHI checker..."
# SCENARIO_05_MAIN_CHECKER_INTEGRATION_v0_2
$scenario05RequiredFiles = @(
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $scenario05RequiredFiles) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required Scenario 05 file: $path"
        exit 1
    }

    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 05 JSON artifacts through main AHI checker..."
$scenario05JsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $scenario05JsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    } catch {
        Write-Host "FAIL: invalid Scenario 05 JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Running Scenario 05 semantic checker through main AHI checker..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_05_non_claim_suppression_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: Scenario 05 semantic checker failed inside main AHI checker"
    exit 1
}

Write-Host "PASS: Scenario 05 validation completed inside main AHI checker."


# Scenario 06 structuralization validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 06 multi-system distributed handoff through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_multi_system_distributed_handoff_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 06 checker failed."
}
Write-Host "PASS: Scenario 06 validation completed inside main AHI checker."
# Scenario 06 semantic invariant validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 06 semantic invariants through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_06_semantic_invariants_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 06 semantic invariant checker failed."
}
Write-Host "PASS: Scenario 06 semantic invariant validation completed inside main AHI checker."
# Scenario 06 semantic invariant validation END

# Scenario 06 structuralization validation END

# Scenario 07 external authority bridge validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 07 external authority bridge through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_07_external_authority_bridge_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 07 external authority bridge checker failed."
}
Write-Host "PASS: Scenario 07 validation completed inside main AHI checker."
# Scenario 07 external authority bridge validation END

# Scenario 08 stale validity / authority revocation validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 08 stale validity / authority revocation through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 08 stale validity / authority revocation checker failed."
}
Write-Host "PASS: Scenario 08 validation completed inside main AHI checker."
# Scenario 08 stale validity / authority revocation validation END
Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."