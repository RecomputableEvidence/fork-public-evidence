# Fork Inlet Routing and Onboarding Cadence v0.1

## Purpose

This document defines how public reviewers, enterprise contacts, workflow owners, technical counterparts, and co-integration partners route themselves from the public Fork repository into the appropriate input channel.

Fork routes by evidence-boundary input, not by buyer persona.

A visitor does not need to know whether they are the buyer. They need to identify what workflow information they can provide.

This document is a routing and boundary artifact. It is not a production-readiness claim, onboarding approval, implementation approval, commercial pilot approval, compliance conclusion, legal sufficiency claim, audit conclusion, security approval, risk acceptance, or procurement artifact.

## Routing principle

Do not choose a path by title.

Choose the inlet that matches the information available.

Fork is inclusive across enterprise functions because AI-assisted workflow evidence can involve legal, compliance, audit, risk, security, technical systems, source-system owners, AI governance leads, executive sponsors, and co-integration partners.

Fork does not route those parties into separate buyer channels.

Fork routes their input into the evidence-boundary mapping process.

## Inlet map

### I0 -- Public Review Inlet

Use when a reviewer wants to understand Fork, challenge its doctrine, inspect its public boundaries, or reproduce bounded verification commands.

Start with:

- `REVIEWER_QUICK_START_v0_1.md`
- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

This inlet does not imply enterprise discovery, client suitability, implementation readiness, or commercial pilot approval.

### I1 -- Candidate Workflow Inlet

Use when a contact can identify a real AI-assisted workflow where later reconstruction would matter.

Examples include vendor-risk review, audit evidence assembly, legal operations review, compliance review, security triage, model evaluation handoff, AI-assisted approval chains, or other institutional workflows where AI-assisted output enters action, review, escalation, or reliance.

Start with:

- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`

This inlet identifies a possible workflow. It does not establish workflow suitability.

### I2 -- Source-System / Export Inlet

Use when a contact can describe the systems, logs, records, exports, APIs, files, tickets, messages, approval systems, or data surfaces involved in a candidate workflow.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/SOURCE_SYSTEM_INVENTORY.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/ACCESS_AND_EXPORT_MODEL.md`

This inlet does not establish that Fork can access, capture, export, observe, or verify all listed systems.

### I3 -- Evidence-Artifact Inlet

Use when a contact can describe what should be preserved, hashed, referenced, sealed, excluded, redacted, or treated as unavailable.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/EVIDENCE_ARTIFACT_MAP.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CLAIMS_AND_NON_CLAIMS.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CLAIMS_AND_NON_CLAIMS_ACKNOWLEDGMENT.md`

This inlet does not establish source completeness, legal admissibility, compliance sufficiency, audit sufficiency, or decision correctness.

### I4 -- State-Transition Inlet

Use when a contact can identify where the workflow changes state.

Examples include request creation, AI output generation, human review, escalation, approval, rejection, override, exception handling, evidence attachment, downstream reliance, or external handoff.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/STATE_TRANSITION_MAP.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/AI_ASSISTED_SURFACE.md`

This inlet does not establish that Fork controls, blocks, approves, or modifies runtime workflow execution.

### I5 -- Security / Data-Handling Inlet

Use when a contact can describe confidentiality constraints, redaction needs, retention rules, air-gap requirements, access limitations, data residency issues, regulated data, or prohibited capture surfaces.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/SECURITY_AND_DATA_HANDLING_CONSTRAINTS.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/ACCESS_AND_EXPORT_MODEL.md`

This inlet does not establish security approval, risk acceptance, production access, or client data handling authorization.

### I6 -- Institutional Ownership Inlet

Use when a contact can identify workflow owners, decision owners, source-system owners, legal/compliance/audit/risk owners, security reviewers, executive sponsors, or approval authorities.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/INSTITUTIONAL_OWNERSHIP_MAP.md`

This inlet does not transfer institutional authority to Fork.

The institution owns the action.

Fork preserves the bounded evidence record.

### I7 -- Co-Integration Inlet

Use when a platform, GRC, audit, AI governance, evidence, workflow, or integration counterparty needs to map its own boundary to Fork's boundary.

Map into:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CO_INTEGRATION_BOUNDARY.md`
- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/CONFIGURATION_OUTPUT_TARGETS.md`

This inlet does not establish compatibility, endorsement, implementation readiness, shared authority, or proof-obligation transfer.

## Onboarding cadence

Fork public routing follows this sequence:

1. Public repo orientation.
2. Inlet identification.
3. Candidate workflow identification.
4. Client Discovery Return Packet completion.
5. Fork review of returned workflow/source-system facts.
6. Client Evidence Boundary Packet draft, if responsible.
7. Client review of the evidence boundary.
8. Sidecar bridge specification candidate, if the boundary is accepted.
9. Bounded workflow PoV scope, if commercially and operationally appropriate.
10. Preservation execution only within the accepted boundary.

No later step is implied by an earlier step.

## Mapping protocol

The mapping protocol is:

```text
Public Repo
  -> Inlet Router
  -> Client Discovery Return Packet
  -> Fork Mapping Review
  -> Client Evidence Boundary Packet
  -> Sidecar Bridge Specification Candidate
  -> Bounded Workflow PoV / Not Suitable / Blocked

The Client Discovery Return Packet is the inbound mapping record.
The Client Evidence Boundary Packet is the Fork-authored boundary draft.
The sidecar bridge is downstream of the accepted evidence boundary.
The bounded workflow PoV is a commercial and operational wrapper around one accepted bounded workflow.
Required separation
Fork must not collapse these stages:
Public review is not client discovery.
Client discovery is not onboarding.
Onboarding is not deployment.
Discovery return is not sidecar approval.
Client evidence boundary is not production integration.
Sidecar bridge specification is not workflow authority.
Bounded preservation is not legal, compliance, audit, security, risk, or decision approval.
Non-claim boundary
This routing does not establish:
production readiness
customer deployment
procurement approval
legal sufficiency
legal admissibility
compliance satisfaction
audit sufficiency
security approval
risk acceptance
workflow suitability
commercial pilot approval
source completeness
AI-output correctness
decision correctness
runtime control
response authority
remediation ownership
institutional authority
co-integration compatibility
proof-obligation transfer
Canonical sentence
Fork does not route by title.
Fork routes by evidence-boundary input.
Process sentence
The public repo orients the reviewer; the inlet router identifies the input channel; the Client Discovery Return Packet captures the client-side facts; the Client Evidence Boundary Packet converts those facts into a bounded preservation surface; the sidecar bridge follows only after the boundary is accepted.