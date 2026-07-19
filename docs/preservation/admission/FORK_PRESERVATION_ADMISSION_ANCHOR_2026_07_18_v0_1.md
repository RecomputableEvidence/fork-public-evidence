# Fork Preservation Admission Anchor — 2026-07-18 v0.1

Status: `PROPOSED_APPEND_ONLY_ADMISSION`

This record proposes an attributable, append-only admission of PRs #61, #62, #64, and #63 into `preservation/clean-continuance-v0.1`. It records exact reviewed heads, merge commits, successful head-commit workflow runs, Mac McFall / M87's exterior-review standing, the four unchanged source enclosures, and the two bounded residual observations.

The machine-readable anchor is `FORK_PRESERVATION_ADMISSION_ANCHOR_2026_07_18_v0_1.json`.

## Exact merge lineage

| PR | Reviewed or proposed head | Merge commit | Standing if this anchor is admitted |
|---|---|---|---|
| #61 | `cf878ee8c9d1c50af17a83937ecf1bd6bf043db9` | `86adf1a8a0f3a27b696777e5c340d27604df2397` | admitted preservation record |
| #62 | `1102113556edfc54b43a328317961c4896d6dd6c` | `599d3e193d86a9661fbbec3213ae1921b4959f10` | admitted claim-admission control |
| #64 | `d911ad5c33e0ec32037414effa7749326983d5ff` | `528f4306acf75b9b4e349aaf191fcda2c1c1430b` | admitted verification surface |
| #63 | `82c34252d7b8d9e8957fb5a86500e12da6cf363a` | `1ab4316b5de6100674695912a077b168cc36651b` | admitted pre-execution amendment; execution blocked |

PR #63's merge commit has PR #64's merge as first parent and the exact reviewed PR #63 head as second parent. The only conflict resolution regenerated the claim-admission self-check receipt against the combined tree. The reviewed head was not rebased or rewritten.

## Exterior-review standing

Mac's PR #64 disposition is `REPRODUCED_WITHIN_DECLARED_SCOPE`; all seven requested PR #63 review items are supported. The four direct-transmission enclosures are preserved byte-for-byte under `docs/verification/exterior-reviews/M87_PR63_PR64_2026_07_18/source/` and bound by `SHA256SUMS`.

This evidence is independent recomputation and bounded exterior review only. It is not GitHub-native approval, merge authority, security certification, endorsement, or Pair-001 execution authority.

## Residuals

Two non-blocking observations remain distinguishable and were addressed prospectively by successor PR #68, reviewed at head `ce8c0815d3a332224c6072ac5e567dffbee5f4c7` and merged as `a82c4fdc16b4cc7f10df396458b1a1d0ff9fc1f3`:

1. non-execution fields were declared literals rather than derived from an operation record;
2. a contradictory declared readiness status was normalized rather than explicitly reported.

Their preservation here does not convert PR #68 into exterior review or include it in this anchor's PR #61–#64 admission set.

## Current-state projection

At preservation commit `a82c4fdc16b4cc7f10df396458b1a1d0ff9fc1f3`, Pair-001 remains `STRUCTURALLY_READY_EXECUTION_BLOCKED`, `executable=false`, and provider calls remain zero. The instrumentation release anchor is not published, and provider identity, credential scope, quota, and receipt-path validation are not satisfied.

This projection does not rewrite the original Pair-001 attempts or any historical record.

## Non-claims

This anchor does not certify security, compliance, legality, truth, production readiness, or endorsement. It does not publish the instrumentation release anchor, validate provider access, authorize Pair-001 execution, or transfer authority from verification, review, merge, or admission.
