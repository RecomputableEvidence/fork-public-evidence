# Scenario 03: Scope Expansion Attempt

## Purpose

This scenario tests whether Fork exposes a downstream claim expansion attempt.

## Flow

1. Upstream artifact records a narrow claim: preliminary vendor-risk review completed.
2. Downstream system treats the artifact as vendor cleared.
3. Fork records whether the downstream claim preserved, narrowed, expanded, or exceeded the upstream boundary.

## Original Claim

`Vendor-risk memo reviewed for preliminary triage only.`

## Downstream Inference

`Vendor cleared for onboarding.`

## Expected Classification

`CLAIM_SCOPE_EXPANSION`

## Expected Reconstruction Outcome

`UNSUPPORTED_INHERITANCE_EXPOSED`

## What Remains Outside Fork

- Whether the vendor should be onboarded.
- Whether the reviewer had approval authority.
- Whether compliance requirements were satisfied.
- Whether the decision was correct.