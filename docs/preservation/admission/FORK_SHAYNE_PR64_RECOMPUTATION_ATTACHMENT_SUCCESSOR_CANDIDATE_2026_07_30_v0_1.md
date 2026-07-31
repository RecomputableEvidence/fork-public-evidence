# Fork Shayne PR #64 recomputation attachment successor candidate — 2026-07-30 v0.1

Status: `PROPOSED_APPEND_ONLY_SUCCESSOR_ADMISSION`

Reviewer-declared disposition: `REPRODUCED_WITHIN_DECLARED_SCOPE`

This candidate succeeds, rather than rewrites, the initial Shayne transmission
candidate already present on draft PR #105. At the initial capture point, the
findings attachment was correctly recorded as `REFERENCED_NOT_RECEIVED`. The
later public release now supplies and digest-binds that attachment.

## Successor coordinates

- predecessor draft commit:
  `e245f86457ac9ed9d4e52c76edc5c395970492d9`;
- predecessor tree:
  `21ea6ba69b09925f37d816258a538fc80e2f564c`;
- release:
  `Icon369/verdict-evidence-transfers@pr63-pr64-ivs-v0_1_1`;
- exact release asset SHA-256:
  `1ccf11595fcc88b1bab187f2dd301a04e123e02ba92867e90491b619b0a11d2d`;
- reviewed PR #64 head:
  `d911ad5c33e0ec32037414effa7749326983d5ff`.

The reviewer-quoted digest, GitHub's release-asset digest, and a recipient-side
download digest are identical.

## Admission scope

If separately authorized and merged, the candidate would admit:

- the exact release ZIP;
- the exact findings memo;
- the exact surviving raw artifacts;
- the upstream checksum manifest;
- direct inspection copies of every regular archive member;
- the successor adjudication and its precision corrections.

It would not admit a complete raw execution transcript. The original
fresh-runner JSON stdout was not captured, the memo's account is a
transcription, the command table is abbreviated, and the environment record is
explicitly assembly-time rather than run-time. Those boundaries remain
visible.

The raw plan comparison also establishes that the stated one-character
candidate-SHA change appears at six redundant byte positions. The fail-closed
output remains adverse and the reported process exit code remains 2; the
literal “single-byte” wording is narrowed without weakening the result.

## Continuing standing

The initial `REFERENCED_NOT_RECEIVED` state remains historically valid and is
not overwritten. The successor state is
`EXACT_RELEASE_ATTACHMENT_RECEIVED_AND_VERIFIED_WITH_INTERNAL_CAPTURE_GAP`.

PR #63 remains `STRUCTURALLY_READY_EXECUTION_BLOCKED`. Opening this candidate,
passing checks, or later merging it does not create endorsement, approval,
execution permission, Pair-001 authorization, certification, or authority
transfer. Merge requires separate explicit authorization.
