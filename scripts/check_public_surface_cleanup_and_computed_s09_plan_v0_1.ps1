# scripts/check_public_surface_cleanup_and_computed_s09_plan_v0_1.ps1
$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }

if (-not (Test-Path ".git")) { Fail "Run from repository root." }

$requiredFiles = @(
    "docs/reviewer/PUBLIC_SURFACE_CLEANUP_AND_COMPUTED_SCENARIO_09_PLAN_v0_1.md",
    "docs/reviewer/AHI_REVIEWER_PACKET_LIMITATIONS_v0_1.md",
    "docs/reviewer/AHI_COMPUTED_SCENARIO_09_PLAN_v0_1.md",
    "scripts/check_no_mojibake_utf8_v0_1.ps1"
)

foreach ($path in $requiredFiles) {
    if (-not (Test-Path $path)) { Fail "missing required file: $path" }
}
Pass "required plan files are present"

$combined = ""
foreach ($path in $requiredFiles) {
    $combined += [System.IO.File]::ReadAllText((Resolve-Path $path), [System.Text.Encoding]::UTF8)
    $combined += "`n"
}

$requiredPhrases = @(
    "bounded fixture consistency",
    "computed transition-state derivation",
    "does not assert that Fork approves",
    "does not yet prove that Fork independently derives",
    "System A",
    "System B",
    "System C",
    "freshness or tolerance policy"
)

foreach ($phrase in $requiredPhrases) {
    if (-not $combined.Contains($phrase)) { Fail "missing required phrase: $phrase" }
}
Pass "required limitation and computed-derivation language is present"

$forbiddenPhrases = @(
    "Fork approved",
    "Fork certifies",
    "Fork determines compliance",
    "Fork establishes legal sufficiency",
    "Fork decides acceptance",
    "Fork determines negligence",
    "Fork determines excuse",
    "Fork authorizes execution"
)

foreach ($phrase in $forbiddenPhrases) {
    if ($combined.Contains($phrase)) { Fail "forbidden phrase found: $phrase" }
}
Pass "forbidden authority/compliance/fault phrases are absent"

Pass "public surface cleanup and computed Scenario 09 plan checks completed"
