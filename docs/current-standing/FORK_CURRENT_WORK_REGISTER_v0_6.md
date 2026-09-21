# Fork Current Standing — v0.6

**Snapshot date:** 2026-09-21  
**Base commit:** `38f7a278211fca62b02fb3ee2cec26814e9ed9b6`  
**PRs:** [#158](https://github.com/RecomputableEvidence/fork-public-evidence/pull/158) (reconciliation + anchor), [#159](https://github.com/RecomputableEvidence/fork-public-evidence/pull/159) (repetition outcomes)  
**Form:** Predecessor-plus-delta; [v0.5 predecessor](FORK_CURRENT_WORK_REGISTER_v0_5.json) unchanged  

## Delta: CSH v0.1

**Material state:** `FROZEN_BASELINE_WITH_ORIGINAL_ATTEMPTS_REPETITIONS_ATTEMPTED_RECEIVER_RETIRED`  
**Research state:** `BASELINE_BLOCKED_RECEIVER_PLATFORM_RETIRED`  
**Gate:** `BLOCKED_RECEIVER_RETIRED` — continue_frozen_baseline = false

### What happened

| Event | Commit/PR | Time |
|---|---|---|
| Reconciliation patch + anchor published | PR #158 → `56c73f0b` | 2026-09-21T17:09:25Z |
| Both required CI workflows green on anchor commit | runs 35630191369, 35630191332 | 2026-09-21T17:09:25Z |
| Repetition CSH-RUN-001-RPT executed | — | 2026-09-21T17:15:30Z UTC |
| Repetition CSH-RUN-002-RPT executed | — | 2026-09-21T17:15:40Z UTC |
| Repetition outcomes published | PR #159 → `38f7a278` | 2026-09-21T17:27:31Z |

### Repetition outcomes

Both `CSH-RUN-001-RPT-20260921171515-R01` (linked CSH-RUN-001, control_h0) and `CSH-RUN-002-RPT-20260921171515-R01` (linked CSH-RUN-002, instrumented_h1) returned **HTTP 410** with body:

```
{"error":{"code":"github_models_retirement_brownout","message":"GitHub Models is temporarily unavailable as part of a scheduled retirement brownout."}}
```

The "temporarily unavailable" wording conflicts with GitHub's official retirement notice (2026-07-30). The platform is documented as retired, not temporarily suspended.

**No model output was received. No classifiable pair. No comparative result.**

### Platform retirement

GitHub Models (endpoint `https://models.github.ai/inference/chat/completions`) retired 2026-07-30 per the GitHub changelog. Both frozen receiver classes use this endpoint. 72 of 108 run-order units are affected. The 36 deterministic-receiver units are not affected.

### Baseline population (108 units)

| Category | Count |
|---|---|
| Original attempts with terminal dispositions | 2 (CSH-RUN-001: HTTP 200, CSH-RUN-002: HTTP 429) |
| Repetition attempts (HTTP 410, both exhausted) | 2 |
| Units with terminal dispositions total | 4 |
| Units not executed (ordinals 3–108) | 106 |
| Units dependent on retired GitHub Models endpoint | 72 |
| Deterministic receiver units (not retired-platform-dependent) | 36 |

The protocol does not contain an explicit provision for declaring the 106 unattempted units as terminated by platform retirement without individual execution. This remains an **unresolved adjudication question** pending receiver-migration authorization.

### Next gate

Reviewer authorization of the CSH-AMEND-004 receiver-migration proposal; new receiver freeze; fresh repetition execution under the new receiver configuration.

See: [`FORK_CURRENT_WORK_REGISTER_v0_6.json`](FORK_CURRENT_WORK_REGISTER_v0_6.json)

---

*Predecessor objects (v0.1–v0.5 deltas) retain their last recorded standing without fresh verification in this overlay.*
