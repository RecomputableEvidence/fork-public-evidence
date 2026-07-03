# scripts/apply_scenario_08_stale_validity_authority_revocation_v0_1.ps1
# Applies Scenario 08 stale validity / authority revocation boundary simulation.
# Patches scenario_registry.json, main AHI checker, viewer v0.1 bundle, and optional viewer v0.2 comparison data.
# It does not commit, push, or tag.

$ErrorActionPreference = "Stop"

function Write-Utf8NoBom($Path, $Text) {
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Resolve-Path $Path), $Text, $utf8NoBom)
}

if (-not (Test-Path ".git")) {
    throw "Run this script from repository root, e.g. C:\N\fork-public-evidence"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH."
}

Write-Host "Checking Scenario 08 before registry integration..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 08 checker failed. Registry was not patched."
}

Write-Host "Patching scenario registry..."
$tempPy = Join-Path $env:TEMP "patch_scenario_08_registry_v0_1.py"
$py = @'
import copy
import json
from pathlib import Path

path = Path("examples/simulations/governance-proof-surface/scenario_registry.json")
with path.open("r", encoding="utf-8") as f:
    registry = json.load(f)

sid = "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY"
scenario_path = "examples/simulations/governance-proof-surface/scenario_08_stale_validity_authority_revocation_boundary.md"
artifacts = [
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_revocation_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_validity_timeline.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_transition_graph.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_08_non_claims_panel.md",
]

scenarios = registry.setdefault("scenarios", [])

existing = None
for s in scenarios:
    if s.get("scenario_id") == sid:
        existing = s
        break

template = None
for s in scenarios:
    if s.get("scenario_id") == "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE":
        template = copy.deepcopy(s)
        break

scenario = existing if existing is not None else (template if template is not None else {})
scenario["scenario_id"] = sid
scenario["scenario_number"] = 8
scenario["title"] = "Scenario 08 — Stale Validity / Authority Revocation Boundary"

for key in ("scenario_path", "path", "narrative_path", "file_path", "file"):
    if key in scenario:
        scenario[key] = scenario_path
if not any(k in scenario for k in ("scenario_path", "path", "narrative_path", "file_path", "file")):
    scenario["scenario_path"] = scenario_path

scenario["verification_posture"] = "SEMANTICALLY_VERIFIED"
scenario["posture_description"] = (
    "Artifact family present; dedicated checker verifies bounded stale-validity and authority-revocation invariants. "
    "This does not establish current authority, current compliance, current approval, current legal sufficiency, "
    "current acceptance, current execution eligibility, or correctness."
)
scenario["artifact_files"] = artifacts
scenario["main_checker"] = {
    "invoked_by": "scripts/run_ahi_sim_v0_1_checks.ps1",
    "dedicated_checker": "scripts/check_scenario_08_stale_validity_authority_revocation_v0_1.ps1",
    "semantic_invariants_checked": [
        "prior_validity_recorded",
        "validity_state_changed",
        "prior_authority_not_current_authority",
        "stale_validity_reliance_attempt_recorded",
        "unsupported_current_authority_inference_recorded",
        "current_revalidation_required",
        "non_authority_posture_preserved"
    ]
}
scenario["checker_coverage"] = {
    "required_files": True,
    "json_validity": True,
    "semantic_invariants": True,
    "non_authority_scan": True,
    "viewer_bundle": True
}

if existing is None:
    inserted = False
    for i, s in enumerate(scenarios):
        if s.get("scenario_id") == "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE":
            scenarios.insert(i + 1, scenario)
            inserted = True
            break
    if not inserted:
        scenarios.append(scenario)

with path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
'@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($tempPy, $py, $utf8NoBom)
python $tempPy
Remove-Item $tempPy -Force

Write-Host "Patching main AHI checker..."
$mainChecker = "scripts/run_ahi_sim_v0_1_checks.ps1"
$mainText = Get-Content -Raw -Path $mainChecker
$marker = "# Scenario 08 stale validity / authority revocation validation BEGIN"

if ($mainText -notmatch [regex]::Escape($marker)) {
    $block = @'

# Scenario 08 stale validity / authority revocation validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 08 stale validity / authority revocation through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 08 stale validity / authority revocation checker failed."
}
Write-Host "PASS: Scenario 08 validation completed inside main AHI checker."
# Scenario 08 stale validity / authority revocation validation END

'@

    $finalPass = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'
    if ($mainText.Contains($finalPass)) {
        $mainText = $mainText.Replace($finalPass, $block + $finalPass)
    } else {
        $mainText = $mainText.TrimEnd() + "`n" + $block
    }

    Write-Utf8NoBom $mainChecker $mainText
} else {
    Write-Host "Main checker already contains Scenario 08 block."
}

Write-Host "Patching viewer v0.1 builder artifact labels if needed..."
$builder = "scripts/build_ahi_viewer_data_v0_1.py"
if (Test-Path $builder) {
    $builderText = Get-Content -Raw -Path $builder
    if ($builderText -notmatch "revocation_event") {
        $patched = $false
        $replacements = @(
            @('"external_authority_failure_event": "EAFE",', '"external_authority_failure_event": "EAFE",' + "`n" + '        "revocation_event": "REV",'),
            @("'external_authority_failure_event': 'EAFE',", "'external_authority_failure_event': 'EAFE'," + "`n" + "        'revocation_event': 'REV',"),
            @('"distributed_authority_failure_event": "DAFE",', '"distributed_authority_failure_event": "DAFE",' + "`n" + '        "revocation_event": "REV",'),
            @("'distributed_authority_failure_event': 'DAFE',", "'distributed_authority_failure_event': 'DAFE'," + "`n" + "        'revocation_event': 'REV',")
        )

        foreach ($pair in $replacements) {
            if ($builderText.Contains($pair[0])) {
                $builderText = $builderText.Replace($pair[0], $pair[1])
                $patched = $true
                break
            }
        }

        if ($patched) {
            Write-Utf8NoBom $builder $builderText
        } else {
            Write-Host "No known artifact-label dictionary pattern found; continuing without builder label patch."
        }
    } else {
        Write-Host "Viewer v0.1 builder already references revocation_event."
    }
}

Write-Host "Regenerating deterministic viewer v0.1 bundle..."
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
if ($LASTEXITCODE -ne 0) {
    throw "Viewer v0.1 bundle rebuild failed."
}

Write-Host "Patching optional Viewer v0.2 comparison data..."
$v02Builder = "scripts/build_ahi_viewer_comparison_data_v0_2.py"
if (Test-Path $v02Builder) {
    $text = Get-Content -Raw -Path $v02Builder
    if ($text -notmatch "PAIR-S07-S08") {
        $pairBlock = @'
    {
        "pair_id": "PAIR-S07-S08",
        "label": "Scenario 07 vs Scenario 08 — external authority bridge versus stale validity",
        "left_scenario_id": "SCENARIO_07_EXTERNAL_AUTHORITY_BRIDGE",
        "right_scenario_id": "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY",
        "comparison_posture": "EXTERNAL_AUTHORITY_AND_TEMPORAL_VALIDITY_COMPARISON",
        "purpose": "Compare external authority bridge overclaim with stale-validity reliance after revocation, expiry, supersession, narrowing, or changed context.",
        "boundary_movement": [
            "Scenario 07 tests whether internal record inspectability is treated as external authority.",
            "Scenario 08 tests whether prior validity is treated as current validity after the validity state changes.",
        ],
        "attempted_inference": [
            "Inspectable Fork record treated as external admissibility, compliance, approval, legal sufficiency, acceptance, or execution eligibility.",
            "Prior validity or prior authority treated as current validity or current authority.",
        ],
        "required_revalidation": [
            "External authority conclusions require separate external authority, rule, standard, or decision process.",
            "Current reliance requires current authority, current policy, current evidence, current role, current purpose, current environment, and current validity-window support.",
        ],
        "fork_can_show": [
            "whether external authority bridge inference was attempted",
            "whether stale-validity reliance was attempted",
            "whether required current revalidation remained visible",
        ],
        "fork_does_not_show": [
            "external admissibility",
            "current regulatory compliance",
            "current legal sufficiency",
            "current approval",
            "current evidence sufficiency",
            "current execution eligibility",
            "correctness",
        ],
        "reviewer_use": [
            "Use this pair to distinguish external authority non-transfer from temporal validity non-inheritance.",
        ],
    },
'@

        $marker2 = "`n]`n`n`n`ndef read_json"
        if ($text.Contains($marker2)) {
            $text = $text.Replace($marker2, $pairBlock + $marker2)
            Write-Utf8NoBom $v02Builder $text

            powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite
            if ($LASTEXITCODE -ne 0) {
                throw "Viewer v0.2 comparison data rebuild failed."
            }
        } else {
            Write-Host "Could not locate end of CANONICAL_PAIRS; skipping v0.2 comparison pair patch."
        }
    } else {
        Write-Host "Viewer v0.2 comparison builder already contains PAIR-S07-S08."
        powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite
    }
} else {
    Write-Host "Viewer v0.2 builder not found; skipping comparison pair integration."
}

Write-Host ""
Write-Host "Scenario 08 stale validity / authority revocation applied."
Write-Host "Next run:"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_scenario_08_stale_validity_authority_revocation_v0_1.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1"
Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1"
