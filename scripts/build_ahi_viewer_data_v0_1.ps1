# scripts/build_ahi_viewer_data_v0_1.ps1
# Builds the static data bundle for docs/viewer/ahi-viewer-v0_1.
# Does not stage, commit, push, tag, or modify source artifacts.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

$registryPath = "examples/simulations/governance-proof-surface/scenario_registry.json"
$viewerDir = "docs/viewer/ahi-viewer-v0_1"
$dataDir = Join-Path $viewerDir "data"
$outputPath = Join-Path $dataDir "scenarios_bundle.json"

if (-not (Test-Path $registryPath)) {
    throw "Missing scenario registry: $registryPath"
}

if ((Test-Path $outputPath) -and -not $ForceOverwrite) {
    Write-Host "SKIP existing viewer bundle: $outputPath"
    Write-Host "Use -ForceOverwrite to regenerate."
    exit 0
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $parent = Split-Path -Parent $Path

    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
    Write-Host "WROTE: $Path"
}

function Get-PropertyValue {
    param(
        [Parameter(Mandatory = $false)]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if ($null -eq $Object) { return $null }
    $prop = $Object.PSObject.Properties[$Name]
    if ($null -eq $prop) { return $null }
    return $prop.Value
}

function As-Array {
    param([Parameter(Mandatory = $false)]$Value)
    if ($null -eq $Value) { return @() }
    if ($Value -is [System.Array]) { return @($Value) }
    return @($Value)
}

function Add-String {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$List,
        [Parameter(Mandatory = $false)]$Value
    )
    if ($null -eq $Value) { return }
    if ($Value -is [string]) {
        $trimmed = $Value.Trim()
        if ($trimmed.Length -gt 0 -and -not $List.Contains($trimmed)) { [void]$List.Add($trimmed) }
        return
    }
    foreach ($item in (As-Array $Value)) { if ($null -ne $item) { Add-String -List $List -Value ([string]$item) } }
}

function Get-ArtifactType {
    param([Parameter(Mandatory = $true)][string]$Path)
    $file = [System.IO.Path]::GetFileName($Path)
    switch -Regex ($file) {
        "boundary_delta_record" { return "BDR" }
        "claim_boundary_contract" { return "CBC" }
        "claim_consumption_event" { return "CCE" }
        "system_mapping_receipt" { return "SMR" }
        "unsupported_inheritance_event" { return "UIE" }
        "suppressed_limitations_event" { return "SLE" }
        "authority_policy_context" { return "APC" }
        "policy_reference_context" { return "PRC" }
        "original_non_claims_panel" { return "ONCP" }
        "non_claims_panel" { return "NCP" }
        "downstream_memo_excerpt" { return "DME" }
        default {
            if ($file.EndsWith(".json")) { return "JSON" }
            if ($file.EndsWith(".md")) { return "MD" }
            return "ARTIFACT"
        }
    }
}

function Read-JsonArtifact {
    param([Parameter(Mandatory = $true)][string]$Path)
    try { return Get-Content -Raw -Path $Path | ConvertFrom-Json }
    catch { throw "Invalid JSON artifact: $Path`n$($_.Exception.Message)" }
}

function Add-ClaimsFromBdr {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$Claims,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$NonClaims,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$Unresolved,
        [Parameter(Mandatory = $false)]$Bdr
    )
    if ($null -eq $Bdr) { return }
    $upstream = Get-PropertyValue -Object $Bdr -Name "upstream_state"
    foreach ($claim in (As-Array (Get-PropertyValue -Object $upstream -Name "recorded_claims"))) {
        $statement = Get-PropertyValue -Object $claim -Name "statement"
        $scope = Get-PropertyValue -Object $claim -Name "scope"
        if ($statement) { if ($scope) { Add-String -List $Claims -Value "$statement Scope: $scope" } else { Add-String -List $Claims -Value $statement } }
    }
    Add-String -List $NonClaims -Value (Get-PropertyValue -Object $upstream -Name "recorded_non_claims")
    foreach ($item in (As-Array (Get-PropertyValue -Object $upstream -Name "unresolved_state"))) {
        Add-String -List $Unresolved -Value (Get-PropertyValue -Object $item -Name "description")
    }
    Add-String -List $Unresolved -Value (Get-PropertyValue -Object $Bdr -Name "required_revalidation")
    Add-String -List $Unresolved -Value (Get-PropertyValue -Object $Bdr -Name "required_revalidation_for")
}

function Add-ClaimsFromCbc {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$Claims,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$NonClaims,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$Unresolved,
        [Parameter(Mandatory = $false)]$Cbc
    )
    if ($null -eq $Cbc) { return }
    foreach ($claim in (As-Array (Get-PropertyValue -Object $Cbc -Name "claims_allowed_to_cross"))) {
        $statement = Get-PropertyValue -Object $claim -Name "statement"
        $scope = Get-PropertyValue -Object $claim -Name "scope"
        if ($statement) { if ($scope) { Add-String -List $Claims -Value "$statement Scope: $scope" } else { Add-String -List $Claims -Value $statement } }
    }
    foreach ($nonClaim in (As-Array (Get-PropertyValue -Object $Cbc -Name "material_non_claims_required_to_cross"))) {
        Add-String -List $NonClaims -Value (Get-PropertyValue -Object $nonClaim -Name "statement")
    }
    Add-String -List $NonClaims -Value (Get-PropertyValue -Object $Cbc -Name "claims_not_allowed_to_be_inferred")
    Add-String -List $Unresolved -Value (Get-PropertyValue -Object $Cbc -Name "revalidation_required_for")
}

function Add-ClaimsFromCce {
    param(
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.ArrayList]$Unresolved,
        [Parameter(Mandatory = $false)]$Cce
    )
    if ($null -eq $Cce) { return }
    Add-String -List $Unresolved -Value (Get-PropertyValue -Object $Cce -Name "required_next_action")
}

function Extract-MarkdownNonClaims {
    param([Parameter(Mandatory = $false)][string]$Text)
    $items = New-Object System.Collections.ArrayList
    if ([string]::IsNullOrWhiteSpace($Text)) { return @() }
    $lines = $Text -split "`r?`n"
    foreach ($line in $lines) {
        $trim = $line.Trim()
        if ($trim -match "^(This handoff record|This record|Fork does not|The upstream record does not|The policy reference does not|The preliminary review does not)") {
            Add-String -List $items -Value $trim
        }
    }
    return @($items)
}

Write-Host "Reading scenario registry: $registryPath"
$registry = Get-Content -Raw -Path $registryPath | ConvertFrom-Json
$scenarioRecords = New-Object System.Collections.ArrayList
$registryScenarios = As-Array (Get-PropertyValue -Object $registry -Name "scenarios")

foreach ($scenario in $registryScenarios) {
    $scenarioId = Get-PropertyValue -Object $scenario -Name "scenario_id"
    $scenarioNumber = Get-PropertyValue -Object $scenario -Name "scenario_number"
    $scenarioFile = Get-PropertyValue -Object $scenario -Name "file"
    $posture = Get-PropertyValue -Object $scenario -Name "verification_posture"
    $mainChecker = Get-PropertyValue -Object $scenario -Name "main_checker"
    $viewerTreatment = Get-PropertyValue -Object $scenario -Name "viewer_treatment"

    Write-Host "Bundling $scenarioId"

    $narrative = $null
    if ($scenarioFile -and (Test-Path $scenarioFile)) { $narrative = Get-Content -Raw -Path $scenarioFile }

    $artifactPaths = As-Array (Get-PropertyValue -Object $scenario -Name "artifact_files")
    $artifactRecords = New-Object System.Collections.ArrayList
    $artifactByType = @{}

    foreach ($artifactPath in $artifactPaths) {
        $artifactType = Get-ArtifactType -Path $artifactPath
        $exists = Test-Path $artifactPath
        $format = if ($artifactPath.EndsWith(".json")) { "json" } elseif ($artifactPath.EndsWith(".md")) { "markdown" } else { "text" }
        $raw = $null
        $parsed = $null
        if ($exists) {
            $raw = Get-Content -Raw -Path $artifactPath
            if ($format -eq "json") {
                $parsed = Read-JsonArtifact -Path $artifactPath
                $artifactByType[$artifactType] = $parsed
            }
        }
        [void]$artifactRecords.Add([ordered]@{ artifact_type = $artifactType; path = $artifactPath; format = $format; exists = $exists; raw_content = $raw; parsed = $parsed })
    }

    $supports = New-Object System.Collections.ArrayList
    $nonSupports = New-Object System.Collections.ArrayList
    $unresolved = New-Object System.Collections.ArrayList
    Add-ClaimsFromBdr -Claims $supports -NonClaims $nonSupports -Unresolved $unresolved -Bdr $artifactByType["BDR"]
    Add-ClaimsFromCbc -Claims $supports -NonClaims $nonSupports -Unresolved $unresolved -Cbc $artifactByType["CBC"]
    Add-ClaimsFromCce -Unresolved $unresolved -Cce $artifactByType["CCE"]

    foreach ($artifact in $artifactRecords) {
        if ($artifact.format -eq "markdown" -and ($artifact.artifact_type -eq "NCP" -or $artifact.artifact_type -eq "ONCP")) {
            Add-String -List $nonSupports -Value (Extract-MarkdownNonClaims -Text $artifact.raw_content)
        }
    }

    $classifications = [ordered]@{}
    $bdr = $artifactByType["BDR"]
    $cce = $artifactByType["CCE"]
    $uie = $artifactByType["UIE"]
    $sle = $artifactByType["SLE"]
    if ($null -ne $bdr) {
        $classifications["delta_classification"] = Get-PropertyValue -Object $bdr -Name "delta_classification"
        $classifications["inspectability_result"] = Get-PropertyValue -Object $bdr -Name "inspectability_result"
        $classifications["fork_role"] = Get-PropertyValue -Object $bdr -Name "fork_role"
        $classifications["fork_non_authority_statement"] = Get-PropertyValue -Object $bdr -Name "fork_non_authority_statement"
    }
    if ($null -ne $cce) { $classifications["claim_consumption_classification"] = Get-PropertyValue -Object $cce -Name "classification" }
    if ($null -ne $uie) {
        $classifications["unsupported_inheritance_event"] = [ordered]@{
            category = Get-PropertyValue -Object $uie -Name "category"
            secondary_categories = Get-PropertyValue -Object $uie -Name "secondary_categories"
            inferred_claim = Get-PropertyValue -Object $uie -Name "inferred_claim"
            record_support = Get-PropertyValue -Object $uie -Name "record_support"
            why_unsupported = Get-PropertyValue -Object $uie -Name "why_unsupported"
            fork_result = Get-PropertyValue -Object $uie -Name "fork_result"
        }
    }
    if ($null -ne $sle) {
        $classifications["suppressed_limitations_event"] = [ordered]@{
            category = Get-PropertyValue -Object $sle -Name "category"
            secondary_categories = Get-PropertyValue -Object $sle -Name "secondary_categories"
            inferred_claim = Get-PropertyValue -Object $sle -Name "inferred_claim"
            record_support = Get-PropertyValue -Object $sle -Name "record_support"
            why_unsupported = Get-PropertyValue -Object $sle -Name "why_unsupported"
            fork_result = Get-PropertyValue -Object $sle -Name "fork_result"
            fork_non_authority_statement = Get-PropertyValue -Object $sle -Name "fork_non_authority_statement"
        }
    }

    $checkerCoverage = [ordered]@{
        included_in_checker = [bool]((Get-PropertyValue -Object $mainChecker -Name "narrative_file_required") -or (Get-PropertyValue -Object $mainChecker -Name "artifact_files_required"))
        json_validated = [bool](Get-PropertyValue -Object $mainChecker -Name "json_validation")
        semantic_assertions_present = [bool](Get-PropertyValue -Object $mainChecker -Name "semantic_classification_assertions")
        dedicated_checker_invoked = [bool](Get-PropertyValue -Object $mainChecker -Name "dedicated_checker_invoked")
        overclaim_scan_covered = [bool](Get-PropertyValue -Object $mainChecker -Name "overclaim_scan_covered")
    }

    [void]$scenarioRecords.Add([ordered]@{
        scenario_number = $scenarioNumber
        scenario_id = $scenarioId
        title = Get-PropertyValue -Object $scenario -Name "title"
        purpose = Get-PropertyValue -Object $scenario -Name "purpose"
        file = $scenarioFile
        verification_posture = $posture
        posture_description = Get-PropertyValue -Object $scenario -Name "posture_description"
        primary_category = Get-PropertyValue -Object $scenario -Name "primary_category"
        secondary_categories = As-Array (Get-PropertyValue -Object $scenario -Name "secondary_categories")
        viewer_treatment = $viewerTreatment
        narrative_markdown = $narrative
        artifacts = @($artifactRecords)
        selected_fields = [ordered]@{
            supports_summary = @($supports)
            non_support_summary = @($nonSupports)
            requires_separate_evidence_summary = @($unresolved)
            classifications = $classifications
        }
        checker_coverage = $checkerCoverage
    })
}

$bundle = [ordered]@{
    artifact_type = "AHI_VIEWER_SCENARIOS_BUNDLE"
    artifact_version = "0.1"
    generated_at_utc = [DateTime]::UtcNow.ToString("o")
    source_registry = $registryPath
    source_checker = "scripts/run_ahi_sim_v0_1_checks.ps1"
    non_authority_statement = "Fork Boundary Explorer is a read-only evidence viewer for accountable handoff records. It does not approve, certify, score, authorize, or judge correctness. It shows what the record supports, what it explicitly does not support, and what remains unresolved."
    posture_enum = @("BASELINE", "STRUCTURAL", "SEMANTICALLY_VERIFIED", "SCAFFOLD")
    posture_note = "Posture enum is the primary maturity layer. Failure-mode terms are categories or boundary effects, not verification posture."
    scenarios = @($scenarioRecords)
}

$json = $bundle | ConvertTo-Json -Depth 100
Write-Utf8NoBomFile -Path $outputPath -Content ($json + "`n")

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Validate:"
Write-Host "  Get-Content -Raw .\docs\viewer\ahi-viewer-v0_1\data\scenarios_bundle.json | ConvertFrom-Json | Out-Null"
Write-Host ""
Write-Host "Open:"
Write-Host "  python -m http.server 8765"
Write-Host "  http://localhost:8765/docs/viewer/ahi-viewer-v0_1/"
