# RGV v0.3 Publication Hardening Patch

## Status

Patch note: `RGV_v0_3_PUBLICATION_HARDENING_PATCH`

Base commit:

- `6b65337` — Add stateless relational graph verifier v0.3

## Purpose

This patch hardens RGV v0.3 for publication and external review.

It does not change the verifier's architecture.

It clarifies result semantics, corrects one example-artifact description, warns against schema-only validation, and adds adversarial tests for graph-level edge cases.

## Changes

1. Corrected the external pointer graph example so its evidence-reference description no longer says a downstream CBC was locally resolved when the graph intentionally records an `EXTERNAL_POINTER`.

2. Clarified `CLOSED_LOCAL` as self-contained local topology, not complete historical truth.

3. Clarified graph-level `PASS` as topology / relational-structure verification only, not truth, compliance, safety, legal sufficiency, deployment readiness, or complete-history verification.

4. Added CLI usage warning: exit code `0` is not a deployment gate, compliance approval, legal signoff, runtime authorization, or truth approval.

5. Added schema-only warning: JSON Schema validation is necessary but not sufficient. Conformant v0.3 verification requires the reference relational checks or equivalent behavior.

6. Added a closure-state interpretation table.

7. Added targeted tests for:
   - duplicate bundle non-claim IDs;
   - duplicate CCE non-claim IDs;
   - `NOT_APPLICABLE` with `EXPANDED`;
   - local source artifact claim-ID mismatch;
   - self-referential expansion cycle detection.

## Non-claims

This patch does not make RGV a compliance engine, legal authority, runtime control layer, deployment approval system, source-truth verifier, or complete-history verifier.

RGV remains stateless, bounded, local-bundle graph verification.
