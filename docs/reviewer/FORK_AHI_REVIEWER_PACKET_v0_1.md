# Fork AHI Reviewer Packet v0.1

## Purpose

This packet gives a technical, governance, risk, audit, or GRC reviewer a short path into the Fork AHI proof surface.

The goal is not endorsement.

The goal is to determine whether the proof surface is coherent, bounded, locally verifiable, and relevant to workflows where AI-assisted artifacts become part of institutional reliance.

## Reviewer question

```text
Can this repo make boundary-state loss visible where an AI-assisted artifact crosses systems, actors, policy contexts, authority contexts, or validity windows?
```

## What Fork is demonstrating

```text
preserve what crossed
preserve what did not cross
preserve what was relied on
preserve what remained unsupported
preserve what required revalidation
make unsupported inheritance visible later
```

## What Fork is not claiming

Fork is not claiming to govern the model, enforce runtime behavior, approve the workflow, certify compliance, decide admissibility, establish legal sufficiency, determine correctness, assign negligence, excuse reliance, or replace audit, GRC, legal, policy, or security review.

## Current proof surface

| Component | Current state |
|---|---|
| Scenarios | 9 |
| Simulation tag | `ahi-sim-v0.1.10` |
| Viewer v0.1 tag | `ahi-viewer-v0.1.7` |
| Viewer v0.2 tag | `ahi-viewer-v0.2.2` |
| Release index | `ahi-release-index-v0.3` |
| Reviewer packet | `ahi-reviewer-packet-v0.1` |

## Fast review path

1. Read `docs/reviewer/AHI_PROOF_SURFACE_MAP_v0_1.md`.
2. Read `docs/releases/AHI_SCENARIO_LADDER_v0_3.md`.
3. Inspect Scenario 08 and Scenario 09 together.
4. Run the local verification commands in `docs/releases/AHI_LOCAL_VERIFICATION_GUIDE_v0_3.md`.
5. Open the viewer files locally:
   - `docs/viewer/ahi-viewer-v0_1/index.html`
   - `docs/viewer/ahi-viewer-v0_2/index.html`

## Most important reviewer seam

```text
Scenario 08: prior validity does not imply current validity.
Scenario 09: a current validity-changing event does not automatically become visible, consumed, or operative across downstream systems.
```

That pair is the current clearest expression of Fork’s transition-state thesis.

## Useful review questions

```text
Where is the boundary model coherent?
Where is it too narrow?
Where is it too broad?
Which scenario maps to a real workflow?
Which missing transition would matter in your environment?
What would you need to see before trusting this as a design-partner pilot surface?
```
