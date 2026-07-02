# Scenario 05: Policy-Reference Laundering Attempt

## Purpose

This scenario tests whether Fork exposes policy-reference laundering.

## Flow

1. A policy reference is included in the workflow context.
2. Downstream system treats the policy reference as policy applicability or compliance satisfaction.
3. Fork preserves the distinction between policy referenced and policy satisfied.

## Recorded Context

`Policy VR-PRELIM-REVIEW-v0.1 referenced during preliminary review.`

## Downstream Inference

`Workflow complied with VR-PRELIM-REVIEW-v0.1.`

## Expected Classification

`POLICY_APPROVAL_CONFUSION` or `COMPLIANCE_CERTIFICATION_CONFUSION`

## Expected Reconstruction Outcome

`POLICY_LAUNDERING_EXPOSED`

## What Remains Outside Fork

- Whether the policy applied.
- Whether the policy was satisfied.
- Whether compliance was determined.
- Whether the policy was current or adequate.