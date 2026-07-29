# PROOF-001 — A Review Does Not Silently Travel

**Packaging standing:**
`BOUNDED_NONSEMANTIC_PACKAGING_CANDIDATE_NOT_ADMITTED`

## Plain-language failure

A later artifact must not inherit review standing merely because it preserves
the earlier review record.

## One-command recomputation

Install the repository's hash-locked proof-surface environment:

```bash
python -m pip install --require-hashes -r requirements-proof-surface.lock.txt
```

Then run from the repository root:

```bash
python tools/run_proof_001_review_does_not_silently_travel_v0_1.py
```

The wrapper invokes the existing v0.2 longitudinal checker, derives the
changed/preserved table, executes the `CURRENT_HEAD_REVIEW_STALE` mutation,
checks the package bindings, and reports the separately preserved public-route
freshness result.

Machine-readable output:

```bash
python tools/run_proof_001_review_does_not_silently_travel_v0_1.py --json
```

## Exact lineage

| Role | Coordinate or standing |
|---|---|
| Replay start | `bac40d9bdbd7f6b4927a676fef8def70756ad9d5` |
| Replay closure | `f955834681d2f2ee257276acbf68afde0ae0e69d` |
| PR #91 reviewed head | `e848ea0825bafc1aa3754d89e719d71b5a9f3982` |
| PR #91 reviewed tree | `0b5f11eb6c1cd8c90b4cacce2a747045da917741` |
| PR #91 exterior result | `REPRODUCED_WITH_CORRECTION_REQUIRED` |
| Clean exterior suite | `726 passed, 3 skipped` |
| PR #97 later admission merge | `9c779c305be8455f355051a561e9ea89e7feee36` |
| Construction base | `96e17cd5ae8a923b9074cfdfe6718cf0e15611b0` |

The replay interval itself has admission effect `NONE`. PR #97 later admitted
the longitudinal lineage with the correction-required return retained. The
later admission does not rewrite the earlier interval.

## Generated summary

`PROOF-SUMMARY.md` is rendered from the existing v0.2 checker output. The
wrapper fails if the committed summary differs from a fresh derivation.

## Public-route finding

The package also records `PUBLIC_ROUTE_STALE` against the exact admitted
checkpoint configured in `PUBLIC-ROUTE-FRESHNESS-CONTRACT.json`.

Run:

```bash
python tools/check_public_route_freshness_v0_1.py --json
```

This is preserved negative evidence. The candidate does not modify the root
README, state routing, `main`, default-branch settings, Pages, existing pull
requests, repository settings, or authority state.

## Boundary

A pass proves only that the bound replay, changed/preserved dimensions,
adversarial rejection, package bindings, and declared route comparison were
recomputed as specified.

It does not establish global event completeness, truth, correctness,
causality, endorsement, compliance, legal sufficiency, safety, production
readiness, present reliance, institutional authority, or execution permission.
