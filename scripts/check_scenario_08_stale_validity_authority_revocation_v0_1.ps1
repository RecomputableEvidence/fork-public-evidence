# scripts/check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
# Semantic checker for Scenario 08 stale validity / authority revocation boundary.
# Scope: verifies bounded temporal validity and revocation-state semantics only.

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

$scenarioId = "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY"
$scenarioPath = "examples/simulations/governance-proof-surface/scenario_08_stale_validity_authority_revocation_boundary.md"
$root = "examples/simulations/governance-proof-surface/artifacts"

$bdrPath = "$root/scenario_08_boundary_delta_record.json"
$cbcPath = "$root/scenario_08_claim_boundary_contract.json"
$ccePath = "$root/scenario_08_claim_consumption_event.json"
$smrPath = "$root/scenario_08_system_mapping_receipt.json"
$revPath = "$root/scenario_08_revocation_event.json"
$timelinePath = "$root/scenario_08_validity_timeline.md"
$graphPath = "$root/scenario_08_transition_graph.md"
$nonClaimsPath = "$root/scenario_08_non_claims_panel.md"

Write-Host "Checking Scenario 08 required files..."
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$revPath,$timelinePath,$graphPath,$nonClaimsPath)) {
    Require-File $p
}

Write-Host ""
Write-Host "Validating Scenario 08 JSON artifacts..."
$bdr = Read-Json $bdrPath
$cbc = Read-Json $cbcPath
$cce = Read-Json $ccePath
$smr = Read-Json $smrPath
$rev = Read-Json $revPath
foreach ($p in @($bdrPath,$cbcPath,$ccePath,$smrPath,$revPath)) {
    Write-Host "VALID JSON: $p"
}

Write-Host ""
Write-Host "Checking scenario identity..."
foreach ($a in @($bdr,$cbc,$cce,$smr,$rev)) { Eq $a.scenario_id $scenarioId "scenario_id" }
Pass "Scenario 08 identity preserved"

Write-Host ""
Write-Host "Checking temporal validity boundary sequence..."
Eq $bdr.boundary_type "TEMPORAL_VALIDITY_AND_AUTHORITY_REVOCATION" "BDR boundary_type"
Eq $bdr.inspectability_result "INSPECTABLE" "BDR inspectability_result"
Eq $bdr.delta_classification "STALE_VALIDITY_RELIANCE_ATTEMPT_RECORDED" "BDR delta_classification"
Has $bdr.temporal_invariant "valid_at_T1_does_not_imply_valid_at_T3" "BDR temporal invariant"

$boundaries = @(Arr $bdr.boundary_sequence)
Eq $boundaries.Count 3 "BDR boundary_sequence count"
foreach ($id in @("S08-B01","S08-B02","S08-B03")) {
    True (@($boundaries | Where-Object { $_.boundary_id -eq $id }).Count -eq 1) "$id must be present exactly once"
}

$b01 = @($boundaries | Where-Object { $_.boundary_id -eq "S08-B01" })[0]
Eq $b01.transition_effect "PRIOR_VALIDITY_RECORDED" "S08-B01 transition_effect"
Eq $b01.authority_effect "AUTHORITY_CONTEXT_BOUNDED_TO_T1" "S08-B01 authority_effect"
Has $b01.claim_state_after_transition "does not establish current authority" "S08-B01 claim_state_after_transition"

$b02 = @($boundaries | Where-Object { $_.boundary_id -eq "S08-B02" })[0]
Eq $b02.transition_effect "VALIDITY_STATE_CHANGED" "S08-B02 transition_effect"
Eq $b02.authority_effect "PRIOR_AUTHORITY_NOT_CURRENT_AUTHORITY" "S08-B02 authority_effect"
Has $b02.claim_state_after_transition "requires current revalidation" "S08-B02 claim_state_after_transition"

$b03 = @($boundaries | Where-Object { $_.boundary_id -eq "S08-B03" })[0]
Eq $b03.transition_effect "STALE_VALIDITY_RELIANCE_ATTEMPT_RECORDED" "S08-B03 transition_effect"
Eq $b03.authority_effect "UNSUPPORTED_CURRENT_AUTHORITY_INFERENCE" "S08-B03 authority_effect"
Has $b03.claim_state_after_transition "prior validity as current validity|does not support" "S08-B03 claim_state_after_transition"

Pass "temporal validity boundary chain is explicit"

Write-Host ""
Write-Host "Checking unsupported current conclusions and required revalidation..."
$notSupported = Join-Text $bdr.not_supported_after_transition
foreach ($t in @("current authority","current approval","current policy satisfaction","current regulatory compliance","current legal sufficiency","current evidence sufficiency","current execution eligibility","current external acceptance")) {
    Has $notSupported $t "BDR not_supported_after_transition"
}

$required = Join-Text $bdr.required_revalidation_for
foreach ($t in @("current authority","current policy version","current evidence basis","current role or delegation","current purpose","current operating environment","current approval eligibility","current execution eligibility")) {
    Has $required $t "BDR required_revalidation_for"
}
Pass "unsupported current conclusions remain unsupported"

Write-Host ""
Write-Host "Checking CBC temporal non-inheritance boundary..."
$blocked = Join-Text $cbc.claims_not_allowed_to_be_inferred
foreach ($t in @("prior validity establishes current validity","prior authority establishes current authority","prior policy reference establishes current policy satisfaction","prior evidence establishes current evidence sufficiency","prior approval establishes current approval eligibility","prior compliance posture establishes current compliance","prior legal review establishes current legal sufficiency","prior execution eligibility establishes current execution eligibility")) {
    Has $blocked ([regex]::Escape($t)) "CBC claims_not_allowed_to_be_inferred"
}
Has $cbc.non_inheritance_rule "No current authority-bearing or validity-bearing property transfers" "CBC non_inheritance_rule"
Eq $cbc.temporal_boundary.bridge_result "REQUIRES_CURRENT_REVALIDATION" "CBC bridge_result"
Pass "CBC prohibits stale validity inheritance"

Write-Host ""
Write-Host "Checking CCE expanded stale-validity consumption..."
Eq $cce.consumer_identity "SYSTEM_C_DOWNSTREAM_RELIANCE_ACTOR" "CCE consumer_identity"
Eq $cce.classification "EXPANDED" "CCE classification"
Eq $cce.boundary_effect "EXPANDED_BEYOND_CURRENT_VALIDITY_SCOPE" "CCE boundary_effect"
Eq $cce.new_claim_boundary_contract_id "REQUIRED_BUT_ABSENT" "CCE new_claim_boundary_contract_id"
Has $cce.required_next_action "current-validity claim boundary contract|current authority" "CCE required_next_action"
Eq $cce.fork_result "STALE_VALIDITY_CONSUMPTION_RECORDED_NOT_AUTHORIZED" "CCE fork_result"
Pass "CCE records expanded stale-validity consumption"

Write-Host ""
Write-Host "Checking SMR unsupported stale-validity mapping..."
Has $smr.overall_mapping_classification "UNSUPPORTED_STALE_VALIDITY_INHERITANCE" "SMR overall_mapping_classification"
Eq $smr.fork_result "STRUCTURAL_MAPPING_RECORDED" "SMR fork_result"
Eq $smr.temporal_mapping_status "STALE_VALIDITY_INFERENCE_NOT_SUPPORTED" "SMR temporal_mapping_status"
$unsupported = @(Arr $smr.unsupported_mappings)
True ($unsupported.Count -ge 3) "SMR must include at least three unsupported mappings"
Has (Join-Text $unsupported) "prior validity|current validity|prior authority|current authority|current evidence sufficiency" "SMR unsupported mapping list"
Pass "SMR records unsupported stale-validity mapping"

Write-Host ""
Write-Host "Checking revocation event..."
Eq $rev.category "STALE_VALIDITY_RELIANCE_ATTEMPT" "revocation category"
Eq $rev.record_support "NOT_SUPPORTED" "revocation record_support"
Eq $rev.boundary_effect "EXPANDED" "revocation boundary_effect"
Eq $rev.fork_result "UNSUPPORTED_STALE_VALIDITY_INFERENCE_RECORDED" "revocation fork_result"
Has $rev.validity_change_type "REVOCATION_OR_EXPIRY_OR_SUPERSESSION_OR_NARROWING" "revocation validity_change_type"
Has $rev.attempted_inference "Prior validity|current validity|current authority|current execution eligibility" "revocation attempted_inference"

$revRequired = Join-Text $rev.required_revalidation
foreach ($t in @("current authority","current policy version","current evidence basis","current role or permission","current purpose","current operating environment","current validity window","current execution eligibility")) {
    Has $revRequired $t "revocation required_revalidation"
}
Pass "revocation event records unsupported stale-validity inference"

Write-Host ""
Write-Host "Scanning Scenario 08 surface for non-authority posture..."
$scan = ""
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$revPath,$timelinePath,$graphPath,$nonClaimsPath)) {
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
        Fail "prohibited Scenario 08 overclaim phrase found: $phrase"
    }
}

Pass "Scenario 08 non-authority posture is preserved"

Write-Host ""
Pass "Scenario 08 stale validity / authority revocation checks completed"
