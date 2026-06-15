# Sidecar Bridge Spec Placeholder v0.1

## Purpose

This document is a placeholder for the client-specific Fork sidecar bridge specification.

It exists to prevent an unsafe assumption:

The sidecar bridge is not generic.

The sidecar bridge is discovered, specified, and constrained from the client's actual workflow, source systems, access model, evidence artifacts, state transitions, security constraints, and institutional ownership.

This document must not be treated as a deployment specification.

It is a controlled placeholder that identifies what must be known before a client-native sidecar bridge can be responsibly designed.

## Status

Status: PLACEHOLDER

This document does not claim:

- deployment readiness
- client onboarding readiness
- production integration
- access to client systems
- source completeness
- evidence sufficiency
- legal admissibility
- compliance satisfaction
- AI output correctness
- decision correctness
- runtime enforcement
- workflow control

This document exists to preserve the boundary between:

1. Fork's public evidence architecture
2. qualified pilot discovery
3. client-specific implementation design

## Governing principle

The bridge is discovered, not assumed.

Fork may define the evidentiary architecture before a client exists.

Fork may define the discovery frame before a client exists.

Fork may define the release package ladder before a client exists.

Fork should not define the final sidecar bridge in the abstract.

The sidecar bridge must follow the client evidence boundary.

## What this placeholder protects against

This placeholder prevents the following overclaims:

- "Fork can connect to any enterprise system."
- "Fork is plug-and-play for all workflows."
- "Fork can capture all relevant evidence."
- "Fork can reconstruct hidden vendor behavior."
- "Fork can replay AI behavior completely."
- "Fork can certify compliance."
- "Fork can prove the decision was correct."
- "Fork can become the execution control plane."
- "Fork can responsibly deploy before the workflow is mapped."

Fork should not make those claims.

## Required inputs before bridge design

A client-specific sidecar bridge specification requires the following inputs.

### 1. Client workflow profile

Required:

- workflow name
- workflow owner
- business function
- consequence-bearing action
- current workflow stage
- AI-assisted surface
- human review point
- approval or denial path
- execution path
- escalation path
- remediation path, if any
- reporting path, if any

Output needed:

- client workflow profile
- seriousness level
- pilot suitability signal

### 2. Source system map

Required:

- systems that record the original request
- systems that record AI-assisted output
- systems that record human review
- systems that record approval, denial, escalation, modification, or execution
- systems that record policy or authority state
- systems that record audit, legal, compliance, risk, security, remediation, or reporting activity
- source-system owners
- authoritative system distinctions
- downstream copy or summary distinctions

Output needed:

- source system map
- system owner map
- authority distinction table
- source uncertainty list

### 3. Access and export model

Required:

- export availability
- export format
- export cadence
- file-drop availability
- API pull availability
- manual export availability
- read-only access constraints
- service account constraints
- credential restrictions
- retention limits
- mutation or overwrite behavior
- deletion or expiration behavior

Output needed:

- access model
- export model
- retention and mutation risk map
- bridge feasibility signal

### 4. Evidence artifact map

Required:

- artifacts that can be captured directly
- artifacts that can be hashed but not stored
- artifacts that can only be externally referenced
- artifacts that are unavailable
- artifacts that are sensitive, restricted, privileged, confidential, regulated, or vendor-controlled
- artifacts that are too large to store
- artifacts that are mutable or time-sensitive
- artifacts that cannot support source-completeness claims

Output needed:

- captured evidence list
- hashed reference list
- external pointer list
- source unavailable list
- explicit non-claim list

### 5. State transition map

Required:

- proposed state
- generated state
- reviewed state
- approved state
- denied state
- escalated state
- modified state
- executed state
- remediated state
- reported state
- verified state
- failed state
- not checked state
- partial state
- stale context state
- out of scope state
- source unavailable state

Output needed:

- workflow state transition map
- collapsed-state risks
- missing-state risks
- evidence-state requirements

### 6. Security and data-handling boundary

Required:

- data classifications
- privileged data constraints
- regulated data constraints
- personal data constraints
- financial data constraints
- health data constraints
- employment data constraints
- customer data constraints
- security-sensitive data constraints
- redaction requirements
- hash-only requirements
- external-pointer requirements
- retention requirements
- destruction requirements
- vendor-risk review requirements
- security review requirements

Output needed:

- security and data-handling boundary
- redaction model
- hash-only model
- external-pointer model
- retention model

### 7. Institutional ownership map

Required:

- legal owner
- compliance owner
- audit owner
- risk owner
- security owner
- workflow owner
- source-system owner
- vendor-risk owner
- remediation owner
- reporting owner
- incident-response owner
- executive sponsor

Output needed:

- institutional ownership map
- response owner map
- escalation map

### 8. Claims and non-claims

Required:

- what Fork may claim
- what Fork must not claim
- what evidence cannot be observed
- what source systems are outside scope
- what vendor behavior cannot be reconstructed
- what AI behavior cannot be replayed
- what legal conclusions remain outside Fork
- what compliance obligations remain outside Fork
- what audit conclusions remain outside Fork
- what source completeness limitations exist
- what correctness claims must be excluded

Output needed:

- client-specific claims
- client-specific non-claims
- source completeness limitations
- correctness limitations
- legal, compliance, audit, and risk limitations

## Candidate bridge patterns

The actual sidecar bridge pattern must be selected only after discovery.

Possible bridge patterns include:

### 1. Manual export bridge

Description:

Client provides manually exported workflow records, reports, files, logs, or evidence bundles.

Use when:

- no API access is available
- security constraints prohibit service accounts
- early pilot discovery requires low operational burden
- the workflow can be evaluated from bounded exports

Non-claim:

Manual export does not prove source completeness.

### 2. File-drop bridge

Description:

Client places approved exports into a controlled folder or transfer location for read-only Fork observation.

Use when:

- exports can be generated periodically
- file-drop access is acceptable
- watch-folder evidence preservation is sufficient for pilot scope

Non-claim:

File-drop observation does not prove that unexported source events do not exist.

### 3. Watch-folder bridge

Description:

Fork observes an agreed folder for new or changed artifacts without modifying the client workflow.

Use when:

- the client can produce stable artifact drops
- file-level observation is sufficient
- read-only sidecar posture can be preserved

Non-claim:

Watch-folder observation does not certify the source system that produced the files.

### 4. API pull bridge

Description:

Fork performs read-only pulls from approved client or vendor APIs under constrained scope.

Use when:

- API access is approved
- credentials and service accounts are permitted
- source-system fields are mapped
- rate limits, retention, and access boundaries are known

Non-claim:

API access does not by itself prove completeness, correctness, or legal sufficiency.

### 5. Hybrid reference bridge

Description:

Fork captures some artifacts directly, hashes some artifacts, and records pointers to other artifacts that remain in client systems.

Use when:

- data sensitivity prevents full copying
- large artifacts cannot be stored
- privileged or regulated material must remain in place
- external systems remain the system of record

Non-claim:

References and hashes preserve integrity posture only within the declared evidence boundary.

## Bridge selection table

| Discovery condition | Likely bridge pattern |
|---|---|
| Client can only provide exports | Manual export bridge |
| Client can generate periodic files | File-drop bridge |
| Client can support monitored artifact drops | Watch-folder bridge |
| Client approves constrained API access | API pull bridge |
| Sensitive data cannot leave client systems | Hybrid reference bridge |
| Source systems are unknown | No bridge selected |
| Evidence boundary is unclear | No bridge selected |
| Security review is incomplete | No bridge selected |
| Non-claims are not accepted | No bridge selected |

## Minimum viable bridge specification

A client-native sidecar bridge cannot be specified until the following fields are complete:

- candidate workflow
- source systems
- evidence artifacts
- access/export model
- data-handling constraints
- state transitions
- institutional ownership
- claims and non-claims
- acceptance criteria
- implementation blockers

If any of these are unknown, the bridge remains provisional.

## Implementation blockers

The following conditions block responsible bridge specification:

- no named workflow
- no workflow owner
- unknown source systems
- unknown export model
- unknown data sensitivity
- unavailable security reviewer
- unavailable institutional owner
- unresolved legal or compliance constraints
- expectation that Fork will control live workflow action
- expectation that Fork will prove AI correctness
- expectation that Fork will prove decision correctness
- expectation that Fork will certify compliance
- refusal to accept explicit non-claims

## Acceptance criteria placeholder

Client-specific acceptance criteria must define:

- what evidence is expected to be captured
- what evidence is expected to be hashed
- what evidence is expected to be referenced
- what evidence is known to be unavailable
- what verification output is expected
- what reviewer report is expected
- what constitutes PASS
- what constitutes FAIL
- what constitutes NOT_CHECKED
- what constitutes PARTIAL
- what constitutes STALE_CONTEXT
- what constitutes OUT_OF_SCOPE
- what constitutes SOURCE_UNAVAILABLE
- what Fork must not claim
- who owns response if verification fails or evidence is missing

## Required client-specific outputs

Before pilot-ready implementation, the following outputs should exist:

- client workflow profile
- source system map
- evidence artifact map
- state transition map
- access and export model
- security and data-handling boundary
- institutional ownership map
- claims and non-claims
- acceptance criteria
- implementation blockers
- selected bridge pattern
- pilot-ready implementation scope

## Boundary-preserving deployment statement

A future client-specific bridge specification may state:

"Fork will observe only the source systems, export paths, files, APIs, references, artifacts, and evidence states declared in this client evidence boundary. Fork does not claim source completeness, decision correctness, AI output correctness, legal admissibility, compliance satisfaction, or authority to control workflow execution."

## Non-deployment statement

Until the required client-specific fields are completed, the correct statement is:

"Fork is ready for qualified pilot discovery. The sidecar bridge has not been finalized because the client workflow, source systems, access model, evidence artifacts, state transitions, security constraints, and institutional ownership have not yet been mapped."

## Governing close

The evidence architecture can be public.

The bridge cannot be assumed.

The bridge follows the boundary.

The boundary follows discovery.

Fork preserves the record.

The institution owns the action.