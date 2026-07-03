# scripts/check_scenario_06_multi_system_distributed_handoff_v0_1.ps1
# Dedicated checker for Scenario 06 multi-system distributed handoff structuralization.
# Scope: structural simulation checks only.
# This checker does not approve, certify, score, authorize, determine compliance, or judge correctness.

$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }
function Require-File($Path) { if (-not (Test-Path $Path)) { Fail "missing required file: $Path" }; Write-Host "FOUND: $Path" }
function Read-Json($Path) { try { return Get-Content -Raw -Path $Path | ConvertFrom-Json } catch { Fail "invalid JSON: $Path :: $($_.Exception.Message)" } }
function Assert-Equal($Actual, $Expected, $Label) { if ($Actual -ne $Expected) { Fail "$Label expected '$Expected' but found '$Actual'" } }
function Assert-Match($Actual, $Pattern, $Label) { if ($Actual -notmatch $Pattern) { Fail "$Label expected to match '$Pattern' but found '$Actual'" } }
function Assert-True($Condition, $Label) { if (-not $Condition) { Fail $Label } }
function To-Array($Value) { if ($null -eq $Value) { return @() }; if ($Value -is [System.Array]) { return @($Value) }; return @($Value) }

if (-not (Test-Path ".git")) { Fail "run this script from the repository root, e.g. C:\N\fork-public-evidence" }

$scenarioId = "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF"
$scenarioPath = "examples/simulations/governance-proof-surface/scenario_06_multi_system_distributed_handoff.md"
$artifactRoot = "examples/simulations/governance-proof-surface/artifacts"
$bdrPath = "$artifactRoot/scenario_06_boundary_delta_record.json"
$cbcPath = "$artifactRoot/scenario_06_claim_boundary_contract.json"
$ccePath = "$artifactRoot/scenario_06_claim_consumption_event.json"
$smrPath = "$artifactRoot/scenario_06_system_mapping_receipt.json"
$failurePath = "$artifactRoot/scenario_06_distributed_authority_failure_event.json"
$graphPath = "$artifactRoot/scenario_06_transition_graph.md"
$nonClaimsPath = "$artifactRoot/scenario_06_non_claims_panel.md"

Write-Host "Checking Scenario 06 required files..."
$required = @($scenarioPath,$bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath,$graphPath,$nonClaimsPath)
foreach ($path in $required) { Require-File $path }

Write-Host ""
Write-Host "Validating Scenario 06 JSON artifacts..."
$bdr = Read-Json $bdrPath
$cbc = Read-Json $cbcPath
$cce = Read-Json $ccePath
$smr = Read-Json $smrPath
$failure = Read-Json $failurePath
foreach ($path in @($bdrPath,$cbcPath,$ccePath,$smrPath,$failurePath)) { Write-Host "VALID JSON: $path" }

Write-Host ""
Write-Host "Checking Scenario 06 structural classifications..."
Assert-Equal $bdr.scenario_id $scenarioId "BDR scenario_id"
Assert-Equal $bdr.inspectability_result "INSPECTABLE" "BDR inspectability_result"
Assert-Match $bdr.delta_classification "DISTRIBUTED.*EXPANSION.*RECORDED" "BDR delta_classification"
Assert-Match $bdr.fork_role "records.*boundary.*state|records.*transition" "BDR fork_role"
$boundarySequence = @(To-Array $bdr.boundary_sequence)
Assert-Equal $boundarySequence.Count 2 "BDR boundary sequence count"
Assert-True (@($boundarySequence | Where-Object { $_.authority_effect -eq "NO_AUTHORITY_TRANSFER" }).Count -ge 1) "BDR must record no-authority-transfer boundary"
Assert-True (@($boundarySequence | Where-Object { $_.authority_effect -eq "UNSUPPORTED_AUTHORITY_INHERITANCE_ATTEMPT" }).Count -ge 1) "BDR must record unsupported authority inheritance attempt"

Assert-Equal $cbc.scenario_id $scenarioId "CBC scenario_id"
Assert-Match (($cbc.claims_not_allowed_to_be_inferred -join " | ")) "approval authority" "CBC prohibited inference approval authority"
Assert-Match (($cbc.claims_not_allowed_to_be_inferred -join " | ")) "compliance determination" "CBC prohibited inference compliance determination"
Assert-Match $cbc.non_inheritance_rule "No authority-bearing property transfers" "CBC non_inheritance_rule"

Assert-Equal $cce.scenario_id $scenarioId "CCE scenario_id"
Assert-Equal $cce.consumer_identity "SYSTEM_C_APPROVAL_ROUTER" "CCE consumer_identity"
Assert-Equal $cce.classification "EXPANDED" "CCE classification"
Assert-Equal $cce.new_claim_boundary_contract_id "REQUIRED_BUT_ABSENT" "CCE new_claim_boundary_contract_id"
Assert-Match $cce.required_next_action "separate approval-authority claim boundary contract" "CCE required_next_action"

Assert-Equal $smr.scenario_id $scenarioId "SMR scenario_id"
Assert-Match $smr.overall_mapping_classification "UNSUPPORTED_DISTRIBUTED_AUTHORITY_INHERITANCE" "SMR overall mapping classification"
Assert-Equal $smr.fork_result "STRUCTURAL_MAPPING_RECORDED" "SMR fork_result"
Assert-True (@(To-Array $smr.unsupported_mappings).Count -ge 1) "SMR must record at least one unsupported mapping"

Assert-Equal $failure.scenario_id $scenarioId "failure scenario_id"
Assert-Equal $failure.category "DISTRIBUTED_AUTHORITY_INHERITANCE_ATTEMPT" "failure category"
Assert-Equal $failure.record_support "NOT_SUPPORTED" "failure record_support"
Assert-Equal $failure.boundary_effect "EXPANDED" "failure boundary_effect"
Assert-Equal $failure.fork_result "UNSUPPORTED_DISTRIBUTED_AUTHORITY_INFERENCE_RECORDED" "failure fork_result"
Pass "Scenario 06 structural classifications are bounded and explicit"

Write-Host ""
Write-Host "Scanning Scenario 06 surface for prohibited overclaim language..."
$scanText = ""
foreach ($path in $required) { $scanText += "`n--- $path ---`n"; $scanText += Get-Content -Raw -Path $path }
$prohibitedPhrases = @("Fork approved","Fork approves","Fork certified","Fork certifies","Fork authorized","Fork authorizes","Fork scored","Fork scores","compliance certified","approved by Fork","authorized by Fork","certified by Fork")
foreach ($phrase in $prohibitedPhrases) { if ($scanText.ToLowerInvariant().Contains($phrase.ToLowerInvariant())) { Fail "prohibited Scenario 06 overclaim phrase found: $phrase" } }
$requiredBoundaryTerms = @("does not approve","certify","score","authorize","determine compliance","judge correctness")
foreach ($term in $requiredBoundaryTerms) { if ($scanText.ToLowerInvariant() -notmatch [regex]::Escape($term.ToLowerInvariant())) { Fail "Scenario 06 missing non-authority term: $term" } }
Pass "no prohibited Scenario 06 overclaim language found"
Write-Host ""
Pass "Scenario 06 multi-system distributed handoff checks completed"
