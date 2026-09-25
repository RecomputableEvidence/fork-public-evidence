# FORK-EVIDENCE-LENS-GALLERY-001 — Population 002 Predeclaration

Status: `PREDECLARATION__SELECTION_RULE_AND_PROCEDURE_FROZEN_BEFORE_EVENT_SELECTION`

Predecessor design freeze: `FORK-EVIDENCE-LENS-GALLERY-001 v0.1` (merge `5ee76df67f25ff6be03f025cf6795088b9c4aef2`)

Predecessor calibration population: `FORK-EVIDENCE-LENS-GALLERY-001-POPULATION-001` (merge `56b4e064fa061417a82b7017f56d0dd98f225aa5`)

Repository base coordinate: `main@56b4e064fa061417a82b7017f56d0dd98f225aa5`

## Purpose

Population 001 asked:

> Can one cleanly bound source event be represented correctly through the frozen Gallery machinery?

Population 002 asks:

> Does that machinery remain coherent when the evidence comes from different objects, different failure trajectories, and different standing states?

Population 002 is therefore a heterogeneity test, not a scale test.

```text
POPULATION_002_PURPOSE
= TEST_CROSS_OBJECT_ROUTING

HETEROGENEITY
!= SCALE

CROSS_OBJECT_COHERENCE
!= COMPLETENESS
```

## Lens Shift

Population 001 established the calibration Lens Shift:

```text
FIRST_POPULATION
!= SHOWCASE

FIRST_POPULATION
= CALIBRATION_OF_POPULATION_MECHANICS
```

Population 002 extends that discipline with a second shift:

```text
SECOND_POPULATION
!= HISTORICAL_SWEEP

SECOND_POPULATION
= HETEROGENEITY_PRESSURE_TEST
```

The second population is deliberately not an attempt to route all of Fork's preserved failures, rank them by importance, or establish a comprehensive failure taxonomy. It tests whether the frozen machinery remains coherent under cross-object, cross-trajectory, cross-standing conditions.

## Predeclared Selection Rule

The selection rule and selection procedure are frozen before any events are selected. No event is selected or evaluated against the Population 002 selection procedure before this predeclaration is preserved.

Fork already knows its own history. The predeclaration freeze does not require or claim ignorance of preserved events. It requires that the selection procedure be frozen before any event is evaluated against it.

```text
PREDECLARATION_FREEZE
PRECEDES
POPULATION_002_SELECTION

PREDECLARATION_FREEZE
!= FIRST_AWARENESS_OF_ALL_POSSIBLE_EVENTS

KNOWN_EVENT
!= SELECTED_EVENT

GENERAL_ELIGIBILITY
!= POPULATION_002_ELIGIBILITY_DETERMINATION
```

### Selection Criteria

Population 002 entries must be drawn from source events satisfying all of the following:

1. **Multiple source objects.** At least two distinct source objects must be represented. A source object is a distinct Fork research object, experiment, admission, exterior return, or preserved procedural record — not a second manifestation of the same source event already represented in Population 001.

2. **Multiple failure manifestations.** At least two distinct observable manifestations must be present across the selected entries. These manifestations must be genuinely distinct under the frozen cardinality rule, not merely the same manifestation described differently.

3. **At least one unresolved or unrepaired path.** At least one selected entry must reference a source event whose standing is unresolved, withheld, pending, or whose repair path was not completed. This tests whether the Gallery can represent an incomplete trajectory without implying resolution.

```text
SELECTION_CRITERIA
!= SELECTION_PROCEDURE

SELECTION_RULE
= PREDECLARED

EVENT_SELECTION
!= EDITORIAL_IMPORTANCE_RANKING

TARGET
= MULTIPLE_SOURCE_OBJECTS
+ MULTIPLE_FAILURE_MANIFESTATIONS
+ AT_LEAST_ONE_UNRESOLVED_OR_UNREPAIRED_PATH
```

### Selection Non-Criteria

The following must not influence event selection:

- perceived severity or impressiveness of the failure;
- rhetorical or persuasive value;
- recency;
- alignment with any informal pattern recognized during Population 001;
- desire to produce a balanced or representative sample;
- desire to demonstrate that the Gallery "works" or "is useful."

```text
SEVERITY
!= SELECTION_CRITERION

PERSUASIVE_VALUE
!= SELECTION_CRITERION

RECENCY
!= SELECTION_CRITERION

PATTERN_ALIGNMENT_WITH_POPULATION_001
!= SELECTION_CRITERION

REPRESENTATIVE_BALANCE
!= SELECTION_CRITERION

DEMONSTRATED_UTILITY
!= SELECTION_CRITERION
```

## What Population 002 Tests

Population 001 exercised the frozen ELG machinery against a single source event with clean immutable bindings and two clearly separable manifestations. That validated the mechanics: source binding, entry cardinality, multi-lens membership, temporal standing binding, derived-boundary attribution, and non-promotion.

Population 002 applies pressure to different dimensions:

### Cross-Object Source Binding

Population 001 bound to one source object with one set of artifacts. Population 002 requires binding to at least two distinct source objects, each with its own immutable commit coordinate, Git blobs, and SHA-256 identities. This tests whether the source binding rule remains coherent when the artifacts come from different repository paths, different experiments, or different admission coordinates.

### Cross-Trajectory Coherence

Population 001 represented two manifestations from one trajectory (a single exterior return). Population 002 requires manifestations from different trajectories. This tests whether multiple lens memberships across entries from different objects remain non-contradictory.

Any concrete examples of manifestation types are illustrative only and must not be treated as selection cues:

```text
ILLUSTRATIVE_EXAMPLE
!= SELECTION_HINT

EXAMPLE_MATCH
!= ELIGIBILITY_PRIORITY
```

### Standing Heterogeneity

Population 001 bound standing at one observation commit for both entries. Population 002 requires at least one entry whose source event has an unresolved, withheld, pending, or incomplete standing trajectory. This tests whether the temporal standing binding rule can represent a standing observation that is itself provisional without implying resolution.

```text
UNRESOLVED_STANDING_REPRESENTED
!= UNRESOLVED_STANDING_RESOLVED

PROVISIONAL_STANDING_OBSERVATION
!= PROVISIONAL_STANDING_PROMOTION

INCOMPLETE_TRAJECTORY_REPRESENTED
!= INCOMPLETE_TRAJECTORY_COMPLETED
```

## Recursive Eligibility Boundary

The construction of Population 001 itself produced a preserved procedural failure: the `__dummy__` branch write (commit `b9ad3c54517cda7047b9d2533d904820865b2350`), two unreferenced commit objects, and subsequent additive correction. That procedural failure is eligible for future Gallery routing.

However:

```text
GALLERY_PROCESS_FAILURE
MAY_BECOME
FUTURE_SOURCE_EVENT

BUT

FAILURE_OCCURRED
!= GALLERY_ENTRY_CREATED

GALLERY_ELIGIBILITY
!= GALLERY_ADMISSION

ELG_INSPECTING_ELG_CONSTRUCTION
!= ELG_SELF_AUTHORIZATION
```

A failure in the Gallery's own construction does not become a Gallery entry by virtue of having occurred. It must pass through the same predeclared selection rule, source binding, entry cardinality, temporal standing binding, and non-promotion boundary as any other source event. If it is selected for a future population, its gallery-derived boundary must be explicitly marked `GALLERY_DERIVED` and must not be attributed backward to the Gallery itself.

This means ELG can eventually inspect failures arising in its own construction without becoming self-authorizing. The Gallery does not grant itself standing to interpret its own procedural errors.

## Population 002 Non-Claims

```text
POPULATION_002
!= COMPLETE_FAILURE_POPULATION

POPULATION_002
!= REPRESENTATIVE_SAMPLE

POPULATION_002
!= HISTORICAL_SWEEP

POPULATION_002
!= FAILURE_TAXONOMY

HETEROGENEITY_TEST
!= COMPLETENESS_TEST

CROSS_OBJECT_COHERENCE
!= CROSS_OBJECT_COMPLETENESS

UNRESOLVED_PATH_REPRESENTED
!= UNRESOLVED_PATH_RESOLVED

ENTRY_COUNT
!= FAILURE_FREQUENCY

COMMON_LENS_MEMBERSHIP
!= ESTABLISHED_TAXONOMIC_CLASS

GALLERY_DERIVED_BOUNDARY
!= SOURCE_ASSERTED_BOUNDARY

POPULATION_ADMISSION
!= SOURCE_STANDING_CHANGE

PREDECLARATION
!= POPULATION
```

## Selection Procedure

Selection criteria define what a valid Population 002 must contain. Selection procedure determines which qualifying events are chosen when many combinations satisfy those criteria. Without a frozen procedure, Population 002 could obey every declared criterion and still be shaped by severity, convenience, rhetorical value, or unconscious pattern preference.

```text
SELECTION_CRITERIA
!= SELECTION_PROCEDURE

QUALIFYING_EVENT_SET
!= SELECTED_EVENT_SET
```

### Predeclared Selection Procedure

#### Step 1 — Candidate Universe Definition

The candidate universe is every distinct source-event × observable-manifestation pair having an explicit preserved event or object identifier in the tree or ancestry of `main@56b4e064fa061417a82b7017f56d0dd98f225aa5` and satisfying the frozen ELG source-binding fields (immutable commit + path + Git blob + SHA-256 where available).

```text
CANDIDATE_SELECTION_UNIT
= SOURCE_EVENT × OBSERVABLE_MANIFESTATION
```

The exact repository surfaces from which event identifiers are enumerated:

- `docs/exterior-returns/` — each exterior return directory is a candidate source event; each distinct correction, finding, or observed manifestation within that return is a distinct candidate manifestation
- `admissions/` — each admission directory containing a preserved object or event identifier is a candidate source event; each distinct preserved finding, discrepancy, or uncovered surface within that admission is a distinct candidate manifestation
- `research/` — each research object directory containing preserved stage records (AG0–AG8, CAPTURE_001, CAPTURE_002) is a candidate source event; each distinct preserved stage, attempt, or dimensional evaluation within that object is a distinct candidate manifestation
- `docs/observations/` — each observation directory containing a preserved event identifier is a candidate source event; each distinct preserved observation within that directory is a distinct candidate manifestation
- `docs/experiments/` — each experiment directory containing preserved run records or procedural records is a candidate source event; each distinct run, attempt, or procedural record within that experiment is a distinct candidate manifestation
- `docs/current-standing/` — current-standing register entries are not candidate events; they are routing surfaces

The operator cannot decide ad hoc what "looks like an event" or what "looks like a manifestation." A candidate exists if and only if:

- the source event has an explicit preserved event or object identifier in one of the enumerated surfaces above;
- the manifestation has a unique addressable preserved record within the canonical source artifact;
- and the frozen source-binding requirements are satisfied.

The source event requires an explicit preserved identifier. The manifestation requires a unique preserved record boundary, not an explicit manifestation identifier. An explicit manifestation identifier is optional; if absent, a generated ELG candidate identifier is permitted under the Manifestation ID Assignment Rule below.

```text
SOURCE_EVENT
= MUST_HAVE_EXPLICIT_PRESERVED_EVENT_OR_OBJECT_IDENTIFIER

OBSERVABLE_MANIFESTATION
= MUST_HAVE_UNIQUE_PRESERVED_RECORD_BOUNDARY
  WITHIN_CANONICAL_SOURCE_ARTIFACT

EXPLICIT_MANIFESTATION_ID
= OPTIONAL

IF_EXPLICIT_MANIFESTATION_ID_ABSENT
= GENERATED_ELG_CANDIDATE_ID_PERMITTED

IF_NO_UNIQUE_PRESERVED_RECORD_BOUNDARY
= CANDIDATE_ENUMERATION_FAILURE
  NOT_CANDIDATE_INELIGIBILITY

CANDIDATE_EXISTS
IFF
  SOURCE_EVENT_HAS_EXPLICIT_PRESERVED_IDENTIFIER
  AND
  MANIFESTATION_HAS_UNIQUE_ADDRESSABLE_PRESERVED_RECORD
  IN_CANONICAL_SOURCE_ARTIFACT
  AND
  FROZEN_SOURCE_BINDING_REQUIREMENTS_ARE_SATISFIED
```

```text
CANDIDATE_UNIVERSE
= EVERY_DISTINCT_SOURCE_EVENT × OBSERVABLE_MANIFESTATION
  WHERE_SOURCE_EVENT_HAS_EXPLICIT_PRESERVED_IDENTIFIER
  AND_MANIFESTATION_HAS_UNIQUE_ADDRESSABLE_PRESERVED_RECORD
  IN_THE_TREE_OR_ANCESTRY_OF
  main@56b4e064fa061417a82b7017f56d0dd98f225aa5
  AND_SATISFYING_THE_FROZEN_SOURCE_BINDING_FIELDS

CANDIDATE_ENUMERATION_FAILURE
!= CANDIDATE_INELIGIBILITY

CURRENT_STANDING_REGISTER
!= CANDIDATE_EVENT_SURFACE
```

##### Canonical Source Binding Rule

A candidate (source-event × manifestation pair) may have multiple preserved artifacts or may appear at multiple later coordinates. The canonical binding is determined by the source record itself, not by the operator.

```text
CANONICAL_SOURCE_BINDING
= THE IMMUTABLE_COMMIT + PATH + GIT_BLOB + SHA256
  EXPLICITLY_DECLARED_BY_THE_PRESERVED_RECORD
  FOR_THAT_MANIFESTATION

IF_MULTIPLE_BINDINGS_EXIST
= USE_THE_BINDING_EXPLICITLY_IDENTIFIED
  AS_PRIMARY_OR_CANONICAL_BY_THE_SOURCE_RECORD

IF_NO_UNIQUE_CANONICAL_BINDING_EXISTS
= CANDIDATE_ENUMERATION_FAILURE
  NOT_CANDIDATE_INELIGIBILITY
```

If a preserved record declares a primary or canonical binding for a manifestation, that binding is used. If the record declares multiple bindings without identifying one as primary, that is an enumeration failure — the candidate is not excluded as ineligible, but it cannot be ordered until the source record is separately reconciled.

##### Manifestation ID Assignment Rule

Each candidate requires a manifestation identifier for ordering. The assignment procedure is frozen before any candidate is enumerated.

```text
MANIFESTATION_ID
= EXPLICIT_SOURCE_MANIFESTATION_ID
  WHERE_ONE_EXISTS

IF_NONE_EXISTS
= ASSIGN ELG-CANDIDATE-MANIFESTATION-ID
  BY_FROZEN_DETERMINISTIC_RULE

GENERATED_MANIFESTATION_ID
!= SOURCE_ASSERTED_IDENTIFIER
```

The frozen deterministic rule for generated IDs:

```text
GENERATED_MANIFESTATION_ID
= "ELG-CANDIDATE-"
  + CANONICAL_SOURCE_PATH
  + ":"
  + SOURCE_LOCAL_RECORD_OFFSET
```

Where `SOURCE_LOCAL_RECORD_OFFSET` is the zero-based byte offset of the first byte of the unique addressable manifestation record within the canonical Git blob bytes, or the explicit finding/correction identifier declared by the source record if one exists. If neither a byte offset nor an explicit finding identifier is available, the candidate is an enumeration failure.

```text
SOURCE_LOCAL_RECORD_OFFSET
= ZERO_BASED_BYTE_OFFSET
  OF_FIRST_BYTE
  OF_THE_UNIQUE_ADDRESSABLE_MANIFESTATION_RECORD
  IN_CANONICAL_GIT_BLOB_BYTES

BYTE_OFFSET
!= LINE_NUMBER

BYTE_OFFSET
!= CHARACTER_OFFSET

BYTE_OFFSET
!= DISPLAY_POSITION
```

The byte offset is measured against the raw bytes of the canonical Git blob, not against any rendered, decoded, or display representation. This ensures that the same repository, the same predeclaration, the same candidate decomposition, the same binding per candidate, the same order, and the same selected set are produced by any compliant operator.

```text
SAME_REPOSITORY
+ SAME_PREDECLARATION
→ SAME_CANDIDATE_DECOMPOSITION
→ SAME_BINDING_PER_CANDIDATE
→ SAME_ORDER
→ SAME_SELECTED_SET
```

1. **Enumerate candidates.** Enumerate all source-event × observable-manifestation pairs in the candidate universe reachable from `main@56b4e064fa061417a82b7017f56d0dd98f225aa5`. Each candidate is recorded with its source-object identifier, manifestation identifier (explicit or generated), canonical source binding (commit + path + Git blob + SHA-256), and standing state.

#### Step 2 — Pre-Evaluation Recording

2. **Record each candidate before evaluating fit.** Every enumerated candidate is recorded before any candidate is evaluated against the Population 002 selection criteria. The candidate enumeration is preserved as part of the population package.

#### Step 3 — Constrained Evaluation

3. **Evaluate each candidate only against:**
   - source-object identity (distinct from Population 001 source event and from other selected candidates);
   - observable-manifestation distinctness (genuinely distinct under the frozen cardinality rule);
   - standing state (resolved, unresolved, withheld, pending, or incomplete);
   - source-binding completeness (immutable commit, path, Git blob, and SHA-256 all available).

#### Step 4 — Population 001 Reuse Edge

4. **Population 001 source event is enumerated for audit and is ineligible for Population 002 selection.**

   ```text
   POPULATION_001_SOURCE_EVENT
   = ENUMERATED_FOR_AUDIT
   = INELIGIBLE_FOR_POPULATION_002_SELECTION

   IF_NO_QUALIFYING_SET_EXISTS_WITHOUT_IT
   = NO_QUALIFYING_SET
   ```

   Population 001's source event is included in the candidate enumeration for audit completeness. It is excluded from selection. If no qualifying set exists without it, there is no qualifying set — the procedure does not fall back to a Population 001 reuse.

#### Step 5 — Byte-Exact Ordering Semantics and Combination Selection

5. **Select the qualifying combination under a byte-exact ordering rule.**

   Ordering semantics:

   ```text
   IMMUTABLE_SOURCE_COMMIT_ASCENDING
   = LOWERCASE_HEX_BYTEWISE_ASCENDING

   SOURCE_PATH_LEXICOGRAPHIC
   = UTF8_BYTEWISE_ASCENDING
   OVER_REPOSITORY_CANONICAL_PATH

   MANIFESTATION_ID_LEXICOGRAPHIC
   = UTF8_BYTEWISE_ASCENDING
   OVER_PREASSIGNED_MANIFESTATION_ID
   ```

   These definitions eliminate ambiguity from case handling, locale, Unicode collation, or normalization. Lowercase hexadecimal commit hashes are compared byte-by-byte. Repository canonical paths are compared as UTF-8 byte sequences. Manifestation identifiers are encoded as UTF-8 and compared byte-by-byte in ascending order. No locale-sensitive collation, Unicode normalization, decoded-character ordering, or display ordering is applied.

   Combination selection rule:

   ```text
   SELECTED_EVENT_SET
   = SMALLEST_CARDINALITY_QUALIFYING_SET

   IF_MULTIPLE
   = LEXICOGRAPHICALLY_EARLIEST_VECTOR
   OF_CANDIDATE_ORDER_INDICES
   ```

   First, all qualifying event sets are identified. A qualifying set is a set of candidates that, taken together, satisfies all three selection criteria (multiple source objects, multiple failure manifestations, at least one unresolved or unrepaired path).

   Among qualifying sets, the smallest cardinality set is preferred. If multiple qualifying sets share the smallest cardinality, the set whose sorted vector of candidate order indices is lexicographically earliest is selected.

   Example: if candidates A, B, C, D are ordered as [1, 2, 3, 4] and qualifying pairs exist at {A,C}=[1,3], {A,D}=[1,4], and {B,C}=[2,3], then {A,C}=[1,3] is selected because [1,3] is lexicographically earlier than [1,4] and [2,3]. No qualifying triple can outrank any qualifying pair.

   ```text
   QUALIFICATION
   → FIXED_CANDIDATE_UNIVERSE
   → FIXED_TOTAL_ORDER
   → FIXED_SUBSET_ORDER
   → UNIQUE_SELECTED_SET
   ```

#### Step 6 — Preservation of Unselected Qualifying Candidates

6. **Preserve rejected qualifying candidates and reason they were not selected.** If multiple event sets satisfy all three criteria, the non-selected qualifying sets are preserved with the ordering reason. They are not rejected as invalid; they were ordered later.

```text
QUALIFYING_BUT_UNSELECTED
!= REJECTED_AS_INVALID

NOT_SELECTED
!= LOW_SIGNIFICANCE

EARLIER_ORDER
!= GREATER_IMPORTANCE
```

The ordering rule is deterministic and reproducible. It does not rank by importance, severity, or evidentiary priority. Earlier order under the predeclared rule is a mechanical property, not an evaluative judgment.

## Ordered Gates

1. **Admit this predeclaration.** The selection rule and selection procedure are frozen before any event is evaluated against the Population 002 selection procedure. No event is selected before this predeclaration is preserved on main.

2. **Enumerate and select events under the frozen selection procedure.** Source events are enumerated, recorded, evaluated, and selected by the predeclared ordering rule. Selection must satisfy all three criteria. Selection must not be influenced by any non-criterion. Qualifying but unselected candidates are preserved with ordering reason.

3. **Construct gallery entries.** Each entry binds to an immutable commit, path, Git blob, and SHA-256. Each entry declares lens memberships. Each entry records `boundary_made_observable` with `statement_origin` and `support_refs` where applicable. Each entry binds `current_standing` to `standing_observed_at_commit`, `standing_source_path`, and `standing_source_identity`.

4. **Preserve the population package.** Machine-readable JSON, README, SHA256SUMS, candidate enumeration, and any procedural notes are preserved as a bounded population artifact. Source artifacts are referenced, not copied. The design freeze is not modified.

5. **Admit the population.** On merge, the population takes effect with `STANDING_INHERITANCE = NONE` and `DESIGN_FREEZE_MODIFIED = FALSE`.

## Instantiation

This predeclaration defines the selection rule and selection procedure for `FORK-EVIDENCE-LENS-GALLERY-001-POPULATION-002`. No events have been selected. No entries have been created. The selection rule and procedure are frozen before any event is evaluated against the Population 002 selection procedure.

```text
PREDECLARATION
= FROZEN

EVENT_SELECTION
= NOT_BEGUN

SELECTION_RULE
= FROZEN

SELECTION_PROCEDURE
= FROZEN

SELECTION_NON_CRITERIA
= FROZEN

RECURSIVE_ELIGIBILITY_BOUNDARY
= FROZEN

POPULATION_002_ENTRIES
= ZERO_AT_PREDECLARATION
```

Population 002 requires a separately recorded successor step that:

1. preserves this predeclaration unchanged;
2. enumerates all preserved source events reachable from `main@56b4e064fa061417a82b7017f56d0dd98f225aa5` satisfying the frozen ELG source-binding requirements;
3. records each candidate before evaluating Population 002 fit;
4. evaluates each candidate only against source-object identity, observable-manifestation distinctness, standing state, and source-binding completeness;
5. selects the first qualifying combination under the predeclared ordering rule;
6. preserves qualifying but unselected candidates with ordering reason;
7. rejects any selection influenced by a declared non-criterion;
8. creates gallery entries that reference, not copy, source artifacts;
9. binds each entry's source coordinate to an immutable commit hash, path, Git blob, and SHA-256 where available;
10. declares lens memberships per entry;
11. records `boundary_made_observable` with `statement_origin` and `support_refs` where applicable;
12. binds `current_standing` to `standing_observed_at_commit`, `standing_source_path`, and `standing_source_identity`;
13. does not promote standing for any referenced artifact;
14. preserves every non-claim declared in the design freeze and in this predeclaration.

## Canonical Boundary Sentences

```text
POPULATION_002_PURPOSE
= TEST_CROSS_OBJECT_ROUTING

HETEROGENEITY
!= SCALE

SECOND_POPULATION
!= HISTORICAL_SWEEP

SECOND_POPULATION
= HETEROGENEITY_PRESSURE_TEST

SELECTION_RULE
= PREDECLARED

SELECTION_PROCEDURE
= PREDECLARED

SELECTION_CRITERIA
!= SELECTION_PROCEDURE

EVENT_SELECTION
!= EDITORIAL_IMPORTANCE_RANKING

PREDECLARATION_FREEZE
!= FIRST_AWARENESS_OF_ALL_POSSIBLE_EVENTS

KNOWN_EVENT
!= SELECTED_EVENT

GENERAL_ELIGIBILITY
!= POPULATION_002_ELIGIBILITY_DETERMINATION

CANDIDATE_SELECTION_UNIT
= SOURCE_EVENT × OBSERVABLE_MANIFESTATION

CANDIDATE_UNIVERSE
= EVERY_DISTINCT_SOURCE_EVENT × OBSERVABLE_MANIFESTATION

CANDIDATE_EXISTS
IFF
  SOURCE_EVENT_HAS_EXPLICIT_PRESERVED_IDENTIFIER
  AND_MANIFESTATION_HAS_UNIQUE_ADDRESSABLE_PRESERVED_RECORD
  AND_FROZEN_SOURCE_BINDING_REQUIREMENTS_ARE_SATISFIED

EXPLICIT_MANIFESTATION_ID
= OPTIONAL

IF_NO_UNIQUE_PRESERVED_RECORD_BOUNDARY
= CANDIDATE_ENUMERATION_FAILURE NOT_CANDIDATE_INELIGIBILITY

SOURCE_LOCAL_RECORD_OFFSET
= ZERO_BASED_BYTE_OFFSET OF_FIRST_BYTE
  OF_THE_UNIQUE_ADDRESSABLE_MANIFESTATION_RECORD
  IN_CANONICAL_GIT_BLOB_BYTES

BYTE_OFFSET
!= LINE_NUMBER

BYTE_OFFSET
!= CHARACTER_OFFSET

BYTE_OFFSET
!= DISPLAY_POSITION

CANONICAL_SOURCE_BINDING
= BINDING_EXPLICITLY_DECLARED_BY_PRESERVED_RECORD_FOR_THAT_MANIFESTATION

IF_NO_UNIQUE_CANONICAL_BINDING_EXISTS
= CANDIDATE_ENUMERATION_FAILURE NOT_CANDIDATE_INELIGIBILITY

GENERATED_MANIFESTATION_ID
!= SOURCE_ASSERTED_IDENTIFIER

MANIFESTATION_ORDER_KEY
= CANONICAL_SOURCE_PATH + SOURCE_LOCAL_RECORD_OFFSET_OR_EXPLICIT_FINDING_ID

SAME_REPOSITORY + SAME_PREDECLARATION
→ SAME_CANDIDATE_DECOMPOSITION
→ SAME_BINDING_PER_CANDIDATE
→ SAME_ORDER
→ SAME_SELECTED_SET

CANDIDATE_ORDER
= IMMUTABLE_SOURCE_COMMIT_ASCENDING
THEN SOURCE_PATH_LEXICOGRAPHIC
THEN MANIFESTATION_ID_LEXICOGRAPHIC

IMMUTABLE_SOURCE_COMMIT_ASCENDING
= LOWERCASE_HEX_BYTEWISE_ASCENDING

SOURCE_PATH_LEXICOGRAPHIC
= UTF8_BYTEWISE_ASCENDING

MANIFESTATION_ID_LEXICOGRAPHIC
= UTF8_BYTEWISE_ASCENDING

SELECTED_EVENT_SET
= SMALLEST_CARDINALITY_QUALIFYING_SET
THEN LEXICOGRAPHICALLY_EARLIEST_VECTOR_OF_CANDIDATE_ORDER_INDICES

POPULATION_001_SOURCE_EVENT
= ENUMERATED_FOR_AUDIT
= INELIGIBLE_FOR_POPULATION_002_SELECTION

QUALIFYING_BUT_UNSELECTED
!= REJECTED_AS_INVALID

NOT_SELECTED
!= LOW_SIGNIFICANCE

EARLIER_ORDER
!= GREATER_IMPORTANCE

CANDIDATE_ENUMERATION_FAILURE
!= CANDIDATE_INELIGIBILITY

CURRENT_STANDING_REGISTER
!= CANDIDATE_EVENT_SURFACE

GALLERY_PROCESS_FAILURE
MAY_BECOME FUTURE_SOURCE_EVENT

FAILURE_OCCURRED
!= GALLERY_ENTRY_CREATED

GALLERY_ELIGIBILITY
!= GALLERY_ADMISSION

ELG_INSPECTING_ELG_CONSTRUCTION
!= ELG_SELF_AUTHORIZATION

UNRESOLVED_STANDING_REPRESENTED
!= UNRESOLVED_STANDING_RESOLVED

PROVISIONAL_STANDING_OBSERVATION
!= PROVISIONAL_STANDING_PROMOTION

PREDECLARATION
!= POPULATION

PREDECLARATION_FROZEN
!= EVENT_SELECTION_BEGUN
```
