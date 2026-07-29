# PR #101 Proof 001 Admission Anchor

This append-only candidate binds the merge of PR #101 into
`preservation/clean-continuance-v0.1`.

## Exact coordinates

- pre-merge base: `96e17cd5ae8a923b9074cfdfe6718cf0e15611b0`
- reviewed PR head: `a273ab0a95decb0d43f1c091743a72ac4261027e`
- merge commit: `ded38bf56f950b8813614132c92bf531553a8b34`
- expected ordered parents: pre-merge base first, reviewed head second
- reviewed-head-to-merge file delta: `0`

## Standing

The merge admits the **Proof 001 packaging surface**. It does not widen the
underlying PR #91 exterior disposition, which remains
`REPRODUCED_WITH_CORRECTION_REQUIRED`.

Review remains exact-head bound. No review standing is inherited by the merge
commit merely because its tree content is identical to the reviewed head.

The public-route observation remains `PUBLIC_ROUTE_STALE` until a separately
constructed and admitted routing successor changes that state.

## Recompute

```bash
python tools/check_pr101_proof001_admission_anchor_v0_1.py
pytest -q tests/test_pr101_proof001_admission_anchor_v0_1.py
```

Expected candidate result:

`PR101_PROOF001_ADMISSION_ANCHOR_CANDIDATE_CONFORMS_NOT_ADMITTED`

## Boundary

This anchor is itself a candidate until separately reviewed and admitted. It
does not change `main`, repository settings, Pages, authority, execution,
provider calls, Pair-001, or existing pull-request standing.
