param(
    [string]$Root = ".",
    [string]$CommitMessage = "Fix surface interaction fixture coherence and proof surface crosswalk",
    [string]$TagName = "surface-interaction-coherence-v0.1.1",
    [string]$TagMessage = "Surface interaction coherence fixes v0.1.1",
    [switch]$AllowDirty,
    [switch]$SkipAddScript,
    [switch]$NoCommit,
    [switch]$NoTag,
    [switch]$NoPush
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path -LiteralPath $Root).Path

function Require-GitRepo {
    $Inside = git -C $RepoRoot rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -ne 0 -or $Inside.Trim() -ne "true") {
        throw "Not inside a Git repository: $RepoRoot"
    }
}

function Write-Utf8NoBomLf {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    $FullPath = [System.IO.Path]::GetFullPath($Path)
    $Parent = Split-Path -Parent $FullPath

    if (-not (Test-Path -LiteralPath $Parent)) {
        New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    }

    $Normalized = $Text -replace "`r`n", "`n"
    $Normalized = $Normalized -replace "`r", "`n"
    $Normalized = $Normalized.TrimEnd() + "`n"

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($FullPath, $Normalized, $Utf8NoBom)
}

function Assert-NoOddMarkdownFences {
    param([string[]]$Paths)

    foreach ($Path in $Paths) {
        if (Test-Path -LiteralPath $Path) {
            $Count = @(Select-String -Path $Path -Pattern '^```').Count
            Write-Host "$Path fence count: $Count"
            if (($Count % 2) -ne 0) {
                throw "Odd markdown code-fence count detected in $Path"
            }
        }
    }
}

Require-GitRepo

$PlannedPaths = @(
    "examples\surface-interaction\invalid\invalid_authority_absorption_attempt_v0_1.json",
    "examples\surface-interaction\invalid\invalid_interop_semantic_adoption_attempt_v0_1.json",
    "docs\modular-surface\FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md",
    "docs\modular-surface\FORK_MODULAR_SURFACE_v0_1.md",
    "docs\VERIFICATION_COMMANDS_v0_1.md",
    "tests\test_surface_interaction_v0_1.py",
    ".github\workflows\surface-interaction-v0-1.yml"
)

if (-not $AllowDirty) {
    $DirtyTargets = git -C $RepoRoot status --porcelain -- $PlannedPaths
    if ($DirtyTargets) {
        Write-Host "Dirty planned target files detected:" -ForegroundColor Yellow
        $DirtyTargets | ForEach-Object { Write-Host $_ }
        throw "Refusing to continue with dirty planned target files. Commit/stash them first, or rerun with -AllowDirty."
    }

    git -C $RepoRoot diff --cached --quiet
    if ($LASTEXITCODE -ne 0) {
        throw "Refusing to continue because staged changes already exist. Commit/stash them first, or rerun with -AllowDirty."
    }
}

if (-not $NoTag) {
    git -C $RepoRoot rev-parse -q --verify "refs/tags/$TagName" *> $null
    if ($LASTEXITCODE -eq 0) {
        throw "Tag already exists: $TagName"
    }
}

$PatchPy = @'
import json
import os
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

root = Path(os.environ["FORK_REPO_ROOT"]).resolve()

schema_path = root / "schemas" / "surface_interaction_v0_1.schema.json"
checker_path = root / "tools" / "check_surface_interaction_v0_1.py"
valid_path = root / "examples" / "surface-interaction" / "valid" / "valid_reliance_references_evidence_boundary_v0_1.json"
semantic_path = root / "examples" / "surface-interaction" / "invalid" / "invalid_interop_semantic_adoption_attempt_v0_1.json"
authority_path = root / "examples" / "surface-interaction" / "invalid" / "invalid_authority_absorption_attempt_v0_1.json"
crosswalk_path = root / "docs" / "modular-surface" / "FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md"
modular_surface_path = root / "docs" / "modular-surface" / "FORK_MODULAR_SURFACE_v0_1.md"
verification_path = root / "docs" / "VERIFICATION_COMMANDS_v0_1.md"
tests_path = root / "tests" / "test_surface_interaction_v0_1.py"
workflow_path = root / ".github" / "workflows" / "surface-interaction-v0-1.yml"

required = [schema_path, checker_path, valid_path, semantic_path, crosswalk_path]
missing = [str(p.relative_to(root)) for p in required if not p.exists()]
if missing:
    raise SystemExit("Missing required file(s): " + ", ".join(missing))

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")

def load_json(path: Path):
    return json.loads(read_text(path))

def dump_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

schema = load_json(schema_path)
valid = load_json(valid_path)
semantic_original = load_json(semantic_path)

def unique(seq):
    out = []
    seen = set()
    for item in seq:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out

neutral_authority = valid.get("authority_effect")
neutral_semantic = valid.get("semantic_effect")

if not neutral_authority:
    raise SystemExit(f"Valid fixture missing authority_effect: {valid_path.relative_to(root)}")
if not neutral_semantic:
    raise SystemExit(f"Valid fixture missing semantic_effect: {valid_path.relative_to(root)}")

base_ops = list(valid.get("permitted_operations", []))

authority_trigger_ops = {
    "IMPORT_EXTERNAL_AUTHORITY",
    "CERTIFY_AUTHORITY",
    "TRANSFER_AUTHORITY",
    "EXPAND_AUTHORITY",
    "ADOPT_AUTHORITY",
}

semantic_trigger_ops = {
    "ADOPT_EXTERNAL_ASSERTION",
    "REINTERPRET_CLAIM",
    "EXPAND_CLAIM_SCOPE",
    "DROP_NON_CLAIMS",
    "SEMANTIC_COMPRESSION",
}

# Preserve the existing semantic fixture name, but make it a single-condition semantic-adoption fixture.
semantic = deepcopy(semantic_original)
semantic["interaction_id"] = "surface-interaction-invalid-interop-semantic-adoption-v0-1"
semantic["description"] = (
    "Invalid Interoperability Surface interaction: attempts to adopt an external assertion "
    "as Fork-native semantics without borrowing authority."
)
semantic["permitted_operations"] = unique(
    [op for op in base_ops if op not in authority_trigger_ops and op not in semantic_trigger_ops]
    + ["ADOPT_EXTERNAL_ASSERTION"]
)
semantic["authority_effect"] = neutral_authority
semantic["semantic_effect"] = "SEMANTIC_ADOPTION_ATTEMPTED"
semantic["declared_outcome"] = "SEMANTIC_ADOPTION_ATTEMPTED"
semantic.setdefault("limitations", [])
if "Fixture intentionally isolates semantic adoption from authority absorption." not in semantic["limitations"]:
    semantic["limitations"].append("Fixture intentionally isolates semantic adoption from authority absorption.")

# Add a separate single-condition authority-absorption fixture.
authority = deepcopy(semantic_original)
authority["interaction_id"] = "surface-interaction-invalid-authority-absorption-v0-1"
authority["description"] = (
    "Invalid Interoperability Surface interaction: attempts to import external authority "
    "into Fork's evidence-boundary surface without semantic adoption."
)
authority["permitted_operations"] = unique(
    [op for op in base_ops if op not in authority_trigger_ops and op not in semantic_trigger_ops]
    + ["IMPORT_EXTERNAL_AUTHORITY"]
)
authority["authority_effect"] = "AUTHORITY_BORROWING_ATTEMPTED"
authority["semantic_effect"] = neutral_semantic
authority["declared_outcome"] = "AUTHORITY_ABSORPTION_ATTEMPTED"
authority.setdefault("limitations", [])
if "Fixture intentionally isolates authority absorption from semantic adoption." not in authority["limitations"]:
    authority["limitations"].append("Fixture intentionally isolates authority absorption from semantic adoption.")

dump_json(semantic_path, semantic)
dump_json(authority_path, authority)
print(f"Updated semantic-only fixture: {semantic_path.relative_to(root)}")
print(f"Created authority-only fixture: {authority_path.relative_to(root)}")

# Update crosswalk stale roadmap section.
crosswalk = read_text(crosswalk_path)

hardening_section = """## Surface Interaction Hardening Status

The first Surface Interaction Contract hardening pass has now been added.

Current artifacts include:

- `schemas/surface_interaction_v0_1.schema.json`
- `tools/check_surface_interaction_v0_1.py`
- A valid reliance-to-evidence-boundary fixture.
- A boundary-mutation invalid fixture.
- A semantic-adoption invalid fixture.
- An authority-absorption invalid fixture.
- `tests/test_surface_interaction_v0_1.py`
- `.github/workflows/surface-interaction-v0-1.yml`

The remaining hardening work is narrower:

- Expand fixture coverage across additional surface pairs.
- Keep each invalid fixture focused on a single failure mode unless a fixture is explicitly testing multi-trigger precedence.
- Keep the checker outcome bounded to structural inspectability and non-absorption failures.
- Continue syncing this crosswalk when checker coverage changes.
"""

pattern = re.compile(
    r"(?ms)^##\s+Next Hardening Milestone\s*\n.*?(?=^##\s+|\Z)"
)
if pattern.search(crosswalk):
    crosswalk = pattern.sub(hardening_section.rstrip() + "\n\n", crosswalk)
elif "## Surface Interaction Hardening Status" not in crosswalk:
    crosswalk = crosswalk.rstrip() + "\n\n" + hardening_section

proof_surface_section = """<!-- FORK-PROOF-SURFACE-TERMINOLOGY:START -->
## Proof Surface Terminology Reconciliation

The phrase "proof surface" appears historically in two bounded senses inside the Fork repository.

First, in audience-facing surface doctrine, the Proof Surface is a technical-review lane: the schemas, checkers, fixtures, receipts, and verification commands a diligence reviewer can inspect.

Second, in simulation doctrine, the Governance Simulation Proof Surface is a falsifiability mechanism: scenarios that test whether claim boundaries, non-claims, handoff rules, and reliance semantics remain inspectable under recomposition, altered conditions, invalid handoffs, or adversarial interpretation.

Under the modular surface model, these meanings reconcile as follows:

| Historical phrase | Modular-surface mapping | Boundary |
|---|---|---|
| Proof Surface as reviewer lane | Reviewer access to Evidence Boundary, Transition, Reliance, Interoperability, and Simulation artifacts through schemas, checkers, fixtures, receipts, and verification commands. | Does not mean proof of correctness, compliance, safety, legal sufficiency, or authority. |
| Governance Simulation Proof Surface | Primarily maps to the Simulation Surface. | Tests whether boundary failures are inspectable; does not certify real-world correctness or policy sufficiency. |

Accordingly, "proof surface" should be read as bounded structural inspectability, not truth certification or authority.
<!-- FORK-PROOF-SURFACE-TERMINOLOGY:END -->"""

marker_pattern = re.compile(r"(?ms)<!-- FORK-PROOF-SURFACE-TERMINOLOGY:START -->.*?<!-- FORK-PROOF-SURFACE-TERMINOLOGY:END -->")
if marker_pattern.search(crosswalk):
    crosswalk = marker_pattern.sub(proof_surface_section, crosswalk)
else:
    insert_after = re.search(r"(?m)^##\s+Reconciling Existing Fork Models\s*$", crosswalk)
    if insert_after:
        start = insert_after.end()
        next_heading = re.search(r"(?m)^##\s+", crosswalk[start:])
        if next_heading:
            pos = start + next_heading.start()
            crosswalk = crosswalk[:pos].rstrip() + "\n\n" + proof_surface_section + "\n\n" + crosswalk[pos:].lstrip()
        else:
            crosswalk = crosswalk.rstrip() + "\n\n" + proof_surface_section + "\n"
    else:
        crosswalk = crosswalk.rstrip() + "\n\n" + proof_surface_section + "\n"

write_text(crosswalk_path, crosswalk)
print(f"Updated crosswalk: {crosswalk_path.relative_to(root)}")

# Clarify the one ambiguous proof-surface sentence in modular surface doc if present.
if modular_surface_path.exists():
    modular_surface = read_text(modular_surface_path)
    modular_surface = modular_surface.replace(
        "Fork has matured from a bounded proof surface into modular evidence-boundary infrastructure",
        "Fork has matured from a bounded technical proof-surface package into modular evidence-boundary infrastructure"
    )
    write_text(modular_surface_path, modular_surface)
    print(f"Checked modular surface terminology: {modular_surface_path.relative_to(root)}")

# Add verification command section.
verification_section = """<!-- FORK-SURFACE-INTERACTION-VERIFY:START -->
## Surface Interaction Contract v0.1

Run the Surface Interaction Contract checker against the valid fixture:

```powershell
python .\\tools\\check_surface_interaction_v0_1.py `
  .\\examples\\surface-interaction\\valid\\valid_reliance_references_evidence_boundary_v0_1.json
```

Expected outcome:

```text
SURFACE_INTERACTION_CONFORMS
```

Run the checker against the invalid fixtures with expected-invalid handling:

```powershell
python .\\tools\\check_surface_interaction_v0_1.py `
  .\\examples\\surface-interaction\\invalid\\invalid_evidence_boundary_mutation_attempt_v0_1.json `
  .\\examples\\surface-interaction\\invalid\\invalid_interop_semantic_adoption_attempt_v0_1.json `
  .\\examples\\surface-interaction\\invalid\\invalid_authority_absorption_attempt_v0_1.json `
  --expect-invalid
```

Expected outcomes include:

```text
SURFACE_INTERACTION_NOT_INSPECTABLE
SEMANTIC_ADOPTION_ATTEMPTED
AUTHORITY_ABSORPTION_ATTEMPTED
```

The checker remains bounded to structural inspectability and non-absorption outcomes. It does not establish truth, correctness, compliance, safety, legal sufficiency, or authority.
<!-- FORK-SURFACE-INTERACTION-VERIFY:END -->"""

if verification_path.exists():
    verification = read_text(verification_path)
    ver_pattern = re.compile(r"(?ms)<!-- FORK-SURFACE-INTERACTION-VERIFY:START -->.*?<!-- FORK-SURFACE-INTERACTION-VERIFY:END -->")
    if ver_pattern.search(verification):
        verification = ver_pattern.sub(verification_section, verification)
    else:
        verification = verification.rstrip() + "\n\n" + verification_section + "\n"
    write_text(verification_path, verification)
    print(f"Updated verification commands: {verification_path.relative_to(root)}")
else:
    write_text(verification_path, "# Verification Commands v0.1\n\n" + verification_section + "\n")
    print(f"Created verification commands: {verification_path.relative_to(root)}")

# Add pytest coverage.
test_text = r'''import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_surface_interaction_v0_1.py"
VALID_FIXTURE = ROOT / "examples" / "surface-interaction" / "valid" / "valid_reliance_references_evidence_boundary_v0_1.json"
INVALID_FIXTURES = {
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_evidence_boundary_mutation_attempt_v0_1.json": "SURFACE_INTERACTION_NOT_INSPECTABLE",
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_interop_semantic_adoption_attempt_v0_1.json": "SEMANTIC_ADOPTION_ATTEMPTED",
    ROOT / "examples" / "surface-interaction" / "invalid" / "invalid_authority_absorption_attempt_v0_1.json": "AUTHORITY_ABSORPTION_ATTEMPTED",
}


def run_checker(*args):
    return subprocess.run(
        [sys.executable, str(CHECKER), *[str(arg) for arg in args]],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def combined_output(result):
    return (result.stdout or "") + (result.stderr or "")


def test_valid_surface_interaction_fixture_conforms():
    result = run_checker(VALID_FIXTURE)
    output = combined_output(result)

    assert result.returncode == 0, output
    assert "SURFACE_INTERACTION_CONFORMS" in output
    assert "DECLARED_OUTCOME_MISMATCH" not in output


def test_invalid_surface_interaction_fixtures_match_declared_outcomes():
    for fixture, expected_outcome in INVALID_FIXTURES.items():
        result = run_checker(fixture)
        output = combined_output(result)

        assert result.returncode != 0, output
        assert expected_outcome in output
        assert "DECLARED_OUTCOME_MISMATCH" not in output


def test_invalid_surface_interaction_fixtures_pass_with_expect_invalid():
    result = run_checker(*INVALID_FIXTURES.keys(), "--expect-invalid")
    output = combined_output(result)

    assert result.returncode == 0, output
    for expected_outcome in INVALID_FIXTURES.values():
        assert expected_outcome in output
    assert "DECLARED_OUTCOME_MISMATCH" not in output
'''
write_text(tests_path, test_text)
print(f"Created pytest coverage: {tests_path.relative_to(root)}")

workflow_text = """name: Surface Interaction v0.1

on:
  push:
    paths:
      - "schemas/surface_interaction_v0_1.schema.json"
      - "tools/check_surface_interaction_v0_1.py"
      - "examples/surface-interaction/**"
      - "tests/test_surface_interaction_v0_1.py"
      - ".github/workflows/surface-interaction-v0-1.yml"
  pull_request:
    paths:
      - "schemas/surface_interaction_v0_1.schema.json"
      - "tools/check_surface_interaction_v0_1.py"
      - "examples/surface-interaction/**"
      - "tests/test_surface_interaction_v0_1.py"
      - ".github/workflows/surface-interaction-v0-1.yml"

jobs:
  surface-interaction:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install pytest
        run: python -m pip install pytest

      - name: Run Surface Interaction valid fixture
        run: |
          python tools/check_surface_interaction_v0_1.py \\
            examples/surface-interaction/valid/valid_reliance_references_evidence_boundary_v0_1.json

      - name: Run Surface Interaction invalid fixtures
        run: |
          python tools/check_surface_interaction_v0_1.py \\
            examples/surface-interaction/invalid/invalid_evidence_boundary_mutation_attempt_v0_1.json \\
            examples/surface-interaction/invalid/invalid_interop_semantic_adoption_attempt_v0_1.json \\
            examples/surface-interaction/invalid/invalid_authority_absorption_attempt_v0_1.json \\
            --expect-invalid

      - name: Run Surface Interaction pytest coverage
        run: python -m pytest tests/test_surface_interaction_v0_1.py -q
"""
write_text(workflow_path, workflow_text)
print(f"Created CI workflow: {workflow_path.relative_to(root)}")
'@

$TempPy = Join-Path $RepoRoot ".tmp_fix_surface_interaction_coherence_v0_1.py"
$env:FORK_REPO_ROOT = $RepoRoot

Write-Utf8NoBomLf -Path $TempPy -Text $PatchPy

try {
    Write-Host "Applying coherence fixes..." -ForegroundColor Cyan
    python $TempPy
    if ($LASTEXITCODE -ne 0) {
        throw "Python patch failed."
    }
}
finally {
    if (Test-Path -LiteralPath $TempPy) {
        Remove-Item -LiteralPath $TempPy -Force
    }
}

$MarkdownPaths = @(
    (Join-Path $RepoRoot "docs\modular-surface\FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md"),
    (Join-Path $RepoRoot "docs\modular-surface\FORK_MODULAR_SURFACE_v0_1.md"),
    (Join-Path $RepoRoot "docs\VERIFICATION_COMMANDS_v0_1.md")
) | Where-Object { Test-Path -LiteralPath $_ }

Assert-NoOddMarkdownFences -Paths $MarkdownPaths

Write-Host ""
Write-Host "Running Surface Interaction checker on valid fixture..." -ForegroundColor Cyan
python (Join-Path $RepoRoot "tools\check_surface_interaction_v0_1.py") `
    (Join-Path $RepoRoot "examples\surface-interaction\valid\valid_reliance_references_evidence_boundary_v0_1.json")

if ($LASTEXITCODE -ne 0) {
    throw "Valid Surface Interaction fixture failed."
}

Write-Host ""
Write-Host "Running Surface Interaction checker on invalid fixtures..." -ForegroundColor Cyan
python (Join-Path $RepoRoot "tools\check_surface_interaction_v0_1.py") `
    (Join-Path $RepoRoot "examples\surface-interaction\invalid\invalid_evidence_boundary_mutation_attempt_v0_1.json") `
    (Join-Path $RepoRoot "examples\surface-interaction\invalid\invalid_interop_semantic_adoption_attempt_v0_1.json") `
    (Join-Path $RepoRoot "examples\surface-interaction\invalid\invalid_authority_absorption_attempt_v0_1.json") `
    --expect-invalid

if ($LASTEXITCODE -ne 0) {
    throw "Invalid Surface Interaction fixture check failed."
}

Write-Host ""
Write-Host "Running pytest coverage for Surface Interaction..." -ForegroundColor Cyan
python -m pytest (Join-Path $RepoRoot "tests\test_surface_interaction_v0_1.py") -q

if ($LASTEXITCODE -ne 0) {
    throw "Surface Interaction pytest coverage failed."
}

Write-Host ""
Write-Host "Checking diff whitespace..." -ForegroundColor Cyan
git -C $RepoRoot diff --check -- $PlannedPaths
if ($LASTEXITCODE -ne 0) {
    throw "git diff --check failed."
}

Write-Host ""
Write-Host "Diff stat:" -ForegroundColor Cyan
git -C $RepoRoot diff --stat -- $PlannedPaths

if ($NoCommit) {
    Write-Host "NoCommit specified; skipping git add/commit/tag/push." -ForegroundColor Yellow
    exit 0
}

$AddPaths = @(
    "examples\surface-interaction\invalid\invalid_authority_absorption_attempt_v0_1.json",
    "examples\surface-interaction\invalid\invalid_interop_semantic_adoption_attempt_v0_1.json",
    "docs\modular-surface\FORK_MODULAR_SURFACE_CROSSWALK_v0_1.md",
    "docs\modular-surface\FORK_MODULAR_SURFACE_v0_1.md",
    "docs\VERIFICATION_COMMANDS_v0_1.md",
    "tests\test_surface_interaction_v0_1.py",
    ".github\workflows\surface-interaction-v0-1.yml"
)

if (-not $SkipAddScript) {
    $ScriptPath = $MyInvocation.MyCommand.Path
    if ($ScriptPath) {
        $FullScriptPath = [System.IO.Path]::GetFullPath($ScriptPath)
        if ($FullScriptPath.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            $RelativeScriptPath = $FullScriptPath.Substring($RepoRoot.Length).TrimStart('\', '/')
            $AddPaths += $RelativeScriptPath
        }
    }
}

$ExistingAddPaths = @()
foreach ($Path in $AddPaths) {
    if (Test-Path -LiteralPath (Join-Path $RepoRoot $Path)) {
        $ExistingAddPaths += $Path
    }
}

Write-Host ""
Write-Host "Staging planned files..." -ForegroundColor Cyan
git -C $RepoRoot add -- $ExistingAddPaths

$StagedFiles = git -C $RepoRoot diff --cached --name-only
if (-not $StagedFiles) {
    Write-Host "No staged changes detected. Nothing to commit." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Staged files:" -ForegroundColor Cyan
$StagedFiles | ForEach-Object { Write-Host " - $_" }

Write-Host ""
Write-Host "Commit diff stat:" -ForegroundColor Cyan
git -C $RepoRoot diff --cached --stat

Write-Host ""
Write-Host "Committing..." -ForegroundColor Cyan
git -C $RepoRoot commit -m $CommitMessage

if (-not $NoTag) {
    Write-Host ""
    Write-Host "Creating annotated tag $TagName..." -ForegroundColor Cyan
    git -C $RepoRoot tag -a $TagName -m $TagMessage
}

if (-not $NoPush) {
    Write-Host ""
    Write-Host "Pushing main..." -ForegroundColor Cyan
    git -C $RepoRoot push

    if (-not $NoTag) {
        Write-Host ""
        Write-Host "Pushing tag $TagName..." -ForegroundColor Cyan
        git -C $RepoRoot push origin $TagName
    }
}
else {
    Write-Host "NoPush specified; skipping git push." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Final status:" -ForegroundColor Cyan
git -C $RepoRoot status -sb
