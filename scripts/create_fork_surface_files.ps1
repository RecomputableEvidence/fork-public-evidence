param(
    [switch]$Overwrite,
    [switch]$WriteReadmeDraft
)

$ErrorActionPreference = "Stop"

# Run from repo root.
$RepoRoot = (Get-Location).Path

function Normalize-LF {
    param([Parameter(Mandatory = $true)][string]$Text)

    return ($Text -replace "`r`n", "`n" -replace "`r", "`n")
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $FullPath = Join-Path $RepoRoot $Path
    $Dir = Split-Path -Parent $FullPath

    if ($Dir -and -not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Force -Path $Dir | Out-Null
    }

    if ((Test-Path $FullPath) -and -not $Overwrite) {
        Write-Host "SKIP existing file: $Path"
        return
    }

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $LfContent = Normalize-LF $Content
    [System.IO.File]::WriteAllText($FullPath, $LfContent, $Utf8NoBom)

    Write-Host "WROTE: $Path"
}

Write-Utf8NoBomFile "docs/README_SURFACE_DOCTRINE.md" @'
# Fork Surface Doctrine v0.1

This document defines the current public and product surface doctrine for Fork. Treat these lines as invariants for the next iteration of the repository, reviewer artifacts, golden workflow, and pilot materials.

## Locked doctrine

### Product sentence

Fork preserves the evidence boundary around AI-assisted institutional work.

### Commercial metaphor

Fork is the missing evidence room for AI-assisted decisions.

### Signature feature

Every Fork packet exposes a **Not Established by This Record** panel.

### Pilot offer

One bounded AI-assisted workflow. One sealed evidence packet. One verification path. One reviewer-facing closeout report.

### Golden workflow

AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

## Surface separation

Fork maintains three distinct surfaces.

### Reviewer surface

What Legal, Audit, Risk, Compliance, GC, and AI governance reviewers can inspect directly.

Primary locations:

- `docs/reviewer-artifacts/`
- `examples/vendor-risk/`

### Pilot surface

What buyers and design partners evaluate when deciding whether Fork is useful for one bounded workflow.

Primary location:

- `docs/pilots/`

### Proof surface

What technical reviewers, standards participants, and diligence reviewers inspect to evaluate schemas, checkers, fixtures, receipts, and reproducibility materials.

Primary location:

- `docs/proof/`

## Surface QA question

Every new public artifact, feature, example, or outreach message should answer:

> Can a GC, auditor, CRO, or AI governance lead open the repo or packet and understand, in one pass, what Fork preserves, what it does not claim, and why that matters at the moment of institutional reliance?

If the answer is no, the surface is not yet legible.
'@

Write-Utf8NoBomFile "docs/reviewer-artifacts/EVIDENCE_CARD_SPEC_v0_1.md" @'
# Fork Evidence Card Specification v0.1

## Purpose

The Fork Evidence Card is a one-page reviewer-facing summary of an AI-assisted workflow.

It is designed for Legal, Audit, Risk, Compliance, GC, and AI governance reviewers who need to understand what happened, what was relied on, what evidence was preserved, and what the record explicitly does not establish.

## Audience

- General Counsel / Legal
- Internal Audit
- Compliance
- Risk
- AI governance leads
- Procurement or security reviewers for the golden workflow

## Required sections

1. Workflow summary
2. Packet identifier
3. Workflow participants or roles
4. AI-assisted artifact summary
5. Human review or change summary
6. Evidence references
7. First moment of institutional reliance
8. Verification status
9. Not Established by This Record

## Required fields

- `packet_id`
- `workflow_name`
- `workflow_type`
- `summary`
- `ai_artifact_reference`
- `human_review_reference`
- `evidence_references`
- `institutional_reliance_moment`
- `verification_receipt_reference`
- `non_claims_reference`

## Relationship to packet

The Evidence Card summarizes the sealed packet. It does not replace the packet, the manifest, the boundary map, or the verification receipt.

## Artifact non-claims

The Evidence Card does not certify:

- truth;
- legal sufficiency;
- regulatory compliance;
- model correctness;
- vendor approval;
- safety;
- downstream authority.

It summarizes the bounded evidence record preserved by Fork.

## Required rendered section

Every Evidence Card MUST include:

> **Not Established by This Record**
'@

Write-Utf8NoBomFile "docs/reviewer-artifacts/BOUNDARY_MAP_SPEC_v0_1.md" @'
# Fork Boundary Map Specification v0.1

## Purpose

The Fork Boundary Map makes claim movement legible across an AI-assisted workflow.

It shows how a request, AI output, human review, acceptance, modification, reliance event, and downstream consumption attempt relate to one another.

## Canonical flow

requested → generated → reviewed → accepted → modified → relied upon → consumed downstream

## Audience

- Legal reviewers
- Audit reviewers
- Risk reviewers
- Compliance teams
- AI governance teams
- AI platform teams

## Required sections

1. Workflow identifier
2. Node list
3. Edge list
4. First moment of institutional reliance
5. Downstream consumption events
6. Boundary expansion attempts, if any
7. Evidence references
8. Non-claim references

## Required node fields

- `node_id`
- `node_type`
- `timestamp`
- `actor_or_system`
- `artifact_reference`
- `claim_fragment`
- `evidence_reference`
- `non_claim_reference`

## Required edge fields

- `from`
- `to`
- `transition_type`
- `boundary_effect`
- `notes`

## Boundary effects

Permitted boundary effects include:

- `PRESERVED`
- `NARROWED`
- `EXPANDED`
- `UNRESOLVED`
- `MIXED`

Any `EXPANDED` effect MUST identify the authority or evidence supporting the expansion.

If no such authority exists, the expansion must be marked as unresolved or unsupported.

## Artifact non-claims

The Boundary Map does not certify:

- correctness;
- compliance;
- legal sufficiency;
- safety;
- model quality;
- vendor approval.

It records the structure of claim movement and makes possible boundary changes inspectable.

## Required rendered section

Every reviewer-facing Boundary Map MUST include or link to:

> **Not Established by This Record**
'@

Write-Utf8NoBomFile "docs/reviewer-artifacts/VERIFICATION_RECEIPT_SPEC_v0_1.md" @'
# Fork Verification Receipt Specification v0.1

## Purpose

The Fork Verification Receipt is the deterministic reviewer-facing artifact that records whether a Fork packet structurally verifies.

It is intentionally dry, bounded, and difficult to overread as approval.

## Audience

- Audit
- Legal
- Compliance
- Risk
- Technical reviewers
- Design partners

## Required sections

1. Packet identifier
2. Verification timestamp
3. Verifier name and version
4. Manifest verification result
5. Hash verification result
6. Boundary structure result
7. Non-claim preservation result
8. Files verified
9. Exceptions, warnings, or failures
10. Not Established by This Record

## Required fields

- `packet_id`
- `verified_at`
- `verifier_name`
- `verifier_version`
- `manifest_result`
- `hash_result`
- `boundary_result`
- `non_claims_result`
- `files_verified`
- `warnings`
- `failures`
- `non_claims_reference`

## Verifier behavior requirements

A Fork verifier SHOULD:

- fail if `non_claims.json` is missing;
- warn or fail if `not_established` is empty;
- display non-claims by default;
- include a non-claim summary in the Verification Receipt.

## Artifact non-claims

The Verification Receipt does not certify that the underlying AI output was correct, lawful, safe, compliant, complete, fair, or approved.

It only records whether the packet structurally verifies within Fork's declared scope.

## Required rendered section

Every Verification Receipt MUST include:

> **Not Established by This Record**
'@

Write-Utf8NoBomFile "docs/reviewer-artifacts/REVIEW_PACKET_SPEC_v0_1.md" @'
# Fork Review Packet Specification v0.1

## Purpose

The Fork Review Packet is the reviewer-operable bundle that Legal, Audit, Risk, Compliance, or AI governance teams can inspect after an AI-assisted workflow becomes eligible for institutional reliance.

## Audience

- General Counsel
- Compliance leadership
- Internal Audit
- Risk leadership
- AI governance teams
- Public-sector oversight reviewers
- Procurement reviewers
- Security reviewers

## Required contents

A Review Packet MUST include:

1. Evidence Card
2. Boundary Map
3. Verification Receipt
4. Evidence references or pointers
5. Human review/change record
6. AI artifact reference
7. Non-Claim Panel
8. Minimal verification instructions

## Relationship to sealed packet

The Review Packet is a rendered reviewer-facing view of the sealed packet.

It should not make broader claims than the packet itself supports.

## Required reviewer questions

The Review Packet should help answer:

- What was requested?
- What did the AI produce?
- What did a human review or change?
- What evidence was referenced?
- What became eligible for institutional reliance?
- What was explicitly not established?
- Does the packet still verify?
- Did any downstream consumer attempt to expand the claim?

## Artifact non-claims

The Review Packet does not certify:

- truth;
- compliance;
- legal sufficiency;
- model quality;
- safety;
- vendor approval.

It preserves and renders the bounded evidence record.

## Required rendered section

Every Review Packet MUST include:

> **Not Established by This Record**
'@

Write-Utf8NoBomFile "docs/reviewer-artifacts/NON_CLAIM_PANEL_SPEC_v0_1.md" @'
# Fork Non-Claim Panel Specification v0.1

## Purpose

The Non-Claim Panel is Fork's signature reviewer-facing feature.

It makes explicit what a sealed record does not establish.

This prevents preserved evidence from silently becoming broader authority.

## Required packet file

Every Fork packet MUST include:

`non_claims.json`

## Minimal structure

```json
{
  "version": "0.1.0",
  "not_established": [
    "This record does not certify legal sufficiency.",
    "This record does not establish vendor approval.",
    "This record does not certify model correctness.",
    "This record does not establish regulatory compliance.",
    "This record does not transfer upstream authority.",
    "This record does not prove underlying sources were true.",
    "This record preserves only the bounded evidence and reliance structure."
  ]
}
```

## Required rendered title

Every reviewer-facing artifact MUST render a section titled:

> Not Established by This Record

## Required appearances

The Non-Claim Panel MUST appear in:

- Evidence Card
- Review Packet
- Verification Receipt
- Replay / Recompute View, if present

## Verifier behavior

The verifier SHOULD:

- fail if `non_claims.json` is missing;
- warn or fail if `not_established` is empty;
- display non-claims by default;
- include a non-claim summary in the Verification Receipt.

## Boundary discipline

The Non-Claim Panel does not weaken the record.

It preserves the boundary of the record.

Fork's doctrine is:

> Preservation without inheritance.

That doctrine becomes operational when every packet states what the record does not establish.
'@

Write-Utf8NoBomFile "docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md" @'
Fork Reliance Evidence Pilot v0.1

Name
Fork Reliance Evidence Pilot

Duration
60–90 days

Scope
One bounded AI-assisted workflow.
One sealed evidence packet.
One verification path.
One reviewer-facing closeout report.

Default golden workflow
AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

Pilot purpose
The pilot evaluates whether Fork can preserve a reviewer-operable evidence boundary for one AI-assisted workflow at the moment the output becomes eligible for institutional reliance.

Deliverables

1. Sealed Evidence Packet
A sealed packet containing the workflow record, manifest, evidence references, boundary map, non-claims, and verification metadata.

2. Evidence Card
A one-page reviewer-facing summary of what happened, what was relied on, what evidence was preserved, what was not established, and whether the packet verifies.

3. Boundary Map
A reviewer-facing map of claim movement across the workflow.

4. Verification Receipt
A deterministic receipt showing packet integrity, structural verification, boundary conformance, and non-claim preservation.

5. Review Packet
A reviewer-operable bundle for Legal, Audit, Risk, Compliance, or AI governance review.

6. Non-Claim Panel
A required section titled:
Not Established by This Record

7. Closeout Report
The closeout report includes:
Workflow summary
First moment of institutional reliance
AI artifact and human review/change record
Evidence references
Preserved non-claims
Downstream expansion attempts, if any
Packet verification result
Recommended next workflows

Pricing lane
Indicative commercial ladder:
Design partner: $0–$25K
Proof of value: $75K / 60–90 days
Limited production: $125K–$175K/year
Enterprise: $400K–$750K/year+
Regulated multi-workflow deployments may require higher scope and pricing.

Explicit exclusions
The pilot does not:
certify compliance;
certify truth;
certify legal sufficiency;
certify model correctness;
establish vendor approval;
guarantee safety;
replace GRC, legal judgment, audit judgment, or governance programs;
act as runtime control;
transfer upstream authority.

Buyer-facing statement
At the end of the pilot, the organization receives a sealed evidence packet for one real AI-assisted workflow and a reviewer-facing closeout report showing what Fork preserved, what it did not claim, and where downstream reliance would require additional authority.
'@

Write-Utf8NoBomFile "docs/proof/README.md" @'
Fork Proof Surface

This directory is reserved for Fork's proof-layer materials:
schemas;
checkers;
fixtures;
receipts;
reproducibility materials;
boundary discipline.

The proof surface is for technical reviewers, standards participants, diligence reviewers, and design partners who need to inspect how Fork preserves boundaries without silently expanding claims.

The primary public surface should remain reviewer-operable and should not require readers to understand internal acronyms before understanding what Fork preserves.

Boundary
The proof surface may document internal mechanisms such as:
claim boundaries;
claim consumption events;
boundary deltas;
graph verification;
system mapping receipts;
transition localization;
recomputability design.

Those mechanisms support Fork's product surface but should not displace the reviewer-facing artifacts:
Evidence Card
Boundary Map
Verification Receipt
Review Packet
Non-Claim Panel
'@

Write-Utf8NoBomFile "examples/vendor-risk/README.md" @'
Vendor-Risk Golden Workflow Example

Purpose
This example is Fork's golden workflow for the current product surface.

It demonstrates:
AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

Scenario
A team requests an AI-assisted vendor-risk summary.
The AI produces a recommendation.
A human reviewer edits and accepts parts of the output.
The resulting memo becomes eligible for institutional reliance.
A downstream consumer later attempts to treat the memo as broader vendor approval.

Fork preserves the evidence boundary around that handoff.

Reviewer artifacts
This example includes:
evidence-card.md
boundary-map.md
non-claims.json
verification-receipt.json
review-packet/README.md

What this example shows
What was requested
What AI produced
What a human reviewed or changed
What evidence was referenced
The first moment of institutional reliance
What was explicitly not established
How a downstream expansion attempt is surfaced
Whether the record structurally verifies

What this example does not show
This example does not certify:
vendor approval;
legal sufficiency;
compliance;
model correctness;
safety;
truth of the underlying sources.
'@

Write-Utf8NoBomFile "examples/vendor-risk/evidence-card.md" @'
Fork Evidence Card: Vendor-Risk Golden Workflow

Workflow summary
An AI-assisted vendor-risk recommendation was generated, reviewed by a human, incorporated into an internal decision memo, and later referenced by a downstream consumer as if it established broader vendor approval.
Fork preserves the bounded evidence record for that workflow.

Packet
Packet ID: fork-example-vendor-risk-001
Workflow type: AI_ASSISTED_VENDOR_RISK_RECOMMENDATION
Golden workflow: AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt

What was requested
A vendor-risk summary to support internal review of a prospective vendor.

What AI produced
An AI-assisted recommendation summarizing vendor risk factors and suggesting a conditional internal path forward.

Human review/change record
A human reviewer accepted some portions, modified others, and incorporated the output into an internal decision memo.

Evidence references
Evidence references are represented in the associated review packet and boundary map.

First moment of institutional reliance
The first moment of institutional reliance occurs when the reviewed memo becomes eligible to inform an internal vendor-risk decision.

Downstream reliance attempt
A downstream consumer attempted to treat the memo as broader vendor approval.
Fork records that attempted expansion as a boundary issue rather than silently inheriting the broader claim.

Verification status
See:
verification-receipt.json

Not Established by This Record
This record does not certify legal sufficiency.
This record does not establish vendor approval.
This record does not certify model correctness.
This record does not establish regulatory compliance.
This record does not transfer upstream authority.
This record does not prove underlying sources were true.
This record preserves only the bounded evidence and reliance structure.
'@

Write-Utf8NoBomFile "examples/vendor-risk/boundary-map.md" @'
Fork Boundary Map: Vendor-Risk Golden Workflow

Canonical flow
requested → generated → reviewed → accepted/modified → relied upon → consumed downstream

Nodes
N1 — Request
Type: REQUESTED
Description: A user requests an AI-assisted vendor-risk summary.
Boundary effect: PRESERVED

N2 — AI output
Type: GENERATED
Description: The AI produces a vendor-risk recommendation.
Boundary effect: PRESERVED

N3 — Human review
Type: REVIEWED
Description: A human reviewer evaluates the AI output.
Boundary effect: PRESERVED

N4 — Human modification / acceptance
Type: ACCEPTED_MODIFIED
Description: The reviewer accepts some parts and modifies others.
Boundary effect: NARROWED

N5 — Institutional reliance
Type: RELIED_UPON
Description: The reviewed memo becomes eligible to inform an internal vendor-risk decision.
Boundary effect: PRESERVED

N6 — Downstream consumption attempt
Type: CONSUMED_DOWNSTREAM
Description: A downstream consumer attempts to treat the memo as broader vendor approval.
Boundary effect: EXPANDED

Boundary issue
The downstream consumption attempt expands the original record from a reviewed vendor-risk memo into apparent vendor approval.
Fork does not silently accept that expansion.
The expansion requires additional authority or evidence outside this packet.

Not Established by This Record
This record does not certify legal sufficiency.
This record does not establish vendor approval.
This record does not certify model correctness.
This record does not establish regulatory compliance.
This record does not transfer upstream authority.
This record does not prove underlying sources were true.
This record preserves only the bounded evidence and reliance structure.
'@

Write-Utf8NoBomFile "examples/vendor-risk/non-claims.json" @'
{
  "version": "0.1.0",
  "packet_id": "fork-example-vendor-risk-001",
  "not_established": [
    "This record does not certify legal sufficiency.",
    "This record does not establish vendor approval.",
    "This record does not certify model correctness.",
    "This record does not establish regulatory compliance.",
    "This record does not transfer upstream authority.",
    "This record does not prove underlying sources were true.",
    "This record preserves only the bounded evidence and reliance structure."
  ]
}
'@

Write-Utf8NoBomFile "examples/vendor-risk/verification-receipt.json" @'
{
  "version": "0.1.0",
  "packet_id": "fork-example-vendor-risk-001",
  "verified_at": "TBD",
  "verifier_name": "fork-verifier",
  "verifier_version": "TBD",
  "manifest_result": "EXAMPLE_NOT_EXECUTED",
  "hash_result": "EXAMPLE_NOT_EXECUTED",
  "boundary_result": "EXAMPLE_BOUNDARY_RENDERED",
  "non_claims_result": "NON_CLAIMS_PRESENT",
  "files_verified": [
    "examples/vendor-risk/evidence-card.md",
    "examples/vendor-risk/boundary-map.md",
    "examples/vendor-risk/non-claims.json",
    "examples/vendor-risk/review-packet/README.md"
  ],
  "warnings": [
    "This is a rendered example receipt, not an executed verifier output."
  ],
  "failures": [],
  "not_established_summary": [
    "This record does not certify legal sufficiency.",
    "This record does not establish vendor approval.",
    "This record does not certify model correctness.",
    "This record does not establish regulatory compliance.",
    "This record does not transfer upstream authority.",
    "This record does not prove underlying sources were true.",
    "This record preserves only the bounded evidence and reliance structure."
  ]
}
'@

Write-Utf8NoBomFile "examples/vendor-risk/review-packet/README.md" @'
Fork Review Packet: Vendor-Risk Golden Workflow

Purpose
This review packet provides a reviewer-operable view of the vendor-risk golden workflow.
It is intended for Legal, Audit, Risk, Compliance, Procurement, Security, or AI governance review.

Workflow
AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

Packet components
Evidence Card: ../evidence-card.md
Boundary Map: ../boundary-map.md
Non-Claims: ../non-claims.json
Verification Receipt: ../verification-receipt.json

Reviewer questions
This packet helps answer:
What was requested?
What did the AI produce?
What did the human reviewer accept or change?
What evidence was referenced?
When did the AI-assisted memo become eligible for institutional reliance?
What did a downstream consumer attempt to infer?
What does the record explicitly not establish?
Does the packet structurally verify?

Not Established by This Record
This record does not certify legal sufficiency.
This record does not establish vendor approval.
This record does not certify model correctness.
This record does not establish regulatory compliance.
This record does not transfer upstream authority.
This record does not prove underlying sources were true.
This record preserves only the bounded evidence and reliance structure.
'@

if ($WriteReadmeDraft) {
    Write-Utf8NoBomFile "README_SURFACE_TOP_LAYER_DRAFT.md" @'
Fork

Fork is evidence-boundary infrastructure for AI-assisted workflows. It preserves a reviewer-operable record of what was requested, what AI produced, what humans reviewed or changed, what evidence was referenced, what was explicitly not claimed, and whether the sealed packet still verifies later.

Fork does not certify truth, compliance, safety, legal sufficiency, model quality, or vendor approval. It preserves what the record can legitimately be said to establish, and what it explicitly does not establish.

What Fork is

Fork is designed to preserve the evidence boundary around AI-assisted institutional work.

It provides reviewer-facing artifacts for AI-assisted workflows, including:

- Evidence Card
- Boundary Map
- Verification Receipt
- Review Packet
- Non-Claim Panel

Fork helps reviewers answer:

> When an AI-assisted output became a basis for action, what exactly did the organization rely on, and does that record still verify?

What Fork is not

Fork is not:

- an AI governance platform;
- a compliance automation system;
- a model monitoring or observability tool;
- a runtime policy engine;
- an explainability or truth-certification system;
- a replacement for GRC, legal judgment, audit judgment, or governance programs.

Fork does not:

- certify legal sufficiency;
- establish regulatory compliance;
- declare vendor approval;
- prove model correctness;
- guarantee safety;
- transfer authority from one record to another.

Fork's doctrine is:

> Preservation without inheritance.

Golden workflow

The current golden workflow is:

> AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

This workflow demonstrates the moment an AI-assisted artifact becomes eligible for institutional reliance and the downstream risk that a bounded record may be silently expanded into a broader claim.

See:

- examples/vendor-risk/

Reviewer artifacts

Reviewer-facing artifacts are defined under:

- docs/reviewer-artifacts/

The current artifact set includes:

- Fork Evidence Card
- Fork Boundary Map
- Fork Verification Receipt
- Fork Review Packet
- Fork Non-Claim Panel

Pilot

The current buyer-facing pilot is:

> One bounded AI-assisted workflow. One sealed evidence packet. One verification path. One reviewer-facing closeout report.

See:

- docs/pilots/FORK_RELIANCE_EVIDENCE_PILOT_v0_1.md

Proof surface

Technical and proof-layer materials live under:

- docs/proof/

The proof surface may document schemas, checkers, fixtures, receipts, reproducibility materials, and boundary discipline. These mechanisms support the reviewer-facing product surface but should not be required for a reviewer to understand what Fork preserves.
'@
}

Write-Host ""
Write-Host "Fork surface files created."
Write-Host ""
Write-Host "Next commands:"
Write-Host " git status -sb"
Write-Host " git diff -- docs examples"
if ($WriteReadmeDraft) {
    Write-Host " Review README_SURFACE_TOP_LAYER_DRAFT.md before editing README.md"
}