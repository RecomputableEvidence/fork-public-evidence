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