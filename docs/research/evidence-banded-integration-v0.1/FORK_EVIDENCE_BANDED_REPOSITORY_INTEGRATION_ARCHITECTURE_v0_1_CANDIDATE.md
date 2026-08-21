# Fork Evidence-Banded Repository Integration Architecture v0.1 — Candidate

Status: `CANDIDATE_INTEGRATION_ARCHITECTURE_NO_ADMISSION_EFFECT`

## 1. Purpose

This architecture gives repository users an explicit routing layer for evidence of different maturity and standing without rewriting the native standing of the underlying artifacts.

It solves an integration problem, not a governance-substitution problem.

```text
NATIVE_STANDING
  remains native to the artifact / governance record

INTEGRATION_BAND
  expresses how that artifact may be routed or presented now
```

Therefore:

```text
INTEGRATION_BAND != NATIVE_STANDING
BAND_PLACEMENT != ADMISSION
BAND_A != TRUTH_OR_GENERAL_VALIDATION
BAND_B != ADMITTED_PROOF
BAND_C != IMPLEMENTED_CAPABILITY
BAND_D != HISTORICAL_INVALIDATION
BAND_E != OBSOLETE_OR_ERASABLE
```

## 2. The five bands

### BAND A — ADOPTION BASELINE

Purpose: surfaces that may support present adopter-facing explanation or integration **within their exact declared scope**.

Eligible classes include:

- already-admitted Fork repository primitives whose native standing permits their bounded use;
- the Fork Research Program/Candidate Model vocabulary and governance primitives only to the extent their native records permit;
- D5.0 only as an adopted temporal vocabulary/specification **if its external source identity is separately bound**; not as an implemented temporal checker or capability.

Band A permits no inference of general validation, production readiness, compliance, legal sufficiency, institutional authority, or execution permission.

### BAND B — QUALIFIED CANDIDATE PROOFS

Purpose: executable or otherwise pressure-tested surfaces that provide useful purpose-specific evidence but retain explicit qualification, candidate, freeze, admission, or generality limits.

Initial external candidates:

- AP-Q03 v0.1.1 — candidate proof for nomenclature/semantic-regression pressure, with its source-level qualifications preserved;
- Capture-Coverage — candidate proof bounded to a synthetic population and its reported-review strength.

A Band B proof may support a bounded demonstration. It may not be rounded upward into generalized Fork validation or silently described as admitted when its native standing says otherwise.

### BAND C — ACTIVE EMPIRICAL RESEARCH

Purpose: preregistered, construction-ready, executing, or exploratory scientific work that is producing evidence but has not crossed the applicable admission/qualification gates.

Initial classes include:

- SCTD semantic-compression/transferal-deviation research;
- D5.1 closed-rule candidate work;
- semantic-environment/feature-consumption successor fixtures;
- active research/simulation candidates such as GHCH and CAD research surfaces where applicable.

Band C is where Fork is allowed to learn without marketing research state as product behavior.

### BAND D — REPAIR / EXCLUDED FROM ADOPTION

Purpose: surfaces with a known material repair obligation, unresolved defect, or standing that makes adopter-facing reliance inappropriate until a named repair or disposition closes.

Initial classes include:

- LPT v0.1.1 until its material oracle repairs are closed;
- active correction candidates such as PROOF-005 F3 v0.2.3 while the correction/review sequence remains open;
- adverse or superseded experimental material where current use would overread the evidence.

Band D does not erase earlier useful observations. It blocks inappropriate current adoption treatment.

### BAND E — HISTORICAL / PRESERVATION

Purpose: immutable predecessor, adverse-result, correction-lineage, failed-transport, stale-projection, and exterior-review records retained so that current state remains reconstructable.

Band E artifacts may be essential evidence even when they are not current operational guidance.

```text
HISTORICAL != FALSE
SUPERSEDED != DELETED
CORRECTED != RETROACTIVELY_NEVER_OCCURRED
```

## 3. Placement dimensions

Every registry entry should independently record:

1. `repository_presence`
2. `native_standing`
3. `integration_band`
4. `purpose_specific_use`
5. `qualifications`
6. `prohibited_claims`
7. `admission_binding`, if any
8. `execution_state`
9. `exteriority/recomputation_state`
10. `successor_or_predecessor_relationship`

Missing coordinates remain missing. Band assignment may not manufacture them.

## 4. Repository-presence vocabulary

Use at least:

- `PRESENT_AT_GOVERNED_BASE`
- `OPEN_PR_CANDIDATE`
- `RESEARCH_BRANCH_ONLY`
- `EXTERNAL_PACKET_ONLY_NOT_REPOSITORY_BOUND`
- `HISTORICAL_COORDINATE_ONLY`
- `NOT_ESTABLISHED`

Rules:

```text
PRESENT_AT_GOVERNED_BASE != ADMITTED_FOR_ALL_PURPOSES
OPEN_PR_CANDIDATE != ADMITTED
RESEARCH_BRANCH_ONLY != GOVERNED_BASELINE
EXTERNAL_PACKET_ONLY != REPOSITORY_ADMITTED
ABSENT_FROM_ONE_ROUTE != NEVER_EXISTED
```

## 5. Non-inheritance controls

The routing layer must preserve these controls:

```text
REPOSITORY_PRESENCE != ADMISSION
CHECKER_PASS != GENERAL_VALIDATION
SPECIFICATION_ADOPTED != CAPABILITY_IMPLEMENTED
HISTORICAL_AUTHORIZATION != CONTINUING_AUTHORITY
SELF_REPORTED_INDEPENDENT_EXECUTION != EXTERIOR_REVIEWER_VERIFIED_EXECUTION
MULTI_REVIEWER_AGREEMENT != INDEPENDENT_CORROBORATION
MANIFEST_COMPONENT_PRESENCE != COMPONENT_BYTE_INTEGRITY
SOURCE_CONTINUITY != TRANSFER_REPRESENTATION_CONTINUITY
```

Reviewer independence must itself be evidenced before agreement is counted as independent corroboration.

## 6. Routing rules

### From Band C to Band B

Requires purpose-specific executed evidence, preserved input/output coordinates, explicit oracle/result boundaries, and whatever independent/exterior qualification the candidate's own protocol requires. Execution alone does not require or authorize promotion.

### From Band B to Band A

Requires a separate adoption/admission decision identifying exactly what proposition becomes adopter-facing, the supporting candidate proof, its retained qualifications, and prohibited claims. Proof success does not self-promote.

### From Band D

A successor may leave Band D only after the named repair condition is closed and the appropriate recomputation/review/disposition sequence is preserved. The predecessor remains Band E or otherwise historically addressable.

### Into Band E

Preservation is append-only. Band E is not a trash category. It is the repository's reconstructive memory.

## 7. D5.0 / D5.1 boundary

D5.0 may be described only as temporal semantic vocabulary/specification under the evidence currently available outside the repository re-entry base. No repository presence or checker implementation is inferred from that external disposition.

D5.1 remains research-only until its own authorized schema, checker, fixtures, execution, and disposition are separately established.

```text
D5_0_SPECIFICATION_STANDING
  != D5_0_EXECUTABLE_CAPABILITY

D5_0_ADOPTION
  != D5_1_IMPLEMENTATION
```

## 8. SCTD placement

SCTD begins in Band C. A repository branch may preserve its preregistration, immutable T0, harness, TF-00 execution, receipts, and longitudinal dataset without changing that standing.

TF-00 establishes only the registered lossless-control proposition. It does not demonstrate the future transfer/compression hypotheses.

```text
TF00_PASS
  != SCTD_GENERAL_PATTERN_DEMONSTRATED
  != PRODUCT_CAPABILITY
```

## 9. Architecture standing

This architecture is itself Band C / candidate integration research until separately reviewed and, if desired, admitted. It cannot self-assign Band A standing to itself or to any other artifact.
