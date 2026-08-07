# Fork RFC 0 — Model Evolution and Evidence Governance v0.1

```yaml
artifact:
  name: Fork RFC 0
  title: Model Evolution and Evidence Governance
  version: "0.1"
  instantiated_at: "2026-08-06"
  author: Ryan Feller
  capacity: INDIVIDUAL

status: PROVISIONAL_GOVERNANCE_SPECIFICATION
conceptual_phase: CLOSED
next_phase: EMPIRICAL_VALIDATION
change_authority:
  state: DEFINED_NOT_YET_EXERCISED
```

## 1. Purpose

This RFC defines how a versioned Fork candidate model may be preserved, challenged, reduced, extended, clarified, reclassified, superseded, or retained unchanged.

Its authority is procedural. It governs model continuity, the admission of change evidence, the preservation of research records, and the issuance of successor versions.

It does not determine whether an external claim, transformation, classification, decision, institution, or implementation is substantively correct.

> Governance authority is not evidentiary authority.

## 2. Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative within this RFC.

## 3. Scope boundary

RFC 0 governs:

- version immutability;
- attributable change authorization;
- evidence-backed extension;
- evidence-backed compression;
- preservation of observations, diagnoses, disagreements, dispositions, failures, and negative results;
- independent challenge;
- scoped standing; and
- self-application.

RFC 0 does not define:

- the truth of an external object;
- the universal meaning of a transformation;
- institutional, scientific, legal, or regulatory acceptance;
- runtime execution authority;
- model-monitoring or approval authority; or
- substantive correctness.

## 4. Core governance requirements

### 4.1 Version immutability

Once frozen or published, a model version **MUST NOT** be retroactively rewritten. A substantive change **MUST** create an explicitly identified successor version. Historical versions **MUST** remain reconstructable within their declared scope.

### 4.2 Extension gate

No primitive, invariant, relation, vector, event type, mandatory field, or equivalent conceptual element **MAY** enter a successor candidate model without an admitted inadequacy witness.

An inadequacy witness **MUST** preserve a real operational case, independently supplied corpus case, deterministic counterexample, adversarial fixture, rule contradiction, or distinguishability failure demonstrating that the frozen model cannot represent or evaluate a materially distinct evidentiary phenomenon without at least one of:

- ambiguity;
- contradiction;
- material information loss; or
- prohibited implication.

A discrepancy alone is not an inadequacy witness.

### 4.3 Compression gate

A concept **MUST** be considered for reduction or demotion when admitted evidence shows that it is:

- derivable from existing concepts without material loss;
- redundant;
- observationally indistinguishable;
- unnecessary for declared conformance; or
- incapable of exposing an independent failure class.

Permitted dispositions include removal in a successor version, demotion to a derived rule, relocation to a profile, relocation to a representation or implementation layer, collapse into another concept, historical preservation, or unresolved retention.

### 4.4 Minimal remediation

An authorized successor change **MUST** be the smallest change sufficient to address the admitted evidence. A change authorization **MUST NOT** silently bundle unrelated conceptual changes.

### 4.5 Symmetric evidence gate

Any conceptual change requires:

```yaml
conceptual_change_gate:
  evidence_record:
    one_or_more_of:
      - failure_ledger_entry
      - negative_result_entry

  analysis:
    one_or_more_of:
      - adequacy_analysis
      - compression_analysis

  required:
    - governance_disposition
    - attributable_change_authorization
    - explicit_successor_version
```

### 4.6 Implementation non-authority

Undocumented behavior of any implementation **MUST NOT** become normative merely because it exists. Reference implementations, checkers, schemas, examples, and fixtures possess only their declared standing.

### 4.7 Explicit unresolved state

Governance **MUST NOT** force closure when evidence is insufficient. `UNRESOLVED`, `LOCUS_DISPUTED`, `NOT_REPRODUCED`, `NO_CHANGE`, and other bounded non-closure outcomes **MUST** remain representable where applicable.

## 5. Classification provenance

A transformation classification is not an intrinsic property attached directly to a transformation. It is the result of an attributable classification event.

The provisional dependency is:

\[
\text{Transformation} \rightarrow \text{Classification Event} \rightarrow \text{Classification Result}
\]

Every admitted classification result **MUST** remain bound to:

- evaluator identity and evaluator type;
- performed-at time;
- source and target identities;
- transformation identity;
- procedure and version;
- declared profile or explicit profile unavailability;
- bounded evidence basis;
- assumptions and unresolved conditions;
- scope; and
- reproducibility standing.

The presence of a classification in a Fork-compatible record **MUST NOT** independently confer truth, authority, correctness, or conformance.

Evaluator disagreement **MUST** be preserved. Results **MUST NOT** be collapsed solely by majority vote or evaluator prestige.

## 6. Failure Ledger

The Failure Ledger is append-only and preserves three separate histories.

### 6.1 Observation history

An observation answers: **What was recorded as occurring?**

It **MUST** preserve source and target identities, transformation identity or description, environment, versions, raw artifacts or references, execution status, time, and reproduction information.

It **MUST NOT** silently contain evaluator conclusions. Corrections **MUST** be new linked events, not edits that erase the earlier observation.

### 6.2 Diagnosis history

A diagnosis answers: **What might explain the observation?**

It **MUST** identify the evaluator, procedure, evidence basis, asserted failure loci, uncertainty, competing explanations, and any supersession relation.

Failure locus is plural. Supported combinations **MUST NOT** be forced into a single cause.

Initial locus vocabulary:

```yaml
failure_locus:
  - IMPLEMENTATION_FAILURE
  - SPECIFICATION_AMBIGUITY
  - VOCABULARY_INSUFFICIENCY
  - CONSTITUTIONAL_INSUFFICIENCY
  - PROFILE_INSUFFICIENCY
  - INPUT_INSUFFICIENCY
  - PROCEDURE_DIVERGENCE
  - FIXTURE_DEFECT
  - LEGITIMATE_UNRESOLVED
```

### 6.3 Disposition history

A disposition answers: **What was procedurally decided?**

Initial disposition vocabulary:

```yaml
disposition:
  - IMPLEMENTATION_REPAIR
  - SPECIFICATION_CLARIFICATION
  - PROFILE_REVISION
  - FIXTURE_CORRECTION
  - MODEL_EXTENSION
  - MODEL_REDUCTION
  - NO_CHANGE
  - UNRESOLVED_PRESERVATION
```

A disposition **MUST** identify its authority, procedure, evidence basis, linked diagnoses, limitations, disagreements, and any resulting change authorization.

Observation, diagnosis, and disposition **MUST NOT** be treated as interchangeable standing.

## 7. Negative Results Register

The Negative Results Register is a first-class research artifact with standing independent of the Failure Ledger. It **MUST** preserve tested concepts, intended distinctions, existing concepts tested, derivation or redundancy arguments, corpus or experimental results, reviewers, dispositions, and reopening conditions.

A rejected or demoted proposal **MUST NOT** be erased. It **MAY** be reopened only when new evidence materially defeats or makes inapplicable the original rejection basis.

## 8. Change authority

Change authority maintains procedural integrity and version continuity. It may:

- determine whether required evidence records exist;
- accept, reject, or preserve dispute concerning an inadequacy or compression analysis;
- approve a disposition;
- issue a successor version; and
- record unresolved disagreement.

It may not, by governance action alone, establish universal correctness, completeness, semantic truth, legality, compliance, institutional acceptance, or permanent finality.

Every model transition **MUST** have an attributable change-authorization record containing:

```yaml
change_authorization:
  authorization_id:
  proposal_ids: []
  baseline_version:
  successor_version:
  evidence_basis:
    inadequacy_witnesses: []
    negative_results_considered: []
  review_record:
    procedure:
    reviewers: []
    conflicts: []
    disagreements: []
  disposition:
    type: EXTEND | REDUCE | CLARIFY | RECLASSIFY | NO_CHANGE
    affected_components: []
  limitations:
    unresolved_questions: []
  authorized_by:
  authorized_at:
```

## 9. Model standing

```yaml
model_standing:
  - PROVISIONAL_RESEARCH_BASELINE
  - INDEPENDENTLY_VALIDATED_BASELINE
  - HISTORICAL_VERSION
```

`INDEPENDENTLY_VALIDATED_BASELINE` means only that a model version completed its declared corpus evaluation, reduction review, and independent challenge requirements within its declared scope.

It does not imply universal correctness, completeness, institutional acceptance, legal validity, or permanent finality.

Advancement in standing **MUST** satisfy a previously declared independent-challenge procedure and **MUST** be recorded as an attributable governance event. Standing **MUST NOT** be inferred from elapsed time, implementation use, publication, popularity, or the absence of known objections.

## 10. Self-application

Fork's governance artifacts, classification procedures, model changes, standing changes, and evaluations are subject to Fork's own rules concerning attribution, versioning, non-retroactivity, scoped conclusions, non-inheritance, and unresolved preservation.

No Fork-produced classification or governance record receives special evidentiary standing merely because Fork produced it.

## 11. Research cycle

The governed cycle is:

\[
\boxed{
\text{Freeze} \rightarrow
\text{Observe} \rightarrow
\text{Reproduce} \rightarrow
\text{Diagnose} \rightarrow
\text{Test Adequacy} \rightarrow
\text{Govern} \rightarrow
\text{Compress or Extend} \rightarrow
\text{Independently Reproduce}
}
\]

These are procedural events, not a scalar standing ladder. A case may remain unresolved, be found inapplicable, fail reproduction, or receive `NO_CHANGE` without progressing through every named event.

## 12. Closing rule

> Fork does not change because a concept is elegant. Fork changes only when preserved evidence demonstrates that the frozen model is insufficient or unnecessarily complex, and an attributable governance action authorizes the smallest justified successor transition.

