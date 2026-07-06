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

<!-- FORK-PROOF-SURFACE-TERMINOLOGY:START -->
## Proof Surface Terminology Reconciliation

The phrase "proof surface" appears historically in two bounded senses inside the Fork repository.

First, in audience-facing surface doctrine, the Proof Surface is a technical-review lane: the schemas, checkers, fixtures, receipts, and verification commands a diligence reviewer can inspect.

Second, in simulation doctrine, the Governance Simulation Proof Surface is a falsifiability mechanism: scenarios that test whether claim boundaries, non-claims, handoff rules, and reliance semantics remain inspectable under recomposition, altered conditions, invalid handoffs, or adversarial interpretation.

Under the modular surface model, these meanings reconcile as follows:

| Historical phrase | Modular-surface mapping | Boundary |
|---|---|---|
| Proof Surface as reviewer lane | Reviewer access to Evidence Boundary, Transition, Reliance, Interoperability, and Simulation artifacts through schemas, checkers, fixtures, receipts, and verification commands. | Does not mean proof of correctness, compliance, safety, legal sufficiency, or authority. |
| Governance Simulation Proof Surface | Primarily maps to the Simulation Surface. | Tests whether boundary failures are inspectable; does not certify real-world correctness or policy sufficiency. |

Accordingly, "proof surface" should be read as bounded structural inspectability, not truth certification or authority.
<!-- FORK-PROOF-SURFACE-TERMINOLOGY:END -->

## Surface Doctrine Reconciliation

The earlier Surface Doctrine remains useful as an audience-lane model.

The Modular Surface is the functional architecture model.

A Proof-surface artifact, for example, may belong to the Simulation Surface if it demonstrates a valid or invalid recomposition. It may also reference the Evidence Boundary Surface if it includes structural verification material.

The important distinction is:

- Surface Doctrine answers: who is this material for?
- Modular Surface answers: what functional role does this material play?

## Surface Interaction Hardening Status

The first Surface Interaction Contract hardening pass has now been added.

Current artifacts include:

- `schemas/surface_interaction_v0_1.schema.json`
- `tools/check_surface_interaction_v0_1.py`
- A valid reliance-to-evidence-boundary fixture.
- A boundary-mutation invalid fixture.
- A semantic-adoption invalid fixture.
- An authority-absorption invalid fixture.
- `tests/test_surface_interaction_v0_1.py`
- `.github/workflows/surface-interaction-v0-1.yml`

The remaining hardening work is narrower:

- Expand fixture coverage across additional surface pairs.
- Keep each invalid fixture focused on a single failure mode unless a fixture is explicitly testing multi-trigger precedence.
- Keep the checker outcome bounded to structural inspectability and non-absorption failures.
- Continue syncing this crosswalk when checker coverage changes.

## Status Boundary

This crosswalk is a reviewer-orientation artifact.

It does not add new authority to Fork.

It does not certify any workflow, artifact, model, organization, policy, or decision.

It maps current repo structure so Fork's existing artifacts can be reviewed as a coherent evidence-boundary architecture.
