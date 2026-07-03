param(
    [string]$ReadmePath = "README.md"
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$FullReadmePath = Join-Path $RepoRoot $ReadmePath

if (-not (Test-Path $FullReadmePath)) {
    throw "README not found at: $FullReadmePath"
}

function Normalize-LF {
    param([Parameter(Mandatory = $true)][string]$Text)
    return ($Text -replace "`r`n", "`n" -replace "`r", "`n")
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $LfContent = Normalize-LF $Content
    [System.IO.File]::WriteAllText($Path, $LfContent, $Utf8NoBom)
}

$topBlock = @'
# Fork Public Evidence

> **Boundary note:** This repository provides a bounded, read-only evidence disclosure and verification surface. It does not certify legal admissibility, production readiness, security posture, SOC 2, ISO, HIPAA, regulatory compliance, customer deployment, commercial pilot approval, AI-output correctness, source completeness, or institutional authority.

**Recomputable Evidence for AI-assisted workflows.**

Fork is evidence-boundary infrastructure for AI-assisted workflows. It preserves a reviewer-operable record of what was requested, what AI produced, what humans reviewed or changed, what evidence was referenced, what was explicitly not claimed, and whether the sealed packet still verifies later.

Fork preserves the evidence boundary around AI-assisted institutional work.

Fork does **not** certify truth, compliance, safety, legal sufficiency, model quality, vendor approval, production readiness, source completeness, or institutional authority. It preserves what the record can legitimately be said to establish, and what it explicitly does not establish.

Fork is not a runtime control plane, policy engine, compliance oracle, audit function, legal determination system, AI-output correctness validator, production-deployment claim, or authority-transfer mechanism.

## What Fork is

Fork is designed to preserve the evidence boundary around AI-assisted institutional work.

It provides reviewer-facing artifacts for AI-assisted workflows, including:

- Evidence Card
- Boundary Map
- Verification Receipt
- Review Packet
- Non-Claim Panel

Fork helps reviewers answer:

> When an AI-assisted output became a basis for action, what exactly did the organization rely on, what was explicitly not established, and does that record still verify?

## What Fork is not

Fork is not:

- an AI governance platform;
- a compliance automation system;
- a model monitoring or observability tool;
- a runtime policy engine;
- an explainability or truth-certification system;
- a replacement for GRC, legal judgment, audit judgment, risk acceptance, or governance programs.

Fork does not:

- certify legal sufficiency;
- establish regulatory compliance;
- declare vendor approval;
- prove model correctness;
- guarantee safety;
- validate AI-output correctness;
- establish source completeness;
- transfer authority from one record to another.

Fork's doctrine is:

> Preservation without inheritance.

## Golden workflow

The current golden workflow is:

> AI-assisted vendor-risk recommendation -> internal decision memo -> downstream reliance attempt.

This workflow demonstrates the moment an AI-assisted artifact becomes eligible for institutional reliance and the downstream risk that a bounded record may be silently expanded into a broader claim.

See:

- `examples/vendor-risk/`

## Reviewer artifacts

Reviewer-facing artifacts are defined under:

- `docs/reviewer-artifacts/`

The current artifact set includes:

- Fork Evidence Card
- Fork Boundary Map
- Fork Verification Receipt
- Fork Review Packet
- Fork Non-Claim Panel

Every Fork packet exposes a required section titled:

> **Not Established by This Record**

## Pilot

The current buyer-facing pilot is:

> One bounded AI-assisted workflow. One sealed evidence packet. One verification path. One reviewer-facing closeout report.

See:

- `docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md`

## Proof surface

Technical and proof-layer materials live under:

- `docs/proof/`

The proof surface may document schemas, checkers, fixtures, receipts, reproducibility materials, and boundary discipline. These mechanisms support the reviewer-facing product surface but should not be required for a reviewer to understand what Fork preserves.

'@

$routingStart = "<!-- FORK_PUBLIC_PRESENCE_ROUTING_START -->"
$routingEnd = "<!-- FORK_PUBLIC_PRESENCE_ROUTING_END -->"

$routingBlock = @"
$routingStart

## Public presence and workflow-inlet routing

Fork routes by evidence-boundary input, not by buyer persona.

A reviewer, advisor, enterprise sponsor, legal/compliance leader, audit leader, risk leader, technical sponsor, source-system owner, GRC owner, AI governance lead, or co-integration partner may all enter through the same public surface.

The correct inlet depends on what the visitor can provide.

### Public review input

Use:

- `REVIEWER_QUICK_START_v0_1.md`
- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

### Candidate workflow input

Start with:

- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`

### Client-side workflow/source-system input

Complete:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/`

### Fork-authored evidence-boundary output

Fork may draft:

- `release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/`

only after reviewing a completed Client Discovery Return Packet.

### Sidecar bridge specification

A sidecar bridge follows an accepted evidence boundary. It is not assumed from public review alone.

### Bounded workflow PoV

A PoV may be scoped only around one accepted bounded workflow.

For the canonical routing cadence, see:

- `docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md`

This routing does not establish production readiness, customer deployment, procurement approval, legal sufficiency, compliance satisfaction, audit sufficiency, source completeness, security approval, risk acceptance, workflow suitability, commercial pilot approval, AI-output correctness, decision correctness, or institutional authority.

## Enterprise discovery and bounded workflow PoV

Fork can be evaluated only around a bounded AI-assisted workflow whose evidence boundary has been described, reviewed, and accepted for scoping.

The governing sequence is:

1. Public repo orientation.
2. Workflow-inlet routing.
3. Client Discovery Return Packet.
4. Fork review of returned workflow/source-system facts.
5. Client Evidence Boundary Packet draft, if responsible.
6. Client review of the proposed evidence boundary.
7. Sidecar bridge specification candidate, if the boundary is accepted.
8. Bounded workflow PoV scope, if commercially and operationally appropriate.

The Client Discovery Return Packet is the inbound mapping record.

The Client Evidence Boundary Packet is the Fork-authored boundary draft.

The sidecar bridge is downstream of the accepted boundary.

The institution owns the action. Fork preserves the bounded evidence record.

For bounded technical review, design-partner discussion, or enterprise discovery, contact Ryan Feller via LinkedIn.

This routing does not establish a binding quote, procurement approval, production readiness, customer deployment, commercial pilot approval, legal sufficiency, security certification, compliance satisfaction, audit sufficiency, risk acceptance, workflow suitability, source-system access approval, implementation approval, or sidecar bridge approval.

$routingEnd
"@

$text = Get-Content -Raw -Path $FullReadmePath
$text = Normalize-LF $text

# Replace everything from the top of README through the "## Start here" heading,
# while preserving the existing Start here content below the heading.
$topPattern = "(?ms)\A# Fork Public Evidence.*?^## Start here\s*"
if ($text -match $topPattern) {
    $text = [regex]::Replace(
        $text,
        $topPattern,
        ($topBlock.TrimEnd() + "`n`n## Start here`n"),
        1
    )
}
else {
    throw "Could not locate top README block ending at '## Start here'. No changes written."
}

# Normalize/repair the managed public-presence routing block if it exists.
$routingPattern = "(?s)$([regex]::Escape($routingStart)).*?$([regex]::Escape($routingEnd))"
if ($text -match $routingPattern) {
    $text = [regex]::Replace(
        $text,
        $routingPattern,
        $routingBlock.TrimEnd(),
        1
    )
}

# Repair common mojibake introduced by encoding mismatch.
$text = $text -replace ("Copyright" + [char]0x00C3 + [char]0x0082 + [char]0x00C2 + [char]0x00A9), ("Copyright" + [char]0x00A9)

Write-Utf8NoBomFile -Path $FullReadmePath -Content ($text.TrimEnd() + "`n")

Write-Host "Updated README top surface layer and repaired managed routing block."