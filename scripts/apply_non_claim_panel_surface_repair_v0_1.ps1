# scripts/apply_non_claim_panel_surface_repair_v0_1.ps1
# Purpose:
# - Add a human-readable NON_CLAIMS_PANEL.md for the vendor-risk golden workflow.
# - Link the panel from reviewer-facing vendor-risk files.
# - Add a reviewer-artifacts index if missing.
# - Repair the highest-risk README wording/path issues.
# - Normalize touched Markdown/JSON files to UTF-8 without BOM and LF line endings.
#
# This script does not commit or push.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-RepoRoot {
    if (!(Test-Path ".git") -or !(Test-Path "README.md")) {
        throw "Run this script from the fork-public-evidence repository root."
    }

    if (!(Test-Path "examples/vendor-risk")) {
        throw "Expected examples/vendor-risk directory was not found."
    }
}

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and !(Test-Path $parent)) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    $normalized = $normalized -replace "`r", "`n"

    if (!$normalized.EndsWith("`n")) {
        $normalized += "`n"
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Resolve-OrCreatePath $Path), $normalized, $encoding)
}

function Resolve-OrCreatePath {
    param([Parameter(Mandatory = $true)][string]$Path)

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }

    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Path))
}

function Read-TextIfExists {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (!(Test-Path $Path)) {
        return $null
    }

    return [System.IO.File]::ReadAllText((Resolve-Path $Path))
}

function Save-TextIfChanged {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $existing = Read-TextIfExists $Path
    $normalized = $Content -replace "`r`n", "`n"
    $normalized = $normalized -replace "`r", "`n"

    if (!$normalized.EndsWith("`n")) {
        $normalized += "`n"
    }

    if ($null -eq $existing -or (($existing -replace "`r`n", "`n") -replace "`r", "`n") -ne $normalized) {
        Write-Utf8NoBomLf -Path $Path -Content $normalized
        Write-Host "UPDATED $Path"
    } else {
        Write-Host "UNCHANGED $Path"
    }
}

function Append-SectionIfMissing {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Needle,
        [Parameter(Mandatory = $true)][string]$Section
    )

    if (!(Test-Path $Path)) {
        Write-Host "SKIP missing $Path"
        return
    }

    $text = Read-TextIfExists $Path
    if ($text -match [regex]::Escape($Needle)) {
        Write-Host "UNCHANGED $Path already references $Needle"
        return
    }

    $updated = (($text -replace "`r`n", "`n") -replace "`r", "`n").TrimEnd() + "`n`n" + $Section.Trim() + "`n"
    Save-TextIfChanged -Path $Path -Content $updated
}

function Normalize-FileUtf8Lf {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (!(Test-Path $Path)) {
        return
    }

    $text = Read-TextIfExists $Path
    Save-TextIfChanged -Path $Path -Content $text
}

function Repair-CommonReadmeIssues {
    $path = "README.md"
    if (!(Test-Path $path)) {
        return
    }

    $text = Read-TextIfExists $path
    $updated = $text

    # Repair broken routing path typo observed in rendered README.
    $updated = $updated -replace '\belease_packages/', 'release_packages/'

    # Reduce formal product-release implication in the public surface.
    $updated = $updated -replace '(?m)^Release:\s*\*\*Fork Public Technical Disclosure', 'Publication: **Fork Public Technical Disclosure'
    $updated = $updated -replace '(?m)^Release:\s*Fork Public Technical Disclosure', 'Publication: Fork Public Technical Disclosure'

    # Harden verification language where it may imply legal/compliance establishment.
    $updated = $updated -replace 'A passing command establishes only', 'A passing command indicates only'
    $updated = $updated -replace 'Passing verification establishes only', 'Passing verification indicates only'
    $updated = $updated -replace 'pass establishes only', 'pass indicates only'

    # Repair common mojibake if present.
    $updated = $updated -replace 'â€™', "'"
    $updated = $updated -replace 'â€œ', '"'
    $updated = $updated -replace 'â€', '"'
    $updated = $updated -replace 'â€“', '-'
    $updated = $updated -replace 'â€”', '-'
    $updated = $updated -replace 'â†’', '->'
    $updated = $updated -replace 'Â©', '(c)'

    Save-TextIfChanged -Path $path -Content $updated
}

function Repair-PilotIssues {
    $path = "docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md"
    if (!(Test-Path $path)) {
        return
    }

    $text = Read-TextIfExists $path
    $updated = $text

    # Repair common mojibake if present.
    $updated = $updated -replace 'â€™', "'"
    $updated = $updated -replace 'â€œ', '"'
    $updated = $updated -replace 'â€', '"'
    $updated = $updated -replace 'â€“', '-'
    $updated = $updated -replace 'â€”', '-'
    $updated = $updated -replace 'â†’', '->'
    $updated = $updated -replace 'Â©', '(c)'

    if ($updated -notmatch 'Indicative pricing and readiness boundary') {
        $section = @'

## Indicative pricing and readiness boundary

Any pricing, sequencing, or commercial ladder described for this pilot is indicative only and subject to scoped discovery.

The pilot does not imply production readiness, legal sufficiency, compliance satisfaction, security certification, customer deployment approval, model correctness, source completeness, or workflow suitability. Those determinations remain with the institution and its authorized legal, compliance, audit, risk, security, procurement, and governance reviewers.
'@
        $updated = $updated.TrimEnd() + "`n`n" + $section.Trim() + "`n"
    }

    Save-TextIfChanged -Path $path -Content $updated
}

function Create-NonClaimsPanel {
    $path = "examples/vendor-risk/NON_CLAIMS_PANEL.md"

    $content = @'
# Not Established by This Record

**Panel status:** Required  
**Panel function:** Boundary-control surface  
**Empty panel allowed:** No  
**Applies to packet:** `vendor-risk-golden-workflow-v0.1`  
**Workflow:** AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt  
**Machine-readable companion:** `non-claims.json`

## Purpose of This Panel

This panel identifies claims that a downstream reader might be tempted to infer from this Fork packet, but that this packet does **not** establish.

This is not a general disclaimer. It is a required reviewer-facing boundary-control surface. Its function is to prevent preserved evidence from being silently promoted into broader legal, compliance, security, operational, vendor-approval, or institutional authority.

## What This Record Preserves

This record preserves the bounded evidence state for the vendor-risk workflow, including:

- what was requested;
- what the AI-assisted system produced;
- what a human reviewed, accepted, rejected, or modified;
- what evidence references were recorded;
- when the reviewed memo became eligible to inform an internal vendor-risk decision;
- where a downstream reliance expansion was attempted;
- whether the packet structure still verifies.

## What This Record Does Not Establish

This record does not establish the truth, completeness, legal sufficiency, compliance status, security approval, production readiness, vendor suitability, model correctness, or institutional authority of the underlying AI-assisted output or resulting decision.

The packet may help a reviewer inspect what was recorded. It does not decide whether the underlying decision was correct, lawful, compliant, safe, fair, complete, or approved.

## Non-Claims

| ID | Tempting inference | Status | Why this is not established | Required external authority or evidence |
|---|---|---|---|---|
| NC-001 | The vendor is approved for production use. | Not established | The packet records an AI-assisted vendor-risk recommendation and reviewed memo. It does not record final procurement, security, legal, executive, or control-owner approval. | Formal vendor approval record, procurement authorization, security review, legal/compliance signoff, or other institutionally recognized approval authority. |
| NC-002 | The AI output was correct. | Not established | The packet records the AI output and human review state. It does not certify factual accuracy, completeness, reasoning quality, or source sufficiency. | Independent factual validation, source review, subject-matter expert review, or other accepted verification process. |
| NC-003 | The workflow satisfied legal or regulatory requirements. | Not established | The packet records workflow evidence boundaries. It does not interpret law, determine regulatory sufficiency, or certify compliance with any legal framework. | Legal analysis, compliance review, regulator-facing control assessment, or other institutionally authorized determination. |
| NC-004 | All relevant vendor risks were considered. | Not established | The packet records the evidence references and review actions available within the bounded workflow. It does not establish that all relevant risks, documents, systems, jurisdictions, or business contexts were included. | Complete vendor-risk review scope, source inventory, risk register mapping, control owner review, or additional evidence collection. |
| NC-005 | The decision can be reused for another vendor, contract, jurisdiction, department, or use case. | Not established | The packet is bound to the specified workflow instance and recorded reliance context. It does not authorize transitive reuse outside that boundary. | New boundary record, new institutional approval, new evidence review, or explicit authority for the expanded context. |
| NC-006 | Fork approved, validated, or certified the institutional decision. | Not established | Fork records and preserves the bounded evidence state. It does not approve the decision, validate institutional judgment, or certify legal, compliance, security, audit, or operational sufficiency. | Institutionally authorized reviewer determination outside the Fork packet. |

## Downstream Use Rule

A downstream consumer may cite this packet only for the bounded evidence state it preserves.

A downstream consumer may not treat any item listed in this panel as established unless a separate authority, review, approval, or evidence record explicitly establishes that claim.

If a downstream process attempts to rely on this packet for any listed non-claim, that attempt must be recorded as a boundary expansion and must not inherit authority from this packet.

## Reviewer Acknowledgement

By reviewing this panel, the reviewer acknowledges that:

- the packet preserves a bounded record;
- the packet does not establish the non-claims listed above;
- the packet does not replace legal, compliance, audit, security, risk, procurement, or executive judgment;
- any downstream expansion requires separate authority or evidence.
'@

    Save-TextIfChanged -Path $path -Content $content
}

function Create-ReviewerArtifactsIndex {
    $path = "docs/reviewer-artifacts/README.md"

    if (Test-Path $path) {
        Normalize-FileUtf8Lf $path
        return
    }

    $content = @'
# Reviewer Artifacts

This directory defines the reviewer-facing product objects used by Fork evidence packets.

These artifacts are intended for legal, audit, compliance, risk, governance, procurement, security, and executive reviewers who need to inspect what a bounded AI-assisted workflow record preserves and what it does not establish.

## Read Order

1. `EVIDENCE_CARD_SPEC_v0_1.md` - reviewer cover sheet for the packet.
2. `BOUNDARY_MAP_SPEC_v0_1.md` - map of the recorded workflow boundary and downstream reliance transitions.
3. `NON_CLAIM_PANEL_SPEC_v0_1.md` - required "Not Established by This Record" panel.
4. `VERIFICATION_RECEIPT_SPEC_v0_1.md` - record of packet-structure verification, not truth, compliance, approval, or legal sufficiency.
5. `REVIEW_PACKET_SPEC_v0_1.md` - assembled reviewer packet format.

## Boundary Note

Reviewer artifacts are not legal opinions, compliance certifications, audit conclusions, security approvals, model evaluations, or production-readiness determinations.

They are reviewer-operable records showing what Fork preserved for a bounded AI-assisted workflow and what the record explicitly does not establish.
'@

    Save-TextIfChanged -Path $path -Content $content
}

function Update-NonClaimPanelSpec {
    $path = "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md"
    if (!(Test-Path $path)) {
        Write-Host "SKIP missing $path"
        return
    }

    $text = Read-TextIfExists $path
    if ($text -match 'Human-readable rendering') {
        Normalize-FileUtf8Lf $path
        return
    }

    $section = @'

## Human-readable rendering

Reviewer-facing packets SHOULD include a human-readable Markdown rendering of the machine-readable `non-claims.json` file.

For examples and review packets, this rendering may appear as `NON_CLAIMS_PANEL.md`.

The Markdown rendering is not a replacement for the machine-readable non-claim record. It is the reviewer-facing surface that allows legal, compliance, audit, risk, governance, procurement, security, and executive reviewers to see which tempting downstream inferences are not established by the packet.

A conformant rendering should identify:

- the tempting inference;
- that the inference is not established;
- why the packet does not establish it;
- what external authority, review, approval, or evidence would be required before relying on it;
- the relevant boundary-map reference where applicable.
'@

    $updated = (($text -replace "`r`n", "`n") -replace "`r", "`n").TrimEnd() + "`n`n" + $section.Trim() + "`n"
    Save-TextIfChanged -Path $path -Content $updated
}

function Link-PanelFromVendorRiskFiles {
    $section = @'
## Human-readable non-claims panel

See `NON_CLAIMS_PANEL.md` for the reviewer-facing **Not Established by This Record** panel. The JSON file `non-claims.json` remains the machine-readable companion; the Markdown panel is the human-readable boundary-control surface.
'@

    $targets = @(
        "examples/vendor-risk/README.md",
        "examples/vendor-risk/evidence-card.md",
        "examples/vendor-risk/boundary-map.md",
        "examples/vendor-risk/review-packet/README.md"
    )

    foreach ($target in $targets) {
        Append-SectionIfMissing -Path $target -Needle "NON_CLAIMS_PANEL.md" -Section $section
    }
}

function Normalize-TouchedSurfaceFiles {
    $paths = @(
        "README.md",
        "docs/README_SURFACE_DOCTRINE.md",
        "docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md",
        "docs/proof/README.md",
        "docs/reviewer-artifacts/README.md",
        "docs/reviewer-artifacts/EVIDENCE_CARD_SPEC_v0_1.md",
        "docs/reviewer-artifacts/BOUNDARY_MAP_SPEC_v0_1.md",
        "docs/reviewer-artifacts/VERIFICATION_RECEIPT_SPEC_v0_1.md",
        "docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md",
        "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md",
        "examples/vendor-risk/README.md",
        "examples/vendor-risk/evidence-card.md",
        "examples/vendor-risk/boundary-map.md",
        "examples/vendor-risk/non-claims.json",
        "examples/vendor-risk/verification-receipt.json",
        "examples/vendor-risk/review-packet/README.md",
        "examples/vendor-risk/NON_CLAIMS_PANEL.md"
    )

    foreach ($path in $paths) {
        Normalize-FileUtf8Lf $path
    }
}

Assert-RepoRoot

Write-Host "Applying Fork public surface non-claim panel repair..."

Repair-CommonReadmeIssues
Repair-PilotIssues
Create-NonClaimsPanel
Create-ReviewerArtifactsIndex
Update-NonClaimPanelSpec
Link-PanelFromVendorRiskFiles
Normalize-TouchedSurfaceFiles

Write-Host ""
Write-Host "Done. Recommended next commands:"
Write-Host "  git diff -- README.md docs examples"
Write-Host "  pytest"
Write-Host "  git status -sb"