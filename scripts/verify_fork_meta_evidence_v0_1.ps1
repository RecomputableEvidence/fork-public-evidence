#requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter()]
    [string]$RepoRoot = (
        Split-Path -Parent (
            Split-Path -Parent $PSScriptRoot
        )
    )
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$RepoRoot = [System.IO.Path]::GetFullPath($RepoRoot)
Push-Location $RepoRoot

try {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw 'python was not found.'
    }

    & python tools/check_fork_meta_evidence_package_v0_1.py --json
    if ($LASTEXITCODE -ne 0) {
        throw 'Fork Meta-Evidence package-integrity check failed.'
    }

    & python tools/check_experiment_meta_evidence_v0_1.py `
        registries/experiment_meta_evidence_registry_v0_1.json `
        --json
    if ($LASTEXITCODE -ne 0) {
        throw 'Fork Meta-Evidence integrated checker failed.'
    }

    $Tests = @(
        'tests/test_attribution_authorization_record_v0_1.py',
        'tests/test_experiment_meta_evidence_v0_1.py',
        'tests/test_experiment_outcome_record_v0_1.py',
        'tests/test_external_context_reference_set_v0_1.py',
        'tests/test_interaction_provenance_record_v0_1.py',
        'tests/test_participant_context_receipt_v0_1.py',
        'tests/test_fork_meta_evidence_package_integrity_v0_1.py'
    )

    & python -m pytest @Tests -q
    if ($LASTEXITCODE -ne 0) {
        throw 'Fork Meta-Evidence bounded test suite failed.'
    }

    [ordered]@{
        verifier = 'verify_fork_meta_evidence_v0_1.ps1'
        package = 'FORK-META-EVIDENCE-v0.1'
        package_integrity = 'PASS'
        integrated_checker = 'CONFORMING'
        bounded_tests = 'PASS'
        state = 'PASS'
    } | ConvertTo-Json -Depth 5
}
finally {
    Pop-Location
}