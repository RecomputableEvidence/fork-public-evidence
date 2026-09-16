# Fork Current Standing — Reviewer Entry Point

**Historical closure snapshot:** 2026-09-09  
**Historical closure base:** `1663674949ec90ff7e8878c27bea9dbde97096d7`  
**Closure merge:** `cf5c617987a7f1fcde534f46daada42976583b48` via PR `#143`  
**Current successor overlay:** 2026-09-15, based on `73228007910f0e4781005133e9a4e9484fd2969a`  
**Standing:** `REPOSITORY_STANDING_INDEX_ADMITTED_WITH_SUCCESSOR_OVERLAY`  
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

## Read in this order

1. [`FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md`](FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md) — status vocabulary and interpretation rules.
2. [`FORK_CURRENT_WORK_REGISTER_v0_2.md`](FORK_CURRENT_WORK_REGISTER_v0_2.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_2.json) — current successor overlay; additive to the predecessor.
3. [`FORK_VOS_E002_ADMISSION_MERGE_RECEIPT_2026_09_15.md`](FORK_VOS_E002_ADMISSION_MERGE_RECEIPT_2026_09_15.md) — bounded E002 admission event.
4. [`FORK_CURRENT_WORK_REGISTER_v0_1.md`](FORK_CURRENT_WORK_REGISTER_v0_1.md) / [`json`](FORK_CURRENT_WORK_REGISTER_v0_1.json) — preserved September 9 predecessor population.
5. [`FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md`](FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md) — routes reviewers without collapsing purposes.
6. [`FORK_CLOSURE_PASS_MERGE_RECEIPT_2026_09_09.md`](FORK_CLOSURE_PASS_MERGE_RECEIPT_2026_09_09.md) — admission of the original current-standing layer; not underlying-object byte admission.

## Current repository versus current program

The standing layer distinguishes:

```text
PROGRAM_OBJECT_EXISTS
!= ARTIFACT_BYTES_PRESENT_ON_CURRENT_REPOSITORY_BRANCH
```

The E002 successor makes the material distinction more explicit:

```text
TERMINAL_NATIVE_RECORDS_ADMITTED
!= DEVELOPMENT_PACKAGE_BYTES_ADMITTED
!= BINARY_SUPPORT_BYTES_ADMITTED
!= RAW_CAPTURE_ARCHIVES_ADMITTED
!= INDEPENDENT_RAW_RECOMPUTATION
```

Objects not changed by the v0.2 delta retain their predecessor-register standing. The v0.1 record remains historical evidence of what was reported at its own snapshot coordinate; the v0.2 overlay does not mutate it.

## Current top-level posture

Fork remains a research-grade evidence-boundary and recomputation program. Passing structural checks, successful bounded experiments, external observations, commercial materials, repository admission, or inclusion in a current-standing layer do not establish truth, compliance, legal sufficiency, production readiness, safety, authorization, institutional approval, procurement approval, or justified downstream reliance.

The repository's purpose is preservation and examination. It is not an authority oracle.
