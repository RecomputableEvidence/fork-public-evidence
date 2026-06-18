
# Legal Language for Claim Boundary Inheritance v0.1

## Status and Scope

This document is a position paper and terminology artifact.

It defines legal-language inspirations and Fork-defined engineering primitives for claim boundary inheritance.

It does not claim that `SYSTEM_MAPPING_RECEIPT`, the claim-inheritance simulator, or any related artifact is fully implemented in production.

It does not claim that any Fork artifact satisfies any legal standard.

Terms defined in this document are provisional until formalized in `schemas/fork_controlled_vocabulary_v0_1.schema.json`.

The future controlled vocabulary schema takes precedence over this document if the schema and this document diverge after publication.

The simulation schema may reference terms defined here as provisional vocabulary until the controlled vocabulary schema is published.

## Mandatory Legal Non-Claims

This document does not constitute legal advice.

This document does not provide legal services.

This document does not create an attorney-client relationship.

This document does not claim to define legal sufficiency, admissibility, enforceability, liability, regulatory compliance, evidentiary admissibility, hearsay exception status, retention compliance, legal authentication, legal attribution, legal custody, legal provenance, or legal chain of custody for any jurisdiction or context.

Fork is not an e-discovery preservation tool, legal hold system, retention-compliance system, discovery-response system, or regulatory safe harbor.

Fork does not satisfy Federal Rule of Civil Procedure 26 ESI preservation duties, litigation hold obligations, statutory retention obligations, records-management obligations, or equivalent legal preservation requirements.

Fork records are not designed to satisfy, do not claim to satisfy, and should not be evaluated as satisfying any hearsay exception, including the business-records exception under Federal Rule of Evidence 803(6) or equivalent state rules.

Reference to legal concepts in this document is limited to identifying useful distinctions for engineering design.

## Borrowed Terms and Non-Claims

This document uses terms and concepts borrowed from legal frameworks in Fork-defined engineering senses only.

Borrowed concepts include, but are not limited to, record, assertion, claim use, attribution, custody, provenance, verification, recomputation, persistence, and sufficiency.

These terms do not carry the legal meaning those terms hold in their native legal contexts.

They do not create legal determinations, legal duties, legal reliance, legal attribution, legal custody, evidentiary admissibility, retention compliance, legal preservation status, or compliance status.

Fork does not claim that its use of these terms constitutes legal analysis, produces legally operative records, or maps one-to-one to any legal doctrine.

## Design Thesis

Legal systems already distinguish record, assertion, claim use, attribution, custody, provenance, verification, recomputation, persistence, and sufficiency.

Fork translates those distinctions into a controlled engineering language for AI-assisted system handoffs, without claiming to decide legal effect.

Evidence-boundary language must be strong enough to preserve claim meaning across handoffs, but light enough to remain portable through the systems that carry it.

## Purpose

AI-assisted governance systems suffer from silent semantic expansion.

A structural check becomes a claim of truth.

A mapped policy becomes a compliance determination.

A reviewed artifact becomes a legally sufficient decision.

A logged event becomes an approved action.

A synthetic test becomes perceived production readiness.

To prevent silent expansion, system handoffs require vocabulary that precisely names what is happening at the boundary.

Fork draws structural inspiration from established evidentiary, electronic-record, chain-of-custody, provenance, and contractual concepts.

These frameworks already manage distinctions between the existence of a record, the structural condition of a record, the source of an assertion, the path through which information moved, and the use placed upon a claim.

Fork uses those distinctions as engineering primitives.

Fork does not claim legal effect.

## Legal Foundations Translated to Engineering Boundaries

Fork borrows structural inspiration, but not legal authority, from the following concepts.

### Federal Rule of Evidence 901 — Authentication

In law, authentication involves evidence sufficient to support a finding that an item is what the proponent claims it is.

In Fork, this inspires structural record-state language.

Fork may provide evidence that a payload structurally matches its claimed schema, hash, receipt, or declared artifact form.

Fork does not prove that the underlying semantic claim is true.

Fork does not claim legal authentication.

Fork avoids using `AUTHENTICATION_STATE` as a primitive because that term imports legal meaning beyond Fork's claim.

The Fork-native primitive is `RECORD_STRUCTURAL_STATE`.

### Federal Rule of Evidence 803(6) — Records of a Regularly Conducted Activity

In law, records of regularly conducted activity are associated with requirements such as timing, source knowledge, regular practice, and record context.

In Fork, this inspires temporal, source, process, and context metadata.

Fork does not claim that its records satisfy the business-records exception or any other hearsay exception.

Fork borrows only the discipline of recording the context in which a boundary event occurred.

### Federal Rules of Evidence 1002 and 1003 — Originals and Duplicates

In law, originals and duplicates are treated through rules governing proof of content, authenticity concerns, and fairness.

In Fork, this inspires recomputation and structural comparison.

Fork distinguishes original observed payloads, derived artifacts, recomputed outputs, and structural mismatches.

Fork does not claim that a Fork artifact qualifies as an original or admissible duplicate.

Fork avoids using `REPRODUCTION_STATE` as a primitive because it creates unnecessary proximity to legal duplicate and reproduction concepts.

The Fork-native primitive is `RECOMPUTATION_STATE`.

### E-SIGN and UETA-Style Electronic Records

Electronic-record frameworks distinguish electronic form, persistence, reproducibility, and attribution.

In Fork, this inspires separation between:

* existence of an electronic record;
* structural state of the record;
* asserted source of a record;
* recomputation of the record later;
* declared persistence context.

Fork does not claim that any record satisfies E-SIGN, UETA, legal retention, legal preservation, legal attribution, or other statutory electronic-record requirements.

### Chain of Custody

Chain-of-custody concepts address how evidence is identified, transferred, preserved, and accounted for across custodians.

This is relevant to evidence-boundary handoff mapping.

Fork does not use `CUSTODY_EVENT` as a primitive because it may imply legal custody, legal possession, spoliation exposure, or legal chain-of-custody status.

The Fork-native primitive is `HANDOFF_EVENT`.

A `HANDOFF_EVENT` records that an artifact, claim, pointer, receipt, or boundary-bearing record moved between systems, actors, or processing contexts.

It does not establish legal custody, legal possession, legal chain of custody, evidentiary admissibility, preservation compliance, or physical custody of any physical record or evidence.

### Provenance

Provenance concerns origin, history, source context, and lineage.

In Fork, provenance is represented by references to upstream artifacts, receipts, systems, handoff events, and system-mapping records.

A `PROVENANCE_REF` points to origin or lineage context.

Fork does not claim that provenance references are complete unless completeness is separately asserted and structurally verified.

Fork does not claim legal proof of provenance.

### Contract Non-Reliance

Contract non-reliance language distinguishes statements made from statements used by another party.

Fork does not use `RELIANCE` or `NON_RELIANCE` as primitives because those terms import tort, contract, and fraud doctrine.

The Fork-native primitives are `CLAIM_USAGE` and `CLAIM_NON_USAGE`.

A downstream system may observe or reference an upstream claim without using it as support.

If it uses the claim as support for a downstream artifact, route, summary, classification, or decision-support output, that usage should be recorded.

`CLAIM_USAGE` does not mean legal reliance, detrimental reliance, justifiable reliance, reasonable reliance, or any reliance in a legal sense.

A Fork claim-usage record does not create any legal inference, duty, obligation, or liability.

### Discovery Burden and Proportionality

Discovery and ESI frameworks recognize that preservation and access obligations may involve burden and proportionality.

In Fork, this supports structural minimalism.

Evidence-boundary language should be strong enough to preserve meaning, but not so heavy that it overburdens the systems that carry it.

Fork does not claim discovery compliance, legal-hold compliance, preservation sufficiency, or regulatory safe-harbor status.

## Controlled Vocabulary Primitives

The following primitives form Fork's engineering vocabulary for claim boundary inheritance.

They are structural mapping concepts, not legal conclusions.

### CLAIM

An assertion made by an upstream system, human, model, workflow, or artifact payload.

### NON_CLAIM

An explicit boundary constraint attached to a claim.

A non-claim states what the claim does not support.

Example:

`does_not_claim_legal_sufficiency`

A non-claim should travel with the claim unless the downstream system explicitly records that it was not preserved.

### SYSTEM_ASSERTION

A system-generated statement about an artifact, process step, boundary event, source state, or structural condition.

`SYSTEM_ASSERTION` replaces `REPRESENTATION`.

It does not mean legal representation, contractual representation, warranty, disclosure, assurance, or statement made to induce action.

A system assertion may contain a claim, but it does not by itself create any legal duty, obligation, reliance, liability, or warranty.

### CLAIM_USAGE

A downstream consumer's structural declaration that it used an upstream claim as support for a downstream artifact, route, summary, classification, or decision-support output.

`CLAIM_USAGE` replaces `RELIANCE`.

It does not mean legal reliance, detrimental reliance, justifiable reliance, reasonable reliance, or reliance in any tort, contract, fraud, securities, insurance, regulatory, or evidentiary sense.

A Fork claim-usage record does not create any legal inference, duty, obligation, reliance, or liability.

### CLAIM_NON_USAGE

A downstream consumer's structural declaration that it observed or referenced an upstream artifact or claim but did not use it as support for its downstream output.

`CLAIM_NON_USAGE` replaces `NON_RELIANCE`.

Presence is not usage.

Reference is not usage.

### ATTRIBUTION_REF

A pointer or metadata value linking a claim, expansion, receipt, handoff event, or boundary behavior to an asserted producer system, consumer system, actor identifier, cryptographic identity, token, or signing context.

`ATTRIBUTION_REF` does not establish legal agency, legal authorship, vicarious liability, binding authority, legal attribution under UETA or E-SIGN, or any legal responsibility.

It records asserted source linkage only.

### AUTHORITY_REF

A pointer supplied by a system to designate the source of its asserted authority to make a claim or expansion.

`AUTHORITY_REF` does not prove authority.

It records that the downstream system supplied a reference to an asserted authority source.

### AUTHORITY_REF_RESOLUTION_STATE

The structural resolution state of an authority reference.

Suggested values include:

* `AUTHORITY_REF_MISSING`
* `AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `AUTHORITY_REF_UNRESOLVED`
* `AUTHORITY_REF_STRUCTURALLY_RESOLVED`
* `AUTHORITY_REF_STRUCTURAL_MISMATCH_DETECTED`

`AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED` means Fork recorded the reference but did not attempt resolution.

It does not mean resolution was attempted and failed.

### EVIDENCE_REF

A pointer supplied by a system to designate the data, logic, receipt, policy, review record, or artifact supporting a claim or expansion.

`EVIDENCE_REF` does not prove evidentiary sufficiency.

It records that a reference was supplied.

### EVIDENCE_REF_RESOLUTION_STATE

The structural resolution state of an evidence reference.

Suggested values include:

* `EVIDENCE_REF_MISSING`
* `EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `EVIDENCE_REF_UNRESOLVED`
* `EVIDENCE_REF_STRUCTURALLY_RESOLVED`
* `EVIDENCE_REF_STRUCTURAL_MISMATCH_DETECTED`

`EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED` means Fork recorded the reference but did not attempt resolution.

It does not mean resolution was attempted and failed.

### RECORD_STRUCTURAL_STATE

The structural condition of a referenced record or artifact.

`RECORD_STRUCTURAL_STATE` replaces `AUTHENTICATION_STATE` and `RECORD_VERIFICATION_STATE`.

Suggested values include:

* `STRUCTURALLY_INTACT`
* `STRUCTURAL_MISMATCH_DETECTED`
* `STRUCTURAL_VERIFICATION_NOT_PERFORMED`
* `HASH_MISMATCH_DETECTED`
* `SCHEMA_MISMATCH_DETECTED`

`RECORD_STRUCTURAL_STATE` does not mean legal authentication, legal verification, truth verification, substantive correctness, compliance verification, or admissibility.

### RECOMPUTATION_STATE

The status of a system's attempt to recompute, regenerate, or structurally compare an artifact from sealed or declared components.

`RECOMPUTATION_STATE` replaces `REPRODUCTION_STATE`.

Suggested values include:

* `RECOMPUTATION_NOT_PERFORMED`
* `RECOMPUTED_MATCH`
* `RECOMPUTED_MISMATCH`
* `RECOMPUTATION_INPUT_MISSING`
* `RECOMPUTATION_BLOCKED_BY_UNRESOLVED_POINTER`

`RECOMPUTATION_STATE` does not claim legal duplicate status, evidentiary admissibility, legal reproduction sufficiency, or compliance with any best-evidence rule.

### RECORD_PERSISTENCE_STATE

The declared persistence state attached to an artifact, receipt, pointer, or system mapping record.

`RECORD_PERSISTENCE_STATE` replaces `RETENTION_STATE`.

Suggested values include:

* `PERSISTENCE_NOT_DECLARED`
* `PERSISTENCE_DECLARED`
* `PERSISTENCE_POINTER_SUPPLIED`
* `PERSISTENCE_NOT_CHECKED`
* `PERSISTENCE_UNRESOLVED`

`RECORD_PERSISTENCE_STATE` does not claim legal retention compliance, legal-hold compliance, preservation sufficiency, records-management compliance, or regulatory safe-harbor status.

### HANDOFF_EVENT

A structural record that an artifact, claim, receipt, pointer, or boundary-bearing record moved between systems, actors, or processing contexts.

`HANDOFF_EVENT` replaces `CUSTODY_EVENT`.

A handoff event may record:

* sender;
* receiver;
* timestamp;
* artifact reference;
* receipt reference;
* record structural state;
* recomputation state;
* unresolved pointers;
* non-claims preserved or dropped.

`HANDOFF_EVENT` does not constitute a legal chain-of-custody record.

It does not satisfy any legal chain-of-custody requirement.

It does not support any inference of evidentiary admissibility.

It does not document physical custody of any physical record or evidence.

### PROVENANCE_REF

A pointer to origin, source, lineage, upstream receipt context, or prior handoff record.

`PROVENANCE_REF` does not prove complete provenance.

It does not guarantee legal proof of provenance, authenticity, admissibility, ownership, or custody history.

It records a technical lineage pointer only unless stronger states are separately asserted and structurally verified.

### BOUNDARY_BEHAVIOR

The specific action reportedly or structurally observed when a consumer system handles an inherited boundary.

Suggested values include:

* `BOUNDARY_PRESERVED`
* `BOUNDARY_NARROWED`
* `BOUNDARY_EXPANSION_DETECTED`
* `BOUNDARY_EXPANSION_RECORDED`
* `CLAIM_REJECTED`
* `POINTER_UNRESOLVED`
* `NON_CLAIM_DROPPED`
* `SCHEMA_BEHAVIOR_COLLAPSE_DETECTED`

Boundary behavior may be consumer-declared, validator-observed, or both.

### STRUCTURAL_OUTCOME

The validator-observed result of comparing declared boundary behavior against the claims, non-claims, authority references, evidence references, unresolved pointers, handoff records, provenance references, and receipt fields present in the handoff mapping.

Suggested values include:

* `BOUNDARY_MAPPING_PRESENT`
* `BOUNDARY_PRESERVED`
* `BOUNDARY_NARROWED`
* `BOUNDARY_EXPANSION_DETECTED`
* `BOUNDARY_EXPANSION_RECORDED`
* `CLAIM_REJECTED`
* `NON_CLAIM_DROPPED`
* `POINTER_UNRESOLVED`
* `AUTHORITY_REF_MISSING`
* `AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `EVIDENCE_REF_MISSING`
* `EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `SCHEMA_BEHAVIOR_COLLAPSE_DETECTED`
* `MAPPING_INCOMPLETE`
* `MAPPED_WITH_UNRESOLVED_REFERENCES`
* `RECEIPT_STRUCTURALLY_COMPLETE`

`STRUCTURAL_OUTCOME` does not claim substantive correctness, legal sufficiency, compliance, admissibility, authority, approval, safety, or truth.

### AGGREGATE_POSTURE

A high-level structural summary state for the handoff, receipt, simulation case, or handoff chain.

Suggested values include:

* `NO_MAPPING_PRESENT`
* `INCOMPLETE_MAPPING`
* `MAPPED_WITH_UNRESOLVED_REFERENCES`
* `EXPANSION_MAPPED`
* `FULLY_MAPPED`
* `RECEIPT_STRUCTURALLY_COMPLETE`

`AGGREGATE_POSTURE` prevents unresolved pointers, missing authority references, dropped non-claims, or boundary expansions from being collapsed into a false success binary.

It does not claim approval, compliance, safety, legal sufficiency, admissibility, institutional authorization, or truth.

## Aggregate Posture Rule

A checker or simulator should compute aggregate posture from structural outcomes using explicit precedence.

Suggested v0.1 precedence:

1. If no mapping receipt exists where one is expected, emit `NO_MAPPING_PRESENT`.
2. If `MAPPING_INCOMPLETE`, `AUTHORITY_REF_MISSING`, `EVIDENCE_REF_MISSING`, `NON_CLAIM_DROPPED`, `POINTER_UNRESOLVED`, or `SCHEMA_BEHAVIOR_COLLAPSE_DETECTED` appears, emit `INCOMPLETE_MAPPING`.
3. If `BOUNDARY_EXPANSION_DETECTED` appears with all required authority and evidence references recorded but at least one reference has `*_RECORDED_RESOLUTION_NOT_PERFORMED` or `*_UNRESOLVED`, emit `MAPPED_WITH_UNRESOLVED_REFERENCES`.
4. If `BOUNDARY_EXPANSION_DETECTED` appears and all required authority and evidence references structurally resolve under the selected verification mode, emit `EXPANSION_MAPPED`.
5. If structural outcomes contain only `BOUNDARY_MAPPING_PRESENT`, `BOUNDARY_PRESERVED`, and optionally `BOUNDARY_NARROWED`, emit `FULLY_MAPPED`.
6. If all required fields, references, non-claim mappings, handoff events, provenance references, and recomputation checks structurally resolve under the selected verification mode, emit `RECEIPT_STRUCTURALLY_COMPLETE`.

`INCOMPLETE_MAPPING` takes precedence over `BOUNDARY_MAPPING_PRESENT`.

`BOUNDARY_EXPANSION_DETECTED` takes precedence over `BOUNDARY_PRESERVED`.

`POINTER_UNRESOLVED` must not be counted as a pass state.

No aggregate posture claims legal sufficiency, compliance, admissibility, safety, institutional approval, or truth.

## Claim Inheritance Failure Modes

Fork should model recurring inheritance failures as named synthetic boundary-mutation patterns.

Examples include:

* `logged_to_verified`
* `verified_to_true`
* `reviewed_to_approved`
* `policy_cited_to_compliant`
* `human_seen_to_legally_sufficient`
* `synthetic_tested_to_production_ready`
* `upstream_safe_to_downstream_safe`

These are not legal conclusions.

They are boundary-mutation patterns.

Each pattern should be simulated as a structural transformation from a bounded upstream claim to an expanded downstream claim.

## Simulation Scope Non-Claims

Simulation classes are synthetic models of boundary behavior.

They do not represent, predict, or characterize the behavior of any actual institution, system, workflow, regulatory process, legal dispute, compliance program, or operational deployment.

The cascading inheritance simulation models how claim mutation can propagate across synthetic handoff sequences.

It does not model actual institutional failure modes.

It does not constitute a risk assessment of any workflow.

It does not predict how any regulatory body, court, auditor, investigator, or institution would evaluate a multi-system AI-assisted governance chain.

A structurally complete `SYSTEM_MAPPING_RECEIPT` may still be evidentiary evidence of an inaccurate self-report.

Fork records what systems report and what validators structurally observe.

Fork does not verify that reported boundary behavior fully or accurately reflects actual downstream behavior.

## Simulation Classes

The first claim-inheritance simulator should include at least the following synthetic classes.

### SIM_A_BOUNDARY_PRESERVED

The downstream system uses the upstream claim and preserves all inherited non-claims.

### SIM_B_BOUNDARY_NARROWED

The downstream system uses only a subset of the upstream claim and records the narrowed scope.

### SIM_C_NON_CLAIM_DROPPED

The downstream system uses an upstream claim but omits one or more inherited non-claims.

Expected outcomes include:

* `NON_CLAIM_DROPPED`
* `MAPPING_INCOMPLETE`

### SIM_D_EXPANSION_WITHOUT_AUTHORITY

The downstream system adds a new claim without `AUTHORITY_REF` or `EVIDENCE_REF`.

Expected outcomes include:

* `BOUNDARY_EXPANSION_DETECTED`
* `AUTHORITY_REF_MISSING`
* `EVIDENCE_REF_MISSING`
* `MAPPING_INCOMPLETE`

### SIM_E_EXPANSION_WITH_RECORDED_UNRESOLVED_AUTHORITY

The downstream system adds a new claim and supplies authority and evidence references, but resolution is not performed or remains unresolved.

Expected outcomes include one or more of:

* `BOUNDARY_EXPANSION_RECORDED`
* `AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED`
* `MAPPED_WITH_UNRESOLVED_REFERENCES`

### SIM_F_POINTER_UNRESOLVED

The downstream system cannot resolve an upstream evidence pointer and preserves the unresolved state.

Expected outcomes include:

* `POINTER_UNRESOLVED`
* `INCOMPLETE_MAPPING`

### SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED

The consumer declares boundary preservation, but validator-observed fields show non-claim loss.

### SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED

The consumer declares boundary preservation, but validator-observed fields show boundary expansion.

### SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED

The consumer declares boundary narrowing, but validator-observed fields show expansion.

### SIM_H_CASCADING_INHERITANCE

A multi-hop simulation in which a dropped non-claim or unresolved pointer becomes the upstream context for a later handoff.

This class demonstrates how local mapping gaps can compound across a synthetic institutional chain.

### SIM_I_BOUNDARY_REJECTION

The downstream system observes or references an upstream claim but records `CLAIM_NON_USAGE` and rejects the claim as support for downstream output.

This class demonstrates that presence is not usage and reference is not usage.

Expected outcomes include:

* `CLAIM_REJECTED`
* `BOUNDARY_MAPPING_PRESENT`

### SIM_J_SCHEMA_BEHAVIOR_COLLAPSE

A schema, checker, dashboard, or report collapses unresolved, incomplete, or expanded boundary states into a binary pass/fail or success/failure count.

This class models infrastructure behavior failure rather than consumer behavior failure.

Expected outcomes include:

* `SCHEMA_BEHAVIOR_COLLAPSE_DETECTED`
* `MAPPING_INCOMPLETE`

### SIM_K_MULTI_BEHAVIOR_HANDOFF

A single handoff preserves one claim, narrows another, expands another, drops a non-claim on another, and leaves a pointer unresolved.

This class demonstrates why per-claim boundary behavior records are necessary.

Expected outcomes may include:

* `BOUNDARY_PRESERVED`
* `BOUNDARY_NARROWED`
* `BOUNDARY_EXPANSION_DETECTED`
* `NON_CLAIM_DROPPED`
* `POINTER_UNRESOLVED`
* `MAPPING_INCOMPLETE`

### SIM_L_STRUCTURALLY_VALID_MISLEADING_SELF_REPORT

A receipt contains all required fields and is structurally complete, but the system generating it inaccurately characterizes its own boundary behavior or supplies a fabricated external authority reference that Fork cannot detect from the available structure.

This class demonstrates Fork's honest scope limit.

Expected lesson:

* structural completeness is not substantive truth;
* reference presence is not authority;
* Fork records reported behavior and structurally observable behavior;
* Fork does not verify that reported behavior fully reflects actual behavior.

## Machine-Readable Vocabulary Schema

A prose vocabulary is not enough for executable doctrine.

Recommended next artifact:

`schemas/fork_controlled_vocabulary_v0_1.schema.json`

This schema should enumerate controlled primitive names, allowed structural outcome values, aggregate posture values, boundary behaviors, reference-resolution states, handoff/provenance fields, recomputation states, record structural states, persistence states, and required non-claims.

The claim-inheritance simulation schema should reference this controlled vocabulary rather than redefining values ad hoc.

The terminology document may precede the vocabulary schema as a provisional doctrine artifact.

The simulation model should not become canonical until the controlled vocabulary schema exists.

## Conclusion

Legal language is useful to Fork only when translated into bounded engineering terms.

Fork does not borrow legal concepts to claim legal effect.

Fork borrows them because they already distinguish records, system assertions, claim usage, attribution, handoffs, provenance, structural state, recomputation, persistence, and sufficiency.

Those distinctions are exactly what AI-assisted system handoffs need.

The next step is to formalize the controlled vocabulary in machine-readable form, then instantiate these primitives in a synthetic claim-inheritance simulation model that shows how claims mutate when boundaries, non-claims, authority references, evidence references, handoff events, and provenance references are not explicitly preserved.

## Vocabulary Hardening Notes

Fork does not use CUSTODY_EVENT as a primitive because it may imply legal custody, legal possession, spoliation exposure, or legal chain-of-custody status. The Fork-native primitive is HANDOFF_EVENT.

Fork does not use RELIANCE or NON_RELIANCE as primitives because those terms import tort, contract, fraud, and reliance-doctrine meaning. The Fork-native primitives are CLAIM_USAGE and CLAIM_NON_USAGE.

SYSTEM_ASSERTION replaces REPRESENTATION because representation carries contract, fraud, warranty, securities, insurance, and disclosure meanings that Fork does not claim.


`SYSTEM_ASSERTION` replaces `REPRESENTATION` because representation carries contract, fraud, warranty, securities, insurance, and disclosure meanings that Fork does not claim.

SYSTEM_ASSERTION replaces REPRESENTATION because representation carries contract, fraud, warranty, securities, insurance, and disclosure meanings that Fork does not claim.
