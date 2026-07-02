# Scenario 06: Multi-System Distributed Handoff

## Purpose

This scenario tests whether Fork preserves handoff state across multiple independently accountable systems.

## Flow

1. System A produces an AI-assisted artifact.
2. System B preserves handoff state.
3. System C consumes the artifact and records constrained review context.
4. System D routes the artifact or takes downstream action.
5. System E reconstructs the transition later.

## Systems

| System | Native Responsibility | Fork Does Not Become |
|---|---|---|
| System A | Artifact production | Model evaluator |
| System B | Boundary-state preservation | Authority layer |
| System C | Institutional review context | Compliance oracle |
| System D | Routing or operation | Runtime controller |
| System E | Audit or reconstruction | Legal authority |

## Expected Result

The handoff remains inspectable across multiple hops without any system inheriting authority from another system by default.

## Expected Reconstruction Outcome

`RECONSTRUCTABLE_BOUNDARY`

Potential additional outcomes:

- `UNSUPPORTED_INHERITANCE_EXPOSED`
- `AUTHORITY_LEAKAGE_EXPOSED`
- `NON_CLAIM_LOSS_EXPOSED`

## What Remains Outside Fork

- Whether the final downstream action was correct.
- Whether governance authority was sufficient.
- Whether the institution should have acted.
- Whether compliance or legal requirements were satisfied.