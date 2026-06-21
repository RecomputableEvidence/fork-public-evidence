# Boundary Delta Record v0.1

## Status

Boundary Delta Record v0.1 is a narrow structural artifact for making boundary expansion visible at the point where a downstream statement relies on, narrows, drops, suppresses, or expands material from an upstream claim boundary.

This release does not introduce a new governance doctrine. It implements a mechanical inspection record for boundary transitions.

## Category sentence

Fork makes unauthorized semantic expansion mechanically visible.

## Core boundary sentence

Fork does not evaluate downstream statements. Fork evaluates whether downstream statements require authority, scope, evidence, reference status, or recomputation status that was not transferred across the boundary.

## Purpose

A Boundary Delta Record records the delta between an upstream boundary surface and a downstream statement surface.

It answers only these questions:

- What arrived at the boundary?
- What crossed the boundary?
- What did not cross the boundary?
- What was lost at the boundary?
- What was suppressed at the boundary?
- What was generalized, added, or converted beyond what crossed the boundary?
- Whether the authored record is structurally inspectable under the v0.1 checker.

It does not answer:

- Whether the downstream statement is true.
- Whether the downstream statement is safe.
- Whether the downstream statement is compliant.
- Whether the downstream statement is legally sufficient.
- Whether a human or institution should rely on the downstream statement.
- Whether suppressed or lost material was substantively important.
- Whether an expansion is permitted by external policy, contract, law, or governance authority.

## v0.1 hard locks

Boundary Delta Record v0.1 enforces the following locks:

1. `licensed_claim_surface` is derived by the checker. If the authored value does not match the derived value, the record fails closed.
2. Unknown transition kinds fail closed.
3. Unknown transformation rules fail closed.
4. Any true derived flag without a supporting transition fails closed.
5. Loss and suppression are structurally distinct.
6. No scoring, severity, confidence, LLM interpretation, recommendation, approval, or cross-record inference is allowed.
7. Each recognized `transition_kind` must use a compatible recognized `transformation_rule`; known-but-incompatible pairs fail closed.
8. The checker emits only `INSPECTABLE` or `NOT_INSPECTABLE`.

## Structural outcome

The checker emits one binary outcome:

- `INSPECTABLE`
- `NOT_INSPECTABLE`

`INSPECTABLE` means the record is structurally coherent under the v0.1 rules and does not contain an unlicensed expansion transition.

`NOT_INSPECTABLE` means at least one v0.1 hard lock failed, or the record contains a transition that requires authority, scope, evidence, reference status, non-claim continuity, or recomputation status that was not transferred across the boundary.

`NOT_INSPECTABLE` is not a legal, safety, compliance, quality, or truth finding.

## Licensed claim surface

The checker derives one of the following surfaces:

- `SOURCE_SURFACE_PRESERVED`
- `SOURCE_SURFACE_NARROWED`
- `REFERENCE_SUPPRESSED_AT_BOUNDARY`
- `UNLICENSED_EXPANSION_DETECTED`

The author may include `licensed_claim_surface`, but the checker recomputes it from the transitions and flags. Authored mismatch fails closed.

## Derived flags

The checker derives these flags:

- `claim_scope_generalized`
- `silence_converted_to_claim`
- `authority_expansion_required`
- `evidence_reference_expansion_required`
- `recomputation_status_converted_to_truth`
- `evidence_reference_lost`
- `evidence_reference_suppressed`
- `non_claim_dropped`

A true authored flag must be supported by at least one transition that mechanically produces the flag.

A false authored flag must not hide a transition that mechanically produces the flag.

## Transition kinds

v0.1 recognizes these transition kinds:

Safe or inspectable transition kinds:

- `CLAIM_SCOPE_PRESERVED`
- `CLAIM_SCOPE_NARROWED`
- `NON_CLAIM_PRESERVED`
- `EVIDENCE_REFERENCE_PRESERVED`
- `EVIDENCE_REFERENCE_LOST`
- `RECOMPUTATION_STATUS_PRESERVED`
- `AUTHORITY_PRESERVED`

Fail-closed transition kinds:

- `CLAIM_SCOPE_GENERALIZED`
- `CLAIM_ADDED_FROM_SILENCE`
- `AUTHORITY_EXPANDED`
- `EVIDENCE_REFERENCE_EXPANDED`
- `EVIDENCE_REFERENCE_SUPPRESSED`
- `RECOMPUTATION_STATUS_CONVERTED_TO_TRUTH`
- `NON_CLAIM_DROPPED`

A fail-closed transition kind is still mechanically visible. The checker does not erase it, reinterpret it, or score it. It emits `NOT_INSPECTABLE`.

## Transformation rules

v0.1 recognizes these transformation rules:

Safe or inspectable rules:

- `PRESERVE_AS_IS`
- `NARROW_SCOPE`
- `RETAIN_NON_CLAIM`
- `PRESERVE_EVIDENCE_REFERENCE`
- `RECORD_REFERENCE_LOSS`
- `PRESERVE_RECOMPUTATION_STATUS`
- `PRESERVE_AUTHORITY`

Fail-closed rules:

- `GENERALIZE_SCOPE`
- `CONVERT_SILENCE_TO_CLAIM`
- `EXPAND_AUTHORITY`
- `ADD_UNTRANSFERRED_EVIDENCE_REFERENCE`
- `SUPPRESS_REFERENCE`
- `MAP_RECOMPUTATION_TO_TRUTH`
- `DROP_NON_CLAIM`

Unknown transformation rules fail closed.

## Loss vs suppression

Reference loss means a referenced item did not cross the boundary and the record represents that loss as loss.

Reference suppression means a referenced item did not cross the boundary and the record represents the removal as intentional suppression.

v0.1 treats loss and suppression differently:

- `EVIDENCE_REFERENCE_LOST` may still be `INSPECTABLE` if the record is otherwise structurally coherent.
- `EVIDENCE_REFERENCE_SUPPRESSED` fails closed as `NOT_INSPECTABLE`.

The checker does not decide whether suppression was justified.

## Prohibited fields

The following fields are prohibited anywhere in a Boundary Delta Record v0.1 object:

- `score`
- `severity`
- `risk_score`
- `confidence`
- `llm_interpretation`
- `cross_record_inference`
- `ranking`
- `recommendation`
- `approval_status`

Presence of any prohibited field fails closed.

## Acceptance gate

A third party should be able to:

1. Read the record.
2. Recompute the licensed claim surface.
3. Reproduce each derived flag from the transition list.
4. Distinguish loss from suppression.
5. Confirm that no scoring, severity, confidence, LLM interpretation, recommendation, approval, or cross-record inference is present.
6. Reach the same binary checker result.

If that cannot be done mechanically, the record is not inspectable under v0.1.
