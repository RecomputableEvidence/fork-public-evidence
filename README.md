# Fork

Fork is a research implementation exploring whether explicit handoff-state artifacts reduce unsupported inheritance in AI-assisted institutional workflows.

Fork does **not** certify, validate, approve, authorize, guarantee, or establish legal, compliance, operational, or institutional sufficiency.

Start here: [`docs/REVIEWER_START_HERE_v0_1.md`](docs/REVIEWER_START_HERE_v0_1.md)

## Research Status

Fork's current evidence supports an engineering pattern and a motivated hypothesis, not a proven general systems theory.

Fork is one implementation case for AI-assisted institutional workflows. It does not establish that explicit handoff-state communication is universally required, superior to existing mechanisms, or sufficient for accountability by itself.

## What Fork Is

Fork is a boundary-recording pattern for AI-assisted workflow handoffs. It helps later reviewers inspect:

- what crossed a boundary;
- what did not cross;
- what claim scope was preserved;
- what authority or policy context was recorded;
- what evidence was referenced;
- what non-claims remained explicit;
- what required revalidation;
- what should not be inferred downstream.

Fork implements and explores an accountable handoff pattern. It provides initial evidence consistent with the hypothesis that explicit handoff-state records may reduce unsupported inheritance in bounded workflows.

## What Fork Is Not

- Fork does not determine whether a decision was correct.
- Fork does not authorize execution.
- Fork does not certify compliance.
- Fork does not prove institutional authority.
- Fork does not establish legal sufficiency.
- Fork does not approve production use.
- Fork does not verify the correctness, legality, completeness, or adequacy of underlying workflow data.
- Fork does not replace governance, runtime authority, audit, legal review, procurement review, compliance review, or institutional judgment.
- Fork does not convert post-execution evidence into retrospective authorization.
- Fork does not decide whether downstream reliance is justified.

## Example Workflow

Current worked example:

AI-assisted vendor-risk recommendation → internal decision memo → downstream reliance attempt.

This is one test case, not a recommended, validated, or industry-standard pattern.

The example explores how an AI-assisted artifact can move into institutional reliance, and how a bounded handoff record can help reviewers inspect whether downstream actors silently expanded the claim, authority basis, evidence basis, or reliance context.

## Start Here

Primary reviewer path:

1. [`docs/REVIEWER_START_HERE_v0_1.md`](docs/REVIEWER_START_HERE_v0_1.md)

Additional routing is available here:

- [`docs/REVIEWER_ROUTING_GUIDE_v0_1.md`](docs/REVIEWER_ROUTING_GUIDE_v0_1.md)

## Research Context

The broader research hypothesis is described here:

- [`docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md`](docs/research/ACCOUNTABLE_HANDOFF_INTEROPERABILITY_POSITION_PAPER_v0_1.md)

Short form:

> Accountable Handoff Interoperability is the hypothesis that independently accountable systems require explicit handoff-state communication when exchanging consequential state. Fork is one implementation case for AI-assisted institutional workflows. The hypothesis is not proven.

## Falsifiability

Let `U` represent the rate of unsupported inheritance events per workflow.

Let `H` represent the presence of explicit handoff-state artifacts.

The hypothesis predicts:

> E[U | H = 1] < E[U | H = 0]

If controlled or quasi-controlled evaluation fails to show reduced unsupported inheritance, reliance ambiguity, or authority leakage in workflows with explicit handoff-state records, the hypothesis is weakened or requires refinement.

## Policy Reference Non-Claim

Presence of a policy reference does not imply:

- policy applicability;
- policy approval;
- compliance determination;
- authority sufficiency;
- legal adequacy;
- operational readiness.

A policy reference records only that a policy context was asserted or referenced in the bounded workflow record. Any determination that the policy was applicable, adequate, current, satisfied, or sufficient requires separate institutional authority.

## Verification

Verification commands and structural checks are documented here:

- [`docs/VERIFICATION_COMMANDS_v0_1.md`](docs/VERIFICATION_COMMANDS_v0_1.md)

A passing command indicates only the bounded structural result described by that checker. It does not establish correctness, compliance, legal sufficiency, production readiness, institutional authority, or factual truth.

## Non-Claims

Fork preserves bounded handoff records so later reviewers can inspect what was claimed, relied upon, excluded, changed, unresolved, or explicitly not transferred.

The following non-claims are invariant:

- This system does not assert legal sufficiency.
- This system does not grant authority.
- This system does not certify compliance.
- This system does not approve production use.
- This system does not replace institutional review.
- This system does not verify correctness of underlying workflow data.

## Commercial surface

A buyer-facing post-v0.1 commercial package is available at:

- [Commercial package](docs/commercial/)

<!-- FORK-MODULAR-SURFACE-README:START -->
## Fork Modular Surface

Fork's current architecture is organized through a modular evidence-boundary surface.

The six functional surfaces are:

- Evidence Boundary
- Transition
- Reliance
- Interoperability
- Simulation
- Commercial

These surfaces are governed by a single constraint: preservation without inheritance.

Fork may preserve, reference, inspect, and reconstruct evidence-boundary records, but it does not absorb external authority or convert structural verification into truth, approval, compliance, admissibility, legal sufficiency, or downstream decision correctness.

Start here:

- `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
- `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
<!-- FORK-MODULAR-SURFACE-README:END -->

<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:START -->
## Maturity and Terminology Boundary

Fork is research-grade and pilot-discovery ready for bounded AI-assisted evidence-boundary workflows. It is not a general production governance platform, compliance engine, runtime control plane, approval system, or authority layer.

For terminology guardrails and maturity boundaries, see:

- `docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md`
<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:END -->

<!--  -->
## Human recomputation sandbox â€” Boundary-State Interop v0.1.1

A bounded human recomputation sandbox is available at:

docs/recomputation/boundary-state-interop-v0.1.1/README.md

It files an exterior verification receipt and gives independent reviewers a branch-local way to recompute the v0.1.1 evidence packet without treating the original receipt, checker, or Fork repository as authority.
<!--  -->

## Exterior Observance Experiment v0.1

Fork is entering an Exterior Observance Experiment v0.1.

The purpose is not endorsement, promotion, validation, production adoption, certification, approval, consensus, or praise.

The purpose is to expose a bounded evidence-boundary experiment to practitioners who can observe, challenge, misunderstand, refine, or pressure-test its surfaces without becoming authority for Fork's claims.

Fork is no longer only asking:

- Can this evidence surface be internally specified and recomputed?

It can now also ask:

- How do exterior observers from different governance positions interpret the surface, its limits, its failure modes, and its adjacent responsibilities?

In this phase:

- the repository is the observance surface;
- the sandbox is the controlled environment;
- contributors are exterior observers, not authorities;
- observations are preserved with scope, limitations, interaction type, and non-endorsement;
- exterior commentary is not converted into validation, endorsement, or inherited authority.

The current sandbox question is:

> Does the evidence surface continue to preserve distinguishability between structural reproduction, unresolved state, evidentiary sufficiency, authority, and truth-claims under adverse conditions?

Exterior observations are preserved under `docs/exterior-observations/`.

Fork now has enough articulated form to be observed without asking observers to believe in it.

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_START -->

## Repository review posture

Fork's repository-specific review posture is maintained here:

- [Fork Repository Review Posture v0.1](docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)

This guide explains how reviewers and contributors should interpret Fork artifacts, recomputation receipts, exterior observations, PR history, non-claims, and boundary-pressure concerns without converting evidence into authority, endorsement, certification, production readiness, legal sufficiency, or compliance conclusions.

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_END -->

<!-- FORK_BUYER_QUICK_START_GC_CISO_RISK:START -->

## Buyer-facing overview (GC / CISO / Risk)

For legal, security, risk, compliance, audit-adjacent, and design-partner readers, start here:

- [Buyer Quick Start for GC / CISO / Risk v0.1](docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Fork preserves reconstructable evidence context for AI-assisted reliance. It does not certify compliance, establish legal admissibility, replace institutional controls, operate detection systems, function as a GRC system, replace SIEM or logging platforms, or act as a runtime control plane.

<!-- FORK_BUYER_QUICK_START_GC_CISO_RISK:END -->

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:START -->

Current proof surface and public verifier
Reviewers can inspect the current bounded proof surface here:
docs/CURRENT_PROOF_SURFACE_v0_1.md

Run the current public review verifier from the repository root:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier checks required public-review files and executes the stable boundary-pressure checker. It does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, or institutional authority.

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:END -->

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:START -->

## Public review quickstart

For a one-page reviewer path, use:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

The public verifier is:

- scripts/verify_public_review_package_v0_1.ps1

Run from repo root:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

This path is for public inspection, structural verification, and exterior review. It is not endorsement, certification, compliance approval, legal sufficiency, safety approval, production readiness, or authority transfer.

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:END -->
<!-- FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK:START -->

Public verifier platform fallback
Primary public verifier:
scripts/verify_public_review_package_v0_1.ps1
For Linux/macOS reviewers without PowerShell or pwsh, use:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Important distinction:
executing the PowerShell verifier is public verifier execution;
running the documented cross-platform commands is manual public-verifier reconstruction.
Manual reconstruction is useful review evidence, but it is not identical to executing the named verifier artifact.

<!-- FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK:END -->
