# CSH v0.1 Hosted Receiver Execution Protocol

Status: **draft, unfrozen, execution-blocked**

This protocol binds the two hosted CSH receivers to explicit GitHub Models
identifiers and one shared adapter contract. It does not authorize baseline
execution. The adapter refuses all live requests until the canonical corpus
freeze reports both `freeze_status: frozen` and
`baseline_execution_permitted: true`.

## Receiver bindings

| Receiver | Requested model ID | Expected returned model |
|---|---|---|
| `llm_receiver_a` | `meta/Llama-4-Scout-17B-16E-Instruct` | `Llama-4-Scout-17B-16E-Instruct` |
| `llm_receiver_b` | `deepseek/DeepSeek-V3-0324` | `DeepSeek-V3-0324` |

Both receivers use:

- endpoint `https://models.github.ai/inference/chat/completions`;
- bearer authentication from `GITHUB_TOKEN`;
- `temperature: 0`;
- `top_p: 1`;
- `max_tokens: 2048`;
- `presence_penalty: 0`;
- `frequency_penalty: 0`;
- `stream: false`;
- no seed;
- no tools, retrieval, memory, or prior conversation history;
- one system message and one user message;
- no silent retry, response repair, normalization, or classification.

## Entrypoints

```text
python tools/csh_receiver_a_llama_v0_1.py ...
python tools/csh_receiver_b_deepseek_v0_1.py ...
```

Required arguments:

```text
--system-prompt PATH
--prompt PATH
--output RAW_PROVIDER_RESPONSE.json
--metadata-output EXECUTION_METADATA.json
```

Optional arguments:

```text
--request-output EXACT_REQUEST.json
--freeze-file CORPUS_FREEZE_v0_1.json
--timeout-seconds 120
```

When `--request-output` is omitted, the adapter derives it from the metadata
path. Every output path must be new. Existing artifacts are never overwritten.

## Preservation contract

For each attempted request, the adapter preserves:

- exact UTF-8 prompt and system-instruction digests;
- exact serialized request bytes;
- exact raw provider-response bytes when a response exists;
- requested and returned model identifiers;
- fixed parameter values;
- selected non-secret response headers;
- usage metadata when present;
- start and completion timestamps;
- terminal HTTP, transport, validation, or model-mismatch state.

The bearer token and authorization header value are never written.

## Execution boundary

Smoke-test responses created before this protocol are
`PILOT_CONFIGURATION_TEST` artifacts and remain excluded from the baseline and
hypothesis test. This adapter does not create CSH run or result records; the
future frozen runner must do that separately.

Both hosted receivers share the GitHub Models serving platform. The experiment
therefore compares model families, not independent serving platforms. Explicit
model IDs do not prove an immutable backend deployment, fixed provider routing,
or bit-identical future behavior.

## Non-claims

A successful adapter invocation proves only that one bounded request completed
and that the specified artifacts were preserved. It does not establish truth,
correctness, compliance, legal sufficiency, safety, authorization, approval,
certification, endorsement, production readiness, institutional authority, or
the CSH hypothesis.
