# Scenario 09 — Revocation Visibility / Split-State Boundary

## Scenario ID

`SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY`

## Summary

A validity-changing event exists in one system, but another system has not consumed it.

A downstream actor relies on stale, partial, or locally visible state and treats local non-awareness as current validity.

## Core invariant

```text
Revocation recorded in System A
≠ revocation visible to System B
≠ revocation consumed by System C
≠ downstream reliance resolved
```

## Systems

### System A — Revocation Source

Records a revocation, expiry, supersession, narrowing, policy update, role change, or other validity-changing event.

### System B — Intermediate State Holder

Has a local state view that may not include the revocation or validity-changing event.

### System C — Downstream Reliance Actor

Attempts to rely on the prior or locally visible state.

## Expected failure mode

`REVOCATION_VISIBILITY_GAP`

## Fork result

Fork records the revocation visibility gap and split-state boundary.

Fork can preserve where the validity-changing event was recorded, where it was not yet visible, where it was not yet consumed, what state a downstream actor relied on, and what revalidation or synchronization remained unresolved.

Fork does not decide whether the downstream actor was negligent, excused, authorized, compliant, legally sufficient, accepted, correct, or eligible to execute.

## Relationship to Scenario 08

Scenario 08 tested stale validity after a validity change.

Scenario 09 tests whether the validity change was visible, consumed, and operative across systems.
