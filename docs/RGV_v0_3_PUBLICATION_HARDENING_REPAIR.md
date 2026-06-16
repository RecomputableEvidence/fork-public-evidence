# RGV v0.3 Publication Hardening Repair

## Status

Patch note: `RGV_v0_3_PUBLICATION_HARDENING_REPAIR`

Base patch:

- `rgv-v0.3-publication-hardening`

## Purpose

This repair closes two narrow publication-readiness issues found during reassessment.

It does not change RGV's architecture.

It preserves the stateless verifier while ensuring that publication-hardening semantics travel with emitted verifier output and that unresolved-pointer examples do not contain locally-resolved wording.

## Repairs

1. Corrected `examples/relational_graph_bundle_v0_3/unresolved_pointer_graph_bundle.json` so the unresolved expansion target is not described as locally resolved.

2. Added `RGV_RESULT_NON_CLAIM_EXIT_CODE_APPROVAL` to emitted verifier `result_non_claims`.

   This makes the exit-code warning travel with every JSON verifier result instead of appearing only in CLI help.

3. Tightened "or equivalent behavior" wording to "documented equivalent behavior that enforces the same required relational checks."

4. Added a regression test proving emitted results contain the exit-code / non-approval non-claim.

## Non-claims

This repair does not make RGV a compliance engine, legal authority, runtime control layer, deployment approval system, source-truth verifier, or complete-history verifier.

RGV remains stateless, bounded, local-bundle graph verification.
