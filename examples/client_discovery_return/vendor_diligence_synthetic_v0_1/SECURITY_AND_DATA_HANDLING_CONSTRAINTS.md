# Security and Data-Handling Constraints

## Purpose

This file identifies security, privacy, confidentiality, privilege, retention, and data-handling constraints.

## Data classification

- [ ] public
- [x] internal
- [x] confidential
- [ ] privileged
- [ ] regulated
- [ ] personal data
- [ ] customer data
- [x] financial data
- [ ] health data
- [ ] employment data
- [x] procurement data
- [x] security-sensitive data
- [ ] trade secret
- [ ] other: Not used
- [ ] unknown

## Handling constraints

- May artifacts leave the client environment? PARTIAL
- Are redactions required? YES
- Are hash-only representations required? PARTIAL
- Are external pointers required? YES
- Are retention limits required? YES
- Are destruction requirements required? YES
- Is privileged material involved? NO
- Is security review required before pilot scoping? YES
- Is vendor-risk review required before pilot scoping? YES
- Is legal approval required before any data transfer? YES

## Redaction requirements

Vendor confidential fields, security-control details, and pricing data should be redacted from exported copies where possible.

## Hash-only requirements

Full vendor attachment bundles should be represented by SHA-256 hashes during discovery.

## External-pointer requirements

Vendor documents should remain in ExampleDocs and be referenced by repository path and document ID.

## Retention and destruction requirements

Synthetic pilot exports would be retained for 90 days unless converted into a client evidence boundary review package.

## Required reviewers

Security reviewer, legal reviewer, vendor-risk owner, GRC platform owner.

## Security blockers

None