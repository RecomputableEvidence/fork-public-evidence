STATUS: INTERNAL_CONTRACT
DEPENDS_ON:
  - docs/CLAIM_BOUNDARY_CONTRACT_v0_1.md
  - docs/CLAIM_BOUNDARY_ENFORCEMENT_PHASE_2.md
  - docs/CLAIM_BOUNDARY_BINDING_v0_1.md
  - docs/DEFINITION_BOUNDARY_CONTRACT_v0_1.md

TITLE: Fork Provenance Tier Contract v0.1

1. Purpose

Fork must not allow meaning to become more certain than its weakest supporting
evidence.

Provenance is not descriptive metadata. It is an admissibility constraint.

Fork is not restricting what systems may observe or infer. Fork is restricting
what systems may treat as true for action.

2. Core Invariant

Meaning must not become more certain than its weakest supporting evidence.

Operational invariant:
  No artifact may satisfy a higher provenance requirement than its declared tier
  or dependency graph permits.

3. Provenance Tiers v0.1

Supported tiers:

  - DOCUMENTED
  - ATTRIBUTED
  - INTERPRETIVE
  - GENERATED
  - UNRESOLVED

These tiers define admissibility constraints, not merely rank order.

Provenance should be treated as a lattice. v0.1 exposes a narrow enforcement
subset, but the doctrine must not assume a simple universal ladder.

4. Composition Rule

Composite artifacts inherit the lowest admissible provenance tier across their
dependency graph unless an approved recomputable, non-inferential transformation
emits a new artifact with its own provenance declaration.

v0.1 does not implement a full lattice engine. It implements two narrow refusal
rules around GENERATED and DOCUMENTED.

5. Re-elevation Discipline

Re-elevation must be narrowly constrained.

Approved non-inferential transformations for future re-elevation profiles may
include:

  - FORMAT_NORMALIZATION
  - CANONICALIZATION
  - CRYPTOGRAPHIC_VERIFICATION

Forbidden as provenance re-elevation mechanisms:

  - SUMMARIZATION
  - CLASSIFICATION
  - MODEL_EXTRACTION
  - SEMANTIC_INFERENCE
  - HUMAN_INTERPRETATION

v0.1 reserves this doctrine but does not yet implement full re-elevation
profiles.

6. No Silent Upgrade

No process may upgrade a provenance tier in place.

Any attempted provenance upgrade must emit a new artifact with:

  - its own provenance declaration
  - a dependency trace
  - a transformation declaration

No mutation of provenance status in place is permitted as a doctrine principle.

7. UNRESOLVED Discipline

UNRESOLVED is a structured evidentiary state, not a generic unknown.

Reserved reason codes:

  - UNRESOLVED_MISSING_SOURCE
  - UNRESOLVED_AMBIGUOUS_IDENTITY
  - UNRESOLVED_NON_RECOMPUTABLE
  - UNRESOLVED_CONFLICTING_EVIDENCE
  - UNRESOLVED_UNSUPPORTED_TIER

v0.1 documents these codes but does not enforce them beyond schema support.

8. ATTRIBUTED Discipline

ATTRIBUTED must be anchored.

Future enforcement should require:

  - source_identity
  - source_reference
  - source_timestamp_or_version

Without these, ATTRIBUTED risks collapsing into unsupported assertion.

v0.1 documents this rule but does not fully enforce attribution completeness.

9. First Enforceable Rules

v0.1 implements two narrow rules:

Rule 1:
  If required_provenance_tier is DOCUMENTED and declared_provenance_tier is
  GENERATED, fail.

Failure code:
  PROVENANCE_ESCALATION_DEFECT

Rule 2:
  If declared_provenance_tier is DOCUMENTED and dependency_provenance_tiers
  contains GENERATED, fail.

Failure code:
  PROVENANCE_DEPENDENCY_CONTAMINATION

10. Reserved Failure Codes

Implemented in v0.1:

  - PROVENANCE_ESCALATION_DEFECT
  - PROVENANCE_DEPENDENCY_CONTAMINATION

Reserved for future versions:

  - PROVENANCE_UNRESOLVED_REASON_MISSING
  - PROVENANCE_ATTRIBUTION_INCOMPLETE
  - PROVENANCE_SILENT_UPGRADE_DEFECT

11. Architectural Position

In the Fork boundary stack:

  - Claim Boundary: prevents evidence from claiming too much.
  - Definition Boundary: prevents systems from classifying too much.
  - Provenance Tier: prevents epistemic laundering.
  - Recomputability Class: will prevent unverifiable replay.
  - Semantic Inference Boundary: will prevent probabilistic interpretation from
    becoming authority.

Provenance Tier v0.1 establishes:

  Generated output is not documented evidence.

And its dual:

  Documented evidence must not depend on generated content.
