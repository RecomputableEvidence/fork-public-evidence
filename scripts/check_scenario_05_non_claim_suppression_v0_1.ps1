# scripts/check_scenario_05_non_claim_suppression_v0_1.ps1
# Validates Scenario 05 policy-reference laundering / non-claim suppression artifacts.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Checking Scenario 05 required files..."

$required = @(
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

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required Scenario 05 file: $path"
        exit 1
    }

    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 05 JSON artifacts..."

$jsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $jsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    } catch {
        Write-Host "FAIL: invalid JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Checking Scenario 05 semantic classifications..."

$bdr = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json" | ConvertFrom-Json
$cbc = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json" | ConvertFrom-Json
$cce = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json" | ConvertFrom-Json
$smr = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json" | ConvertFrom-Json
$sle = Get-Content -Raw -Path "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json" | ConvertFrom-Json

if ($bdr.delta_classification.non_claims -ne "SUPPRESSED") {
    Write-Host "FAIL: Scenario 05 BDR must classify non_claims as SUPPRESSED"
    exit 1
}

if ($bdr.delta_classification.policy_reference -ne "LAUNDERED") {
    Write-Host "FAIL: Scenario 05 BDR must classify policy_reference as LAUNDERED"
    exit 1
}

if ($bdr.downstream_suppression.new_compliance_determination_present -ne $false) {
    Write-Host "FAIL: Scenario 05 downstream suppression must not include a new compliance determination"
    exit 1
}

if ($cbc.suppression_guard.policy_reference_may_be_treated_as_policy_satisfaction -ne $false) {
    Write-Host "FAIL: Scenario 05 CBC must forbid treating policy reference as policy satisfaction"
    exit 1
}

if ($cbc.suppression_guard.positive_claim_may_be_preserved_without_material_limitations -ne $false) {
    Write-Host "FAIL: Scenario 05 CBC must forbid preserving positive claim without material limitations"
    exit 1
}

if ($cce.classification.primary_category -ne "NON_CLAIM_SUPPRESSION") {
    Write-Host "FAIL: Scenario 05 CCE primary category must be NON_CLAIM_SUPPRESSION"
    exit 1
}

if ($cce.classification.consumption_classification -ne "NON_CLAIM_SUPPRESSION_UNSUPPORTED") {
    Write-Host "FAIL: Scenario 05 CCE consumption classification must be NON_CLAIM_SUPPRESSION_UNSUPPORTED"
    exit 1
}

if ($smr.non_claim_mapping.downstream_non_claims_preserved -ne $false) {
    Write-Host "FAIL: Scenario 05 SMR must record downstream non-claims as not preserved"
    exit 1
}

if ($sle.category -ne "NON_CLAIM_SUPPRESSION") {
    Write-Host "FAIL: Scenario 05 suppressed limitations event category must be NON_CLAIM_SUPPRESSION"
    exit 1
}

if ($sle.fork_result -ne "NON_CLAIM_SUPPRESSION_EXPOSED") {
    Write-Host "FAIL: Scenario 05 suppressed limitations event fork_result must be NON_CLAIM_SUPPRESSION_EXPOSED"
    exit 1
}

Write-Host "PASS: Scenario 05 non-claim suppression and policy-reference laundering classifications are bounded and explicit."

Write-Host ""
Write-Host "Scanning Scenario 05 surface for prohibited overclaim language..."

$scanFiles = @(
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md"
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

$violations = @()

foreach ($file in $scanFiles) {
    foreach ($pattern in $patterns) {
        $matches = Select-String -Path $file -Pattern $pattern -SimpleMatch -CaseSensitive:$false
        foreach ($match in $matches) {
            $violations += [PSCustomObject]@{
                Path = $file
                LineNumber = $match.LineNumber
                Pattern = $pattern
                Line = $match.Line.Trim()
            }
        }
    }
}

if ($violations.Count -gt 0) {
    Write-Host "FAIL: prohibited Scenario 05 overclaim language found:"
    foreach ($v in $violations) {
        Write-Host "$($v.Path):$($v.LineNumber):[$($v.Pattern)] $($v.Line)"
    }
    exit 1
}

Write-Host "PASS: no prohibited Scenario 05 overclaim language found."
Write-Host ""
Write-Host "PASS: Scenario 05 policy-reference laundering / non-claim suppression checks completed."