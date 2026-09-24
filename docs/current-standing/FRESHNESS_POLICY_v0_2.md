# Recognized program-change accounting v0.2

This policy succeeds, but does not rewrite, [`FRESHNESS_POLICY_v0_1.md`](FRESHNESS_POLICY_v0_1.md). The active admission gate continues to run `python scripts/check_standing_freshness_v0_1.py --json`; the checker version name is retained for workflow continuity while its active accounting source advances to [`PROGRAM_CHANGE_ACCOUNTING_v0_2.json`](PROGRAM_CHANGE_ACCOUNTING_v0_2.json).

## Why the accounting base moves

v0.8 bound active accounting to PR #164. Between that coordinate and PR #178, the preserved v0.1 ledger accumulated recognized transitions for later merged research/admission work. The `Current Standing Structural Check` passed at exact main commit `115992d750f0e893d07b61dbb6d584c87dc64d5d`, establishing that the declared v0.1 structural accounting matched the recognized transition population at that coordinate.

v0.2 therefore uses PR #178 as the new active coverage base **only after** mechanically closing the predecessor ledger. The checker must:

1. load the preserved `PROGRAM_CHANGE_ACCOUNTING_v0_1.json`;
2. verify its declared Git blob identity;
3. recompute every recognized first-parent transition from the v0.1 base `4e80ee7f33ac890c4101d741cf3da93522d2fd33` through `115992d750f0e893d07b61dbb6d584c87dc64d5d`;
4. require exact equality with the preserved v0.1 transition set;
5. only then compute active transitions from the v0.2 base through current `HEAD` and the working checkout.

A base move is therefore a successor accounting event, not a deletion of earlier accounting.

## Recognition scope

The recognized prefixes remain unchanged:

- `admissions/`
- `docs/experiments/`
- `registries/`
- `receipts/`
- `schemas/`
- `tools/`

This is a declared structural recognition scope, not an exhaustive definition of program significance. Changes to routing, current-standing prose, snapshots, workflows, repository settings, external services, permissions, reviewer exposure, unmerged pull requests, and other out-of-scope surfaces may be significant without being automatically discovered by this detector.

Each active recognized transition after the v0.2 base must still be declared with exact path, before/after Git blob identity, disposition, reason, and standing reference. The accepted dispositions remain `INCORPORATED`, `EXPLICITLY_DEFERRED`, and `IN_FLIGHT`.

## v0.9 routing relation

The active standing register is [`FORK_CURRENT_WORK_REGISTER_v0_9.json`](FORK_CURRENT_WORK_REGISTER_v0_9.json), with snapshot base `115992d750f0e893d07b61dbb6d584c87dc64d5d`. The open-candidate snapshot and reviewer routes are representational surfaces outside the recognized research-object prefixes. Their exclusion from the active transition set does not mean they are semantically insignificant; it means this checker has a deliberately narrower mechanical job.

The v0.9 register also carries the earlier RLO preservation binding and the CSH/CSH-S001 non-promotion state. Those checks remain structural guardrails against accidentally converting a routing repair into a research-state promotion.

```text
PREDECESSOR_LEDGER_CLOSED != PREDECESSOR_LEDGER_DISCARDED
ACCOUNTED_FOR != SEMANTICALLY_COMPLETE
PRESERVATION != SYNCHRONIZATION
PRESERVED != CURRENTLY_INTERPRETED
CURRENTLY_INTERPRETED != CURRENTLY_REPRESENTATIVE
```
