# AHI Reviewer Packet Limitations v0.1

## Purpose

This document narrows how the current AHI proof surface should be read by reviewers.

It is intended to prevent over-reading the current checker and viewer results.

## Current AHI v0.1 proof posture

The current AHI v0.1 surface demonstrates:

- presence of expected scenario files;
- JSON parseability for authored fixture files;
- bounded literal semantic assertions over authored fixture fields;
- absence of selected overclaim phrases;
- preservation of non-claim vocabulary;
- viewer bundle generation;
- deterministic viewer reconstruction from a clean working tree.

This is a valid and useful proof-surface stage. It shows that the authored scenario fixtures and reviewer-facing bundles are internally consistent with the stated boundary model.

## What current AHI v0.1 does not yet prove

Current AHI v0.1 does not yet prove that Fork independently derives a revocation visibility gap from modeled System A/B/C behavior.

Current AHI v0.1 does not yet stand up independent state systems and compute a split-state condition from their divergence.

Current AHI v0.1 does not yet prove live-system detection, runtime enforcement, execution blocking, compliance determination, legal sufficiency, admissibility, correctness, negligence, excuse, or production readiness.

## Recommended wording

Use:

```text
The current AHI proof surface verifies bounded fixture consistency, reconstruction posture, non-claim discipline, and viewer determinism.
```

Avoid:

```text
The current AHI proof surface proves Fork detects split-state failures.
```

Use:

```text
Scenario 09 records and verifies the structure of a revocation visibility and split-state boundary.
```

Avoid:

```text
Scenario 09 proves Fork dynamically detected a revocation propagation failure.
```

## Scenario 08/09 boundary

Scenario 08 and Scenario 09 remain distinct.

Scenario 08:

```text
prior validity does not imply current validity
```

Scenario 09:

```text
a current validity-changing event does not automatically become visible, consumed, or operative downstream
```

Together, they model a real cross-system governance failure pattern. The current proof posture verifies that the scenario artifacts preserve this distinction without turning Fork into an authority, compliance, or fault oracle.

## Next maturity target

The next maturity target is computed Scenario 09 v0.2.

The computed variant should derive the gap from independent inputs:

- System A revocation state;
- System B synchronization or cache state;
- System C reliance attempt;
- freshness or tolerance policy.

The checker should then compute whether the result is:

- no gap;
- gap within tolerance;
- revocation visibility gap recorded;
- split-state consumption gap recorded.

## Non-claims

This document does not reduce the value of the current AHI surface.

This document does not assert that Fork approves, certifies, authorizes, determines compliance, determines admissibility, establishes legal sufficiency, decides acceptance, judges correctness, determines negligence, determines excuse, or determines execution eligibility.

This document exists to keep reviewer-facing language aligned with what the current checkers actually verify.
