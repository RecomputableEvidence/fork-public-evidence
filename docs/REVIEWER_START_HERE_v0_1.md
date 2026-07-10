# Fork Reviewer Start Here v0.1

## Purpose

This guide is the canonical entry point for external review of Fork's public repository. It exists to reduce misinterpretation by giving reviewers one authoritative reading path, one technical validation path, one package index, and one non-claim boundary.

The root `README.md` is a short orientation. This document is the authoritative reviewer path.

## One-sentence description

Fork is read-only evidence-boundary infrastructure for AI-assisted workflows: it preserves bounded records of what was observable and captured so later reviewers can inspect the record without inheriting claims the record did not establish.

## What to read first

### Ten-minute orientation

1. Root `README.md`
2. `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
3. `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`

### Thirty-minute reviewer path

1. Root `README.md`
2. `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`
3. `docs/FORK_OPERATIONAL_BOUNDARY_MAP_v0_1.md`
4. `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/README.md`
5. `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`
6. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/README.md`
7. `docs/VERIFICATION_COMMANDS_v0_1.md`

## Technical validation path

1. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/VERIFICATION_INSTRUCTIONS.md`
2. `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/TECHNICAL_VALIDATION_MAP.md`
3. `technical-disclosure/README_VERIFY_PUBLIC_DISCLOSURE_v0_1_1.md`
4. `tools/`, `schemas/`, `examples/`, and `tests/`

## Executive buyer orientation path

Use this path only when an executive, advisor, technical sponsor, legal/compliance leader, audit leader, or design-partner sponsor asks why Fork matters commercially or organizationally.

This packet is an orientation surface. It does not establish pricing, procurement readiness, pilot approval, production deployment, legal sufficiency, compliance satisfaction, risk acceptance, or client-specific suitability.

1. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/README.md`
2. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/EXECUTIVE_BRIEF.md`
3. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/BUYER_PROBLEM.md`
4. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/USE_CASES.md`
5. `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

## Pilot discovery path

Use this path only when a serious prospect asks how a bounded workflow would be evaluated for possible pilot scoping.

This packet supports discovery and boundary scoping. It does not establish workflow suitability, commercial pilot readiness, production readiness, implementation approval, legal sufficiency, compliance satisfaction, or client-specific deployment coverage.

1. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/README.md`
2. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/EVIDENCE_BOUNDARY_WORKSHEET.md`
3. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SOURCE_SYSTEM_INVENTORY.md`
4. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/SECURITY_AND_DATA_HANDLING_QUESTIONS.md`
5. `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/CLAIMS_AND_NON_CLAIMS.md`

## Public-surface boundary

The public-review surface is not every file visible in the repository.

For external review, use the files and packages listed in this guide and in `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`.

Some publicly visible directories may contain internal working materials, legacy auxiliary materials, or non-release artifacts. Those materials must not be cited as Fork's released public-review posture unless a boundary document expressly says they are in scope.

Specific boundary markers:

- `docs/internal/` contains internal working materials and is not part of the released public-review surface.
- `pilot_package/` is an auxiliary controlled-pilot index area and is not the same thing as `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`.
- Branch-specific work is governed by `docs/EXPERIMENTAL_BRANCH_WORK_v0_1.md`.

## Reviewer posture

Review Fork as an evidence-boundary system, not as a general AI governance platform.

A valid review should distinguish:

- what the artifact preserves;
- what the verifier checks;
- what the package claims;
- what the package expressly does not claim;
- whether the artifact is released public material, internal working material, auxiliary material, or branch-specific experimental work.

## Correct interpretation of verification

A successful verification result means the checked artifact satisfied the declared structural condition for that verifier.

It does not mean the underlying workflow was correct, lawful, compliant, complete, independently witnessed, safe, production-ready, commercially ready, or client-suitable.

## Common misreadings to avoid

Do not treat Fork as:

- a policy engine;
- a workflow controller;
- an AI-output truth validator;
- a legal-admissibility system;
- a compliance certification system;
- a production deployment claim;
- a substitute for client-specific source-system analysis;
- a basis for automatic runtime blocking or authorization.

## External review rule

When citing Fork externally, cite the smallest bounded artifact that supports the statement.

Do not cite the whole repository as support for a claim that only one package, checker, or branch artifact addresses.

## Authority and policy context

Fork reviewer packets should show the stated authority and policy context for the reviewed workflow artifact.

This helps a reviewer distinguish:

- the evidence state Fork preserved;
- the purpose for which the artifact was accepted;
- the authority context asserted at the time of reliance;
- any downstream narrowing or expansion of that authority context.

Fork does not establish that the stated authority was sufficient, that the policy was adequate, or that the resulting reliance was legally, commercially, operationally, or regulatorily sufficient.

## Commercial buyer orientation

For the narrative buyer-facing commercial package, see:

- [docs/commercial/](commercial/)

This path is a lightweight buyer-orientation surface. The formal checksummed executive buyer packet remains available under:

- [
elease_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/](../release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/)

<!-- FORK-MODULAR-SURFACE-REVIEWER-PATH:START -->
## Modular Surface Reading Path

Fork now includes a dedicated modular surface architecture.

Reviewers should read these documents as the current functional map of Fork's evidence-boundary architecture:

1. `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
2. `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
3. `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`

The Modular Surface does not replace existing Fork artifacts.

It explains how existing doctrine, checkers, simulations, review packets, interoperability materials, and commercial-facing documents relate across six functional surfaces: Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial.

Its governing constraint is preservation without inheritance.
<!-- FORK-MODULAR-SURFACE-REVIEWER-PATH:END -->

<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:START -->
## Maturity and Terminology Boundary

Before treating Fork materials as production, compliance, approval, or authority infrastructure, reviewers should read:

- `docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md`

Fork is research-grade and pilot-discovery ready for bounded AI-assisted evidence-boundary workflows. It is not a general production governance platform, compliance engine, runtime control plane, approval system, or authority layer.
<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:END -->

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_START -->

## Repository review posture

Fork's repository-specific review posture is maintained here:

- [Fork Repository Review Posture v0.1](review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)

This guide explains how reviewers and contributors should interpret Fork artifacts, recomputation receipts, exterior observations, PR history, non-claims, and boundary-pressure concerns without converting evidence into authority, endorsement, certification, production readiness, legal sufficiency, or compliance conclusions.

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_END -->

<!-- FORK_BOUNDARY_PRESSURE_REVIEW_REVIEWER_START:START -->

## Boundary Pressure Review

Fork includes an experimental Boundary Pressure Review case for retrieval distortion:

- [Boundary Pressure Review / Retrieval Distortion Test Case v0.1](review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md)

This case tests whether failed retrieval or partial access is preserved as unresolved access state rather than upgraded into review, execution, recomputation, endorsement, approval, compliance, legal sufficiency, or truth.

<!-- FORK_BOUNDARY_PRESSURE_REVIEW_REVIEWER_START:END -->

<!-- FORK_COMMERCIAL_BUYER_REVIEW_PATH:START -->

## Commercial / buyer-facing review path

For GC, CISO, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers:

- [Buyer Quick Start for GC / CISO / Risk v0.1](commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Exterior commercial-surface reviews are preserved as observations, not endorsements or certifications:

- [Commercial Surface Buyer Readiness Observation Index v0.1](exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md)

<!-- FORK_COMMERCIAL_BUYER_REVIEW_PATH:END -->

<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEWER_START:START -->

Boundary Pressure Case: Recomputation Receipt Overread
Fork includes an experimental boundary-pressure case for recomputation receipt overread.
This case tests whether a recomputation receipt remains evidence of bounded structural replay rather than becoming replacement evidence, validation, approval, compliance, legal sufficiency, truth, safety, production readiness, or authority.
Start with:
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
Then run:
python tools/check_boundary_pressure_review_cases_v0_1.py --json


<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_REVIEWER_START:END -->

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:START -->

One-command public verification
From the repository root, run:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

Then read:
docs/CURRENT_PROOF_SURFACE_v0_1.md

The verifier checks the public review package surface and the stable boundary-pressure checker only. It does not validate truth, compliance, legal sufficiency, authorization, approval, safety, or production readiness.

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:END -->

<!-- FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS:START -->

## Public Review Round 004 interaction filings

Round 004 filings are preserved here:

- docs/review/public-rounds/round-004/

The interaction schema is:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Validate filed interactions with:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

These filings preserve access-path reviews, no-access observations, exterior governance articulations, and execution/recomputation observations. They are not endorsements, certifications, approvals, legal opinions, compliance opinions, production-readiness assessments, or authority transfers.

<!-- FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS:END -->

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:START -->

## Public review quickstart

Use this first when reviewing the repository from the outside:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

Primary verifier:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier now includes expanded coverage for boundary-pressure adversarial regression and Round 004 interaction filings.

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:END -->

<!-- FORK_LONGITUDINAL_DAY0_PACKET:START -->

## Longitudinal Day-0 reconstruction packet

The Day-0 packet for later longitudinal replay is available at:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

This verifies packet presence, artifact hashes, manifest sidecar, outer receipt binding, and boundary statement presence. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, or authority.

<!-- FORK_LONGITUDINAL_DAY0_PACKET:END -->

<!-- FORK_PUBLIC_REVIEW_ROUND_005:START -->

## Public Review Round 005

A Day-0 exterior review filing is available:

- docs/review/public-rounds/round-005/README.md

The filing records a Linux access-path review where the PowerShell public verifier could not run, but the reviewer manually reconstructed the verifier's underlying checks and executed the Day-0 checker directly.

Run:

- python tools/check_public_review_round_005_interactions_v0_1.py --json

<!-- FORK_PUBLIC_REVIEW_ROUND_005:END -->
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
