# Claim Boundary Contract v0.2.1

## Status

Version: `CBC_v0_2_1`

CBC v0.2.1 is a precision patch over CBC v0.2. It hardens naming, upstream-claim structure, policy-association non-claims, benchmark terminology, and partial-verification semantics.

## Core boundary

A CBC defines a source-side claim boundary.

It records what an artifact claims, what it does not claim, what verification scope applies, what upstream claims were received, which were relied on, which were rejected, and which human or institutional decisions remain outside the record.

CBC v0.2.1 does not assert source truth, legal sufficiency, compliance sufficiency, deployment readiness, policy correctness, malicious intent, or source completeness.

## Precision changes in v0.2.1

- Benchmark artifacts are named as benchmark execution records rather than benchmark pass records.
- Runtime blocked-tool-call examples explicitly avoid claims about user intent, legal sufficiency, policy correctness, and compliance certification.
- Policy association is explicitly non-certifying.
- Upstream claim records require `claim_id` in schema, not only in tests.
- `issuer_semantics_authority.mode` is constrained by enum.
- `sealed_by.name` and `sealed_by.type` are non-empty and schema-enforced.
- Partial verification scopes remain available as bounded states, but `PASS` may only pair with `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`.

## Partial verification posture

CBC v0.2.1 intentionally preserves partial verification terms such as `RECORD_INTEGRITY_ONLY` and `BOUNDARY_STRUCTURE_ONLY`.

Those terms can describe bounded partial inspection states. They cannot be paired with `PASS`.

A full `PASS` requires `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`.

## Benchmark execution non-claim

A benchmark execution record may record that benchmark execution yielded the recorded result. It does not claim deployment readiness, general safety, legal sufficiency, production performance, or safety against out-of-distribution conditions.

## Runtime blocked-tool-call non-claim

A runtime blocked-tool-call record may record that a policy trigger was matched and a tool call was structurally halted. It does not assert malicious user intent, legal sufficiency, compliance certification, or policy correctness.

## Policy association non-claim

Association with a policy identifier does not constitute institutional certification of correctness, compliance, or legal sufficiency.
