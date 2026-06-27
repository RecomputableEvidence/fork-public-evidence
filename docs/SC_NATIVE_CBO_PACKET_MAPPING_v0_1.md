# SC Native CBO Packet Mapping v0.1

## Status

Draft adapter profile.

This artifact defines a sandboxed mapping from an SC-native continuity packet into Fork's normalized CBO minimum packet envelope.

It does not declare integration, compatibility, interoperability, endorsement, approval, certification, safety, compliance, admissibility, authorization, runtime participation, or causal proof.

## Purpose

The mapping preserves two separate objects:

1. the issuer-native SC packet, preserving how SC emits continuity evidence;
2. the Fork-normalized CBO minimum packet, preserving the boundary semantics required for out-of-band structural evaluation.

Fork should not require SC to rewrite its internal representation in order to be inspectable.

Fork only needs a stable mapping from SC-native fields into the CBO minimum packet fields that Fork can structurally evaluate.

## Mapping Sequence

The intended sequence is:

1. SC emits one native continuity packet from one governed workload.
2. Fork maps the SC-native packet into the normalized CBO minimum packet envelope.
3. Fork runs the CBO minimum packet checker.
4. Fork reports whether the declared continuity identity remains structurally traceable without inheriting SC governance authority.

## Boundary Rule

The SC-native packet remains issuer-native.

The normalized CBO packet is a Fork-side evaluation envelope.

The adapter does not validate SC governance, SC invariants, runtime execution, causality, safety, compliance, authorization, approval, admissibility, or truth.

## Opaque Invariant Rule

SC-declared invariant references are mapped as opaque issuer-declared references.

Fork may preserve that SC emitted references such as:

- `invariant://continuity`
- `invariant://causality`
- `invariant://consciousness`

Fork does not validate the meaning, correctness, authority, causal force, or semantic truth of those invariant references.

## Field Mapping

| SC-native field | Fork-normalized CBO field |
|---|---|
| `cbo_version` | `cbo_version` |
| `cbo_id` | `cbo_id` |
| generated adapter packet id | `packet_id` |
| `issuer_system` | `issuer_system` |
| `authority_domain` | `authority_domain` |
| `stable_workload_id` | `stable_workload_id` |
| `emitted_at` | `emitted_at` |
| `admission_decision_ref` | `continuity_chain.admission_decision_ref` |
| `sc_declared_invariant_refs` | `continuity_chain.invariant_binding_refs` |
| `state_transition_refs` | `continuity_chain.state_transition_refs` |
| `execution_event_refs` | `continuity_chain.execution_event_refs` |
| `emitted_artifact_refs` | `continuity_chain.emitted_artifact_refs` |
| `digest_seal_anchor_metadata` | `integrity_metadata` |
| `preservation_refs` | `preservation_refs` |
| `recomputation_refs` | `recomputation_refs` |
| `authority_boundary` | `boundary_semantics` |
| `sc_claims` | `issuer_claims` |
| `sc_non_claims` | `issuer_non_claims` |
| `downstream_do_not_infer` | `downstream_constraints.do_not_infer` plus canonical do-not-infer tokens |
| `unresolved_or_excluded_refs` | `unresolved_or_excluded_refs` |

## Status Normalization

SC-native lifecycle statuses may be lower-case.

The adapter normalizes:

- `pending` to `PENDING`
- `present` to `PRESENT`
- `absent` to `ABSENT`
- `unresolved` to `UNRESOLVED`

Ambiguous lifecycle values such as `pending-or-present` are rejected.

## Required Authority Boundary

A valid SC-native packet must preserve:

- `authority_transfer: false`
- `fork_validates_sc_governance: false`
- `fork_validates_causality: false`
- `fork_participates_in_runtime_control: false`

The normalized Fork envelope additionally asserts:

- `fork_accepts_runtime_credentials: false`
- `fork_claims_control_path_authority: false`
- `issuer_invariant_refs_are_opaque_to_fork: true`

## Design Principle

The adapter maps emitted continuity evidence.

It does not convert SC governance conclusions into Fork conclusions.

It lets Fork evaluate whether a declared continuity identity remains structurally traceable while preserving the rule that authority does not transfer across the packet boundary.
