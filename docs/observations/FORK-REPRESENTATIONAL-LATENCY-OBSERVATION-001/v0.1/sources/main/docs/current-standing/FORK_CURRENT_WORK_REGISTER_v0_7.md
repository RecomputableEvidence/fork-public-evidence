# Fork Current Standing — v0.7

**Snapshot date:** 2026-09-21  
**Base commit:** `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`  
**PR:** [#160](https://github.com/RecomputableEvidence/fork-public-evidence/pull/160) (post-execution reconciliation base) + this delta (corrections PR)  
**Form:** Predecessor-plus-delta; [v0.6 predecessor](FORK_CURRENT_WORK_REGISTER_v0_6.json) unchanged  

## Delta: CSH v0.1 — additive corrections

**Material state:** `FROZEN_BASELINE_WITH_ORIGINAL_ATTEMPTS_REPETITIONS_ATTEMPTED_RECEIVER_RETIRED`  
**Research state:** `BASELINE_BLOCKED_RECEIVER_PLATFORM_RETIRED`  
**Gate:** `BLOCKED_RECEIVER_RETIRED` — continue_frozen_baseline = false (unchanged)

### Corrections in this delta

| Correction | Subject | Binding document |
|---|---|---|
| `CSH-BASELINE-POPULATION-ACCOUNTING-CORRECTION-20260921-001` | Units vs. attempts accounting | `BASELINE_POPULATION_ACCOUNTING_20260921.json` (original preserved) |
| `CSH-PAIR001-ADJUDICATION-CHRONOLOGY-CORRECTION-20260921-001` | Anchor CI completed timestamp | `PAIR001_POST_EXECUTION_ADJUDICATION_20260921.json` (original preserved) |
| `CSH-AMEND-004-PROPOSAL-20260921-002` | Concrete migration research replacing skeleton | `CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json` (skeleton preserved) |

### Correction 1: Units vs. attempts

The original record listed 4 "units with recorded terminal dispositions". The correct accounting is:

| Measure | Value |
|---|---|
| Units attempted (distinct ordinals) | **2** (ordinals 1 and 2, both llm_receiver_b) |
| Total recorded attempts | **4** (2 original + 2 repetitions) |
| Unattempted hosted units | **70** (72 hosted total minus 2 attempted) |
| Unattempted deterministic units | **36** |
| Total unattempted | **106** |

Repetitions are linked to the same ordinals as their originals; they are not additional experimental units. 2 + 106 = 108. ✓

### Correction 2: Anchor CI chronology

The original adjudication record set `anchor_ci_completed_utc = 2026-09-21T17:09:25Z` (the PR #158 merge time). The corrected value is `2026-09-21T17:10:55Z`:

| Workflow | Run ID | Last job completed |
|---|---|---|
| Cross-System Claim Handoff v0.1 | 35630191369 | `2026-09-21T17:09:56Z` |
| Fork Proof-Surface Integration | 35630191332 | `2026-09-21T17:10:55Z` |

Gap from anchor CI completion to first repetition start: **4 min 35.8 s** (≈275 s). Chronology is consistent. Gate decision unchanged.

### Correction 3: AMEND-004 concrete research (v0.2)

The skeleton (v0.1) contained TO-BE-DETERMINED placeholders. The v0.2 proposal supplies:

**Protocol version boundary:** A receiver change is substantive under protocol §7 and preregistration §12. Migration requires a new experiment version (CSH v0.2). The v0.1 frozen receiver configs are preserved; results from the new version are not retroactive substitutes for unexecuted v0.1 units.

**Request-byte resolution:** Original frozen requests contain `"model": "deepseek/DeepSeek-V3-0324"` in the JSON body. New endpoint requires a different model field. Original requests are preserved unchanged; new requests are composed and hash-bound separately.

**receiver_b (DeepSeek) finding:** DeepSeek-V3-0324 is **not documented** in the current DeepSeek API (`api-docs.deepseek.com`, 2026-09-21). Current models: `deepseek-flash`, `deepseek-v4-pro`. V3-0324 snapshot is not accessible via the direct API. Reviewer must decide: accept nearest available model, locate alternative platform, or declare blocked.

**receiver_a (Llama Scout) finding:** Groq lists `meta-llama/llama-4-scout-17b-16e-instruct` as available (`console.groq.com/docs/models`). Endpoint: `https://api.groq.com/openai/v1/chat/completions`, auth: `GROQ_API_KEY`. **Blocker:** Llama 4 Scout reportedly retired for free/developer access on Groq; enterprise exception requires confirmation and documentation.

### Next gate

Reviewer authorization of CSH-AMEND-004 v0.2 proposal; version-boundary decision (CSH v0.2 designation); receiver_b availability resolution (V3-0324 access or model substitution decision); receiver_a Groq access-tier confirmation; new receiver freeze; fresh request composition; fresh repetition execution.

See: [`FORK_CURRENT_WORK_REGISTER_v0_7.json`](FORK_CURRENT_WORK_REGISTER_v0_7.json)

---

*Predecessor objects (v0.1–v0.6 deltas) retain their last recorded standing without fresh verification in this overlay.*
