# Fork Internal Release Note  
## v0.6-provenance-tier-contract-lock

**Status:** Internal provenance-tier lock  
**Tag:** `v0.6-provenance-tier-contract-lock`  
**Commit:** `3bc62775782e307a0463dc932c1baa0182e7f3c4`  
**Repository state:** `main`  
**CI status:** Fork Evidence CI passed on `main`

## Summary

This internal lock records the first integrated Provenance Tier layer in Fork.

Fork now has a machine-enforced mechanism for preventing provenance escalation between generated output and documented evidence.

The v0.6 constitutional line is:

**Generated output is not documented evidence.**

The purpose of this lock is to prevent generated, interpretive, or derivative artifacts from silently satisfying stricter evidentiary requirements reserved for documented material.

This is an internal architectural milestone, not a product-readiness or external validation release.

## What Was Locked

This tag locks the following components on `main`:

1. **Provenance Tier Contract v0.1**

   Fork now defines provenance as an **admissibility constraint**, not merely descriptive metadata.

   **Epistemic invariant:**

   Meaning must not become more certain than its weakest supporting evidence.

   **Operational invariant:**

   No artifact may satisfy a higher provenance requirement than its declared tier or dependency graph permits.

2. **Supported Provenance Tiers**

   The v0.1 contract defines the following tiers:

   `DOCUMENTED`  
   `ATTRIBUTED`  
   `INTERPRETIVE`  
   `GENERATED`  
   `UNRESOLVED`

   In v0.1 these tiers are treated as admissibility states. Only `DOCUMENTED` and `GENERATED` are currently enforced in CI, with `ATTRIBUTED`, `INTERPRETIVE`, and `UNRESOLVED` reserved for future profiles.

3. **Generated-to-Documented Escalation Rejection**

   Provenance payloads are checked by:

   `tools/check_provenance_tier.py`

   The checker rejects a payload when:

   `required_provenance_tier = DOCUMENTED`  
   and  
   `declared_provenance_tier = GENERATED`

   In other words: a `GENERATED` artifact cannot satisfy a `DOCUMENTED` requirement under v0.1.

   Example failure class:

   `PROVENANCE_ESCALATION_DEFECT`

4. **Generated Dependency Contamination Rejection**

   The checker also rejects a payload when:

   `declared_provenance_tier = DOCUMENTED`  
   and  
   `dependency_provenance_tiers` contains `GENERATED`

   In other words: a `DOCUMENTED` artifact cannot depend on `GENERATED` content under v0.1.

   Example failure class:

   `PROVENANCE_DEPENDENCY_CONTAMINATION`

5. **Schema, Tooling, Examples, and Tests**

   This lock adds:

   `tools/check_provenance_tier.py`  
   `schemas/provenance_tier_v0_1.schema.json`  
   `examples/provenance_tier/valid_documented_source.json`  
   `examples/provenance_tier/invalid_generated_satisfies_documented.json`  
   `examples/provenance_tier/invalid_documented_depends_on_generated.json`  
   `tests/test_provenance_tier_v0_1.py`

6. **CI Enforcement**

   The Provenance Tier checks were added to the Fork Evidence CI workflow.

   The merged `main` branch passed CI after the Provenance Tier layer landed.

## Verified Local / CI State

At the time of lock:

- `python tools/check_line_endings.py` passed.
- `python tools/check_provenance_tier.py examples/provenance_tier/valid_documented_source.json` passed.
- Full invariant test suite passed with `27 passed`.
- GitHub Actions Fork Evidence CI passed on `main`.
- Tag `v0.6-provenance-tier-contract-lock` was pushed.

## What This Lock Claims

This lock claims only that:

1. Provenance Tier v0.1 is present on `main`.

2. Fork defines provenance as an admissibility constraint.

3. The checker rejects `GENERATED` artifacts attempting to satisfy `DOCUMENTED` requirements.

4. The checker rejects `DOCUMENTED` artifacts that depend on `GENERATED` content.

5. The valid documented-source example passes.

6. The invalid generated-as-documented example fails with `PROVENANCE_ESCALATION_DEFECT`.

7. The invalid documented-depends-on-generated example fails with `PROVENANCE_DEPENDENCY_CONTAMINATION`.

8. The Provenance Tier test suite passed locally and in CI after merge.

## What This Lock Does Not Claim

This lock does **not** claim the following planned or deferred capabilities:

1. Full provenance lattice enforcement.

2. Full re-elevation logic.

3. Attribution completeness enforcement.

4. `UNRESOLVED` reason-code enforcement.

5. Recomputability class enforcement.

6. Semantic inference governance.

This lock also does **not** claim:

7. Legal admissibility.

8. Regulatory compliance.

9. Source completeness.

10. Decision correctness.

11. Model accuracy.

12. Full reconstruction fidelity.

13. That all possible provenance escalation paths are detectable.

14. That generated material can never be useful.

15. That Fork determines truth.

## Interpretation Rule

A generated artifact may be preserved, inspected, routed, or reviewed.

It may not satisfy a documented-evidence requirement under v0.1.

Later profiles may define controlled, recomputable promotion paths; v0.1 explicitly does not.

A documented artifact must not depend on generated content unless a later approved profile explicitly permits a recomputable, non-inferential transformation path.

## Architectural Significance

This lock moves Provenance Tiers from metadata into repository-enforced admissibility control.

The boundary stack now present on `main` is:

- Claim Boundary: prevents evidence from claiming too much.
- Definition Boundary: prevents systems from classifying too much.
- Provenance Tier: prevents generated or lower-admissibility artifacts from satisfying higher evidentiary requirements.

Together, these layers provide semantic non-escalation guarantees: no artifact can silently escalate meaning beyond the weakest admissible evidence that supports it.

The resulting internal invariant is:

**Meaning must not become more certain than its weakest supporting evidence.**

The v0.6 constitutional line is:

**Generated output is not documented evidence.**
