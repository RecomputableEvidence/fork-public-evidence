# Fork 2 temporal routing pressure v0.1

## Purpose

Pressure the five-phase routing prototype with Fork-shaped cases before adding more vocabulary or architecture.

This pressure does not promote relation standing, freeze the routing topology, or establish a universal evidentiary ontology.

## Cases exercised

1. PR #189 technical candidate with explicit authority-authentication and predecessor-recomputation limits.
2. Truncated/source-incomplete artifact requiring remediation.
3. Failed recomputation that remains unresolved after another attempt.
4. Exterior return preserved while source origin remains unbound.
5. Materially revised artifact represented as a distinct successor subject.
6. Adverse findings paired with an externally supplied outbound disposition.
7. Completed repair attempting to skip redetermination.
8. Historical failed attempt routed archive-only.
9. Invalid ingress routed discard-only while preserving the receipt event.

## Supported within this pressure surface

The current five-phase route can represent:

```text
INBOUND
→ EXAMINE
→ DETERMINE
→ [RESOLVE → DETERMINE]*
→ OUTBOUND
```

without creating new route types for truncation, source incompleteness, recomputation failure, authority boundaries, archival handling, or invalid-format findings.

It also preserves the executable invariant:

```text
REMEDIATION DOES NOT PROMOTE

RESOLVE
!=
OUTBOUND

RESOLVE
→ DETERMINE
```

`OUTBOUND_ELIGIBLE` replaces the earlier experimental `CLEAR` label because the new term expresses routing permission without implying truth, approval, correctness, sufficiency, or authority.

## Pressure findings / open seams

### P-001 — unresolved outbound is not representable

Current v0.1 semantics force every `UNRESOLVED` determination into `RESOLVE`.

A realistic exterior return may need to leave the router while remaining explicitly unresolved, for example:

```text
EXTERIOR_RETURN_PRESERVED
SOURCE_ORIGIN_NOT_BOUND
DISPOSITION = UNRESOLVED
```

The current machine rejects `DETERMINE(UNRESOLVED) → OUTBOUND(UNRESOLVED)`.

This is preserved as an open design seam. No repair is made in this pressure record.

### P-002 — materially revised successor identity is outside the current route model

The router correctly rejects silent `subject_id` substitution.

However, if remediation creates materially different artifact bytes and the repaired artifact must be represented as a distinct subject:

```text
A' != A
A' SUCCESSOR_OF A
```

v0.1 has no explicit cross-subject successor relation. The current transition validator rejects the identity change rather than representing the relation.

This is preserved as an open design seam. No repair is made in this pressure record.

### P-003 — routing does not determine disposition from findings

The router validates phase progression; it does not implement the decision rule that maps findings to a disposition.

Therefore an externally supplied snapshot can currently contain:

```text
FINDINGS
= SOURCE_INCOMPLETE
= AUTHORITY_NOT_ESTABLISHED

DISPOSITION
= OUTBOUND_ELIGIBLE
```

and the routing layer will permit `OUTBOUND`.

This is not treated as a hidden defect: it establishes that the current module is a temporal transition validator, not yet a determination engine.

### P-004 — transition basis is required but not independently verified

Every transition requires a non-empty `basis`, but v0.1 treats that basis as an asserted string. It does not content-address, authenticate, recompute, or evaluate the referenced basis.

This is an explicit limit of the current experiment.

### P-005 — append-only history is structurally implied, not repository-enforced by the router

Snapshots are immutable and successors bind predecessor state IDs, but `routing.py` does not itself provide persistent append-only storage or prove that the complete chain has been retained.

The router validates supplied adjacent states. History completeness remains outside this module.

## Current disposition of the experiment

```text
FIVE_PHASE_ROUTE
= STILL PLAUSIBLE

TAXONOMY_EXPLOSION
= NOT OBSERVED IN THIS PRESSURE SET

UNRESOLVED_OUTBOUND
= OPEN

CROSS_SUBJECT_SUCCESSOR_RELATION
= OPEN

FINDING_TO_DISPOSITION_DETERMINATION
= OUTSIDE CURRENT ROUTER

BASIS VERIFICATION
= OUTSIDE CURRENT ROUTER

APPEND_ONLY STORAGE COMPLETENESS
= OUTSIDE CURRENT ROUTER
```

## Non-claims

```text
PRESSURE_PASS != ARCHITECTURE_FREEZE
ROUTING_VALIDITY != DISPOSITION_CORRECTNESS
NONEMPTY_BASIS != VERIFIED_BASIS
PREDECESSOR_BINDING != COMPLETE_HISTORY_PROOF
SUBJECT_ID_STABILITY != UNIVERSAL IDENTITY ONTOLOGY
OUTBOUND_ELIGIBLE != APPROVED
```

## Next question

Do P-001 and P-002 require changes to the five-phase route itself, or can they be resolved by adding a small relation/event layer around the existing route while leaving the five temporal phases unchanged?
