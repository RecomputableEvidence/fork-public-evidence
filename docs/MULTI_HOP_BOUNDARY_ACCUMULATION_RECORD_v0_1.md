# Multi-Hop Boundary Accumulation Record v0.1

**Short name:** MHBAR v0.1
**Artifact type:** `MULTI_HOP_BOUNDARY_ACCUMULATION_RECORD`
**Status:** Draft v0.1
**Scope:** Structural evidence record for chain-level authority accumulation
**Boundary:** Descriptive, non-adjudicative, non-runtime, non-policy-enforcing

---

## 1. Purpose

A Multi-Hop Boundary Accumulation Record records how evidence, claims, assumptions, and authority language change across a sequence of boundary crossings.

MHBAR exists to make visible a failure mode that single-boundary records only partially expose:

> authority accumulation across sequential reinterpretations.

In a single boundary crossing, preserved evidence may be over-read as authority in a new context.

In a multi-hop chain, each downstream context may preserve some evidence while introducing new assumptions, new abstractions, or new authority language. The accumulated result may appear to support a final action or permission that no individual upstream artifact established.

MHBAR records that accumulation without deciding whether the final action is safe, compliant, authorized, valid, or invalid.

---

## 2. Core distinction

MHBAR is based on the following distinction:

> Provenance tracks the persistence of the object.
> Boundary accounting tracks the mutation of the license.

A provenance record may show that an artifact, report, approval, receipt, evaluation, or manifest persisted across a chain.

MHBAR records whether the meaning or authority attributed to that artifact changed as it crossed contexts.

---

## 3. Non-transitive authority rule

Authority is non-transitive by default.

An authority basis recorded in one context does not become authority in a later context merely because:

- an artifact persisted,
- a record was preserved,
- a prior system approved a narrower action,
- an upstream evaluator produced a passing result,
- a downstream consumer received a valid object,
- a tool permission existed,
- an integration was completed,
- or a chain of records remained intact.

Authority in a later context must be separately established by an explicit claim, transition, approval, rule, mandate, or other declared basis appropriate to that later context.

MHBAR does not determine whether such a basis is sufficient. It records whether the basis was declared, whether assumptions accumulated, and what was not established by the recorded chain.

---

## 4. Example stress chain

The canonical MHBAR v0.1 stress chain is:

```text
benchmark
-> internal approval
-> vendor integration
-> agent autonomy
```

The corresponding authority mutation pattern is:

```text
technical fact
-> policy state
-> integration assurance
-> execution right
```

Example:

A benchmark emits a technical result:
“System scores 92% on task X under evaluated conditions.”

An internal approval process converts that result into a scoped policy state:
“Approved for integration based on score.”

A vendor integration consumes the approval state as an assurance:
“Because it is approved, it is safe to connect to a live database.”

An agentic system treats the integration as an execution right:
“I am connected to the database, therefore I have authority to execute writes.”

By the final hop, the original evidence may remain traceable, but the authority being exercised may no longer be established by the original evidence. MHBAR records each mutation point.

---

## 5. Relationship to existing Fork boundary records

MHBAR extends the single-boundary mapping surface.

A single-boundary record asks:
Did preserved evidence get over-read as authority across one boundary?

MHBAR asks:
Did locally bounded reinterpretations accumulate into a final authority state that no recorded upstream artifact established?

MHBAR may reference:

- boundary mapping evidence records,
- Boundary Delta Records,
- System Mapping Receipts,
- Claim Consumption Events,
- execution receipts,
- governance manifests,
- evaluation reports,
- approval records,
- vendor integration artifacts,
- agent execution traces.

Referencing those artifacts does not cause MHBAR to inherit their authority.

---

## 6. Required record-level fields

An MHBAR v0.1 record SHOULD contain the following top-level fields:

- `record_id`
- `artifact_type`
- `artifact_version`
- `chain_summary`
- `chain_subject`
- `hop_count`
- `originating_evidence_refs`
- `hops`
- `authority_lineage`
- `accumulated_assumptions`
- `non_transitive_authority_findings`
- `composition_status`
- `unresolved_accumulation_questions`
- `result_tokens`
- `non_claims`

### 6.1 record_id

A stable identifier for the multi-hop record.

Example:
`mhbar_benchmark_to_agent_database_write_authority_v0_1`

### 6.2 artifact_type

Must be:
`MULTI_HOP_BOUNDARY_ACCUMULATION_RECORD`

### 6.3 artifact_version

For this version:
`0.1`

### 6.4 chain_summary

A concise description of the chain being recorded.

Example:
Benchmark result is transformed through internal approval and vendor integration into claimed agent database write authority.

### 6.5 chain_subject

The object, system, model, workflow, or artifact whose authority chain is being inspected.

### 6.6 hop_count

The number of boundary crossings recorded.

### 6.7 originating_evidence_refs

References to the earliest evidence objects in the chain. These may include benchmark reports, evaluation records, policy approvals, receipts, manifests, or other upstream artifacts.

### 6.8 hops

An ordered list of boundary crossings. Each hop records a local reinterpretation.

### 6.9 authority_lineage

A chain-level summary of authority language introduced or relied upon at each hop. The authority lineage is descriptive only; it does not establish that authority composed across the chain.

### 6.10 accumulated_assumptions

A list of assumptions introduced across the chain. Each assumption SHOULD identify the hop where it appeared.

### 6.11 non_transitive_authority_findings

Findings that identify authority that was not established merely by earlier evidence, approval, integration, or access. These findings must remain non-adjudicative.

Permitted form:
“Operational database write authority is not established by the recorded benchmark result, internal approval, or vendor integration record alone.”

Prohibited form:
“The agent is unsafe and must be blocked.”

### 6.12 composition_status

A structural status describing whether authority composition was established by an explicit recorded basis.

Allowed values SHOULD include:

- `COMPOSITION_BASIS_DECLARED`
- `COMPOSITION_BASIS_NOT_RECORDED`
- `COMPOSITION_BASIS_UNRESOLVED`

These values are structural statuses, not judgments of sufficiency.

### 6.13 unresolved_accumulation_questions

Questions that remain open after the chain is inspected.

### 6.14 result_tokens

Machine-readable bounded result tokens.

### 6.15 non_claims

Claims expressly not made by the MHBAR record.

---

## 7. Required hop-level fields

Each hop SHOULD contain:

- `hop_index`
- `hop_id`
- `from_context`
- `to_context`
- `source_object`
- `source_claim`
- `evidence_preserved`
- `boundary_crossed`
- `downstream_assumption`
- `reinterpretation_kind`
- `authority_attempted_to_be_inherited`
- `new_authority_language_introduced`
- `non_claims_preserved`
- `unresolved_questions`
- `local_result_tokens`

### 7.1 hop_index

The hop order, starting at 1.

### 7.2 hop_id

Stable local identifier for the hop.

Example:
`hop_2_internal_approval_to_vendor_integration`

### 7.3 from_context

The context where the incoming claim, artifact, or authority language originated.

### 7.4 to_context

The context where the artifact, claim, or authority language was consumed.

### 7.5 source_object

The object crossing the boundary.

Examples:

- benchmark report
- validation summary
- internal approval record
- vendor integration ticket
- API permission record
- agent tool manifest

### 7.6 source_claim

The bounded claim actually made before the boundary crossing.

### 7.7 evidence_preserved

The evidence that remained available across the boundary.

### 7.8 boundary_crossed

The contextual shift that creates possible authority mutation.

Examples:

- evaluation environment -> product approval process
- internal approval -> third-party integration
- integration status -> agent execution context

### 7.9 downstream_assumption

The assumption introduced by the consuming context.

### 7.10 reinterpretation_kind

The kind of semantic mutation observed.

Suggested values:

- `TECHNICAL_FACT_TO_POLICY_STATE`
- `POLICY_STATE_TO_INTEGRATION_ASSURANCE`
- `INTEGRATION_ASSURANCE_TO_EXECUTION_RIGHT`
- `EVALUATION_RESULT_TO_SAFETY_GUARANTEE`
- `PERMISSION_TO_ACTION_AUTHORITY`
- `VALIDATION_TO_COMPLIANCE_STATUS`
- `RECORD_INTEGRITY_TO_TRUTH_STATUS`

### 7.11 authority_attempted_to_be_inherited

The authority the downstream context appears to treat as inherited.

### 7.12 new_authority_language_introduced

Any new authority-bearing words or statuses introduced at this hop.

Examples:

- approved
- safe to integrate
- authorized
- production-ready
- write-capable
- autonomous action allowed

### 7.13 non_claims_preserved

Claims not made by the source object and not established by the hop.

### 7.14 unresolved_questions

Questions not resolved by the local boundary record.

### 7.15 local_result_tokens

Bounded result tokens for the hop.

---

## 8. Result tokens

MHBAR v0.1 records may use the following result tokens:

- `MULTI_HOP_BOUNDARY_ACCUMULATION_RECORDED`
- `AUTHORITY_LINEAGE_RECORDED`
- `ASSUMPTION_STACK_RECORDED`
- `NON_TRANSITIVE_AUTHORITY_RECORDED`
- `COMPOSITION_BASIS_NOT_RECORDED`
- `COMPOSITION_BASIS_UNRESOLVED`
- `UNRESOLVED_AUTHORITY_ACCUMULATION_RECORDED`
- `STRUCTURAL_ACCUMULATION_RECORDED`

These tokens do not mean the chain is unsafe, safe, compliant, noncompliant, valid, invalid, approved, rejected, blocked, or permitted. They mean only that the structural boundary accumulation record was formed.

---

## 9. Prohibited result meanings

MHBAR MUST NOT produce or imply the following determinations:

- SAFE
- UNSAFE
- COMPLIANT
- NONCOMPLIANT
- APPROVED
- REJECTED
- AUTHORIZED
- UNAUTHORIZED
- VALID
- INVALID
- DEPLOYABLE
- NOT_DEPLOYABLE
- BLOCKED
- PERMITTED
- CERTIFIED
- ENDORSED

MHBAR may record that a claim, approval, or authorization was asserted by another system. MHBAR must not convert that assertion into Fork authority.

---

## 10. Structural checker posture

A future MHBAR checker should determine only whether the record is structurally complete.

A checker may confirm that:

- required fields exist,
- hop ordering is explicit,
- each hop records source claim and downstream assumption,
- authority language is identified,
- non-claims are preserved,
- accumulated assumptions are listed,
- composition status is declared,
- prohibited determinations are absent.

A checker must not determine that:

- a system is safe,
- a system is unsafe,
- a deployment is approved,
- a deployment is blocked,
- a claim is legally sufficient,
- a claim is compliant,
- a benchmark is valid,
- a vendor is trustworthy,
- an agent is authorized,
- a chain is institutionally accepted.

The preferred structural result is:

`STRUCTURAL_ACCUMULATION_RECORDED`

Not:

`PASS`

If `PASS` is used by tooling, it must be explicitly scoped to structural completeness only.

---

## 11. Non-claims

An MHBAR record does not claim:

- legal sufficiency,
- regulatory compliance,
- audit acceptance,
- deployment safety,
- model truth,
- benchmark validity,
- vendor trustworthiness,
- agent authorization,
- runtime enforcement,
- institutional approval,
- external endorsement,
- business fitness,
- claim inheritance,
- authority transfer,
- or independent external validation.

MHBAR does not decide whether a downstream assumption is permissible. MHBAR records that the assumption exists, identifies where it appeared, and preserves what was not established by the recorded chain.

---

## 12. Reviewer-supplied design pressure

The MHBAR v0.1 primitive responds to a reviewer-supplied structural test:

```text
benchmark -> internal approval -> vendor integration -> agent autonomy
```

The design pressure is that single-boundary authority discontinuity becomes chain-level authority accumulation when sequential reinterpretations are treated as composing authority.

MHBAR records that accumulation while preserving Fork's core boundary:

> Evidence may be preserved.
> Authority is not inherited.

---

## 13. Bounded claim supported by MHBAR v0.1

MHBAR v0.1 supports the following bounded claim:

> Fork can record a multi-hop chain in which evidence, assumptions, and authority language change across sequential contexts, while preserving the distinction between evidence persistence and authority transfer.

MHBAR v0.1 does not support the claim that Fork has determined whether the chain is safe, compliant, authorized, or institutionally valid.
