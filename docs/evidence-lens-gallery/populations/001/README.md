# FORK-EVIDENCE-LENS-GALLERY-001 — Population 001

Status: `POPULATION_CANDIDATE__EFFECTIVE_ON_MERGE`

Predecessor design freeze: `FORK-EVIDENCE-LENS-GALLERY-001 v0.1`

Predecessor merge coordinate: `5ee76df67f25ff6be03f025cf6795088b9c4aef2`

## Lens Shift

```text
FIRST_POPULATION
!= SHOWCASE

FIRST_POPULATION
= CALIBRATION_OF_POPULATION_MECHANICS
```

The first population is deliberately not an attempt to select Fork's most important, representative, severe, or persuasive failure. Doing so would convert the first population step into an editorial ranking exercise.

Population 001 instead uses one already-admitted exterior recomputation/correction return with two distinct observable manifestations. This is a calibration population: it exercises the frozen ELG machinery before any broad historical routing is attempted.

```text
CALIBRATION_SELECTION
!= REPRESENTATIVE_SAMPLE

FIRST_ENTRY_ORDER
!= IMPORTANCE_ORDER

EASE_OF_BINDING
!= EVIDENTIARY_PRIORITY
```

## Source event

`FORK-RRD-001-AG0-GIT-OBJECT-INDEPENDENT-RECOMPUTATION-RETURN-001`

The source return was admitted by merge commit:

`c2ae0ee435857c08cb074fc28e8302045572f50d`

Population 001 references the native source records. It does not copy them.

Bound source records:

- `docs/exterior-returns/FORK-RRD-001-AG0-GIT-OBJECT-INDEPENDENT-RECOMPUTATION-RETURN-001/SOURCE_RETURN.md`
  - Git blob: `da221713c9270cf548f567ef728de17d0cfdf0df`
  - SHA-256: `4f428025fd41038bb66c9cdb491292ae10a6a35dcd8fbda82b1f9d6c679269bc`
- `docs/exterior-returns/FORK-RRD-001-AG0-GIT-OBJECT-INDEPENDENT-RECOMPUTATION-RETURN-001/ADMISSION.json`
  - Git blob: `254c4bdce5fe79375a3981ae5fd1ba00edb4ab24`
  - SHA-256: `61d7983ef5fd6782542793a1f015648b82f0ca6a3637d0a63fd61e94e4d0c4f1`
- `docs/exterior-returns/FORK-RRD-001-AG0-GIT-OBJECT-INDEPENDENT-RECOMPUTATION-RETURN-001/RECONCILIATION.md`
  - Git blob: `11fac298615ced1d3ad5d3e8bd36f307adb33817`
  - SHA-256: `93e1b27988d51d087e61e040462d85ed7981a9de84d6e2b996695aacfcc16e34`

## Why two entries

The frozen ELG cardinality rule is:

```text
GALLERY_ENTRY_UNIT
= SOURCE_EVENT × OBSERVABLE_MANIFESTATION

MULTIPLE_ENTRIES_FOR_SAME_SOURCE_EVENT
REQUIRE
DISTINCT_OBSERVABLE_MANIFESTATIONS
```

The admitted exterior return contains two distinct corrected manifestations:

1. the source document's timestamp conversion was wrong;
2. the source document's parent-to-child elapsed-time result was wrong.

Therefore Population 001 creates two entries from one source event rather than duplicating one manifestation through multiple lenses.

## Entries

### ELG-ENTRY-0001 — timestamp conversion

Observed manifestation:

```text
RAW_GIT_TIMESTAMP
= 1790310255 -0700

SOURCE_DOCUMENT_CLAIMED_LOCAL_TIME
= 2026-09-24 18:30:55 PDT

CORRECTED_LOCAL_TIME
= 2026-09-24 21:24:15 PDT
```

Lens memberships:

- `FAILURE_MANIFESTATION`
- `RECOMPUTATION`
- `BOUNDARY_DISCOVERY`

Gallery-derived boundary:

```text
STRUCTURAL_TIMESTAMP_PRESENCE
!= CORRECT_TEMPORAL_DERIVATION
```

### ELG-ENTRY-0002 — elapsed-time derivation

Observed manifestation:

```text
SOURCE_DOCUMENT_CLAIMED_ELAPSED
= 00:34:10

CORRECTED_ELAPSED
= 03:27:30

CORRECTED_ELAPSED_SECONDS
= 12450
```

Lens memberships:

- `FAILURE_MANIFESTATION`
- `RECOMPUTATION`
- `BOUNDARY_DISCOVERY`

Gallery-derived boundary:

```text
ARITHMETIC_CONSISTENCY_WITH_INCORRECT_INPUT
!= CORRECT_DERIVED_RESULT
```

## Standing

Both entries bind standing at repository coordinate `5ee76df67f25ff6be03f025cf6795088b9c4aef2` to the preserved reconciliation source.

```text
SOURCE_RETURN
= REPOSITORY_ADMITTED_EXTERIOR_RETURN

TIMESTAMP_DERIVATION_CORRECTION
= ADMITTED_APPEND_ONLY

ELAPSED_TIME_CORRECTION
= ADMITTED_APPEND_ONLY

AG0_BYTES
= UNCHANGED

RRD_OBJECT_STATUS
= CLOSED_HISTORICAL_EVIDENCE

SEMANTIC_STANDING_CHANGE
= NONE
```

Gallery membership does not alter any of those standings.

## Population effect

On merge:

```text
GALLERY_POPULATION
= 2_ENTRIES

SOURCE_EVENTS_REFERENCED
= 1

SOURCE_ARTIFACTS_COPIED
= 0

HISTORICAL_SOURCE_ARTIFACTS_MODIFIED
= 0

SOURCE_STANDING_CHANGES
= 0

DESIGN_FREEZE_MODIFIED
= FALSE
```

## Non-claims

```text
POPULATION_001
!= COMPLETE_FAILURE_POPULATION

POPULATION_001
!= REPRESENTATIVE_SAMPLE

FIRST_ENTRY_ORDER
!= IMPORTANCE_ORDER

ENTRY_COUNT
!= FAILURE_FREQUENCY

COMMON_LENS_MEMBERSHIP
!= ESTABLISHED_TAXONOMIC_CLASS

GALLERY_DERIVED_BOUNDARY
!= SOURCE_ASSERTED_BOUNDARY

POPULATION_ADMISSION
!= SOURCE_STANDING_CHANGE
```
