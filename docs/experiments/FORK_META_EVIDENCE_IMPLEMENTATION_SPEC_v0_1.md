# Fork Meta-Evidence Package v0.1 — Frozen Implementation Specification

**Specification ID:** `FORK-META-EVIDENCE-SPEC-v0.1`<br>
**Status:** `FROZEN_FOR_IMPLEMENTATION`<br>
**Conceptual design:** `CLOSED`<br>
**Engineering status:** `READY_FOR_IMPLEMENTATION`<br>
**Publication authority:** `IMPLEMENTED_SCHEMAS_CHECKERS_TESTS_AND_RECEIPTS_ONLY`<br>
**Historical modification authority:** `NONE`

## Purpose

This package governs favorable, unfavorable, mixed, null, ambiguous, corrected, and withdrawn experimental outcomes through the same structural and provenance discipline.

The controlling invariant is:

> Outcome polarity must not determine evidentiary treatment.

Evidence standing follows declared provenance, observation method, reproducibility, scope, lineage, and externally supplied authority—not reward, consequence, professional recognition, or commercial usefulness.

## External-context boundary

`risk_tier_ref`, `impact_assessment_id`, `aims_process_phase`, and `required_provenance_profile_id` are externally owned references. Fork may preserve, structurally validate, link, and recompute declared relationships around them. Fork must not originate, infer, reclassify, approve, or validate their substantive meaning.

## Frozen surface

The package creates five protocols, seven JSON Schemas, two conservative registries, six Python checkers, valid and invalid fixtures, six unit-test modules, two execution receipts, and a SHA-256 manifest.

## Historical preservation

Existing CSH, Pair-001, CSH-AMEND-002, v0.1.1 repair, BDR, RGV, retrieval-degradation, exterior-review, recognition, attribution, and unfavorable execution artifacts are not rewritten. Older artifacts may be referenced only through bounded wrappers that identify missing context and prohibit retrospective inference.

## Checker authority

Checkers determine structural conformance to this package. They do not determine truth, correctness, legality, fairness, safety, compliance, legitimacy, risk classification, impact-assessment sufficiency, institutional authority, or production readiness.

## Implementation order

1. Protocols and specification.
2. Schemas.
3. Conservative registries.
4. Individual checkers.
5. Valid fixtures.
6. Invalid fixtures.
7. Unit tests.
8. Integrated checker.
9. Test execution.
10. Receipts and checksums.
11. Stop without commit, tag, publication, or push.

## Acceptance

Implementation is complete only when every generated JSON parses and conforms to its applicable schema, valid fixtures pass, invalid fixtures fail for intended reasons, multi-defect fixtures aggregate defects, non-conforming runs return non-zero, external context remains opaque, historical material remains unmodified, and the bounded package is covered by checksums.
