# CSH-S001 Hosted Receiver Candidate Revision — 2026-09-23

**Status:** PRE-FREEZE CANDIDATE REVISION  
**Experiment:** `CROSS-SYSTEM-CLAIM-HANDOFF-SUCCESSOR-001-v0.1`

## Reason

The prior Groq/DeepSeek candidate pair was selected before repository credentials and zero-cost access conditions were established. DeepSeek was not demonstrated to satisfy the researcher's zero-spend constraint, and neither prior provider credential was established in the repository Actions context.

The researcher subsequently established repository secrets named `MISTRAL_API_KEY` and `OPENAI_API_KEY`.

This record therefore revises the **candidate preflight pair only**, before receiver-registry freeze and before any corpus-bearing hosted execution.

## New candidate pair

- `hosted_receiver_a_candidate`: Mistral Chat Completions, model alias `mistral-small-latest`, credential name `MISTRAL_API_KEY`.
- `hosted_receiver_b_candidate`: OpenAI Chat Completions, model `gpt-5.6-luna`, credential name `OPENAI_API_KEY`.

## Access rule

Presence of a repository secret is not evidence that the account has usable quota, credits, model entitlement, or endpoint access.

Both candidates must pass the existing neutral, non-corpus access preflight before either receiver identity can be frozen.

An HTTP quota, billing, entitlement, authentication, model-unavailable, or parameter-incompatibility response is an access/preflight result only. It is not a CSH content result.

If either candidate fails, revise the candidate registry again before freeze. Do not silently substitute a provider or model.

## Non-claims

- `SECRET_PRESENT != API_ACCESS_ESTABLISHED`
- `API_KEY_VALID != MODEL_ACCESS_ESTABLISHED`
- `MODEL_ENDPOINT_REACHABLE != RECEIVER_FROZEN`
- `PREFLIGHT_PASS != CSH_RESULT`
- This candidate revision does not thaw or alter any predecessor CSH v0.1 evidence.
