# BC-101 — AST-100 to FK-100 Boundary Profile

Identifier: BC-101  
Title: AST-100 to FK-100 Boundary Profile  
Status: Draft v0.1  
Classification: Normative Profile  
Conforms To: BC-100 Boundary Contract Model v0.1  
Question Answered: How do AST-100 and FK-100 communicate through a declared proof-surface seam?  
Prerequisites: FK-100, BC-100, AST-100  
Dependents: AST100_FK100 Enterprise Workflow Example

> BC-101 applies BC-100 to the AST-100 to FK-100 seam. AST-100 and FK-100 remain independent proof surfaces.

## 1. Profile Declaration

Producer Proof Surface: AST-100  
Consumer Proof Surface: FK-100  

Producer Proof Surface Responsibility: Operational Continuation Validity.  
Consumer Proof Surface Responsibility: Reconstructable Reliance.

BC-101 defines how selected AST-100 operational-continuation artifacts MAY be consumed by Fork as boundary evidence without transferring authority, correctness, sufficiency, or proof obligations.

## 2. Scope

BC-101 covers boundary events in which AST-100 artifact instances are presented to FK-100 for evidence consumption and structural preservation.

BC-101 is limited to consumer-side structural and evidentiary treatment by FK-100.

## 3. Non-Scope

BC-101 does not:

- determine whether AST-100 was correct;
- authorize execution;
- validate continuation decisions;
- determine legal, clinical, financial, regulatory, policy, or factual sufficiency;
- transfer AST-100 authority to Fork;
- extend FK-100 to cover AST-100 proof obligations.

## 4. Permitted Artifact Classes

| Class ID | Artifact Class | Producer Scope | Consumer Use |
|---|---|---|---|
| BC101-AC-001 | Continuation Decision Record | AST-100 continuation determination | FK-001, FK-003, FK-007 boundary evidence |
| BC101-AC-002 | Condition Snapshot | Operational state/context associated with continuation | FK-001, FK-002, FK-006 context evidence |
| BC101-AC-003 | Continuation Evidence Bundle | Evidence referenced by AST-100 decision | FK-001, FK-005, FK-006 structural preservation |
| BC101-AC-004 | AST-100 Non-Claim Declaration | Producer-side non-claims | FK-004 non-claim preservation |
| BC101-AC-005 | Producer Verification Receipt | Producer-side verification status | FK-006 structural reference only |

## 5. Prohibited Transfers

The following SHALL NOT transfer under BC-101:

- operational authority;
- continuation authority;
- organizational authority;
- legal sufficiency;
- policy correctness;
- compliance status;
- artifact authenticity;
- truth;
- AST-100 proof obligations;
- FK-100 proof obligations.

## 6. Required Metadata Extensions

In addition to BC-100 metadata, each BC-101 artifact instance SHALL include or explicitly record absence of:

| Field | Required | Notes |
|---|---|---|
| ast100_spec_version | Yes | AST-100 version applicable to producer artifact |
| ast100_claim_scope | Yes | Producer verification scope |
| continuation_outcome | Required for BC101-AC-001 | Producer outcome as declared |
| decision_timestamp | Required for BC101-AC-001 | Producer decision timestamp or sequence |
| producer_non_claims | Where available or required | Preserved by FK-004 |
| evidence_bundle_ref | Where applicable | Reference to evidence bundle |
| fork_consumption_scope | Yes | Consumer-side scope under FK-100 |
| authority_non_transfer_statement | Yes | Explicit non-transfer statement |

## 7. Mapping to FK-100 Claims

| Producer Artifact Class | FK-100 Claim(s) | Boundary Role |
|---|---|---|
| Continuation Decision Record | FK-001, FK-003, FK-007 | Boundary artifact and transition record |
| Condition Snapshot | FK-001, FK-002, FK-006 | Context artifact supporting reliance reconstruction |
| Continuation Evidence Bundle | FK-001, FK-005, FK-006 | Preserved evidence set for structural recomputation |
| AST-100 Non-Claim Declaration | FK-004 | Preserved non-claim |
| Producer Verification Receipt | FK-006, FK-007 | Structural reference; no correctness inheritance |

## 8. Evaluation Outcomes

BC-101 uses BC-100 evaluation outcomes:

- Accepted;
- Rejected;
- Narrowed;
- Defect;
- Out of Contract;
- Version Incompatible.

A Narrowed outcome SHALL preserve the original producer verification scope and the narrowed consumer verification scope.

## 9. Additional Constraints

### 9.1 Operational Evidence May Cross; Operational Authority Shall Not

AST-100 operational-continuation evidence MAY cross into FK-100 as boundary evidence. Operational authority SHALL NOT cross.

### 9.2 Continuation Validity May Be Recorded; Continuation Authority Shall Not Be Inherited

Fork MAY preserve reliance upon an AST-100 continuation artifact. Fork SHALL NOT assert that AST-100 was correct, authoritative, compliant, or sufficient.

### 9.3 Scope Preservation

Fork SHALL preserve AST-100's declared verification scope and SHALL NOT broaden it.

### 9.4 Non-Claim Preservation

Fork SHALL preserve producer non-claims where supplied or required. Missing required non-claims SHALL produce a defect or rejection outcome.

## 10. Conformant Boundary Event Example

An AST-100 implementation emits a Continuation Decision Record declaring:

- artifact class: Continuation Decision Record;
- producer proof surface: AST-100;
- continuation outcome: Continue with Constraint;
- verification scope: Operational Continuation Validity;
- non-claims: no legal sufficiency, no artifact authenticity, no organizational approval;
- evidence bundle reference: Bundle-2026-07-08-001.

Fork evaluates the artifact under BC-101.

If metadata is complete and no prohibited transfer is asserted, Fork records the event as Accepted or Narrowed, preserves the producer verification scope, preserves non-claims, and indexes the record under FK-001, FK-003, FK-004, FK-006, and FK-007.

Fork does not assert that continuation was correct.

## 11. Non-Conformant Boundary Event Example

An AST-100 artifact declares that receipt by Fork "confirms operational authority and legal compliance."

Fork SHALL reject or classify the artifact as Defect because the artifact attempts to transfer authority and broaden verification scope.

## 12. Conformance Statement

BC-101 conforms to BC-100 only if every BC-100 invariant BCI-001 through BCI-009 is preserved.

BC-101 conformance does not imply AST-100 conformance, FK-100 conformance, production readiness, external endorsement, or legal sufficiency.
