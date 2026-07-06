# Fork Modular Surface Crosswalk v0.1

## Purpose

This document maps Fork's six functional surfaces to existing doctrine, schemas, examples, simulations, and enforcement surfaces.

It exists so reviewers can read the Modular Surface as a concordance across existing work rather than as a competing taxonomy.

The Modular Surface does not replace existing Fork artifacts. It provides a functional map over them.

## Governing Constraint

All surfaces remain governed by preservation without inheritance.

Fork may preserve, reference, inspect, recompute, and reconstruct evidence-boundary records.

Fork does not absorb external authority or convert structural verification into truth, approval, compliance, admissibility, legal sufficiency, safety, or downstream decision correctness.

## Surface-to-Artifact Crosswalk

| Modular surface | Existing repo line | Current enforcement posture |
|---|---|---|
| Evidence Boundary | Claim Boundary Contract line, Required Source Non-Claims, Provenance Tier, Relational Graph Verifier | Checker/CI-backed across core evidence-boundary artifacts |
| Transition | Boundary Delta Record, Transition Integrity materials | Fixture/checker-backed where BDR applies; not yet surfaced as modular-surface enforcement |
| Reliance | Claim Consumption Events, System Mapping Receipt | Checker-backed in existing lines; not yet wired to the modular surface contract |
| Interoperability | CCEC Governance Interoperability Profile, GLM declaration, system mapping materials | Checker-backed in existing profile lines; modular-surface interaction rules not yet separately enforced |
| Simulation | Governance proof-surface scenarios, claim-inheritance simulations, ESAL/RGV-related replay materials | Partially CI-backed through simulation checkers and scenario fixtures |
| Commercial | docs/commercial/*, buyer/discovery materials | Narrative only by design; derivative of technical surfaces |

## Reading Guidance

The crosswalk should be read as a map from function to implementation.

It does not imply that every surface has the same maturity level.

It also does not imply that every surface currently has a dedicated schema, fixture set, checker, or CI workflow.

Fork's recurring hardening pattern remains:

1. Doctrine
2. Schema
3. Fixtures
4. Checker
5. CI
6. Reviewer-facing evidence

The Surface Interaction Contract is currently at the doctrine/design-control stage. Its candidate machine-readable constraints are intended to guide a later schema and fixture pass.

## Reconciling Existing Fork Models

Fork currently contains several organizing models. They are not equivalent, and they should not be read as competing definitions.

### Conceptual Stack

The Conceptual Stack describes dependency order: independent establishment, recomputable evidence, preservation without inheritance, transition integrity, and bounded propagation.

### Six-Layer Evidentiary Model

The Six-Layer Evidentiary Model describes evidentiary interpretation layers: content, attribution, mechanical status, inference boundary, resolution authority, and resolution history.

### Surface Doctrine

The earlier Surface Doctrine describes audience-facing lanes: Reviewer, Pilot, and Proof.

### Reviewer Artifact Set

The Reviewer Artifact Set describes reviewable artifact forms: Evidence Card, Boundary Map, Verification Receipt, Review Packet, and Non-Claim Panel.

### Modular Surface

The Modular Surface describes functional architecture: Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial.

These are different axes.

A reviewer-facing proof artifact may exercise one or more functional surfaces, but audience routing does not define Fork's internal modular architecture.

## Surface Doctrine Reconciliation

The earlier Surface Doctrine remains useful as an audience-lane model.

The Modular Surface is the functional architecture model.

A Proof-surface artifact, for example, may belong to the Simulation Surface if it demonstrates a valid or invalid recomposition. It may also reference the Evidence Boundary Surface if it includes structural verification material.

The important distinction is:

- Surface Doctrine answers: who is this material for?
- Modular Surface answers: what functional role does this material play?

## Next Hardening Milestone

The next natural hardening step is to convert the Surface Interaction Contract into a minimal schema and fixture set.

A small first pass should include:

1. A valid interaction fixture.
2. A Rule 1 Evidence Boundary immutability violation.
3. A Non-Absorption Test failure.
4. A checker that returns structural outcomes only.

This should remain bounded. The checker should not produce truth, approval, compliance, safety, admissibility, legal sufficiency, or authority outcomes.

## Status Boundary

This crosswalk is a reviewer-orientation artifact.

It does not add new authority to Fork.

It does not certify any workflow, artifact, model, organization, policy, or decision.

It maps current repo structure so Fork's existing artifacts can be reviewed as a coherent evidence-boundary architecture.
