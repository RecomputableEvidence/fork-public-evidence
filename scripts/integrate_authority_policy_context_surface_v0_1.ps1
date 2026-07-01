# scripts/integrate_authority_policy_context_surface_v0_1.ps1
# Purpose:
# - Integrate Authority and Policy Context into Fork reviewer surface.
# - Add a reviewer-artifact spec for authority/policy context.
# - Add a vendor-risk example authority/policy context file.
# - Link it from reviewer-facing golden workflow files.
# - Extend the Non-Claim Panel to preserve authority context without certifying authority.
# - Normalize touched files, including this script, to UTF-8 without BOM and LF.
#
# This script does not commit or push.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-FullPath {
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

    return [System.IO.File]::ReadAllText((Resolve-FullPath $Path))
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
    [System.IO.File]::WriteAllText((Resolve-FullPath $Path), $normalized, $encoding)
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

    if ($null -eq $existing) {
        Write-Utf8NoBomLf -Path $Path -Content $normalized
        Write-Host "CREATED $Path"
        return
    }

    $existingNormalized = $existing -replace "`r`n", "`n"
    $existingNormalized = $existingNormalized -replace "`r", "`n"

    if ($existingNormalized -ne $normalized) {
        Write-Utf8NoBomLf -Path $Path -Content $normalized
        Write-Host "UPDATED $Path"
    } else {
        Write-Host "UNCHANGED $Path"
    }
}

function Assert-RepoRoot {
    if (!(Test-Path ".git") -or !(Test-Path "README.md")) {
        throw "Run this script from the fork-public-evidence repository root."
    }

    if (!(Test-Path "examples/vendor-risk")) {
        throw "Expected examples/vendor-risk directory was not found."
    }

    if (!(Test-Path "docs/reviewer-artifacts")) {
        throw "Expected docs/reviewer-artifacts directory was not found."
    }
}

function Normalize-FileUtf8Lf {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (!(Test-Path $Path)) {
        return
    }

    $text = Read-TextIfExists $Path
    Save-TextIfChanged -Path $Path -Content $text
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
        Write-Host "UNCHANGED $Path already contains $Needle"
        return
    }

    $updated = (($text -replace "`r`n", "`n") -replace "`r", "`n").TrimEnd()
    $updated = $updated + "`n`n" + $Section.Trim() + "`n"
    Save-TextIfChanged -Path $Path -Content $updated
}

function Create-AuthorityPolicySpec {
    $path = "docs/reviewer-artifacts/AUTHORITY_POLICY_CONTEXT_SPEC_v0_1.md"

    $content = @'
# Authority and Policy Context Spec v0.1

## Purpose

The Authority and Policy Context section preserves the stated institutional context under which an AI-assisted claim, recommendation, memo, or workflow artifact was reviewed, accepted, or relied upon.

This section does not establish that the stated authority was sufficient, that the policy was adequate, or that the resulting reliance was legally, commercially, operationally, or regulatorily sufficient.

Its purpose is to prevent later reviewers from having to reconstruct the governance context from memory, surrounding systems, or unstated assumptions.

## Reviewer question

A reviewer should be able to answer:

Who accepted or relied on the claim, under what role or policy context, for what purpose, and did later use stay inside or move beyond that context?

## Required fields

A conformant reviewer-facing packet SHOULD expose the following fields when available:

| Field | Meaning |
|---|---|
| `accepted_by_role` | The role, group, or function that accepted or relied on the artifact. |
| `accepted_by_actor_or_group` | The named actor or group, if appropriate and permitted by privacy/security constraints. |
| `accepted_under_policy` | The policy, procedure, control, playbook, review process, or governance context asserted for the acceptance event. |
| `policy_version_or_reference` | The policy version, document reference, control ID, or process identifier if available. |
| `accepted_for_purpose` | The bounded purpose for which the artifact was accepted or relied upon. |
| `review_status` | The recorded review state, such as reviewed, modified, rejected in part, escalated, or unresolved. |
| `approval_status` | The recorded approval state, if any. Absence of approval must not be inferred as approval. |
| `authority_scope_statement` | A plain-language statement of the authority context asserted for the acceptance event. |
| `assumptions_and_unresolved_items` | Assumptions, open verification items, unresolved questions, or known gaps at the time of acceptance. |
| `authority_not_established` | Explicit statement that the record preserves stated authority context but does not establish authority sufficiency. |
| `downstream_authority_change` | Whether a later consumer narrowed, preserved, expanded, or attempted to expand the original authority context. |

## Required non-claim

Every reviewer-facing use of this section MUST preserve the following non-claim in substance:

This record preserves the stated authority and policy context associated with the review, acceptance, or reliance event. It does not establish that the reviewer had sufficient institutional authority, that the policy was adequate, that the review was complete, or that the resulting decision satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.

## Boundary behavior

If a downstream consumer uses the packet for a purpose outside the recorded authority or policy context, that use must be treated as a downstream authority-context change.

The change may be:

- `PRESERVED` - later use stays within the recorded authority and policy context.
- `NARROWED` - later use is more limited than the recorded authority and policy context.
- `EXPANDED` - later use attempts to rely beyond the recorded authority and policy context.
- `UNRESOLVED` - the later authority context cannot be determined from the packet.

Fork records the authority-context state and any downstream change. Fork does not decide whether the authority was valid, sufficient, legally effective, or institutionally adequate.

## Placement in reviewer artifacts

Authority and Policy Context SHOULD be visible in:

- Evidence Card
- Boundary Map
- Review Packet
- Non-Claim Panel
- Verification Receipt when the verification receipt lists packet sections or required panels

## Not established by this section

This section does not establish:

- legal authority;
- compliance satisfaction;
- audit sufficiency;
- procurement approval;
- security approval;
- production readiness;
- executive approval;
- regulatory adequacy;
- correctness of the AI-assisted output;
- completeness of the evidence base;
- adequacy of the policy or governance process;
- institutional authority beyond the recorded context.
'@

    Save-TextIfChanged -Path $path -Content $content
}

function Create-VendorRiskAuthorityContext {
    $path = "examples/vendor-risk/authority-policy-context.md"

    $content = @'
# Authority and Policy Context

**Workflow:** AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt  
**Applies to packet:** `vendor-risk-golden-workflow-v0.1`  
**Related human-readable panel:** `NON_CLAIMS_PANEL.md`  
**Related machine-readable record:** `non-claims.json`

## Purpose

This file preserves the stated authority and policy context under which the AI-assisted vendor-risk recommendation was reviewed and became eligible to inform an internal decision memo.

It does not establish that the authority was sufficient, that the policy was adequate, or that the resulting reliance satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.

## Minimum surviving authority context

| Field | Example value |
|---|---|
| Accepted by role | Vendor risk analyst or vendor risk review function |
| Accepted under policy | Internal vendor-risk review process for preliminary vendor assessment |
| Policy version or reference | Synthetic example policy reference: `VR-PRELIM-REVIEW-v0.1` |
| Accepted for purpose | Internal vendor-risk triage and preparation of a decision memo |
| Review status | Human reviewed; AI recommendation partially accepted and partially modified |
| Approval status | No final vendor approval established by this packet |
| Authority scope | The reviewed memo may inform internal vendor-risk discussion within the bounded workflow. |
| Assumptions and unresolved items | Source completeness, final security approval, legal review, procurement approval, and production suitability remain unresolved. |

## First institutional reliance moment

The first institutional reliance moment occurs when the human-reviewed memo becomes eligible to inform an internal vendor-risk decision.

This packet records that reliance boundary. It does not establish that the decision was correct, complete, compliant, approved, or sufficient for production vendor use.

## Downstream authority-context change

A downstream consumer attempted to treat the reviewed memo as broader vendor approval.

That attempted use expands the original authority context.

The original packet preserved a vendor-risk review boundary. It did not establish production vendor approval, procurement authorization, security approval, legal approval, or authority for reuse in a different workflow.

## Authority-context non-claim

This record preserves the stated authority and policy context associated with the review and reliance event.

It does not establish that:

- the reviewer had sufficient institutional authority;
- the policy was adequate;
- the review was complete;
- the decision was legally sufficient;
- the decision satisfied compliance obligations;
- the vendor was approved;
- the vendor was suitable for production use;
- the AI-assisted output was correct;
- the evidence base was complete;
- any downstream consumer may reuse the memo outside the recorded boundary.
'@

    Save-TextIfChanged -Path $path -Content $content
}

function Update-ReviewerArtifactsReadme {
    $path = "docs/reviewer-artifacts/README.md"

    $section = @'
## Authority and policy context

`AUTHORITY_POLICY_CONTEXT_SPEC_v0_1.md` defines how reviewer-facing packets preserve who accepted or relied on a claim, under what role or policy context, for what purpose, and whether later use stayed within or moved beyond that context.

This artifact does not establish that the authority was sufficient, the policy was adequate, or the reliance was legally, commercially, operationally, or regulatorily sufficient.
'@

    Append-SectionIfMissing -Path $path -Needle "AUTHORITY_POLICY_CONTEXT_SPEC_v0_1.md" -Section $section
}

function Update-SurfaceDoctrine {
    $path = "docs/README_SURFACE_DOCTRINE.md"

    $section = @'
## Authority and policy context invariant

Fork packets should preserve not only what was claimed and what evidence was referenced, but also the stated authority and policy context under which the claim was reviewed, accepted, or relied upon.

This does not make Fork an authority validator. Fork does not establish that the reviewer had sufficient authority, that the policy was adequate, or that the resulting reliance was legally, commercially, operationally, or regulatorily sufficient.

The purpose is preservation without inheritance: a later reviewer should not be forced to reconstruct authority context that should have survived with the artifact.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority and policy context invariant" -Section $section
}

function Update-ReviewerStartHere {
    $path = "docs/REVIEWER_START_HERE_v0_1.md"

    $section = @'
## Authority and policy context

Fork reviewer packets should show the stated authority and policy context for the reviewed workflow artifact.

This helps a reviewer distinguish:

- the evidence state Fork preserved;
- the purpose for which the artifact was accepted;
- the authority context asserted at the time of reliance;
- any downstream narrowing or expansion of that authority context.

Fork does not establish that the stated authority was sufficient, that the policy was adequate, or that the resulting reliance was legally, commercially, operationally, or regulatorily sufficient.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority and policy context" -Section $section
}

function Update-NonClaimPanelSpec {
    $path = "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md"

    $section = @'
## Authority and policy context non-claim

The Non-Claim Panel SHOULD include a non-claim covering authority and policy context when the packet records an institutional review, acceptance, approval, memo, recommendation, or reliance event.

Required substance:

This record preserves the stated authority and policy context associated with the review, acceptance, or reliance event. It does not establish that the reviewer had sufficient institutional authority, that the policy was adequate, that the review was complete, or that the resulting decision satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority and policy context non-claim" -Section $section
}

function Update-ExampleNonClaimsPanel {
    $path = "examples/vendor-risk/NON_CLAIMS_PANEL.md"

    $section = @'
## Authority and Policy Context Non-Claims

| ID | Tempting inference | Status | Why this is not established | Required external authority or evidence |
|---|---|---|---|---|
| NC-007 | The reviewer had sufficient institutional authority to approve the vendor. | Not established | The packet preserves the stated review role and authority context. It does not certify that the reviewer had authority to issue final vendor approval. | Institutionally recognized approval record, role authorization, procurement approval, security approval, legal/compliance signoff, or executive authorization. |
| NC-008 | The policy context was adequate for the decision. | Not established | The packet may record the policy or review process asserted for the workflow. It does not establish that the policy was complete, current, legally sufficient, or appropriate for the decision. | Policy owner review, legal/compliance analysis, control assessment, audit review, or other institutionally authorized determination. |
| NC-009 | The downstream consumer may reuse the memo under the same authority context. | Not established | The packet is bound to the recorded workflow purpose. Reuse in another workflow, department, jurisdiction, contract, or approval path may require separate authority and evidence. | New boundary record, new authority record, new policy mapping, or explicit authorization for the expanded use. |
'@

    Append-SectionIfMissing -Path $path -Needle "NC-007" -Section $section
}

function Link-AuthorityContextFromVendorRiskFiles {
    $section = @'
## Authority and policy context

See `authority-policy-context.md` for the reviewer-facing authority and policy context associated with this vendor-risk workflow.

That file preserves the stated role, policy context, reliance purpose, unresolved authority questions, and downstream authority-context expansion. It does not establish that the authority was sufficient, that the policy was adequate, or that the decision was legally, commercially, operationally, or regulatorily sufficient.
'@

    $targets = @(
        "examples/vendor-risk/README.md",
        "examples/vendor-risk/evidence-card.md",
        "examples/vendor-risk/boundary-map.md",
        "examples/vendor-risk/review-packet/README.md"
    )

    foreach ($target in $targets) {
        Append-SectionIfMissing -Path $target -Needle "authority-policy-context.md" -Section $section
    }
}

function Update-EvidenceCardSpec {
    $path = "docs/reviewer-artifacts/EVIDENCE_CARD_SPEC_v0_1.md"

    $section = @'
## Authority and policy context section

Evidence Cards SHOULD include an Authority and Policy Context section when the packet records a review, acceptance, approval, memo, recommendation, or institutional reliance event.

The section should identify the stated role, policy context, reliance purpose, review status, approval status if any, unresolved authority questions, and any downstream authority-context change.

This section preserves the stated authority context. It does not establish that the authority was sufficient, that the policy was adequate, or that the decision satisfied legal, compliance, audit, procurement, security, risk, executive, or regulatory requirements.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority and policy context section" -Section $section
}

function Update-BoundaryMapSpec {
    $path = "docs/reviewer-artifacts/BOUNDARY_MAP_SPEC_v0_1.md"

    $section = @'
## Authority-context boundary changes

Boundary Maps SHOULD mark whether a downstream reliance event preserves, narrows, expands, or leaves unresolved the original authority and policy context.

A downstream consumer expands the authority context when it treats a packet as supporting a broader approval, legal/compliance conclusion, security clearance, procurement approval, production authorization, or institutional decision than the original recorded context supports.

Fork records the authority-context change. Fork does not decide whether the new authority context is valid, sufficient, or approved.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority-context boundary changes" -Section $section
}

function Update-ReviewPacketSpec {
    $path = "docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md"

    $section = @'
## Authority and policy context inclusion

Review Packets SHOULD include the Authority and Policy Context section when the packet contains a human review, acceptance, memo, recommendation, approval state, or institutional reliance event.

The packet should make clear what authority context was recorded and what authority, policy, legal, compliance, audit, security, procurement, risk, executive, or regulatory determinations remain outside the packet.
'@

    Append-SectionIfMissing -Path $path -Needle "Authority and policy context inclusion" -Section $section
}

function Normalize-TouchedFiles {
    $paths = @(
        "docs/reviewer-artifacts/AUTHORITY_POLICY_CONTEXT_SPEC_v0_1.md",
        "docs/reviewer-artifacts/README.md",
        "docs/reviewer-artifacts/EVIDENCE_CARD_SPEC_v0_1.md",
        "docs/reviewer-artifacts/BOUNDARY_MAP_SPEC_v0_1.md",
        "docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md",
        "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md",
        "docs/README_SURFACE_DOCTRINE.md",
        "docs/REVIEWER_START_HERE_v0_1.md",
        "examples/vendor-risk/authority-policy-context.md",
        "examples/vendor-risk/NON_CLAIMS_PANEL.md",
        "examples/vendor-risk/README.md",
        "examples/vendor-risk/evidence-card.md",
        "examples/vendor-risk/boundary-map.md",
        "examples/vendor-risk/review-packet/README.md"
    )

    foreach ($path in $paths) {
        Normalize-FileUtf8Lf $path
    }

    if ($PSCommandPath) {
        Normalize-FileUtf8Lf $PSCommandPath
    }
}

Assert-RepoRoot

Write-Host "Integrating Authority and Policy Context surface..."

Create-AuthorityPolicySpec
Create-VendorRiskAuthorityContext
Update-ReviewerArtifactsReadme
Update-SurfaceDoctrine
Update-ReviewerStartHere
Update-NonClaimPanelSpec
Update-ExampleNonClaimsPanel
Link-AuthorityContextFromVendorRiskFiles
Update-EvidenceCardSpec
Update-BoundaryMapSpec
Update-ReviewPacketSpec
Normalize-TouchedFiles

Write-Host ""
Write-Host "Done. Recommended next commands:"
Write-Host "  python -m pytest tests/test_line_endings_v0_1.py"
Write-Host "  python -m pytest"
Write-Host "  git diff -- docs examples scripts"
Write-Host "  git status -sb"
