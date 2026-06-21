Set-Location (git rev-parse --show-toplevel)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -Scope Global -ErrorAction SilentlyContinue) {
    $Global:PSNativeCommandUseErrorActionPreference = $false
}

$ExpectedBranch = "boundary-delta-record-v0.1"
$ExpectedHead   = "e1612fa"
$FixtureWin = "examples\boundary_delta_record\invalid_transition_kind_rule_mismatch_v0_1.json"
$FixtureGit = "examples/boundary_delta_record/invalid_transition_kind_rule_mismatch_v0_1.json"
$ValidWin   = "examples\boundary_delta_record\valid_preserved_v0_1.json"

function Invoke-BdrChecker {
    param(
        [Parameter(Mandatory=$true)][string]$Path
    )

    $Output = & python tools\check_boundary_delta_record.py $Path 2>&1
    $ExitCode = $LASTEXITCODE
    $Text = ($Output | Out-String).Trim()

    if ($Text.Length -eq 0) {
        throw "Checker produced no output for $Path"
    }

    try {
        $Json = $Text | ConvertFrom-Json
    } catch {
        throw "Checker output was not valid JSON for $Path. Output:`n$Text"
    }

    return [pscustomobject]@{
        Path     = $Path
        ExitCode = $ExitCode
        Json     = $Json
        Raw      = $Text
    }
}

"`n=== BDR v0.1 TECHNICAL REVIEW GATE ==="

"`n=== STATUS ==="
$Status = git status --short
$Status
if ($Status) {
    throw "Working tree is not clean."
}

"`n=== BRANCH ==="
$Branch = git branch --show-current
$Branch
if ($Branch -ne $ExpectedBranch) {
    throw "Unexpected branch. Expected $ExpectedBranch, got $Branch."
}

"`n=== LAST COMMITS ==="
git log --oneline -3

"`n=== HEAD COMMIT ==="
$Head = git rev-parse --short=7 HEAD
$Head
if ($Head -ne $ExpectedHead) {
    throw "Unexpected HEAD. Expected $ExpectedHead, got $Head."
}

"`n=== FIXTURE PRESENT IN HEAD ==="
git cat-file -e "HEAD:$FixtureGit"
if ($LASTEXITCODE -ne 0) {
    throw "Mismatch fixture is not present in HEAD. Use forward slashes in Git object paths."
}

"`n=== FIXTURE HISTORY ==="
$FixtureHistory = git log --oneline -- $FixtureWin
$FixtureHistory
if (-not ($FixtureHistory -match "730e906")) {
    throw "Expected mismatch fixture history to include commit 730e906."
}

"`n=== HASHES ==="
$HeadFull  = git rev-parse HEAD
$Tree      = git rev-parse "HEAD^{tree}"
$FixtureHash = git hash-object $FixtureWin
"HEAD=$HeadFull"
"TREE=$Tree"
"FIXTURE_HASH=$FixtureHash"

"`n=== COMPILE ==="
python -m py_compile tools\check_boundary_delta_record.py tests\test_boundary_delta_record_v0_1.py
if ($LASTEXITCODE -ne 0) {
    throw "Python compile gate failed."
}

"`n=== VALID FIXTURE ==="
$Valid = Invoke-BdrChecker -Path $ValidWin
if ($Valid.ExitCode -ne 0) {
    throw "Valid fixture should exit 0."
}
if ($Valid.Json.structural_outcome -ne "INSPECTABLE") {
    throw "Valid fixture should return INSPECTABLE."
}
if ($Valid.Json.findings.Count -ne 0) {
    throw "Valid fixture should have no findings."
}

$ValidLimitations = $Valid.Json.limitations
foreach ($Key in @(
    "does_not_infer_scope_from_text",
    "does_not_infer_authority_from_text",
    "does_not_infer_evidence_requirements_from_text",
    "requires_declared_transitions",
    "treats_references_as_opaque_tokens"
)) {
    if ($ValidLimitations.$Key -ne $true) {
        throw "Valid fixture output is missing non-inference limitation: $Key"
    }
}

$Valid.Json.structural_outcome

"`n=== ADVERSARIAL MISMATCH FIXTURE ==="
$Mismatch1 = Invoke-BdrChecker -Path $FixtureWin
if ($Mismatch1.ExitCode -ne 1) {
    throw "Mismatch fixture should exit 1."
}
if ($Mismatch1.Json.structural_outcome -ne "NOT_INSPECTABLE") {
    throw "Mismatch fixture should return NOT_INSPECTABLE."
}
if (-not ($Mismatch1.Json.findings | Where-Object { $_.code -eq "TRANSITION_KIND_RULE_MISMATCH" })) {
    throw "Mismatch fixture must include TRANSITION_KIND_RULE_MISMATCH."
}
if (-not ($Mismatch1.Json.findings | Where-Object { $_.code -eq "STRUCTURAL_OUTCOME_MISMATCH" })) {
    throw "Mismatch fixture must include STRUCTURAL_OUTCOME_MISMATCH."
}

$Mismatch2 = Invoke-BdrChecker -Path $FixtureWin
if ($Mismatch2.ExitCode -ne 1) {
    throw "Second mismatch run should exit 1."
}
if ($Mismatch1.Raw -ne $Mismatch2.Raw) {
    throw "Mismatch fixture output is not deterministic across repeated runs."
}

$Mismatch1.Json.structural_outcome
($Mismatch1.Json.findings | Where-Object { $_.code -eq "TRANSITION_KIND_RULE_MISMATCH" }).code

"`n=== FINAL STATUS ==="
$FinalStatus = git status --short
$FinalStatus
if ($FinalStatus) {
    throw "Working tree changed during review gate."
}

"`n=== REVIEW GATE PASSED ==="
"Branch: $Branch"
"HEAD: $HeadFull"
"Tree: $Tree"
"Fixture hash: $FixtureHash"
"Valid fixture: INSPECTABLE"
"Mismatch fixture: NOT_INSPECTABLE / TRANSITION_KIND_RULE_MISMATCH"
