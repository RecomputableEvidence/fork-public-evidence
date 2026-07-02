# Scenario 03: Scope Expansion Attempt

## Purpose

This scenario tests whether Fork exposes downstream claim expansion.

The modeled expansion is:

```text
reviewed for preliminary triage
        ->
approved / cleared for onboarding
```

The purpose is not to block the downstream actor. The purpose is to make the semantic expansion visible, classifiable, and reconstructable.

## Participating Systems

| System   | Role                                           |
|---------|------------------------------------------------|
| System A | AI-assisted production system                 |
| System B | Fork boundary-record layer                    |
| System C | Institutional review / policy context system  |
| System D1 | First downstream consumer                    |
| System D2 | Second downstream consumer / operational labeler |
| System E | Audit / reconstruction / oversight system     |

## Flow

- System A produces an AI-assisted vendor-risk memo.
- System C records preliminary review context.
- System B preserves the original handoff boundary.
- System D1 consumes the memo within the preliminary triage scope.
- System D2 rephrases the status as "approved for onboarding" or "cleared for onboarding."
- System E reconstructs the transition and identifies scope expansion.

## Original Claim

The vendor-risk memo was produced and reviewed for preliminary triage only.

## Downstream Expanded Claim

The vendor is approved / cleared for onboarding.

## Expected Classification

Primary:

- CLAIM_SCOPE_EXPANSION

Secondary:

- AUTHORITY_LEAKAGE

## Expected Fork Behavior

Fork does not block the downstream phrasing.  
Fork preserves the original claim boundary, records the attempted expanded consumption, and exposes that the downstream wording exceeds the recorded preliminary review scope unless supported by separate authority and evidence.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Preliminary triage review claim.
- Evidence references.
- Authority and policy context.
- Non-claims.
- Unresolved state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final vendor approval.
- Cleared onboarding status.
- Compliance determination.
- Legal sufficiency.
- Production readiness.
- Factual correctness guarantee.
- Institutional authorization.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_INHERITANCE_EXPOSED`

## Non-Claims

This scenario does not establish correctness, compliance, legal sufficiency, institutional authority, production readiness, or general validity.  
This scenario tests whether a downstream scope expansion becomes inspectable.