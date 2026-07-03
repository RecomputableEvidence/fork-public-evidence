# scripts/check_no_mojibake_utf8_v0_1.ps1
# Repository-wide UTF-8/mojibake scan for reviewer-facing text files.
# Reads files with explicit UTF-8 to avoid Windows PowerShell 5.1 code-page ambiguity.

$ErrorActionPreference = "Stop"

function Fail($Message) { Write-Host "FAIL: $Message" -ForegroundColor Red; exit 1 }
function Pass($Message) { Write-Host "PASS: $Message" -ForegroundColor Green }

if (-not (Test-Path ".git")) { Fail "Run from repository root." }

$includeExtensions = @(".md", ".json", ".html", ".js", ".css", ".ps1", ".py", ".yml", ".yaml", ".txt")
$excludeDirFragments = @("\.git\", "\node_modules\", "\.venv\", "\venv\", "\__pycache__\")

$badCodepoints = @(
    0x00C3,
    0x00C2,
    0x00E2,
    0xFFFD
)

$hits = New-Object System.Collections.Generic.List[string]

$files = Get-ChildItem -Recurse -File | Where-Object {
    $ext = [System.IO.Path]::GetExtension($_.FullName)
    if ($includeExtensions -notcontains $ext) { return $false }

    $full = $_.FullName
    foreach ($frag in $excludeDirFragments) {
        if ($full -like "*$frag*") { return $false }
    }

    return $true
}

foreach ($file in $files) {
    try {
        $text = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    } catch {
        $hits.Add("$($file.FullName): unable to read as UTF-8: $($_.Exception.Message)")
        continue
    }

    foreach ($cp in $badCodepoints) {
        $ch = [char]$cp
        if ($text.Contains([string]$ch)) {
            $hits.Add("$($file.FullName): contains suspicious codepoint U+$('{0:X4}' -f $cp)")
        }
    }
}

if ($hits.Count -gt 0) {
    Write-Host ""
    Write-Host "Mojibake scan hits:" -ForegroundColor Yellow
    foreach ($hit in $hits) { Write-Host " - $hit" }
    Write-Host ""
    Fail "mojibake scan found $($hits.Count) issue(s)"
}

Pass "no mojibake patterns found in reviewer-facing text files"
