# Fork II Failure Routing Candidates — 2026-09-26

**Object:** `FORK_II_FAILURE_ROUTING_CANDIDATES_20260926`  
**Target surface:** Evidence Lens Gallery  
**Status:** `ROUTING_CANDIDATES_ONLY`  
**Standing effect:** `NONE`  
**Population 002 effect:** `NONE`.

This file does **not** enumerate, qualify, select, construct, or admit Evidence Lens Gallery Population 002 entries.

Population 002 already has a frozen selection procedure and declares `EVENT_SELECTION = NOT_BEGUN`. Therefore these observations are routed only as **candidate source-event pointers** for a future lawful enumeration under the frozen procedure.

```text
ROUTED_FOR_FUTURE_ENUMERATION
!= ELG_ELIGIBLE
!= ELG_SELECTED
!= ELG_ADMITTED
!= SOURCE_STANDING_CHANGE
```

## Candidate routes

| Candidate route | Preserved manifestation | Suggested lenses | Current source standing | Gallery effect |
| --- | --- | --- | --- | --- |
| `ELG-ROUTE-CANDIDATE-RUN003-RANGE-SERIALIZATION` | Run 003 recomputation initially produced `0/17` range-hash matches under a plausible serialization; exact final-LF contract later yielded `17/17` | `FAILURE_MANIFESTATION`, `RECOMPUTATION`, `BOUNDARY_DISCOVERY` | Initial failure and later recomputation both preserved; later result does not rewrite first observation | Reference only |
| `ELG-ROUTE-CANDIDATE-HISD001-MISSING-FREEZE` | promised pre-inspection freeze cannot be established from surviving historical record | `FAILURE_MANIFESTATION`, `BOUNDARY_DISCOVERY`, `TEMPORAL_STANDING` | Historical gap preserved; external reviewer lane remains protected | Reference only |
| `ELG-ROUTE-CANDIDATE-SPT001-VALIDATOR-DEFECTS` | symlink check after resolution; global byte-scan conflation; fixture normalization; status label not bound to execution evidence | `FAILURE_MANIFESTATION`, `VALIDATOR`, `BOUNDARY_DISCOVERY` | Residual implementation repairs identified; no generic execution correctness claimed | Reference only |
| `ELG-ROUTE-CANDIDATE-LS-ORACLE-B-BLINDING` | internal provisional-selection file included in archive intended for independent rating | `FAILURE_MANIFESTATION`, `INDEPENDENCE_BOUNDARY`, `BOUNDARY_DISCOVERY` | Package-level blinding risk; no evidence external rater viewed it or rating was affected | Reference only |
| `ELG-ROUTE-CANDIDATE-IDENTITY-AUTHORITY-SEPARATION` | stable artifact identity coexists with changing authority relation/state; adjacency does not transfer authority | `BOUNDARY_DISCOVERY`, `TEMPORAL_STANDING`, `NON_INHERITANCE` | Demonstrated as a bounded relation-separation pattern; not universal authority ontology | Reference only |
| `ELG-ROUTE-CANDIDATE-ORIGINAL-HYPOTHESIS-RUN001` | Run 001 reduced unsupported inheritance but violated false-withholding guardrail | `FAILURE_MANIFESTATION`, `SUCCESSOR_REPAIR`, `BOUNDARY_DISCOVERY` | Failed instrument run preserved; Run 002 does not retroactively pass it | Reference only |

## Source-boundary notes

### Run 003 representation failure

The event is not “hashing failed.” The narrower manifestation is:

```text
SAME LOGICAL RANGE
+ DIFFERENT SERIALIZATION ASSUMPTION
→ DIFFERENT HASH PREIMAGE
```

Later `17/17` recomputation establishes agreement under the identified byte-production contract. It does not erase the earlier underspecification.

### HISD-001 historical gap

The event is not “review failed.” The preserved manifestation is that a promised state transition cannot be established after the fact. The reviewer kept the package unopened rather than inheriting authority from the earlier intention.

This routing record does not inspect, resolve, or reconstruct the external lane.

### SPT-001 validator defects

Keep the four manifestations separable. They are not one generic validator failure:

1. symlink detection performed after resolution;
2. byte-convention checks applied globally to binary as well as text objects;
3. test fixtures normalized before byte-validation;
4. a `VERIFIED` label not bound to a content-addressed execution record.

### Lens Shift blinding risk

The record says **risk**, not contamination:

```text
INTERNAL_SELECTION_INFORMATION_EXPOSED_IN_ORACLE_HANDOFF
!= EXTERNAL_RATER_OPENED_FILE
!= RATING_CONTAMINATED
```

### Identity / authority separation

The Gallery route should preserve the observed distinction:

```text
ARTIFACT_IDENTITY_PERSISTS
!= AUTHORITY_RELATION_PERSISTS

HISTORICAL_AUTHORITY
!= CURRENT_AUTHORITY
```

## Non-promotion boundary

```text
GALLERY_ROUTE != GALLERY_ENTRY
GALLERY_ENTRY != SOURCE_CORRECTION
GALLERY_ADMISSION != SOURCE_STANDING_CHANGE
FAILURE_INSPECTABILITY != FAILURE_RESOLUTION
COMMON_LENS_MEMBERSHIP != ESTABLISHED_TAXONOMY
```
