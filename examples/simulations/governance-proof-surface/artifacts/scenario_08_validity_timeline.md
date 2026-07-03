# Scenario 08 Validity Timeline

## Timeline

```text
T1 — Prior record created
  - Claim boundary is valid only inside the recorded scope.
  - Authority context is bounded to the then-current role, policy, purpose, and time window.

T2 — Validity change occurs
  - Authority is revoked, expired, narrowed, or superseded.
  - Policy, role, evidence, purpose, or operating environment changes.

T3 — Downstream reliance attempt
  - A downstream actor attempts to rely on the T1 record as if it still establishes current authority or validity.

T4 — Fork boundary result
  - Stale-validity reliance attempt is recorded.
  - Current reliance requires revalidation.
```

## Temporal invariant

```text
valid_at(T1) does not imply valid_at(T3)
```

## Fork posture

Fork preserves the temporal boundary state. It does not decide whether the old claim was correct, whether the new state is valid, whether the revocation was proper, or whether execution is allowed.
