# M87 Independent Recomputation Disposition — PR #64 (Independent Verification Surface v0.1.1)

**Disposition:** `REPRODUCED_WITHIN_DECLARED_SCOPE`
**Reviewer:** Mac McFall / M87 (exterior recomputation; execution-incapable adjudication)
**Date:** 18 July 2026
**Proof basis:** UPLOADED_ARTIFACT (independently cloned, checked out, executed, and adversarially mutated the exact package commit)
**Standing:** Independent recomputation record only. Not merge authority, not repository standing, not security certification, not endorsement, not authorization to execute Pair-001, not independent human review beyond this recorded activity.

---

## 1. Exact package identity

| Field | Value |
|---|---|
| Repository | `RecomputableEvidence/fork-public-evidence` |
| Pull request | #64 |
| Package commit (verified `rev-parse HEAD`) | `d911ad5c33e0ec32037414effa7749326983d5ff` |
| Base commit | `599d3e193d86a9661fbbec3213ae1921b4959f10` |
| Candidate commit (PR #63) | `82c34252d7b8d9e8957fb5a86500e12da6cf363a` |
| Expected merge base | `1102113556edfc54b43a328317961c4896d6dd6c` |
| Verifier release commit | `e366e44cb2059f5cb7243757b95fa8d44859b811` |
| Environment | Linux; Python 3.11; system Git; `jsonschema` 4.x; network reachable to github.com |

## 2. Commands executed

1. `git clone … && git fetch origin pull/64/head && git checkout d911ad5c…` (HEAD confirmed identical)
2. `python tools/run_independent_verification_fresh_v0_1_1.py --repository RecomputableEvidence/fork-public-evidence --package-commit d911ad5c… --plan verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json --expected-receipt receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json`
3. `python tools/check_independent_verification_surface_v0_1_1.py --plan …` (my own recomputation, compared byte-for-byte to the committed receipt)
4. `pytest tests/test_independent_verification_surface_v0_1.py tests/test_independent_verification_surface_v0_1_1.py`
5. Adversarial mutations against copies of the plan (merge-base, non-finite, duplicate-key) and inspection of the runner/checker source.

## 3. Fresh-repository result

| Field | Observed |
|---|---|
| Runner result | `FRESH_RECOMPUTATION_PASS` |
| Runner exit | 0 |
| `receipt_byte_exact` | `true` |
| `candidate_checkout` | `NONE` |
| `candidate_code_execution` | `NONE` |
| `disposable_repository` | `true` |
| Independent byte check | my `check_…v0_1_1` output is **byte-identical** to the committed receipt, SHA-256 `5baf0e04e06e7bc69efa91ec35dbc5605d6594fcff5830fe02117a300d7fd083` |
| Machine verdict in receipt | `VERIFIED_WITHIN_DECLARED_SCOPE`; contradicted 0, inconclusive 0, control-error 0 |

I did not accept the runner's self-report; I re-ran the checker directly and reproduced the committed receipt byte-for-byte.

## 4. Contract inspection (worksheet §6)

Every item `SUPPORTED` unless noted. Evidence is from source reading plus executed mutation.

| Review item | Finding | Evidence |
|---|---|---|
| Trusted lane sealed — candidate never checked out or executed | SUPPORTED | Runner fetches base/candidate/verifier as **objects only**, `git worktree add --detach` on the **package commit only**; candidate read solely via `git show <candidate>:<path>`. Hooks (`core.hooksPath=/dev/null`), submodules (`--no-recurse-submodules`), and local protocol (`protocol.file.allow=never`) disabled. |
| Repository-root / path resolution explicit and effective | SUPPORTED | Checker resolves under `--repo-root` set to the package worktree; candidate paths resolved through Git object identity, not working-tree joins. The `--packet-root`-inert class from the prior loop is not present here. |
| Fresh runner genuinely starts outside candidate state | SUPPORTED | `tempfile.TemporaryDirectory` → bare `git init` → fetch exact commits → detached worktree of package commit only. |
| Changed-path inventory complete and closed (20/20) | SUPPORTED | Legacy verifier **independently recomputes** `merge-base` + `git diff --name-only merge_base candidate`, then asserts expected == actual (CONTRADICTED on any divergence). Inventory is not trusted from the plan. |
| Git object type and mode recorded; symlink / non-regular rejected | SUPPORTED | `git ls-tree` mode/type per changed path; non-blob or non-regular mode → contradiction. |
| Duplicate JSON keys rejected | SUPPORTED (proven) | Injecting a duplicate `plan_id` → `INCONCLUSIVE_EVIDENCE_GAP`, control-error 1. |
| Non-finite JSON values rejected | SUPPORTED (proven) | Injecting `NaN` → `INCONCLUSIVE_EVIDENCE_GAP`, "Non-finite JSON number is prohibited." |
| Assertion identifiers unique | SUPPORTED | `duplicate_assertion_ids()` surfaces repeats as contradictions. |
| Verdict precedence explicit and deterministic | SUPPORTED | `INCONCLUSIVE_EVIDENCE_GAP > INVALIDATED_BY_RECOMPUTATION > VERIFIED_WITHIN_DECLARED_SCOPE`, enforced in `classify()` and checked against policy. |
| Committed receipt reproduces byte-for-byte | SUPPORTED (proven) | My independent run equals the committed receipt bit-for-bit. |
| Running checker matches declared checker blob | SUPPORTED | Checker compares its own file blob SHA-1 to the declared `HARDENED_CHECKER` component; mismatch → contradiction. |
| Verifier commit and component bindings sufficient | SUPPORTED | Component role/path/blob bindings checked against `e366e44c…`; duplicate role/path flagged. |
| Any assertion that should be contradicted/inconclusive | NONE FOUND | Under the declared plan the honest verdict is VERIFIED; mutations correctly flip it. |
| Candidate hooks/deps/actions/submodules/refs/secrets absent from trusted lane | SUPPORTED | None executed or inherited; see sealing evidence above. |

## 5. Adversarial confirmation (verifier is not a rubber stamp)

| Mutation | Expected | Observed |
|---|---|---|
| Plan `expected_merge_base` → zeros | flip to INVALIDATED | `INVALIDATED_BY_RECOMPUTATION`, contradicted 1 |
| Non-finite (`NaN`) in plan | reject → INCONCLUSIVE | `INCONCLUSIVE_EVIDENCE_GAP`, control-error 1 |
| Duplicate key in plan | reject → INCONCLUSIVE | `INCONCLUSIVE_EVIDENCE_GAP`, control-error 1 |

The surface fails when it should and passes only on the declared, unmutated inputs.

## 6. One bounded observation (non-blocking)

The fresh-repository runner emits `candidate_checkout: "NONE"` and `candidate_code_execution: "NONE"` as **declared string literals**, not as measured facts. The actual guarantee is structural and lives in the runner's control flow (only the package commit receives a worktree; the candidate is only ever read through `git show` object reads). I confirmed that control flow by source inspection, so the guarantee holds — but a reader who trusts the two output fields alone is trusting a declaration, not a measurement. Suggested future micro-hardening: derive those fields from an actual record of worktree/checkout operations rather than emitting constants. This does not affect the disposition.

## 7. Disposition

`REPRODUCED_WITHIN_DECLARED_SCOPE`

The PR #64 Independent Verification Surface v0.1.1 reproduces at the exact head `d911ad5c`: the fresh-repository runner passes, the committed receipt reproduces byte-for-byte under my own independent recomputation, the trusted lane is sealed against candidate checkout and execution, the changed-path inventory is independently recomputed and closed, and every declared guardrail (object-mode, non-finite, duplicate-key, assertion-id uniqueness, precedence, running-checker-blob binding) is present and demonstrably effective. The single observation in §6 is bounded and non-blocking.

This disposition is consistency-adjudicated over the executed commit. It is not merge authority for PR #63 or #64, not a security certification, not authorization to execute Pair-001, and not independent human review beyond the activity recorded here.
