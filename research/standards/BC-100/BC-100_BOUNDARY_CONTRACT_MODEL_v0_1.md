# Normative Boundary Model — BC-100

Identifier: BC-100  
Title: Boundary Contract Model for Independent Proof Surfaces  
Status: Draft v0.1  
Classification: Normative, with informative appendices  
Question Answered: How do independent proof surfaces communicate without transferring authority?  
Prerequisites: Fork Standards Architecture v0.1  
Dependents: BC-10x profiles, Enterprise Workflow examples

> BC-100 defines Fork's proposed normative model for communication between independent proof surfaces. BC-10x profiles apply that model to specific proof-surface seams.

> **Status Notice**
>
> BC-100 is a proposed normative model within the Fork research track. It does not claim general adoption or interoperability beyond completed profiles and evidence artifacts.

## 1. Purpose

BC-100 defines a domain-neutral boundary contract model for communication between independent proof surfaces.

BC-100 specifies:

- the semantic model of boundary contracts;
- the roles and participants in a boundary event;
- artifact class and artifact instance semantics;
- required metadata categories;
- contract lifecycle and versioning concepts;
- profile mechanisms; and
- universal boundary invariants every conforming profile MUST satisfy.

BC-100 defines semantics, not serialization. It SHALL NOT require JSON, YAML, XML, Markdown, a database schema, a transport protocol, or a wire format.

## Part I — Boundary Contract Model

## 2. Participants

A boundary contract involves at least two participant proof surfaces.

### 2.1 Producer Proof Surface

The Producer Proof Surface is the architecture that originates a boundary artifact and remains responsible for its own proof claims.

### 2.2 Consumer Proof Surface

The Consumer Proof Surface is the architecture that receives or references a boundary artifact and uses it under its own proof obligations.

### 2.3 Optional Observer

A profile MAY define an observer role for review, audit, or independent recomputation. Observer roles SHALL NOT alter producer or consumer proof obligations unless separately defined by another proof surface.

## 3. Roles

### 3.1 Producer

The Producer emits or exposes artifact instances according to a profile.

The Producer SHALL remain responsible for producer-side proof obligations and SHALL NOT rely on the boundary contract to transfer such obligations to the Consumer.

### 3.2 Consumer

The Consumer evaluates boundary artifact instances against a profile for purposes defined by the Consumer proof surface.

The Consumer SHALL remain responsible for consumer-side proof obligations and SHALL NOT use boundary artifacts to silently expand producer claims.

### 3.3 Profile Author

The Profile Author defines a BC-10x profile that binds BC-100 to specific producer and consumer proof surfaces.

The Profile Author SHALL identify participant proof surfaces, permitted artifact classes, required metadata, additional constraints, and examples.

## 4. Artifact Classes and Artifact Instances

### 4.1 Artifact Class

An Artifact Class is a category of artifact permitted or prohibited by a boundary profile.

Examples of artifact classes include, informatively:

- decision record;
- evidence bundle;
- condition snapshot;
- reliance declaration;
- boundary evaluation record;
- non-claim declaration.

Profiles SHALL define permitted artifact classes.

### 4.2 Artifact Instance

An Artifact Instance is a concrete occurrence of an Artifact Class.

Artifact Instances SHALL carry instance-specific metadata, including unique identifier, timestamp or sequence marker, producer reference, and verification scope where required.

### 4.3 Class-Level Semantics

Profiles SHOULD attach semantic requirements to Artifact Classes, including required metadata, permissible verification scopes, and non-claims.

### 4.4 Instance-Level Records

Artifact Instances SHALL be evaluated against the requirements of their declared Artifact Class.

An Artifact Instance without a declared Artifact Class SHALL NOT be considered contract-conformant.

## 5. Required Metadata

Each boundary artifact instance conforming to BC-100 through a BC-10x profile SHALL provide, or explicitly record absence of, the following metadata categories:

- boundary contract identifier and version;
- profile identifier and version;
- producer proof surface identifier and version;
- consumer proof surface identifier and version, where applicable;
- artifact class;
- artifact instance identifier;
- creation timestamp or sequence marker;
- boundary emission timestamp or sequence marker, where different;
- verification scope;
- declared non-claims, where applicable or required;
- producer provenance, where available or required by profile;
- integrity metadata, where available or required by profile;
- evaluation outcome, for consumer-side boundary evaluation records.

Profiles MAY define additional required metadata.

## 6. Contract Lifecycle

A boundary profile MAY define lifecycle states. Where lifecycle states are defined, they SHOULD include:

- Draft;
- Active;
- Deprecated;
- Superseded;
- Withdrawn;
- Archived.

A boundary artifact instance SHALL identify the profile version under which it was evaluated.

Profiles SHALL NOT retroactively alter the status of already-recorded boundary events without preserving the original evaluation context.

## 7. Versioning

BC-100 uses versioned identifiers.

A profile SHALL identify:

- BC-100 version;
- profile version;
- producer proof surface version;
- consumer proof surface version;
- artifact class version, where applicable;
- schema or binding version, where applicable.

Version incompatibility SHALL produce a boundary evaluation outcome rather than undefined behavior.

## 8. Profiles

A BC-10x profile applies BC-100 to a specific proof-surface seam.

A profile SHALL specify:

- profile identifier;
- profile title;
- profile status;
- producer proof surface;
- consumer proof surface;
- conformance statement to BC-100;
- permitted artifact classes;
- prohibited artifact classes or fields, where applicable;
- required metadata extensions;
- mappings from producer artifact classes to consumer proof claims;
- additional constraints;
- evaluation outcomes;
- conformant and non-conformant examples.

Profiles SHALL NOT redefine BC-100 invariants. Profiles MAY add stricter constraints.

## Part II — Boundary Invariants

## BCI-001 — Authority Non-Transfer

Authority SHALL NOT cross a boundary unless explicitly delegated by a separate authority specification outside BC-100.

A boundary contract governs evidence communication. It does not transfer authority, correctness, sufficiency, approval, compliance, or proof obligations.

## BCI-002 — Proof Surface Independence

Communication SHALL NOT merge proof surfaces.

Producer and Consumer proof surfaces SHALL remain architecturally independent. Each remains responsible for its own claims and obligations.

## BCI-003 — Explicit Artifact Classification

Every transferred artifact instance SHALL declare its Artifact Class.

Every transferred artifact instance SHALL declare:

- producer proof surface;
- contract/profile identifier and version;
- artifact class;
- artifact instance identifier;
- verification scope;
- declared non-claims where applicable or required.

Unclassified artifact instances SHALL NOT be accepted as contract-conformant boundary artifacts.

## BCI-004 — Consumer Narrowing

Consumers MAY narrow claims associated with received artifacts.

Consumers SHALL NOT broaden claims, verification scope, or proof obligations associated with a received artifact unless the Consumer originates a new claim under its own proof surface.

## BCI-005 — Replay Independence

Boundary records SHALL permit recomputation of consumer-side structural claims without requiring the producer runtime.

Replay independence does not require the Consumer to recompute the Producer's decisions. It requires the Consumer to recompute its own structural claims about received or referenced boundary artifacts.

## BCI-006 — Explicit Non-Claims

Boundary profiles SHALL support explicit non-claim declarations.

Consumers SHALL preserve declared non-claims as part of boundary and reliance context where such non-claims are supplied or required.

A non-claim SHALL NOT be converted into a positive claim by transfer, preservation, or recomputation.

## BCI-007 — Contract-Bound Communication

Only artifact classes, fields, and relationships explicitly specified by a boundary profile SHALL be treated as crossing under that profile.

Other communication SHALL be treated as outside the boundary contract unless captured by another profile or future version.

## BCI-008 — Evidence Scope Preservation

A boundary contract SHALL preserve the declared verification scope of every transferred artifact.

Consumers SHALL NOT broaden the verification scope of a transferred artifact unless they originate a new claim under their own proof surface and preserve the boundary between the received scope and the new claim.

## BCI-009 — Boundary Transparency

Every accepted, rejected, narrowed, or defect boundary artifact SHALL leave an inspectable record describing:

- the contract/profile under which it was evaluated;
- the artifact instance evaluated;
- the artifact class declared;
- the verification scope;
- the evaluation outcome;
- the reason for acceptance, rejection, narrowing, or defect classification;
- the evaluator or consumer context, where available or required by profile.

Boundary transparency enables independent reviewers to reconstruct why a boundary evaluation produced its outcome.

## 9. Boundary Evaluation Outcomes

Profiles SHOULD define concrete outcome values. At minimum, profiles SHOULD support:

- Accepted;
- Rejected;
- Narrowed;
- Defect;
- Out of Contract;
- Version Incompatible.

A boundary evaluation outcome SHALL be preserved with reason information sufficient to support BCI-009.

## 10. Conformance

A profile conforms to BC-100 only if it:

- identifies producer and consumer proof surfaces;
- defines permitted artifact classes;
- defines required metadata;
- preserves all BCI-001 through BCI-009 invariants;
- defines boundary evaluation outcomes;
- distinguishes normative requirements from informative examples;
- avoids domain-specific semantics in BC-100 itself;
- does not transfer authority or proof obligations across the seam.

## Appendix A — Informative Profile Template

See `profile_template.md`.

## Appendix B — Informative Example Profile

A future BC-101 profile may apply BC-100 to an AST-100 producer and FK-100 consumer. Such a profile would be profile-specific and SHALL NOT alter BC-100's domain-neutral model.

## Appendix C — Informative Worked Example

A worked example SHOULD show:

1. Producer emits artifact instance.
2. Consumer evaluates artifact instance against profile.
3. Consumer records accepted/rejected/narrowed/defect outcome.
4. Consumer preserves reason information.
5. Independent reviewer recomputes consumer-side structural claims without producer runtime.
