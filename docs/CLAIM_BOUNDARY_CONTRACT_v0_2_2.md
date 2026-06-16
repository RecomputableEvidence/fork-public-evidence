# Claim Boundary Contract v0.2.2

## Status

Version: `CBC_v0_2_2`

CBC v0.2.2 is the final precision hardening patch in the CBC v0.2 line.

It preserves CBC v0.2.1's source-side claim-boundary structure and closes residual drift surfaces identified during external review.

## Purpose

A Claim Boundary Contract records how a source-side claim boundary is represented as evidence.

It does not assert source truth, legal sufficiency, compliance sufficiency, deployment readiness, policy correctness, source completeness, or runtime enforcement.

## v0.2.2 hardening

CBC v0.2.2 adds or reinforces:

- duplicate `upstream_claims_received.claim_id` rejection;
- explicit carrythrough of preserved upstream non-claim IDs into downstream CBC non-claims;
- stronger documentation that partial verification scopes cannot imply full verification;
- clearer distinction between claim-boundary representation and institutional/legal authority.

## Non-claim carrythrough

If a downstream CBC relies on an upstream claim and lists preserved upstream non-claim IDs, those IDs must remain represented in the downstream CBC's own `non_claims` array.

An aggregate statement is not enough for per-non-claim traceability.

## Partial verification posture

Partial verification terms can describe bounded partial inspection states.

They must not be used to imply completeness where none exists.

A `PASS` verification state remains bounded to the stated verification scope and does not assert truth, safety, compliance, deployment readiness, or institutional authorization.

## Relationship to CCE v0.2.2

CBC records the source-side claim-boundary node.

CCE records the downstream consumption edge.

The edge does not become the node.
