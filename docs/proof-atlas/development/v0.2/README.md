# Fork Proof Portfolio Sequence v0.2

## Purpose

This successor control surface updates the historical v0.1 proof-portfolio sequence to the current governed preservation coordinate after admission of the Shayne PR #64 exterior-evidence successor.

It separates **source-evidence standing** from **proof-packaging standing**. Evidence admitted for a proposed proof does not finish, admit, publish, or operationalize that proof.

## Exact basis

- governed branch: `preservation/clean-continuance-v0.1`
- exact construction base: `8f17d3de2d22e9dcb1f49c3813926d6166bc1bb8`
- historical predecessor candidate: PR #106 at `1038be6cf56d2b6ed74d2bee888c38cdd6fd0f92`
- admitted exterior-evidence successor: PR #118 merge `8f17d3de2d22e9dcb1f49c3813926d6166bc1bb8`

## Current sequence

1. **PROOF-001 — A Review Does Not Silently Travel** — existing governed surface remains unchanged by v0.2.
2. **PROOF-002 — Correction Does Not Erase Failure** — corrected PR #65 head still requires independent exact-head exterior recomputation.
3. **PROOF-003 — Independent Recomputation Has Temporal Boundaries** — Shayne exterior source evidence is admitted through PR #118; proof packaging remains not admitted.
4. **PROOF-004 — Evidence Can Cross Systems Without Authority Transfer** — GHCH PR #100 remains a deterministic simulation candidate pending exact-head exterior recomputation; no live adapters are authorized.
5. **PROOF-005 — Conversational Authority Drift Is Detectable** — PR #84/#86 source-grounding, correction, dependency, and exterior-review gates remain unresolved.
6. **PROOF-006 — Cross-Model Reconstruction Preserves or Degrades Declared Structure** — preregistration/offline research only; provider calls and live execution remain closed.

## Standing boundary

Candidate Model v0.1 remains `PROVISIONAL_RESEARCH_BASELINE`. Corpus cases admitted remain `0`. Empirical validation and independent model validation remain `NOT_ESTABLISHED`.

No v0.2 portfolio record may use CI success, review, source-PR merge, market relevance, preregistration, or admitted source evidence as automatic proof admission, authority, endorsement, execution permission, or production standing.

## Verification

```bash
python tools/check_proof_portfolio_sequence_v0_2.py --json
python -m pytest -q tests/test_proof_portfolio_sequence_v0_2.py
```

## Non-effects

This successor does not execute any experiment, call any provider, admit a corpus case, finish a proposed proof, reopen PROOF-001, authorize a pilot or production use, change model standing, or transfer institutional authority.
