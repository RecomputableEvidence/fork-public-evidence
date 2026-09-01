# Fork

Fork is a research implementation for preserving recomputable evidence across AI-assisted workflow boundaries without silently transferring claim scope, review standing, authority, approval, or execution permission.

Fork does **not** certify, validate, approve, authorize, guarantee, or establish legal, compliance, operational, safety, production, or institutional sufficiency.

## Choose a path

### Recompute one bounded proof

Start with [Proof Atlas](docs/proof-atlas/README.md) and [Proof 001 — A Review Does Not Silently Travel](docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/README.md).

```bash
python tools/run_proof_001_review_does_not_silently_travel_v0_1.py --json
```

A passing proof establishes only the bounded result declared by that proof surface.

### Evaluate adoption or integration

Start with the [adoption-facing evidence route](docs/adoption/README.md). It presents existing Fork evidence by purpose while preserving each source artifact's native standing.

### Review research and standing

Start with the [Fork Research Program](docs/research/fork-research-program-v0.1/README.md) and the [current standing projection](docs/preservation/current-standing/FORK_CURRENT_STANDING_PROJECTION_2026_08_08_v0_1.json).

### Inspect failures, correction lineage, and history

Start with the [failure-mode archive](docs/preservation/failure-mode-archive-v0.1/README.md). Fork preserves adverse results and predecessor states rather than rewriting them out of history.

## Technical review

For a short cold-review path, use [Reviewer Start Here v0.2](docs/REVIEWER_START_HERE_v0_2.md).

For the versioned public technical disclosure successor, use [Public Disclosure v0.1.2](technical-disclosure/v0.1.2/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_2.md).

## What Fork records

Fork helps later reviewers inspect:

- what crossed a workflow boundary and what did not;
- what claim scope was preserved, narrowed, expanded, or left unresolved;
- what evidence was referenced;
- what human or machine review occurred and against which exact coordinate;
- what authority or policy context was recorded;
- what non-claims remained explicit;
- what requires revalidation;
- what must not be inferred downstream.

## Functional architecture

Fork's six functional surfaces are Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial. Their governing constraint is preservation without inheritance.

See the [Fork Modular Surface](docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md) and [Surface Interaction Contract](docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md) when architectural depth is needed.

## Routing and exact standing

The human entry surface is intentionally small. Exact temporal routing, source coordinates, proof standing, adoption projections, review evidence, and historical predecessor records remain available beneath it.

Candidate routing record: [FORK_STATE_ROUTING_v0_5_CANDIDATE](docs/state/FORK_STATE_ROUTING_v0_5_CANDIDATE.json).

<!-- FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING:START -->

### Machine-consumed temporal route

The compact human route above does not replace Fork's exact temporal-routing contract. Public branches and artifacts do not silently inherit one another's standing.

- `main@fd93d051235ec43bee925878bc916d09179b3c90` is the repaired historical default-branch line. It is not the governed evidence line used by this route.
- `preservation/clean-continuance-v0.1@723aa9aee8c329f760bcdabd323fd471a916e822` is the exact admitted evidence checkpoint used by the current public-route projection.
- Open pull requests and research branches remain candidates. Their presence, checks, or review do not confer admission.
- The routing-only successor does not represent its own future merge as a new evidentiary checkpoint.

Use these records according to scope and temporal standing:

- [Public state routing v0.4](docs/state/FORK_STATE_ROUTING_v0_4.json)
- [Narrow current public-route projection](docs/state/FORK_PUBLIC_ROUTE_CURRENT_PROJECTION_v0_1.json)
- [Broader predecessor projection](docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json), source coordinate `1241c0084900f2c60f362205525464582e57b4a7`
- [Historical July 11 projection](docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json)
- [Temporal-succession rule](docs/state/FORK_TEMPORAL_SUCCESSION_v0_1.md)

Here, `current` means current only with respect to the named immutable coordinate and declared projection scope. It does not mean current with respect to an unpinned branch name, every open candidate, external truth, or execution authority.

The earlier `PUBLIC_ROUTE_STALE` result remains preserved as historical negative evidence at exact Proof 001 reviewed head `a273ab0a95decb0d43f1c091743a72ac4261027e`. This successor does not retroactively repair or overwrite that observation.

<!-- FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING:END -->

### Machine-consumed hypothesis contract

Fork provides evidence consistent with the hypothesis that explicit handoff-state records may reduce unsupported inheritance in bounded workflows. It does not prove that hypothesis generally. Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

Let `U` represent the rate of unsupported inheritance events per workflow, and let `H` represent the presence of explicit handoff-state artifacts. The declared causal hypothesis is:

> E[U | H = 1] < E[U | H = 0]

If controlled or quasi-controlled evaluation fails to show reduced unsupported inheritance, reliance ambiguity, or authority leakage when explicit handoff-state records are present, the hypothesis is weakened or requires refinement.

## Invariant non-claims

- Repository presence is not admission.
- Projection inclusion is not native standing.
- Source-evidence admission is not proof-packaging admission.
- Structural verification is not truth, compliance, legal sufficiency, safety, production readiness, or authority.
- Exterior observation is not endorsement.
- A correction does not erase predecessor failure.
- No unresolved item may be resolved by assumption.
