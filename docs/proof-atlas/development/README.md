# Fork Proof Portfolio Development

**Standing:** `DEVELOPMENT_CONTROL_SURFACE_CANDIDATE_NOT_ADMITTED`

This directory defines the proposed sequence through which bounded source
lineages may later become finished Fork proof surfaces.

Start with:

1. `FORK_PROOF_PORTFOLIO_SEQUENCE_v0_1.md`
2. `PROOF_PORTFOLIO_REGISTRY_v0_1.json`
3. `PROOF_PORTFOLIO_PROMOTION_CONTRACT_v0_1.json`

The current public Proof Atlas and `PROOF_INDEX_v0_1.json` remain unchanged.
Nothing in this directory adds Proofs 002–006 to the public index, finishes a
proof, admits a source pull request, transfers exterior-review standing,
authorizes execution, or establishes commercial readiness.

The sequence keeps three dimensions separate:

- scientific or technical standing;
- institutional utility;
- commercial relevance.

A candidate may be relevant in one dimension without acquiring standing in
another.

Recompute the control surface:

```bash
python tools/check_proof_portfolio_sequence_v0_1.py
pytest -q tests/test_proof_portfolio_sequence_v0_1.py
```

Expected candidate result:

`PROOF_PORTFOLIO_SEQUENCE_CANDIDATE_CONFORMS_NOT_ADMITTED`
