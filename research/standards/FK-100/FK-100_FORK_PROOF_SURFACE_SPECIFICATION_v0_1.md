# FK-100 — Fork Proof Surface Specification

**Identifier:** FK-100  
**Title:** Fork Proof Surface Specification  
**Status:** Draft v0.1  
**Classification:** Normative  
**Question Answered:** What does Fork prove?  
**Prerequisites:** Fork Standards Architecture v0.1  
**Dependents:** BC-100 Boundary Contract Model, BC-101 AST-100 ↔ FK-100 Profile, Enterprise Workflow Examples

---

## 1. Purpose

FK-100 defines the normative proof surface for the Fork architecture. It specifies the set of claims Fork is responsible for proving and the evidence obligations required to support those claims.

Fork is a normative architecture for preserving the evidence required to independently reconstruct reliance across architectural boundaries.

Fork defines proof obligations associated with evidence-boundary preservation, reliance-context preservation, boundary-transition preservation, declared non-claim preservation, independent recomputation, structural verification, and boundary-state interoperability.

Fork does not define execution control, continuation validity, runtime governance, policy enforcement, admissibility, authority, legal sufficiency, artifact authenticity, or truth.

The core question FK-100 answers is:

> Can later reliance be independently reconstructed?

## 2. Normative Language

The key words SHALL, SHALL NOT, SHOULD, SHOULD NOT, MAY, and MUST are to be interpreted as normative when they appear in normative sections of this specification.

Informative appendices do not create additional conformance requirements.

## 3. Definitions

### 3.1 Proof Surface

A proof surface is the bounded set of normative claims an architecture asserts and is obligated to support with replayable, recomputable evidence.

### 3.2 Fork Proof Surface

The Fork proof surface includes only FK-001 through FK-007 and excludes all claims listed in the Normative Non-Proof Surface.

### 3.3 Architectural Responsibility

Fork's architectural responsibility is limited to preserving an evidentiary record sufficient to reconstruct what was relied upon, what was intentionally excluded, and how information crossed architectural boundaries; and enabling deterministic structural verification and independent recomputation of that preserved record.

Architectural responsibility SHALL NOT extend to execution authorization, policy evaluation, or determination of correctness.

### 3.4 Boundary Contract

A boundary contract is a declared specification that defines how artifacts produced by an external proof surface may be consumed as evidence by Fork without transferring authority or proof obligations.

### 3.5 External Proof Surface

An external proof surface is an architecture independent of FK-100 that defines its own proof obligations and evidence requirements. Fork SHALL treat all external proof surfaces as independent.

### 3.6 Independent Recomputation

Independent recomputation is the ability to re-derive Fork's structural claims from preserved evidence without requiring the original execution environment, runtime authority, or external system state.

### 3.7 Structural Verification

Structural verification is the process of checking that preserved records remain structurally consistent over time. Structural verification SHALL NOT be interpreted as proof of truth, legal sufficiency, policy compliance, or artifact authenticity beyond structural integrity.

### 3.8 Evidence-Boundary Preservation

Evidence-boundary preservation is the preservation of artifacts, metadata, and boundary decisions at architectural seams, including what crossed, what did not cross, what was excluded, and the conditions under which the boundary event occurred.

### 3.9 Reliance Context

Reliance context is the recorded relationship between actors or systems and the evidence they relied upon.

### 3.10 Declared Non-Claim

A declared non-claim is an explicit statement that a system, actor, artifact, or proof surface does not assert a particular responsibility, property, sufficiency, truth, authority, or conclusion.

### 3.11 Boundary Transition

A boundary transition is a recorded movement, consumption, exclusion, or transformation of evidence across an architectural seam. A boundary transition does not transfer authority.

## 4. Architectural Principles (FP-00x)

### FP-001 — No Unsupported Claims

Fork SHALL NOT assert any claim that cannot be supported by preserved, replayable evidence within its proof surface.

### FP-002 — Evidence Before Interpretation

Fork SHALL prioritize preservation and recomputation of evidence over semantic interpretation or policy evaluation.

### FP-003 — Authority SHALL NOT Transfer Through Preservation

Fork SHALL NOT treat recording, hashing, referencing, preserving, or recomputing external artifacts as inheriting authority, correctness, or proof obligations of the originating system.

### FP-004 — Explicit Boundary Contracts

Interoperability between Fork and external proof surfaces SHALL occur only through explicit boundary contracts.

### FP-005 — Independent Recomputation

Fork SHALL enable independent recomputation of its structural claims from preserved evidence without dependence on the originating runtime authority.

### FP-006 — Deterministic Structural Verification

Structural verification performed by Fork SHALL be deterministic.

### FP-007 — Evidence Preservation Without Execution Authority

Fork SHALL preserve and verify structural relationships of evidence. Fork SHALL NOT control, authorize, deny, or continue execution.

### FP-008 — External Proof Surfaces Remain Independent

Fork SHALL treat external proof surfaces as independent. Consuming artifacts from an external proof surface SHALL NOT collapse, extend, merge, or inherit proof surfaces.

## 5. Scope

### 5.1 Fork SHALL

Within its proof surface, Fork SHALL preserve evidence, declared non-claims, boundary transitions, reliance context, explicit boundary declarations, and contract references sufficient to support deterministic recomputation and structural verification.

### 5.2 Fork SHALL NOT

Within FK-100, Fork SHALL NOT authorize execution, evaluate policy, determine legal sufficiency, determine clinical or financial correctness, perform runtime governance, transfer authority, infer omitted evidence, or validate external proof surfaces beyond structural conformance to declared boundary contracts.

## 6. Normative Proof Claims (FK-00x)

Each FK-00x claim defines a specific proof obligation within the Fork proof surface.

---

## FK-001 — Evidence Boundary Preservation

**Purpose:** To prove that Fork preserved a complete and replayable representation of evidence at architectural boundaries.

**Requirement:** Fork SHALL capture and preserve boundary-state artifacts sufficient to reconstruct what evidence crossed, what was excluded, what was out of scope, and the conditions under which the boundary transition occurred.

**Inputs:** Boundary contract, upstream artifact references, artifact identifiers, context metadata, timestamps, assumptions, exclusions, and non-claims.

**Outputs:** Boundary-state records, inclusion records, exclusion records, boundary metadata records, structural indices, and failure records.

**Failure Conditions:** Missing required metadata, inconsistent boundary records, absent artifact classification, contract violation, or insufficient evidence for reconstruction.

**Verification Method:** Independent recomputation of boundary-state records MUST yield a structure consistent with the declared boundary contract.

**Conformance Criteria:** An implementation conforms to FK-001 only if it can enumerate boundary transitions, distinguish included/excluded/out-of-scope evidence, replay records, and surface boundary failures.

---

## FK-002 — Reliance Context Preservation

**Purpose:** To prove that Fork preserves who or what relied on which evidence, for which decisions or actions, and under which declared assumptions.

**Requirement:** Fork SHALL record reliance relationships between actors, systems, decisions, and evidence artifacts.

**Inputs:** Reliance declarations, artifact references, actor or system identifiers where declared, decision context, assumptions, non-claims, timestamps, and boundary references.

**Outputs:** Reliance-context records, reliance graphs or equivalent structures, linkages between evidence and decisions, and inconsistency records.

**Failure Conditions:** Undeclared reliance, ambiguous reliance records, missing metadata, unresolved evidence references, or inability to reconstruct reliance context.

**Verification Method:** Independent recomputation MUST reconstruct the reliance graph or equivalent reliance structure for a given artifact, time window, decision, or workflow.

**Conformance Criteria:** An implementation conforms to FK-002 only if it can enumerate reliance relationships, reconstruct decision contexts, distinguish declared reliance from inferred reliance, and detect missing reliance declarations.

---

## FK-003 — Boundary Transition Preservation

**Purpose:** To prove that Fork preserves the sequence, directionality, and structure of transitions across architectural boundaries.

**Requirement:** Fork SHALL record ordered boundary transitions, including directionality and associated artifact instances.

**Inputs:** Boundary events, contract identifiers, producer and consumer identifiers, artifact references, timestamps, and transition metadata.

**Outputs:** Boundary-transition ledgers, transition graphs or equivalent sequences, orphan-transition failure records, and contract-reference records.

**Failure Conditions:** Missing transition events, structurally out-of-order events, orphaned transitions, unresolved references, or impossible transition reconstruction.

**Verification Method:** Independent recomputation MUST yield the same transition ordering and participant set from preserved records.

**Conformance Criteria:** An implementation conforms to FK-003 only if it can reconstruct cross-boundary paths, demonstrate ordering, detect invalid transitions, and preserve directionality without implying authority flow.

---

## FK-004 — Declared Non-Claim Preservation

**Purpose:** To prove that Fork preserves explicit statements of what Fork or external systems do not claim, assert, certify, validate, or decide.

**Requirement:** Fork SHALL record declared non-claims associated with artifacts, decisions, boundary events, reliance events, and proof surfaces.

**Inputs:** Non-claim declarations, associated artifact references, boundary or reliance context, declarant identity or role where available, timestamps, and contract references.

**Outputs:** Non-claim records, non-claim linkage records, non-claim coverage reports where implemented, and failure records for missing or ambiguous required non-claims.

**Failure Conditions:** Missing required non-claims, ambiguous non-claims, mislinked non-claims, contradiction with declared proof surface, or inability to enumerate applicable non-claims.

**Verification Method:** Independent recomputation MUST enumerate all non-claims applicable to a preserved artifact, boundary event, reliance event, or decision context.

**Conformance Criteria:** An implementation conforms to FK-004 only if it can show non-claim coverage, preserve non-claim attachment across recomputation, distinguish preserved from inferred non-claims, and surface missing required non-claims.

---

## FK-005 — Independent Recomputation

**Purpose:** To prove that Fork's structural claims can be recomputed from preserved evidence without the originating runtime.

**Requirement:** Fork SHALL preserve all inputs, structural relationships, assumptions, references, and evaluation logic identifiers required to recompute its proof-surface claims.

**Inputs:** Preserved artifacts, boundary records, reliance records, non-claim records, transition records, evaluation logic identifiers, assumptions, and integrity metadata.

**Outputs:** Recomputation results, verification reports, failure reports, and evidence reconstruction summaries.

**Failure Conditions:** Missing evidence, unavailable or incompatible evaluation logic, inconsistent assumptions, non-deterministic outcomes, or insufficient records.

**Verification Method:** Independent actors MUST reproduce Fork's structural results using only preserved artifacts, declared assumptions, and declared evaluation logic.

**Conformance Criteria:** An implementation conforms to FK-005 only if independent recomputation yields deterministic structural outcomes or deterministic explanations for failure.

---

## FK-006 — Structural Verification

**Purpose:** To prove that the preserved record remains structurally consistent over time.

**Requirement:** Fork SHALL verify integrity and consistency of preserved evidence artifacts, boundary-state records, reliance-context records, declared non-claims, transition ledgers, contract references, and evaluation logic references.

**Inputs:** Preserved record sets, artifact references, integrity metadata, hashes or signatures where implemented, contract references, and evaluation logic identifiers.

**Outputs:** Structural verification results, integrity status reports, reference failure records, contract violation records, and recomputation status reports.

**Failure Conditions:** Integrity mismatch, broken references, contract violation, inconsistent records, or non-reproducible structural verification.

**Verification Method:** Independent recomputation MUST detect structural inconsistencies and confirm structurally consistent records as valid within the limits of FK-100.

**Conformance Criteria:** An implementation conforms to FK-006 only if it can detect structural failures, demonstrate consistency across recomputations, distinguish structural verification from correctness, and preserve verification results.

---

## FK-007 — Boundary-State Interoperability

**Purpose:** To prove that Fork interoperates with external proof surfaces via declared boundary contracts without transferring authority or proof obligations.

**Requirement:** Fork SHALL evaluate boundary events against declared boundary contracts for purposes of evidence consumption and structural verification.

**Inputs:** Boundary contract specifications, external artifact instances, artifact class declarations, producer and consumer identifiers, verification scope declarations, non-claim declarations, local evidence records, and contract metadata.

**Outputs:** Interoperability event records, contract-conformance reports, accepted boundary artifact records, rejected boundary artifact records, narrowing records where applicable, and authority non-transfer records.

**Failure Conditions:** Non-conformant artifacts, missing metadata, absent or broadened verification scope, missing contract identifiers, missing required non-claims, or asserted authority transfer.

**Verification Method:** Independent recomputation MUST show that contract requirements were evaluated, outcomes were recorded, authority did not transfer, only declared evidence crossed, and acceptance/rejection/narrowing rationale is inspectable.

**Conformance Criteria:** An implementation conforms to FK-007 only if it can evaluate boundary events under declared contracts, preserve boundary outcomes, demonstrate non-transfer of authority, replay boundary interactions, and preserve boundary transparency.

---

## 7. Normative Non-Proof Surface

Fork SHALL NOT be designed, described, or interpreted as proving any of the following:

- runtime admissibility;
- execution authorization;
- execution continuation validity;
- operational validity;
- organizational authority;
- governance approval;
- legal compliance;
- legal sufficiency;
- clinical correctness;
- clinical safety;
- financial correctness;
- risk sufficiency;
- policy correctness;
- policy enforcement outcomes;
- identity verification;
- credential validity;
- artifact authenticity beyond structural integrity;
- execution validity;
- operational correctness;
- truth;
- factual accuracy;
- epistemic certainty;
- or external proof-surface correctness.

Attempts to extend Fork into these domains MUST be treated as outside-spec behavior and SHALL NOT be claimed as conformant to FK-100.

## 8. Conformance

An implementation claiming conformance to FK-100 SHALL demonstrate conformance to FK-001 through FK-007.

An implementation SHALL also demonstrate that it does not assert claims listed in the Normative Non-Proof Surface.

Partial implementation MAY be described as implementing specific FK-00x claims, but SHALL NOT be described as conformant to FK-100 unless all normative proof claims are satisfied.

Conformance to FK-100 does not imply conformance to BC-100, any BC-10x profile, any external proof surface, any legal standard, any compliance standard, or any runtime governance system.

## 9. Informative Appendices

### Appendix A — Demonstrated Evidence

Potential evidence includes Boundary-State Interoperability v0.1.1, Computed Proof Surface v0.1, Claim Boundary Contract definitions, Claim Consumption Event logs, GLM-related evidence artifacts, Boundary Delta Records, Human Recomputation Sandbox reports, independent recomputation reports, deterministic inventory files, and verification scripts.

### Appendix B — Related Fork Standards

Related standards should be listed by identifier, version, relationship to FK-100, scope summary, normative/informative classification, and current status.

### Appendix C — External Proof Surface Crosswalk

| External Proof Surface | Relationship | Authority Transfer |
|---|---|---|
| AST-100 | Boundary profile | No |
| GLM | Boundary profile or consumed artifact | No |
| SCQOS | Boundary profile or consumed artifact | No |
| CBC | Native Fork specification | N/A |
| CCEC | Native Fork specification | N/A |

This crosswalk is illustrative. Inclusion does not imply completed interoperability, endorsement, adoption, or conformance.

### Appendix D — Review Checklist

1. Does FK-100 answer only "What does Fork prove?"
2. Are FK-001 through FK-007 sufficient to describe Fork's proof surface?
3. Does any clause imply execution authority?
4. Does any clause imply legal, policy, clinical, financial, or factual correctness?
5. Are external proof surfaces preserved as independent?
6. Are non-claims explicit and normative?
7. Is conformance limited to structural and recomputable evidence claims?
8. Are informative examples clearly non-normative?
