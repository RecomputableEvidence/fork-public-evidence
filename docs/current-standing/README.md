# Fork Current Standing — Reviewer Entry Point

**Closure snapshot:** 2026-09-09  
**Closure base:** `1663674949ec90ff7e8878c27bea9dbde97096d7`  
**Standing:** `REPOSITORY_STANDING_INDEX_CANDIDATE`  
**Scope:** interpretation and routing of repository evidence; no underlying artifact is promoted by inclusion here.

This directory is the current reviewer entry point for reconstructing what Fork presently contains, what has been executed, what failed, what remains provisional, what is frozen, what awaits independent review, what was intentionally stopped, and what next evidence-bearing gate remains open.

It exists because the repository serves several legitimate purposes at once: research record, proof surface, failure-mode corpus, Recomputable Evidence implementation surface, interoperability work, longitudinal evidence, pilot/procurement material, and adjacent NGAST consultation material. Those purposes may share artifacts without sharing standing.

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

A reviewer should therefore determine an artifact's standing from its own record and from the current work register, not from directory proximity, naming similarity, later references, or successful execution of another artifact.

## Read in this order

1. [`FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md`](FORK_STANDING_NONINHERITANCE_CONTRACT_v0_1.md) — status vocabulary and interpretation rules.
2. [`FORK_CURRENT_WORK_REGISTER_v0_1.md`](FORK_CURRENT_WORK_REGISTER_v0_1.md) — human-readable current program state.
3. [`FORK_CURRENT_WORK_REGISTER_v0_1.json`](FORK_CURRENT_WORK_REGISTER_v0_1.json) — machine-readable counterpart.
4. [`FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md`](FORK_REPOSITORY_PURPOSE_ROUTING_v0_1.md) — routes reviewers to the appropriate repository surface without collapsing purposes.
5. [`FORK_CLOSURE_PASS_RECEIPT_2026_09_09.md`](FORK_CLOSURE_PASS_RECEIPT_2026_09_09.md) — what this closure pass changed and, equally important, what it did not change.

## Historical artifacts remain historical

This closure pass does not move, rewrite, delete, or retrospectively strengthen existing versioned research, simulation, review, reconstruction, commercial, interoperability, or proof-surface artifacts. Historical versions remain evidence of what existed at their own time and scope.

A later status record may say that an older artifact is `SUPERSEDED`, `HISTORICAL`, `STOPPED`, `REPAIR_REQUIRED`, or `NO_LONGER_CURRENT`. That later classification does not alter the historical bytes or retroactively change what the older artifact established at the time.

## Current repository versus current program

The register explicitly distinguishes:

```text
PROGRAM_OBJECT_EXISTS
!= ARTIFACT_BYTES_PRESENT_ON_CURRENT_REPOSITORY_BRANCH
```

Some current research objects were executed or frozen outside the present repository tree and are therefore registered as `PENDING_BYTE_ADMISSION`. Their existence and standing may be reported here without pretending that their canonical bytes are already available from this branch.

That state is intentional and temporary. It permits a reviewer to reconstruct the program's current shape while preserving the difference between a status record and admission of the underlying evidence package.

## Current top-level posture

Fork remains a research-grade evidence-boundary and recomputation program. Passing structural checks, successful bounded experiments, external observations, commercial materials, or inclusion in this repository do not establish truth, compliance, legal sufficiency, production readiness, safety, authorization, institutional approval, procurement approval, or justified downstream reliance.

The repository's purpose is preservation and examination. It is not an authority oracle.