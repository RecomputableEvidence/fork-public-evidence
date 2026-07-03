# scripts/check_encoding_cleanup_allowlist_targets_v0_1.ps1
$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }

if (-not (Test-Path ".git")) { Fail "Run from repository root." }

$allowlistPath = "encoding\encoding_cleanup_allowlist_v0_1.txt"
if (-not (Test-Path $allowlistPath)) { Fail "missing allowlist: $allowlistPath" }

$targets = Get-Content $allowlistPath | Where-Object {
    $line = $_.Trim()
    $line.Length -gt 0 -and -not $line.StartsWith("#")
}

if ($targets.Count -lt 1) { Fail "allowlist is empty" }

foreach ($target in $targets) {
    if ($target -match "(^|[\\/])app\.js$") {
        Fail "allowlist must not include app.js: $target"
    }
    if (-not (Test-Path $target)) {
        Fail "allowlist target does not exist: $target"
    }
}

if (-not ($targets -contains "examples/simulations/governance-proof-surface/scenario_09_revocation_visibility_split_state_boundary.md")) {
    Fail "allowlist must include Scenario 09 public scenario file"
}

if (-not ($targets -contains "docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json")) {
    Fail "allowlist must include viewer v0.2 comparison_pairs.json"
}

Pass "encoding cleanup allowlist targets are present and scoped"
