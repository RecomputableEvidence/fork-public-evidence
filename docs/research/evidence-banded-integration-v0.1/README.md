# Fork Evidence-Banded Repository Integration — v0.1 Candidate

Status: `INTEGRATION_ARCHITECTURE_CANDIDATE_NO_ADMISSION_EFFECT`

This surface records a repository-reentry observation and a proposed evidence-banded integration architecture for Fork. It does **not** alter the native standing of any referenced artifact. It does not admit a candidate, merge an open pull request, promote a proof, authorize execution, authorize pilot or production use, or modify `main` or the governed preservation branch.

## Why this surface exists

Fork has accumulated artifacts with materially different native standings: admitted repository primitives, governed specifications, qualified candidate proofs, active empirical research, known repair obligations, and historical/preservation evidence. Presenting those surfaces without an explicit integration treatment risks accidental semantic inheritance from adjacency.

The band model therefore provides an **integration/adopter-routing axis**, not a replacement governance ontology.

```text
INTEGRATION_BAND
  != NATIVE_STANDING

REPOSITORY_PRESENCE
  != ADMISSION

REVIEW_OR_RECOMPUTATION
  != STANDING_PROMOTION
```

## Files

- `FORK_REPOSITORY_REENTRY_RECOMPUTATION_2026_08_21_v0_1.json` — exact repository observations used for this construction.
- `FORK_EVIDENCE_BANDED_REPOSITORY_INTEGRATION_ARCHITECTURE_v0_1_CANDIDATE.md` — band semantics, gates, and routing rules.
- `EVIDENCE_BAND_REGISTRY_v0_1.json` — initial surface-by-surface treatment registry.
- `OPEN_CANDIDATE_ROUTING_2026_08_21_v0_1.json` — observed open-PR routing snapshot.
- `NO_ADMISSION_OR_STANDING_EFFECT_v0_1.json` — explicit non-effects.

## Construction basis

The mutable governed ref was freshly compared to the previously reviewed coordinate before construction. At observation time:

- `main = fd93d051235ec43bee925878bc916d09179b3c90`
- `preservation/clean-continuance-v0.1 = 0c60bbdd2b7c50e1758968464485fac0dfbf008d`
- preservation tree = `94e68d68547222506fbf67665db4d75b8649eac9`
- the governed preservation ref was byte/tree-identical to the reviewed `0c60bbdd...` coordinate.

This candidate must remain distinct from any later act that changes artifact standing.
