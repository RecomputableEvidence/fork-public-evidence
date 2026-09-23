# Current Standing

For the repository-wide current program state, begin here:

Current standing: [v0.8](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_8.md) / [JSON](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_8.json). Admitted evidence through `4e80ee7f33ac890c4101d741cf3da93522d2fd33` (PR #164). CSH baseline blocked; CSH-S001 measurement/coding and execution-record semantics frozen, exact packets bound, hosted access blocked; receiver registry and run order unfrozen. PR #165 is open preflight context at the observation coordinate.

## Current-state routing clarification

`CURRENT_STANDING.md` and the v0.8 register above are the current program-standing route for this coordinate.

Earlier proof-surface state files, generated summaries, and embedded README status blocks retain their own historical coordinates. They do **not** become current merely because they remain present in the repository.

For machine-readable routing, see:

- [`docs/state/CURRENT_STATE_ROUTING_v0_1.json`](docs/state/CURRENT_STATE_ROUTING_v0_1.json)

The July proof-state snapshot remains preserved unchanged. Its historical `not_started` CSH state must not be read as superseding the later September execution/reconciliation record.

A separately named successor, `CSH-S001-v0.1`, has admitted measurement/coding and execution-record freezes. The full experiment is not frozen or executed by those narrower freezes: G06, G07, G08, and G11 remain unsatisfied. It is not a continuation or retroactive completion of CSH v0.1.

[RLO-001](docs/observations/FORK-REPRESENTATIONAL-LATENCY-OBSERVATION-001/v0.1/README.md) preserves the discrepancy before this repair. [Freshness accounting](docs/current-standing/FRESHNESS_POLICY_v0_1.md) detects unaccounted changes within its declared scope.

- Preserved v0.7: [Markdown](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_7.md) / [JSON](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_7.json)

- [`docs/current-standing/README.md`](docs/current-standing/README.md)
- Preserved v0.6 (2026-09-21 post-execution reconciliation): [`FORK_CURRENT_WORK_REGISTER_v0_6.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_6.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_6.json)
- Preserved v0.5 (2026-09-21 preflight): [`FORK_CURRENT_WORK_REGISTER_v0_5.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_5.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_5.json)
- Preserved September 17 UEM overlay: [`FORK_CURRENT_WORK_REGISTER_v0_4.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_4.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_4.json)
- Preserved September 17 Lens Shift overlay: [`FORK_CURRENT_WORK_REGISTER_v0_3.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_3.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_3.json)
- Preserved September 15 overlay: [`FORK_CURRENT_WORK_REGISTER_v0_2.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_2.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_2.json)
- Historical September 9 snapshot: [`FORK_CURRENT_WORK_REGISTER_v0_1.md`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_1.md) / [`json`](docs/current-standing/FORK_CURRENT_WORK_REGISTER_v0_1.json)

The v0.8 overlay incorporates PR #163/#164 and separates PR #165 open context. Historical v0.1–v0.7 and underlying research artifacts remain unchanged.

That current-standing layer reports what exists, what was executed, what failed or produced no scorable result, what remains provisional, what is frozen, what awaits independence, what was intentionally stopped, what has since been repository-admitted, and the next evidence-bearing gate.

It is an interpretation and routing layer only.

```text
INDEXED HERE
!= VALIDATED
!= FROZEN
!= INDEPENDENTLY REVIEWED
!= COMMERCIALLY QUALIFIED
!= GOVERNANCE ADOPTED
```

Likewise, byte admission and replay have their own boundaries:

```text
TERMINAL_NATIVE_RECORDS_ADMITTED
!= LARGE_PREDECESSOR_OR_SUPPORT_ARCHIVES_ADMITTED
!= INDEPENDENT_EXECUTOR_FROM_FIXTURES_REPRODUCTION

VERIFIER_RECEIPT_REPLAY_PASS
!= UNIVERSAL_UEM_CORRECTNESS
!= INDEPENDENT_SURFACE_GENERALIZATION
```

Existing historical, proof, research, review, reconstruction, interoperability, simulation, commercial, and admitted empirical artifacts retain their own scope and standing.
