# FPCF-002 — Public preservation publication receipt v0.1

**Status:** PUBLIC_SOURCE_PRESERVATION_OBSERVED / FORECAST_ADMISSION_WITHHELD / METHOD_CAUSAL_CLAIM_WITHHELD / OUTCOMES_NOT_ADJUDICATED.

## Publication event

- Public repo: `RecomputableEvidence/fork-public-evidence`.
- Public draft PR: https://github.com/RecomputableEvidence/fork-public-evidence/pull/200
- GitHub-provided PR `created_at`: `2026-10-27T01:36:30Z` (October 26, 2026, 18:36:30 PDT).
- Initial published binary-containing commit: `d4efa648e1cde5e2fcf10b0331ef81c2eed99d79`.
- Later fixed-commit readback coordinate for original bytes and five textual companion assets: `0fe93d1620bc088a080c9da26c251b18403974d9`.
- Release binary: `docs/experiments/FPCF-002/public-preservation-v0.1/FPCF_002_PUBLIC_PRESERVATION_BUNDLE_v0.1.zip`.
- Binary size: 578,773 bytes.
- Binary SHA-256: `762d10b7d0d64d7e75052360b8011ca168764c3337afb820f87db83011a4bc22`.
- Binary Git object SHA-1: `f75c93de5042a257174101170aaea2a4cf431f23`.

## Observed publication verification

1. Local bundle verifier: `PASS` for 15 manifest-checked files, including 12 preserved preexisting source files; the bundle index describes 18 fresh forecasts (6 per arm) and explicitly separates the earlier 25-case catalogue.
2. Scratch mutation of `README.md` inside ZIP: read-only verifier rejected it; modified whole-bundle SHA-256 did not match pinned original.
3. GitHub object-store `create_blob` returned SHA-1 `f75c93de5042a257174101170aaea2a4cf431f23`, equal to independently calculated local `git hash-object` for the exact bundle bytes.
4. GitHub tree traversed at fixed commit `0fe93d1620bc088a080c9da26c251b18403974d9`; targeted ZIP entry type `blob`, size `578773`, SHA-1 `f75c93de5042a257174101170aaea2a4cf431f23`.
5. Separate fixed-commit GitHub readback for `README.md`, `CASE_INDEX.md`, `PUBLIC_FORECAST_INDEX.json`, `OUTCOME_PROTOCOL.md`, and `verify_public_release.py`: all textual contents matched their separately retained local originals.

## What has NOT been established

- No qualified RFC3161 certificate, independent trusted timestamping service, external multi-party attestation or full historical raw source HTML archive.
- GitHub server PR timestamp witnesses public publication, not the execution or Stage-1-to-final order inside any earlier participant archive.
- No participant identity independence proof; A and B share a model family, use different selected events and sources, and C had exposure to prior forecasts.
- No result has been checked against future events. No forecasting skill, general method superiority or causal effect established.
- Source authenticity beyond the preservation and separate source references remains unverified except where documented.
- No current-standing admission or merge into `main`; draft PR is intentionally review-only.

## Governing correction

The previously reported apparent contradictory order of A and B messages was an examiner mistake: the app timestamps were completion times, not dispatch times. Preserve both `FPCF_002_TEMPORAL_DISCREPANCY_PREDECESSOR.md` and the explicit `FPCF_002_TEMPORAL_CORRECTION_SUCCESSOR.md` inside the archive. A occurred before B under clarified timing semantics. The exact 1,800-second Stage-1 offset remains an archive observation of unresolved cause.

## Future event resolution

Resolution documents, critique, dissent, and scoring must be additive successors referencing this exact bundle digest and relevant original case records. Do not edit or overwrite original forecasts or manufacture retrospective method reasoning. The public outcome protocol provides required minimum fields. No automatic ongoing monitoring has been initiated by this receipt.