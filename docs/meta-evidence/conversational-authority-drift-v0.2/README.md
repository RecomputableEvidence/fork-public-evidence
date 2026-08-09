# Conversational Authority Drift v0.2 — PROOF-005 Correction Successor

## Standing

`CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED`

This surface is an additive successor to historical PR #84 and PR #86. It does not rewrite, rebase, merge, or invalidate either historical review result.

Historical review standing preserved:

- PR #84 @ `46fcd2c2580abd86ffbe215e6c387fee2bcb1b39`: `REPRODUCED_WITH_CORRECTIONS_REQUIRED`.
- PR #86 @ `f72ca3fad82bee068527fe63eaf1c8eba87dd698`: `REVIEW_INCONCLUSIVE`, with bounded scaffold support.

## What v0.2 corrects

The successor mechanically separates:

- attachment supply/presence from turn-specific access and later direct read;
- attributed execution reports from verified execution receipts;
- artifact content theme from declared evidentiary role;
- similar vocabulary from established scope equivalence;
- observable register from behavioral influence;
- artifact presence from contextual, chronological, parse-state, and evidentiary completeness;
- model self-report from verified mechanism;
- review activity from admission, readiness, execution, or authority.

The checker also validates control effects that were outside the v0.1 checker surface and uses a controlled event vocabulary plus `source_role` so renaming a self-report event cannot silently promote mechanism standing.

## Source-grounding boundary

The historical PR #86 meta-assessment proposed fifteen candidate families, but the historical review found the 20→15 consolidation unrecomputable because exact source spans, original instance IDs, chronology, versions, and merge lineage were not bound.

v0.2 does **not** invent those missing facts.

Every family remains:

`grounding_status = INCOMPLETE`

with empty source-span/version/chronology bindings and no canonical case IDs or finding codes. The workbook/artifact question remains:

`UNRESOLVED_ARTIFACT_EXISTENCE`

Absence is not inferred from omission.

The assessor correction event also remains explicitly `CORRECTION_BINDING_INCOMPLETE_NOT_ADMITTED` because the original statement it purports to correct is not source-addressed in the available repository surface.

## Run

```text
python tools/check_fork_cad_candidate_v0_2.py
python -m pytest -q tests/test_fork_cad_candidate_v0_2.py
```

The focused tests include mutation cases for the historical bypasses and for later promotion pressure: renamed self-report, missing provenance fields, provider/Pair-001/readiness/admission promotion, access-state collapse, execution overclaim, completeness promotion, fabricated family grounding, and artifact-absence inference.

## Progression

A green v0.2 candidate establishes only:

`CORRECTION_SUCCESSOR_CANDIDATE_READY_FOR_EXACT_HEAD_REVIEW`

It does not establish PROOF-005 admission, independent validation, empirical validation, provider execution, pilot standing, production standing, endorsement, compliance, legal sufficiency, or authority transfer.

Required order:

`PRESERVE HISTORICAL REVIEWS`
→ `CONSTRUCT CURRENT-TIP CORRECTION SUCCESSOR`
→ `EXACT-HEAD CI`
→ `BOUNDED INTERNAL REVIEW`
→ `FREEZE REVIEWABLE COORDINATE`
→ `INDEPENDENT EXTERIOR REVIEW`
→ `PRESERVE RETURN`
→ `SEPARATE SOURCE-EVIDENCE / PROOF-PACKAGING DISPOSITION`
