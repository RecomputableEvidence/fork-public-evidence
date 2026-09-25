# Evidence Lens Gallery v0.1

Status: Design/freeze stage — lens contract, entry schema, routing rules, and non-promotion boundary defined before any historical evidence is placed into the gallery.

Classification: Derived inspection surface; not a source artifact, not an experiment result, not a governance authority.

Repository base coordinate: `main@c2ae0ee435857c08cb074fc28e8302045572f50d`

## Canonical Definition

Evidence Lens Gallery (ELG): a standing-preserving inspection surface that projects preserved Fork evidence through explicitly defined lenses — such as failure manifestation, repair lineage, boundary discovery, environmental divergence, negative result, or unresolved standing — while retaining source identity, chronology, provenance, and original evidentiary standing.

## Governing Invariant

```text
THE LENS MAY CHANGE
WHAT IS EASY TO SEE.

THE LENS MUST NOT CHANGE
WHAT THE EVIDENCE ESTABLISHES.
```

## Core Distinctions

The Evidence Lens Gallery is a projection layer over preserved evidence. It does not move, reinterpret, duplicate, or strengthen any source artifact.

```text
EVIDENCE_LENS_GALLERY
= DERIVED_INSPECTION_SURFACE
OVER
PRESERVED_FORK_RECORDS

GALLERY_ENTRY
!= SOURCE_ARTIFACT

LENS_MEMBERSHIP
!= STANDING_PROMOTION

LENS_LABEL
!= GENERAL_FAILURE_CLASSIFICATION

DERIVED_VIEW
!= HISTORICAL_REWRITE
```

Fork already preserves immutable historical objects, failed attempts, corrections, successor paths, recomputation records, negative results, withholding states, and explicit standing boundaries. The Gallery does not need to move or reinterpret any of them. It gives those records a second, inspectable coordinate system.

## Why the Gallery Is Not a Bug Tracker, Postmortem, or Benchmark Failure Set

A bug tracker is oriented toward removing failures.
A postmortem is oriented toward explaining failures.
A benchmark failure set is oriented toward measuring performance.
The Evidence Lens Gallery is oriented toward preserving the evidentiary anatomy of failure.

The Gallery does not say, "these are the failure modes of AI systems." It says something much narrower:

"These are bounded failure manifestations that occurred in preserved Fork objects, under these conditions, with these detection paths and subsequent dispositions."

## Purpose

Many of Fork's most informative records are currently structurally awkward precisely because the experiment did not proceed cleanly: 0/17 recomputation before recovery, serialization differences, enum mismatches preventing execution, misleading PASS conditions, blinding leaks, source-binding discrepancies, environment-sensitive behavior, artifacts that survived while relations fractured, repairs that required successor objects, and so forth. Those are not embarrassing debris around the "real" results. In many cases they are where the boundary became observable.

The Gallery exposes those same events as an inspectable cross-cutting evidence surface without changing their standing.

The original disorder, failed attempt, misleading output, recovery, and changed understanding remain historically intact. The Gallery merely supplies a stable coordinate system through which an outsider can inspect them.

```text
ORGANIZATION_WITHOUT_SANITIZATION

PRESERVED_DISORDER
REMAINS_HISTORICALLY_INTACT

GALLERY_SUPPLIES
COORDINATE_SYSTEM
NOT
INTERPRETATION
```

## Lens Contract

### What a Lens Is

A lens is a representational projection rule that groups preserved evidence by an observable pattern. A lens changes how evidence is routed and inspected. It does not change what the evidence means or what standing it has.

### Declared Lenses

The following lenses are declared at v0.1 freeze. Additional lenses may be added only through a separately recorded protocol amendment that preserves this version.

1. **Failure Manifestation Lens** — projects events where something failed or behaved unexpectedly.
2. **Recomputation Lens** — projects events involving recomputation attempts, divergences, or confirmations.
3. **Boundary Discovery Lens** — projects events where a previously implicit distinction became operationally visible.
4. **Repair / Successor Lens** — projects events involving repair paths, successor objects, or recovery sequences.
5. **Environmental Divergence Lens** — projects events where behavior diverged across environments, platforms, or serialization conventions.
6. **Authority / Standing Lens** — projects events involving authority discontinuities, standing transitions, or standing-presence-versus-authority boundaries.
7. **Negative Result Lens** — projects events that produced no scorable result, a null result, or an intentional stop.
8. **Unresolved Standing Lens** — projects events whose standing remains unresolved, withheld, or pending.

### Many-to-Many Representation

A single preserved event may appear through multiple lenses. Lenses are representational projections of a gallery entry, not separate entries. Multiple lens memberships on one entry do not create multiple historical events.

```text
GALLERY_ENTRY_UNIT
= SOURCE_EVENT × OBSERVABLE_MANIFESTATION

ONE_ENTRY
MAY_HAVE
MULTIPLE_LENS_MEMBERSHIPS

NEW_LENS_MEMBERSHIP
!= NEW_GALLERY_ENTRY

MULTIPLE_ENTRIES_FOR_SAME_SOURCE_EVENT
= PERMITTED_ONLY_IF
DISTINCT_OBSERVABLE_MANIFESTATIONS_EXIST
```

This prevents one event from being accidentally counted several times merely because it is visible through several lenses. A source event that exhibits one observable manifestation is one gallery entry with multiple lens memberships. A source event that exhibits two distinct observable manifestations is two gallery entries, each with its own lens memberships.

For example, the Run 003 serialization episode is simultaneously a failed recomputation attempt, a misleading-success-signal case, a serialization-boundary case, a recovery lineage, and eventually a procedural-hardening event. These are multiple lens memberships on one entry (or a small number of entries for distinct manifestations), not duplicated entries for the same manifestation. Making one of those interpretations canonical would actually reduce the information.

### Lens Amendment Rule

A new lens requires:

- a recorded protocol amendment preserving this version;
- an explicit declaration that the new lens is representational only;
- an explicit non-claim that the new lens does not establish a taxonomic class;
- no retroactive population of historical evidence into the new lens before the amendment is itself preserved.

## Entry Schema

Every Gallery entry conforms to the following stable schema. The schema is frozen before any historical evidence is placed into the Gallery, so that the first population cannot influence the classification machinery used to construct the Gallery.

### Required Fields

| Field | Meaning |
|:--|:--|
| `gallery_entry_id` | Stable gallery identifier |
| `source_object_id` | Native preserved artifact or run identifier |
| `source_coordinate` | Immutable commit hash + path + Git blob + SHA-256 where available (see Source Binding Rule) |
| `source_artifact_paths` | Hash-bound source paths into preserved records |
| `observation_type` | Category of observable event (e.g., failure, divergence, boundary) |
| `observable_manifestation` | Exactly what failed or behaved unexpectedly |
| `detection_path` | Test, reviewer, recomputation, environment, exterior return, etc. |
| `preconditions` | Bounded conditions under which the manifestation appeared |
| `preserved_evidence` | Hash-bound source paths |
| `initial_standing` | WITHHOLD / FAILED / unresolved / repaired, etc. |
| `subsequent_disposition` | What happened after detection |
| `successor_or_repair_refs` | Separate object references where applicable |
| `standing_observed_at_commit` | Commit at which `current_standing` was observed |
| `standing_source_path` | Path to the source artifact from which standing was read |
| `standing_source_identity` | Git blob or SHA-256 of the source artifact at the standing observation commit |
| `current_standing` | Historical only; unresolved; reproduced; etc. (see Temporal Standing Binding) |
| `lens_memberships` | List of lens identifiers through which this entry is projected |
| `non_claims` | What the failure does not establish |

### Boundary-Made-Observable Field

Each entry may record a `boundary_made_observable` field. This field must not say "lesson learned." It records the distinction that became operationally visible.

Format:

```text
OBSERVED_EVENT:
  <exact description of what was observed>

BOUNDARY_MADE_OBSERVABLE:
  <the distinction that became visible>

STATEMENT_ORIGIN:
  SOURCE_EXPLICIT
  | EXTERIOR_RETURN_EXPLICIT
  | GALLERY_DERIVED

SUPPORT_REFS:
  <hash-bound source paths supporting the boundary statement>
```

`statement_origin` records whether the boundary was explicit in the source record, explicit in an exterior return, or derived later by the Gallery. This prevents a later abstraction from being laundered back into the historical object as though it were source-asserted.

```text
GALLERY_DERIVED_BOUNDARY
!= SOURCE_ASSERTED_BOUNDARY

GALLERY_DERIVED_BOUNDARY
!= EXTERIOR_RETURN_ASSERTED_BOUNDARY
```

Example:

```text
OBSERVED_EVENT:
  unconditional shell PASS while substantive recomputation failed

BOUNDARY_MADE_OBSERVABLE:
  process-success signal != evidentiary-success result

STATEMENT_ORIGIN:
  GALLERY_DERIVED

SUPPORT_REFS:
  research/fork-relational-resolution-demonstration-001/AG5_LOCAL_RECOMPUTATION_RECEIPT_ATTEMPT_002.json
```

Example:

```text
OBSERVED_EVENT:
  cryptographically continuous artifact after authority termination

BOUNDARY_MADE_OBSERVABLE:
  artifact persistence != authority persistence

STATEMENT_ORIGIN:
  GALLERY_DERIVED

SUPPORT_REFS:
  admissions/FORK-II-KERNEL-001/v0.1.1-CLOSED-HISTORICAL-EVIDENCE/README.md
```

Example:

```text
OBSERVED_EVENT:
  successful recovery only after specifying UTF-8/LF serialization

BOUNDARY_MADE_OBSERVABLE:
  logical content equivalence != recomputation equivalence without serialization binding

STATEMENT_ORIGIN:
  SOURCE_EXPLICIT

SUPPORT_REFS:
  research/fork-relational-resolution-demonstration-001/AG5_RECOMPUTATION_ADMISSION.md
```

### Schema Constraint

The `boundary_made_observable` field records an observed distinction, not a universal principle. It describes what became visible in this specific preserved trajectory. It does not claim that the distinction is a general systems law. The `statement_origin` field records whether the boundary was source-asserted, exterior-return-asserted, or gallery-derived, preventing later abstractions from being laundered back into the historical record.

```text
FAILURE
-> DIFFERENTIATION
-> EXPLICIT_BOUNDARY
-> PROCEDURAL_HARDENING

!=

FAILURE
-> UNIVERSAL_PRINCIPLE

GALLERY_DERIVED_BOUNDARY
!= SOURCE_ASSERTED_BOUNDARY

GALLERY_DERIVED_BOUNDARY
!= EXTERIOR_RETURN_ASSERTED_BOUNDARY
```

## Routing Rules

### Source Integrity Rule

The Gallery contains references into preserved records. It does not contain copies of source artifacts. A gallery entry points to its source through hash-bound paths and immutable commit coordinates.

Because the entry is bound to an immutable historical commit, the historical source binding itself does not become stale. What may become stale is any claim about its current route or current repository location.

```text
IMMUTABLE_SOURCE_BINDING
= REMAINS_VALID

CURRENT_ROUTE
= MAY_BECOME_STALE

HISTORICAL_PATH_NO_LONGER_CURRENT
!= HISTORICAL_SOURCE_BINDING_INVALID
```

If a source artifact has been moved, renamed, or deleted from its historical path in a later commit, the gallery entry records a routing staleness. That routing staleness is itself a preserved observation, not a silent correction. The immutable binding to the historical commit, path, Git blob, and SHA-256 remains valid regardless of current repository layout.

```text
SOURCE_STALENESS
!= ROUTING_STALENESS
```

If the Gallery later exposes current routes for inspection, entries may carry optional fields:

| Field | Meaning |
|:--|:--|
| `current_route_status` | CURRENT / MOVED / DELETED / UNRESOLVED |
| `current_route_observed_at_commit` | Commit at which the current route was last checked |
| `current_route_path` | Path at the current route observation commit, if resolvable |

These fields describe routing status only. They do not affect the immutable source binding.

### Source Binding Rule

Source binding requires an immutable coordinate. A mutable branch name alone is not a source coordinate.

```text
SOURCE_BINDING
= IMMUTABLE_COMMIT
+ PATH
+ GIT_BLOB
+ SHA256_WHERE_AVAILABLE

BRANCH_NAME
= OPTIONAL_DESCRIPTIVE_CONTEXT

BRANCH_NAME_ALONE
!= SOURCE_COORDINATE
```

This is particularly appropriate given the mutable-ref failures Fork has already preserved. The Gallery's integrity model depends on hash-bound preserved records, not on mutable branch pointers that may move between the time a gallery entry is created and the time it is inspected.

### Non-Duplication Rule

A gallery entry references exactly one source event and one observable manifestation. One entry may carry multiple lens memberships. Multiple entries for the same source event are permitted only when distinct observable manifestations exist.

```text
ONE_ENTRY
= ONE_SOURCE_EVENT
× ONE_OBSERVABLE_MANIFESTATION

MULTIPLE_LENS_MEMBERSHIPS_ON_ONE_ENTRY
!= MULTIPLE_ENTRIES

MULTIPLE_ENTRIES_FOR_SAME_SOURCE_EVENT
REQUIRE
DISTINCT_OBSERVABLE_MANIFESTATIONS
```

This prevents one event from being accidentally counted several times merely because it is visible through several lenses.

### Chronology Preservation Rule

Gallery entries do not impose a chronology on source artifacts. The source chronology remains the authoritative temporal sequence. Gallery ordering is a display convenience only.

### Standing Preservation Rule

```text
LENS_MEMBERSHIP
!= STANDING_PROMOTION

A failure does not become canonical
merely because it appears in the gallery.

A repair does not become correct
merely because it follows a gallery entry.

A pattern occurring three times
does not become a general law.

The gallery describes preserved observations
and their relations.
```

### Temporal Standing Binding

The source event is immutable, but its current representational standing may later change. A gallery entry must therefore preserve the coordinate at which standing was observed, the path from which it was read, and the identity of the source artifact at that commit.

```text
CURRENT_STANDING
+ STANDING_OBSERVED_AT_COMMIT
+ STANDING_SOURCE_PATH
+ STANDING_SOURCE_IDENTITY

= TEMPORALLY_BOUND_STANDING_OBSERVATION
```

Without these fields, a gallery entry could remain structurally valid while silently becoming stale with respect to standing. The source event does not change, but a later admission, correction, successor, or closure may change how the event's standing is represented. The temporal binding preserves the distinction between the immutable source event and its current representational standing.

```text
IMMUTABLE_SOURCE_EVENT
!= IMMUTABLE_STANDING

STANDING_AT_FREEZE
!= STANDING_AT_INSPECTION

SILENT_STANDING_DRIFT
!= PRESERVED_STANDING_OBSERVATION
```

If the standing source artifact has changed identity since the standing observation commit, the gallery entry records a standing-source drift. That drift is itself a preserved observation, not a silent correction. This extends the same staleness discipline already declared for source integrity to the standing dimension.

## Non-Promotion Boundary

### Gallery Membership Does Not Promote Standing

Inclusion in the Gallery does not:

- validate, freeze, qualify, authorize, or strengthen an underlying artifact;
- establish a taxonomic class;
- establish that a scientifically valid failure class exists;
- establish that a recurrence is explained;
- establish a general system property;
- create derivation, equivalence, endorsement, or standing inheritance;
- convert a preserved observation into a proven principle;
- or authorize downstream reliance.

### Separation of Observation From Aggregation

```text
COMMON_LENS_MEMBERSHIP
!= ESTABLISHED_TAXONOMIC_CLASS

RECURRENCE_VISIBLE
!= RECURRENCE_EXPLAINED

MULTIPLE_INSTANCES
!= GENERAL_SYSTEM_PROPERTY
```

If six entries eventually exhibit something informally recognized as serialization-related failure, the Gallery may route all six under a common inspection lens, but that does not establish that a scientifically valid failure class exists.

### Research Object Boundary

Later experiments that study recurrence, prevalence, causal patterns, or whether certain hardenings suppress particular manifestations must become separately opened research objects using Gallery records as their bounded corpus. The Gallery itself remains descriptive. It does not become an inferential surface.

An experiment using only Gallery entries studies the derived representation. An experiment making claims about the underlying failures should bind both the selected Gallery population and the native source artifacts behind it. The Gallery corpus is not the source corpus.

```text
GALLERY_CORPUS
!= UNDERLYING_SOURCE_CORPUS

GALLERY_AS_FROZEN_EVIDENCE_POPULATION
!= GALLERY_AS_INFERENTIAL_SURFACE

DESCRIPTIVE_ROUTING
!= CAUSAL_ANALYSIS

DERIVED_REPRESENTATION_STUDY
!= SOURCE_ARTIFACT_STUDY
```

## Longitudinal Surface

After enough entries accumulate, the Gallery itself becomes a longitudinal research surface. Questions may eventually be asked:

- which classes recur;
- which disappear after procedural hardening;
- which only appear under cross-environment pressure;
- which are detectable only externally;
- which failures repeatedly generate new boundaries.

Without changing one historical result.

```text
LONGITUDINAL_OBSERVATION
!= LONGITUDINAL_CONCLUSION

ACCUMULATED_ENTRIES
!= ESTABLISHED_TAXONOMY
```

## Failure Lineage Exposure

The Gallery can expose multi-step trajectories as one failure lineage while leaving every individual object independent.

A conventional system often leaves:

```text
BEFORE
-> FIXED_VERSION
```

Fork can sometimes preserve:

```text
BEFORE
-> FAILED_ATTEMPT
-> MISLEADING_SIGNAL
-> DIAGNOSIS
-> CORRECTION
-> RECOMPUTATION
-> EXTERIOR_PRESSURE
-> FINAL_BOUNDED_STANDING
```

The Gallery makes that path readable as a single lineage without rewriting any intermediate object.

## Required Non-Claims

The Evidence Lens Gallery does not claim:

- approval;
- authorization;
- certification;
- compliance;
- completeness of the failure population;
- correctness of any repair;
- endorsement;
- establishment of a failure taxonomy;
- establishment of a general systems property;
- legal sufficiency;
- production readiness;
- provenance recognition;
- risk acceptance;
- runtime control;
- safety;
- scientific validity of any observed pattern;
- semantic authority over source artifacts;
- truth;
- universality of any boundary made observable.

## Naming Boundary

This object is deliberately named non-evaluatively. "Gallery," "lens," or "surface" preserves the observational posture. "Taxonomy" would imply that Fork has established the underlying classes. "Atlas" would imply comprehensive coverage. The Gallery is neither comprehensive nor taxonomic.

## Instantiation

This document defines the design/freeze stage of `FORK-EVIDENCE-LENS-GALLERY-001`. No historical evidence has been placed into the Gallery at this stage. The lens contract, entry schema, routing rules, and non-promotion boundary are frozen before any population begins, so that the first Gallery population cannot influence the classification machinery used to construct the Gallery.

```text
DESIGN_FROZEN
POPULATION_NOT_BEGUN

LENS_CONTRACT
= FROZEN

ENTRY_SCHEMA
= FROZEN

ROUTING_RULES
= FROZEN

NON_PROMOTION_BOUNDARY
= FROZEN

HISTORICAL_EVIDENCE_PLACED_INTO_GALLERY
= ZERO_ENTRIES_AT_FREEZE
```

Population of the Gallery with preserved historical evidence requires a separately recorded successor step that:

1. preserves this design/freeze document unchanged;
2. selects source artifacts by their existing preserved immutable commit coordinates only;
3. creates gallery entries that reference, not copy, source artifacts;
4. binds each entry's source coordinate to an immutable commit hash, path, Git blob, and SHA-256 where available;
5. declares lens memberships per entry;
6. records `boundary_made_observable` with `statement_origin` and `support_refs` where applicable;
7. binds `current_standing` to `standing_observed_at_commit`, `standing_source_path`, and `standing_source_identity`;
8. does not promote standing for any referenced artifact;
9. preserves every non-claim declared in this document.

## Canonical Boundary Sentences

```text
EVIDENCE_LENS_GALLERY
= DERIVED_INSPECTION_SURFACE

GALLERY_ENTRY
!= SOURCE_ARTIFACT

GALLERY_ENTRY_UNIT
= SOURCE_EVENT × OBSERVABLE_MANIFESTATION

NEW_LENS_MEMBERSHIP
!= NEW_GALLERY_ENTRY

LENS_MEMBERSHIP
!= STANDING_PROMOTION

LENS_LABEL
!= TAXONOMIC_CLASS

DERIVED_VIEW
!= HISTORICAL_REWRITE

SOURCE_BINDING
= IMMUTABLE_COMMIT + PATH + GIT_BLOB + SHA256_WHERE_AVAILABLE

BRANCH_NAME_ALONE
!= SOURCE_COORDINATE

IMMUTABLE_SOURCE_BINDING
= REMAINS_VALID

HISTORICAL_PATH_NO_LONGER_CURRENT
!= HISTORICAL_SOURCE_BINDING_INVALID

SOURCE_STALENESS
!= ROUTING_STALENESS

IMMUTABLE_SOURCE_EVENT
!= IMMUTABLE_STANDING

STANDING_AT_FREEZE
!= STANDING_AT_INSPECTION

GALLERY_DERIVED_BOUNDARY
!= SOURCE_ASSERTED_BOUNDARY

RECURRENCE_VISIBLE
!= RECURRENCE_EXPLAINED

COMMON_LENS_MEMBERSHIP
!= ESTABLISHED_FAILURE_CLASS

MULTIPLE_INSTANCES
!= GENERAL_SYSTEM_PROPERTY

BOUNDARY_MADE_OBSERVABLE
!= UNIVERSAL_PRINCIPLE

ORGANIZATION
!= SANITIZATION

GALLERY_CORPUS
!= UNDERLYING_SOURCE_CORPUS

GALLERY_AS_POPULATION
!= GALLERY_AS_INFERENTIAL_SURFACE

DERIVED_REPRESENTATION_STUDY
!= SOURCE_ARTIFACT_STUDY

DESIGN_FROZEN
!= POPULATION_BEGUN
```
