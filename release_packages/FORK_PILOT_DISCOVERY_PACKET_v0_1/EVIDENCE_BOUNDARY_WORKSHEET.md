# Evidence Boundary Worksheet

## Purpose

This worksheet defines what Fork may preserve for a candidate pilot workflow.

The worksheet separates captured evidence from references, unavailable sources, and explicit non-claims.

## Workflow identification

- Workflow name:
- Business owner:
- Technical owner:
- Legal/compliance/audit/risk owner:
- AI-assisted function:
- Consequence-bearing action:
- Review timeframe:

## Evidence categories

### 1. Captured evidence

Artifacts or events that can be copied into the evidence packet or preserved directly.

Examples:

- Prompt or request text
- Output text
- Review note
- Approval record
- Denial record
- Escalation record
- Policy snapshot
- Workflow event export
- Ticket export
- System-generated report

### 2. Hashed reference

Artifacts that may not be copied, but can be hashed and referenced.

Examples:

- Large document set
- Retrieval corpus export
- Policy bundle
- Vendor report
- Evidence bundle held in another system

### 3. External pointer

Artifacts that are referenced by location or identifier, but not copied or hashed in full.

Examples:

- Ticket URL
- Case ID
- Vendor invocation ID
- Model call ID
- Document repository path
- External audit reference

### 4. Source unavailable

Artifacts or sources that would be relevant but are unavailable.

Examples:

- Hidden vendor routing logic
- Unexported model telemetry
- Deleted source document
- Unavailable retrieval item
- Missing approval history
- Non-retained prompt context

### 5. Explicit non-claim

Matters that Fork must not imply from the preserved record.

Examples:

- Source completeness
- Legal admissibility
- Decision correctness
- AI output correctness
- Compliance satisfaction
- Authority validity
- Remediation sufficiency
- Reporting sufficiency
- Full replayability of AI behavior

## Evidence-state mapping

For each candidate evidence item, assign one category:

- CAPTURED
- HASHED_REFERENCE
- EXTERNAL_POINTER
- SOURCE_UNAVAILABLE
- EXPLICIT_NON_CLAIM

## Boundary rule

Fork should not infer reliance, authority, correctness, completeness, or legal sufficiency unless those facts are explicitly observable and captured within the declared evidence boundary.