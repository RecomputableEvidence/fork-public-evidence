# Relational Graph Verifier v0.3 Release Notes

## Status

Release note: `RGV_v0_3_RELEASE_NOTES`

Base required tags:

- `claim-boundary-contract-v0.2.2`
- `claim-consumption-events-v0.2.2`
- `cbc-cce-v0.2.2-final-precision-hardening`
- `cbc-cce-v0.2.2-enforcement-repair`

## Summary

RGV v0.3 adds stateless graph verification over supplied CBC / CCE bundles.

The verifier accepts a bounded graph bundle containing local CBC and CCE records, validates each record against its schema, applies relational checks across the bundle, detects cycles, distinguishes local and external pointers, and emits a verification result with explicit non-claims.

## Added artifacts

- `docs/STATELESS_RELATIONAL_GRAPH_VERIFIER_v0_3.md`
- `schemas/relational_graph_bundle_v0_3.schema.json`
- `examples/relational_graph_bundle_v0_3/local_expansion_graph_bundle.json`
- `examples/relational_graph_bundle_v0_3/external_pointer_graph_bundle.json`
- `examples/relational_graph_bundle_v0_3/unresolved_pointer_graph_bundle.json`
- `tools/check_relational_graph_v0_3.py`
- `tests/test_relational_graph_verifier_v0_3.py`

## Core design decision

The verifier is stateless by default.

It verifies the bundle it is given. It does not rely on a stateful database, external registry, network lookup, or vendor runtime.

External and unresolved references are preserved as explicit verification states rather than silently treated as validated graph nodes.

## Scope

RGV v0.3 verifies graph structure and relation integrity.

It does not assert source truth, legal sufficiency, compliance sufficiency, runtime enforcement, source completeness, complete historical lineage, or deployment readiness.

## Relationship to future work

A stateful registry profile may be added later for enterprise lineage lookup.

That profile should remain optional.

The recomputable public verifier should remain stateless, portable, and bounded.
