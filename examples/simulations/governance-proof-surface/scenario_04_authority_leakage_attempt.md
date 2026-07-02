# Scenario 04: Authority Leakage Attempt

## Purpose

This scenario tests whether Fork exposes authority leakage.

## Flow

1. A reviewer role is recorded in the authority/policy context.
2. Downstream system treats the recorded role as sufficient final authority.
3. Fork preserves the role context and the non-claim that role presence does not equal authority sufficiency.

## Recorded Context

`Vendor-risk analyst reviewed memo for preliminary triage.`

## Downstream Inference

`Vendor-risk function approved final action.`

## Expected Classification

`AUTHORITY_LEAKAGE`

## Expected Reconstruction Outcome

`AUTHORITY_LEAKAGE_EXPOSED`

## What Remains Outside Fork

- Whether the analyst had final authority.
- Whether the institution approved the action.
- Whether delegated review was sufficient.