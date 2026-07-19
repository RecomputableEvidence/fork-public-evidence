# Fork Independent Verification Surface Amendment v0.1.1

**Status:** proposed for external recomputation; no merge, repository-standing, security-certification, endorsement, or experiment-execution authority.

## Amendment purpose

This amendment repairs the review blockers identified in Independent Verification Surface v0.1 without rewriting or erasing the original v0.1 plan, receipt, dependency-scope example, or machine result. The original PR #63 receipt remains preserved as historical machine evidence. v0.1.1 adds a hardening layer that independently binds and recomputes that lineage.

## Repaired boundaries

1. **Schema-valid inconclusive receipts.** Every ordinary verification outcome uses one closed receipt schema. Evidence unavailable at the time of recomputation is represented explicitly through availability fields rather than omitted or emitted through an undeclared structure.
2. **Verifier provenance.** The plan binds a fixed verifier source commit and exact Git blob identities for the hardened checker, policy, schemas, legacy checker, claim-admission checker, and fresh-repository runner. The running checker bytes must match the declared checker blob.
3. **Fresh-repository recomputation.** A dedicated runner begins from an empty disposable Git repository, fetches the exact package, verifier, base, and candidate commits, checks out only the trusted package commit, executes no candidate code, and compares the regenerated receipt byte-for-byte with the committed receipt.
4. **Frozen verdict precedence.** `INCONCLUSIVE_EVIDENCE_GAP` precedes `INVALIDATED_BY_RECOMPUTATION`, which precedes `VERIFIED_WITHIN_DECLARED_SCOPE`. Mixed evidence preserves contradiction and inconclusive counts even when the top-level result is inconclusive.
5. **Observation attribution.** Every external observation records its observation time, observer, method, subject coordinates, and `OBSERVATION_ONLY` authority.
6. **Strict JSON.** Duplicate keys, non-finite numbers, unknown properties, invalid UTF-8, and unsafe paths are rejected. Canonical and receipt serialization prohibit NaN and infinities.
7. **Assertion identity and Git modes.** Assertion identifiers must be unique. Every changed candidate path is inspected as a Git tree entry and must be a regular blob with mode `100644` or `100755`; symlinks and non-blob substitutions are not silently treated as equal files.

## Preserved v0.1 evidence

The v0.1.1 checker does not replace the v0.1 PR #63 plan or receipt. It verifies their exact Git blob identities, strictly parses both records, reruns the v0.1 checker against the preserved plan, and requires the emitted v0.1 receipt to be byte-identical to the committed v0.1 receipt before the v0.1.1 result can be supported.

## External reviewer procedure

The reviewer should:

1. identify themselves separately from the machine receipt;
2. begin from the exact package commit identified in the review request;
3. run the fresh-repository command without reusing an existing Fork clone;
4. inspect the v0.1.1 plan, policy, checker, schemas, and fresh runner;
5. record whether the receipt reproduced byte-for-byte;
6. record any contradiction or evidence gap without editing the machine receipt;
7. avoid treating a successful recomputation as merge approval, security certification, endorsement, or experiment authority.

## Result boundary

A v0.1.1 result can support, contradict, or leave inconclusive only the exact declared verification surface. It does not establish the semantic correctness of candidate executable behavior, authorize PR #63, publish the CSH release anchor, validate provider credentials, or start Pair-001.
