# Fork Current Standing — Reviewer Entry Point

**Historical closure snapshot:** 2026-09-09  
**Historical closure base:** `1663674949ec90ff7e8878c27bea9dbde97096d7`  
**Closure merge:** `cf5c617987a7f1fcde534f46daada42976583b48` via PR `#143`  
**Current successor overlay:** v0.9, 2026-09-24, synchronized through `115992d750f0e893d07b61dbb6d584c87dc64d5d` (PR #178)  
**Preserved predecessor:** v0.8, 2026-09-23, admitted CSH evidence through PR #164  
**Standing:** representational synchronization only; CSH baseline blocked, CSH-S001 hosted access blocked, Fork II bounded release admitted through its own record, LS-MDRC-002 reconciliation preserved without freeze qualification, and Five-Layer Run 005 external adjudication dispatched but not returned at the repository coordinate.  
**Scope:** interpretation and routing of repository evidence; no underlying artifact is promoted by inclusion here.

This directory is the reviewer entry point for reconstructing what Fork presently contains, what has been executed, what failed, what remains provisional, what is frozen, what awaits independent review, what was intentionally stopped, and what has subsequently been admitted under repository discipline.

## Governing rule

```text
ARTIFACT PRESENT
!= CURRENTLY RELIED UPON
!= EXECUTED
!= PASSED
!= FAILED
!= FROZEN
!= INDEPENDENTLY REVIEWED
!= REPOSITORY ADMITTED AS BASELINE
!= COMMERCIALLY QUALIFIED
!= GOVERNANCE ADOPTED
```

Likewise:

```text
ADJACENT IN REPOSITORY
!= DERIVED FROM
!= EQUIVALENT TO
!= ENDORSED BY
!= VALIDATED BY
!= STRONGER IN STANDING
```

And for the present synchronization:

```text
OPEN != CURRENT_STANDING
SOURCE_EVIDENCE_ADMITTED != PROOF_PACKAGING_ADMITTED
PRESERVATION_BRANCH_ADMISSION != MAIN_BRANCH_ADMISSION
OFF_REPOSITORY_RETURN != REPOSITORY_STANDING
ACCOUNTED_FOR != SEMANTICALLY_COMPLETE
```

Current overlay: [v0.9](FORK_CURRENT_WORK_REGISTER_v0_9.md) / [JSON](FORK_CURRENT_WORK_REGISTER_v0_9.json). [Open-candidate snapshot](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.md) records the 18 open PRs at the dated observation coordinate without modifying them. Preserved v0.8: [Markdown](FORK_CURRENT_WORK_REGISTER_v0_8.md) / [JSON](FORK_CURRENT_WORK_REGISTER_v0_8.json). Preserved v0.7: [Markdown](FORK_CURRENT_WORK_REGISTER_v0_7.md) / [JSON](FORK_CURRENT_WORK_REGISTER_v0_7.json). Preserved v0.6 (post-execution reconciliation): [v0.6](FORK_CURRENT_WORK_REGISTER_v0_6.md) / [JSON](FORK_CURRENT_WORK_REGISTER_v0_6.json). Preserved v0.5 (preflight): [v0.5](FORK_CURRENT_WORK_REGISTER_v0_5.md) / [JSON](FORK_CURRENT_WORK_REGISTER_v0_5.json).

## Current synchronization boundaries

- PR #165 remains open hosted-access context. Recorded 429 responses are access observations only; receiver registry and run order remain unfrozen and no CSH corpus execution is established.
- PR #162 remains open and unmerged. PR #167 preserves freeze-identity discrepancies without admitting or qualifying the original package; PR #168 is an evidence-only reconciliation follow-up.
- PR #123's source-evidence admission for #65 and #100 occurred on `preservation/clean-continuance-v0.1`. It does not become `main` proof-packaging admission by routing adjacency.
- Fork II KERNEL-002 v0.1 is admitted only within the bounded release standing recorded in `FORK_II_RELEASE_ADMISSION_20260923.md`.
- Run 005 is `EXTERNAL_ADJUDICATION_DISPATCH_PREPARED_NOT_RETURNED`: no external return is repository-preserved/admitted at the PR #178 coordinate and the synthetic lane remains unopened.
- [`PROGRAM_CHANGE_ACCOUNTING_v0_2.json`](PROGRAM_CHANGE_ACCOUNTING_v0_2.json) advances the active accounting base only after mechanically closing the preserved v0.1 ledger through PR #178. See [`FRESHNESS_POLICY_v0_2.md`](FRESHNESS_POLICY_v0_2.md).

## Read preserved sources in this order

1. [`FORK_CURRENT_WORK_REGISTER_v0_9.md`](FORK_CURRENT_WORK_REGISTER_v0_9.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_9.json) — current representational synchronization through PR #178.
2. [`OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.md`](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.md) / [`json`](OPEN_CANDIDATE_STANDING_SNAPSHOT_20260924_v0_1.json) — dated 18-entry open-candidate snapshot.
3. [`FORK_CURRENT_WORK_REGISTER_v0_8.md`](FORK_CURRENT_WORK_REGISTER_v0_8.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_8.json) — preserved CSH/CSH-S001 predecessor overlay.
4. [`FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md`](FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md) — status vocabulary and interpretation rules.
5. [`FORK_CURRENT_WORK_REGISTER_v0_4.md`](FORK_CURRENT_WORK_REGISTER_v0_4.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_4.json) — preserved UEM Epoch 010 successor overlay; additive to v0.3.
6. [`UEM_v0_1_EPOCH_010_CRII_ADMISSION_MERGE_RECEIPT_2026_09_17.md`](UEM_v0_1_EPOCH_010_CRII_ADMISSION_MERGE_RECEIPT_2026_09_17.md) — bounded UEM Epoch 010 admission event.
7. [`FORK_CURRENT_WORK_REGISTER_v0_3.md`](FORK_CURRENT_WORK_REGISTER_v0_3.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_3.json) — preserved Lens Shift overlay.
8. [`LENS_SHIFT_v0_1_BLIND_EPOCH_003_ADMISSION_MERGE_RECEIPT_2026_09_17.md`](LENS_SHIFT_v0_1_BLIND_EPOCH_003_ADMISSION_MERGE_RECEIPT_2026_09_17.md) — bounded Lens Shift v0.1 admission event.
9. [`FORK_CURRENT_WORK_REGISTER_v0_2.md`](FORK_CURRENT_WORK_REGISTER_v0_2.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_2.json) — preserved September 15 overlay.
10. [`FORK_VOS_E002_ADMISSION_MERGE_RECEIPT_2026_09_15.md`](FORK_VOS_E002_ADMISSION_MERGE_RECEIPT_2026_09_15.md) — bounded E002 admission event.
11. [`FORK_CURRENT_WORK_REGISTER_v0_1.md`](FORK_CURRENT_WORK_REGISTER_v0_1.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_1.json) — preserved September 9 predecessor population.
12. [`FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md`](FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md) — routes reviewers without collapsing purposes.
13. [`FORK_CLOSURE_PASS_MERGE_RECEIPT_2026_09_09.md`](FORK_CLOSURE_PASS_MERGE_RECEIPT_2026_09_09.md) — admission of the original current-standing layer; not underlying-object byte admission.

## Current repository versus current program

The standing layer distinguishes:

```text
PROGRAM_OBJECT_EXISTS
!= ARTIFACT_BYTES_PRESENT_ON_CURRENT_REPOSITORY_BRANCH
```

The admitted successor records make material boundaries explicit:

```text
TERMINAL_NATIVE_RECORDS_ADMITTED
!= DEVELOPMENT_OR_PREDECESSOR_PACKAGE_BYTES_ADMITTED
!= BINARY_SUPPORT_BYTES_ADMITTED
!= RAW_CAPTURE_ARCHIVES_ADMITTED
!= INDEPENDENT_RAW_RECOMPUTATION
```

For UEM Epoch 010 specifically:

```text
BOUNDED_CRII_EPOCH_010_PASS
!= UNIVERSAL_UEM_CORRECTNESS

VERIFIER_RECEIPT_REPLAY_PASS
!= INDEPENDENT_EXECUTOR_FROM_FIXTURES_REPRODUCTION

MANIFEST_BOUND_PRE_EXPOSURE_RECORD
!= TRUSTED_TIMESTAMP_PROOF_OF_PRE_EXPOSURE_CHRONOLOGY

EPOCH_010_PASS
!= INDEPENDENT_SURFACE_GENERALIZATION
!= EPOCH_011_GENERALIZATION
```

For Lens Shift specifically:

```text
BLIND_EPOCH_003_SCOPE_QUALIFIED
!= UNIVERSALLY_VALIDATED

OPERATIONALLY_ATTESTED_BLINDNESS
!= CRYPTOGRAPHIC_PROOF_OF_NO_PRIOR_EXPOSURE

24_OF_24
!= EXHAUSTIVE_PROTOCOL_PROOF
```

Objects not changed by the v0.9 delta retain their last recorded predecessor-register standing; this is not a fresh check of off-repository state. The v0.1–v0.8 records remain historical evidence of what was represented at their own snapshot coordinates; v0.9 does not mutate them.

## Current top-level posture

Fork remains a research-grade evidence-boundary and recomputation program. Passing structural checks, successful bounded experiments, external observations, commercial materials, repository admission, or inclusion in a current-standing layer do not establish truth, compliance, legal sufficiency, production readiness, safety, authorization, institutional approval, procurement approval, or justified downstream reliance.

The repository's purpose is preservation and examination. It is not an authority oracle.
