# Public Review Round 005

Status: Exterior review filing surface.
Round: Longitudinal Day-0 Packet Accessibility, Reconstruction Boundary, and Replay Readiness Review.

## Scope

Round 005 asks whether an outside reviewer can inspect the public repo, run or reconstruct the verifier/checkers, inspect the Day-0 packet, and determine what can and cannot be reconstructed later without absorbing authority.

It does not ask reviewers to assess Fork as true, compliant, legally sufficient, safe, authorized, approved, certified, endorsed, production-ready, validated, or institutionally authoritative.

## Filed observations

- observations/ROUND005_OBS_001_claude_lrt_day0_exterior_review_v0_1.json

## Source receipts

- sources/EXTERIOR_REVIEW_LRT_DAY0_PACKET_v0_1.md

## Checker

Run from repository root:

- python tools/check_public_review_round_005_interactions_v0_1.py --json

## Key findings preserved

- PowerShell-only primary verifier path created access friction.
- The reviewer manually reconstructed verifier checks rather than running the named verifier.
- Day-0 packet checker passed 27/27.
- Stale Day-0 status contradictions exist in read-first docs.
- Protocol section 8 and the Day-0 packet provenance structure diverge.
- Day-0 schema is declared and present but not enforced by the checker.
- Non-authority language checking is lexical, not semantic.
- Coordinated re-seal passed 27/27 after falsified provenance and recomputed hashes.
- Evidence-file byte verification can be overread as content verification.

## Boundary

This round files exterior observations. It does not convert reviewer execution into endorsement, validation, certification, legal sufficiency, compliance sufficiency, safety, authorization, approval, production readiness, or institutional authority.
<!-- FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE:START -->

Round 005 response: status repair and verifier fallback
Response receipt:
docs/review/public-rounds/round-005/ROUND005_RESPONSE_STATUS_AND_VERIFIER_FALLBACK_v0_1.md
Public verifier fallback:
docs/review/PUBLIC_VERIFIER_PLATFORM_FALLBACK_v0_1.md
This response fixes stale Day-0 status language and documents manual public-verifier reconstruction for reviewers who cannot execute the PowerShell verifier.

<!-- FORK_ROUND005_STATUS_AND_VERIFIER_FALLBACK_RESPONSE:END -->

<!-- FORK_ROUND005_COORDINATED_RESEAL_RESPONSE:START -->

## Round 005 response: coordinated re-seal adversarial case

The coordinated re-seal finding from Round 005 is now preserved as a reproducible adversarial case.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`

Case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_COORDINATED_RESEAL_ADVERSARIAL_CASE_v0_1.md`

Checker:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

This response records a root-of-trust limitation. It does not validate the adversarially mutated packet.

<!-- FORK_ROUND005_COORDINATED_RESEAL_RESPONSE:END -->

<!-- FORK_ROUND005_LEXICAL_NON_AUTHORITY_LIMIT_RESPONSE:START -->

## Round 005 response: lexical non-authority limit adversarial case

The lexical non-authority finding from Round 005 is now preserved as a reproducible adversarial case.

Response receipt:

- `docs/review/public-rounds/round-005/ROUND005_RESPONSE_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`

Case:

- `docs/reconstruction/adversarial/LONGITUDINAL_DAY0_LEXICAL_NON_AUTHORITY_LIMIT_ADVERSARIAL_CASE_v0_1.md`

Checker:

- `python tools/check_longitudinal_day0_adversarial_cases_v0_1.py --json`

This response records a lexical checker limitation. It does not mean the clean Day-0 packet asserts authority.

<!-- FORK_ROUND005_LEXICAL_NON_AUTHORITY_LIMIT_RESPONSE:END -->
