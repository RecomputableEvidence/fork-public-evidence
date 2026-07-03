# AHI Viewer v0.2 — Comparison Mode

## Purpose

AHI Viewer v0.2 is a static comparison surface for Fork AHI scenarios.

It helps a reviewer compare two scenarios across:

- boundary movement;
- attempted inference;
- artifact coverage;
- required revalidation;
- Fork-supported verification;
- Fork non-claims.

## Current comparison pairs

The deterministic comparison builder generates the following canonical pairs when the corresponding scenarios exist in the v0.1 bundle:

| Pair | Purpose |
|---|---|
| Scenario 01 → Scenario 02 | Baseline unbounded handoff versus Fork-preserved handoff |
| Scenario 03 → Scenario 04 | Scope expansion versus authority leakage |
| Scenario 05 → Scenario 06 | Policy-reference laundering versus distributed handoff |
| Scenario 06 → Scenario 07 | Distributed internal authority boundary versus external authority bridge |

## Data sources

Viewer v0.2 consumes:

- `docs/viewer/ahi-viewer-v0_1/data/scenarios_bundle.json`
- `docs/viewer/ahi-viewer-v0_2/data/comparison_pairs.json`

The v0.2 builder is deterministic and does not call external services.

## Non-authority posture

The viewer is read-only and repo-local.

It does not approve, certify, score, authorize, determine compliance, determine admissibility, establish legal sufficiency, decide acceptance, or judge correctness.
