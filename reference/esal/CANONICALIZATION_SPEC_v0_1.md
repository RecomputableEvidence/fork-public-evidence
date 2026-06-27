# ESAL v0.1 Canonicalization Specification

**Project:** Fork — Recomputable Evidence for AI-Assisted Workflows  
**Artifact:** ESAL v0.1 Canonicalization Specification  
**Status:** Reference-oracle specification  
**Scope:** `reference/esal/canonicalization.py`  
**Applies to:** ESAL v0.1 Reference Oracle  
**Branch:** `boundary-delta-record-v0.1`  
**Repair baseline:** `41759ba`

---

## 1. Purpose

This document defines the canonicalization behavior used by the ESAL v0.1 Reference Oracle.

Canonicalization is the function:

```text
C(E) -> E*
```

where:

- \(E\) is an unordered or differently represented event log.  
- \(E^*\) is the normalized, deterministically ordered canonical event sequence.

The purpose of canonicalization is to ensure that independent implementations processing the same event log can converge on the same canonical event sequence before reduction:

```text
F(S₀, E*)
```

This document describes the behavior implemented by the reference oracle. It is not a general-purpose production canonical JSON standard.

---

## 2. Canonical Event Contract

Each input event MUST be normalized into the following canonical event object before ordering:

```json
{
  "event_id": "<string>",
  "event_type": "BDR_CREATED | EXECUTION",
  "timestamp": 123,
  "boundary_id": "<string>",
  "body": {}
}
```

- The event envelope contains replay-routing and ordering fields.  
- The event body contains governance payload.

Governance payload MUST be consumed from:

- `event["body"]`

Governance payload MUST NOT be consumed from event top-level fields after normalization.

This separation is required to prevent the prior empty-state-collapse defect in which canonicalization nested governance payloads while reduction read only top-level fields.

---

## 3. Required Canonical Fields

A canonical event MUST contain:

| Field       | Type   | Description                                   |
|------------|--------|-----------------------------------------------|
| `event_id` | string | Stable event identifier                       |
| `event_type` | string | Canonical event type                         |
| `timestamp` | integer | Deterministic ordering timestamp             |
| `boundary_id` | string | Boundary identifier or deterministic surrogate |
| `body`     | object | Governance payload                            |

Missing required fields that cannot be deterministically inferred MUST produce `StructuralError` and classify as **S**.

---

## 4. Event Type Normalization

The reference oracle recognizes the following event type aliases:

| Input value | Canonical value |
|------------|-----------------|
| `BDR`      | `BDR_CREATED`    |
| `BDR_CREATED` | `BDR_CREATED` |
| `EXECUTION` | `EXECUTION`    |

Unknown event types MUST produce `StructuralError` and classify as **S**.

The canonical event type priority used for sorting is:

| Canonical event type | Priority |
|----------------------|----------|
| `BDR_CREATED`        | 0        |
| `EXECUTION`          | 1        |
| unknown fallback     | 99       |

Unknown event types should normally be rejected before sorting. The fallback priority exists only as a defensive implementation guard.

---

## 5. Event Body Normalization

The canonical body is selected as follows:

1. If the input event contains `body` and it is an object, use a shallow copy of `body`.  
2. Else, if the input event contains `payload` and it is an object, use a shallow copy of `payload`.  
3. Else, construct `body` from all non-envelope fields.

The following are **envelope fields** and are not copied into `body` under fallback construction:

- `event_id`  
- `id`  
- `event_type`  
- `type`  
- `timestamp`  
- `boundary_id`  
- `boundary`  
- `payload`  
- `body`

All other input fields are treated as governance payload and copied into `body`.

If `body` or `payload` exists but is not an object, canonicalization MUST raise `StructuralError` and classify as **S**.

---

## 6. Boundary ID Normalization

A canonical event MUST contain `boundary_id`.

The reference oracle determines `boundary_id` in the following order.

### 6.1 Explicit Boundary Fields

Use the first non-empty value from:

- `event["boundary_id"]`  
- `event["boundary"]`  
- `body["boundary_id"]`  
- `body["boundary"]`  
- `body["boundary_ref"]`  
- `body["boundary_reference"]`

### 6.2 Boundary Pair Inference

If no explicit boundary field exists, infer the boundary from the first available left/right pair:

- `source_boundary` → `target_boundary`  
- `from_boundary` → `to_boundary`  
- `source_context` → `target_context`  
- `from_context` → `to_context`  
- `source_system` → `target_system`  
- `from_system` → `to_system`  
- `source` → `target`  
- `from` → `to`

The inferred value is:

```text
<left>-><right>
```

### 6.3 BDR-Based Boundary Surrogate

If no explicit or pair-inferred boundary exists, use:

```text
bdr:<bdr_id>
```

where `bdr_id` is taken from:

- `body["bdr_id"]`  
- `body["governed_by_bdr_id"]`

### 6.4 Event-Based Boundary Surrogate

If no BDR identifier is available:

- For `BDR_CREATED`, use:

  ```text
  bdr-event:<event_id>
  ```

- For `EXECUTION`, use:

  ```text
  execution-event:<event_id>
  ```

This deterministic surrogate prevents otherwise valid legacy fixtures from failing solely due to missing boundary envelope data.

---

## 7. Timestamp Normalization

The input timestamp MUST be present.

The reference oracle converts timestamp using integer conversion:

```python
int(event["timestamp"])
```

If conversion fails, canonicalization MUST raise `StructuralError` and classify as **S**.

The reference oracle does not interpret wall-clock time, time zones, leap seconds, or clock synchronization. The timestamp is used only as a deterministic ordering key.

---

## 8. Canonical JSON Encoding

The reference oracle encodes JSON for digest purposes using:

```python
json.dumps(
    value,
    sort_keys=True,
    separators=(",", ":"),
    ensure_ascii=False,
)
```

This means:

- Object keys are sorted.  
- Whitespace is removed.  
- UTF-8 characters are emitted directly where valid JSON permits.  
- Array order is preserved.  
- No semantic array sorting is performed by canonicalization.

Important v0.1 limitation:

- The reference oracle does **not** sort authority, constraints, obligations, or other array-valued fields during canonicalization.  
- Set-like normalization occurs later in the reducer and fingerprint layers where applicable.

Independent implementations MUST match this behavior for ESAL v0.1 reference-oracle convergence.

---

## 9. Body Digest

The body digest is:

```text
SHA-256(canonical_json(event["body"]))
```

represented as lowercase hexadecimal.

The body digest is used as the final tie-breaker in canonical event ordering.

---

## 10. Canonical Event Ordering

After normalization, canonical events are sorted by this comparator, applied left-to-right:

1. `timestamp` ascending  
2. `event_type` priority ascending  
3. `event_id` ascending  
4. `boundary_id` ascending  
5. SHA-256 digest of canonical event body ascending

In Python reference form:

```python
(
    event["timestamp"],
    event_priority.get(event["event_type"], 99),
    event["event_id"],
    event["boundary_id"],
    payload_digest(event["body"]),
)
```

where:

```python
event_priority = {
    "BDR_CREATED": 0,
    "EXECUTION": 1,
}
```

This comparator is the ESAL v0.1 reference-oracle ordering rule.

Independent implementations MUST use the same comparator to reproduce reference fingerprints.

---

## 11. Duplicate Event ID Handling

The reference oracle maintains a mapping of observed event IDs during canonicalization.

- If two events share the same `event_id` and their **normalized canonical event objects differ**, canonicalization MUST raise `DeterminismError` and classify the trace as **D**.  
- If two events share the same `event_id` and their **normalized canonical event objects are identical**, the reference oracle does **not** raise `DeterminismError`.

Important v0.1 behavior:

- Identical duplicate events are **not** deduplicated by the current reference oracle canonicalization step. They remain in the canonical event sequence.  
- Future ESAL versions may specify idempotent duplicate elimination, but ESAL v0.1 reference-oracle convergence requires matching the current behavior.

---

## 12. Determinism Failure

A determinism failure occurs when canonicalization cannot construct one stable canonical event sequence from the supplied log.

The canonical ESAL v0.1 determinism failure currently covered by the reference corpus is:

- Duplicate `event_id` with differing normalized event content.

Expected classification:

- **D**

Expected exception type:

- `DeterminismError`

Expected error code:

- `EVENT_ID_CONFLICT`

---

## 13. Relationship to Validation

The replay pipeline is:

```text
raw JSONL
  ↓
validate event shape
  ↓
canonicalize C(E)
  ↓
validate lineage
  ↓
reduce F(S₀, E*)
  ↓
fingerprint H(S)
  ↓
classify PASS/G/S/D
```

- Shape validation occurs **before** canonicalization.  
- Lineage validation occurs **after** canonicalization.

This order is intentional. It allows canonicalization to establish deterministic replay order before parent/child lineage checks are applied.

---

## 14. Relationship to Reduction

Canonicalization does **not** decide governance validity.

- Canonicalization produces a deterministic event sequence.  
- Governance semantics are enforced during reduction.

Examples:

- Authority inflation is detected during reduction and classified as **G**.  
- Constraint failure is represented during reduction and classified as **G**.  
- Broken lineage is detected during lineage validation and classified as **S**.  
- Duplicate event ID conflict is detected during canonicalization and classified as **D**.

---

## 15. Relationship to Fingerprinting

The state fingerprint is **not** computed from raw events.

The state fingerprint is computed after:

```text
canonicalization -> validation -> reduction
```

The canonical event sequence hash and state fingerprint are separate commitments:

| Commitment                    | Meaning                                 |
|------------------------------|-----------------------------------------|
| canonical event sequence hash | Commitment to normalized ordered events |
| state fingerprint            | Commitment to reduced ESAL state        |

A divergence in either value may indicate:

- Implementation bug  
- Corpus mutation  
- Platform-specific determinism issue  
- Under-specified ESAL semantic

---

## 16. Reference Oracle Closure

Canonicalization MUST NOT depend on:

- Network calls  
- External evidence retrieval  
- Current time  
- Environment variables  
- Local machine state  
- Runtime policy injection  
- Human review  
- Distributed consensus  
- Cryptographic identity infrastructure

The canonicalizer operates only over supplied event objects and deterministic local code.

---

## 17. ESAL v0.1 Scope Boundary

The following are out of scope for ESAL v0.1 canonicalization:

- Multi-parent BDR merge algebra  
- Cryptographic signature validation  
- External evidence retrieval  
- Production policy interpretation  
- Human review semantics  
- Distributed consensus ordering  
- Semantic array sorting beyond the implemented JSON encoding behavior

A BDR that declares multiple parents is **not** interpreted as a deterministic merge by the ESAL v0.1 reference oracle. Until a merge algebra is specified, multi-parent merge behavior should be rejected as structurally unsupported or reserved for a future ESAL version.

---

## 18. Conformance Requirement

An implementation conforms to the ESAL v0.1 reference canonicalization surface only if, for the same input event log, it produces:

- The same normalized canonical event objects,  
- The same canonical event ordering,  
- The same duplicate-event conflict behavior,  
- The same canonical event sequence hash, and  
- The same downstream reduced state fingerprint when paired with the ESAL v0.1 reducer.

This document does not establish independent cross-implementation convergence by itself. It defines the comparator and normalization behavior needed for such convergence to be tested.

---

## 19. Current Claim Boundary

Correct claim:

> ESAL v0.1 defines a deterministic reference-oracle canonicalization behavior suitable for first-surface conformance testing.

Incorrect claim:

> ESAL v0.1 has proven independent implementation convergence.

Independent convergence requires at least one independently implemented oracle to reproduce the same canonical event sequence, reduced state, fingerprint, and taxonomy classifications over the same corpus.
