# Evidence Artifact Map

## Purpose

This file classifies evidence artifacts for the candidate workflow.

## Artifact table

| Artifact | Description | Source system | Category | Format | Sensitivity | Retention risk | Notes |
|---|---|---|---|---|---|---|---|
| Vendor intake ticket export | Request metadata and initiating event | ExampleTickets | CAPTURED | CSV | MEDIUM | LOW | Captures request state |
| Vendor questionnaire metadata | Questionnaire response metadata | ExampleGRC | CAPTURED | JSON | HIGH | MEDIUM | Full attachments not copied |
| AI review output | AI summary and risk flags | ExampleAIReview | CAPTURED | JSON | MEDIUM | MEDIUM | Used for reconstruction, not correctness |
| Vendor attachment bundle hash | Hash of supporting vendor documents | ExampleDocs | HASHED_REFERENCE | SHA-256 list | RESTRICTED | HIGH | Documents remain in client repository |
| Vendor document repository path | Pointer to source documents | ExampleDocs | EXTERNAL_POINTER | Repository path | RESTRICTED | HIGH | External pointer only |
| Hidden vendor model routing | Vendor backend logic | ExampleAIReview | SOURCE_UNAVAILABLE | Not available | HIGH | HIGH | Explicitly not reconstructed |
| Legal admissibility | Legal conclusion | Not applicable | EXPLICIT_NON_CLAIM | Not applicable | HIGH | Not applicable | Outside Fork claim boundary |

## Captured evidence

Vendor intake ticket export, vendor questionnaire metadata, AI review output, human review note, disposition state, escalation marker, final vendor-risk disposition.

## Hashed references

Vendor attachment bundle hash and policy snapshot hash.

## External pointers

Vendor document repository path, ticket URL, GRC case ID, vendor questionnaire ID.

## Source unavailable

Hidden vendor model routing, complete backend system prompts, unexported internal vendor telemetry.

## Explicit non-claims

Fork does not claim source completeness, AI output correctness, decision correctness, legal admissibility, compliance satisfaction, or audit sufficiency.

## Evidence sufficiency concern

- [x] YES
- [ ] PARTIAL
- [ ] NO
- [ ] UNKNOWN

Reason:

The available evidence appears sufficient for a bounded pilot discovery review of the vendor diligence workflow, subject to client review of hash-only and external pointer constraints.