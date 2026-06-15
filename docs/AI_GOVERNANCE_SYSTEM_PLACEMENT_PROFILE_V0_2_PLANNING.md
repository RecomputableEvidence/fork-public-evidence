# AI Governance System Placement Profile v0.2 Planning

Status: `PLANNING_ONLY`

Version: `0.2-planning`

Applies to lineage:

* `ai-governance-system-placement-profile-v0.1`
* `ai-governance-system-placement-profile-schema-fixtures-v0.1`
* `ai-governance-system-placement-profile-checker-v0.1`
* `ai-governance-system-placement-profile-checker-hardening-v0.1.1`

## 1. Purpose

This document defines candidate planning scope for a future v0.2 evolution of the AI Governance System Placement Profile.

It is a planning artifact only.

It is not a schema.

It is not a checker.

It is not a runtime feature.

It does not authorize implementation.

It does not expand Fork’s authority beyond structural and boundary validation.

The purpose of v0.2 planning is to identify possible next directions while preserving the stabilized v0.1.1 boundary:

> Fork validates structural and boundary consistency of placement-profile records. Fork does not validate semantic truth, legal sufficiency, compliance sufficiency, audit sufficiency, model safety, runtime behavior, external artifact existence, cross-record graph validity, or institutional authority.

## 2. Current Baseline

The v0.1.1 Placement Profile checker line currently provides a hardened single-record structural and boundary validator.

The current line includes:

* placement-profile doctrine
* minimal schema and fixtures
* executable checker
* parser-boundary hardening
* Unicode-aware lexical restricted-claim hardening
* explicit exit-code contract:

  * `PASS = 0`
  * `FAIL = 1`
  * `INDETERMINATE = 2`
* performance smoke coverage
* overclaim-language regression coverage
* normalized-output comparison guidance
* schema-path edge-case handling
* committed raw and normalized fixture outputs
* preserved regression compatibility with prior Placement Profile and AI Governance Mapping Record checker lines

The current checker remains single-record only.

It validates local consistency inside one placement-profile record.

It does not resolve external files.

It does not compile multiple profiles.

It does not verify external artifacts.

It does not evaluate whether a declared evidence item actually proves a claim.

It does not determine whether a governance system is safe, compliant, lawful, approved, admissible, sufficient, or institutionally authorized.

## 3. v0.2 Planning Premise

v0.2 should not be treated as a general expansion phase.

v0.2 should only be considered if it preserves the core Placement Profile doctrine:

> Governance claims are non-transitive unless explicitly declared, bounded, evidenced, and handed off.

The main question for v0.2 is:

> Can Fork add controlled structural expressiveness around placement profiles without turning the checker into a policy engine, compliance oracle, runtime controller, legal authority, audit substitute, model evaluator, external artifact resolver, or institution of approval?

Any v0.2 feature must satisfy the following admission test:

1. It strengthens structural clarity.
2. It preserves non-transitive claim boundaries.
3. It produces deterministic, reviewable outputs.
4. It does not evaluate semantic truth.
5. It does not make legal, compliance, audit, safety, runtime, or institutional authority claims.
6. It does not create hidden dependence on live systems.
7. It can be explained as evidence-boundary infrastructure.

## 4. Candidate v0.2 Modules

The following modules are planning candidates only. Inclusion in this document does not mean they are accepted build scope.

Each candidate must be separately reviewed before implementation.

### 4.1 Optional Schema Extensions

Candidate status: `CANDIDATE`

Purpose:

Add optional fields that make placement profiles more expressive without increasing Fork’s authority.

Possible fields:

* `claim_conditions`
* `local_definitions`
* `profile_dependencies`
* `review_requirements`
* `downstream_decision_roles`
* `evidence_type_constraints`
* `handoff_conditions`
* `profile_limitations`
* `automation_guidance`

Boundary:

These fields may describe conditions, constraints, or dependencies, but they must not assert that claims are true, compliant, legally sufficient, audit-ready, safe, approved, or institutionally accepted.

Allowed:

* declaring required evidence types
* declaring local definitions
* declaring downstream decision roles
* declaring conditions under which a claim may be reviewed
* declaring unresolved dependencies

Not allowed:

* certifying a claim
* approving a system
* determining compliance
* granting authority
* resolving legal meaning
* asserting model safety
* replacing institutional review

Potential checker behavior:

* verify field shape
* verify local references
* verify role enum values
* verify no claim/non-claim/unknown overlap
* verify no restricted authority leakage
* emit deterministic normalized output

Deferred:

* semantic interpretation of conditions
* legal or compliance evaluation
* external artifact verification

### 4.2 Workspace Manifest Resolution

Candidate status: `CANDIDATE_WITH_BOUNDARY_RISK`

Purpose:

Allow a placement profile to reference a local workspace manifest that lists declared artifacts by path, hash, or identifier.

This would let Fork verify that a declared evidence reference exists in a local manifest.

Boundary:

Manifest resolution may verify local declaration and hash consistency. It must not verify that the artifact’s content proves the claim it is associated with.

Allowed:

* checking that a declared evidence ID appears in a manifest
* checking that a declared file path exists inside a local test workspace
* checking that a declared hash matches a local file
* reporting missing artifacts
* reporting hash mismatch

Not allowed:

* judging whether the artifact content is sufficient
* interpreting model cards, policies, audit reports, contracts, or certifications
* asserting evidentiary admissibility
* asserting compliance sufficiency
* resolving external URLs or live network resources
* authenticating an external organization

Possible output states:

* `MANIFEST_REFERENCE_PRESENT`
* `MANIFEST_REFERENCE_MISSING`
* `MANIFEST_HASH_MATCH`
* `MANIFEST_HASH_MISMATCH`
* `MANIFEST_NOT_CHECKED`

Risk:

This candidate sits close to external artifact verification. It must remain local, deterministic, and bounded.

### 4.3 Cross-Record Reference Validation

Candidate status: `CANDIDATE_WITH_SCOPE_RISK`

Purpose:

Allow multiple local placement profiles to be checked for declared handoff consistency.

This would support structural validation of whether one profile’s declared output is referenced by another profile’s declared input.

Boundary:

Cross-record validation may check local reference consistency among profiles. It must not infer inherited authority or claim transitivity.

Allowed:

* checking that referenced local profile IDs exist
* checking that referenced output IDs exist
* checking that handoff direction is structurally valid
* checking that no profile silently inherits another profile’s claim
* checking that downstream claims restate their own evidence basis

Not allowed:

* validating the truth of upstream claims
* approving downstream claim inheritance
* declaring a chain compliant
* determining institutional authority
* resolving graph semantics beyond local structure

Core rule:

> A downstream placement profile must not inherit an upstream claim merely because a handoff exists.

Potential checker behavior:

* compile a local set of profiles
* detect missing profile references
* detect missing output references
* detect direct self-reference
* detect simple local cycles
* emit graph-reference warnings or failures

Deferred:

* full topological compilation
* policy evaluation
* institutional review
* external identity resolution

### 4.4 DAG / Topological Placement Compilation

Candidate status: `DEFERRED_CANDIDATE`

Purpose:

Compile multiple placement profiles into a local directed graph showing how governance systems are structurally positioned relative to one another.

Boundary:

The graph would describe declared structural placement. It would not prove system correctness, compliance, safety, or authority.

Allowed:

* building a local graph from declared profiles
* identifying nodes and directed handoffs
* detecting cycles
* detecting missing nodes
* detecting disconnected components
* detecting unresolved unknowns in a graph
* emitting graph-level structural findings

Not allowed:

* declaring a graph compliant
* declaring a governance chain safe
* treating upstream claims as inherited by downstream systems
* performing external discovery
* making regulatory or legal conclusions

Potential output states:

* `GRAPH_WELL_FORMED`
* `GRAPH_HAS_MISSING_REFERENCE`
* `GRAPH_HAS_CYCLE`
* `GRAPH_HAS_ACTIVE_UNKNOWN`
* `GRAPH_NOT_CHECKED`

Reason for deferral:

Graph compilation is useful but can easily cause category drift. It must remain structurally descriptive and must not become workflow orchestration, runtime enforcement, compliance scoring, or institutional approval.

### 4.5 Output Hashing and Verification Receipts

Candidate status: `CANDIDATE`

Purpose:

Add optional hashing over normalized checker outputs so results can be independently compared across environments.

Boundary:

A hash proves that the normalized output has not changed. It does not prove that the underlying system is safe, compliant, legally sufficient, or correct.

Allowed:

* computing SHA-256 over normalized outputs
* emitting a result hash
* emitting a verification receipt
* supporting recomputation across clean machines
* comparing declared and recomputed normalized-output hashes

Not allowed:

* using the hash as proof of claim truth
* using the hash as proof of legal admissibility
* using the hash as proof of compliance
* using the hash as institutional approval

Potential output fields:

* `normalized_output_sha256`
* `checker_version`
* `schema_version`
* `record_id`
* `computed_at_utc`
* `hash_algorithm`
* `non_claims`

Design concern:

Environment-specific fields must remain outside normalized hash scope unless explicitly included by design.

### 4.6 Downstream Automation Guidance

Candidate status: `CANDIDATE`

Purpose:

Document how CI/CD systems, local scripts, and review workflows should treat checker exit codes and output states.

Boundary:

Automation guidance may describe safe handling of checker outputs. It must not turn Fork into a deployment authority.

Allowed:

* documenting that `PASS = 0`
* documenting that `FAIL = 1`
* documenting that `INDETERMINATE = 2`
* recommending that `INDETERMINATE` not be treated as success
* showing examples of safe CI gating
* showing how to archive normalized outputs

Not allowed:

* requiring deployment blocking
* claiming production governance readiness
* claiming regulatory sufficiency
* replacing human review
* asserting organizational approval

Potential guidance:

* `PASS` means structurally and boundary consistent.
* `FAIL` means structural or boundary violation.
* `INDETERMINATE` means structurally interpretable but unresolved unknowns remain.
* Downstream systems must not collapse `INDETERMINATE` into `PASS`.

## 5. Proposed v0.2 Sequence

v0.2 should proceed in planning gates rather than implementation-first commits.

Recommended sequence:

1. Create this v0.2 planning document.
2. Submit planning document for external review.
3. Select at most one v0.2 module for first implementation.
4. Generate a v0.2 design artifact for the selected module.
5. Generate schema or fixture updates only after design review.
6. Generate checker changes only after schema/fixture review.
7. Run full regression across:

   * Placement Profile v0.1 checker
   * Placement Profile v0.1.1 checker hardening
   * AI Governance Mapping Record checker line
   * semantic alignment review
8. Freeze v0.2 only if all prior boundaries remain intact.

Preferred order if implementation proceeds:

1. Output hashing and verification receipts
2. Downstream automation guidance
3. Optional schema extensions
4. Workspace manifest resolution
5. Cross-record reference validation
6. DAG/topological placement compilation

Reason:

The first two candidates strengthen recomputability and operational clarity without immediately expanding into graph or external-artifact territory.

## 6. v0.2 Admission Gates

A v0.2 candidate must pass all gates before implementation.

### Gate 1: Boundary Preservation

The candidate must preserve all existing non-claims.

The candidate must not validate:

* semantic truth
* legal sufficiency
* compliance sufficiency
* audit sufficiency
* model safety
* runtime behavior
* external artifact existence unless explicitly scoped as local manifest resolution
* cross-record graph validity unless explicitly scoped as structural graph validation
* institutional authority

### Gate 2: Non-Transitivity

The candidate must not allow a downstream profile to inherit an upstream claim without explicit declaration.

Every claim must remain locally declared and locally bounded.

### Gate 3: Determinism

The candidate must produce deterministic outputs or clearly distinguish environment-specific fields from normalized fields.

### Gate 4: Reviewability

The candidate must produce outputs that a reviewer can inspect without relying on hidden runtime state.

### Gate 5: Clean-Machine Recomputability

Where possible, the candidate must support recomputation on a clean machine using committed fixtures, schemas, tools, and outputs.

### Gate 6: No Runtime Dependency

The candidate must not create a runtime dependency on live workflow execution.

Fork must remain out-of-band and evidence-oriented.

### Gate 7: No Institutional Substitution

The candidate must not replace legal, compliance, audit, safety, risk, or institutional review.

## 7. Candidate v0.2 Output States

Potential v0.2 output states should remain explicit and bounded.

Current states:

* `PASS`
* `FAIL`
* `INDETERMINATE`

Possible future states for specific modules:

* `NOT_CHECKED`
* `REFERENCE_MISSING`
* `HASH_MISMATCH`
* `GRAPH_HAS_CYCLE`
* `MANIFEST_MISSING`
* `PROFILE_REFERENCE_MISSING`

Any new status must state what was checked and what was not checked.

No status may imply:

* legal approval
* compliance certification
* audit sufficiency
* model safety
* institutional authority
* production readiness

## 8. v0.2 Non-Claims

A future v0.2 must preserve these non-claims:

Fork does not validate semantic truth.

Fork does not validate legal sufficiency.

Fork does not validate compliance sufficiency.

Fork does not validate audit sufficiency.

Fork does not validate model safety.

Fork does not enforce runtime behavior.

Fork does not approve systems.

Fork does not grant institutional authority.

Fork does not certify governance systems.

Fork does not guarantee source completeness.

Fork does not determine whether evidence is legally admissible.

Fork does not determine whether a workflow decision was correct.

Fork does not determine whether an organization satisfied its regulatory obligations.

Fork does not infer claim inheritance across handoffs.

Fork does not treat graph connectivity as governance sufficiency.

## 9. v0.2 Risks

### 9.1 Scope Creep into Runtime Enforcement

Risk:

Workspace or graph validation could be mistaken for runtime orchestration.

Mitigation:

Keep v0.2 local, deterministic, and out-of-band.

### 9.2 Scope Creep into Compliance Claims

Risk:

A profile graph or manifest check could be misread as compliance validation.

Mitigation:

Every output must preserve explicit non-claims.

### 9.3 Semantic Validation Drift

Risk:

Restricted-claim hardening could drift from lexical checks into semantic or NLP-based judgment.

Mitigation:

Keep restricted-claim detection deterministic and lexical unless a future design explicitly introduces a separate, bounded semantic-review artifact.

### 9.4 Graph Authority Inflation

Risk:

A graph of governance profiles could be mistaken for proof that the whole governance chain is valid.

Mitigation:

Graph outputs must describe structural relationships only.

### 9.5 External Artifact Trust Confusion

Risk:

Manifest resolution could be mistaken for external artifact authentication.

Mitigation:

Limit v0.2 manifest resolution to local declared files and hashes unless a separate trust model is designed.

## 10. Recommended Immediate Next Step

Do not implement v0.2 yet.

The immediate next step is external review of this planning document.

Review questions:

1. Which v0.2 candidate preserves Fork’s evidence-boundary posture most cleanly?
2. Which candidate creates the highest risk of authority drift?
3. Should v0.2 start with output hashing and verification receipts rather than graph or manifest work?
4. Should workspace manifest resolution be deferred until after output hashing?
5. Should cross-record validation and DAG compilation be postponed to v0.3?
6. Does the planning document sufficiently distinguish structural validation from semantic, legal, compliance, audit, and runtime authority?
7. Are any candidate modules too broad for v0.2?

## 11. Planning Recommendation

Recommended v0.2 planning posture:

* Prefer recomputability improvements before topology expansion.
* Prefer output hashing before workspace manifest resolution.
* Prefer manifest resolution before cross-record validation.
* Prefer cross-record validation before DAG compilation.
* Defer DAG compilation unless there is a clear evidence-boundary reason to include it.
* Treat every v0.2 module as opt-in, local, deterministic, and bounded.

Recommended first v0.2 candidate:

`Output Hashing and Verification Receipts`

Reason:

This strengthens Fork’s core recomputable-evidence posture without immediately expanding into external artifact resolution, cross-record graph validation, or workflow governance authority.

Recommended deferred candidates:

* `Workspace Manifest Resolution`
* `Cross-Record Reference Validation`
* `DAG / Topological Placement Compilation`

Reason:

These are valuable but have higher authority-drift risk.

## 12. Status

This document is a planning artifact.

No v0.2 feature is approved by this document.

No schema change is approved by this document.

No checker change is approved by this document.

No runtime behavior is introduced by this document.

No legal, compliance, audit, safety, or institutional authority is claimed by this document.

Final status:

`V0_2_PLANNING_ONLY_NOT_IMPLEMENTED`
