# Fork Standing and Non-Inheritance Contract v0.1

**Artifact type:** repository interpretation contract  
**Standing:** `CANDIDATE_REPOSITORY_INTERPRETATION_CONTRACT`  
**Date:** 2026-09-09

## 1. Purpose

This contract defines how current and historical Fork artifacts are interpreted when multiple research, proof, commercial, interoperability, longitudinal, and review surfaces coexist in one repository.

Its function is representational only. It does not grant authority to an artifact, repair an artifact, execute an experiment, validate a result, or convert repository presence into adoption.

## 2. Orthogonal status dimensions

Each current work object should be classified independently across the following dimensions.

### Artifact state

- `NOT_CONSTRUCTED`
- `CONSTRUCTED`
- `PENDING_BYTE_ADMISSION`
- `PRESENT_IN_REPOSITORY`
- `HISTORICAL_VERSION`
- `SUPERSEDED`

### Execution state

- `NOT_EXECUTED`
- `EXECUTED_BOUNDED`
- `EXECUTED_NONSCORABLE`
- `REPRODUCTION_INCONCLUSIVE`
- `STOPPED_BY_DESIGN`
- `NOT_APPLICABLE`

### Result state

- `NOT_DETERMINED`
- `PASS_WITHIN_SCOPE`
- `PARTIAL`
- `FAIL_LOCALIZED`
- `INDETERMINATE`
- `NO_SCORABLE_CONDITION`
- `NEGATIVE_RESULT`

### Freeze state

- `NOT_FROZEN`
- `FROZEN_FOR_PRESSURE`
- `FROZEN_RESEARCH_METHOD_BASELINE`
- `FREEZE_REVIEW_PENDING`
- `FREEZE_ELIGIBILITY_SUPPORTED`
- `FROZEN`

### Independence state

- `NOT_ASSESSED`
- `PROCEDURAL_ONLY`
- `DEPENDENT_BUT_USEFUL_PRESSURE`
- `INDEPENDENCE_NOT_ESTABLISHED`
- `INDEPENDENT_REVIEW_PENDING`
- `INDEPENDENT_WITHIN_DECLARED_SCOPE`

### Admission state

- `NOT_REGISTERED`
- `REGISTERED_CURRENT_STATE_ONLY`
- `PENDING_BYTE_ADMISSION`
- `ADMITTED_RESEARCH_RECORD`
- `ADMITTED_HISTORICAL_RECORD`
- `ADMITTED_METHOD_BASELINE`
- `ADMITTED_PROOF_SURFACE`
- `INTENTIONALLY_EXCLUDED`

### Commercial-use state

- `NOT_APPLICABLE`
- `RESEARCH_ONLY`
- `CANDIDATE_FOR_APPLIED_USE`
- `METHOD_QUALIFICATION_REQUIRED`
- `BOUNDED_PILOT_DISCOVERY_ONLY`

No value in one dimension supplies a value in another dimension.

## 3. Mandatory non-implications

```text
CONSTRUCTED != EXECUTED
EXECUTED != PASSED
PASSED != FROZEN
FROZEN != INDEPENDENTLY_REVIEWED
INDEPENDENTLY_REVIEWED != REPOSITORY_ADMITTED
REPOSITORY_ADMITTED != GOVERNANCE_ADOPTED
REPOSITORY_ADMITTED != COMMERCIALLY_QUALIFIED
STRUCTURALLY_VERIFIED != FACTUALLY_TRUE
PRESERVED != COMPLETE
HISTORICALLY_VALID != PRESENTLY_AUTHORIZED
OBSERVED != OCCURRED
STOP_REQUESTED != CONSEQUENCE_PREVENTED
RECOMPUTABLE != SUFFICIENT_FOR_RELIANCE
```

## 4. Adjacency rule

Repository proximity has no inheritance semantics.

```text
A adjacent_to B
```

establishes only that both artifacts are represented within a shared repository surface or index. It does not establish:

- derivation;
- equivalence;
- dependency;
- endorsement;
- validation;
- applicability;
- semantic compatibility;
- authority transfer;
- standing transfer;
- chronological succession;
- causal relation.

Any such relation must be separately recorded.

## 5. Historical preservation rule

A successor status record may classify a predecessor but must not rewrite the predecessor's historical meaning.

```text
SUCCESSOR_REPAIR
!= PREDECESSOR_ERASURE
```

```text
CURRENT_STANDING_CHANGED
!= HISTORICAL_EVENT_CHANGED
```

Failed, adverse, superseded, abandoned, stopped, inconclusive, and non-scorable records remain part of the longitudinal corpus when they materially explain the program's development.

## 6. Failure preservation rule

The following are valid terminal or intermediate research outcomes and must not be silently rewritten as unfinished work merely because they lack a positive score:

- `FAIL_LOCALIZED`
- `NO_SCORABLE_CONDITION`
- `REPRODUCTION_INCONCLUSIVE`
- `MISSING_PREMISE`
- `INDEPENDENCE_NOT_ESTABLISHED`
- `STOPPED_BY_DESIGN`
- `NO_MATERIAL_BOUNDARY`
- `MAPPING_REJECTED`
- `NON_COMPARABLE`
- `EXTERNAL_EVIDENCE_REQUIRED`
- `INDETERMINATE`

## 7. Current-state record authority

The current work register is authoritative only for the repository's declared **current program-state representation at its snapshot date**.

It is not authoritative for:

- the truth of an underlying external claim;
- the correctness of an experiment;
- the completeness of all historical evidence;
- institutional, legal, compliance, safety, procurement, or production determinations;
- the canonical bytes of a `PENDING_BYTE_ADMISSION` object.

When the current register conflicts with an older status summary, the newer register controls only the question "what standing does the repository presently assign?" It does not retroactively change what the older record said or what occurred historically.

## 8. Multi-purpose repository rule

An artifact may be discoverable from multiple purpose routes without changing identity or standing.

For example, an adversarial fixture may simultaneously be relevant to research, failure modes, proof surfaces, and procurement diligence. That multi-route visibility does not create four separate artifacts and does not strengthen the result.

```text
MULTIPLE_PURPOSE_ROUTES
!= MULTIPLE_INDEPENDENT_CONFIRMATIONS
```

## 9. Closure rule

A repository closure pass succeeds when a competent reviewer can determine, for every registered active work object:

1. what the object is;
2. whether its bytes are present;
3. whether it was executed;
4. the bounded result, including failure or non-result;
5. whether it is frozen;
6. whether independence is established;
7. whether work intentionally stopped;
8. the next evidence-bearing gate;
9. what stronger claims are not inherited.

Nothing in this contract inherits stronger meaning from adjacency, indexing, cross-reference, derivation, naming, execution success, or repository presence.