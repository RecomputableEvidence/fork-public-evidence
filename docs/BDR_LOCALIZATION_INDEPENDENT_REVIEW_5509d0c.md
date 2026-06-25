# Independent Review Note — BDR Localization v0.1

**Repository:** fork-public-evidence  
**Branch:** \dr-localization-v0.1\  
**Commit:** ``5509d0c``  
**Reviewer:** Claude (Anthropic) — Independent Third-Party Verifier  
**Method:** Fresh clone, branch checkout, direct artifact inspection, independent execution of tools and tests.

## Repository State

- Working tree: clean (no staged or unstaged changes).
- Remote tracking: ``origin/bdr-localization-v0.1`` synchronized with local.
- Commit scope: confined to ``README.md`` (normalizing encoding and fixing mojibake in copyright section).
- Test suite: 533 tests passing, 0 failing (as recorded at review time).

The reviewer confirms that the repository state at ``5509d0c`` is reproducible from the remote and that no unexplained generated artifacts or hygiene anomalies are present.

## Structural Assessment

**Disposition:** Supported with observations.

The BDR Localization implementation is internally coherent:

- Doctrine:
  - ``docs/TRANSITION_LOCALIZATION_AND_INDEPENDENT_ESTABLISHMENT_v0_1.md``
  - ``docs/BDR_LOCALIZATION_POSTURE_v0_1.md``
- Implementation:
  - \	ools/check_boundary_delta_record.py\
- Fixtures and tests:
  - Boundary-delta fixtures in ``examples/boundary_delta_record/``
  - Test suite in \	ests/\

Key structural findings:

- The localization-status vocabulary and limitation tokens are consistently named across docs, code, and tests.
- The Class A/B/C/D taxonomy in doctrine maps correctly to Case 001's Class D determination.
- Case 001 and its reviewer worksheet/addendum independently converge on:
  - Establishment: Safety Protocol Y on Model X V1
  - Mechanism analysis: no preservation / no governed transfer / no new establishment
  - Determination path: Unlocalized
  - Classification: Class D — Unlocalized transfer path

Observation:

- ``check_boundary_delta_record.py`` currently emits \"outcome": "INSPECTABLE"\ as a disclosed placeholder. The posture doc discusses ``NOT_INSPECTABLE`` as a v0.1 structural outcome, but the implementation does not yet produce it. This is a known implementation boundary, not a hidden discrepancy.

## Boundary Analysis

**Correctly localized claims:**

- The localization test inspects whether an establishment event is declared (via ``establishment_ref``), not whether it “should” exist.
- Fixtures with claims but no establishment_ref correctly produce ``NO_LOCALIZABLE_ESTABLISHMENT``.
- The non-claim limitation \
o_localized_establishment_for_transferred_property\ is emitted as a non-inferential, machine-readable limitation.

**Transition classification:**

- Doctrine defines four establishment classes (A–D) with clear criteria.
- Case 001 correctly classifies a fine-tune scenario (Model X V1 → Model X-FT V2, no preservation/transfer/new establishment) as Class D.
- The three mechanism paths (preservation, governed transfer, new establishment) are explicitly evaluated and found absent.

**Ambiguities and gaps:**

- Advisory vs. blocking posture for ``NO_LOCALIZABLE_ESTABLISHMENT`` is described in doctrine but not yet parameterized in the checker output (no explicit flag for advisory vs. blocking profile).
- Two doctrine documents referenced in the Case 001 addendum are absent:
  - ``docs/TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md``
  - ``docs/CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md``
  Their absence means fine-tune boundary-scoping guidance is currently implicit in the case narrative and addendum rather than encoded in reusable doctrine.

## Reproducibility Assessment

**Result:** Reproducible from repository artifacts alone, with one noted caveat.

An independent reviewer can:

- Clone the repo and check out \dr-localization-v0.1\ at ``5509d0c``.
- Read the core doctrine documents and posture.
- Execute \	ools/check_boundary_delta_record.py\ against the provided fixtures and obtain the documented outputs.
- Run the test suite and confirm all tests pass.
- Read:
  - ``docs/cases/CASE_001_AI_SAFETY_FINE_TUNE.md``
  - ``docs/cases/CASE_001_REVIEW_WORKSHEET.md``
  - ``docs/cases/CASE_001_REVIEW_WORKSHEET_ADDENDUM.md``
  and reconstruct the Case 001 determination path.

Caveat:

- ``docs/cases/CASE_001_VARIANCE_REPORT.md`` has unpopulated metric fields (reviewer count, review period, agreement rates). These are structural placeholders for future multi-reviewer calibration and do not yet contain data.

## Findings (Summary)

- **FINDING-BDR-001 (Cosmetic):**  
  README contains one residual U+FFFD replacement character in the string \Cases 002–003\ (en-dash was previously corrupted and replaced). This does not affect any governance artifact or checker behavior.

- **FINDING-BDR-002 (Observation):**  
  Checker emits ``INSPECTABLE`` unconditionally as a placeholder; posture doc anticipates ``NOT_INSPECTABLE`` as a structural outcome. Implementation and doctrine are aligned on localization status but not yet on the full outcome space.

- **FINDING-BDR-003 (Documentation completeness):**  
  ``TRANSITION_LOCALIZATION_INVARIANTS_v0_1.md`` and ``CASEBOOK_TRANSITION_LOCALIZATION_v0_1.md`` are referenced but absent. Boundary-scoping rules for fine-tune scenarios are thus carried only in Case 001 narrative and addendum.

- **FINDING-BDR-004 (Calibration maturity):**  
  ``CASE_001_VARIANCE_REPORT.md`` metric fields are unpopulated; multi-reviewer calibration data has not yet been recorded.

## Summary Determination

The BDR Localization branch at ``5509d0c`` is structurally coherent and internally consistent for its declared v0.1 scope. Claims are correctly localized to the evidence boundary; no unsupported inheritance or authority escalation was observed.

The identified findings are informational or observational, not correctness failures. They primarily concern documentation completeness, placeholder implementation boundaries, and future calibration metadata.

This review note is evidence about the branch at ``5509d0c``. It does not, by itself, extend authority to future versions or derived systems without their own establishment events.


