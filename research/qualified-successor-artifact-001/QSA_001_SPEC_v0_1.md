# QUALIFIED-SUCCESSOR-ARTIFACT-001 (QSA-001) v0.1

Status: CONCEPTUAL_ARCHITECTURE_FROZEN_FOR_V0_1

## 1. Kernel

QSA-001 defines an identifiable artifact whose canonical state may evolve only through qualified, attributed, inspected, authorized, and recomputably accounted successor events.

```text
IDENTITY != STASIS
IDENTITY = ACCOUNTABLE_CONTINUITY

CHANGE_IS_PERMITTED
UNACCOUNTED_CHANGE_IS_NOT
```

QSA-001 is not a blockchain, consensus network, token system, or truth oracle. Canonicality is produced by an explicit adoption event under a declared policy, not by longest-chain, proof-of-work, proof-of-stake, or network majority.

## 2. Architectural layers

```text
L0 RECOMPUTABLE_EVIDENCE
   deterministic representation, hashes, signatures, schemas,
   environment capture, receipts, reproducible verification

L1 QSA
   qualification, proposal, inspection, observation, adoption,
   marks, non-adoption, successor accounting

L2 FORK
   standing, authority relations, attribution, non-inheritance,
   temporal scope, bounded interpretation

L3 DOMAIN_OBJECT
   specification, plan, protocol, charter, evidence package,
   policy, or another governed artifact
```

QSA uses Recomputable Evidence to govern artifact evolution. QSA does not create semantic truth, universal authority, legitimacy, compliance, or empirical validity.

## 3. Logical artifact

A QSA is one logical artifact with two inseparable planes:

```text
QSA
=
CURRENT_CANONICAL_STATE
+
APPEND_ONLY_SUCCESSOR_HISTORY
```

The current state may evolve. Historical canonical states and preserved events may not be silently rewritten.

## 4. Genesis

Every QSA history begins at an explicit immutable genesis object.

```text
QSA_GENESIS = DECLARED_ROOT_OF_THIS_QSA_HISTORY
GENESIS != UNIVERSALLY_LEGITIMATE
```

Genesis MUST bind the artifact identifier, genesis state hash, genesis constitution hash, initial acceptance-authority policy, initial qualification policy, initial inspection policy, trust roots, creation event, and genesis signatures.

A genesis signature establishes only signature verification under the declared public key and integrity of the signed payload.

```text
SIGNATURE_VALID
=
SIGNED_PAYLOAD_UNALTERED
+
SIGNATURE_VERIFIES_UNDER_DECLARED_PUBLIC_KEY

SIGNATURE_VALID != EXTERNAL_IDENTITY_ESTABLISHED
KEY_ID != ACTOR_IDENTITY
KEY_AUTHORIZED_BY_POLICY != KEY_HOLDER_UNIVERSALLY_AUTHORIZED

ACTOR_BINDING = SEPARATE_EVIDENCE_RELATION
AUTHORITY_BINDING = SEPARATE_POLICY_RELATION
```

## 5. Canonical state continuity

Each implemented canonical state MUST identify its direct canonical parent, except the genesis state.

```text
STATE_N
  state_hash = HN

STATE_N_PLUS_1
  parent_state_hash = HN
  state_hash = HN1
```

Cryptographic descent does not create semantic inheritance.

```text
CHAIN_CONTINUITY != SEMANTIC_INHERITANCE
CONTENT_CONTINUITY != AUTHORITY_CONTINUITY
CONTENT_CONTINUITY != STANDING_CONTINUITY
```

A successor event MAY separately declare content, schema, authority, standing, and semantic-continuity relations. No standing inherits solely from adjacency or descent.

## 6. Roles

QSA-001 distinguishes:

- BUILDER: creates a proposal.
- QUALIFICATION_ISSUER: establishes bounded eligibility for a change class.
- INSPECTOR: evaluates a proposal against declared criteria.
- ACCEPTANCE_AUTHORITY: authorizes canonical adoption.

Role colocation is not automatically invalid, but MUST be explicit and policy-evaluated.

```text
ROLE_COLOCATION
=
EXPLICITLY_DECLARED
+
POLICY_EVALUATED
+
PRESERVED_IN_RECEIPT
```

## 7. Qualification

Qualification is capability-specific and temporal.

```text
QUALIFIED_FOR_CHANGE_CLASS_X != QUALIFIED_FOR_ALL_CHANGES
QUALIFIED_AT_TIME_T != QUALIFIED_AT_TIME_T_PLUS_1
QUALIFICATION != ACCEPTANCE_AUTHORITY
```

A qualification receipt attests only that a builder satisfied a named qualification policy for a named change class during a named validity interval.

The workflow MUST evaluate qualification at submission, inspection, and adoption using a declared status vocabulary that includes at least VALID, EXPIRED, REVOKED, SUSPENDED, UNVERIFIABLE, NOT_APPLICABLE, and UNKNOWN.

```text
VALID_ONCE != VALID_FOREVER
```

The v0.1 default rule is:

```text
ADOPTION_REQUIRES QUALIFICATION_VALID_AT_ADOPTION
```

A constitution MAY declare stricter requirements for protected-operational or constitutional change classes.

## 8. Proposal and proposal mark

A proposal is immutable after submission and MUST bind:

- proposal id;
- artifact id;
- exact parent-state hash;
- builder key id;
- change class;
- qualification receipt;
- intended transformation;
- proposed patch or payload commitment;
- expected effect;
- builder proposal mark.

```text
PROPOSAL != CANONICAL_MUTATION
PROPOSAL_PARENT_HASH = CANONICAL_STATE_HASH_AT_SUBMISSION
```

The proposal mark means only:

```text
THIS_DECLARED_KEY_SUBMITTED_THIS_PROPOSAL_PAYLOAD
```

It does not create a build mark.

```text
PROPOSAL_MARK != BUILD_MARK
VALID_PROPOSAL != ACCEPTED_PROPOSAL
VALID_PROPOSAL != CURRENTLY_ADOPTABLE_PROPOSAL
```

## 9. Inspection

Inspection is not approval. It MUST evaluate declared criteria such as qualification validity, parent binding, payload integrity, proposed-successor recomputation, schema validity, change-class impact, and protected-invariant impact.

```text
TECHNICALLY_VALID != AUTHORIZED_FOR_IMPLEMENTATION
AUTHORIZED_FOR_IMPLEMENTATION != SEMANTICALLY_TRUE
```

Material observations are independently preservable and do not mutate canonical state by themselves.

## 10. Change classes and route escalation

QSA-001 v0.1 defines at least:

- EDITORIAL
- STRUCTURAL
- PROTECTED_OPERATIONAL
- CONSTITUTIONAL

The builder-declared class is a claim subject to inspection.

```text
DECLARED_CHANGE_CLASS != VERIFIED_CHANGE_CLASS
```

If observed impact requires a higher route, inspection MUST emit a route-escalation finding and direct adoption under the lower route MUST fail.

```text
CHANGE_CLASS_MISMATCH
ELEVATED_ROUTE_REQUIRED
PROTECTED_INVARIANT_IMPACT
CONSTITUTIONAL_ROUTE_REQUIRED
```

## 11. Protected invariants

QSA-001 v0.1 freezes these protected invariants:

```text
I1 HISTORICAL_STATE_IMMUTABILITY
I2 PROPOSAL_DOES_NOT_EQUAL_ADOPTION
I3 QUALIFICATION_DOES_NOT_EQUAL_ACCEPTANCE_AUTHORITY
I4 EVERY_IMPLEMENTED_STATE_HAS_DECLARED_PARENT_STATE
I5 EVERY_IMPLEMENTED_STATE_BINDS_TO_PROPOSAL_AND_INSPECTION
I6 FAILURE_AND_NON_ADOPTION_ARE_PRESERVABLE_OUTCOMES
I7 CRYPTOGRAPHIC_INTEGRITY_DOES_NOT_EQUAL_SEMANTIC_TRUTH
I8 STANDING_DOES_NOT_INHERIT_WITHOUT_EXPLICIT_BRIDGE
I9 SUCCESSOR_CLAIMS_MUST_BE_RECOMPUTABLY_ACCOUNTED_FOR
```

A change to these rules is a constitutional successor event, not an ordinary mutation.

## 12. Proposal outcomes

QSA-001 v0.1 defines four dispositions.

### P0 — METADATA_ONLY

No canonical change and no material observation. A cryptographic commitment to the submitted proposal MUST remain. Full proposal payload retention is policy-dependent.

```text
PAYLOAD_NOT_RETAINED != PROPOSAL_NEVER_EXISTED
```

### P1 — OBSERVATION_PRESERVED

No canonical change. Proposal metadata plus material observation and inspection receipt are preserved.

### P2 — SUCCESSOR_IMPLEMENTED

Canonical state changes. Proposal, qualification, inspection, adoption, accepted transformation, successor state, and build mark are preserved.

### P3 — REJECTED_OR_INVALIDATED

No canonical change. The failed criterion, rejection basis, inspection evidence, and disposition are preserved.

## 13. Adoption and canonical ordering

A single-chain QSA has one explicitly adopted direct successor from a current canonical parent.

```text
CANONICAL_SUCCESSOR
=
SUCCESSOR_DECLARED_BY_A_VALID_ADOPTION_EVENT
AGAINST_THE_CURRENT_CANONICAL_PARENT_STATE
```

If another valid proposal refers to the former parent after adoption, it becomes stale for direct adoption and MUST be rebased, superseded, withdrawn, preserved-not-adopted, or rejected.

```text
VALID_PROPOSAL != CURRENTLY_ADOPTABLE_PROPOSAL
TECHNICALLY_ACCEPTABLE != CANONICALLY_ADOPTED
```

## 14. Build mark

Only P2 creates a build mark on the canonical successor chain.

The build mark MUST bind at least:

```text
BUILDER_KEY_ID
ARTIFACT_ID
PARENT_STATE_HASH
PROPOSAL_HASH
QUALIFICATION_RECEIPT_HASH
INSPECTION_RECEIPT_HASH
ADOPTION_RECEIPT_HASH
SUCCESSOR_STATE_HASH
TIME
SIGNATURE
```

The build mark establishes an attributable, integrity-protected relation among those objects. It does not establish that the change was wise, true, compliant, legitimate, or externally authorized beyond the recorded policy relation.

## 15. Canonical serialization and cryptographic domain separation

QSA-001 v0.1 defines `QSA-CANONICAL-JSON-001` for protocol objects:

```text
ENCODING = UTF-8
BYTE_ORDER_MARK = PROHIBITED
OBJECT_KEY_ORDER = LEXICOGRAPHIC_BY_UNICODE_CODE_POINT
WHITESPACE = NONE_OUTSIDE_JSON_STRING_VALUES
NUMBER_FORM = SIGNED_64_BIT_INTEGER_ONLY
FLOATING_POINT_NUMBERS = PROHIBITED
DUPLICATE_OBJECT_KEYS = PROHIBITED
STRING_NORMALIZATION = NO_AMBIENT_NORMALIZATION
DATE_TIME = RFC_3339_UTC_WITH_Z_SUFFIX
HASH_ALGORITHM = SHA-256
SIGNATURE_ALGORITHM = Ed25519
```

Signed objects MUST use a type-specific domain separator:

```text
QSA:GENESIS:v1
QSA:STATE:v1
QSA:PROPOSAL:v1
QSA:PROPOSAL_MARK:v1
QSA:QUALIFICATION:v1
QSA:INSPECTION:v1
QSA:OBSERVATION:v1
QSA:ADOPTION:v1
QSA:BUILD_MARK:v1
QSA:REVOCATION:v1
QSA:VERIFICATION_RECEIPT:v1
```

Signable bytes are:

```text
UTF8(DOMAIN_SEPARATOR + "\n" + CANONICAL_SERIALIZED_PAYLOAD)
```

A signature valid for one domain MUST NOT be treated as a signature over another domain.

## 16. Verification contract

The reference verifier MUST mechanically evaluate at least:

```text
GENESIS_BINDING
CURRENT_STATE_RECOMPUTATION
STATE_PARENT_BINDING
SCHEMA_VALIDATION
CONTENT_HASHES
SIGNATURES
PROPOSAL_MARK_BINDING
QUALIFICATION_STATUS_AT_SUBMISSION
QUALIFICATION_STATUS_AT_INSPECTION
QUALIFICATION_STATUS_AT_ADOPTION
INSPECTION_BINDING
CHANGE_CLASS_ROUTE
ADOPTION_ORDERING
BUILD_MARK_BINDING
PROTECTED_INVARIANTS
```

It MUST also state what it does not evaluate:

```text
SEMANTIC_TRUTH = NOT_EVALUATED
MORAL_LEGITIMACY = NOT_EVALUATED
POLICY_WISDOM = NOT_EVALUATED
UNIVERSAL_AUTHORITY = NOT_ESTABLISHED
EMPIRICAL_HYPOTHESIS_STATUS = OUT_OF_SCOPE
```

## 17. Bootstrap boundary

QSA-001 v0.1 does not claim to have governed its own pre-QSA creation.

```text
PRE_QSA_SPECIFICATION
+
EXTERNAL_REFERENCE_IMPLEMENTATION
+
DECLARED_GENESIS
→ QSA_BOOTSTRAP_EVENT
→ FIRST_QSA_GOVERNED_SUCCESSOR
```

Pre-bootstrap material remains identifiable as historical input. A bootstrap event MUST NOT retroactively represent pre-QSA history as QSA-governed history.

## 18. v0.1 reference implementation boundary

The first reference package MUST demonstrate:

```text
GENESIS
→ QUALIFIED_BUILDER
→ P0_METADATA_ONLY
→ P1_OBSERVATION_PRESERVED
→ P2_SUCCESSOR_IMPLEMENTED
→ STATE_001
→ P3_ROUTE_INVALID_FOR_ADOPTION
→ DETERMINISTIC_VERIFICATION_RECEIPT
```

The P3 fixture MUST demonstrate a declared lower change class whose inspected impact requires a constitutional route, preserving rejection without canonical mutation.

## 19. Explicitly deferred from v0.1

The following are outside the v0.1 conceptual freeze:

- multisignature or quorum governance;
- key rotation and recovery;
- hardware-backed keys;
- remote attestation;
- encrypted proposal payloads;
- selective disclosure beyond hash commitment;
- distributed replication;
- multi-branch canonicality;
- cross-QSA composition;
- legal-identity resolution;
- institutional trust federation;
- zero-knowledge proofs.

## 20. Freeze standing

This document freezes the QSA-001 v0.1 conceptual architecture only.

```text
CONCEPTUAL_ARCHITECTURE_FROZEN != REFERENCE_IMPLEMENTATION_VALIDATED
REFERENCE_IMPLEMENTATION_VALIDATED != PRODUCTION_READY
SIGNATURE_VALID != SEMANTIC_TRUTH
QSA_CHAIN_VALID != UNIVERSAL_AUTHORITY
```
