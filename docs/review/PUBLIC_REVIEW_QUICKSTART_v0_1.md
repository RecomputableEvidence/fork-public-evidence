# Fork Public Review Quickstart v0.1

Status: Reviewer quickstart.
Scope: Public GitHub review path, verification commands, expected outputs, and objective review data.

## 1. Purpose

This quickstart gives outside reviewers a short path through Fork's current public proof surface.

It is intended for:

- access-path reviewers;
- exterior governance reviewers;
- recomputation reviewers;
- no-access reviewers documenting execution barriers;
- reviewers proposing adversarial fixtures.

This quickstart is not an endorsement request, certification request, compliance request, legal sufficiency request, safety request, production-readiness request, procurement approval request, or authority-transfer request.

## 2. Start from a clean clone

From a working directory outside the repo:

- git clone https://github.com/RecomputableEvidence/fork-public-evidence.git
- cd fork-public-evidence
- git status -sb
- git log -1 --oneline

Record:

- commit hash;
- operating system;
- shell;
- Python version;
- Git version;
- whether PowerShell was already available.

## 3. Primary proof surface

Read first:

- docs/CURRENT_PROOF_SURFACE_v0_1.md

Then read:

- docs/REVIEWER_START_HERE_v0_1.md
- docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md
- docs/review/FORK_REPOSITORY_REVIEW_POSTURE_v0_1.md

Reviewer question:

Can you tell what Fork currently demonstrates and what it explicitly does not demonstrate?

## 4. One-command public verifier

From repo root, run:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1

Expected signal:

- PUBLIC_REVIEW_PACKAGE_VERIFY_PASS

The verifier now checks:

- core public proof-surface files;
- boundary-pressure checker and fixtures;
- boundary-pressure adversarial regression fixtures;
- Round 004 interaction filing schema and observations;
- longitudinal reconstruction protocol presence;
- BPEF framework presence;
- Git whitespace checks.

This verifier checks public review package presence and bounded checker execution. It does not validate truth, compliance, legal sufficiency, safety, authorization, approval, production readiness, endorsement, certification, or institutional authority.

## 5. JSON verifier output

For structured output:

- powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1 -Json

Record:

- total;
- passed;
- failed;
- boundary-pressure default count;
- boundary-pressure adversarial count;
- Round 004 filing count;
- any failure reason.

## 6. Run the boundary-pressure checker directly

Default suite:

- python tools/check_boundary_pressure_review_cases_v0_1.py --json

Expected current signal:

- total: 4
- passed: 4
- failed: 0

Default plus adversarial regression:

- python tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial

Expected current adversarial signal:

- adversarial.total: 4
- adversarial.passed: 4
- adversarial.failed: 0

Boundary-pressure fixtures are under:

- docs/review/boundary-pressure/fixtures/

Adversarial fixtures are under:

- docs/review/boundary-pressure/fixtures/adversarial/

## 7. Run the Round 004 interaction checker directly

Run:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

Expected current signal:

- total: 4
- passed: 4
- failed: 0

Filed observations are under:

- docs/review/public-rounds/round-004/observations/

Round 004 synthesis is:

- docs/review/public-rounds/round-004/PUBLIC_REVIEW_ROUND_004_SYNTHESIS_v0_1.md

## 8. Inspect one experiment

Recommended first inspection:

- docs/review/boundary-pressure/BOUNDARY_PRESSURE_RETRIEVAL_DISTORTION_TEST_CASE_v0_1.md
- docs/review/boundary-pressure/BOUNDARY_PRESSURE_RECOMPUTATION_RECEIPT_OVERREAD_TEST_CASE_v0_1.md
- docs/review/boundary-pressure/BOUNDARY_PRESSURE_CHECKER_INVALID_FIXTURE_HARDENING_RECEIPT_v0_1.md

Reviewer question:

Can you explain why the valid fixture remains valid and why the invalid fixture is rejected without treating rejection as approval, truth, compliance, legal sufficiency, safety, or production readiness?

## 9. Optional adversarial interaction

The boundary-pressure checker supports an adversarial regression mode.

A reviewer may construct a separate fixture root and run:

- python tools/check_boundary_pressure_review_cases_v0_1.py --fixtures-root path\to\scratch_fixtures --json --run-adversarial

Suggested adversarial fixture types:

- valid-shaped content placed under invalid expectation;
- invalid fixture without explicit boundary-pressure signal;
- malformed or content-free fixture;
- unknown fixture family;
- receipt overread without overread flags;
- retrieval limitation upgraded into review, approval, authorization, validation, or compliance.

Do not edit shipped fixtures unless the review purpose is to test a proposed patch.

## 10. Longitudinal reconstruction protocol

Read:

- docs/reconstruction/FORK_LONGITUDINAL_RECONSTRUCTION_TRIAL_v0_1.md

Current status:

- protocol exists;
- Day-0 packet is implemented; replay receipts are not yet implemented;
- Day-7/30/90 replay receipts are not yet produced.

Reviewer question:

What would Fork need to preserve today so that a future reviewer could answer the same question later without inheriting today's authority?

## 11. Objective review data to record

Recommended fields:

- review round;
- reviewer role;
- operating system;
- shell;
- Python version;
- Git version;
- PowerShell version, if used;
- whether repo clone succeeded;
- whether current proof surface was found;
- whether verifier was found;
- whether boundary-pressure cases were found;
- whether longitudinal protocol was found;
- verifier attempted;
- verifier passed;
- failure reason, if any;
- time to first verifier run;
- whether command was run unmodified;
- whether underlying Python checker was run directly;
- whether adversarial fixture was constructed;
- points of confusion;
- overclaim risks noticed;
- what an exterior governance model would consume;
- what it would refuse to inherit;
- required boundary state;
- missing longitudinal artifacts;
- checker drift concerns;
- packet failure concerns;
- final review classification.

## 12. Filing template

Use:

- docs/templates/PUBLIC_REVIEW_ROUND_004_INTERACTION_TEMPLATE_v0_1.json

Schema:

- schemas/public_review_round_004_interaction_v0_1.schema.json

Checker:

- python tools/check_public_review_round_004_interactions_v0_1.py --json

## 13. Review classifications

Use one or more:

- access-path review;
- no-access observation;
- execution receipt;
- recomputation receipt;
- adversarial boundary-pressure observation;
- exterior governance articulation;
- usability review;
- longitudinal readiness observation;
- mixed review.

## 14. Boundary statement

A public verifier pass means the bounded public review package is present and the included structural checkers passed under the reviewer environment.

It does not mean Fork is true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production ready, or institutionally authoritative.

<!-- FORK_LONGITUDINAL_DAY0_PACKET:START -->

## Longitudinal Day-0 packet

The Day-0 packet is the first sealed object for later Day-7, Day-30, and Day-90 replay.

Read:

- docs/reconstruction/LONGITUDINAL_RECONSTRUCTION_DAY0_PACKET_RECEIPT_v0_1.md
- docs/reconstruction/longitudinal/day0/LRT_DAY0_PACKET_v0_1/README.md

Run:

- python tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

Record:

- packet manifest hash;
- outer receipt manifest hash;
- expected reconstruction hash;
- environment manifest hash;
- non-authority boundary statement hash;
- checker result.

Current limitation:

- expected reconstruction provenance is author-declared fixture baseline in v0.1, not independent external reviewer provenance.

<!-- FORK_LONGITUDINAL_DAY0_PACKET:END -->

<!-- FORK_PUBLIC_REVIEW_ROUND_005:START -->

## Round 005 Day-0 exterior review

Round 005 filed a Day-0 exterior review that should be read before designing the Day-0 replay checker:

- docs/review/public-rounds/round-005/PUBLIC_REVIEW_ROUND_005_SYNTHESIS_v0_1.md

Key preserved findings:

- PowerShell-only verifier access needs a cross-platform fallback.
- Day-0 status contradictions need repair.
- Coordinated re-seal risk needs an adverse longitudinal fixture.
- Lexical non-authority checking needs a limit receipt or adversarial fixture.
- Schema-present versus schema-enforced behavior needs clarification.

<!-- FORK_PUBLIC_REVIEW_ROUND_005:END -->
<!-- FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK:START -->

Platform fallback for public verifier
Primary verifier path:
powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1
If PowerShell / pwsh is unavailable, use:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
Classification rule:
PowerShell verifier ran: public verifier execution.
Fallback commands ran: manual public-verifier reconstruction.
Do not describe fallback reconstruction as execution of the named PowerShell verifier.

<!-- FORK_PUBLIC_VERIFIER_PLATFORM_FALLBACK:END -->

<!-- FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL:START -->

## Longitudinal Day-0 coordinated re-seal adversarial case

Round 005 found that coordinated re-sealing could falsify provenance, recompute internal hashes, and still pass the current Day-0 checker.

This finding is now preserved as a reproducible adversarial case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_001_coordinated_reseal_v0_1.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

Interpretation:

- a pass confirms the root-of-trust limitation is reproducible under the current v0.1 checker;
- it does not validate the mutated packet;
- it does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.

<!-- FORK_LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL:END -->

<!-- FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT:START -->

## Longitudinal Day-0 lexical non-authority limit adversarial case

Round 005 found that the Day-0 non-authority check is lexical, not semantic or negation-aware.

This finding is now preserved as a reproducible adversarial case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`
- `docs/reconstruction/adversarial/fixtures/LRT_DAY0_ADV_002_lexical_non_authority_limit_v0_1.json`
- `tools/check_longitudinal_day0_adversarial_cases_v0_1.py`

Run:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

Interpretation:

- a pass confirms the lexical limit is reproducible under the current v0.1 checker;
- it does not mean the clean Day-0 packet asserts authority;
- it does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.

<!-- FORK_LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT:END -->
