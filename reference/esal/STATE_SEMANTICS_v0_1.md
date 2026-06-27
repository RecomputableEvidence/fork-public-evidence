# ESAL v0.1 State Semantics

**Project:** Fork — Recomputable Evidence for AI-Assisted Workflows  
**Artifact:** ESAL v0.1 State Semantics  
**Status:** Normative for ESAL v0.1 reference-oracle state semantics  
**Applies to:** `reference/esal/reducer.py`, `reference/esal/models.py`, `reference/esal/taxonomy.py`  
**Branch:** `boundary-delta-record-v0.1`  
**Reference surface:** ESAL v0.1 Reference Oracle

---

## 1. Purpose

This document defines the state semantics implemented by the ESAL v0.1 Reference Oracle.

It exists to prevent independent implementers from inferring stronger semantics than the v0.1 oracle currently enforces.

The ESAL v0.1 Reference Oracle is a conformance interpreter, not a production governance engine. It records and reduces governance-relevant event state deterministically. It does not decide legal sufficiency, ethical adequacy, institutional appropriateness, or production readiness.

---

## 2. State Model

The ESAL v0.1 reduced state contains:

```text
State :=
  authority:   Set<Capability>
  constraints: Set<Constraint>
  obligations: Set<Obligation>
  lineage:     OrderedList<BDR_ID>
  validity:    Boolean
  violations:  OrderedList<ViolationRecord>
```

The reference implementation represents state as an immutable object. Each event transition returns a new state.

The initial state is:

```text
authority   = {}
constraints = {}
obligations = {}
lineage     = []
validity    = true
violations  = []
```

---

## 3. Event Classes

ESAL v0.1 recognizes two state-transition event classes:

- `BDR_CREATED`  
- `EXECUTION`

### 3.1 BDR_CREATED

`BDR_CREATED` events may update:

- `authority`  
- `constraints`  
- `obligations`  
- `lineage`

### 3.2 EXECUTION

`EXECUTION` events may update only:

- `validity`  
- `violations`

An `EXECUTION` event must not mutate `authority`, `constraints`, `obligations`, or `lineage`.

---

## 4. Authority Semantics

### 4.1 Cumulative Trace-Level Authority

In ESAL v0.1, authority state is **cumulative trace-level authority**.

This means the authority set represents capabilities established anywhere in the replayed trace up to the current point.

Formally, for `BDR_CREATED` events:

```text
state.authority_next = state.authority_current ∪ event.delegated_authority
```

### 4.2 Not Per-Hop Active Scope

ESAL v0.1 does **not** model per-hop active authority scope.

A child BDR may declare a narrowed authority set, but the reduced trace-level authority remains cumulative.

Example:

```text
Root authority:  {read, write}
Child authority: {read}
Reduced state:   {read, write}
```

This does not mean the child BDR grants `write`. It means the v0.1 state records that `write` exists in the accumulated trace authority.

Per-BDR active-scope enforcement is out of scope for ESAL v0.1.

### 4.3 Authority Inflation

ESAL v0.1 prohibits silent authority inflation.

If a child BDR declares authority that is not already present in the accumulated authority state, and no explicit expansion marker is present, the reducer raises a governance error.

Example:

```text
Parent state authority:    {read}
Child delegated authority: {read, write}
Expansion marker:          absent
Result:                    GovernanceError / G
```

Expected error code:

```text
AUTHORITY_INFLATION
```

#### 4.3.1 Explicit Expansion Marker Definition
The ESAL v0.1 Reference Oracle recognizes the following explicit authority expansion markers in the BDR event body:

- Boolean field `expanded_authority: true`
- String field `authority_delta_type` with one of these values:
  - `expand`
  - `expanded`
  - `expanded_authority`
  - `authority_expansion`

If neither marker is present, any net-new authority in a child BDR raises `GovernanceError` with:

```text
error_code = AUTHORITY_INFLATION
```

This is a halted G-class path.

Marker recognition confirms structural compliance with the expansion declaration requirement.

It does not constitute validation that the expanding actor held authority to authorize the expansion.

It does not establish that the expansion was institutionally approved, legally sufficient, policy-compliant, or valid outside the ESAL v0.1 reference-oracle structure.

It also does not establish decision correctness, substantive validity, truth, safety, compliance, admissibility, or governance adequacy.

The foregoing list is illustrative, not exhaustive. Marker recognition is a structural recognition event inside the ESAL v0.1 reference oracle, not an authorization, approval, certification, or validation of the underlying expansion.

### 4.4 Empty Authority

In ESAL v0.1, an empty authority set means:

> no authority restriction has been declared

It does **not** mean:

> deny all actions

The current reference oracle therefore does not reject execution solely because `state.authority` is empty.

A future ESAL version may introduce explicit deny-all or closed-world authority semantics, but that is not part of v0.1.

Important v0.1 non-claim:

```text
PASS does not imply affirmative authorization.

A trace may pass the authority check because the action is present in a non-empty accumulated authority set.
A trace may also pass the authority check because no authority restriction was declared.
The ESAL v0.1 Reference Oracle does not distinguish those two PASS paths in its classification output.

ESAL v0.1 cannot determine whether an execution was affirmatively authorized or merely proceeded because no authority restriction was declared.

PASS is therefore a replay classification, not an authorization decision.

Consumers MUST NOT interpret PASS as proof that an action was affirmatively authorized.
```
---

### 4.5 Action-Outside-Authority Enforcement
If `state.authority` is non-empty and an `EXECUTION` event body contains an `action` field whose value is not present in `state.authority`, the reducer raises `GovernanceError` with:

```text
error_code = ACTION_OUTSIDE_AUTHORITY
```

This halts reduction.

Expected result:

```text
classification = G
fingerprint = None
state = None
exception = GovernanceError
```

If `state.authority` is empty, this check does not fire.  
If the EXECUTION body does not include an  ction field, this check does not fire.
In ESAL v0.1, an EXECUTION event without an action field does not trigger `ACTION_OUTSIDE_AUTHORITY`.

Absent action fields are therefore treated as outside the v0.1 authority check, not as structural errors and not as automatic governance errors.

This is an open-world v0.1 behavior. A future ESAL version may require action for all EXECUTION events or classify missing action as S or G.
This rule preserves the v0.1 distinction between:

- empty authority = no restriction declared  
- non-empty authority = declared authority envelope


### 4.6 Compound Open-World PASS Case

The following compound path is possible in ESAL v0.1:

```text
state.authority = {}
EXECUTION body has no action field
no other structural or governance failure occurs
```

In this path:

- the empty-authority rule means no authority restriction has been declared,  
- the absent-action rule means ACTION_OUTSIDE_AUTHORITY does not fire,  
- reduction continues under ordinary replay rules, and  
- if no other structural, governance, or determinism failure occurs, the trace classifies as `PASS`.

This PASS classification does **not** imply affirmative authorization.

It means only that the ESAL v0.1 Reference Oracle did not detect a structural, governance, or determinism failure under its current open-world semantics.

This `PASS` result does not constitute authorization, approval, legal sufficiency, policy compliance, decision correctness, or substantive validity.

This behavior reflects ESAL v0.1 open-world authority semantics and may not apply to future ESAL versions.

## 5. Constraint Semantics

Constraints accumulate into trace state.

For `BDR_CREATED` events:

```text
state.constraints_next = state.constraints_current ∪ event.constraints
```

The ESAL v0.1 Reference Oracle does not evaluate a constraint language.

Instead, it consumes encoded constraint-check results from `EXECUTION` event bodies.

Constraint check results are interpreted as follows:

- pass-like status: no violation appended  
- fail-like status: `validity = false`, append violation record  
- deferred/unknown/unresolved status: structural non-conformance unless policy treatment is encoded

---

## 6. Obligation Semantics

### 6.1 Obligations Accumulate by Union

In ESAL v0.1, obligations accumulate by union.

For `BDR_CREATED` events:

```text
state.obligations_next = state.obligations_current ∪ event.obligations
```

This means once an obligation is introduced into the trace state, it remains present unless a future ESAL version defines an explicit discharge or termination mechanism.

### 6.2 Child BDRs Need Not Restate Inherited Obligations

A child BDR is not required in v0.1 to explicitly restate every inherited obligation.

Example:

```text
Parent obligations: {log_all_outputs}
Child obligations:  {}
Reduced obligations: {log_all_outputs}
Classification: PASS, unless another violation occurs
```

This behavior is intentional for ESAL v0.1.

### 6.3 Obligation Dropping Is Not Enforced in v0.1

ESAL v0.1 does not classify omission of an inherited obligation from a child BDR as governance failure.

A future version may introduce an explicit rule such as:

```text
child_declared_obligations ⊇ inherited_obligations
```

or an explicit obligation-discharge mechanism.

Until then, obligation-dropping fixtures should not be used as expected-G tests for v0.1.

---

## 7. Lineage Semantics

Lineage is an ordered list of BDR identifiers appended during reduction.

For `BDR_CREATED` events:

```text
state.lineage_next = state.lineage_current + [bdr_id]
```

The reference oracle validates basic lineage before reduction after canonicalization.

Current lineage validation includes:

- unknown parent BDR detection  
- self-parent detection  
- duplicate BDR ID detection

Cycle detection is not implemented as a separate graph algorithm in v0.1. Multi-hop cycles are generally rejected through the canonical ordering and unknown-parent constraints.

---

## 8. Validity Semantics

The `validity` field is **monotonic false**.

Initial value:

```text
validity = true
```

If an execution records a failing constraint check:

```text
validity = false
```

Once `false`, validity remains false for the replayed trace.

There is no automatic restoration of validity in ESAL v0.1.

---

## 9. Violation Semantics

Violations are append-only records produced by replayable governance failures.

A constraint failure during `EXECUTION` appends a `ViolationRecord`.

A replayable governance-invalid trace may therefore produce:

```text
classification = G
fingerprint != None
state.validity = false
violations.length >= 1
```

This is distinct from a governance exception that halts reduction.

---

## 10. G-Class Semantics

ESAL v0.1 has **two** G-class paths.

### 10.1 Halted Governance Error

Some governance failures halt reduction.

Example:

- authority inflation without explicit expansion delta

Expected halted governance error codes include:

- `AUTHORITY_INFLATION`
- `ACTION_OUTSIDE_AUTHORITY`

Expected result:

```text
classification = G
fingerprint = None
state = None
exception = GovernanceError
```

### 10.2 Replayable Governance-Invalid State

Some governance failures are recorded inside the reduced state.

Example:

- constraint check status = fail

Expected result:

```text
classification = G
fingerprint != None
state.validity = false
violations.length >= 1
exception = None
```

Both are valid G-class outcomes in ESAL v0.1.

Independent implementations must preserve this distinction.

---

## 11. Failure Taxonomy

ESAL v0.1 classifications are:

| Classification | Meaning                         |
|----------------|---------------------------------|
| PASS           | Structurally valid and governance-valid replay |
| G              | Governance violation            |
| S              | Structural or substrate failure |
| D              | Determinism failure             |

### 11.1 PASS

A trace classifies as PASS when:

- event shape is valid,  
- canonicalization succeeds,  
- lineage validation succeeds,  
- reduction succeeds,  
- no governance violation is recorded,  
- state validity remains true.

### 11.2 G

A trace classifies as G when:

- reduction raises `GovernanceError`, **or**  
- reduction completes but state validity is false.

### 11.3 S

A trace classifies as S when:

- event shape is invalid,  
- JSONL substrate is malformed,  
- required fields are missing,  
- lineage validation fails,  
- unsupported structure is encountered.

### 11.4 D

A trace classifies as D when canonicalization detects determinism failure.

The primary v0.1 D-class fixture is conflicting duplicate `event_id` with differing normalized content.

---

## 12. Empty, Missing, and Legacy Fields

The reference oracle includes compatibility normalization for legacy fixtures.

However, after canonicalization, governance semantics are read from:

- `event["body"]`

not from top-level event fields.

Missing `body` fields are generally interpreted as empty sets or absent values unless the field is structurally required.

This compatibility behavior is part of the v0.1 reference surface.

---

## 13. Multi-Parent Merge Scope Boundary

Multi-parent BDR merge is out of scope for ESAL v0.1.

A BDR declaring multiple parents is not interpreted as a deterministic merge by the reference oracle.

Until a merge algebra is specified, multi-parent BDR behavior should be treated as unsupported structure or reserved for a future ESAL version.

ESAL v0.1 should not claim conformance over DAG merge semantics.

---

## 14. Per-Hop Enforcement Scope Boundary

ESAL v0.1 does not enforce per-hop active authority.

The oracle records cumulative trace-level authority and detects unauthorized expansion.

It does not determine whether a later execution is permitted under the immediately preceding BDR's narrowed authority envelope.

A future ESAL version may introduce explicit active-scope state, such as:

```text
active_authority_by_bdr
```

or:

```text
current_boundary_scope
```

That is outside the v0.1 state model.

---

## 15. Production Governance Boundary

The ESAL v0.1 Reference Oracle does not provide:

- legal sufficiency  
- compliance certification  
- policy enforcement  
- runtime access control  
- human review adjudication  
- cryptographic signature validation  
- production governance approval

It only establishes deterministic replay semantics over the supplied event corpus.

---

## 16. Conformance Boundary

An implementation conforms to ESAL v0.1 state semantics only if, for the same canonical event sequence, it produces the same:

- authority set,  
- constraints set,  
- obligations set,  
- lineage list,  
- validity value,  
- violations list,  
- state fingerprint,  
- and classification behavior.

This document does not establish independent convergence by itself. It defines the state semantics required for convergence to be tested.

---

## 17. Current Claim Boundary

Correct claim:

> ESAL v0.1 defines a deterministic reference-oracle state model with cumulative authority, union-accumulated obligations, append-only violations, and PASS/G/S/D classification behavior.

Incorrect claim:

> ESAL v0.1 enforces complete per-hop authority isolation, obligation carry-forward, multi-parent merge semantics, or production governance sufficiency.

Those stronger claims are out of scope for v0.1.

---

## 18. Review Notes

The following design decisions are intentional for ESAL v0.1:

- Authority is cumulative trace-level authority.  
- Authority inflation is detected, but per-hop narrowing is not enforced.  
- Obligations accumulate by union.  
- Child BDRs are not required to restate inherited obligations.  
- Empty authority means no declared restriction, not deny-all.  
- G-class may halt reduction or produce a replayable invalid state.  
- Multi-parent merge is out of scope.  
- Production governance semantics are out of scope.

These decisions may be revisited in future ESAL versions but should not be treated as defects in the v0.1 reference oracle.






