# FPCF-002 public forecast archive — change-accounting repair v0.1

**Status:** ADDITIVE_CHANGE_ACCOUNTING_IN_FLIGHT. **Subject:** public draft PR #201, `docs/experiments/FPCF-002/public-release/`.

## What happened
CI runs triggered after PR #201 was opened reported six failed jobs. Four failed the standing freshness/change-accounting check directly, and both Python regression jobs failed solely at `tests/test_standing_freshness_v0_1.py::test_current_specimen_and_standing_verify`. Linux reported 772 passing tests and one failed; Windows likewise 772 passing and one failed. The failure identified twelve newly added recognized paths that were absent from the active `PROGRAM_CHANGE_ACCOUNTING_v0_2.json` ledger.

These are *real accounting failures*, not evidence that the archive records are false or that the original forecast results are wrong. Do not reclassify the paths to avoid recognized scope. This record accounts for the twelve effective path introductions in the GitHub PR synthetic merge first-parent snapshot as `IN_FLIGHT`.

## Evidence coordinates
- Original public PR: https://github.com/RecomputableEvidence/fork-public-evidence/pull/201
- Initial observed head: `4be513ddd26ef9557024ab091df602d4b946b834`
- GitHub CI run group: proof surface 40434819813; standing 40434819848; admission 40434819776; CSH 40434819767.
- Public archive and its original rationale/returns remain unchanged.
- The part 10 publishing transport contained a duplicated 44-character final line at an intermediate commit. The successor corrected it at `8851ff521717916f9e912ac48242e76ea42342a2`. Its preservation and public readback are described under `docs/experiments/FPCF-002/public-release/PUBLICATION_READBACK_v0_1.md`.
- CI checks out `refs/pull/201/merge`, whose first-parent history presents the **twelve effective additions** from the mainline base. The PR development branch records additional intermediate part-10 creation/replacement transitions; these are visible in branch commit history, but are not independently enumerated by the first-parent merge-checker account. **Do not claim CI's active ledger exhaustively accounts for every development-branch transition.**

## Bounded dispositions
- The twelve recognized new paths are recorded as `IN_FLIGHT`, with exact Git blob identities. No research, forecast, prediction-skill, method-efficacy, legal, institutional, or production standing is conferred.
- Original 25 candidate forecasts and 18 A/B/C candidate forecasts remain historically preserved and unadmitted as predictive results.
- The participant decision chronology and causal benefit of Lens methods remain unestablished by file consistency or GitHub publication.
- Main current standing and the closed predecessor v0.1 accounting stay unchanged.
- Draft PR status remains the human admission boundary. CI success cannot authorize a merge, standing promotion, or forecast resolution.

## Independent review protocol
Re-run `python scripts/check_standing_freshness_v0_1.py --json` against the GitHub-generated PR merge checkout and run both Linux and Windows full regressions. For a direct-checkout of the PR development branch, separately inspect its first-parent history and note the intermediate part-10 replacement; that different traversal may not have the same active accounting population as the synthetic merge. Do not suppress a mismatch by changing the checker or removing the adversarial transition.

This is an account of actual paths, Git blobs, and limits. It is not an endorsement or release admission.
