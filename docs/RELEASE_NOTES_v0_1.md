# Release Notes v0.1

## Transition Localization Measurement Layer

This release introduces the first reviewer calibration artifacts.

Added:

- docs/cases/CASE_001_REVIEW_WORKSHEET.md
- docs/cases/CASE_001_VARIANCE_REPORT.md

Purpose:

These artifacts measure whether independent reviewers can reproduce:

- establishment localization,
- transition definition,
- mechanism identification,
- determination path,
- A/B/C/D classification.

## Specification Freeze

The following remain stable during initial reviewer testing:

- TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md
- CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md
- CASE_001_AI_SAFETY_FINE_TUNE.md

Changes should be driven by observed variance, not hypothetical concerns.

## Current Validation Target

Independent reviewers applying the same procedure should produce consistent authority-path determinations for the same transition scenario.

This release does not claim:

- artifact safety,
- truth of underlying properties,
- correctness of deployment decisions,
- universal validation.

It measures reproducibility of transition analysis.
