# Endogenous Case: Historical Validity Is Not Current Reliance Standing v0.1

**Case ID:** `FTM-ENDO-001`

**Candidate:** `FTM-CANDIDATE-2026-07-22-001`

**Standing:** `POST_BASE_ENDOGENOUS_CASE_NOT_FIXED_BASE_EVIDENCE`

**Classification:** `REPOSITORY_ENDOGENOUS_MANIFESTATION_NOT_CAUSAL_PROOF`

## Event

Claude audited the public repository at exact historical coordinate
`main@fd93d051235ec43bee925878bc916d09179b3c90`. Among its bounded findings,
Claude observed that the July 11 proof-surface state still appeared in public
status routing as current even though later governed history contained
state-changing freeze, attempt, amendment, pre-execution, provider-validation,
drift, sequence, and checksum-integrity events.

The audit is preserved at:

- `docs/exterior-observations/observations/EXTERIOR_OBSERVATION_CLAUDE_MAIN_FD93D05_REPOSITORY_AUDIT_v0_1.md`

## Preserved predecessor

The July 11 state record remains byte-identical:

- `docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json`
- SHA-256:
  `8e62fdf1adc5cacb087b8f1b2a1a1d8674521990d42b4d3897d17c49f433b098`

Its retained values are not corrected in place. The record remains a valid
historical projection at its recorded temporal closure.

## Successor reconciliation

The governed preservation lineage has a separately bound successor
projection:

- `docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json`
- governed source coordinate:
  `preservation/clean-continuance-v0.1@1241c0084900f2c60f362205525464582e57b4a7`
- succession ledger:
  `docs/state/FORK_TEMPORAL_SUCCESSION_LEDGER_v0_1.json`

The temporal-succession checker fails when a projection represented as current
is followed by a declared admitted state-changing event within its scope and
no later successor reconciles that event.

## Thesis manifestation

The case manifests the candidate thesis inside Fork's own repository history:

> Historical validity does not carry current reliance standing across an
> unreconciled state-changing event.

The failure was not loss of the historical artifact. The artifact and its
original meaning remained available. The failure was that its earlier
`current` standing survived in routing after the evidentiary conditions had
changed.

This is an endogenous architectural case supporting the distinction between:

- artifact preservation;
- validity at an earlier temporal closure;
- current evidentiary projection;
- current reliance standing; and
- authority to act.

## Fixed-base boundary

This case was filed after construction of the candidate's fixed evidence map.
It is therefore a post-base manifestation and challenge surface, not a new
`FTM-E###` entry and not evidence silently inherited into claims bound only to
`1241c008...`.

Its inclusion does not change the exact-base evidence map, establish
causality, prove generality, admit the thesis, authorize execution, or alter
Pair-001.
