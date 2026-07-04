# scripts/check_computed_proof_surface_v0_1.ps1
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
    "README_COMPUTED_PROOF_SURFACE_v0_1.md",
    "docs\reviewer\COMPUTED_PROOF_SURFACE_v0_1.md",
    "docs\reviewer\COMPUTED_PROOF_SURFACE_REVIEW_NOTE_v0_1.md",
    "examples\simulations\governance-proof-surface\computed_proof_surface\README.md",
    "examples\simulations\governance-proof-surface\computed_proof_surface\computed_proof_surface_manifest_v0_1.json",
    "scripts\check_computed_proof_surface_v0_1.ps1",
    "scripts\check_computed_scenario_09_revocation_split_state_v0_1.ps1",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\derived_result.json",
    "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\derived_result.json"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Fail "missing required file: $path"
    }
    Write-Host "FOUND: $path"
}

$manifestPath = "examples\simulations\governance-proof-surface\computed_proof_surface\computed_proof_surface_manifest_v0_1.json"
$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

if ($manifest.manifest_id -ne "COMPUTED_PROOF_SURFACE_v0_1") {
    Fail "manifest_id mismatch"
}

if ($manifest.version -ne "v0.1") {
    Fail "manifest version mismatch"
}

$layerIds = @($manifest.surface_layers | ForEach-Object { $_.layer_id })

$requiredLayerIds = @(
    "primitive_layer",
    "scenario_layer",
    "viewer_layer",
    "computed_layer",
    "computed_proof_surface_layer"
)

foreach ($layerId in $requiredLayerIds) {
    if (-not ($layerIds -contains $layerId)) {
        Fail "missing manifest layer: $layerId"
    }
}

$derivationIds = @($manifest.computed_derivations | ForEach-Object { $_.derivation_id })
if (-not ($derivationIds -contains "computed_scenario_09_revocation_split_state_v0_1")) {
    Fail "computed Scenario 09 derivation missing from manifest"
}

$nonConclusions = @($manifest.non_conclusions)
$requiredNonConclusions = @(
    "truth_of_underlying_claim",
    "external_validity_of_underlying_claim",
    "legal_sufficiency",
    "compliance_status",
    "safety_status",
    "fault_allocation",
    "approval_status",
    "execution_eligibility",
    "business_suitability",
    "policy_correctness",
    "regulatory_adequacy"
)

foreach ($nonConclusion in $requiredNonConclusions) {
    if (-not ($nonConclusions -contains $nonConclusion)) {
        Fail "missing non-conclusion: $nonConclusion"
    }
}

$gapResult = Get-Content "examples\simulations\governance-proof-surface\computed_scenario_09\cases\visibility_gap_detected\derived_result.json" -Raw | ConvertFrom-Json
$closedResult = Get-Content "examples\simulations\governance-proof-surface\computed_scenario_09\cases\gap_closed_by_revalidation\derived_result.json" -Raw | ConvertFrom-Json

if ($gapResult.derivation_status -ne "COMPUTED_GAP_RECORDED") {
    Fail "computed proof surface expected visibility_gap_detected to be COMPUTED_GAP_RECORDED"
}

if ($closedResult.derivation_status -ne "NO_COMPUTED_GAP_RECORDED") {
    Fail "computed proof surface expected gap_closed_by_revalidation to be NO_COMPUTED_GAP_RECORDED"
}

$surfaceFiles = @(
    "README_COMPUTED_PROOF_SURFACE_v0_1.md",
    "docs\reviewer\COMPUTED_PROOF_SURFACE_v0_1.md",
    "docs\reviewer\COMPUTED_PROOF_SURFACE_REVIEW_NOTE_v0_1.md",
    "examples\simulations\governance-proof-surface\computed_proof_surface\README.md",
    "examples\simulations\governance-proof-surface\computed_proof_surface\computed_proof_surface_manifest_v0_1.json"
)

$requiredPhrases = @(
    "fixture-declared",
    "structurally checked",
    "computed derivation",
    "reconstructed",
    "preserved",
    "non-conclusions"
)

foreach ($phrase in $requiredPhrases) {
    $found = $false
    foreach ($file in $surfaceFiles) {
        $content = Get-Content $file -Raw
        if ($content -match [regex]::Escape($phrase)) {
            $found = $true
            break
        }
    }

    if (-not $found) {
        Fail "required phrase missing from computed proof surface: $phrase"
    }
}

$forbidden = @(
    "truth certified",
    "safety certified",
    "approved for use",
    "permission to rely",
    "runtime enforcement",
    "legal determination",
    "compliance determination",
    "decides fault",
    "decides liability"
)

foreach ($file in $surfaceFiles) {
    $content = Get-Content $file -Raw
    foreach ($term in $forbidden) {
        if ($content -match [regex]::Escape($term)) {
            Fail "forbidden overclaim term '$term' found in $file"
        }
    }
}

Pass "Computed Proof Surface v0.1 checks completed"
