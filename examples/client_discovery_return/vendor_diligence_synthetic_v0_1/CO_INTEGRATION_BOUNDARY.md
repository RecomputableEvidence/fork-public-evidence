# Co-Integration Boundary

## Purpose

This file is used when Fork may be mapped beside another system, vendor, execution-governance layer, admissibility layer, workflow platform, GRC system, AI infrastructure provider, or partner technology.

## Is co-integration involved?

- [ ] YES
- [x] NO
- [ ] POSSIBLE
- [ ] UNKNOWN

If yes or possible, name the system or partner:

Not applicable for this synthetic example.

## Partner or adjacent system role

No external co-integration partner is included in this synthetic example. ExampleGRC and ExampleAIReview are client-side systems for mapping purposes.

## Boundary map

| Layer | Owner | Function | Fork receives? | Fork controls? | Notes |
|---|---|---|---|---|---|
| Client institution | ExampleCo | Vendor-risk workflow and institutional action | YES | NO | Owns approval, escalation, and response |
| Partner system | Not applicable | Not applicable | NO | NO | No co-integration partner in this example |
| Fork | Fork | Evidence preservation and verification within declared boundary | N/A | NO RUNTIME CONTROL | Fork remains read-only and out-of-band |

## What Fork may receive from adjacent system

- [ ] governed state export
- [ ] admissibility result
- [x] execution state
- [x] approval state
- [x] denial state
- [x] escalation state
- [x] policy snapshot
- [ ] authority marker
- [x] event log
- [x] artifact hash
- [x] external pointer
- [ ] none
- [ ] unknown
- [ ] other: Not used

## What Fork must not inherit

- [x] Fork does not inherit partner authority.
- [x] Fork does not inherit partner execution-control role.
- [x] Fork does not inherit partner legal conclusions.
- [x] Fork does not inherit partner compliance conclusions.
- [x] Fork does not inherit partner source-completeness claims.
- [x] Fork does not inherit partner correctness claims.
- [x] Fork does not become dependent on partner system for workflow continuity.
- [x] Fork remains read-only and out-of-band.

## Co-integration risks

None

## Co-integration suitability signal

- [ ] CO_INTEGRATION_POTENTIALLY_SUITABLE
- [ ] CO_INTEGRATION_REQUIRES_MORE_DISCOVERY
- [ ] CO_INTEGRATION_NOT_SUITABLE_AT_THIS_STAGE
- [x] UNKNOWN

Reason:

No co-integration partner is included in this synthetic example.