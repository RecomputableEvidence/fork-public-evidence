$ErrorActionPreference = "Stop"

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$files = @(
    "docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md",
    "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md",
    "docs/README_SURFACE_DOCTRINE.md",
    "docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md",
    "docs/proof/README.md",
    "docs/reviewer-artifacts/BOUNDARY_MAP_SPEC_v0_1.md",
    "docs/reviewer-artifacts/EVIDENCE_CARD_SPEC_v0_1.md",
    "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md",
    "docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md",
    "docs/reviewer-artifacts/VERIFICATION_RECEIPT_SPEC_v0_1.md",
    "examples/vendor-risk/README.md",
    "examples/vendor-risk/boundary-map.md",
    "examples/vendor-risk/evidence-card.md",
    "examples/vendor-risk/non-claims.json",
    "examples/vendor-risk/review-packet/README.md",
    "examples/vendor-risk/verification-receipt.json",
    "release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/README.md",
    "release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/README.md",
    "scripts/add_inlet_routing_v0_1.ps1",
    "scripts/add_public_presence_routing_to_readme.ps1",
    "scripts/add_surface_top_layer_to_readme.ps1",
    "scripts/create_fork_surface_files.ps1"
)

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        Write-Host "MISSING: $file"
        continue
    }

    $raw = [System.IO.File]::ReadAllText((Resolve-Path $file))
    $lf = ($raw -replace "`r`n", "`n" -replace "`r", "`n")
    [System.IO.File]::WriteAllText((Resolve-Path $file), $lf, $Utf8NoBom)

    Write-Host "LF normalized: $file"
}

Write-Host ""
Write-Host "LF normalization complete."