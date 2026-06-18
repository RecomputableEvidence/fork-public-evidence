
# Claim Inheritance Simulation Model v0.1

**Status:** Draft doctrine model
**Artifact ID:** `CLAIM_INHERITANCE_SIMULATION_MODEL_v0_1`
**Depends on:** `schemas/fork_controlled_vocabulary_v0_1.schema.json`
**Vocabulary baseline:** `fork-controlled-vocabulary-hardening-v0.1.1`
**Purpose:** Define synthetic simulation classes for inspecting claim-boundary inheritance behavior across handoffs.

---

## 1. Purpose

This document defines a bounded simulation model for claim-boundary inheritance.

The model is designed to test whether a downstream system preserves, narrows, expands, rejects, drops, collapses, or leaves unresolved the claim boundary it receives from an upstream artifact.

The simulation model does not test whether any claim is true, lawful, safe, compliant, medically correct, clinically appropriate, authorized, approved, enforceable, admissible, or legally sufficient.

It tests whether a claim-boundary representation remains inspectable across synthetic handoffs.

---

## 2. Relationship to controlled vocabulary

This model uses the hardened Fork controlled vocabulary defined in:

```text
schemas/fork_controlled_vocabulary_v0_1.schema.json
```

The simulation model is downstream of the controlled vocabulary. It does not introduce new primary primitives where the vocabulary already defines them.

The following vocabulary terms are especially load-bearing for this model:

```text
CLAIM
NON_CLAIM
SYSTEM_ASSERTION
CLAIM_REFERENCED
CLAIM_USED_AS_SUPPORT
CLAIM_NON_USAGE_DECLARED
HANDOFF_EVENT
PROVENANCE_REF
AUTHORITY_REF
EVIDENCE_REF
RECORD_STRUCTURAL_STATE
RECOMPUTATION_STATE
RECORD_PERSISTENCE_STATE
BOUNDARY_BEHAVIOR
STRUCTURAL_OUTCOME
AGGREGATE_POSTURE
```

The model uses `CLAIM_REFERENCED`, `CLAIM_USED_AS_SUPPORT`, and `CLAIM_NON_USAGE_DECLARED` to avoid collapsing reference into support use.

Reference is not support use. Support use is not legal reliance. Declared non-usage is not verified non-use.

---

## 3. Non-claims

This simulation model does not claim:

* legal sufficiency;
* admissibility;
* evidentiary admissibility;
* legal authentication;
* legal attribution;
* legal custody;
* legal chain of custody;
* legal provenance;
* legal reliance;
* legal representation;
* legal retention compliance;
* legal hold compliance;
* e-discovery preservation;
* regulatory compliance;
* policy sufficiency;
* safety;
* production readiness;
* medical correctness;
* clinical appropriateness;
* authority validity;
* reference truth;
* complete provenance;
* actual downstream behavior;
* intellectual-property license;
* legal claim status;
* insurance claim status;
* patent claim status;
* cause of action;
* entitlement;
* truth.

The simulation model records synthetic structural behavior. It does not adjudicate the underlying domain.

---

## 4. Definition of CLAIM for this model

`CLAIM` means a bounded statement asserted by a system, actor, model, workflow, or artifact about a subject.

In this model, `CLAIM` does not mean:

* legal claim;
* insurance claim;
* patent claim;
* cause of action;
* demand;
* entitlement;
* assertion of legal right.

A simulated claim may be referenced, used as support, rejected, narrowed, expanded, or left unresolved. None of those states establishes legal reliance, legal representation, authority, correctness, or truth.

---

## 5. Claim relationship states

### 5.1 `CLAIM_REFERENCED`

`CLAIM_REFERENCED` means the downstream artifact includes, cites, links, summarizes, quotes, or otherwise points to an upstream claim without declaring that the upstream claim supports a downstream assertion.

A referenced claim remains visible, but reference alone does not indicate dependency.

### 5.2 `CLAIM_USED_AS_SUPPORT`

`CLAIM_USED_AS_SUPPORT` means the downstream artifact declares that it used an upstream claim as support, context, basis, or input for a downstream assertion or output.

This is a computational or representational dependency state. It is not legal reliance.

### 5.3 `CLAIM_NON_USAGE_DECLARED`

`CLAIM_NON_USAGE_DECLARED` means the downstream artifact declares that it did not use the upstream claim as support for its output.

Fork records the declaration. Fork does not verify actual non-use.

A structurally conformant `CLAIM_NON_USAGE_DECLARED` record may still coexist with undisclosed actual downstream usage. That is why `SIM_L_STRUCTURALLY_VALID_MISLEADING_SELF_REPORT` remains part of this model.

### 5.4 `CLAIM_RELATIONSHIP_NOT_DECLARED`

`CLAIM_RELATIONSHIP_NOT_DECLARED` means the downstream artifact did not declare whether the upstream claim was referenced, used as support, or not used.

This is not treated as a positive state. It contributes to incomplete mapping unless a later artifact provides the missing boundary relation.

---

## 6. Boundary behavior records

The simulation model represents handoff behavior per claim.

A single handoff may contain multiple `boundary_behavior_record` objects because a downstream system can preserve one claim, narrow another, expand another, reject another, and drop non-claims on another.

A scalar handoff result is not sufficient for this model.

Each synthetic `boundary_behavior_record` should carry:

```json
{
  "claim_ref": "synthetic_claim_001",
  "claim_relationship_state": "CLAIM_USED_AS_SUPPORT",
  "consumer_declared_boundary_behavior": "BOUNDARY_PRESERVED",
  "validator_observed_boundary_behavior": "BOUNDARY_EXPANSION_DETECTED",
  "preserved_non_claims": [
    "does_not_claim_truth"
  ],
  "dropped_non_claims": [
    "does_not_claim_legal_sufficiency"
  ],
  "authority_refs": [],
  "evidence_refs": [],
  "structural_outcomes": [
    "BOUNDARY_EXPANSION_DETECTED",
    "NON_CLAIM_DROPPED",
    "AUTHORITY_REF_MISSING",
    "MAPPING_INCOMPLETE"
  ]
}
```

The `consumer_declared_boundary_behavior` field records the downstream system's self-characterization.

The `validator_observed_boundary_behavior` field records the boundary behavior visible from the synthetic structure being inspected.

A mismatch between the two produces:

```text
DECLARED_BEHAVIOR_MISMATCH_DETECTED
```

The mismatch does not prove intent, fraud, negligence, or bad faith. It only records a structural inconsistency between declared and observable boundary behavior.

---

## 7. Resolution states

Authority and evidence references are structural references.

A structurally reachable authority reference does not mean legally valid authority.

A structurally reachable evidence reference does not mean evidentiary sufficiency.

The model uses the following distinction:

```text
*_RECORDED_RESOLUTION_NOT_PERFORMED
```

means a reference was recorded, but no resolution attempt was made by the inspecting process.

```text
*_RESOLUTION_ATTEMPTED_UNREACHABLE
```

means the inspecting process attempted structural reachability and could not reach the reference.

```text
*_STRUCTURALLY_REACHABLE
```

means the inspecting process could structurally reach the reference. It does not mean the reference was true, authoritative, legally sufficient, admissible, policy-sufficient, or domain-correct.

```text
*_STRUCTURAL_MISMATCH_DETECTED
```

means the reference did not structurally match the expected pointer, digest, schema, or relation. It does not determine legal invalidity.

---

## 8. Aggregate posture rules

Aggregate posture summarizes structural boundary mapping across one or more boundary behavior records.

Aggregate posture is not a compliance score, safety score, approval state, sufficiency state, truth state, or production readiness state.

### 8.1 Precedence order

The simulation model uses this precedence order:

1. `NO_MAPPING_PRESENT_PRECEDENCE`
2. `AGGREGATE_COLLAPSE_PRECEDENCE`
3. `INCOMPLETE_MAPPING_PRECEDENCE`
4. `UNRESOLVED_REFERENCES_PRECEDENCE`
5. `EXPANSION_MAPPING_PRESENT_PRECEDENCE`
6. `BOUNDARY_MAPPING_COMPLETE_PRECEDENCE`
7. `STRUCTURAL_CONFORMANCE_CONFIRMED_PRECEDENCE`

Higher-precedence issues prevent lower-precedence positive summaries from becoming the aggregate posture.

### 8.2 Aggregate posture outcomes

| Aggregate posture                   | Meaning                                                                                                                                                                                                        |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NO_MAPPING_PRESENT`                | No boundary mapping records were supplied.                                                                                                                                                                     |
| `AGGREGATE_COLLAPSE_DETECTED`       | A report, dashboard, summary, or schema layer collapsed unresolved, incomplete, expanded, or mixed states into an overly simple summary.                                                                       |
| `INCOMPLETE_MAPPING`                | Required boundary data, non-claim tracking, authority references, evidence references, or per-claim behavior records are missing.                                                                              |
| `MAPPED_WITH_UNRESOLVED_REFERENCES` | Boundary mapping exists, but one or more references remain unresolved or resolution was not performed.                                                                                                         |
| `EXPANSION_MAPPING_PRESENT`         | Expansion was detected or recorded and remains visible in the mapping.                                                                                                                                         |
| `BOUNDARY_MAPPING_COMPLETE`         | Per-claim boundary mapping exists and required non-claim preservation/drop states are represented.                                                                                                             |
| `STRUCTURAL_CONFORMANCE_CONFIRMED`  | Required structural checks completed without detected schema, hash, mapping, or recomputation mismatch. This does not mean truth, safety, compliance, admissibility, authority validity, or legal sufficiency. |

---

## 9. Validator emission expectations

This document is not the checker implementation. It defines expected structural behavior for future fixtures and tests.

A future checker should emit `MAPPING_INCOMPLETE` when:

* a downstream artifact adds a new claim without an authority reference;
* a downstream artifact adds a new claim without an evidence reference;
* a required claim relationship state is missing;
* a required per-claim boundary behavior record is missing;
* non-claims are neither preserved nor explicitly marked as dropped;
* unresolved pointers are collapsed into positive structural summaries;
* aggregate summaries omit unresolved, incomplete, expanded, or mixed per-claim states.

A future checker should emit `AUTHORITY_REF_MISSING` when a new or expanded claim requires an authority reference and none is supplied.

A future checker should emit `EVIDENCE_REF_MISSING` when a new or expanded claim requires an evidence reference and none is supplied.

A future checker should emit `DECLARED_BEHAVIOR_MISMATCH_DETECTED` when the downstream self-characterization differs from structurally observable boundary behavior.

A future checker should emit `AGGREGATE_COLLAPSE_DETECTED` when unresolved, incomplete, expanded, rejected, or mixed states are omitted from an aggregate report or collapsed into a positive structural summary.

---

## 10. Synthetic simulation class catalog

The following simulation classes are synthetic inheritance classes. They are not risk classes, compliance classes, approval classes, or legal classes.

### 10.1 Summary table

| Class                                                       | Name                                                 | Primary behavior                                                                                     |
| ----------------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `SIM_A_BOUNDARY_PRESERVED`                                  | Boundary preserved                                   | Claim and non-claims travel without expansion.                                                       |
| `SIM_B_BOUNDARY_NARROWED`                                   | Boundary narrowed                                    | Downstream claim is narrower than upstream claim.                                                    |
| `SIM_C_NON_CLAIM_DROPPED`                                   | Non-claim dropped                                    | Claim travels but one or more non-claims disappear.                                                  |
| `SIM_D_EXPANSION_WITHOUT_AUTHORITY`                         | Expansion without authority                          | Downstream adds claim scope without required authority reference.                                    |
| `SIM_E_EXPANSION_WITH_RECORDED_UNRESOLVED_AUTHORITY`        | Expansion with unresolved authority                  | Downstream adds claim scope and records a reference that remains unresolved or uninspected.          |
| `SIM_F_POINTER_UNRESOLVED`                                  | Pointer unresolved                                   | Claim boundary depends on an unresolved reference.                                                   |
| `SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED`  | Self-characterization mismatch: dropped non-claim    | Consumer says preserved; validator observes dropped non-claim.                                       |
| `SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED` | Self-characterization mismatch: expansion            | Consumer says preserved; validator observes expansion.                                               |
| `SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED`  | Self-characterization mismatch: narrowed vs expanded | Consumer says narrowed; validator observes expansion.                                                |
| `SIM_H_CASCADING_INHERITANCE`                               | Cascading inheritance                                | Multi-hop claim transmission accumulates boundary changes.                                           |
| `SIM_I_BOUNDARY_REJECTION`                                  | Boundary rejection                                   | Downstream explicitly rejects one or more upstream claims.                                           |
| `SIM_J_SCHEMA_BEHAVIOR_COLLAPSE`                            | Schema behavior collapse                             | Schema or representation collapses distinct per-claim behaviors into one insufficient field.         |
| `SIM_K_MULTI_BEHAVIOR_HANDOFF`                              | Multi-behavior handoff                               | One handoff contains preserved, narrowed, expanded, rejected, and unresolved records.                |
| `SIM_L_STRUCTURALLY_VALID_MISLEADING_SELF_REPORT`           | Structurally valid misleading self-report            | Receipt is structurally conformant but self-report may not reflect actual behavior.                  |
| `SIM_M_AGGREGATE_COLLAPSE`                                  | Aggregate collapse                                   | Reporting layer collapses incomplete, unresolved, mixed, or expanded states into a positive summary. |

---

## 11. Class definitions

### 11.1 `SIM_A_BOUNDARY_PRESERVED`

**Pattern:** The downstream artifact carries the upstream claim and preserves all attached non-claims.

**Expected relationship state:** `CLAIM_USED_AS_SUPPORT` or `CLAIM_REFERENCED`, depending on the synthetic case.

**Expected boundary behavior:** `BOUNDARY_PRESERVED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
BOUNDARY_PRESERVED
BOUNDARY_MAPPING_COMPLETE
```

**Expected aggregate posture:** `BOUNDARY_MAPPING_COMPLETE`

**Non-claim:** This does not prove the claim is true or sufficient.

---

### 11.2 `SIM_B_BOUNDARY_NARROWED`

**Pattern:** The downstream artifact uses a narrower statement than the upstream claim.

Example:

```text
Upstream claim: The synthetic workflow event was observed.
Downstream claim: The synthetic workflow event timestamp was observed.
```

**Expected boundary behavior:** `BOUNDARY_NARROWED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
BOUNDARY_NARROWED
BOUNDARY_MAPPING_COMPLETE
```

**Expected aggregate posture:** `BOUNDARY_MAPPING_COMPLETE`

**Non-claim:** Narrowing does not prove the narrower claim is true.

---

### 11.3 `SIM_C_NON_CLAIM_DROPPED`

**Pattern:** The downstream artifact carries the upstream claim but drops one or more non-claims.

Example:

```text
Upstream non-claim: does_not_claim_legal_sufficiency
Downstream mapping: non-claim absent and not marked as dropped
```

**Expected boundary behavior:** `NON_CLAIM_DROPPED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
NON_CLAIM_DROPPED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

**Non-claim:** This does not determine whether downstream legal sufficiency exists. It only records that the inherited non-claim did not travel.

---

### 11.4 `SIM_D_EXPANSION_WITHOUT_AUTHORITY`

**Pattern:** The downstream artifact adds claim scope without supplying an authority reference.

Example:

```text
Upstream claim: The synthetic event was observed.
Downstream claim: The synthetic event was observed and satisfies institutional review requirements.
```

**Expected boundary behavior:** `BOUNDARY_EXPANSION_DETECTED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
BOUNDARY_EXPANSION_DETECTED
AUTHORITY_REF_MISSING
EVIDENCE_REF_MISSING
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

**Non-claim:** This does not prove the expanded claim is false. It only records that the expansion is not structurally supported inside the mapping.

---

### 11.5 `SIM_E_EXPANSION_WITH_RECORDED_UNRESOLVED_AUTHORITY`

**Pattern:** The downstream artifact adds claim scope and supplies an authority reference or evidence reference, but resolution was not performed or remains unreachable.

**Expected boundary behavior:** `BOUNDARY_EXPANSION_RECORDED`

**Expected structural outcomes may include:**

```text
BOUNDARY_MAPPING_PRESENT
BOUNDARY_EXPANSION_RECORDED
AUTHORITY_REF_RECORDED_RESOLUTION_NOT_PERFORMED
EVIDENCE_REF_RECORDED_RESOLUTION_NOT_PERFORMED
MAPPED_WITH_UNRESOLVED_REFERENCES
```

or:

```text
BOUNDARY_MAPPING_PRESENT
BOUNDARY_EXPANSION_RECORDED
AUTHORITY_REF_RESOLUTION_ATTEMPTED_UNREACHABLE
EVIDENCE_REF_RESOLUTION_ATTEMPTED_UNREACHABLE
MAPPED_WITH_UNRESOLVED_REFERENCES
```

**Expected aggregate posture:** `MAPPED_WITH_UNRESOLVED_REFERENCES`

**Non-claim:** A recorded reference does not mean authority validity, evidence sufficiency, or truth.

---

### 11.6 `SIM_F_POINTER_UNRESOLVED`

**Pattern:** The downstream artifact depends on a pointer that remains unresolved.

**Expected boundary behavior:** `POINTER_UNRESOLVED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
POINTER_UNRESOLVED
MAPPED_WITH_UNRESOLVED_REFERENCES
```

**Expected aggregate posture:** `MAPPED_WITH_UNRESOLVED_REFERENCES`

**Non-claim:** Unresolved does not mean false. It means the referenced boundary cannot be structurally inspected from the available artifact set.

---

### 11.7 `SIM_G1_SELF_CHARACTERIZATION_PRESERVED_NON_CLAIM_DROPPED`

**Pattern:** The downstream artifact declares `BOUNDARY_PRESERVED`, but the mapping shows that one or more upstream non-claims were dropped.

**Consumer-declared behavior:**

```text
BOUNDARY_PRESERVED
```

**Validator-observed behavior:**

```text
NON_CLAIM_DROPPED
```

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
DECLARED_BEHAVIOR_MISMATCH_DETECTED
NON_CLAIM_DROPPED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

---

### 11.8 `SIM_G2_SELF_CHARACTERIZATION_PRESERVED_EXPANSION_OBSERVED`

**Pattern:** The downstream artifact declares `BOUNDARY_PRESERVED`, but structurally observable output adds claim scope.

**Consumer-declared behavior:**

```text
BOUNDARY_PRESERVED
```

**Validator-observed behavior:**

```text
BOUNDARY_EXPANSION_DETECTED
```

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
DECLARED_BEHAVIOR_MISMATCH_DETECTED
BOUNDARY_EXPANSION_DETECTED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

---

### 11.9 `SIM_G3_SELF_CHARACTERIZATION_NARROWED_EXPANSION_OBSERVED`

**Pattern:** The downstream artifact declares that it narrowed the claim boundary, but structurally observable output expands claim scope.

**Consumer-declared behavior:**

```text
BOUNDARY_NARROWED
```

**Validator-observed behavior:**

```text
BOUNDARY_EXPANSION_DETECTED
```

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
DECLARED_BEHAVIOR_MISMATCH_DETECTED
BOUNDARY_EXPANSION_DETECTED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

---

### 11.10 `SIM_H_CASCADING_INHERITANCE`

**Pattern:** A claim travels through multiple downstream systems, and boundary changes accumulate across hops.

Example:

```text
System A emits bounded claim with non-claims.
System B references the claim and preserves non-claims.
System C uses the claim as support and drops a non-claim.
System D expands the claim and supplies unresolved references.
```

**Expected behavior:** Each hop gets its own boundary behavior records.

**Expected structural outcomes may include:**

```text
BOUNDARY_PRESERVED
CLAIM_REFERENCED
CLAIM_USED_AS_SUPPORT
NON_CLAIM_DROPPED
BOUNDARY_EXPANSION_RECORDED
MAPPED_WITH_UNRESOLVED_REFERENCES
```

**Expected aggregate posture:** Highest-precedence applicable posture, usually `INCOMPLETE_MAPPING` or `MAPPED_WITH_UNRESOLVED_REFERENCES`.

**Non-claim:** A later structurally complete hop does not repair an earlier incomplete hop unless the missing boundary data is explicitly supplied and mapped.

---

### 11.11 `SIM_I_BOUNDARY_REJECTION`

**Pattern:** The downstream system explicitly rejects one or more upstream claims.

**Expected boundary behavior:** `CLAIM_REJECTED`

**Expected structural outcomes:**

```text
BOUNDARY_MAPPING_PRESENT
CLAIM_REJECTED
BOUNDARY_MAPPING_COMPLETE
```

**Expected aggregate posture:** `BOUNDARY_MAPPING_COMPLETE` when the rejection is explicit, per-claim, and non-claims remain accounted for.

**Non-claim:** Rejection does not prove the upstream claim is false. It records that the downstream artifact did not inherit the claim as support.

---

### 11.12 `SIM_J_SCHEMA_BEHAVIOR_COLLAPSE`

**Pattern:** A schema, adapter, or representation collapses multiple per-claim boundary behaviors into one field.

Example:

```text
Input records:
- claim_001 preserved
- claim_002 narrowed
- claim_003 expanded
- claim_004 unresolved

Collapsed output:
- handoff_status: mapped
```

**Expected boundary behavior:** `SCHEMA_BEHAVIOR_COLLAPSE_DETECTED`

**Expected structural outcomes:**

```text
SCHEMA_BEHAVIOR_COLLAPSE_DETECTED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `INCOMPLETE_MAPPING`

**Non-claim:** Collapse detection does not prove the downstream system acted improperly. It records that the representation cannot preserve required boundary distinctions.

---

### 11.13 `SIM_K_MULTI_BEHAVIOR_HANDOFF`

**Pattern:** One handoff contains multiple claim-boundary behaviors.

Example:

```text
claim_001: preserved
claim_002: narrowed
claim_003: expanded without authority reference
claim_004: rejected
claim_005: pointer unresolved
```

**Expected behavior:** The simulation requires one boundary behavior record per claim.

**Expected structural outcomes may include:**

```text
BOUNDARY_PRESERVED
BOUNDARY_NARROWED
BOUNDARY_EXPANSION_DETECTED
AUTHORITY_REF_MISSING
CLAIM_REJECTED
POINTER_UNRESOLVED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** Highest-precedence applicable posture, usually `INCOMPLETE_MAPPING`.

**Non-claim:** A preserved claim in the same handoff does not sanitize an expanded or unresolved claim.

---

### 11.14 `SIM_L_STRUCTURALLY_VALID_MISLEADING_SELF_REPORT`

**Pattern:** A downstream artifact is structurally conformant and complete according to its supplied fields, but the self-report may not reflect actual downstream behavior.

This class preserves Fork's boundary: Fork records declared and structurally observable behavior. Fork does not verify actual undisclosed internal behavior unless that behavior becomes structurally observable through supplied evidence.

**Expected structural outcomes may include:**

```text
BOUNDARY_MAPPING_PRESENT
STRUCTURAL_CONFORMANCE_CONFIRMED
```

When an inconsistency is structurally observable, the expected structural outcomes include:

```text
DECLARED_BEHAVIOR_MISMATCH_DETECTED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** Depends on whether the misleading behavior is structurally observable.

**Non-claim:** A structurally conformant self-report is not proof of actual downstream behavior.

---

### 11.15 `SIM_M_AGGREGATE_COLLAPSE`

**Pattern:** A reporting layer receives multiple receipts or boundary behavior records and collapses incomplete, unresolved, expanded, rejected, or mixed states into an overly simple aggregate.

Example:

```text
Input:
- receipt_001: BOUNDARY_MAPPING_COMPLETE
- receipt_002: MAPPED_WITH_UNRESOLVED_REFERENCES
- receipt_003: INCOMPLETE_MAPPING
- receipt_004: EXPANSION_MAPPING_PRESENT

Collapsed summary:
- total_mapped: 4
```

**Expected boundary behavior:** `AGGREGATE_COLLAPSE_DETECTED`

**Expected structural outcomes:**

```text
AGGREGATE_COLLAPSE_DETECTED
MAPPING_INCOMPLETE
```

**Expected aggregate posture:** `AGGREGATE_COLLAPSE_DETECTED`

**Non-claim:** Aggregate collapse detection does not prove intent, negligence, or substantive error. It records that the aggregate representation erased boundary-relevant distinctions.

---

## 12. Fixture design constraints

Simulation fixtures should be synthetic and domain-neutral.

Fixture names should use neutral labels such as:

```text
synthetic_claim_001
synthetic_non_claim_001
synthetic_handoff_001
synthetic_authority_ref_001
synthetic_evidence_ref_001
synthetic_receipt_001
```

Fixtures should avoid domain outcomes such as:

```text
approved
authorized
compliant
safe
clinically appropriate
legally sufficient
production ready
```

Synthetic fixture payloads should not imitate a real statutory process, medical process, legal process, insurance process, employment process, credit process, or regulatory process.

The simulation model may use abstract examples, but implementation fixtures should remain structurally synthetic.

---

## 13. Expected implementation sequence

Recommended implementation sequence:

1. Add `schemas/claim_inheritance_simulation_model_v0_1.schema.json`.
2. Add synthetic examples for each `SIM_*` class.
3. Add checker logic for per-claim boundary behavior records.
4. Add checker logic for authority and evidence reference states.
5. Add checker logic for aggregate posture precedence.
6. Add tests for each simulation class.
7. Add regression tests for aggregate collapse.
8. Add regression tests proving that unresolved or incomplete mappings do not collapse into positive summaries.
9. Add regression tests proving that reference does not collapse into support use.
10. Add regression tests proving that declared non-usage is recorded as a declaration, not verified actual non-use.

This document defines the model. It does not claim implementation completion.

---

## 14. Readiness criteria before schema implementation

Before the simulation schema is generated, the following criteria should hold:

* The controlled vocabulary schema parses as JSON.
* The controlled vocabulary schema includes `CLAIM_REFERENCED`.
* The controlled vocabulary schema includes `CLAIM_USED_AS_SUPPORT`.
* The controlled vocabulary schema includes `CLAIM_NON_USAGE_DECLARED`.
* The controlled vocabulary schema includes `AUTHORITY_REF_STRUCTURALLY_REACHABLE`.
* The controlled vocabulary schema includes `EVIDENCE_REF_STRUCTURALLY_REACHABLE`.
* The controlled vocabulary schema includes `STRUCTURAL_CHECK_PASSED`.
* The controlled vocabulary schema includes `RECORD_PRESENT_AT_STRUCTURAL_INSPECTION`.
* The controlled vocabulary schema includes `AGGREGATE_COLLAPSE_DETECTED`.
* The controlled vocabulary schema includes `SIM_M_AGGREGATE_COLLAPSE`.
* The controlled vocabulary schema includes `aggregate_posture_precedence`.
* The controlled vocabulary schema includes `boundary_behavior_record`.
* The controlled vocabulary schema includes machine-readable non-claims.
* The controlled vocabulary schema avoids legally loaded primitive names.
* The controlled vocabulary schema avoids authority-verification and truth-verification labels.

---

## 15. Final boundary statement

The claim inheritance simulation model exists to make boundary expansion, narrowing, rejection, non-claim dropping, unresolved references, schema collapse, aggregate collapse, and misleading self-characterization inspectable.

It does not make Fork a legal oracle, compliance oracle, authority oracle, safety oracle, truth oracle, or production-readiness oracle.

Fork records claim-boundary behavior. It does not decide the substantive correctness of the claim.
