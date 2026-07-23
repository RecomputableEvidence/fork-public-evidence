# Narrow Successor Review Instructions v0.1

## Review object

Review only the preservation delta added after reviewed PR #90 head
`bac40d9bdbd7f6b4927a676fef8def70756ad9d5`. Do not repeat the full conceptual
review unless implementation outside this package changes.

## Required checks

1. Confirm the preserved review differs from the transmitted Sections 5–7 only by replacing both `1241c008…e296` table abbreviations with `1241c008…b4a7`.
2. Confirm the correction note classifies the change as editorial and assigns no substantive-review effect.
3. Run `python tools/check_exterior_review_pr89_pr90_v0_1.py --json`.
4. Recompute all manifest SHA-256 digests and byte sizes.
5. Recompute the receipt payload digest according to its declared canonicalization rule.
6. Confirm PR #89 still resolves to `b93f9a1bce094e8c65e0d1ef04dbe52a11aab0b1`.
7. Confirm the reviewed PR #90 object remains bound to head `bac40d9bdbd7f6b4927a676fef8def70756ad9d5` and tree `aa8b1e5f47d2ca062588b8f50c58fa6014ee29ba`.
8. Confirm no package file claims admission, publication, merge authorization, authority transfer, execution authority, Pair-001 calls, or Pair-001 repetition.
9. Run the full relevant regression and preserve command output, exit status, environment, and dependency facts.

## Expected disposition boundary

A conforming narrow review establishes only accurate preservation and integrity of
the successor review package. It does not repeat or enlarge Claude's substantive
review, authenticate attribution, admit either candidate, authorize merge, or
confer execution authority.
