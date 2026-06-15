# Fork Release Package Ladder v0.1

## Purpose

This document defines the bounded release-package ladder for Fork.

Fork should not have one master package that is sent to every reviewer, prospect, or technical evaluator. Different audiences require different levels of disclosure, different evidence, different claims, and different non-claims.

The purpose of this ladder is to ensure that Fork can respond cleanly when a reviewer, buyer, integration partner, or pilot-ready client asks:

"What can you send me?"

The answer should depend on the stage of seriousness, the recipient role, and the evidence boundary being discussed.

Fork's release packages must preserve the same discipline as the system itself:

- Bounded scope
- Explicit claims
- Explicit non-claims
- Read-only posture
- No implied authority
- No implied runtime control
- No implied legal admissibility
- No implied source completeness
- No implied decision correctness

A release package should never create a stronger claim than the underlying artifacts can support.

## Relationship to Fork's operational boundary

This ladder extends the operational boundary defined in:

`docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`

The operational boundary map states the core production principle:

Fork validates system boundaries by preserving evidence of hand-offs, not by absorbing the functions on either side.

The release package ladder applies that principle to external communication and delivery.

A package may describe authority mechanisms, workflow mechanisms, audit mechanisms, compliance mechanisms, legal review, risk, security response, remediation, or reporting.

But a Fork package must not imply that Fork owns those mechanisms.

Fork remains the evidence hand-off.

## Core release rule

Every Fork release package must answer four questions:

1. Who is this package for?
2. What stage of seriousness does it correspond to?
3. What exactly does it prove, support, or prepare?
4. What must not be inferred from it?

The fourth question is mandatory.

If a package does not clearly state what must not be inferred, it is not release-ready.

## Package ladder overview

Fork's bounded release package ladder contains six package types:

1. Public Doctrine Packet
2. Executive Buyer Packet
3. Technical Validation Packet
4. Pilot Discovery Packet
5. Pilot-Ready Implementation Packet
6. Client Evidence Boundary Packet

These packages are not maturity claims by themselves.

They are disclosure levels.

A later package in the ladder does not mean Fork is claiming broader authority. It means the discussion has become more specific, more qualified, and more bounded.

## 1. Public Doctrine Packet

### Purpose

Establish Fork's category, doctrine, and boundary.

This package is for public review and early-stage orientation. It should help a reader understand what Fork is, what it is not, why recomputable evidence matters, and where the project currently stands.

### Intended recipients

- LinkedIn contacts
- AI governance practitioners
- Legal, audit, compliance, and risk reviewers
- Early technical readers
- General public repository visitors
- People asking "What is Fork?"

### Typical contents

- Repository README
- Reading Guide
- Operational Boundary Map v0.1
- White paper or public doctrine paper
- Public release notes
- Public schemas, examples, and verification materials
- Claims and non-claims summary

### Supported claim

Fork is a public, bounded, recomputable evidence project with doctrine, executable evidence constraints, and versioned public artifacts.

### Non-claims

This package does not claim:

- Enterprise production deployment
- Legal admissibility
- Source completeness
- Decision correctness
- Runtime enforcement
- Compliance satisfaction
- Client-specific readiness
- Integration with any live enterprise system

### Send when

Use this package when the recipient needs to understand the category and public evidence posture.

## 2. Executive Buyer Packet

### Purpose

Help a decision-maker understand why Fork matters commercially.

This package translates Fork into buyer-facing language without overloading the reader with code, schemas, or implementation details.

### Intended recipients

- General Counsel
- Chief Legal Officer
- Chief Compliance Officer
- Chief Risk Officer
- Audit leadership
- Legal operations leadership
- Governance and risk executives
- Enterprise AI governance sponsors

### Typical contents

- One-page or two-page executive brief
- Buyer problem statement
- "What can we prove six months later?" framing
- Operational Boundary Map summary
- Priority use cases
- Pilot path overview
- High-level technical validation summary
- Public repository reference

### Supported claim

Fork addresses a reconstructive-fidelity gap in AI-assisted workflows by preserving bounded evidence records for later review.

### Non-claims

This package does not claim:

- Fork replaces governance, compliance, legal review, audit, or risk
- Fork decides whether an action was valid
- Fork proves AI output correctness
- Fork can reconstruct hidden vendor behavior
- Fork is a general-purpose enterprise control plane
- Fork is production-deployed in the recipient's environment

### Send when

Use this package when an executive wants to understand relevance, buyer pain, commercial fit, and pilot suitability.

## 3. Technical Validation Packet

### Purpose

Demonstrate that Fork has an actual technical spine.

This package is for technical diligence and evidence validation. It should show that Fork is not merely a doctrine or article series. It should demonstrate bounded packet construction, sealing, verification, failure reporting, and explicit non-claims.

### Intended recipients

- CTO
- CISO
- Engineering evaluator
- Security architect
- Technical diligence reviewer
- Integration partner
- AI infrastructure lead
- Audit technology lead

### Typical contents

- Architecture overview
- Evidence packet structure
- Schema references
- Example packets
- Verifier instructions
- PASS / FAIL / NOT_CHECKED examples
- PARTIAL / STALE_CONTEXT / OUT_OF_SCOPE / SOURCE_UNAVAILABLE semantics where applicable
- SHA-256 manifest
- Tamper or failure demonstration
- Boundary tests showing Fork does not control the workflow
- Claims and non-claims

### Supported claim

Fork can produce and verify bounded evidence artifacts under controlled conditions.

### Non-claims

This package does not claim:

- Production operation inside a client environment
- Full replay of AI model behavior
- Source completeness
- Legal admissibility
- Runtime blocking or enforcement
- Correctness of any AI-assisted decision
- Completeness of external vendor telemetry

### Send when

Use this package when the recipient asks:

"Is this real technically?"

or:

"What can I inspect, run, or verify?"

## 4. Pilot Discovery Packet

### Purpose

Prepare a serious client conversation before any deployment or proof-of-value pilot.

This package helps determine whether a client workflow is suitable for Fork. It should define the discovery process, evidence sources, candidate workflows, and boundary questions.

### Intended recipients

- Serious prospect
- Pilot sponsor
- Legal operations lead
- Audit or compliance lead
- Risk lead
- Enterprise AI governance lead
- Technical integration counterpart

### Typical contents

- Pilot purpose
- Candidate workflow list
- Stakeholder interview map
- Evidence boundary worksheet
- Source system inventory
- Artifact categories:
  - captured evidence
  - hashed reference
  - external pointer
  - unavailable source
  - explicit non-claim
- Workflow suitability criteria
- Security and data-handling questions
- Read-only sidecar explanation
- Pilot success criteria
- Next-step checklist

### Supported claim

Fork can evaluate whether a defined client workflow is suitable for bounded evidence preservation.

### Non-claims

This package does not claim:

- The workflow is already suitable
- Fork can ingest every relevant system
- Fork can capture hidden backend facts
- Fork can reconstruct missing evidence
- Fork will block or control the client workflow
- Fork will satisfy legal, audit, or compliance obligations by itself

### Send when

Use this package when a prospect asks:

"How would we evaluate a pilot?"

or:

"What would you need from us?"

## 5. Pilot-Ready Implementation Packet

### Purpose

Define the actual bounded proof-of-value or design-partner pilot.

This package is for qualified opportunities after discovery. It should be specific enough to support planning, scoping, internal review, and commercial discussion.

### Intended recipients

- Qualified pilot sponsor
- Legal or compliance owner
- Technical implementation owner
- Procurement or vendor-risk reviewer
- Security reviewer
- Executive sponsor

### Typical contents

- Pilot scope
- Workflow selection
- Integration boundary
- Source system matrix
- Evidence artifact map
- Read-only capture mechanism
- Deployment assumptions
- Data-handling assumptions
- Security posture
- Verification process
- Roles and responsibilities
- Deliverables
- Acceptance criteria
- Known limitations
- Explicit non-claims
- Timeline
- Commercial terms, if appropriate

### Supported claim

Fork is ready for a bounded proof-of-value pilot against defined workflows, defined source systems, defined evidence artifacts, and defined verification outputs.

### Non-claims

This package does not claim:

- General enterprise production readiness
- Full source completeness
- Full model behavior replay
- Legal admissibility
- Decision correctness
- Compliance satisfaction
- Runtime enforcement
- Authority over remediation or reporting

### Send when

Use this package only after the workflow, sponsor, source systems, security expectations, and pilot objective are sufficiently qualified.

## 6. Client Evidence Boundary Packet

### Purpose

Define the exact evidence boundary for one client workflow.

This is the most specific package in the ladder. It is not generic marketing material. It is a workflow-specific boundary artifact.

### Intended recipients

- Client pilot team
- Legal reviewer
- Compliance reviewer
- Audit reviewer
- Risk reviewer
- Security reviewer
- Technical integration team

### Typical contents

- Client workflow name
- Workflow purpose
- Systems observed
- Systems not observed
- Events captured
- Events not captured
- Artifact retention model
- Copy / hash / reference rules
- Verification states
- Known blind spots
- Escalation and response ownership
- Source availability assumptions
- Explicit non-claims
- Client-specific acceptance criteria

### Supported claim

For this workflow, Fork preserves this defined evidence boundary and nothing beyond it.

### Non-claims

This package does not claim:

- Other workflows are covered
- Unobserved systems are represented
- Missing artifacts can be reconstructed
- External vendor behavior is fully known
- Fork owns response, remediation, or reporting
- Fork's verification state is a legal or compliance conclusion

### Send when

Use this package only after discovery has identified a specific workflow and the evidence boundary can be stated precisely.

## Universal package controls

Every Fork release package should include the following controls unless there is a specific reason not to.

### Required file set

- `README.md`
- `PACKAGE_MANIFEST.json`
- `CLAIMS_AND_NON_CLAIMS.md`
- `RELEASE_NOTES.md`
- `SHA256SUMS.txt`
- `NEXT_STEPS.md`

### Required language

Every package should state:

- What the package is for
- Who it is for
- What it supports
- What it does not support
- What stage it corresponds to
- Whether it is public, restricted, client-specific, or NDA-only
- Whether it contains executable evidence materials
- Whether it contains client-specific assumptions

### Required non-claim categories

Every package should address whether it does or does not claim:

- Decision correctness
- Legal admissibility
- Compliance satisfaction
- Source completeness
- Runtime control
- Authority validity
- Remediation sufficiency
- Reporting sufficiency
- Full replayability of AI behavior
- Completeness of vendor telemetry
- Production deployment

## Technical package controls

Technical packages may include:

- `schemas/`
- `examples/`
- `tools/`
- `verification_results/`
- `tamper_cases/`
- `manifests/`
- `SHA256SUMS.txt`

Technical packages must include a verifier path or explanation.

Technical packages must distinguish:

- record integrity
- artifact inclusion
- schema validity
- verification state
- non-claims
- unverified or unavailable sources

A technical package must not imply that a passing verification result proves decision correctness.

## Pilot package controls

Pilot packages may include:

- `pilot_scope.md`
- `workflow_selection_matrix.md`
- `evidence_boundary_worksheet.md`
- `source_system_inventory.md`
- `roles_and_responsibilities.md`
- `acceptance_criteria.md`
- `security_and_data_handling_questions.md`
- `known_limitations.md`

Pilot packages must define:

- workflow scope
- source systems
- observed events
- unobserved events
- artifact handling rules
- verification outputs
- responsible client functions
- response ownership
- out-of-scope conditions

A pilot package must not imply that Fork will become a runtime gate.

## Send matrix

| Situation | Recommended package |
|---|---|
| General LinkedIn interest | Public Doctrine Packet |
| AI governance practitioner asks what Fork is | Public Doctrine Packet |
| GC, CLO, CCO, CRO, or audit leader asks for an overview | Executive Buyer Packet |
| Legal ops or audit asks where Fork fits | Public Doctrine Packet plus Executive Buyer Packet |
| CTO, CISO, or engineer asks whether Fork is real | Technical Validation Packet |
| Integration partner asks what the stack does | Technical Validation Packet |
| Serious prospect asks how to evaluate a pilot | Pilot Discovery Packet |
| Qualified paid pilot discussion | Pilot-Ready Implementation Packet |
| Specific workflow under review | Client Evidence Boundary Packet |

## Build priority

Fork should not build all packages at once.

The first three packages to build are:

1. Public Doctrine Packet
2. Technical Validation Packet
3. Pilot Discovery Packet

These cover the near-term outreach path:

- public understanding
- technical credibility
- pilot qualification

The Pilot-Ready Implementation Packet should follow after the discovery packet is stable.

The Client Evidence Boundary Packet should remain a template until a real workflow is under review.

## Naming convention

Release package directories should use explicit versioned names:

- `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/`
- `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/`
- `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/`
- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`
- `release_packages/FORK_PILOT_READY_IMPLEMENTATION_PACKET_v0_1/`
- `release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/`

Package names should not imply production readiness unless the package is explicitly scoped to a bounded pilot or actual deployment context.

## Versioning rule

Package versions should change when:

- supported claims change
- non-claims change
- package contents change materially
- verifier behavior changes
- schema requirements change
- target audience changes
- pilot assumptions change

Cosmetic edits do not require a package version bump unless they affect interpretation.

## Release-readiness checks

Before sending any package externally, confirm:

- The package has a clear audience.
- The package has a clear stage.
- The package has a claims and non-claims file.
- The package does not imply authority or control.
- The package does not imply legal admissibility.
- The package does not imply source completeness.
- The package does not imply decision correctness.
- The package does not overstate production readiness.
- The package contains only materials appropriate to the recipient.
- The package can be explained in one sentence.

## One-sentence package test

A package is ready only if it can be described in one sentence without overclaiming.

Examples:

Public Doctrine Packet:

"This package explains Fork's public doctrine and evidence boundary for recomputable evidence in AI-assisted workflows."

Technical Validation Packet:

"This package demonstrates Fork's bounded packet, manifest, and verification mechanics under controlled conditions."

Pilot Discovery Packet:

"This package helps determine whether a specific client workflow is suitable for bounded, read-only evidence preservation."

Pilot-Ready Implementation Packet:

"This package defines a bounded proof-of-value pilot against specified workflows, source systems, evidence artifacts, and verification outputs."

Client Evidence Boundary Packet:

"This package states exactly what Fork preserves for this client workflow and what must not be inferred from that preserved record."

## Governing principle

Fork release packages should make the project easier to evaluate without making the project appear broader than it is.

The objective is not to impress every recipient with maximum scope.

The objective is to send the smallest package that truthfully answers the recipient's question.

That is how Fork preserves credibility as it moves from public doctrine to technical validation to pilot readiness.