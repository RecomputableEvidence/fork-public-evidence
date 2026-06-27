param(
    [switch]$SkipConformanceRun
)

$ErrorActionPreference = 'Stop'

Write-Host '== Update ESAL v0.1 Docs for Conformance Harness =='

if (!(Test-Path '.git')) {
    throw 'Run this script from the repository root.'
}

$RequiredPaths = @(
    'reports\ESAL_v0_1_RELEASE_RECORD.md',
    'docs\ESAL_CONFORMANCE_KIT_v0_1.md',
    'docs\ESAL_v0_1_START_HERE.md',
    'reports\ESAL_v0_1_EXPECTED_OUTPUTS.md',
    'tools\New-EsalV01DocumentationPack.ps1',
    'tools\Test-EsalConformance.ps1'
)

foreach ($Path in $RequiredPaths) {
    if (!(Test-Path $Path)) {
        throw "Required path missing: $Path"
    }
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $FullPath = (Resolve-Path $Path).Path
    $Normalized = $Content.Replace("`r`n", "`n").TrimEnd() + "`n"
    [System.IO.File]::WriteAllText($FullPath, $Normalized, $Utf8NoBom)
}

function Join-Lines {
    param([string[]]$Lines)
    return ($Lines -join "`n")
}

function Add-After {
    param(
        [string]$Text,
        [string]$Anchor,
        [string]$Insert,
        [string]$Marker,
        [string]$Label
    )

    if ($Text.Contains($Marker)) {
        Write-Host "Already present: $Label"
        return $Text
    }

    if (-not $Text.Contains($Anchor)) {
        throw "Anchor not found for ${Label}: $Anchor"
    }

    Write-Host "Patching: $Label"
    return $Text.Replace($Anchor, "$Anchor`n$Insert")
}

function Add-Before {
    param(
        [string]$Text,
        [string]$Anchor,
        [string]$Insert,
        [string]$Marker,
        [string]$Label
    )

    if ($Text.Contains($Marker)) {
        Write-Host "Already present: $Label"
        return $Text
    }

    if (-not $Text.Contains($Anchor)) {
        throw "Anchor not found for ${Label}: $Anchor"
    }

    Write-Host "Patching: $Label"
    return $Text.Replace($Anchor, "$Insert`n`n$Anchor")
}

function Patch-ReleaseRecord {
    $Path = 'reports\ESAL_v0_1_RELEASE_RECORD.md'
    $Text = Get-Content $Path -Raw

    $Text = Add-After $Text '- `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`' '- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`' '- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`' "$Path package contents conformance report"
    $Text = Add-After $Text '- `tools/Test-EsalPermutationInvariance.ps1`' '- `tools/Test-EsalConformance.ps1`' '- `tools/Test-EsalConformance.ps1`' "$Path package contents conformance harness"
    $Text = Add-After $Text '.\tools\Test-EsalPermutationInvariance.ps1' '.\tools\Test-EsalConformance.ps1' '.\tools\Test-EsalConformance.ps1' "$Path reproduction command"

    $Section = Join-Lines @(
        '## Executable Conformance Evidence',
        '',
        'The ESAL v0.1 executable conformance harness is:',
        '',
        '```text',
        'tools/Test-EsalConformance.ps1',
        '```',
        '',
        'It checks the ESAL v0.1 reference oracle against the expected-output surface and writes:',
        '',
        '```text',
        'reports/ESAL_v0_1_CONFORMANCE_REPORT.json',
        '```',
        '',
        'A passing run emits:',
        '',
        '```text',
        'CONFORMANCE_PASS',
        '```',
        '',
        'This establishes executable reference-oracle conformance checking only. It does not establish independent implementation convergence.'
    )

    $Text = Add-Before $Text '## 7. Non-Claims' $Section '## Executable Conformance Evidence' "$Path executable conformance evidence section"

    Write-Utf8NoBom $Path $Text
}

function Patch-ConformanceKit {
    $Path = 'docs\ESAL_CONFORMANCE_KIT_v0_1.md'
    $Text = Get-Content $Path -Raw

    $Text = Add-After $Text '- `tools/Test-EsalPermutationInvariance.ps1`' '- `tools/Test-EsalConformance.ps1`' '- `tools/Test-EsalConformance.ps1`' "$Path required repository surface harness"
    $Text = Add-After $Text '- `reports/ESAL_v0_1_EXPECTED_OUTPUTS.md`' '- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`' '- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`' "$Path required repository surface report"
    $Text = Add-After $Text '.\tools\Test-EsalPermutationInvariance.ps1' '.\tools\Test-EsalConformance.ps1' '.\tools\Test-EsalConformance.ps1' "$Path reproduction command"

    $Section = Join-Lines @(
        '## Executable Conformance Harness',
        '',
        'The ESAL v0.1 conformance harness is:',
        '',
        '```text',
        'tools/Test-EsalConformance.ps1',
        '```',
        '',
        'It runs the reference verification, checks fixture-level classifications, fingerprints, exception expectations, runs permutation invariance, and writes:',
        '',
        '```text',
        'reports/ESAL_v0_1_CONFORMANCE_REPORT.json',
        '```',
        '',
        'A passing run emits:',
        '',
        '```text',
        'CONFORMANCE_PASS',
        '```',
        '',
        'This establishes executable reference-oracle conformance checking only. It does not establish independent implementation convergence.'
    )

    $Text = Add-Before $Text '## 4. Expected Classification Distribution' $Section '## Executable Conformance Harness' "$Path executable conformance harness section"

    Write-Utf8NoBom $Path $Text
}

function Patch-StartHere {
    $Path = 'docs\ESAL_v0_1_START_HERE.md'
    $Text = Get-Content $Path -Raw

    $Text = Add-After $Text '.\tools\Test-EsalPermutationInvariance.ps1' '.\tools\Test-EsalConformance.ps1' '.\tools\Test-EsalConformance.ps1' "$Path quick verification command"

    $Section = Join-Lines @(
        'The executable conformance harness is:',
        '',
        '```text',
        'tools/Test-EsalConformance.ps1',
        '```',
        '',
        'It writes:',
        '',
        '```text',
        'reports/ESAL_v0_1_CONFORMANCE_REPORT.json',
        '```'
    )

    $Text = Add-Before $Text '## 4. Core Claim Boundary' $Section 'The executable conformance harness is:' "$Path conformance navigation note"

    Write-Utf8NoBom $Path $Text
}

function Patch-ExpectedOutputs {
    $Path = 'reports\ESAL_v0_1_EXPECTED_OUTPUTS.md'
    $Text = Get-Content $Path -Raw

    $Section = Join-Lines @(
        'These expected outputs are checked by `tools/Test-EsalConformance.ps1`, which writes `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`.',
        '',
        'A passing conformance run emits `CONFORMANCE_PASS`.',
        '',
        'This establishes executable reference-oracle conformance checking only. It does not establish independent implementation convergence.'
    )

    $Text = Add-Before $Text '## 2. Expected Distribution' $Section 'These expected outputs are checked by `tools/Test-EsalConformance.ps1`' "$Path conformance harness note"

    Write-Utf8NoBom $Path $Text
}

function Patch-DocumentationPackGenerator {
    $Path = 'tools\New-EsalV01DocumentationPack.ps1'
    $Text = Get-Content $Path -Raw

    if (-not $Text.Contains('- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`')) {
        Write-Host "$Path generated package/report references need manual follow-up."
    }
    else {
        Write-Host "Already present: $Path generated package/report references"
    }

    if (-not $Text.Contains('- `tools/Test-EsalConformance.ps1`')) {
        Write-Host "$Path generated harness references need manual follow-up."
    }
    else {
        Write-Host "Already present: $Path generated harness references"
    }

    if (-not $Text.Contains('.\tools\Test-EsalConformance.ps1')) {
        Write-Host "$Path generated reproduction commands need manual follow-up."
    }
    else {
        Write-Host "Already present: $Path generated reproduction commands"
    }

    Write-Utf8NoBom $Path $Text
}

Patch-ReleaseRecord
Patch-ConformanceKit
Patch-StartHere
Patch-ExpectedOutputs
Patch-DocumentationPackGenerator

if (-not $SkipConformanceRun) {
    Write-Host ''
    Write-Host 'Running conformance harness...'
    .\tools\Test-EsalConformance.ps1
}
else {
    Write-Host ''
    Write-Host 'Skipping conformance harness because -SkipConformanceRun was supplied.'
}

Write-Host ''
Write-Host 'Updated ESAL v0.1 documentation for conformance harness.'
Write-Host ''
Write-Host 'Review:'
Write-Host '  git diff -- reports/ESAL_v0_1_RELEASE_RECORD.md'
Write-Host '  git diff -- docs/ESAL_CONFORMANCE_KIT_v0_1.md'
Write-Host '  git diff -- docs/ESAL_v0_1_START_HERE.md'
Write-Host '  git diff -- reports/ESAL_v0_1_EXPECTED_OUTPUTS.md'
Write-Host '  git diff -- tools/New-EsalV01DocumentationPack.ps1'
Write-Host '  git diff -- reports/ESAL_v0_1_CONFORMANCE_REPORT.json'
Write-Host ''
Write-Host 'Commit:'
Write-Host '  git add reports/ESAL_v0_1_RELEASE_RECORD.md docs/ESAL_CONFORMANCE_KIT_v0_1.md docs/ESAL_v0_1_START_HERE.md reports/ESAL_v0_1_EXPECTED_OUTPUTS.md tools/New-EsalV01DocumentationPack.ps1 reports/ESAL_v0_1_CONFORMANCE_REPORT.json tools/Update-EsalDocsForConformanceHarness.ps1'
Write-Host '  git commit -m "Document ESAL v0.1 conformance harness"'
Write-Host '  git push'
