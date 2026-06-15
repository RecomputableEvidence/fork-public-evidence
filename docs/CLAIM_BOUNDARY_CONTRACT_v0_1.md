# Claim Boundary Contract v0.1

Status: Draft v0.1  
Scope: Evidence-boundary contract for AI-assisted governance records  
Non-goal: This document does not define governance correctness, legal sufficiency, safety, compliance, or institutional approval.

## Canonical Fork Positioning

Fork is evidence-boundary infrastructure for AI-assisted governance. It does not decide whether a claim is legally sufficient, safe, compliant, or true. It preserves what was claimed, what was not claimed, what evidence was referenced, what upstream claims were relied on or rejected, and whether the sealed record still structurally verifies later.

## Canonical Definition

A Claim Boundary Contract does not define whether a governance claim is correct. It defines the minimum evidentiary structure required to preserve the claim's scope, exclusions, upstream reliance, known gaps, and verification boundary without allowing downstream systems to silently expand it.

## Scope-Safe Ingestion Language

Fork ingests claim-bearing records from configured governance sources and wraps them in a Claim Boundary Contract when the minimum evidentiary structure is present.

## Design Principles

### Claim boundaries as an architectural primitive

Governance becomes composable only when claims are bounded objects with explicit scope, support, and limits.

### Explicit non-claims

Every governance record must say what it does not guarantee, to prevent silent expansion into institutional assurance.

### Non-transitivity by default

No governance claim should be treated as transitive across systems unless explicitly declared and scoped.

### Runtime enforcement versus evidence architecture

Runtime enforcement answers what is allowed right now. Evidence architecture answers what can later be proven about the bounded claims that were made, what evidence supported them, and what remained unresolved.

### Recomputable evidence as structural verification

Recomputability checks whether preserved artifacts and structure still match the sealed record and its declared boundary. It does not determine whether the underlying claim was legally correct, safe, compliant, approved, or true.

## CBC v0.1 Required Fields

### `claim_id`

Unique identifier for this bounded record.

### `claim_type`

Issuer-defined type of claim, such as an eval result, runtime enforcement event, legal review, or policy mapping.

Fork does not define the semantics of `claim_type`.

### `issuer`

System, team, or institution that made the claim.

### `issuer_semantics_authority`

Identifies who owns the meaning of `claim_type` and `positive_claims`.

Examples:

- `issuer_defined`
- `legal_department_policy_taxonomy_v2026_06`
- `model_risk_management_taxonomy_v1`

This field prevents Fork from being mistaken as the semantic authority over issuer-defined claim vocabulary.

### `scope`

What the claim is about.

Examples:

- specific model version
- workflow
- dataset
- tool call
- policy document
- review event
- deployment configuration

### `positive_claims`

Explicit assertions the issuer is making within this scope.

### `non_claims`

Explicit exclusions: what the issuer is not asserting.

Examples:

- no statement about legal sufficiency
- no statement about regulatory compliance
- no statement about system-wide safety
- no statement about completeness of monitoring
- no statement about production readiness

### `evidence_refs`

References, hashes, manifests, receipts, or URIs for artifacts that support the claim.

### `upstream_claims_received`

Claims ingested from other systems as context.

### `upstream_claims_relied_on`

Subset of upstream claims the issuer actually depended on.

### `upstream_claims_rejected`

Upstream claims explicitly not trusted, overridden, ignored, or treated as insufficient.

### `transitivity_policy`

How, if at all, the positive claim may be inherited downstream.

Recommended modes:

- `LOCAL_ONLY`
- `SCOPED`
- `CONDITIONAL`
- `NON_TRANSITIVE`

Default posture: claims are non-transitive unless explicitly declared and scoped.

### `inheritance_policy`

Rules for how this claim's non-claims and exclusions must travel downstream.

The core doctrine is:

- claims do not automatically compose;
- exclusions must not be silently peeled off;
- downstream systems may narrow a claim;
- downstream systems may not drop original exclusions without issuing a new explicit claim.

### `known_gaps`

Known missing evidence, unresolved issues, or limitations.

### `human_or_institutional_decisions_remaining`

Decisions still pending at the human or institutional authority layer.

### `sealed_at`

When and how the CBC was sealed.

### `verification_status`

One of:

- `PASS`
- `FAIL`
- `NOT_CHECKED`
- `PARTIAL`

### `verification_scope`

What `verification_status` actually applies to.

Recommended value for Fork v0.1:

- `RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`

The pairing is mandatory for safe interpretation:

```text
verification_status: PASS
verification_scope: RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY
```

PASS never means compliant, safe, legally sufficient, true, approved, or production-ready.  
It only means the sealed CBC and its preserved evidentiary structure verified within the declared scope.

## Relationship to AI Risk Management Frameworks and Standards

The Claim Boundary Contract is designed to support AI risk management and AI governance environments by preserving the evidentiary boundary around governance-related claims. Risk management frameworks and AI management system standards may require organizations to identify, assess, document, monitor, govern, or improve the management of AI-related risks. A Claim Boundary Contract does not replace those frameworks or standards and does not certify that an organization has satisfied them.

Instead, a Claim Boundary Contract provides a bounded evidence structure for preserving what a system, team, or institution claimed; what it did not claim; what evidence it referenced; what upstream claims it relied on or rejected; what gaps remained; and what verification scope applies to the sealed record.

Fork therefore does not assert compliance with any external risk management framework, AI management system standard, law, regulation, or certification regime. Fork provides evidence-boundary infrastructure that may help organizations preserve, inspect, and structurally verify the records they use inside broader governance, risk management, audit, and accountability processes.

Canonical posture:

> Fork is not a risk management framework or AI management system standard. Fork preserves the bounded evidence records that such frameworks and standards increasingly require organizations to produce, inspect, and defend.

## What Fork Does With a CBC

Fork may:

- ingest a claim-bearing record from a configured governance source;
- wrap that record in a Claim Boundary Contract when minimum evidentiary structure is present;
- preserve claims, non-claims, evidence references, upstream reliance, known gaps, and remaining institutional decisions;
- seal the CBC and associated evidence manifests;
- emit verification results with explicit status and scope;
- later structurally verify whether the sealed record still matches its preserved evidentiary structure.

## Non-Goals

Fork does not:

- define global governance semantics;
- determine whether a claim is correct;
- determine whether a claim is legally sufficient;
- certify compliance with laws, regulations, standards, or frameworks;
- determine model safety;
- determine production readiness;
- replace policy engines, runtime enforcement systems, legal review, compliance review, or institutional judgment;
- silently promote local claims into transferable assurances.

## References

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF 1.0 PDF: https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf
- ISO/IEC 42001: https://www.iso.org/standard/42001
## Future Extension: Claim Consumption Events

Claim Boundary Contracts govern creation-time boundaries for governance-related claims. A complementary future primitive, the Claim Consumption Event, may describe how downstream actors rely on a CBC, whether they preserve, narrow, ignore, or expand its boundary, and how such expansions become explicit, attributable, and recomputable rather than silent.

A Claim Consumption Event records when a downstream actor, system, workflow, or institution relies on a Claim Boundary Contract; what parts of the bounded claim were relied on; which non-claims were preserved; whether the original boundary was preserved, narrowed, ignored, or expanded; and whether any expansion produced a new explicit claim with its own Claim Boundary Contract.

Claim boundaries prevent silent ambiguity at creation; claim-consumption friction prevents silent expansion at use.

Fork does not solve incentive pressure by pretending people will stop compressing meaning. It makes that compression explicit. If a downstream actor turns "checked" into "approved," Fork's posture is that the expansion should become a recorded, attributable, recomputable event, not invisible semantic drift.
