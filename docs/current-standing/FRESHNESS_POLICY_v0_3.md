# Freshness Policy v0.3

This policy governs the structural current-standing accounting used by v0.10.

## Active base

`PROGRAM_CHANGE_ACCOUNTING_v0_3.json` begins at exact `main@734bf2cc1981a52d8b9d0c0b9eeb2aece6253f52`.

Before v0.3 active transitions are evaluated, the checker replays every recognized first-parent transition from the v0.2 coverage base `115992d750f0e893d07b61dbb6d584c87dc64d5d` through `734bf2cc1981a52d8b9d0c0b9eeb2aece6253f52` and requires exact equality with the preserved v0.2 ledger.

The preserved v0.2 file is bound by Git blob `3cd0cd35722125ca42a8fdbc6b68cc55e99a7a2d`.

## Scope

Recognized implementation prefixes remain:

- `admissions/`
- `docs/experiments/`
- `registries/`
- `receipts/`
- `schemas/`
- `tools/`

The v0.10 routing/register/checker/test changes are outside that recognized implementation scope. Therefore an empty v0.3 active transition population does not mean no repository files changed.

```text
PREDECESSOR_LEDGER_CLOSED != PREDECESSOR_LEDGER_DISCARDED
ACCOUNTING_SUCCESSOR != HISTORICAL_LEDGER_REWRITE
ZERO_ACTIVE_RECOGNIZED_TRANSITIONS != ZERO_REPOSITORY_CHANGES
ACCOUNTED_FOR != SEMANTICALLY_COMPLETE
```

This mechanism establishes bounded structural accounting only. It does not establish semantic completeness, truth, authorization, reviewer exposure, production readiness, or governance adoption.
