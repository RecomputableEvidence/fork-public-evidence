# AHI Viewer v0.1 — Fork Boundary Explorer

## Purpose

`ahi-viewer-v0.1` is a static, repo-local, read-only Fork Boundary Explorer for the Accountable Handoff Interoperability simulation proof surface.

It reduces ambiguity for reviewers with different technical backgrounds by rendering the existing scenario registry and artifacts as an inspectable evidence surface.

## Non-authority statement

Fork Boundary Explorer is a read-only evidence viewer for accountable handoff records. It does not approve, certify, score, authorize, or judge correctness. It shows what the record supports, what it explicitly does not support, and what remains unresolved.

## Scope

This viewer is:

- static only
- repo-local
- read-only
- backend-free
- auth-free
- workflow-free
- scoring-free
- GRC-integration-free

It does not modify artifacts and does not create new governance claims.

## Source of truth

The viewer data builder reads:

```text
examples/simulations/governance-proof-surface/scenario_registry.json
examples/simulations/governance-proof-surface/scenario_0X_*.md
examples/simulations/governance-proof-surface/artifacts/scenario_0X_*.json
examples/simulations/governance-proof-surface/artifacts/scenario_0X_*.md
```

The generated viewer bundle is written to:

```text
docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json
```

## Build data bundle

From repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_ahi_viewer_data_v0_1.ps1 -ForceOverwrite
```

Validate the generated bundle:

```powershell
Get-Content -Raw .\docs\viewer\ahi-viewer-v0_1\data\scenarios_bundle.json | ConvertFrom-Json | Out-Null
```

## Open locally

Use a local static server from repo root so the browser can fetch `data/scenarios_bundle.json`.

```powershell
python -m http.server 8765
```

Then open:

```text
http://localhost:8765/docs/viewer/ahi-viewer-v0_1/
```

If you use `file://`, some browsers may block `fetch`. The local server path is preferred.

## Viewer functions

The v0.1 viewer implements four functions:

1. Scenario Catalog
2. Scenario Detail
3. Claims / Non-Claims / Unresolved
4. Artifact Drilldown

## Posture enum

The viewer uses the posture enum from `scenario_registry.json` as the primary maturity layer:

```text
BASELINE
STRUCTURAL
SEMANTICALLY_VERIFIED
SCAFFOLD
```

Failure-mode terms such as `AUTHORITY_LEAKAGE`, `NON_CLAIM_SUPPRESSION`, and `POLICY_REFERENCE_LAUNDERING` are categories or boundary effects, not verification posture.

## Commit note

Recommended commit message:

```text
Add static AHI boundary explorer scaffold
```

Use a separate viewer tag only after the viewer renders and the bundle verifies locally:

```text
ahi-viewer-v0.1
```
