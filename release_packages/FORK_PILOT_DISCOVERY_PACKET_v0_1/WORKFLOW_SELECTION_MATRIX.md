# Workflow Selection Matrix

## Purpose

This matrix helps evaluate whether a candidate workflow is appropriate for Fork pilot discovery.

## Scoring guidance

Use qualitative ratings:

- HIGH
- MEDIUM
- LOW
- UNKNOWN
- OUT_OF_SCOPE

## Candidate workflow fields

| Field | Notes |
|---|---|
| Workflow name | Name of the workflow under consideration |
| Business owner | Internal owner of the workflow |
| Consequence level | Legal, financial, operational, security, employment, healthcare, procurement, or public-accountability relevance |
| AI involvement | Generation, classification, summarization, routing, recommendation, review support, or other |
| Human review | Whether human review, approval, denial, or escalation exists |
| Source systems | Systems that may emit relevant observable events |
| Existing exports | Whether event exports, logs, reports, tickets, records, or approvals are available |
| Evidence need | Why later reconstruction matters |
| Boundary clarity | Whether captured / referenced / unavailable / non-claim categories can be stated |
| Security sensitivity | Whether data sensitivity requires special handling |
| Pilot suitability | HIGH / MEDIUM / LOW / UNKNOWN / OUT_OF_SCOPE |

## Suitability indicators

A candidate workflow is stronger when:

- The workflow is consequential.
- The AI-assisted surface is identifiable.
- The human review path is identifiable.
- Source-system artifacts are available.
- The evidence boundary can be bounded.
- Later reconstruction is a real institutional need.

A candidate workflow is weaker when:

- Source systems are unknown.
- AI involvement is vague.
- No artifacts can be exported or observed.
- The client expects Fork to block, approve, or enforce.
- The workflow requires hidden vendor reconstruction.
- The scope cannot be narrowed.