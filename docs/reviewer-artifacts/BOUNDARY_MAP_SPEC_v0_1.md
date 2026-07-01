# Fork Boundary Map Specification v0.1

## Purpose

The Fork Boundary Map makes claim movement legible across an AI-assisted workflow. It shows how a request, AI output, human review, acceptance, modification, reliance event, and downstream consumption attempt relate to one another.

## Canonical flow

requested â†’ generated â†’ reviewed â†’ accepted â†’ modified â†’ relied upon â†’ consumed downstream

## Audience

- Legal reviewers
- Audit reviewers
- Risk reviewers
- Compliance teams
- AI governance and platform teams

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

Any `EXPANDED` effect MUST identify the authority or evidence supporting the expansion. If no such authority exists, the expansion must be marked as unresolved or unsupported.

## Artifact non-claims

The Boundary Map does not certify correctness, compliance, legal sufficiency, safety, or vendor approval. It records the structure of claim movement and makes possible boundary changes inspectable.

## Required rendered section

Every reviewer-facing Boundary Map MUST include or link to:

> **Not Established by This Record**
