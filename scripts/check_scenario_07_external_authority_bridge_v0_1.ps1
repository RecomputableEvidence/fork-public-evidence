# scripts/check_scenario_07_external_authority_bridge_v0_1.ps1
# Semantic checker for Scenario 07 external authority bridge.
# Scope: verifies bounded record semantics only.
# This checker does not approve, certify, score, authorize, determine compliance,
# determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }
function Require-File($Path) { if (-not (Test-Path $Path)) { Fail "missing required file: $Path" }; Write-Host "FOUND: $Path" }
function Read-Json($Path) { try { Get-Content -Raw -Path $Path | ConvertFrom-Json } catch { Fail "invalid JSON: $Path :: $($_.Exception.Message)" } }
function Arr($Value) { if ($null -eq $Value) { @() } elseif ($Value -is [System.Array]) { @($Value) } else { @($Value) } }
function Join-Text($Value) { ((Arr $Value) | ForEach-Object { if ($_ -is [string]) { $_ } else { $_ | ConvertTo-Json -Depth 20 -Compress } }) -join " | " }
function Eq($Actual, $Expected, $Label) { if ($Actual -ne $Expected) { Fail "$Label expected '$Expected' but found '$Actual'" } }
function Has($Text, $Pattern, $Label) { if ($Text -notmatch $Pattern) { Fail "$Label expected pattern '$Pattern'" } }
function True($Condition, $Label) { if (-not $Condition) { Fail $Label } }

if (-not (Test-Path ".git")) { Fail "run this script from repository root" }

$scenarioId = "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE"
$scenarioPath = "examples/simulations/governance-proof-surface/scenario_07_external_authority_bridge.md"
$root = "examples/simulations/governance-proof-surface/artifacts"

$bdrPath = "$root/scenario_07_boundary_delta_record.json"
$cbcPath = "$root/scenario_07_claim_boundary_contract.json"
$ccePath = "$root/scenario_07_claim_consumption_event.json"
$smrPath = "$root/scenario_07_system_mapping_receipt.json"
$failurePath = "$root/scenario_07_external_authority_failure_event.json"
$contextPath = "$root/scenario_07_external_review_context.md"
$graphPath = "$root/scenario_07_transition_graph.md"
$nonClaimsPath = "$root/scenario_07_non_claims_panel.md"

Write-Host "Checking Scenario 07 required files..."
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath,$contextPath,$graphPath,$nonClaimsPath)) {
    Require-File $p
}

Write-Host ""
Write-Host "Validating Scenario 07 JSON artifacts..."
$bdr = Read-Json $bdrPath
$cbc = Read-Json $cbcPath
$cce = Read-Json $ccePath
$smr = Read-Json $smrPath
$failure = Read-Json $failurePath
foreach ($p in @($bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath)) {
    Write-Host "VALID JSON: $p"
}

Write-Host ""
Write-Host "Checking scenario identity..."
foreach ($a in @($bdr,$cbc,$cce,$smr,$failure)) { Eq $a.scenario_id $scenarioId "scenario_id" }
Pass "Scenario 07 identity preserved"

Write-Host ""
Write-Host "Checking external authority bridge boundary sequence..."
Eq $bdr.external_boundary_type "EXTERNAL_AUTHORITY_BRIDGE" "BDR external_boundary_type"
Eq $bdr.inspectability_result "INSPECTABLE" "BDR inspectability_result"
Has $bdr.delta_classification "EXTERNAL_AUTHORITY_BRIDGE_EXPANSION_RECORDED" "BDR delta_classification"

$boundaries = @(Arr $bdr.boundary_sequence)
Eq $boundaries.Count 2 "BDR boundary_sequence count"
True (@($boundaries | Where-Object { $_.boundary_id -eq "S07-B01" }).Count -eq 1) "S07-B01 must be present exactly once"
True (@($boundaries | Where-Object { $_.boundary_id -eq "S07-B02" }).Count -eq 1) "S07-B02 must be present exactly once"

$b01 = @($boundaries | Where-Object { $_.boundary_id -eq "S07-B01" })[0]
Eq $b01.transition_effect "PRESERVED_FOR_EXTERNAL_INSPECTION" "S07-B01 transition_effect"
Eq $b01.authority_effect "NO_EXTERNAL_AUTHORITY_TRANSFER" "S07-B01 authority_effect"
Has $b01.claim_state_after_transition "no external admissibility|authority transfers" "S07-B01 claim_state_after_transition"

$b02 = @($boundaries | Where-Object { $_.boundary_id -eq "S07-B02" })[0]
Eq $b02.transition_effect "EXTERNAL_INTERPRETATION_ATTEMPT_RECORDED" "S07-B02 transition_effect"
Eq $b02.authority_effect "UNSUPPORTED_EXTERNAL_AUTHORITY_INFERENCE" "S07-B02 authority_effect"
Has $b02.claim_state_after_transition "authority-bearing conclusion|does not support" "S07-B02 claim_state_after_transition"
Pass "external authority bridge boundaries are explicit"

Write-Host ""
Write-Host "Checking unsupported external conclusions and required revalidation..."
$notSupported = Join-Text $bdr.downstream_state.not_supported_after_transition
foreach ($t in @("external admissibility","regulatory compliance determination","legal sufficiency","external approval","audit acceptance","customer acceptance","board authorization","insurance coverage","execution eligibility")) {
    Has $notSupported $t "BDR not_supported_after_transition"
}

$required = Join-Text $bdr.required_revalidation_for
foreach ($t in @("external admissibility","regulatory compliance determination","legal sufficiency","external approval","customer acceptance","board authorization","insurance coverage","execution eligibility")) {
    Has $required $t "BDR required_revalidation_for"
}
Pass "unsupported external conclusions remain unsupported"

Write-Host ""
Write-Host "Checking CBC non-inheritance boundary..."
$blocked = Join-Text $cbc.claims_not_allowed_to_be_inferred
foreach ($t in @("external admissibility","regulatory compliance determination","legal sufficiency","external approval authority","audit acceptance","customer acceptance","board authorization","insurance coverage","execution eligibility")) {
    Has $blocked $t "CBC claims_not_allowed_to_be_inferred"
}
Has $cbc.non_inheritance_rule "No external authority-bearing property transfers" "CBC non_inheritance_rule"
Eq $cbc.external_authority_boundary.bridge_result "REQUIRES_SEPARATE_EXTERNAL_AUTHORITY" "CBC bridge_result"
Pass "CBC prohibits external authority inference"

Write-Host ""
Write-Host "Checking CCE expanded external consumption..."
Eq $cce.consumer_identity "SYSTEM_C_EXTERNAL_AUTHORITY_CONTEXT" "CCE consumer_identity"
Eq $cce.classification "EXPANDED" "CCE classification"
Eq $cce.boundary_effect "EXPANDED_BEYOND_RECORDED_CLAIM_SCOPE" "CCE boundary_effect"
Eq $cce.new_claim_boundary_contract_id "REQUIRED_BUT_ABSENT" "CCE new_claim_boundary_contract_id"
Has $cce.required_next_action "separate external-authority claim boundary contract|external authority decision" "CCE required_next_action"
Pass "CCE records expanded external consumption"

Write-Host ""
Write-Host "Checking SMR unsupported external authority mapping..."
Has $smr.overall_mapping_classification "UNSUPPORTED_EXTERNAL_AUTHORITY_INHERITANCE" "SMR overall_mapping_classification"
Eq $smr.fork_result "STRUCTURAL_MAPPING_RECORDED" "SMR fork_result"
Eq $smr.external_mapping_status "EXTERNAL_AUTHORITY_INFERENCE_NOT_SUPPORTED" "SMR external_mapping_status"
$unsupported = @(Arr $smr.unsupported_mappings)
True ($unsupported.Count -ge 3) "SMR must include at least three unsupported mappings"
Has (Join-Text $unsupported) "admissibility|compliance|legal sufficiency|approval" "SMR unsupported mapping list"
Pass "SMR records unsupported external authority mapping"

Write-Host ""
Write-Host "Checking external authority failure event..."
Eq $failure.category "EXTERNAL_AUTHORITY_BRIDGE_ATTEMPT" "failure category"
Eq $failure.record_support "NOT_SUPPORTED" "failure record_support"
Eq $failure.boundary_effect "EXPANDED" "failure boundary_effect"
Eq $failure.fork_result "UNSUPPORTED_EXTERNAL_AUTHORITY_INFERENCE_RECORDED" "failure fork_result"
Has $failure.attempted_inference "admissibility|compliance|legal sufficiency|acceptance|authority" "failure attempted_inference"
$failureRequired = Join-Text $failure.required_revalidation
foreach ($t in @("external admissibility","regulatory compliance determination","legal sufficiency","external approval","customer acceptance","execution eligibility")) {
    Has $failureRequired $t "failure required_revalidation"
}
Pass "failure event records unsupported external authority bridge"

Write-Host ""
Write-Host "Scanning Scenario 07 surface for non-authority posture..."
$scan = ""
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath,$contextPath,$graphPath,$nonClaimsPath)) {
    $scan += "`n--- $p ---`n" + (Get-Content -Raw -Path $p)
}

foreach ($t in @("does not approve","certify","score","authorize","determine compliance","determine admissibility","establish legal sufficiency","judge correctness")) {
    Has $scan ([regex]::Escape($t)) "non-authority posture"
}

$prohibitedPhrases = @(
    "Fork approved",
    "Fork approves",
    "Fork certified",
    "Fork certifies",
    "Fork authorized",
    "Fork authorizes",
    "Fork scored",
    "Fork scores",
    "approved by Fork",
    "authorized by Fork",
    "certified by Fork",
    "admissible because Fork",
    "compliant because Fork",
    "legally sufficient because Fork",
    "risk score",
    "go/no-go"
)

foreach ($phrase in $prohibitedPhrases) {
    if ($scan.ToLowerInvariant().Contains($phrase.ToLowerInvariant())) {
        Fail "prohibited Scenario 07 overclaim phrase found: $phrase"
    }
}

Pass "Scenario 07 non-authority posture is preserved"

Write-Host ""
Pass "Scenario 07 external authority bridge checks completed"
