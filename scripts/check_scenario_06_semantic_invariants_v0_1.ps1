# scripts/check_scenario_06_semantic_invariants_v0_1.ps1
# Semantic invariant checker for Scenario 06 distributed handoff.
# This checker verifies bounded record semantics only.
# It does not approve, certify, score, authorize, determine compliance, establish legal sufficiency, or judge correctness.

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

$scenarioId = "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF"
$root = "examples/simulations/governance-proof-surface/artifacts"

$bdrPath = "$root/scenario_06_boundary_delta_record.json"
$cbcPath = "$root/scenario_06_claim_boundary_contract.json"
$ccePath = "$root/scenario_06_claim_consumption_event.json"
$smrPath = "$root/scenario_06_system_mapping_receipt.json"
$failurePath = "$root/scenario_06_distributed_authority_failure_event.json"
$graphPath = "$root/scenario_06_transition_graph.md"
$nonClaimsPath = "$root/scenario_06_non_claims_panel.md"

Write-Host "Checking Scenario 06 semantic invariant inputs..."
foreach ($p in @($bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath,$graphPath,$nonClaimsPath)) { Require-File $p }

$bdr = Read-Json $bdrPath
$cbc = Read-Json $cbcPath
$cce = Read-Json $ccePath
$smr = Read-Json $smrPath
$failure = Read-Json $failurePath

Write-Host ""
Write-Host "Checking scenario identity..."
foreach ($a in @($bdr,$cbc,$cce,$smr,$failure)) { Eq $a.scenario_id $scenarioId "scenario_id" }
Pass "Scenario 06 identity preserved"

Write-Host ""
Write-Host "Checking two-boundary distributed transition chain..."
$boundaries = @(Arr $bdr.boundary_sequence)
Eq $boundaries.Count 2 "BDR boundary_sequence count"
True (@($boundaries | Where-Object { $_.boundary_id -eq "S06-B01" }).Count -eq 1) "S06-B01 must be present exactly once"
True (@($boundaries | Where-Object { $_.boundary_id -eq "S06-B02" }).Count -eq 1) "S06-B02 must be present exactly once"
Pass "two-boundary chain is explicit"

Write-Host ""
Write-Host "Checking S06-B01 preservation/narrowing without authority transfer..."
$b01 = @($boundaries | Where-Object { $_.boundary_id -eq "S06-B01" })[0]
Eq $b01.transition_effect "PRESERVED_WITH_NARROWING" "S06-B01 transition_effect"
Eq $b01.authority_effect "NO_AUTHORITY_TRANSFER" "S06-B01 authority_effect"
Has $b01.claim_state_after_transition "narrowed|routing" "S06-B01 claim_state_after_transition"
Pass "S06-B01 preserves/narrows without authority transfer"

Write-Host ""
Write-Host "Checking S06-B02 unsupported authority inheritance..."
$b02 = @($boundaries | Where-Object { $_.boundary_id -eq "S06-B02" })[0]
Eq $b02.transition_effect "EXPANSION_ATTEMPT_RECORDED" "S06-B02 transition_effect"
Eq $b02.authority_effect "UNSUPPORTED_AUTHORITY_INHERITANCE_ATTEMPT" "S06-B02 authority_effect"
Has $b02.claim_state_after_transition "approval authority|authority" "S06-B02 claim_state_after_transition"
Pass "S06-B02 records unsupported authority inheritance"

Write-Host ""
Write-Host "Checking BDR unsupported downstream claims and required revalidation..."
Eq $bdr.inspectability_result "INSPECTABLE" "BDR inspectability_result"
Has $bdr.delta_classification "DISTRIBUTED.*EXPANSION.*RECORDED" "BDR delta_classification"
$notSupported = Join-Text $bdr.downstream_state.not_supported_after_transition
foreach ($t in @("Approval authority","approved","Compliance","certified","Policy criteria")) { Has $notSupported $t "BDR not-supported list" }
$required = Join-Text $bdr.required_revalidation_for
foreach ($t in @("approval authority","policy satisfaction","compliance determination","execution eligibility")) { Has $required $t "BDR required_revalidation_for" }
Pass "BDR unsupported downstream claims remain unsupported"

Write-Host ""
Write-Host "Checking CBC prohibited inference list..."
$blocked = Join-Text $cbc.claims_not_allowed_to_be_inferred
foreach ($t in @("approval authority","case approval","policy satisfaction","compliance determination","legal sufficiency","operational authorization","execution")) { Has $blocked $t "CBC claims_not_allowed_to_be_inferred" }
Has $cbc.non_inheritance_rule "No authority-bearing property transfers" "CBC non_inheritance_rule"
Pass "CBC prohibits authority-bearing inference"

Write-Host ""
Write-Host "Checking CCE expanded consumption..."
Eq $cce.consumer_identity "SYSTEM_C_APPROVAL_ROUTER" "CCE consumer_identity"
Eq $cce.classification "EXPANDED" "CCE classification"
Eq $cce.boundary_effect "EXPANDED_BEYOND_RECORDED_CLAIM_SCOPE" "CCE boundary_effect"
Eq $cce.new_claim_boundary_contract_id "REQUIRED_BUT_ABSENT" "CCE new_claim_boundary_contract_id"
Has $cce.required_next_action "separate approval-authority claim boundary contract" "CCE required_next_action"
Pass "CCE expanded consumption requires separate authority"

Write-Host ""
Write-Host "Checking SMR unsupported distributed authority inheritance..."
Has $smr.overall_mapping_classification "UNSUPPORTED_DISTRIBUTED_AUTHORITY_INHERITANCE" "SMR overall_mapping_classification"
Eq $smr.fork_result "STRUCTURAL_MAPPING_RECORDED" "SMR fork_result"
$unsupported = @(Arr $smr.unsupported_mappings)
True ($unsupported.Count -ge 1) "SMR must include unsupported_mappings"
Has (Join-Text $unsupported) "authority|approval|claim boundary contract" "SMR unsupported mapping reason"
Pass "SMR unsupported mapping is explicit"

Write-Host ""
Write-Host "Checking failure event..."
Eq $failure.category "DISTRIBUTED_AUTHORITY_INHERITANCE_ATTEMPT" "failure category"
Eq $failure.record_support "NOT_SUPPORTED" "failure record_support"
Eq $failure.boundary_effect "EXPANDED" "failure boundary_effect"
Eq $failure.fork_result "UNSUPPORTED_DISTRIBUTED_AUTHORITY_INFERENCE_RECORDED" "failure fork_result"
$failureRequired = Join-Text $failure.required_revalidation
foreach ($t in @("approval authority","policy satisfaction","execution eligibility")) { Has $failureRequired $t "failure required_revalidation" }
Pass "failure event preserves unsupported inference and revalidation"

Write-Host ""
Write-Host "Checking non-authority posture and prohibited oracle language..."
$scan = ""
foreach ($p in @($bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath,$graphPath,$nonClaimsPath)) {
    $scan += "`n--- $p ---`n" + (Get-Content -Raw -Path $p)
}

foreach ($t in @("does not approve","certify","score","authorize","determine compliance","judge correctness")) { Has $scan ([regex]::Escape($t)) "non-authority posture" }

foreach ($phrase in @(
    "Fork approved","Fork approves","Fork certified","Fork certifies","Fork authorized","Fork authorizes",
    "Fork scored","Fork scores","compliance certified","approved by Fork","authorized by Fork","certified by Fork",
    "risk score","go/no-go"
)) {
    if ($scan.ToLowerInvariant().Contains($phrase.ToLowerInvariant())) { Fail "prohibited Scenario 06 semantic overclaim phrase found: $phrase" }
}
Pass "non-authority posture is preserved"

Write-Host ""
Pass "Scenario 06 semantic invariants verified"
