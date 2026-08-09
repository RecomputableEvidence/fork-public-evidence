# PROOF-005 CAD Correction Successor v0.2.1

Status: `CORRECTION_SUCCESSOR_CANDIDATE_NOT_ADMITTED`

This is an additive successor to the frozen PROOF-005 v0.2 candidate at
`4ce0413e70fc9355c1319d7e25b5157497faa90c`.

It does not rewrite that reviewed coordinate. The v0.2 data artifacts remain
unchanged. v0.2.1 is intentionally narrow because the exterior return identified
checker-level residuals rather than a new defect in the underlying corrected
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
checker.

For the fixed historical event register, v0.2.1 uses a strict JSON loader that
rejects duplicate object keys before interpretation. It then computes a
canonical parsed-JSON SHA-256 fingerprint. This binds the complete reviewed
register, including event values and non-claims, rather than only closing the
set of field names.

The strict-parse step matters because a default JSON loader can collapse
repeated keys before hashing. Without duplicate-key rejection, raw text could be
representation-ambiguous while producing the same parsed object. v0.2.1 rejects
that state rather than treating it as equivalent evidence.

The canonical fingerprint deliberately normalizes formatting and object-key
ordering. Whitespace or key-order differences that parse to the same
unambiguous JSON structure therefore do not create a false semantic change.
Changes to event content, source references, dispositions, summaries,
non-claims, array ordering, or other parsed values change the fingerprint.

Separately, the successor exposes a generic model-self-report invariant for
reviewer-created pressure cases:

- a model-self-report event must use exactly the controlled event keys;
- `mechanism_verified` must remain `false`;
- `causal_standing` must remain `UNRESOLVED` regardless of the literal
  `statement_origin`.

This separates two questions cleanly: the historical v0.2 register is fixed and
reconstructable, while the epistemic non-promotion rule can still be challenged
against synthetic events from other model origins.

`tests/test_fork_cad_candidate_v0_2_1.py` adds focused coverage for:

- duplicate-key parser ambiguity;
- both exterior-review residual bypasses;
- origin-agnostic compliant model-self-report handling;
- overclaim substitution through allowed event fields;
- mutation of the register non-claims;
- C005 scope-promotion pressure;
- C008 automatic-proof-promotion pressure;
- mutation of all 13 actually governed `CONTROL_EFFECTS_v0_2.json` fields;
- explicit confirmation that informational `record_id` is not misrepresented as
  a governed effect;
- missing controlled model-self-report event keys.

## Review sequence

A green local or CI result establishes only
`CORRECTION_SUCCESSOR_CANDIDATE_READY_FOR_EXACT_HEAD_REVIEW`.

Required order:

1. exact-head CI;
2. bounded construction-assisted review;
3. freeze exact successor coordinate;
4. exterior recomputation including the two reproduced residual attacks,
   allowed-field substitution pressure, and parser-representation pressure;
5. preserve the exterior return;
6. separate source-evidence / proof-packaging disposition.

No step inherits authority from the previous step.

## Non-effects

This successor does not admit PROOF-005, establish global independent or
empirical validation, promote Fork Candidate Model standing, authorize provider
calls or Pair-001, authorize a pilot or production deployment, establish legal
or compliance sufficiency, endorse any actor, or transfer authority.
