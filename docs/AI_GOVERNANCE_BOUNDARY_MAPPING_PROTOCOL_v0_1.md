# AI Governance Boundary Mapping Protocol v0.1

## Status

Draft operational mapping protocol.

This document defines a bounded way to map neighboring AI governance systems without collapsing their claims, authority, artifacts, or responsibilities into each other.

## Purpose

AI governance systems increasingly operate near each other.

One system may anchor model output.

Another may evaluate execution validity.

Another may preserve workflow evidence.

Another may determine policy admissibility.

Another may support audit, compliance, legal review, risk review, remediation, or reporting.

The problem is not that these systems overlap.

The problem is that their claims can silently collapse into each other.

This protocol exists to prevent that collapse.

## Core principle

Systems may exchange artifacts, but they may not silently exchange claims.

A system that receives an artifact from another system must not inherit claims that the originating system did not explicitly make.

A system that emits an artifact must not allow that artifact to be treated as proving more than its declared claim boundary supports.

## Scope

This protocol is for mapping adjacent AI governance systems by:

- system function;
- pipeline position;
- supported claims;
- explicit non-claims;
- emitted artifacts;
- consumable artifacts;
- safe handoff conditions;
- prohibited claim inheritance;
- authority boundaries;
- dependency boundaries;
- verification model;
- failure states.

## Non-scope

This protocol is not:

- a legal standard;
- a compliance certification;
- an audit standard;
- a liability framework;
- a procurement approval;
- a production deployment claim;
- a universal ontology;
- a claim that mapped systems are interoperable;
- a claim that mapped systems should be integrated;
- a claim that one system can absorb another.

## Why this is needed

Adjacent systems can be individually valid while becoming dangerous when their claims are merged informally.

Examples:

- Runtime output anchoring does not prove decision correctness.
- Evidence preservation does not prove legal admissibility.
- Execution control does not prove source completeness.
- Compliance review does not prove AI truth.
- Audit readiness does not prove remediation sufficiency.
- Institutional authority does not transfer into a tool merely because the tool preserved or emitted an artifact.

The protocol creates a structured map so engineers, architects, reviewers, and institutions can see where systems reinforce each other and where their boundaries must remain separate.

## System mapping record

Each system should be described using a system mapping record.

### Required fields

| Field | Meaning |
|---|---|
| SYSTEM_ID | Stable name or identifier for the mapped system. |
| SYSTEM_OWNER | Entity, team, or party responsible for the system. |
| SYSTEM_FUNCTION | What the system is designed to do. |
| PIPELINE_POSITION | Where the system sits in the governance or workflow sequence. |
| SUPPORTED_CLAIMS | What the system may assert within its declared boundary. |
| EXPLICIT_NON_CLAIMS | What the system must not be treated as proving. |
| EMITTED_ARTIFACTS | Artifacts the system can emit. |
| CONSUMABLE_ARTIFACTS | Artifacts the system can consume. |
| SAFE_HANDOFFS | Conditions under which artifacts may pass to another system. |
| PROHIBITED_CLAIM_INHERITANCE | Claims that must not transfer from or to the system. |
| AUTHORITY_BOUNDARY | What authority remains outside the system. |
| DEPENDENCY_BOUNDARY | What the system depends on and what must not depend on it. |
| VERIFICATION_MODEL | How outputs, artifacts, or claims can be checked. |
| FAILURE_STATES | Known states where claims fail, degrade, or require review. |

### Optional fields

| Field | Meaning |
|---|---|
| HUMAN_REVIEW_ROLE | Whether humans review, approve, veto, or interpret system outputs. |
| DATA_SENSITIVITY | Data classes handled by the system. |
| RETENTION_MODEL | How long artifacts are retained. |
| MUTABILITY_MODEL | Whether artifacts can be changed after creation. |
| EXTERNAL_REVIEWER_MODEL | Whether outsiders can verify artifacts without trusting the originating system. |
| CLIENT_ENVIRONMENT_DEPENDENCE | Whether behavior depends on client-specific systems or configuration. |
| DEPLOYMENT_STAGE | Concept, prototype, reference implementation, pilot, production, or other. |

## Pipeline positions

A mapped system may sit in one or more positions.

Common positions include:

- consequence formation;
- policy admissibility;
- pre-execution governance;
- execution control;
- continuation validity;
- runtime output anchoring;
- model invocation recording;
- workflow evidence preservation;
- evidence boundary verification;
- audit review;
- legal review;
- compliance review;
- risk review;
- remediation tracking;
- reporting.

Position does not create authority.

A position only states where the system acts or observes.

## Claim boundary

A claim boundary states what the system may assert.

Claims should be narrow, testable, and tied to artifacts or verification behavior.

Examples:

- This output hash matches the recorded output artifact.
- This timestamp receipt corresponds to a recorded runtime event.
- This packet manifest recomputes against the included files.
- This discovery return is structurally REVIEWABLE.
- This evidence boundary identifies captured, hashed, externally referenced, unavailable, not checked, and out-of-scope artifacts.

Claims should not be expanded by implication.

## Non-claim boundary

A non-claim boundary states what the system must not be treated as proving.

Examples:

- Does not prove AI output correctness.
- Does not prove decision correctness.
- Does not prove source completeness.
- Does not assert legal admissibility.
- Does not satisfy compliance obligations.
- Does not perform audit.
- Does not own risk acceptance.
- Does not own remediation.
- Does not own reporting.
- Does not control workflow execution.
- Does not inherit institutional authority.

Non-claims are not marketing disclaimers.

They are system invariants.

## Artifact handoff

Artifact handoff occurs when one system emits an artifact that another system consumes, references, hashes, stores, verifies, or includes in a later record.

Possible handoff artifacts include:

- output hash;
- trace ID;
- timestamp;
- model invocation reference;
- public-log receipt;
- runtime receipt;
- external pointer;
- artifact digest;
- signed assertion;
- sealed assertion;
- model identifier;
- prompt reference;
- prompt-template reference;
- output reference;
- event reference;
- verification receipt;
- manifest entry;
- source-system export;
- policy snapshot;
- authority marker;
- escalation state;
- review note.

## Handoff rule

An artifact may pass between systems only with its claim boundary attached.

The receiving system must record what the artifact does and does not prove.

Example:

A runtime output receipt may be included in an evidence packet.

That does not mean the evidence packet proves the output was correct.

Example:

An evidence packet may reference a runtime receipt.

That does not mean the runtime system proves the whole workflow evidence surface was complete.

## Pairwise boundary map

When two systems are mapped together, the map should describe the relationship explicitly.

### Required pairwise fields

| Field | Meaning |
|---|---|
| SYSTEM_A | First system. |
| SYSTEM_B | Second system. |
| SHARED_WORKFLOW_SURFACE | Workflow or scenario where both systems may apply. |
| ARTIFACTS_FROM_A_TO_B | Artifacts A may safely hand to B. |
| ARTIFACTS_FROM_B_TO_A | Artifacts B may safely hand to A. |
| CLAIMS_PRESERVED | Claims that remain valid during handoff. |
| CLAIMS_NOT_INHERITED | Claims that must not transfer. |
| AUTHORITY_RETAINED_BY | Institution, human reviewer, legal function, compliance function, risk owner, or other authority holder. |
| FAILURE_MODES | Ways the mapping can fail or become misleading. |
| REVIEWER_BURDEN | What later reviewers must still evaluate. |
| NEXT_PROOF | Minimal demonstration needed before stronger claims are made. |

## Non-inheritance rules

No claim silently transfers between systems.

The following claim classes must never transfer unless explicitly declared and independently supported:

- correctness;
- completeness;
- legal sufficiency;
- compliance satisfaction;
- liability outcome;
- audit sufficiency;
- institutional authority;
- decision justification;
- workflow continuation;
- source completeness;
- human-review sufficiency;
- remediation sufficiency;
- final action appropriateness;
- deployment readiness;
- production fitness.

## Authority boundary

Mapped systems do not own institutional authority unless that authority is explicitly delegated by the institution.

By default, the institution retains authority over:

- action;
- approval;
- denial;
- escalation;
- legal interpretation;
- compliance posture;
- risk acceptance;
- remediation;
- reporting;
- audit conclusions;
- liability conclusions;
- production deployment decisions.

## Dependency boundary

Mapping systems together does not automatically create a runtime dependency.

A system may reference another system artifact without depending on that system for workflow continuity.

Dependency must be declared separately from artifact handoff.

## Verification model

Each mapped system should state how its artifacts or claims are verified.

Verification models may include:

- checksum recomputation;
- manifest verification;
- public-log verification;
- timestamp receipt verification;
- signature verification;
- schema validation;
- state classification;
- replay or reconstruction;
- independent verifier output;
- human review;
- external audit inspection.

A verification model should state what successful verification means and what it does not mean.

## Failure states

Mapped systems should declare failure states.

Common failure states include:

- FAIL;
- INCOMPLETE;
- BLOCKED;
- NOT_CHECKED;
- PARTIAL;
- STALE_CONTEXT;
- OUT_OF_SCOPE;
- SOURCE_UNAVAILABLE;
- AUTHORITY_GAP;
- ACCESS_MODEL_BLOCKED;
- SECURITY_BLOCKED;
- UNACCEPTED_NON_CLAIMS;
- CLAIM_BOUNDARY_VIOLATION;
- PROHIBITED_INHERITANCE;
- VERIFICATION_FAILED.

## Example system positions

These examples are illustrative only.

They do not certify, endorse, integrate, or fully describe any external system.

### Fork

Pipeline position:

- workflow evidence preservation;
- evidence boundary verification;
- evidentiary reconstruction.

Supported claim boundary:

Fork may support claims about what evidence was captured, hashed, externally referenced, unavailable, not checked, out of scope, and whether the preserved record verifies against a declared evidence boundary.

Explicit non-claims:

Fork does not claim AI output correctness, decision correctness, source completeness, legal admissibility, compliance satisfaction, audit performance, risk acceptance, remediation ownership, reporting ownership, institutional authority, or runtime workflow control.

### Runtime anchoring system

Pipeline position:

- model invocation recording;
- runtime output anchoring;
- external receipt generation.

Supported claim boundary:

A runtime anchoring system may support claims that a specific output, trace, hash, or invocation artifact existed at a certain point and can be checked against a receipt, log, signature, or public reference.

Explicit non-claims:

A runtime anchoring system should not be treated as proving workflow completeness, human-review sufficiency, final decision correctness, legal admissibility, compliance satisfaction, liability resolution, or institutional authority.

### Execution validity system

Pipeline position:

- execution control;
- continuation validity;
- pressure-route visibility;
- assumption health review.

Supported claim boundary:

An execution validity system may support claims about whether continuation remained justified under live or degraded operating conditions, subject to its declared telemetry and authority model.

Explicit non-claims:

An execution validity system should not be treated as preserving the full downstream evidentiary record unless it explicitly does so within a declared evidence boundary.

### Policy admissibility system

Pipeline position:

- pre-execution governance;
- admissibility review;
- policy gatekeeping.

Supported claim boundary:

A policy admissibility system may support claims that a proposed action satisfied, failed, or required review under a declared policy or authority framework.

Explicit non-claims:

A policy admissibility system should not be treated as proving later evidence completeness, AI truth, final decision correctness, or legal sufficiency beyond its declared scope.

## Example pairwise map: Fork and runtime anchoring system

Shared workflow surface:

AI-assisted vendor review.

Runtime anchoring lens:

- What did the AI produce?
- When was it produced?
- Was the output anchored externally?
- Can the output record be checked later?
- Was the runtime record altered after the fact?

Fork lens:

- What was requested?
- What evidence was available?
- What did the model output?
- What did the human reviewer see?
- What was reviewed?
- What was not checked?
- What was unavailable?
- What was externally referenced?
- What claims were made?
- What claims remain supportable?
- Does the preserved record still verify against the declared evidence boundary?

Safe handoff artifacts:

- output hash;
- trace ID;
- timestamp;
- model invocation reference;
- runtime receipt;
- public-log receipt;
- external pointer.

Claims preserved:

- Runtime artifact existed according to the anchoring model.
- Evidence packet included or referenced the artifact according to the declared Fork boundary.

Claims not inherited:

- AI output correctness;
- workflow completeness;
- source completeness;
- human-review sufficiency;
- final decision correctness;
- legal admissibility;
- compliance satisfaction;
- liability resolution;
- institutional authority.

## Example pairwise map: Fork and execution validity system

Shared workflow surface:

AI-assisted vendor review or remote operational control.

Execution validity lens:

- Should the workflow have continued?
- Were assumptions still healthy?
- Was telemetry fresh enough?
- Was authority still applicable?
- Were pressure routes exposed?
- Were escalation conditions triggered?

Fork lens:

- Can the record later show what was requested, produced, reviewed, unavailable, not checked, and still supportable?
- Does the evidence boundary verify?
- Which states were captured, hashed, externally referenced, unavailable, or out of scope?

Claims preserved:

- Execution validity system may record continuation-validity assessment under its own boundary.
- Fork may preserve that assessment as an artifact within a declared evidence boundary.

Claims not inherited:

- Fork does not inherit authority to decide whether continuation should have occurred.
- Execution validity system does not inherit Fork claims about evidence packet integrity unless it verifies or consumes them under a declared boundary.

## Shared scenario: AI-assisted vendor review

A vendor is reviewed through an AI-assisted workflow.

The workflow may include:

- procurement or vendor-risk request;
- source evidence;
- vendor questionnaire;
- supporting documents;
- model output;
- AI-generated summary;
- risk classification;
- human review;
- approval;
- denial;
- escalation;
- final action;
- later audit, legal, compliance, or risk review.

Possible failure:

The runtime output may be validly anchored.

The evidence record may later be reconstructable.

The final approval may still be flawed because evidence was stale, missing, unavailable, not checked, escalations were ignored, authority was incomplete, or the risk classification was misapplied.

Lesson:

Runtime verification does not prove workflow justification.

Evidence reconstruction does not prove decision correctness.

Execution validity does not prove evidence completeness.

Each layer matters, but each layer must keep its own claim boundary.

## Next proof pattern

A useful minimal proof should show systems reinforcing each other without claim collapse.

Candidate sequence:

1. Select one AI-assisted workflow.
2. Complete or simulate a discovery return.
3. Classify the return as REVIEWABLE / INCOMPLETE / BLOCKED.
4. If REVIEWABLE, draft a client-specific evidence boundary.
5. Define captured, hashed, externally referenced, unavailable, not checked, and out-of-scope artifacts.
6. Identify safe artifacts from neighboring systems.
7. Build a minimal bridge for that assessed workflow only.
8. Generate observed workflow events.
9. Construct a sealed evidence packet.
10. Verify the packet independently.
11. Confirm explicit non-claims remain intact.

## Fork-specific use of this protocol

Fork may use this protocol to map neighboring systems without being absorbed into them.

This helps protect Fork from being miscategorized as:

- runtime anchoring;
- execution control;
- compliance automation;
- legal judgment;
- audit performance;
- correctness verification;
- institutional authority;
- generic AI trust.

Fork can instead remain mapped as:

- read-only evidence preservation;
- recomputable evidence boundary;
- evidentiary reconstruction;
- explicit non-claim enforcement.

## Protocol maturity

This v0.1 document is a mapping protocol, not a formal standard.

It is intended to support disciplined technical conversations between AI governance builders, enterprise architects, legal operations leaders, audit/risk/compliance reviewers, and implementation teams.

## Approved short-form language

Systems may exchange artifacts, but they may not silently exchange claims.

The goal is not to merge adjacent governance systems. The goal is to make their boundaries operationally mappable.

Fork does not need to absorb neighboring systems to cooperate with them.

Neighboring systems do not need to absorb Fork to reference Fork artifacts.

What matters is claim discipline, artifact discipline, and authority discipline.

## Closing statement

AI governance will not be solved by one system absorbing all functions.

It will require adjacent systems with clearly declared claim boundaries, explicit non-claims, safe artifact handoffs, and prohibited inheritance rules.

This protocol is a first step toward making those boundaries operationally inspectable.
