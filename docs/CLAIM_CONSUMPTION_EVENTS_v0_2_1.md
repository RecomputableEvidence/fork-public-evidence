# Claim Consumption Events v0.2.1

## Status

Version: `CCE_v0_2_1`

CCE v0.2.1 is a precision patch over CCE v0.2. It hardens edge naming, expansion pointer semantics, source non-claim matching, and local versus external reference validation.

## Core boundary

A CCE records a downstream consumption edge.

It does not become the expanded claim node.

A CCE may record that an upstream claim boundary was preserved, narrowed, or explicitly expanded. When expansion occurs, the CCE records the vector of expansion and terminates at a reference to a separate CBC.

## Canonical expansion rule

A CCE never holds an expanded claim. It records the vector of expansion and terminates at the explicit reference pointer of the newly generated CBC.

## Expansion pointer resolution

CCE v0.2.1 records one of four pointer-resolution states:

- `LOCAL_RESOLVED` -- the referenced downstream CBC exists in the analyzed bundle and validates against the CBC schema.
- `EXTERNAL_POINTER` -- the referenced CBC is external; the pointer is recorded, but the verifier does not claim the CBC was inspected.
- `NOT_RESOLVED` -- the pointer was recorded but not resolved; the unresolved state must be explicitly recorded.
- `NOT_APPLICABLE` -- no new claim boundary is referenced because the CCE is preserved or narrowed rather than expanded.

This keeps Fork substrate-neutral and avoids pretending that an external pointer was inspected when it was only referenced.

## Edge naming

CCE v0.2.1 avoids naming expansion examples as if the CCE is the resulting expanded claim. The expansion example is named:

`edge_eval_benchmark_expansion.json`

The edge records consumption and points to the new CBC. It does not contain the new claim as its own authority.

## Source non-claim matching

When the source CBC is locally resolvable, CCE v0.2.1 relational tests verify that the consumed claim's `source_non_claim_ids` match the source CBC's non-claims.

## Relationship to Fork

Fork remains out-of-band evidence-boundary infrastructure.

CCE v0.2.1 does not enforce runtime behavior, certify compliance, approve deployment, establish source truth, or guarantee legal sufficiency.
