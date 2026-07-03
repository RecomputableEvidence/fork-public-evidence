# AHI Verification Matrix v0.3

## Purpose

This matrix gives reviewers a bounded view of what the current AHI proof surface verifies structurally.

The checks verify presence, JSON validity, bounded scenario semantics, non-authority language posture, viewer bundle integrity, canonical comparison pairs, and deterministic rebuild behavior.

They do not verify legal sufficiency, compliance, admissibility, approval, authorization, safety, correctness, negligence, excuse, external acceptance, or execution eligibility.

## Verification commands

| Check | Command | Expected result |
|---|---|---|
| Main AHI proof surface | `powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1` | Scenarios 01–09 pass bounded proof-surface checks |
| Viewer v0.1 | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism` | Scenario count: 9; deterministic clean rebuild |
| Viewer v0.2 | `powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism` | Canonical comparison pairs pass; deterministic clean rebuild |
| Whitespace and patch hygiene | `git diff --check` | No whitespace errors |
| Repository state | `git status -sb` | Clean branch after commit |

## Non-authority posture

Permitted interpretation:

```text
Fork preserved an inspectable boundary record.
Fork recorded unsupported inheritance.
Fork recorded required revalidation.
Fork made a downstream reliance gap visible.
```

Forbidden interpretation:

```text
Fork approved, authorized, certified, scored, determined compliance, established legal sufficiency, decided correctness, assigned negligence, or excused reliance.
```
