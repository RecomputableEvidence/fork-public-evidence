# scripts/check_scenario_09_revocation_visibility_split_state_v0_1.ps1
$ErrorActionPreference = "Stop"
function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }
function Require-File($Path) { if (-not (Test-Path $Path)) { Fail "missing required file: $Path" }; Write-Host "FOUND: $Path" }
function Read-Json($Path) { try { Get-Content -Raw -Path $Path | ConvertFrom-Json } catch { Fail "invalid JSON: $Path :: $($_.Exception.Message)" } }
function Arr($Value) { if ($null -eq $Value) { @() } elseif ($Value -is [System.Array]) { @($Value) } else { @($Value) } }
function Join-Text($Value) { ((Arr $Value) | ForEach-Object { if ($_ -is [string]) { $_ } else { $_ | ConvertTo-Json -Depth 20 -Compress } }) -join " | " }
function Eq($Actual, $Expected, $Label) { if ($Actual -ne $Expected) { Fail "$Label expected '$Expected' but found '$Actual'" } }
function Has($Text, $Pattern, $Label) { if ($Text -notmatch $Pattern) { Fail "$Label expected pattern '$Pattern'" } }

if (-not (Test-Path ".git")) { Fail "run this script from repository root" }

$scenarioId = "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY"
$scenarioPath = "examples/simulations/governance-proof-surface/scenario_09_revocation_visibility_split_state_boundary.md"
$root = "examples/simulations/governance-proof-surface/artifacts"
$bdrPath = "$root/scenario_09_boundary_delta_record.json"
$cbcPath = "$root/scenario_09_claim_boundary_contract.json"
$ccePath = "$root/scenario_09_claim_consumption_event.json"
$smrPath = "$root/scenario_09_system_mapping_receipt.json"
$vgePath = "$root/scenario_09_visibility_gap_event.json"
$timelinePath = "$root/scenario_09_split_state_timeline.md"
$graphPath = "$root/scenario_09_transition_graph.md"
$nonClaimsPath = "$root/scenario_09_non_claims_panel.md"

Write-Host "Checking Scenario 09 required files..."
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$vgePath,$timelinePath,$graphPath,$nonClaimsPath)) { Require-File $p }

Write-Host ""
Write-Host "Validating Scenario 09 JSON artifacts..."
$bdr = Read-Json $bdrPath
$cbc = Read-Json $cbcPath
$cce = Read-Json $ccePath
$smr = Read-Json $smrPath
$vge = Read-Json $vgePath
foreach ($p in @($bdrPath,$cbcPath,$ccePath,$smrPath,$vgePath)) { Write-Host "VALID JSON: $p" }

foreach ($a in @($bdr,$cbc,$cce,$smr,$vge)) { Eq $a.scenario_id $scenarioId "scenario_id" }
Eq $bdr.boundary_type "REVOCATION_VISIBILITY_AND_SPLIT_STATE" "BDR boundary_type"
Eq $bdr.inspectability_result "INSPECTABLE" "BDR inspectability_result"
Eq $bdr.delta_classification "REVOCATION_VISIBILITY_GAP_RECORDED" "BDR delta_classification"
Has $bdr.split_state_invariant "recorded_in_A_does_not_imply_visible_in_B_or_consumed_by_C" "BDR split_state_invariant"

$boundaries = @(Arr $bdr.boundary_sequence)
if ($boundaries.Count -ne 3) { Fail "BDR boundary_sequence count expected 3 but found $($boundaries.Count)" }
Has (Join-Text $boundaries) "VALIDITY_CHANGE_RECORDED|VISIBILITY_GAP_RECORDED|SPLIT_STATE_RELIANCE_ATTEMPT_RECORDED" "BDR boundary sequence"
Has (Join-Text $bdr.not_supported_after_transition) "global visibility|global consumption|current validity|negligence determination|excuse determination|correctness determination" "BDR unsupported outcomes"
Has (Join-Text $bdr.required_revalidation_for) "revocation visibility|revocation consumption|state synchronization|current execution eligibility" "BDR required revalidation"

Has (Join-Text $cbc.claims_not_allowed_to_be_inferred) "recorded revocation establishes global visibility|local non-awareness establishes current validity|split-state record establishes negligence|split-state record establishes excuse" "CBC prohibited inferences"
Eq $cbc.visibility_boundary.bridge_result "REQUIRES_VISIBILITY_AND_CONSUMPTION_EVIDENCE" "CBC bridge_result"

Eq $cce.classification "EXPANDED" "CCE classification"
Eq $cce.boundary_effect "EXPANDED_BEYOND_VISIBLE_AND_CONSUMED_STATE" "CCE boundary_effect"
Eq $cce.new_claim_boundary_contract_id "REQUIRED_BUT_ABSENT" "CCE new_claim_boundary_contract_id"
Eq $cce.fork_result "SPLIT_STATE_CONSUMPTION_RECORDED_NOT_AUTHORIZED" "CCE fork_result"

Has $smr.overall_mapping_classification "UNSUPPORTED_VISIBILITY_AND_CONSUMPTION_INFERENCE" "SMR overall_mapping_classification"
Eq $smr.visibility_mapping_status "REVOCATION_VISIBILITY_GAP_RECORDED" "SMR visibility_mapping_status"
Has (Join-Text $smr.unsupported_mappings) "revocation recorded in System A|revocation visible in System B|revocation consumed by System C|local non-awareness" "SMR unsupported mappings"

Eq $vge.category "REVOCATION_VISIBILITY_GAP" "VGE category"
Eq $vge.record_support "NOT_SUPPORTED" "VGE record_support"
Eq $vge.boundary_effect "EXPANDED" "VGE boundary_effect"
Eq $vge.fork_result "UNSUPPORTED_VISIBILITY_AND_CONSUMPTION_INFERENCE_RECORDED" "VGE fork_result"

$scan = ""
foreach ($p in @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$vgePath,$timelinePath,$graphPath,$nonClaimsPath)) { $scan += "`n--- $p ---`n" + (Get-Content -Raw -Path $p) }
foreach ($t in @("does not approve","certify","score","authorize","determine compliance","determine admissibility","establish legal sufficiency","judge correctness","determine negligence","determine excuse")) { Has $scan ([regex]::Escape($t)) "non-authority posture" }

$prohibitedPhrases = @("Fork approved","Fork approves","Fork certified","Fork certifies","Fork authorized","Fork authorizes","Fork scored","Fork scores","approved by Fork","authorized by Fork","certified by Fork","compliant because Fork","legally sufficient because Fork","negligent because Fork","excused because Fork","risk score","go/no-go")
foreach ($phrase in $prohibitedPhrases) { if ($scan.ToLowerInvariant().Contains($phrase.ToLowerInvariant())) { Fail "prohibited Scenario 09 overclaim phrase found: $phrase" } }

Pass "Scenario 09 revocation visibility / split-state checks completed"
