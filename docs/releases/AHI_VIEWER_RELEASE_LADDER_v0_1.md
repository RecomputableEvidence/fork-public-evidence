# AHI Viewer Release Ladder v0.1

## Purpose

This file maps the AHI viewer release tags to their functional milestones.

The viewer is a static, repo-local evidence viewer. It does not execute workflows, call external systems, approve records, determine compliance, or certify correctness.

## Release ladder

| Tag | Milestone |
|---|---|
| `ahi-viewer-v0.1` | Static AHI Boundary Explorer scaffold |
| `ahi-viewer-v0.1.1` | Deterministic bundle generation |
| `ahi-viewer-v0.1.2` | Viewer hardening checks and schemas |
| `ahi-viewer-v0.1.3` | Scenario 06 structural bundle support |
| `ahi-viewer-v0.1.4` | Scenario 06 semantic verification posture |
| `ahi-viewer-v0.1.5` | Scenario 07 external authority bridge support |

## Current latest viewer tag

```text
ahi-viewer-v0.1.5
```

## Viewer verification command

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_ahi_viewer_v0_1.ps1 -CheckDeterminism
```

Expected result:

```text
PASS: viewer builder is deterministic from a clean working tree
PASS: AHI viewer v0.1 hardening checks completed
```

## Viewer invariants

The viewer checker verifies:

- required viewer files exist;
- bundle and scenario registry parse as JSON;
- bundle header is bounded and deterministic;
- scenario count matches registry;
- scenario postures are in the approved enum;
- scenario IDs and numbers are unique;
- registry scenario IDs are represented in bundle;
- referenced scenario and artifact paths exist;
- selected fields and checker coverage are present;
- viewer JavaScript avoids forbidden runtime primitives;
- non-authority posture language is present;
- prohibited oracle phrases are absent;
- deterministic builder behavior does not dirty the repository.

## Non-authority posture

The viewer is read-only and repo-local.

It does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.