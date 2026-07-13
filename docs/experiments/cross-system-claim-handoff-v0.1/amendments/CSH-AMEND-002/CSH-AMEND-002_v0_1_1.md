# CSH-AMEND-002 - Execution-State Separation and Pair-001 Preservation

Status: **FINAL**
Amendment class: **instrumentation repair**
Experiment: `cross_system_claim_handoff_v0_1`
Patch version: `v0.1.1`

## Defect

The immutable v0.1 experiment configuration represented receiver execution as not started, while provider requests had occurred and terminal records had been preserved for `CSH-RUN-001` and `CSH-RUN-002`. The defect is not that either observed attempt was unfavorable. The defect is that mutable execution state was represented inside, or derived from, an immutable semantic/configuration freeze.

## Preserved affected attempts

- `CSH-RUN-001` is preserved as the original HTTP 200 attempt.
- `CSH-RUN-002` is preserved as the original HTTP 429 attempt.
- Their existing `exact-request.json`, `execution-metadata.json`, and `raw-provider-response.json` files remain at their original paths and are bound by `ORIGINAL_ATTEMPT_SEAL_v0_1_1.json`.
- Neither attempt is replaced, corrected, superseded, deleted, or retroactively reclassified by this amendment.

An HTTP status is an execution observation. It is not, by itself, a semantic content finding or an experimental outcome.

## Authorized repair

This amendment authorizes only the following instrumentation changes:

1. Create a separate mutable execution-state record with append-only transition history.
2. Add a v0.1.1 execution checker, schema, fixtures, and regression tests.
3. Integrate the v0.1.1 checker into the existing verifier and CI workflows.
4. Create an instrumentation-only freeze and release anchor.
5. Repeat only the two affected Pair-001 units after the patch is committed, pushed, and CI-green.
6. Use new linked run identifiers for every repeated attempt.
7. File a bounded execution-instrumentation result that preserves original and repeated attempts separately.

## Prohibited changes

This amendment does not authorize any change to:

- the v0.1 hypothesis;
- scenario or corpus meaning;
- frozen prompt bytes;
- handoff-state artifacts;
- receiver identity, version, parameters, or access path;
- scoring, classification, or interpretation rules;
- original run identifiers or original attempt bytes.

A substantive change to any of those surfaces requires a new experiment version rather than v0.1.1.

## Repetition rule

Pair-001 may be repeated only after the instrumentation patch and its release anchor are published and the required CI workflows are green. Repeated runs must:

- use new run identifiers;
- identify the linked original run;
- preserve an exact-request digest equal to the corresponding original request;
- write to new directories;
- preserve every terminal outcome, including another provider error or unavailable execution;
- remain separate from the original attempts.

## Bounded interpretation

This amendment establishes a repair and evidence-preservation procedure. It does not establish the CSH hypothesis, semantic correctness, truth, approval, compliance, legal sufficiency, safety, production readiness, endorsement, certification, or institutional authority.
