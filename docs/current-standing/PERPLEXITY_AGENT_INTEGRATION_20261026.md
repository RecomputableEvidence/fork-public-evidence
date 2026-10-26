# Perplexity Agent integration v0.1

Optional Python CLI/library capability for web-grounded research answers. This
does not replace CSH receivers, change their freeze, satisfy hosted-access gates,
or start the baseline. Orchestrator and Decisions are separate APIs and are not
needed for this requested capability.

## Use from the repository root (PowerShell)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-perplexity-agent.txt
```

Create a key at https://console.perplexity.ai if necessary. Set it in your own
terminal, never in chat. This masked prompt avoids putting the key in history:

```powershell
$secret = Read-Host "Perplexity API key" -AsSecureString
$env:PERPLEXITY_API_KEY = [System.Net.NetworkCredential]::new('', $secret).Password
Remove-Variable secret
if ($env:PERPLEXITY_API_KEY) { 'PERPLEXITY_API_KEY is set' }
.\.venv\Scripts\python.exe tools/perplexity_agent_answer_v0_1.py --smoke
.\.venv\Scripts\python.exe tools/perplexity_agent_answer_v0_1.py "What does Python's official documentation say about virtual environments?"
```

If a key is exposed, rotate it in the console. Do not commit credentials or
private outputs. No key is available in the implementation environment; real
HTTP 200 smoke verification is therefore pending user-side setup.

## Contract

- Official `perplexityai==0.46.1`, optional requirements file; no new framework.
- Explicit `openai/gpt-5.6-sol` model, web_search enabled, two research steps,
  512 output tokens by default (256 for smoke), 60-second SDK timeout. These
  are request bounds, not a dollar-cost guarantee. Token and tool charges apply.
- The SDK uses documented `/v1/responses`, an alias for `/v1/agent`.
- Answer comes from `output_text`; source records and URL annotations are kept
  separately. `grounding_metadata_present` describes returned metadata, not
  source verification; enabling search does not guarantee it is invoked.
- `--previous-response-id` continues a completed response in the same account.
  Provider default storage applies. No structured model output is required by
  this prose-answer tool; its CLI result envelope is JSON.
- Completed status, nonempty text, HTTP 200, and no reported error/incompletion
  are required for PASS. Partial answers retain a non-success disposition.
- No automatic retries. HTTP 401 is AUTHENTICATION_ERROR; HTTP 429 is RATE_LIMITED
  with parsed `retry_after_seconds`. Wait at least that interval before a new
  invocation. If absent, consult the console and back off; do not retry in a loop.
- Exceptions are reported by class/status only. Smoke output contains status and
  shape indicators only. No API key, authorization header, or error body is logged.

## Verification and accounting

Tests use the real SDK with HTTP mock transport, including request URL/body,
continuation, text/source/citation extraction, incomplete/malformed output,
missing credentials, HTTP errors, no retries, connection failure, and smoke
redaction. Dedicated Linux/Windows CI installs the optional SDK and runs these
tests. Other suites can skip the optional module if the SDK is absent.
The tool addition is recorded IN_FLIGHT in the active change ledger; existing
predecessor entries remain intact. No repository lint/type-check configuration
was found; pytest and the standing checker are the applicable project commands.

## Documentation consulted (2026-10-26)

- https://docs.perplexity.ai/llms.txt
- https://docs.perplexity.ai/docs/agent-api/quickstart
- https://docs.perplexity.ai/docs/agent-api/presets (redirects to effort)
- https://docs.perplexity.ai/docs/agent-api/tools/overview
- https://docs.perplexity.ai/docs/agent-api/output-control
- https://docs.perplexity.ai/api-reference/agent-post
- https://docs.perplexity.ai/docs/sdk/overview
- https://docs.perplexity.ai/docs/sdk/configuration
- https://docs.perplexity.ai/docs/getting-started/pricing
- https://docs.perplexity.ai/docs/admin/rate-limits-usage-tiers

Current docs use `effort`; `preset` is deprecated in the installed SDK. This
implementation chooses an explicit model and tools, so neither alias is needed.

## Local verification result

- SDK integration tests: 20 passed.
- Full project regression: 793 passed in 45.35 seconds.
- Standing accounting: PASS, zero errors.
- Python compilation and git diff --check: passed.
- Smoke command: CREDENTIAL_UNAVAILABLE, request_attempted=false, exit 1.
- Live API behavior remains unverified; no HTTP success is claimed.
