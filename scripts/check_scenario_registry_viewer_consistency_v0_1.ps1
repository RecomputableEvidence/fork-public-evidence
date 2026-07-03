# scripts/check_scenario_registry_viewer_consistency_v0_1.ps1
$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }
function HasProp($Obj, $Name) { return $null -ne $Obj.PSObject.Properties[$Name] }
function Arr($Value) {
    if ($null -eq $Value) { return @() }
    if ($Value -is [System.Array]) { return @($Value) }
    return @($Value)
}

if (-not (Test-Path ".git")) { Fail "Run from repository root." }

$path = "examples/simulations/governance-proof-surface/scenario_registry.json"
if (-not (Test-Path $path)) { Fail "missing scenario registry: $path" }

try {
    $registry = Get-Content -Raw -Path $path | ConvertFrom-Json
} catch {
    Fail "scenario registry is not valid JSON: $($_.Exception.Message)"
}

$scenarios = @(Arr $registry.scenarios)
if ($scenarios.Count -ne 9) { Fail "expected 9 scenarios, found $($scenarios.Count)" }

Write-Host "Checking scenario number format..."
foreach ($s in $scenarios) {
    if (($s.scenario_number -isnot [string]) -or ($s.scenario_number -notmatch "^\d{2}$")) {
        Fail "$($s.scenario_id) scenario_number must be zero-padded string, found '$($s.scenario_number)'"
    }
}
Pass "scenario numbers are zero-padded strings"

Write-Host "Checking artifact family flags..."
foreach ($s in $scenarios) {
    $artifacts = @(Arr $s.artifact_files)
    if ($artifacts.Count -gt 0 -and $s.artifact_family_present -ne $true) {
        Fail "$($s.scenario_id) has artifact_files but artifact_family_present is not true"
    }
    foreach ($artifact in $artifacts) {
        if (-not (Test-Path $artifact)) {
            Fail "$($s.scenario_id) references missing artifact file: $artifact"
        }
    }
}
Pass "artifact family flags and referenced files are consistent"

Write-Host "Checking main_checker fields used by viewer..."
$requiredMainCheckerKeys = @(
    "narrative_file_required",
    "artifact_files_required",
    "json_validation",
    "semantic_classification_assertions",
    "dedicated_checker_invoked",
    "overclaim_scan_covered"
)

foreach ($s in $scenarios) {
    if ($s.verification_posture -eq "SEMANTICALLY_VERIFIED") {
        if (-not (HasProp $s "main_checker")) { Fail "$($s.scenario_id) missing main_checker" }
        foreach ($key in $requiredMainCheckerKeys) {
            if (-not (HasProp $s.main_checker $key)) {
                Fail "$($s.scenario_id) main_checker missing viewer key: $key"
            }
        }
    }
}
Pass "main_checker viewer badge fields are present"

Write-Host "Checking viewer_treatment structure..."
foreach ($s in $scenarios) {
    if (-not (HasProp $s "viewer_treatment")) { Fail "$($s.scenario_id) missing viewer_treatment" }
    if (-not (HasProp $s.viewer_treatment "display_group")) { Fail "$($s.scenario_id) viewer_treatment missing display_group" }
    if (-not (HasProp $s.viewer_treatment "display_weight")) { Fail "$($s.scenario_id) viewer_treatment missing display_weight" }
    if (-not (HasProp $s.viewer_treatment "should_present_as_verified_fork_claim")) { Fail "$($s.scenario_id) viewer_treatment missing should_present_as_verified_fork_claim" }
}
Pass "viewer_treatment structures are renderable"

Write-Host "Checking Scenario 07-09 purpose uniqueness..."
$s06 = @($scenarios | Where-Object { $_.scenario_id -eq "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF" })[0]
foreach ($sid in @(
    "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE",
    "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY",
    "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY"
)) {
    $s = @($scenarios | Where-Object { $_.scenario_id -eq $sid })[0]
    if ($s.purpose -eq $s06.purpose) {
        Fail "$sid purpose is stale copy of Scenario 06 purpose"
    }
}
Pass "Scenario 07-09 purposes are scenario-specific"

Write-Host "Checking Scenario 06-09 category specificity..."
$expectedPrimary = @{
    "SCENARIO_06_MULTI_SYSTEM_DISTRIBUTED_HANDOFF" = "MULTI_SYSTEM_DISTRIBUTED_HANDOFF"
    "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE" = "EXTERNAL_AUTHORITY_BRIDGE"
    "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY" = "STALE_VALIDITY_AUTHORITY_REVOCATION"
    "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY" = "REVOCATION_VISIBILITY_SPLIT_STATE"
}

foreach ($sid in $expectedPrimary.Keys) {
    $s = @($scenarios | Where-Object { $_.scenario_id -eq $sid })[0]
    if ($s.primary_category -ne $expectedPrimary[$sid]) {
        Fail "$sid primary_category expected $($expectedPrimary[$sid]) but found $($s.primary_category)"
    }
}
Pass "Scenario 06-09 primary categories are specific"

Write-Host "Checking checker_coverage and selected_fields for Scenario 06-09..."
foreach ($sid in $expectedPrimary.Keys) {
    $s = @($scenarios | Where-Object { $_.scenario_id -eq $sid })[0]
    if (-not (HasProp $s "checker_coverage")) { Fail "$sid missing checker_coverage" }
    foreach ($key in @("required_files","json_validity","semantic_invariants","non_authority_scan","viewer_bundle")) {
        if (-not (HasProp $s.checker_coverage $key)) { Fail "$sid checker_coverage missing $key" }
        if ($s.checker_coverage.$key -ne $true) { Fail "$sid checker_coverage.$key must be true" }
    }
    if (-not (HasProp $s "selected_fields")) { Fail "$sid missing selected_fields" }
}
Pass "Scenario 06-09 checker_coverage and selected_fields are present"

Write-Host "Checking for mojibake lead characters and prohibited phrase forms..."
$raw = [System.IO.File]::ReadAllText((Resolve-Path $path), [System.Text.Encoding]::UTF8)
$suspiciousChars = @([char]0x00C3, [char]0x00C2, [char]0x00E2, [char]0xFFFD)

foreach ($ch in $suspiciousChars) {
    if ($raw.Contains([string]$ch)) {
        $code = [int][char]$ch
        Fail "possible mojibake lead character found: U+$('{0:X4}' -f $code)"
    }
}

if ($raw -match "legally sufficient") {
    Fail "prohibited phrase form found: legally sufficient"
}
Pass "no mojibake lead characters or prohibited phrase form found"

Write-Host ""
Pass "scenario registry viewer consistency checks completed"
