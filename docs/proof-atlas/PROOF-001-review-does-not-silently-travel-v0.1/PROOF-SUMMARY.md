# PROOF-001 Generated Summary

> Generated from the existing v0.2 longitudinal checker by
> `tools/run_proof_001_review_does_not_silently_travel_v0_1.py`.

## Exact replay

- Start: `bac40d9bdbd7f6b4927a676fef8def70756ad9d5`
- Closure: `f955834681d2f2ee257276acbf68afde0ae0e69d`
- Replay: `LONGITUDINAL_STATE_REPRODUCED`
- Diff: `LONGITUDINAL_DIFF_REPRODUCED`

## Changed and preserved dimensions

| Dimension | T1 standing | Effect | T2 standing |
|---|---|---|---|
| `artifact_state` | `EXACT_ARTIFACT_COORDINATE_AT_REPLAY_START` | **CHANGED** | `EXACT_ARTIFACT_COORDINATE_AT_REPLAY_CLOSURE` |
| `verification_state` | `SOURCE_HEAD_CONFORMANCE_DECLARED_IN_SOURCE_MATERIAL_NOT_YET_EXTERIORLY_RECOMPUTED_IN_THIS_LINEAGE` | **CHANGED** | `PREDECESSOR_HEAD_INDEPENDENTLY_RECOMPUTED_CURRENT_HEAD_NOT_SEPARATELY_RECOMPUTED` |
| `review_state` | `NO_EXTERIOR_REVIEW_RECEIPT_PRESENT_AT_REPLAY_START` | **CHANGED** | `BOUNDED_EXTERIOR_REVIEW_PRESERVED` |
| `admission_state` | `NONE` | **PRESERVED** | `NONE` |
| `authority_state` | `NONE` | **PRESERVED** | `NONE` |
| `execution_state` | `STRUCTURALLY_READY_EXECUTION_BLOCKED` | **PRESERVED** | `STRUCTURALLY_READY_EXECUTION_BLOCKED` |
| `unresolved_state` | `OPEN` | **CHANGED** | `OPEN` |
| `temporal_closure` | `CLOSED_AT_EXACT_COMMIT` | **CHANGED** | `CLOSED_AT_EXACT_COMMIT` |

Changed dimensions: `artifact_state`, `review_state`, `temporal_closure`, `unresolved_state`, `verification_state`

Preserved dimensions: `admission_state`, `authority_state`, `execution_state`

## Adversarial demonstration

- Case: `FLR-ADV-003`
- Mutation: `PROMOTE_REVIEW_TO_CURRENT_HEAD`
- Result: `CURRENT_HEAD_REVIEW_STALE`
- Disposition: mutation rejected; review remains exact-head bound.

## Public-route observation

- Result: `PUBLIC_ROUTE_STALE`
- Effect: routing gap detected and preserved; not repaired by this candidate.

## Boundary

The replay interval has admission, authority, and execution effects `NONE`.
Later admission of the replay lineage does not rewrite the earlier interval.
This summary does not establish truth, correctness, causality, endorsement,
compliance, legal sufficiency, safety, production readiness, present reliance,
institutional authority, or execution permission.
