# Claim Boundary Contract v0.2

**Status**: DRAFT  
**Previous Version**: `claim-boundary-contract-v0.1`  
**Target Tag**: `claim-boundary-contract-v0.2`

## Purpose

Claim Boundary Contract v0.2 preserves the v0.1 doctrine while hardening the object against implementation misuse.

CBC v0.1 established the creation-time boundary discipline:

- what was claimed;
- what was not claimed;
- what evidence was referenced;
- what upstream claims were received, relied on, or rejected;
- what gaps remained;
- what human or institutional decisions remained;
- what verification status and verification scope applied.

CBC v0.2 adds stricter structural requirements so the boundary is harder to misread, weaken, or silently expand.

## Terminology Clarification

"Contract" in **Claim Boundary Contract** refers to a structural evidentiary contract.

It is not a legal contract, service-level agreement, smart contract, policy instrument, compliance certification, approval mechanism, or institutional authorization.

Fork records and preserves the declared claim boundary. It does not decide whether the claim is legally sufficient, safe, compliant, approved, true, or institutionally authorized.

## CBC as Node

A Claim Boundary Contract is a node in the governance evidence graph.

It contains the bounded claim, non-claims, evidence references, upstream reliance posture, known gaps, human or institutional decisions remaining, sealing information, verification status, and verification scope.

A Claim Consumption Event is the edge that records downstream use or transformation of a CBC. If downstream consumption expands the original boundary, that expansion belongs in a new CBC. The CCE records the edge; it does not become the expanded claim node.

## Changes from v0.1

### 1. Required Versioning

CBC v0.2 adds:

```json
"claim_boundary_contract_version": "0.2"
```

This field is required. A CBC should identify the schema version under which it was created so later reviewers and checkers can interpret the record without guessing.

### 2. Verification Scope Guardrail

CBC v0.2 enforces the following structural rule:

- `verification_status: "PASS"` requires  
- `verification_scope: "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"`

This prevents a PASS state from being paired with a weaker or ambiguous verification scope.

A PASS result still does not mean the claim is true, safe, compliant, legally sufficient, approved, production-ready, or institutionally authorized. It only means the record passed within the declared structural verification scope.

### 3. Downstream Narrowing Must Remain Allowed

CBC v0.2 requires:

```json
"downstream_may_narrow": true
```

Downstream systems may rely on less than the original claim. They may not silently broaden the claim or drop non-claims without issuing a new explicit claim boundary.

### 4. Sealing Accountability

CBC v0.2 adds `sealed_by` inside `sealed_at`.

Required fields:

- `name`
- `type`

Optional field:

- `system_id`

This adds structural accountability for the sealing actor or process without making Fork an identity provider, access-control system, or institutional authority.

### Non-Changes from v0.1

CBC v0.2 does not weaken the v0.1 doctrine.

- `must_travel_downstream: true` remains required for declared non-claims.
- Non-claims remain part of the claim boundary.
- Fork remains evidence-boundary infrastructure.
- Fork does not become a policy engine, runtime controller, legal authority, compliance oracle, model-safety evaluator, or approval system.
- Verification remains structural, not semantic.

## Enforcement Split

CBC v0.2 separates single-record structural validation from relational graph validation.

JSON Schema enforces:

- required fields;
- enum values;
- SHA-256 patterns;
- `additionalProperties: false`;
- required CBC version;
- required `sealed_by`;
- `downstream_may_narrow: true`;
- `verification_status: "PASS"` requiring `verification_scope: "RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY"`.

Python tests/checkers enforce relational invariants, including:

- `upstream_claims_relied_on` must be a subset of `upstream_claims_received`;
- example fixtures must preserve valid upstream claim references.

## v0.2 Boundary Statement

A CBC v0.2 record preserves a bounded structural claim and its declared non-claims. It does not validate the semantic truth of the claim, the correctness of an AI model, legal sufficiency, regulatory compliance, safety, institutional approval, or source-of-record authority.
