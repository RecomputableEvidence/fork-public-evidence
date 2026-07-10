# Public Verifier Platform Fallback v0.1

Status: Public review accessibility note.
Scope: Platform fallback for reviewers who cannot execute the PowerShell public verifier.

## 1. Background

The primary public review verifier is:

- `scripts/verify_public_review_package_v0_1.ps1`

Run on Windows PowerShell or PowerShell Core:

- `powershell -ExecutionPolicy Bypass -File .\scripts\verify_public_review_package_v0_1.ps1`
- `pwsh -File ./scripts/verify_public_review_package_v0_1.ps1`

Public Review Round 005 showed that a Linux reviewer may not have `pwsh` available. In that case, the reviewer cannot claim to have executed the named PowerShell verifier.

## 2. Fallback classification

If the PowerShell verifier cannot run, use this classification:

- manual public-verifier reconstruction

Do not classify it as:

- public verifier execution

Manual reconstruction is useful evidence, but it is not identical to running the named verifier artifact.

## 3. Linux/macOS fallback commands

From repo root, run:

```bash
git status -sb
git log -1 --oneline

python3 tools/check_boundary_pressure_review_cases_v0_1.py --json --run-adversarial
python3 tools/check_public_review_round_004_interactions_v0_1.py --json
python3 tools/check_public_review_round_005_interactions_v0_1.py --json
python3 tools/check_longitudinal_reconstruction_day0_packet_v0_1.py --json

git diff --check
git diff --cached --check
```

If `python3` is unavailable but `python` is available, substitute `python`.

## 4. Expected current signals

Boundary pressure checker:

- default total: 4
- default passed: 4
- default failed: 0
- adversarial total: 4
- adversarial passed: 4
- adversarial failed: 0

Round 004 interaction checker:

- total: 4
- passed: 4
- failed: 0

Round 005 interaction checker:

- total: 1
- passed: 1
- failed: 0

Longitudinal Day-0 checker:

- total: 27
- passed: 27
- failed: 0

Git checks:

- `git diff --check` exits 0
- `git diff --cached --check` exits 0

## 5. What this fallback does not prove

This fallback does not execute the PowerShell verifier.
It reconstructs the underlying currently documented checker and Git conditions using cross-platform commands.
A reviewer should record: operating system; shell; Python version; Git version; whether `powershell` or `pwsh` was available; whether the PowerShell verifier actually executed; whether manual reconstruction was used instead.

## 6. Boundary statement

A successful fallback reconstruction does not establish truth, compliance, legal sufficiency, safety, authorization, approval, certification, endorsement, validation, production readiness, procurement approval, or institutional authority.
It only records that the reviewer independently executed the listed underlying checks in their environment.