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
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_non_claims_panel.md"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 02 JSON artifacts..."
$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_02_unsupported_inheritance_event.json"
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
Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."