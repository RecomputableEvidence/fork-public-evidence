# AHI Viewer Release Ladder v0.2

## Purpose

This document maps AHI viewer releases to the current proof-surface state.

## Viewer v0.1 family

Viewer v0.1 provides the canonical static scenario-bundle surface.

| Tag | Scope |
|---|---|
| `ahi-viewer-v0.1.5` | Scenario 07 external authority bridge support |
| `ahi-viewer-v0.1.6` | Scenario 08 stale validity / authority revocation support |

Current Viewer v0.1 expected scenario count:

```text
8
```

Verification:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected result:

```text
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Viewer v0.2 family

Viewer v0.2 provides static comparison mode.

| Tag | Scope |
|---|---|
| `ahi-viewer-v0.2` | Initial comparison mode implementation |
| `ahi-viewer-v0.2-main` | Main-merge tag for initial comparison mode |
| `ahi-viewer-v0.2.1` | Scenario 08 comparison support and determinism hardening |

Current canonical comparison pairs:

| Pair | Meaning |
|---|---|
| `PAIR-S01-S02` | baseline unbounded handoff vs Fork-preserved handoff |
| `PAIR-S03-S04` | scope expansion vs authority leakage |
| `PAIR-S05-S06` | policy-reference laundering vs distributed handoff |
| `PAIR-S06-S07` | distributed handoff vs external authority bridge |
| `PAIR-S07-S08` | external authority bridge vs stale validity / authority revocation |

Verification:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_2.ps1 -CheckDeterminism
```

Expected result:

```text
PASS: viewer v0.2 comparison builder is deterministic from a clean working tree
PASS: AHI viewer v0.2 comparison mode checks completed
```

## Viewer non-authority posture

The viewers are static inspection surfaces.

They do not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, judge correctness, or create execution eligibility.
