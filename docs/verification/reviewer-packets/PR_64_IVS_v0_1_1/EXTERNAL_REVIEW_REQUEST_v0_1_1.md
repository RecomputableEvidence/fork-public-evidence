# External Recomputation Request — Fork Independent Verification Surface v0.1.1

**Subject:** Pull request #64, `feat(verification): add Independent Verification Surface v0.1`

**Requested disposition:** independently reproduce, invalidate, or return an evidence gap for the v0.1.1 hardening package.

## Review boundary

This request does not ask the reviewer to approve a merge, certify security, endorse Fork, establish repository standing, authorize Cross-System Claim Handoff execution, or validate the substantive behavior of candidate executable code.

The requested review is limited to whether the exact package identified in the pull-request review request:

1. emits schema-valid receipts for supported, contradicted, and inconclusive outcomes;
2. binds the verifier release and exact component Git objects;
3. preserves and byte-exactly recomputes the v0.1 PR #63 plan and receipt;
4. reproduces from an empty disposable Git repository without candidate checkout or candidate-code execution;
5. applies the declared verdict precedence deterministically;
6. rejects duplicate keys and non-finite JSON values;
7. requires unique assertion identifiers;
8. attributes external observations in time and by method;
9. records Git object type and mode and rejects non-regular changed-path substitutions.

## Exact subject resolution

Use the full PR head commit stated in the public review-request comment. Do not use a branch name, mutable tag, local-only commit, or GitHub-generated test merge commit as the package identity.

The preserved candidate under examination remains:

- repository: `RecomputableEvidence/fork-public-evidence`
- base commit: `599d3e193d86a9661fbbec3213ae1921b4959f10`
- candidate commit: `82c34252d7b8d9e8957fb5a86500e12da6cf363a`
- expected merge base: `1102113556edfc54b43a328317961c4896d6dd6c`
- verifier release commit: `e366e44cb2059f5cb7243757b95fa8d44859b811`

## Fresh-repository command

From a machine with Git, Python 3.11+, and network access to GitHub, run the following command from any trusted checkout of the exact package commit:

```text
python tools/run_independent_verification_fresh_v0_1_1.py \
  --repository RecomputableEvidence/fork-public-evidence \
  --package-commit <EXACT_PR_HEAD_SHA> \
  --plan verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json \
  --expected-receipt receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json
```

The runner creates an empty disposable bare repository, fetches exact commits, checks out only the trusted package commit, executes no candidate code, and requires byte equality with the committed v0.1.1 receipt.

## Files requiring direct inspection

- `docs/verification/INDEPENDENT_VERIFICATION_SURFACE_AMENDMENT_v0_1_1.md`
- `policies/independent-verification/INDEPENDENT_VERIFICATION_POLICY_v0_1_1.json`
- `schemas/independent_verification_policy_v0_1_1.schema.json`
- `schemas/independent_verification_plan_v0_1_1.schema.json`
- `schemas/independent_verification_receipt_v0_1_1.schema.json`
- `tools/check_independent_verification_surface_v0_1_1.py`
- `tools/run_independent_verification_fresh_v0_1_1.py`
- `verification/plans/PR_63_CSH_AMENDMENT_v0_1_1.json`
- `receipts/independent-verification/PR_63_CSH_AMENDMENT_VERIFICATION_v0_1_1.json`
- `tests/test_independent_verification_surface_v0_1_1.py`

## Admissible reviewer outcomes

Record one of these outcomes without forcing a pass/fail judgment where evidence is unavailable:

- `REPRODUCED_WITHIN_DECLARED_SCOPE`
- `INVALIDATED_BY_INDEPENDENT_RECOMPUTATION`
- `INCONCLUSIVE_EVIDENCE_GAP`

A reproduced result means only that the declared package recomputed under the recorded conditions. It does not inherit the machine receipt's claims, grant authority, or convert evidence continuity into authority continuity.

## Attribution

Record reviewer identity, environment, commands, observations, and disposition in the accompanying worksheet or an equivalent separately attributable record. Do not edit the committed machine receipt to imply human attribution.
