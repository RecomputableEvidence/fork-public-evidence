Set-Location (git rev-parse --show-toplevel)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -Scope Global -ErrorAction SilentlyContinue) {
    $Global:PSNativeCommandUseErrorActionPreference = $false
}

$ExpectedBranch = "boundary-delta-record-v0.1"
$FixtureWin  = "examples\boundary_delta_record\invalid_transition_kind_rule_mismatch_v0_1.json"
$FixtureGit  = "examples/boundary_delta_record/invalid_transition_kind_rule_mismatch_v0_1.json"
$ValidWin    = "examples\boundary_delta_record\valid_preserved_v0_1.json"
$ReviewDir   = "output\boundary_delta_record\review"

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Text
    )

    $Dir = Split-Path -Parent $Path
    if ($Dir -and -not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Force -Path $Dir | Out-Null
    }

    $Normalized = $Text.Replace("`r`n", "`n").Replace("`r", "`n").TrimEnd("`n") + "`n"
    [System.IO.File]::WriteAllText($Path, $Normalized, $Utf8NoBom)
}

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

"`n=== PREPARE BDR v0.1 PR PACKAGE ==="

$Status = git status --short
if ($Status) {
    throw "Working tree is not clean. Review package generation is intentionally clean-tree only."
}

$Branch = git branch --show-current
if ($Branch -ne $ExpectedBranch) {
    throw "Unexpected branch. Expected $ExpectedBranch, got $Branch."
}

git cat-file -e "HEAD:$FixtureGit"
if ($LASTEXITCODE -ne 0) {
    throw "Mismatch fixture is not present in HEAD. Use forward slashes in Git object paths."
}

python -m py_compile tools\check_boundary_delta_record.py tests\test_boundary_delta_record_v0_1.py
if ($LASTEXITCODE -ne 0) {
    throw "Python compile gate failed."
}

$HeadFull      = git rev-parse HEAD
$HeadShort     = git rev-parse --short=7 HEAD
$Tree          = git rev-parse "HEAD^{tree}"
$FixtureHash   = git hash-object $FixtureWin
$FixtureHistory = @(git log --oneline -- $FixtureWin)
$RecentCommits  = @(git log --oneline -3)

$Valid = Invoke-BdrChecker -Path $ValidWin
if ($Valid.ExitCode -ne 0 -or $Valid.Json.structural_outcome -ne "INSPECTABLE") {
    throw "Valid preserved fixture did not return INSPECTABLE with exit 0."
}

$Mismatch1 = Invoke-BdrChecker -Path $FixtureWin
if ($Mismatch1.ExitCode -ne 1 -or $Mismatch1.Json.structural_outcome -ne "NOT_INSPECTABLE") {
    throw "Mismatch fixture did not return NOT_INSPECTABLE with exit 1."
}
if (-not ($Mismatch1.Json.findings | Where-Object { $_.code -eq "TRANSITION_KIND_RULE_MISMATCH" })) {
    throw "Mismatch fixture output lacks TRANSITION_KIND_RULE_MISMATCH."
}

$Mismatch2 = Invoke-BdrChecker -Path $FixtureWin
if ($Mismatch2.ExitCode -ne 1) {
    throw "Second mismatch run should exit 1."
}
$DeterministicMismatch = ($Mismatch1.Raw -eq $Mismatch2.Raw)
if (-not $DeterministicMismatch) {
    throw "Mismatch fixture output is not deterministic across repeated runs."
}

New-Item -ItemType Directory -Force -Path $ReviewDir | Out-Null

$Evidence = [ordered]@{
    review_package   = "BDR_v0_1_hardened_technical_review"
    branch           = $Branch
    head_commit      = $HeadFull
    head_short       = $HeadShort
    tree_hash        = $Tree
    fixture_path     = $FixtureWin
    fixture_git_object_path = $FixtureGit
    fixture_hash     = $FixtureHash
    recent_commits   = $RecentCommits
    fixture_history  = $FixtureHistory
    valid_fixture    = [ordered]@{
        path               = $ValidWin
        exit_code          = $Valid.ExitCode
        structural_outcome = $Valid.Json.structural_outcome
        findings_count     = $Valid.Json.findings.Count
        limitations        = $Valid.Json.limitations
    }
    mismatch_fixture = [ordered]@{
        path               = $FixtureWin
        exit_code          = $Mismatch1.ExitCode
        structural_outcome = $Mismatch1.Json.structural_outcome
        finding_codes      = @($Mismatch1.Json.findings | ForEach-Object { $_.code })
        deterministic_replay = $DeterministicMismatch
    }
    non_claims = [ordered]@{
        not_truth              = $true
        not_safety             = $true
        not_compliance         = $true
        not_legal_sufficiency  = $true
        not_approval           = $true
        not_risk_or_severity   = $true
        not_runtime_enforcement = $true
        not_semantic_inference = $true
    }
}

$EvidenceJson = $Evidence | ConvertTo-Json -Depth 20
Write-Utf8NoBomLf -Path "$ReviewDir\bdr_v0_1_review_evidence.json" -Text $EvidenceJson

$PrDescription = @"
# Boundary Delta Record v0.1 — hardened technical review candidate

## Summary

This PR adds Boundary Delta Record v0.1 as a narrow mechanical inspection artifact for Fork.

BDR v0.1 inspects declared boundary transitions and determines whether the record is structurally inspectable under finite v0.1 rules. It is designed to make declared boundary expansion and transition mismatch visible without becoming a semantic, policy, risk, compliance, safety, legal, or approval interpreter.

## Current branch evidence

- Branch: `$Branch`
- HEAD: `$HeadFull`
- Tree: `$Tree`
- Mismatch fixture hash: `$FixtureHash`

Recent commits:

```text
$($RecentCommits -join "`n")
```

Mismatch fixture history:

```text
$($FixtureHistory -join "`n")
```

## Core locks

BDR v0.1 is constrained by:

- declared inputs only
- opaque references only
- finite transition vocabulary
- finite transition kind / transformation rule compatibility map
- binary outcome only: INSPECTABLE / NOT_INSPECTABLE
- no natural-language inference
- no scoring, severity, confidence, risk, approval, or policy judgment
- authored structural_outcome is recomputed and not trusted as authoritative

## Hardened behavior

The checker emits explicit non-inference limitations:

- does_not_infer_scope_from_text
- does_not_infer_authority_from_text
- does_not_infer_evidence_requirements_from_text
- requires_declared_transitions
- treats_references_as_opaque_tokens

The adversarial mismatch fixture returns:

- NOT_INSPECTABLE
- TRANSITION_KIND_RULE_MISMATCH

The valid preserved fixture returns:

- INSPECTABLE

## What BDR v0.1 does not claim

BDR v0.1 does not determine truth, safety, compliance, legal sufficiency, approval, admissibility, risk, severity, or upstream completeness. NOT_INSPECTABLE is a structural inspection outcome only.

## Review ask

Please review this PR against one narrow question:

> Does BDR v0.1 mechanically expose declared boundary expansion and transition mismatch without becoming a semantic, policy, risk, or governance interpreter?

## Deferred backlog

Deferred outside this v0.1 branch:

- schema/checker enum parity tests
- canonicalization tests
- reviewer harness script hardening
- schema/checker authority relationship clarification
- declared requires_* / transferred_* model
- cross-record or bundle-level verification
"@
Write-Utf8NoBomLf -Path "$ReviewDir\bdr_v0_1_pr_description.md" -Text $PrDescription

$ReviewerChecklist = @"
Boundary Delta Record v0.1 Reviewer Checklist

1. Confirm branch state

```bash
git status --short
git branch --show-current
git log --oneline -3
```

Expected:

- clean working tree
- branch: boundary-delta-record-v0.1
- recent commits include:
$($RecentCommits -join "`n")

2. Confirm fixture provenance

Use forward slashes for Git object paths:

```bash
git cat-file -e "HEAD:examples/boundary_delta_record/invalid_transition_kind_rule_mismatch_v0_1.json"
git log --oneline -- examples\boundary_delta_record\invalid_transition_kind_rule_mismatch_v0_1.json
```

Expected fixture history includes:

$($FixtureHistory -join "`n")

3. Compile checker and tests

```bash
python -m py_compile tools\check_boundary_delta_record.py tests\test_boundary_delta_record_v0_1.py
```

Expected: no output and exit code 0.

4. Reproduce valid fixture

```bash
python tools\check_boundary_delta_record.py examples\boundary_delta_record\valid_preserved_v0_1.json
```

Expected:

- "structural_outcome": "INSPECTABLE"
- "findings": []

5. Reproduce adversarial mismatch fixture

```bash
python tools\check_boundary_delta_record.py examples\boundary_delta_record\invalid_transition_kind_rule_mismatch_v0_1.json
```

Expected:

- "structural_outcome": "NOT_INSPECTABLE"
- finding codes include "TRANSITION_KIND_RULE_MISMATCH"

The fixture authors INSPECTABLE, but the checker recomputes NOT_INSPECTABLE.

6. Confirm deterministic replay

Run the mismatch fixture twice and confirm output is identical.

7. Confirm outcome discipline

The checker emits only:

- INSPECTABLE
- NOT_INSPECTABLE

Do not reinterpret NOT_INSPECTABLE as risk, severity, compliance, safety, truth, approval, or legal sufficiency.

8. Review question

Does BDR v0.1 mechanically expose declared boundary expansion and transition mismatch without becoming a semantic, policy, risk, or governance interpreter?
"@
Write-Utf8NoBomLf -Path "$ReviewDir\bdr_v0_1_reviewer_checklist.md" -Text $ReviewerChecklist

$ShareNote = @"
I have a narrow Fork branch ready for controlled technical review: boundary-delta-record-v0.1.

The branch adds Boundary Delta Record v0.1 as a mechanical inspection artifact. It does not evaluate whether a downstream statement is true, safe, compliant, legally sufficient, approved, or risky.

The review question is narrow:

Does BDR v0.1 mechanically expose declared boundary expansion and transition mismatch without becoming a semantic, policy, risk, or governance interpreter?

The key adversarial behavior is that a fixture can author INSPECTABLE, but if the declared transition uses an incompatible transition kind / transformation rule pairing, the checker recomputes NOT_INSPECTABLE and emits TRANSITION_KIND_RULE_MISMATCH.

The branch is intentionally frozen for review. I’m not looking to add features in this pass, only to confirm whether the v0.1 mechanics hold under inspection.
"@
Write-Utf8NoBomLf -Path "$ReviewDir\bdr_v0_1_review_share_note.md" -Text $ShareNote

"`n=== REVIEW PACKAGE GENERATED ==="
Get-ChildItem $ReviewDir | Select-Object Name, Length
"`n=== GENERATED FILES ==="
"output\boundary_delta_record\review\bdr_v0_1_review_evidence.json"
"output\boundary_delta_record\review\bdr_v0_1_pr_description.md"
"output\boundary_delta_record\review\bdr_v0_1_reviewer_checklist.md"
"output\boundary_delta_record\review\bdr_v0_1_review_share_note.md"
"`n=== STATUS ==="
git status --short
