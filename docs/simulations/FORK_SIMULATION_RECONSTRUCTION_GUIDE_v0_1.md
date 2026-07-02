# Fork Simulation Reconstruction Guide v0.1

## Purpose

This guide defines how a reviewer reconstructs simulated handoffs in the Fork Governance Simulation Proof Surface.

The goal is to determine whether a later reviewer can inspect what crossed the boundary, what did not cross, what was inferred downstream, and what remains outside Fork's authority.

## Reconstruction Questions

For every scenario, answer:

1. What artifact crossed the boundary?
2. What claims crossed with it?
3. What non-claims crossed with it?
4. What evidence references were preserved?
5. What authority or policy context was recorded?
6. What remained unresolved?
7. What did the downstream system infer?
8. Did the downstream inference preserve, narrow, expand, or exceed the recorded boundary?
9. Did any expansion include new authority or evidence?
10. What remains outside Fork's authority?

## Reconstruction Table

| Question | Reviewer Answer | Evidence Reference | Confidence |
|---|---|---|---|
| What crossed the boundary? | TBD | TBD | TBD |
| What did not cross? | TBD | TBD | TBD |
| What was inferred downstream? | TBD | TBD | TBD |
| Was claim scope preserved? | TBD | TBD | TBD |
| Were non-claims preserved? | TBD | TBD | TBD |
| Was authority inferred? | TBD | TBD | TBD |
| Was policy reference laundered? | TBD | TBD | TBD |
| Was unresolved state preserved? | TBD | TBD | TBD |
| What requires revalidation? | TBD | TBD | TBD |

## Reconstruction Outcomes

Use one of the following outcomes:

| Outcome | Meaning |
|---|---|
| RECONSTRUCTABLE_BOUNDARY | Reviewer can reconstruct the handoff boundary |
| PARTIALLY_RECONSTRUCTABLE_BOUNDARY | Reviewer can reconstruct some but not all boundary state |
| UNSUPPORTED_INHERITANCE_EXPOSED | Reviewer can identify downstream overreach |
| AUTHORITY_LEAKAGE_EXPOSED | Reviewer can identify implied authority transfer |
| POLICY_LAUNDERING_EXPOSED | Reviewer can identify policy reference treated as approval or compliance |
| NON_CLAIM_LOSS_EXPOSED | Reviewer can identify missing or dropped non-claims |
| NOT_RECONSTRUCTABLE | Reviewer cannot reconstruct the handoff boundary from available records |

## Non-Claims

Reconstruction does not determine whether the underlying decision was correct.

Reconstruction does not establish legal, compliance, procurement, audit, operational, or institutional sufficiency.

Reconstruction does not convert Fork into an authority layer.