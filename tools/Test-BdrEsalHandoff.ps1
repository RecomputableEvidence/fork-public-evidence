param(
    [string]$ValidExamplePath = 'examples\bdr_esal_handoff\valid_vendor_risk_handoff_event.json',
    [string]$InvalidExamplePath = 'examples\bdr_esal_handoff\invalid_authority_inheritance_handoff_event.json',
    [string]$ReportPath = 'reports\BDR_ESAL_HANDOFF_VALIDATION_REPORT.json',
    [switch]$VerboseOutput
)

$ErrorActionPreference = 'Stop'

Write-Host '== BDR / ESAL Handoff Validator v0.1 =='

if (!(Test-Path '.git')) {
    throw 'Run this script from the repository root.'
}

$RequiredPaths = @(
    'docs\BDR_ESAL_HANDOFF_CONTRACT_v0_1.md',
    $ValidExamplePath,
    $InvalidExamplePath
)

foreach ($Path in $RequiredPaths) {
    if (!(Test-Path $Path)) {
        throw "Required path missing: $Path"
    }
}

New-Item -ItemType Directory -Force -Path 'reports' | Out-Null

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Get-GitValue {
    param([string[]]$Args)

    $Value = & git @Args 2>$null
    if ($LASTEXITCODE -ne 0) {
        return ''
    }

    return ($Value | Select-Object -First 1).Trim()
}

function Read-JsonFile {
    param([string]$Path)

    try {
        return Get-Content $Path -Raw | ConvertFrom-Json
    }
    catch {
        throw "Invalid JSON in ${Path}: $($_.Exception.Message)"
    }
}

function As-Array {
    param($Value)

    if ($null -eq $Value) {
        return @()
    }

    if ($Value -is [System.Array]) {
        return @($Value)
    }

    return @($Value)
}

function Add-Issue {
    param(
        [System.Collections.Generic.List[string]]$Issues,
        [string]$Message
    )

    $Issues.Add($Message) | Out-Null
}

function Has-NonEmptyString {
    param($Value)

    return ($null -ne $Value -and "$Value".Trim().Length -gt 0)
}

function Test-RequiredString {
    param(
        [System.Collections.Generic.List[string]]$Issues,
        $Object,
        [string]$PropertyName,
        [string]$Label
    )

    if (-not (Has-NonEmptyString $Object.$PropertyName)) {
        Add-Issue $Issues "Missing or empty required string: $Label.$PropertyName"
    }
}

function Test-RequiredArray {
    param(
        [System.Collections.Generic.List[string]]$Issues,
        $Object,
        [string]$PropertyName,
        [string]$Label
    )

    $Array = As-Array $Object.$PropertyName
    if ($Array.Count -eq 0) {
        Add-Issue $Issues "Missing or empty required array: $Label.$PropertyName"
    }
}

function Test-CommonSourceBdr {
    param(
        [System.Collections.Generic.List[string]]$Issues,
        $SourceBdr,
        [string]$Label
    )

    if ($null -eq $SourceBdr) {
        Add-Issue $Issues "Missing source_bdr in $Label"
        return
    }

    Test-RequiredString $Issues $SourceBdr 'bdr_id' $Label
    Test-RequiredString $Issues $SourceBdr 'boundary_id' $Label
    Test-RequiredString $Issues $SourceBdr 'source_boundary' $Label
    Test-RequiredString $Issues $SourceBdr 'target_boundary' $Label
    Test-RequiredString $Issues $SourceBdr 'transition_kind' $Label
    Test-RequiredArray $Issues $SourceBdr 'evidence_refs' $Label
    Test-RequiredArray $Issues $SourceBdr 'preserved_non_claims' $Label
}

function Test-ValidHandoff {
    param(
        [string]$Path,
        $Doc
    )

    $Issues = New-Object 'System.Collections.Generic.List[string]'

    if ($Doc.profile -ne 'BDR_ESAL_HANDOFF_CONTRACT_v0_1') {
        Add-Issue $Issues "Expected profile BDR_ESAL_HANDOFF_CONTRACT_v0_1, actual '$($Doc.profile)'"
    }

    if ($Doc.status -ne 'VALID_HANDOFF_EXAMPLE') {
        Add-Issue $Issues "Expected status VALID_HANDOFF_EXAMPLE, actual '$($Doc.status)'"
    }

    Test-RequiredString $Issues $Doc 'artifact_id' 'root'
    Test-CommonSourceBdr $Issues $Doc.source_bdr 'source_bdr'

    if ($null -eq $Doc.esal_event) {
        Add-Issue $Issues 'Missing esal_event'
    }
    else {
        Test-RequiredString $Issues $Doc.esal_event 'event_id' 'esal_event'
        Test-RequiredString $Issues $Doc.esal_event 'event_type' 'esal_event'
        Test-RequiredString $Issues $Doc.esal_event 'timestamp' 'esal_event'

        if ($Doc.esal_event.event_type -ne 'BDR_CREATED') {
            Add-Issue $Issues "Expected esal_event.event_type BDR_CREATED, actual '$($Doc.esal_event.event_type)'"
        }

        if ($null -eq $Doc.esal_event.body) {
            Add-Issue $Issues 'Missing esal_event.body'
        }
        else {
            $Body = $Doc.esal_event.body

            Test-RequiredString $Issues $Body 'bdr_id' 'esal_event.body'
            Test-RequiredString $Issues $Body 'boundary_id' 'esal_event.body'
            Test-RequiredArray $Issues $Body 'constraints' 'esal_event.body'
            Test-RequiredArray $Issues $Body 'obligations' 'esal_event.body'
            Test-RequiredArray $Issues $Body 'evidence_refs' 'esal_event.body'
            Test-RequiredArray $Issues $Body 'preserved_non_claims' 'esal_event.body'

            if ($Body.bdr_id -ne $Doc.source_bdr.bdr_id) {
                Add-Issue $Issues "BDR id mismatch: source_bdr.bdr_id '$($Doc.source_bdr.bdr_id)' vs esal_event.body.bdr_id '$($Body.bdr_id)'"
            }

            $Authority = As-Array $Body.authority
            if ($Authority.Count -gt 0) {
                Add-Issue $Issues "Valid handoff must not introduce ESAL authority. Found authority entries: $($Authority -join ', ')"
            }

            if ($Body.attempted_authority_inheritance -eq $true) {
                Add-Issue $Issues 'Valid handoff must not set attempted_authority_inheritance=true'
            }

            if ($Body.attempted_external_validity_transfer -eq $true) {
                Add-Issue $Issues 'Valid handoff must not set attempted_external_validity_transfer=true'
            }

            $ForbiddenTerms = @(
                'ESAL approves',
                'ESAL validates',
                'ESAL establishes compliance',
                'ESAL establishes legal sufficiency',
                'ESAL transfers upstream authority',
                'ESAL certifies external governance validity'
            )

            $BodyText = $Body | ConvertTo-Json -Depth 30 -Compress
            foreach ($Term in $ForbiddenTerms) {
                if ($BodyText -match [regex]::Escape($Term)) {
                    Add-Issue $Issues "Valid handoff contains forbidden authority/validity phrase: $Term"
                }
            }
        }
    }

    if ($null -eq $Doc.handoff_assertion) {
        Add-Issue $Issues 'Missing handoff_assertion'
    }
    else {
        if ($Doc.handoff_assertion.allowed -ne $true) {
            Add-Issue $Issues 'Valid handoff must have handoff_assertion.allowed=true'
        }

        Test-RequiredArray $Issues $Doc.handoff_assertion 'non_inheritance' 'handoff_assertion'
    }

    return [ordered]@{
        path = $Path
        expected = 'ACCEPT'
        actual = $(if ($Issues.Count -eq 0) { 'ACCEPT' } else { 'REJECT' })
        passed = ($Issues.Count -eq 0)
        issues = @($Issues)
    }
}

function Test-InvalidAuthorityInheritance {
    param(
        [string]$Path,
        $Doc
    )

    $Issues = New-Object 'System.Collections.Generic.List[string]'
    $DetectedAuthorityInheritance = $false
    $DetectedExternalValidityTransfer = $false
    $DetectedInvalidClaims = $false

    if ($Doc.profile -ne 'BDR_ESAL_HANDOFF_CONTRACT_v0_1') {
        Add-Issue $Issues "Expected profile BDR_ESAL_HANDOFF_CONTRACT_v0_1, actual '$($Doc.profile)'"
    }

    if ($Doc.status -ne 'INVALID_HANDOFF_EXAMPLE') {
        Add-Issue $Issues "Expected status INVALID_HANDOFF_EXAMPLE, actual '$($Doc.status)'"
    }

    Test-RequiredString $Issues $Doc 'artifact_id' 'root'
    Test-CommonSourceBdr $Issues $Doc.source_bdr 'source_bdr'

    if ($null -eq $Doc.attempted_esal_event) {
        Add-Issue $Issues 'Missing attempted_esal_event'
    }
    else {
        Test-RequiredString $Issues $Doc.attempted_esal_event 'event_id' 'attempted_esal_event'
        Test-RequiredString $Issues $Doc.attempted_esal_event 'event_type' 'attempted_esal_event'
        Test-RequiredString $Issues $Doc.attempted_esal_event 'timestamp' 'attempted_esal_event'

        if ($Doc.attempted_esal_event.event_type -ne 'BDR_CREATED') {
            Add-Issue $Issues "Expected attempted_esal_event.event_type BDR_CREATED, actual '$($Doc.attempted_esal_event.event_type)'"
        }

        if ($null -eq $Doc.attempted_esal_event.body) {
            Add-Issue $Issues 'Missing attempted_esal_event.body'
        }
        else {
            $Body = $Doc.attempted_esal_event.body

            Test-RequiredString $Issues $Body 'bdr_id' 'attempted_esal_event.body'
            Test-RequiredString $Issues $Body 'boundary_id' 'attempted_esal_event.body'
            Test-RequiredArray $Issues $Body 'evidence_refs' 'attempted_esal_event.body'

            $Authority = As-Array $Body.authority
            if ($Authority.Count -gt 0) {
                $DetectedAuthorityInheritance = $true
            }

            if ($Body.attempted_authority_inheritance -eq $true) {
                $DetectedAuthorityInheritance = $true
            }

            if ($Body.attempted_external_validity_transfer -eq $true) {
                $DetectedExternalValidityTransfer = $true
            }

            $InvalidClaims = As-Array $Body.invalid_derived_claims
            if ($InvalidClaims.Count -gt 0) {
                $DetectedInvalidClaims = $true
            }

            $BodyText = $Body | ConvertTo-Json -Depth 30 -Compress
            $ForbiddenPatterns = @(
                'ESAL replay establishes',
                'ESAL fingerprint establishes',
                'transfers into ESAL state',
                'certify:compliance',
                'approve:vendor'
            )

            foreach ($Pattern in $ForbiddenPatterns) {
                if ($BodyText -match [regex]::Escape($Pattern)) {
                    $DetectedInvalidClaims = $true
                }
            }
        }
    }

    if ($null -eq $Doc.expected_contract_result) {
        Add-Issue $Issues 'Missing expected_contract_result'
    }
    else {
        if ($Doc.expected_contract_result.allowed -ne $false) {
            Add-Issue $Issues 'Invalid example must have expected_contract_result.allowed=false'
        }

        if ($Doc.expected_contract_result.classification -ne 'INVALID_HANDOFF_AUTHORITY_INHERITANCE_ATTEMPT') {
            Add-Issue $Issues "Expected classification INVALID_HANDOFF_AUTHORITY_INHERITANCE_ATTEMPT, actual '$($Doc.expected_contract_result.classification)'"
        }
    }

    if (-not $DetectedAuthorityInheritance) {
        Add-Issue $Issues 'Invalid example did not contain a detectable authority-inheritance attempt'
    }

    if (-not $DetectedExternalValidityTransfer) {
        Add-Issue $Issues 'Invalid example did not contain a detectable external-validity-transfer attempt'
    }

    if (-not $DetectedInvalidClaims) {
        Add-Issue $Issues 'Invalid example did not contain detectable invalid derived claims'
    }

    $Rejected = (
        $DetectedAuthorityInheritance -and
        $DetectedExternalValidityTransfer -and
        $DetectedInvalidClaims -and
        $Doc.expected_contract_result.allowed -eq $false
    )

    return [ordered]@{
        path = $Path
        expected = 'REJECT'
        actual = $(if ($Rejected) { 'REJECT' } else { 'ACCEPT' })
        classification = $(if ($Rejected) { 'INVALID_HANDOFF_AUTHORITY_INHERITANCE_ATTEMPT' } else { 'INVALID_HANDOFF_NOT_DETECTED' })
        passed = ($Rejected -and $Issues.Count -eq 0)
        detected_authority_inheritance = $DetectedAuthorityInheritance
        detected_external_validity_transfer = $DetectedExternalValidityTransfer
        detected_invalid_claims = $DetectedInvalidClaims
        issues = @($Issues)
    }
}

$StartedUtc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$Branch = Get-GitValue @('branch', '--show-current')
$Commit = Get-GitValue @('rev-parse', 'HEAD')

$ValidDoc = Read-JsonFile $ValidExamplePath
$InvalidDoc = Read-JsonFile $InvalidExamplePath

$ValidResult = Test-ValidHandoff $ValidExamplePath $ValidDoc
$InvalidResult = Test-InvalidAuthorityInheritance $InvalidExamplePath $InvalidDoc

$Passed = ($ValidResult.passed -and $InvalidResult.passed)

$Report = [ordered]@{
    artifact_id = 'BDR-ESAL-HANDOFF-VALIDATION-REPORT-v0.1'
    generated_utc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    started_utc = $StartedUtc
    branch = $Branch
    commit = $Commit
    result = $(if ($Passed) { 'HANDOFF_VALIDATOR_PASS' } else { 'HANDOFF_VALIDATOR_FAIL' })
    contract = 'docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md'
    valid_example = $ValidResult
    invalid_example = $InvalidResult
    non_claims = @(
        'does not establish BDR truth',
        'does not establish legal sufficiency',
        'does not establish compliance sufficiency',
        'does not establish real-world authorization',
        'does not establish policy approval',
        'does not establish external governance validity',
        'does not establish ESAL validation of the underlying transition',
        'does not establish independent implementation convergence'
    )
}

$ReportJson = $Report | ConvertTo-Json -Depth 30
$ReportFullPath = Join-Path (Get-Location) $ReportPath
$ReportDirectory = Split-Path $ReportFullPath -Parent

if (!(Test-Path $ReportDirectory)) {
    New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
}

[System.IO.File]::WriteAllText($ReportFullPath, $ReportJson + "`n", $Utf8NoBom)

Write-Host ''
Write-Host '== BDR / ESAL Handoff Validation Result =='

if ($Passed) {
    Write-Host 'HANDOFF_VALIDATOR_PASS'
}
else {
    Write-Host 'HANDOFF_VALIDATOR_FAIL'
}

Write-Host ''
Write-Host "Valid example:   expected ACCEPT, actual $($ValidResult.actual)"
Write-Host "Invalid example: expected REJECT, actual $($InvalidResult.actual)"

if ($InvalidResult.classification) {
    Write-Host "Invalid classification: $($InvalidResult.classification)"
}

Write-Host "Report written: $ReportPath"

if ($VerboseOutput -or -not $Passed) {
    Write-Host ''
    Write-Host 'Valid example issues:'
    foreach ($Issue in $ValidResult.issues) {
        Write-Host "  - $Issue"
    }

    Write-Host ''
    Write-Host 'Invalid example issues:'
    foreach ($Issue in $InvalidResult.issues) {
        Write-Host "  - $Issue"
    }
}

if (-not $Passed) {
    exit 1
}

exit 0