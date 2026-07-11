# Cross-System Claim Handoff v0.1 Method

## Sequence

1. Validate the repository proof-surface gate.
2. Complete the corpus, receiver, parameter, prompt, and schema freeze.
3. Generate a release-anchor manifest.
4. Execute paired control and instrumented receiver runs.
5. Preserve exact inputs, raw outputs, metadata, timestamps, errors, and digests.
6. Normalize receiver outputs into the classifier input contract without deleting raw output.
7. Run deterministic event-level classification.
8. Preserve human coding and disagreements separately.
9. Complete all planned units or terminal dispositions.
10. File bounded synthesis.
11. Obtain independent classification recomputation.
12. Begin delayed replay checkpoints.
13. Admit optimization only after the gate passes.

## Pairing rule

For a given scenario, receiver class, and replicate:

- source artifact is identical;
- workflow instruction is identical;
- receiver identity/version and parameters are identical;
- access path is identical;
- only the explicit handoff-state artifact differs.

## Normalization boundary

Natural-language receiver output may require a normalized representation for deterministic classification.

The normalized representation must:

- retain a hash and path to raw output;
- identify who or what performed normalization;
- preserve uncertainty;
- avoid silently inserting missing non-claims, authority references, or boundary identifiers;
- be independently inspectable.

Normalization is not classification.

## Result interpretation

A lower observed event rate under `H = 1` is evidence consistent with the bounded hypothesis under the frozen design. It is not universal proof, certification, compliance evidence, legal sufficiency, production approval, or authority.
