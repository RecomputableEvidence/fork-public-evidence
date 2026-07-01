# Fork Evidence Card Specification v0.1

## Purpose

The Fork Evidence Card is a one-page reviewer-facing summary of an AI-assisted workflow. It is designed for Legal, Audit, Risk, Compliance, GC, and AI governance reviewers who need to understand what happened, what was relied on, what evidence was preserved, and what the record explicitly does not establish.

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

The Evidence Card does not certify truth, legal sufficiency, regulatory compliance, model correctness, vendor approval, safety, or downstream authority. It summarizes the bounded evidence record preserved by Fork.

## Required rendered section

Every Evidence Card MUST include:

> **Not Established by This Record**
