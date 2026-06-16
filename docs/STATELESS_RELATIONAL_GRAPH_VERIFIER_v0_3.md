# Stateless Relational Graph Verifier v0.3

## Status

Version: `RGV_v0_3`

The Stateless Relational Graph Verifier is the v0.3 verifier for bounded Fork graph bundles.

It verifies a supplied bundle of CBC and CCE records without a database, external registry lookup, network call, runtime service, or historical state.

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
