# CSH-AMEND-003 - Instrumentation Workflow Lineage Repair v0.1.2

## Status

Local candidate pending remote CI.

## Finding

The live integration workflow at `.github/workflows/fork-proof-surface-integration.yml` no longer matched the byte identity recorded by `docs/experiments/cross-system-claim-handoff-v0.1/amendments/CSH-AMEND-002/INSTRUMENTATION_FREEZE_v0_1_1.json`.

- Frozen SHA-256: `7a1fbc7b3e97bf0946e018b5be6613f5d8329238d5347cf444abe28e5aaae166`
- Observed SHA-256: `bfbde899d4c710e761b7070390b69a68c355fd48fe058fd0c3b12d49bf4c4400`
- Historical source commit: `54b04dc8d685c79abeceb9d79ddbcf6493ee1a71`
- Detection context: pull request #58

The divergence occurred because later Meta-Evidence integration steps were added to a workflow path that the v0.1.1 instrumentation freeze treated as immutable.

## Corrective action

1. Preserve the divergent workflow bytes at `docs/experiments/cross-system-claim-handoff-v0.1/amendments/CSH-AMEND-003/OBSERVED_DIVERGENT_FORK_PROOF_SURFACE_INTEGRATION.yml`.
2. Preserve the historically frozen bytes at `docs/experiments/cross-system-claim-handoff-v0.1/amendments/CSH-AMEND-003/FROZEN_FORK_PROOF_SURFACE_INTEGRATION_v0_1_1.yml`.
3. Restore `.github/workflows/fork-proof-surface-integration.yml` to the frozen SHA-256 without rewriting Git history.
4. Retain Meta-Evidence verification in the separate workflow `.github/workflows/fork-meta-evidence-v0-1.yml`.
5. Add `.github/workflows/fork-admission-gate.yml` with the stable check name `fork-admission-gate` and no path filters.

## Boundary effect

This repair affects instrumentation workflow lineage only. It does not modify the semantic freeze, corpus, hypothesis, prompts, original attempts, classification authority, or network-execution prohibition.

## Non-claims

- Local verification is not remote clean-machine verification.
- Restoring frozen workflow bytes does not erase or conform the recorded divergent state.
- Passing structural checks does not establish truth, compliance, safety, approval, authority, or production readiness.