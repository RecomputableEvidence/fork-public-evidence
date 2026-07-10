# Fork Public Review Package Index v0.1

## Purpose

This index identifies the stable public/reviewer package surface for Fork. It separates public orientation, executive orientation, technical validation, and pilot discovery so reviewers do not have to infer which materials are current, released, or appropriate to their role.

This index is not a maturity claim. It is a navigation and boundary artifact.

## Canonical entry point


<!-- BEGIN FORK_WORKFLOW_INLET_ROUTING_V0_1 -->

Workflow-inlet routing
Fork routes by evidence-boundary input, not by buyer persona.
Use docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md to determine whether a visitor should enter through public review, candidate workflow identification, source-system/export mapping, evidence-artifact mapping, state-transition mapping, security/data-handling constraints, institutional ownership, or co-integration boundary review.
The routing sequence is:
Public repo orientation.
Workflow-inlet routing.
Client Discovery Return Packet.
Fork review of returned workflow/source-system facts.
Client Evidence Boundary Packet draft, if responsible.
Sidecar bridge specification candidate, if the boundary is accepted.
Bounded workflow PoV scope, if commercially and operationally appropriate.
This routing does not establish production readiness, legal sufficiency, compliance satisfaction, audit sufficiency, security approval, risk acceptance, workflow suitability, source completeness, commercial pilot approval, or institutional authority.
<!-- END FORK_WORKFLOW_INLET_ROUTING_V0_1 -->
Start with:

1. `README.md`
2. `docs/REVIEWER_START_HERE_v0_1.md`
3. `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`

## Package table

| Package                               | Path                                                     | Use when                                                                 | Supported claim                                                                                                          | Non-claim boundary                                                                                                                                                                                                 |
|---------------------------------------|----------------------------------------------------------|---------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Public Doctrine Packet v0.1           | `release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1/`     | A reviewer asks what Fork is and where it sits.                           | Fork has a public, bounded doctrine and evidence posture for recomputable evidence in AI-assisted workflows.            | No production deployment, legal admissibility, source completeness, decision correctness, runtime enforcement, compliance satisfaction, or client-specific readiness.                                               |
| Executive Buyer Packet v0.1           | `release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/`     | A GC, CLO, CCO, CRO, audit leader, legal ops leader, or sponsor asks why Fork matters commercially. | Fork addresses a reconstructive-fidelity gap by preserving bounded evidence records for later review.                   | No replacement of governance, compliance, audit, legal review, risk ownership, or remediation authority.                                                                                                         |
| Technical Validation Packet v0.1      | `release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1/`| A technical reviewer asks what can be inspected, checked, or verified.    | Fork has inspectable public technical materials for bounded evidence preservation and verification under controlled repository conditions. | No client production operation, full model replay, complete vendor telemetry, legal admissibility, compliance satisfaction, runtime enforcement, or decision correctness.                                         |
| Pilot Discovery Packet v0.1           | `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`     | A serious prospect asks how a bounded workflow would be evaluated for a possible pilot. | Fork can help evaluate whether a defined client workflow is suitable for bounded, read-only evidence preservation.      | No claim that the workflow is already suitable, no universal ingestion claim, no hidden backend reconstruction, no automatic blocking, and no compliance/legal conclusion.                                         |
| Client Discovery Return Packet v0.1   | `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/` | A client-side team needs to provide workflow/source-system facts before scoping. | A candidate workflow can be described in a structured way for boundary review.                                           | No claim that Fork can capture all listed systems or that the workflow is approved for pilot.                                                                                                                     |
| Client Evidence Boundary Packet v0.1  | `release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/` | Fork translates completed discovery into a specific workflow evidence-boundary draft. | A workflow-specific preservation boundary can be stated for review.                                                      | No coverage of other workflows, no unobserved-system claim, no legal/compliance conclusion, and no response/remediation ownership.                                                                                |

## Technical validation commands

From the repository root:

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PUBLIC_DOCTRINE_PACKET_v0_1
python ./tools/check_release_package.py ./release_packages/FORK_TECHNICAL_VALIDATION_PACKET_v0_1
```

Before checking the pilot discovery package, note: This verifies package structure and checksums only; it does not validate commercial pilot readiness.

```powershell
python ./tools/check_release_package.py ./release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1
```

For public technical disclosure verification:

```powershell
cd ./technical-disclosure
python ./verify_public_disclosure.py
cd ..
```

## Release status rule

Materials on `main` are the public-review baseline unless a review request explicitly names a different branch. Tagged GitHub releases are frozen release artifacts.

Branch work is not part of the public-review baseline until merged into `main`, tagged, or explicitly listed in a bounded review request.

## Package-selection rule

Send the smallest package that truthfully answers the recipient's question.

Do not send a later-stage package merely to appear more mature.

Do not let a package imply a broader claim than its `CLAIMS_AND_NON_CLAIMS.md` supports.

## Commercial buyer orientation

- [docs/commercial/](commercial/) — narrative buyer-facing commercial package for post-v0.1 design-partner and reviewer conversations.
- [
elease_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/](../release_packages/FORK_EXECUTIVE_BUYER_PACKET_v0_1/) — formal checksummed executive buyer packet.

<!-- FORK-MODULAR-SURFACE-PUBLIC-INDEX:START -->
## Modular Surface Package

The Modular Surface package provides the current functional map for Fork's evidence-boundary architecture.

Reviewers should use it to understand how Fork separates Evidence Boundary, Transition, Reliance, Interoperability, Simulation, and Commercial surfaces without transferring authority across them.

Package files:

- `docs/modular-surface/FORK_MODULAR_SURFACE_v0_1.md`
- `docs/modular-surface/FORK_SURFACE_INTERACTION_CONTRACT_v0_1.md`
- `docs/modular-surface/FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md`
<!-- FORK-MODULAR-SURFACE-PUBLIC-INDEX:END -->

<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:START -->
## Maturity and Terminology Boundary

This package defines Fork's current maturity posture and terminology guardrails so reviewers do not confuse evidence-boundary preservation with authority, approval, compliance, correctness, continuation validity, or production governance.

- `docs/architecture/FORK_MATURITY_AND_TERMINOLOGY_BOUNDARY_v0_1.md`
<!-- FORK-MATURITY-TERMINOLOGY-BOUNDARY:END -->

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_START -->

## Repository review posture

Fork's repository-specific review posture is maintained here:

- [Fork Repository Review Posture v0.1](review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md)

This guide explains how reviewers and contributors should interpret Fork artifacts, recomputation receipts, exterior observations, PR history, non-claims, and boundary-pressure concerns without converting evidence into authority, endorsement, certification, production readiness, legal sufficiency, or compliance conclusions.

<!-- FORK_REPOSITORY_REVIEW_POSTURE_LINK_END -->

<!-- FORK_BOUNDARY_PRESSURE_REVIEW_PUBLIC_INDEX:START -->

## Boundary Pressure Review

Boundary Pressure Review artifacts exercise failure cases where structural evidence, unresolved state, authority, sufficiency, truth, endorsement, and compliance may be incorrectly collapsed.

- [Boundary Pressure Review / Retrieval Distortion Test Case v0.1](review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md)
- Checker: `tools/check_boundary_pressure_review_cases_v0_1.py`
- Fixtures: `docs/review/boundary-pressure/fixtures/`

<!-- FORK_BOUNDARY_PRESSURE_REVIEW_PUBLIC_INDEX:END -->

<!-- FORK_COMMERCIAL_SURFACE_BUYER_READINESS_ROUTING:START -->

## Buyer-facing commercial surface

For GC, CISO, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers:

- [Buyer Quick Start for GC / CISO / Risk v0.1](commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md)

Commercial-surface exterior observations are preserved here:

- [Commercial Surface Buyer Readiness Observation Index v0.1](exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md)

These observations are buyer-surface interpretation reviews only. They are not endorsements, validations, certifications, approvals, production-readiness assessments, legal conclusions, compliance conclusions, procurement conclusions, audit conclusions, or control-effectiveness conclusions.

<!-- FORK_COMMERCIAL_SURFACE_BUYER_READINESS_ROUTING:END -->

<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_PUBLIC_INDEX:START -->

Boundary Pressure Review: Recomputation Receipt Overread
This boundary-pressure case tests whether a recomputation receipt is preserved as structural evidence without being upgraded into validation, endorsement, approval, compliance, legal sufficiency, truth, safety, production readiness, or institutional authority.
Test case: docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
Valid fixture: docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json
Invalid fixture: docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json
Checker: tools/check_boundary_pressure_review_cases_v0_1.py
The case does not validate Fork, certify Fork, approve Fork, establish legal sufficiency, establish compliance sufficiency, or prove the truth of any underlying artifact.

<!-- FORK_BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_PUBLIC_INDEX:END -->

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:START -->

Current proof surface and verifier
Start here for the current public proof surface:
docs/CURRENT_PROOF_SURFACE_v0_1.md

Run the public review verifier:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

The verifier checks the current public-review routing surface and runs the stable boundary-pressure checker. Passing verification is not certification, endorsement, legal sufficiency, compliance sufficiency, safety, production readiness, procurement approval, or institutional authority.

<!-- FORK_CURRENT_PROOF_SURFACE_AND_PUBLIC_VERIFIER:END -->

<!-- FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS:START -->

## Public Review Round 004

Round 004 preserves structured interaction filings for GitHub accessibility, exterior governance articulation, objective data capture, and longitudinal recomputation readiness.

Start here:

- docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md

Schema:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Checker:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

<!-- FORK_PUBLIC_REVIEW_ROUND_004_INTERACTION_FILINGS:END -->

<!-- FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING:START -->

## Boundary-pressure checker invalid-fixture hardening

Hardening receipt:

- `docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md`

Adversarial regression fixtures:

- `docs/review/boundary-pressure/fixtures/adversarial/`

Run default plus adversarial regression:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`

<!-- FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING:END -->

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:START -->

## Public review quickstart and expanded verifier coverage

Quickstart:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

Expanded public verifier:

- scripts/verify_public_review_package_v0_1.ps1

The verifier checks core proof-surface files, boundary-pressure fixtures, adversarial regression fixtures, Round 004 interaction filings, longitudinal protocol presence, BPEF presence, and Git whitespace checks.

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:END -->

<!-- FORK_LONGITUDINAL_DAY0_PACKET:START -->

## Longitudinal Reconstruction Trial Day-0 packet

Receipt:

- docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md

Packet root:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

Checker:

- tools/check_longitudinal_reconstruction_day0_packet_v0_1.py

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

<!-- FORK_LONGITUDINAL_DAY0_PACKET:END -->

<!-- FORK_PUBLIC_REVIEW_ROUND_005:START -->

## Public Review Round 005

Round 005 files an exterior review of the Longitudinal Reconstruction Day-0 packet.

Read:

- docs/review/public-rounds/round-005/README.md
- docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md
- docs/review/public-rounds/round-005/observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json
- docs/review/public-rounds/round-005/sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md

Run:

- python tools/check_public_review_round_005_interactions_v0_1.py --json

<!-- FORK_PUBLIC_REVIEW_ROUND_005:END -->
