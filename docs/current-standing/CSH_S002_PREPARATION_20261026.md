# CSH-S002 affordable successor preparation

Prepared a separately identified 24-unit pilot using existing Perplexity access.
No paid calls were made by the assistant. Candidate and preregistration are in
`docs/experiments/cross-system-claim-handoff-successor-002-v0.1/`.

The failed S001 access attempt is preserved byte-for-byte in
`CSH_S001_ACCESS_ATTEMPT_20261026/`: Groq HTTP 403 body `error code: 1010`,
DeepSeek HTTP 402 body reports insufficient balance. All four saved request and
response digests match receipts. These are neutral access failures, not corpus
runs, invalid-key findings, or experimental hypothesis results. They remain
predecessor evidence after selecting a new platform.

The source Perplexity integration remains PR #196. This successor is prepared
on that branch's commit 2901eea7c5eb155c74f15a839187453db479664d and does not
silently merge either change. The old research artifacts and ledger entries
remain intact; recognized additions are IN_FLIGHT.

## Commands (repository root, PowerShell)

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-perplexity-agent.txt
$planDir = Join-Path 'C:\N' ('csh-s002-plan-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
.\.venv\Scripts\python.exe tools/prepare_csh_s002_v0_1.py --output-dir $planDir
```

The command above is entirely offline. To qualify the two candidates using the
existing PERPLEXITY_API_KEY in your terminal, the following explicit command
makes at most two paid neutral calls, stopping on the first failure. It reserves
$0.03 per attempted call for planning; actual provider billing can differ.

```powershell
$neutralDir = Join-Path 'C:\N' ('csh-s002-neutral-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
.\.venv\Scripts\python.exe tools/prepare_csh_s002_v0_1.py --neutral-live --output-dir $neutralDir
$neutralExit = $LASTEXITCODE
Write-Host "Exit code: $neutralExit; evidence: $neutralDir"
```

Do not paste credentials. Raw response files need review before publication.
If a key is absent, no request is sent. SDK retries are disabled; do not repeatedly
invoke the command after failures. A new batch is a new paid attempt.

Candidate plan is recomputable; it is not a frozen authorization to execute.
Source code and exact SDK version are bound at the subsequent freeze, after
candidate compatibility and cost are observed. Next implementation work is the
corpus runner and coding handoff; not the predecessor GitHub Models adapters.

## Local verification

Final full suite: 811 passed in 44.56 seconds. Targeted preparation tests: 18 passed.
Standing accounting, Python compilation, and diff formatting passed. All four
preserved S001 request/response hashes match receipts. Offline candidate plan:
24 hosted units; nominal token estimate $0.0344910; planned corpus reservations
$0.72. No paid calls, receiver qualification, freeze or corpus execution occurred.
