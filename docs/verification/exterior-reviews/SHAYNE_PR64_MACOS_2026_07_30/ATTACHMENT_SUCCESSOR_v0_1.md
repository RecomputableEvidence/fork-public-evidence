# Shayne PR #63 / PR #64 release attachment successor — 2026-07-30

Status: `PROPOSED_APPEND_ONLY_ATTACHMENT_SUCCESSOR_RECEIPT`

Reviewer-declared disposition: `REPRODUCED_WITHIN_DECLARED_SCOPE`

The initial transmission record remains unchanged and historically valid: at
that capture point, the referenced findings attachment had not been received.
This successor records its later arrival from the public GitHub release
[`Icon369/verdict-evidence-transfers@pr63-pr64-ivs-v0_1_1`](https://github.com/Icon369/verdict-evidence-transfers/releases/tag/pr63-pr64-ivs-v0_1_1).

## Exact release binding

| Coordinate | Value |
|---|---|
| Release asset | `pr63-pr64-evidence-bundle.zip` |
| Bytes | `16,901` |
| Reviewer-quoted SHA-256 | `1ccf11595fcc88b1bab187f2dd301a04e123e02ba92867e90491b619b0a11d2d` |
| GitHub asset digest | `sha256:1ccf11595fcc88b1bab187f2dd301a04e123e02ba92867e90491b619b0a11d2d` |
| Recipient-computed SHA-256 | `1ccf11595fcc88b1bab187f2dd301a04e123e02ba92867e90491b619b0a11d2d` |
| Release tag target | `c9ddbe6f81dd06a719cd0c72da7a38d242e8b362` |

The archive passes its integrity test, contains no duplicate or unsafe member
paths, and is preserved byte-for-byte. Its 12 regular files are also retained
as direct inspection copies. Git does not preserve filesystem modification
time semantics for those copies; the exact ZIP bytes retain the upstream
timestamp metadata.

## What the bundle establishes directly

- The exact findings memo is now present and digest-bound.
- The upstream `SHA256SUMS.txt` entries all verify.
- The direct receipt, checker stdout capture, and three seed receipts are five
  byte-identical 2,380-byte files with SHA-256
  `5baf0e04e06e7bc69efa91ec35dbc5605d6594fcff5830fe02117a300d7fd083`.
- The independently produced 20-path inventory is byte-identical to a new
  recipient-side `git diff --name-only` recomputation.
- The tampered plan and adverse checker output are preserved as exact bytes.

The changed-path inventory is therefore first-class and digest-bound in this
successor evidence package. That improves direct inspectability; it does not
retroactively alter the PR #64 plan schema or imply an earlier integrity gap.

## Preserved gaps and precision corrections

The bundle note states that the fresh runner's JSON stdout was not redirected
at run time. Its original bytes do not exist in the bundle, the memo account is
a transcription, and no rerun was used to manufacture a replacement. That gap
remains `PRESERVED_NOT_REPAIRED`.

The memo abbreviates command lines rather than supplying a full shell
transcript. The surviving raw artifacts are exact, but the bundle is not
represented as a complete raw stdout, stderr, and machine exit-code capture
for every reported step. The environment record is explicitly labeled as
generated at bundle-assembly time on the attributed same host and session.

Raw comparison also narrows the phrase “single-byte tamper.” The semantic
change is one candidate-SHA nibble (`a` to `b`) propagated across six redundant
plan coordinates, producing six changed file bytes. The checker output remains
adverse (`INCONCLUSIVE_EVIDENCE_GAP`), and the memo plus bundle note report
process exit code 2. No separate machine exit-code file is present. This
precision correction does not weaken the fail-closed result.

## Continuing boundary

The public release corroborates the transfer outcome; it does not authenticate
the reviewer's identity or reconstruct a complete local shell transcript.
PR #63 remains `STRUCTURALLY_READY_EXECUTION_BLOCKED`. This successor grants no
endorsement, merge authority, GitHub-native approval, execution authorization,
Pair-001 permission, universality claim, certification, or authority transfer.

Recompute the preservation surface with:

```bash
python tools/check_shayne_pr63_pr64_attachment_successor_v0_1.py
```

Expected result:
`SHAYNE_PR63_PR64_ATTACHMENT_SUCCESSOR_CONFORMS_NOT_ADMITTED`.
