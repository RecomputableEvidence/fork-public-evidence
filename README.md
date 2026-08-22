# Fork

Fork is a research implementation for preserving recomputable evidence across AI-assisted workflow boundaries without silently transferring claim scope, review standing, authority, approval, or execution permission.

Fork does **not** certify, validate, approve, authorize, guarantee, or establish legal, compliance, operational, safety, production, or institutional sufficiency.

## Proof-first start

Begin with the compact public proof surface:

1. [Proof Atlas](docs/proof-atlas/README.md)
2. [Proof 001 — A Review Does Not Silently Travel](docs/proof-atlas/PROOF-001-review-does-not-silently-travel-v0.1/README.md)
3. [Public state routing v0.4](docs/state/FORK_STATE_ROUTING_v0_4.json)
4. [Narrow current public-route projection](docs/state/FORK_PUBLIC_ROUTE_CURRENT_PROJECTION_v0_1.json)

Proof 001 demonstrates a bounded proposition: a review remains attached to the exact artifact coordinate that was reviewed. Preserving the review record in a later artifact does not silently transfer that review standing.

A passing proof or checker establishes only the bounded result declared by that surface. It does not establish truth, correctness, endorsement, compliance, legal sufficiency, safety, production readiness, present reliance, or institutional authority.

## Adoption-facing evidence map — candidate

For a bounded adopter-facing view of the existing governed corpus, use:

- [Adoption-facing five-band projection](docs/adoption/README.md)
- [Machine-readable five-band projection](docs/adoption/FORK_ADOPTION_FACING_PROJECTION_v0_1_CANDIDATE.json)
- [Purpose-oriented evidence index](docs/adoption/FORK_ADOPTION_PURPOSE_INDEX_v0_1_CANDIDATE.json)

This is a non-authoritative projection over exact native coordinates. Projection inclusion does not change native standing; source-evidence admission does not become proof-packaging admission; exterior recomputation does not become generalized validation; and research remains research unless its own governed gates close.

<!-- FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING:START -->

## Branch standing and temporal routing

Fork's public branches and artifacts do not silently inherit one another's standing.

- `main@fd93d051235ec43bee925878bc916d09179b3c90` is the repaired historical default-branch line. It is not the governed evidence line used by this route.
- `preservation/clean-continuance-v0.1@723aa9aee8c329f760bcdabd323fd471a916e822` is the exact admitted evidence checkpoint used by the current public-route projection.
- Open pull requests and research branches remain candidates. Their presence, checks, or review do not confer admission.
- The routing-only successor does not represent its own future merge as a new evidentiary checkpoint.

Use these records according to scope and temporal standing:

- Current public discovery route:
  [FORK_STATE_ROUTING_v0_4.json](docs/state/FORK_STATE_ROUTING_v0_4.json)
- Narrow current public-route projection:
  [FORK_PUBLIC_ROUTE_CURRENT_PROJECTION_v0_1.json](docs/state/FORK_PUBLIC_ROUTE_CURRENT_PROJECTION_v0_1.json)
- Broader predecessor projection at its exact source coordinate:
  [FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json](docs/state/FORK_PROOF_SURFACE_CURRENT_PROJECTION_v0_2.json)
  Source coordinate: `1241c0084900f2c60f362205525464582e57b4a7`.
- Historical July 11 projection:
  [FORK_PROOF_SURFACE_STATE_v0_1.json](docs/state/FORK_PROOF_SURFACE_STATE_v0_1.json)
- Temporal-succession rule and checker:
  [FORK_TEMPORAL_SUCCESSION_v0_1.md](docs/state/FORK_TEMPORAL_SUCCESSION_v0_1.md)

Here, `current` means current only with respect to the named immutable coordinate and declared projection scope. It does not mean current with respect to an unpinned branch name, every open candidate, external truth, or execution authority.

The earlier `PUBLIC_ROUTE_STALE` result remains preserved as historical negative evidence at exact Proof 001 reviewed head `a273ab0a95decb0d43f1c091743a72ac4261027e`. This successor does not retroactively repair or overwrite that observation.

<!-- FORK_BRANCH_STANDING_AND_TEMPORAL_ROUTING:END -->

## What Fork records

Fork is a boundary-recording pattern for AI-assisted workflow handoffs. It helps later reviewers inspect:

- what crossed a boundary and what did not;
- what claim scope was preserved, narrowed, expanded, or left unresolved;
- what evidence was referenced;
- what human or machine review occurred and against which exact coordinate;
- what authority or policy context was recorded;
- what non-claims remained explicit;
- what requires revalidation;
- what must not be inferred downstream.

Fork provides evidence consistent with the hypothesis that explicit handoff-state records may reduce unsupported inheritance in bounded workflows. It does not prove that hypothesis generally.

## What Fork is not

- Fork does not determine whether a decision was correct.
- Fork does not authorize execution.
- Fork does not certify compliance or legal sufficiency.
- Fork does not prove institutional authority.
- Fork does not approve production use.
- Fork does not verify the correctness, legality, completeness, or adequacy of underlying workflow data.
- Fork does not replace governance, audit, legal review, procurement review, compliance review, runtime controls, or institutional judgment.
- Fork does not convert post-execution evidence into retrospective authorization.
- Fork does not decide whether downstream reliance is justified.

## Recompute

From the repository root, recompute Proof 001:

```bash
python tools/run_proof_001_review_does_not_silently_travel_v0_1.py --json
```

Recompute the proof-first route successor candidate:

```bash
python tools/check_public_route_successor_v0_1.py
pytest -q tests/test_public_route_successor_v0_1.py
```

General verification commands are documented at:

- [Verification commands](docs/VERIFICATION_COMMANDS_v0_1.md)
- [Public review quickstart](docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md)
- [Cross-platform verifier fallback](docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md)

PowerShell public verifier:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

A passing command indicates only the bounded structural or semantic result described by that checker.

## Reviewer and contributor routes

- [Reviewer start here](docs/REVIEWER_START_HERE_v0_1.md)
- [Reviewer routing guide](docs/REVIEWER_ROUTING_GUIDE_v0_1.md)
- [Repository review posture](docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)
- [Current bounded proof surface](docs/CURRENT_PROOF_SURFACE_v0_1.md)
- [Human recomputation sandbox](docs/recomputation/boundary-state-interop-v0.1.1/README.md)
- [Exterior observations](docs/exterior-observations/)

Exterior reviewers are observers, not authorities for Fork's claims. Their relationship, prior exposure, environment, methods, limitations, and exact review coordinates should remain visible.

## Architecture and research

- [Accountable Handoff Interoperability position paper](docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md)
- [Fork Modular Surface](docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md)
- [Surface Interaction Contract](docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md)
- [Modular Surface Crosswalk](docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md)
- [Maturity and Terminology Boundary](docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md)

The modular surfaces are Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial. They are constrained by preservation without inheritance.

## Worked context

A recurring worked example is:

> AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

This is one test case, not a recommended, validated, or industry-standard workflow. It is used to inspect whether downstream actors silently expand claim scope, authority basis, evidence basis, review standing, or reliance context.

## Commercial and buyer-facing surfaces

- [Commercial package](docs/commercial/)
- [Buyer Quick Start for GC / CISO / Risk](docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Fork preserves reconstructable evidence context for AI-assisted reliance. It is not a GRC system, SIEM replacement, runtime control plane, compliance oracle, approval system, or authority layer.

## Research status and falsifiability

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

Let `U` represent the rate of unsupported inheritance events per workflow, and let `H` represent the presence of explicit handoff-state artifacts. The hypothesis predicts:

> E[U | H = 1] < E[U | H = 0]

If controlled or quasi-controlled evaluation fails to show reduced unsupported inheritance, reliance ambiguity, or authority leakage when explicit handoff-state records are present, the hypothesis is weakened or requires refinement.

## Invariant non-claims

- No artifact grants authority merely by preserving evidence.
- No review silently travels to an unreviewed successor.
- No merge silently converts a candidate into truth or correctness.
- No policy reference proves policy applicability or satisfaction.
- No structural pass establishes legal, compliance, safety, or production sufficiency.
- No exterior observation becomes endorsement or institutional authority.
- No evidence reference becomes approval.
- No unresolved item may be resolved by assumption.
