param(
    [string]$ReadmePath = "README.md"
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Get-Location).Path
$FullReadmePath = Join-Path $RepoRoot $ReadmePath

if (-not (Test-Path $FullReadmePath)) {
    throw "README not found at: $FullReadmePath"
}

function Normalize-LF {
    param([Parameter(Mandatory=$true)][string]$Text)
    return ($Text -replace "`r`n", "`n" -replace "`r", "`n")
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    $LfContent = Normalize-LF $Content
    [System.IO.File]::WriteAllText($Path, $LfContent, $Utf8NoBom)
}

$startMarker = "<!-- FORK_PUBLIC_PRESENCE_ROUTING_START -->"
$endMarker = "<!-- FORK_PUBLIC_PRESENCE_ROUTING_END -->"

$block = @"
$startMarker

## Public presence and workflow-inlet routing

Fork routes by evidence-boundary input, not by buyer persona.

A reviewer, advisor, enterprise sponsor, legal/compliance leader, audit leader, risk leader, technical sponsor, source-system owner, GRC owner, AI governance lead, or co-integration partner may all enter through the same public surface.

The correct inlet depends on what the visitor can provide.

### Public review input

Use:

- `REVIEWER_QUICK_START_v0_1.md`
- `docs/REVIEWER_START_HERE_v0_1.md`
- `docs/FORK_NON_CLAIM_BOUNDARY_v0_1.md`
- `docs/PUBLIC_REVIEW_PACKAGE_INDEX_v0_1.md`

### Candidate workflow input

Start with:

- `release_packages/FORK_PILOT_DISCOVERY_PACKET_v0_1/`

### Client-side workflow/source-system input

Complete:

- `release_packages/FORK_CLIENT_DISCOVERY_RETURN_PACKET_TEMPLATE_v0_1/`

### Fork-authored evidence-boundary output

Fork may draft:

- `release_packages/FORK_CLIENT_EVIDENCE_BOUNDARY_PACKET_TEMPLATE_v0_1/`

only after reviewing a completed Client Discovery Return Packet.

### Sidecar bridge specification

A sidecar bridge follows an accepted evidence boundary. It is not assumed from public review alone.

### Bounded workflow PoV

A PoV may be scoped only around one accepted bounded workflow.

For the canonical routing cadence, see:

- `docs/FORK_INLET_ROUTING_AND_ONBOARDING_CADENCE_v0_1.md`

This routing does not establish production readiness, customer deployment, procurement approval, legal sufficiency, compliance satisfaction, audit sufficiency, source completeness, security approval, risk acceptance, workflow suitability, commercial pilot approval, AI-output correctness, decision correctness, or institutional authority.

## Enterprise discovery and bounded workflow PoV

Fork can be evaluated only around a bounded AI-assisted workflow whose evidence boundary has been described, reviewed, and accepted for scoping.

The governing sequence is:

1. Public repo orientation.
2. Workflow-inlet routing.
3. Client Discovery Return Packet.
4. Fork review of returned workflow/source-system facts.
5. Client Evidence Boundary Packet draft, if responsible.
6. Client review of the proposed evidence boundary.
7. Sidecar bridge specification candidate, if the boundary is accepted.
8. Bounded workflow PoV scope, if commercially and operationally appropriate.

The Client Discovery Return Packet is the inbound mapping record.

The Client Evidence Boundary Packet is the Fork-authored boundary draft.

The sidecar bridge is downstream of the accepted boundary.

The institution owns the action. Fork preserves the bounded evidence record.

For bounded technical review, design-partner discussion, or enterprise discovery, contact Ryan Feller via LinkedIn.

This routing does not establish a binding quote, procurement approval, production readiness, customer deployment, commercial pilot approval, legal sufficiency, security certification, compliance satisfaction, audit sufficiency, risk acceptance, workflow suitability, source-system access approval, implementation approval, or sidecar bridge approval.

$endMarker
"@

$text = Get-Content -Raw -Path $FullReadmePath
$text = Normalize-LF $text

# Remove existing managed block, if present.
$managedPattern = "(?s)\n?$([regex]::Escape($startMarker)).*?$([regex]::Escape($endMarker))\n?"
$text = [regex]::Replace($text, $managedPattern, "`n")

# Remove rough unformatted pasted tail if it was previously appended after Copyright.
$roughTailPattern = "(?s)\n+Public presence and workflow-inlet routing\s+Fork routes by evidence-boundary input, not by buyer persona\..*\z"
$text = [regex]::Replace($text, $roughTailPattern, "`n")

# Insert before Copyright so copyright remains the final section.
$copyrightPattern = "(?m)^## Copyright\s*$"

if ($text -match $copyrightPattern) {
    $text = [regex]::Replace(
        $text,
        $copyrightPattern,
        ($block.TrimEnd() + "`n`n## Copyright"),
        1
    )
}
else {
    $text = $text.TrimEnd() + "`n`n" + $block.TrimEnd() + "`n"
}

Write-Utf8NoBomFile -Path $FullReadmePath -Content ($text.TrimEnd() + "`n")

Write-Host "Updated README with public presence, workflow-inlet routing, and bounded workflow PoV sections."