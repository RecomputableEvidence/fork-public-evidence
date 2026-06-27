param(
    [switch]$SkipPermutation,
    [switch]$NoVerifyRun,
    [switch]$VerboseOutput
)

$ErrorActionPreference = "Stop"

Write-Host "== ESAL v0.1 Conformance Harness =="

# --------------------------------------------------------------------
# Claim boundary
# --------------------------------------------------------------------

$NonClaims = @(
    "production completeness",
    "legal sufficiency",
    "compliance sufficiency",
    "authorization correctness",
    "external governance validity",
    "endorsement",
    "approval",
    "safety",
    "truth",
    "independent implementation convergence"
)

# --------------------------------------------------------------------
# Safety checks
# --------------------------------------------------------------------

if (!(Test-Path ".git")) {
    throw "Run this script from the repository root."
}

$RequiredPaths = @(
    "reference\esal",
    "esal-tests",
    "tools\esal_verify.ps1",
    "tools\Test-EsalPermutationInvariance.ps1",
    "reports\ESAL_v0_1_EXPECTED_OUTPUTS.md"
)

foreach ($Path in $RequiredPaths) {
    if (!(Test-Path $Path)) {
        throw "Required path missing: $Path"
    }
}

New-Item -ItemType Directory -Force -Path "reports" | Out-Null

# --------------------------------------------------------------------
# Expected ESAL v0.1 surface
# --------------------------------------------------------------------

$ExpectedDistribution = [ordered]@{
    PASS = 4
    G    = 3
    S    = 2
    D    = 1
}

$ExpectedFixtures = @(
    [ordered]@{
        CorpusGroup = "adversarial"
        Log = "log2-constraints-tighten.jsonl"
        Classification = "G"
        Fingerprint = $null
        FingerprintPresent = $false
        ExceptionClass = "GovernanceError"
        MessageContains = "authority inflation without explicit expansion delta: translate"
    },
    [ordered]@{
        CorpusGroup = "adversarial"
        Log = "log4-constraint-violation.jsonl"
        Classification = "G"
        Fingerprint = "bee2ca4f6ef180c915ea84c1aad8fb68f1229fa549585103197f499889736e44"
        FingerprintPresent = $true
        ExceptionClass = $null
        MessageContains = "replayable governance-invalid state"
    },
    [ordered]@{
        CorpusGroup = "adversarial"
        Log = "log5-authority-inflation.jsonl"
        Classification = "G"
        Fingerprint = $null
        FingerprintPresent = $false
        ExceptionClass = "GovernanceError"
        MessageContains = "authority inflation without explicit expansion delta: write:data"
    },
    [ordered]@{
        CorpusGroup = "adversarial"
        Log = "log6-lineage-truncation.jsonl"
        Classification = "S"
        Fingerprint = $null
        FingerprintPresent = $false
        ExceptionClass = "StructuralError"
        MessageContains = "unknown parent_bdr_id: bdr-missing-000"
    },
    [ordered]@{
        CorpusGroup = "adversarial"
        Log = "log7-event-reordering.jsonl"
        Classification = "D"
        Fingerprint = $null
        FingerprintPresent = $false
        ExceptionClass = "DeterminismError"
        MessageContains = "event_id conflict with differing event content"
    },
    [ordered]@{
        CorpusGroup = "canonical"
        Log = "C-001-placeholder.jsonl"
        Classification = "PASS"
        Fingerprint = "39fde2d6cb76d9409fdf09cb5e76ab2ba8b7174b430cb19c455038f2ded37bb1"
        FingerprintPresent = $true
        ExceptionClass = $null
        MessageContains = "minimal passing fixture"
    },
    [ordered]@{
        CorpusGroup = "canonical"
        Log = "log1-basic-A-B-C.jsonl"
        Classification = "PASS"
        Fingerprint = "6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836"
        FingerprintPresent = $true
        ExceptionClass = $null
        MessageContains = "canonical baseline trace"
    },
    [ordered]@{
        CorpusGroup = "canonical"
        Log = "log2-constraints-tighten.jsonl"
        Classification = "PASS"
        Fingerprint = "50b3d57de240108c39ab25be712114f6efb9ef0903fe1661a931e99fe4fc8393"
        FingerprintPresent = $true
        ExceptionClass = $null
        MessageContains = "valid constraint tightening trace"
    },
    [ordered]@{
        CorpusGroup = "canonical"
        Log = "log3-obligations-accumulate.jsonl"
        Classification = "PASS"
        Fingerprint = "95659c757320ac0c0db79154e4f7d06cd9db0284cf2d2413d421c238ccdaf5bb"
        FingerprintPresent = $true
        ExceptionClass = $null
        MessageContains = "valid obligation accumulation trace"
    },
    [ordered]@{
        CorpusGroup = "malformed"
        Log = "log8-schema-invalid.jsonl"
        Classification = "S"
        Fingerprint = $null
        FingerprintPresent = $false
        ExceptionClass = "StructuralError"
        MessageContains = "missing event_id"
    }
)

$ExpectedPermutation = [ordered]@{
    TargetLog = "esal-tests\canonical\log1-basic-A-B-C.jsonl"
    Iterations = 50
    Seed = 1701
    Classification = "PASS"
    Fingerprint = "6b38d8a5a586052c68cb767a6e44fe583c62e952bf1df54f3f4cf7763870a836"
    CanonicalEventsHash = "a50c88fabb07842722f0251721dab5ed4fc0a175e283c8bdb8e20f7f5cb85878"
    RequiredOutputFragment = "PASS: 50 permutations preserved canonical hash, state, fingerprint, and classification."
}

# --------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------

function Get-GitValue {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Args
    )

    $Value = & git @Args 2>$null
    if ($LASTEXITCODE -ne 0) {
        return ""
    }

    return ($Value | Select-Object -First 1).Trim()
}

function Get-PropertyValue {
    param(
        [Parameter(Mandatory = $true)]
        $Object,

        [Parameter(Mandatory = $true)]
        [string[]]$Names
    )

    if ($null -eq $Object) {
        return $null
    }

    foreach ($Name in $Names) {
        foreach ($Property in $Object.PSObject.Properties) {
            if ($Property.Name -ieq $Name) {
                return $Property.Value
            }
        }
    }

    return $null
}

function ConvertTo-FlatEntries {
    param(
        [Parameter(Mandatory = $true)]
        $Node,

        [int]$Depth = 0
    )

    if ($Depth -gt 12 -or $null -eq $Node) {
        return @()
    }

    $Entries = @()

    if ($Node -is [System.Array]) {
        foreach ($Item in $Node) {
            $Entries += ConvertTo-FlatEntries -Node $Item -Depth ($Depth + 1)
        }
        return $Entries
    }

    if ($Node -is [System.Collections.IEnumerable] -and -not ($Node -is [string]) -and -not ($Node -is [pscustomobject])) {
        foreach ($Item in $Node) {
            $Entries += ConvertTo-FlatEntries -Node $Item -Depth ($Depth + 1)
        }
        return $Entries
    }

    $Classification = Get-PropertyValue -Object $Node -Names @("classification", "Classification", "class", "result")
    $Log = Get-PropertyValue -Object $Node -Names @("log", "Log", "filename", "file", "path", "name", "test")

    if ($Classification -and $Log) {
        $Entries += $Node
    }

    foreach ($Property in $Node.PSObject.Properties) {
        if ($Property.Value -is [pscustomobject] -or $Property.Value -is [System.Array]) {
            $Entries += ConvertTo-FlatEntries -Node $Property.Value -Depth ($Depth + 1)
        }
    }

    return $Entries
}

function Normalize-Fingerprint {
    param($Value)

    if ($null -eq $Value) {
        return $null
    }

    $Text = "$Value".Trim()

    if ($Text -eq "" -or $Text -ieq "None" -or $Text -ieq "null") {
        return $null
    }

    return $Text
}

function Get-ExceptionText {
    param($Entry)

    $Exception = Get-PropertyValue -Object $Entry -Names @("exception", "Exception", "error", "Error", "message", "Message")

    if ($null -eq $Exception) {
        return ""
    }

    if ($Exception -is [string]) {
        return $Exception
    }

    $Type = Get-PropertyValue -Object $Exception -Names @("type", "class", "name", "exception_type")
    $Message = Get-PropertyValue -Object $Exception -Names @("message", "detail", "text")

    if ($Type -and $Message) {
        return "$Type`: $Message"
    }

    return ($Exception | ConvertTo-Json -Compress -Depth 10)
}

function Find-MatchingEntry {
    param(
        [Parameter(Mandatory = $true)]
        [array]$Entries,

        [Parameter(Mandatory = $true)]
        [hashtable]$Expected
    )

    $ExpectedLog = Split-Path $Expected.Log -Leaf
    $ExpectedClass = $Expected.Classification

    $Candidates = @()

    foreach ($Entry in $Entries) {
        $ActualLogRaw = Get-PropertyValue -Object $Entry -Names @("log", "Log", "filename", "file", "path", "name", "test")
        $ActualClass = Get-PropertyValue -Object $Entry -Names @("classification", "Classification", "class", "result")

        if (-not $ActualLogRaw -or -not $ActualClass) {
            continue
        }

        $ActualLog = Split-Path "$ActualLogRaw" -Leaf

        if ($ActualLog -eq $ExpectedLog -and "$ActualClass" -eq $ExpectedClass) {
            $Candidates += $Entry
        }
    }

    if ($Candidates.Count -eq 1) {
        return $Candidates[0]
    }

    if ($Candidates.Count -gt 1) {
        foreach ($Candidate in $Candidates) {
            $CandidatePath = "$(Get-PropertyValue -Object $Candidate -Names @("path", "file", "log", "Log", "filename", "name", "test"))"
            if ($CandidatePath -match [regex]::Escape($Expected.CorpusGroup)) {
                return $Candidate
            }
        }

        return $Candidates[0]
    }

    return $null
}

function Add-Issue {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.Generic.List[string]]$Issues,

        [Parameter(Mandatory = $true)]
        [string]$Message
    )

    $Issues.Add($Message) | Out-Null
}

# --------------------------------------------------------------------
# Metadata
# --------------------------------------------------------------------

$StartedUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$Branch = Get-GitValue @("branch", "--show-current")
$Commit = Get-GitValue @("rev-parse", "HEAD")
$ReleaseTag = "esal-v0.1-rc6"
$ReleaseTagCommit = Get-GitValue @("rev-parse", "$ReleaseTag^{commit}")

if ([string]::IsNullOrWhiteSpace($ReleaseTagCommit)) {
    $ReleaseTagCommit = "UNKNOWN"
}

# --------------------------------------------------------------------
# Execute reference verification
# --------------------------------------------------------------------

$VerifyExitCode = 0
$VerifyOutput = @()

if (-not $NoVerifyRun) {
    Write-Host ""
    Write-Host "Running ESAL reference verification..."

    $VerifyOutput = & powershell .\tools\esal_verify.ps1 2>&1
    $VerifyExitCode = $LASTEXITCODE

    if ($VerboseOutput) {
        $VerifyOutput | Out-Host
    }

    if ($VerifyExitCode -ne 0) {
        throw "ESAL verification script failed with exit code $VerifyExitCode."
    }
}
else {
    Write-Host ""
    Write-Host "Skipping ESAL reference verification because -NoVerifyRun was supplied."
}

if (!(Test-Path "reports\latest-report.json")) {
    throw "Expected report missing: reports\latest-report.json"
}

$LatestReportRaw = Get-Content "reports\latest-report.json" -Raw
$LatestReport = $LatestReportRaw | ConvertFrom-Json
$Entries = @(ConvertTo-FlatEntries -Node $LatestReport)

if ($Entries.Count -eq 0) {
    throw "Could not locate fixture entries in reports\latest-report.json. The report schema may have changed."
}

# --------------------------------------------------------------------
# Distribution checks
# --------------------------------------------------------------------

$ActualDistribution = [ordered]@{
    PASS = 0
    G    = 0
    S    = 0
    D    = 0
}

foreach ($Entry in $Entries) {
    $Classification = "$(Get-PropertyValue -Object $Entry -Names @("classification", "Classification", "class", "result"))"

    if ($ActualDistribution.Contains($Classification)) {
        $ActualDistribution[$Classification] = $ActualDistribution[$Classification] + 1
    }
}

$DistributionIssues = New-Object "System.Collections.Generic.List[string]"

foreach ($Key in $ExpectedDistribution.Keys) {
    if ($ActualDistribution[$Key] -ne $ExpectedDistribution[$Key]) {
        Add-Issue -Issues $DistributionIssues -Message "Distribution mismatch for ${Key}: expected $($ExpectedDistribution[$Key]), actual $($ActualDistribution[$Key])."
    }
}

# --------------------------------------------------------------------
# Fixture checks
# --------------------------------------------------------------------

$FixtureResults = @()
$FixturePassCount = 0

foreach ($Expected in $ExpectedFixtures) {
    $Issues = New-Object "System.Collections.Generic.List[string]"
    $Entry = Find-MatchingEntry -Entries $Entries -Expected $Expected

    $Actual = [ordered]@{
        log = $null
        classification = $null
        fingerprint = $null
        exception = $null
    }

    if ($null -eq $Entry) {
        Add-Issue -Issues $Issues -Message "Expected fixture not found: $($Expected.CorpusGroup)/$($Expected.Log) classification $($Expected.Classification)."
    }
    else {
        $ActualLog = Get-PropertyValue -Object $Entry -Names @("log", "Log", "filename", "file", "path", "name", "test")
        $ActualClass = Get-PropertyValue -Object $Entry -Names @("classification", "Classification", "class", "result")
        $ActualFingerprint = Normalize-Fingerprint (Get-PropertyValue -Object $Entry -Names @("fingerprint", "Fingerprint", "state_fingerprint", "hash"))
        $ActualExceptionText = Get-ExceptionText -Entry $Entry

        $Actual.log = "$ActualLog"
        $Actual.classification = "$ActualClass"
        $Actual.fingerprint = $ActualFingerprint
        $Actual.exception = $ActualExceptionText

        if ("$ActualClass" -ne $Expected.Classification) {
            Add-Issue -Issues $Issues -Message "Classification mismatch: expected $($Expected.Classification), actual $ActualClass."
        }

        if ($Expected.FingerprintPresent -and -not $ActualFingerprint) {
            Add-Issue -Issues $Issues -Message "Expected fingerprint to be present, but actual fingerprint was None."
        }

        if (-not $Expected.FingerprintPresent -and $ActualFingerprint) {
            Add-Issue -Issues $Issues -Message "Expected fingerprint to be None, but actual fingerprint was $ActualFingerprint."
        }

        if ($Expected.FingerprintPresent -and $Expected.Fingerprint -and $ActualFingerprint -ne $Expected.Fingerprint) {
            Add-Issue -Issues $Issues -Message "Fingerprint mismatch: expected $($Expected.Fingerprint), actual $ActualFingerprint."
        }

        if ($Expected.ExceptionClass) {
            if ($ActualExceptionText -notmatch [regex]::Escape($Expected.ExceptionClass)) {
                Add-Issue -Issues $Issues -Message "Expected exception class $($Expected.ExceptionClass), actual exception text: $ActualExceptionText"
            }

            if ($Expected.MessageContains -and $ActualExceptionText -notmatch [regex]::Escape($Expected.MessageContains)) {
                Add-Issue -Issues $Issues -Message "Expected exception message fragment '$($Expected.MessageContains)', actual exception text: $ActualExceptionText"
            }
        }
    }

    $Passed = ($Issues.Count -eq 0)

    if ($Passed) {
        $FixturePassCount += 1
    }

    $FixtureResults += [ordered]@{
        corpus_group = $Expected.CorpusGroup
        log = $Expected.Log
        expected = [ordered]@{
            classification = $Expected.Classification
            fingerprint = $Expected.Fingerprint
            fingerprint_present = $Expected.FingerprintPresent
            exception_class = $Expected.ExceptionClass
            message_contains = $Expected.MessageContains
        }
        actual = $Actual
        passed = $Passed
        issues = @($Issues)
    }
}

# --------------------------------------------------------------------
# Permutation invariance check
# --------------------------------------------------------------------

$PermutationResult = [ordered]@{
    skipped = $SkipPermutation.IsPresent
    exit_code = $null
    passed = $false
    issues = @()
    expected = $ExpectedPermutation
    output_excerpt = @()
}

if (-not $SkipPermutation) {
    Write-Host ""
    Write-Host "Running ESAL permutation invariance check..."

    $PermutationOutput = & .\tools\Test-EsalPermutationInvariance.ps1 2>&1
    $PermutationExitCode = $LASTEXITCODE

    if ($VerboseOutput) {
        $PermutationOutput | Out-Host
    }

    $PermutationIssues = New-Object "System.Collections.Generic.List[string]"
    $PermutationText = ($PermutationOutput -join "`n")

    if ($PermutationExitCode -ne 0) {
        Add-Issue -Issues $PermutationIssues -Message "Permutation invariance script failed with exit code $PermutationExitCode."
    }

    if ($PermutationText -notmatch [regex]::Escape($ExpectedPermutation.RequiredOutputFragment)) {
        Add-Issue -Issues $PermutationIssues -Message "Required permutation PASS fragment not found."
    }

    if ($PermutationText -notmatch [regex]::Escape($ExpectedPermutation.Fingerprint)) {
        Add-Issue -Issues $PermutationIssues -Message "Expected permutation fingerprint not found."
    }

    if ($PermutationText -notmatch [regex]::Escape($ExpectedPermutation.CanonicalEventsHash)) {
        Add-Issue -Issues $PermutationIssues -Message "Expected canonical events hash not found."
    }

    $PermutationResult.exit_code = $PermutationExitCode
    $PermutationResult.passed = ($PermutationIssues.Count -eq 0)
    $PermutationResult.issues = @($PermutationIssues)
    $PermutationResult.output_excerpt = @($PermutationOutput | Select-Object -Last 12)
}
else {
    $PermutationResult.passed = $true
}

# --------------------------------------------------------------------
# Final result
# --------------------------------------------------------------------

$AllIssues = New-Object "System.Collections.Generic.List[string]"

foreach ($Issue in $DistributionIssues) {
    $AllIssues.Add($Issue) | Out-Null
}

foreach ($FixtureResult in $FixtureResults) {
    foreach ($Issue in $FixtureResult.issues) {
        $AllIssues.Add("$($FixtureResult.corpus_group)/$($FixtureResult.log): $Issue") | Out-Null
    }
}

foreach ($Issue in $PermutationResult.issues) {
    $AllIssues.Add("permutation: $Issue") | Out-Null
}

$ConformancePassed = ($AllIssues.Count -eq 0)

$CompletedUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$Report = [ordered]@{
    artifact_id = "ESAL-CONFORMANCE-REPORT-v0.1"
    generated_utc = $CompletedUtc
    started_utc = $StartedUtc
    branch = $Branch
    commit = $Commit
    release_candidate_tag = $ReleaseTag
    release_candidate_tag_commit = $ReleaseTagCommit
    result = $(if ($ConformancePassed) { "CONFORMANCE_PASS" } else { "CONFORMANCE_FAIL" })
    expected_distribution = $ExpectedDistribution
    actual_distribution = $ActualDistribution
    distribution_passed = ($DistributionIssues.Count -eq 0)
    fixture_count = $ExpectedFixtures.Count
    fixture_pass_count = $FixturePassCount
    fixture_results = $FixtureResults
    permutation = $PermutationResult
    non_claims = $NonClaims
    issues = @($AllIssues)
}

$ReportPath = "reports\ESAL_v0_1_CONFORMANCE_REPORT.json"
$ReportJson = $Report | ConvertTo-Json -Depth 30
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$ReportFullPath = Join-Path (Get-Location) $ReportPath
$ReportDirectory = Split-Path $ReportFullPath -Parent

if (!(Test-Path $ReportDirectory)) {
    New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
}

[System.IO.File]::WriteAllText($ReportFullPath, $ReportJson + "`n", $Utf8NoBom)

Write-Host ""
Write-Host "== ESAL v0.1 Conformance Result =="

if ($ConformancePassed) {
    Write-Host "CONFORMANCE_PASS"
}
else {
    Write-Host "CONFORMANCE_FAIL"
}

Write-Host ""
Write-Host "Distribution:"
Write-Host "  PASS: actual $($ActualDistribution.PASS), expected $($ExpectedDistribution.PASS)"
Write-Host "  G:    actual $($ActualDistribution.G), expected $($ExpectedDistribution.G)"
Write-Host "  S:    actual $($ActualDistribution.S), expected $($ExpectedDistribution.S)"
Write-Host "  D:    actual $($ActualDistribution.D), expected $($ExpectedDistribution.D)"
Write-Host ""
Write-Host "Fixtures: $FixturePassCount / $($ExpectedFixtures.Count) passed"

if (-not $SkipPermutation) {
    Write-Host "Permutation: $(if ($PermutationResult.passed) { "passed" } else { "failed" })"
}
else {
    Write-Host "Permutation: skipped"
}

Write-Host "Report written: $ReportPath"

if (-not $ConformancePassed) {
    Write-Host ""
    Write-Host "Issues:"
    foreach ($Issue in $AllIssues) {
        Write-Host "  - $Issue"
    }

    exit 1
}

exit 0

