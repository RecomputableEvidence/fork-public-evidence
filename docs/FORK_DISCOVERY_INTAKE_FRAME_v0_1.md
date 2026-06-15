# Fork Discovery Intake Frame v0.1

## Purpose

This document provides an internal discovery intake frame for Fork.

It is used to guide early qualified conversations before any client-specific sidecar bridge, pilot-ready implementation package, or client evidence boundary is drafted.

This is not a sales form.

This is not an onboarding form.

This is not a deployment checklist.

This is a structured conversation guide for determining whether a real client workflow can be mapped into bounded, read-only, recomputable evidence preservation.

## Governing posture

Fork is ready for qualified pilot discovery.

Fork is not presented as generic production onboarding.

The evidentiary architecture is defined.

The release ladder is public.

The client-specific bridge is discovered, not assumed.

The final sidecar path depends on the client's actual workflow, source systems, access model, evidence surfaces, security constraints, and institutional responsibilities.

## Core discovery rule

Do not design the bridge before mapping the environment.

Do not imply that Fork can observe systems that have not been identified.

Do not imply that Fork can capture evidence that the client cannot export, expose, attest, hash, reference, or preserve.

Do not collapse discovery into deployment.

Discovery determines whether a bounded pilot can be responsibly scoped.

## What discovery is

Discovery is the process of determining:

- what workflow is being considered
- why the workflow matters
- where AI assistance enters
- what source systems generate evidence
- what events or artifacts are observable
- what can be captured directly
- what can be hashed or referenced
- what is unavailable
- what must be stated as a non-claim
- who owns legal, compliance, audit, risk, security, remediation, and reporting responses
- what next build is actually required

## What discovery is not

Discovery is not:

- production onboarding
- runtime integration
- legal review
- audit performance
- compliance certification
- security approval
- vendor-risk approval
- deployment authorization
- sidecar installation
- source completeness certification
- AI output correctness validation
- decision correctness validation

## Classification event model

Each inbound conversation should be treated as a classification event.

The goal is not to answer everything.

The goal is to classify the recipient's need and route the conversation into the correct package, question set, or boundary.

## Classification table

| Signal | Likely classification | Route |
|---|---|---|
| "What is Fork?" | Public orientation | Public Doctrine Packet |
| "Why does this matter?" | Executive buyer orientation | Executive Buyer Packet |
| "Where would this sit?" | Institutional fit | Executive Buyer Packet |
| "Is this technically real?" | Technical diligence | Technical Validation Packet |
| "What can I inspect?" | Technical diligence | Technical Validation Packet |
| "How would we evaluate a pilot?" | Pilot discovery | Pilot Discovery Packet |
| "What would you need from us?" | Pilot discovery | Discovery Intake Frame |
| "Can you show me a demo?" | Boundary test | Clarify scope before demo claim |
| "Can this stop bad decisions?" | Control-plane confusion | Reassert evidence boundary |
| "Can this prove the AI was right?" | Correctness confusion | Reassert non-claim |
| "Can this satisfy compliance?" | Compliance overread | Reassert support vs satisfaction |
| "Can this connect to our system?" | Client-specific bridge question | Discovery before implementation |

## First response principle

The first response should reduce scope.

It should not expand claims.

Recommended pattern:

"Fork has a defined evidence architecture and release boundary. The client-specific bridge depends on the workflow, source systems, access model, evidence surfaces, and institutional review requirements. Discovery is how those are mapped before any pilot-ready implementation is scoped."

## Intake sequence

Use this sequence during a serious discovery conversation.

Do not ask every question at once.

Use the sequence to keep the conversation bounded.

### 1. Workflow identification

Purpose:

Identify the specific workflow under consideration.

Questions:

- What workflow are we discussing?
- What business function owns it?
- Why is this workflow consequential?
- What decision, recommendation, approval, denial, escalation, or review does it affect?
- Is this workflow already in use, planned, experimental, or under review?
- Is the workflow internal, customer-facing, vendor-facing, regulated, or operational?

Output:

- named workflow
- business owner
- consequence-bearing action
- seriousness level
- initial pilot suitability signal

### 2. AI-assisted surface

Purpose:

Identify where AI assistance enters the workflow.

Questions:

- Where does AI participate?
- Does AI generate, summarize, classify, route, recommend, rank, draft, review, or assist?
- Is the AI system internal, vendor-provided, embedded, or ad hoc?
- Does the AI output directly affect the next workflow step?
- Does a human review the output before action?
- Are prompts, outputs, retrieval context, model identifiers, or vendor invocation identifiers retained?

Output:

- AI-assisted function
- model or vendor surface if known
- retained AI artifacts
- unavailable AI artifacts
- human review dependency

### 3. Source-system map

Purpose:

Identify systems that may emit observable evidence.

Questions:

- What system records the original request?
- What system records the AI-assisted output?
- What system records human review?
- What system records approval, denial, escalation, or modification?
- What system records execution?
- What system records policy, authority, or control state?
- What system records exceptions or remediation?
- What system records audit, compliance, legal, risk, or security review?
- Which systems are authoritative?
- Which systems are merely downstream copies or summaries?

Output:

- source-system list
- system owners
- system authority distinctions
- event or artifact candidates
- source-system uncertainty

### 4. Access and export model

Purpose:

Determine what can be observed without turning Fork into a runtime dependency.

Questions:

- Can the relevant system export data?
- What export formats are available?
- Can exports be delivered manually?
- Can exports be delivered by file drop?
- Is API pull possible later?
- Is read-only access acceptable?
- Are service accounts allowed?
- Are production credentials prohibited?
- Are there existing audit exports, workflow reports, GRC exports, ticket exports, or logs?
- How often do relevant records change?
- Are records overwritten, deleted, expired, or mutable?

Output:

- export format
- access model
- read-only feasibility
- retention risk
- data mutation risk
- sidecar bridge implications

### 5. Evidence artifact map

Purpose:

Classify evidence into direct capture, hash/reference, external pointer, unavailable source, or explicit non-claim.

Questions:

- Which artifacts can be copied into an evidence packet?
- Which artifacts can be hashed but not stored?
- Which artifacts can only be referenced externally?
- Which artifacts are unavailable?
- Which artifacts are sensitive, privileged, regulated, confidential, or restricted?
- Which artifacts are too large to copy?
- Which artifacts are controlled by a vendor?
- Which artifacts are mutable or time-sensitive?
- Which artifacts cannot be relied on for source completeness?

Output:

- captured evidence list
- hashed reference list
- external pointer list
- source unavailable list
- explicit non-claim list

### 6. State-transition map

Purpose:

Separate workflow states that should not be collapsed.

Questions:

- Where does proposed become reviewed?
- Where does reviewed become approved?
- Where does approved become executed?
- Where does denied become final?
- Where does escalation occur?
- Where does remediation occur?
- Where does reporting occur?
- Are approval and execution recorded separately?
- Are AI recommendation and human decision recorded separately?
- Are policy state and decision state recorded separately?

Output:

- state-transition map
- collapsed states
- missing transitions
- reviewer-facing evidence states
- boundary risks

### 7. Institutional ownership map

Purpose:

Keep Fork from becoming the actor.

Questions:

- Who owns legal review?
- Who owns compliance review?
- Who owns audit review?
- Who owns risk acceptance?
- Who owns security review?
- Who owns remediation?
- Who owns reporting?
- Who owns workflow control?
- Who owns source-system administration?
- Who owns vendor-risk review?
- Who owns incident response if evidence shows something went wrong?

Output:

- institutional owner map
- upstream authority owners
- downstream review owners
- response owner for gaps or failures
- escalation path

### 8. Security and data-handling constraints

Purpose:

Determine whether discovery can proceed without overbroad access or unsafe handling.

Questions:

- What data classifications are involved?
- Does the workflow include privileged, confidential, personal, regulated, health, financial, employment, security, procurement, or customer data?
- Which artifacts may not leave the client environment?
- Which artifacts require redaction?
- Which artifacts may be hashed only?
- Which artifacts may be referenced only?
- What retention limits apply?
- What security review is required before any pilot?
- What vendor-risk review is required?
- What access restrictions apply?

Output:

- data classification
- storage constraints
- redaction constraints
- hashing-only constraints
- external-pointer constraints
- security review requirements

### 9. Boundary and non-claim map

Purpose:

Prevent discovery from becoming an implicit claim of completeness, authority, correctness, legal sufficiency, or compliance satisfaction.

Questions:

- What must Fork not claim?
- What evidence cannot be observed?
- What source systems are outside scope?
- What vendor behavior cannot be reconstructed?
- What AI behavior cannot be replayed?
- What legal conclusions remain outside Fork?
- What compliance obligations remain outside Fork?
- What audit conclusions remain outside Fork?
- What source completeness limitations exist?
- What correctness claims must be excluded?

Output:

- explicit non-claims
- scope exclusions
- source completeness limitations
- correctness limitations
- legal/compliance/audit limitations

### 10. Next-build implication

Purpose:

Translate discovery into responsible next engineering work.

Questions:

- What specific bridge would be required?
- Would the first bridge be file-drop, manual export, watch-folder, API pull, or another read-only pattern?
- What format normalization is required?
- What evidence states must be supported?
- What schemas would need to be extended?
- What verifier output would the client need?
- What reviewer report would be useful?
- What cannot be built until the client provides more information?
- What must remain out of scope?

Output:

- candidate sidecar bridge pattern
- required normalizers
- evidence packet requirements
- verifier/report requirements
- implementation blockers
- pilot-ready implementation prerequisites

## Intake summary format

Use this format after a serious discovery conversation.

### Discovery summary

- Date:
- Prospect / organization:
- Contact:
- Role:
- Workflow discussed:
- Current classification:
- Recommended package route:
- Recommended next step:

### Workflow

- Workflow name:
- Business function:
- Consequence-bearing action:
- Current stage:
- Pilot suitability signal:

### AI-assisted surface

- AI function:
- AI system or vendor:
- Human review point:
- Retained AI artifacts:
- Unavailable AI artifacts:

### Source systems

- Source systems identified:
- System owners:
- Export formats:
- Access model:
- Retention or mutation risks:

### Evidence boundary

- Captured evidence:
- Hashed references:
- External pointers:
- Source unavailable:
- Explicit non-claims:

### Institutional ownership

- Legal owner:
- Compliance owner:
- Audit owner:
- Risk owner:
- Security owner:
- Remediation owner:
- Reporting owner:
- Workflow-control owner:

### Security and data handling

- Data sensitivity:
- Redaction requirements:
- Hash-only constraints:
- External-pointer constraints:
- Security review required:
- Vendor-risk review required:

### Next-build implications

- Candidate bridge pattern:
- Required normalizers:
- Required schemas:
- Required verifier/report output:
- Blockers:
- Recommended next artifact:

## Recommended next artifact decision

Use this decision table after intake.

| Discovery result | Next artifact |
|---|---|
| Recipient only needs orientation | Public Doctrine Packet |
| Executive sponsor needs fit framing | Executive Buyer Packet |
| Technical reviewer needs inspectable mechanics | Technical Validation Packet |
| Workflow suitability is being evaluated | Pilot Discovery Packet |
| Workflow is identified but not scoped | Continue discovery intake |
| Workflow is scoped and source systems are known | Pilot-Ready Implementation Packet when available |
| Client-specific evidence boundary can be drafted | Client Evidence Boundary Packet when available |
| Source systems are unknown | Source System Inventory |
| Data-handling constraints dominate | Security and Data-Handling Questions |
| Non-claims are not accepted | Pause or decline pilot path |
| Recipient expects Fork to control action | Reassert boundary before proceeding |

## Red flags during intake

Pause the conversation if the prospect expects Fork to:

- stop bad decisions
- approve decisions
- deny decisions
- route live workflows
- replace GRC
- replace audit
- replace legal review
- replace compliance review
- replace risk ownership
- replace security response
- certify legal admissibility
- certify compliance satisfaction
- prove AI output correctness
- prove decision correctness
- prove source completeness
- reconstruct hidden vendor behavior
- recover evidence that was never observed, exported, attested, captured, hashed, or referenced

If a red flag appears, clarify the boundary before continuing.

## Boundary-preserving replies

### When asked for a demo

"Fork is not presented as a generic plug-and-play connector. The evidence architecture is defined, but the client-specific bridge depends on the workflow, source systems, access model, and evidence boundary. The right next step is to map the candidate workflow before implying a deployment pattern."

### When asked if Fork can connect to their systems

"Potentially, but that cannot be responsibly answered in the abstract. We first need to identify which systems generate the evidence, what export or read-only access model exists, what data constraints apply, and what Fork must not claim."

### When asked what Fork would need from them

"The first discovery layer is workflow, source systems, AI-assisted surface, human review point, approval or state transition, audit or compliance requirement, security constraints, and the owner of any response if evidence shows a gap."

### When asked if Fork is production-ready

"Fork is ready for qualified pilot discovery. It is not represented as generic production onboarding. The public architecture and release ladder are defined; the client-specific sidecar bridge is scoped through discovery."

### When asked if Fork can prove correctness

"Fork does not prove AI output correctness or decision correctness. It preserves a bounded record of what was observable, captured, referenced, unavailable, and not claimed."

### When asked if Fork handles compliance

"Fork does not satisfy compliance obligations by itself. It preserves evidence that compliance, audit, legal, risk, or governance teams may later need to inspect."

## Maturity posture

The mature posture is not to claim universal readiness.

The mature posture is to show that readiness is bounded by the client's actual environment.

Fork is ahead when it refuses to assume:

- source completeness
- access availability
- evidence sufficiency
- legal admissibility
- compliance satisfaction
- decision correctness
- runtime control authority

## Governing principle

The bridge is discovered, not assumed.

Discovery maps the environment.

The evidence boundary defines the pilot.

The sidecar bridge follows the boundary.

Fork preserves the record.

The institution owns the action.