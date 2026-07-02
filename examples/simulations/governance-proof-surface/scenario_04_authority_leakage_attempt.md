# Scenario 04: Authority Leakage Attempt

## Purpose

This scenario tests whether Fork exposes downstream authority leakage.

The modeled drift is:

```text
reviewed by vendor-risk analyst
        ->
authorized by vendor-risk function
```

The purpose is not to block the downstream actor. The purpose is to make the authority leakage visible, classifiable, and reconstructable without converting role or policy context into transferred approval authority.

## Participating Systems

| System   | Role                                           |
|---------|------------------------------------------------|
| System A | AI-assisted production system                 |
| System B | Fork boundary-record layer                    |
| System C | Institutional review / policy context system  |
| System D  | Downstream operational or decision system    |
| System E | Audit / reconstruction / oversight system     |

## Flow

- System A produces an AI-assisted vendor-risk memo.
- System C records preliminary review by a vendor-risk analyst, with policy references.
- System B preserves the handoff boundary, including recorded role and policy context and explicit non-claims.
- System D reads the memo and context and treats it as if the "vendor-risk function" has authorized onboarding or approved the vendor.
- System E reconstructs the transition and identifies authority leakage.

## Original Role and Context

Recorded role:

- Vendor-risk analyst / preliminary reviewer.

Recorded policy context:

- Vendor-risk preliminary review policy reference (for example, `VR-PRELIM-REVIEW-v0.1`).

Recorded non-claims:

- Role and policy references do not establish approval authority, onboarding clearance, compliance, legal sufficiency, or institutional authorization.

## Downstream Authority Leakage Claim

The vendor-risk function (or equivalent) is treated as if it has:

- authorized onboarding, or
- issued final vendor approval.

## Expected Classification

Primary category:

- AUTHORITY_LEAKAGE

Secondary categories:

- CLAIM_SCOPE_EXPANSION
- POLICY_APPROVAL_CONFUSION

## Expected Fork Behavior

Fork does not block the downstream reliance attempt.  
Fork preserves the original role and policy context, records the attempted authority transfer, and exposes that no approval authority or policy-approval decision crossed the boundary.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Preliminary triage review claim.
- Recorded reviewer role.
- Recorded policy reference.
- Non-claims.
- Unresolved authority and compliance state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final approval authority.
- Onboarding clearance.
- Compliance determination.
- Legal sufficiency determination.
- Production readiness.
- Institutional authorization.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_AUTHORITY_LEAKAGE_EXPOSED`

## Non-Claims

This scenario does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.  
This scenario tests whether downstream authority leakage becomes inspectable.