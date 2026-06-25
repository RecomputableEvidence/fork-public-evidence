# Release Notes v0.1

## Overview

This release introduces the initial Transition Localization discipline artifacts and the first calibration case.

## Included Artifacts

- `docs/TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md`  
  - Defines the Transition Localization invariants as a normative dependency.

- `docs/CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md`  
  - Specifies the casebook procedure for applying the invariants to concrete transitions.

- `docs/cases/CASE_001_AI_SAFETY_FINE_TUNE.md`  
  - Calibration case: AI safety evaluation → fine-tuned derivative model.
  - Demonstrates a Class D (Unlocalized transfer path) outcome without making claims about artifact safety.

- `docs/cases/CASE_001_REVIEW_WORKSHEET.md`  
  - Reviewer worksheet for Case 001.
  - Supports systematic application of the procedure and captures confidence per stage.

- `docs/cases/CASE_001_VARIANCE_REPORT.md`  
  - Template for summarizing reviewer variance on Case 001.
  - Distinguishes observational, procedural, and taxonomic variance.

## Specification Freeze Rule (v0.1)

For this release:

- The invariant grammar (`TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md`) and casebook procedure (`CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md`) are treated as frozen.
- No changes to the invariants should be made until:
  - Case 001 reviewer replay is completed,
  - Case 001 variance report is completed,
  - At least one additional domain case is executed.

Exceptions:

- Ambiguity that prevents procedure execution,
- Internal contradiction in the invariant layer.

The goal of v0.1 is to begin generating empirical evidence about the reproducibility of the Transition Localization method, not to further refine the theory in the absence of data.
