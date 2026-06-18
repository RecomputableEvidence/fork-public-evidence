# Legal Language for Claim Boundary Inheritance v0.1

## Status and Mandatory Non-Claims

This document is a position paper and terminology artifact.

It defines a controlled vocabulary for evidence-boundary engineering.

This document does not constitute legal advice.

This document does not create an attorney-client relationship.

This document does not claim to define legal sufficiency, admissibility, enforceability, liability, regulatory compliance, evidentiary admissibility, hearsay exception status, retention compliance, or legal authentication for any jurisdiction or context.

Terms borrowed from legal frameworks, including but not limited to reliance, attribution, representation, authentication, retention, custody, and provenance, are used in Fork-defined engineering senses.

Fork does not claim that its use of these terms constitutes legal analysis, produces legally operative records, or maps one-to-one to any legal doctrine.

The terminology defined here maps legal concepts to structural engineering states.

It does not confer legal effect upon those structural states.

## Design Thesis

Legal systems already distinguish record, representation, reliance, attribution, authentication, custody, provenance, and sufficiency.

Fork translates those distinctions into a controlled engineering language for AI-assisted system handoffs, without claiming to decide legal effect.

Evidence-boundary language must be strong enough to preserve claim meaning across handoffs, but light enough to remain portable through the systems that carry it.

## Purpose

AI-assisted governance systems suffer from silent semantic expansion.

A structural verification becomes a claim of truth.

A mapped policy becomes a compliance determination.

A reviewed artifact becomes a legally sufficient decision.

A logged event becomes an approved action.

A synthetic test becomes perceived production readiness.

To prevent silent expansion, system handoffs require a vocabulary that precisely names what is happening at the boundary.

Rather than inventing this vocabulary from scratch, Fork draws structural inspiration from established evidentiary, electronic-record, chain-of-custody, provenance, and contractual concepts.

These legal frameworks already manage distinctions between the existence of a record, the verification of its structure, the attribution of its source, the custody path through which it moved, and the substantive reliance placed upon its claims.

Fork uses those distinctions as engineering primitives.

Fork does not claim legal effect.

## Legal Foundations Translated to Engineering Boundaries

Fork borrows structural inspiration, but not legal authority, from the following concepts.

### Federal Rule of Evidence 901 — Authentication

In law, authentication requires evidence sufficient to support a finding that an item is what the proponent claims it is.

In Fork, this maps to structural record verification.

Fork may provide evidence that a payload structurally matches its claimed schema, hash, receipt, or declared artifact form.

Fork does not prove that the underlying semantic claim is true.

Fork does not claim legal authentication.

### Federal Rule of Evidence 803(6) — Records of a Regularly Conducted Activity

In law, records of regularly conducted activity are associated with requirements such as timing, source knowledge, regular practice, and record context.

In Fork, this inspires temporal, source, process, and context metadata.

Fork does not claim that its records satisfy the business-records exception or any other hearsay exception.

Fork borrows the discipline of recording the context in which a boundary event occurred.

### Federal Rules of Evidence 1002 and 1003 — Originals and Duplicates

In law, originals and duplicates are treated through rules governing proof of content, authenticity concerns, and fairness.

In Fork, this maps to artifact integrity and reproduction state.

Fork distinguishes original claim payloads, duplicate reproductions, derived artifacts, and integrity mismatches.

Fork does not claim that a Fork artifact qualifies as an original or admissible duplicate.

### E-SIGN and UETA-Style Electronic Records

Electronic-record frameworks distinguish electronic form, retention, reproducibility, and attribution.

In Fork, this inspires separation between:

- existence of an electronic record;
- structural verification of the record;
- attribution of a record to a system or actor;
- reproduction of the record later;
- retention context.

Fork does not claim that any record satisfies E-SIGN, UETA, or other statutory electronic-record requirements.

### Chain of Custody

Chain-of-custody concepts address how evidence is identified, transferred, preserved, and accounted for across custodians.

This is central to evidence-boundary handoff mapping.

In Fork, this maps to system handoffs.

A `CUSTODY_EVENT` records that an artifact, claim, receipt, pointer, or boundary-bearing record moved from one system, actor, or custody context to another.

A `SYSTEM_MAPPING_RECEIPT` can preserve evidence of that handoff without claiming that legal chain-of-custody requirements are satisfied.

Fork does not claim to establish legal chain of custody.

Fork records structural custody-path information where available.

### Provenance

Provenance concerns origin, history, source context, and custody path.

In Fork, provenance is represented by references to upstream artifacts, receipts, systems, custody events, and handoff records.

A `PROVENANCE_REF` points to an origin or custody-history record.

Fork does not claim that provenance references are complete unless completeness is separately asserted and structurally verified.

### Contract Non-Reliance

Contract non-reliance language distinguishes representations made from representations relied upon.

In Fork, this distinction becomes an engineering primitive.

A downstream system may observe or reference an upstream claim without relying on it.

If it relies on the claim, that reliance should be recorded.

Fork’s `RELIANCE` primitive means reported system reliance.

It does not mean legal reliance.

### Discovery Burden and Proportionality

Discovery and ESI frameworks recognize that preservation and access obligations can be affected by burden and proportionality.

In Fork, this supports structural minimalism.

Evidence-boundary language should be strong enough to preserve meaning, but not so heavy that it overburdens the systems that carry it.

Fork does not claim discovery compliance or preservation sufficiency.

## Controlled Vocabulary Primitives

The following primitives form Fork’s engineering vocabulary for claim boundary inheritance.

They are structural mapping concepts, not legal conclusions.

### CLAIM

An assertion made by an upstream system, human, model, workflow, or artifact payload.

### NON_CLAIM

An explicit boundary constraint attached to a claim.

A non-claim states what the claim does not support.

Example:

`does_not_claim_legal_sufficiency`

A non-claim should travel with the claim unless the downstream system explicitly records that it was not preserved.

### REPRESENTATION

A structurally recorded presentation of a claim, state, source assertion, or boundary event.

In Fork, representation does not mean legal representation or contractual representation unless separately stated by a qualified authority outside Fork.

A representation may contain a claim, but not every claim is a legal representation.

### RELIANCE

A downstream consumer’s structural declaration that it used an upstream claim as support for a downstream artifact, route, summary, classification, or decision-support output.

RELIANCE does not mean legal reliance.

### NON_RELIANCE

A downstream consumer’s structural declaration that it observed or referenced an upstream artifact or claim but did not use it as support for its downstream output.

Presence is not reliance.

Reference is not reliance.

### ATTRIBUTION

Metadata linking a claim, expansion, receipt, custody event, or boundary behavior to a specific producer system, consumer system, actor identifier, or cryptographic identity.

Attribution records the asserted source of the assertion.

It does not assign legal accountability, liability, fault, negligence, or duty.

### AUTHORITY_REF

A pointer supplied by a system to designate the source of its asserted authority to make a claim or expansion.

AUTHORITY_REF does not prove authority.

It records that the downstream system supplied a reference to an asserted authority source.

### EVIDENCE_REF

A pointer supplied by a system to designate the data, logic, receipt, policy, review record, or artifact supporting a claim or expansion.

EVIDENCE_REF does not prove evidentiary sufficiency.

It records that a reference was supplied.

### RECORD_VERIFICATION_STATE

The structural condition of a referenced record or artifact.

Examples include:

- `NOT_CHECKED`
- `SUPPLIED_NOT_VERIFIED`
- `UNRESOLVED`
- `STRUCTURALLY_VERIFIED`
- `HASH_MISMATCH`
- `SCHEMA_MISMATCH`

RECORD_VERIFICATION_STATE does not mean legal authentication.

### REPRODUCTION_STATE

The status of a system’s attempt to reproduce, copy, narrow, or derive an artifact.

Examples include:

- `ORIGINAL_OBSERVED`
- `DUPLICATE_OBSERVED`
- `REPRODUCED_WITH_MATCHING_HASH`
- `REPRODUCTION_NOT_CHECKED`
- `REPRODUCTION_MISMATCH`

REPRODUCTION_STATE does not claim legal duplicate status or evidentiary admissibility.

### RETENTION_STATE

The declared retention or persistence state attached to an artifact, receipt, pointer, or system mapping record.

Examples include:

- `RETENTION_NOT_DECLARED`
- `RETENTION_DECLARED`
- `RETENTION_POINTER_SUPPLIED`
- `RETENTION_NOT_CHECKED`

RETENTION_STATE does not claim legal retention compliance.

### INTEGRITY_STATE

The result of a structural validation check against a hash, schema, receipt, boundary constraint, or manifest.

Examples include:

- `STRUCTURALLY_VERIFIED`
- `STRUCTURAL_MISMATCH`
- `HASH_MISMATCH`
- `SCHEMA_VALID`
- `SCHEMA_INVALID`
- `NOT_CHECKED`

INTEGRITY_STATE does not prove truth, safety, compliance, approval, or legal sufficiency.

### CUSTODY_EVENT

A structural record that an artifact, claim, receipt, pointer, or boundary-bearing record moved from one system, actor, or custody context to another.

A custody event may record:

- sender;
- receiver;
- timestamp;
- artifact reference;
- receipt reference;
- integrity state;
- unresolved pointers;
- non-claims preserved or dropped.

CUSTODY_EVENT does not claim legal chain of custody.

### PROVENANCE_REF

A pointer to origin, source, lineage, custody history, or upstream receipt context.

PROVENANCE_REF does not prove complete provenance unless completeness is separately asserted and structurally verified.

### BOUNDARY_BEHAVIOR

The specific action reportedly taken by a consumer system upon an inherited boundary.

Examples include:

- `BOUNDARY_PRESERVED`
- `BOUNDARY_NARROWED`
- `BOUNDARY_EXPANSION_DETECTED`
- `CLAIM_REJECTED`
- `POINTER_UNRESOLVED`
- `NON_CLAIM_DROPPED`

BOUNDARY_BEHAVIOR may be consumer-declared, validator-observed, or both.

### STRUCTURAL_OUTCOME

The validator-observed result of comparing declared boundary behavior against the claims, non-claims, authority references, evidence references, unresolved pointers, and receipt fields present in the handoff mapping.

Examples include:

- `BOUNDARY_MAPPING_PRESENT`
- `BOUNDARY_EXPANSION_RECORDED`
- `AUTHORITY_REF_MISSING`
- `EVIDENCE_REF_MISSING`
- `MAPPING_INCOMPLETE`
- `RECEIPT_STRUCTURALLY_COMPLETE`

STRUCTURAL_OUTCOME does not claim substantive correctness.

### AGGREGATE_POSTURE

A high-level summary state for the handoff, receipt, or simulation case.

Examples include:

- `NO_MAPPING_PRESENT`
- `INCOMPLETE_MAPPING`
- `MAPPED_WITH_UNRESOLVED_REFERENCES`
- `EXPANSION_MAPPED`
- `FULLY_MAPPED`
- `RECEIPT_STRUCTURALLY_COMPLETE`

AGGREGATE_POSTURE prevents unresolved pointers or missing authority references from being collapsed into a false success binary.

It does not claim approval, compliance, safety, legal sufficiency, or truth.

## Aggregate Posture Rule

A checker or simulator should compute aggregate posture from structural outcomes using explicit precedence.

Suggested v0.1 precedence:

1. If no mapping receipt exists where one is expected, emit `NO_MAPPING_PRESENT`.
2. If `MAPPING_INCOMPLETE`, `AUTHORITY_REF_MISSING`, `EVIDENCE_REF_MISSING`, `NON_CLAIM_DROPPED`, or `POINTER_UNRESOLVED` appears, emit `INCOMPLETE_MAPPING`.
3. If `BOUNDARY_EXPANSION_DETECTED` appears and no required authority or evidence reference is missing, emit `EXPANSION_MAPPED`.
4. If structural outcomes contain only `BOUNDARY_MAPPING_PRESENT`, `BOUNDARY_PRESERVED`, and optionally `BOUNDARY_NARROWED`, emit `FULLY_MAPPED`.
5. If all required fields, references, non-claim mappings, and custody/provenance pointers structurally resolve under the selected verification mode, emit `RECEIPT_STRUCTURALLY_COMPLETE`.

No aggregate posture claims legal sufficiency, compliance, admissibility, safety, institutional approval, or truth.

## Claim Inheritance Failure Modes

Fork should model recurring inheritance failures as named synthetic cases.

Examples include:

- `logged_to_verified`
- `verified_to_true`
- `reviewed_to_approved`
- `policy_cited_to_compliant`
- `human_seen_to_legally_sufficient`
- `synthetic_tested_to_production_ready`
- `upstream_safe_to_downstream_safe`

These are not legal conclusions.

They are boundary-mutation patterns.

Each pattern should be simulated as a structural transformation from a bounded upstream claim to an expanded downstream claim.

## Simulation Classes

The first claim-inheritance simulator should include at least the following synthetic classes.

### SIM_A_BOUNDARY_PRESERVED

The downstream system relies on the upstream claim and preserves all inherited non-claims.

### SIM_B_BOUNDARY_NARROWED

The downstream system relies only on a subset of the upstream claim and records the narrowed scope.

### SIM_C_NON_CLAIM_DROPPED

The downstream system relies on an upstream claim but omits one or more inherited non-claims.

Expected outcomes include:

- `NON_CLAIM_DROPPED`
- `MAPPING_INCOMPLETE`

### SIM_D_EXPANSION_WITHOUT_AUTHORITY

The downstream system adds a new claim without `AUTHORITY_REF` or `EVIDENCE_REF`.

Expected outcomes include:

- `BOUNDARY_EXPANSION_DETECTED`
- `AUTHORITY_REF_MISSING`
- `EVIDENCE_REF_MISSING`
- `MAPPING_INCOMPLETE`

### SIM_E_EXPANSION_WITH_RECORDED_UNVERIFIED_AUTHORITY

The downstream system adds a new claim and supplies authority and evidence references, but resolution was not performed.

Expected outcomes include:

- `BOUNDARY_EXPANSION_RECORDED`
- `AUTHORITY_REF_SUPPLIED_NOT_VERIFIED`
- `EVIDENCE_REF_SUPPLIED_NOT_VERIFIED`
- `MAPPED_WITH_UNRESOLVED_REFERENCES`

### SIM_F_POINTER_UNRESOLVED

The downstream system cannot resolve an upstream evidence pointer and preserves the unresolved state.

Expected outcomes include:

- `POINTER_UNRESOLVED`
- `INCOMPLETE_MAPPING`

### SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED

The consumer declares boundary preservation, but validator-observed fields show non-claim loss.

### SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED

The consumer declares boundary preservation, but validator-observed fields show boundary expansion.

### SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED

The consumer declares boundary narrowing, but validator-observed fields show expansion.

### SIM_H_CASCADING_INHERITANCE

A multi-hop simulation in which a dropped non-claim or unresolved pointer becomes the upstream context for a later handoff.

This class demonstrates how local mapping gaps can compound across an institutional chain.

## Machine-Readable Vocabulary Schema

A prose vocabulary is not enough.

A controlled vocabulary should be made machine-readable before the simulation schema is treated as canonical.

Recommended next artifact:

`schemas/fork_controlled_vocabulary_v0_1.schema.json`

This schema should enumerate controlled primitive names, allowed structural outcome values, aggregate posture values, boundary behaviors, verification states, custody/provenance fields, and required non-claims.

The simulation schema should reference this controlled vocabulary rather than redefining values ad hoc.

## Conclusion

Legal language is useful to Fork only when translated into bounded engineering terms.

Fork does not borrow legal concepts to claim legal effect.

Fork borrows them because they already distinguish records, reliance, attribution, custody, provenance, verification, and sufficiency.

Those distinctions are exactly what AI-assisted system handoffs need.

The next step is to instantiate these primitives in a synthetic claim-inheritance simulation model that shows how claims mutate when boundaries, non-claims, authority references, evidence references, custody events, and provenance references are not explicitly preserved.
