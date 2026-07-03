# scripts/check_ahi_viewer_v0_2.ps1
# Checker for AHI Viewer v0.2 Comparison Mode.
# Scope: static viewer shape, comparison data, non-authority posture, and optional deterministic builder check.

param(
    [switch] $CheckDeterminism
)

$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }
function Require-File($Path) { if (-not (Test-Path $Path)) { Fail "missing required file: $Path" }; Write-Host "FOUND: $Path" }
function Read-Json($Path) { try { Get-Content -Raw -Path $Path | ConvertFrom-Json } catch { Fail "invalid JSON: $Path :: $($_.Exception.Message)" } }
function Get-NormalizedTextHash($Path) {
    $text = Get-Content -Raw -Path $Path
    $text = $text -replace "`r`n", "`n"
    $text = $text -replace "`r", "`n"

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($text)
    $sha = [System.Security.Cryptography.SHA256]::Create()

    try {
        $hash = $sha.ComputeHash($bytes)
    } finally {
        $sha.Dispose()
    }

    return -join ($hash | ForEach-Object { $_.ToString("x2") })
}
function Arr($Value) { if ($null -eq $Value) { @() } elseif ($Value -is [System.Array]) { @($Value) } else { @($Value) } }
function Has($Text, $Pattern, $Label) { if ($Text -notmatch $Pattern) { Fail "$Label expected pattern '$Pattern'" } }

if (-not (Test-Path ".git")) {
    Fail "run this script from repository root"
}

Write-Host "Checking required AHI viewer v0.2 files..."
$required = @(
    "docs/viewer/ahi-viewer-v0_2/README.md",
    "docs/viewer/ahi-viewer-v0_2/index.html",
    "docs/viewer/ahi-viewer-v0_2/app.js",
    "docs/viewer/ahi-viewer-v0_2/styles.css",
    "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json",
    "docs/viewer/ahi-viewer-v0_2/schema/comparison_pairs.schema.json",
    "docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json",
    "scripts/build_ahi_viewer_comparison_data_v0_2.ps1",
    "scripts/build_ahi_viewer_comparison_data_v0_2.py"
)
foreach ($p in $required) { Require-File $p }

Write-Host ""
Write-Host "Parsing comparison data and v0.1 scenario bundle..."
$bundle = Read-Json "docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json"
$pairsDoc = Read-Json "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json"
Pass "comparison data and scenario bundle parse as JSON"

Write-Host ""
Write-Host "Checking comparison data header..."
if ($pairsDoc.artifact_type -ne "AHI_VIEWER_COMPARISON_PAIRS") { Fail "unexpected artifact_type: $($pairsDoc.artifact_type)" }
if ($pairsDoc.artifact_version -ne "0.2") { Fail "unexpected artifact_version: $($pairsDoc.artifact_version)" }
if ($pairsDoc.generation_mode -ne "deterministic") { Fail "comparison data must be deterministic" }
Has $pairsDoc.non_authority_statement "does not approve" "non_authority_statement"
Pass "comparison data header is bounded and deterministic"

Write-Host ""
Write-Host "Checking comparison pairs..."
$pairs = @(Arr $pairsDoc.comparison_pairs)
if ($pairs.Count -lt 4) { Fail "expected at least 4 comparison pairs; found $($pairs.Count)" }

$pairIds = @($pairs | ForEach-Object { $_.pair_id })
if (($pairIds | Select-Object -Unique).Count -ne $pairIds.Count) { Fail "comparison pair IDs must be unique" }

$scenarioIds = @((Arr $bundle.scenarios) | ForEach-Object { $_.scenario_id })
foreach ($pair in $pairs) {
    foreach ($field in @("pair_id","label","left_scenario_id","right_scenario_id","comparison_posture","purpose")) {
        if (-not $pair.$field) { Fail "comparison pair missing required field '$field'" }
    }

    if ($scenarioIds -notcontains $pair.left_scenario_id) {
        Fail "left_scenario_id not found in v0.1 bundle: $($pair.left_scenario_id)"
    }

    if ($scenarioIds -notcontains $pair.right_scenario_id) {
        Fail "right_scenario_id not found in v0.1 bundle: $($pair.right_scenario_id)"
    }

    foreach ($arrField in @("boundary_movement","attempted_inference","required_revalidation","fork_can_show","fork_does_not_show","reviewer_use")) {
        if (@(Arr $pair.$arrField).Count -lt 1) {
            Fail "comparison pair $($pair.pair_id) must include at least one '$arrField' entry"
        }
    }
}
Pass "comparison pairs are complete and reference existing scenarios"

Write-Host ""
Write-Host "Checking required canonical pairs..."
foreach ($pairId in @("PAIR-S01-S02","PAIR-S03-S04","PAIR-S05-S06","PAIR-S06-S07")) {
    if ($pairIds -notcontains $pairId) { Fail "missing canonical comparison pair: $pairId" }
}
Pass "canonical comparison pairs are present"

Write-Host ""
Write-Host "Checking viewer JavaScript for forbidden runtime primitives..."
$app = Get-Content -Raw -Path "docs/viewer/ahi-viewer-v0_2/app.js"
foreach ($pattern in @("eval\s*\(","new\s+Function\s*\(","document\.write\s*\(","innerHTML\s*=\s*.*<script")) {
    if ($app -match $pattern) { Fail "forbidden JavaScript primitive found: $pattern" }
}
Has $app "SCENARIO_BUNDLE_URL" "app.js"
Has $app "COMPARISON_URL" "app.js"
Pass "viewer JavaScript avoids forbidden runtime primitives"

Write-Host ""
Write-Host "Checking non-authority posture language..."
$scanPaths = @(
    "docs/viewer/ahi-viewer-v0_2/README.md",
    "docs/viewer/ahi-viewer-v0_2/index.html",
    "docs/viewer/ahi-viewer-v0_2/app.js",
    "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json",
    "docs/releases/AHI_VIEWER_v0_2_COMPARISON_MODE.md"
)

$scan = ""
foreach ($p in $scanPaths) {
    if (Test-Path $p) {
        $scan += "`n--- $p ---`n" + (Get-Content -Raw -Path $p)
    }
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
        Fail "prohibited viewer v0.2 overclaim phrase found: $phrase"
    }
}
Pass "viewer v0.2 non-authority posture is preserved"

if ($CheckDeterminism) {
    Write-Host ""
    Write-Host "Checking deterministic comparison builder behavior..."

    $status = git status --porcelain
    if ($status) {
        Fail "working tree must be clean before determinism check"
    }

    $before = Get-NormalizedTextHash "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json"

    powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite
    if ($LASTEXITCODE -ne 0) { Fail "comparison data builder failed" }

    $after = Get-NormalizedTextHash "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json"
    if ($before -ne $after) {
        Fail "comparison data builder changed normalized output hash"
    }

    $statusAfter = git status --porcelain
    if ($statusAfter) {
        Fail "comparison data builder dirtied working tree"
    }

    Pass "viewer v0.2 comparison builder is deterministic from a clean working tree"
}

Write-Host ""
Pass "AHI viewer v0.2 comparison mode checks completed"
