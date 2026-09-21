# CSH-AMEND-004: Receiver Migration Proposal

**Status:** `PREPARED_NOT_AUTHORIZED_NOT_ACTIVATED`  
**Prepared:** 2026-09-21  
**Source commit:** `38f7a278211fca62b02fb3ee2cec26814e9ed9b6`

## Motivation

GitHub Models (endpoint `https://models.github.ai/inference/chat/completions`) retired 2026-07-30. Both frozen receiver classes use this endpoint:

- **llm_receiver_b**: DeepSeek-V3-0324 via GitHub Models
- **llm_receiver_a**: Llama-4-Scout-17B-16E-Instruct via GitHub Models

HTTP 410 was received on both AMEND-002 repetition attempts (2026-09-21). Continuation requires migration to an alternative serving platform.

## What this proposal changes

**Receiver configurations only.** All experimental design elements are preserved:
hypothesis, corpus, conditions, scoring, classification, run-order method, prompts, handoff artifacts, stopping rules.

The proposed change identifies that new receiver configurations are needed for both hosted receivers. Specific endpoints, model identifiers, and credentials are **not selected in this document** — those selections require reviewer authorization and must pass availability gates before freezing.

## Comparability limits

Matching displayed model names across serving platforms does not establish receiver equivalence. Backend deployment, quantization, serving software, and infrastructure may differ. Results obtained on a new platform carry this additional uncertainty. This is a limitation on probative strength, not a reason to abandon the experiment.

## Required gates (all PENDING)

1. **Reviewer authorization** — explicit written authorization required
2. **Endpoint selection** — specific alternative endpoints must be identified
3. **Availability check** — bounded smoke test per proposed endpoint (non-experimental)
4. **New receiver freeze** — updated configuration files committed and verified
5. **Adapter verification** — adapter source hash recorded before execution
6. **Credential provision** — via approved secret mechanism, not printed or committed
7. **Fresh repetition execution** — new run IDs, same original request bytes
8. **Execution gate evaluation** — per existing protocol; HTTP 200 alone is insufficient

## What this proposal does not authorize

No provider calls, model output, result assertions, baseline declarations, or activation of any kind.

See [`CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json`](CSH_AMEND_004_RECEIVER_MIGRATION_PROPOSAL_v0_1.json) for full detail.
