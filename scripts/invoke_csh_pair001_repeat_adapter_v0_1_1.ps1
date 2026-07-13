#requires -Version 5.1
<#
Provider-specific executor adapter contract for CSH Pair-001 v0.1.1 repetition.

This file is intentionally non-operative. Copy it outside the repository, implement the
provider call using the repository's already-approved receiver mechanism, and pass that
implemented copy to repair_csh_execution_instrumentation_v0_1_1.ps1 -Mode Repeat.

The orchestrator invokes the adapter once per affected original run with:
- RepoRoot
- OriginalRunId
- NewRunId
- SourceAttemptDirectory
- OutputDirectory

The adapter MUST write at least these evidence files under OutputDirectory:
- exact-request.json (byte-identical to SourceAttemptDirectory\exact-request.json)
- execution-metadata.json
- raw-provider-response.json

Every terminal outcome must be preserved. Do not retry under the same NewRunId.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$RepoRoot,
    [Parameter(Mandatory = $true)][string]$OriginalRunId,
    [Parameter(Mandatory = $true)][string]$NewRunId,
    [Parameter(Mandatory = $true)][string]$SourceAttemptDirectory,
    [Parameter(Mandatory = $true)][string]$OutputDirectory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

throw "Provider-specific CSH repeat adapter is not implemented. Copy this template, implement the approved receiver invocation, and pass the implemented script with -RepeatExecutorScript."
