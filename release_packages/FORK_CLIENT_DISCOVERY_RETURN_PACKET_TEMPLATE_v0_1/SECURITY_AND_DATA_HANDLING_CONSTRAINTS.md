# Security and Data-Handling Constraints

## Purpose

This file identifies security, privacy, confidentiality, privilege, retention, and data-handling constraints.

Fork discovery should not request broader access than needed.

The client-specific evidence boundary must respect these constraints before any bridge is scoped.

## Data classification

Select all that may appear in the workflow:

- `[ ] public`
- `[ ] internal`
- `[ ] confidential`
- `[ ] privileged`
- `[ ] regulated`
- `[ ] personal data`
- `[ ] customer data`
- `[ ] financial data`
- `[ ] health data`
- `[ ] employment data`
- `[ ] procurement data`
- `[ ] security-sensitive data`
- `[ ] trade secret`
- `[ ] other: [CLIENT_TO_COMPLETE]`
- `[ ] unknown`

## Handling constraints

- May artifacts leave the client environment? `[YES / NO / PARTIAL / UNKNOWN]`
- Are redactions required? `[YES / NO / PARTIAL / UNKNOWN]`
- Are hash-only representations required? `[YES / NO / PARTIAL / UNKNOWN]`
- Are external pointers required? `[YES / NO / PARTIAL / UNKNOWN]`
- Are retention limits required? `[YES / NO / PARTIAL / UNKNOWN]`
- Are destruction requirements required? `[YES / NO / PARTIAL / UNKNOWN]`
- Is privileged material involved? `[YES / NO / POSSIBLE / UNKNOWN]`
- Is security review required before pilot scoping? `[YES / NO / UNKNOWN]`
- Is vendor-risk review required before pilot scoping? `[YES / NO / UNKNOWN]`
- Is legal approval required before any data transfer? `[YES / NO / UNKNOWN]`

## Redaction requirements

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Hash-only requirements

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## External-pointer requirements

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Retention and destruction requirements

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Required reviewers

List required reviewers before any pilot-ready implementation is scoped.

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`

## Security blockers

`[CLIENT_TO_COMPLETE / NONE / UNKNOWN]`