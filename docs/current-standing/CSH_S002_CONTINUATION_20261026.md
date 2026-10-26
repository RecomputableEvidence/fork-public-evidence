# CSH-S002 versioned continuation v0.2 — 2026-10-26

Standing: frozen continuation implementation, verified offline; remaining corpus
execution not yet observed. User requested proceeding after the parser repair
and screenshot showing its 16 successful remote checks and two hosted skips.

The continuation binds the preserved one-request stopped attempt, parser v0.2,
original freeze, exact remaining order, and source code. It carries the first
response by a separately recorded offline reparse and admits only the original
23 unattempted requests. The original FAIL receipt, STOPPED ledger, campaign
marker, and frozen runner/request package remain unchanged.

Continuation SHA-256:
`31674682367761a325e1f03e94c65015a466ee01ce757f5289c6eb8ec8bd9ec3`.

Admission starts at USD 0.09 gross committed reservations. Remaining allowance
is USD 0.69 (23 times USD 0.03), planned final commitment USD 0.78 within the
unchanged USD 1.00 ceiling. Reported prior neutral plus corpus cost USD 0.00062
is retained separately. No additional hosted qualification or first-unit retry.
This is local admission control, not a provider billing cap.

The original run directory must match all nine preserved files exactly. The
original campaign claim must name that directory and the original freeze. The
continuation atomically claims a new subdirectory inside that existing marker;
it never deletes or resets it. Any failure stops further requests. Its own
interruption does not enable automatic resume. Both attempts remain evidence.

Tests cover 23-request exact order, first-response carry without replay, full
prior-file preservation, cost continuity, stop on invalid/uncertain outcomes,
crash reservations, duplicate-run prevention, incorrect prior claims, missing
credentials, and frozen-order tampering. Initial targeted result: 17 passed.
No live API call was made during implementation or verification.

## Local commands

From the updated S002 branch in the same PowerShell session containing the key:

```powershell
$priorDir = 'C:\N\csh-s002-corpus-20261026-105606'
$continuation = '31674682367761a325e1f03e94c65015a466ee01ce757f5289c6eb8ec8bd9ec3'
.\.venv\Scripts\python.exe tools/continue_csh_s002_v0_2.py `
    --prior-output-dir $priorDir `
    --expected-continuation-sha256 $continuation
if ($LASTEXITCODE -ne 0) { throw "Continuation verification failed." }

$nextDir = Join-Path 'C:\N' ('csh-s002-continuation-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
.\.venv\Scripts\python.exe tools/continue_csh_s002_v0_2.py `
    --live --prior-output-dir $priorDir --output-dir $nextDir `
    --expected-continuation-sha256 $continuation
$continuationExit = $LASTEXITCODE
Write-Host "Exit code: $continuationExit"
Write-Host "Evidence: $nextDir"
if (Test-Path $nextDir) {
    Compress-Archive -Path $nextDir -DestinationPath "$nextDir.zip"
}
```

This command can send up to 23 paid requests. Preserve and upload stopped results
as well as successful ones. No marker reset or second continuation is provided.
