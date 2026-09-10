# Fork Repository Purpose Routing v0.1

**Standing:** `CANDIDATE_REPOSITORY_ROUTING_RECORD`  
**Date:** 2026-09-09

Fork is intentionally a multi-purpose evidence repository. A route answers **where to begin for a purpose**. It does not change the standing of any artifact reached through that route.

## Purpose routes

| Reviewer purpose | Start here | Typical material | Boundary |
|---|---|---|---|
| **Current program standing** | [`README.md`](README.md) in this directory | Current work register, freeze/independence state, pending admission, next gates | Current-state representation is not canonical evidence for underlying `PENDING_BYTE_ADMISSION` packages |
| **Research hypotheses and methods** | [`../research/`](../research/) plus the current work register | Position papers, research frameworks, candidate/frozen methods, empirical questions | Method existence != method validation; hypothesis != result |
| **Current bounded proof surface** | [`../CURRENT_PROOF_SURFACE_v0_1.md`](../CURRENT_PROOF_SURFACE_v0_1.md) | Public verifier path, structural checks, bounded scenarios | Structural pass != truth, compliance, authority, production readiness, or general theory |
| **Human / independent recomputation** | [`../recomputation/`](../recomputation/) | Boundary-state interoperability sandboxes, receipts, reconstruction instructions | Successful recomputation establishes only the declared recomputation property |
| **Failure modes and adversarial evidence** | [`../reconstruction/adversarial/`](../reconstruction/adversarial/) and simulation surfaces | Reproducible limitations, negative fixtures, coordinated reseal, lexical/scope failures | Reproduced limitation != universal exploitability or harm |
| **Interoperability and modular architecture** | [`../modular-surface/FORK_MODULAR_SURFACE_v0_1.md`](../modular-surface/FORK_MODULAR_SURFACE_v0_1.md) | Evidence Boundary, Transition, Reliance, Interoperability, Simulation, Commercial surfaces | Shared interface != shared authority or semantic equivalence |
| **Longitudinal evidence** | [`../reconstruction/longitudinal/`](../reconstruction/longitudinal/) and current work register | Replay receipts, temporal reconstruction, successor/predecessor records, retrieval corpus status | Historical persistence != present standing; corpus presence != completeness |
| **Exterior review / field observations** | [`../exterior-observations/`](../exterior-observations/) and [`../review/`](../review/) | Public review rounds, observer comments, challenge records, response records | Observation, praise, criticism, acknowledgement, or participation != validation or endorsement |
| **Pilot / buyer / procurement discovery** | [`../commercial/`](../commercial/) | Buyer overview, FAQ, design-partner material, reviewer packet example, when Fork is not needed | Buyer-facing material != certification, assurance, legal advice, procurement approval, or unrestricted production qualification |
| **NGAST consultation / applied assessment** | Current work register, then applicable commercial material | Candidate assessment/triage service boundary and method-selection context | Fork Evidence Research Program != NGAST consulting practice; each applied method requires its own qualification |
| **Repository examination of external systems** | Current work register until protocol bytes are admitted | Remora, Kin, admission, Continuance and disposition records | Observed seam != bug; analogy != equivalence; reproduction != intervention authority |

## One artifact, multiple routes

A single artifact may legitimately appear in several routes. For example, an adversarial replay fixture may be relevant to research, failure-mode analysis, proof-surface review, interoperability, and procurement diligence.

That means only:

```text
ARTIFACT_RELEVANT_TO(PURPOSE_A)
AND
ARTIFACT_RELEVANT_TO(PURPOSE_B)
```

It does not mean:

```text
PURPOSE_A_VALIDATES_PURPOSE_B
```

or:

```text
MULTIPLE_ROUTES = MULTIPLE_INDEPENDENT_CONFIRMATIONS
```

## Research and commercial separation

The repository may expose commercial or procurement-facing material because external reviewers need to understand intended application surfaces. This does not convert research standing into commercial qualification.

```text
RESEARCH_RESULT
!= CLIENT_FINDING
!= PROFESSIONAL_OPINION
!= ASSURANCE
!= CERTIFICATION
```

NGAST may later apply a specifically qualified method under an engagement boundary. Such application must be recorded separately from the Fork research lineage.

## Failure-mode route

Failure records are first-class repository objects. They should remain discoverable even after repair.

```text
FAILURE_FOUND
-> FAILURE_PRESERVED
-> REPAIR_CANDIDATE
-> SUCCESSOR_EXECUTION
```

not:

```text
FAILURE_FOUND
-> REPAIR
-> DELETE_FAILURE_HISTORY
```

## Longitudinal route

Longitudinal material should preserve event order and standing transitions rather than present only the latest state. A reviewer should be able to distinguish:

```text
PREDECESSOR
-> PRESSURE
-> FAILURE / NON-RESULT
-> REPAIR
-> RECOMPUTATION
-> SUCCESSOR STANDING
```

Each arrow requires its own record where material.

## Routing is not classification authority

This document is a navigation surface. Artifact-specific standing remains governed by the artifact, its receipts, and the current work register. A route cannot promote an object merely by displaying it under a stronger-sounding purpose.