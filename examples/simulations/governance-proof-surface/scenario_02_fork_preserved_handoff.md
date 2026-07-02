# Scenario 02: Fork-Preserved Handoff

## Purpose

This scenario models the same vendor-risk handoff with Fork-style boundary records.

The goal is to test whether explicit handoff-state records make claim scope, non-claims, authority context, unresolved state, and revalidation requirements inspectable.

## Participating Systems

| System | Role |
|---|---|
| System A | AI-assisted production system |
| System B | Fork boundary-record layer |
| System C | Institutional review / policy context system |
| System D | Downstream operational or decision system |
| System E | Audit / reconstruction / oversight system |

## Flow

1. System A produces an AI-assisted vendor-risk memo.
2. System C human reviewer accepts or modifies the memo.
3. System B records handoff state.
4. System D receives the memo and the bounded handoff record.
5. System E later reconstructs the handoff.

## Fork Records

Expected artifacts:

- Claim Boundary Contract;
- Boundary Delta Record;
- Claim Consumption Event;
- System Mapping Receipt;
- Authority Policy Context;
- Non-Claims Panel.

## What Crossed the Boundary

- AI-assisted vendor-risk memo.
- Recorded claim scope.
- Evidence references.
- Authority and policy context.
- Non-claims.
- Unresolved state.
- Revalidation requirements.

## What Did Not Cross the Boundary

- Final approval authority.
- Compliance determination.
- Legal sufficiency.
- Production readiness.
- Factual correctness guarantee.
- Institutional authorization.

## Downstream Inference Attempt

System D attempts to infer that the vendor was approved for onboarding.

## Expected Fork Behavior

Fork does not block the inference.

Fork exposes that the inference exceeds recorded claim scope unless supported by separate authority and evidence.

## Reconstruction Result

Expected outcome:

`UNSUPPORTED_INHERITANCE_EXPOSED`

## Non-Claims

This scenario does not establish that the vendor-risk decision was correct.

It tests whether the handoff boundary is reconstructable.