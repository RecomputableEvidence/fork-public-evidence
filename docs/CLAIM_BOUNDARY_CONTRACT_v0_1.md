# Fork Claim Boundary Contract v0.1

Status: INTERNAL_CONSTITUTIONAL_CONTRACT  
Scope: Fork evidence artifacts, verifier outputs, receipts, reviewer reports, release metadata, and future reconstruction layers.

## 1. Purpose

This contract defines the first enforceable Claim Boundary layer for Fork.

Fork preserves recomputable evidence. Claim Boundaries define what that evidence is permitted to establish, what it is not permitted to imply, what was checked, what was not checked, and where later human, legal, causal, or institutional judgment must begin.

This contract is not buyer-facing marketing copy. It is constitutional architecture.

## 2. Definition

A claim boundary is an explicit, machine-readable constraint on what a piece of evidence, verifier, receipt, release, or reconstructed state is permitted to establish.

Practical rule:

Fork does not only preserve records. It preserves the limits of what those records are allowed to prove.

## 3. Constitutional Invariant

**Every Fork evidence artifact must carry its evidentiary perimeter**: what it proves, what it does not prove, what was checked, what was not checked, and where later human, legal, causal, or institutional judgment must begin.

## 4. Supported Claim Type in v0.1

The only claim type supported in v0.1 is:

`OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY`

This claim type allows only integrity and execution-of-checks claims.

It may assert that:

- The declared artifact set recomputes against its manifest under the recorded verifier environment.
- The verifier evaluated the declared checks defined for the relevant integrity profile.
- PASS, FAIL, and NOT_CHECKED states were emitted for those declared checks.
- The record preserves bounded evidence and explicit non-claims.

It must not assert or imply that:

- The decision was correct.
- The workflow was complete.
- The source system was complete.
- The action was lawful.
- The output was compliant.
- The human reviewer meaningfully reviewed it.
- The evidence is admissible.
- The model was accurate.
- The result is fair, unbiased, authorized, validated, enterprise-proven, or a source of truth.

## 5. PASS / FAIL / NOT_CHECKED Semantics

### PASS

PASS means the evaluated integrity conditions met their declared checks.

PASS does not mean the underlying workflow was complete, lawful, correct, compliant, fair, unbiased, authorized, admissible, or meaningfully reviewed.

### FAIL

FAIL means the evaluated integrity conditions did not meet their declared checks.

FAIL is evidence of a failed check. It is not a comprehensive causal explanation.

### NOT_CHECKED

NOT_CHECKED means the condition was not evaluated.

A NOT_CHECKED state cannot be inferred as a pass, soft pass, warning-only state, or implied satisfaction of the unchecked condition.

## 6. Required Claim Boundary Payload Fields

Every v0.1 claim boundary payload must include:

- `claim_type`
- `claim_statement`
- `allowed_inferences`
- `forbidden_inferences`
- `not_checked`
- `non_claims`

For v0.1, all arrays must be present and non-empty.

## 7. Required Non-Claims

Unless a separate claim type and gate explicitly supports them, the following remain outside the integrity-only claim boundary:

- `SOURCE_COMPLETENESS`
- `DECISION_CORRECTNESS`
- `LEGAL_ADMISSIBILITY`
- `POLICY_COMPLIANCE`
- `HUMAN_IDENTITY`
- `MEANINGFUL_HUMAN_REVIEW`
- `MODEL_ACCURACY`
- `FAIRNESS_OR_BIAS_OUTCOME`
- `AUTHORIZATION_VALIDITY`

## 8. Forbidden Claim Expansion

Under `OBSERVED_WORKFLOW_EVENT_INTEGRITY_ONLY`, the following claim-expanding terms are prohibited in `claim_statement` and `allowed_inferences`:

- compliant
- compliance
- lawful
- admissible
- correct
- complete
- authorized
- unbiased
- fair
- validated
- enterprise-proven
- source of truth

These terms are not globally forbidden forever. They are forbidden under this claim type unless a future claim type and supporting gate make them legitimate.

## 9. Release and Receipt Rule

No receipt, release metadata, or machine-readable evidence summary is valid unless it includes a claim boundary payload that passes `tools/check_claim_boundary.py`.

The release process and CI should run the checker against:

- Coherence receipts
- Future conformance receipts
- Machine-readable release metadata
- Reviewer-facing summaries that declare what a Fork artifact proves

## 10. Reconstruction / Hypothesis Boundary

Reconstruction layers must distinguish between:

- What the evidence shows
- What the evidence failed to show
- What was not checked
- What remains unresolved
- What is hypothesized
- What requires later legal, causal, institutional, or human judgment

A reconstruction may attach hypotheses to evidence. It may not rewrite the evidentiary substrate or convert sequence coherence into proof of causality.

## 11. v0.1 Enforcement Rule

For integrity-only claims, any overclaiming term in `claim_statement` or `allowed_inferences` causes a failing Claim Boundary check.

The immediate goal of v0.1 is narrow:

Make overclaiming fail a test.