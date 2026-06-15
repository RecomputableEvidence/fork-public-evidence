# State Transition Map

## Purpose

This file identifies workflow states that must remain separate.

## State table

| State | Exists in workflow? | Recorded where? | Evidence available? | Notes |
|---|---|---|---|---|
| Requested | YES | ExampleTickets | YES | Vendor diligence request created |
| AI generated | YES | ExampleAIReview | YES | AI summary and risk flags created |
| Human reviewed | YES | ExampleGRC | YES | Vendor-risk analyst review |
| Modified | YES | ExampleGRC | PARTIAL | Analyst may modify risk classification |
| Approved | YES | ExampleGRC | YES | Vendor approved for procurement continuation |
| Denied | YES | ExampleGRC | YES | Vendor denied or rejected |
| Escalated | YES | ExampleGRC | YES | Vendor-risk committee escalation |
| Executed | YES | ExampleTickets | PARTIAL | Procurement handoff marker |
| Remediated | YES | ExampleGRC | PARTIAL | Conditional remediation tasks |
| Reported | YES | ExampleGRC | PARTIAL | Committee summary export |

## Collapsed states

Procurement handoff and final execution are partially collapsed in ExampleTickets. Review and approval are separated in ExampleGRC.

## Required Fork evidence states

- [x] PASS
- [x] FAIL
- [x] NOT_CHECKED
- [x] PARTIAL
- [x] STALE_CONTEXT
- [x] OUT_OF_SCOPE
- [x] SOURCE_UNAVAILABLE
- [ ] UNKNOWN

## State-transition risks

Approved and executed may be interpreted incorrectly if procurement handoff is treated as final vendor onboarding. Fork should preserve the distinction.