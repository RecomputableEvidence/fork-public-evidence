# scripts/check_ahi_viewer_v0_1.ps1
# Verifies the static AHI viewer surface.
# Scope: structural/read-only viewer checks only.
# This script does not approve, certify, score, authorize, or judge correctness.

param(
    [switch]$CheckDeterminism
)

$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    exit 1
}

function Pass($Message) {
    Write-Host "PASS: $Message" -ForegroundColor Green
}

function Require-File($Path) {
    if (-not (Test-Path $Path)) {
        Fail "missing required file: $Path"
    }
    Write-Host "FOUND: $Path"
}

function Read-Json($Path) {
    try {
        return Get-Content -Raw -Path $Path | ConvertFrom-Json
    } catch {
        Fail "invalid JSON: $Path :: $($_.Exception.Message)"
    }
}

function To-Array($Value) {
    if ($null -eq $Value) { return @() }
    if ($Value -is [System.Array]) { return @($Value) }
    return @($Value)
}

function Assert-Equal($Actual, $Expected, $Label) {
    if ($Actual -ne $Expected) {
        Fail "$Label expected '$Expected' but found '$Actual'"
    }
}

function Assert-True($Condition, $Label) {
    if (-not $Condition) { Fail $Label }
}

function Get-JsonPropertyNames($Object) {
    return @($Object.PSObject.Properties | ForEach-Object { $_.Name })
}

if (-not (Test-Path ".git")) {
    Fail "run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

$viewerRoot = "docs/viewer/ahi-viewer-v0_1"
$bundlePath = "$viewerRoot/data/scenarios_bundle.json"
$registryPath = "examples/simulations/governance-proof-surface/scenario_registry.json"
$bundleSchemaPath = "$viewerRoot/schema/scenarios_bundle.schema.json"
$registrySchemaPath = "examples/simulations/governance-proof-surface/scenario_registry.schema.json"
$builderPs1 = "scripts/build_ahi_viewer_data_v0_1.ps1"
$builderPy = "scripts/build_ahi_viewer_data_v0_1.py"

Write-Host "Checking required AHI viewer files..."
$requiredFiles = @(
    "$viewerRoot/README.md",
    "$viewerRoot/index.html",
    "$viewerRoot/app.js",
    "$viewerRoot/styles.css",
    $bundlePath,
    $bundleSchemaPath,
    $registryPath,
    $registrySchemaPath,
    $builderPs1,
    $builderPy
)
foreach ($file in $requiredFiles) { Require-File $file }

Write-Host ""
Write-Host "Parsing viewer bundle and scenario registry..."
$bundle = Read-Json $bundlePath
$registry = Read-Json $registryPath
Pass "viewer bundle and scenario registry parse as JSON"

Write-Host ""
Write-Host "Checking bundle header..."
Assert-Equal $bundle.artifact_type "AHI_VIEWER_SCENARIOS_BUNDLE" "bundle artifact_type"
Assert-Equal $bundle.artifact_version "0.1" "bundle artifact_version"
Assert-True ($bundle.generated -eq $true) "bundle.generated must be true"
Assert-Equal $bundle.generation_mode "deterministic" "bundle generation_mode"
Assert-Equal $bundle.source_registry $registryPath.Replace("\", "/") "bundle source_registry"
Pass "bundle header is bounded and deterministic"

Write-Host ""
Write-Host "Checking scenario cardinality..."
$bundleScenarios = @(To-Array $bundle.scenarios)
$registryScenarios = @(To-Array $registry.scenarios)
Assert-Equal $bundleScenarios.Count $registryScenarios.Count "bundle scenario count versus registry scenario count"
Assert-True ($bundleScenarios.Count -gt 0) "bundle must contain at least one scenario"
Pass "bundle scenario count matches registry"

Write-Host ""
Write-Host "Checking posture enum..."
$allowedPostures = @("BASELINE", "STRUCTURAL", "SEMANTICALLY_VERIFIED", "SCAFFOLD")
foreach ($scenario in $bundleScenarios) {
    if (-not $scenario.scenario_id) { Fail "scenario missing scenario_id" }
    if (-not $scenario.scenario_number) { Fail "$($scenario.scenario_id) missing scenario_number" }
    if (-not $scenario.title) { Fail "$($scenario.scenario_id) missing title" }
    if (-not ($allowedPostures -contains $scenario.verification_posture)) {
        Fail "$($scenario.scenario_id) has invalid verification_posture: $($scenario.verification_posture)"
    }
    if (-not $scenario.viewer_treatment) { Fail "$($scenario.scenario_id) missing viewer_treatment" }
}
Pass "all scenario postures are in the approved enum"

Write-Host ""
Write-Host "Checking uniqueness..."
$ids = @($bundleScenarios | ForEach-Object { $_.scenario_id })
$numbers = @($bundleScenarios | ForEach-Object { $_.scenario_number })
if (($ids | Select-Object -Unique).Count -ne $ids.Count) { Fail "scenario_id values must be unique" }
if (($numbers | Select-Object -Unique).Count -ne $numbers.Count) { Fail "scenario_number values must be unique" }
Pass "scenario IDs and numbers are unique"

Write-Host ""
Write-Host "Checking registry-to-bundle scenario identity alignment..."
$registryIds = @($registryScenarios | ForEach-Object { $_.scenario_id })
foreach ($id in $registryIds) {
    if (-not ($ids -contains $id)) { Fail "registry scenario missing from bundle: $id" }
}
Pass "all registry scenario IDs are represented in bundle"

Write-Host ""
Write-Host "Checking referenced scenario and artifact paths..."
foreach ($scenario in $bundleScenarios) {
    if ($scenario.file) { Require-File $scenario.file }
    foreach ($artifact in @(To-Array $scenario.artifacts)) {
        if (-not $artifact.path) { Fail "$($scenario.scenario_id) has artifact entry without path" }
        if ($artifact.exists -ne $true) { Fail "$($scenario.scenario_id) artifact marked missing in bundle: $($artifact.path)" }
        Require-File $artifact.path
    }
}
Pass "all referenced scenario and artifact paths exist"

Write-Host ""
Write-Host "Checking selected_fields and checker_coverage shape..."
foreach ($scenario in $bundleScenarios) {
    if (-not $scenario.selected_fields) { Fail "$($scenario.scenario_id) missing selected_fields" }
    if (-not $scenario.checker_coverage) { Fail "$($scenario.scenario_id) missing checker_coverage" }
    $selectedFieldNames = Get-JsonPropertyNames $scenario.selected_fields
    foreach ($requiredName in @("supports_summary", "non_support_summary", "requires_separate_evidence_summary", "classifications")) {
        if (-not ($selectedFieldNames -contains $requiredName)) { Fail "$($scenario.scenario_id) selected_fields missing $requiredName" }
    }
    $coverageNames = Get-JsonPropertyNames $scenario.checker_coverage
    foreach ($requiredName in @("included_in_checker", "json_validated", "semantic_assertions_present", "dedicated_checker_invoked", "overclaim_scan_covered")) {
        if (-not ($coverageNames -contains $requiredName)) { Fail "$($scenario.scenario_id) checker_coverage missing $requiredName" }
    }
}
Pass "scenario selected_fields and checker_coverage shapes are present"

Write-Host ""
Write-Host "Checking viewer JavaScript for unsafe runtime primitives..."
$appJs = Get-Content -Raw -Path "$viewerRoot/app.js"
$forbiddenJsPatterns = @(
    "eval\s*\(",
    "new\s+Function\s*\(",
    "document\.cookie",
    "localStorage",
    "sessionStorage"
)
foreach ($pattern in $forbiddenJsPatterns) {
    if ($appJs -match $pattern) { Fail "viewer app.js contains forbidden runtime primitive matching pattern: $pattern" }
}
$fetchMatches = [regex]::Matches($appJs, "fetch\s*\(")
if ($fetchMatches.Count -gt 1) { Fail "viewer app.js should not contain more than one fetch call" }
if ($fetchMatches.Count -eq 1 -and $appJs -notmatch "data/scenarios_bundle\.json") {
    Fail "viewer app.js fetch must be limited to data/scenarios_bundle.json"
}
Pass "viewer JavaScript avoids forbidden runtime primitives"

Write-Host ""
Write-Host "Checking non-authority posture language..."
$scanFiles = @(
    "$viewerRoot/README.md",
    "$viewerRoot/index.html",
    "$viewerRoot/app.js",
    "$viewerRoot/styles.css",
    $builderPs1,
    $builderPy,
    $bundlePath
)
$combined = ""
foreach ($file in $scanFiles) {
    $combined += "`n--- $file ---`n"
    $combined += Get-Content -Raw -Path $file
}
$lower = $combined.ToLowerInvariant()
$requiredNonAuthorityTerms = @("does not approve", "certify", "score", "authorize", "judge correctness")
foreach ($term in $requiredNonAuthorityTerms) {
    if ($lower -notmatch [regex]::Escape($term.ToLowerInvariant())) {
        Fail "viewer surface missing non-authority posture term: $term"
    }
}
$prohibitedPhrases = @(
    "approved by fork",
    "certified by fork",
    "fork certifies",
    "fork approves",
    "fork authorizes",
    "fork scores",
    "compliance certified",
    "legally sufficient",
    "go/no-go",
    "risk score"
)
foreach ($phrase in $prohibitedPhrases) {
    if ($lower.Contains($phrase)) { Fail "viewer surface contains prohibited non-authority phrase: $phrase" }
}
Pass "viewer non-authority posture language is present and no prohibited oracle phrases were found"

if ($CheckDeterminism) {
    Write-Host ""
    Write-Host "Checking deterministic builder behavior..."
    $before = git status --porcelain
    if ($LASTEXITCODE -ne 0) { Fail "git status failed before determinism check" }
    if ($before) { Fail "working tree must be clean before determinism check" }
    powershell -ExecutionPolicy Bypass -File $builderPs1 -ForceOverwrite
    if ($LASTEXITCODE -ne 0) { Fail "viewer builder failed during determinism check" }
    $after = git status --porcelain
    if ($LASTEXITCODE -ne 0) { Fail "git status failed after determinism check" }
    if ($after) {
        Write-Host $after
        Fail "rerunning viewer builder dirtied the repository"
    }
    Pass "viewer builder is deterministic from a clean working tree"
}

Write-Host ""
Pass "AHI viewer v0.1 hardening checks completed"
