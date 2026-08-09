# PROOF-005 CAD Correction Successor v0.2.1

Status: `CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED`

This is an additive successor to the frozen PROOF-005 v0.2 candidate at
`4ce0413e70fc9355c1319d7e25b5157497faa90c`.

It does not rewrite that reviewed coordinate. The v0.2 data artifacts remain
unchanged. v0.2.1 is intentionally narrow because the exterior return identified
two checker-level residuals rather than a new defect in the underlying corrected
C001-C008 records.

## Exterior-return basis

Claude (Anthropic) returned
`EXTERIOR_RECOMPUTATION_CONFORMING_WITH_QUALIFICATIONS` against the frozen v0.2
head. Baseline checker and focused tests reproduced, but two reviewer-originated
mutations were accepted:

1. an otherwise compliant `MODEL_SELF_REPORT` event could carry undeclared
   overclaim-bearing fields because event objects were not schema-closed;
2. `causal_standing == UNRESOLVED` was enforced for model self-report only when
   `statement_origin == "CLAUDE"`, leaving a latent origin-asymmetry for other
   model self-reports.

The return also noted missing dedicated shipped-test coverage for C005 and C008.

## v0.2.1 corrections

`tools/check_fork_cad_candidate_v0_2_1.py` first executes the complete v0.2
checker, then applies two successor invariants:

- every event object must contain exactly the controlled event keys; undeclared
  fields are rejected;
- any event whose `source_role` is `MODEL_SELF_REPORT` must keep
  `causal_standing = UNRESOLVED`, regardless of the literal origin string.

The successor deliberately reuses the exact reviewed v0.2 JSON data rather than
silently rewriting them.

`tests/test_fork_cad_candidate_v0_2_1.py` adds focused coverage for:

- both exterior-review residual bypasses;
- origin-agnostic compliant model-self-report handling;
- C005 scope-promotion pressure;
- C008 automatic-proof-promotion pressure;
- mutation of every field in `CONTROL_EFFECTS_v0_2.json`;
- missing controlled event keys.

## Review sequence

A green local or CI result establishes only
`CORRECTION_SUCCESSOR_CANDIDATE_READY_FOR_EXACT_HEAD_REVIEW`.

Required order:

1. exact-head CI;
2. bounded construction-assisted review;
3. freeze exact successor coordinate;
4. exterior recomputation including both reproduced residual attacks;
5. preserve the exterior return;
6. separate source-evidence / proof-packaging disposition.

No step inherits authority from the previous step.

## Non-effects

This successor does not admit PROOF-005, establish global independent or
empirical validation, promote Fork Candidate Model standing, authorize provider
calls or Pair-001, authorize a pilot or production deployment, establish legal
or compliance sufficiency, endorse any actor, or transfer authority.
