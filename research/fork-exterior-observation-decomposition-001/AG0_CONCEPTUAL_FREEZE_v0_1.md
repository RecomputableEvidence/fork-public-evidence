# FORK-EXTERIOR-OBSERVATION-DECOMPOSITION-001 — AG0 Conceptual Freeze v0.1

**Object ID:** `FORK-EXTERIOR-OBSERVATION-DECOMPOSITION-001`  
**Short Name:** `FEOD-001`  
**Object Type:** exterior-observation decomposition and reproduction-governance object  
**Freeze Standing:** `FROZEN_FOR_THIS_VERSION`  
**Freeze Base Coordinate:** `main@56b4e064fa061417a82b7017f56d0dd98f225aa5`  
**Freeze Scope:** conceptual and execution-governance model only. `SOURCE-REVIEW-001`, proposition decomposition, coordinate evaluation, R0-R3 execution, repair, ELG admission, and research promotion remain unopened unless separately advanced.

## 1. Governing abstraction

```text
THE_DEFECTS
= HYPOTHESES

THE_HANDOFF
= OBSERVATION
```

The exterior review is a foreign observation entering Fork through an untrusted semantic boundary. Its existence and preservation establish what the reviewer asserted, not whether the assertions are true.

```text
DOCUMENT_IDENTITY
!= ASSERTION_IDENTITY

DOCUMENT_PROVENANCE
!= ASSERTION_STANDING

REVIEW_SOURCE
= AUTHORITY_FOR_WHAT_THE_REVIEWER_ASSERTED

REVIEW_SOURCE
!= AUTHORITY_FOR_WHETHER_THE_ASSERTION_IS_TRUE

COMMON_SOURCE
!= COMMON_STANDING

ADJACENT_CLAIMS
!= COUPLED_DISPOSITION
```

## 2. Opening standing

```text
SOURCE_EVENT
= OBSERVED

SOURCE_REVIEW
= AVAILABLE

SOURCE_REVIEW_PRESERVED_AS_FEOD_ARTIFACT
= NO_AT_OPEN

SOURCE_CONTENT_IDENTITY
= UNBOUND_AT_OPEN

SOURCE_FREEZE
= UNOPENED

ASSERTION_DECOMPOSITION
= UNOPENED

TECHNICAL_ASSERTION_SET
= UNESTABLISHED

NONTECHNICAL_ASSERTION_SET
= UNESTABLISHED

COORDINATE_BINDING
= UNOPENED

R0-R3_REPRODUCTION
= UNOPENED

FINDING_DISPOSITIONS
= UNOPENED

REPAIR
= UNAUTHORIZED

ELG_ADMISSION
= UNOPENED

RESEARCH_PROMOTION
= UNAUTHORIZED

INDEPENDENCE
= NOT_SCALARLY_ASSERTED
```

```text
AVAILABLE
!= PRESERVED

PRESERVED
!= DECOMPOSED

DECOMPOSED
!= TRUE
```

## 3. Required bounded artifacts

```text
SOURCE-REVIEW-001
HANDOFF-GOVERNANCE-CRITERIA-001
ASSERTION-REGISTER-001
COORDINATE-BINDING-REGISTER-001
REPRODUCTION-PLAN-001
FINDING-DISPOSITIONS-001
```

Object creation authorizes no repair, ELG entry, or successor research claim.

## 4. SOURCE-REVIEW-001

The review source must be fixed before any proposition is derived from it.

```text
SOURCE_REVIEW_CONTENT
= SHALL_BE_PRESERVED_AS_RECEIVED

SOURCE_REVIEW_CONTENT
= IMMUTABLE_AFTER_FREEZE

SOURCE_CONTENT_IDENTITY
= SHALL_BE_EXPLICITLY_BOUND
```

The frozen source shall carry at minimum:

```text
source_review_id
content_byte_length
content_sha256
source_representation
media_type
encoding_or_binary_status
normalization_status
link_handling_status
freeze_status
```

For textual capture, the canonical source is the exact preserved byte representation selected for FEOD. No newline conversion, Unicode normalization, link rewriting, rendered-text substitution, or semantic cleanup may occur after that representation is selected.

```text
AS_RECEIVED
= CANONICAL_PRESERVED_BYTE_REPRESENTATION

CANONICAL_SOURCE_BYTES
!= ABSTRACT_MESSAGE_MEANING

CONTENT_HASH
!= REPOSITORY_COORDINATE
```

Unavailable contextual metadata remains unavailable rather than inferred.

```text
MISSING_METADATA
!= LICENSE_TO_INFER
```

## 5. HANDOFF-GOVERNANCE-CRITERIA-001

Experiment B must be falsifiable before decomposition begins. The criteria artifact shall be preserved and frozen before `ASSERTION-REGISTER-001` is instantiated.

It shall record at minimum evaluator identity and relation to construction, required canonical records, required downstream representations, criterion IDs, evidence requirements, failure conditions, completion rule, overall result rule, and freeze status.

```text
EXPERIMENT_B_CRITERIA_FREEZE
PRECEDES
ASSERTION_DECOMPOSITION

POST_HOC_SUCCESS_CRITERIA
= PROHIBITED

CRITERIA_FROZEN
!= EXPERIMENT_B_PASSED
```

Required Experiment B failure classes include any observed case in which:

- a material source condition, uncertainty statement, or qualifier is silently dropped or strengthened during decomposition;
- a recommendation acquires technical-confirmation or repair-authority standing;
- review-observed and evaluation-target coordinates are conflated without an explicit relation;
- an unresolved coordinate or standing limitation is omitted from a required downstream representation;
- a Fork-derived classification is attributed to the reviewer without source support;
- a required assertion cannot be mapped recomputably to its frozen source span;
- a downstream summary or presentation materially changes the standing recorded in the canonical FEOD record.

```text
INTERNAL_PRESERVATION
!= DOWNSTREAM_PRESERVATION
```

Overall Experiment B result:

```text
FAIL
= ANY_REQUIRED_CRITERION_FAILS

PASS
= ALL_REQUIRED_CRITERIA_PASS

INCONCLUSIVE
= NO_REQUIRED_CRITERION_FAILS
  AND_AT_LEAST_ONE_REQUIRED_CRITERION_REMAINS_INCONCLUSIVE_OR_UNEVALUATED
```

## 6. ASSERTION-REGISTER-001 and source mapping

Assertion decomposition occurs only after `SOURCE-REVIEW-001` and `HANDOFF-GOVERNANCE-CRITERIA-001` are frozen.

Each proposition receives its own assertion ID and binds to the frozen source. Each bounded source-derived assertion should record at minimum:

```text
assertion_id
source_review_id
source_content_sha256
source_span_start_byte
source_span_end_byte_exclusive
representation_mode
source_qualifiers_preserved
related_assertion_ids
assertion_text
assertion_class
reviewer_basis
claimed_target
review_observed_coordinate
runtime_claim
static_analysis_claim
evaluative_content
recommendation_content
initial_standing
```

`source_span_start_byte` and `source_span_end_byte_exclusive` identify a zero-based byte range in frozen source bytes. `representation_mode` distinguishes at least `QUOTED`, `PARAPHRASED`, and `STRUCTURED_EXTRACTION`. Fork-derived classification is not reviewer assertion content.

```text
SOURCE_HASH_MATCH
!= FAITHFUL_DECOMPOSITION

FAITHFUL_DECOMPOSITION
REQUIRES
RECOMPUTABLE_SOURCE_TO_ASSERTION_MAPPING
```

Technical defect assertions begin as `EXTERIOR_TECHNICAL_ASSERTION`, not `REPRODUCED_DEFECT`.

## 7. Technical and nontechnical proposition scope

```text
ASSERTION_REGISTER
= ALL_DECOMPOSED_PROPOSITIONS

TECHNICAL_ASSERTION_SET
= R0-R3_ELIGIBLE

NONTECHNICAL_ASSERTION_SET
= NOT_FORCED_THROUGH_R0-R3
```

Technical classes ordinarily include implementation-behavior and representation-state assertions. Nontechnical classes ordinarily include architectural interpretation, research recommendation, exterior evaluation, and meta-observation unless a separately decomposable technical claim is present.

```text
RESEARCH_RECOMMENDATION
!= RUNTIME_REPRODUCTION_TARGET

EXTERIOR_EVALUATION
!= TECHNICAL_FINDING

NONTECHNICAL_PRESERVATION
!= TECHNICAL_REPRODUCTION
```

## 8. Coordinate model

The review coordinate is part of proposition identity, but the review-observed coordinate and a later FEOD evaluation coordinate are different relations.

```text
DEFECT_IDENTITY
= ASSERTION
+ COORDINATE
+ ENVIRONMENT
+ REPRODUCTION_METHOD

REVIEW_OBSERVED_COORDINATE
!= EVALUATION_TARGET_COORDINATE

ASSERTION_HOLDS_AT_EVALUATION_COORDINATE_X
!= REVIEWER_INSPECTED_COORDINATE_X
```

If the review's exact atomic coordinate cannot be recovered:

```text
REVIEW_OBSERVED_COORDINATE
= UNRESOLVED
```

A later evaluation may bind to a known commit without retroactively asserting that the reviewer inspected that commit.

```text
REPRODUCED_AT_T1
!= PRESENT_AT_T2

REPAIRED_AT_T2
!= REPRODUCED_AT_T1_ERASED
```

## 9. R0-R3 reproduction model

Technical reproduction is staged, not Boolean:

```text
R0 = SOURCE_EXISTENCE
R1 = STRUCTURAL_RECONSTRUCTION
R2 = BEHAVIORAL_POSSIBILITY
R3 = EMPIRICAL_MANIFESTATION
```

Not every technical assertion requires every stage. Before evaluation, each assertion must predeclare stage applicability and the evidence condition sufficient to disposition that bounded proposition.

```text
R_STAGE_STATUS
= PASS
| FAIL
| NOT_ATTEMPTED
| NOT_APPLICABLE
| INCONCLUSIVE

ASSERTION_EVIDENCE_REQUIREMENT
= PREDECLARED_PER_ASSERTION

R3_NOT_APPLICABLE
!= ASSERTION_UNRESOLVED
```

`NOT_APPLICABLE` requires a reason tied to the proposition. A later-stage behavior claim must be decomposed separately rather than imported into a narrower source-order proposition.

```text
SOURCE_CONFIRMED
!= DEFECT_CONFIRMED

STATIC_CONTROL_FLOW_CONFIRMED
!= RUNTIME_MANIFESTATION

BEHAVIOR_POSSIBLE
!= BEHAVIOR_OBSERVED

RUNTIME_MANIFESTATION
!= GENERAL_FAILURE_RATE
```

## 10. Technical disposition model

Technical disposition shall separate evidence results from scope, current applicability, and repair standing.

```text
TECHNICAL_DISPOSITION
= EVIDENCE_STAGE_RESULTS
+ OVERALL_EVIDENCE_DISPOSITION
+ ENVIRONMENT_SCOPE
+ COORDINATE_SCOPE
+ CURRENT_MAIN_APPLICABILITY
+ REPAIR_STATUS
```

Bounded evidence dispositions may include:

```text
SOURCE_UNRESOLVED
SOURCE_CONFIRMED
STATICALLY_REPRODUCED
BEHAVIORALLY_REACHABLE
RUNTIME_REPRODUCED
BOUNDED_PREDICTION_CONTRADICTED
PARTIALLY_REPRODUCED
INCONCLUSIVE
```

`NOT_REPRODUCED` is not a synonym for an unsuccessful attempt.

```text
EXECUTION_FAILED_TO_MANIFEST
!= CLAIM_DISPROVED

BOUNDED_PREDICTION_CONTRADICTED
REQUIRES
PREDECLARED_PREDICTION
+ VALID_TEST
+ CONTRADICTORY_OBSERVATION
```

`ENVIRONMENT_SCOPE`, `COORDINATE_SCOPE`, `CURRENT_MAIN_APPLICABILITY`, and `REPAIR_STATUS` remain orthogonal fields.

```text
RUNTIME_REPRODUCED
!= ENVIRONMENT_DEPENDENT

ENVIRONMENT_DEPENDENT
!= STALE_AT_CURRENT_MAIN

STALE_AT_CURRENT_MAIN
!= REPAIR_STATUS
```

## 11. Repair, classification, ELG, and research boundaries

```text
NO_REPAIR
UNTIL
ASSERTION-SPECIFIC_REPRODUCTION_DISPOSITION
```

A reviewer assertion does not directly authorize repair. Repair, if later authorized, creates a successor relation rather than rewriting historical standing.

```text
REPRODUCED_DEFECT
!= REPAIR_CORRECTNESS

PATCH_APPLIED
!= DEFECT_RESOLVED

REGRESSION_TEST_PASS
!= GENERAL_ABSENCE_OF_FAILURE
```

Reviewer observation remains distinct from Fork classification:

```text
REVIEWER_DISCOVERED_FAILURE
!= REVIEWER_DISCOVERED_FORK_BOUNDARY_MODEL

EXTERIOR_OBSERVATION
→ PRESERVED

FORK_CLASSIFICATION
→ SEPARATELY_DERIVED
```

ELG routing is downstream-only:

```text
EXTERIOR_ASSERTION
→ REPRODUCTION
→ DISPOSITION
→ POSSIBLE_ELG_ELIGIBILITY

EXTERIOR_REVIEW
!= ELG_ENTRY
```

A reproduced defect may become a research evidence surface, but:

```text
PHENOMENON_MATCHES_FORK_CONCERN
!= VALIDATION

EMPIRICAL_SURFACE
!= GENERALIZATION
```

## 12. Dual experimental surface

Experiment A asks whether any technical assertions are boundedly reproducible.

Experiment B asks whether Fork can govern the heterogeneous foreign handoff without collapsing source, assertion, evaluation, reproduction, repair, and research inference.

```text
VALUE_OF_REVIEW_EVENT
!= NUMBER_OF_CONFIRMED_DEFECTS

EXPERIMENT_A_RESULT
DOES_NOT_DETERMINE
EXPERIMENT_B_RESULT

PROCEDURE_FOLLOWED
!= EXPERIMENT_B_PASS
```

Experiment B evaluates both canonical FEOD records and at least one required downstream representation.

## 13. Independence model

Independence is relational, not scalar. Where relevant, record independence from object construction, fixture design, expected finding, repository authorship, Fork terminology, reproduction procedure, scoring, and repair design separately.

```text
INDEPENDENT_OF_CONSTRUCTION
!= INDEPENDENT_OF_DOCUMENTATION

INDEPENDENT_DISCOVERY
!= TOTAL_INFORMATIONAL_ISOLATION
```

No label such as `INDEPENDENT_REVIEW` supplies independence standing by itself.

## 14. Opening gates

Before assertion decomposition:

```text
SOURCE-REVIEW-001
MUST_BE
PRESERVED_AND_FROZEN

SOURCE-REVIEW-001
MUST_HAVE
EXPLICIT_CONTENT_IDENTITY

HANDOFF-GOVERNANCE-CRITERIA-001
MUST_BE
PRESERVED_AND_FROZEN

ASSERTION-REGISTER-001
MUST_BIND_TO
FROZEN_SOURCE-REVIEW-001
```

Before technical reproduction:

```text
ASSERTION-REGISTER-001
MUST_BE
INSTANTIATED_FROM_FROZEN_SOURCE

TECHNICAL_AND_NONTECHNICAL_SCOPE
MUST_BE
EXPLICIT

TARGET_TECHNICAL_ASSERTION
MUST_HAVE
ASSERTION-SPECIFIC_COORDINATE_BINDING
OR
EXPLICIT_COORDINATE_UNRESOLVED_STANDING

TARGET_TECHNICAL_ASSERTION
MUST_HAVE
PREDECLARED_STAGE_APPLICABILITY
AND
ASSERTION_RESOLUTION_CRITERION
```

Before ELG admission:

```text
NO_ELG_ADMISSION
FROM
SOURCE_REVIEW_ALONE
```

Before research promotion:

```text
NO_GENERAL_CLAIM
FROM
DEFECT_MATCH_ALONE
```

## 15. Governing sequence

```text
EXTERIOR_OBSERVATION_ARRIVES
→ SOURCE_AVAILABLE
→ SOURCE_REVIEW_CONTENT_PRESERVED
→ SOURCE_CONTENT_IDENTITY_BOUND
→ SOURCE_FREEZE
→ HANDOFF_GOVERNANCE_CRITERIA_FROZEN
→ PROPOSITIONS_DECOMPOSED
→ ASSERTIONS_BOUND_TO_FROZEN_SOURCE
→ TECHNICAL_NONTECHNICAL_SCOPE_SEPARATED
→ TECHNICAL_COORDINATES_BOUND
→ TECHNICAL_STANDING_WITHHELD
→ STAGE_APPLICABILITY_AND_ASSERTION_SUFFICIENCY_PREDECLARED
→ APPLICABLE_R0_R3_STAGES_EVALUATED_IN_ORDER
→ ASSERTION_SPECIFIC_TECHNICAL_DISPOSITION
→ OPTIONAL_REPAIR_AUTHORIZATION
→ OPTIONAL_SUCCESSOR_RESPONSE
→ OPTIONAL_ELG_ROUTING
→ OPTIONAL_RESEARCH_ANALYSIS
```

No arrow transfers standing automatically.

## 16. Core invariant

```text
LAYER_N
DOES_NOT_INHERIT_STANDING
FROM_LAYER_N-1
WITHOUT_AN_EXPLICIT_BRIDGE
```

This includes:

```text
UNFROZEN_SOURCE
!= VALID_ASSERTION_DERIVATION_BASE

SOURCE_HASH_MATCH
!= FAITHFUL_DECOMPOSITION

REVIEW_OBSERVED_COORDINATE
!= EVALUATION_TARGET_COORDINATE

INTERNAL_PRESERVATION
!= DOWNSTREAM_PRESERVATION

REPRODUCED
!= REPAIR_AUTHORIZED

REPAIRED
!= HISTORICAL_FAILURE_ERASED

PRESERVED_RECOMMENDATION
!= AUTHORIZED_RECOMMENDATION
```

## 17. Freeze boundary

The following are design decisions frozen for this version, not declarations of operational success:

```text
FEOD_001_CONCEPTUAL_MODEL
= FROZEN_FOR_THIS_VERSION

DOCUMENT_VS_ASSERTION_BOUNDARY
= FROZEN_FOR_THIS_VERSION

R0_R3_MODEL
= FROZEN_FOR_THIS_VERSION

TEMPORAL_COORDINATE_MODEL
= FROZEN_FOR_THIS_VERSION

REPAIR_SUCCESSOR_MODEL
= FROZEN_FOR_THIS_VERSION

ELG_BOUNDARY
= FROZEN_FOR_THIS_VERSION

RESEARCH_NONPROMOTION
= FROZEN_FOR_THIS_VERSION

INDEPENDENCE_MODEL
= RELATIONAL_AND_FROZEN_FOR_THIS_VERSION

SOURCE_AVAILABILITY_VS_PRESERVATION
= FROZEN_FOR_THIS_VERSION

TECHNICAL_VS_NONTECHNICAL_DISPOSITION_SCOPE
= FROZEN_FOR_THIS_VERSION

SOURCE_FREEZE_BEFORE_ASSERTION_DECOMPOSITION
= FROZEN_FOR_THIS_VERSION

SOURCE_CONTENT_PRESERVATION_NORMATIVITY
= FROZEN_FOR_THIS_VERSION

EXPERIMENT_B_FALSIFIABILITY
= FROZEN_FOR_THIS_VERSION

ORTHOGONAL_TECHNICAL_DISPOSITION_FIELDS
= FROZEN_FOR_THIS_VERSION

STAGE_APPLICABILITY_AND_ASSERTION_SUFFICIENCY
= FROZEN_FOR_THIS_VERSION

SOURCE_TO_ASSERTION_MAPPING
= FROZEN_FOR_THIS_VERSION

REVIEW_VS_EVALUATION_COORDINATE
= FROZEN_FOR_THIS_VERSION
```

```text
OPERATIONAL_VALIDITY
= NOT_YET_ESTABLISHED

IMPLEMENTATION_PRESSURE
MAY_DISCLOSE
SUCCESSOR_REPAIR_REQUIREMENTS
```

Successor implementation work may operationalize this model. It may not silently expand the standing of this frozen version. Implementation-disclosed ambiguity or defect becomes successor evidence rather than a rewrite of this freeze.
