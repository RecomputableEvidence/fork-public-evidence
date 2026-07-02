# scripts/integrate_scenario_05_into_ahi_checker_and_release_note_v0_2.ps1
# Robustly integrates Scenario 05 into the main AHI simulation checker and writes the v0.1.5 release note.
# Does not stage, commit, push, or tag.

param(
    [switch]$ForceOverwrite
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path ".git")) {
    throw "Run this script from the repository root, e.g. C:\N\fork-public-evidence"
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content,
        [switch]$Overwrite
    )

    $parent = Split-Path -Parent $Path

    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    if ((Test-Path $Path) -and -not $Overwrite) {
        Write-Host "SKIP existing file: $Path"
        return
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
    Write-Host "WROTE: $Path"
}

$checkerPath = "scripts/run_ahi_sim_v0_1_checks.ps1"
$scenario05CheckerPath = "scripts/check_scenario_05_non_claim_suppression_v0_1.ps1"
$releaseNotePath = "docs/release_notes/ahi-sim-v0.1.5.md"

if (-not (Test-Path $checkerPath)) {
    throw "Missing main AHI checker: $checkerPath"
}

if (-not (Test-Path $scenario05CheckerPath)) {
    throw "Missing Scenario 05 standalone checker: $scenario05CheckerPath"
}

Write-Host "Integrating Scenario 05 into main AHI checker using robust validation block..."

$text = Get-Content -Raw -Path $checkerPath
$marker = "SCENARIO_05_MAIN_CHECKER_INTEGRATION_v0_2"

$scenario05Block = @'

Write-Host ""
Write-Host "Checking Scenario 05 artifacts through main AHI checker..."
# SCENARIO_05_MAIN_CHECKER_INTEGRATION_v0_2
$scenario05RequiredFiles = @(
    "examples/simulations/governance-proof-surface/scenario_05_policy_reference_laundering_attempt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_original_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_policy_reference_context.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_downstream_memo_excerpt.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_non_claims_panel.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $scenario05RequiredFiles) {
    if (-not (Test-Path $path)) {
        Write-Host "FAIL: missing required Scenario 05 file: $path"
        exit 1
    }

    Write-Host "FOUND: $path"
}

Write-Host ""
Write-Host "Validating Scenario 05 JSON artifacts through main AHI checker..."
$scenario05JsonFiles = @(
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_05_suppressed_limitations_event.json"
)

foreach ($path in $scenario05JsonFiles) {
    try {
        Get-Content -Raw -Path $path | ConvertFrom-Json | Out-Null
        Write-Host "VALID JSON: $path"
    } catch {
        Write-Host "FAIL: invalid Scenario 05 JSON: $path"
        Write-Host $_.Exception.Message
        exit 1
    }
}

Write-Host ""
Write-Host "Running Scenario 05 semantic checker through main AHI checker..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_05_non_claim_suppression_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAIL: Scenario 05 semantic checker failed inside main AHI checker"
    exit 1
}

Write-Host "PASS: Scenario 05 validation completed inside main AHI checker."

'@

if ($text -like "*$marker*") {
    Write-Host "SKIP: Scenario 05 main checker integration block already present"
} else {
    $finalPassPattern = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'

    if ($text -notlike "*$finalPassPattern*") {
        throw "Could not find final PASS anchor in $checkerPath. Inspect the checker and insert the Scenario 05 block manually before the final PASS line."
    }

    $text = $text.Replace($finalPassPattern, $scenario05Block + "`n" + $finalPassPattern)

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($checkerPath, $text, $utf8NoBom)
    Write-Host "WROTE: $checkerPath"
}

$releaseNote = @'
# Fork Governance Simulation Proof Surface v0.1.5

## Scenario 05: Non-Claim Suppression / Policy-Reference Laundering

This release adds Scenario 05 to the Fork Governance Simulation Proof Surface.

Scenario 05 tests a downstream handoff failure in which a favorable upstream claim is preserved while the limitations, exclusions, unresolved issues, and non-claims required to interpret that claim are suppressed.

The concrete subcase is policy-reference laundering:

```text
policy referenced during preliminary review
-> policy treated as applied or satisfied
-> compliance or downstream reliance inferred
```

## What this release adds

This release adds a complete Scenario 05 artifact family:

- Scenario narrative for the policy-reference laundering attempt
- Boundary Delta Record
- Claim Boundary Contract
- Claim Consumption Event
- System Mapping Receipt
- Suppressed Limitations Event
- Original Non-Claims Panel
- Policy Reference Context
- Downstream Memo Excerpt
- Non-Claims Panel
- Scenario artifact generation script
- Scenario-specific semantic checker

Together, these artifacts model a transition in which an upstream record supports only preliminary vendor-risk triage with a recorded policy reference, while a downstream memo treats that policy reference as policy applicability, policy satisfaction, compliance, or onboarding clearance.

## Core failure mode

The simulated failure is not that the upstream record is missing or corrupted.

The failure is selective preservation.

The downstream artifact keeps the favorable claim that a review occurred and that a policy was referenced, but drops the material non-claims that bounded the original record.

Scenario 05 therefore distinguishes between:

- policy referenced,
- policy applicable,
- policy satisfied,
- compliance determined,
- downstream reliance cleared,
- and final vendor approval.

Fork's role in this scenario remains bounded. It does not decide whether the policy applied, whether the policy was satisfied, whether the vendor should be approved, whether compliance exists, or whether downstream onboarding may proceed.

Fork preserves the handoff state and exposes that material limitations were suppressed during the transition.

## Governance significance

Scenario 05 strengthens the simulation ladder by adding limitation loss as a distinct failure class.

Earlier scenarios focused on preserved handoff state, scope expansion, and authority leakage. Scenario 05 adds the case where the downstream system does not necessarily add an explicit new claim at first; instead, it removes the non-claims that prevented the original claim from being read too broadly.

The release reinforces a core Fork principle:

> A preserved claim without its material non-claims is no longer the same governance object.

A downstream reviewer may cite a bounded record, but may not treat omitted limitations as resolved unless a separate record establishes that resolution.

## Verification posture

The release is tagged as:

```text
ahi-sim-v0.1.5
```

The tag points to the Scenario 05 merge commit on `main`.

The Scenario 05 standalone checker verifies:

- required Scenario 05 files exist,
- Scenario 05 JSON artifacts parse,
- non-claim suppression and policy-reference laundering classifications are explicit,
- no prohibited overclaim language appears in the Scenario 05 surface.

The main AHI simulation checker now invokes Scenario 05 validation as part of the primary `ahi-sim-v0.1.x` verification path.

## Boundary statement

Scenario 05 shows that Fork can preserve and expose downstream suppression of material limitations across a simulated handoff.

It does not claim that Fork prevents limitation laundering, certifies compliance, validates policy satisfaction, approves a vendor, grants authority, evaluates truth, or determines legal sufficiency.

The value of the release is inspectability: it makes the suppressed limitations visible, bounded, and reviewable.
'@

Write-Utf8NoBomFile -Path $releaseNotePath -Content $releaseNote -Overwrite:$ForceOverwrite

Write-Host ""
Write-Host "Done."
Write-Host ""
Write-Host "Next commands:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  git diff --stat -- scripts\run_ahi_sim_v0_1_checks.ps1 docs\release_notes\ahi-sim-v0.1.5.md scripts\integrate_scenario_05_into_ahi_checker_and_release_note_v0_2.ps1"
