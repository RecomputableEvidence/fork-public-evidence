# AHI Simulation v0.1.10 â€” Scenario 09 Revocation Visibility / Split-State Boundary

Scenario 09 adds split-state visibility coverage to the AHI simulation proof surface.

Failure mode:

```text
REVOCATION_VISIBILITY_GAP
```

Core invariant:

```text
recorded_in_A does not imply visible_in_B
visible_in_B does not imply consumed_by_C
not_visible_locally does not imply still_valid_currently
```

Fork records the revocation visibility gap and preserves required visibility, consumption, synchronization, or current revalidation.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, judge correctness, determine negligence, or determine excuse.
