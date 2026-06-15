# Client Workflow Profile

## Purpose

This file identifies the candidate client workflow under consideration.

## Completion status

- Completed by: Synthetic Vendor Risk Lead
- Role: Vendor Risk Lead
- Organization: ExampleCo Synthetic Enterprise
- Date: 2026-06-14
- Confidentiality level of this completed packet: INTERNAL SYNTHETIC

## Workflow identification

- Workflow name: AI-assisted vendor diligence review
- Business function: Vendor risk management
- Workflow owner: Vendor Risk Lead
- Technical owner: GRC Platform Owner
- Executive sponsor, if any: Chief Risk Officer
- Current workflow stage: PLANNED PILOT
- Workflow type: VENDOR_FACING INTERNAL GOVERNANCE

## Consequence-bearing action

The workflow supports vendor-risk classification and escalation decisions before a vendor is approved for procurement review.

## Why later reconstruction matters

Later reconstruction matters because vendor approval, exception handling, and risk escalation may be reviewed by audit, compliance, security, legal, procurement, or executive governance if a vendor issue arises after onboarding.

## Workflow summary

1. Procurement submits a vendor diligence request.
2. The vendor completes a security and compliance questionnaire.
3. The GRC platform stores the questionnaire and supporting artifacts.
4. An AI-assisted review tool summarizes questionnaire responses and flags risk themes.
5. A human vendor-risk analyst reviews the AI output.
6. The analyst records approval, denial, or escalation.
7. Escalated vendors are reviewed by a vendor-risk committee.
8. The final disposition is recorded in the GRC platform.
9. Procurement receives the approved, denied, or escalated state.

## Initial pilot suitability signal

- [x] HIGH
- [ ] MEDIUM
- [ ] LOW
- [ ] UNKNOWN
- [ ] NOT_SUITABLE_AT_THIS_STAGE

Reason:

The workflow is consequential, has identifiable source systems, includes AI-assisted summarization/classification, includes human review, and produces approval or escalation states that may require later reconstruction.

## Known constraints

Sensitive vendor artifacts should not be copied in full during early discovery. Hash-only or external pointer handling may be required for some documents.

## Unknowns

None