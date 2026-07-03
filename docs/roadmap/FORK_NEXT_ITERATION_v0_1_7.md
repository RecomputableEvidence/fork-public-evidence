# Fork Next Iteration v0.1.7

## Current baseline

- `ahi-sim-v0.1.6`: Scenario 06 distributed handoff structural simulation.
- `ahi-viewer-v0.1.3`: viewer support for Scenario 06 structural bundle.
- Deterministic static viewer bundle generation.
- Viewer hardening checks and schemas.

## Objective

Promote Scenario 06 from `STRUCTURAL` to `SEMANTICALLY_VERIFIED` only after a stronger checker verifies the actual semantic invariants around distributed authority non-inheritance.

## Required result

The repo should be able to show:

```text
Scenario 06 is artifact-backed.
Scenario 06 has a structural checker.
Scenario 06 has a semantic invariant checker.
The main AHI checker invokes both.
The viewer bundle remains deterministic.
The viewer can render Scenario 06 without implying approval, compliance, scoring, authorization, or correctness.
```

## Recommended tags after merge

- `ahi-sim-v0.1.7`
- optional: `ahi-viewer-v0.1.4`

## Next after v0.1.7

1. Viewer comparison mode v0.2.
2. Scenario 07 external authority bridge.
3. Release index mapping tags, scenarios, checkers, and viewer milestones.
