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

The Verification Receipt does not certify that the underlying AI output was correct, lawful, safe, compliant, complete, fair, or approved. It only records whether the packet structurally verifies within Fork's declared scope.

## Required rendered section

Every Verification Receipt MUST include:

> **Not Established by This Record**
