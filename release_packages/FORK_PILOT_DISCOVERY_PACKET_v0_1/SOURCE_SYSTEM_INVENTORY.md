# Source System Inventory

## Purpose

This document identifies systems that may contain observable workflow evidence for a candidate Fork pilot.

## Source system fields

| Field | Notes |
|---|---|
| System name | Name of source system |
| System owner | Business or technical owner |
| System type | Workflow, GRC, legal ops, ticketing, AI platform, document repository, approval system, audit system, security system, other |
| Relevant events | Events or artifacts potentially useful for reconstruction |
| Export available | YES / NO / UNKNOWN |
| Export format | JSON, JSONL, CSV, PDF, API, report, manual export, other |
| Access model | Read-only, export-only, API pull, file drop, manual delivery, unknown |
| Contains sensitive data | YES / NO / UNKNOWN |
| Retention risk | Whether the system mutates, deletes, overwrites, or expires relevant evidence |
| Boundary category | Captured, hashed reference, external pointer, source unavailable, explicit non-claim |

## Source-system questions

1. What system records the initial request?
2. What system records the AI-assisted output?
3. What system records human review?
4. What system records approval, denial, escalation, or modification?
5. What system records execution?
6. What system records policy or authority state?
7. What system records exceptions?
8. What system records remediation or reporting actions, if any?
9. What source material changes over time?
10. What source material cannot be exported or retained?

## Boundary rule

A system should not be treated as observed merely because it exists.

Fork can only preserve what is exported, observed, captured, referenced, or explicitly declared unavailable within the pilot boundary.