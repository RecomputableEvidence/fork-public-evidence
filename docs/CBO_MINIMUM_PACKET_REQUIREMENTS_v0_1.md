# CBO Minimum Packet Requirements v0.1

## Status

Draft requirements profile.

This artifact defines the minimum exported continuity packet required for Fork-side structural continuity evaluation of one externally governed workload.

The profile is intended for sandboxed collaboration and pressure-testing. It does not declare integration, endorsement, compatibility, interoperability, approval, certification, compliance, safety, admissibility, authorization, or causal proof.

## Purpose

A CBO minimum packet is a bounded exported continuity object.

It represents an issuer-declared continuity path through an upstream execution or governance environment while preserving enough structure for a downstream evidentiary system to inspect continuity without entering the control path or inheriting upstream authority.

For the initial SC/Fork sandbox, the packet represents one SC-governed workload moving through:

1. admission decision;
2. invariant binding;
3. state transition;
4. execution event;
5. emitted artifact;
6. preservation reference;
7. recomputation reference;
8. downstream interpretation constraint.

## Canonical Boundary Line

The upstream issuer may claim that the packet represents an emitted continuity path through its declared environment.

Fork may preserve, recompute, compare, report, and identify structural continuity loss within the emitted evidence boundary.

Fork does not validate upstream governance authority, admissibility authority, authorization authority, runtime control authority, safety, compliance, truth, causal authority, or approval.

## Required Normalization

The first packet normalization preserves three rules:

1. Issuer invariants are treated as opaque issuer-declared references.
2. Ambiguous lifecycle strings such as `pending-or-present` are not allowed as status values.
3. Authority-transfer limits are machine-readable, not only prose.

## Opaque Invariant Rule

Fork may preserve references such as:

- `invariant://continuity`
- `invariant://causality`
- `invariant://consciousness`

Fork does not validate the meaning, correctness, governance authority, metaphysical status, or causal force of those invariants.

They are preserved as issuer-declared invariant references only.

## Minimum Required Fields

A valid CBO minimum packet includes:

- `profile_id`
- `cbo_version`
- `cbo_id`
- `packet_id`
- `issuer_system`
- `authority_domain`
- `stable_workload_id`
- `emitted_at`
- `continuity_chain`
- `integrity_metadata`
- `preservation_refs`
- `recomputation_refs`
- `boundary_semantics`
- `issuer_claims`
- `issuer_non_claims`
- `fork_permissions`
- `fork_restrictions`
- `downstream_constraints`
- `unresolved_or_excluded_refs`
- `expected_fork_evaluation`

## Boundary Semantics

The following values are required:

- `authority_transfer: false`
- `fork_validates_issuer_governance: false`
- `fork_validates_causality: false`
- `fork_participates_in_runtime_control: false`
- `fork_accepts_runtime_credentials: false`
- `fork_claims_control_path_authority: false`

## Fork-Side Evaluation

Fork may evaluate whether:

- required continuity references are present;
- identifier continuity is preserved;
- declared claims and non-claims remain visible;
- issuer authority does not transfer to Fork;
- ambiguous status values are absent;
- unresolved or excluded references remain explicit;
- the packet preserves a structurally traceable declared continuity identity.

Fork does not evaluate whether:

- SC governance was correct;
- the workload should have been admitted;
- invariants were substantively valid;
- execution was safe;
- the workflow was compliant;
- the packet proves causality;
- downstream interpretation is institutionally sufficient.

## Failure Modes

A CBO minimum packet is boundary-invalid if:

- it transfers authority to Fork;
- it asks Fork to validate issuer governance;
- it asks Fork to validate causality;
- it places Fork in the runtime control path;
- it uses ambiguous status values such as `pending-or-present`;
- it drops issuer non-claims;
- it omits downstream do-not-infer constraints;
- it hides unresolved or excluded references.

## Design Principle

The packet should expose continuity without transferring authority.

The first test is not whether Fork accepts SC governance conclusions.

The first test is whether a declared continuity identity remains structurally traceable across evidence-state transformations without mutating into a stronger claim.
