<#
.SYNOPSIS
  Adds Fork workflow-inlet routing and onboarding cadence documentation.

.DESCRIPTION
  This script:
    1. Creates docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md
    2. Replaces README.md buyer/persona routing with workflow-inlet routing
    3. Adds a routing reference to docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md
    4. Adds an inbound-mapping note to the Client Discovery Return Packet README
    5. Adds an outbound-boundary note to the Client Evidence Boundary Packet README

  It does not commit or push.
#>

[CmdletBinding()]
param(
    [switch]$AllowDirtyTree,
    [switch]$CreateBranch,
    [string]$BranchName = "workflow-inlet-routing-v0.1"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-RepoRoot {
    if (-not (Test-Path ".git")) {
        throw "Run this script from the repository root. Expected .git directory was not found."
    }

    if (-not (Test-Path "README.md")) {
        throw "Run this script from the repository root. README.md was not found."
    }
}

function Assert-CleanTree {
    if ($AllowDirtyTree) {
        Write-Warning "AllowDirtyTree supplied; skipping clean-tree check."
        return
    }

    $status = git status --porcelain
    if ($status) {
        throw @"
Working tree is not clean.

Run:
  git status

Then either commit/stash existing work, or rerun with:
  -AllowDirtyTree
"@
    }
}

function Use-WorkingBranch {
    if (-not $CreateBranch) {
        return
    }

    $existing = git branch --list $BranchName
    if ($existing) {
        Write-Step "Switching to existing branch $BranchName"
        git switch $BranchName | Out-Null
    } else {
        Write-Step "Creating branch $BranchName"
        git switch -c $BranchName | Out-Null
    }
}

function Set-Utf8NoBom {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Content
    )

    $resolvedPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($resolvedPath, $Content, $utf8NoBom)
}

function New-DirectoryIfMissing {
    param([string]$Path)

    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Upsert-ManagedBlock {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$BlockName,
        [Parameter(Mandatory=$true)][string]$BlockContent,
        [string]$AppendAfterHeading
    )

    if (-not (Test-Path $Path)) {
        Write-Warning "File not found; skipping: $Path"
        return
    }

    $content = Get-Content $Path -Raw
    $start = "<!-- BEGIN $BlockName -->"
    $end = "<!-- END $BlockName -->"

    $fullBlock = @"
$start
$BlockContent
$end
"@

    $pattern = "(?s)<!-- BEGIN $([regex]::Escape($BlockName)) -->.*?<!-- END $([regex]::Escape($BlockName)) -->"

    if ($content -match $pattern) {
        $content = [regex]::Replace(
            $content,
            $pattern,
            [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $fullBlock }
        )

        Set-Utf8NoBom -Path $Path -Content $content
        return
    }

    if ($AppendAfterHeading) {
        $headingPattern = "(?m)^## $([regex]::Escape($AppendAfterHeading))\s*$"
        $match = [regex]::Match($content, $headingPattern)

        if ($match.Success) {
            $insertAt = $match.Index + $match.Length
            $content = $content.Insert($insertAt, "`r`n`r`n$fullBlock")
            Set-Utf8NoBom -Path $Path -Content $content
            return
        }
    }

    $content = $content.TrimEnd() + "`r`n`r`n" + $fullBlock + "`r`n"
    Set-Utf8NoBom -Path $Path -Content $content
}

function Write-InletRoutingDoc {
    New-DirectoryIfMissing "docs"

    $path = "docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md"

    $content = @'
# Fork Inlet Routing and Onboarding Cadence v0.1

## Purpose

This document defines how public reviewers, enterprise contacts, workflow owners, technical counterparts, and co-integration partners route themselves from the public Fork repository into the appropriate input channel.

Fork routes by evidence-boundary input, not by buyer persona.

A visitor does not need to know whether they are the buyer. They need to identify what workflow information they can provide.

This document is a routing and boundary artifact. It is not a production-readiness claim, onboarding approval, implementation approval, commercial pilot approval, compliance conclusion, legal sufficiency claim, audit conclusion, security approval, risk acceptance, or procurement artifact.

## Routing principle

Do not choose a path by title.

Choose the inlet that matches the information available.

Fork is inclusive across enterprise functions because AI-assisted workflow evidence can involve legal, compliance, audit, risk, security, technical systems, source-system owners, AI governance leads, executive sponsors, and co-integration partners.

Fork does not route those parties into separate buyer channels.

Fork routes their input into the evidence-boundary mapping process.

## Inlet map

### I0 — Public Review Inlet

Use when a reviewer wants to understand Fork, challenge its doctrine, inspect its public boundaries, or reproduce bounded verification commands.

Start with:

- `REVIEWER_QUICK_START_v0_1.md`
- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

This inlet does not imply enterprise discovery, client suitability, implementation readiness, or commercial pilot approval.

### I1 — Candidate Workflow Inlet

Use when a contact can identify a real AI-assisted workflow where later reconstruction would matter.

Examples include vendor-risk review, audit evidence assembly, legal operations review, compliance review, security triage, model evaluation handoff, AI-assisted approval chains, or other institutional workflows where AI-assisted output enters action, review, escalation, or reliance.

Start with:

- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`

This inlet identifies a possible workflow. It does not establish workflow suitability.

### I2 — Source-System / Export Inlet

Use when a contact can describe the systems, logs, records, exports, APIs, files, tickets, messages, approval systems, or data surfaces involved in a candidate workflow.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/SOURCE_SYSTEM_INVENTORY.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/ACCESS_AND_EXPORT_MODEL.md`

This inlet does not establish that Fork can access, capture, export, observe, or verify all listed systems.

### I3 — Evidence-Artifact Inlet

Use when a contact can describe what should be preserved, hashed, referenced, sealed, excluded, redacted, or treated as unavailable.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/EVIDENCE_ARTIFACT_MAP.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CLAIMS_AND_NON_CLAIMS.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md`

This inlet does not establish source completeness, legal admissibility, compliance sufficiency, audit sufficiency, or decision correctness.

### I4 — State-Transition Inlet

Use when a contact can identify where the workflow changes state.

Examples include request creation, AI output generation, human review, escalation, approval, rejection, override, exception handling, evidence attachment, downstream reliance, or external handoff.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/STATE_TRANSITION_MAP.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/AI_ASSISTED_SURFACE.md`

This inlet does not establish that Fork controls, blocks, approves, or modifies runtime workflow execution.

### I5 — Security / Data-Handling Inlet

Use when a contact can describe confidentiality constraints, redaction needs, retention rules, air-gap requirements, access limitations, data residency issues, regulated data, or prohibited capture surfaces.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/ACCESS_AND_EXPORT_MODEL.md`

This inlet does not establish security approval, risk acceptance, production access, or client data handling authorization.

### I6 — Institutional Ownership Inlet

Use when a contact can identify workflow owners, decision owners, source-system owners, legal/compliance/audit/risk owners, security reviewers, executive sponsors, or approval authorities.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/INSTITUTIONAL_OWNERSHIP_MAP.md`

This inlet does not transfer institutional authority to Fork.

The institution owns the action.

Fork preserves the bounded evidence record.

### I7 — Co-Integration Inlet

Use when a platform, GRC, audit, AI governance, evidence, workflow, or integration counterparty needs to map its own boundary to Fork's boundary.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CO_INTEGRATION_BOUNDARY.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CONFIGURATION_OUTPUT_TARGETS.md`

This inlet does not establish compatibility, endorsement, implementation readiness, shared authority, or proof-obligation transfer.

## Onboarding cadence

Fork public routing follows this sequence:

1. Public repo orientation.
2. Inlet identification.
3. Candidate workflow identification.
4. Client Discovery Return Packet completion.
5. Fork review of returned workflow/source-system facts.
6. Client Evidence Boundary Packet draft, if responsible.
7. Client review of the evidence boundary.
8. Sidecar bridge specification candidate, if the boundary is accepted.
9. Bounded workflow PoV scope, if commercially and operationally appropriate.
10. Preservation execution only within the accepted boundary.

No later step is implied by an earlier step.

## Mapping protocol

The mapping protocol is:

```text
Public Repo
  -> Inlet Router
  -> Client Discovery Return Packet
  -> Fork Mapping Review
  -> Client Evidence Boundary Packet
  -> Sidecar Bridge Specification Candidate
  -> Bounded Workflow PoV / Not Suitable / Blocked

The Client Discovery Return Packet is the inbound mapping record.
The Client Evidence Boundary Packet is the Fork-authored boundary draft.
The sidecar bridge is downstream of the accepted evidence boundary.
The bounded workflow PoV is a commercial and operational wrapper around one accepted bounded workflow.
Required separation
Fork must not collapse these stages:
Public review is not client discovery.
Client discovery is not onboarding.
Onboarding is not deployment.
Discovery return is not sidecar approval.
Client evidence boundary is not production integration.
Sidecar bridge specification is not workflow authority.
Bounded preservation is not legal, compliance, audit, security, risk, or decision approval.
Non-claim boundary
This routing does not establish:
production readiness
customer deployment
procurement approval
legal sufficiency
legal admissibility
compliance satisfaction
audit sufficiency
security approval
risk acceptance
workflow suitability
commercial pilot approval
source completeness
AI-output correctness
decision correctness
runtime control
response authority
remediation ownership
institutional authority
co-integration compatibility
proof-obligation transfer
Canonical sentence
Fork does not route by title.
Fork routes by evidence-boundary input.
Process sentence
The public repo orients the reviewer; the inlet router identifies the input channel; the Client Discovery Return Packet captures the client-side facts; the Client Evidence Boundary Packet converts those facts into a bounded preservation surface; the sidecar bridge follows only after the boundary is accepted.
'@
    Set-Utf8NoBom -Path $path -Content $content
}

function Replace-ReadmeRoutingSections {
    $path = "README.md"
    if (-not (Test-Path $path)) {
        throw "README.md not found."
    }

    $content = Get-Content $path -Raw

    $replacement = @'

Public presence and workflow-inlet routing
Fork routes by evidence-boundary input, not by buyer persona.
A reviewer, advisor, enterprise sponsor, legal/compliance leader, audit leader, risk leader, technical sponsor, source-system owner, GRC owner, AI governance lead, or co-integration partner may all enter through the same public surface.
The correct inlet depends on what the visitor can provide:
Public review input: use REVIEWER_QUICK_START_v0_1.md, docs/REVIEWER_START_HERE_v0_1.md, docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md, and docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md.
Candidate workflow input: start with release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/.
Client-side workflow/source-system input: complete release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/.
Fork-authored evidence-boundary output: Fork may draft release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/ only after reviewing a completed Client Discovery Return Packet.
Sidecar bridge specification: a sidecar bridge follows an accepted evidence boundary; it is not assumed from public review alone.
Bounded workflow PoV: a PoV may be scoped only around one accepted bounded workflow.
For the canonical routing cadence, see:
docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md
This routing does not establish production readiness, customer deployment, procurement approval, legal sufficiency, compliance satisfaction, audit sufficiency, source completeness, security approval, risk acceptance, workflow suitability, commercial pilot approval, AI-output correctness, decision correctness, or institutional authority.
Enterprise discovery and bounded workflow PoV
Fork can be evaluated only around a bounded AI-assisted workflow whose evidence boundary has been described, reviewed, and accepted for scoping.
The governing sequence is:
Public repo orientation.
Workflow-inlet routing.
Client Discovery Return Packet.
Fork review of returned workflow/source-system facts.
Client Evidence Boundary Packet draft, if responsible.
Client review of the proposed evidence boundary.
Sidecar bridge specification candidate, if the boundary is accepted.
Bounded workflow PoV scope, if commercially and operationally appropriate.
The Client Discovery Return Packet is the inbound mapping record.
The Client Evidence Boundary Packet is the Fork-authored boundary draft.
The sidecar bridge is downstream of the accepted boundary.
The institution owns the action. Fork preserves the bounded evidence record.
For bounded technical review, design-partner discussion, or enterprise discovery, contact Ryan Feller via LinkedIn.
This routing does not establish a binding quote, procurement approval, production readiness, customer deployment, commercial pilot approval, legal sufficiency, security certification, compliance satisfaction, audit sufficiency, risk acceptance, workflow suitability, source-system access approval, implementation approval, or sidecar bridge approval.
'@

    $pattern = "(?ms)^## Public presence and buyer routing.*?(?=^## About.*$|\z)"

    if ($content -match $pattern) {
        $content = [regex]::Replace(
            $content,
            $pattern,
            [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $replacement + "`r`n" }
        )
    } else {
        $content = $content.TrimEnd() + "`r`n`r`n" + $replacement + "`r`n"
    }

    Set-Utf8NoBom -Path $path -Content $content
}

function Update-PublicReviewPackageIndex {
    $path = "docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md"
    $block = @'

Workflow-inlet routing
Fork routes by evidence-boundary input, not by buyer persona.
Use docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md to determine whether a visitor should enter through public review, candidate workflow identification, source-system/export mapping, evidence-artifact mapping, state-transition mapping, security/data-handling constraints, institutional ownership, or co-integration boundary review.
The routing sequence is:
Public repo orientation.
Workflow-inlet routing.
Client Discovery Return Packet.
Fork review of returned workflow/source-system facts.
Client Evidence Boundary Packet draft, if responsible.
Sidecar bridge specification candidate, if the boundary is accepted.
Bounded workflow PoV scope, if commercially and operationally appropriate.
This routing does not establish production readiness, legal sufficiency, compliance satisfaction, audit sufficiency, security approval, risk acceptance, workflow suitability, source completeness, commercial pilot approval, or institutional authority.
'@

    Upsert-ManagedBlock `
        -Path $path `
        -BlockName "FORK_WORKFLOW_INLET_ROUTING_V0_1" `
        -BlockContent $block `
        -AppendAfterHeading "Canonical entry point"
}

function Update-ClientDiscoveryReadme {
    $path = "release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/README.md"
    $block = @'

Workflow-inlet routing role
This packet is the inbound mapping record for workflow-inlet routing.
A visitor may arrive through any of the following input channels:
candidate workflow identification
source-system/export mapping
evidence-artifact mapping
AI-assisted surface description
state-transition mapping
security/data-handling constraints
institutional ownership mapping
co-integration boundary review
The packet consolidates those inputs into a single client-side discovery return.
Fork uses the completed packet to determine whether a client-specific evidence boundary can be responsibly drafted.
Completion of this packet does not establish onboarding, deployment, source-system access approval, production integration approval, workflow suitability, legal sufficiency, compliance satisfaction, audit sufficiency, security approval, risk acceptance, or sidecar bridge approval.
'@

    Upsert-ManagedBlock `
        -Path $path `
        -BlockName "FORK_WORKFLOW_INLET_ROLE_V0_1" `
        -BlockContent $block `
        -AppendAfterHeading "Purpose"
}

function Update-ClientEvidenceBoundaryReadme {
    $path = "release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/README.md"
    $block = @'

Workflow-inlet routing role
This packet is the Fork-authored boundary draft produced only after review of a completed Client Discovery Return Packet.
It converts client-side workflow/source-system facts into a bounded preservation surface.
It is downstream of workflow-inlet routing and upstream of any sidecar bridge specification candidate.
The governing sequence is:
Client Discovery Return Packet maps the environment.
Fork reviews the returned facts and unknowns.
Fork drafts this Client Evidence Boundary Packet only if responsible.
The client reviews the proposed boundary.
A sidecar bridge specification candidate may follow only after the boundary is accepted.
This packet does not establish production deployment, client onboarding, source-system access approval, legal admissibility, compliance satisfaction, audit conclusions, security approval, risk acceptance, AI-output correctness, decision correctness, runtime workflow control, or sidecar bridge approval.
'@

    Upsert-ManagedBlock `
        -Path $path `
        -BlockName "FORK_WORKFLOW_INLET_ROLE_V0_1" `
        -BlockContent $block `
        -AppendAfterHeading "Purpose"
}

function Show-Result {
    Write-Host ""
    Write-Host "Updated files:" -ForegroundColor Green
    git status --short
    Write-Host ""
    Write-Host "Review with:" -ForegroundColor Cyan
    Write-Host "  git diff -- README.md"
    Write-Host "  git diff -- docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md"
    Write-Host "  git diff -- docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md"
    Write-Host "  git diff -- release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/README.md"
    Write-Host "  git diff -- release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/README.md"
    Write-Host ""
    Write-Host "No commit or push was performed." -ForegroundColor Yellow
}

Assert-RepoRoot
Assert-CleanTree
Use-WorkingBranch

Write-Step "Writing inlet routing and onboarding cadence doc"
Write-InletRoutingDoc

Write-Step "Replacing README buyer routing with workflow-inlet routing"
Replace-ReadmeRoutingSections

Write-Step "Updating public review package index"
Update-PublicReviewPackageIndex

Write-Step "Updating Client Discovery Return Packet README"
Update-ClientDiscoveryReadme

Write-Step "Updating Client Evidence Boundary Packet README"
Update-ClientEvidenceBoundaryReadme

