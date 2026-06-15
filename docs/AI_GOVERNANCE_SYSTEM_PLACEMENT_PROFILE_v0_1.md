# AI Governance System Placement Profile v0.1

Status: Draft doctrine artifact
Scope: Conceptual contract for future schema/checker implementation
Related family: AI Governance Mapping Record
Claim boundary: Placement and handoff declaration only

---

## 1. Purpose

The AI Governance System Placement Profile defines how an AI governance system declares where it sits in a broader governance environment.

It exists to prevent implicit authority inheritance across systems.

A governance system may evaluate, monitor, classify, review, map, escalate, preserve, or report. But downstream systems must not silently treat those outputs as approval, compliance satisfaction, legal sufficiency, audit sufficiency, safety assurance, or institutional authorization unless such claims are explicitly declared, bounded, evidenced, and handed off.

The Placement Profile provides a machine-checkable structure for declaring:

* what a governance system is;
* what role it performs;
* what claims it supports;
* what claims it explicitly does not support;
* what evidence it consumes;
* what evidence it emits;
* what conditions bound its claims;
* what unknowns remain unresolved;
* what handoffs are required;
* what downstream authority must still decide.

---

## 2. Core Doctrine

### 2.1 Non-Transitive Governance Claims

No governance claim is transitive by default.

A claim made by one governance system does not automatically propagate to another system, workflow, reviewer, institution, or decision environment.

A claim may only propagate if the record explicitly declares:

1. the claim;
2. the scope of the claim;
3. the evidence basis for the claim;
4. the non-claims that must travel with it;
5. the unresolved unknowns that remain;
6. the required downstream handoff;
7. the role authorized to interpret or rely on it.

### 2.2 Claim Production vs. Claim Interpretation

The Placement Profile separates claim production from claim interpretation.

A governance system may produce a bounded claim.

A downstream reviewer, institution, or governance process may interpret that claim.

Fork does not collapse those acts.

Fork does not decide whether a governance claim is true, sufficient, legally meaningful, compliant, safe, or institutionally authorized. Fork preserves the boundary around what was declared and what was not declared.

---

## 3. Relationship to Fork

Fork does not rank AI governance systems.

Fork does not replace policy systems, evaluation systems, monitoring systems, compliance systems, audit systems, legal review systems, runtime control systems, or human decision systems.

Fork provides a placement and handoff grammar by which those systems can declare their role, claim boundaries, evidence interfaces, unresolved unknowns, and downstream dependencies.

The Placement Profile is therefore an extension of the AI Governance Mapping Record family. It should be treated as a system-placement profile within the broader mapping-record architecture, not as a replacement for the existing checker lineage.

Recommended naming:

AI Governance Mapping Record: System Placement Profile v0.1

---

## 4. Admission Gate for New Placement Designs

A proposed placement design should only be built if it passes all three gates.

### 4.1 Need

Does AI governance actually need this placement concept?

The design should address a real governance failure mode, such as:

* claim leakage;
* silent authority inheritance;
* ambiguous handoffs;
* unresolved unknowns being hidden;
* downstream reviewers misreading upstream outputs;
* system roles being confused with institutional authority.

### 4.2 Fork Fit

Can Fork represent the concept as evidence-boundary structure?

A concept fits Fork if it can be expressed through:

* claims;
* non-claims;
* evidence inputs;
* evidence outputs;
* handoff requirements;
* unresolved unknowns;
* verification states;
* reviewer or institutional boundaries.

A concept does not fit Fork if it requires Fork to become:

* a policy engine;
* a legal authority;
* a compliance oracle;
* an audit substitute;
* a runtime controller;
* a model evaluator;
* a decision validator;
* an institutional approval system.

### 4.3 External Legibility

Can another governance system understand its placement without accepting Fork as authority?

The record must let external systems declare their own boundaries without being absorbed into Fork.

Fork should make placement legible. It should not force ecosystem lock-in.

---

## 5. Minimal Required Core

A minimal Placement Profile should include the following fields.

### 5.1 System Identity

Identifies the governance system being placed.

Expected content:

* system name;
* system version;
* publisher or maintainer;
* record identifier;
* record version;
* profile creation timestamp;
* profile status.

The identity section does not prove that the system exists, is deployed, is trustworthy, or is authorized. It only identifies the system as declared in the record.

### 5.2 Role Classification

Declares the governance role performed by the system.

Example role classes:

* evaluator;
* runtime monitor;
* policy mapper;
* compliance mapper;
* legal review support;
* audit support;
* human review workflow;
* risk scoring system;
* incident response system;
* evidence preservation system;
* provenance system;
* escalation router;
* workflow orchestrator.

A system may declare multiple roles, but each role must preserve its own claim boundaries.

### 5.3 Authority Boundary

Declares what the system is authorized to do and what it is not authorized to do.

This section should distinguish operational function from institutional authority.

Example:

A monitoring system may detect anomalies within defined thresholds.

That does not mean it approves deployment, satisfies compliance, determines legal admissibility, or accepts institutional risk.

### 5.4 Supported Claims

Declares positive assertions the system supports.

Supported claims must be bounded by:

* conditions;
* evidence basis;
* scope;
* version;
* applicable environment;
* known limitations;
* required handoffs.

Example:

“System X detects policy-threshold deviations in observed workflow events according to rule set Y version Z.”

This is a bounded claim.

It is not a claim that the workflow is compliant, safe, lawful, complete, or approved.

### 5.5 Explicit Non-Claims

Declares claims the system does not make.

Non-claims must be explicit enough to prevent downstream authority inflation.

Common non-claims include:

* no claim of AI output correctness;
* no claim of decision correctness;
* no claim of source completeness;
* no claim of legal admissibility;
* no claim of compliance satisfaction;
* no claim of audit sufficiency;
* no claim of institutional approval;
* no claim of runtime control;
* no claim of policy authority;
* no claim of risk acceptance;
* no claim of safety assurance;
* no claim of deployment authorization.

Non-claims are not decorative. They are part of the evidence boundary.

### 5.6 Evidence Inputs

Declares the evidence the system requires or consumes.

Evidence inputs may include:

* model evaluation reports;
* workflow event records;
* human review records;
* policy documents;
* runtime telemetry;
* audit logs;
* risk assessments;
* incident records;
* data lineage records;
* provenance artifacts;
* prior placement records.

Each evidence input should identify:

* input type;
* source;
* expected format;
* custody expectation;
* freshness expectation;
* completeness assumption;
* whether the input is required or optional.

### 5.7 Evidence Outputs

Declares the evidence the system emits.

Evidence outputs may include:

* findings;
* alerts;
* classifications;
* mappings;
* review records;
* verification receipts;
* anomaly records;
* unresolved unknown reports;
* handoff packets;
* evidence manifests.

Each evidence output should identify:

* output type;
* format;
* claim supported;
* claim not supported;
* downstream role expected to review or interpret it.

### 5.8 Handoff Requirements

Declares required downstream roles, not merely named systems.

A handoff should specify:

* required downstream role;
* reason for handoff;
* evidence to be handed off;
* non-claims that must travel with the handoff;
* unresolved unknowns that must remain visible;
* whether the handoff is blocking, advisory, or informational.

Example downstream roles:

* legal reviewer;
* compliance officer;
* audit reviewer;
* risk owner;
* model governance owner;
* human decision authority;
* incident response lead;
* deployment approver;
* policy owner.

A handoff does not prove the downstream role accepted responsibility. It only declares that the upstream system requires that role before further interpretation or action.

### 5.9 Unresolved Unknowns

Declares known epistemic gaps.

Unknowns may include:

* source completeness uncertainty;
* data drift;
* distribution shift;
* missing telemetry;
* incomplete human review;
* unresolved policy conflict;
* unsupported jurisdictional mapping;
* uncertain model behavior;
* ambiguous authority boundary;
* external dependency not verified.

Unknowns should be classified as either:

* declared unknown classes;
* active unresolved unknowns.

Declared unknown classes identify categories of uncertainty inherent to the system.

Active unresolved unknowns identify specific unresolved gaps affecting the current placement or handoff.

### 5.10 Verification State

Declares how the placement record has been checked.

Possible states:

* SELF_DECLARED;
* STRUCTURALLY_CHECKED;
* EXTERNALLY_REVIEWED;
* VERIFIED_AGAINST_SCHEMA;
* VERIFIED_AGAINST_CHECKER;
* INDETERMINATE;
* NOT_CHECKED.

Verification state does not mean the underlying governance claim is true. It only describes the status of the record or evidence boundary check.

---

## 6. Optional Extensions

Optional extensions may be added without making the minimal profile too heavy.

Recommended optional extensions:

* claim conditions;
* non-transitive clauses;
* local definitions;
* reviewer role requirements;
* external framework mappings;
* confidence conditions;
* evidence retention expectations;
* freshness constraints;
* jurisdictional notes;
* deployment environment notes;
* upstream and downstream placement references.

These extensions should remain bounded. They must not convert the Placement Profile into a policy engine, compliance checker, legal review system, runtime controller, or decision authority.

---

## 7. Validation States

Placement records should distinguish well-formedness, completeness, and verification.

### 7.1 Well-Formed

A record is well-formed if it contains required fields, valid identifiers, valid role classifications, declared claims, declared non-claims, evidence interfaces, handoff requirements, and no structural conflicts.

A well-formed record may still be incomplete, unverified, or substantively wrong.

### 7.2 Complete

A record is complete if it provides enough placement information for downstream reviewers to understand the system’s role, claim boundaries, evidence interfaces, unknowns, and handoff requirements.

Completeness does not prove correctness, sufficiency, compliance, legality, or safety.

### 7.3 Verified

A record is verified if a specified checker or reviewer has evaluated the record against a specified contract.

Verification must state what was verified.

Examples:

* schema conformance verified;
* required fields verified;
* claim/non-claim disjointness verified;
* restricted authority leakage checked;
* handoff references checked;
* unresolved unknown status checked.

Verification does not imply that the underlying governance claims are true unless that is separately and explicitly established by an authorized system.

### 7.4 Indeterminate

A record is indeterminate if unresolved unknowns, missing dependencies, ambiguous authority boundaries, or incomplete evidence prevent a clean pass/fail status.

Indeterminate is not failure. It is a bounded declaration that the record cannot be responsibly closed under current evidence.

---

## 8. Non-Transitive Clauses

A Placement Profile should support explicit non-transitive clauses.

These clauses declare what cannot propagate downstream by implication.

Examples:

* An evaluation result does not propagate as deployment approval.
* A monitoring result does not propagate as compliance satisfaction.
* A human review record does not propagate as institutional risk acceptance.
* A policy mapping does not propagate as legal advice.
* An audit-support finding does not propagate as audit sufficiency.
* A provenance record does not propagate as source completeness.
* A verification receipt does not propagate as truth of the underlying claim.

Non-transitive clauses are central to the profile.

They prevent false closure.

---

## 9. Illustrative Example

### 9.1 Evaluation System Placement

System role:

* evaluator

Supported claim:

* benchmark risk reduction was observed under defined test conditions.

Explicit non-claims:

* no claim of real-world safety;
* no claim of regulatory compliance;
* no claim of deployment approval;
* no claim of adversarial robustness outside tested conditions;
* no claim of decision correctness.

Evidence inputs:

* benchmark suite;
* model version;
* test configuration;
* evaluation run records.

Evidence outputs:

* evaluation report;
* benchmark result summary;
* unresolved limitation list.

Handoff requirements:

* deployment risk review;
* runtime monitoring;
* compliance mapping;
* human institutional approval before production use.

Unresolved unknowns:

* distribution shift;
* adversarial adaptation;
* incomplete real-world telemetry;
* jurisdictional policy variance.

Non-transitive clause:

* Evaluation success does not propagate as deployment approval or compliance satisfaction.

### 9.2 Monitoring System Placement

System role:

* runtime monitor

Supported claim:

* anomaly threshold detection was performed on observed workflow telemetry.

Explicit non-claims:

* no claim of policy adherence;
* no claim of legal compliance;
* no claim of complete telemetry;
* no claim of incident absence;
* no claim of runtime control unless separately declared.

Evidence inputs:

* telemetry feed;
* threshold configuration;
* observed event stream.

Evidence outputs:

* alert record;
* anomaly classification;
* monitoring receipt.

Handoff requirements:

* incident review if alert threshold is crossed;
* risk owner review if unresolved anomalies persist.

Unresolved unknowns:

* silent failure modes;
* missing telemetry;
* threshold misconfiguration;
* unobserved behavior outside instrumentation.

Non-transitive clause:

* Monitoring pass does not propagate as compliance satisfaction or safety assurance.

### 9.3 Compliance Mapping System Placement

System role:

* compliance mapper

Supported claim:

* declared workflow evidence was mapped against specified policy requirements.

Explicit non-claims:

* no claim of legal advice;
* no claim of regulatory approval;
* no claim of audit sufficiency;
* no claim of complete evidence;
* no claim of institutional risk acceptance.

Evidence inputs:

* policy requirements;
* evaluation evidence;
* monitoring evidence;
* human review records;
* unresolved unknowns from upstream systems.

Evidence outputs:

* compliance mapping record;
* gap list;
* required reviewer list.

Handoff requirements:

* legal reviewer;
* compliance officer;
* institutional risk owner.

Unresolved unknowns:

* ambiguous policy interpretation;
* missing evidence;
* jurisdictional variation;
* unresolved upstream non-claims.

Non-transitive clause:

* Compliance mapping does not propagate as compliance satisfaction unless an authorized compliance role explicitly asserts that conclusion.

---

## 10. Checker Implications

A future checker for this profile should initially verify only structural and boundary properties.

Initial checker scope may include:

* required fields present;
* valid profile version;
* valid role classification;
* claim and non-claim arrays present;
* claim/non-claim disjointness;
* restricted authority leakage guard;
* evidence input/output structure;
* handoff role references;
* unresolved unknown declaration;
* verification state declaration;
* non-transitive clause presence;
* duplicate ID rejection;
* local reference integrity;
* normalized output emission.

Initial checker scope should not include:

* semantic truth of claims;
* legal sufficiency;
* compliance sufficiency;
* audit sufficiency;
* model safety;
* runtime enforcement;
* institutional approval;
* external artifact existence unless separately scoped;
* cross-record graph validity unless introduced by a later version.

---

## 11. Public Positioning

Safe description:

Fork provides machine-checkable placement records for AI governance systems, enabling each system to declare its claim boundaries, non-claims, evidence interfaces, unresolved unknowns, and required handoffs so that authority is never implicitly inherited across systems.

Shorter description:

Fork makes governance claims non-transitive unless explicitly declared.

Do not describe this profile as:

* a governance framework;
* a compliance engine;
* a legal verification system;
* an audit substitute;
* a runtime control layer;
* a model safety evaluator;
* an institutional approval system;
* a universal AI governance standard.

---

## 12. v0.1 Status

This v0.1 document is a doctrine and design artifact.

It is not yet a schema.

It is not yet a checker.

It does not add runtime behavior.

It defines the conceptual contract for future implementation of a System Placement Profile within the AI Governance Mapping Record family.

The next appropriate step is to create a minimal schema and fixture set only after this doctrine is reviewed for:

* need;
* Fork fit;
* external legibility;
* non-transitive claim clarity;
* non-claim completeness;
* handoff semantics;
* implementation weight.
