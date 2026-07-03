# Computed Scenario 09 Cases

This directory contains deterministic Scenario 09 state-divergence fixtures.

## Cases

```text
visibility_gap_detected
gap_closed_by_revalidation
```

Each case is evaluated by:

```text
scripts/derive_computed_scenario_09_revocation_split_state_v0_1.py
```

The checker writes derived output to each case directory and verifies it against the expected result.
