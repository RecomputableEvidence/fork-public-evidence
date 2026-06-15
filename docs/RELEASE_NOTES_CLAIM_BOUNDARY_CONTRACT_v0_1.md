# Release Notes: Claim Boundary Contract v0.1

Status: `LOCKED`

Tag: `claim-boundary-contract-v0.1`

Primary document:

- `docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md`

Supporting artifacts:

- `examples/claim_boundary_contract/runtime_blocked_tool_call.json`
- `examples/claim_boundary_contract/eval_benchmark_pass.json`
- `schemas/claim_boundary_contract_v0_1.schema.json`
- `tests/test_claim_boundary_contract_v0_1.py`

## Summary

Claim Boundary Contract v0.1 defines Fork's creation-time boundary discipline for governance-related claims.

A Claim Boundary Contract does not define whether a governance claim is correct. It defines the minimum evidentiary structure required to preserve the claim's scope, exclusions, upstream reliance, known gaps, and verification boundary without allowing downstream systems to silently expand it.

Fork's role remains bounded:

> Fork is evidence-boundary infrastructure for AI-assisted governance. It does not decide whether a claim is legally sufficient, safe, compliant, or true. It preserves what was claimed, what was not claimed, what evidence was referenced, what upstream claims were relied on or rejected, and whether the sealed record still structurally verifies later.

## What v0.1 Adds

Claim Boundary Contract v0.1 introduces a bounded record structure for preserving:

- `claim_id`
- `claim_type`
- `issuer`
- `issuer_semantics_authority`
- `scope`
- `positive_claims`
- `non_claims`
- `evidence_refs`
- `upstream_claims_received`
- `upstream_claims_relied_on`
- `upstream_claims_rejected`
- `transitivity_policy`
- `inheritance_policy`
- `known_gaps`
- `human_or_institutional_decisions_remaining`
- `sealed_at`
- `verification_status`
- `verification_scope`

The pairing of `verification_status` and `verification_scope` is mandatory for safe interpretation.

Example:

```text
verification_status: PASS
verification_scope: RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY
```

PASS does not mean compliant, safe, legally sufficient, true, approved, or production-ready. It only means the sealed CBC and its preserved evidentiary structure verified within the declared scope.

## Examples Added

### Runtime Blocked Tool Call

`examples/claim_boundary_contract/runtime_blocked_tool_call.json`

This example shows a CBC around a runtime enforcement event. It preserves the fact that a specific tool call was blocked while explicitly refusing to promote that event into broader legal, regulatory, safety, monitoring-completeness, or workflow-sufficiency claims.

### Eval Benchmark Pass

`examples/claim_boundary_contract/eval_benchmark_pass.json`

This example shows a CBC around an evaluation result. It preserves the benchmark-pass claim while explicitly excluding deployment readiness, legal sufficiency, regulatory compliance, and future-performance claims.

## Schema Added

`schemas/claim_boundary_contract_v0_1.schema.json`

The schema enforces:

- required CBC fields
- explicit non-claims
- downstream preservation of non-claims
- SHA-256-shaped evidence and manifest hashes
- bounded `verification_status` values
- bounded `verification_scope` values
- no undeclared top-level properties

## Tests Added

`tests/test_claim_boundary_contract_v0_1.py`

The test suite validates:

- both committed CBC examples
- scoped interpretation of PASS
- preservation of downstream non-claims
- rejection of missing non-claims
- rejection of invalid verification statuses
- rejection of invalid evidence hashes
- rejection of attempts to silently drop non-claims downstream

Observed local test result before release:

- `10 passed`

## Doctrine Locked

CBC v0.1 locks the following doctrine:

- Claim boundaries are an architectural primitive.
- Non-claims must be explicit.
- Claims are non-transitive by default.
- Runtime enforcement is distinct from evidence architecture.
- Recomputable evidence means structural verification, not semantic truth.
- Fork is not a legal, compliance, safety, approval, or institutional authority.

## Relationship to Risk Frameworks and Standards

Fork is not a risk management framework or AI management system standard. Fork preserves the bounded evidence records that such frameworks and standards increasingly require organizations to produce, inspect, and defend.

A CBC may support governance, risk management, audit, and accountability processes, but it does not certify conformity with any framework, standard, law, regulation, or certification regime.

## Future Extension

CBC v0.1 remains focused on creation-time claim boundaries.

A complementary future primitive, the Claim Consumption Event, may describe how downstream actors rely on a CBC, whether they preserve, narrow, ignore, or expand its boundary, and how such expansions become explicit, attributable, and recomputable rather than silent.

Claim boundaries prevent silent ambiguity at creation; claim-consumption friction prevents silent expansion at use.

## Non-Goals

CBC v0.1 does not:

- define global governance semantics
- determine whether a claim is correct
- certify compliance
- determine legal sufficiency
- determine safety
- approve deployment
- replace policy engines
- replace runtime enforcement
- replace human or institutional judgment
- silently promote local claims into transferable assurances