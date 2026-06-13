# Recomputability Class Contract v0.1

## Status

**Contract status:** Doctrine-only  
**Enforcement status:** Not yet enforced by schema, checker, test, or CI  
**Layer:** Recomputability Class  
**Version:** v0.1

This document defines the initial Fork recomputability doctrine.

It does not introduce a schema, executable checker, CI gate, verifier result format, or release lock.

## Constitutional Line

A preserved output is not necessarily a recomputable result.

## Purpose

Fork preserves evidence so later reviewers can determine what was observed, what was sealed, what still verifies, and what is not being claimed.

Preservation alone does not establish recomputability.

A hash can show that an artifact has not changed.

A manifest can show that an artifact set remains intact.

A verifier can report that packet contents still recompute against declared hashes.

But none of that, by itself, proves that the underlying result can be re-derived under governed replay conditions.

The purpose of the Recomputability Class Contract is to prevent preserved artifacts from being silently promoted into recomputable results.

## First Refusal

Fork refuses the following escalation:

```text
artifact preserved
-> artifact hash verifies
-> therefore artifact can be replayed
-> therefore artifact is recomputable
-> therefore artifact can support governed claims
```

That chain is invalid unless the artifact declares and satisfies an applicable recomputability class.

## Core Distinction

### Preservation

Preservation answers:

```text
Was this output observed or retained?
```

Preservation may support custody, integrity, and occurrence claims.

Preservation may show that an artifact existed in a recorded state and has not changed since sealing.

Preservation does not prove that the result can be re-derived.

### Recomputability

Recomputability answers:

```text
Can this result be re-derived under a declared, sealed, admissible replay class?
```

Recomputability requires more than artifact retention.

It requires a declared replay class, bounded inputs, relevant context, and admissible recomputation conditions.

Preservation and recomputability are related, but they are not equivalent.

## Recomputability Classes

Fork v0.1 defines four recomputability classes:

```text
STRONG_RECOMPUTATION
BOUNDED_RECOMPUTATION
REFERENTIAL_RECOMPUTATION
NON_RECOMPUTABLE
```

These classes describe what kind of replay, if any, an artifact may support.

In v0.1, these classes are doctrinal only. They are not yet enforced by repository tooling.

## Class 1: STRONG_RECOMPUTATION

### Meaning

`STRONG_RECOMPUTATION` means the result can be re-derived under sealed deterministic conditions.

The same sealed inputs, code, configuration, runtime, policy snapshot, dependency set, and execution context are expected to produce the same result.

### May Support

`STRONG_RECOMPUTATION` may support integrity-style replay where:

- inputs are sealed;
- code or verifier logic is identified;
- configuration is fixed;
- runtime context is bounded;
- relevant policy or rule snapshots are identified;
- dependency versions are declared;
- recomputation is deterministic or treated as deterministic under the declared replay class.

### Must Not Imply

`STRONG_RECOMPUTATION` must not imply:

- substantive correctness;
- legal correctness;
- regulatory compliance;
- policy validity;
- source completeness;
- human authorization;
- meaningful human review;
- model accuracy;
- current truth;
- that the underlying decision was appropriate.

A strongly recomputable result may still be wrong.

The class only supports the bounded claim that the same declared process and context can re-derive the same result.

`STRONG_RECOMPUTATION` may be downgraded if any required part of the sealed context is unavailable, unverifiable, or inconsistent with the declared replay class.

Required context may include inputs, code, configuration, runtime, dependency set, policy snapshot, reference material, or other execution conditions needed to re-derive the result.

A partially preserved context is not strong recomputation.

## Class 2: BOUNDED_RECOMPUTATION

### Meaning

`BOUNDED_RECOMPUTATION` means the result can be re-derived within declared tolerances, bounds, ranges, equivalence classes, or probabilistic constraints.

This class is intended for workflows where bit-for-bit identity is not the admissible replay standard.

### May Support

`BOUNDED_RECOMPUTATION` may support replay for:

- numerical workflows with declared tolerances;
- probabilistic systems with bounded variance;
- machine-learning workflows with declared acceptance criteria;
- transformations where exact identity is not expected but admissible variance is specified;
- result classes where equivalence is defined by policy or contract rather than byte identity.

### Must Not Imply

`BOUNDED_RECOMPUTATION` must not imply:

- bit-for-bit identity;
- absence of drift outside the declared bounds;
- correctness of the model or method;
- completeness of input data;
- that the tolerated variance is legally or operationally acceptable outside the declared use;
- that a future replay under different context remains comparable.

A bounded replay is only as strong as its declared bounds.

Undeclared tolerance is not bounded recomputation.

A tolerance, bound, range, or equivalence class declared only in prose may be insufficient for future enforcement.

Future profiles may require bounds to be machine-checkable before an artifact can satisfy `BOUNDED_RECOMPUTATION`.

A bounded-replay claim without an enforceable bound may be downgraded by future profiles.

## Class 3: REFERENTIAL_RECOMPUTATION

### Meaning

`REFERENTIAL_RECOMPUTATION` means replay depends on a preserved external snapshot, reference set, registry state, ledger state, policy corpus, retrieval set, or other declared reference material.

The result may be re-derived only by replaying against that preserved reference context.

### May Support

`REFERENTIAL_RECOMPUTATION` may support historical verification such as:

- whether an output was consistent with a specific policy snapshot;
- whether a result matched a preserved reference dataset;
- whether a retrieval-augmented result used a declared retrieval set;
- whether a workflow state can be replayed against a recorded registry state;
- whether an artifact was consistent with the evidence available at the time.

### Must Not Imply

`REFERENTIAL_RECOMPUTATION` must not imply:

- current truth;
- current policy validity;
- current legal compliance;
- current source completeness;
- that the reference set was correct;
- that the reference set was authoritative;
- that the reference set remains valid;
- that a live system would produce the same result today.

`REFERENTIAL_RECOMPUTATION` may support the claim that a result was consistent with a declared historical reference context.

It does not support the claim that the reference context itself was correct, complete, authoritative, current, or legally sufficient.

The replay is only as strong as the preserved reference context and the claims permitted for that context.

Referential recomputation is historical.

It says, at most, that a result may be replayable against a declared preserved reference context.

## Class 4: NON_RECOMPUTABLE

### Meaning

`NON_RECOMPUTABLE` means the artifact is preserved as an observed output, but the result cannot be independently re-derived under the available evidence and declared context.

The artifact may still be valuable evidence.

`NON_RECOMPUTABLE` artifacts may still carry substantial evidentiary weight for occurrence, preservation, custody, or review.

They are constrained only in what replay-related claims they may support.

Non-recomputable does not mean useless.

It means not admissible as recomputation.

It is not replayable evidence of result derivation.

### May Support

`NON_RECOMPUTABLE` may support claims such as:

- this output was observed;
- this file was preserved;
- this artifact was sealed;
- this record was present in the packet;
- this hash still verifies;
- this artifact has not changed since sealing.

### Must Not Imply

`NON_RECOMPUTABLE` must not imply:

- that the result can be regenerated;
- that the result can be independently replayed;
- that the result was produced by the claimed process;
- that the result is correct;
- that the result is complete;
- that the result satisfies a recomputation requirement;
- that the artifact can support claims requiring `STRONG_RECOMPUTATION`, `BOUNDED_RECOMPUTATION`, or `REFERENTIAL_RECOMPUTATION`.

A non-recomputable artifact may prove occurrence or preservation.

It must not be treated as proof of replay.

## Relationship to Claim Boundary

Claim Boundaries answer:

```text
What may this evidence establish?
```

Recomputability Classes constrain which replay-related claims an artifact may support.

A claim requiring recomputation must identify the admissible recomputability class.

A preserved artifact must not satisfy a recomputation-dependent claim merely because it exists, hashes, or appears in a packet.

### Claim Boundary Rule

An artifact must not support a claim that requires a stronger recomputability class than the artifact declares and satisfies.

Examples:

- A `NON_RECOMPUTABLE` artifact may support an occurrence claim.
- It must not support a strong replay claim.
- A `BOUNDED_RECOMPUTATION` artifact may support bounded replay within declared tolerance.
- It must not support bit-for-bit identity unless separately qualified.
- A `REFERENTIAL_RECOMPUTATION` artifact may support historical replay against a preserved reference set.
- It must not support current truth or current policy validity.

## Relationship to Definition Boundary

Definition Boundaries answer:

```text
What may this system define or classify this thing as?
```

Recomputability Classes constrain whether replay can justify a definition or equivalence.

A replay result must not silently redefine an artifact, actor, state, or workflow beyond its recomputability class.

### Definition Boundary Rule

A recomputation event must not convert an undefined or weakly supported state into a stronger definition unless the applicable Definition Boundary permits it.

Examples:

- Replaying an account event does not verify the natural person behind the account.
- Recomputing a workflow state does not prove meaningful human review.
- Replaying a classifier output does not prove that the classification is correct.
- Replaying against a historical policy snapshot does not prove current policy validity.

Recomputation may reproduce a result.

It does not automatically define what that result means.

## Relationship to Provenance Tier

Provenance Tiers answer:

```text
What kind of source or admissibility state supports this artifact?
```

Recomputability Classes answer:

```text
What kind of replay, if any, can re-derive this result?
```

These are separate dimensions.

An artifact may be documented but non-recomputable.

An artifact may be generated but strongly recomputable.

An artifact may be referentially recomputable against a preserved snapshot without being currently authoritative.

A provenance tier must not be silently upgraded because an artifact has a recomputability class.

A recomputability class must not be silently upgraded because an artifact has a provenance tier.

### Provenance Interaction Rule

Provenance and recomputability must both remain explicit.

Neither dimension may silently promote the other.

Examples:

- `DOCUMENTED` provenance does not automatically imply `STRONG_RECOMPUTATION`.
- `GENERATED` provenance does not automatically imply `NON_RECOMPUTABLE`.
- `STRONG_RECOMPUTATION` does not convert generated output into documented evidence.
- `REFERENTIAL_RECOMPUTATION` does not make a reference set authoritative.
- `NON_RECOMPUTABLE` does not make an artifact useless; it only limits replay claims.

## Required Context for Future Enforcement

This v0.1 contract does not yet define executable requirements.

Future enforcement profiles may require declarations such as:

- recomputability class;
- required recomputability class;
- replay method;
- sealed inputs;
- code or verifier identifier;
- configuration identifier;
- runtime or environment identifier;
- dependency versions;
- policy snapshot identifier;
- reference snapshot identifier;
- tolerance or bound declaration;
- non-recomputability reason;
- dependency recomputability classes.

These fields are not yet part of an enforced schema in v0.1.

They are listed only to clarify likely future enforcement surfaces.

## Reserved Failure Classes

Future enforcement may introduce failure classes such as:

```text
RECOMPUTABILITY_ESCALATION_DEFECT
RECOMPUTABILITY_DEPENDENCY_CONTAMINATION
RECOMPUTABILITY_CONTEXT_UNSEALED
RECOMPUTABILITY_TOLERANCE_UNDECLARED
RECOMPUTABILITY_REFERENCE_SNAPSHOT_MISSING
RECOMPUTABILITY_SILENT_UPGRADE_DEFECT
```

These failure classes are reserved doctrinally.

They are not yet emitted by repository tooling under this v0.1 contract.

## Candidate Future Executable Refusal

A later enforcement phase may implement the following narrow refusal:

```text
NON_RECOMPUTABLE artifacts must not satisfy gates that require STRONG_RECOMPUTATION.
```

This document does not implement that refusal.

It only defines the doctrine required before such enforcement can be responsibly added.

## What This Contract Claims

This contract claims only that:

1. Preservation and recomputability are distinct.

2. A preserved output is not necessarily a recomputable result.

3. Recomputability must be declared by class before replay-related claims can be evaluated.

4. Four doctrinal recomputability classes are defined for future use:

   - `STRONG_RECOMPUTATION`
   - `BOUNDED_RECOMPUTATION`
   - `REFERENTIAL_RECOMPUTATION`
   - `NON_RECOMPUTABLE`

5. Each class has defined support limits and non-implications.

6. Recomputability Classes interact with Claim Boundary, Definition Boundary, and Provenance Tier without replacing any of them.

## What This Contract Does Not Claim

This contract does not claim:

1. That recomputability is currently enforced by code.

2. That a recomputability schema exists.

3. That a recomputability checker exists.

4. That CI enforces recomputability classes.

5. That any artifact in the repository currently satisfies a recomputability class.

6. That all replay contexts can be captured.

7. That all generated outputs are non-recomputable.

8. That all documented artifacts are recomputable.

9. That bit-for-bit replay proves correctness.

10. That bounded replay proves model accuracy.

11. That referential replay proves current truth.

12. That non-recomputable artifacts lack evidentiary value.

13. That recomputation proves legal admissibility.

14. That recomputation proves regulatory compliance.

15. That recomputation proves source completeness.

16. That recomputation proves meaningful human review.

17. That recomputation proves identity, authority, or authorization.

18. That recomputation resolves all claim, definition, or provenance boundaries.

## Boundary Stack Position

The current Fork boundary stack is:

```text
Claim Boundary:
Prevents evidence from claiming too much.

Definition Boundary:
Prevents systems from classifying too much.

Provenance Tier:
Prevents lower-admissibility artifacts from satisfying higher evidentiary requirements.

Recomputability Class:
Prevents preserved artifacts from being treated as replayable results without a declared and satisfied replay class.
```

Together, these layers provide semantic non-escalation guarantees.

No artifact may silently escalate meaning beyond the weakest admissible evidence, definition, provenance, and recomputability state that supports it.

## Summary

A preserved output may be evidence.

A verified hash may prove integrity.

A manifest may prove artifact-set consistency.

But none of those alone prove recomputability.

Fork must therefore distinguish preserved artifacts from recomputable results.

The v0.1 constitutional line is:

**A preserved output is not necessarily a recomputable result.**
