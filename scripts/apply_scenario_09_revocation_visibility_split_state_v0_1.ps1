# scripts/apply_scenario_09_revocation_visibility_split_state_v0_1.ps1
# Applies Scenario 09 revocation visibility / split-state integration.
# Patches registry, main AHI checker, viewer v0.1 bundle, and optional viewer v0.2 comparison pair.
# Does not commit, push, or tag.

$ErrorActionPreference = "Stop"

function Fail($Message) {
    Write-Host "FAIL: $Message" -ForegroundColor Red
    exit 1
}

function Write-Utf8NoBom($Path, $Text) {
    $Full = [System.IO.Path]::GetFullPath($Path)
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Full, $Text, $Utf8NoBom)
}

function Require-File($Path) {
    if (-not (Test-Path $Path)) {
        Fail "missing required file: $Path"
    }
    Write-Host "FOUND: $Path"
}

if (-not (Test-Path ".git")) {
    Fail "Run from repository root."
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "Python was not found on PATH."
}

Write-Host "Checking Scenario 09 artifact layer before integration..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_09_revocation_visibility_split_state_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    Fail "Scenario 09 checker failed before integration."
}

$scenarioId = "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY"
$scenarioPath = "examples/simulations/governance-proof-surface/scenario_09_revocation_visibility_split_state_boundary.md"
$registryPath = "examples/simulations/governance-proof-surface/scenario_registry.json"
$mainCheckerPath = "scripts/run_ahi_sim_v0_1_checks.ps1"

Require-File $registryPath
Require-File $mainCheckerPath

Write-Host ""
Write-Host "Patching scenario registry..."

$tempPy = Join-Path $env:TEMP "patch_scenario_09_registry_v0_1.py"

$py = @'
import copy
import json
from pathlib import Path

registry_path = Path("examples/simulations/governance-proof-surface/scenario_registry.json")

sid = "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY"
scenario_path = "examples/simulations/governance-proof-surface/scenario_09_revocation_visibility_split_state_boundary.md"
artifacts = [
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_boundary_delta_record.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_claim_boundary_contract.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_claim_consumption_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_system_mapping_receipt.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_visibility_gap_event.json",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_split_state_timeline.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_transition_graph.md",
    "examples/simulations/governance-proof-surface/artifacts/scenario_09_non_claims_panel.md",
]

with registry_path.open("r", encoding="utf-8") as f:
    registry = json.load(f)

scenarios = registry.setdefault("scenarios", [])

existing = None
for scenario in scenarios:
    if scenario.get("scenario_id") == sid:
        existing = scenario
        break

template = None
for scenario in scenarios:
    if scenario.get("scenario_id") == "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY":
        template = copy.deepcopy(scenario)
        break

if existing is not None:
    scenario = existing
else:
    scenario = template if template is not None else {}

scenario["scenario_id"] = sid

# Preserve common field shape while making Scenario 09 explicit.
for key in ("scenario_number", "number"):
    if key in scenario:
        scenario[key] = 9

if not any(k in scenario for k in ("scenario_number", "number")):
    scenario["scenario_number"] = 9

for key in ("title", "scenario_title", "name"):
    if key in scenario or key == "title":
        scenario[key] = "Scenario 09 — Revocation Visibility / Split-State Boundary"

path_keys = ("scenario_path", "path", "narrative_path", "file_path", "file")
had_path_key = False
for key in path_keys:
    if key in scenario:
        scenario[key] = scenario_path
        had_path_key = True
if not had_path_key:
    scenario["scenario_path"] = scenario_path

# Preserve existing viewer-selected field pattern if present.
scenario["artifact_files"] = artifacts
scenario["verification_posture"] = "SEMANTICALLY_VERIFIED"
scenario["posture_description"] = (
    "Artifact family present; dedicated checker verifies bounded revocation visibility and split-state invariants. "
    "This does not establish global visibility, global consumption, current authority, current validity, compliance, "
    "legal sufficiency, negligence, excuse, execution eligibility, or correctness."
)
scenario["failure_mode"] = "REVOCATION_VISIBILITY_GAP"
scenario["core_invariant"] = (
    "recorded_in_A does not imply visible_in_B; "
    "visible_in_B does not imply consumed_by_C; "
    "not_visible_locally does not imply still_valid_currently"
)
scenario["selected_fields"] = {
    "boundary_type": "REVOCATION_VISIBILITY_AND_SPLIT_STATE",
    "delta_classification": "REVOCATION_VISIBILITY_GAP_RECORDED",
    "record_support": "NOT_SUPPORTED",
    "boundary_effect": "EXPANDED",
    "required_revalidation": [
        "visibility evidence",
        "consumption evidence",
        "state synchronization evidence",
        "current authority",
        "current policy version",
        "current evidence basis",
        "current validity window",
        "current execution eligibility"
    ],
    "fork_does_not_establish": [
        "global visibility",
        "global consumption",
        "current validity",
        "current authority",
        "current approval",
        "current policy satisfaction",
        "current evidence sufficiency",
        "current regulatory compliance",
        "current legal sufficiency",
        "current execution eligibility",
        "current external acceptance",
        "negligence",
        "excuse",
        "correctness"
    ]
}
scenario["checker_coverage"] = {
    "required_files": True,
    "json_validity": True,
    "semantic_invariants": True,
    "non_authority_scan": True,
    "viewer_bundle": True
}
scenario["main_checker"] = {
    "invoked_by": "scripts/run_ahi_sim_v0_1_checks.ps1",
    "dedicated_checker": "scripts/check_scenario_09_revocation_visibility_split_state_v0_1.ps1",
    "semantic_invariants_checked": [
        "validity_change_recorded",
        "not_automatically_global",
        "visibility_gap_recorded",
        "local_non_awareness_not_current_validity",
        "split_state_reliance_attempt_recorded",
        "current_revalidation_required",
        "non_authority_posture_preserved"
    ]
}

if existing is None:
    inserted = False
    for i, candidate in enumerate(scenarios):
        if candidate.get("scenario_id") == "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY":
            scenarios.insert(i + 1, scenario)
            inserted = True
            break
    if not inserted:
        scenarios.append(scenario)

with registry_path.open("w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
'@

Write-Utf8NoBom $tempPy $py
python $tempPy
if ($LASTEXITCODE -ne 0) {
    Fail "registry patch failed"
}
Remove-Item $tempPy -Force

Write-Host "Patching main AHI checker..."

$mainText = Get-Content -Raw -Path $mainCheckerPath
$blockStart = "# Scenario 09 revocation visibility / split-state validation BEGIN"

if ($mainText -notmatch [regex]::Escape($blockStart)) {
    $block = @'

# Scenario 09 revocation visibility / split-state validation BEGIN
Write-Host ""
Write-Host "Checking Scenario 09 revocation visibility / split-state through main AHI checker..."
& powershell -ExecutionPolicy Bypass -File scripts\check_scenario_09_revocation_visibility_split_state_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    throw "Scenario 09 revocation visibility / split-state checker failed."
}
Write-Host "PASS: Scenario 09 validation completed inside main AHI checker."
# Scenario 09 revocation visibility / split-state validation END

'@

    $finalPass = 'Write-Host "PASS: ahi-sim-v0.1.x simulation proof-surface checks completed."'
    if ($mainText.Contains($finalPass)) {
        $mainText = $mainText.Replace($finalPass, $block + $finalPass)
    } else {
        $mainText = $mainText.TrimEnd() + "`n" + $block
    }

    Write-Utf8NoBom $mainCheckerPath $mainText
} else {
    Write-Host "Main checker already includes Scenario 09 block."
}

Write-Host ""
Write-Host "Regenerating viewer v0.1 bundle..."
Require-File "scripts/build_ahi_viewer_data_v0_1.ps1"
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
if ($LASTEXITCODE -ne 0) {
    Fail "viewer v0.1 bundle rebuild failed"
}

Write-Host ""
Write-Host "Patching viewer v0.2 canonical comparison pair..."

$v02Builder = "scripts/build_ahi_viewer_comparison_data_v0_2.py"
if (Test-Path $v02Builder) {
    $text = Get-Content -Raw -Path $v02Builder

    if ($text -notmatch "PAIR-S08-S09") {
        $pairBlock = @'
    {
        "pair_id": "PAIR-S08-S09",
        "label": "Scenario 08 vs Scenario 09 — stale validity versus revocation visibility",
        "left_scenario_id": "SCENARIO_08_STALE_VALIDITY_AUTHORITY_REVOCATION_BOUNDARY",
        "right_scenario_id": "SCENARIO_09_REVOCATION_VISIBILITY_SPLIT_STATE_BOUNDARY",
        "comparison_posture": "TEMPORAL_VALIDITY_AND_SPLIT_STATE_VISIBILITY_COMPARISON",
        "purpose": "Compare stale-validity reliance after a validity change with split-state reliance where the validity-changing event is not confirmed visible or consumed across systems.",
        "boundary_movement": [
            "Scenario 08 tests whether prior validity is treated as current validity after a validity state changes.",
            "Scenario 09 tests whether the validity-changing event itself is visible, consumed, and operative across system boundaries."
        ],
        "attempted_inference": [
            "Prior validity or prior authority treated as current validity or current authority.",
            "Revocation recorded in one system treated as globally visible and consumed, or local non-awareness treated as current validity."
        ],
        "required_revalidation": [
            "Current reliance requires current authority, current policy, current evidence, current role, current purpose, current environment, and current validity-window support.",
            "Split-state reliance requires explicit visibility, consumption, synchronization, or current revalidation evidence."
        ],
        "fork_can_show": [
            "whether stale-validity reliance was attempted",
            "whether revocation visibility or consumption was unconfirmed",
            "whether split-state reliance occurred",
            "whether required revalidation remained visible"
        ],
        "fork_does_not_show": [
            "current validity",
            "global visibility",
            "global consumption",
            "current regulatory compliance",
            "current legal sufficiency",
            "current approval",
            "current execution eligibility",
            "negligence",
            "excuse",
            "correctness"
        ],
        "reviewer_use": [
            "Use this pair to distinguish temporal non-inheritance from visibility and consumption gaps in distributed state."
        ]
    },

'@

        $inserted = $false

        # Preferred shape: CANONICAL_PAIRS list followed by read_json function.
        $marker = "`n]`n`n`ndef read_json"
        if ($text.Contains($marker)) {
            $text = $text.Replace($marker, $pairBlock + $marker)
            $inserted = $true
        }

        # Alternate shape: last canonical pair before a named function.
        if (-not $inserted) {
            $marker = "`n]`r`n`r`ndef read_json"
            if ($text.Contains($marker)) {
                $text = $text.Replace($marker, $pairBlock + $marker)
                $inserted = $true
            }
        }

        if (-not $inserted) {
            Write-Host "WARNING: Could not locate canonical-pair insertion point in $v02Builder"
            Write-Host "         v0.2 builder was not patched. Manual PAIR-S08-S09 insertion may be required."
        } else {
            Write-Utf8NoBom $v02Builder $text
        }
    } else {
        Write-Host "Viewer v0.2 builder already contains PAIR-S08-S09."
    }

    Require-File "scripts/build_ahi_viewer_comparison_data_v0_2.ps1"
    powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_comparison_data_v0_2.ps1 -ForceOverwrite
    if ($LASTEXITCODE -ne 0) {
        Fail "viewer v0.2 comparison rebuild failed"
    }
} else {
    Write-Host "Viewer v0.2 builder not found; skipping v0.2 comparison integration."
}

Write-Host ""
Write-Host "Running integrated Scenario 09 checks..."
powershell -ExecutionPolicy Bypass -File scripts\check_scenario_09_revocation_visibility_split_state_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    Fail "Scenario 09 checker failed after integration"
}

powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1
if ($LASTEXITCODE -ne 0) {
    Fail "main AHI checker failed after Scenario 09 integration"
}

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1
if ($LASTEXITCODE -ne 0) {
    Fail "viewer v0.1 checker failed after Scenario 09 integration"
}

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1
if ($LASTEXITCODE -ne 0) {
    Fail "viewer v0.2 checker failed after Scenario 09 integration"
}

Write-Host ""
Write-Host "Scenario 09 integration applied successfully."
Write-Host "Next:"
Write-Host "  git diff --check"
Write-Host "  git status -sb"
Write-Host "  git add examples\simulations\governance-proof-surface\scenario_registry.json scripts\run_ahi_sim_v0_1_checks.ps1 docs\viewer\ahi-viewer-v0_1\data\scenarios_bundle.json docs\viewer\ahi-viewer-v0_2\data\comparison_pairs.json scripts\build_ahi_viewer_comparison_data_v0_2.py scripts\apply_scenario_09_revocation_visibility_split_state_v0_1.ps1 README_SCENARIO_09_INTEGRATION_PATCH_v0_1.md"
Write-Host "  git commit -m `"Integrate Scenario 09 into AHI proof surface`""
