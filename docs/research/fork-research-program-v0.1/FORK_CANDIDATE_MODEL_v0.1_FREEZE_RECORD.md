# Fork Candidate Model v0.1 — Freeze Record

```yaml
artifact:
  name: Fork Candidate Model
  version: "0.1"
  record_type: FREEZE_RECORD
  instantiated_at: "2026-08-06"
  author: Ryan Feller
  capacity: INDIVIDUAL

standing: PROVISIONAL_RESEARCH_BASELINE
conceptual_phase: CLOSED
empirical_phase: ACTIVE
canonical_binding:
  standalone_artifact_binding: COMPLETE_AFTER_DIGEST_GENERATION
  repository_binding: UNRESOLVED_PENDING_REPOSITORY_ADMISSION
  admitted_evaluation: BLOCKED_PENDING_REPOSITORY_BINDING

governance_binding:
  artifact: Fork RFC 0 — Model Evolution and Evidence Governance
  version: "0.1"
```

## 1. Freeze declaration

This record identifies the provisional model entering empirical evaluation. Version 0.1 is historically immutable once bound. It is not protected from reduction, extension, reclassification, or supersession in a governed successor version.

No new primitive, invariant, relation, vector, event type, mandatory field, or equivalent conceptual element may enter Candidate Model v0.1 after this freeze.

Discussion and hypotheses remain permitted with `PROPOSAL_ONLY` standing. They do not alter this version.

## 2. Included evidentiary states

```yaml
states:
  - source_state
  - target_state
  - historical_state
  - published_state
  - evaluated_state
```

These identify historically situated records. Their presence does not establish truth, equivalence, correctness, or authority transfer.

## 3. Included transformation record

```yaml
transformation_record:
  required_surfaces:
    - transformation_event
    - transformation_identity
    - transformation_method
    - transformation_version
    - transformation_scope
```

The transformation record preserves the occurrence or assertion of an operation connecting source and target states. It does not intrinsically contain a relation classification or conformance conclusion.

## 4. Included classification-event record

The status of `classification_event` is resolved as follows:

```yaml
classification_event_status:
  state: INCLUDED_IN_PROVISIONAL_BASELINE
  category: EVALUATION_RECORD_TYPE
  ontological_role: ATTRIBUTABLE_CLASSIFICATION_EVENT
  primitive_relation_property: false
```

A classification event records an evaluator's attributable description of a transformation. It binds the result to the evaluator, time, source and target identities, transformation identity, procedure, profile status, evidence basis, assumptions, unresolved conditions, scope, and standing.

This inclusion makes explicit an evaluation structure already required by the model's evaluator classifications and disagreement records. It does not declare that the classification is intrinsic, true, correct, conforming, or authoritative.

The provisional schema is `schemas/classification-event-v0.1.schema.yaml`.

## 5. Observational relation vocabulary under test

```yaml
relations:
  - PRESERVED
  - NARROWED
  - EXPANDED
  - OMITTED
  - SPLIT
  - MERGED
  - SUPERSEDED
  - CONTRADICTED
  - RE_ESTABLISHED
  - LOSSY
  - UNRESOLVED
```

These values are classification results produced by attributable classification events. They do not independently establish truth, legality, authority, correctness, compliance, usefulness, or institutional acceptance.

## 6. Classification comparison vocabulary under test

```yaml
classification_comparison:
  - AGREEMENT
  - PARTIAL_AGREEMENT
  - MATERIAL_DISAGREEMENT
  - PROFILE_DIVERGENCE
  - PROCEDURAL_DIVERGENCE
  - UNRESOLVED
```

Comparison values describe relations among preserved classification events. They do not automatically select a winning classification.

## 7. Constitutional invariants under test

```yaml
invariants:
  - historical_states_are_not_retroactively_rewritten
  - authority_does_not_silently_inherit_across_transitions
  - absence_does_not_silently_become_presence
  - evaluation_scope_does_not_exceed_declared_object_scope
  - semantic_expansion_requires_attributable_basis
  - recomputability_does_not_imply_substantive_correctness
```

Each invariant has `PROVISIONAL_RESEARCH_BASELINE` standing. None is immune from governed compression, clarification, or rejection in a successor version.

## 8. Failure and negative-result structures

The model includes the following research-record structures:

```yaml
research_records:
  failure_ledger:
    histories:
      - observation
      - diagnosis
      - disposition
  negative_results_register:
    purpose: preserve_reduction_rejection_and_reopening_basis
```

Observation, diagnosis, and disposition are independent histories. Their presence or acceptance must not silently transfer standing to one another.

## 9. Explicit unresolved and excluded proposals

```yaml
unresolved_proposals:
  - proposal_id: assumption_record
    standing: PROPOSAL_ONLY
    admission_condition: >-
      Preserved evidence must demonstrate that existing states,
      classification bases, ledgers, or governance artifacts cannot
      adequately represent the relevant hidden dependency.

  - proposal_id: separate_conformance_receipt_as_model_object
    standing: PROPOSAL_ONLY
    admission_condition: >-
      Preserved evidence must demonstrate that profile-bound evaluation
      cannot be adequately represented by the current evaluation records.

excluded_interpretations:
  - classification_as_intrinsic_transformation_property
  - majority_vote_as_automatic_truth_resolution
  - evaluator_prestige_as_substitute_for_basis
  - recomputability_as_substantive_correctness
  - governance_authorization_as_truth_authority
```

## 10. Binding requirement

The exact standalone artifacts are listed in `baseline_manifest_v0.1.yaml` and bound by SHA-256. Repository identity, commit SHA, and tree digest remain unresolved until repository admission.

No corpus case may receive admitted evaluation standing while repository binding is unresolved.

```yaml
binding_gate:
  required_before_admitted_evaluation:
    - repository_identity
    - commit_sha
    - tree_digest
    - normative_artifact_hashes
    - schema_hashes
    - procedure_hashes
    - fixture_manifest_hash
```

## 11. Symmetric successor gate

Conceptual extension or compression is prohibited without:

```yaml
successor_gate:
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
    - successor_version
```

## 12. Non-claims

This freeze does not establish:

- model completeness or correctness;
- universal applicability;
- empirical validation;
- independent validation;
- production readiness;
- legal validity or compliance;
- institutional acceptance;
- substantive truth of any classification; or
- authority to control an observed workflow.

## 13. Final determination

Candidate Model v0.1 is instantiated as a frozen, provisional research baseline. The conceptual phase is closed. The next legitimate source of model change is preserved evidence admitted and governed under Fork RFC 0.

