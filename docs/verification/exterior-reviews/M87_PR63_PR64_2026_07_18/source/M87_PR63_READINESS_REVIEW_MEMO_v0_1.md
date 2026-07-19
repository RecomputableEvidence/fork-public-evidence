# M87 Review Memo — PR #63 (CSH v0.1.2 Pre-Execution Readiness)

**Reviewer:** Mac McFall / M87 (exterior review; execution-incapable)
**Date:** 18 July 2026
**Proof basis:** UPLOADED_ARTIFACT (checked out and executed the exact candidate head; ran fail-closed mutations)
**Standing:** Adverse-findings-preserved review. No bounded disposition token was requested for PR #63; this memo records findings only. Not merge authority, not endorsement, not authorization to execute Pair-001.

---

## Subject

| Field | Value |
|---|---|
| Pull request | #63 |
| Candidate head (verified) | `82c34252d7b8d9e8957fb5a86500e12da6cf363a` |
| Base | `preservation/clean-continuance-v0.1` @ `599d3e19…` |
| Readiness checker | `tools/check_csh_pre_execution_readiness_v0_1_2.py` |
| Observed state | `STRUCTURALLY_READY_EXECUTION_BLOCKED` (12/12 checks, `executable=false`, `provider_calls_performed=0`) |

## Seven-point checklist

| # | Item | Finding | Evidence |
|---|---|---|---|
| 1 | Predecessor/successor workflow lineage preserved and independently inspectable | SUPPORTED | `CSH-AMEND-003/CSH-AMEND-003_v0_1_2.{json,md}` present; predecessor bytes archived outside `.github/workflows`; successors bound to predecessor SHA-256 / blob / source commit per PR body and lineage records. |
| 2 | Hardened workflows semantically separate from frozen scientific inputs | SUPPORTED | Binding separates `bound_hypothesis` / `design` (frozen: 108 units in 54 fixed pairs, hypothesis `E[U\|H=1] < E[U\|H=0]`) from the hardened successor workflows; the `frozen_design_and_order` and `immutable_input_digests` checks pass. |
| 3 | Readiness checker fails closed under missing or altered prerequisites | SUPPORTED (proven) | Removing a required surface file → `PRE_EXECUTION_BINDING_FAILED`, `structural_ok=false`, exit 1. Forcing the binding `status` field to `READY_FOR_EXECUTION` had **no effect**: the checker recomputes state and held `STRUCTURALLY_READY_EXECUTION_BLOCKED`, `executable=false`. |
| 4 | Release-anchor and provider-validation prerequisites cannot be bypassed or inferred | SUPPORTED | `executable = all_prerequisites AND anchor_published AND execution_permitted`. All five prerequisites are `satisfied:false`, `provider_execution_permitted:false`; none can be forged in-repo. Executability requires external facts (PR #61/#62 admitted, release anchor published, provider validated). |
| 5 | Original Pair-001 attempts preserved rather than retrospectively conformed | SUPPORTED | `affected_pair_001`: `originals_immutable:true`, `originals_replaced:false`, `originals_superseded:false`; `receipts/baseline/pair-001` retained. |
| 6 | Required new repetitions properly linked without rewriting the originals | SUPPORTED | `repeat_count_required:2`, `repeat_ids_must_be_new:true`, `repeat_exact_request_bytes_must_match_original:true`. New repetitions are lineage-linked, not overwrites. |
| 7 | No language or mechanism promotes structural readiness into execution authority | SUPPORTED | State is `STRUCTURALLY_READY_EXECUTION_BLOCKED`; `provider_calls_performed_by_this_stage:0`; `--require-executable` returns non-zero while blocked. Structural readiness and execution authority are held distinct. |

Relevant suites: 89 passed (readiness / lineage / csh / pre-execution / preservation).

## One bounded observation (non-blocking)

The readiness checker recomputes execution state from the prerequisite set and ignores the binding's self-declared `status` field — which is the correct fail-closed behavior for the execution boundary. However, when I mutated that `status` field to `READY_FOR_EXECUTION`, the checker overrode it silently and did **not** raise a failed check for the tampered field. The execution decision is unaffected (it derives from prerequisites, not the field), and that file's integrity is bound elsewhere (it is one of the 20 changed paths whose Git-blob identity is checked by the PR #64 verification surface). Still, at the readiness-checker layer alone, a tampered `status` value is silently normalized rather than flagged. Suggested future micro-hardening: emit a contradiction when the declared `status` disagrees with the recomputed state. This does not change any checklist finding.

## Summary

All seven review items are SUPPORTED. The pre-execution boundary is fail-closed and cannot be flipped to executable by in-repo edits; Pair-001 lineage and frozen scientific inputs are preserved; no readiness-to-execution promotion is present. Adverse finding preserved: the one bounded, non-blocking status-field observation above. No contradiction, omitted dependency, path-scope defect, or evidence gap was found that would make the candidate not independently reproducible within the declared readiness scope.
