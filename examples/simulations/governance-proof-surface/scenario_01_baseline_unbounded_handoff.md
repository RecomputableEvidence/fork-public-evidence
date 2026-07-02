# Scenario 01: Baseline Unbounded Handoff

## Purpose

This scenario models a vendor-risk handoff without Fork-style boundary records.

The goal is to expose how unsupported inheritance can occur when an AI-assisted artifact moves downstream without explicit handoff state.

## Participating Systems

| System | Role |
|---|---|
| System A | AI-assisted production system |
| System C | Institutional review / policy context system |
| System D | Downstream operational or decision system |
| System E | Audit / reconstruction / oversight system |

System B, the Fork boundary-record layer, is intentionally absent.

## Flow

1. System A produces an AI-assisted vendor-risk memo.
2. System C human reviewer accepts or lightly edits the memo.
3. The memo is sent to System D.
4. System D treats the memo as sufficient for downstream action.
5. System E later attempts reconstruction.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Human-reviewed status.
- Ordinary workflow notes.

## What Did Not Cross the Boundary

- Explicit non-claims.
- Authority sufficiency record.
- Policy applicability determination.
- Compliance determination.
- Revalidation requirements.
- Unresolved evidence gaps.

## Downstream Inference Attempt

System D infers:

- the vendor was approved;
- the reviewer had sufficient authority;
- the cited policy was satisfied;
- unresolved issues were resolved or irrelevant.

## Expected Failure Mode

Unsupported inheritance occurs because downstream reliance exceeds the recorded evidence.

## Reconstruction Result

Expected outcome:

`NOT_RECONSTRUCTABLE` or `PARTIALLY_RECONSTRUCTABLE_BOUNDARY`

## Non-Claims

This scenario does not prove that Fork would prevent the failure.

It establishes a baseline failure mode for later comparison.