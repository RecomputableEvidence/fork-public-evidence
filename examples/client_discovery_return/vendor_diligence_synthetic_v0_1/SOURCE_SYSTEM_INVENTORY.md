# Source System Inventory

## Purpose

This file identifies systems that may contain observable evidence for the candidate workflow.

## Source-system table

| System name | System type | Owner | Relevant evidence | Authoritative? | Export available? | Export format | Access model | Retention/mutation risk | Data sensitivity | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| ExampleGRC | GRC | GRC Platform Owner | Vendor questionnaire, review state, approval, escalation, final disposition | YES | YES | CSV and JSON report export | Manual export and file drop | MEDIUM | HIGH | Authoritative for vendor diligence workflow state |
| ExampleAIReview | AI Platform | AI Governance Lead | Prompt, AI summary, risk flags, model identifier, output timestamp | PARTIAL | YES | JSON export | Manual export | MEDIUM | MEDIUM | Retrieval context retained as document IDs only |
| ExampleDocs | Document Repository | Procurement Operations | Vendor attachments and supporting documents | YES | PARTIAL | External pointer and hash export | Hash-only reference | HIGH | RESTRICTED | Full documents remain in client repository |
| ExampleTickets | Ticketing | Procurement Operations | Procurement request and vendor intake ticket | PARTIAL | YES | CSV export | Manual export | LOW | MEDIUM | Downstream copy of request metadata |

## Required source-system questions

### Original request

- What system records the original request or initiating event?
- System: ExampleTickets
- Evidence available: Ticket ID, requester, vendor name, request date, intake category

### AI-assisted output

- What system records the AI-assisted output?
- System: ExampleAIReview
- Evidence available: AI summary, risk flags, model identifier, output timestamp, prompt template ID

### Human review

- What system records human review?
- System: ExampleGRC
- Evidence available: reviewer ID, review note, review timestamp, disposition

### Approval, denial, escalation, or modification

- What system records approval, denial, escalation, or modification?
- System: ExampleGRC
- Evidence available: disposition state, escalation reason, committee review marker

### Execution

- What system records execution?
- System: ExampleGRC and ExampleTickets
- Evidence available: final vendor-risk disposition and procurement handoff marker

### Policy or authority state

- What system records policy, authority, or control state?
- System: ExampleGRC
- Evidence available: vendor-risk policy version and review workflow configuration snapshot

### Audit, compliance, legal, risk, security, remediation, or reporting

- What systems record downstream review or response?
- Systems: ExampleGRC and ExampleTickets
- Evidence available: escalation state, committee review outcome, audit export marker

## Systems outside scope

Vendor production systems and vendor internal control evidence repositories are outside scope.

## Source-system unknowns

None