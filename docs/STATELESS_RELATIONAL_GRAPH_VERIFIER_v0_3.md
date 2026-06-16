# Stateless Relational Graph Verifier v0.3

## Status

Version: `RGV_v0_3`

The Stateless Relational Graph Verifier is the v0.3 verifier for bounded Fork graph bundles.

It verifies a supplied bundle of CBC and CCE records without a database, external registry lookup, network call, runtime service, or historical state.

## Critical warning for enterprise integrators

The Stateless Relational Graph Verifier is a structural verifier for supplied evidentiary graph bundles.

It is not a compliance gatekeeper, runtime policy engine, deployment-approval system, legal authority, or truth arbiter.

A `PASS` result means graph topology and relational structure passed within the stated verification scope. It does not mean the underlying claims are true, compliant, safe, legally sufficient, production-ready, or historically complete.

`CLOSED_LOCAL` means self-contained local topology: every checked edge in the supplied bundle terminates at a node supplied in that same bundle. It does not mean complete historical truth, complete workflow history, or complete institutional record coverage.

JSON Schema validation is necessary but not sufficient for v0.3 conformance. A conformant implementation must also apply the relational checks enforced by the reference verifier.

CLI exit code `0` means the supplied bundle passed structural / relational verification within its emitted `graph_closure_state`. It is not a deployment gate, compliance approval, legal signoff, or runtime authorization. Callers must inspect the JSON result, including `graph_closure_state`, `warnings`, `external_pointers`, `unresolved_pointers`, and `result_non_claims`.

## Purpose

v0.3 moves Fork from individual claim-boundary and claim-consumption artifacts into bounded graph verification.

The verifier checks whether the supplied CBC / CCE graph is structurally coherent.

It records what it can resolve locally, what remains external, what remains unresolved, and whether any local graph relationships are cyclic, contradictory, or malformed.

## Non-claims

The v0.3 verifier does not assert:

- source truth;
- legal, regulatory, contractual, or compliance sufficiency;
- deployment readiness;
- source completeness;
- complete historical lineage;
- runtime enforcement or authorization;
- validation of external pointers not supplied inside the local bundle.

## Stateless-by-default rule

v0.3 is stateless by default.

The verifier only inspects the bundle it is given.

It does not require a database to verify its core claim.

A stateful registry may be added later as an enterprise profile, but the public verifier remains portable, bounded, and independently inspectable.

## Graph closure states

The verifier emits:

- `CLOSED_LOCAL` â€” all checked graph relationships resolved inside the supplied bundle;
- `OPEN_EXTERNAL_POINTERS` â€” the bundle is structurally valid, but at least one reference points outside the local bundle;
- `OPEN_UNRESOLVED_POINTERS` â€” at least one required reference is explicitly unresolved;
- `INVALID` â€” the graph contains schema errors, relational errors, cycles, missing local references, or other invalid states.

## Closure-state interpretation table

| Graph closure state | Result state | Interpretation |
| --- | --- | --- |
| `CLOSED_LOCAL` | `PASS` | Self-contained local topology. All checked graph edges resolve inside the supplied bundle. This is not a claim of complete history, truth, safety, compliance, deployment readiness, or legal sufficiency. |
| `OPEN_EXTERNAL_POINTERS` | `PASS` | The supplied bundle is structurally valid, but at least one pointer is external. External artifacts are recorded as references only and are not locally inspected by RGV. |
| `OPEN_UNRESOLVED_POINTERS` | `INDETERMINATE` | The supplied bundle is structurally coherent, but one or more explicitly unresolved boundary horizons prevent local graph closure. |
| `INVALID` | `FAIL` | The supplied bundle is structurally broken, contradictory, cyclic, missing required local references, or otherwise invalid. |

## Result states

The verifier emits:

- `PASS` â€” the supplied bundle is structurally and relationally valid within its stated closure state;
- `INDETERMINATE` â€” the supplied bundle is structurally valid but contains unresolved pointers that prevent local graph closure;
- `FAIL` â€” the supplied bundle violates schema, relation, edge, non-claim, or graph-cycle rules.

## Relationship to CBC / CCE v0.2.2

CBC records claim-boundary nodes.

CCE records claim-consumption edges.

RGV v0.3 verifies the supplied local graph of those nodes and edges.

It does not convert graph structure into truth, compliance, legal sufficiency, runtime enforcement, or deployment readiness.
