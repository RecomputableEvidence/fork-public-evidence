# AHI Viewer Release Ladder v0.3

## Viewer v0.1

Current tag:

```text
ahi-viewer-v0.1.7
```

Scope:

- Bundles Scenarios 01–09 from the scenario registry.
- Verifies scenario cardinality.
- Checks registry-to-bundle identity alignment.
- Checks referenced scenario and artifact paths.
- Preserves non-authority posture.
- Rebuilds deterministically from a clean working tree.

## Viewer v0.2

Current tag:

```text
ahi-viewer-v0.2.2
```

Scope:

- Presents canonical scenario comparison pairs.
- Includes the Scenario 08 ↔ Scenario 09 comparison.
- Verifies comparison-pair completeness.
- Preserves non-authority posture.
- Rebuilds comparison data deterministically from a clean working tree.

## Current comparison posture

```text
PAIR-S08-S09
```

Purpose:

```text
Compare stale-validity reliance after a validity change with split-state reliance where the validity-changing event is not confirmed visible or consumed across systems.
```
