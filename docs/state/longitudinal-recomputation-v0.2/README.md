# Fork Longitudinal Recomputation Replay v0.2

**Standing:** `RESEARCH_CANDIDATE_NOT_ADMITTED`
**Exact base:** `f955834681d2f2ee257276acbf68afde0ae0e69d`

## Purpose

This candidate treats a committed state projection as a cache rather than as
the authority for its own conclusions. The checker rebuilds an eight-dimension
standing vector from:

1. an exact predecessor coordinate;
2. every commit in a bounded Git ancestry-path interval;
3. normalized, evidence-bound event classifications;
4. the deterministic Fork Sequence Surface reducer; and
5. explicit non-effects for admission, authority, and execution.

The first endogenous replay covers the transition from PR #90's independently
reviewed implementation head `bac40d9b...` to the later preservation head
`f955834...`. It preserves the distinction:

- `bac40d9b...` was independently recomputed within the review's declared
  scope;
- `f955834...` preserves that review and has different artifact bytes;
- the review standing does not silently inherit to `f955834...`.

## Commands

Install the repository's hash-locked proof-surface environment:

```bash
python -m pip install --require-hashes -r requirements-proof-surface.lock.txt
```

Then run:

```bash
python tools/check_longitudinal_recomputation_v0_2.py --json
python tools/check_longitudinal_recomputation_v0_2.py --derive-projection
python tools/check_longitudinal_recomputation_v0_2.py \
  --as-of bac40d9bdbd7f6b4927a676fef8def70756ad9d5
python tools/check_longitudinal_recomputation_v0_2.py \
  --diff-from bac40d9bdbd7f6b4927a676fef8def70756ad9d5 \
  --diff-to f955834681d2f2ee257276acbf68afde0ae0e69d
python -m pytest tests/test_longitudinal_recomputation_v0_2.py -q
```

`--write-derived` mechanically regenerates the projection cache, bounded
coverage receipt, standing-transition receipt, and package manifest. It is a
maintainer command, not a standing transition.

The successor candidate also mechanically refreshes the claim-admission
self-check receipt after all intended paths are staged. The predecessor
mismatch and non-effects are preserved in
`CLAIM_ADMISSION_RECEIPT_RECOMPUTATION_v0_1.md`.

## Result vocabulary

- `LONGITUDINAL_STATE_REPRODUCED`
- `PROJECTION_REDUCER_DIVERGENCE`
- `EVENT_COVERAGE_UNRESOLVED`
- `CURRENT_HEAD_REVIEW_STALE`
- `CONCURRENT_SUCCESSOR_UNRECONCILED`
- `AUTHORITY_EXPIRED_OR_REVOKED`

See `NON_CLAIMS_AND_LIMITS_v0_2.md` for the proof boundary.
