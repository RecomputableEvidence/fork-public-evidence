# Fork Release Package Send Guide v0.1

## Purpose

This guide explains which Fork release package to send based on recipient, stage, question, and disclosure need.

It is an operating guide for live outreach, follow-up, executive review, technical diligence, and pilot qualification.

Fork should not send every recipient the same package.

The correct package is the smallest bounded package that truthfully answers the recipient's question without implying broader readiness, authority, control, legal admissibility, source completeness, decision correctness, or compliance satisfaction.

## Core send rule

Send the package that matches the recipient's current question.

Do not send a later-stage package merely to look more advanced.

Do not send a technical package when the question is executive fit.

Do not send a pilot package when the question is public orientation.

Do not send a client-specific boundary package until a real workflow has been identified.

The package should reduce ambiguity, not create a broader claim.

## Available packages

### Public Doctrine Packet

Path:

`release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/`

Use when the recipient asks:

- What is Fork?
- What is the doctrine?
- Where does Fork sit?
- What does Fork claim and not claim?
- What should I read first?

Primary audience:

- public reviewers
- LinkedIn contacts
- AI governance practitioners
- legal, audit, compliance, risk, security, and technical readers
- early category reviewers

Supported claim:

Fork has a public, bounded doctrine and evidence posture for recomputable evidence in AI-assisted workflows.

Do not use it to claim:

- pilot readiness
- client readiness
- production deployment
- legal admissibility
- source completeness
- decision correctness
- runtime enforcement

### Executive Buyer Packet

Path:

`release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/`

Use when the recipient asks:

- Why does this matter commercially?
- Where would this sit inside an enterprise?
- Who owns this problem?
- What buyer pain does Fork address?
- How would we think about a pilot?

Primary audience:

- General Counsel
- Chief Legal Officer
- Chief Compliance Officer
- Chief Risk Officer
- audit leadership
- legal operations leadership
- enterprise AI governance sponsor
- governance, risk, compliance, security, or information governance executives
- pilot sponsor

Supported claim:

Fork addresses a reconstructive-fidelity gap in AI-assisted workflows by preserving bounded evidence records for later review.

Do not use it to claim:

- technical proof beyond public technical materials
- client-specific readiness
- production deployment
- compliance satisfaction
- legal conclusions
- source completeness
- decision correctness

### Technical Validation Packet

Path:

`release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/`

Use when the recipient asks:

- Is Fork technically real?
- What can I inspect?
- What can I verify?
- What does the packet, manifest, checksum, schema, and verification posture look like?
- Can a technical reviewer run checks?

Primary audience:

- CTO
- CISO
- engineering evaluator
- security architect
- technical diligence reviewer
- integration partner
- AI infrastructure lead
- audit technology lead

Supported claim:

Fork has inspectable public technical materials for bounded evidence preservation and verification under controlled repository conditions.

Do not use it to claim:

- production operation inside a client environment
- full replay of AI model behavior
- complete vendor telemetry
- source completeness
- legal admissibility
- compliance satisfaction
- runtime enforcement
- decision correctness

### Pilot Discovery Packet

Path:

`release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`

Use when the recipient asks:

- How would we evaluate a pilot?
- What would you need from us?
- Which workflow would make sense?
- What systems would Fork need to observe?
- What would Fork capture and not capture?

Primary audience:

- serious enterprise prospect
- pilot sponsor
- legal operations lead
- compliance lead
- audit lead
- risk lead
- security or GRC reviewer
- enterprise AI governance lead
- technical integration counterpart
- workflow owner

Supported claim:

Fork can help evaluate whether a defined client workflow is suitable for bounded, read-only evidence preservation.

Do not use it to claim:

- the workflow is already suitable
- deployment is authorized
- source systems are sufficient
- Fork can ingest every relevant system
- Fork can reconstruct missing or hidden evidence
- Fork will control, block, approve, or enforce the workflow

## Send matrix

| Situation | Send |
|---|---|
| General LinkedIn interest | Public Doctrine Packet |
| Someone asks "What is Fork?" | Public Doctrine Packet |
| AI governance practitioner asks for background | Public Doctrine Packet |
| Legal, compliance, audit, or risk reader asks for orientation | Public Doctrine Packet |
| GC / CLO / CCO / CRO asks why this matters | Executive Buyer Packet |
| Legal operations lead asks where this fits | Executive Buyer Packet |
| Audit leader asks what problem this solves | Executive Buyer Packet |
| Executive sponsor asks how to think about a pilot | Executive Buyer Packet plus Pilot Discovery Packet |
| CTO / CISO / engineer asks if it is real | Technical Validation Packet |
| Integration partner asks what can be inspected | Technical Validation Packet |
| Technical reviewer asks for verifier/checksum posture | Technical Validation Packet |
| Prospect asks "How would we evaluate this?" | Pilot Discovery Packet |
| Prospect identifies a candidate workflow | Pilot Discovery Packet |
| Qualified pilot discussion after discovery | Pilot-Ready Implementation Packet when available |
| Specific workflow under review after discovery | Client Evidence Boundary Packet when available |

## Package combinations

### Public orientation only

Send:

1. Public Doctrine Packet

Use when:

The recipient is early, curious, or category-oriented.

Do not include:

- Executive Buyer Packet
- Technical Validation Packet
- Pilot Discovery Packet

unless the recipient asks a more specific question.

### Executive orientation

Send:

1. Executive Buyer Packet
2. Public Doctrine Packet as optional background

Use when:

The recipient is a senior decision-maker or buyer-facing stakeholder.

Do not lead with technical materials unless the executive asks for diligence or introduces a technical reviewer.

### Technical diligence

Send:

1. Technical Validation Packet
2. Public Doctrine Packet as boundary background

Use when:

The recipient asks whether Fork has inspectable mechanics.

Do not use this to imply production deployment.

### Pilot qualification

Send:

1. Pilot Discovery Packet
2. Executive Buyer Packet if the sponsor needs commercial framing
3. Technical Validation Packet if technical reviewers are involved

Use when:

The prospect has moved beyond category interest and wants to evaluate a possible workflow.

Do not imply that discovery is deployment.

### Client-specific workflow

Send:

1. Client Evidence Boundary Packet when available
2. Pilot-Ready Implementation Packet when available
3. Supporting package references as needed

Use only after:

- a workflow is identified
- source systems are known
- stakeholders are identified
- security/data-handling questions are open or answered
- non-claims can be stated

## Live response guide

### If asked: "Can you send me something?"

Ask or infer the recipient's need.

If no specific need is stated, send the Public Doctrine Packet.

Suggested reply:

"I can send the public doctrine orientation packet first. It explains what Fork is, what it does not claim, and where the evidence boundary sits."

### If asked: "Where would this fit inside our organization?"

Send the Executive Buyer Packet.

Suggested reply:

"The executive buyer packet is the right starting point. It maps Fork to legal, compliance, audit, risk, security, governance, and pilot-sponsor concerns without treating Fork as the authority or control plane."

### If asked: "Is there actual technical work behind this?"

Send the Technical Validation Packet.

Suggested reply:

"The technical validation packet is the right artifact. It points to the public packet, manifest, checksum, schema, and verification posture that can be inspected under controlled repository conditions."

### If asked: "How would we pilot this?"

Send the Pilot Discovery Packet.

Suggested reply:

"The pilot discovery packet is the right next step. It does not assume deployment. It helps determine whether a defined workflow is suitable for bounded, read-only evidence preservation."

### If asked: "Can Fork stop bad decisions?"

Do not send a pilot package first.

Clarify the boundary.

Suggested reply:

"Fork is not designed to stop or approve decisions. It preserves the evidence boundary so the appropriate legal, compliance, audit, risk, security, or operational function can review what happened."

Then send:

- Public Doctrine Packet
- Operational Boundary Map reference

### If asked: "Can Fork prove the AI was right?"

Do not send the Technical Validation Packet as if it proves correctness.

Clarify the boundary.

Suggested reply:

"Fork does not prove that AI output was correct. It preserves and verifies the bounded record of what was observable and captured."

Then send:

- Public Doctrine Packet
- Technical Validation Packet only if technical review is requested

### If asked: "Can Fork satisfy compliance requirements?"

Do not answer as if Fork is a compliance engine.

Suggested reply:

"Fork does not satisfy compliance obligations by itself. It preserves evidence that compliance, audit, legal, risk, or governance teams may later need to inspect."

Then send:

- Executive Buyer Packet
- Pilot Discovery Packet if workflow evaluation is requested

## Red flags

Pause before sending a package if the recipient expects Fork to:

- approve decisions
- deny decisions
- block workflows
- route workflows
- certify legal validity
- certify compliance satisfaction
- prove AI output correctness
- prove source completeness
- replace audit
- replace legal review
- replace governance
- replace security response
- reconstruct hidden vendor behavior
- recover evidence that was never captured

In those situations, clarify the boundary before sending materials.

## Disclosure discipline

A package should not be sent simply because it exists.

A package should be sent because it matches the recipient's stage.

The release ladder is not a sales funnel that forces every person forward.

It is a boundary-preserving disclosure system.

## Current package status

As of v0.1, the following packages are available:

- Public Doctrine Packet v0.1
- Executive Buyer Packet v0.1
- Technical Validation Packet v0.1
- Pilot Discovery Packet v0.1

The following packages are not yet available:

- Pilot-Ready Implementation Packet
- Client Evidence Boundary Packet Template

## Governing principle

Send the smallest package that truthfully answers the question.

Do not let the package imply more than the current evidence supports.

Fork preserves evidence boundaries.

The release process must do the same.