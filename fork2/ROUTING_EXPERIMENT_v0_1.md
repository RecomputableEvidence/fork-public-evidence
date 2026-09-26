# Fork 2 temporal routing experiment v0.1

## Experimental question

Can a five-phase temporal route handle materially different evidentiary objects and findings without either losing important state or creating a large fixed taxonomy?

This is a prototype, not an admitted architecture freeze.

## Proposed temporal spine

```text
INBOUND
  ↓
EXAMINE
  ↓
DETERMINE
  ↓
[RESOLVE → DETERMINE]*
  ↓
OUTBOUND
```

The route asks only what may happen next. It does not try to encode everything known about the subject into the route name.

## Dispositions

The prototype uses a deliberately small disposition set:

- `UNDETERMINED`
- `OUTBOUND_ELIGIBLE`
- `REMEDIATION_REQUIRED`
- `UNRESOLVED`
- `ARCHIVE_ONLY`
- `DISCARD_ONLY`

`OUTBOUND_ELIGIBLE` replaces the earlier experimental label `CLEAR` because it states only an operational routing permission and does not imply truth, approval, correctness, adequacy, or authority.

`REMEDIATION_REQUIRED` and `UNRESOLVED` route to `RESOLVE`.

`OUTBOUND_ELIGIBLE`, `ARCHIVE_ONLY`, and `DISCARD_ONLY` route to `OUTBOUND`.

## Findings and operations remain open

Examples such as `FILE_TRUNCATED`, `OBSERVATION_TRUNCATED`, `INVALID_FORMAT`, `SOURCE_INCOMPLETE`, `RECOMPUTE`, `REPAIR`, `RECOVER`, or `REVISE` are not frozen as a global vocabulary here.

They remain open strings attached to snapshots or transitions. The experiment is specifically testing whether a small temporal route can remain useful while findings and remediation operations stay extensible.

```text
ROUTE != FINDING
ROUTE != OBJECT TYPE
ROUTE != AUTHORITY STATE
ROUTE != EPISTEMIC STANDING
```

## Transition model

Each routing state is immutable. Advancing the same subject creates a new routing-state identifier and an explicit predecessor binding.

Each transition records:

- transition ID
- subject ID
- source state ID
- successor state ID
- source phase
- successor phase
- explicit basis
- optional open-ended operations

This prototype does not claim that a new routing state necessarily means new artifact bytes. It records a new temporal routing coordinate only.

## Resolution invariant

```text
REMEDIATION DOES NOT PROMOTE

REMEDIATION PRODUCES
A NEW BASIS FOR DETERMINATION
```

A subject entering `RESOLVE` must return to `DETERMINE` before it can become outbound.

Therefore:

```text
RECOMPUTED != RESOLVED
REVISED != ACCEPTABLE
REPAIRED != AUTHORIZED
SEALED != TRUE
OUTBOUND != APPROVED
OUTBOUND_ELIGIBLE != TRUE
```

## Current transition conditions

```text
INBOUND + UNDETERMINED
→ EXAMINE

EXAMINE + UNDETERMINED
→ DETERMINE + explicit disposition

DETERMINE + {REMEDIATION_REQUIRED, UNRESOLVED}
→ RESOLVE

RESOLVE
→ DETERMINE + explicit disposition

DETERMINE + {OUTBOUND_ELIGIBLE, ARCHIVE_ONLY, DISCARD_ONLY}
→ OUTBOUND

OUTBOUND
→ terminal in this prototype
```

Direct skips such as `INBOUND → OUTBOUND` are rejected.

## Relationship to PR #189

This branch is stacked on PR #189's current Fork 2 kernel head. It does not alter the relation standing established there.

The routing experiment does not implement or promote R1, R2, R4, R6, or R8. It does not expand the four frozen relations R3, R5, R7a, or R7b.

It also preserves the first-class PR #189 boundary:

```text
TECHNICAL CANDIDATE = CLEAN

AUTHORITY ORIGIN
= DECLARED
= BOUNDED
= NOT EXTERNALLY AUTHENTICATED

FULL PREDECESSOR RECOMPUTATION
= NOT AVAILABLE FROM PR #189 ALONE
```

## What would count as useful evidence

The model earns further consideration if real Fork objects can pass through these five phases while:

1. preserving findings without turning them into route types;
2. preserving predecessor/successor temporal bindings;
3. forcing remediation back through determination;
4. rejecting route-skipping and subject substitution;
5. avoiding standing or authority promotion by routing alone.

If realistic objects require a proliferating number of phases or dispositions, that is a negative result about this abstraction and should be preserved rather than hidden.
