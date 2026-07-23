# Fork Temporal Succession v0.1

## Purpose

Fork preserves historical projections without allowing their former `current`
label to silently survive later admitted state-changing events.

The July 11 record remains unchanged at:

- `docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json`

Its successor projection is:

- `docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json`

The succession ledger is:

- `docs/state/FORK_TEMPORAL_SUCCESSION_LEDGER_v0_1.json`

## Rule

For a projection `P_t` represented as current at time `t`, any later declared
and admitted state-changing event within `P_t`'s scope requires a successor
projection that:

1. has a later temporal closure;
2. names `P_t` as its predecessor;
3. reconciles every applicable later event by identifier;
4. binds the exact source bytes used for the successor; and
5. preserves `P_t` rather than rewriting it.

If those conditions are absent, the checker returns
`TEMPORAL_SUCCESSION_RECONCILIATION_REQUIRED`.

## Run

```bash
python tools/check_temporal_succession_v0_1.py --json
python -m pytest tests/test_temporal_succession_v0_1.py -q
```

## Boundary

The checker evaluates events declared in the temporal-succession ledger. It
does not infer semantic state change from arbitrary repository history and
cannot discover an omitted event. Event registration, classification, and
admission remain governance responsibilities.

A passing result does not establish truth, correctness, completeness,
causality, authority, approval, compliance, legal sufficiency, safety,
production readiness, or execution permission.
