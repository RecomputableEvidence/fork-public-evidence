# Fork Current Work Register v0.9

Snapshot: 2026-09-24. Repository coordinate: `115992d750f0e893d07b61dbb6d584c87dc64d5d` (merge of PR #178). Predecessor: [v0.8](FORK_CURRENT_WORK_REGISTER_v0_8.md), preserved unchanged. [Machine-readable overlay](FORK_CURRENT_WORK_REGISTER_v0_9.json). [Open-candidate snapshot](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.md).

This successor is a **representational synchronization**. It closes the umbrella register's lag from the v0.8 PR #164 horizon through the exact PR #178 main coordinate without rewriting the underlying research objects, admissions, failures, review returns, or unresolved gates.

## Current bounded route

| Object/event | Bounded standing at this coordinate | Next gate |
| --- | --- | --- |
| CSH v0.1 | Baseline remains blocked by receiver-platform retirement; no continuation or retroactive completion through S001 | None inferred from successor activity |
| CSH-S001 v0.1 / PR #165 | Measurement/coding and execution-record semantics remain frozen; exact packets remain bound; hosted access remains blocked; receiver registry and run order remain unfrozen; corpus execution not established | Successful neutral hosted access, then receiver and exact run-order freeze before corpus-bearing execution |
| LS-MDRC-002 / PR #162 | Original PR remains open/unmerged; PR #167 preserves receipt-digest, manifest-binding, and population discrepancies and does not admit or qualify the freeze; PR #168 is evidence-only follow-up | Historical-byte recovery or a separately named successor; no automatic continuation |
| Fork II KERNEL-002 v0.1 | Bounded research release admitted through PR #173 after preserved pre-repair failure, control freeze, successor-only repair, combined execution, and separate recomputation | Any successor work must retain the release's declared non-claims and separate identity |
| Five-Layer Run 005 / PR #178 | `EXTERNAL_ADJUDICATION_DISPATCH_PREPARED_NOT_RETURNED`; Phase A/B dispatch exists for preselected seams M12/M18 and M14; no repository external result claimed; Stage 3 unchanged; synthetic lane unopened | Preserve external Phase A return as a separate repository object before any reconciliation effect or synthetic-lane opening |

## Why v0.9 exists

The repository had become intentionally uneven: `CURRENT_STANDING.md` already carried later Fork II standing notes while the umbrella register still ended at PR #164. v0.9 records that unevenness as historical fact and then restores a single reviewer route through PR #178. It does not pretend the lag never existed.

The predecessor v0.8 remains the exact September 23 representation of the CSH/CSH-S001 state. The RLO observation that motivated the earlier freshness repair also remains byte-bound and preserved. v0.9 carries those constraints forward rather than replacing their history.

## Open candidates

At `2026-09-24T23:47:00Z`, GitHub reported **18 open pull requests**. Their original PR descriptions are not automatically their current standing: later preservation, exterior review, correction, admission, or reconciliation records may narrow what an open PR now represents.

The dated [open-candidate snapshot](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.md) therefore separates active gates, exterior-review dependencies, evidence-only reconciliation, historical holds, superseded-but-preserved candidates, proof-packaging review, and intentionally unresolved coordinates.

Two cross-branch distinctions are especially important:

- **PR #65 / PROOF-002:** PR #123 admitted the bounded recomputation return as source evidence on `preservation/clean-continuance-v0.1`; direct merge of #65 was not selected and proof packaging remains not admitted.
- **PR #100 / PROOF-004:** PR #123 admitted the bounded deterministic-simulation recomputation return as source evidence on the preservation branch; direct merge was not selected, live adapters remain closed, and proof packaging remains not admitted.

Thus neither PR should be represented simply as “review pending,” but neither preservation-branch source-evidence admission is a `main` proof-packaging admission.

## Change-accounting transition

The predecessor accounting file, [`PROGRAM_CHANGE_ACCOUNTING_v0_1.json`](PROGRAM_CHANGE_ACCOUNTING_v0_1.json), remains unchanged. It was structurally checked at the exact PR #178 main coordinate by the successful `Current Standing Structural Check` run on that commit. v0.9 starts a successor ledger, [`PROGRAM_CHANGE_ACCOUNTING_v0_2.json`](PROGRAM_CHANGE_ACCOUNTING_v0_2.json), whose active coverage base is the PR #178 merge commit.

The v0.2 checker does not discard the old ledger: it recomputes recognized first-parent transitions from the v0.1 PR #164 base through the PR #178 closing coordinate and requires an exact match with the preserved v0.1 accounting before it evaluates post-PR-178 transitions. Moving the coverage base is therefore conditional on predecessor accounting closure rather than a silent reset.

See [Freshness Policy v0.2](FRESHNESS_POLICY_v0_2.md).

## Boundary

```text
PRESERVATION != SYNCHRONIZATION
PRESERVED != CURRENTLY_INTERPRETED
CURRENTLY_INTERPRETED != CURRENTLY_REPRESENTATIVE
OPEN != CURRENT_STANDING
SOURCE_EVIDENCE_ADMITTED != PROOF_PACKAGING_ADMITTED
OFF_REPOSITORY_RETURN != REPOSITORY_STANDING
ACCOUNTED_FOR != SEMANTICALLY_COMPLETE
```

This register changes no research-object bytes and makes no new empirical finding. It does not establish truth, correctness, completeness, compliance, legal sufficiency, production readiness, deployment authority, institutional approval, or global independence.
