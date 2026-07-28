# PR #98 TP-001 append-only admission-anchor candidate

This directory is a separate candidate that follows merge commit `1d6350cd4545e873078e8c088da608416dee3802`.

It binds:

- the exact reviewed PR head `aa07846cdea30ab06ee8c56cbf72946fc9266bca`;
- the actual PR #98 merge commit and ordered parents;
- merge-tree content identity to the reviewed head by an empty file-delta comparison;
- the three successful exact-head workflow runs;
- the absence of post-merge runs observed through the available connector query;
- the initial green head and five append-only correction commits;
- the public/restricted evidence boundary and public surface digests;
- all explicit non-claims.

Current standing:

`APPEND_ONLY_ADMISSION_ANCHOR_CANDIDATE_NOT_ADMITTED`

This candidate does not self-authorize and must remain separate from PR #98's merge. Its eventual merge requires a separate explicit authorization after exact-head CI and bounded review.
