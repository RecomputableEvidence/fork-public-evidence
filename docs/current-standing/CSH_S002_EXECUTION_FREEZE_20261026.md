# CSH-S002 execution freeze and local runner — 2026-10-26

Standing: executable frozen 24-request package; corpus execution remains unobserved.
Predecessor candidate, source S001 experiment, and failed Groq/DeepSeek access
receipts are preserved unchanged. This note succeeds preparation standing only.

## Evidence and budget

The uploaded csh-s002-neutral-20261026-103105.zip is preserved byte-for-byte per
member in CSH_S002_NEUTRAL_20261026. Both receivers returned HTTP 200, completed,
exact expected JSON and exact permitted model strings. Four captured-body hashes
recomputed; intended requests match captured requests semantically. Reported
combined USD cost is 0.00003. No corpus was included. Returned tool_choice=auto
conflicts with wire tool_choice=none; empty tools and no recorded tool activity
support only the bounded observation, not provider internal enforcement.

The execution-v0.1 directory contains the original recomputable plan, 24 exact
wire request bodies, coding handoff, and FREEZE.json binding repository sources,
SDK requirement, neutral evidence and package members. Freeze SHA-256:
`95857e56d8cf563fb313a439e85dfb40c4d9ae298dce9aee6c12e811a01b77c2`.

Runner: tools/run_csh_s002_v0_1.py. USD 1.00 admission ceiling, USD 0.06 prior
neutral reservation retained, USD 0.03 reserved per corpus request, USD 0.78 gross
planned commitment. Actual observed charges are separate. No automated retries,
no concurrency, no recovery/resume. One persistent repository-root campaign claim
prevents local repeated campaigns. It cannot prevent a deliberate deletion,
another checkout/machine, unrelated spending, or an in-flight billing overrun.
Do not delete the marker to rerun; preserve any failure for separate review.

## Verification record

Initial targeted run: 7 failed, 41 passed. The strict wire-byte guard rejected
SDK key ordering before transport (zero mock calls in those failures). Freeze
serialization was corrected to the pinned SDK's alphabetical request key order;
the guard was retained. The repaired run passed all 48 then-existing tests.
Additional failure-path fixtures cover timeout, incomplete response, malformed
response, absent cost, and disk failure before admission. No paid calls were made.

The runner preserves raw responses before parsing, leaves unknown costs reserved,
stops at first failed qualification, and produces all 24 analysis rows without
numeric scoring. Synthetic S002 inputs pass the inherited classifier schemas and
paired-analysis path. Human normalization and adjudication remain outstanding.

## Windows invocation

Run inside C:\N\fork-day0-csh-repair on the updated S002 branch with the existing
PERPLEXITY_API_KEY environment variable set in that same terminal. Offline:

```powershell
.\.venv\Scripts\python.exe tools/run_csh_s002_v0_1.py
if ($LASTEXITCODE -ne 0) { throw "Frozen package verification failed." }
```

One live campaign (up to 24 paid requests, stops on first failure):

```powershell
$runDir = Join-Path 'C:\N' ('csh-s002-corpus-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
.\.venv\Scripts\python.exe tools/run_csh_s002_v0_1.py `
    --live `
    --expected-freeze-sha256 95857e56d8cf563fb313a439e85dfb40c4d9ae298dce9aee6c12e811a01b77c2 `
    --output-dir $runDir
$runExit = $LASTEXITCODE
Write-Host "Exit code: $runExit"
Write-Host "Evidence: $runDir"
if (Test-Path $runDir) {
    Compress-Archive -Path $runDir -DestinationPath "$runDir.zip"
}
```

Upload the resulting ZIP, including stopped/failed results. Do not rerun the
neutral preflight or corpus campaign to obtain a preferred result.

## Final local validation

- Targeted preparation/execution regressions: 53 passed in 1.99 seconds.
- Full repository regression: 846 passed in 92.80 seconds.
- Standing freshness: PASS, zero errors.
- Frozen package recomputation and pinned digest: VERIFIED_OFFLINE, 24 units.
- Python compilation and git diff formatting checks: passed.
- Remote CI for this successor is recorded separately by the hosted workflow.

An interrupted process may leave only its durable ledger/reservation and partial
unit files; treat these as authoritative unknown outcomes. Handoff summaries are
written during normal progress and completion, and are not a crash-recovery tool.

## Hosted optional-dependency correction

At commit 9b78b0031afa2d26f33ffe7e692ef129feb0e916, dedicated execution jobs
passed on Linux and Windows, but the generic Linux proof job reported 13 failed,
811 passed, 3 skipped: new mock-transport tests imported optional httpx before
checking availability. Job 121742600324 preserves that failure. The tests now
explicitly skip unavailable optional transport dependencies, consistent with
the existing optional SDK suite. Dedicated CI still installs the pinned SDK and
runs every execution test. Runner, freeze and all request bytes are unchanged.

Post-correction targeted verification: 53 passed with SDK installed; in a fresh
proof-only virtual environment, 38 passed and 15 optional transport tests skipped.
