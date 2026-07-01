# Non-Claims Contract v0.1

## Purpose

This document defines the reviewer-facing non-claims contract for Fork's public evidence surface.

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

The non-claims contract is intended to make negative boundaries explicit and partially machine-checkable.

## Machine-Readable Contract

The machine-readable contract is located at:

`examples/vendor-risk/non_claims_contract.json`

The schema is located at:

`schemas/non_claims_contract.schema.json`

The checker is located at:

`tools/check_non_claims_contract.py`

## Invariant Non-Claims

The following statements are invariant for the current public surface:

- This system does not assert legal sufficiency.
- This system does not grant authority.
- This system does not certify compliance.
- This system does not approve production use.
- This system does not replace institutional review.
- This system does not verify correctness of underlying workflow data.

## Boundary Meaning

These non-claims are negative boundaries only.

They do not create authority, compliance status, legal sufficiency, production readiness, or factual correctness.

They are intended to prevent reviewers from treating Fork records as approval, authorization, certification, compliance determination, legal judgment, or factual truth verification.

## Current Scope

The v0.1 checker verifies that required non-claim statements appear in the public README and scans selected public paths for prohibited positive assertions.

This is not a complete legal review, compliance review, or proof of semantic safety.

Future versions may extend this contract into CI and add richer semantic checks.
