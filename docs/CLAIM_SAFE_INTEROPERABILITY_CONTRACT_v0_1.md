# Claim-Safe Interoperability Contract v0.1

Minimum contract for exchanging artifacts across AI governance systems without silent claim inheritance.

## Status

Draft normative contract.

This document defines a minimum contract for claim-safe interoperability between adjacent AI governance systems.

It is intended to follow the architectural mapping layer defined in:

- `docs/AI_GOVERNANCE_BOUNDARY_MAPPING_PROTOCOL_v0_1.md`

This document is not a runtime enforcement proxy, legal standard, compliance certification, audit standard, or production deployment claim.

## Purpose

AI governance systems may need to exchange artifacts.

Those artifacts may include traces, logs, hashes, receipts, evidence packets, policy outputs, runtime records, review records, or verification results.

The risk is that when artifacts move between systems, claims may silently move with them.

This contract prevents that failure mode.

The purpose is to allow artifact interoperability without silent claim inheritance.

## Scope

This contract applies to systems exchanging artifacts with attached or implied claims, including:

- runtime systems;
- model invocation systems;
- evidence collectors;
- evidence packet systems;
- compliance evaluators;
- audit stores;
- legal review systems;
- risk review systems;
- policy admissibility systems;
- execution validity systems;
- external verification systems;
- boundary enforcement layers.

## Non-scope

This contract does not define:

- legal admissibility;
- compliance satisfaction;
- audit sufficiency;
- liability resolution;
- decision correctness;
- AI output truth;
- institutional authority;
- production deployment readiness;
- a runtime boundary enforcement proxy;
- a complete governance framework;
- a universal ontology for all AI systems.

This contract defines minimum interoperability discipline for claims attached to artifacts.

## Governing invariant

Claims are attached, typed, scoped, authority-bound, assurance-declared, non-transitive by default, and stripped at system boundaries unless locally re-verified.

## Core principle

Systems may exchange artifacts.

They may not silently exchange claims.

## Definitions

### Artifact

An artifact is any object, record, export, receipt, trace, log, packet, hash, manifest, policy result, model output, review record, or reference that may be exchanged between systems.

### Claim

A claim is an assertion made about an artifact, process, source, system, decision, state, authority, verification result, or workflow condition.

### Non-claim

A non-claim is an explicit statement of what a system refuses to assert.

Non-claims are part of the contract surface.

They are not marketing disclaimers.

### Unknown

An unknown is a condition, source, dependency, context, authority, fact, or evidence surface that the system did not observe, did not verify, could not access, or did not evaluate.

### Dependency

A dependency is any upstream artifact, source, model, policy, environment, authority, data set, service, or verification result required to support a claim.

### Verification

Verification means checking whether a claim is structurally and evidentially supported under its declared claim type, scope, authority, assurance level, and verification method.

### Evaluation

Evaluation means determining whether an artifact, claim, process, or decision is acceptable under policy, law, risk tolerance, business judgment, audit criteria, compliance obligations, or institutional authority.

Verification and evaluation are separate.

## Claim types

All claims MUST declare exactly one primary claim type.

Un-typed claims MUST NOT be accepted.

The allowed v0.1 claim types are:

| Claim type | Meaning |
|---|---|
| `EXECUTION` | Asserts that a a process, workflow, or runtime event occurred under a declared execution model. |
| `INTEGRITY` | Asserts that an artifact matches a declared digest, signature, manifest, Merkle root, or other integrity check. |
| `PROVENANCE` | Asserts origin, custody, source, environment, model, system, or production context. |
| `VALIDITY` | Asserts satisfaction of a specific declared rule set or validation rule. |
| `AUTHORIZATION` | Asserts permission, entitlement, role, or institutional authority to perform or approve a defined action. |
| `ADMISSIBILITY` | High-risk claim type asserting suitability for legal, evidentiary, or formal regulatory process under a declared jurisdictional basis. |

Systems MUST declare which claim types they emit.

Systems MUST declare which claim types they verify.

Systems MUST NOT invent new claim types without extending the contract or publishing a compatible extension profile.

## High-risk admissibility claims

`ADMISSIBILITY` is a high-risk claim type.

A system MUST NOT emit, consume, reattach, or rely on an `ADMISSIBILITY` claim unless the claim explicitly declares:

- asserting authority;
- jurisdictional basis;
- applicable legal or regulatory framework;
- verification method;
- scope of admissibility;
- explicit non-claims;
- unresolved unknowns;
- dependencies;
- time and context bindings.

An `ADMISSIBILITY` claim MUST NOT be inferred from integrity, provenance, execution, authorization, or validity claims.

Evidence integrity does not equal admissibility.

Runtime anchoring does not equal admissibility.

Workflow reconstruction does not equal admissibility.

## Assurance levels

Each claim MUST declare an assurance level.

Allowed v0.1 assurance levels are:

| Assurance level | Meaning |
|---|---|
| `CRYPTOGRAPHIC` | Supported by cryptographic proof, such as signatures, hashes, Merkle roots, timestamp receipts, or equivalent integrity mechanisms. |
| `DETERMINISTIC` | Supported by reproducible logic with no probabilistic or heuristic element. |
| `HEURISTIC` | Supported by probabilistic, statistical, classifier-based, model-based, or rule-of-thumb methods. |
| `ASSERTED` | Declared by a human, institution, external authority, or system without programmatic proof. |

Assurance levels describe verification support.

They do not create approval, compliance, admissibility, correctness, completeness, liability resolution, or actionability.

## Required envelope fields

Any system exchanging artifacts under this contract SHOULD wrap them in a claim envelope.

The v0.1 envelope MUST include, at minimum:

| Field | Requirement |
|---|---|
| `envelope_version` | Version of the claim envelope. |
| `artifact` | Artifact metadata, including identifier, type, and integrity reference. |
| `origin` | Origin system identifier and authority metadata. |
| `asserted_claims[]` | Claims asserted by the origin system. |
| `non_claims[]` | Explicit statements of what is not being claimed. |
| `unknowns[]` | Explicit unresolved or unevaluated conditions. |
| `dependencies[]` | Required upstream artifacts, claims, sources, models, policies, or services. |
| `transitivity` | MUST default to `NON_TRANSITIVE`. |
| `envelope_signature` | Envelope-level integrity or assertion signature when signing is supported. |

A receiving system MUST NOT treat absent fields as implied favorable evidence.

Missing non-claims do not imply a positive claim.

Missing unknowns do not imply completeness.

Missing dependencies do not imply dependency closure.

## Required claim fields

Each claim in `asserted_claims[]` MUST include:

| Field | Requirement |
|---|---|
| `claim_id` | Stable identifier for the claim. |
| `claim_type` | One v0.1 claim type. |
| `claim_statement` | Human-readable claim text. |
| `scope` | The bounded scope of the claim. |
| `asserting_authority` | Entity or authority asserting the claim. |
| `assurance_level` | One v0.1 assurance level. |
| `verification_method` | Declared method by which the claim may be checked. |
| `verifier_ref` | Reference to verifier, verifier class, schema, procedure, or external method. |
| `time_scope` | Time window or temporal context for the claim. |
| `context_binding` | Bound policy, model, environment, workflow, or source context. |
| `dependencies[]` | Claim-specific dependencies. |
| `non_claims[]` | Claim-specific non-claims. |
| `unknowns[]` | Claim-specific unknowns. |
| `transitivity` | MUST default to `NON_TRANSITIVE`. |

## Verification interface

A system MAY expose a verification interface.

If exposed, the interface SHOULD follow this semantic shape:

```text
verifyClaim(claim, artifact, context) -> TRUE | FALSE | INDETERMINATE

An HTTP implementation MAY use:
POST /verifyClaim
Request:  { claim, artifact, context }
Response: { result, reason, evidence }

The response result MUST use one of:
TRUE
FALSE
INDETERMINATE

Lowercase transport encodings MAY be used if mapped unambiguously to these states.
```

### Verification semantics

Verification is not evaluation.

A result of TRUE means only:

- The receiving system may reattach the claim within the declared claim type, scope, authority, assurance level, and verification method.

A result of TRUE does not mean the artifact is:

- approved;
- compliant;
- admissible;
- correct;
- complete;
- sufficient for action;
- legally sufficient;
- audit sufficient;
- risk accepted;
- institutionally authorized beyond the declared claim.

A result of FALSE means:

- The claim failed verification and MUST NOT be reattached.

A result of INDETERMINATE means:

- The claim was not verified as true or false under the declared method and context.

INDETERMINATE is blocking.

An indeterminate claim MUST NOT be:

- promoted to true;
- treated as a soft pass;
- reattached as verified;
- used as a dependency for downstream claims;
- treated as approval;
- treated as compliance;
- treated as admissibility;
- treated as correctness;
- treated as completeness.

### Verification is not evaluation

Systems MUST distinguish verification from evaluation.

The following equivalences are prohibited:

- verified equals approved;
- verified equals compliant;
- verified equals admissible;
- verified equals correct;
- verified equals complete;
- verified equals sufficient for action;
- verified equals legally sufficient;
- verified equals audit sufficient;
- verified equals institutionally authorized.

Any downstream approval, denial, escalation, legal interpretation, compliance conclusion, audit conclusion, risk acceptance, remediation decision, or reporting decision MUST be recorded as a separate claim, artifact, or institutional action under the appropriate authority.

## Boundary enforcement rules

At a system boundary, the receiving system MUST apply claim-safe handling.

### Rule 1: Strip by default

Incoming claims MUST be stripped, suspended, or treated as untrusted upon ingestion.

The artifact may be received.

The claims do not automatically transfer.

### Rule 2: No silent inheritance

Claims MUST NOT traverse boundaries by:

- implication;
- proximity;
- encapsulation;
- shared file structure;
- vendor trust;
- common workflow context;
- prior system reputation;
- human assumption;
- downstream convenience.

### Rule 3: Local re-verification

A receiving system MAY reattach a claim only after local verification returns TRUE under the receiving system's declared verification method, authority basis, and acceptance policy.

### Rule 4: Preserve non-claims and unknowns

A receiving system MUST preserve or explicitly restate incoming non-claims and unknowns.

A receiving system MUST NOT erase non-claims or unknowns merely because the artifact was accepted.

### Rule 5: Record verification result

The receiving system SHOULD record:

- original artifact reference;
- original claims;
- stripped claims;
- verification requests;
- verification results;
- reattached claims;
- non-claims;
- unknowns;
- dependencies;
- failure states;
- timestamp;
- receiving system identifier.

### Rule 6: No opaque claim consumption

A system MUST NOT consume a claim unless it declares:

- how the claim is verified;
- what authority supports verification;
- what assurance level applies;
- what acceptance policy applies;
- what non-claims remain;
- what unknowns remain;
- what dependencies are unresolved.

### Formal non-inheritance rule

If system S2 receives artifact A with claim C1 from system S1, then:

- C1 MUST NOT be an element of Claims(S2, A)  
  unless  
- V_S2(C1, A, context) = TRUE.

Even when V_S2(C1, A, context) = TRUE, the reattached claim remains bounded by:

- claim type;
- scope;
- asserting authority;
- assurance level;
- verification method;
- context;
- dependencies;
- non-claims;
- unknowns.

## Non-claims

A system MUST explicitly declare material non-claims.

Examples include:

- does not claim AI output correctness;
- does not claim decision correctness;
- does not claim source completeness;
- does not claim legal admissibility;
- does not claim compliance satisfaction;
- does not claim audit sufficiency;
- does not claim risk acceptance;
- does not claim remediation sufficiency;
- does not claim institutional authority;
- does not claim workflow continuation was justified;
- does not claim final action appropriateness.

Non-claims MUST travel with the artifact unless explicitly superseded by a later verified claim under declared authority.

A later verified claim MUST NOT silently erase earlier non-claims.

## Unknowns

A system MUST explicitly declare material unknowns.

Examples include:

- source completeness not evaluated;
- external dependency unavailable;
- model version not verified;
- policy version not verified;
- human review not observed;
- authority basis not observed;
- legal context not evaluated;
- downstream action not observed;
- runtime environment not verified;
- artifact dependency unresolved.

Unknowns MUST NOT be treated as resolved by omission.

## Dependencies

Claims MUST identify material dependencies.

Each dependency MUST be marked as one of:

- CLOSED: dependency is present and verified within the declared boundary;
- REFERENCED: dependency is externally referenced with an integrity or authority reference;
- UNRESOLVED: dependency is known but not verified, unavailable, inaccessible, or incomplete;
- OUT_OF_SCOPE: dependency is outside the declared boundary.

A claim MUST NOT be treated as fully verified if required dependencies are unresolved.

Unresolved dependencies SHOULD cause dependent claims to become INDETERMINATE unless the claim explicitly does not depend on them.

## Authority declaration

A system participating in claim-safe interoperability SHOULD publish an authority profile.

An authority profile SHOULD include:

- system_id;
- system owner;
- public keys or key references;
- claim types emitted;
- claim types verified;
- assurance levels supported;
- verifier references;
- authority source;
- jurisdictional basis, where applicable;
- non-authority statements;
- contact or discovery endpoint, where appropriate.

A system MUST NOT assert claims outside its declared authority profile unless the claim itself contains an explicit authority basis.

### Authority is not inherited

Institutional authority does not transfer merely because an artifact is exchanged.

Tool authority does not become legal authority.

Runtime authority does not become compliance authority.

Evidence authority does not become audit authority.

Compliance authority does not become decision correctness.

Legal authority does not become source completeness.

## Failure taxonomy

A receiving system SHOULD classify failures using a defined failure taxonomy.

Minimum v0.1 failure states:

- `VERIFICATION_FAILURE`: Signature, hash, schema, verifier, or evidence check fails. Required response: reject or quarantine the claim or artifact.
- `UNSUPPORTED_CLAIM_TYPE`: Receiver does not support the claim type. Required response: strip claim and mark unsupported.
- `AUTHORITY_MISMATCH`: Origin lacks authority for the claim type or scope. Required response: reject claim and escalate if material.
- `TEMPORAL_INVALIDITY`: Time scope expired, missing, or outside allowed context. Required response: mark claim false or indeterminate according to policy.
- `DEPENDENCY_INCONSISTENCY`: Required dependency missing, unverifiable, or contradictory. Required response: quarantine or mark dependent claim indeterminate.
- `MISSING_NON_CLAIMS`: Required non-claims absent from envelope. Required response: reject, degrade, or request corrected envelope.
- `MISSING_UNKNOWNS`: Unknowns required but absent or ambiguous. Required response: reject, degrade, or request corrected envelope.
- `TRANSITIVITY_VIOLATION`: Claim treated as inherited without local verification. Required response: reject reattached claim and log boundary violation.
- `OPAQUE_CLAIM_CONSUMPTION`: System consumes claim without method, authority, or policy declaration. Required response: reject or quarantine claim.
- `EVALUATION_CREEP`: Verification treated as approval, compliance, correctness, or admissibility. Required response: reject conclusion and require separate evaluation artifact.

Each material failure SHOULD produce an audit record containing:

- artifact_id;
- claim_id;
- origin_system_id;
- receiving_system_id;
- failure_state;
- failure_reason;
- timestamp;
- action_taken;
- non_claims_preserved;
- unknowns_preserved.

## Acceptance policy

A receiving system MUST define an acceptance policy before consuming claims.

The acceptance policy SHOULD state:

- accepted claim types;
- required assurance levels;
- accepted authorities;
- accepted verification methods;
- dependency requirements;
- handling for unknowns;
- handling for non-claims;
- handling for indeterminate results;
- escalation requirements;
- logging requirements.

No opaque claim consumption is permitted.

## Relationship to the AI Governance Boundary Mapping Protocol

The AI Governance Boundary Mapping Protocol defines how adjacent systems are described and compared.

This contract defines the minimum rules for exchanging artifacts between those systems without silently transferring claims.

The mapping protocol answers:

- Where does the system sit?
- What does it claim?
- What does it not claim?
- What artifacts does it emit?
- What artifacts does it consume?
- What authority does it have?

This contract answers:

- How may claims attach to artifacts?
- What must happen at a system boundary?
- When may a claim be reattached?
- What does verification mean?
- What must remain unknown or non-claimed?
- What must never silently transfer?

## Relationship to Fork

Fork may use this contract to describe how externally produced artifacts, receipts, traces, claims, or verification results can be referenced within an evidence boundary without inheriting unsupported claims.

Fork's role remains bounded.

Fork does not become a runtime anchoring system, compliance system, legal authority, audit function, policy authority, or execution-control plane merely because it references or preserves artifacts from those systems.

Fork may preserve:

- artifacts;
- claims;
- non-claims;
- unknowns;
- dependencies;
- verification results;
- failure states;
- evidence boundaries.

Fork does not automatically validate:

- AI output correctness;
- decision correctness;
- source completeness;
- legal admissibility;
- compliance satisfaction;
- audit sufficiency;
- risk acceptance;
- remediation sufficiency;
- reporting sufficiency;
- institutional authority.

## Future-state boundary enforcement proxy

A boundary enforcement proxy is a possible future infrastructure component.

It is not claimed by this contract.

A future boundary enforcement proxy may enforce:

- envelope validation;
- claim stripping;
- verifier dispatch;
- reattachment rules;
- authority graph checks;
- failure taxonomy actions;
- audit recording;
- non-claim and unknown preservation.

No runtime proxy capability is claimed until separately specified, implemented, tested, and verified.

## Next implementation artifacts

Future artifacts may include:

- `schemas/governance_claim_envelope_v0_1.schema.json`;
- `examples/claim_safe_interop/runtime_to_fork_vendor_review_v0_1/`;
- `tools/check_governance_claim_envelope.py`;
- `tests/test_governance_claim_envelope_v0_1.py`;
- authority profile template;
- valid, invalid, and indeterminate conformance vectors.

These future artifacts are not implied by this contract until present in the repository and independently checkable.

## Approved short-form language

- Claim-safe interoperability for AI systems.
- Systems may exchange artifacts, but they may not silently exchange claims.
- Claims are attached, typed, scoped, authority-bound, assurance-declared, non-transitive by default, and stripped at system boundaries unless locally re-verified.
- Verification is not evaluation.
- Indeterminate is blocking, not a soft pass.
- Non-claims and unknowns must travel with artifacts.

## Closing statement

AI governance systems can cooperate without collapsing into one platform.

Artifact interoperability is useful.

Claim interoperability is dangerous unless explicitly typed, scoped, authority-bound, assurance-declared, locally verified, and non-transitive by default.

This contract defines the minimum discipline required to exchange artifacts without silently exchanging claims.