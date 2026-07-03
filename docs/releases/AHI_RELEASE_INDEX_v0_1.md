# AHI Release Index v0.1

## Purpose

This index is the reviewer-facing entry point for the Fork AHI simulation proof surface.

It maps the current simulation releases, viewer releases, scenario ladder, verification matrix, and local verification commands.

## Current release state

| Surface | Latest tag | Description |
|---|---:|---|
| AHI simulation surface | `ahi-sim-v0.1.8` | Scenario 07 external authority bridge simulation |
| AHI viewer surface | `ahi-viewer-v0.1.5` | Scenario 07 external authority bridge viewer support |

## Current scenario count

```text
7
```

## Current scenario ladder

| Scenario | Title | Primary boundary/failure mode |
|---:|---|---|
| 01 | Baseline unbounded handoff | Unbounded AI-assisted handoff |
| 02 | Fork-preserved handoff | Bounded evidence preservation |
| 03 | Scope expansion attempt | Downstream scope expansion |
| 04 | Authority leakage attempt | Authority-context leakage |
| 05 | Policy-reference laundering / non-claim suppression | Policy reference treated as policy satisfaction |
| 06 | Multi-system distributed handoff | Distributed authority inheritance |
| 07 | External authority bridge | Inspectability treated as external authority |

## Release documents

- `docs/releases/AHI_RELEASE_INDEX_v0_1.md`
- `docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md`
- `docs/releases/AHI_SCENARIO_LADDER_v0_1.md`
- `docs/releases/AHI_VIEWER_RELEASE_LADDER_v0_1.md`
- `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md`

## Primary verification commands

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_ahi_sim_v0_1_checks.ps1

powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected high-level results:

```text
PASS: ahi-sim-v0.1.x simulation proof-surface checks completed.
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Non-authority boundary

Fork records and verifies bounded evidence and transition-state properties.

Fork does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.

## Reviewer route

A cold reviewer should read in this order:

1. `docs/releases/AHI_RELEASE_INDEX_v0_1.md`
2. `docs/releases/AHI_VERIFICATION_MATRIX_v0_1.md`
3. `docs/releases/AHI_SCENARIO_LADDER_v0_1.md`
4. `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_1.md`
5. `docs/viewer/ahi-viewer-v0_1/README.md`
6. `docs/viewer/ahi-viewer-v0_1/index.html`

## Latest release tags

```text
ahi-sim-v0.1.8
ahi-viewer-v0.1.5
```

## Verification posture summary

The current surface demonstrates that Fork can preserve and check boundary-state records across increasingly complex governance handoffs without becoming an approval, compliance, authority, admissibility, or correctness layer.