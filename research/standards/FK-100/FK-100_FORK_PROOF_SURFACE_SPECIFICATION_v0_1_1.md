# Normative Architecture Standard — FK-100

Identifier: FK-100  
Title: Fork Proof Surface Specification  
Subtitle: Recomputable Evidence and Boundary-State Preservation  
Status: Draft v0.1.1  
Supersedes: FK-100 Draft v0.1 (Phase 1 baseline retained for chain continuity)  
Classification: Normative  
Question Answered: What does Fork prove?  
Prerequisites: Fork Standards Architecture v0.1.1  
Dependents: BC-100, BC-101, Enterprise Workflow examples

> FK-100 defines Fork's proof surface for reconstructable reliance. It does not define execution control, continuation validity, policy enforcement, admissibility, authority, legal sufficiency, artifact authenticity, or truth.

> **Status Notice**
>
> FK-100 v0.1.1 is a proposed normative specification within the Fork research track. It is not a production-readiness assessment, compliance certification, legal opinion, or external endorsement.

## 1. Purpose

Fork is a normative architecture for preserving the evidence required to independently reconstruct reliance across architectural boundaries.

FK-100 defines the normative proof surface for Fork. It specifies the claims Fork is responsible for proving and the evidence obligations required to support those claims.

Fork defines proof obligations associated with:

- evidence-boundary preservation;
- reliance-context preservation;
- boundary-transition preservation;
- declared non-claim preservation;
- independent recomputation;
- structural verification; and
- boundary-state interoperability.

Fork SHALL NOT be treated as an execution-control, compliance, policy-interpretation, authority-validation, or truth-certification system.

The core question FK-100 answers is:

> Can later reliance be independently reconstructed?

## 2. Definition of Proof Surface

### 2.1 Proof Surface

A proof surface is the bounded set of normative claims an architecture asserts and is obligated to support with evidence, replayability, and verification.

The Fork proof surface is limited to the claims defined in Section 5. Claims outside this proof surface SHALL NOT be attributed to Fork unless incorporated through a future revision of FK-100 or a separate proof-surface specification.

### 2.2 Architectural Responsibility

Architectural responsibility denotes the obligations Fork assumes when operating within its proof surface.

Fork's architectural responsibility is limited to:

- preserving evidentiary records sufficient to reconstruct what was relied upon;
- preserving what was intentionally excluded;
- preserving how information crossed architectural boundaries;
- preserving declared non-claims;
- supporting deterministic structural verification; and
- enabling independent recomputation of preserved records after the originating execution context no longer exists.

Fork's architectural responsibility SHALL NOT extend to execution authorization, policy evaluation, organizational authority, legal sufficiency, clinical correctness, financial correctness, factual truth, artifact authenticity, or runtime continuation validity.

### 2.3 Boundary Contracts

A boundary contract is a declared specification that defines how artifacts from a producer proof surface may be consumed as evidence by a consumer proof surface without transferring authority or proof obligations.

Boundary contracts MAY be defined using BC-100 and BC-10x profiles.

Fork MAY consume artifacts through declared boundary contracts. Fork SHALL NOT infer authority, correctness, sufficiency, or compliance from the existence of a boundary contract.

### 2.4 External Proof Surfaces

External proof surfaces are architectures that define their own proof obligations outside FK-100.

Fork SHALL treat external proof surfaces as independent. Consumption of an artifact from an external proof surface SHALL NOT extend Fork's proof surface to cover that external surface's obligations, nor extend that external surface's proof obligations to Fork.

### 2.5 Independent Recomputation

Independent recomputation is the ability to re-derive Fork's structural claims from preserved evidence without requiring the original execution environment, runtime authority, or live producer system state.

Fork SHALL preserve sufficient evidence and evaluation logic identifiers to support independent recomputation of its own structural claims.

### 2.6 Structural Verification

Structural verification is the deterministic evaluation of preserved records for integrity, completeness, reference consistency, contract alignment, and recomputation eligibility.

Structural verification SHALL NOT be interpreted as truth verification, legal sufficiency, policy correctness, organizational approval, or runtime authorization.

## 3. Architectural Principles

### FP-001 — No Unsupported Claims

Fork SHALL NOT assert any claim that cannot be supported by preserved, replayable evidence within its proof surface.

### FP-002 — Evidence Before Interpretation

Fork SHALL prioritize preservation and recomputation of evidence over semantic interpretation or policy evaluation. Interpretation of preserved evidence is outside Fork's proof surface unless separately and explicitly defined by another proof surface.

### FP-003 — Authority SHALL NOT Transfer Through Preservation

Fork SHALL NOT treat recording, hashing, sealing, referencing, or preserving an external artifact as inheriting the authority, correctness, or proof obligations of the originating system.

### FP-004 — Explicit Boundary Contracts

Cross-surface relationships SHOULD be described through explicit boundary contracts. Fork SHALL NOT treat undocumented or implicit exchanges as sufficient to establish a normative boundary relationship.

### FP-005 — Independent Recomputation

Fork SHALL enable independent recomputation of its structural claims from preserved evidence without dependence on the originating runtime authority.

### FP-006 — Deterministic Structural Verification

Given the same preserved record, declared assumptions, and evaluation logic, Fork SHALL produce equivalent structural verification outcomes.

### FP-007 — Evidence Preservation Without Execution Authority

Fork SHALL preserve and verify structural relationships of evidence but SHALL NOT control, authorize, continue, deny, or govern execution.

### FP-008 — External Proof Surfaces Remain Independent

Fork SHALL treat external proof surfaces as independent. Consuming artifacts from an external proof surface SHALL NOT collapse, extend, or merge proof surfaces.

## 4. Scope

### 4.1 Fork SHALL

Within FK-100, Fork SHALL:

- preserve evidence necessary to reconstruct what was relied upon;
- preserve evidence that was intentionally excluded when such exclusions are declared or captured;
- preserve declared non-claims alongside associated evidence;
- preserve boundary transitions, including artifacts crossing seams, conditions of crossing, and declared assumptions;
- preserve reliance context, including relying actor or system, relied-upon artifact, decision context, and applicable assumptions where declared;
- support deterministic recomputation of structural verification outcomes;
- support replay of preserved evidence under declared assumptions;
- preserve explicit boundary declarations and contracts governing evidence consumption.

### 4.2 Fork SHALL NOT

Within FK-100, Fork SHALL NOT:

- authorize execution, continuation, or operational state changes;
- evaluate policy, governance approval, or organizational authority;
- determine legal sufficiency, admissibility, or regulatory compliance;
- determine clinical correctness, financial correctness, safety, or factual truth;
- perform runtime governance or operational continuation validity decisions;
- transfer authority from external systems through preservation, hashing, sealing, or referencing;
- infer omitted evidence, unstated assumptions, or undeclared authority beyond what is explicitly preserved and declared;
- certify artifact authenticity beyond structural integrity of the preserved record.

## 5. Normative Proof Claims

Each FK-00x claim defines a specific Fork proof obligation. Each claim uses the following structure: Purpose, Requirement, Assumptions, Inputs, Evaluation Logic, Produced Outputs, Failure Conditions, Evidence Requirements, Verification Method, Conformance Criteria, Demonstrated By, Related Standards.

### FK-001 — Evidence Boundary Preservation

#### Purpose

To prove that Fork preserves a replayable representation of evidence at architectural boundaries, including inclusions, exclusions, and structural context.

#### Requirement

Fork SHALL capture and preserve boundary-state records sufficient to reconstruct:

- what evidence crossed a boundary;
- what evidence was available but excluded, where exclusion evidence is declared or captured;
- the conditions and assumptions under which the boundary transition occurred; and
- the structural relationship between the boundary event and the preserved record.

#### Assumptions

- A boundary event is observable or declared.
- Required boundary metadata is available or its absence is recorded.
- Boundary artifacts can be referenced structurally.

#### Inputs

- Boundary artifact references.
- Boundary event metadata.
- Declared inclusion and exclusion records.
- Associated contract identifiers, where applicable.
- Timestamp or sequence indicator.

#### Evaluation Logic

Fork SHALL encode boundary events into structured records and verify that required references, identifiers, and declared relationships are present.

#### Produced Outputs

- Boundary-state records.
- Boundary artifact index.
- Inclusion and exclusion records.
- Boundary verification status.

#### Failure Conditions

FK-001 SHALL fail or produce a boundary-defect record when:

- required boundary metadata is missing;
- boundary artifact references are unresolved;
- inclusion or exclusion records conflict;
- boundary event ordering cannot be reconstructed; or
- contract-required fields are absent.

#### Evidence Requirements

Evidence SHALL include boundary artifact references, event identifiers, timestamps or sequence markers, declared assumptions, inclusion/exclusion markers, and verification status.

#### Verification Method

Independent recomputation SHALL reconstruct the boundary-state representation from preserved records and produce equivalent structural results under unchanged evidence.

#### Conformance Criteria

An implementation conforms to FK-001 if it can enumerate boundary transitions, replay boundary-state records, detect missing required boundary elements, and preserve inclusion/exclusion context without asserting upstream correctness.

#### Demonstrated By

- Boundary-State Interoperability artifacts.
- Boundary Delta Records.
- Computed Proof Surface records.
- Human recomputation sandbox materials, where applicable.

#### Related Standards

- FK-003 Boundary Transition Preservation.
- FK-006 Structural Verification.
- FK-007 Boundary-State Interoperability.
- BC-100 Boundary Contract Model.

### FK-002 — Reliance Context Preservation

#### Purpose

To prove that Fork preserves who or what relied on which evidence, for what decision context, and under which declared assumptions.

#### Requirement

Fork SHALL preserve reliance declarations sufficient to reconstruct:

- the relying actor, system, role, or process;
- the relied-upon artifact or record;
- the decision, review, handoff, or downstream context;
- applicable assumptions and declared non-claims.

Fork SHALL NOT infer reliance that has not been declared or captured.

#### Assumptions

- Reliance events are declared, captured, or otherwise observable.
- The relying entity can be represented structurally.
- The relied-upon artifact is identifiable.

#### Inputs

- Reliance declaration.
- Relying entity identifier or role.
- Relied artifact reference.
- Decision or workflow context.
- Declared assumptions and non-claims.

#### Evaluation Logic

Fork SHALL encode reliance relationships as structured records linking entities, artifacts, contexts, assumptions, and non-claims.

#### Produced Outputs

- Reliance-context records.
- Reliance graph edges.
- Reliance verification status.

#### Failure Conditions

FK-002 SHALL fail or produce a reliance-defect record when:

- the relying entity is missing where required;
- the relied artifact is unresolved;
- reliance context is ambiguous;
- reliance declarations conflict; or
- required assumptions/non-claims are absent.

#### Evidence Requirements

Evidence SHALL include reliance declarations, artifact references, context identifiers, timestamps or sequence markers, and applicable assumptions/non-claims.

#### Verification Method

Independent recomputation SHALL reconstruct the reliance graph for a preserved decision, artifact, or time window and produce equivalent structural relationships.

#### Conformance Criteria

An implementation conforms to FK-002 if it can enumerate reliance relationships, reconstruct reliance context, preserve declared assumptions/non-claims, and surface missing or inconsistent reliance declarations.

#### Demonstrated By

- Claim Consumption Events.
- Reliance-context examples.
- Human recomputation sandbox materials.

#### Related Standards

- FK-001 Evidence Boundary Preservation.
- FK-004 Declared Non-Claim Preservation.
- FK-006 Structural Verification.

### FK-003 — Boundary Transition Preservation

#### Purpose

To prove that Fork preserves the sequence and structure of transitions across architectural boundaries.

#### Requirement

Fork SHALL record ordered boundary transitions, participating surfaces or systems where declared, artifact references, and transition directionality.

#### Assumptions

- Boundary event order can be represented through timestamps, sequence numbers, or causal references.
- Participating endpoints are identifiable or their absence is recorded.
- Artifact references can be resolved or marked unresolved.

#### Inputs

- Boundary event records.
- Contract identifiers, where applicable.
- Producer and consumer identifiers.
- Artifact references.
- Sequence indicators.

#### Evaluation Logic

Fork SHALL construct a transition ledger or graph sufficient to reconstruct cross-boundary paths.

#### Produced Outputs

- Boundary-transition ledger.
- Transition graph or sequence representation.
- Transition verification status.

#### Failure Conditions

FK-003 SHALL fail or produce a transition-defect record when:

- event order cannot be reconstructed;
- a transition has no identifiable endpoint where required;
- a transition references a missing artifact;
- the transition violates a declared contract; or
- multiple incompatible transition histories are present.

#### Evidence Requirements

Evidence SHALL include event identifiers, endpoint identifiers, artifact references, order markers, contract identifiers, and transition status.

#### Verification Method

Independent recomputation SHALL yield the same transition ordering and participant set from preserved records.

#### Conformance Criteria

An implementation conforms to FK-003 if it can reconstruct cross-boundary paths, detect orphaned transitions, preserve order, and distinguish declared boundary transitions from non-contract communication.

#### Demonstrated By

- Boundary-State Interoperability artifacts.
- Boundary Delta Records.
- Transition Integrity artifacts, where applicable.

#### Related Standards

- FK-001 Evidence Boundary Preservation.
- FK-007 Boundary-State Interoperability.
- BC-100 Boundary Contract Model.

### FK-004 — Declared Non-Claim Preservation

#### Purpose

To prove that Fork preserves explicit statements of what is not claimed or asserted by an artifact, system, profile, workflow, or boundary event.

#### Requirement

Fork SHALL preserve declared non-claims associated with artifacts, decisions, reliance events, boundary events, and proof surfaces where such non-claims are available or required by contract.

Fork SHALL NOT convert non-claims into positive claims.

#### Assumptions

- Non-claims are explicitly declared or contractually required.
- Non-claims can be associated with relevant artifacts or contexts.
- Missing required non-claims can be detected structurally.

#### Inputs

- Non-claim declarations.
- Associated artifact references.
- Boundary or reliance context.
- Declarant metadata, where available or required by boundary contract.

#### Evaluation Logic

Fork SHALL attach non-claims to relevant records as structured annotations and preserve their association during recomputation.

#### Produced Outputs

- Non-claim records.
- Non-claim coverage map.
- Non-claim verification status.

#### Failure Conditions

FK-004 SHALL fail or produce a non-claim-defect record when:

- required non-claims are missing;
- non-claims are mislinked;
- a non-claim is contradicted by a Fork assertion; or
- a non-claim is suppressed during boundary or reliance preservation.

#### Evidence Requirements

Evidence SHALL include immutable non-claim statements and provenance of the declarant where available or required by boundary contract.

#### Verification Method

Independent recomputation SHALL enumerate all non-claims applicable to an artifact, boundary event, reliance event, or preserved record.

#### Conformance Criteria

An implementation conforms to FK-004 if it can preserve non-claims, attach them to relevant records, detect missing required non-claims, and prevent non-claim suppression from appearing as proof-surface expansion.

#### Demonstrated By

- Claim Boundary Contract artifacts.
- Claim Consumption Events.
- Boundary-State Interoperability examples.

#### Related Standards

- FK-002 Reliance Context Preservation.
- FK-006 Structural Verification.
- BC-100 Explicit Non-Claims invariant.

### FK-005 — Independent Recomputation

#### Purpose

To prove that Fork's structural claims can be recomputed from preserved evidence without the originating runtime.

#### Requirement

Fork SHALL preserve all inputs, structural relationships, references, assumptions, and evaluation logic identifiers required to recompute Fork's own structural claims.

#### Assumptions

- Evaluation logic is versioned or identifiable.
- Preserved evidence is available.
- External runtime state is not required to recompute Fork's structural claims.

#### Inputs

- Preserved evidence artifacts.
- Evaluation logic identifiers and versions.
- Assumption declarations.
- Integrity metadata.
- Contract identifiers, where applicable.

#### Evaluation Logic

Fork SHALL define deterministic procedures for recomputing structural claims, including boundary integrity, reliance graph consistency, non-claim preservation, transition preservation, and contract alignment.

#### Produced Outputs

- Recomputation results.
- Verification reports.
- Recomputed structural graph or record set.
- Defect records, if recomputation fails.

#### Failure Conditions

FK-005 SHALL fail or produce a recomputation-defect record when:

- required evidence is missing;
- evaluation logic cannot be identified;
- recomputation is nondeterministic under unchanged conditions;
- required assumptions are unavailable;
- preserved references cannot be resolved and no unresolved-reference record exists.

#### Evidence Requirements

Evidence SHALL include complete evidence sets, reference graphs, evaluation logic identifiers, assumption records, and verification outputs.

#### Verification Method

Independent actors SHALL be able to reproduce Fork's structural results using preserved artifacts and declared logic.

#### Conformance Criteria

An implementation conforms to FK-005 if independent recomputation yields equivalent structural outcomes or deterministic defect records explaining why recomputation cannot complete.

#### Demonstrated By

- Computed Proof Surface artifacts.
- Human Recomputation Sandbox.
- Independent recomputation reports.

#### Related Standards

- FK-001 through FK-004.
- FK-006 Structural Verification.

### FK-006 — Structural Verification

#### Purpose

To prove that preserved records remain structurally consistent over time.

#### Requirement

Fork SHALL verify integrity and consistency of preserved records, including evidence artifacts, boundary-state records, reliance-context records, non-claim annotations, transition ledgers, references, hashes, and contract relationships.

#### Assumptions

- Integrity mechanisms are present or their absence is recorded.
- References are resolvable or explicitly unresolved.
- Verification logic is deterministic.

#### Inputs

- Preserved record sets.
- Hashes, signatures, or structural integrity metadata where available.
- Reference graphs.
- Contract identifiers.
- Evaluation logic identifiers.

#### Evaluation Logic

Fork SHALL perform deterministic structural checks, including:

- reference completeness;
- hash or digest verification where available;
- required-field verification;
- cross-reference consistency;
- contract alignment;
- non-claim preservation;
- reliance graph consistency.

#### Produced Outputs

- Structural verification result.
- Integrity status report.
- Defect records.
- Verification timestamp or sequence marker.

#### Failure Conditions

FK-006 SHALL fail or produce a structural-defect record when:

- hashes mismatch;
- required references are broken;
- required fields are missing;
- contract requirements are violated;
- reliance or boundary graphs are inconsistent;
- non-claims are missing or suppressed.

#### Evidence Requirements

Evidence SHALL include integrity metadata, reference graphs, verification logic identifiers, record sets, and verification outputs.

#### Verification Method

Independent recomputation SHALL detect structural inconsistencies and confirm structurally consistent records as valid within Fork's proof surface.

#### Conformance Criteria

An implementation conforms to FK-006 if it can produce deterministic structural verification results and detect integrity, reference, boundary, reliance, and contract defects without asserting truth or correctness.

#### Demonstrated By

- Computed Proof Surface artifacts.
- Hash receipts.
- Structural verification checkers.
- Independent verification reports.

#### Related Standards

- FK-005 Independent Recomputation.
- BC-100 Boundary Contract Model.

### FK-007 — Boundary-State Interoperability

#### Purpose

To prove that Fork can consume and preserve boundary artifacts from external proof surfaces through declared contracts without transferring authority or proof obligations.

#### Requirement

Fork SHALL evaluate boundary events against declared boundary contracts for purposes of evidence consumption and structural verification.

Fork SHALL NOT enforce producer obligations, inherit producer authority, or assert producer correctness.

#### Assumptions

- Boundary contracts are declared, versioned, and accessible.
- External artifacts declare verification scope.
- Contract-required metadata is available or absence is recorded.

#### Inputs

- Boundary contract specification.
- External boundary artifacts.
- Producer proof-surface identifier.
- Artifact classification.
- Verification scope.
- Declared non-claims.

#### Evaluation Logic

Fork SHALL validate received boundary artifacts against declared contract requirements and record compliant, rejected, narrowed, or defect events as boundary-state records.

#### Produced Outputs

- Boundary interoperability records.
- Contract-conformance results.
- Accepted, rejected, narrowed, or defect event records.
- Preserved non-claims.

#### Failure Conditions

FK-007 SHALL fail or produce an interoperability-defect record when:

- no applicable boundary contract exists;
- required artifact classification is missing;
- verification scope is undeclared;
- authority-transfer language is present;
- contract-required metadata is absent;
- artifact claims exceed the producer proof surface or consumer proof surface.

#### Evidence Requirements

Evidence SHALL include contract definitions, artifact records, classification metadata, verification scope, non-claims, boundary evaluation outcomes, and reason codes.

#### Verification Method

Independent recomputation SHALL show, for any boundary event, the contract used, artifact classification, verification scope, evaluation outcome, and whether authority or proof obligations were preserved as non-transferred.

#### Conformance Criteria

An implementation conforms to FK-007 if it can evaluate boundary events against declared contracts, preserve boundary-state outcomes, surface non-conformance, and demonstrate non-transfer of authority through inspectable records.

#### Demonstrated By

- Boundary-State Interoperability v0.1.1.
- BC-100 and BC-10x profiles.
- Human recomputation sandbox materials.

#### Related Standards

- BC-100 Boundary Contract Model.
- BC-101 AST-100 to FK-100 Profile.

## 6. Normative Non-Proof Surface

The following concerns are explicitly outside the Fork proof surface. Fork SHALL NOT be designed, described, or interpreted as proving:

- runtime admissibility;
- execution authorization;
- continuation validity;
- organizational authority;
- governance approval;
- legal compliance;
- legal sufficiency;
- clinical correctness;
- safety;
- financial correctness;
- risk sufficiency;
- policy correctness;
- policy enforcement outcomes;
- identity verification;
- credential validity;
- artifact authenticity beyond structural integrity of Fork's preserved record;
- execution validity;
- operational correctness;
- truth;
- factual accuracy;
- epistemic certainty.

Attempts to extend Fork into these domains MUST be treated as outside-spec behavior and SHALL NOT be claimed as conformant to FK-100.

## Appendix A — Demonstrated Evidence

This appendix maps FK-00x claims to existing or planned evidence artifacts.

| Claim | Evidence Category | Status |
|---|---|---|
| FK-001 | Boundary-State Interoperability artifacts; Boundary Delta Records | Existing / to be mapped |
| FK-002 | Claim Consumption Events; reliance records | Existing / to be mapped |
| FK-003 | Transition ledgers; boundary-state records | Existing / to be mapped |
| FK-004 | Claim Boundary Contracts; non-claim preservation examples | Existing / to be mapped |
| FK-005 | Computed Proof Surface; Human Recomputation Sandbox | Existing / to be mapped |
| FK-006 | Hash receipts; structural verification reports | Existing / to be mapped |
| FK-007 | Boundary-State Interop v0.1.1; BC-10x profiles | Existing / planned |

A completed release SHOULD replace "to be mapped" entries with concrete repository paths, version identifiers, and verification receipts.

## Appendix B — Related Fork Standards

Related Fork specifications include:

- Claim Boundary Contract series.
- Claim Consumption Event series.
- Boundary Delta Record series.
- Boundary-State Interoperability series.
- Computed Proof Surface artifacts.
- Human Recomputation Sandbox.
- BC-100 Boundary Contract Model.
- BC-10x Boundary Profiles.

## Appendix C — External Proof Surface Crosswalk

| External Surface | Relationship to Fork | Authority Transfer |
|---|---|---|
| AST-100 | Profile candidate through BC-101 | No |
| GLM | Profile candidate through BC-102 | No |
| SCQOS | Profile candidate through BC-103 | No |
| CBC | Native Fork-related claim-boundary standard | N/A |
| CCEC | Native Fork-related claim-consumption standard | N/A |

This crosswalk is informative unless a completed BC-10x profile declares a normative relationship.
