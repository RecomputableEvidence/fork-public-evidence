# CSH-AMEND-004: Receiver Migration Proposal

**Status:** `PREPARED_NOT_AUTHORIZED_NOT_ACTIVATED`  
**Current version:** v0.2 (concrete) — [`CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_2.json`](CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_2.json)  
**Superseded skeleton:** v0.1 — [`CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json`](CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json) (preserved unchanged)  
**Prepared:** 2026-09-21  
**Source commit:** `2dab684fc904f43ca0d35d1c1bbc500e92156ec4`

## Motivation

GitHub Models (endpoint `https://models.github.ai/inference/chat/completions`) retired 2026-07-30. Both frozen receiver classes use this endpoint:

- **llm_receiver_b**: DeepSeek-V3-0324 via GitHub Models
- **llm_receiver_a**: Llama-4-Scout-17B-16E-Instruct via GitHub Models

HTTP 410 was received on both AMEND-002 repetition attempts (2026-09-21). Continuation requires migration to an alternative serving platform.

## Protocol version boundary

A receiver change is a substantive experimental change under the governing protocol (§7) and preregistration (§12). This migration **cannot silently continue CSH v0.1** under the frozen receiver configs. It requires:

1. A new experiment version (proposed: CSH v0.2 or CSH-MIGRATION-v0.1) with new frozen receiver config files.
2. The v0.1 frozen configs (`RECEIVER_A_GITHUB_MODELS_LLAMA_SCOUT_v0_1.json`, `RECEIVER_B_GITHUB_MODELS_DEEPSEEK_V3_0324_v0_1.json`) preserved unchanged.
3. Results obtained under the new version are not retroactive replacements for unexecuted CSH v0.1 units.

## Request-byte accounting

The original frozen requests contain the `model` field inside the JSON body. Transmitting to a new endpoint requires a different model identifier. The original requests are therefore **preserved unchanged as reference records** for CSH-RUN-001 and CSH-RUN-002. New requests for migrated-receiver execution are composed separately, hash-bound, and recorded as new artifacts.

## Concrete research findings (2026-09-21)

### receiver_b (DeepSeek)

| Field | Finding |
|---|---|
| Source | `https://api-docs.deepseek.com/quick_start/pricing` |
| V3-0324 availability | **NOT DOCUMENTED** in current DeepSeek API |
| Current documented models | `deepseek-flash` (DeepSeek-V4.1-Flash), `deepseek-v4-pro` (DeepSeek-V4-Pro-0813) |
| Direct endpoint | `https://api.deepseek.com/chat/completions` |
| Auth env | `DEEPSEEK_API_KEY` |
| **Blocker** | V3-0324 snapshot not accessible via direct API; reviewer must decide: accept nearest available model, find alternative platform serving V3-0324, or declare blocked |

### receiver_a (Llama Scout)

| Field | Finding |
|---|---|
| Source | `https://console.groq.com/docs/models` |
| Groq model ID | `meta-llama/llama-4-scout-17b-16e-instruct` (listed as available) |
| Groq endpoint | `https://api.groq.com/openai/v1/chat/completions` |
| Auth env | `GROQ_API_KEY` |
| **Blocker** | Llama 4 Scout reportedly retired for free/developer access on Groq; enterprise exception needs confirmation and documentation |

## Required gates (all PENDING)

1. **Reviewer authorization** — explicit written authorization required
2. **Version boundary decision** — authorize new experiment version (CSH v0.2) before freezing new configs
3. **receiver_b availability resolution** — V3-0324 not documented in current DeepSeek API; option selection required
4. **receiver_a access-tier confirmation** — Groq enterprise access for Llama Scout must be confirmed
5. **Endpoint selection and freeze** — new receiver configs with v0.2 identifiers
6. **Availability check** — bounded smoke test per proposed endpoint (non-experimental)
7. **Adapter update and hash** — update API-envelope fields only; record new source hash
8. **Credential provision** — via approved secret mechanism, not printed or committed
9. **Fresh request composition** — new requests from original experimental content, new API-envelope fields, hash-bound
10. **Fresh repetition execution** — new run IDs, composed requests, all outcomes preserved
11. **Execution gate evaluation** — per existing protocol; HTTP 200 alone is insufficient

## Population accounting

| Category | Count |
|---|---|
| Total units | 108 |
| Attempted units (distinct ordinals) | 2 |
| Unattempted hosted units | 70 |
| Unattempted deterministic units | 36 |
| Total unattempted | 106 |

The 70 unattempted hosted units cannot receive terminal dispositions from platform retirement alone. See `BASELINE_POPULATION_ACCOUNTING_20260921_CORRECTION_001.json`.

## What this proposal does not authorize

No provider calls, model output, result assertions, baseline declarations, closed-object reopening, or activation of any kind. This document becomes an amendment only upon explicit reviewer authorization.

---

*Preserved skeleton (v0.1): [`CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json`](CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json) — unchanged.*
