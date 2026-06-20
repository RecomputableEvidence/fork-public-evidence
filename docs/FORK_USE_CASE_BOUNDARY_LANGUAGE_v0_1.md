# Fork Use Case Boundary Language v0.1

## Status

Draft public doctrine artifact for staging Fork use cases across regulated, high-stakes, and audit-sensitive workflows.

## Purpose

This artifact defines the canonical boundary language that Fork use case documents and machine-readable use case records should use.

Fork use cases should not be framed as universal automation, policy enforcement, legal certification, clinical validation, safety validation, or approval infrastructure. They should be framed as evidence-boundary staging records.

## Canonical Fork role

Fork is evidence-boundary infrastructure for AI-assisted governance.

Fork preserves:

- what was claimed;
- what was not claimed;
- what evidence was referenced;
- what upstream claims were relied on or rejected;
- how a downstream actor consumed the record; and
- whether the sealed record still structurally verifies later.

Fork does not determine whether the underlying claim is true, safe, legally sufficient, compliant, clinically appropriate, financially sound, production-ready, or approved.

## Use case staging pattern

Every Fork use case should be staged through the same five-part structure.

| Layer | Fork question |
| --- | --- |
| Source event | What artifact, workflow, or handoff occurred? |
| Supported claim | What narrow claim is actually supported by the record? |
| Non-claims | What stronger claims are explicitly not being made? |
| Consumption event | How did a downstream actor, system, or institution rely on the claim? |
| Boundary result | Was the boundary preserved, unresolved, expanded, or structurally incomplete? |

## Required boundary outcomes

Use case records should use this outcome vocabulary.

| Outcome | Meaning |
| --- | --- |
| `BOUNDARY_PRESERVED` | Downstream use stayed within the declared claim boundary. |
| `POINTER_UNRESOLVED` | A required evidence, authority, or reference pointer could not be resolved. |
| `BOUNDARY_EXPANSION_DETECTED` | A downstream actor treated a narrow claim as a broader claim. |
| `NON_CLAIM_DROPPED` | A downstream artifact omitted one or more upstream non-claims. |
| `EXPANSION_AUTHORITY_REF_MISSING` | A stronger downstream claim was added without an authority reference and evidence reference. |
| `MAPPING_INCOMPLETE` | Preserved and dropped non-claims do not cover the upstream non-claim set. |

A valid Fork use case record may report `BOUNDARY_EXPANSION_DETECTED`, `POINTER_UNRESOLVED`, or another adverse boundary result. Valid means the boundary record is structurally complete and interpretable. It does not mean the downstream use was approved.

## Required verification scope phrase

Use case records should bind verification to this phrase:

`RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`

This phrase prevents a structural result from being interpreted as truth, safety, compliance, approval, or legal sufficiency.

## Standard non-claim pattern

Use case records should express non-claims using stable lower-case tokens:

- `does_not_claim_truth`
- `does_not_claim_safety`
- `does_not_claim_compliance`
- `does_not_claim_legal_sufficiency`
- `does_not_claim_approval`

Domain-specific non-claims may extend this pattern:

- `does_not_claim_control_effectiveness`
- `does_not_claim_vendor_approval`
- `does_not_claim_model_safety`
- `does_not_claim_patient_safety`
- `does_not_claim_medical_necessity`
- `does_not_claim_no_breach_occurred`

## Prohibited readings

Fork use cases should explicitly reject the following readings:

| Prohibited reading | Boundary correction |
| --- | --- |
| Verified means true. | Verified means the record structurally verifies within the declared boundary. |
| Reviewed means approved. | Review metadata is not approval unless approval is separately claimed by an authorized actor. |
| Evidence present means compliant. | Evidence presence is not a compliance determination. |
| Benchmark passed means safe. | Benchmark records do not generalize into model safety claims. |
| Triage found no issue means no breach occurred. | Observed evidence in a triage record is not proof of absence. |
| Packet complete means vendor approved. | Completeness of evidence inventory is not risk acceptance or vendor approval. |

## Reusable use case paragraph

This use case stages Fork as evidence-boundary infrastructure. Fork preserves the claim made by an upstream artifact, the non-claims that limit that artifact, the evidence references associated with the claim, and the way a downstream actor consumed or expanded the claim. Fork does not determine whether the underlying decision is true, safe, compliant, legally sufficient, clinically appropriate, financially sound, production-ready, or approved. A passing Fork verification result means the record structurally verifies within its declared boundary; it does not convert the record into substantive approval.

## Minimum record discipline

A complete use case record should include:

- a source event;
- exactly one primary supported claim;
- at least one evidence reference;
- at least one non-claim;
- a downstream consumption event;
- a preserved or dropped mapping for every upstream non-claim;
- any unresolved pointers;
- any added downstream claims;
- authority references for added downstream claims; and
- explicit limitations that prevent mapping Fork results to approval, truth, safety, compliance, or legal sufficiency.
