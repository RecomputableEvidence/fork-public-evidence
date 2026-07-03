# scripts/check_computed_scenario_09_revocation_split_state_v0_1.ps1
$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    exit 1
}

function Pass($Message) {
    Write-Host "PASS: $Message" -ForegroundColor Green
}

if (-not (Test-Path ".git")) {
    Fail "Run from repository root."
}

$required = @(
    "README_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md",
    "docs\reviewer\AHI_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md",
    "examples\simulations\governance-proof-surface\computed_scenario_09\README.md",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\system_a_current_revocation_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\system_b_visibility_sync_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\system_c_consumption_attempt_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\freshness_policy.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\expected_derived_result.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\system_a_current_revocation_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\system_b_visibility_sync_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\system_c_consumption_attempt_state.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\freshness_policy.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\expected_derived_result.json",
    "scripts\derive_computed_scenario_09_revocation_split_state_v0_1.py"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Fail "missing required file: $path"
    }
    Write-Host "FOUND: $path"
}

python -m py_compile scripts\derive_computed_scenario_09_revocation_split_state_v0_1.py

python scripts\derive_computed_scenario_09_revocation_split_state_v0_1.py --write

$gapResult = Get-Content "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\derived_result.json" -Raw | ConvertFrom-Json
$closedResult = Get-Content "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\derived_result.json" -Raw | ConvertFrom-Json

if ($gapResult.derivation_status -ne "COMPUTED_GAP_RECORDED") {
    Fail "visibility_gap_detected did not compute COMPUTED_GAP_RECORDED"
}

if (-not ($gapResult.gap_types -contains "REVOCATION_VISIBILITY_GAP")) {
    Fail "visibility_gap_detected missing REVOCATION_VISIBILITY_GAP"
}

if (-not ($gapResult.gap_types -contains "SPLIT_STATE_CONSUMPTION_GAP")) {
    Fail "visibility_gap_detected missing SPLIT_STATE_CONSUMPTION_GAP"
}

if ($closedResult.derivation_status -ne "NO_COMPUTED_GAP_RECORDED") {
    Fail "gap_closed_by_revalidation did not compute NO_COMPUTED_GAP_RECORDED"
}

$scanPaths = @(
    "README_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md",
    "docs\reviewer\AHI_COMPUTED_SCENARIO_09_REVOCATION_SPLIT_STATE_v0_1.md",
    "examples\simulations\governance-proof-surface\computed_scenario_09",
    "scripts\derive_computed_scenario_09_revocation_split_state_v0_1.py"
)

$forbidden = @(
    "legally sufficient",
    "compliant",
    "authorized",
    "safe to execute",
    "negligent",
    "fault established",
    "truth certified"
)

foreach ($path in $scanPaths) {
    if (-not (Test-Path $path)) { continue }

    $items = @()
    if ((Get-Item $path).PSIsContainer) {
        $items = Get-ChildItem $path -Recurse -File
    } else {
        $items = @(Get-Item $path)
    }

    foreach ($item in $items) {
        $content = Get-Content $item.FullName -Raw
        foreach ($term in $forbidden) {
            if ($content -match [regex]::Escape($term)) {
                Fail "forbidden overclaim term '$term' found in $($item.FullName)"
            }
        }
    }
}

Pass "computed Scenario 09 revocation split-state derivation checks completed"
