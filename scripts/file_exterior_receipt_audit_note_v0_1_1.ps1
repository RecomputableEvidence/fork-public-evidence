param(
    [string]$RepoRoot = "C:\N\fork-public-evidence",
    [string]$BranchName = "recomputation/exterior-receipt-audit-v0-1-1",
    [switch]$AllowDirty,
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"

function Fail {
    param([string]$Message)
    throw $Message
}

function Invoke-Git {
    param([Parameter(Mandatory = $true)][string[]]$Args)
    & git @Args
    if ($LASTEXITCODE -ne 0) {
        Fail "git $($Args -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $normalized = $Content -replace "`r`n", "`n"
    $normalized = $normalized -replace "`r", "`n"

    if (-not $normalized.EndsWith("`n")) {
        $normalized = $normalized + "`n"
    }

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $normalized, $encoding)
}

function Read-TextOrEmpty {
    param([string]$Path)

    if (Test-Path -LiteralPath $Path) {
        return [System.IO.File]::ReadAllText($Path)
    }

    return ""
}

function Add-Unique {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Value
    )

    if (-not $List.Contains($Value)) {
        [void]$List.Add($Value)
    }
}

function Append-IfMissing {
    param(
        [Parameter(Mandatory = $true)][string]$RelativePath,
        [Parameter(Mandatory = $true)][string]$Needle,
        [Parameter(Mandatory = $true)][string]$AppendText,
        [Parameter(Mandatory = $true)][System.Collections.Generic.List[string]]$Touched,
        [switch]$CreateIfMissing,
        [string]$InitialContent = ""
    )

    $path = Join-Path $RepoRoot $RelativePath

    if (-not (Test-Path -LiteralPath $path)) {
        if (-not $CreateIfMissing) {
            Write-Host "Skipping missing file: $RelativePath"
            return
        }

        Write-Utf8NoBomLf -Path $path -Content $InitialContent
        Write-Host "Created file: $RelativePath"
    }

    $existing = Read-TextOrEmpty -Path $path

    if ($existing -match [regex]::Escape($Needle)) {
        Write-Host "Entry already present: $RelativePath"
        return
    }

    $updated = $existing.TrimEnd() + "`n`n" + $AppendText.Trim() + "`n"
    Write-Utf8NoBomLf -Path $path -Content $updated
    Add-Unique -List $Touched -Value $RelativePath

    Write-Host "Updated: $RelativePath"
}

function Test-CommandExists {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Invoke-OptionalChecks {
    param([Parameter(Mandatory = $true)][string[]]$Files)

    Write-Host ""
    Write-Host "Running available checks..."

    Write-Host "Running git diff --check..."
    & git diff --check -- $Files
    if ($LASTEXITCODE -ne 0) {
        Fail "git diff --check failed"
    }

    if (Test-CommandExists "markdownlint-cli2") {
        Write-Host "Running markdownlint-cli2..."
        & markdownlint-cli2 $Files
        if ($LASTEXITCODE -ne 0) {
            Fail "markdownlint-cli2 failed"
        }
    }
    elseif (Test-CommandExists "markdownlint") {
        Write-Host "Running markdownlint..."
        & markdownlint $Files
        if ($LASTEXITCODE -ne 0) {
            Fail "markdownlint failed"
        }
    }
    else {
        Write-Host "No markdownlint command found; skipping markdown lint."
    }

    $linkCheckScripts = @(
        "scripts\check_markdown_links.ps1",
        "scripts\check_links.ps1",
        "scripts\run_markdown_link_checks.ps1"
    )

    $ranLinkScript = $false

    foreach ($candidate in $linkCheckScripts) {
        $candidatePath = Join-Path $RepoRoot $candidate
        if (Test-Path -LiteralPath $candidatePath) {
            Write-Host "Running link check script: $candidate"
            powershell -ExecutionPolicy Bypass -File $candidatePath
            if ($LASTEXITCODE -ne 0) {
                Fail "$candidate failed"
            }
            $ranLinkScript = $true
            break
        }
    }

    if (-not $ranLinkScript) {
        if (Test-CommandExists "lychee") {
            Write-Host "Running lychee..."
            & lychee $Files
            if ($LASTEXITCODE -ne 0) {
                Fail "lychee failed"
            }
        }
        else {
            Write-Host "No repo link-check script or lychee command found; skipping link check."
        }
    }
}

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    Fail "Repo root does not exist: $RepoRoot"
}

Push-Location $RepoRoot

try {
    Invoke-Git @("rev-parse", "--show-toplevel") | Out-Null

    $preStatus = (& git status --porcelain)
    if ($preStatus -and -not $AllowDirty) {
        Write-Host "Working tree has existing changes:"
        Write-Host $preStatus
        Fail "Refusing to mix exterior receipt audit filing with existing changes. Re-run with -AllowDirty only if intentional."
    }

    $currentBranch = (& git branch --show-current).Trim()

    if ($currentBranch -ne $BranchName) {
        $localBranch = (& git branch --list $BranchName).Trim()

        if ($localBranch) {
            Write-Host "Switching to existing branch: $BranchName"
            Invoke-Git @("switch", $BranchName)
        }
        else {
            Write-Host "Creating branch: $BranchName"
            Invoke-Git @("switch", "-c", $BranchName)
        }
    }
    else {
        Write-Host "Already on branch: $BranchName"
    }

    $Touched = New-Object System.Collections.Generic.List[string]

    $ReceiptRel = "docs/recomputation/RECEIPT_AUDIT_NOTE_v0_1_1_2026-07-07.md"
    $ReceiptPath = Join-Path $RepoRoot $ReceiptRel

    $ReceiptContent = @'
# Receipt Audit Note — Boundary-State Interoperability Checker v0.1.1

**Date:** 2026-07-07

---

## 1. Final Classification

**RECEIPT_AUDIT_COMPLETE — SOURCE ARTIFACTS NOT PROVIDED THIS PASS**

## 2. Scope and a Necessary Distinction

This note audits `boundary_state_interop_v0_1_1_recomputation_bundle.zip` as uploaded, cross-referenced against `EXECUTABLE_RECOMPUTATION_REPORT_v0_1_1.md` and `RECOMPUTATION_CHAIN_NOTE_v0_1_1_2026-07-06.md`.

**Important:** the uploaded bundle contains only the *fresh receipts* produced by a prior recomputation pass — `fresh_receipts/*.json`, `fresh_receipts/hashseed/*.json`, `DETERMINISTIC_INVENTORY_v0_1_1.tsv`, and `verify_shasums.py`. It does not contain `boundary_state_interop_evidence_packet_v0_1_1.zip`, `source_artifacts/boundary_state_interop_checker_v0_1_1.zip`, or any underlying fixture files. Without those, a from-scratch re-extraction and re-execution against the original checker source is not possible from this upload alone.

What follows is an **independent audit of the delivered evidence for internal consistency and arithmetic/hash correctness** — not a fourth from-scratch recomputation. Every check below was actually run against the actual bytes in the bundle in this session; none of it restates the prior reports' prose as if it were newly derived.

## 3. Audited Surfaces (all actually executed against the delivered bundle)

- Byte-identity of each `*_receipt_FRESH.json` against its corresponding `*_stdout_FRESH.txt`
- Independent per-fixture recount of canonical / adversarial / reviewer-regression results, using both `status_matches_expected` and `outcome_matches_expected` on every entry — not the summary counters alone
- Direct SHA256 hashing of all five `hashseed/seed_*.json` outputs (seeds 0, 1, 2, 42, and unset/OS-random)
- Full 90-row cross-check of `DETERMINISTIC_INVENTORY_v0_1_1.tsv` against the file/size/hash table embedded in §3 of `EXECUTABLE_RECOMPUTATION_REPORT_v0_1_1.md`
- Independent recomputation of the per-directory file-count breakdown from the raw TSV
- `checker_id` / `profile_revision` consistency sweep across every receipt and every nested per-fixture result
- Confirmation that all 9 stderr capture files are 0 bytes
- Line-by-line read of `verify_shasums.py` for logic correctness

## 4. Confirmed Results

- **Stdout/receipt identity:** all 4 pairs (`canonical`, `adversarial`, `reviewer_regression`, `accept_outcome_echo_probe`) are byte-identical — the receipts are the actual captured runtime output, not separately authored text.
- **Canonical suite:** independently recounted **18/18** (both match-fields true on every fixture) — agrees with the receipt's own `passed_count`.
- **Adversarial suite:** independently recounted **15/15**. `ADV_008` and `ADV_009` both resolve to `AUTHORITY_ALIAS_OF_RUNTIME_ATTESTATION_ATTEMPTED`, consistent with canonical fixture 13's outcome.
- **Reviewer regression suite:** independently recounted **1/1**.
- **RWF_ADV_A:** receipt confirms `validation_phase: SEMANTIC`, violations `NONOPERATIVE_EXTENSION_FIELD_CONTAINS_PROTECTED_SEMANTICS` and `UNDECLARED_EXTENSION_SEMANTIC_EXPANSION_ATTEMPTED` — not a schema/path failure. (The fixture's underlying free-text wording is not present in this bundle, so the specific paraphrase quoted in §10 of the executable report could not itself be re-inspected this pass — only the checker's resulting classification, which matches.)
- **Accept-outcome independence:** the canary `expected_outcome: "RWF_SHOULD_NOT_BE_ECHOED"` does not appear anywhere in the computed `outcome` (`ATTESTATION_REFERENCED_AS_EXISTENCE_EVIDENCE_ONLY`); `status_matches_expected: true`, `outcome_matches_expected: false` — the correct, passing shape for this probe.
- **PYTHONHASHSEED determinism:** all five `seed_*.json` files hash to the identical SHA256 (`021102974c0d2dc6831311b3da7f6e4ef23ec74c795fcd3fb517561ed9661f3c`) — genuinely byte-identical, confirmed by direct hashing, not read off a claimed table.
- **Inventory table integrity:** all 90 rows of the raw TSV match the markdown-embedded table exactly — 0 missing, 0 extra, 0 hash/size mismatches. Per-directory counts (4 / 23 / 14 / 5 / 28 / 10 / 1 / 2 / 3 = 90) reproduce exactly from the TSV.
- **Version consistency:** every receipt and every nested per-fixture result declares the same `checker_id` (`BOUNDARY_STATE_INTEROPERABILITY_CHECKER_v0_1_1`) and `profile_revision` (`v0.1.4`) — no mixed-run contamination anywhere in the bundle.
- **`verify_shasums.py`:** reviewed line-by-line — case-insensitive hash comparison, correct handling of the binary-mode `*` prefix, correct self-exclusion semantics for "on disk but unlisted." No defect found. (Not executed this pass — the evidence-packet files it operates on were not part of this upload.)
- **Stderr:** all 9 stderr captures (4 primary runs + 5 hashseed runs) confirmed 0 bytes.

## 5. Relationship to Prior Reports

Every claim in `RECOMPUTATION_CHAIN_NOTE_v0_1_1_2026-07-06.md` §4 and `EXECUTABLE_RECOMPUTATION_REPORT_v0_1_1.md` that concerns the receipts, the inventory, or the determinism probe is corroborated by this pass through direct, independent recomputation of the delivered bytes — not by re-reading their prose. No discrepancy was found anywhere.

Claims in those two reports that concern the evidence-packet ZIP, the source-artifact ZIPs, or the checker `.py` source itself (top-level `SHA256SUMS.txt` verification, `EVIDENCE_PACKET_MANIFEST_v0_1_1.json` hash cross-check, nested `checker_v0_1_1/SHA256SUMS.txt`, `CHECKER_ID`/`PROFILE_REVISION` source inspection, stale-marker scan) are **not** independently re-confirmed by this pass, because those files were not part of this upload.

## 6. What Would Close the Gap

A genuine fourth-pass, from-scratch recomputation would need — in addition to what was uploaded here — `boundary_state_interop_evidence_packet_v0_1_1.zip` and/or `source_artifacts/boundary_state_interop_checker_v0_1_1.zip` (the actual checker source and fixtures), so the suites can be re-run against a fresh extraction rather than audited from receipts alone.

## 7. Open Item Carried Forward (Unchanged)

The structural observation in §13 of `EXECUTABLE_RECOMPUTATION_REPORT_v0_1_1.md` — that `_profile_binding_violations()` does not separately gate on a standalone `profile_revision` mismatch — remains untested by any pass to date, including this one, since resolving it requires the checker source plus a constructed fixture that isolates that field. It is not a finding against the current suite results.

## 8. Non-Claims

This note does not establish truth, correctness, compliance, safety, authority, approval, production readiness, reliance sufficiency, legal sufficiency, operational sufficiency, institutional sufficiency, market readiness, or exhaustive adversarial coverage. It confirms internal consistency and arithmetic/hash correctness of the delivered receipts only.

## 9. Closeout Statement

No discrepancy found in any audited surface. The existing State Lock (v0.1.1 recomputed baseline; v0.1.2 not opened) is unaffected — this pass surfaced no new behavioral counterexample and neither expands nor contracts checker scope.

*Soli Deo Gloria.*
'@

    Write-Utf8NoBomLf -Path $ReceiptPath -Content $ReceiptContent
    Add-Unique -List $Touched -Value $ReceiptRel
    Write-Host "Created/updated receipt audit note: $ReceiptRel"

    $ReceiptRootLink = "docs/recomputation/RECEIPT_AUDIT_NOTE_v0_1_1_2026-07-07.md"
    $ReceiptLocalLink = "RECEIPT_AUDIT_NOTE_v0_1_1_2026-07-07.md"
    $ReceiptDoctrineLink = "../recomputation/RECEIPT_AUDIT_NOTE_v0_1_1_2026-07-07.md"
    $Needle = "RECEIPT_AUDIT_NOTE_v0_1_1_2026-07-07.md"

    $RecomputationReadmeInitial = @'
# Recomputations and Exterior Audits

This directory collects recomputation notes, receipt audits, and related exterior evidence for Fork releases and packets.
'@

    $RecomputationReadmeSection = @"
## Exterior Receipt Audits

- [Receipt Audit Note v0.1.1 — 2026-07-07]($ReceiptLocalLink) records an independent exterior audit of the boundary-state interop v0.1.1 recomputation receipt bundle. This pass confirmed receipt/stdout byte identity, suite recounts, PYTHONHASHSEED determinism, deterministic inventory integrity, version consistency, and zero-byte stderr captures. It is explicitly a receipt/internal-consistency audit, not a fourth from-source recomputation, because source artifacts and fixture files were not provided in this pass.
"@

    Append-IfMissing `
        -RelativePath "docs/recomputation/README.md" `
        -Needle $Needle `
        -AppendText $RecomputationReadmeSection `
        -Touched $Touched `
        -CreateIfMissing `
        -InitialContent $RecomputationReadmeInitial

    $ReviewIndexSection = @"
## Exterior Receipt Audit — Boundary-State Interop v0.1.1

- [Receipt Audit Note v0.1.1 — 2026-07-07]($ReceiptRootLink) records an independent exterior audit of the recomputation receipt bundle. It strengthens the v0.1.1 recomputation chain by confirming internal consistency of delivered receipts, deterministic hashseed output, inventory integrity, version consistency, and zero-byte stderr captures. It is not classified as a fourth from-source recomputation because source artifacts were not provided in this pass.
"@

    Append-IfMissing `
        -RelativePath "PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md" `
        -Needle $Needle `
        -AppendText $ReviewIndexSection `
        -Touched $Touched

    $ReviewerStartSection = @"
## Exterior Receipt Audit

The [Receipt Audit Note v0.1.1 — 2026-07-07]($ReceiptRootLink) should be read as an exterior receipt/internal-consistency audit. It corroborates the delivered recomputation receipts but does not replace a from-source recomputation using the evidence packet and checker source artifacts.
"@

    Append-IfMissing `
        -RelativePath "REVIEWER_START_HERE_v0_1.md" `
        -Needle $Needle `
        -AppendText $ReviewerStartSection `
        -Touched $Touched

    $DoctrineSection = @"
## Exterior Receipt Audit Evidence

The [Receipt Audit Note v0.1.1 — 2026-07-07]($ReceiptDoctrineLink) is an exterior receipt/internal-consistency audit supporting Fork's independent evidentiary capability doctrine. It confirms that delivered recomputation receipts are internally consistent and deterministic, while preserving the distinction between receipt audit and from-source recomputation.
"@

    Append-IfMissing `
        -RelativePath "docs/doctrine/FORK_INDEPENDENT_EVIDENTIARY_CAPABILITY_v0_1.md" `
        -Needle $Needle `
        -AppendText $DoctrineSection `
        -Touched $Touched

    $Files = @($Touched | Select-Object -Unique)

    if ($Files.Count -eq 0) {
        Write-Host "No files changed."
        Invoke-Git @("status", "-sb")
        exit 0
    }

    Invoke-OptionalChecks -Files $Files

    Write-Host ""
    Write-Host "Preparing diff..."
    & git add -N -- $Files 2>$null

    Write-Host ""
    Write-Host "git status -sb"
    Invoke-Git @("status", "-sb")

    Write-Host ""
    Write-Host "git diff --stat"
    & git diff --stat -- $Files

    Write-Host ""
    Write-Host "git diff"
    & git diff -- $Files

    Write-Host ""
    Write-Host "Staging files..."
    $addArgs = @("add", "--") + $Files
    Invoke-Git $addArgs

    $staged = (& git diff --cached --name-only)
    if (-not $staged) {
        Write-Host "No staged changes to commit."
        Invoke-Git @("status", "-sb")
        exit 0
    }

    Write-Host ""
    Write-Host "Staged files:"
    Write-Host $staged

    Invoke-Git @("commit", "-m", "Add exterior receipt audit note for boundary-state interop v0.1.1")

    if ($NoPush) {
        Write-Host "NoPush specified; skipping push."
    }
    else {
        Invoke-Git @("push", "-u", "origin", $BranchName)
    }

    Write-Host ""
    Write-Host "Done."
    Invoke-Git @("status", "-sb")
}
finally {
    Pop-Location
}