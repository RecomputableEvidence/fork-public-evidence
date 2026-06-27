param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'

Write-Host '== BDR / ESAL Handoff Contract v0.1 Generator =='

if (!(Test-Path '.git')) {
    throw 'Run this script from the repository root.'
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $Directory = Split-Path $Path -Parent

    if ($Directory -and !(Test-Path $Directory)) {
        New-Item -ItemType Directory -Force -Path $Directory | Out-Null
    }

    if ((Test-Path $Path) -and (-not $Force)) {
        throw "File already exists: $Path. Re-run with -Force to overwrite."
    }

    $FullPath = Join-Path (Get-Location) $Path
    $Normalized = $Content.Replace("`r`n", "`n").TrimEnd() + "`n"
    [System.IO.File]::WriteAllText($FullPath, $Normalized, $Utf8NoBom)

    Write-Host "Wrote: $Path"
}

function Join-Lines {
    param([string[]]$Lines)
    return ($Lines -join "`n")
}

New-Item -ItemType Directory -Force -Path 'docs' | Out-Null
New-Item -ItemType Directory -Force -Path 'examples\bdr_esal_handoff' | Out-Null

$ContractPath = 'docs\BDR_ESAL_HANDOFF_CONTRACT_v0_1.md'
$ValidExamplePath = 'examples\bdr_esal_handoff\valid_vendor_risk_handoff_event.json'
$InvalidExamplePath = 'examples\bdr_esal_handoff\invalid_authority_inheritance_handoff_event.json'

$Contract = Join-Lines @(
    '# BDR / ESAL Handoff Contract v0.1',
    '',
    '**Artifact ID:** BDR-ESAL-HANDOFF-CONTRACT-v0.1-001',
    '**Status:** Draft contract',
    '**Scope:** Boundary Delta Record to ESAL reference-oracle event handoff',
    '',
    '---',
    '',
    '## 1. Purpose',
    '',
    'This contract defines how a Boundary Delta Record may be represented as ESAL replay input without transferring authority, approval, compliance status, legal sufficiency, truth, safety, or external governance validity into the ESAL oracle.',
    '',
    'The purpose is narrow:',
    '',
    '```text',
    'BDR records a boundary-crossing evidence transition.',
    'ESAL consumes bounded event data for replay, reduction, classification, and fingerprinting.',
    'The handoff preserves evidence boundaries and non-claims.',
    'The handoff does not create inherited authority.',
    '```',
    '',
    '---',
    '',
    '## 2. Object Boundary',
    '',
    '| Object | Role | What it may establish | What it must not imply |',
    '|---|---|---|---|',
    '| BDR | Boundary-crossing evidence record | What changed, what was preserved, what narrowed, what expanded, what became unresolved, and what evidence was referenced | Truth, legal sufficiency, compliance sufficiency, approval, external validity, or real-world authority |',
    '| ESAL | Event-state replay and fingerprint oracle | Deterministic replay behavior under ESAL rules, state reduction, classification, and fingerprinting | External governance validity, legal sufficiency, compliance, approval, safety, truth, or authorization correctness |',
    '| Handoff Contract | Boundary between BDR and ESAL | Which BDR-derived fields may become ESAL event input and which non-claims survive the transition | Any transfer of authority, approval, compliance, or external validity |',
    '',
    '---',
    '',
    '## 3. Core Handoff Rule',
    '',
    'ESAL may consume BDR-derived events for replay, state reduction, classification, and fingerprinting.',
    '',
    'ESAL does not inherit, validate, certify, approve, or expand the authority, compliance status, legal sufficiency, truth, safety, or external governance validity of the BDR or the underlying transition.',
    '',
    'A BDR-derived ESAL event is admissible as replay input only when the event preserves the BDR claim boundary and does not transform evidence preservation into authority inheritance.',
    '',
    '---',
    '',
    '## 4. BDR Fields Eligible for ESAL Consumption',
    '',
    'The following BDR-derived fields may be represented in ESAL event input:',
    '',
    '- `bdr_id`',
    '- `parent_bdr_id` or other declared lineage reference',
    '- `boundary_id`',
    '- `source_boundary`',
    '- `target_boundary`',
    '- `transition_kind`',
    '- `preserved_claims`',
    '- `preserved_non_claims`',
    '- `evidence_refs`',
    '- `constraints`',
    '- `obligations`',
    '- `unresolved_unknowns`',
    '- `timestamp`',
    '- `issuer` or declared source actor',
    '',
    'These fields are consumed as event data. Their presence does not establish that the underlying BDR is true, sufficient, approved, compliant, or externally valid.',
    '',
    '---',
    '',
    '## 5. ESAL Event Construction',
    '',
    'A BDR-derived ESAL event should use an ESAL event type such as:',
    '',
    '```text',
    'BDR_CREATED',
    '```',
    '',
    'The ESAL event body may carry BDR-derived identifiers, constraints, obligations, lineage, and evidence references.',
    '',
    'The ESAL event body must not add claims such as:',
    '',
    '- `ESAL approves this transition`',
    '- `ESAL validates BDR authority`',
    '- `ESAL establishes compliance`',
    '- `ESAL establishes legal sufficiency`',
    '- `ESAL transfers upstream authority`',
    '- `ESAL certifies external governance validity`',
    '',
    '---',
    '',
    '## 6. Preservation Rules',
    '',
    'A valid BDR to ESAL handoff must preserve:',
    '',
    '1. The BDR identifier.',
    '2. The declared lineage relationship, if present.',
    '3. The source and target boundary references, if present.',
    '4. Evidence references used by the BDR.',
    '5. Constraints and obligations carried into ESAL state.',
    '6. Non-claims attached to the BDR.',
    '7. Unresolved unknowns, if present.',
    '',
    'The handoff may narrow representational detail for ESAL replay, but it must not silently drop non-claims or unresolved unknowns when those omissions would create a broader interpretation of the event.',
    '',
    '---',
    '',
    '## 7. Explicit Non-Inheritance Rules',
    '',
    'The following are invalid handoff interpretations:',
    '',
    '- BDR reviewed implies ESAL approved.',
    '- BDR evidence preserved implies ESAL validated truth.',
    '- BDR transition recorded implies ESAL established compliance.',
    '- BDR issuer authority implies ESAL inherited issuer authority.',
    '- ESAL `PASS` implies the underlying transition was legally sufficient.',
    '- ESAL fingerprint implies the BDR was correct.',
    '- ESAL replayability implies policy adequacy.',
    '- ESAL state reduction implies external governance validity.',
    '',
    'A valid handoff must preserve the distinction between evidence preservation and authority transfer.',
    '',
    '---',
    '',
    '## 8. Valid Handoff Example',
    '',
    'Example file:',
    '',
    '```text',
    'examples/bdr_esal_handoff/valid_vendor_risk_handoff_event.json',
    '```',
    '',
    'This example shows a vendor-risk BDR represented as an ESAL `BDR_CREATED` event.',
    '',
    'The example is valid because:',
    '',
    '- it carries BDR identifiers and evidence references;',
    '- it preserves non-claims;',
    '- it does not state that ESAL approves the vendor-risk decision;',
    '- it does not state that ESAL validates legal or compliance sufficiency;',
    '- it treats ESAL replay as replay only.',
    '',
    '---',
    '',
    '## 9. Invalid Handoff Example',
    '',
    'Example file:',
    '',
    '```text',
    'examples/bdr_esal_handoff/invalid_authority_inheritance_handoff_event.json',
    '```',
    '',
    'This example is intentionally invalid.',
    '',
    'It attempts to treat a BDR-derived ESAL event as establishing inherited authority, compliance, approval, or external validity.',
    '',
    'The invalid example must not be used as an admissible handoff fixture. It exists only to document the forbidden pattern.',
    '',
    '---',
    '',
    '## 10. Non-Claims',
    '',
    'This contract does not establish:',
    '',
    '- BDR truth;',
    '- BDR legal sufficiency;',
    '- BDR compliance sufficiency;',
    '- real-world authorization;',
    '- policy approval;',
    '- external governance validity;',
    '- downstream admissibility;',
    '- ESAL validation of the underlying transition;',
    '- production completeness;',
    '- independent implementation convergence;',
    '- or safety.',
    '',
    'This list is illustrative, not exhaustive.',
    '',
    '---',
    '',
    '## 11. Relationship to TIS, SMR, and Fork',
    '',
    'TIS defines transition-validity semantics.',
    '',
    'BDR records boundary-crossing evidence and inspectability.',
    '',
    'ESAL replays event-state traces and fingerprints reduced state under oracle rules.',
    '',
    'SMR records external system mapping and integration context.',
    '',
    'This handoff contract sits between BDR and ESAL. It defines how BDR evidence may become ESAL replay input without allowing authority, compliance, approval, or external validity to transfer silently across the boundary.',
    '',
    '---',
    '',
    '## 12. Future Work',
    '',
    'Future work may add:',
    '',
    '- a machine-checkable BDR to ESAL handoff schema;',
    '- a handoff validator;',
    '- conformance fixtures for valid and invalid handoff examples;',
    '- explicit preservation checks for non-claims;',
    '- explicit detection of authority-inheritance attempts;',
    '- and integration with the ESAL conformance harness.',
    '',
    'No future work should collapse BDR evidence preservation into ESAL approval, certification, compliance, or external validity.'
)

$ValidExample = [ordered]@{
    artifact_id = 'EXAMPLE-BDR-ESAL-HANDOFF-VALID-VENDOR-RISK-001'
    profile = 'BDR_ESAL_HANDOFF_CONTRACT_v0_1'
    status = 'VALID_HANDOFF_EXAMPLE'
    purpose = 'Demonstrates a bounded BDR-derived ESAL event without authority inheritance.'
    source_bdr = [ordered]@{
        bdr_id = 'bdr-vendor-risk-001'
        parent_bdr_id = $null
        boundary_id = 'boundary-vendor-risk-review'
        source_boundary = 'ai-assisted-summary-generation'
        target_boundary = 'human-reviewed-vendor-risk-record'
        transition_kind = 'PRESERVED'
        subject_reference = 'vendor-risk-summary-2026-06-27'
        evidence_refs = @(
            'evidence://vendor-risk/input-materials-hash',
            'evidence://vendor-risk/ai-output-hash',
            'evidence://vendor-risk/human-review-notes-hash'
        )
        preserved_claims = @(
            'The vendor-risk summary was generated, reviewed, and recorded under the stated workflow.'
        )
        preserved_non_claims = @(
            'The record does not establish that the vendor is safe.',
            'The record does not establish legal sufficiency.',
            'The record does not establish compliance sufficiency.',
            'The record does not establish approval.',
            'The record does not establish external governance validity.',
            'The record does not establish that underlying facts are true.'
        )
        unresolved_unknowns = @(
            'Whether all relevant vendor-risk materials were available to the reviewer.',
            'Whether downstream policy review is required.'
        )
    }
    esal_event = [ordered]@{
        event_id = 'event-bdr-vendor-risk-001'
        event_type = 'BDR_CREATED'
        timestamp = '2026-06-27T00:00:00Z'
        body = [ordered]@{
            bdr_id = 'bdr-vendor-risk-001'
            parent_bdr_id = $null
            boundary_id = 'boundary-vendor-risk-review'
            source_boundary = 'ai-assisted-summary-generation'
            target_boundary = 'human-reviewed-vendor-risk-record'
            authority = @()
            constraints = @(
                'preserve-non-claims',
                'no-authority-inheritance',
                'no-compliance-inference'
            )
            obligations = @(
                'retain-evidence-refs',
                'retain-unresolved-unknowns'
            )
            evidence_refs = @(
                'evidence://vendor-risk/input-materials-hash',
                'evidence://vendor-risk/ai-output-hash',
                'evidence://vendor-risk/human-review-notes-hash'
            )
            preserved_non_claims = @(
                'no legal sufficiency',
                'no compliance sufficiency',
                'no approval',
                'no external governance validity',
                'no truth certification'
            )
        }
    }
    handoff_assertion = [ordered]@{
        allowed = $true
        allowed_effect = 'ESAL may replay, reduce, classify, and fingerprint this event under ESAL oracle rules.'
        non_inheritance = @(
            'ESAL does not inherit BDR issuer authority.',
            'ESAL does not approve the vendor-risk decision.',
            'ESAL does not establish compliance.',
            'ESAL does not establish legal sufficiency.',
            'ESAL does not establish external governance validity.',
            'ESAL does not certify truth or safety.'
        )
    }
}

$InvalidExample = [ordered]@{
    artifact_id = 'EXAMPLE-BDR-ESAL-HANDOFF-INVALID-AUTHORITY-INHERITANCE-001'
    profile = 'BDR_ESAL_HANDOFF_CONTRACT_v0_1'
    status = 'INVALID_HANDOFF_EXAMPLE'
    purpose = 'Documents a forbidden authority-inheritance pattern. This file is not an admissible handoff fixture.'
    source_bdr = [ordered]@{
        bdr_id = 'bdr-invalid-authority-inheritance-001'
        boundary_id = 'boundary-invalid-authority-transfer'
        source_boundary = 'human-reviewed-record'
        target_boundary = 'esal-replay-oracle'
        transition_kind = 'EXPANDED'
        evidence_refs = @(
            'evidence://invalid/example-review-record'
        )
        preserved_claims = @(
            'A review occurred.'
        )
        preserved_non_claims = @(
            'The review did not establish compliance.',
            'The review did not establish approval.',
            'The review did not establish external governance validity.'
        )
    }
    attempted_esal_event = [ordered]@{
        event_id = 'event-invalid-authority-inheritance-001'
        event_type = 'BDR_CREATED'
        timestamp = '2026-06-27T00:00:00Z'
        body = [ordered]@{
            bdr_id = 'bdr-invalid-authority-inheritance-001'
            boundary_id = 'boundary-invalid-authority-transfer'
            authority = @(
                'approve:vendor',
                'certify:compliance'
            )
            constraints = @(
                'preserve-evidence'
            )
            evidence_refs = @(
                'evidence://invalid/example-review-record'
            )
            invalid_derived_claims = @(
                'ESAL replay establishes that the vendor-risk decision is approved.',
                'ESAL fingerprint establishes compliance sufficiency.',
                'BDR review authority transfers into ESAL state.'
            )
            attempted_authority_inheritance = $true
            attempted_external_validity_transfer = $true
        }
    }
    expected_contract_result = [ordered]@{
        allowed = $false
        classification = 'INVALID_HANDOFF_AUTHORITY_INHERITANCE_ATTEMPT'
        reason = 'The attempted handoff converts BDR evidence preservation into ESAL authority, approval, compliance, and external-validity claims.'
        required_response = 'Reject as a bounded BDR to ESAL handoff. Preserve only as an invalid example of a forbidden pattern.'
    }
    non_claims = @(
        'This invalid example does not establish that ESAL has authority.',
        'This invalid example does not establish compliance.',
        'This invalid example does not establish approval.',
        'This invalid example does not establish external governance validity.'
    )
}

$ValidJson = $ValidExample | ConvertTo-Json -Depth 30
$InvalidJson = $InvalidExample | ConvertTo-Json -Depth 30

Write-Utf8NoBom $ContractPath $Contract
Write-Utf8NoBom $ValidExamplePath $ValidJson
Write-Utf8NoBom $InvalidExamplePath $InvalidJson

# Basic JSON parse check.
Get-Content $ValidExamplePath -Raw | ConvertFrom-Json | Out-Null
Get-Content $InvalidExamplePath -Raw | ConvertFrom-Json | Out-Null

Write-Host ''
Write-Host 'Created BDR / ESAL handoff contract and examples.'
Write-Host ''
Write-Host 'Review:'
Write-Host '  git diff -- docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md'
Write-Host '  git diff -- examples/bdr_esal_handoff/valid_vendor_risk_handoff_event.json'
Write-Host '  git diff -- examples/bdr_esal_handoff/invalid_authority_inheritance_handoff_event.json'
Write-Host ''
Write-Host 'Commit:'
Write-Host '  git add docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md examples/bdr_esal_handoff/valid_vendor_risk_handoff_event.json examples/bdr_esal_handoff/invalid_authority_inheritance_handoff_event.json tools/New-BdrEsalHandoffContract.ps1'
Write-Host '  git commit -m "Add BDR ESAL handoff contract v0.1"'
Write-Host '  git push'
