# Controlled Pilot Synthetic Corpus Structural Outcome Hardening v0.1.1

## Purpose

Controlled Pilot Synthetic Dry-Run Corpus v0.1 introduced a synthetic-only corpus for exercising Fork controlled-pilot dry-run paths.

This hardening document narrows how the corpus may be interpreted.

The purpose of v0.1.1 is to prevent structural dry-run outcomes and healthcare-adjacent synthetic terminology from being misread as domain validation, live-ingestion authorization, clinical judgment, legal sufficiency, regulatory compliance, HIPAA compliance, source truth, or real institutional workflow fidelity.

This document does not replace the v0.1 corpus document.

It binds the v0.1 corpus to a stricter structural-outcome interpretation.

## Status

This document defines the v0.1.1 structural-outcome hardening requirements for the Controlled Pilot Synthetic Dry-Run Corpus.

The hardening is not complete merely because this document exists.

v0.1.1 is complete only when the acceptance criteria in this document are satisfied by the corpus documentation, package index, checker receipts, invalid fixtures, and test suite.
## Mandatory structural-only banner

All uses of the synthetic dry-run corpus are governed by the following banner:

```text
PASS, INDETERMINATE, and FAIL are structural evidence-boundary outcomes only.

They are not medical, legal, regulatory, clinical, coverage, authorization, fairness, source-truth, production-readiness, live-ingestion, or compliance determinations.
```

The banner applies to:

- corpus documentation;
- manifest interpretation;
- checker receipts;
- release notes;
- demonstrations;
- screenshots;
- downstream explanations;
- any controlled-pilot dry-run review using the corpus.

## Not-representative statement

The corpus is not representative of any real-world healthcare, payer, provider, member, patient, claim, appeal, authorization, utilization-management, compliance, legal, regulatory, or institutional source-system process.

The corpus does not model, simulate, reproduce, mirror, replay, certify, validate, or approximate any real:

- payer workflow;
- provider workflow;
- member workflow;
- patient record;
- medical record;
- claim;
- prior-authorization request;
- denial;
- appeal;
- internal review;
- external review;
- clinical policy;
- utilization-management standard;
- plan rule;
- jurisdictional rule;
- regulatory regime;
- legal standard;
- institutional export;
- live ingestion path.

Any healthcare-adjacent labels in the corpus exist only to provide a recognizable synthetic payload shape for evidence-boundary testing.

They do not create domain authority.

## Structural outcome contract

The v0.1 corpus uses three expected outcomes:

- PASS
- INDETERMINATE
- FAIL

In v0.1.1, these are interpreted only through the following structural contract.

### Structural PASS

PASS means only that the synthetic record preserves the expected evidence boundary for its class.

A structural PASS may indicate that:

- required synthetic-only flags are present;
- required canonical non-claims are preserved;
- no unresolved pointer is present where none is expected;
- no attempted expansion claim is present where none is permitted;
- the record matches the expected structural class;
- the checker did not detect a prohibited structural violation.

A structural PASS does not mean:

- the synthetic denial was medically correct;
- the synthetic appeal was legally sufficient;
- the synthetic record was clinically appropriate;
- the synthetic workflow was compliant;
- the synthetic workflow was fair;
- the synthetic source was true;
- the synthetic source was complete;
- live ingestion is authorized;
- any real-world process has been validated.

### Structural INDETERMINATE

INDETERMINATE means only that the synthetic record intentionally contains unresolved pointer state without detected boundary expansion.

A structural INDETERMINATE may indicate that:

- the record is synthetically bounded;
- at least one required unresolved pointer is present;
- canonical non-claims remain preserved;
- the unresolved state prevents safe collapse into structural PASS;
- no explicit attempted expansion claim was detected.

A structural INDETERMINATE does not mean:

- a medical outcome is uncertain;
- legal sufficiency is uncertain;
- compliance is uncertain;
- clinical correctness is uncertain;
- a real source system is incomplete;
- a real workflow needs escalation;
- Fork has evaluated the underlying domain issue.

### Structural FAIL

FAIL means only that the synthetic record violates a structural boundary rule.

A structural FAIL may indicate that:

- an attempted expansion claim is present;
- required non-claims were not preserved;
- a class label conflicts with record content;
- a prohibited PII-like pattern was detected;
- unresolved pointer requirements were violated;
- synthetic-only flags were violated;
- the record attempted to convert bounded evidence into a claim Fork does not make.

A structural FAIL does not mean:

- a payer was wrong;
- a provider was wrong;
- a denial was improper;
- an appeal should succeed;
- a legal claim is valid;
- a regulatory violation occurred;
- a medical decision was incorrect;
- a real-world workflow failed.

## Domain terminology boundary

The corpus may use healthcare-adjacent terms only as synthetic payload labels.

Those labels must not be interpreted as claims of:

- healthcare-domain competence;
- payer-domain competence;
- utilization-management sufficiency;
- clinical review capability;
- medical necessity determination;
- claim adjudication;
- appeal adjudication;
- coverage determination;
- HIPAA compliance;
- legal review;
- regulatory review;
- production workflow readiness.

The controlled-pilot corpus tests evidence-boundary behavior over synthetic payloads.

It does not test whether the payload is medically, legally, clinically, operationally, or regulatorily correct.

## Required disclaimer propagation

Any document, release note, checker receipt, or package index entry that describes this corpus MUST preserve the following statement or an equivalent stricter statement:

> This corpus tests structural evidence-boundary behavior only. It does not validate clinical logic, legal sufficiency, regulatory compliance, HIPAA compliance, payer workflow fidelity, provider workflow fidelity, authorization correctness, appeal correctness, source truth, source completeness, production readiness, or live-ingestion authorization.

This statement should appear before any reader encounters PASS, INDETERMINATE, or FAIL labels.

## Adversarial fixture hardening targets

v0.1.1 should add or prepare the following invalid fixture classes.

Class A, Class B, and Class C refer to the structural fixture classes defined in Controlled Pilot Synthetic Dry-Run Corpus v0.1.

### Invalid Class A overclaim

Purpose: Detect records labeled as bounded preservation that introduce domain claims.

Example prohibited patterns include claims that a synthetic action:

- was medically necessary;
- met coverage criteria;
- satisfied a plan rule;
- was legally sufficient;
- was HIPAA compliant;
- was authorized for live ingestion.

Expected checker result: **FAIL**

### Invalid class mislabel

Purpose: Detect records whose declared class conflicts with their structural content.

Examples:

- Class A label with unresolved pointer behavior;
- Class A label with attempted expansion behavior;
- Class B label without unresolved pointer behavior;
- Class C label without attempted expansion behavior.

Expected checker result: **FAIL**

### Invalid encoded PII-like content

Purpose: Detect attempts to hide PII-like content through encoding or formatting.

Examples:

- base64-encoded SSN-like token;
- URL-encoded email-like token;
- phone-like string embedded in a non-obvious field;
- identifier-like string hidden in metadata;
- synthetic field name containing real-contact-like text.

Expected checker result: **FAIL**

### Invalid pointer cycle

Purpose: Detect unresolved pointer structures that are circular, self-referential, or alias-based.

Examples:

- pointer refers to its own `event_id`;
- pointer A refers to pointer B and pointer B refers to pointer A;
- unresolved pointer is presented as unresolved while resolvable inside the same corpus;
- pointer chain creates unbounded traversal risk.

Expected checker result: **FAIL**

### Invalid real-regime reference

Purpose: Detect synthetic records that name real institutions, real payers, real providers, real plans, real statutes, real regulations, real cases, or real source-system exports in a way that could imply real-world provenance or domain fidelity.

Expected checker result: **FAIL**

## Checker hardening requirements

The synthetic corpus checker should preserve the existing v0.1 validations and add structural-outcome hardening.

At minimum, the checker should verify:

- `expected_rgv_result` is a structural outcome label only;
- PASS records do not include unresolved pointers or attempted expansion claims;
- INDETERMINATE records include unresolved pointer state and no attempted expansion claims;
- FAIL records include a structural failure reason or prohibited expansion condition;
- class labels and structural content are consistent;
- canonical non-claims are preserved exactly;
- synthetic-only flags remain enforced;
- PII-like text patterns are rejected;
- encoded PII-like content is rejected for explicitly supported bounded decoders, including base64 and URL encoding. The checker does not claim universal detection of all possible encodings, obfuscations, or hidden identifiers;
- circular or self-referencing pointers are rejected;
- real-regime and real-institution references are rejected when they appear as synthetic payload provenance, source-system identity, institutional identity, authority basis, fixture content, or domain-fidelity evidence. This does not prohibit canonical non-claim language or doctrine text from naming examples such as HIPAA, legal sufficiency, or regulatory compliance for boundary-preservation purposes;
- checker receipts repeat structural-only non-claims.

## Receipt hardening requirements

Synthetic corpus validation receipts should not emit bare PASS, INDETERMINATE, or FAIL without structural qualification.

Receipts should include:

```json
{
  "outcome_interpretation": "STRUCTURAL_EVIDENCE_BOUNDARY_ONLY"
}
```

Receipts should preserve non-claims equivalent to:

```json
[
  "DOES_NOT_CLAIM_MEDICAL_CORRECTNESS",
  "DOES_NOT_CLAIM_LEGAL_SUFFICIENCY",
  "DOES_NOT_CLAIM_REGULATORY_COMPLIANCE",
  "DOES_NOT_CLAIM_HIPAA_COMPLIANCE",
  "DOES_NOT_CLAIM_SOURCE_TRUTH",
  "DOES_NOT_AUTHORIZE_LIVE_INGESTION",
  "DOES_NOT_USE_REAL_PATIENT_DATA",
  "DOES_NOT_CLAIM_REAL_WORLD_WORKFLOW_FIDELITY",
  "DOES_NOT_CLAIM_DOMAIN_REPRESENTATIVENESS"
]
```

## Package index hardening requirement

The controlled pilot package index should include this document as a required hardening document for the controlled pilot synthetic dry-run corpus.

Recommended component entry:

```json
{
  "component_id": "controlled_pilot_synthetic_corpus_structural_outcome_hardening",
  "component_type": "DOCUMENT",
  "path": "docs/CONTROLLED_PILOT_SYNTHETIC_CORPUS_STRUCTURAL_OUTCOME_HARDENING_v0_1_1.md",
  "required": true
}
```

## Acceptance criteria

v0.1.1 hardening is complete when:

- this hardening document exists;
- the v0.1 corpus document references the structural-only outcome contract;
- the package index includes this hardening document;
- the checker rejects at least:
  - Class A overclaim;
  - class/content mislabel;
  - encoded PII-like content;
  - circular or self-referencing pointer;
  - real-regime or real-institution reference;
- checker receipts include structural-only outcome interpretation;
- tests cover all new invalid fixtures;
- the full repository test suite passes;
- release notes state that v0.1.1 hardens interpretation and adversarial coverage without converting the corpus into a clinical, legal, regulatory, compliance, or live-ingestion system.

## Non-claims

This hardening document does not claim that Fork provides:

- medical review;
- legal review;
- regulatory review;
- compliance certification;
- HIPAA certification;
- clinical correctness;
- coverage determination;
- claim adjudication;
- appeal adjudication;
- utilization-management sufficiency;
- source truth;
- source completeness;
- live-ingestion authorization;
- production readiness;
- real-world workflow fidelity;
- domain representativeness.

Fork remains evidence-boundary infrastructure.

The controlled pilot synthetic dry-run corpus remains synthetic-only test material.

## Summary

v0.1 established the synthetic dry-run corpus.

v0.1.1 hardens the interpretation layer.

The central rule is:

> Structural outcomes are not domain outcomes.

Fork may preserve, compare, and verify evidence-boundary structure.

Fork does not convert synthetic healthcare-adjacent dry-run records into clinical, legal, regulatory, compliance, authorization, or source-truth claims.
