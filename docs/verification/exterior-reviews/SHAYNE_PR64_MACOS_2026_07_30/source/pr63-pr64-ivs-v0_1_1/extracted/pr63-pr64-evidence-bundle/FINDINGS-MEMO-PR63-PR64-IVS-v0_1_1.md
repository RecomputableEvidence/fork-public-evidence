# Independent Recomputation — Findings Memo
## Fork PR #63 (CSH v0.1.2 pre-execution readiness) / PR #64 (Independent Verification Surface v0.1.1)

**Reviewer:** Shayne Beavan (independent; fresh clone; no prior run state)
**Date:** 2026-07-30
**Disposition:** **REPRODUCED_WITHIN_DECLARED_SCOPE**

---

## Environment
- macOS 15.7.7 (Darwin 24.6.0)
- Python 3.14.4 · git 2.39.5 (Apple Git-154) · pip 26.1
- Dependencies installed into a dedicated venv from the repository's own lock files with `--require-hashes`; both installs exited 0 with no resolution errors on Python 3.14. Resulting set includes jsonschema 4.26.0, pytest 8.4.2, PyYAML 6.0.3, referencing 0.37.0, rpds-py 2026.6.3.

## Exact subjects reviewed
- PR #64 review-package head: `d911ad5c33e0ec32037414effa7749326983d5ff` (checked out detached, verified via `git rev-parse HEAD`)
- PR #63 base `599d3e19…10`, candidate head `82c34252…3a`, both confirmed as commit objects via `git cat-file -t`
- **Merge base independently recomputed:** `git merge-base 599d3e19… 82c34252…` → `1102113556edfc54b43a328317961c4896d6dd6c`, **equal to the plan's expected_merge_base**

## Commands executed and results

| Step | Command (abbreviated) | Result |
|---|---|---|
| Fresh runner | `run_independent_verification_fresh_v0_1_1.py --repository … --package-commit d911ad5c… --plan … --expected-receipt …` | `FRESH_RECOMPUTATION_PASS`, `receipt_byte_exact: true`, `candidate_checkout: NONE`, `candidate_code_execution: NONE`, exit 0 |
| Direct checker | `check_independent_verification_surface_v0_1_1.py --plan … --write-receipt /tmp/…` | exit 0 |
| Receipt comparison | `cmp --silent /tmp/receipt receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json` | **BYTE-IDENTICAL** |
| Test suite | `pytest tests/test_independent_verification_surface_v0_1_1.py -q` | **8 passed** |
| Determinism | checker re-run under `PYTHONHASHSEED` ∈ {1, 2, 42, default} | identical receipt sha256 (`5baf0e04…`) across all four conditions, exit 0 each |
| Fail-closed probe | plan copy with one hex character of the candidate SHA altered | checker **exit 2** (non-zero; fails closed, does not emit a passing receipt) |

## Pressure checks (source-inspected or executed, not taken on the tool's word)

1. **Runner genuinely begins outside candidate state — supported.** Source inspection: the runner builds its workspace in `tempfile.TemporaryDirectory(prefix="fork-ivs-fresh-")` and fetches into it; it does not read my working copy. Output confirms `candidate_checkout: NONE`.
2. **Trusted lane reads objects, not checkouts — supported.** The hardened checker resolves content through `git cat-file`-style full-SHA object reads (e.g., `cat-file -e <source_commit>^{commit}`); no candidate checkout or candidate-code execution path found in the verification lane.
3. **Fail-closed behavior — supported by test, not assumption.** Single-byte plan tamper → exit 2. Verdict precedence in the plan is adverse-first (`INCONCLUSIVE_EVIDENCE_GAP` > `INVALIDATED_BY_RECOMPUTATION` > reproduced), which is the correct fail-closed ordering.
4. **Exit-code discipline — supported.** This checker family exits non-zero on failure. (Noted because the v0.2.1 mapping checker I reviewed in June printed CHECK_FAIL but exited 0; that defect is absent here.)
5. **PR #63 workflow lineage — supported by byte comparison over git objects only.** Both archived predecessor workflows (`cross-system-claim-handoff-v0-1.v0-1-1.yml.txt`, `fork-proof-surface-integration.v0-1-1.yml.txt` at the PR #63 head) are **byte-identical** to the corresponding `.github/workflows/*.yml` blobs at the expected merge base. The archive is a true copy, not a paraphrase.
6. **Structural readiness cannot promote to execution authority — supported at the vocabulary level.** The readiness checker's own success terminal state is `STRUCTURALLY_READY_EXECUTION_BLOCKED`; the failure state is `PRE_EXECUTION_BINDING_FAILED`. There is no terminal state that grants execution. The `fail_closed_execution_boundary` check records the boundary explicitly.
7. **PR #63 candidate tests — 5/5 pass.** `tests/test_csh_pre_execution_readiness_v0_1_2.py` executed **in my own sandbox, outside the trusted lane, and recorded as such** (candidate code was executed by me as reviewer, deliberately; the trusted lane itself executed none).

## Observations (not defects)

- **Changed-path inventory is implicit, not enumerated.** The plan binds the subject cryptographically at the commit level (base, candidate, expected merge base). A commit SHA transitively binds every path, so integrity coverage is complete; but the 20-file PR #63 diff inventory is not enumerated as a first-class plan assertion. I derived it independently (`git diff --name-only <merge-base> <head>` → 20 paths, including both workflow files, the CSH-AMEND-003 set, the pre-execution binding and release-anchor JSONs, both readiness tools, and both test files). A reviewer who wants the human-scope view must compute it, as I did. Worth considering enumerating it (or a diff digest) in future plan versions purely for reviewer ergonomics.
- **External observations accepted as recorded, not re-verified live.** The plan's `external_observations` (PR state snapshot, two GitHub Actions run states) are labeled `OBSERVATION_ONLY` and I treated them exactly that way; I did not re-query the GitHub API to confirm the recorded snapshots. This is a declared-scope boundary, not a gap.

## Contradictions / evidence gaps
None found. No assertion I exercised should be reclassified as contradicted or inconclusive.

## Platform deviations
None required. The published procedure ran unmodified on macOS 15.7.7 / Python 3.14.4, including both `--require-hashes` installs.

## Limitations on the conclusion
- Single platform, single Python minor version. I did not exercise locale, line-ending, exotic-filesystem, or temporary-directory variations beyond the hash-seed conditions above.
- Byte-identity of the receipt was verified against the committed receipt at the reviewed head; I make no claim about other branches or later commits.
- This review is not endorsement, approval, security certification, merge authority, or authorization to execute Pair-001, and must not be represented as any of those.

**Disposition: REPRODUCED_WITHIN_DECLARED_SCOPE.**
