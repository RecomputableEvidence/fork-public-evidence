# Current Proof Surface v0.1

Status: Current proof-surface index.
Scope: Public review orientation for currently available Fork evidence, checkers, protocols, and exterior observations.
Classification: Proof-surface index, not certification, validation, endorsement, legal conclusion, compliance conclusion, procurement approval, audit conclusion, safety assessment, or production-readiness assessment.

## 1. Purpose

This document states what the public repository currently demonstrates, what remains experimental, and what must not be inferred.

Its role is to help reviewers distinguish:

```text
machine-checkable proof surfaces;
doc-only protocols;
exterior observations;
interpretive reviews;
boundary-pressure experiments;
future work;
non-claims.
```

Fork's current public claim is bounded:
Fork preserves and tests evidence-boundary structures for AI-assisted workflows without absorbing authority from governance, legal, compliance, risk, audit, security, procurement, or institutional decision layers.

## 2. How to Verify the Current Public Review Package

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

Expected high-level result:

```text
PUBLIC_REVIEW_PACKAGE_VERIFY_PASS
```

The verifier currently checks required public-review files and runs the stable boundary-pressure checker.

## 3. Stable Machine-Checkable Surface

### 3.1 Boundary Pressure Review Checker v0.1

Primary checker:

```text
tools/check_boundary_pressure_review_cases_v0_1.py
```

Run directly:

```bash
python tools/check_boundary_pressure_review_cases_v0_1.py --json
```

Current checked fixture families:

- boundary_pressure_retrieval_distortion
- boundary_pressure_recomputation_receipt_overread

Current expected result:

```text
total: 4
passed: 4
failed: 0
```

### 3.2 What This Checker Demonstrates

The checker demonstrates that selected boundary-pressure fixtures are classified according to preserved boundary rules.

It currently tests whether:

- failed or partial retrieval is preserved as access limitation rather than upgraded into review or authority;
- a recomputation receipt is preserved as structural evidence rather than upgraded into validation, truth, approval, compliance, legal sufficiency, production readiness, or replacement evidence.

### 3.3 What This Checker Does Not Demonstrate

The checker does not demonstrate that:

- Fork is complete;
- Fork is production ready;
- Fork is legally sufficient;
- Fork establishes compliance;
- Fork validates truth;
- Fork approves any workflow;
- Fork authorizes execution;
- Fork proves safety;
- Fork replaces institutional controls;
- Fork provides a SIEM, GRC, audit, compliance, or policy-control system.

## 4. Boundary-Pressure Proof Surface

Boundary-pressure cases are preserved under:

```text
docs/review/boundary-pressure/
```

Current cases:

```text
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
```

Current fixtures:

```text
docs/review/boundary-pressure/fixtures/valid/BPR_RD_VALID_001_access_limitation_preserved_v0_1.json
docs/review/boundary-pressure/fixtures/invalid/BPR_RD_INVALID_001_failed_retrieval_treated_as_review_v0_1.json
docs/review/boundary-pressure/fixtures/valid/BPR_RR_VALID_001_receipt_preserved_as_structural_v0_1.json
docs/review/boundary-pressure/fixtures/invalid/BPR_RR_INVALID_001_receipt_upgraded_to_validation_v0_1.json
```

Boundary-pressure cases are experimental. They exercise failure modes where evidence, receipts, access state, or exterior observations may be overread as authority.

## 5. Protocol-Only Surfaces

### 5.1 Longitudinal Reconstruction Trial Protocol v0.1

Protocol document:

```text
docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md
```

This is currently a protocol surface, not yet a completed reconstruction trial.

It defines the target temporal claim:

```text
Fork can reconstruct a preserved AI-assisted reliance event over time from sealed artifacts alone, detect tampering or reference decay, distinguish checker drift from packet failure, and preserve the boundary between reconstruction and authorization.
```

Current status:

- protocol defined;
- schemas not yet implemented;
- Day-0 fixture not yet implemented;
- longitudinal replay receipts not yet produced.

Do not cite the longitudinal protocol as evidence that Fork has already demonstrated delayed replay over time.

### 5.2 Boundary Pressure Evaluation Framework v0.1

Framework document:

```text
docs/research/BPEF_BOUNDARY_PRESSURE_EVALUATION_FRAMEWORK_v0_1.md
```

BPEF is a framework surface. It defines pressure classes, invariants, examples, counterexamples, and cross-class cases.

Current status:

- framework documented;
- examples and counterexamples defined;
- not a certification or compliance framework;
- not a legal, safety, or production-readiness assessment.

## 6. Commercial and Buyer-Facing Surfaces

Commercial orientation files:

```text
docs/commercial/BUYER_QUICK_START_GC_CISO_RISK_v0_1.md
docs/commercial/COMMERCIAL_SURFACE_LANGUAGE_SWEEP_v0_1.md
docs/commercial/README.md
```

These materials are buyer-facing orientation surfaces.

They do not establish:

- production readiness;
- legal admissibility;
- legal sufficiency;
- compliance sufficiency;
- security-control effectiveness;
- procurement approval;
- audit approval;
- buyer approval.

Their purpose is to reduce misclassification risk for legal, security, risk, compliance, audit-adjacent, procurement-adjacent, and design-partner readers.

## 7. Exterior Observations

Exterior observations are preserved under:

```text
docs/exterior-observations/
```

Commercial-surface exterior observations include:

```text
docs/exterior-observations/commercial-surface/COMMERCIAL_SURFACE_BUYER_READINESS_OBSERVATION_INDEX_v0_1.md
```

Exterior observations may be useful as interpretive feedback.

They are not:

- recomputation receipts;
- execution receipts;
- certifications;
- endorsements;
- legal opinions;
- compliance opinions;
- security assessments;
- production-readiness assessments;
- procurement approvals;
- audit conclusions.

## 8. Repository Review Posture

Repository review posture document:

```text
docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md
```

This document explains how reviewers should interpret Fork artifacts, recomputation receipts, exterior observations, pull request history, non-claims, and boundary-pressure concerns.

Review posture rule:

```text
Evidence may be preserved.
Authority is not inherited.
Reconstruction is not approval.
Structural verification is not truth.
Exterior observation is not endorsement.
```

## 9. Current Claims Ladder

The current repository contains proof surfaces at different maturity levels.

```text
Level 0: Framing / doctrine
Level 1: Static artifact exists
Level 2: Checker executes locally
Level 3: Deterministic replay passes for bounded fixture set
Level 4: Independent reviewer recomputes
Level 5: Delayed replay succeeds over time
Level 6: Adverse cases remain detectable over time
```

Current approximate placement:

- Boundary-pressure checker: Level 2 to Level 3 for its bounded fixture set.
- Human recomputation sandbox receipts: Level 4 where preserved as exterior receipts and where execution actually occurred.
- Longitudinal reconstruction protocol: Level 1 protocol surface only.
- BPEF: Level 1 framework surface only.
- Commercial buyer surface: orientation surface only, not proof of production readiness.

This ladder is descriptive. It does not upgrade any artifact into authority.

## 10. What Fork Currently Does Not Prove

Fork currently does not prove that:

- an AI-assisted decision was correct;
- an AI-assisted artifact was true;
- an admission event was valid;
- a workflow was authorized;
- a system was compliant;
- an artifact was legally sufficient;
- a system was safe;
- a deployment was production ready;
- a buyer should approve procurement;
- a reviewer endorsed Fork;
- a receipt replaces missing source evidence;
- a failed retrieval equals review;
- reconstruction equals approval.

## 11. Screenshots and Live Systems

Screenshots may support orientation.

Screenshots are not recomputation receipts, execution receipts, source artifacts, canonical evidence packets, or proof that a sealed record reconstructs.

Live-system state is not a substitute for preserved artifacts unless the live state was itself captured, identified, and preserved according to the relevant evidence boundary.

## 12. Reviewer First Path

Recommended one-command verification:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
```

Recommended reading path:

1. docs/CURRENT_PROOF_SURFACE_v0_1.md
2. docs/REVIEWER_START_HERE_v0_1.md
3. docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md
4. docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
5. docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
6. docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md

## 13. Non-Authority Boundary

This current proof-surface index does not validate Fork, certify Fork, endorse Fork, approve Fork, establish compliance, establish legal sufficiency, establish safety, establish production readiness, or assert that any underlying AI-assisted workflow was correct.

It exists to make the public proof surface inspectable and to reduce overread.

<!-- FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING:START -->

## Boundary-pressure invalid-fixture hardening

The boundary-pressure checker now distinguishes fixture classification from evaluator confidence.

Default shipped fixture suite:

- valid retrieval limitation preserved;
- invalid retrieval distortion detected;
- valid recomputation receipt preserved as structural evidence;
- invalid recomputation receipt overread detected.

Adversarial regression suite:

- valid-shaped retrieval limitation content must not pass as invalid distortion;
- near-empty recomputation receipt overread fixture must not pass;
- invalid recomputation receipt overread fixture without overread flags must not pass;
- unknown fixture family must not pass by placement or self-declaration.

Run:

- `python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial`

This hardening does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.

<!-- FORK_BOUNDARY_PRESSURE_INVALID_FIXTURE_HARDENING:END -->

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:START -->

## Public review quickstart and expanded verifier coverage

A one-page reviewer path is now available:

- docs/review/PUBLIC_REVIEW_QUICKSTART_v0_1.md

The public verifier now includes expanded coverage for:

- current proof-surface routing;
- boundary-pressure default fixtures;
- boundary-pressure adversarial regression fixtures;
- Round 004 structured interaction filings;
- longitudinal reconstruction protocol presence;
- BPEF framework presence;
- Git whitespace checks.

Run:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

A pass remains bounded. It means required public review artifacts are present and included structural checkers passed. It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.

<!-- FORK_PUBLIC_REVIEW_QUICKSTART:END -->

<!-- FORK_LONGITUDINAL_DAY0_PACKET:START -->

## Longitudinal Reconstruction Trial Day-0 packet

The Day-0 packet for the longitudinal reconstruction trial is now present at:

- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/

The Day-0 packet includes:

- packet manifest;
- manifest SHA-256 sidecar;
- outer receipt binding the manifest hash;
- request record;
- AI output record;
- human review record;
- boundary state record;
- non-claims record;
- expected reconstruction;
- environment manifest;
- non-authority boundary statement;
- Day-0 receipts.

Checker:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

Current limitation:

- the expected reconstruction provenance is an author-declared Day-0 fixture baseline, not independent external reviewer provenance.

Boundary:

- Day-0 packet verification checks presence, hashes, manifest binding, and boundary statements only.
- It does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, production readiness, or institutional authority.

<!-- FORK_LONGITUDINAL_DAY0_PACKET:END -->
