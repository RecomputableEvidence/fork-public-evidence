# BDR-ESAL v0.1 Normative Specification

**Document ID:** `BDR_ESAL_v0_1_NORMATIVE_SPEC`
**Status:** Draft v0.1
**Intended path:** `spec/BDR-ESAL-v0.1.md`
**Applies to:** Boundary Delta Record to Event State Artifact Loop handoff and replay semantics.
**Companion artifacts:**
- `docs/BOUNDARY_DELTA_RECORD_v0_1.md`
- `docs/BDR_ESAL_HANDOFF_CONTRACT_v0_1.md`
- `docs/ESAL_v0_1_START_HERE.md`
- `docs/ESAL_CONFORMANCE_KIT_v0_1.md`
- `reference/esal/*`
- `reports/BDR_ESAL_HANDOFF_VALIDATION_REPORT.json`
- `reports/ESAL_v0_1_CONFORMANCE_REPORT.json`

**Boundary posture:** Preservation without inheritance.

**Normative keywords:** The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are to be interpreted as conformance requirements for this specification.

---

## 1. Purpose

This specification defines the normative behavior of the BDR-ESAL v0.1 handoff surface.

BDR-ESAL connects two Fork evidence surfaces:

1. **Boundary Delta Record (BDR):** an inspectability record describing a boundary-crossing evidence transition.
2. **Event State Artifact Loop (ESAL):** a replay model that reduces ordered evidence events into a deterministic governance state fingerprint.

The purpose of BDR-ESAL v0.1 is to make boundary-crossing evidence transitions replayable without allowing the transition, replay, or fingerprint to become a claim of legal sufficiency, compliance, safety, truth, approval, runtime authorization, or external authority.

This specification is intended to be sufficiently precise for an independent implementer to construct a conforming replay implementation without reading any reference implementation source code.

---

## 2. Scope

BDR-ESAL v0.1 specifies:

- The event envelope required to carry a BDR into ESAL.
- The canonical ordering of events.
- The governance state model produced by replay.
- The reduction rules for supported event types.
- The canonical serialization requirements for state fingerprinting.
- The conformance result classes.
- The non-claims that constrain every conforming result.

BDR-ESAL v0.1 does not specify:

- Legal sufficiency.
- Regulatory compliance.
- Audit acceptance.
- Safety certification.
- Security certification.
- Runtime authorization.
- Runtime prevention.
- Truth verification.
- Institutional approval.
- External endorsement.
- Business fitness.
- Policy consequence.
- Deployment readiness.

A conforming implementation may preserve evidence about these matters only as bounded claims made by source artifacts. It MUST NOT convert preserved evidence into a broader conclusion.

---

## 3. Core invariant

The BDR-ESAL invariant is:

> The same valid event log, processed under the same BDR-ESAL specification version, MUST reduce to the same canonical governance state and the same governance state fingerprint across conforming implementations.

This invariant is structural. It does not mean the resulting governance state is legally correct, compliant, safe, approved, or externally authoritative.

---

## 4. Terminology

### 4.1 Boundary Delta Record

A **Boundary Delta Record** is a structured record describing an evidence transition across a boundary.

A BDR may describe preservation, loss, narrowing, expansion, suppression, ambiguity, or other boundary effects.

Within BDR-ESAL, a BDR is consumed only as an event input. ESAL does not reinterpret the underlying legal, compliance, safety, or factual meaning of the BDR.

### 4.2 Event

An **event** is an append-only record in an ESAL event log.

Each event has:

- A stable event identifier.
- An event type.
- A timestamp.
- A payload.
- Optional provenance metadata.
- Optional source artifact references.

### 4.3 Governance state

A **governance state** is the deterministic state produced by reducing a canonicalized event log.

The v0.1 governance state contains:

- `authority`
- `constraints`
- `obligations`
- `lineage`
- `validity`
- `violations`

### 4.4 Canonicalization

**Canonicalization** is the deterministic transformation of semantically equivalent event or state representations into a single normalized representation suitable for comparison and hashing.

### 4.5 Reduction

**Reduction** is the deterministic application of ordered events to an initial governance state.

### 4.6 Fingerprint

A **fingerprint** is a cryptographic digest of the canonical governance state serialization.

A fingerprint proves only that the same canonical state serialization was hashed. It does not prove external truth or sufficiency.

### 4.7 Conformance implementation

A **conformance implementation** is any implementation that accepts BDR-ESAL v0.1 event logs and produces the required state, fingerprint, and conformance classification according to this specification.

---

## 5. Inputs

A BDR-ESAL v0.1 implementation MUST accept an event log containing one or more newline-delimited JSON event objects or an equivalent ordered JSON array.

If both formats are supported, the implementation MUST produce equivalent results for equivalent event sequences.

### 5.1 Required event fields

Every event object MUST contain:

```json
{
  "event_id": "string",
  "event_type": "string",
  "timestamp": "RFC3339 timestamp string",
  "payload": {}
}
```

### 5.2 Optional event fields

An event object MAY contain:

```json
{
  "source_refs": [],
  "provenance": {},
  "schema_version": "string",
  "spec_version": "string"
}
```

If present, optional fields MUST be preserved in validation or diagnostic output when relevant to an error, but they MUST NOT alter reduction semantics unless explicitly specified by this document.

### 5.3 Event identifier requirements

`event_id` MUST be a non-empty string.

A conforming implementation MUST treat duplicate `event_id` values in the same event log as invalid.

Duplicate identifiers MUST produce a conformance failure.

### 5.4 Timestamp requirements

`timestamp` MUST be parseable as an RFC3339-compatible timestamp.

For canonical ordering and serialization, timestamps MUST be normalized to UTC using the canonical form:

```text
YYYY-MM-DDTHH:MM:SSZ
```

If subsecond precision is present, implementations MUST either:

1. Preserve subsecond precision consistently in canonical form, or
2. Reject the event log as unsupported by v0.1.

An implementation MUST NOT silently truncate timestamp precision.

### 5.5 Unknown top-level fields

Unknown top-level event fields MAY be preserved for diagnostics but MUST NOT alter reduction behavior.

A strict implementation MAY reject unknown top-level fields if its declared conformance profile says so.

A permissive implementation MAY accept unknown top-level fields, provided the canonical governance state and fingerprint remain unaffected by those fields.

---

## 6. Supported event types

BDR-ESAL v0.1 defines two normative event types:

```text
BDR_CREATED
EXECUTION
```

A conforming implementation MUST support these two event types.

Unknown event types MUST produce a conformance failure unless the implementation declares a strict extension profile and the extension profile is included in the event log metadata.

Extension profiles are out of scope for v0.1 baseline conformance.

---

## 7. Governance state model

A BDR-ESAL v0.1 governance state MUST contain exactly the following logical fields:

```json
{
  "authority": [],
  "constraints": [],
  "obligations": [],
  "lineage": [],
  "validity": true,
  "violations": []
}
```

### 7.1 Initial state

Replay MUST begin from the following initial state:

```json
{
  "authority": [],
  "constraints": [],
  "obligations": [],
  "lineage": [],
  "validity": true,
  "violations": []
}
```

### 7.2 Authority

`authority` is a set of capability or authority descriptors asserted by events as structurally present.

Authority entries MUST be treated as set members.

Authority entries MUST NOT be interpreted as legal or operational authorization.

Adding authority descriptors to state preserves that a descriptor was declared. It does not establish that the authority is valid outside the evidence boundary.

### 7.3 Constraints

`constraints` is a set of predicates, limitations, boundary conditions, or non-claim constraints.

Constraints are monotonic by default.

A conforming implementation MUST NOT remove a constraint unless a future version of this specification defines an explicit constraint-removal transition.

BDR-ESAL v0.1 does not define constraint removal.

### 7.4 Obligations

`obligations` is a set of obligations, follow-up duties, review requirements, or evidence-preservation requirements declared by events.

Obligations are monotonic by default.

A conforming implementation MUST NOT remove an obligation unless a future version of this specification defines an explicit obligation-removal transition.

BDR-ESAL v0.1 does not define obligation removal.

### 7.5 Lineage

`lineage` is an ordered list of BDR identifiers or source transition identifiers.

Lineage MUST preserve append order after canonical event ordering.

Lineage MUST NOT be deduplicated unless the event itself is rejected as duplicate.

### 7.6 Validity

`validity` is a boolean structural replay state.

The initial value is `true`.

Once `validity` becomes `false`, it MUST remain `false` for the rest of the replay.

This is the **validity monotonic-false rule**.

`validity=false` does not mean the underlying decision is illegal, unsafe, non-compliant, or false. It means a structural replay rule produced an invalid state under BDR-ESAL v0.1.

### 7.7 Violations

`violations` is an ordered list of violation records emitted during replay.

Violation records are observational. They preserve replay findings.

A violation record MUST NOT be interpreted as a legal finding, compliance finding, safety finding, or institutional decision.

---

## 8. Event payload semantics

### 8.1 `BDR_CREATED` payload

A `BDR_CREATED` event payload SHOULD contain:

```json
{
  "bdr_id": "string",
  "authority_delta": [],
  "constraints_delta": [],
  "obligations_delta": [],
  "validity_delta": null,
  "violation": null
}
```

A `BDR_CREATED` payload MUST contain `bdr_id`.

`bdr_id` MUST be a non-empty string.

If present:

- `authority_delta` MUST be an array.
- `constraints_delta` MUST be an array.
- `obligations_delta` MUST be an array.
- `validity_delta` MUST be either `false`, `null`, or omitted.
- `violation` MUST be either an object, `null`, or omitted.

BDR-ESAL v0.1 does not define `validity_delta=true` as a meaningful operation. If `validity_delta` is `true`, the implementation MUST reject the event.

### 8.2 `EXECUTION` payload

An `EXECUTION` event payload SHOULD contain:

```json
{
  "execution_id": "string",
  "validity_delta": null,
  "violation": null
}
```

If present:

- `execution_id` MUST be a non-empty string.
- `validity_delta` MUST be either `false`, `null`, or omitted.
- `violation` MUST be either an object, `null`, or omitted.

An `EXECUTION` event MUST NOT mutate `authority`, `constraints`, `obligations`, or `lineage`.

An `EXECUTION` event MAY set `validity` to `false` and MAY append a violation.

### 8.3 Violation record shape

A violation record SHOULD contain:

```json
{
  "violation_id": "string",
  "violation_type": "string",
  "message": "string",
  "source_event_id": "string"
}
```

A conforming implementation MAY add diagnostic fields.

The canonical state MUST include violation records after canonical normalization.

If `source_event_id` is absent, the implementation SHOULD populate it with the current event's `event_id`.

---

## 9. Canonical event ordering

A conforming implementation MUST canonicalize event order before reduction.

Events MUST be ordered by the following keys:

1. Normalized timestamp ascending.
2. Event type priority ascending.
3. `event_id` lexicographic ascending.

### 9.1 Event type priority

BDR-ESAL v0.1 defines the following event type priorities:

| Event type | Priority |
|---|---:|
| `BDR_CREATED` | 10 |
| `EXECUTION` | 20 |

Unknown event types are invalid under baseline v0.1 and therefore have no priority.

### 9.2 Equal timestamp handling

If two or more events have the same normalized timestamp, event type priority MUST determine order.

If event type priority is also equal, `event_id` lexicographic order MUST determine order.

### 9.3 Idempotence

Canonicalization MUST be idempotent.

Applying canonical event ordering to an already canonicalized event log MUST produce the same event order.

---

## 10. Reduction function

The BDR-ESAL reduction function is:

```text
F(S0, C(E)) -> S
```

Where:

- `S0` is the initial governance state.
- `E` is the input event log.
- `C(E)` is the canonicalized event sequence.
- `S` is the final governance state.

Reduction MUST process one event at a time in canonical event order.

### 10.1 Reduction for `BDR_CREATED`

For each `BDR_CREATED` event:

1. Validate required payload fields.
2. Append `payload.bdr_id` to `state.lineage`.
3. Add each item in `payload.authority_delta` to `state.authority` as a set member.
4. Add each item in `payload.constraints_delta` to `state.constraints` as a set member.
5. Add each item in `payload.obligations_delta` to `state.obligations` as a set member.
6. If `payload.validity_delta` is `false`, set `state.validity=false`.
7. If `payload.violation` is present and non-null, append the normalized violation record to `state.violations`.

A `BDR_CREATED` event MUST NOT remove authority, constraints, obligations, lineage, or violations.

### 10.2 Reduction for `EXECUTION`

For each `EXECUTION` event:

1. Validate payload fields.
2. If the payload attempts to include `authority_delta`, `constraints_delta`, `obligations_delta`, or `bdr_id`, the implementation MUST reject the event as invalid.
3. If `payload.validity_delta` is `false`, set `state.validity=false`.
4. If `payload.violation` is present and non-null, append the normalized violation record to `state.violations`.

An `EXECUTION` event MUST NOT mutate `authority`, `constraints`, `obligations`, or `lineage`.

### 10.3 Validity monotonic-false rule

If `state.validity` is already `false`, no later event may restore it to `true`.

Any event attempting to restore validity MUST be rejected as invalid.

Because v0.1 does not define `validity_delta=true`, this attempt is invalid whether it appears in `BDR_CREATED` or `EXECUTION`.

### 10.4 Constraint and obligation monotonicity

BDR-ESAL v0.1 only defines addition of constraints and obligations.

A payload field such as `constraints_remove`, `obligations_remove`, `constraint_removal`, or any semantically equivalent removal field MUST be rejected under strict conformance.

A permissive implementation MAY ignore unknown fields only if doing so cannot be interpreted as accepting constraint removal. A conformance report MUST disclose permissive unknown-field behavior.

---

## 11. Canonical state serialization

Before fingerprinting, the final governance state MUST be serialized into a canonical JSON representation.

### 11.1 Object key ordering

All JSON object keys MUST be sorted lexicographically.

### 11.2 Whitespace

Canonical JSON MUST use no insignificant whitespace.

### 11.3 Unicode

Strings MUST be serialized in a deterministic Unicode form.

A conforming implementation SHOULD normalize strings to Unicode NFC before serialization.

If it does not normalize Unicode, it MUST disclose that behavior in its conformance report.

### 11.4 Set ordering

The following fields are logical sets and MUST be sorted in canonical serialization:

- `authority`
- `constraints`
- `obligations`

Set entries MUST be deduplicated according to their canonical JSON representation.

If set entries are strings, sort lexicographically.

If set entries are objects, sort by their canonical JSON serialization.

### 11.5 Ordered list fields

The following fields are ordered lists and MUST NOT be sorted after reduction:

- `lineage`
- `violations`

`lineage` order is determined by canonical event order.

`violations` order is determined by canonical event order and violation emission order.

### 11.6 Boolean serialization

`validity` MUST serialize as a JSON boolean.

### 11.7 Required canonical state field order

Although object keys are generally sorted lexicographically, implementations SHOULD emit top-level governance state keys in this order for human readability:

```json
{
  "authority": [],
  "constraints": [],
  "lineage": [],
  "obligations": [],
  "validity": true,
  "violations": []
}
```

For fingerprinting, lexicographic key ordering is controlling.

---

## 12. Fingerprint construction

A BDR-ESAL v0.1 fingerprint MUST be computed as:

```text
SHA256(canonical_state_json_utf8)
```

Where:

- `canonical_state_json_utf8` is the UTF-8 byte sequence of the canonical JSON state serialization.
- The digest is represented as lowercase hexadecimal.

A conforming implementation MUST identify the fingerprint algorithm as:

```text
sha256
```

The fingerprint output SHOULD be represented as:

```json
{
  "fingerprint_algorithm": "sha256",
  "fingerprint": "<lowercase hex digest>"
}
```

A fingerprint does not establish truth, compliance, legal sufficiency, safety, approval, or authorization. It establishes only that the same canonical state serialization produces the same digest.

---

## 13. Output

A conforming implementation MUST emit, at minimum:

```json
{
  "spec_version": "BDR-ESAL-v0.1",
  "result": "PASS",
  "state": {},
  "fingerprint_algorithm": "sha256",
  "fingerprint": "string",
  "errors": [],
  "warnings": []
}
```

### 13.1 Result values

The top-level `result` MUST be one of:

| Result | Meaning |
|---|---|
| `PASS` | Event log was valid and replay completed |
| `FAIL` | Event log was invalid or replay could not complete |

`PASS` is a structural conformance result only.

`FAIL` is a structural conformance failure only.

### 13.2 Error records

An error record SHOULD contain:

```json
{
  "error_code": "string",
  "message": "string",
  "event_id": "string"
}
```

If an error is not attributable to a specific event, `event_id` MAY be omitted.

### 13.3 Warning records

A warning record SHOULD contain:

```json
{
  "warning_code": "string",
  "message": "string",
  "event_id": "string"
}
```

Warnings MUST NOT change `PASS` to `FAIL` unless this specification explicitly requires failure.

---

## 14. Required failure classes

A conforming implementation MUST fail for the following conditions:

| Error code | Required condition |
|---|---|
| `DUPLICATE_EVENT_ID` | Duplicate `event_id` values in the same log |
| `MISSING_EVENT_ID` | Event lacks `event_id` |
| `MISSING_EVENT_TYPE` | Event lacks `event_type` |
| `MISSING_TIMESTAMP` | Event lacks `timestamp` |
| `INVALID_TIMESTAMP` | Timestamp cannot be parsed or normalized |
| `UNKNOWN_EVENT_TYPE` | Event type is not supported by v0.1 baseline |
| `MISSING_PAYLOAD` | Event lacks `payload` |
| `MISSING_BDR_ID` | `BDR_CREATED` event lacks `payload.bdr_id` |
| `INVALID_VALIDITY_TRUE` | Event attempts to set `validity_delta=true` |
| `EXECUTION_STATE_MUTATION` | `EXECUTION` event attempts to mutate authority, constraints, obligations, or lineage |
| `UNSUPPORTED_REMOVAL` | Event attempts to remove constraints or obligations |
| `CANONICALIZATION_FAILURE` | Event or state cannot be canonicalized |
| `FINGERPRINT_FAILURE` | Fingerprint cannot be computed |

Implementations MAY define additional error codes, provided they do not contradict the required classes.

---

## 15. Conformance test vectors

A BDR-ESAL v0.1 conformance suite SHOULD include, at minimum, the following test vector classes:

| Vector ID | Purpose | Expected result |
|---|---|---|
| `C-001` | Empty or placeholder canonical log handling, if supported | Implementation-defined |
| `C-002` | Basic ordered BDR lineage replay | `PASS` |
| `C-003` | Constraint accumulation | `PASS` |
| `C-004` | Obligation accumulation | `PASS` |
| `A-001` | Constraint violation creates `validity=false` and violation record | `PASS` with invalid state |
| `A-002` | Authority inflation attempt recorded or rejected according to payload shape | `PASS` or `FAIL` as specified by fixture |
| `A-003` | Lineage truncation attempt | `FAIL` |
| `A-004` | Event reordering invariance | Same fingerprint across permuted input order |
| `M-001` | Schema-invalid event | `FAIL` |

The conformance suite MUST include at least one positive replay, one validity-false replay, one malformed event failure, and one ordering-invariance check.

---

## 16. Event reordering invariance

A conforming implementation MUST produce the same canonical state and fingerprint for any two input logs that contain the same valid events in different physical order, provided the canonical ordering keys are unchanged.

This is the event reordering invariant.

If two events have identical timestamp, event type, and event ID, they are duplicate events and MUST fail.

If two events have identical timestamp and type but different event IDs, lexicographic `event_id` order MUST determine the canonical order.

---

## 17. BDR handoff requirements

A BDR handoff into ESAL MUST preserve:

- The BDR identifier.
- The boundary transition reference.
- Any declared constraints added by the BDR.
- Any declared obligations added by the BDR.
- Any declared authority descriptors, if present.
- Any validity-affecting structural finding.
- Any violation record emitted by the BDR checker or handoff checker.

The handoff MUST NOT convert BDR inspectability into governance validity.

A BDR result of `INSPECTABLE` MAY be represented as evidence that the transition preserved inspectable structure. It MUST NOT be represented as evidence that the underlying transition was legal, compliant, safe, true, authorized, or approved.

A BDR result of `NOT_INSPECTABLE` MAY create a violation or set `validity=false` if the handoff contract specifies that behavior. It MUST NOT be represented as a legal or compliance determination by ESAL.

---

## 18. Relationship to BDR

BDR determines whether a boundary transition is inspectable under BDR rules.

ESAL replays the event consequences declared by the BDR-to-ESAL handoff.

BDR-ESAL does not require ESAL to re-run the BDR checker.

A conforming ESAL implementation MAY verify that a BDR reference exists or that a BDR checker result is attached, but baseline v0.1 conformance does not require dereferencing external BDR artifacts.

If an implementation dereferences BDR artifacts, it MUST disclose that extension behavior in its conformance report.

---

## 19. Relationship to TIS

Transition Integrity Specification concepts MAY inform BDR construction, BDR validation, or BDR-to-ESAL handoff rules.

BDR-ESAL v0.1 does not require a TIS checker.

If a TIS checker is used, its findings MUST be preserved as bounded evidence and MUST NOT become runtime authorization or external validity decisions.

---

## 20. Relationship to System Mapping Receipts

System Mapping Receipts may describe how BDR-ESAL outputs are consumed by external systems.

An SMR may record whether an external system preserved, narrowed, expanded, or left unresolved the BDR-ESAL result.

An SMR MUST NOT treat an ESAL fingerprint as external authority, legal sufficiency, compliance, safety, approval, or truth.

---

## 21. Relationship to Governance Layer Manifests

A Governance Layer Manifest may declare that a system produces or consumes BDR-ESAL artifacts.

A manifest declaration does not establish external recognition, compatibility approval, registry acceptance, or endorsement unless separately granted by an external authority.

---

## 22. Security and integrity considerations

BDR-ESAL v0.1 relies on deterministic replay and fingerprinting.

It does not by itself provide:

- Identity proofing.
- Signature verification.
- Timestamp authority.
- Transport security.
- Access control.
- Tamper-proof storage.
- Runtime blocking.
- Secrets management.

Implementations MAY add these features, but such additions are out of scope for baseline conformance.

If signatures, timestamp authorities, or transparency logs are used, they MUST be represented as separate evidence surfaces with explicit claim boundaries.

---

## 23. Privacy considerations

A BDR-ESAL event log may contain sensitive governance information.

Implementations SHOULD minimize personally identifiable information.

Implementations SHOULD preserve identifiers by stable reference when possible rather than embedding unnecessary personal data.

Redaction MUST NOT silently alter replay semantics.

If redaction changes replay semantics, the redacted artifact MUST have its own claim boundary.

---

## 24. Non-claims

A conforming BDR-ESAL v0.1 result does not establish:

- Legal admissibility.
- Legal sufficiency.
- Regulatory compliance.
- Audit acceptance.
- Safety certification.
- Security certification.
- Output truth.
- Model correctness.
- Human-review adequacy.
- Institutional approval.
- External endorsement.
- Runtime authorization.
- Runtime prevention.
- Deployment readiness.
- Host-system conformance.
- Business fitness.
- Authority transfer.
- Claim inheritance.

These non-claims are normative.

An implementation that emits a result implying any of the above from BDR-ESAL replay alone is non-conforming.

---

## 25. Conformance profiles

BDR-ESAL v0.1 defines the following baseline profile:

```text
BDR_ESAL_BASELINE_REPLAY_v0_1
```

A baseline-conforming implementation MUST support:

- `BDR_CREATED`
- `EXECUTION`
- Canonical event ordering
- Initial state construction
- State reduction
- Validity monotonic-false
- Constraint and obligation monotonicity
- Canonical state serialization
- SHA-256 state fingerprinting
- Required failure classes
- Required non-claims

An implementation MAY define additional profiles, but additional profiles MUST NOT weaken the baseline requirements while claiming baseline conformance.

---

## 26. Conformance report requirements

A BDR-ESAL conformance report SHOULD include:

```json
{
  "spec_version": "BDR-ESAL-v0.1",
  "profile": "BDR_ESAL_BASELINE_REPLAY_v0_1",
  "implementation_name": "string",
  "implementation_version": "string",
  "repository": "string",
  "commit": "string",
  "command": "string",
  "input_vectors": [],
  "result": "PASS",
  "fingerprints": {},
  "errors": [],
  "warnings": [],
  "limitations": [],
  "non_claims": []
}
```

A conformance report MUST NOT claim that conformance proves legal, compliance, safety, approval, truth, runtime, or institutional validity.

---

## 27. Independent reproduction requirements

An independent reproduction of BDR-ESAL v0.1 SHOULD satisfy all of the following:

1. Implement replay behavior from this specification rather than copying the reference implementation.
2. Use the same published conformance vectors.
3. Produce the same canonical state fingerprints for positive vectors.
4. Produce required failure classifications for negative vectors.
5. Preserve implementation provenance.
6. Preserve command, commit, environment, and tool version.
7. Preserve limitations and non-claims.

Independent reproduction does not imply endorsement.

Independent reproduction establishes only that the replay behavior was reproduced under the declared conditions.

---

## 28. Versioning

A future BDR-ESAL version MUST change the version identifier if it changes any of the following:

- Event type semantics.
- Event ordering rules.
- State model fields.
- Reduction behavior.
- Canonical serialization.
- Fingerprint construction.
- Failure classes.
- Non-claim requirements.
- Conformance profile requirements.

Editorial changes that do not alter semantics MAY be released as patch notes without changing the baseline conformance profile.

---

## 29. v0.1 determination

BDR-ESAL v0.1 defines a bounded, deterministic handoff and replay model for preserving boundary-crossing evidence consequences in a recomputable governance state.

A conforming implementation can show that a given event log reduces to a deterministic governance state and fingerprint under the declared rules.

It cannot show that the underlying decision, claim, transition, or external system action was legally sufficient, compliant, safe, true, approved, or authorized.

That boundary is intentional.

Preservation without inheritance remains controlling.

---

## Appendix A — Minimal valid event log

```json
{"event_id":"evt-001","event_type":"BDR_CREATED","timestamp":"2026-01-01T00:00:00Z","payload":{"bdr_id":"bdr-001","authority_delta":["declared-reviewer-observed"],"constraints_delta":["no-compliance-claim"],"obligations_delta":["preserve-non-claims"],"validity_delta":null,"violation":null}}
```

A conforming implementation should reduce this to a state containing:

```json
{
  "authority": ["declared-reviewer-observed"],
  "constraints": ["no-compliance-claim"],
  "lineage": ["bdr-001"],
  "obligations": ["preserve-non-claims"],
  "validity": true,
  "violations": []
}
```

The exact fingerprint depends on the canonical JSON serialization rules and MUST be stable across conforming implementations.

---

## Appendix B — Minimal validity-false event log

```json
{"event_id":"evt-001","event_type":"BDR_CREATED","timestamp":"2026-01-01T00:00:00Z","payload":{"bdr_id":"bdr-001","constraints_delta":["no-compliance-claim"],"validity_delta":false,"violation":{"violation_id":"vio-001","violation_type":"AUTHORITY_EXPANSION_RISK","message":"Downstream transition attempted to treat preserved evidence as approval.","source_event_id":"evt-001"}}}
```

A conforming implementation should reduce this to a state where:

```json
{
  "validity": false
}
```

and `violations` contains the normalized violation record.

This result does not establish legal or compliance invalidity.

---

## Appendix C — Minimal invalid execution mutation

```json
{"event_id":"evt-001","event_type":"EXECUTION","timestamp":"2026-01-01T00:00:00Z","payload":{"execution_id":"exec-001","constraints_delta":["new-constraint"]}}
```

A conforming implementation MUST reject this event with:

```text
EXECUTION_STATE_MUTATION
```

because `EXECUTION` events do not mutate constraints under BDR-ESAL v0.1.

---

## Appendix D — Implementation checklist

A baseline implementation is not ready for conformance review until it can answer yes to all of the following:

- Does it reject duplicate event IDs?
- Does it normalize timestamps deterministically?
- Does it sort events by timestamp, event type priority, and event ID?
- Does it enforce BDR_CREATED payload requirements?
- Does it prevent EXECUTION events from mutating authority, constraints, obligations, or lineage?
- Does it enforce validity monotonic-false?
- Does it enforce constraint and obligation monotonicity?
- Does it canonicalize set fields deterministically?
- Does it preserve ordered lineage and violation lists?
- Does it compute SHA-256 over canonical UTF-8 JSON?
- Does it emit bounded PASS/FAIL results?
- Does it preserve non-claims?
- Does it avoid legal, compliance, safety, truth, approval, or runtime claims?

---

## Appendix E — Reserved terms

The following terms are reserved and MUST NOT be used as BDR-ESAL result tokens in v0.1:

- `APPROVED`
- `COMPLIANT`
- `CERTIFIED`
- `SAFE`
- `VALIDATED`
- `AUTHORIZED`
- `ENDORSED`
- `LEGAL`
- `ADMISSIBLE`
- `TRUSTED`
- `CONTROL_SATISFIED`

These terms may appear only as quoted source claims, preserved non-claims, or diagnostic text that does not become a BDR-ESAL result token.
