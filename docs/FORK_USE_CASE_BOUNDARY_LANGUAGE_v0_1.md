# Fork Use Case Boundary Language v0.1

## Status

Draft public doctrine artifact for staging Fork use cases across regulated, high-stakes, and audit-sensitive workflows.

This document is integration-hardened by **v0.1.1**. The record format remains v0.1; the v0.1.1 hardening clarifies machine-readable interpretation so downstream tools do not collapse structural validity into approval, compliance, safety, risk acceptance, control effectiveness, or truth.

## Purpose

This artifact defines the canonical boundary language that Fork use case documents and machine-readable use case records should use.

Fork use cases should not be framed as universal automation, policy enforcement, legal certification, clinical validation, safety validation, compliance validation, control-effectiveness validation, risk acceptance, or approval infrastructure. They should be framed as evidence-boundary staging records.

## Canonical Fork role

Fork is evidence-boundary infrastructure for AI-assisted governance.

Fork preserves:

- what was claimed;
- what was not claimed;
- what evidence was referenced;
- what upstream claims were relied on or rejected;
- how a downstream actor consumed the record; and
- whether the sealed record still structurally verifies later.

Fork does not determine whether the underlying claim is true, safe, legally sufficient, compliant, clinically appropriate, financially sound, production-ready, risk-accepted, control-effective, audit-ready, or approved.

## Use case staging pattern

Every Fork use case should be staged through the same five-part structure.

| Layer | Fork question |
| --- | --- |
| Source event | What artifact, workflow, or handoff occurred? |
| Supported claim | What narrow claim is actually supported by the record? |
| Non-claims | What stronger claims are explicitly not being made? |
| Consumption event | How did a downstream actor, system, or institution rely on the claim? |
| Boundary result | Was the boundary preserved, unresolved, expanded, dropped, or structurally incomplete? |

## Required boundary outcomes

Use case records should use this outcome vocabulary.

| Outcome | Meaning |
| --- | --- |
| `BOUNDARY_PRESERVED` | Downstream use stayed within the declared claim boundary. This does not indicate that the underlying decision, control, content, model, vendor, clinical workflow, cyber triage, or evidence packet is correct, safe, compliant, sufficient, risk-accepted, control-effective, audit-ready, or approved. |
| `POINTER_UNRESOLVED` | A required evidence, authority, or reference pointer could not be resolved. This is a structural resolution state, not an assessment of whether the remaining evidence is sufficient or correct. |
| `BOUNDARY_EXPANSION_DETECTED` | A downstream actor treated a narrow claim as a broader claim. This records the structural expansion; it does not determine whether the expanded claim is true, acceptable, authorized, or approved. |
| `NON_CLAIM_DROPPED` | A downstream artifact omitted one or more upstream non-claims. This is a structural boundary anomaly and should not be silently converted into approval, acceptance, or readiness. |
| `EXPANSION_AUTHORITY_REF_MISSING` | A stronger downstream claim was added without a non-empty authority reference and non-empty evidence-reference list. Fork checks pointer presence only; it does not validate authority legitimacy, sufficiency, legal effect, or approval. |
| `MAPPING_INCOMPLETE` | Preserved and dropped non-claims do not cover the upstream non-claim set. Fork does not infer whether the unmapped gaps are acceptable for any governance process. |

A valid Fork use case record may report `BOUNDARY_EXPANSION_DETECTED`, `POINTER_UNRESOLVED`, `NON_CLAIM_DROPPED`, or another adverse boundary result. Valid means the boundary record is structurally complete and interpretable. It does not mean the downstream use was approved.

## Machine-readable interpretation rule

Checker output should be read as follows:

- `ok: true` means the record is structurally valid and interpretable by the checker.
- `ok: true` does **not** mean the use case outcome was substantively acceptable.
- `boundary_preserved: true` is the machine-readable signal that the computed outcome is `BOUNDARY_PRESERVED`.
- `outcome_requires_review: true` means the computed outcome is not `BOUNDARY_PRESERVED` and should not be automatically mapped to approval, authorization, risk acceptance, compliance, safety, control effectiveness, production readiness, legal sufficiency, or truth.

Downstream systems should not gate workflow approval, vendor approval, clinical approval, deployment approval, incident closure, risk acceptance, compliance status, or audit readiness on `ok == true`.

## Required verification scope phrase

Use case records should bind verification to this phrase:

`RECORD_INTEGRITY_AND_BOUNDARY_STRUCTURE_ONLY`

This phrase prevents a structural result from being interpreted as truth, safety, compliance, approval, legal sufficiency, control effectiveness, model safety, patient safety, production readiness, or risk acceptance.

## Standard non-claim pattern

Use case records should express non-claims using stable lower-case tokens:

- `does_not_claim_truth`
- `does_not_claim_safety`
- `does_not_claim_compliance`
- `does_not_claim_legal_sufficiency`
- `does_not_claim_approval`

Domain-specific non-claims may extend this pattern. Tokens already used by v0.1 use-case fixtures include:

- `does_not_claim_audit_opinion`
- `does_not_claim_clinical_correctness`
- `does_not_claim_containment_success`
- `does_not_claim_contract_sufficiency`
- `does_not_claim_control_effectiveness`
- `does_not_claim_coverage_determination`
- `does_not_claim_generalized_performance`
- `does_not_claim_incident_scope`
- `does_not_claim_medical_necessity`
- `does_not_claim_model_safety`
- `does_not_claim_model_superiority`
- `does_not_claim_no_breach_occurred`
- `does_not_claim_patient_safety`
- `does_not_claim_production_readiness`
- `does_not_claim_remediation_sufficiency`
- `does_not_claim_reporting_obligation`
- `does_not_claim_risk_acceptance`
- `does_not_claim_security_effectiveness`
- `does_not_claim_vendor_approval`
- `does_not_claim_vendor_security`

## Prohibited readings

Fork use cases should explicitly reject the following readings:

| Prohibited reading | Boundary correction |
| --- | --- |
| Verified means true. | Verified means the record structurally verifies within the declared boundary. |
| Verified means compliant or audit-ready. | Structural verification is not a compliance determination and does not constitute an audit opinion. |
| Reviewed means approved. | Review metadata is not approval unless approval is separately claimed by an authorized actor. |
| Evidence present means compliant. | Evidence presence is not a compliance determination. |
| Evidence referenced means evidence integrity was verified. | Evidence reference recording is not evidence-authenticity, evidence-integrity, or tamper-verification unless separately claimed by an appropriate artifact. |
| Benchmark passed means safe. | Benchmark records do not generalize into model safety claims. |
| Triage found no issue means no breach occurred. | Observed evidence in a triage record is not proof of absence. |
| Packet complete means vendor approved. | Completeness of evidence inventory is not risk acceptance or vendor approval. |
| Authority reference present means authority was valid. | Fork checks structural pointer presence only; it does not validate authority legitimacy, sufficiency, legal effect, or approval. |

## Reusable use case paragraph

This use case stages Fork as evidence-boundary infrastructure. Fork preserves the claim made by an upstream artifact, the non-claims that limit that artifact, the evidence references associated with the claim, and the way a downstream actor consumed or expanded the claim. Fork does not determine whether the underlying decision is true, safe, compliant, legally sufficient, clinically appropriate, financially sound, production-ready, control-effective, risk-accepted, audit-ready, or approved. A passing Fork verification result means the record structurally verifies within its declared boundary; it does not convert the record into substantive approval.

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
- non-empty authority references for added downstream claims;
- non-empty evidence-reference lists for added downstream claims; and
- explicit limitations that prevent mapping Fork results to approval, truth, safety, compliance, control effectiveness, risk acceptance, production readiness, or legal sufficiency.

## Self-reporting limitation

Use-case boundary records make declared claim boundaries and downstream consumption behavior inspectable. They do not independently prove that a downstream actor honestly preserved every non-claim or accurately described every consumption event. A record may structurally declare non-claim preservation; Fork checks the structure of that declaration. It does not substitute for external audit, investigation, legal review, clinical review, security review, or governance review of whether the declaration was accurate.