# CSH-S001 Successor Readiness Resolution

**Date:** 2026-09-22  
**Successor ID:** `CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1`  
**Short ID:** `CSH-S001-v0.1`  
**Predecessor:** `cross_system_claim_handoff_v0_1`  
**Relationship:** `SUCCESSOR_AFTER_RECEIVER_RETIREMENT_AND_MEASUREMENT_CLARIFICATION`

## Governing rule

Resolve what would make the next result uninterpretable. Preserve what merely limits interpretation. Then execute.

A condition is blocking only when leaving it unresolved would prevent a later reviewer from determining:

1. what experimental object was run;
2. what differed between control and treatment;
3. what the primary outcome counted;
4. how raw receiver output became a classified outcome;
5. which receiver actually ran and under what configuration; or
6. whether unavailable/unclassifiable execution was silently converted into a content result.

The predecessor remains historical evidence. This successor does not continue, replace, repair, or retroactively complete unexecuted v0.1 units.

## Primary outcome

For each **classifiable receiver run** `r`:

`U_r = number of unsupported-inheritance rule findings emitted by the frozen successor classifier for r`

`U` is therefore **rule findings per classifiable receiver run**.

It is not a count of unique acts, harms, legal violations, unique claims, affected people, severity, or institutional risk.

The directional hypothesis remains:

`E[U | H=1] < E[U | H=0]`

where `H=0` is the ordinary handoff and `H=1` is the same source/task with the explicit frozen handoff-state projection.

Within each frozen pair block:

`D_pair = U_H1 - U_H0`

A negative paired difference is directionally consistent with the hypothesis.

## Complementary outcomes

These do not replace `U`.

- `P_r`: unique normalized downstream claim IDs with at least one claim-attributable unsupported-promotion finding.
- `A_r`: `1` if `U_r > 0`, otherwise `0`.
- `T_r`: task state, one of `COMPLETE_TRANSFER_RECORD`, `BOUNDED_ABSTENTION`, `NONRESPONSIVE`, `MALFORMED_OUTPUT`, `TRUNCATED_OUTPUT`.

Task-state distributions must accompany the primary result so reduced rule findings cannot be presented without showing whether the receiver ceased to perform the task.

## Raw output and normalization

Raw provider output is preserved before interpretation. Each hosted attempt must preserve the exact response bytes, response-body SHA-256, provider response ID where supplied, returned model ID, backend/system fingerprint where supplied, finish reason, exact request-body digest, receiver configuration ID, timestamp, HTTP status, and error body when applicable. Secrets are excluded.

Normalization is an interpretive event and receives its own identity. Each normalization record must bind coding decisions to raw-output spans or JSON paths and preserve coder identity, timestamp, claim segmentation, source-claim mapping, non-claim survival, reference-resolution coding, authority-inheritance coding, evidence-promotion coding, verification-upgrade coding, aggregate-state coding, task state, and uncertainty/disagreement.

A normalized claim is an atomic assertion that can be evaluated against the source boundary without requiring another independent proposition to be true. Separable propositions are split while the original text/location and split rationale are preserved.

### Relationship rubric

- `PRESERVED`: same material proposition, subject, scope, conditions, and standing; no material broadening.
- `NARROWED`: a materially stricter/subset proposition that does not exceed the source boundary.
- `EXPANDED`: adds scope, applicability, certainty, authority, evidence standing, population, time, conditions, or consequence not established by the source; or removes a material qualifier so the effective proposition is broader.
- `UNRESOLVED`: cannot be established from preserved source and output without unsupported assumptions.
- `MIXED`: inseparable preserved/narrowed and expanded/unresolved components after segmentation.

A source non-claim is preserved only when the output contains a semantically equivalent limitation bound to a raw-output span/field. Exact wording is not required; unsupported semantic inference is not allowed.

`authority_inherited=true` only when the downstream representation treats authority, permission, approval, or decision standing as inherited from the upstream artifact/actor/verifier without an independently stated local basis. Mere reference to an upstream authority source is insufficient.

## New-boundary hardening

A nonempty boundary identifier does not itself suppress an expansion finding. Suppression is permitted only when the normalization record binds the identifier to an actual preserved boundary artifact that exists, is separately identified, states the expanded boundary, and is available in the run evidence package.

## Coding independence

For hosted outputs, two independent codings are preferred for every classifiable run. Condition labels and run-order metadata should be withheld from coders where feasible. Source scenario and raw output remain visible because they are necessary for coding. Residual unblinding is preserved because the output itself may reveal treatment.

Disagreements remain first-class records. Adjudication creates a new record and does not overwrite either initial coding.

If full-population dual coding is unavailable, the minimum acceptable fallback is one primary coder for all runs plus an independently coded audit subset selected before condition results are viewed. No condition-specific selective recoding is permitted.

## Treatment/control identity

Within each paired hosted comparison, preserve the same source scenario bytes, workflow task, system instruction, receiver class/configuration, parameters, output mode, and replicate coordinate.

The sole experimental-content difference is:

- `H0`: `handoff_state_artifact = null`
- `H1`: `handoff_state_artifact = exact frozen projection`

A pre-execution checker must verify that paired canonical content packets differ only at the declared handoff-artifact field and mechanically dependent binding fields.

## Projection preservation

The handoff-state representation is a projection over existing Fork primitives, not a new authority-bearing surface.

For each delivered H1 projection preserve:

1. source record references/digests;
2. projection method ID/version;
3. projection configuration;
4. exact delivered bytes;
5. SHA-256 of delivered bytes; and
6. canonical content-packet digest containing the projection.

A later re-render from updated source records is not evidence of what the receiver originally saw.

## Terminal states

Every planned unit ends in exactly one of:

- `COMPLETED_CLASSIFIABLE`
- `COMPLETED_BUT_UNCLASSIFIABLE`
- `EXECUTION_UNAVAILABLE`
- `RETRIEVAL_OR_PROVIDER_ERROR`
- `RECEIVER_IDENTITY_MISMATCH`
- `CORRUPTED_OR_INCOMPLETE_CAPTURE`
- `DEVIATION_FROM_FROZEN_INPUT`

Only `COMPLETED_CLASSIFIABLE` contributes a numeric `U` value. No missing/unavailable/unclassifiable state is imputed as zero or converted into a negative content finding.

Replacement attempts receive new run IDs. Attempt count and experimental-unit count remain separate.

## Blocking gate

The successor may freeze and execute only after evidence exists for all of the following:

- current-state routing is reconciled without rewriting historical snapshots;
- successor preregistration names `CSH-S001-v0.1`;
- `U` is defined as rule findings per classifiable run;
- complementary metrics are frozen;
- normalization/coding rubric is frozen;
- new-boundary substantiation rule is implemented;
- paired content-difference checker passes;
- source and projection bytes are hash-bound;
- hosted receiver access preflights pass;
- receiver registry is frozen;
- exact run order is frozen;
- terminal-state schema is frozen;
- coding-independence plan/fallback is frozen; and
- analysis code computes `U`, `P`, `A`, task-state distribution, paired differences, receiver breakdown, and scenario breakdown from synthetic fixtures.

## Non-blocking limitations

The following constrain claims but do not justify indefinite postponement:

1. hosted-model nondeterminism;
2. residual condition unblinding;
3. limited receiver population;
4. limited scenario population;
5. two-arm design does not isolate structure from information/salience;
6. deterministic receiver is an engineering reference rather than behavioral diversity;
7. equal-information prose comparator is deferred;
8. foreign-native mapping study is independent of the CSH execution gate;
9. external timestamp/cryptographic anchoring is deferred absent a specific chronology claim;
10. the classifier is a bounded operationalization rather than a universal ontology of semantic error;
11. `P_r` captures only claim-attributable promotion;
12. task completion does not establish usefulness/correctness/decision quality; and
13. provider serving infrastructure may change during the study.

## Permitted result language

A completed successor may support language of the form:

> Under the frozen CSH-S001-v0.1 corpus, receiver configurations, coding procedure, classifier, and execution conditions, the explicit handoff-state condition produced [lower / equal / higher / mixed] unsupported-inheritance rule findings than the control condition, with the following receiver- and scenario-specific results.

It does not establish universal superiority of Fork, compliance, truth, legal sufficiency, institutional authority, production readiness, universal organizational effectiveness, that structure alone caused any observed difference, or that every rule finding is a distinct harmful act.
