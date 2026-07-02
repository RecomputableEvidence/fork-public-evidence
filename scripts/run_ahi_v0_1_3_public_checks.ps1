# scripts/run_ahi_v0_1_3_public_checks.ps1
# Runs focused public-surface checks for the ahi-v0.1.3 evaluation-readiness path.
# Does not stage, commit, push, or tag.

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

Write-Host "Running non-claims contract checker..."
python tools\check_non_claims_contract.py

Write-Host ""
Write-Host "Scanning focused public surface for retired language..."

$grepOutput = git grep -n -i "golden workflow\|demonstrates" -- README.md docs\reviewer-artifacts docs\reviewer_notes docs\research docs\evaluation examples\vendor-risk
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "FAIL: retired public-surface language found:"
    Write-Host $grepOutput
    exit 1
}
elseif ($exitCode -eq 1) {
    Write-Host "PASS: no retired public-surface language found."
}
else {
    throw "git grep failed with exit code $exitCode"
}

Write-Host ""
Write-Host "Checking required evaluation files..."

$required = @(
    "docs/evaluation/VENDOR_RISK_HANDOFF_EVALUATION_DESIGN_v0_1.md",
    "docs/evaluation/VENDOR_RISK_HANDOFF_STUDY_PROTOCOL_v0_1.md",
    "docs/evaluation/VENDOR_RISK_UNSUPPORTED_INHERITANCE_CODING_GUIDE_v0_1.md",
    "docs/evaluation/VENDOR_RISK_HANDOFF_RESULTS_v0_1.md",
    "docs/reviewer-artifacts/NON_CLAIMS_CONTRACT_v0_1.md",
    "examples/vendor-risk/non_claims_contract.json"
)

foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required file: $path"
        exit 1
    }
    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "PASS: ahi-v0.1.3 public evaluation-readiness checks completed."